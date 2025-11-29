import { plan_sprint, summarize_org_health } from '../agents/org/org-chief-staff-01';
import { triage_incident, postmortem_template } from '../agents/org/org-ops-sheriff-01';

describe('org-chief-staff-01 agent', () => {
  it('creates a sprint plan with focus and risks', () => {
    const result = plan_sprint({
      issues: [
        { id: '1', title: 'Improve docs' },
        { id: '2', title: 'Refactor core', risk: 'timeline' }
      ]
    });
    expect(result.focus).toEqual(['Improve docs', 'Refactor core']);
    expect(result.risks).toContain('timeline');
  });

  it('summarizes org health', () => {
    const report = summarize_org_health({
      teams: [
        { name: 'alpha', health: 'steady' },
        { name: 'beta', health: 'at-risk' }
      ]
    });
    expect(report.summary).toContain('Reviewed');
    expect(report.hotspots).toEqual(['beta']);
  });
});

describe('org-ops-sheriff-01 agent', () => {
  it('builds a triage plan', () => {
    const plan = triage_incident({ id: 'INC-1', severity: 'SEV-2', summary: 'test' });
    expect(plan.incidentId).toBe('INC-1');
    expect(plan.actions.length).toBeGreaterThan(0);
  });

  it('generates a postmortem template', () => {
    const doc = postmortem_template({ id: 'INC-2', severity: 'SEV-1', summary: 'another' });
    expect(doc.content).toContain('Postmortem');
    expect(doc.content).toContain('Severity');
  });
});
