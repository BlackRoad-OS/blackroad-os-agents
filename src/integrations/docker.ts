/**
 * Docker Platform Integration
 *
 * Provides container management capabilities via Docker Engine API
 */

import type {
  Integration,
  IntegrationStatus,
  DockerConfig,
} from "./types.js";

interface DockerContainer {
  Id: string;
  Names: string[];
  Image: string;
  State: string;
  Status: string;
  Ports: Array<{
    IP?: string;
    PrivatePort: number;
    PublicPort?: number;
    Type: string;
  }>;
  Created: number;
}

interface DockerImage {
  Id: string;
  RepoTags: string[];
  Created: number;
  Size: number;
}

interface DockerNetwork {
  Id: string;
  Name: string;
  Driver: string;
  Scope: string;
}

interface DockerVolume {
  Name: string;
  Driver: string;
  Mountpoint: string;
  CreatedAt: string;
}

export class DockerClient implements Integration {
  private config: DockerConfig;
  private initialized = false;

  constructor(config: DockerConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    // Verify Docker socket is accessible
    try {
      await this.getVersion();
      this.initialized = true;
    } catch (error) {
      throw new Error(
        `Cannot connect to Docker: ${error instanceof Error ? error.message : "Unknown error"}`
      );
    }
  }

  async getStatus(): Promise<IntegrationStatus> {
    try {
      const version = await this.getVersion();
      const info = await this.getInfo();
      return {
        connected: true,
        healthy: true,
        lastCheck: new Date(),
        metadata: {
          version: version.Version,
          containers: info.Containers,
          images: info.Images,
        },
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
    const socketPath = this.config.socketPath || "/var/run/docker.sock";

    // For Unix sockets, we need to use a special approach
    // In Node.js environments, use the http module with socketPath
    // For now, we'll use fetch with a localhost fallback for Docker API access
    const baseUrl = this.config.host
      ? `http://${this.config.host}:${this.config.port || 2375}`
      : "http://localhost:2375";

    const response = await fetch(`${baseUrl}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(
        (error as { message?: string }).message || `Docker API error: ${response.status}`
      );
    }

    return response.json() as Promise<T>;
  }

  /**
   * Get Docker version
   */
  async getVersion(): Promise<{
    Version: string;
    ApiVersion: string;
    Os: string;
    Arch: string;
  }> {
    return this.request<{
      Version: string;
      ApiVersion: string;
      Os: string;
      Arch: string;
    }>("/version");
  }

  /**
   * Get Docker system info
   */
  async getInfo(): Promise<{
    Containers: number;
    ContainersRunning: number;
    ContainersPaused: number;
    ContainersStopped: number;
    Images: number;
    MemTotal: number;
    NCPU: number;
  }> {
    return this.request<{
      Containers: number;
      ContainersRunning: number;
      ContainersPaused: number;
      ContainersStopped: number;
      Images: number;
      MemTotal: number;
      NCPU: number;
    }>("/info");
  }

  /**
   * List containers
   */
  async listContainers(all = false): Promise<DockerContainer[]> {
    return this.request<DockerContainer[]>(`/containers/json?all=${all}`);
  }

  /**
   * Get container details
   */
  async getContainer(containerId: string): Promise<{
    Id: string;
    Name: string;
    State: { Status: string; Running: boolean };
    Config: { Image: string; Env: string[] };
  }> {
    return this.request(`/containers/${containerId}/json`);
  }

  /**
   * Create container
   */
  async createContainer(options: {
    name?: string;
    Image: string;
    Cmd?: string[];
    Env?: string[];
    ExposedPorts?: Record<string, Record<string, never>>;
    HostConfig?: {
      PortBindings?: Record<string, Array<{ HostPort: string }>>;
      Binds?: string[];
      RestartPolicy?: { Name: string; MaximumRetryCount?: number };
    };
  }): Promise<{ Id: string; Warnings: string[] }> {
    const params = options.name ? `?name=${options.name}` : "";
    return this.request(`/containers/create${params}`, {
      method: "POST",
      body: JSON.stringify(options),
    });
  }

  /**
   * Start container
   */
  async startContainer(containerId: string): Promise<boolean> {
    await this.request(`/containers/${containerId}/start`, {
      method: "POST",
    });
    return true;
  }

  /**
   * Stop container
   */
  async stopContainer(containerId: string, timeout = 10): Promise<boolean> {
    await this.request(`/containers/${containerId}/stop?t=${timeout}`, {
      method: "POST",
    });
    return true;
  }

  /**
   * Restart container
   */
  async restartContainer(containerId: string, timeout = 10): Promise<boolean> {
    await this.request(`/containers/${containerId}/restart?t=${timeout}`, {
      method: "POST",
    });
    return true;
  }

  /**
   * Kill container
   */
  async killContainer(
    containerId: string,
    signal = "SIGKILL"
  ): Promise<boolean> {
    await this.request(`/containers/${containerId}/kill?signal=${signal}`, {
      method: "POST",
    });
    return true;
  }

  /**
   * Remove container
   */
  async removeContainer(
    containerId: string,
    options?: { force?: boolean; v?: boolean }
  ): Promise<boolean> {
    const params = new URLSearchParams();
    if (options?.force) params.set("force", "true");
    if (options?.v) params.set("v", "true");
    await this.request(`/containers/${containerId}?${params}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * Get container logs
   */
  async getContainerLogs(
    containerId: string,
    options?: { stdout?: boolean; stderr?: boolean; tail?: number }
  ): Promise<string> {
    const params = new URLSearchParams();
    params.set("stdout", String(options?.stdout ?? true));
    params.set("stderr", String(options?.stderr ?? true));
    if (options?.tail) params.set("tail", String(options.tail));

    const response = await fetch(
      `http://localhost:2375/containers/${containerId}/logs?${params}`
    );
    return response.text();
  }

  /**
   * List images
   */
  async listImages(): Promise<DockerImage[]> {
    return this.request<DockerImage[]>("/images/json");
  }

  /**
   * Pull image
   */
  async pullImage(image: string, tag = "latest"): Promise<boolean> {
    await this.request(`/images/create?fromImage=${image}&tag=${tag}`, {
      method: "POST",
    });
    return true;
  }

  /**
   * Remove image
   */
  async removeImage(imageId: string, force = false): Promise<boolean> {
    await this.request(`/images/${imageId}?force=${force}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * List networks
   */
  async listNetworks(): Promise<DockerNetwork[]> {
    return this.request<DockerNetwork[]>("/networks");
  }

  /**
   * Create network
   */
  async createNetwork(
    name: string,
    driver = "bridge"
  ): Promise<{ Id: string }> {
    return this.request<{ Id: string }>("/networks/create", {
      method: "POST",
      body: JSON.stringify({ Name: name, Driver: driver }),
    });
  }

  /**
   * Remove network
   */
  async removeNetwork(networkId: string): Promise<boolean> {
    await this.request(`/networks/${networkId}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * List volumes
   */
  async listVolumes(): Promise<{ Volumes: DockerVolume[] }> {
    return this.request<{ Volumes: DockerVolume[] }>("/volumes");
  }

  /**
   * Create volume
   */
  async createVolume(name: string): Promise<DockerVolume> {
    return this.request<DockerVolume>("/volumes/create", {
      method: "POST",
      body: JSON.stringify({ Name: name }),
    });
  }

  /**
   * Remove volume
   */
  async removeVolume(volumeName: string, force = false): Promise<boolean> {
    await this.request(`/volumes/${volumeName}?force=${force}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * Execute command in container
   */
  async execCreate(
    containerId: string,
    cmd: string[],
    options?: { AttachStdout?: boolean; AttachStderr?: boolean }
  ): Promise<{ Id: string }> {
    return this.request<{ Id: string }>(`/containers/${containerId}/exec`, {
      method: "POST",
      body: JSON.stringify({
        Cmd: cmd,
        AttachStdout: options?.AttachStdout ?? true,
        AttachStderr: options?.AttachStderr ?? true,
      }),
    });
  }

  /**
   * Start exec instance
   */
  async execStart(execId: string): Promise<string> {
    const response = await fetch(`http://localhost:2375/exec/${execId}/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ Detach: false }),
    });
    return response.text();
  }

  /**
   * Prune unused resources
   */
  async prune(
    type: "containers" | "images" | "volumes" | "networks"
  ): Promise<{ SpaceReclaimed?: number }> {
    return this.request<{ SpaceReclaimed?: number }>(`/${type}/prune`, {
      method: "POST",
    });
  }
}
