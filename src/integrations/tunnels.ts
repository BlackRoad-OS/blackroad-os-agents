/**
 * Tunnel Services Integration
 *
 * Provides secure tunneling capabilities via Cloudflare Tunnel and ngrok
 */

import type {
  Integration,
  IntegrationStatus,
  TunnelConfig,
} from "./types.js";
import { spawn, ChildProcess } from "child_process";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";

interface TunnelStatus {
  provider: "cloudflare" | "ngrok";
  url: string;
  localPort: number;
  status: "connected" | "connecting" | "disconnected" | "error";
  startedAt?: Date;
  error?: string;
}

interface CloudflareTunnelInfo {
  id: string;
  name: string;
  status: string;
  connections: Array<{
    connectorId: string;
    originIP: string;
    isActive: boolean;
  }>;
}

interface NgrokTunnelInfo {
  public_url: string;
  proto: string;
  config: {
    addr: string;
    inspect: boolean;
  };
}

export class TunnelClient implements Integration {
  private config: TunnelConfig;
  private initialized = false;
  private activeTunnels: Map<string, { process: ChildProcess; status: TunnelStatus }> = new Map();
  private configDir: string;

  constructor(config: TunnelConfig) {
    this.config = config;
    this.configDir = path.join(os.homedir(), ".config", "blackroad", "tunnels");
  }

  async initialize(): Promise<void> {
    if (!fs.existsSync(this.configDir)) {
      fs.mkdirSync(this.configDir, { recursive: true });
    }
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    const tunnels = Array.from(this.activeTunnels.values()).map((t) => t.status);
    const hasCloudflare = !!this.config.cloudflareToken;
    const hasNgrok = !!this.config.ngrokToken;

    return {
      connected: tunnels.some((t) => t.status === "connected"),
      healthy: tunnels.every((t) => t.status !== "error"),
      lastCheck: new Date(),
      metadata: {
        activeTunnels: tunnels.length,
        providers: {
          cloudflare: hasCloudflare,
          ngrok: hasNgrok,
        },
        tunnels,
      },
    };
  }

  async cleanup(): Promise<void> {
    // Stop all active tunnels
    for (const [id] of this.activeTunnels) {
      await this.stopTunnel(id);
    }
    this.initialized = false;
  }

  /**
   * Start a Cloudflare Tunnel
   */
  async startCloudflareTunnel(options: {
    name: string;
    localPort: number;
    hostname?: string;
  }): Promise<TunnelStatus> {
    if (!this.config.cloudflareToken) {
      throw new Error("Cloudflare tunnel token is required");
    }

    const tunnelId = `cf-${options.name}-${options.localPort}`;

    // Check if cloudflared is installed
    const cloudflaredPath = await this.findExecutable("cloudflared");
    if (!cloudflaredPath) {
      throw new Error("cloudflared is not installed");
    }

    const status: TunnelStatus = {
      provider: "cloudflare",
      url: "",
      localPort: options.localPort,
      status: "connecting",
      startedAt: new Date(),
    };

    const args = [
      "tunnel",
      "--url",
      `http://localhost:${options.localPort}`,
    ];

    if (options.hostname) {
      args.push("--hostname", options.hostname);
    }

    const process = spawn(cloudflaredPath, args, {
      env: {
        ...process.env,
        TUNNEL_TOKEN: this.config.cloudflareToken,
      },
    });

    let url = "";

    process.stdout.on("data", (data: Buffer) => {
      const line = data.toString();
      // Parse URL from cloudflared output
      const urlMatch = line.match(/https:\/\/[^\s]+\.trycloudflare\.com/);
      if (urlMatch) {
        url = urlMatch[0];
        status.url = url;
        status.status = "connected";
      }
    });

    process.stderr.on("data", (data: Buffer) => {
      const line = data.toString();
      // Also check stderr for URL
      const urlMatch = line.match(/https:\/\/[^\s]+\.trycloudflare\.com/);
      if (urlMatch) {
        url = urlMatch[0];
        status.url = url;
        status.status = "connected";
      }
    });

    process.on("exit", (code) => {
      status.status = code === 0 ? "disconnected" : "error";
      if (code !== 0) {
        status.error = `Process exited with code ${code}`;
      }
      this.activeTunnels.delete(tunnelId);
    });

    process.on("error", (err) => {
      status.status = "error";
      status.error = err.message;
    });

    this.activeTunnels.set(tunnelId, { process, status });

    // Wait for connection
    await new Promise<void>((resolve) => {
      const checkInterval = setInterval(() => {
        if (status.status === "connected" || status.status === "error") {
          clearInterval(checkInterval);
          resolve();
        }
      }, 500);

      // Timeout after 30 seconds
      setTimeout(() => {
        clearInterval(checkInterval);
        if (status.status === "connecting") {
          status.status = "error";
          status.error = "Connection timeout";
        }
        resolve();
      }, 30000);
    });

    return status;
  }

