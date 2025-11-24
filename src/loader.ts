import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { agentSchema } from './agent.schema.js';
import type { Agent } from './types.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REGISTRY_DIR = path.resolve(__dirname, '..', 'registry');

async function readAgentFile(filePath: string): Promise<Agent> {
  const data = await fs.readFile(filePath, 'utf8');
  const parsed = JSON.parse(data);
  return agentSchema.parse(parsed);
}

export async function loadAllAgents(): Promise<Agent[]> {
  const files = await fs.readdir(REGISTRY_DIR);
  const manifests: Agent[] = [];

  for (const file of files) {
    if (!file.endsWith('.json')) continue;
    const manifest = await readAgentFile(path.join(REGISTRY_DIR, file));
    manifests.push(manifest);
  }

  return manifests;
}

export async function getAgent(id: string): Promise<Agent | undefined> {
  const agents = await loadAllAgents();
  return agents.find((agent) => agent.id === id);
}

// TODO(agents-next): Add graph helpers for dependencies and runtime spawning.
