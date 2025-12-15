/**
 * Open-Source LLM Integration
 *
 * Provides local model inference via llama.cpp and integration with
 * safe, forkable open-source models (GPT-J, LLaMA, Mistral, etc.)
 */

import type {
  Integration,
  IntegrationStatus,
  LLMConfig,
  InferenceResult,
  SafeModel,
  SAFE_OPEN_SOURCE_MODELS,
} from "./types.js";
import { spawn, ChildProcess } from "child_process";
import * as fs from "fs";
import * as path from "path";
import * as os from "os";

interface LocalModel {
  name: string;
  path: string;
  size: number;
  format: "gguf" | "ggml" | "bin";
  quantization?: string;
}

interface InferenceOptions {
  maxTokens?: number;
  temperature?: number;
  topP?: number;
  topK?: number;
  repeatPenalty?: number;
  seed?: number;
  stopSequences?: string[];
}

interface ModelServer {
  process: ChildProcess;
  port: number;
  model: string;
  status: "starting" | "running" | "stopped" | "error";
}

export class LLMClient implements Integration {
  private config: LLMConfig;
  private initialized = false;
  private modelsDir: string;
  private servers: Map<string, ModelServer> = new Map();

  constructor(config: LLMConfig) {
    this.config = config;
    this.modelsDir = config.modelsDir || path.join(os.homedir(), ".blackroad", "models");
  }

  async initialize(): Promise<void> {
    if (!fs.existsSync(this.modelsDir)) {
      fs.mkdirSync(this.modelsDir, { recursive: true });
    }
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    const models = await this.listLocalModels();
    const runningServers = Array.from(this.servers.values()).filter(
      (s) => s.status === "running"
    );

    return {
      connected: true,
      healthy: true,
      lastCheck: new Date(),
      metadata: {
        modelsDir: this.modelsDir,
        localModels: models.length,
        runningServers: runningServers.length,
        llamaCppAvailable: await this.isLlamaCppInstalled(),
      },
    };
  }

  async cleanup(): Promise<void> {
    // Stop all running servers
    for (const [id] of this.servers) {
      await this.stopServer(id);
    }
    this.initialized = false;
  }

  /**
   * Check if llama.cpp is installed
   */
  async isLlamaCppInstalled(): Promise<boolean> {
    const paths = [
      "/usr/local/bin/llama-cli",
      "/usr/bin/llama-cli",
      path.join(os.homedir(), ".local/bin/llama-cli"),
      "/opt/homebrew/bin/llama-cli",
      // Legacy names
      "/usr/local/bin/main",
      path.join(os.homedir(), "llama.cpp/main"),
    ];

    for (const p of paths) {
      if (fs.existsSync(p)) {
        return true;
      }
    }
    return false;
  }

  /**
   * Get llama.cpp executable path
   */
  private getLlamaCppPath(): string | null {
    const paths = [
      "/usr/local/bin/llama-cli",
      "/usr/bin/llama-cli",
      path.join(os.homedir(), ".local/bin/llama-cli"),
      "/opt/homebrew/bin/llama-cli",
      "/usr/local/bin/main",
      path.join(os.homedir(), "llama.cpp/main"),
    ];

    for (const p of paths) {
      if (fs.existsSync(p)) {
        return p;
      }
    }
    return null;
  }

  /**
   * List local models
   */
  async listLocalModels(): Promise<LocalModel[]> {
    if (!fs.existsSync(this.modelsDir)) {
      return [];
    }

    const files = fs.readdirSync(this.modelsDir, { withFileTypes: true });
    const models: LocalModel[] = [];

    for (const file of files) {
      if (file.isFile()) {
        const ext = path.extname(file.name).toLowerCase();
        if ([".gguf", ".ggml", ".bin"].includes(ext)) {
          const fullPath = path.join(this.modelsDir, file.name);
          const stats = fs.statSync(fullPath);

          // Parse quantization from filename
          const quantMatch = file.name.match(/[qQ](\d+)_?(\w+)?/);
          const quantization = quantMatch
            ? `Q${quantMatch[1]}${quantMatch[2] ? `_${quantMatch[2]}` : ""}`
            : undefined;

          models.push({
            name: file.name.replace(ext, ""),
            path: fullPath,
            size: stats.size,
            format: ext.replace(".", "") as "gguf" | "ggml" | "bin",
            quantization,
          });
        }
      }
    }

    return models;
  }

