/**
 * Type definitions for BlackRoad OS Platform Integrations
 */

/**
 * Status of an integration
 */
export interface IntegrationStatus {
  connected: boolean;
  healthy: boolean;
  lastCheck: Date;
  error?: string;
  metadata?: Record<string, unknown>;
}

/**
 * Base integration interface
 */
export interface Integration {
  initialize(): Promise<void>;
  getStatus(): Promise<IntegrationStatus>;
  cleanup(): Promise<void>;
}

/**
 * Railway configuration
 */
export interface RailwayConfig {
  token?: string;
  projectId?: string;
  environmentId?: string;
}

/**
 * Cloudflare configuration
 */
export interface CloudflareConfig {
  apiToken?: string;
  accountId?: string;
  zoneId?: string;
}

/**
 * GitHub configuration
 */
export interface GitHubConfig {
  token?: string;
  owner?: string;
  repo?: string;
}

/**
 * DigitalOcean configuration
 */
export interface DigitalOceanConfig {
  token?: string;
  dropletId?: string;
  region?: string;
}

/**
 * Vercel configuration
 */
export interface VercelConfig {
  token?: string;
  orgId?: string;
  projectId?: string;
}

/**
 * Docker configuration
 */
export interface DockerConfig {
  socketPath?: string;
  host?: string;
  port?: number;
}

/**
 * Raspberry Pi configuration
 */
export interface RaspberryPiConfig {
  hosts?: string[];
  sshKey?: string;
  user?: string;
}

/**
 * Warp terminal configuration
 */
export interface WarpConfig {
  enabled?: boolean;
  themePath?: string;
}

/**
 * Shellfish SSH configuration
 */
export interface ShellfishConfig {
  enabled?: boolean;
  configPath?: string;
}

/**
 * Working Copy configuration
 */
export interface WorkingCopyConfig {
  enabled?: boolean;
  repoPath?: string;
}

/**
 * Pyto Python configuration
 */
export interface PytoConfig {
  enabled?: boolean;
  scriptsPath?: string;
}

/**
 * Asana configuration
 */
export interface AsanaConfig {
  token?: string;
  workspaceId?: string;
  projectId?: string;
}

/**
 * Notion configuration
 */
export interface NotionConfig {
  token?: string;
  databaseId?: string;
  pageId?: string;
}

/**
 * Clerk authentication configuration
 */
export interface ClerkConfig {
  secretKey?: string;
  publishableKey?: string;
}

/**
 * Stripe payments configuration
 */
export interface StripeConfig {
  secretKey?: string;
  publishableKey?: string;
  webhookSecret?: string;
}

/**
 * Hugging Face configuration
 */
export interface HuggingFaceConfig {
  token?: string;
  modelId?: string;
}

/**
 * Tunnel services configuration
 */
export interface TunnelConfig {
  cloudflareToken?: string;
  ngrokToken?: string;
  localPort?: number;
}

/**
 * LLM configuration for open-source models
 */
export interface LLMConfig {
  modelsDir?: string;
  defaultModel?: string;
  contextSize?: number;
}

/**
 * Full integration configuration
 */
export interface IntegrationConfig {
  railway?: RailwayConfig;
  cloudflare?: CloudflareConfig;
  github?: GitHubConfig;
  digitalocean?: DigitalOceanConfig;
  vercel?: VercelConfig;
  docker?: DockerConfig;
  raspberryPi?: RaspberryPiConfig;
  warp?: WarpConfig;
  shellfish?: ShellfishConfig;
  workingCopy?: WorkingCopyConfig;
  pyto?: PytoConfig;
  asana?: AsanaConfig;
  notion?: NotionConfig;
  clerk?: ClerkConfig;
  stripe?: StripeConfig;
  huggingface?: HuggingFaceConfig;
  tunnels?: TunnelConfig;
  llm?: LLMConfig;
}

/**
 * Deployment result
 */
export interface DeploymentResult {
  success: boolean;
  deploymentId?: string;
  url?: string;
  logs?: string[];
  error?: string;
}

