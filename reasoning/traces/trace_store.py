#!/usr/bin/env python3
"""
BlackRoad OS Reasoning Trace Storage

Persistent storage for reasoning chains and traces:
- JSON file-based storage for development
- SQLite for production
- In-memory caching for performance
- Query capabilities for analysis
"""

import json
import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Optional
from dataclasses import dataclass, asdict
from abc import ABC, abstractmethod


@dataclass
class TraceRecord:
    """A stored reasoning trace record."""
    trace_id: str
    chain_id: str
    agent_id: str
    domain: str
    tier: str
    phase: str
    input_hash: str
    output: dict
    confidence: float
    reasoning: str
    duration_ms: int
    timestamp: str
    metadata: dict


class TraceStore(ABC):
    """Abstract base for trace storage."""

    @abstractmethod
    def store_chain(self, chain: dict) -> str:
        """Store a complete reasoning chain."""
        pass

    @abstractmethod
    def store_step(self, chain_id: str, step: dict) -> str:
        """Store a single reasoning step."""
        pass

    @abstractmethod
    def get_chain(self, chain_id: str) -> Optional[dict]:
        """Retrieve a reasoning chain."""
        pass

    @abstractmethod
    def get_agent_chains(self, agent_id: str, limit: int = 100) -> list[dict]:
        """Get chains for an agent."""
        pass

    @abstractmethod
    def query_by_confidence(self, min_confidence: float, max_confidence: float) -> list[dict]:
        """Query chains by confidence range."""
        pass

    @abstractmethod
    def get_statistics(self) -> dict:
        """Get storage statistics."""
        pass


