# 🚦 Trinity & Codex Quick Start Guide

**Fast Track to Using the Light Trinity System and BlackRoad Codex**

---

## What is This?

This repository is **fully integrated** with:

- **🚦 Light Trinity System** - GreenLight, YellowLight, RedLight for project management, infrastructure, and design
- **🛣️ BlackRoad Codex** - Verification and memory system tracking 8,789+ reusable components

---

## 🚀 Quick Start (3 Minutes)

### 1. Source the Trinity Scripts

```bash
# GreenLight (project management & tracking)
source .trinity/greenlight/scripts/memory-greenlight-templates.sh

# YellowLight (infrastructure & deployment)
source .trinity/yellowlight/scripts/memory-yellowlight-templates.sh

# RedLight (visual templates & brand)
source .trinity/redlight/scripts/memory-redlight-templates.sh
```

### 2. Initialize Codex Integration (Optional)

```bash
# Setup BlackRoad Codex integration
source .trinity/yellowlight/scripts/trinity-codex-integration.sh

# Check compliance
.trinity/system/trinity-check-compliance.sh "my-entity"
```

### 3. Start Using Templates

```bash
# Announce work (GreenLight)
gl_announce "team" "Building new feature" "1) Plan 2) Build 3) Test 4) Deploy" "Feature work"

# Deploy with template (YellowLight)
railway up --service my-api
yl_deployment_succeeded "my-api" "railway" "https://my-api.railway.app"

# Create landing page (RedLight)
cp .trinity/redlight/templates/blackroad-ultimate.html ./my-page.html
rl_template_create "my-page" "landing" "Feature landing page"
```

---

## 🟢 GreenLight - Project Management

**Purpose**: Track tasks, workflows, and state

### Most Common Commands

```bash
# Announce new work
gl_announce "team-name" "Task description" "Steps" "Context"

# Mark as work in progress
gl_wip "task-id" "current-status" "effort-emoji" "scale-emoji"

# Complete a phase
gl_phase_done "phase" "project" "summary" "scale-emoji"

# Report success
gl_success "task-id" "outcome" "celebration-emoji"

# Log error
gl_error_detected "service" "error-type" "details" "severity"
```

### Show All Functions

```bash
source .trinity/greenlight/scripts/memory-greenlight-templates.sh
show_help  # Shows all 103 template functions
```

**Docs**: `.trinity/greenlight/docs/GREENLIGHT_CLAUDE_QUICK_REFERENCE.md`

---

## 🟡 YellowLight - Infrastructure

**Purpose**: Deploy services, manage infrastructure, automate workflows

### Most Common Commands

```bash
# Start deployment
yl_deployment_started "service" "platform" "description"

# Successful deployment
yl_deployment_succeeded "service" "platform" "url"

# Health check
yl_health_check "service" "url" "response-time"

# Workflow complete
yl_workflow_done "workflow-id" "status" "duration"

# Store in memory
yl_memory_stored "category" "content"
```

### Platform Examples

**Railway**:
```bash
railway up --service my-api
yl_deployment_succeeded "my-api" "railway" "https://my-api.railway.app"
```

**Cloudflare**:
```bash
wrangler deploy worker.js
yl_deployment_succeeded "worker" "cloudflare" "https://worker.example.com"
```

**Docs**: `.trinity/yellowlight/docs/YELLOWLIGHT_INFRASTRUCTURE_SYSTEM.md`

---

## 🔴 RedLight - Visual Templates

**Purpose**: Create branded landing pages, 3D experiences, visual content

### Most Common Commands

```bash
# Create template
rl_template_create "name" "category" "description"

# Test performance
rl_performance_metrics "name" "fps" "load-time-sec" "memory-mb"

# Validate brand
rl_test_passed "name" "visual" "Brand colors validated"

# Deploy template
rl_template_deploy "name" "url" "platform"

# Store in memory
rl_memory_stored "category" "content"
```

### Available Templates

```bash
# List all RedLight templates (23 total)
ls -1 .trinity/redlight/templates/

# Popular templates:
# - blackroad-ultimate.html (main landing)
# - blackroad-animation.html (animated)
# - blackroad-3d-world.html (3D environment)
```

### Use a Template

```bash
# Copy template
cp .trinity/redlight/templates/blackroad-ultimate.html ./my-page.html

# Record creation
rl_template_create "my-page" "landing" "Product landing page"

# Test and deploy
rl_performance_metrics "my-page" "60" "0.8" "150"
wrangler pages deploy . --project-name=my-page
rl_template_deploy "my-page" "https://my-page.pages.dev" "cloudflare-pages"
```

**Docs**: `.trinity/redlight/docs/REDLIGHT_TEMPLATE_SYSTEM.md`

---

## 🛣️ BlackRoad Codex

**Purpose**: Track compliance, usage, and learning across all templates

### Setup

```bash
# Initialize Codex integration (creates database and tools)
source .trinity/yellowlight/scripts/trinity-codex-integration.sh
```

Creates:
- `~/.blackroad/codex/codex.db` - SQLite database
- `~/trinity-check-compliance.sh` - Compliance checker
- `~/trinity-record-test.sh` - Test recorder

### Usage

**Check Compliance**:
```bash
~/trinity-check-compliance.sh "entity-name"

# Shows:
# 🟢 GreenLight Standards: [results]
# 🟡 YellowLight Standards: [results]  
# 🔴 RedLight Standards: [results]
# ✅ FULL COMPLIANCE or ⚠️ PARTIAL COMPLIANCE
```

