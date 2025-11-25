# 🤖🧬 blackroad-os-agents

**Agent Registry & Brain** – identities, roles, capabilities, and wiring for the BlackRoad OS agent swarm.

---

## 🎯 Mission

Be the **source of truth** for agents in BlackRoad OS:
- Define who they are and what they do
- Specify what they're allowed to touch
- Define agent types, capabilities, and guardrails
- Enable `core`, `operator`, `prism-console`, and Packs to understand agent identities
- Make it easy to add 1 agent or 10,000 agents without chaos

---

## 🏗️ What We Own (✅)

### 🧬 Agent Identities
- Canonical list of agents + classes (e.g., "Cadillac-Operator", "Prism-Sentry", "Finance-Recon", "Legal-Helper") 📋
- Metadata for each agent:
  - Name / ID
  - Description / persona
  - Home repo/pack
  - Capabilities + scopes
  - Risk level (low / medium / high)

### 🤖 Capabilities & Roles
- Capability definitions (read-only, suggest-only, execute-with-approval, etc.) 🧠
- Mappings: which agents can invoke which workflows / services / Packs ⚙️
- Guardrails and disallowed zones (e.g., "never touch prod finance without explicit approval") 🚫💰

### 📓 Config & Schemas
- Schemas for agent config files (JSON Schema) 🧬
- Standard fields for:
  - Input/output formats
  - Logging preferences
  - Escalation paths
  - Associated dashboards / views

### 📡 Integration Glue
- How agents surface in:
  - `blackroad-os-prism-console` agent views 🕹️
  - `blackroad-os-operator` workflows 🤖⚙️
  - `blackroad-os-archive` (agent action logs) 🧾
- Hooks for Packs (Finance, Legal, DevOps, Education, Creator, etc.) to register their own agents 💼

---

## 🚫 What We Don't Own

| Area | Owner |
|------|-------|
| 🚫 Concrete job/workflow implementation | `blackroad-os-operator` ⚙️ |
| 🚫 Live UI representation | `blackroad-os-web`, `-prism-console` 🖥️🕹️ |
| 🚫 Core domain logic | `blackroad-os-core` 🧠 |
| 🚫 Infra-as-code | `blackroad-os-infra` ☁️ |
| 🚫 System docs | `blackroad-os-docs` 📚 |
| 🚫 Brand visuals | `blackroad-os-brand` 🎨 |

---

## 📁 Repository Structure

```
blackroad-os-agents/
├── README.md                 # This file
├── registry/
│   ├── agents.json           # 📋 Canonical agent roster
│   └── packs.yml             # 📦 Pack definitions
├── schemas/
│   ├── agent.schema.json     # 🧬 JSON Schema for agents
│   └── pack.schema.json      # 📦 JSON Schema for packs
├── capabilities/
│   └── definitions.yml       # 🧠 Capability level definitions
└── guardrails/
    └── high-risk-zones.yml   # 🚫 High-risk zone definitions
```

---

## 🧭 Capability Levels

| Capability | Emoji | Description | Risk |
|------------|-------|-------------|------|
| `read-only` | 👀 | Can observe but never modify | Low |
| `suggest-only` | 💡 | Can propose but not execute | Low |
| `execute-with-approval` | ✋ | Can execute after explicit approval | Medium |
| `execute-autonomous` | ⚡ | Can execute independently within guardrails | Medium |
| `admin` | 👑 | Full administrative access (HIGH RISK) | High |

---

## ⚠️ Risk Levels

| Level | Description | Requirements |
|-------|-------------|--------------|
| **Low** | Safe operations, minimal impact | Standard logging |
| **Medium** | Operations that could affect system state | Audit trail, defined escalation path |
| **High** | Operations affecting money, infra, identity, or compliance | **Explicit approval required**, strong guardrails, full audit |

### 🚫 High-Risk Zones

These zones require explicit permissions and strong guardrails:

- 💰 **zone.finance.prod** – Production finance systems
- ☁️ **zone.infra.prod** – Production infrastructure
- 🪪 **zone.identity** – Identity & authentication
- ⚖️ **zone.legal** – Legal & compliance
- 🔐 **zone.secrets** – Secrets & credentials (NO AGENT ACCESS)

---

## 📋 Registering a New Agent

Each agent definition should answer:

1. **What am I?** (persona, purpose, risk level)
2. **What can I do?** (capabilities, allowed workflows, environments)
3. **How are my actions monitored & escalated?** (where logs go, who gets alerts)

### Example Agent Definition

```json
{
  "id": "agent.example.helper",
  "display_name": "Example Helper",
  "pack_id": "pack.example",
  "role": "Assists with example tasks",
  "persona": "🤖 A helpful agent that assists with example workflows.",
  "risk_level": "low",
  "capabilities": ["read-only", "suggest-only"],
  "skills": ["task_a", "task_b"],
  "allowed_workflows": ["workflow.example.run"],
  "disallowed_zones": ["zone.finance.prod", "zone.identity", "zone.secrets"],
  "repos": ["blackroad-os-pack-example"],
  "environments": ["staging", "prod"],
  "permissions": {
    "github": "read",
    "railway": "none"
  },
  "escalation_path": "example-team",
  "logging": {
    "level": "info",
    "archive": true,
    "alert_channels": ["slack.example"]
  },
  "dashboard_views": ["prism.example.dashboard"],
  "status": "active",
  "requires_approval": false
}
```

