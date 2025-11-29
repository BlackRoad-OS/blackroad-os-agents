# Blackroad OS Agents Registry (Gen-0)

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
