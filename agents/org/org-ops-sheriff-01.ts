export interface Incident {
  id: string;
  severity: string;
  summary: string;
}

export interface TriagePlan {
  incidentId: string;
  lead: string;
  actions: string[];
}

export function triage_incident(incident: Incident): TriagePlan {
  const immediateActions = [
    'assign_commander',
    'notify_stakeholders',
    `stabilize_${incident.id}`
  ];
  return {
    incidentId: incident.id,
    lead: 'ops-sheriff',
    actions: immediateActions
  };
}

export interface Markdown {
  content: string;
}

export function postmortem_template(incident: Incident): Markdown {
  const sections = [
    `# Postmortem for ${incident.id}`,
    `## Severity: ${incident.severity}`,
    '## Timeline',
    '## Impact',
    '## Root Cause',
    '## Action Items'
  ];
  return { content: sections.join('\n\n') };
}
