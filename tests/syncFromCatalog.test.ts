import fs from 'fs';
import path from 'path';
import os from 'os';
import yaml from 'js-yaml';
import { syncFromCatalog } from '../scripts/sync_from_catalog';

describe('sync_from_catalog', () => {
  const originalCatalog = process.env.CATALOG_URL;
  const originalRoot = process.env.AGENTS_ROOT;

  afterEach(() => {
    process.env.CATALOG_URL = originalCatalog;
    process.env.AGENTS_ROOT = originalRoot;
  });

  it('creates missing stubs from catalog', async () => {
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-sync-'));
    const catalogPath = path.join(tempDir, 'agents.yaml');
    fs.writeFileSync(catalogPath, yaml.dump([{ id: 'temp-agent-01', org_layer: 'experimental', language: 'ts' }]));

    process.env.CATALOG_URL = catalogPath;
    process.env.AGENTS_ROOT = tempDir;

    await syncFromCatalog();

    const metaPath = path.join(tempDir, 'agents', 'experimental', 'temp-agent-01.agent.yaml');
    const codePath = path.join(tempDir, 'agents', 'experimental', 'temp-agent-01.ts');
    expect(fs.existsSync(metaPath)).toBe(true);
    expect(fs.existsSync(codePath)).toBe(true);
    const meta = yaml.load(fs.readFileSync(metaPath, 'utf-8')) as any;
    expect(meta.lifecycle).toBe('stub');
  });

  it('does not overwrite existing code files', async () => {
    const tempDir = fs.mkdtempSync(path.join(os.tmpdir(), 'catalog-sync-'));
    const catalogPath = path.join(tempDir, 'agents.yaml');
    fs.writeFileSync(catalogPath, yaml.dump([{ id: 'temp-agent-02', org_layer: 'experimental', language: 'ts' }]));

    const metaDir = path.join(tempDir, 'agents', 'experimental');
    fs.mkdirSync(metaDir, { recursive: true });
    const codePath = path.join(metaDir, 'temp-agent-02.ts');
    const metaPath = path.join(metaDir, 'temp-agent-02.agent.yaml');
    fs.writeFileSync(codePath, '// keep me');
    fs.writeFileSync(metaPath, yaml.dump({
      id: 'temp-agent-02',
      display_name: 'Temp',
      role_archetype: 'test',
      org_layer: 'experimental',
      personality: { traits: ['tbd'], leadership_style: 'tbd' },
      capabilities: ['tbd'],
      identity: { ps_sha_infinity: 'pssha∞:br:temp-agent-02:STUB', version: 1 },
      policy_profile: { risk_band: 'low', allowed_domains: ['tbd'], prohibited_actions: [] },
      suitability_profile: { ideal_context: ['tbd'], anti_patterns: ['tbd'] },
      owner: '@test',
      home_repo: 'blackroad-os-agents',
      lifecycle: 'stub'
    }));

    process.env.CATALOG_URL = catalogPath;
    process.env.AGENTS_ROOT = tempDir;

    await syncFromCatalog();

    expect(fs.readFileSync(codePath, 'utf-8')).toBe('// keep me');
  });
});