  /**
   * Start an ngrok tunnel
   */
  async startNgrokTunnel(options: {
    name: string;
    localPort: number;
    subdomain?: string;
    region?: "us" | "eu" | "ap" | "au" | "sa" | "jp" | "in";
  }): Promise<TunnelStatus> {
    if (!this.config.ngrokToken) {
      throw new Error("ngrok auth token is required");
    }

    const tunnelId = `ngrok-${options.name}-${options.localPort}`;

    // Check if ngrok is installed
    const ngrokPath = await this.findExecutable("ngrok");
    if (!ngrokPath) {
      throw new Error("ngrok is not installed");
    }

    const status: TunnelStatus = {
      provider: "ngrok",
      url: "",
      localPort: options.localPort,
      status: "connecting",
      startedAt: new Date(),
    };

    // Set auth token first
    const authProcess = spawn(ngrokPath, ["config", "add-authtoken", this.config.ngrokToken]);
    await new Promise<void>((resolve) => {
      authProcess.on("exit", () => resolve());
    });

    const args = ["http", String(options.localPort)];

    if (options.subdomain) {
      args.push("--subdomain", options.subdomain);
    }

    if (options.region) {
      args.push("--region", options.region);
    }

    const process = spawn(ngrokPath, args);

    process.stdout.on("data", (data: Buffer) => {
      const line = data.toString();
      // Parse URL from ngrok output
      const urlMatch = line.match(/https:\/\/[^\s]+\.ngrok[^\s]*/);
      if (urlMatch) {
        status.url = urlMatch[0];
        status.status = "connected";
      }
    });

    process.stderr.on("data", (data: Buffer) => {
      const line = data.toString();
      if (line.includes("ERR")) {
        status.status = "error";
        status.error = line;
      }
    });

    process.on("exit", (code) => {
      status.status = code === 0 ? "disconnected" : "error";
      if (code !== 0) {
        status.error = `Process exited with code ${code}`;
      }
      this.activeTunnels.delete(tunnelId);
    });

    process.on("error", (err) => {
      status.status = "error";
      status.error = err.message;
    });

    this.activeTunnels.set(tunnelId, { process, status });

    // Wait for connection and get URL from API
    await new Promise((resolve) => setTimeout(resolve, 3000));

    // Try to get URL from ngrok API
    try {
      const response = await fetch("http://127.0.0.1:4040/api/tunnels");
      if (response.ok) {
        const data = (await response.json()) as { tunnels: NgrokTunnelInfo[] };
        const tunnel = data.tunnels.find(
          (t) => t.config.addr === `http://localhost:${options.localPort}`
        );
        if (tunnel) {
          status.url = tunnel.public_url;
          status.status = "connected";
        }
      }
    } catch {
      // API not available yet, might still be starting
    }

    return status;
  }

