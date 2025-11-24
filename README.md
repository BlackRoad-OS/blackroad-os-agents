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