**Record Test Results**:
```bash
~/trinity-record-test.sh "entity" "light-type" "test-name" "passed:0/1" "details"

# Examples:
~/trinity-record-test.sh "my-template" "redlight" "Brand Colors" 1 "Gradient validated"
~/trinity-record-test.sh "my-api" "yellowlight" "Health Check" 1 "200 OK in 150ms"
~/trinity-record-test.sh "my-task" "greenlight" "State Tracking" 1 "All states logged"
```

**Query Database**:
```bash
sqlite3 ~/.blackroad/codex/codex.db "
  SELECT * FROM trinity_compliance 
  WHERE entity_name = 'my-entity'
"
```

---

## 📦 Templates Directory

**Location**: `templates/`

Contains 200+ Trinity-compliant templates for:
- Development (Python, Bash, Docker, etc.)
- Deployment (Railway, Cloudflare, Vercel)
- Documentation (README, API docs, runbooks)
- Integration (Stripe, Clerk, Notion, etc.)

### Key Template Files

- `MASTER-TEMPLATE-SYSTEM.md` - Complete template system overview
- `TEMPLATE-INDEX.md` - Catalog of all 200+ templates
- `TRINITY-INTEGRATION-GUIDE.md` - Detailed Trinity integration guide
- `INDEX.md` - Quick reference
- `COPY-PASTE-COMMANDS-LIBRARY.md` - Command reference

---

## 🔍 Compliance Workflow

### Automated Checking

Trinity compliance is automatically checked via GitHub Actions:

**Workflow**: `.github/workflows/trinity-compliance.yml`

Runs on:
- Every push to main/develop
- Every pull request  
- Weekly on Sunday at midnight

### Manual Check

```bash
# Run compliance check (from workflow)
cd /path/to/repo

# Check structure
[ -d .trinity ] && echo "✅ Trinity present" || echo "❌ Trinity missing"
[ -d .trinity/greenlight ] && echo "✅ GreenLight" || echo "❌ Missing"
[ -d .trinity/yellowlight ] && echo "✅ YellowLight" || echo "❌ Missing"
[ -d .trinity/redlight ] && echo "✅ RedLight" || echo "❌ Missing"

# Count resources
echo "RedLight templates: $(find .trinity/redlight/templates -name '*.html' | wc -l)"
echo "GreenLight docs: $(find .trinity/greenlight/docs -name '*.md' | wc -l)"
echo "YellowLight scripts: $(find .trinity/yellowlight/scripts -name '*.sh' | wc -l)"
```

---

## 🎯 Common Workflows

### Workflow 1: Deploy New Service

```bash
# 1. Announce (GreenLight)
source .trinity/greenlight/scripts/memory-greenlight-templates.sh
gl_announce "dev-team" "Deploying payment API" "1) Build 2) Test 3) Deploy" "New service"

# 2. Deploy (YellowLight)
source .trinity/yellowlight/scripts/memory-yellowlight-templates.sh
railway up --service payment-api
yl_deployment_succeeded "payment-api" "railway" "https://payment.railway.app"

# 3. Create landing page (RedLight)
source .trinity/redlight/scripts/memory-redlight-templates.sh
cp .trinity/redlight/templates/blackroad-ultimate.html payment-landing.html
rl_template_create "payment-landing" "service" "Payment API landing"

# 4. Complete
gl_phase_done "deployment" "Payment API" "Service live with landing page" "🌌"
```

### Workflow 2: Create Template

```bash
# 1. Claim task
source .trinity/greenlight/scripts/memory-greenlight-templates.sh
gl_task_claimed "template-123" "claude-templates" "Create Stripe template"

# 2. Create template
cat > templates/STRIPE-INTEGRATION.md <<'EOF'
# Stripe Integration Template
[content here]
EOF

# 3. Test compliance
source .trinity/yellowlight/scripts/trinity-codex-integration.sh
~/trinity-record-test.sh "stripe-template" "greenlight" "Documentation" 1 "Complete"
~/trinity-record-test.sh "stripe-template" "yellowlight" "Testing" 1 "All tests pass"
~/trinity-record-test.sh "stripe-template" "redlight" "Examples" 1 "Working examples"

# 4. Verify
~/trinity-check-compliance.sh "stripe-template"

# 5. Complete
gl_collaboration_success "template-123" "claude-templates" "Stripe template ready"
```

### Workflow 3: Multi-Agent Coordination

```bash
# Agent 1: Announce availability
source .trinity/greenlight/scripts/memory-greenlight-templates.sh
gl_agent_available "claude-frontend" "frontend" "React, HTML, CSS"

# Agent 2: Announce availability  
gl_agent_available "claude-backend" "backend" "Python, API, DB"

# Coordination
gl_coordinate "claude-frontend" "claude-backend" "Need API endpoint examples"
gl_coordinate "claude-backend" "claude-frontend" "API examples ready"

# Success
gl_collaboration_success "project-123" "claude-frontend,claude-backend" "Complete solution"
```

---

## 📚 Full Documentation

- **Trinity Overview**: `.trinity/README.md`
- **Trinity System**: `.trinity/system/THE_LIGHT_TRINITY.md`
- **Enforcement**: `.trinity/system/LIGHT_TRINITY_ENFORCEMENT.md`
- **Template Integration**: `templates/TRINITY-INTEGRATION-GUIDE.md`
- **Template System**: `templates/MASTER-TEMPLATE-SYSTEM.md`
- **Template Catalog**: `templates/TEMPLATE-INDEX.md`

---

## 🤝 Support

**Questions?** Check the docs in `.trinity/` and `templates/`

**Issues?** GitHub Issues

**Improvements?** All agents encouraged to enhance the system

---

🚦 **One Trinity. One Codex. Infinite Possibilities.** ✨

**Built with** 🌌 Infinite passion, 🔧 Technical precision, 🌸 Collaborative love  
**For** BlackRoad OS, All Agents, The Future