/**
 * Model inference result
 */
export interface InferenceResult {
  text: string;
  tokens?: number;
  duration?: number;
  model: string;
}

/**
 * Safe open-source model metadata
 * Models that are verified safe and forkable
 */
export interface SafeModel {
  id: string;
  name: string;
  source: "huggingface" | "ollama" | "local";
  license: string;
  verified: boolean;
  parameters?: string;
  description?: string;
}

/**
 * Predefined list of safe, forkable open-source models
 */
export const SAFE_OPEN_SOURCE_MODELS: SafeModel[] = [
  // Meta LLaMA family
  {
    id: "meta-llama/Llama-3.2-3B",
    name: "LLaMA 3.2 3B",
    source: "huggingface",
    license: "llama3.2",
    verified: true,
    parameters: "3B",
    description: "Meta's open LLaMA 3.2 model, 3B parameters",
  },
  {
    id: "meta-llama/Llama-3.1-8B",
    name: "LLaMA 3.1 8B",
    source: "huggingface",
    license: "llama3.1",
    verified: true,
    parameters: "8B",
    description: "Meta's open LLaMA 3.1 model, 8B parameters",
  },
  {
    id: "meta-llama/Llama-3.1-70B",
    name: "LLaMA 3.1 70B",
    source: "huggingface",
    license: "llama3.1",
    verified: true,
    parameters: "70B",
    description: "Meta's open LLaMA 3.1 model, 70B parameters",
  },

  // Mistral family
  {
    id: "mistralai/Mistral-7B-v0.3",
    name: "Mistral 7B v0.3",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "7B",
    description: "Mistral AI's open 7B model",
  },
  {
    id: "mistralai/Mixtral-8x7B-v0.1",
    name: "Mixtral 8x7B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "47B",
    description: "Mistral's MoE model with 8 experts",
  },
  {
    id: "mistralai/Mistral-Nemo-12B",
    name: "Mistral Nemo 12B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "12B",
    description: "Mistral's 12B parameter model",
  },

  // Qwen family
  {
    id: "Qwen/Qwen2.5-7B",
    name: "Qwen 2.5 7B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "7B",
    description: "Alibaba's Qwen 2.5 model",
  },
  {
    id: "Qwen/Qwen2.5-72B",
    name: "Qwen 2.5 72B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "72B",
    description: "Alibaba's Qwen 2.5 72B model",
  },
  {
    id: "Qwen/Qwen2.5-Coder-7B",
    name: "Qwen 2.5 Coder 7B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "7B",
    description: "Qwen specialized for code",
  },

  // DeepSeek family
  {
    id: "deepseek-ai/deepseek-coder-6.7b-base",
    name: "DeepSeek Coder 6.7B",
    source: "huggingface",
    license: "mit",
    verified: true,
    parameters: "6.7B",
    description: "DeepSeek's code-focused model",
  },
  {
    id: "deepseek-ai/DeepSeek-V2.5",
    name: "DeepSeek V2.5",
    source: "huggingface",
    license: "deepseek",
    verified: true,
    parameters: "236B",
    description: "DeepSeek's latest MoE model",
  },

  // Google Gemma family
  {
    id: "google/gemma-2-9b",
    name: "Gemma 2 9B",
    source: "huggingface",
    license: "gemma",
    verified: true,
    parameters: "9B",
    description: "Google's open Gemma 2 model",
  },
  {
    id: "google/gemma-2-27b",
    name: "Gemma 2 27B",
    source: "huggingface",
    license: "gemma",
    verified: true,
    parameters: "27B",
    description: "Google's larger Gemma 2 model",
  },

  // Microsoft Phi family
  {
    id: "microsoft/Phi-3.5-mini-instruct",
    name: "Phi 3.5 Mini",
    source: "huggingface",
    license: "mit",
    verified: true,
    parameters: "3.8B",
    description: "Microsoft's efficient Phi model",
  },
  {
    id: "microsoft/Phi-3-medium-128k-instruct",
    name: "Phi 3 Medium 128K",
    source: "huggingface",
    license: "mit",
    verified: true,
    parameters: "14B",
    description: "Phi 3 with 128K context",
  },

  // Stability AI family
  {
    id: "stabilityai/stablelm-2-12b",
    name: "StableLM 2 12B",
    source: "huggingface",
    license: "stablelm",
    verified: true,
    parameters: "12B",
    description: "Stability AI's language model",
  },

  // Yi family
  {
    id: "01-ai/Yi-1.5-9B",
    name: "Yi 1.5 9B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "9B",
    description: "01.AI's Yi model",
  },
  {
    id: "01-ai/Yi-1.5-34B",
    name: "Yi 1.5 34B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "34B",
    description: "01.AI's larger Yi model",
  },

  // Falcon family
  {
    id: "tiiuae/falcon-7b",
    name: "Falcon 7B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "7B",
    description: "TII's Falcon model",
  },
  {
    id: "tiiuae/falcon-40b",
    name: "Falcon 40B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "40B",
    description: "TII's larger Falcon model",
  },

  // StarCoder family
  {
    id: "bigcode/starcoder2-15b",
    name: "StarCoder2 15B",
    source: "huggingface",
    license: "bigcode-openrail-m",
    verified: true,
    parameters: "15B",
    description: "BigCode's code model",
  },

  // CodeLlama family
  {
    id: "codellama/CodeLlama-7b-hf",
    name: "CodeLlama 7B",
    source: "huggingface",
    license: "llama2",
    verified: true,
    parameters: "7B",
    description: "Meta's code-specialized LLaMA",
  },
  {
    id: "codellama/CodeLlama-34b-hf",
    name: "CodeLlama 34B",
    source: "huggingface",
    license: "llama2",
    verified: true,
    parameters: "34B",
    description: "Meta's larger CodeLlama",
  },

  // Nous Research family
  {
    id: "NousResearch/Hermes-3-Llama-3.1-8B",
    name: "Hermes 3 8B",
    source: "huggingface",
    license: "llama3.1",
    verified: true,
    parameters: "8B",
    description: "Nous Research's instruction-tuned model",
  },

  // OpenChat
  {
    id: "openchat/openchat-3.5-0106",
    name: "OpenChat 3.5",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "7B",
    description: "Open-source chat model",
  },

  // Zephyr
  {
    id: "HuggingFaceH4/zephyr-7b-beta",
    name: "Zephyr 7B",
    source: "huggingface",
    license: "mit",
    verified: true,
    parameters: "7B",
    description: "HuggingFace's aligned chat model",
  },

  // SOLAR
  {
    id: "upstage/SOLAR-10.7B-v1.0",
    name: "SOLAR 10.7B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "10.7B",
    description: "Upstage's merged model",
  },

  // InternLM
  {
    id: "internlm/internlm2_5-7b",
    name: "InternLM 2.5 7B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "7B",
    description: "Shanghai AI Lab's model",
  },

  // Command R
  {
    id: "CohereForAI/c4ai-command-r-v01",
    name: "Command R",
    source: "huggingface",
    license: "cc-by-nc-4.0",
    verified: true,
    parameters: "35B",
    description: "Cohere's open Command R model",
  },

  // DBRX
  {
    id: "databricks/dbrx-base",
    name: "DBRX Base",
    source: "huggingface",
    license: "databricks",
    verified: true,
    parameters: "132B",
    description: "Databricks' MoE model",
  },

  // OLMo
  {
    id: "allenai/OLMo-7B",
    name: "OLMo 7B",
    source: "huggingface",
    license: "apache-2.0",
    verified: true,
    parameters: "7B",
    description: "Allen AI's fully open model",
  },

  // Orca
  {
    id: "microsoft/Orca-2-7b",
    name: "Orca 2 7B",
    source: "huggingface",
    license: "microsoft-research",
    verified: true,
    parameters: "7B",
    description: "Microsoft's reasoning-focused model",
  },
];
