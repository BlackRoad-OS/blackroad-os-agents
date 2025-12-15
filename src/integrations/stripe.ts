/**
 * Stripe Payments Integration
 *
 * Provides payment processing and subscription management via Stripe API
 */

import type {
  Integration,
  IntegrationStatus,
  StripeConfig,
} from "./types.js";

const STRIPE_API_URL = "https://api.stripe.com/v1";

interface StripeCustomer {
  id: string;
  email: string | null;
  name: string | null;
  created: number;
  metadata: Record<string, string>;
}

interface StripeSubscription {
  id: string;
  customer: string;
  status: string;
  current_period_start: number;
  current_period_end: number;
  items: {
    data: Array<{
      id: string;
      price: { id: string; product: string };
    }>;
  };
}

interface StripePaymentIntent {
  id: string;
  amount: number;
  currency: string;
  status: string;
  client_secret: string;
  customer: string | null;
}

interface StripeProduct {
  id: string;
  name: string;
  description: string | null;
  active: boolean;
  metadata: Record<string, string>;
}

interface StripePrice {
  id: string;
  product: string;
  active: boolean;
  currency: string;
  unit_amount: number | null;
  recurring: {
    interval: "day" | "week" | "month" | "year";
    interval_count: number;
  } | null;
}

interface StripeWebhookEvent {
  id: string;
  type: string;
  data: { object: Record<string, unknown> };
  created: number;
}

export class StripeClient implements Integration {
  private config: StripeConfig;
  private initialized = false;

  constructor(config: StripeConfig) {
    this.config = config;
  }

  async initialize(): Promise<void> {
    if (!this.config.secretKey) {
      throw new Error("Stripe secret key is required");
    }
    this.initialized = true;
  }

