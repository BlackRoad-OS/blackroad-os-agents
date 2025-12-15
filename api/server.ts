import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { loadAllAgents, getAgent } from '../src/loader.js';
import type { Agent } from '../src/types.js';

const app = new Hono();

app.use('/*', cors());

// Health check
app.get('/health', (c) => {
  return c.json({ status: 'ok', service: 'blackroad-os-agents' });
});

// Get all agents
app.get('/agents', async (c) => {
  try {
    const agents = await loadAllAgents();
    return c.json({ agents, count: agents.length });
  } catch (error) {
    return c.json({ error: 'Failed to load agents', message: String(error) }, 500);
  }
});

// Get agent by ID
app.get('/agents/:id', async (c) => {
  try {
    const id = c.req.param('id');
    const agent = await getAgent(id);

    if (!agent) {
      return c.json({ error: 'Agent not found' }, 404);
    }

    return c.json({ agent });
  } catch (error) {
    return c.json({ error: 'Failed to get agent', message: String(error) }, 500);
  }
});

// Get agents by owner
app.get('/owners/:owner/agents', async (c) => {
  try {
    const owner = c.req.param('owner');
    const allAgents = await loadAllAgents();
    const agents = allAgents.filter((agent: Agent) => agent.owner === owner);

    return c.json({ agents, count: agents.length, owner });
  } catch (error) {
    return c.json({ error: 'Failed to load agents', message: String(error) }, 500);
  }
});

// Get agents by capability
app.get('/capabilities/:capability/agents', async (c) => {
  try {
    const capability = c.req.param('capability');
    const allAgents = await loadAllAgents();
    const agents = allAgents.filter((agent: Agent) =>
      agent.capabilities?.includes(capability)
    );

    return c.json({ agents, count: agents.length, capability });
  } catch (error) {
    return c.json({ error: 'Failed to load agents', message: String(error) }, 500);
  }
});

// Get agents by status
app.get('/status/:status/agents', async (c) => {
  try {
    const status = c.req.param('status');
    const allAgents = await loadAllAgents();
    const agents = allAgents.filter((agent: Agent) => agent.status === status);

    return c.json({ agents, count: agents.length, status });
  } catch (error) {
    return c.json({ error: 'Failed to load agents', message: String(error) }, 500);
  }
});

export default app;
