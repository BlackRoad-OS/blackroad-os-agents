/**
 * Vercel Platform Integration
 *
 * Provides deployment and project management capabilities for Vercel
 */

import type {
  Integration,
  IntegrationStatus,
  VercelConfig,
  DeploymentResult,
} from "./types.js";

const VERCEL_API_URL = "https://api.vercel.com";

interface VercelProject {
  id: string;
  name: string;
  framework: string | null;
  latestDeployments: Array<{
    id: string;
    url: string;
    state: string;
  }>;
}

interface VercelDeployment {
  id: string;
  uid: string;
  url: string;
  state: string;
  readyState: string;
  createdAt: number;
  buildingAt: number | null;
  ready: number | null;
}

interface VercelDomain {
  name: string;
  apexName: string;
  projectId: string;
  verified: boolean;
}

export class VercelClient implements Integration {
  private config: VercelConfig;
  private initialized = false;

  constructor(config: VercelConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    if (!this.config.token) {
      throw new Error("Vercel token is required");
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
        metadata: { username: user.username },
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
      throw new Error("Vercel token not configured");
    }

    const url = new URL(`${VERCEL_API_URL}${path}`);
    if (this.config.orgId) {
      url.searchParams.set("teamId", this.config.orgId);
    }

    const response = await fetch(url.toString(), {
      ...options,
      headers: {
        Authorization: `Bearer ${this.config.token}`,
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(
        (error as { error?: { message?: string } }).error?.message ||
          `Vercel API error: ${response.status}`
      );
    }

    return response.json() as Promise<T>;
  }

  /**
   * Get current user
   */
  async getCurrentUser(): Promise<{ id: string; username: string; email: string }> {
    const result = await this.request<{
      user: { id: string; username: string; email: string };
    }>("/v2/user");
    return result.user;
  }

  /**
   * List projects
   */
  async listProjects(): Promise<VercelProject[]> {
    const result = await this.request<{ projects: VercelProject[] }>(
      "/v9/projects"
    );
    return result.projects;
  }

  /**
   * Get project
   */
  async getProject(projectId: string): Promise<VercelProject> {
    return this.request<VercelProject>(`/v9/projects/${projectId}`);
  }

  /**
   * List deployments
   */
  async listDeployments(projectId?: string): Promise<VercelDeployment[]> {
    const path = projectId
      ? `/v6/deployments?projectId=${projectId}`
      : "/v6/deployments";
    const result = await this.request<{ deployments: VercelDeployment[] }>(
      path
    );
    return result.deployments;
  }

  /**
   * Get deployment
   */
  async getDeployment(deploymentId: string): Promise<VercelDeployment> {
    return this.request<VercelDeployment>(`/v13/deployments/${deploymentId}`);
  }

  /**
   * Create deployment
   */
  async createDeployment(options: {
    name: string;
    gitSource?: {
      type: "github" | "gitlab" | "bitbucket";
      ref: string;
      repoId: string | number;
    };
    files?: Array<{ file: string; data: string }>;
    projectSettings?: {
      framework?: string;
      buildCommand?: string;
      outputDirectory?: string;
    };
  }): Promise<DeploymentResult> {
    try {
      const result = await this.request<VercelDeployment>("/v13/deployments", {
        method: "POST",
        body: JSON.stringify(options),
      });
      return {
        success: true,
        deploymentId: result.id,
        url: `https://${result.url}`,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Deployment failed",
      };
    }
  }

  /**
   * Cancel deployment
   */
  async cancelDeployment(deploymentId: string): Promise<boolean> {
    await this.request(`/v12/deployments/${deploymentId}/cancel`, {
      method: "PATCH",
    });
    return true;
  }

  /**
   * Delete deployment
   */
  async deleteDeployment(deploymentId: string): Promise<boolean> {
    await this.request(`/v13/deployments/${deploymentId}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * List domains for a project
   */
  async listDomains(projectId: string): Promise<VercelDomain[]> {
    const result = await this.request<{ domains: VercelDomain[] }>(
      `/v9/projects/${projectId}/domains`
    );
    return result.domains;
  }

  /**
   * Add domain to project
   */
  async addDomain(projectId: string, domain: string): Promise<VercelDomain> {
    return this.request<VercelDomain>(`/v9/projects/${projectId}/domains`, {
      method: "POST",
      body: JSON.stringify({ name: domain }),
    });
  }

  /**
   * Remove domain from project
   */
  async removeDomain(projectId: string, domain: string): Promise<boolean> {
    await this.request(`/v9/projects/${projectId}/domains/${domain}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * Get environment variables
   */
  async getEnvVars(
    projectId: string
  ): Promise<Array<{ key: string; value: string; target: string[] }>> {
    const result = await this.request<{
      envs: Array<{ key: string; value: string; target: string[] }>;
    }>(`/v9/projects/${projectId}/env`);
    return result.envs;
  }

  /**
   * Set environment variable
   */
  async setEnvVar(
    projectId: string,
    key: string,
    value: string,
    target: ("production" | "preview" | "development")[] = ["production"]
  ): Promise<boolean> {
    await this.request(`/v10/projects/${projectId}/env`, {
      method: "POST",
      body: JSON.stringify({ key, value, target, type: "encrypted" }),
    });
    return true;
  }

  /**
   * Delete environment variable
   */
  async deleteEnvVar(projectId: string, envId: string): Promise<boolean> {
    await this.request(`/v9/projects/${projectId}/env/${envId}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * Promote deployment to production
   */
  async promoteToProduction(
    projectId: string,
    deploymentId: string
  ): Promise<boolean> {
    await this.request(`/v10/projects/${projectId}/promote/${deploymentId}`, {
      method: "POST",
    });
    return true;
  }

  /**
   * Get deployment logs
   */
  async getDeploymentLogs(
    deploymentId: string
  ): Promise<Array<{ created: number; text: string }>> {
    const result = await this.request<
      Array<{ created: number; text: string }>
    >(`/v2/deployments/${deploymentId}/events`);
    return result;
  }
}
