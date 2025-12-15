/**
 * Raspberry Pi Fleet Integration
 *
 * Provides SSH-based management for Raspberry Pi devices
 */

import type {
  Integration,
  IntegrationStatus,
  RaspberryPiConfig,
} from "./types.js";
import { spawn } from "child_process";
import * as fs from "fs";
import * as os from "os";
import * as path from "path";

interface PiDevice {
  host: string;
  user: string;
  connected: boolean;
  hostname?: string;
  model?: string;
  memory?: number;
  cpuTemp?: number;
  uptime?: number;
  diskUsage?: number;
}

interface CommandResult {
  exitCode: number;
  stdout: string;
  stderr: string;
}

export class RaspberryPiClient implements Integration {
  private config: RaspberryPiConfig;
  private initialized = false;
  private devices: Map<string, PiDevice> = new Map();

  constructor(config: RaspberryPiConfig) {
    this.config = {
      hosts: config.hosts || [],
      user: config.user || "pi",
      sshKey: config.sshKey,
    };
  }

  async initialize(): Promise<void> {
    if (!this.config.hosts?.length) {
      throw new Error("No Raspberry Pi hosts configured");
    }

    // Setup SSH key if provided
    if (this.config.sshKey) {
      await this.setupSSHKey();
    }

    // Initialize device map
    for (const host of this.config.hosts) {
      this.devices.set(host, {
        host,
        user: this.config.user || "pi",
        connected: false,
      });
    }

    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    try {
      const connectedCount = await this.probeDevices();
      return {
        connected: connectedCount > 0,
        healthy: connectedCount === this.devices.size,
        lastCheck: new Date(),
        metadata: {
          totalDevices: this.devices.size,
          connectedDevices: connectedCount,
          devices: Array.from(this.devices.values()),
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
    this.devices.clear();
    this.initialized = false;
  }

  private async setupSSHKey(): Promise<void> {
    if (!this.config.sshKey) return;

    const sshDir = path.join(os.homedir(), ".ssh");
    const keyPath = path.join(sshDir, "blackroad_pi_key");

    // Ensure .ssh directory exists
    if (!fs.existsSync(sshDir)) {
      fs.mkdirSync(sshDir, { mode: 0o700 });
    }

    // Write key file
    fs.writeFileSync(keyPath, this.config.sshKey, { mode: 0o600 });
  }

  private getSSHKeyPath(): string | undefined {
    if (this.config.sshKey) {
      return path.join(os.homedir(), ".ssh", "blackroad_pi_key");
    }
    return undefined;
  }

  /**
   * Execute SSH command on a device
   */
  async sshExec(host: string, command: string): Promise<CommandResult> {
    return new Promise((resolve) => {
      const args = ["-o", "StrictHostKeyChecking=no", "-o", "BatchMode=yes"];

      const keyPath = this.getSSHKeyPath();
      if (keyPath) {
        args.push("-i", keyPath);
      }

      const user = this.config.user || "pi";
      args.push(`${user}@${host}`, command);

      const child = spawn("ssh", args, {
        timeout: 30000,
      });

      let stdout = "";
      let stderr = "";

      child.stdout.on("data", (data) => {
        stdout += data.toString();
      });

      child.stderr.on("data", (data) => {
        stderr += data.toString();
      });

      child.on("close", (code) => {
        resolve({
          exitCode: code || 0,
          stdout: stdout.trim(),
          stderr: stderr.trim(),
        });
      });

      child.on("error", (err) => {
        resolve({
          exitCode: 1,
          stdout: "",
          stderr: err.message,
        });
      });
    });
  }

  /**
   * Probe all devices for connectivity
   */
  async probeDevices(): Promise<number> {
    let connectedCount = 0;

    for (const [host, device] of this.devices) {
      const result = await this.sshExec(host, "hostname");
      device.connected = result.exitCode === 0;
      if (device.connected) {
        device.hostname = result.stdout;
        connectedCount++;
      }
    }

    return connectedCount;
  }

  /**
   * Get device info
   */
  async getDeviceInfo(host: string): Promise<PiDevice> {
    const device = this.devices.get(host);
    if (!device) {
      throw new Error(`Device ${host} not found`);
    }

    // Get hostname
    const hostnameResult = await this.sshExec(host, "hostname");
    if (hostnameResult.exitCode === 0) {
      device.hostname = hostnameResult.stdout;
      device.connected = true;
    } else {
      device.connected = false;
      return device;
    }

    // Get model
    const modelResult = await this.sshExec(
      host,
      "cat /proc/device-tree/model 2>/dev/null || echo 'Unknown'"
    );
    device.model = modelResult.stdout.replace(/\0/g, "");

    // Get memory
    const memResult = await this.sshExec(
      host,
      "free -b | awk '/Mem:/ {print $2}'"
    );
    device.memory = parseInt(memResult.stdout, 10) || 0;

    // Get CPU temperature
    const tempResult = await this.sshExec(
      host,
      "cat /sys/class/thermal/thermal_zone0/temp 2>/dev/null || echo '0'"
    );
    device.cpuTemp = parseInt(tempResult.stdout, 10) / 1000;

    // Get uptime
    const uptimeResult = await this.sshExec(host, "cat /proc/uptime");
    device.uptime = parseFloat(uptimeResult.stdout.split(" ")[0]) || 0;

    // Get disk usage
    const diskResult = await this.sshExec(
      host,
      "df / | awk 'NR==2 {print $5}' | tr -d '%'"
    );
    device.diskUsage = parseInt(diskResult.stdout, 10) || 0;

    return device;
  }

  /**
   * Get all devices
   */
  async getAllDevices(): Promise<PiDevice[]> {
    const devices: PiDevice[] = [];
    for (const host of this.devices.keys()) {
      devices.push(await this.getDeviceInfo(host));
    }
    return devices;
  }

  /**
   * Run command on device
   */
  async runCommand(host: string, command: string): Promise<CommandResult> {
    return this.sshExec(host, command);
  }

  /**
   * Run command on all devices
   */
  async runCommandAll(
    command: string
  ): Promise<Map<string, CommandResult>> {
    const results = new Map<string, CommandResult>();
    for (const host of this.devices.keys()) {
      results.set(host, await this.sshExec(host, command));
    }
    return results;
  }

  /**
   * Reboot device
   */
  async reboot(host: string): Promise<boolean> {
    const result = await this.sshExec(host, "sudo reboot");
    return result.exitCode === 0 || result.stderr.includes("Connection");
  }

  /**
   * Shutdown device
   */
  async shutdown(host: string): Promise<boolean> {
    const result = await this.sshExec(host, "sudo shutdown -h now");
    return result.exitCode === 0 || result.stderr.includes("Connection");
  }

  /**
   * Update system packages
   */
  async updatePackages(host: string): Promise<CommandResult> {
    return this.sshExec(
      host,
      "sudo apt-get update && sudo apt-get upgrade -y"
    );
  }

  /**
   * Install package
   */
  async installPackage(host: string, packageName: string): Promise<boolean> {
    const result = await this.sshExec(
      host,
      `sudo apt-get install -y ${packageName}`
    );
    return result.exitCode === 0;
  }

  /**
   * Copy file to device
   */
  async copyFile(
    host: string,
    localPath: string,
    remotePath: string
  ): Promise<boolean> {
    return new Promise((resolve) => {
      const args = ["-o", "StrictHostKeyChecking=no"];

      const keyPath = this.getSSHKeyPath();
      if (keyPath) {
        args.push("-i", keyPath);
      }

      const user = this.config.user || "pi";
      args.push(localPath, `${user}@${host}:${remotePath}`);

      const child = spawn("scp", args);

      child.on("close", (code) => {
        resolve(code === 0);
      });

      child.on("error", () => {
        resolve(false);
      });
    });
  }

  /**
   * Get file from device
   */
  async getFile(
    host: string,
    remotePath: string,
    localPath: string
  ): Promise<boolean> {
    return new Promise((resolve) => {
      const args = ["-o", "StrictHostKeyChecking=no"];

      const keyPath = this.getSSHKeyPath();
      if (keyPath) {
        args.push("-i", keyPath);
      }

      const user = this.config.user || "pi";
      args.push(`${user}@${host}:${remotePath}`, localPath);

      const child = spawn("scp", args);

      child.on("close", (code) => {
        resolve(code === 0);
      });

      child.on("error", () => {
        resolve(false);
      });
    });
  }

  /**
   * Deploy agent to device
   */
  async deployAgent(host: string, agentPath: string): Promise<boolean> {
    // Copy agent files
    const copyResult = await this.copyFile(
      host,
      agentPath,
      "/home/pi/blackroad-agent/"
    );
    if (!copyResult) return false;

    // Install dependencies and start agent
    const installResult = await this.sshExec(
      host,
      "cd /home/pi/blackroad-agent && pip install -r requirements.txt && sudo systemctl restart blackroad-agent"
    );

    return installResult.exitCode === 0;
  }

  /**
   * Get agent status on device
   */
  async getAgentStatus(
    host: string
  ): Promise<{ running: boolean; uptime?: number }> {
    const result = await this.sshExec(
      host,
      "systemctl is-active blackroad-agent && systemctl show blackroad-agent --property=ActiveEnterTimestamp"
    );

    const running = result.stdout.includes("active");
    let uptime: number | undefined;

    if (running) {
      const match = result.stdout.match(/ActiveEnterTimestamp=(.+)/);
      if (match) {
        const startTime = new Date(match[1]).getTime();
        uptime = (Date.now() - startTime) / 1000;
      }
    }

    return { running, uptime };
  }

  /**
   * Enable GPIO pin
   */
  async gpioSetup(
    host: string,
    pin: number,
    mode: "in" | "out"
  ): Promise<boolean> {
    const direction = mode === "out" ? "out" : "in";
    const result = await this.sshExec(
      host,
      `echo ${pin} | sudo tee /sys/class/gpio/export && echo ${direction} | sudo tee /sys/class/gpio/gpio${pin}/direction`
    );
    return result.exitCode === 0;
  }

  /**
   * Set GPIO pin value
   */
  async gpioWrite(host: string, pin: number, value: 0 | 1): Promise<boolean> {
    const result = await this.sshExec(
      host,
      `echo ${value} | sudo tee /sys/class/gpio/gpio${pin}/value`
    );
    return result.exitCode === 0;
  }

  /**
   * Read GPIO pin value
   */
  async gpioRead(host: string, pin: number): Promise<0 | 1> {
    const result = await this.sshExec(
      host,
      `cat /sys/class/gpio/gpio${pin}/value`
    );
    return parseInt(result.stdout, 10) === 1 ? 1 : 0;
  }
}
