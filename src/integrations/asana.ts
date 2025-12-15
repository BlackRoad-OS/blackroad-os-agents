/**
 * Asana Project Management Integration
 *
 * Provides task and project management capabilities via Asana API
 */

import type {
  Integration,
  IntegrationStatus,
  AsanaConfig,
} from "./types.js";

const ASANA_API_URL = "https://app.asana.com/api/1.0";

interface AsanaUser {
  gid: string;
  name: string;
  email: string;
}

interface AsanaWorkspace {
  gid: string;
  name: string;
}

interface AsanaProject {
  gid: string;
  name: string;
  notes?: string;
  color?: string;
  workspace: { gid: string; name: string };
}

interface AsanaTask {
  gid: string;
  name: string;
  notes?: string;
  completed: boolean;
  due_on?: string;
  assignee?: { gid: string; name: string };
  projects?: Array<{ gid: string; name: string }>;
  tags?: Array<{ gid: string; name: string }>;
}

interface AsanaSection {
  gid: string;
  name: string;
  project: { gid: string; name: string };
}

export class AsanaClient implements Integration {
  private config: AsanaConfig;
  private initialized = false;

  constructor(config: AsanaConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    if (!this.config.token) {
      throw new Error("Asana token is required");
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
        metadata: { user: user.name, email: user.email },
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
      throw new Error("Asana token not configured");
    }

    const response = await fetch(`${ASANA_API_URL}${path}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${this.config.token}`,
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(
        (error as { errors?: Array<{ message: string }> }).errors?.[0]?.message ||
          `Asana API error: ${response.status}`
      );
    }

    const data = (await response.json()) as { data: T };
    return data.data;
  }

  /**
   * Get current user
   */
  async getCurrentUser(): Promise<AsanaUser> {
    return this.request<AsanaUser>("/users/me");
  }

  /**
   * List workspaces
   */
  async listWorkspaces(): Promise<AsanaWorkspace[]> {
    return this.request<AsanaWorkspace[]>("/workspaces");
  }

  /**
   * List projects in a workspace
   */
  async listProjects(workspaceId?: string): Promise<AsanaProject[]> {
    const wsId = workspaceId || this.config.workspaceId;
    if (!wsId) {
      throw new Error("Workspace ID is required");
    }
    return this.request<AsanaProject[]>(
      `/workspaces/${wsId}/projects?opt_fields=name,notes,color,workspace`
    );
  }

  /**
   * Get project by ID
   */
  async getProject(projectId: string): Promise<AsanaProject> {
    return this.request<AsanaProject>(
      `/projects/${projectId}?opt_fields=name,notes,color,workspace`
    );
  }

  /**
   * Create project
   */
  async createProject(options: {
    name: string;
    notes?: string;
    color?: string;
    workspaceId?: string;
  }): Promise<AsanaProject> {
    const wsId = options.workspaceId || this.config.workspaceId;
    if (!wsId) {
      throw new Error("Workspace ID is required");
    }

    return this.request<AsanaProject>("/projects", {
      method: "POST",
      body: JSON.stringify({
        data: {
          name: options.name,
          notes: options.notes,
          color: options.color,
          workspace: wsId,
        },
      }),
    });
  }

  /**
   * List tasks in a project
   */
  async listTasks(projectId?: string): Promise<AsanaTask[]> {
    const pId = projectId || this.config.projectId;
    if (!pId) {
      throw new Error("Project ID is required");
    }
    return this.request<AsanaTask[]>(
      `/projects/${pId}/tasks?opt_fields=name,notes,completed,due_on,assignee,projects,tags`
    );
  }

  /**
   * Get task by ID
   */
  async getTask(taskId: string): Promise<AsanaTask> {
    return this.request<AsanaTask>(
      `/tasks/${taskId}?opt_fields=name,notes,completed,due_on,assignee,projects,tags`
    );
  }

