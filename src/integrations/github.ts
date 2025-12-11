/**
 * GitHub Platform Integration
 *
 * Provides repository, issues, PR, and Actions capabilities
 */

import type {
  Integration,
  IntegrationStatus,
  GitHubConfig,
} from "./types.js";

const GITHUB_API_URL = "https://api.github.com";

interface GitHubUser {
  id: number;
  login: string;
  name: string | null;
  email: string | null;
}

interface GitHubRepository {
  id: number;
  name: string;
  full_name: string;
  description: string | null;
  private: boolean;
  default_branch: string;
  html_url: string;
}

interface GitHubIssue {
  id: number;
  number: number;
  title: string;
  body: string | null;
  state: "open" | "closed";
  labels: Array<{ name: string }>;
}

interface GitHubPullRequest {
  id: number;
  number: number;
  title: string;
  body: string | null;
  state: "open" | "closed" | "merged";
  head: { ref: string; sha: string };
  base: { ref: string };
}

interface GitHubWorkflowRun {
  id: number;
  name: string;
  status: string;
  conclusion: string | null;
  html_url: string;
}

export class GitHubClient implements Integration {
  private config: GitHubConfig;
  private initialized = false;

  constructor(config: GitHubConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    if (!this.config.token) {
      throw new Error("GitHub token is required");
    }
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    try {
      const user = await this.getCurrentUser();
      return {
        connected: true,
        healthy: true,
        lastCheck: new Date(),
        metadata: { user: user.login },
      };
    } catch (error) {
      return {
        connected: false,
        healthy: false,
        lastCheck: new Date(),
        error: error instanceof Error ? error.message : "Unknown error",
      };
    }
  }

  async cleanup(): Promise<void> {
    this.initialized = false;
  }

  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    if (!this.config.token) {
      throw new Error("GitHub token not configured");
    }

