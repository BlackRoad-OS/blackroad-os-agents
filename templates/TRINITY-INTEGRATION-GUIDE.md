# 🚦 Trinity Integration Guide for BlackRoad OS Templates

**How to Use GreenLight, YellowLight, and RedLight with Templates**

---

## Overview

The **Light Trinity System** provides three integrated layers for BlackRoad OS development:

- 🟢 **GreenLight** - Project management, task tracking, event logging
- 🟡 **YellowLight** - Infrastructure automation, deployment, CI/CD
- 🔴 **RedLight** - Visual templates, brand system, design patterns

This guide shows how to integrate Trinity standards into your template usage and development workflows.

---

## 🟢 GreenLight: Project & Task Templates

### Quick Start

```bash
# Source GreenLight templates
source .trinity/greenlight/scripts/memory-greenlight-templates.sh

# Available functions (103 total)
show_help
```

### Common Workflows

#### 1. Track Template Creation

```bash
# Announce new template work
gl_announce "template-team" "Creating deployment template" \
  "1) Research best practices 2) Write template 3) Test 4) Document" \
  "Template development"

# Mark as work-in-progress
gl_wip "deployment-template" "Writing Railway deployment section" "🍖" "👉"

# Complete phase
gl_phase_done "implementation" "Deployment Template" \
  "Complete Railway, Cloudflare, and DigitalOcean sections with examples" "🌌"
```

#### 2. Log Template Usage

```bash
# Record template deployment
gl_deployed "my-api" "v1.0.0" "production" "Deployed using Railway template"

# Track success
gl_success "template-deployment" "Used RAILWAY-TEMPLATE successfully" "⭐"
```

#### 3. Coordinate Multi-Agent Template Work

```bash
# Announce agent availability
gl_agent_available "claude-templates" "templates" "Documentation, examples, validation"

# Claim task
gl_task_claimed "template-123" "claude-templates" "Create Notion integration template"

# Share learning
gl_learning_discovered "template-patterns" \
  "Use heredocs for multi-line config files" \
  "Reduces errors and improves copy-paste experience"

# Report collaboration success
gl_collaboration_success "template-123" "claude-templates,claude-docs" \
  "Notion template complete with docs"
```

### GreenLight Documentation
- `.trinity/greenlight/docs/GREENLIGHT_CLAUDE_QUICK_REFERENCE.md` - Quick start
- `.trinity/greenlight/docs/GREENLIGHT_EMOJI_DICTIONARY.md` - 200+ emoji reference
- `.trinity/greenlight/docs/GREENLIGHT_AI_AGENT_COORDINATION.md` - Multi-Claude coordination

---

## 🟡 YellowLight: Infrastructure Templates

### Quick Start

```bash
# Source YellowLight templates
source .trinity/yellowlight/scripts/memory-yellowlight-templates.sh

# Initialize Codex integration
source .trinity/yellowlight/scripts/trinity-codex-integration.sh
```

### Infrastructure Deployment Patterns

#### 1. Railway Deployment

```bash
# Log deployment start
yl_deployment_started "my-api" "railway" "Deploying API service"

# Deploy using template
railway up --service my-api

# Log success
yl_deployment_succeeded "my-api" "railway" "https://my-api.railway.app"

# Record in memory
yl_memory_stored "deployment" "my-api deployed to Railway using template"
```

#### 2. Cloudflare Deployment

```bash
# Deploy Worker
yl_deployment_started "api-worker" "cloudflare" "Deploying API Worker"

cd cloudflare-workers
wrangler deploy api-worker.js --config wrangler-api.toml

yl_deployment_succeeded "api-worker" "cloudflare" "https://api.example.com"

# Health check
yl_health_check "api-worker" "https://api.example.com/health" "200ms"
```

#### 3. Multi-Platform Deployment

```bash
# Deploy to multiple platforms using templates
yl_workflow_started "multi-deploy" "Deploy to Railway + Cloudflare"

# Railway
railway up --service api
yl_deployment_succeeded "api" "railway" "https://api.railway.app"

# Cloudflare  
wrangler deploy worker.js
yl_deployment_succeeded "worker" "cloudflare" "https://worker.example.com"

yl_workflow_done "multi-deploy" "passed" "120s"
```

### BlackRoad Codex Integration

```bash
# Check template compliance
~/trinity-check-compliance.sh "deployment-template"

# Record test result
~/trinity-record-test.sh "deployment-template" "yellowlight" "Railway Deploy" 1 \
  "Successfully deployed to Railway using template"

# View compliance status
sqlite3 ~/.blackroad/codex/codex.db "
  SELECT * FROM trinity_compliance 
  WHERE entity_name = 'deployment-template'
"
```