  /**
   * Stop a tunnel
   */
  async stopTunnel(tunnelId: string): Promise<boolean> {
    const tunnel = this.activeTunnels.get(tunnelId);
    if (!tunnel) {
      return false;
    }

    tunnel.process.kill("SIGTERM");
    this.activeTunnels.delete(tunnelId);
    return true;
  }

  /**
   * Stop all tunnels
   */
  async stopAllTunnels(): Promise<number> {
    let count = 0;
    for (const [id] of this.activeTunnels) {
      if (await this.stopTunnel(id)) {
        count++;
      }
    }
    return count;
  }

  /**
   * List active tunnels
   */
  listTunnels(): TunnelStatus[] {
    return Array.from(this.activeTunnels.values()).map((t) => t.status);
  }

  /**
   * Get tunnel by ID
   */
  getTunnel(tunnelId: string): TunnelStatus | null {
    const tunnel = this.activeTunnels.get(tunnelId);
    return tunnel?.status || null;
  }

  /**
   * Find executable in PATH
   */
  private async findExecutable(name: string): Promise<string | null> {
    const isWindows = os.platform() === "win32";
    const pathVar = process.env.PATH || "";
    const pathDirs = pathVar.split(isWindows ? ";" : ":");

    for (const dir of pathDirs) {
      const fullPath = path.join(dir, isWindows ? `${name}.exe` : name);
      if (fs.existsSync(fullPath)) {
        return fullPath;
      }
    }

    // Check common installation paths
    const commonPaths = isWindows
      ? [
          `C:\\Program Files\\${name}\\${name}.exe`,
          `C:\\Program Files (x86)\\${name}\\${name}.exe`,
        ]
      : [
          `/usr/local/bin/${name}`,
          `/usr/bin/${name}`,
          `/opt/homebrew/bin/${name}`,
          path.join(os.homedir(), `.local/bin/${name}`),
        ];

    for (const p of commonPaths) {
      if (fs.existsSync(p)) {
        return p;
      }
    }

    return null;
  }

  /**
   * Quick tunnel - start the fastest available tunnel
   */
  async quickTunnel(
    localPort: number
  ): Promise<TunnelStatus> {
    // Prefer Cloudflare if configured (free quick tunnels)
    if (this.config.cloudflareToken) {
      return this.startCloudflareTunnel({
        name: "quick",
        localPort,
      });
    }

    // Fall back to ngrok
    if (this.config.ngrokToken) {
      return this.startNgrokTunnel({
        name: "quick",
        localPort,
      });
    }

    throw new Error("No tunnel provider configured");
  }

  /**
   * Create SSH tunnel (for advanced use cases)
   */
  async createSSHTunnel(options: {
    localPort: number;
    remoteHost: string;
    remotePort: number;
    sshHost: string;
    sshUser?: string;
    sshKey?: string;
  }): Promise<TunnelStatus> {
    const tunnelId = `ssh-${options.localPort}-${options.remotePort}`;

    const status: TunnelStatus = {
      provider: "cloudflare", // Using cloudflare as placeholder for SSH
      url: `ssh://${options.sshHost}:${options.remotePort}`,
      localPort: options.localPort,
      status: "connecting",
      startedAt: new Date(),
    };

    const args = [
      "-N",
      "-L",
      `${options.localPort}:${options.remoteHost}:${options.remotePort}`,
    ];

    if (options.sshKey) {
      args.push("-i", options.sshKey);
    }

    const user = options.sshUser || "root";
    args.push(`${user}@${options.sshHost}`);

    const process = spawn("ssh", args);

    process.on("exit", (code) => {
      status.status = code === 0 ? "disconnected" : "error";
      this.activeTunnels.delete(tunnelId);
    });

    process.on("error", (err) => {
      status.status = "error";
      status.error = err.message;
    });

    // SSH tunnels are ready immediately if they don't error
    await new Promise((resolve) => setTimeout(resolve, 2000));
    if (status.status === "connecting") {
      status.status = "connected";
    }

    this.activeTunnels.set(tunnelId, { process, status });
    return status;
  }
}