  /**
   * Create task
   */
  async createTask(options: {
    name: string;
    notes?: string;
    projectId?: string;
    sectionId?: string;
    assigneeId?: string;
    dueOn?: string;
    completed?: boolean;
  }): Promise<AsanaTask> {
    const pId = options.projectId || this.config.projectId;
    if (!pId && !options.sectionId) {
      throw new Error("Project ID or Section ID is required");
    }

    const data: Record<string, unknown> = {
      name: options.name,
      notes: options.notes,
      completed: options.completed || false,
    };

    if (pId) {
      data.projects = [pId];
    }
    if (options.assigneeId) {
      data.assignee = options.assigneeId;
    }
    if (options.dueOn) {
      data.due_on = options.dueOn;
    }

    const task = await this.request<AsanaTask>("/tasks", {
      method: "POST",
      body: JSON.stringify({ data }),
    });

    // Move to section if specified
    if (options.sectionId) {
      await this.addTaskToSection(task.gid, options.sectionId);
    }

    return task;
  }

  /**
   * Update task
   */
  async updateTask(
    taskId: string,
    updates: {
      name?: string;
      notes?: string;
      completed?: boolean;
      dueOn?: string;
      assigneeId?: string;
    }
  ): Promise<AsanaTask> {
    const data: Record<string, unknown> = {};
    if (updates.name !== undefined) data.name = updates.name;
    if (updates.notes !== undefined) data.notes = updates.notes;
    if (updates.completed !== undefined) data.completed = updates.completed;
    if (updates.dueOn !== undefined) data.due_on = updates.dueOn;
    if (updates.assigneeId !== undefined) data.assignee = updates.assigneeId;

    return this.request<AsanaTask>(`/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify({ data }),
    });
  }

  /**
   * Delete task
   */
  async deleteTask(taskId: string): Promise<boolean> {
    await this.request(`/tasks/${taskId}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * Complete task
   */
  async completeTask(taskId: string): Promise<AsanaTask> {
    return this.updateTask(taskId, { completed: true });
  }

  /**
   * List sections in a project
   */
  async listSections(projectId?: string): Promise<AsanaSection[]> {
    const pId = projectId || this.config.projectId;
    if (!pId) {
      throw new Error("Project ID is required");
    }
    return this.request<AsanaSection[]>(`/projects/${pId}/sections`);
  }

  /**
   * Create section
   */
  async createSection(
    name: string,
    projectId?: string
  ): Promise<AsanaSection> {
    const pId = projectId || this.config.projectId;
    if (!pId) {
      throw new Error("Project ID is required");
    }

    return this.request<AsanaSection>(`/projects/${pId}/sections`, {
      method: "POST",
      body: JSON.stringify({ data: { name } }),
    });
  }

  /**
   * Add task to section
   */
  async addTaskToSection(
    taskId: string,
    sectionId: string
  ): Promise<boolean> {
    await this.request(`/sections/${sectionId}/addTask`, {
      method: "POST",
      body: JSON.stringify({ data: { task: taskId } }),
    });
    return true;
  }

  /**
   * Add comment to task
   */
  async addComment(taskId: string, text: string): Promise<{ gid: string }> {
    return this.request<{ gid: string }>(`/tasks/${taskId}/stories`, {
      method: "POST",
      body: JSON.stringify({ data: { text } }),
    });
  }

  /**
   * Create deployment tracking task
   */
  async createDeploymentTask(options: {
    service: string;
    version: string;
    environment: string;
    projectId?: string;
  }): Promise<AsanaTask> {
    const task = await this.createTask({
      name: `Deploy ${options.service} v${options.version} to ${options.environment}`,
      notes: `
## Deployment Details
- **Service**: ${options.service}
- **Version**: ${options.version}
- **Environment**: ${options.environment}
- **Initiated**: ${new Date().toISOString()}

## Checklist
- [ ] Code review completed
- [ ] Tests passed
- [ ] Deployment started
- [ ] Health checks passed
- [ ] Monitoring confirmed
`,
      projectId: options.projectId,
      dueOn: new Date().toISOString().split("T")[0],
    });

    return task;
  }

  /**
   * Mark deployment as complete
   */
  async markDeploymentComplete(
    taskId: string,
    success: boolean,
    details?: string
  ): Promise<AsanaTask> {
    await this.addComment(
      taskId,
      success
        ? `Deployment completed successfully at ${new Date().toISOString()}${details ? `\n\n${details}` : ""}`
        : `Deployment failed at ${new Date().toISOString()}${details ? `\n\nError: ${details}` : ""}`
    );

    return this.completeTask(taskId);
  }
}