### YellowLight Documentation
- `.trinity/yellowlight/docs/YELLOWLIGHT_INFRASTRUCTURE_SYSTEM.md` - Full guide

---

## 🔴 RedLight: Visual & Brand Templates

### Quick Start

```bash
# Source RedLight templates
source .trinity/redlight/scripts/memory-redlight-templates.sh
```

### Brand Template Usage

#### 1. Create Landing Page from Template

```bash
# Copy brand template
cp .trinity/redlight/templates/blackroad-ultimate.html ./my-landing.html

# Record template creation
rl_template_create "my-landing" "landing" "Product landing page from RedLight template"

# Test performance
rl_performance_metrics "my-landing" "60" "0.8" "150"

# Validate brand colors
rl_test_passed "my-landing" "visual" "BlackRoad gradient colors validated"

# Test accessibility
rl_test_passed "my-landing" "accessibility" "WCAG 2.1 AA compliant"
```

#### 2. Deploy Brand Template

```bash
# Deploy to Cloudflare Pages
cd my-landing-page
wrangler pages deploy . --project-name=my-landing

# Record deployment
rl_template_deploy "my-landing" "https://my-landing.pages.dev" "cloudflare-pages"

# Log to memory
rl_memory_stored "brand" "Deployed landing page using RedLight template"
```

#### 3. Available RedLight Templates

```bash
# List all RedLight templates
ls -1 .trinity/redlight/templates/

# Templates include:
# - blackroad-ultimate.html (main landing page)
# - blackroad-animation.html (animated experience)
# - blackroad-motion.html (motion graphics)
# - blackroad-3d-world.html (3D environments)
# - [14+ more templates]
```

### RedLight Standards

All RedLight templates must meet:

**Brand Colors** (BlackRoad gradient):
```css
#FF9D00  /* Amber */
#FF6B00  /* Orange */
#FF0066  /* Pink */
#FF006B  /* Magenta */
#D600AA  /* Purple */
#7700FF  /* Violet */
#0066FF  /* Blue */
```

**Performance Targets**:
- FPS: > 60
- Load time: < 1s
- Memory: < 200MB
- Bundle size: < 500KB

**Accessibility**:
- WCAG 2.1 AA compliant
- Keyboard navigation
- Screen reader support
- High contrast mode

### RedLight Documentation
- `.trinity/redlight/docs/REDLIGHT_TEMPLATE_SYSTEM.md` - Complete guide

---

## 🌈 Trinity Compliance Workflow

### Automated Compliance Checking

The repository includes automated Trinity compliance checking:

**GitHub Workflow**: `.github/workflows/trinity-compliance.yml`

Runs on:
- Every push to main/develop
- Every pull request
- Weekly on Sunday at midnight

### Manual Compliance Check

```bash
# Check Trinity structure
.trinity/system/trinity-check-compliance.sh

# Expected output:
# ✅ .trinity/ directory present
# 🔴 RedLight: 18 templates found
# 🟢 GreenLight: 103 template functions
# 🟡 YellowLight: Infrastructure scripts present
# 🌈 Trinity compliance check PASSED
```

### Compliance Gates

All templates must pass three gates:

#### 🔴 RedLight Gate
- Brand colors validated
- Performance targets met (>60 FPS, <1s load)
- Accessibility standards (WCAG 2.1 AA)
- Self-contained architecture
- Deploy-ready

#### 🟡 YellowLight Gate  
- Approved platform (Railway/Cloudflare/Pi/DO)
- Health endpoint present
- Rollback capability
- CI/CD pipeline configured
- Secrets properly managed
- Memory logging enabled

#### 🟢 GreenLight Gate
- State tracking enabled
- NATS event publishing
- Phase completion logging
- Cross-agent coordination
- PS-SHA∞ memory logging

---

## Integration Examples

### Example 1: Create New Service with Full Trinity Integration

```bash
# 1. GreenLight: Announce work
source .trinity/greenlight/scripts/memory-greenlight-templates.sh
gl_announce "dev-team" "Creating payment service" \
  "1) Setup 2) Implement 3) Deploy 4) Monitor" "New service development"

# 2. YellowLight: Use deployment templates
source .trinity/yellowlight/scripts/memory-yellowlight-templates.sh
cp templates/RAILWAY-SERVICE-TEMPLATE.toml railway.toml
# Customize railway.toml for payment service

# 3. RedLight: Create landing page
source .trinity/redlight/scripts/memory-redlight-templates.sh
cp .trinity/redlight/templates/blackroad-ultimate.html payment-landing.html
rl_template_create "payment-landing" "service" "Payment service landing page"

# 4. Deploy with logging
railway up --service payment-api
yl_deployment_succeeded "payment-api" "railway" "https://payment.railway.app"

# 5. Complete project
gl_phase_done "deployment" "Payment Service" \
  "Service deployed with landing page, monitoring enabled" "🌌"
```