    const response = await fetch(`${GITHUB_API_URL}${path}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${this.config.token}`,
        Accept: "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(
        (error as { message?: string }).message || `GitHub API error: ${response.status}`
      );
    }

    return response.json() as Promise<T>;
  }

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<GitHubUser> {
    return this.request<GitHubUser>("/user");
  }

  /**
   * List repositories for authenticated user
   */
  async listRepositories(options?: {
    type?: "all" | "owner" | "public" | "private";
    sort?: "created" | "updated" | "pushed" | "full_name";
  }): Promise<GitHubRepository[]> {
    const params = new URLSearchParams();
    if (options?.type) params.set("type", options.type);
    if (options?.sort) params.set("sort", options.sort);
    return this.request<GitHubRepository[]>(`/user/repos?${params}`);
  }

  /**
   * Get repository
   */
  async getRepository(owner: string, repo: string): Promise<GitHubRepository> {
    return this.request<GitHubRepository>(`/repos/${owner}/${repo}`);
  }

  /**
   * List issues
   */
  async listIssues(
    owner: string,
    repo: string,
    options?: { state?: "open" | "closed" | "all" }
  ): Promise<GitHubIssue[]> {
    const params = new URLSearchParams();
    if (options?.state) params.set("state", options.state);
    return this.request<GitHubIssue[]>(
      `/repos/${owner}/${repo}/issues?${params}`
    );
  }

  /**
   * Create issue
   */
  async createIssue(
    owner: string,
    repo: string,
    issue: { title: string; body?: string; labels?: string[] }
  ): Promise<GitHubIssue> {
    return this.request<GitHubIssue>(`/repos/${owner}/${repo}/issues`, {
      method: "POST",
      body: JSON.stringify(issue),
    });
  }

  /**
   * Update issue
   */
  async updateIssue(
    owner: string,
    repo: string,
    issueNumber: number,
    update: { title?: string; body?: string; state?: "open" | "closed" }
  ): Promise<GitHubIssue> {
    return this.request<GitHubIssue>(
      `/repos/${owner}/${repo}/issues/${issueNumber}`,
      {
        method: "PATCH",
        body: JSON.stringify(update),
      }
    );
  }

  /**
   * List pull requests
   */
  async listPullRequests(
    owner: string,
    repo: string,
    options?: { state?: "open" | "closed" | "all" }
  ): Promise<GitHubPullRequest[]> {
    const params = new URLSearchParams();
    if (options?.state) params.set("state", options.state);
    return this.request<GitHubPullRequest[]>(
      `/repos/${owner}/${repo}/pulls?${params}`
    );
  }

  /**
   * Create pull request
   */
  async createPullRequest(
    owner: string,
    repo: string,
    pr: { title: string; body?: string; head: string; base: string }
  ): Promise<GitHubPullRequest> {
    return this.request<GitHubPullRequest>(`/repos/${owner}/${repo}/pulls`, {
      method: "POST",
      body: JSON.stringify(pr),
    });
  }

  /**
   * Merge pull request
   */
  async mergePullRequest(
    owner: string,
    repo: string,
    pullNumber: number,
    options?: {
      commit_title?: string;
      commit_message?: string;
      merge_method?: "merge" | "squash" | "rebase";
    }
  ): Promise<{ sha: string; merged: boolean }> {
    return this.request<{ sha: string; merged: boolean }>(
      `/repos/${owner}/${repo}/pulls/${pullNumber}/merge`,
      {
        method: "PUT",
        body: JSON.stringify(options || {}),
      }
    );
  }

  /**
   * List workflow runs
   */
  async listWorkflowRuns(
    owner: string,
    repo: string
  ): Promise<{ workflow_runs: GitHubWorkflowRun[] }> {
    return this.request<{ workflow_runs: GitHubWorkflowRun[] }>(
      `/repos/${owner}/${repo}/actions/runs`
    );
  }

  /**
   * Trigger workflow dispatch
   */
  async triggerWorkflow(
    owner: string,
    repo: string,
    workflowId: string | number,
    ref: string,
    inputs?: Record<string, string>
  ): Promise<boolean> {
    await this.request(
      `/repos/${owner}/${repo}/actions/workflows/${workflowId}/dispatches`,
      {
        method: "POST",
        body: JSON.stringify({ ref, inputs }),
      }
    );
    return true;
  }

  /**
   * Get workflow run
   */
  async getWorkflowRun(
    owner: string,
    repo: string,
    runId: number
  ): Promise<GitHubWorkflowRun> {
    return this.request<GitHubWorkflowRun>(
      `/repos/${owner}/${repo}/actions/runs/${runId}`
    );
  }

  /**
   * Create repository dispatch event
   */
  async createDispatchEvent(
    owner: string,
    repo: string,
    eventType: string,
    clientPayload?: Record<string, unknown>
  ): Promise<boolean> {
    await this.request(`/repos/${owner}/${repo}/dispatches`, {
      method: "POST",
      body: JSON.stringify({
        event_type: eventType,
        client_payload: clientPayload,
      }),
    });
    return true;
  }

  /**
   * Get repository content
   */
  async getContent(
    owner: string,
    repo: string,
    path: string,
    ref?: string
  ): Promise<{ content: string; sha: string }> {
    const params = ref ? `?ref=${ref}` : "";
    const result = await this.request<{ content: string; sha: string }>(
      `/repos/${owner}/${repo}/contents/${path}${params}`
    );
    return {
      content: Buffer.from(result.content, "base64").toString("utf-8"),
      sha: result.sha,
    };
  }

  /**
   * Create or update file
   */
  async createOrUpdateFile(
    owner: string,
    repo: string,
    path: string,
    content: string,
    message: string,
    sha?: string,
    branch?: string
  ): Promise<{ content: { sha: string }; commit: { sha: string } }> {
    return this.request<{ content: { sha: string }; commit: { sha: string } }>(
      `/repos/${owner}/${repo}/contents/${path}`,
      {
        method: "PUT",
        body: JSON.stringify({
          message,
          content: Buffer.from(content).toString("base64"),
          sha,
          branch,
        }),
      }
    );
  }
}
