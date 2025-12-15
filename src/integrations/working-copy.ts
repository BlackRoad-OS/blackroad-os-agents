/**
 * Working Copy Integration
 *
 * Provides integration with Working Copy (iOS Git client) for mobile Git operations.
 * Working Copy uses x-callback-url scheme for automation.
 */

import type {
  Integration,
  IntegrationStatus,
  WorkingCopyConfig,
} from "./types.js";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";

interface WorkingCopyRepo {
  name: string;
  url: string;
  branch?: string;
  key?: string;
}

export class WorkingCopyClient implements Integration {
  private config: WorkingCopyConfig;
  private initialized = false;
  private configPath: string;

  constructor(config: WorkingCopyConfig) {
    this.config = config;
    this.configPath =
      config.repoPath ||
      path.join(os.homedir(), ".config", "blackroad", "working-copy");
  }

  async initialize(): Promise<void> {
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
   * Generate Working Copy URL for cloning a repository
   */
  generateCloneURL(repo: WorkingCopyRepo): string {
    const params = new URLSearchParams({
      repo: repo.url,
    });

    if (repo.branch) {
      params.set("branch", repo.branch);
    }

    return `working-copy://clone?${params.toString()}`;
  }

  /**
   * Generate Working Copy URL for opening a file
   */
  generateOpenFileURL(repoName: string, filePath: string): string {
    const params = new URLSearchParams({
      repo: repoName,
      path: filePath,
    });

    return `working-copy://open?${params.toString()}`;
  }

  /**
   * Generate Working Copy URL for pulling changes
   */
  generatePullURL(repoName: string): string {
    const params = new URLSearchParams({
      repo: repoName,
    });

    return `working-copy://pull?${params.toString()}`;
  }

  /**
   * Generate Working Copy URL for pushing changes
   */
  generatePushURL(repoName: string): string {
    const params = new URLSearchParams({
      repo: repoName,
    });

    return `working-copy://push?${params.toString()}`;
  }

  /**
   * Generate Working Copy URL for committing changes
   */
  generateCommitURL(repoName: string, message: string): string {
    const params = new URLSearchParams({
      repo: repoName,
      message: message,
    });

    return `working-copy://commit?${params.toString()}`;
  }

  /**
   * Generate Working Copy URL for creating a branch
   */
  generateBranchURL(repoName: string, branchName: string): string {
    const params = new URLSearchParams({
      repo: repoName,
      branch: branchName,
    });

    return `working-copy://branch?${params.toString()}`;
  }

  /**
   * Generate Working Copy URL for writing a file
   */
  generateWriteURL(
    repoName: string,
    filePath: string,
    content: string
  ): string {
    const params = new URLSearchParams({
      repo: repoName,
      path: filePath,
      text: content,
    });

    return `working-copy://write?${params.toString()}`;
  }

  /**
   * Generate Working Copy URL for reading a file
   */
  generateReadURL(repoName: string, filePath: string): string {
    const params = new URLSearchParams({
      repo: repoName,
      path: filePath,
    });

    return `working-copy://read?${params.toString()}`;
  }

  /**
   * Generate Working Copy URL for running git command
   */
  generateGitCommandURL(repoName: string, command: string): string {
    const params = new URLSearchParams({
      repo: repoName,
      cmd: command,
    });

    return `working-copy://git?${params.toString()}`;
  }

  /**
   * Save repository configuration
   */
  async saveRepo(repo: WorkingCopyRepo): Promise<boolean> {
    const reposFile = path.join(this.configPath, "repos.json");
    let repos: WorkingCopyRepo[] = [];

    if (fs.existsSync(reposFile)) {
      repos = JSON.parse(fs.readFileSync(reposFile, "utf-8"));
    }

    const existingIndex = repos.findIndex((r) => r.name === repo.name);
    if (existingIndex >= 0) {
      repos[existingIndex] = repo;
    } else {
      repos.push(repo);
    }

    fs.writeFileSync(reposFile, JSON.stringify(repos, null, 2));
    return true;
  }

  /**
   * Get all saved repositories
   */
  async getRepos(): Promise<WorkingCopyRepo[]> {
    const reposFile = path.join(this.configPath, "repos.json");
    if (!fs.existsSync(reposFile)) {
      return [];
    }
    return JSON.parse(fs.readFileSync(reposFile, "utf-8"));
  }

  /**
   * Remove a repository
   */
  async removeRepo(repoName: string): Promise<boolean> {
    const reposFile = path.join(this.configPath, "repos.json");
    if (!fs.existsSync(reposFile)) {
      return false;
    }

    const repos: WorkingCopyRepo[] = JSON.parse(
      fs.readFileSync(reposFile, "utf-8")
    );
    const newRepos = repos.filter((r) => r.name !== repoName);

    if (newRepos.length === repos.length) {
      return false;
    }

    fs.writeFileSync(reposFile, JSON.stringify(newRepos, null, 2));
    return true;
  }

  /**
   * Generate workflow for common operations
   */
  generateWorkflow(repoName: string): {
    clone: string;
    pull: string;
    push: string;
    sync: string;
  } {
    return {
      clone: this.generateCloneURL({
        name: repoName,
        url: `git@github.com:BlackRoad-OS/${repoName}.git`,
      }),
      pull: this.generatePullURL(repoName),
      push: this.generatePushURL(repoName),
      sync: this.generateGitCommandURL(
        repoName,
        "pull --rebase && push"
      ),
    };
  }

  /**
   * Setup BlackRoad repositories
   */
  async setupBlackRoadRepos(): Promise<boolean> {
    const repos: WorkingCopyRepo[] = [
      {
        name: "blackroad-os-agents",
        url: "git@github.com:BlackRoad-OS/blackroad-os-agents.git",
        branch: "main",
      },
      {
        name: "blackroad-agent-os",
        url: "git@github.com:BlackRoad-OS/blackroad-agent-os.git",
        branch: "main",
      },
      {
        name: "blackroad-docs",
        url: "git@github.com:BlackRoad-OS/blackroad-docs.git",
        branch: "main",
      },
    ];

    for (const repo of repos) {
      await this.saveRepo(repo);
    }

    return true;
  }
}
