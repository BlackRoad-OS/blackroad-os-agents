/**
 * Railway Platform Integration
 *
 * Provides deployment and management capabilities for Railway.app
 */

import type {
  Integration,
  IntegrationStatus,
  RailwayConfig,
  DeploymentResult,
} from "./types.js";

const RAILWAY_API_URL = "https://backboard.railway.app/graphql/v2";

interface RailwayProject {
  id: string;
  name: string;
  description?: string;
  createdAt: string;
  updatedAt: string;
}

interface RailwayService {
  id: string;
  name: string;
  projectId: string;
}

interface RailwayDeployment {
  id: string;
  status: string;
  createdAt: string;
  url?: string;
}

export class RailwayClient implements Integration {
  private config: RailwayConfig;
  private initialized = false;

  constructor(config: RailwayConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    if (!this.config.token) {
      throw new Error("Railway token is required");
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
        metadata: { user },
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

  private async graphql<T>(
    query: string,
    variables?: Record<string, unknown>
  ): Promise<T> {
    if (!this.config.token) {
      throw new Error("Railway token not configured");
    }

    const response = await fetch(RAILWAY_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${this.config.token}`,
      },
      body: JSON.stringify({ query, variables }),
    });

    if (!response.ok) {
      throw new Error(`Railway API error: ${response.statusText}`);
    }

    const data = (await response.json()) as {
      data?: T;
      errors?: Array<{ message: string }>;
    };
    if (data.errors) {
      throw new Error(data.errors[0]?.message || "GraphQL error");
    }

    return data.data as T;
  }

  /**
   * Get current authenticated user
   */
  async getCurrentUser(): Promise<{ id: string; email: string; name: string }> {
    const result = await this.graphql<{
      me: { id: string; email: string; name: string };
    }>(`
      query {
        me {
          id
          email
          name
        }
      }
    `);
    return result.me;
  }

  /**
   * List all projects
   */
  async listProjects(): Promise<RailwayProject[]> {
    const result = await this.graphql<{
      projects: { edges: Array<{ node: RailwayProject }> };
    }>(`
      query {
        projects {
          edges {
            node {
              id
              name
              description
              createdAt
              updatedAt
            }
          }
        }
      }
    `);
    return result.projects.edges.map((e) => e.node);
  }

  /**
   * Get project by ID
   */
  async getProject(projectId: string): Promise<RailwayProject | null> {
    const result = await this.graphql<{ project: RailwayProject | null }>(
      `
      query($id: String!) {
        project(id: $id) {
          id
          name
          description
          createdAt
          updatedAt
        }
      }
    `,
      { id: projectId }
    );
    return result.project;
  }

  /**
   * List services in a project
   */
  async listServices(projectId: string): Promise<RailwayService[]> {
    const result = await this.graphql<{
      project: { services: { edges: Array<{ node: RailwayService }> } };
    }>(
      `
      query($projectId: String!) {
        project(id: $projectId) {
          services {
            edges {
              node {
                id
                name
              }
            }
          }
        }
      }
    `,
      { projectId }
    );
    return result.project.services.edges.map((e) => ({
      ...e.node,
      projectId,
    }));
  }

  /**
   * Deploy a service
   */
  async deploy(
    serviceId: string,
    environmentId?: string
  ): Promise<DeploymentResult> {
    try {
      const result = await this.graphql<{
        serviceInstanceRedeploy: { id: string };
      }>(
        `
        mutation($serviceId: String!, $environmentId: String) {
          serviceInstanceRedeploy(serviceId: $serviceId, environmentId: $environmentId) {
            id
          }
        }
      `,
        {
          serviceId,
          environmentId: environmentId || this.config.environmentId,
        }
      );

      return {
        success: true,
        deploymentId: result.serviceInstanceRedeploy.id,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Deployment failed",
      };
    }
  }

  /**
   * Get deployment status
   */
  async getDeployment(deploymentId: string): Promise<RailwayDeployment | null> {
    const result = await this.graphql<{ deployment: RailwayDeployment | null }>(
      `
      query($id: String!) {
        deployment(id: $id) {
          id
          status
          createdAt
        }
      }
    `,
      { id: deploymentId }
    );
    return result.deployment;
  }

  /**
   * Set environment variable
   */
  async setVariable(
    serviceId: string,
    name: string,
    value: string,
    environmentId?: string
  ): Promise<boolean> {
    try {
      await this.graphql(
        `
        mutation($input: VariableUpsertInput!) {
          variableUpsert(input: $input)
        }
      `,
        {
          input: {
            serviceId,
            environmentId: environmentId || this.config.environmentId,
            name,
            value,
          },
        }
      );
      return true;
    } catch {
      return false;
    }
  }

  /**
   * Get service logs
   */
  async getLogs(
    deploymentId: string,
    limit = 100
  ): Promise<Array<{ timestamp: string; message: string }>> {
    const result = await this.graphql<{
      deploymentLogs: Array<{ timestamp: string; message: string }>;
    }>(
      `
      query($deploymentId: String!, $limit: Int) {
        deploymentLogs(deploymentId: $deploymentId, limit: $limit) {
          timestamp
          message
        }
      }
    `,
      { deploymentId, limit }
    );
    return result.deploymentLogs;
  }
}
