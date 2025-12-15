# BlackRoad OS Agents API

Web API for the BlackRoad OS Agents registry. Provides HTTP endpoints to query agent manifests.

## Endpoints

### Health Check
```
GET /health
```

### Get All Agents
```
GET /agents
```
Returns all registered agents with count.

### Get Agent by ID
```
GET /agents/:id
```
Returns a specific agent by ID (e.g., `/agents/cadillac`)

### Get Agents by Owner
```
GET /owners/:owner/agents
```
Filter agents by owner (e.g., `/owners/@blackroad/finance/agents`)

### Get Agents by Capability
```
GET /capabilities/:capability/agents
```
Filter agents by capability (e.g., `/capabilities/forecast/agents`)

### Get Agents by Status
```
GET /status/:status/agents
```
Filter agents by status: `draft`, `active`, or `deprecated`

## Development

```bash
# Install dependencies
npm install

# Start dev server with hot reload
npm run dev

# Build
npm run build

# Start production server
npm start
```

## Deployment

This API is designed to be deployed to Railway:

```bash
railway up
```

Environment variables:
- `PORT` - Server port (default: 3001)

## Tech Stack

- **Hono** - Fast web framework
- **TypeScript** - Type safety
- **Zod** - Schema validation
- **@hono/node-server** - Node.js adapter
