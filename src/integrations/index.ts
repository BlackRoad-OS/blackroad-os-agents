/**
 * BlackRoad OS Platform Integrations
 *
 * Unified module for all platform integrations including:
 * - Cloud platforms (Railway, Cloudflare, Vercel, DigitalOcean)
 * - Development tools (GitHub, Docker, Warp, Working Copy)
 * - Mobile platforms (Shellfish, Pyto)
 * - Productivity (Asana, Notion)
 * - Services (Clerk, Stripe, Hugging Face)
 * - Infrastructure (Tunnels, Raspberry Pi)
 * - AI/ML (Open-source LLMs)
 */

export * from "./railway.js";
export * from "./cloudflare.js";
export * from "./github.js";
export * from "./digitalocean.js";
export * from "./vercel.js";
export * from "./docker.js";
export * from "./raspberry-pi.js";
export * from "./warp.js";
export * from "./shellfish.js";
export * from "./working-copy.js";
export * from "./pyto.js";
export * from "./asana.js";
export * from "./notion.js";
export * from "./clerk.js";
export * from "./stripe.js";
export * from "./huggingface.js";
export * from "./tunnels.js";
export * from "./llm.js";
export * from "./types.js";

import { RailwayClient } from "./railway.js";
import { CloudflareClient } from "./cloudflare.js";
import { GitHubClient } from "./github.js";
import { DigitalOceanClient } from "./digitalocean.js";
import { VercelClient } from "./vercel.js";
import { DockerClient } from "./docker.js";
import { RaspberryPiClient } from "./raspberry-pi.js";
import { WarpClient } from "./warp.js";
import { ShellfishClient } from "./shellfish.js";
import { WorkingCopyClient } from "./working-copy.js";
import { PytoClient } from "./pyto.js";
import { AsanaClient } from "./asana.js";
import { NotionClient } from "./notion.js";
import { ClerkClient } from "./clerk.js";
import { StripeClient } from "./stripe.js";
import { HuggingFaceClient } from "./huggingface.js";
import { TunnelClient } from "./tunnels.js";
import { LLMClient } from "./llm.js";
import type { IntegrationConfig, IntegrationStatus } from "./types.js";

/**
 * Unified integration manager for all platform connections
 */
export class IntegrationManager {
  private config: IntegrationConfig;

  // Cloud platforms
  public railway?: RailwayClient;
  public cloudflare?: CloudflareClient;
  public vercel?: VercelClient;
  public digitalocean?: DigitalOceanClient;

  // Development tools
  public github?: GitHubClient;
  public docker?: DockerClient;
  public warp?: WarpClient;
  public workingCopy?: WorkingCopyClient;

  // Mobile platforms
  public shellfish?: ShellfishClient;
  public pyto?: PytoClient;

  // Productivity
  public asana?: AsanaClient;
  public notion?: NotionClient;

  // Services
  public clerk?: ClerkClient;
  public stripe?: StripeClient;
  public huggingface?: HuggingFaceClient;

  // Infrastructure
  public tunnels?: TunnelClient;
  public raspberryPi?: RaspberryPiClient;

  // AI/ML
  public llm?: LLMClient;

  constructor(config: Partial<IntegrationConfig> = {}) {
    this.config = {
      railway: config.railway,
      cloudflare: config.cloudflare,
      github: config.github,
      digitalocean: config.digitalocean,
      vercel: config.vercel,
      docker: config.docker,
      raspberryPi: config.raspberryPi,
      warp: config.warp,
      shellfish: config.shellfish,
      workingCopy: config.workingCopy,
      pyto: config.pyto,
      asana: config.asana,
      notion: config.notion,
      clerk: config.clerk,
      stripe: config.stripe,
      huggingface: config.huggingface,
      tunnels: config.tunnels,
      llm: config.llm,
    };
  }

