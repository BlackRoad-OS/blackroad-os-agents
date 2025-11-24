import { z } from 'zod';

export const agentSchema = z.object({
  id: z.string().regex(/^[a-z0-9-]+$/, {
    message: 'id must be kebab-case',
  }),
  name: z.string().min(1),
  role: z.string().min(1),
  version: z.string().min(1),
  owner: z.string().min(1),
  endpoints: z
    .object({
      health: z.string().url(),
      invoke: z.string().url(),
    })
    .partial()
    .optional(),
  capabilities: z.array(z.string()).min(1),
  dependencies: z.array(z.string()).optional(),
  status: z.enum(['draft', 'active', 'deprecated']),
});

export type AgentManifest = z.infer<typeof agentSchema>;
