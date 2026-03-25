<!-- BlackRoad SEO Enhanced -->

# ulackroad os agents

> Part of **[BlackRoad OS](https://blackroad.io)** — Sovereign Computing for Everyone

[![BlackRoad OS](https://img.shields.io/badge/BlackRoad-OS-ff1d6c?style=for-the-badge)](https://blackroad.io)
[![BlackRoad Agents](https://img.shields.io/badge/Org-BlackRoad-Agents-2979ff?style=for-the-badge)](https://github.com/BlackRoad-Agents)
[![License](https://img.shields.io/badge/License-Proprietary-f5a623?style=for-the-badge)](LICENSE)

**ulackroad os agents** is part of the **BlackRoad OS** ecosystem — a sovereign, distributed operating system built on edge computing, local AI, and mesh networking by **BlackRoad OS, Inc.**

## About BlackRoad OS

BlackRoad OS is a sovereign computing platform that runs AI locally on your own hardware. No cloud dependencies. No API keys. No surveillance. Built by [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc), a Delaware C-Corp founded in 2025.

### Key Features
- **Local AI** — Run LLMs on Raspberry Pi, Hailo-8, and commodity hardware
- **Mesh Networking** — WireGuard VPN, NATS pub/sub, peer-to-peer communication
- **Edge Computing** — 52 TOPS of AI acceleration across a Pi fleet
- **Self-Hosted Everything** — Git, DNS, storage, CI/CD, chat — all sovereign
- **Zero Cloud Dependencies** — Your data stays on your hardware

### The BlackRoad Ecosystem
| Organization | Focus |
|---|---|
| [BlackRoad OS](https://github.com/BlackRoad-OS) | Core platform and applications |
| [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc) | Corporate and enterprise |
| [BlackRoad AI](https://github.com/BlackRoad-AI) | Artificial intelligence and ML |
| [BlackRoad Hardware](https://github.com/BlackRoad-Hardware) | Edge hardware and IoT |
| [BlackRoad Security](https://github.com/BlackRoad-Security) | Cybersecurity and auditing |
| [BlackRoad Quantum](https://github.com/BlackRoad-Quantum) | Quantum computing research |
| [BlackRoad Agents](https://github.com/BlackRoad-Agents) | Autonomous AI agents |
| [BlackRoad Network](https://github.com/BlackRoad-Network) | Mesh and distributed networking |
| [BlackRoad Education](https://github.com/BlackRoad-Education) | Learning and tutoring platforms |
| [BlackRoad Labs](https://github.com/BlackRoad-Labs) | Research and experiments |
| [BlackRoad Cloud](https://github.com/BlackRoad-Cloud) | Self-hosted cloud infrastructure |
| [BlackRoad Forge](https://github.com/BlackRoad-Forge) | Developer tools and utilities |

### Links
- **Website**: [blackroad.io](https://blackroad.io)
- **Documentation**: [docs.blackroad.io](https://docs.blackroad.io)
- **Chat**: [chat.blackroad.io](https://chat.blackroad.io)
- **Search**: [search.blackroad.io](https://search.blackroad.io)

---


Central registry and SDK for Blackroad OS agents. Each agent is defined by a JSON manifest in `/registry`, validated by a Zod schema, and consumable via the `@blackroad/agent-sdk` package.

## Quickstart

```bash
pnpm install
pnpm br-agent validate
```

Use the SDK:

```ts
import { loadAllAgents } from '@blackroad/agent-sdk';

const agents = await loadAllAgents();
```

## Structure

- `/registry` — one JSON manifest per agent (validated against `agent.schema.ts`).
- `/src` — SDK source: schema, loader utilities, CLI.
- `/scripts/postbuild.ts` — writes `public/sig.beacon.json` after build.
- `/public` — build artifacts exposed by the package.

## CLI

Validate agents:

```bash
pnpm br-agent validate
```

Add a new agent:

```bash
pnpm br-agent add --id thinker --name "Deep Thinker"
```

> Note: the `add` command scaffolds a manifest; git commit automation is marked as TODO.

## Development

- `pnpm lint`
- `pnpm test`
- `pnpm typecheck`
- `pnpm build`

## Notes

- This is a Gen-0 scaffold. Future iterations will extend graph relationships and runtime spawning (`// TODO(agents-next)`).
# BlackRoad OS Agents

BlackRoad OS Agents is the canonical home for policy-aware agent identities, behaviors, and HR-style records. Use this repo for agent source, metadata, and validation; keep operational automations in `blackroad-os-operator`, and maintain the master list of IDs in the global catalog.

## What belongs where
- **blackroad-os-agents**: agent identities, personas, policy hooks, metadata schemas, scaffolding for new agents, validation, and tests.
- **blackroad-os-operator**: operational runtime, orchestration code, integrations, and deployment logic.
- **Global agent catalog**: system of record for IDs and discovery; stored as `agents.yaml` and referenced by sync scripts.

## How to create a new agent
1. Add a new entry to the global `agents.yaml` (Master Catalog) with the agent `id`, `org_layer`, and desired language.
2. Run the catalog sync:
   ```bash
   export CATALOG_URL=./agents.yaml # or remote URL
   NODE_OPTIONS=--loader=./scripts/ts-loader.mjs node scripts/sync_from_catalog.ts
   ```
3. Implement the generated stubs (code + `.agent.yaml`) and add tests.
4. Run validation and test suites:
   ```bash
   NODE_OPTIONS=--loader=./scripts/ts-loader.mjs node scripts/validate_agents.ts
   npm run test:js
   npm run test:py
   ```
5. Open a PR for review.

## Leadership Archetypes
- **Chief Orchestrator**: systems thinker who coordinates cross-repo priorities and removes ambiguity.
- **Policy Steward**: guardian of governance, data handling, and contractual safeguards.
- **Growth Catalyst**: accelerates adoption, onboarding, and capability-building across teams.
- **Incident Sheriff**: decisive incident leader focused on triage, stabilization, and follow-through.
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