  /**
   * Initialize all configured integrations
   */
  async initialize(): Promise<void> {
    const initPromises: Promise<void>[] = [];

    if (this.config.railway?.token) {
      this.railway = new RailwayClient(this.config.railway);
      initPromises.push(this.railway.initialize());
    }

    if (this.config.cloudflare?.apiToken) {
      this.cloudflare = new CloudflareClient(this.config.cloudflare);
      initPromises.push(this.cloudflare.initialize());
    }

    if (this.config.github?.token) {
      this.github = new GitHubClient(this.config.github);
      initPromises.push(this.github.initialize());
    }

    if (this.config.digitalocean?.token) {
      this.digitalocean = new DigitalOceanClient(this.config.digitalocean);
      initPromises.push(this.digitalocean.initialize());
    }

    if (this.config.vercel?.token) {
      this.vercel = new VercelClient(this.config.vercel);
      initPromises.push(this.vercel.initialize());
    }

    if (this.config.docker) {
      this.docker = new DockerClient(this.config.docker);
      initPromises.push(this.docker.initialize());
    }

    if (this.config.raspberryPi) {
      this.raspberryPi = new RaspberryPiClient(this.config.raspberryPi);
      initPromises.push(this.raspberryPi.initialize());
    }

    if (this.config.warp) {
      this.warp = new WarpClient(this.config.warp);
      initPromises.push(this.warp.initialize());
    }

    if (this.config.shellfish) {
      this.shellfish = new ShellfishClient(this.config.shellfish);
      initPromises.push(this.shellfish.initialize());
    }

    if (this.config.workingCopy) {
      this.workingCopy = new WorkingCopyClient(this.config.workingCopy);
      initPromises.push(this.workingCopy.initialize());
    }

    if (this.config.pyto) {
      this.pyto = new PytoClient(this.config.pyto);
      initPromises.push(this.pyto.initialize());
    }

    if (this.config.asana?.token) {
      this.asana = new AsanaClient(this.config.asana);
      initPromises.push(this.asana.initialize());
    }

    if (this.config.notion?.token) {
      this.notion = new NotionClient(this.config.notion);
      initPromises.push(this.notion.initialize());
    }

    if (this.config.clerk?.secretKey) {
      this.clerk = new ClerkClient(this.config.clerk);
      initPromises.push(this.clerk.initialize());
    }

    if (this.config.stripe?.secretKey) {
      this.stripe = new StripeClient(this.config.stripe);
      initPromises.push(this.stripe.initialize());
    }

    if (this.config.huggingface?.token) {
      this.huggingface = new HuggingFaceClient(this.config.huggingface);
      initPromises.push(this.huggingface.initialize());
    }

    if (this.config.tunnels) {
      this.tunnels = new TunnelClient(this.config.tunnels);
      initPromises.push(this.tunnels.initialize());
    }

    if (this.config.llm) {
      this.llm = new LLMClient(this.config.llm);
      initPromises.push(this.llm.initialize());
    }

    await Promise.all(initPromises);
  }

  /**
   * Get status of all integrations
   */
  async getStatus(): Promise<Record<string, IntegrationStatus>> {
    const status: Record<string, IntegrationStatus> = {};

    if (this.railway) {
      status.railway = await this.railway.getStatus();
    }
    if (this.cloudflare) {
      status.cloudflare = await this.cloudflare.getStatus();
    }
    if (this.github) {
      status.github = await this.github.getStatus();
    }
    if (this.digitalocean) {
      status.digitalocean = await this.digitalocean.getStatus();
    }
    if (this.vercel) {
      status.vercel = await this.vercel.getStatus();
    }
    if (this.docker) {
      status.docker = await this.docker.getStatus();
    }
    if (this.raspberryPi) {
      status.raspberryPi = await this.raspberryPi.getStatus();
    }
    if (this.warp) {
      status.warp = await this.warp.getStatus();
    }
    if (this.shellfish) {
      status.shellfish = await this.shellfish.getStatus();
    }
    if (this.workingCopy) {
      status.workingCopy = await this.workingCopy.getStatus();
    }
    if (this.pyto) {
      status.pyto = await this.pyto.getStatus();
    }
    if (this.asana) {
      status.asana = await this.asana.getStatus();
    }
    if (this.notion) {
      status.notion = await this.notion.getStatus();
    }
    if (this.clerk) {
      status.clerk = await this.clerk.getStatus();
    }
    if (this.stripe) {
      status.stripe = await this.stripe.getStatus();
    }
    if (this.huggingface) {
      status.huggingface = await this.huggingface.getStatus();
    }
    if (this.tunnels) {
      status.tunnels = await this.tunnels.getStatus();
    }
    if (this.llm) {
      status.llm = await this.llm.getStatus();
    }

    return status;
  }

