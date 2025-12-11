/**
 * Notion Workspace Integration
 *
 * Provides database and page management capabilities via Notion API
 */

import type {
  Integration,
  IntegrationStatus,
  NotionConfig,
} from "./types.js";

const NOTION_API_URL = "https://api.notion.com/v1";
const NOTION_VERSION = "2022-06-28";

interface NotionUser {
  id: string;
  name: string;
  type: "person" | "bot";
}

interface NotionDatabase {
  id: string;
  title: Array<{ plain_text: string }>;
  properties: Record<string, { type: string }>;
}

interface NotionPage {
  id: string;
  parent: { type: string; database_id?: string; page_id?: string };
  properties: Record<string, unknown>;
  url: string;
}

interface NotionBlock {
  id: string;
  type: string;
  has_children: boolean;
  [key: string]: unknown;
}

export class NotionClient implements Integration {
  private config: NotionConfig;
  private initialized = false;

  constructor(config: NotionConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    if (!this.config.token) {
      throw new Error("Notion token is required");
    }
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    try {
      const user = await this.getCurrentUser();
      return {
        connected: true,
        healthy: true,
        lastCheck: new Date(),
        metadata: { user: user.name, type: user.type },
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
      throw new Error("Notion token not configured");
    }

    const response = await fetch(`${NOTION_API_URL}${path}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${this.config.token}`,
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION,
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(
        (error as { message?: string }).message || `Notion API error: ${response.status}`
      );
    }

    return response.json() as Promise<T>;
  }

  /**
   * Get current user (bot)
   */
  async getCurrentUser(): Promise<NotionUser> {
    return this.request<NotionUser>("/users/me");
  }

  /**
   * Search for pages and databases
   */
  async search(
    query: string,
    filter?: { property: "object"; value: "page" | "database" }
  ): Promise<{ results: Array<NotionPage | NotionDatabase> }> {
    return this.request<{ results: Array<NotionPage | NotionDatabase> }>(
      "/search",
      {
        method: "POST",
        body: JSON.stringify({ query, filter }),
      }
    );
  }

  /**
   * Get database
   */
  async getDatabase(databaseId: string): Promise<NotionDatabase> {
    return this.request<NotionDatabase>(`/databases/${databaseId}`);
  }

  /**
   * Query database
   */
  async queryDatabase(
    databaseId?: string,
    options?: {
      filter?: Record<string, unknown>;
      sorts?: Array<{ property: string; direction: "ascending" | "descending" }>;
      page_size?: number;
    }
  ): Promise<{ results: NotionPage[]; has_more: boolean; next_cursor?: string }> {
    const dbId = databaseId || this.config.databaseId;
    if (!dbId) {
      throw new Error("Database ID is required");
    }

    return this.request<{
      results: NotionPage[];
      has_more: boolean;
      next_cursor?: string;
    }>(`/databases/${dbId}/query`, {
      method: "POST",
      body: JSON.stringify(options || {}),
    });
  }

  /**
   * Get page
   */
  async getPage(pageId?: string): Promise<NotionPage> {
    const pId = pageId || this.config.pageId;
    if (!pId) {
      throw new Error("Page ID is required");
    }
    return this.request<NotionPage>(`/pages/${pId}`);
  }

  /**
   * Create page in database
   */
  async createPage(options: {
    databaseId?: string;
    properties: Record<string, unknown>;
    children?: Array<Record<string, unknown>>;
  }): Promise<NotionPage> {
    const dbId = options.databaseId || this.config.databaseId;
    if (!dbId) {
      throw new Error("Database ID is required");
    }

    return this.request<NotionPage>("/pages", {
      method: "POST",
      body: JSON.stringify({
        parent: { database_id: dbId },
        properties: options.properties,
        children: options.children,
      }),
    });
  }

  /**
   * Update page properties
   */
  async updatePage(
    pageId: string,
    properties: Record<string, unknown>
  ): Promise<NotionPage> {
    return this.request<NotionPage>(`/pages/${pageId}`, {
      method: "PATCH",
      body: JSON.stringify({ properties }),
    });
  }

  /**
   * Archive page
   */
  async archivePage(pageId: string): Promise<NotionPage> {
    return this.request<NotionPage>(`/pages/${pageId}`, {
      method: "PATCH",
      body: JSON.stringify({ archived: true }),
    });
  }

  /**
   * Get block children
   */
  async getBlockChildren(
    blockId: string
  ): Promise<{ results: NotionBlock[] }> {
    return this.request<{ results: NotionBlock[] }>(
      `/blocks/${blockId}/children`
    );
  }

  /**
   * Append blocks to page
   */
  async appendBlocks(
    pageId: string,
    blocks: Array<Record<string, unknown>>
  ): Promise<{ results: NotionBlock[] }> {
    return this.request<{ results: NotionBlock[] }>(
      `/blocks/${pageId}/children`,
      {
        method: "PATCH",
        body: JSON.stringify({ children: blocks }),
      }
    );
  }

  /**
   * Delete block
   */
  async deleteBlock(blockId: string): Promise<boolean> {
    await this.request(`/blocks/${blockId}`, {
      method: "DELETE",
    });
    return true;
  }

  // Helper methods for creating block content

  /**
   * Create heading block
   */
  createHeading(
    text: string,
    level: 1 | 2 | 3 = 1
  ): Record<string, unknown> {
    const key = `heading_${level}`;
    return {
      object: "block",
      type: key,
      [key]: {
        rich_text: [{ type: "text", text: { content: text } }],
      },
    };
  }

  /**
   * Create paragraph block
   */
  createParagraph(text: string): Record<string, unknown> {
    return {
      object: "block",
      type: "paragraph",
      paragraph: {
        rich_text: [{ type: "text", text: { content: text } }],
      },
    };
  }

  /**
   * Create bulleted list item
   */
  createBulletedListItem(text: string): Record<string, unknown> {
    return {
      object: "block",
      type: "bulleted_list_item",
      bulleted_list_item: {
        rich_text: [{ type: "text", text: { content: text } }],
      },
    };
  }

  /**
   * Create code block
   */
  createCodeBlock(
    code: string,
    language = "typescript"
  ): Record<string, unknown> {
    return {
      object: "block",
      type: "code",
      code: {
        rich_text: [{ type: "text", text: { content: code } }],
        language,
      },
    };
  }

  /**
   * Create divider block
   */
  createDivider(): Record<string, unknown> {
    return {
      object: "block",
      type: "divider",
      divider: {},
    };
  }

  /**
   * Create callout block
   */
  createCallout(
    text: string,
    icon = "💡"
  ): Record<string, unknown> {
    return {
      object: "block",
      type: "callout",
      callout: {
        rich_text: [{ type: "text", text: { content: text } }],
        icon: { type: "emoji", emoji: icon },
      },
    };
  }

  /**
   * Create deployment log page
   */
  async createDeploymentLog(options: {
    service: string;
    version: string;
    environment: string;
    status: "started" | "success" | "failed";
    logs?: string[];
    databaseId?: string;
  }): Promise<NotionPage> {
    const statusEmoji =
      options.status === "success" ? "✅" : options.status === "failed" ? "❌" : "🔄";

    const properties: Record<string, unknown> = {
      Name: {
        title: [
          {
            text: {
              content: `${options.service} v${options.version} - ${options.environment}`,
            },
          },
        ],
      },
      Status: {
        select: { name: options.status },
      },
      Service: {
        select: { name: options.service },
      },
      Environment: {
        select: { name: options.environment },
      },
      Version: {
        rich_text: [{ text: { content: options.version } }],
      },
      Timestamp: {
        date: { start: new Date().toISOString() },
      },
    };

    const children: Array<Record<string, unknown>> = [
      this.createHeading(`${statusEmoji} Deployment: ${options.service}`, 1),
      this.createDivider(),
      this.createHeading("Details", 2),
      this.createBulletedListItem(`**Service**: ${options.service}`),
      this.createBulletedListItem(`**Version**: ${options.version}`),
      this.createBulletedListItem(`**Environment**: ${options.environment}`),
      this.createBulletedListItem(`**Status**: ${options.status}`),
      this.createBulletedListItem(`**Timestamp**: ${new Date().toISOString()}`),
    ];

    if (options.logs?.length) {
      children.push(
        this.createDivider(),
        this.createHeading("Logs", 2),
        this.createCodeBlock(options.logs.join("\n"), "bash")
      );
    }

    return this.createPage({
      databaseId: options.databaseId,
      properties,
      children,
    });
  }

  /**
   * Update deployment status
   */
  async updateDeploymentStatus(
    pageId: string,
    status: "success" | "failed",
    logs?: string[]
  ): Promise<NotionPage> {
    // Update status property
    await this.updatePage(pageId, {
      Status: { select: { name: status } },
      "Completed At": { date: { start: new Date().toISOString() } },
    });

    // Add completion log
    if (logs?.length) {
      await this.appendBlocks(pageId, [
        this.createDivider(),
        this.createHeading("Completion Logs", 2),
        this.createCodeBlock(logs.join("\n"), "bash"),
        this.createCallout(
          status === "success"
            ? "Deployment completed successfully!"
            : "Deployment failed. Check logs for details.",
          status === "success" ? "✅" : "❌"
        ),
      ]);
    }

    return this.getPage(pageId);
  }
}