### High-Risk Agent Requirements

For agents with `risk_level: "high"`:

```json
{
  "risk_level": "high",
  "requires_approval": true,
  "escalation_path": "team-name → executive",
  "disallowed_zones": ["zone.secrets"],
  "high_risk_marker": "// HIGH-RISK AGENT – STRONG GUARDRAILS REQUIRED"
}
```

---

## 📦 Registering Pack Agents

Packs can register their own agents by:

1. Adding agent definitions to `registry/agents.json`
2. Referencing the pack ID in `pack_id` field
3. Following the schema in `schemas/agent.schema.json`

---

## 📡 Integration Points

### 🕹️ Prism Console (`blackroad-os-prism-console`)

Agents surface in Prism Console via `dashboard_views`:

```json
"dashboard_views": ["prism.agents.overview", "prism.agents.my-agent"]
```

### ⚙️ Operator (`blackroad-os-operator`)

Agents invoke workflows via `allowed_workflows`:

```json
"allowed_workflows": ["workflow.deploy.staging", "workflow.deploy.prod"]
```

### 🧾 Archive (`blackroad-os-archive`)

Agent actions are logged when `logging.archive: true`:

```json
"logging": {
  "level": "info",
  "archive": true,
  "alert_channels": ["slack.alerts"]
}
```

---

## 🔐 Safety & Compliance

### This repo is **permissions-critical**:

- 🔑 Treat capability changes as high-sensitivity events
- 🧾 Changes to high-risk agents (finance, legal, infra, identity) must be auditable and tagged
- ⚠️ **No secrets or live tokens** – only IDs, scopes, and metadata

### For agents that impact:
- 💰 Money
- ☁️ Prod infra
- 🪪 Identity/auth
- ⚖️ Compliance/regulatory flows

Mark clearly:
```
// HIGH-RISK AGENT – STRONG GUARDRAILS REQUIRED
```

---

## 🧪 Testing & Validation

### Schema Validation
- ✅ Required fields present
- ✅ Types correct
- ✅ Risk levels properly assigned

### Safety Checks
- ✅ High-risk agents require approval
- ✅ Referenced repos/workflows exist
- ✅ No unsafe combinations (e.g., "high-risk agent + no approval required")

### Capability Logic
- 🧪 Ensure downgrade is safe (high → lower permissions)
- 🧪 Ensure upgrades trigger explicit review/approval

---

## 📏 Design Principles

`blackroad-os-agents` = **"who are the agents and what can they do"**, not "what they actually run":

| Concern | Location |
|---------|----------|
| 🧭 Identity + capabilities | Here (`blackroad-os-agents`) |
| ⚙️ Execution | `blackroad-os-operator` |
| 🕹️ Visibility | `blackroad-os-prism-console` |
| 🧾 History | `blackroad-os-archive` |

---

## 🧬 Local Emoji Legend

| Emoji | Meaning |
|-------|---------|
| 🤖 | Agent / persona |
| 🧬 | Agent config / schema |
| 📋 | Registry / roster |
| ⚙️ | Workflows they can run |
| 🧭 | Scopes / permissions |
| ⚠️ | High-risk capabilities |
| 🧾 | Action logs / archive |
| 💰 | Finance-related |
| ☁️ | Infrastructure-related |
| 🪪 | Identity-related |
| ⚖️ | Legal-related |
| 🔐 | Secrets (forbidden zone) |

---

## 🎯 Success Criteria

If a new "Agent Architect" human or meta-agent lands here, they should be able to:

1. ✅ See the full roster of agents and their roles across the OS
2. ✅ Safely define or modify agents without accidentally giving god-mode
3. ✅ Plug agents into Packs, Operator, Prism, and Archive via clear, typed contracts

---

## 📚 Related Repositories

- [`blackroad-os-core`](https://github.com/BlackRoad-OS/blackroad-os-core) – Core domain logic 🧠
- [`blackroad-os-operator`](https://github.com/BlackRoad-OS/blackroad-os-operator) – Workflow execution ⚙️
- [`blackroad-os-prism-console`](https://github.com/BlackRoad-OS/blackroad-os-prism-console) – Agent visibility 🕹️
- [`blackroad-os-archive`](https://github.com/BlackRoad-OS/blackroad-os-archive) – Action history 🧾
- [`blackroad-os-infra`](https://github.com/BlackRoad-OS/blackroad-os-infra) – Infrastructure ☁️

---

*🤖🧬 BlackRoad OS Agent Swarm – defining who the agents are and what they can do.*