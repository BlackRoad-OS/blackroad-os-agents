// @ts-nocheck
import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');

function loadSchema(relativePath) {
  const raw = fs.readFileSync(path.join(repoRoot, relativePath), 'utf-8');
  return JSON.parse(raw);
}

function createValidator() {
  const ajv = new Ajv({ allErrors: true, strict: false });
  addFormats(ajv);
  const persona = loadSchema('schemas/persona.schema.json');
  const policyHook = loadSchema('schemas/policy-hook.schema.json');
  const agent = loadSchema('schemas/agent.schema.json');
  ajv.addSchema(persona, persona.$id);
  ajv.addSchema(policyHook, policyHook.$id);
  return ajv.compile(agent);
}

function findAgentFiles(startDir) {
  const results = [];
  const entries = fs.readdirSync(startDir, { withFileTypes: true });
  for (const entry of entries) {
    const fullPath = path.join(startDir, entry.name);
    if (entry.isDirectory()) {
      results.push(...findAgentFiles(fullPath));
    } else if (entry.isFile() && entry.name.endsWith('.agent.yaml')) {
      results.push(fullPath);
    }
  }
  return results;
}

function summarize(agents) {
  const byRole = new Map();
  const byLayer = new Map();
  for (const agent of agents) {
    byRole.set(agent.role_archetype, (byRole.get(agent.role_archetype) || 0) + 1);
    byLayer.set(agent.org_layer, (byLayer.get(agent.org_layer) || 0) + 1);
  }
  return { byRole, byLayer };
}

export function validateAgents() {
  const validator = createValidator();
  const files = findAgentFiles(path.join(repoRoot, 'agents'));
  let validCount = 0;
  const agents = [];
  const errors = [];

  for (const file of files) {
    const doc = yaml.load(fs.readFileSync(file, 'utf-8'));
    const valid = validator(doc);
    if (!valid) {
      errors.push({ file, messages: validator.errors || [] });
    } else {
      validCount += 1;
      agents.push(doc);
    }
  }

  if (errors.length > 0) {
    for (const error of errors) {
      console.error(`Validation failed for ${path.relative(repoRoot, error.file)}`);
      console.error(JSON.stringify(error.messages, null, 2));
    }
    return { success: false, total: files.length, agents: [] };
  }

  const { byRole, byLayer } = summarize(agents);
  console.log('Agent validation summary');
  console.log('-------------------------');
  console.log(`Total agents: ${validCount}`);
  console.log('By role_archetype:');
  for (const [role, count] of byRole.entries()) {
    console.log(`  ${role}: ${count}`);
  }
  console.log('By org_layer:');
  for (const [layer, count] of byLayer.entries()) {
    console.log(`  ${layer}: ${count}`);
  }

  return { success: true, total: validCount, agents };
}

if (import.meta.url === new URL(process.argv[1], 'file:').href) {
  const { success } = validateAgents();
  if (!success) {
    process.exit(1);
  }
}