### Example 2: Template Development Workflow

```bash
# 1. Announce template development
source .trinity/greenlight/scripts/memory-greenlight-templates.sh
gl_task_claimed "template-456" "claude-templates" "Stripe integration template"

# 2. Create template
cat > templates/STRIPE-INTEGRATION-TEMPLATE.md <<'EOF'
# Stripe Integration Template
[Template content]
EOF

# 3. Test template compliance
source .trinity/yellowlight/scripts/trinity-codex-integration.sh
~/trinity-record-test.sh "stripe-template" "greenlight" "Documentation" 1 "Complete docs"
~/trinity-record-test.sh "stripe-template" "yellowlight" "Testing" 1 "All tests pass"
~/trinity-record-test.sh "stripe-template" "redlight" "Examples" 1 "Working examples"

# 4. Verify compliance
~/trinity-check-compliance.sh "stripe-template"

# 5. Share success
gl_collaboration_success "template-456" "claude-templates" \
  "Stripe template complete, Trinity-compliant, ready for use"
```

### Example 3: Multi-Agent Template Coordination

```bash
# Agent 1: Frontend templates
source .trinity/greenlight/scripts/memory-greenlight-templates.sh
gl_agent_available "claude-frontend" "frontend" "React, HTML, CSS templates"
gl_task_claimed "template-789" "claude-frontend" "Landing page templates"

# Agent 2: Backend templates  
gl_agent_available "claude-backend" "backend" "API, database, deployment templates"
gl_task_claimed "template-790" "claude-backend" "API service templates"

# Coordination
gl_coordinate "claude-frontend" "claude-backend" \
  "Landing page needs API endpoint examples"

gl_coordinate "claude-backend" "claude-frontend" \
  "API template ready with examples"

# Combined success
gl_collaboration_success "templates" "claude-frontend,claude-backend" \
  "Complete full-stack template set with frontend and backend coordination"
```

---

## Best Practices

### 1. Always Log to Memory

Every template action should log to the appropriate light's memory system:

```bash
# GreenLight: Project events
gl_wip "task" "status" "effort" "scale"

# YellowLight: Infrastructure events  
yl_deployment_succeeded "service" "platform" "url"

# RedLight: Visual/brand events
rl_template_create "name" "category" "description"
```

### 2. Use Trinity Compliance Checks

Before finalizing any template work:

```bash
# Check compliance
~/trinity-check-compliance.sh "entity-name"

# Fix any failures
# Re-test
~/trinity-record-test.sh "entity" "light" "test" "1" "details"
```

### 3. Coordinate Across Agents

When multiple agents work on templates:

```bash
# Announce availability
gl_agent_available "agent-id" "domain" "capabilities"

# Claim tasks
gl_task_claimed "task-id" "agent-id" "description"

# Share learnings
gl_learning_discovered "topic" "insight" "impact"

# Report success
gl_collaboration_success "task-id" "agent1,agent2" "outcome"
```

### 4. Document Everything

Every template should include:
- Purpose and use case
- Trinity compliance status
- Copy-paste-ready examples
- Verification commands
- Integration with other templates

### 5. Test Thoroughly

Test templates against all three lights:
- 🔴 Brand, performance, accessibility
- 🟡 Deployment, monitoring, security
- 🟢 Tracking, coordination, memory

---

## Resources

### Trinity Documentation
- `.trinity/README.md` - Overview
- `.trinity/system/THE_LIGHT_TRINITY.md` - Complete system guide
- `.trinity/system/LIGHT_TRINITY_ENFORCEMENT.md` - Compliance standards

### Template Documentation  
- `templates/MASTER-TEMPLATE-SYSTEM.md` - Template system overview
- `templates/TEMPLATE-INDEX.md` - Template catalog
- `templates/INDEX.md` - Quick reference

### Codex Documentation
- `.trinity/yellowlight/scripts/trinity-codex-integration.sh` - Codex setup

---

## Support

**Questions?** Check the Trinity docs in `.trinity/`

**Issues?** Report via GitHub Issues

**Improvements?** All agents encouraged to enhance the system

---

🚦 **One Trinity. One Vision. Infinite Templates.** ✨