  /**
   * Cleanup all integrations
   */
  async cleanup(): Promise<void> {
    const cleanupPromises: Promise<void>[] = [];

    if (this.railway) cleanupPromises.push(this.railway.cleanup());
    if (this.cloudflare) cleanupPromises.push(this.cloudflare.cleanup());
    if (this.github) cleanupPromises.push(this.github.cleanup());
    if (this.digitalocean) cleanupPromises.push(this.digitalocean.cleanup());
    if (this.vercel) cleanupPromises.push(this.vercel.cleanup());
    if (this.docker) cleanupPromises.push(this.docker.cleanup());
    if (this.raspberryPi) cleanupPromises.push(this.raspberryPi.cleanup());
    if (this.warp) cleanupPromises.push(this.warp.cleanup());
    if (this.shellfish) cleanupPromises.push(this.shellfish.cleanup());
    if (this.workingCopy) cleanupPromises.push(this.workingCopy.cleanup());
    if (this.pyto) cleanupPromises.push(this.pyto.cleanup());
    if (this.asana) cleanupPromises.push(this.asana.cleanup());
    if (this.notion) cleanupPromises.push(this.notion.cleanup());
    if (this.clerk) cleanupPromises.push(this.clerk.cleanup());
    if (this.stripe) cleanupPromises.push(this.stripe.cleanup());
    if (this.huggingface) cleanupPromises.push(this.huggingface.cleanup());
    if (this.tunnels) cleanupPromises.push(this.tunnels.cleanup());
    if (this.llm) cleanupPromises.push(this.llm.cleanup());

    await Promise.all(cleanupPromises);
  }
}

/**
 * Create integration manager from environment variables
 */
export function createFromEnv(): IntegrationManager {
  return new IntegrationManager({
    railway: {
      token: process.env.RAILWAY_TOKEN,
      projectId: process.env.RAILWAY_PROJECT_ID,
    },
    cloudflare: {
      apiToken: process.env.CLOUDFLARE_API_TOKEN,
      accountId: process.env.CLOUDFLARE_ACCOUNT_ID,
    },
    github: {
      token: process.env.GITHUB_TOKEN,
    },
    digitalocean: {
      token: process.env.DIGITALOCEAN_TOKEN,
    },
    vercel: {
      token: process.env.VERCEL_TOKEN,
      orgId: process.env.VERCEL_ORG_ID,
    },
    docker: {
      socketPath: process.env.DOCKER_SOCKET || "/var/run/docker.sock",
    },
    raspberryPi: {
      hosts: (process.env.PI_HOSTS || "").split(",").filter(Boolean),
      sshKey: process.env.PI_SSH_KEY,
    },
    asana: {
      token: process.env.ASANA_TOKEN,
    },
    notion: {
      token: process.env.NOTION_TOKEN,
    },
    clerk: {
      secretKey: process.env.CLERK_SECRET_KEY,
      publishableKey: process.env.CLERK_PUBLISHABLE_KEY,
    },
    stripe: {
      secretKey: process.env.STRIPE_SECRET_KEY,
      webhookSecret: process.env.STRIPE_WEBHOOK_SECRET,
    },
    huggingface: {
      token: process.env.HUGGINGFACE_TOKEN,
    },
    tunnels: {
      cloudflareToken: process.env.CLOUDFLARE_TUNNEL_TOKEN,
      ngrokToken: process.env.NGROK_AUTH_TOKEN,
    },
    llm: {
      modelsDir: process.env.LLM_MODELS_DIR || "/var/lib/blackroad/models",
    },
  });
}