  /**
   * Get safe open-source models list
   */
  getSafeModels(): SafeModel[] {
    return SAFE_OPEN_SOURCE_MODELS;
  }

  /**
   * Run inference with llama.cpp
   */
  async runInference(
    modelPath: string,
    prompt: string,
    options: InferenceOptions = {}
  ): Promise<InferenceResult> {
    const llamaPath = this.getLlamaCppPath();
    if (!llamaPath) {
      throw new Error("llama.cpp is not installed");
    }

    const resolvedPath = path.isAbsolute(modelPath)
      ? modelPath
      : path.join(this.modelsDir, modelPath);

    if (!fs.existsSync(resolvedPath)) {
      throw new Error(`Model not found: ${resolvedPath}`);
    }

    const startTime = Date.now();

    const args = [
      "-m", resolvedPath,
      "-p", prompt,
      "-n", String(options.maxTokens || 128),
      "--temp", String(options.temperature ?? 0.7),
      "--top-p", String(options.topP ?? 0.9),
      "--top-k", String(options.topK ?? 40),
      "--repeat-penalty", String(options.repeatPenalty ?? 1.1),
      "--no-display-prompt",
    ];

    if (options.seed !== undefined) {
      args.push("-s", String(options.seed));
    }

    return new Promise((resolve, reject) => {
      const process = spawn(llamaPath, args);
      let output = "";
      let errorOutput = "";

      process.stdout.on("data", (data: Buffer) => {
        output += data.toString();
      });

      process.stderr.on("data", (data: Buffer) => {
        errorOutput += data.toString();
      });

      process.on("close", (code) => {
        const duration = Date.now() - startTime;

        if (code !== 0) {
          reject(new Error(`Inference failed: ${errorOutput}`));
          return;
        }

        // Clean up output
        let text = output.trim();

        // Remove stop sequences if present
        if (options.stopSequences) {
          for (const stop of options.stopSequences) {
            const idx = text.indexOf(stop);
            if (idx !== -1) {
              text = text.substring(0, idx);
            }
          }
        }

        resolve({
          text: text.trim(),
          model: path.basename(resolvedPath),
          duration,
        });
      });

      process.on("error", (err) => {
        reject(err);
      });
    });
  }

  /**
   * Stream inference output
   */
  async *streamInference(
    modelPath: string,
    prompt: string,
    options: InferenceOptions = {}
  ): AsyncGenerator<string, void, unknown> {
    const llamaPath = this.getLlamaCppPath();
    if (!llamaPath) {
      throw new Error("llama.cpp is not installed");
    }

    const resolvedPath = path.isAbsolute(modelPath)
      ? modelPath
      : path.join(this.modelsDir, modelPath);

    const args = [
      "-m", resolvedPath,
      "-p", prompt,
      "-n", String(options.maxTokens || 128),
      "--temp", String(options.temperature ?? 0.7),
      "--no-display-prompt",
    ];

    const process = spawn(llamaPath, args);

    const readStream = async function* (
      stream: NodeJS.ReadableStream
    ): AsyncGenerator<string, void, unknown> {
      for await (const chunk of stream) {
        yield chunk.toString();
      }
    };

    yield* readStream(process.stdout);
  }

  /**
   * Start a model server (llama.cpp server mode)
   */
  async startServer(
    modelPath: string,
    port = 8080
  ): Promise<ModelServer> {
    const serverPath = this.getLlamaCppPath()?.replace("llama-cli", "llama-server") ||
      this.getLlamaCppPath()?.replace("main", "server");

    if (!serverPath || !fs.existsSync(serverPath)) {
      throw new Error("llama.cpp server is not installed");
    }

    const resolvedPath = path.isAbsolute(modelPath)
      ? modelPath
      : path.join(this.modelsDir, modelPath);

    const serverId = `server-${port}`;

    if (this.servers.has(serverId)) {
      throw new Error(`Server already running on port ${port}`);
    }

    const server: ModelServer = {
      process: null as unknown as ChildProcess,
      port,
      model: resolvedPath,
      status: "starting",
    };

    const args = [
      "-m", resolvedPath,
      "--host", "0.0.0.0",
      "--port", String(port),
    ];

    const process = spawn(serverPath, args);

    server.process = process;

    process.stdout.on("data", (data: Buffer) => {
      const line = data.toString();
      if (line.includes("listening")) {
        server.status = "running";
      }
    });

    process.stderr.on("data", (data: Buffer) => {
      const line = data.toString();
      if (line.includes("listening")) {
        server.status = "running";
      }
    });

    process.on("exit", () => {
      server.status = "stopped";
      this.servers.delete(serverId);
    });

    process.on("error", () => {
      server.status = "error";
    });

    this.servers.set(serverId, server);

    // Wait for server to start
    await new Promise((resolve) => setTimeout(resolve, 5000));

    return server;
  }

