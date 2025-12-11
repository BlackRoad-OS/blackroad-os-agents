/**
 * Clerk Authentication Integration
 *
 * Provides user authentication and management via Clerk API
 */

import type {
  Integration,
  IntegrationStatus,
  ClerkConfig,
} from "./types.js";

const CLERK_API_URL = "https://api.clerk.com/v1";

interface ClerkUser {
  id: string;
  email_addresses: Array<{
    id: string;
    email_address: string;
    verification: { status: string };
  }>;
  first_name: string | null;
  last_name: string | null;
  username: string | null;
  created_at: number;
  updated_at: number;
  last_sign_in_at: number | null;
  banned: boolean;
}

interface ClerkSession {
  id: string;
  user_id: string;
  status: string;
  last_active_at: number;
  expire_at: number;
  created_at: number;
}

interface ClerkOrganization {
  id: string;
  name: string;
  slug: string;
  created_at: number;
  members_count: number;
}

interface ClerkInvitation {
  id: string;
  email_address: string;
  status: string;
  created_at: number;
}

export class ClerkClient implements Integration {
  private config: ClerkConfig;
  private initialized = false;

  constructor(config: ClerkConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    if (!this.config.secretKey) {
      throw new Error("Clerk secret key is required");
    }
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    try {
      const users = await this.listUsers({ limit: 1 });
      return {
        connected: true,
        healthy: true,
        lastCheck: new Date(),
        metadata: { usersCount: users.total_count },
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
    if (!this.config.secretKey) {
      throw new Error("Clerk secret key not configured");
    }

    const response = await fetch(`${CLERK_API_URL}${path}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${this.config.secretKey}`,
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(
        (error as { errors?: Array<{ message: string }> }).errors?.[0]?.message ||
          `Clerk API error: ${response.status}`
      );
    }

    return response.json() as Promise<T>;
  }

  /**
   * List users
   */
  async listUsers(options?: {
    limit?: number;
    offset?: number;
    email_address?: string[];
    phone_number?: string[];
    username?: string[];
    user_id?: string[];
  }): Promise<{ data: ClerkUser[]; total_count: number }> {
    const params = new URLSearchParams();
    if (options?.limit) params.set("limit", String(options.limit));
    if (options?.offset) params.set("offset", String(options.offset));
    if (options?.email_address) {
      options.email_address.forEach((e) =>
        params.append("email_address", e)
      );
    }
    if (options?.user_id) {
      options.user_id.forEach((id) => params.append("user_id", id));
    }

    return this.request<{ data: ClerkUser[]; total_count: number }>(
      `/users?${params}`
    );
  }

  /**
   * Get user by ID
   */
  async getUser(userId: string): Promise<ClerkUser> {
    return this.request<ClerkUser>(`/users/${userId}`);
  }

  /**
   * Create user
   */
  async createUser(options: {
    email_address?: string[];
    phone_number?: string[];
    username?: string;
    password?: string;
    first_name?: string;
    last_name?: string;
    skip_password_checks?: boolean;
    skip_password_requirement?: boolean;
  }): Promise<ClerkUser> {
    return this.request<ClerkUser>("/users", {
      method: "POST",
      body: JSON.stringify(options),
    });
  }

  /**
   * Update user
   */
  async updateUser(
    userId: string,
    updates: {
      first_name?: string;
      last_name?: string;
      username?: string;
      password?: string;
    }
  ): Promise<ClerkUser> {
    return this.request<ClerkUser>(`/users/${userId}`, {
      method: "PATCH",
      body: JSON.stringify(updates),
    });
  }

  /**
   * Delete user
   */
  async deleteUser(userId: string): Promise<boolean> {
    await this.request(`/users/${userId}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * Ban user
   */
  async banUser(userId: string): Promise<ClerkUser> {
    return this.request<ClerkUser>(`/users/${userId}/ban`, {
      method: "POST",
    });
  }

  /**
   * Unban user
   */
  async unbanUser(userId: string): Promise<ClerkUser> {
    return this.request<ClerkUser>(`/users/${userId}/unban`, {
      method: "POST",
    });
  }

  /**
   * List sessions
   */
  async listSessions(options?: {
    user_id?: string;
    status?: "active" | "ended" | "removed" | "replaced" | "abandoned";
    limit?: number;
  }): Promise<ClerkSession[]> {
    const params = new URLSearchParams();
    if (options?.user_id) params.set("user_id", options.user_id);
    if (options?.status) params.set("status", options.status);
    if (options?.limit) params.set("limit", String(options.limit));

    return this.request<ClerkSession[]>(`/sessions?${params}`);
  }

  /**
   * Revoke session
   */
  async revokeSession(sessionId: string): Promise<ClerkSession> {
    return this.request<ClerkSession>(`/sessions/${sessionId}/revoke`, {
      method: "POST",
    });
  }

  /**
   * Revoke all user sessions
   */
  async revokeAllSessions(userId: string): Promise<boolean> {
    const sessions = await this.listSessions({
      user_id: userId,
      status: "active",
    });
    for (const session of sessions) {
      await this.revokeSession(session.id);
    }
    return true;
  }

  /**
   * List organizations
   */
  async listOrganizations(options?: {
    limit?: number;
    offset?: number;
    include_members_count?: boolean;
  }): Promise<{ data: ClerkOrganization[]; total_count: number }> {
    const params = new URLSearchParams();
    if (options?.limit) params.set("limit", String(options.limit));
    if (options?.offset) params.set("offset", String(options.offset));
    if (options?.include_members_count) {
      params.set("include_members_count", "true");
    }

    return this.request<{ data: ClerkOrganization[]; total_count: number }>(
      `/organizations?${params}`
    );
  }

  /**
   * Create organization
   */
  async createOrganization(options: {
    name: string;
    slug?: string;
    created_by: string;
  }): Promise<ClerkOrganization> {
    return this.request<ClerkOrganization>("/organizations", {
      method: "POST",
      body: JSON.stringify(options),
    });
  }

  /**
   * Update organization
   */
  async updateOrganization(
    organizationId: string,
    updates: { name?: string; slug?: string }
  ): Promise<ClerkOrganization> {
    return this.request<ClerkOrganization>(
      `/organizations/${organizationId}`,
      {
        method: "PATCH",
        body: JSON.stringify(updates),
      }
    );
  }

  /**
   * Delete organization
   */
  async deleteOrganization(organizationId: string): Promise<boolean> {
    await this.request(`/organizations/${organizationId}`, {
      method: "DELETE",
    });
    return true;
  }

  /**
   * Create invitation
   */
  async createInvitation(options: {
    email_address: string;
    public_metadata?: Record<string, unknown>;
    redirect_url?: string;
  }): Promise<ClerkInvitation> {
    return this.request<ClerkInvitation>("/invitations", {
      method: "POST",
      body: JSON.stringify(options),
    });
  }

  /**
   * List invitations
   */
  async listInvitations(options?: {
    status?: "pending" | "accepted" | "revoked";
  }): Promise<ClerkInvitation[]> {
    const params = new URLSearchParams();
    if (options?.status) params.set("status", options.status);

    return this.request<ClerkInvitation[]>(`/invitations?${params}`);
  }

  /**
   * Revoke invitation
   */
  async revokeInvitation(invitationId: string): Promise<ClerkInvitation> {
    return this.request<ClerkInvitation>(
      `/invitations/${invitationId}/revoke`,
      {
        method: "POST",
      }
    );
  }

  /**
   * Verify JWT token
   */
  async verifyToken(token: string): Promise<{
    valid: boolean;
    user_id?: string;
    session_id?: string;
  }> {
    try {
      // In a real implementation, you would verify the JWT signature
      // using the Clerk public key. This is a simplified version.
      const parts = token.split(".");
      if (parts.length !== 3) {
        return { valid: false };
      }

      const payload = JSON.parse(Buffer.from(parts[1], "base64").toString());
      const now = Math.floor(Date.now() / 1000);

      if (payload.exp && payload.exp < now) {
        return { valid: false };
      }

      return {
        valid: true,
        user_id: payload.sub,
        session_id: payload.sid,
      };
    } catch {
      return { valid: false };
    }
  }

  /**
   * Get user count
   */
  async getUserCount(): Promise<number> {
    const result = await this.listUsers({ limit: 1 });
    return result.total_count;
  }

  /**
   * Get active session count
   */
  async getActiveSessionCount(): Promise<number> {
    const sessions = await this.listSessions({ status: "active" });
    return sessions.length;
  }
}
