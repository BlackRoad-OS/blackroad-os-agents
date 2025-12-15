/**
 * Cloudflare Platform Integration
 *
 * Provides deployment, DNS, and Workers capabilities for Cloudflare
 */

import type {
  Integration,
  IntegrationStatus,
  CloudflareConfig,
  DeploymentResult,
} from "./types.js";

const CF_API_URL = "https://api.cloudflare.com/client/v4";

interface CloudflareZone {
  id: string;
  name: string;
  status: string;
}

interface CloudflareDNSRecord {
  id: string;
  type: string;
  name: string;
  content: string;
  ttl: number;
  proxied: boolean;
}

interface CloudflarePagesProject {
  id: string;
  name: string;
  subdomain: string;
  domains: string[];
  production_branch: string;
}

interface CloudflarePagesDeployment {
  id: string;
  url: string;
  environment: string;
  deployment_trigger: {
    type: string;
    metadata: {
      branch: string;
      commit_hash: string;
    };
  };
}

export class CloudflareClient implements Integration {
  private config: CloudflareConfig;
  private initialized = false;

  constructor(config: CloudflareConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    if (!this.config.apiToken) {
      throw new Error("Cloudflare API token is required");
    }
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    try {
      const user = await this.verifyToken();
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

  private async request<T>(
    path: string,
    options: RequestInit = {}
  ): Promise<T> {
    if (!this.config.apiToken) {
      throw new Error("Cloudflare API token not configured");
    }

    const response = await fetch(`${CF_API_URL}${path}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${this.config.apiToken}`,
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    const data = (await response.json()) as {
      success: boolean;
      result?: T;
      errors?: Array<{ message: string }>;
    };

    if (!data.success) {
      throw new Error(data.errors?.[0]?.message || "Cloudflare API error");
    }

    return data.result as T;
  }

  /**
   * Verify API token
   */
  async verifyToken(): Promise<{ id: string; status: string }> {
    return this.request<{ id: string; status: string }>("/user/tokens/verify");
  }

  /**
   * List zones (domains)
   */
  async listZones(): Promise<CloudflareZone[]> {
    return this.request<CloudflareZone[]>("/zones");
  }

  /**
   * Get zone by ID
   */
  async getZone(zoneId: string): Promise<CloudflareZone> {
    return this.request<CloudflareZone>(`/zones/${zoneId}`);
  }

  /**
   * List DNS records for a zone
   */
  async listDNSRecords(zoneId: string): Promise<CloudflareDNSRecord[]> {
    return this.request<CloudflareDNSRecord[]>(`/zones/${zoneId}/dns_records`);
  }

  /**
   * Create DNS record
   */
  async createDNSRecord(
    zoneId: string,
    record: Omit<CloudflareDNSRecord, "id">
  ): Promise<CloudflareDNSRecord> {
    return this.request<CloudflareDNSRecord>(`/zones/${zoneId}/dns_records`, {
      method: "POST",
      body: JSON.stringify(record),
    });
  }

  /**
   * Update DNS record
   */
  async updateDNSRecord(
    zoneId: string,
    recordId: string,
    record: Partial<CloudflareDNSRecord>
  ): Promise<CloudflareDNSRecord> {
    return this.request<CloudflareDNSRecord>(
      `/zones/${zoneId}/dns_records/${recordId}`,
      {
        method: "PATCH",
        body: JSON.stringify(record),
      }
    );
  }

  /**
   * Delete DNS record
   */
  async deleteDNSRecord(zoneId: string, recordId: string): Promise<boolean> {
    await this.request(`/zones/${zoneId}/dns_records/${recordId}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * List Pages projects
   */
  async listPagesProjects(): Promise<CloudflarePagesProject[]> {
    if (!this.config.accountId) {
      throw new Error("Account ID required for Pages");
    }
    return this.request<CloudflarePagesProject[]>(
      `/accounts/${this.config.accountId}/pages/projects`
    );
  }

  /**
   * Get Pages project
   */
  async getPagesProject(projectName: string): Promise<CloudflarePagesProject> {
    if (!this.config.accountId) {
      throw new Error("Account ID required for Pages");
    }
    return this.request<CloudflarePagesProject>(
      `/accounts/${this.config.accountId}/pages/projects/${projectName}`
    );
  }

  /**
   * List Pages deployments
   */
  async listPagesDeployments(
    projectName: string
  ): Promise<CloudflarePagesDeployment[]> {
    if (!this.config.accountId) {
      throw new Error("Account ID required for Pages");
    }
    return this.request<CloudflarePagesDeployment[]>(
      `/accounts/${this.config.accountId}/pages/projects/${projectName}/deployments`
    );
  }

  /**
   * Create Pages deployment (trigger build)
   */
  async createPagesDeployment(
    projectName: string,
    branch?: string
  ): Promise<DeploymentResult> {
    if (!this.config.accountId) {
      return { success: false, error: "Account ID required for Pages" };
    }

    try {
      const result = await this.request<CloudflarePagesDeployment>(
        `/accounts/${this.config.accountId}/pages/projects/${projectName}/deployments`,
        {
          method: "POST",
          body: JSON.stringify({ branch }),
        }
      );

      return {
        success: true,
        deploymentId: result.id,
        url: result.url,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Deployment failed",
      };
    }
  }

  /**
   * Purge cache for a zone
   */
  async purgeCache(
    zoneId: string,
    options?: { purge_everything?: boolean; files?: string[] }
  ): Promise<boolean> {
    await this.request(`/zones/${zoneId}/purge_cache`, {
      method: "POST",
      body: JSON.stringify(options || { purge_everything: true }),
    });
    return true;
  }

  /**
   * Create a Cloudflare Tunnel
   */
  async createTunnel(
    name: string
  ): Promise<{ id: string; name: string; secret: string }> {
    if (!this.config.accountId) {
      throw new Error("Account ID required for Tunnels");
    }
    return this.request<{ id: string; name: string; secret: string }>(
      `/accounts/${this.config.accountId}/cfd_tunnel`,
      {
        method: "POST",
        body: JSON.stringify({
          name,
          tunnel_secret: Buffer.from(
            crypto.getRandomValues(new Uint8Array(32))
          ).toString("base64"),
        }),
      }
    );
  }

  /**
   * List Cloudflare Tunnels
   */
  async listTunnels(): Promise<
    Array<{ id: string; name: string; status: string }>
  > {
    if (!this.config.accountId) {
      throw new Error("Account ID required for Tunnels");
    }
    return this.request<Array<{ id: string; name: string; status: string }>>(
      `/accounts/${this.config.accountId}/cfd_tunnel`
    );
  }

  /**
   * Delete a Cloudflare Tunnel
   */
  async deleteTunnel(tunnelId: string): Promise<boolean> {
    if (!this.config.accountId) {
      throw new Error("Account ID required for Tunnels");
    }
    await this.request(
      `/accounts/${this.config.accountId}/cfd_tunnel/${tunnelId}`,
      {
        method: "DELETE",
      }
    );
    return true;
  }
}
