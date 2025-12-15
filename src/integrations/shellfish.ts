/**
 * Shellfish SSH Client Integration
 *
 * Provides integration with Shellfish (iOS SSH client) for mobile device management.
 * Shellfish uses x-callback-url scheme for automation.
 */

import type {
  Integration,
  IntegrationStatus,
  ShellfishConfig,
} from "./types.js";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";

interface ShellfishHost {
  name: string;
  hostname: string;
  port: number;
  username: string;
  authMethod: "password" | "key" | "agent";
  keyPath?: string;
}

interface ShellfishSnippet {
  name: string;
  command: string;
  description?: string;
}

export class ShellfishClient implements Integration {
  private config: ShellfishConfig;
  private initialized = false;
  private configPath: string;

  constructor(config: ShellfishConfig) {
    this.config = config;
    this.configPath =
      config.configPath ||
      path.join(os.homedir(), ".config", "blackroad", "shellfish");
  }

  async initialize(): Promise<void> {
    // Create config directory if it doesn't exist
    if (!fs.existsSync(this.configPath)) {
      fs.mkdirSync(this.configPath, { recursive: true });
    }
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    return {
      connected: true,
      healthy: true,
      lastCheck: new Date(),
      metadata: {
        configPath: this.configPath,
        platform: "ios",
      },
    };
  }

  async cleanup(): Promise<void> {
    this.initialized = false;
  }

  /**
   * Generate Shellfish x-callback URL for SSH connection
   */
  generateConnectURL(host: ShellfishHost): string {
    const params = new URLSearchParams({
      host: host.hostname,
      port: String(host.port),
      user: host.username,
    });

    if (host.keyPath) {
      params.set("key", host.keyPath);
    }

    return `shellfish://connect?${params.toString()}`;
  }

  /**
   * Generate Shellfish x-callback URL for running a command
   */
  generateCommandURL(host: ShellfishHost, command: string): string {
    const params = new URLSearchParams({
      host: host.hostname,
      port: String(host.port),
      user: host.username,
      command: command,
    });

    return `shellfish://run?${params.toString()}`;
  }

  /**
   * Generate Shellfish x-callback URL for SFTP transfer
   */
  generateSFTPURL(
    host: ShellfishHost,
    remotePath: string,
    action: "download" | "upload"
  ): string {
    const params = new URLSearchParams({
      host: host.hostname,
      port: String(host.port),
      user: host.username,
      path: remotePath,
      action: action,
    });

    return `shellfish://sftp?${params.toString()}`;
  }

  /**
   * Save host configuration for syncing to iOS
   */
  async saveHost(host: ShellfishHost): Promise<boolean> {
    const hostsFile = path.join(this.configPath, "hosts.json");
    let hosts: ShellfishHost[] = [];

    if (fs.existsSync(hostsFile)) {
      hosts = JSON.parse(fs.readFileSync(hostsFile, "utf-8"));
    }

    // Update or add host
    const existingIndex = hosts.findIndex((h) => h.name === host.name);
    if (existingIndex >= 0) {
      hosts[existingIndex] = host;
    } else {
      hosts.push(host);
    }

    fs.writeFileSync(hostsFile, JSON.stringify(hosts, null, 2));
    return true;
  }

  /**
   * Get all saved hosts
   */
  async getHosts(): Promise<ShellfishHost[]> {
    const hostsFile = path.join(this.configPath, "hosts.json");
    if (!fs.existsSync(hostsFile)) {
      return [];
    }
    return JSON.parse(fs.readFileSync(hostsFile, "utf-8"));
  }

  /**
   * Remove a host
   */
  async removeHost(hostName: string): Promise<boolean> {
    const hostsFile = path.join(this.configPath, "hosts.json");
    if (!fs.existsSync(hostsFile)) {
      return false;
    }

    const hosts: ShellfishHost[] = JSON.parse(
      fs.readFileSync(hostsFile, "utf-8")
    );
    const newHosts = hosts.filter((h) => h.name !== hostName);

    if (newHosts.length === hosts.length) {
      return false;
    }

    fs.writeFileSync(hostsFile, JSON.stringify(newHosts, null, 2));
    return true;
  }

  /**
   * Save command snippet
   */
  async saveSnippet(snippet: ShellfishSnippet): Promise<boolean> {
    const snippetsFile = path.join(this.configPath, "snippets.json");
    let snippets: ShellfishSnippet[] = [];

    if (fs.existsSync(snippetsFile)) {
      snippets = JSON.parse(fs.readFileSync(snippetsFile, "utf-8"));
    }

    // Update or add snippet
    const existingIndex = snippets.findIndex((s) => s.name === snippet.name);
    if (existingIndex >= 0) {
      snippets[existingIndex] = snippet;
    } else {
      snippets.push(snippet);
    }

    fs.writeFileSync(snippetsFile, JSON.stringify(snippets, null, 2));
    return true;
  }

  /**
   * Get all snippets
   */
  async getSnippets(): Promise<ShellfishSnippet[]> {
    const snippetsFile = path.join(this.configPath, "snippets.json");
    if (!fs.existsSync(snippetsFile)) {
      return [];
    }
    return JSON.parse(fs.readFileSync(snippetsFile, "utf-8"));
  }

  /**
   * Generate QR code data for easy import to Shellfish
   */
  generateQRCodeData(host: ShellfishHost): string {
    return JSON.stringify({
      type: "shellfish-host",
      ...host,
    });
  }

  /**
   * Create BlackRoad Pi hosts configuration
   */
  async setupBlackRoadPiHosts(
    hosts: Array<{ name: string; ip: string }>
  ): Promise<boolean> {
    for (const host of hosts) {
      await this.saveHost({
        name: host.name,
        hostname: host.ip,
        port: 22,
        username: "pi",
        authMethod: "key",
        keyPath: "~/.ssh/id_rsa",
      });
    }

    // Add common snippets
    const snippets: ShellfishSnippet[] = [
      {
        name: "Check Status",
        command: "systemctl status blackroad-agent",
        description: "Check BlackRoad agent status",
      },
      {
        name: "View Logs",
        command: "journalctl -u blackroad-agent -f",
        description: "Stream BlackRoad agent logs",
      },
      {
        name: "Restart Agent",
        command: "sudo systemctl restart blackroad-agent",
        description: "Restart the BlackRoad agent",
      },
      {
        name: "System Info",
        command: "vcgencmd measure_temp && free -h && df -h /",
        description: "Show system temperature, memory, and disk",
      },
    ];

    for (const snippet of snippets) {
      await this.saveSnippet(snippet);
    }

    return true;
  }
}
