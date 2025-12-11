/**
 * DigitalOcean Platform Integration
 *
 * Provides Droplet, App Platform, and Spaces capabilities
 */

import type {
  Integration,
  IntegrationStatus,
  DigitalOceanConfig,
  DeploymentResult,
} from "./types.js";

const DO_API_URL = "https://api.digitalocean.com/v2";

interface DODroplet {
  id: number;
  name: string;
  status: string;
  memory: number;
  vcpus: number;
  disk: number;
  region: { slug: string; name: string };
  image: { id: number; name: string };
  networks: {
    v4: Array<{ ip_address: string; type: string }>;
    v6: Array<{ ip_address: string; type: string }>;
  };
}

interface DOApp {
  id: string;
  owner_uuid: string;
  spec: {
    name: string;
    region: string;
    services?: Array<{ name: string }>;
    static_sites?: Array<{ name: string }>;
  };
  default_ingress: string;
  active_deployment?: {
    id: string;
    phase: string;
  };
}

interface DOAppDeployment {
  id: string;
  phase: string;
  created_at: string;
  updated_at: string;
}

export class DigitalOceanClient implements Integration {
  private config: DigitalOceanConfig;
  private initialized = false;

  constructor(config: DigitalOceanConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    if (!this.config.token) {
      throw new Error("DigitalOcean token is required");
    }
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    try {
      const account = await this.getAccount();
      return {
        connected: true,
        healthy: true,
        lastCheck: new Date(),
        metadata: { email: account.email, status: account.status },
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
      throw new Error("DigitalOcean token not configured");
    }

    const response = await fetch(`${DO_API_URL}${path}`, {
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
        (error as { message?: string }).message || `DigitalOcean API error: ${response.status}`
      );
    }

    return response.json() as Promise<T>;
  }

  /**
   * Get account info
   */
  async getAccount(): Promise<{
    email: string;
    status: string;
    droplet_limit: number;
  }> {
    const result = await this.request<{
      account: { email: string; status: string; droplet_limit: number };
    }>("/account");
    return result.account;
  }

  /**
   * List all droplets
   */
  async listDroplets(): Promise<DODroplet[]> {
    const result = await this.request<{ droplets: DODroplet[] }>("/droplets");
    return result.droplets;
  }

  /**
   * Get droplet by ID
   */
  async getDroplet(dropletId: number): Promise<DODroplet> {
    const result = await this.request<{ droplet: DODroplet }>(
      `/droplets/${dropletId}`
    );
    return result.droplet;
  }

  /**
   * Create droplet
   */
  async createDroplet(options: {
    name: string;
    region: string;
    size: string;
    image: string | number;
    ssh_keys?: number[];
    user_data?: string;
    tags?: string[];
  }): Promise<DODroplet> {
    const result = await this.request<{ droplet: DODroplet }>("/droplets", {
      method: "POST",
      body: JSON.stringify(options),
    });
    return result.droplet;
  }

  /**
   * Delete droplet
   */
  async deleteDroplet(dropletId: number): Promise<boolean> {
    await this.request(`/droplets/${dropletId}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * Power cycle droplet
   */
  async powerCycleDroplet(dropletId: number): Promise<boolean> {
    await this.request(`/droplets/${dropletId}/actions`, {
      method: "POST",
      body: JSON.stringify({ type: "power_cycle" }),
    });
    return true;
  }

  /**
   * Reboot droplet
   */
  async rebootDroplet(dropletId: number): Promise<boolean> {
    await this.request(`/droplets/${dropletId}/actions`, {
      method: "POST",
      body: JSON.stringify({ type: "reboot" }),
    });
    return true;
  }

  /**
   * Shutdown droplet
   */
  async shutdownDroplet(dropletId: number): Promise<boolean> {
    await this.request(`/droplets/${dropletId}/actions`, {
      method: "POST",
      body: JSON.stringify({ type: "shutdown" }),
    });
    return true;
  }

  /**
   * Power on droplet
   */
  async powerOnDroplet(dropletId: number): Promise<boolean> {
    await this.request(`/droplets/${dropletId}/actions`, {
      method: "POST",
      body: JSON.stringify({ type: "power_on" }),
    });
    return true;
  }

  /**
   * List App Platform apps
   */
  async listApps(): Promise<DOApp[]> {
    const result = await this.request<{ apps: DOApp[] }>("/apps");
    return result.apps;
  }

  /**
   * Get App Platform app
   */
  async getApp(appId: string): Promise<DOApp> {
    const result = await this.request<{ app: DOApp }>(`/apps/${appId}`);
    return result.app;
  }

  /**
   * Create App Platform deployment
   */
  async createAppDeployment(appId: string): Promise<DeploymentResult> {
    try {
      const result = await this.request<{ deployment: DOAppDeployment }>(
        `/apps/${appId}/deployments`,
        {
          method: "POST",
          body: JSON.stringify({}),
        }
      );
      return {
        success: true,
        deploymentId: result.deployment.id,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : "Deployment failed",
      };
    }
  }

  /**
   * Get App Platform deployment
   */
  async getAppDeployment(
    appId: string,
    deploymentId: string
  ): Promise<DOAppDeployment> {
    const result = await this.request<{ deployment: DOAppDeployment }>(
      `/apps/${appId}/deployments/${deploymentId}`
    );
    return result.deployment;
  }

  /**
   * List SSH keys
   */
  async listSSHKeys(): Promise<
    Array<{ id: number; name: string; fingerprint: string }>
  > {
    const result = await this.request<{
      ssh_keys: Array<{ id: number; name: string; fingerprint: string }>;
    }>("/account/keys");
    return result.ssh_keys;
  }

  /**
   * Add SSH key
   */
  async addSSHKey(
    name: string,
    publicKey: string
  ): Promise<{ id: number; fingerprint: string }> {
    const result = await this.request<{
      ssh_key: { id: number; fingerprint: string };
    }>("/account/keys", {
      method: "POST",
      body: JSON.stringify({ name, public_key: publicKey }),
    });
    return result.ssh_key;
  }

  /**
   * List regions
   */
  async listRegions(): Promise<
    Array<{ slug: string; name: string; available: boolean }>
  > {
    const result = await this.request<{
      regions: Array<{ slug: string; name: string; available: boolean }>;
    }>("/regions");
    return result.regions;
  }

  /**
   * List sizes
   */
  async listSizes(): Promise<
    Array<{
      slug: string;
      memory: number;
      vcpus: number;
      disk: number;
      price_monthly: number;
    }>
  > {
    const result = await this.request<{
      sizes: Array<{
        slug: string;
        memory: number;
        vcpus: number;
        disk: number;
        price_monthly: number;
      }>;
    }>("/sizes");
    return result.sizes;
  }
}
