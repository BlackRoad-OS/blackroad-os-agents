# Repository Communication API

## Overview

The Repository Communication API enables automated communication between all BlackRoad OS repositories, agents, apps, and devices. It supports coordination of 30,000+ AI agents working collaboratively across the entire ecosystem.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Communication Hub                         │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Repository  │  │    Agent     │  │  External    │      │
│  │   Dispatch   │  │ Coordination │  │   Webhook    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────▼────────┐  ┌───────▼────────┐  ┌──────▼─────────┐
│  Repositories  │  │     Agents     │  │  Applications  │
│                │  │                │  │                │
│ • blackroad-   │  │ • Leadership   │  │ • Prism        │
│   os-agents    │  │ • Operational  │  │ • Archive      │
│ • blackroad-   │  │ • Supporting   │  │ • Web Apps     │
│   os-operator  │  │ • Utility      │  │                │
│ • blackroad-   │  │                │  │                │
│   os-core      │  │ (30k agents)   │  │                │
└────────────────┘  └────────────────┘  └────────────────┘
```

---

## Communication Channels

### 1. GitHub Repository Dispatch

**Purpose:** Send events between GitHub repositories

**Endpoint:** `POST /repos/{owner}/{repo}/dispatches`

**Authentication:** GitHub Token with `repo` scope

**Example:**

```bash
curl -X POST \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/repos/BlackRoad-OS/blackroad-os-operator/dispatches \
  -d '{
    "event_type": "cross-repo-sync",
    "client_payload": {
      "message_id": "msg-1234567890",
      "source_repo": "blackroad-os-agents",
      "message_type": "agent_sync",
      "timestamp": "2025-01-04T12:00:00Z"
    }
  }'
```

### 2. Agent Coordination WebSocket

**Purpose:** Real-time agent-to-agent communication

**Endpoint:** `wss://blackroad-agents-hub.io`

**Protocol:** WebSocket with JSON messages

**Example:**

```javascript
const ws = new WebSocket('wss://blackroad-agents-hub.io');

ws.on('open', () => {
  ws.send(JSON.stringify({
    type: 'agent_register',
    agent_id: 'claude',
    capabilities: ['architecture', 'system-design']
  }));
});

ws.on('message', (data) => {
  const message = JSON.parse(data);
  // Handle coordination messages
});
```

### 3. Message Queue

**Purpose:** Asynchronous task distribution

**Queue Name:** `agent-coordination-queue`

**Provider:** Compatible with RabbitMQ, AWS SQS, or similar

**Example:**

```python
import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters('blackroad-mq.io')
)
channel = connection.channel()

channel.queue_declare(queue='agent-coordination-queue')

message = {
    'task_id': 'task-12345',
    'agent_layer': 'operational',
    'action': 'deploy',
    'target': 'staging'
}

channel.basic_publish(
    exchange='',
    routing_key='agent-coordination-queue',
    body=json.dumps(message)
)
```

### 4. HTTP REST API

**Purpose:** Synchronous request/response communication

**Base URL:** `https://api.blackroad.io/agent-coordination`

**Authentication:** Bearer token

**Endpoints:**

```
POST   /v1/messages          # Send message to agent network
GET    /v1/agents            # List active agents
POST   /v1/agents/broadcast  # Broadcast to all agents
GET    /v1/health            # Health check
POST   /v1/sync              # Trigger cross-repo sync
```

---

## Message Format

### Standard Message Structure

```json
{
  "message_id": "msg-{timestamp}-{uuid}",
  "timestamp": "2025-01-04T12:00:00Z",
  "version": "1.0.0",
  "source": {
    "type": "repository|agent|application",
    "id": "blackroad-os-agents",
    "commit": "abc123def456",
    "actor": "github-actor-name"
  },
  "destination": {
    "type": "all|repository|agent|application",
    "targets": ["blackroad-os-operator", "claude"],
    "scope": "organization|global"
  },
  "message": {
    "type": "deployment|security_alert|agent_sync|system_update|health_check",
    "priority": "low|medium|high|critical",
    "payload": {
      // Message-specific data
    }
  },
  "metadata": {
    "requires_ack": true,
    "timeout": 300,
    "retry_count": 3
  }
}
```

---

## Message Types

### 1. Deployment Messages

**Type:** `deployment`

**Purpose:** Notify of deployment events

**Payload:**

```json
{
  "message": {
    "type": "deployment",
    "priority": "high",
    "payload": {
      "environment": "staging|production",
      "status": "started|completed|failed",
      "version": "v2.0.0",
      "services": ["api", "worker"],
      "rollback_available": true
    }
  }
}
```

### 2. Security Alerts

**Type:** `security_alert`

**Purpose:** Broadcast security issues

**Payload:**