class JSONTraceStore(TraceStore):
    """JSON file-based trace storage for development."""

    def __init__(self, base_path: str = "./traces"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.chains_path = self.base_path / "chains"
        self.chains_path.mkdir(exist_ok=True)
        self.index_path = self.base_path / "index.json"
        self._load_index()

    def _load_index(self):
        """Load or create index."""
        if self.index_path.exists():
            with open(self.index_path) as f:
                self.index = json.load(f)
        else:
            self.index = {
                "chains": {},
                "by_agent": {},
                "by_domain": {},
                "statistics": {
                    "total_chains": 0,
                    "total_steps": 0,
                    "avg_confidence": 0.0,
                }
            }
            self._save_index()

    def _save_index(self):
        """Save index to disk."""
        with open(self.index_path, 'w') as f:
            json.dump(self.index, f, indent=2)

    def store_chain(self, chain: dict) -> str:
        """Store a complete reasoning chain."""
        chain_id = chain.get("chain_id")
        agent_id = chain.get("agent_id")

        # Save chain file
        chain_file = self.chains_path / f"{chain_id}.json"
        with open(chain_file, 'w') as f:
            json.dump(chain, f, indent=2)

        # Update index
        self.index["chains"][chain_id] = {
            "agent_id": agent_id,
            "mode": chain.get("mode"),
            "confidence": chain.get("overall_confidence"),
            "status": chain.get("status"),
            "timestamp": chain.get("started_at"),
            "step_count": len(chain.get("steps", [])),
        }

        # Update by_agent index
        if agent_id not in self.index["by_agent"]:
            self.index["by_agent"][agent_id] = []
        self.index["by_agent"][agent_id].append(chain_id)

        # Update statistics
        self.index["statistics"]["total_chains"] += 1
        self.index["statistics"]["total_steps"] += len(chain.get("steps", []))

        # Recalculate average confidence
        confidences = [c["confidence"] for c in self.index["chains"].values() if c.get("confidence")]
        if confidences:
            self.index["statistics"]["avg_confidence"] = sum(confidences) / len(confidences)

        self._save_index()
        return chain_id

    def store_step(self, chain_id: str, step: dict) -> str:
        """Store a single reasoning step (appends to chain)."""
        chain = self.get_chain(chain_id)
        if chain:
            chain["steps"].append(step)
            self.store_chain(chain)
        return chain_id

    def get_chain(self, chain_id: str) -> Optional[dict]:
        """Retrieve a reasoning chain."""
        chain_file = self.chains_path / f"{chain_id}.json"
        if chain_file.exists():
            with open(chain_file) as f:
                return json.load(f)
        return None

    def get_agent_chains(self, agent_id: str, limit: int = 100) -> list[dict]:
        """Get chains for an agent."""
        chain_ids = self.index["by_agent"].get(agent_id, [])[-limit:]
        return [self.get_chain(cid) for cid in chain_ids if self.get_chain(cid)]

    def query_by_confidence(self, min_confidence: float, max_confidence: float) -> list[dict]:
        """Query chains by confidence range."""
        matching = []
        for chain_id, info in self.index["chains"].items():
            conf = info.get("confidence", 0)
            if min_confidence <= conf <= max_confidence:
                chain = self.get_chain(chain_id)
                if chain:
                    matching.append(chain)
        return matching

    def get_statistics(self) -> dict:
        """Get storage statistics."""
        return self.index["statistics"]


class SQLiteTraceStore(TraceStore):
    """SQLite-based trace storage for production."""

    def __init__(self, db_path: str = "./traces.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS chains (
                chain_id TEXT PRIMARY KEY,
                agent_id TEXT NOT NULL,
                domain TEXT,
                tier TEXT,
                mode TEXT,
                overall_confidence REAL,
                status TEXT,
                started_at TEXT,
                completed_at TEXT,
                final_output TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS steps (
                step_id TEXT PRIMARY KEY,
                chain_id TEXT NOT NULL,
                phase TEXT NOT NULL,
                input_context TEXT,
                output TEXT,
                confidence REAL,
                reasoning TEXT,
                duration_ms INTEGER,
                timestamp TEXT,
                metadata TEXT,
                FOREIGN KEY (chain_id) REFERENCES chains(chain_id)
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chains_agent ON chains(agent_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_chains_confidence ON chains(overall_confidence)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_steps_chain ON steps(chain_id)
        """)

        conn.commit()
        conn.close()

    def store_chain(self, chain: dict) -> str:
        """Store a complete reasoning chain."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        chain_id = chain.get("chain_id")

        # Insert chain
        cursor.execute("""
            INSERT OR REPLACE INTO chains
            (chain_id, agent_id, domain, tier, mode, overall_confidence, status,
             started_at, completed_at, final_output)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            chain_id,
            chain.get("agent_id"),
            chain.get("domain"),
            chain.get("tier"),
            chain.get("mode"),
            chain.get("overall_confidence"),
            chain.get("status"),
            chain.get("started_at"),
            chain.get("completed_at"),
            json.dumps(chain.get("final_output")),
        ))

        # Insert steps
        for i, step in enumerate(chain.get("steps", [])):
            step_id = f"{chain_id}_{i}"
            cursor.execute("""
                INSERT OR REPLACE INTO steps
                (step_id, chain_id, phase, input_context, output, confidence,
                 reasoning, duration_ms, timestamp, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                step_id,
                chain_id,
                step.get("phase"),
                json.dumps(step.get("input")),
                json.dumps(step.get("output")),
                step.get("confidence"),
                step.get("reasoning"),
                step.get("duration_ms"),
                step.get("timestamp"),
                json.dumps(step.get("metadata", {})),
            ))

        conn.commit()
        conn.close()
        return chain_id

    def store_step(self, chain_id: str, step: dict) -> str:
        """Store a single reasoning step."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get next step index
        cursor.execute("SELECT COUNT(*) FROM steps WHERE chain_id = ?", (chain_id,))
        count = cursor.fetchone()[0]
        step_id = f"{chain_id}_{count}"

        cursor.execute("""
            INSERT INTO steps
            (step_id, chain_id, phase, input_context, output, confidence,
             reasoning, duration_ms, timestamp, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            step_id,
            chain_id,
            step.get("phase"),
            json.dumps(step.get("input")),
            json.dumps(step.get("output")),
            step.get("confidence"),
            step.get("reasoning"),
            step.get("duration_ms"),
            step.get("timestamp"),
            json.dumps(step.get("metadata", {})),
        ))

        conn.commit()
        conn.close()
        return step_id

    def get_chain(self, chain_id: str) -> Optional[dict]:
        """Retrieve a reasoning chain."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM chains WHERE chain_id = ?", (chain_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return None

        chain = {
            "chain_id": row[0],
            "agent_id": row[1],
            "domain": row[2],
            "tier": row[3],
            "mode": row[4],
            "overall_confidence": row[5],
            "status": row[6],
            "started_at": row[7],
            "completed_at": row[8],
            "final_output": json.loads(row[9]) if row[9] else None,
            "steps": [],
        }

        # Get steps
        cursor.execute(
            "SELECT * FROM steps WHERE chain_id = ? ORDER BY step_id",
            (chain_id,)
        )
        for step_row in cursor.fetchall():
            chain["steps"].append({
                "phase": step_row[2],
                "input": json.loads(step_row[3]) if step_row[3] else {},
                "output": json.loads(step_row[4]) if step_row[4] else None,
                "confidence": step_row[5],
                "reasoning": step_row[6],
                "duration_ms": step_row[7],
                "timestamp": step_row[8],
                "metadata": json.loads(step_row[9]) if step_row[9] else {},
            })

        conn.close()
        return chain

    def get_agent_chains(self, agent_id: str, limit: int = 100) -> list[dict]:
        """Get chains for an agent."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT chain_id FROM chains WHERE agent_id = ? ORDER BY started_at DESC LIMIT ?",
            (agent_id, limit)
        )
        chain_ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        return [self.get_chain(cid) for cid in chain_ids]

    def query_by_confidence(self, min_confidence: float, max_confidence: float) -> list[dict]:
        """Query chains by confidence range."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT chain_id FROM chains WHERE overall_confidence BETWEEN ? AND ?",
            (min_confidence, max_confidence)
        )
        chain_ids = [row[0] for row in cursor.fetchall()]
        conn.close()

        return [self.get_chain(cid) for cid in chain_ids]

    def get_statistics(self) -> dict:
        """Get storage statistics."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM chains")
        total_chains = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM steps")
        total_steps = cursor.fetchone()[0]

        cursor.execute("SELECT AVG(overall_confidence) FROM chains")
        avg_confidence = cursor.fetchone()[0] or 0.0

        cursor.execute("SELECT COUNT(DISTINCT agent_id) FROM chains")
        unique_agents = cursor.fetchone()[0]

        cursor.execute("""
            SELECT mode, COUNT(*) as cnt
            FROM chains
            GROUP BY mode
            ORDER BY cnt DESC
        """)
        mode_distribution = {row[0]: row[1] for row in cursor.fetchall()}

        conn.close()

        return {
            "total_chains": total_chains,
            "total_steps": total_steps,
            "avg_confidence": round(avg_confidence, 4),
            "unique_agents": unique_agents,
            "mode_distribution": mode_distribution,
            "avg_steps_per_chain": round(total_steps / total_chains, 2) if total_chains else 0,
        }


class InMemoryTraceStore(TraceStore):
    """In-memory trace storage for testing and caching."""

    def __init__(self, max_chains: int = 10000):
        self.chains = {}
        self.by_agent = {}
        self.max_chains = max_chains

    def store_chain(self, chain: dict) -> str:
        chain_id = chain.get("chain_id")
        agent_id = chain.get("agent_id")

        # Evict old chains if at capacity
        if len(self.chains) >= self.max_chains:
            oldest = next(iter(self.chains))
            del self.chains[oldest]

        self.chains[chain_id] = chain

        if agent_id not in self.by_agent:
            self.by_agent[agent_id] = []
        self.by_agent[agent_id].append(chain_id)

        return chain_id

    def store_step(self, chain_id: str, step: dict) -> str:
        if chain_id in self.chains:
            self.chains[chain_id]["steps"].append(step)
        return chain_id

    def get_chain(self, chain_id: str) -> Optional[dict]:
        return self.chains.get(chain_id)

    def get_agent_chains(self, agent_id: str, limit: int = 100) -> list[dict]:
        chain_ids = self.by_agent.get(agent_id, [])[-limit:]
        return [self.chains[cid] for cid in chain_ids if cid in self.chains]

    def query_by_confidence(self, min_confidence: float, max_confidence: float) -> list[dict]:
        return [
            chain for chain in self.chains.values()
            if min_confidence <= chain.get("overall_confidence", 0) <= max_confidence
        ]

    def get_statistics(self) -> dict:
        total_steps = sum(len(c.get("steps", [])) for c in self.chains.values())
        confidences = [c.get("overall_confidence", 0) for c in self.chains.values()]
        return {
            "total_chains": len(self.chains),
            "total_steps": total_steps,
            "avg_confidence": sum(confidences) / len(confidences) if confidences else 0,
            "unique_agents": len(self.by_agent),
        }


# Factory function
def create_trace_store(store_type: str = "sqlite", **kwargs) -> TraceStore:
    """Create a trace store of the specified type."""
    if store_type == "json":
        return JSONTraceStore(kwargs.get("base_path", "./traces"))
    elif store_type == "sqlite":
        return SQLiteTraceStore(kwargs.get("db_path", "./traces.db"))
    elif store_type == "memory":
        return InMemoryTraceStore(kwargs.get("max_chains", 10000))
    else:
        raise ValueError(f"Unknown store type: {store_type}")
