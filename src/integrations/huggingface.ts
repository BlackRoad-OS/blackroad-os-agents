/**
 * Hugging Face Integration
 *
 * Provides access to Hugging Face models, datasets, and inference API
 */

import type {
  Integration,
  IntegrationStatus,
  HuggingFaceConfig,
  InferenceResult,
  SafeModel,
  SAFE_OPEN_SOURCE_MODELS,
} from "./types.js";

const HF_API_URL = "https://huggingface.co/api";
const HF_INFERENCE_URL = "https://api-inference.huggingface.co/models";

interface HFModel {
  id: string;
  modelId: string;
  author: string;
  sha: string;
  lastModified: string;
  private: boolean;
  gated: boolean;
  disabled: boolean;
  downloads: number;
  likes: number;
  tags: string[];
  pipeline_tag?: string;
  library_name?: string;
}

interface HFSpace {
  id: string;
  author: string;
  sha: string;
  lastModified: string;
  private: boolean;
  sdk: string;
}

interface HFDataset {
  id: string;
  author: string;
  sha: string;
  lastModified: string;
  private: boolean;
  downloads: number;
  likes: number;
  tags: string[];
}

export class HuggingFaceClient implements Integration {
  private config: HuggingFaceConfig;
  private initialized = false;

  constructor(config: HuggingFaceConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    // Token is optional for public models
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    try {
      // Try to access the API
      const response = await fetch(`${HF_API_URL}/models?limit=1`);
      return {
        connected: response.ok,
        healthy: response.ok,
        lastCheck: new Date(),
        metadata: {
          authenticated: !!this.config.token,
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
    url: string,
    options: RequestInit = {}
  ): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };

    if (this.config.token) {
      headers.Authorization = `Bearer ${this.config.token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers: { ...headers, ...options.headers },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(
        (error as { error?: string }).error || `HuggingFace API error: ${response.status}`
      );
    }

    return response.json() as Promise<T>;
  }

  /**
   * Search models
   */
  async searchModels(options?: {
    search?: string;
    author?: string;
    filter?: string;
    sort?: "downloads" | "likes" | "lastModified";
    direction?: "asc" | "desc";
    limit?: number;
  }): Promise<HFModel[]> {
    const params = new URLSearchParams();
    if (options?.search) params.set("search", options.search);
    if (options?.author) params.set("author", options.author);
    if (options?.filter) params.set("filter", options.filter);
    if (options?.sort) params.set("sort", options.sort);
    if (options?.direction) params.set("direction", options.direction === "asc" ? "1" : "-1");
    if (options?.limit) params.set("limit", String(options.limit));

    return this.request<HFModel[]>(`${HF_API_URL}/models?${params}`);
  }

  /**
   * Get model info
   */
  async getModel(modelId: string): Promise<HFModel> {
    return this.request<HFModel>(`${HF_API_URL}/models/${modelId}`);
  }

  /**
   * Search datasets
   */
  async searchDatasets(options?: {
    search?: string;
    author?: string;
    limit?: number;
  }): Promise<HFDataset[]> {
    const params = new URLSearchParams();
    if (options?.search) params.set("search", options.search);
    if (options?.author) params.set("author", options.author);
    if (options?.limit) params.set("limit", String(options.limit));

    return this.request<HFDataset[]>(`${HF_API_URL}/datasets?${params}`);
  }

  /**
   * Get dataset info
   */
  async getDataset(datasetId: string): Promise<HFDataset> {
    return this.request<HFDataset>(`${HF_API_URL}/datasets/${datasetId}`);
  }

  /**
   * Search spaces
   */
  async searchSpaces(options?: {
    search?: string;
    author?: string;
    sdk?: "gradio" | "streamlit" | "static";
    limit?: number;
  }): Promise<HFSpace[]> {
    const params = new URLSearchParams();
    if (options?.search) params.set("search", options.search);
    if (options?.author) params.set("author", options.author);
    if (options?.sdk) params.set("sdk", options.sdk);
    if (options?.limit) params.set("limit", String(options.limit));

    return this.request<HFSpace[]>(`${HF_API_URL}/spaces?${params}`);
  }

  /**
   * Run inference on a model
   */
  async inference(
    modelId: string,
    inputs: string | Record<string, unknown>,
    options?: {
      parameters?: Record<string, unknown>;
      wait_for_model?: boolean;
    }
  ): Promise<InferenceResult> {
    if (!this.config.token) {
      throw new Error("Token required for inference API");
    }

    const startTime = Date.now();

    const body: Record<string, unknown> = {
      inputs,
    };

    if (options?.parameters) {
      body.parameters = options.parameters;
    }

    if (options?.wait_for_model) {
      body.options = { wait_for_model: true };
    }

    const result = await this.request<unknown>(`${HF_INFERENCE_URL}/${modelId}`, {
      method: "POST",
      body: JSON.stringify(body),
    });

    const duration = Date.now() - startTime;

    // Handle different response formats
    let text: string;
    if (typeof result === "string") {
      text = result;
    } else if (Array.isArray(result)) {
      const first = result[0];
      text = typeof first === "object" && first !== null
        ? (first as { generated_text?: string }).generated_text || JSON.stringify(first)
        : String(first);
    } else if (typeof result === "object" && result !== null) {
      text = (result as { generated_text?: string }).generated_text || JSON.stringify(result);
    } else {
      text = String(result);
    }

    return {
      text,
      model: modelId,
      duration,
    };
  }

  /**
   * Text generation
   */
  async textGeneration(
    modelId: string,
    prompt: string,
    options?: {
      max_new_tokens?: number;
      temperature?: number;
      top_p?: number;
      top_k?: number;
      repetition_penalty?: number;
      do_sample?: boolean;
    }
  ): Promise<InferenceResult> {
    return this.inference(modelId || this.config.modelId || "gpt2", prompt, {
      parameters: options,
      wait_for_model: true,
    });
  }

  /**
   * Text-to-text generation (translation, summarization, etc.)
   */
  async textToText(
    modelId: string,
    text: string
  ): Promise<InferenceResult> {
    return this.inference(modelId, text, { wait_for_model: true });
  }

  /**
   * Conversational (chat)
   */
  async chat(
    modelId: string,
    messages: Array<{ role: "user" | "assistant"; content: string }>,
    options?: {
      max_new_tokens?: number;
      temperature?: number;
    }
  ): Promise<InferenceResult> {
    const prompt = messages
      .map((m) => `${m.role === "user" ? "User" : "Assistant"}: ${m.content}`)
      .join("\n");

    return this.textGeneration(modelId, prompt + "\nAssistant:", options);
  }

  /**
   * Embeddings
   */
  async embeddings(
    modelId: string,
    texts: string[]
  ): Promise<number[][]> {
    const result = await this.request<number[][]>(`${HF_INFERENCE_URL}/${modelId}`, {
      method: "POST",
      body: JSON.stringify({ inputs: texts }),
    });
    return result;
  }

  /**
   * Feature extraction
   */
  async featureExtraction(
    modelId: string,
    text: string
  ): Promise<number[]> {
    const result = await this.embeddings(modelId, [text]);
    return result[0];
  }

  /**
   * Get safe open-source models list
   */
  getSafeModels(): SafeModel[] {
    // Return from the types module
    return SAFE_OPEN_SOURCE_MODELS;
  }

  /**
   * Check if a model is in the safe list
   */
  isModelSafe(modelId: string): boolean {
    return this.getSafeModels().some((m) => m.id === modelId);
  }

  /**
   * Get safe models by license
   */
  getSafeModelsByLicense(license: string): SafeModel[] {
    return this.getSafeModels().filter(
      (m) => m.license.toLowerCase() === license.toLowerCase()
    );
  }

  /**
   * Get safe models by source
   */
  getSafeModelsBySource(source: "huggingface" | "ollama" | "local"): SafeModel[] {
    return this.getSafeModels().filter((m) => m.source === source);
  }

  /**
   * Download model files (for local deployment)
   */
  async getModelFiles(
    modelId: string
  ): Promise<Array<{ filename: string; size: number }>> {
    const model = await this.getModel(modelId);

    // Get file listing from the model page
    const result = await this.request<{
      siblings: Array<{ rfilename: string; size: number }>;
    }>(`${HF_API_URL}/models/${modelId}`);

    return result.siblings.map((s) => ({
      filename: s.rfilename,
      size: s.size,
    }));
  }

  /**
   * Get download URL for a model file
   */
  getFileDownloadURL(
    modelId: string,
    filename: string,
    revision = "main"
  ): string {
    return `https://huggingface.co/${modelId}/resolve/${revision}/${filename}`;
  }
}
