import { describe, expect, it } from 'vitest';
import { loadAllAgents, getAgent } from '../loader.js';

describe('registry loader', () => {
  it('loads all agents from the registry', async () => {
    const agents = await loadAllAgents();
    expect(agents.length).toBeGreaterThanOrEqual(3);
  });

  it('resolves an agent by id', async () => {
    const agent = await getAgent('lucidia');
    expect(agent?.name).toBe('Lucidia');
  });
});
