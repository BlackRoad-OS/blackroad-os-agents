// @ts-nocheck
import fs from 'fs';
import path from 'path';
import yaml from 'js-yaml';
import Ajv from 'ajv';
import addFormats from 'ajv-formats';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const repoRoot = path.resolve(__dirname, '..');

function getAgentsRoot() {
  return process.env.AGENTS_ROOT ? path.resolve(process.env.AGENTS_ROOT) : repoRoot;
}

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

function readCatalog(catalogLocation) {
  if (catalogLocation.startsWith('http://') || catalogLocation.startsWith('https://')) {
    return fetch(catalogLocation).then((resp) => {
      if (!resp.ok) {
        throw new Error(`Failed to fetch catalog: ${resp.status} ${resp.statusText}`);
      }
      return resp.text();
    });
  }
  return Promise.resolve(fs.readFileSync(catalogLocation, 'utf-8'));
}

function ensureDir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
  }
}

function agentFilePath(entry, baseRoot = getAgentsRoot()) {
  const layer = entry.org_layer || 'experimental';
  return path.join(baseRoot, 'agents', layer, `${entry.id}.agent.yaml`);
}

function agentCodePath(entry, baseRoot = getAgentsRoot()) {
  const layer = entry.org_layer || 'experimental';
  const extension = entry.language === 'python' ? 'py' : 'ts';
  return path.join(baseRoot, 'agents', layer, `${entry.id}.${extension}`);
}

function createStubMetadata(entry) {
  return {
    id: entry.id,
    display_name: entry.display_name || entry.id,
    role_archetype: entry.role_archetype || 'unspecified',
    org_layer: entry.org_layer || 'experimental',
    personality: entry.personality || { traits: ['tbd'], leadership_style: 'tbd' },
    capabilities: entry.capabilities || ['tbd'],
    identity: entry.identity || { ps_sha_infinity: `pssha∞:br:${entry.id}:STUB`, version: 1 },
    policy_profile: entry.policy_profile || {
      risk_band: 'low',
      allowed_domains: ['tbd'],
      prohibited_actions: []
    },
    suitability_profile: entry.suitability_profile || {
      ideal_context: ['tbd'],
      anti_patterns: ['tbd']
    },
    owner: entry.owner || '@unknown',
    home_repo: entry.home_repo || 'blackroad-os-agents',
    lifecycle: entry.lifecycle || 'stub'
  };
}

function writeStubCode(filePath, entry) {
  if (fs.existsSync(filePath)) {
    return;
  }
  const dir = path.dirname(filePath);
  ensureDir(dir);
  if (filePath.endsWith('.py')) {
    const content = `# Stub for ${entry.id}\n\n` +
      "def placeholder(**kwargs):\n" +
      "    \"\"\"TODO: implement agent logic.\"\"\"\n" +
      "    return kwargs\n";
    fs.writeFileSync(filePath, content, 'utf-8');
    return;
  }
  const content = `// Stub for ${entry.id}\n// TODO: implement agent logic\nexport function placeholder(payload = {}) {\n  return payload;\n}\n`;
  fs.writeFileSync(filePath, content, 'utf-8');
}

export async function syncFromCatalog(options = { checkOnly: false }) {
  const catalogLocation = process.env.CATALOG_URL || path.join(repoRoot, 'agents.yaml');
  const raw = await readCatalog(catalogLocation);
  const catalog = yaml.load(raw) || [];
  if (!Array.isArray(catalog)) {
    throw new Error('Catalog must be an array of agent entries');
  }
  const validator = createValidator();
  const catalogIds = new Set(catalog.map((entry) => entry.id));

  const agentFiles = [];
  const baseAgentsDir = path.join(getAgentsRoot(), 'agents');
  if (fs.existsSync(baseAgentsDir)) {
    const walk = (dir) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const full = path.join(dir, entry.name);
        if (entry.isDirectory()) walk(full);
        else if (entry.isFile() && entry.name.endsWith('.agent.yaml')) agentFiles.push(full);
      }
    };
    walk(baseAgentsDir);
  }

  const errors = [];
  for (const file of agentFiles) {
    const doc = yaml.load(fs.readFileSync(file, 'utf-8'));
    const valid = validator(doc);
    if (!valid) {
      errors.push({ file, messages: validator.errors || [] });
      continue;
    }
    if (!catalogIds.has(doc.id)) {
      errors.push({ file, messages: [`Unknown id ${doc.id} (not found in catalog)`] });
    }
  }

  if (options.checkOnly) {
    for (const entry of catalog) {
      const metaPath = agentFilePath(entry);
      if (!fs.existsSync(metaPath)) {
        errors.push({ file: metaPath, messages: ['Missing metadata for catalog id'] });
      }
    }
  }

  if (errors.length > 0) {
    for (const error of errors) {
      console.error(`Validation failed for ${path.relative(repoRoot, error.file)}`);
      console.error(JSON.stringify(error.messages, null, 2));
    }
    throw new Error('Validation errors detected.');
  }

  if (options.checkOnly) {
    return;
  }

  const baseRoot = getAgentsRoot();
  for (const entry of catalog) {
    const metaPath = agentFilePath(entry, baseRoot);
    ensureDir(path.dirname(metaPath));
    if (!fs.existsSync(metaPath)) {
      const stub = createStubMetadata(entry);
      fs.writeFileSync(metaPath, yaml.dump(stub, { noRefs: true }), 'utf-8');
      console.log(`Created stub metadata for ${entry.id}`);
    }
    const codePath = agentCodePath(entry, baseRoot);
    writeStubCode(codePath, entry);
  }
}

if (import.meta.url === new URL(process.argv[1], 'file:').href) {
  const checkOnly = process.argv.includes('--check');
  syncFromCatalog({ checkOnly }).catch((err) => {
    console.error(err.message || err);
    process.exit(1);
  });
}