```json
{
  "message": {
    "type": "security_alert",
    "priority": "critical",
    "payload": {
      "severity": "low|medium|high|critical",
      "vulnerability_id": "CVE-2025-12345",
      "affected_components": ["authentication"],
      "mitigation": "Update to v2.1.0",
      "action_required": true
    }
  }
}
```

### 3. Agent Sync

**Type:** `agent_sync`

**Purpose:** Synchronize agent states

**Payload:**

```json
{
  "message": {
    "type": "agent_sync",
    "priority": "medium",
    "payload": {
      "sync_type": "full|incremental",
      "agent_count": 30000,
      "registry_version": "v1.5.0",
      "changes": {
        "added": 150,
        "modified": 75,
        "removed": 5
      }
    }
  }
}
```

### 4. System Updates

**Type:** `system_update`

**Purpose:** Notify of system changes

**Payload:**

```json
{
  "message": {
    "type": "system_update",
    "priority": "medium",
    "payload": {
      "update_type": "feature|bugfix|security|breaking",
      "component": "agent-registry",
      "version": "v2.0.0",
      "breaking_changes": false,
      "migration_required": false
    }
  }
}
```

### 5. Health Checks

**Type:** `health_check`

**Purpose:** Verify system connectivity

**Payload:**

```json
{
  "message": {
    "type": "health_check",
    "priority": "low",
    "payload": {
      "status": "healthy|degraded|unhealthy",
      "components": {
        "api": "healthy",
        "database": "healthy",
        "cache": "degraded"
      },
      "uptime": 86400,
      "last_check": "2025-01-04T12:00:00Z"
    }
  }
}
```

---

## Triggering Communication

### Via GitHub Actions Workflow

```bash
gh workflow run cross-repo-communication.yml \
  -f message_type=deployment \
  -f target_repos=all \
  -f message_payload='{"status":"success","environment":"production"}'
```

### Via API

```bash
curl -X POST https://api.blackroad.io/agent-coordination/v1/messages \
  -H "Authorization: Bearer $API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "source": {
      "type": "repository",
      "id": "blackroad-os-agents"
    },
    "destination": {
      "type": "all",
      "scope": "organization"
    },
    "message": {
      "type": "agent_sync",
      "priority": "high",
      "payload": {
        "sync_type": "full",
        "agent_count": 30000
      }
    }
  }'
```

### Via GitHub CLI

```bash
gh api repos/BlackRoad-OS/blackroad-os-operator/dispatches \
  -f event_type='cross-repo-message' \
  -F 'client_payload={"message_type":"deployment","status":"success"}'
```

---

## Agent Coordination Protocol

### Agent Registration

Agents must register with the coordination hub:

```json
POST /v1/agents/register
{
  "agent_id": "claude",
  "display_name": "Claude // The Architect",
  "agent_type": "leadership",
  "capabilities": ["architecture", "system-design", "code-review"],
  "status": "active",
  "version": "v1.0.0",
  "endpoints": {
    "webhook": "https://agent.blackroad.io/claude/webhook",
    "health": "https://agent.blackroad.io/claude/health"
  }
}
```

### Task Assignment

Coordinator assigns tasks to agents:

```json
POST /v1/tasks/assign
{
  "task_id": "task-12345",
  "assigned_to": "claude",
  "priority": "high",
  "task_type": "code-review",
  "deadline": "2025-01-04T15:00:00Z",
  "payload": {
    "repository": "blackroad-os-agents",
    "pr_number": 123
  }
}
```

### Status Updates

Agents report status:

```json
POST /v1/agents/status
{
  "agent_id": "claude",
  "status": "busy|idle|error",
  "current_task": "task-12345",
  "progress": 75,
  "estimated_completion": "2025-01-04T14:30:00Z"
}
```

---

## Scalability Features

### Load Balancing

- **Round-robin:** Distribute tasks evenly
- **Capability-based:** Route to specialized agents
- **Load-aware:** Consider agent workload
- **Geographic:** Minimize latency

### Rate Limiting

```
Agent Layer    │ Requests/Min │ Burst
──────────────┼──────────────┼───────
Leadership     │ 1000         │ 2000
Operational    │ 5000         │ 10000
Supporting     │ 10000        │ 20000
Utility        │ 20000        │ 40000
```

### Retry Logic

- **Exponential backoff:** 1s, 2s, 4s, 8s, 16s
- **Max retries:** 5 attempts
- **Circuit breaker:** Disable after repeated failures
- **Fallback:** Route to alternative agents

---

## Monitoring and Logging

### Key Metrics

- **Message throughput:** Messages per second
- **Agent utilization:** Active/idle/error states
- **Response latency:** P50, P95, P99
- **Error rate:** Failed messages percentage
- **Queue depth:** Pending messages

### Logging Format

