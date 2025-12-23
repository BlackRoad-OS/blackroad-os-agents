"""
Worker Runner

Pulls jobs from Redis Streams and dispatches to the appropriate executor.
"""

import asyncio
import logging
import os
import signal
from dataclasses import dataclass
from typing import Any, Optional
import asyncpg
import aioredis
import json

from worker.executor import AgentExecutor, ExecutionResult

logger = logging.getLogger(__name__)


@dataclass
class WorkerConfig:
    """Worker configuration."""
    pool_name: str
    queue_name: str
    consumer_group: str = "workers"
    consumer_name: Optional[str] = None
    batch_size: int = 10
    block_ms: int = 5000
    max_retries: int = 3
    claim_min_idle_ms: int = 60000  # Claim stuck messages after 60s


class Worker:
    """
    Agent worker that processes jobs from Redis Streams.

    Flow:
    1. Connect to Redis and Postgres
    2. Create consumer group if needed
    3. Poll for messages from the stream
    4. For each message:
       - Fetch job and agent details from DB
       - Load agent's effective_manifest
       - Execute agent logic
       - Update job status
       - Log to Beacon and Archive
    5. Acknowledge processed messages
    """

    def __init__(
        self,
        db: asyncpg.Pool,
        redis: aioredis.Redis,
        config: WorkerConfig,
        executor: Optional[AgentExecutor] = None,
    ):
        self.db = db
        self.redis = redis
        self.config = config
        self.executor = executor or AgentExecutor()
        self._running = False
        self._consumer_name = config.consumer_name or f"worker-{os.getpid()}"

    async def start(self):
        """Start the worker loop."""
        self._running = True
        logger.info(
            f"Starting worker {self._consumer_name} on pool {self.config.pool_name}, "
            f"queue {self.config.queue_name}"
        )

        # Ensure consumer group exists
        await self._ensure_consumer_group()

        # Set up signal handlers
        for sig in (signal.SIGTERM, signal.SIGINT):
            asyncio.get_event_loop().add_signal_handler(
                sig, lambda: asyncio.create_task(self.stop())
            )

        while self._running:
            try:
                await self._process_batch()
            except Exception as e:
                logger.error(f"Error processing batch: {e}", exc_info=True)
                await asyncio.sleep(1)

    async def stop(self):
        """Stop the worker gracefully."""
        logger.info(f"Stopping worker {self._consumer_name}")
        self._running = False

    async def _ensure_consumer_group(self):
        """Create consumer group if it doesn't exist."""
        try:
            await self.redis.xgroup_create(
                self.config.queue_name,
                self.config.consumer_group,
                id="0",
                mkstream=True,
            )
            logger.info(f"Created consumer group {self.config.consumer_group}")
        except aioredis.ResponseError as e:
            if "BUSYGROUP" not in str(e):
                raise

    async def _process_batch(self):
        """Process a batch of messages from the stream."""
        # First, claim any stuck messages
        await self._claim_stuck_messages()

        # Read new messages
        messages = await self.redis.xreadgroup(
            groupname=self.config.consumer_group,
            consumername=self._consumer_name,
            streams={self.config.queue_name: ">"},
            count=self.config.batch_size,
            block=self.config.block_ms,
        )

        if not messages:
            return

        for stream_name, stream_messages in messages:
            for message_id, data in stream_messages:
                await self._process_message(message_id, data)

    async def _claim_stuck_messages(self):
        """Claim messages that have been pending too long."""
        try:
            pending = await self.redis.xpending_range(
                self.config.queue_name,
                self.config.consumer_group,
                min="-",
                max="+",
                count=self.config.batch_size,
            )

            for entry in pending:
                if entry["time_since_delivered"] > self.config.claim_min_idle_ms:
                    await self.redis.xclaim(
                        self.config.queue_name,
                        self.config.consumer_group,
                        self._consumer_name,
                        min_idle_time=self.config.claim_min_idle_ms,
                        message_ids=[entry["message_id"]],
                    )
                    logger.info(f"Claimed stuck message {entry['message_id']}")
        except Exception as e:
            logger.warning(f"Error claiming stuck messages: {e}")

    async def _process_message(self, message_id: str, data: dict[str, Any]):
        """Process a single message."""
        job_id = data.get("job_id")
        if not job_id:
            logger.warning(f"Message {message_id} missing job_id")
            await self._ack_message(message_id)
            return

        logger.info(f"Processing job {job_id}")

        try:
            # Fetch job from database
            job = await self._fetch_job(job_id)
            if not job:
                logger.warning(f"Job {job_id} not found")
                await self._ack_message(message_id)
                return

            # Fetch agent
            agent = await self._fetch_agent(job["agent_id"], job["org_id"])
            if not agent:
                logger.warning(f"Agent {job['agent_id']} not found")
                await self._fail_job(job_id, "Agent not found")
                await self._ack_message(message_id)
                return

            # Check agent status
            if agent["status"] != "active":
                logger.warning(f"Agent {agent['name']} is not active ({agent['status']})")
                await self._fail_job(job_id, f"Agent is {agent['status']}")
                await self._ack_message(message_id)
                return

            # Mark job as running
            await self._start_job(job_id)

            # Execute the agent
            result = await self.executor.execute(
                manifest=agent["effective_manifest"],
                input=job["input"],
                context={
                    "job_id": str(job_id),
                    "agent_id": str(job["agent_id"]),
                    "org_id": str(job["org_id"]),
                    "trace_id": job["trace_id"],
                },
            )

            # Update job status
            if result.success:
                await self._complete_job(job_id, result.output)
            else:
                await self._fail_job(job_id, result.error or "Unknown error")

            # Log to RoadChain
            await self._log_to_roadchain(job, agent, result)

        except Exception as e:
            logger.error(f"Error processing job {job_id}: {e}", exc_info=True)
            await self._fail_job(job_id, str(e))
        finally:
            await self._ack_message(message_id)

    async def _fetch_job(self, job_id: str) -> Optional[dict[str, Any]]:
        """Fetch job from database."""
        row = await self.db.fetchrow(
            """
            SELECT id, org_id, agent_id, trace_id, status, input, retry_count, max_retries
            FROM jobs
            WHERE id = $1
            """,
            job_id,
        )
        return dict(row) if row else None

    async def _fetch_agent(self, agent_id: str, org_id: str) -> Optional[dict[str, Any]]:
        """Fetch agent from database."""
        row = await self.db.fetchrow(
            """
            SELECT id, ps_sha_id, name, runtime_type, status, effective_manifest
            FROM agents
            WHERE id = $1 AND org_id = $2
            """,
            agent_id,
            org_id,
        )
        if row:
            result = dict(row)
            # Parse JSONB field
            if isinstance(result["effective_manifest"], str):
                result["effective_manifest"] = json.loads(result["effective_manifest"])
            return result
        return None

    async def _start_job(self, job_id: str):
        """Mark job as started."""
        await self.db.execute(
            """
            UPDATE jobs
            SET status = 'running', started_at = now()
            WHERE id = $1
            """,
            job_id,
        )
        await self.db.execute(
            """
            INSERT INTO job_events (job_id, event_type, payload)
            VALUES ($1, 'started', '{}')
            """,
            job_id,
        )

    async def _complete_job(self, job_id: str, output: dict[str, Any]):
        """Mark job as completed."""
        await self.db.execute(
            """
            UPDATE jobs
            SET status = 'succeeded', output = $2, finished_at = now()
            WHERE id = $1
            """,
            job_id,
            json.dumps(output),
        )
        await self.db.execute(
            """
            INSERT INTO job_events (job_id, event_type, payload)
            VALUES ($1, 'completed', $2)
            """,
            job_id,
            json.dumps({"output": output}),
        )
        # Update agent's last_run_at
        await self.db.execute(
            """
            UPDATE agents
            SET last_run_at = now()
            WHERE id = (SELECT agent_id FROM jobs WHERE id = $1)
            """,
            job_id,
        )

    async def _fail_job(self, job_id: str, error: str):
        """Mark job as failed."""
        await self.db.execute(
            """
            UPDATE jobs
            SET status = 'failed', error = $2, finished_at = now()
            WHERE id = $1
            """,
            job_id,
            error,
        )
        await self.db.execute(
            """
            INSERT INTO job_events (job_id, event_type, payload)
            VALUES ($1, 'failed', $2)
            """,
            job_id,
            json.dumps({"error": error}),
        )

    async def _log_to_roadchain(
        self,
        job: dict[str, Any],
        agent: dict[str, Any],
        result: ExecutionResult,
    ):
        """Log execution to RoadChain audit trail."""
        await self.db.execute(
            """
            INSERT INTO roadchain (org_id, entity_type, entity_id, action, actor_type, actor_id, payload, ps_sha_id)
            VALUES ($1, 'job', $2, 'executed', 'agent', $3, $4, $5)
            """,
            job["org_id"],
            job["id"],
            job["agent_id"],
            json.dumps({
                "success": result.success,
                "duration_ms": result.duration_ms,
                "error": result.error,
            }),
            agent["ps_sha_id"],
        )

    async def _ack_message(self, message_id: str):
        """Acknowledge a processed message."""
        await self.redis.xack(
            self.config.queue_name,
            self.config.consumer_group,
            message_id,
        )


async def create_worker(
    pool_name: str,
    queue_name: str,
    database_url: str,
    redis_url: str,
) -> Worker:
    """Factory function to create a worker with connections."""
    db = await asyncpg.create_pool(database_url)
    redis = await aioredis.from_url(redis_url)

    config = WorkerConfig(
        pool_name=pool_name,
        queue_name=queue_name,
    )

    return Worker(db=db, redis=redis, config=config)