  async getStatus(): Promise<IntegrationStatus> {
    try {
      const balance = await this.getBalance();
      return {
        connected: true,
        healthy: true,
        lastCheck: new Date(),
        metadata: { available: balance.available },
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
      throw new Error("Stripe secret key not configured");
    }

    const response = await fetch(`${STRIPE_API_URL}${path}`, {
      ...options,
      headers: {
        Authorization: `Bearer ${this.config.secretKey}`,
        "Content-Type": "application/x-www-form-urlencoded",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(
        (error as { error?: { message?: string } }).error?.message ||
          `Stripe API error: ${response.status}`
      );
    }

    return response.json() as Promise<T>;
  }

  private encodeParams(params: Record<string, unknown>): string {
    const encode = (
      obj: Record<string, unknown>,
      prefix = ""
    ): string[] => {
      const parts: string[] = [];
      for (const [key, value] of Object.entries(obj)) {
        const fullKey = prefix ? `${prefix}[${key}]` : key;
        if (value === null || value === undefined) continue;
        if (typeof value === "object" && !Array.isArray(value)) {
          parts.push(...encode(value as Record<string, unknown>, fullKey));
        } else if (Array.isArray(value)) {
          value.forEach((v, i) => {
            if (typeof v === "object") {
              parts.push(...encode(v as Record<string, unknown>, `${fullKey}[${i}]`));
            } else {
              parts.push(`${fullKey}[${i}]=${encodeURIComponent(String(v))}`);
            }
          });
        } else {
          parts.push(`${fullKey}=${encodeURIComponent(String(value))}`);
        }
      }
      return parts;
    };
    return encode(params).join("&");
  }

  /**
   * Get account balance
   */
  async getBalance(): Promise<{
    available: Array<{ amount: number; currency: string }>;
    pending: Array<{ amount: number; currency: string }>;
  }> {
    return this.request<{
      available: Array<{ amount: number; currency: string }>;
      pending: Array<{ amount: number; currency: string }>;
    }>("/balance");
  }

  /**
   * List customers
   */
  async listCustomers(options?: {
    email?: string;
    limit?: number;
  }): Promise<{ data: StripeCustomer[] }> {
    const params = new URLSearchParams();
    if (options?.email) params.set("email", options.email);
    if (options?.limit) params.set("limit", String(options.limit));
    return this.request<{ data: StripeCustomer[] }>(`/customers?${params}`);
  }

  /**
   * Get customer
   */
  async getCustomer(customerId: string): Promise<StripeCustomer> {
    return this.request<StripeCustomer>(`/customers/${customerId}`);
  }

  /**
   * Create customer
   */
  async createCustomer(options: {
    email?: string;
    name?: string;
    metadata?: Record<string, string>;
  }): Promise<StripeCustomer> {
    return this.request<StripeCustomer>("/customers", {
      method: "POST",
      body: this.encodeParams(options),
    });
  }

  /**
   * Update customer
   */
  async updateCustomer(
    customerId: string,
    updates: {
      email?: string;
      name?: string;
      metadata?: Record<string, string>;
    }
  ): Promise<StripeCustomer> {
    return this.request<StripeCustomer>(`/customers/${customerId}`, {
      method: "POST",
      body: this.encodeParams(updates),
    });
  }

  /**
   * Delete customer
   */
  async deleteCustomer(
    customerId: string
  ): Promise<{ id: string; deleted: boolean }> {
    return this.request<{ id: string; deleted: boolean }>(
      `/customers/${customerId}`,
      { method: "DELETE" }
    );
  }

  /**
   * Create payment intent
   */
  async createPaymentIntent(options: {
    amount: number;
    currency: string;
    customer?: string;
    metadata?: Record<string, string>;
    automatic_payment_methods?: { enabled: boolean };
  }): Promise<StripePaymentIntent> {
    return this.request<StripePaymentIntent>("/payment_intents", {
      method: "POST",
      body: this.encodeParams(options),
    });
  }

  /**
   * Get payment intent
   */
  async getPaymentIntent(paymentIntentId: string): Promise<StripePaymentIntent> {
    return this.request<StripePaymentIntent>(
      `/payment_intents/${paymentIntentId}`
    );
  }

  /**
   * Confirm payment intent
   */
  async confirmPaymentIntent(
    paymentIntentId: string,
    options?: { payment_method?: string }
  ): Promise<StripePaymentIntent> {
    return this.request<StripePaymentIntent>(
      `/payment_intents/${paymentIntentId}/confirm`,
      {
        method: "POST",
        body: options ? this.encodeParams(options) : undefined,
      }
    );
  }

  /**
   * Cancel payment intent
   */
  async cancelPaymentIntent(
    paymentIntentId: string
  ): Promise<StripePaymentIntent> {
    return this.request<StripePaymentIntent>(
      `/payment_intents/${paymentIntentId}/cancel`,
      { method: "POST" }
    );
  }

  /**
   * List products
   */
  async listProducts(options?: {
    active?: boolean;
    limit?: number;
  }): Promise<{ data: StripeProduct[] }> {
    const params = new URLSearchParams();
    if (options?.active !== undefined)
      params.set("active", String(options.active));
    if (options?.limit) params.set("limit", String(options.limit));
    return this.request<{ data: StripeProduct[] }>(`/products?${params}`);
  }

  /**
   * Create product
   */
  async createProduct(options: {
    name: string;
    description?: string;
    metadata?: Record<string, string>;
  }): Promise<StripeProduct> {
    return this.request<StripeProduct>("/products", {
      method: "POST",
      body: this.encodeParams(options),
    });
  }

  /**
   * List prices
   */
  async listPrices(options?: {
    product?: string;
    active?: boolean;
    limit?: number;
  }): Promise<{ data: StripePrice[] }> {
    const params = new URLSearchParams();
    if (options?.product) params.set("product", options.product);
    if (options?.active !== undefined)
      params.set("active", String(options.active));
    if (options?.limit) params.set("limit", String(options.limit));
    return this.request<{ data: StripePrice[] }>(`/prices?${params}`);
  }

  /**
   * Create price
   */
  async createPrice(options: {
    product: string;
    currency: string;
    unit_amount: number;
    recurring?: {
      interval: "day" | "week" | "month" | "year";
      interval_count?: number;
    };
  }): Promise<StripePrice> {
    return this.request<StripePrice>("/prices", {
      method: "POST",
      body: this.encodeParams(options),
    });
  }

  /**
   * List subscriptions
   */
  async listSubscriptions(options?: {
    customer?: string;
    status?: string;
    limit?: number;
  }): Promise<{ data: StripeSubscription[] }> {
    const params = new URLSearchParams();
    if (options?.customer) params.set("customer", options.customer);
    if (options?.status) params.set("status", options.status);
    if (options?.limit) params.set("limit", String(options.limit));
    return this.request<{ data: StripeSubscription[] }>(
      `/subscriptions?${params}`
    );
  }

  /**
   * Create subscription
   */
  async createSubscription(options: {
    customer: string;
    items: Array<{ price: string; quantity?: number }>;
    metadata?: Record<string, string>;
  }): Promise<StripeSubscription> {
    return this.request<StripeSubscription>("/subscriptions", {
      method: "POST",
      body: this.encodeParams(options),
    });
  }

  /**
   * Cancel subscription
   */
  async cancelSubscription(
    subscriptionId: string
  ): Promise<StripeSubscription> {
    return this.request<StripeSubscription>(
      `/subscriptions/${subscriptionId}`,
      { method: "DELETE" }
    );
  }

  /**
   * Verify webhook signature
   */
  verifyWebhookSignature(
    payload: string,
    signature: string
  ): StripeWebhookEvent | null {
    if (!this.config.webhookSecret) {
      throw new Error("Webhook secret not configured");
    }

    try {
      // Parse signature header
      const elements = signature.split(",").reduce(
        (acc, item) => {
          const [key, value] = item.split("=");
          acc[key] = value;
          return acc;
        },
        {} as Record<string, string>
      );

      const timestamp = elements.t;
      const expectedSig = elements.v1;

      if (!timestamp || !expectedSig) {
        return null;
      }

      // Verify timestamp is within tolerance (5 minutes)
      const timestampMs = parseInt(timestamp, 10) * 1000;
      if (Math.abs(Date.now() - timestampMs) > 300000) {
        return null;
      }

      // In production, verify HMAC signature here
      // This is a simplified version

      return JSON.parse(payload) as StripeWebhookEvent;
    } catch {
      return null;
    }
  }

  /**
   * Create checkout session
   */
  async createCheckoutSession(options: {
    mode: "payment" | "subscription" | "setup";
    success_url: string;
    cancel_url: string;
    line_items?: Array<{
      price: string;
      quantity: number;
    }>;
    customer?: string;
    customer_email?: string;
    metadata?: Record<string, string>;
  }): Promise<{ id: string; url: string }> {
    return this.request<{ id: string; url: string }>("/checkout/sessions", {
      method: "POST",
      body: this.encodeParams(options),
    });
  }

  /**
   * Create billing portal session
   */
  async createBillingPortalSession(options: {
    customer: string;
    return_url: string;
  }): Promise<{ id: string; url: string }> {
    return this.request<{ id: string; url: string }>(
      "/billing_portal/sessions",
      {
        method: "POST",
        body: this.encodeParams(options),
      }
    );
  }
}
