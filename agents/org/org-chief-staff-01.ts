export interface IssueList {
  issues: Array<{ id: string; title: string; risk?: string }>;
}

export interface Plan {
  focus: string[];
  risks: string[];
}

export interface OrgMetrics {
  teams: Array<{ name: string; health: string; highlights?: string[] }>; 
}

export interface Report {
  summary: string;
  hotspots: string[];
}

export function plan_sprint(issues: IssueList): Plan {
  return {
    focus: issues.issues.map((issue) => issue.title),
    risks: issues.issues.filter((issue) => issue.risk).map((issue) => issue.risk || '')
  };
}

export function summarize_org_health(metrics: OrgMetrics): Report {
  return {
    summary: `Reviewed ${metrics.teams.length} teams`,
    hotspots: metrics.teams.filter((team) => team.health === 'at-risk').map((team) => team.name)
  };
}
