import { validateAgents } from '../scripts/validate_agents';

describe('agent metadata schema', () => {
  it('validates all agent files against the schema', () => {
    const result = validateAgents();
    expect(result.success).toBe(true);
    expect(result.total).toBeGreaterThan(0);
  });
});
