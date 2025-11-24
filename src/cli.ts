#!/usr/bin/env node
import { Command } from 'commander';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';
import { agentSchema } from './agent.schema.js';
import { getAgent, loadAllAgents } from './loader.js';
import type { Agent } from './types.js';

const program = new Command();
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REGISTRY_DIR = path.resolve(__dirname, '..', 'registry');

async function scaffoldAgent(id: string, name: string): Promise<Agent> {
  const exists = await getAgent(id);
  if (exists) {
    throw new Error(`Agent with id '${id}' already exists`);
  }

  const stub: Agent = {
    id,
    name,
    role: 'Unspecified role',
    version: '0.0.1',
    owner: 'unknown',
    capabilities: ['chat'],
    status: 'draft',
  };

  const parsed = agentSchema.parse(stub);
  const filePath = path.join(REGISTRY_DIR, `${id}.json`);
  await fs.writeFile(filePath, JSON.stringify(parsed, null, 2));
  return parsed;
}

program.name('br-agent').description('Agent registry CLI').version('0.1.0');

program
  .command('validate')
  .description('Validate all agents')
  .action(async () => {
    const agents = await loadAllAgents();
    console.log(`Validated ${agents.length} agents.`);
  });

program
  .command('add')
  .description('Add a new agent manifest')
  .requiredOption('--id <id>', 'Agent id (kebab-case)')
  .requiredOption('--name <name>', 'Agent name')
  .action(async (options: { id: string; name: string }) => {
    const agent = await scaffoldAgent(options.id, options.name);
    console.log(`Created ${agent.id} at registry/${agent.id}.json`);
    console.log('TODO: commit manifest to git');
  });

program.parse();