  /**
   * Stop a model server
   */
  async stopServer(serverId: string): Promise<boolean> {
    const server = this.servers.get(serverId);
    if (!server) {
      return false;
    }

    server.process.kill("SIGTERM");
    this.servers.delete(serverId);
    return true;
  }

  /**
   * Chat with a running server
   */
  async chatWithServer(
    port: number,
    messages: Array<{ role: "user" | "assistant" | "system"; content: string }>,
    options: InferenceOptions = {}
  ): Promise<InferenceResult> {
    const startTime = Date.now();

    const response = await fetch(`http://localhost:${port}/v1/chat/completions`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages,
        max_tokens: options.maxTokens || 128,
        temperature: options.temperature ?? 0.7,
        top_p: options.topP ?? 0.9,
        stop: options.stopSequences,
      }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = (await response.json()) as {
      choices: Array<{ message: { content: string } }>;
      model: string;
    };
    const duration = Date.now() - startTime;

    return {
      text: data.choices[0]?.message?.content || "",
      model: data.model,
      duration,
    };
  }

  /**
   * Complete text with a running server
   */
  async completeWithServer(
    port: number,
    prompt: string,
    options: InferenceOptions = {}
  ): Promise<InferenceResult> {
    const startTime = Date.now();

    const response = await fetch(`http://localhost:${port}/completion`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        prompt,
        n_predict: options.maxTokens || 128,
        temperature: options.temperature ?? 0.7,
        top_p: options.topP ?? 0.9,
        top_k: options.topK ?? 40,
        repeat_penalty: options.repeatPenalty ?? 1.1,
        stop: options.stopSequences,
      }),
    });

    if (!response.ok) {
      throw new Error(`Server error: ${response.status}`);
    }

    const data = (await response.json()) as { content: string; model: string };
    const duration = Date.now() - startTime;

    return {
      text: data.content,
      model: data.model,
      duration,
    };
  }

  /**
   * Get recommended models for different use cases
   */
  getRecommendedModels(useCase: "chat" | "code" | "general" | "small"): SafeModel[] {
    const models = this.getSafeModels();

    switch (useCase) {
      case "chat":
        return models.filter(
          (m) =>
            m.name.toLowerCase().includes("chat") ||
            m.name.toLowerCase().includes("instruct") ||
            m.id.includes("Hermes") ||
            m.id.includes("zephyr")
        );

      case "code":
        return models.filter(
          (m) =>
            m.name.toLowerCase().includes("code") ||
            m.id.includes("Coder") ||
            m.id.includes("starcoder")
        );

      case "small":
        return models.filter((m) => {
          const params = m.parameters?.replace("B", "");
          return params && parseFloat(params) <= 7;
        });

      case "general":
      default:
        return models.filter(
          (m) =>
            m.verified &&
            (m.license === "apache-2.0" || m.license === "mit")
        );
    }
  }

  /**
   * Get GGUF download URL for a Hugging Face model
   */
  getGGUFDownloadUrl(
    modelId: string,
    quantization = "Q4_K_M"
  ): string {
    // TheBloke and similar providers often have GGUF versions
    const blobParts = modelId.split("/");
    const modelName = blobParts[blobParts.length - 1];

    // Common GGUF repository naming patterns
    return `https://huggingface.co/TheBloke/${modelName}-GGUF/resolve/main/${modelName.toLowerCase()}.${quantization.toLowerCase()}.gguf`;
  }
}