```json
{
  "timestamp": "2025-01-04T12:00:00Z",
  "level": "info|warn|error",
  "service": "coordination-hub",
  "message_id": "msg-12345",
  "source": "blackroad-os-agents",
  "destination": "blackroad-os-operator",
  "duration_ms": 150,
  "status": "success|failure"
}
```

---

## Security Considerations

### Authentication

- **GitHub Apps:** For repository dispatch
- **Bearer tokens:** For API access
- **Webhook secrets:** For webhook validation
- **mTLS:** For WebSocket connections

### Authorization

- **Agent permissions:** Role-based access control
- **Repository access:** Org-level or repo-level
- **Rate limiting:** Prevent abuse
- **Audit logging:** Track all communications

### Data Protection

- **Encryption in transit:** TLS 1.3
- **Encryption at rest:** AES-256
- **PII handling:** Minimize and protect
- **Secrets management:** Never in messages

---

## Error Handling

### Common Errors

| Code | Error | Solution |
|------|-------|----------|
| 401 | Unauthorized | Check authentication token |
| 403 | Forbidden | Verify permissions |
| 404 | Not Found | Check target exists |
| 429 | Rate Limited | Implement backoff |
| 500 | Server Error | Retry with backoff |
| 503 | Service Unavailable | Use fallback or queue |

### Error Response Format

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded for agent layer",
    "details": {
      "limit": 1000,
      "window": "60s",
      "retry_after": 30
    },
    "request_id": "req-12345"
  }
}
```

---

## Examples

### Example 1: Broadcast Deployment

```bash
# Trigger deployment notification to all repos
gh workflow run cross-repo-communication.yml \
  -f message_type=deployment \
  -f target_repos=all \
  -f message_payload='{
    "environment": "production",
    "status": "completed",
    "version": "v2.0.0"
  }'
```

### Example 2: Agent Sync

```javascript
// Sync agent registry across repositories
const message = {
  message_type: 'agent_sync',
  payload: {
    sync_type: 'incremental',
    changes: {
      added: ['agent-new-1', 'agent-new-2'],
      modified: ['agent-existing-1'],
      removed: []
    }
  }
};

await fetch('https://api.blackroad.io/agent-coordination/v1/messages', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.API_TOKEN}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(message)
});
```

### Example 3: Health Check

```python
import requests

# Check health across all repositories
response = requests.post(
    'https://api.blackroad.io/agent-coordination/v1/messages',
    headers={
        'Authorization': f'Bearer {os.environ["API_TOKEN"]}',
        'Content-Type': 'application/json'
    },
    json={
        'message_type': 'health_check',
        'target_repos': 'all',
        'payload': {
            'check_depth': 'full',
            'include_agents': True
        }
    }
)
```

---

## Integration with Other Systems

### Prism Console

- **Dashboard:** Real-time communication view
- **Agent Status:** Monitor all 30k agents
- **Message Log:** Searchable history
- **Alerts:** Critical message notifications

### Archive

- **Event Storage:** Long-term message retention
- **Audit Trail:** Compliance and investigation
- **Analytics:** Communication patterns
- **Reporting:** Daily/weekly summaries

### Operator

- **Workflow Triggers:** Start workflows from messages
- **Task Distribution:** Assign work to agents
- **Status Updates:** Report progress
- **Error Handling:** Retry failed operations

---

## Troubleshooting

### Message Not Received

1. Check authentication credentials
2. Verify target exists and is accessible
3. Review rate limits
4. Check network connectivity
5. Examine error logs

### Agent Not Responding

1. Verify agent registration
2. Check agent health endpoint
3. Review agent workload
4. Examine agent logs
5. Try alternative agent

### High Latency

1. Check network conditions
2. Review load balancer metrics
3. Examine queue depth
4. Consider geographic routing
5. Optimize message payload size

---

## Best Practices

1. **Keep messages small:** Optimize payload size
2. **Use async where possible:** Don't block on responses
3. **Implement retries:** Handle transient failures
4. **Log everything:** Enable debugging
5. **Monitor metrics:** Track performance
6. **Use priorities:** Critical messages first
7. **Batch when appropriate:** Reduce overhead
8. **Version messages:** Support migration
9. **Validate input:** Prevent malformed messages
10. **Test thoroughly:** End-to-end validation

---

## Future Enhancements

- 🔄 **GraphQL subscriptions:** Real-time updates
- 🌐 **Global federation:** Multi-region support
- 📊 **Advanced analytics:** ML-powered insights
- 🤖 **Self-healing:** Automatic recovery
- 🔐 **Zero-trust security:** Enhanced authentication
- ⚡ **Edge computing:** Reduced latency
- 📱 **Mobile SDK:** Native app support

---

**Document Version:** 1.0.0  
**Last Updated:** 2025-01-04  
**Maintained By:** BlackRoad OS DevOps & Integration Team
