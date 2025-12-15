import { serve } from '@hono/node-server';
import app from './server.js';

const port = parseInt(process.env.PORT || '3001', 10);

console.log(`🤖 BlackRoad OS Agents API starting on port ${port}...`);

serve({
  fetch: app.fetch,
  port,
});

console.log(`✅ BlackRoad OS Agents API running at http://localhost:${port}`);
