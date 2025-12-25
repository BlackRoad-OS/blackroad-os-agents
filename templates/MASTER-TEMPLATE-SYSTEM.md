# 🎯 BlackRoad OS Master Template System

**Copy-Paste-Ready Templates for EVERYTHING Across ALL Platforms**

🚦 **Powered by the Light Trinity System** (🟢 GreenLight · 🟡 YellowLight · 🔴 RedLight)

---

## 📋 Template Philosophy

**The Revolutionary Pattern**: Copy-Paste-And-Learn

1. **Zero cognitive load** - No thinking, just paste and GO
2. **Self-documenting** - Comments explain everything
3. **Machine-teachable** - AI learns from the patterns
4. **Error-proof** - No typing mistakes
5. **Teaching by doing** - Learn while it works
6. **Trinity-compliant** - All templates follow GreenLight, YellowLight, RedLight standards

---

## 🚦 Light Trinity Integration

This template system is fully integrated with **The Light Trinity** - BlackRoad OS's unified intelligence, templating, and infrastructure system:

### 🟢 GreenLight - Project Management Templates
- Task tracking and workflow templates
- State management for project lifecycle
- NATS event bus integration for real-time updates
- 103 template functions for logging and coordination

### 🟡 YellowLight - Infrastructure Templates  
- Deployment automation templates
- Platform configurations (Railway, Cloudflare, DigitalOcean)
- CI/CD pipeline templates
- BlackRoad Codex integration for accessing 8,789+ reusable components

### 🔴 RedLight - Visual & Brand Templates
- 18 HTML brand templates for landing pages and 3D experiences
- Design system following golden ratio (φ = 1.618)
- Brand gradient: Amber → Hot Pink → Violet → Electric Blue
- Performance-optimized (>60 FPS, <1s load time)

**See:** `.trinity/README.md` for complete Trinity documentation

---

## 🛣️ BlackRoad Codex Integration

All templates are registered in the **BlackRoad Codex** - our verification and memory system:

- **Codex Database**: `~/.blackroad/codex/codex.db`
- **Trinity Standards**: Automated compliance checking via `trinity_standards` table
- **Template Validation**: Each template tested against GreenLight, YellowLight, RedLight gates
- **Usage Tracking**: Template usage logged to PS-SHA∞ memory system

**Setup Codex Integration:**
```bash
# Initialize Codex integration
source .trinity/yellowlight/scripts/trinity-codex-integration.sh

# Check template compliance
~/trinity-check-compliance.sh "my-template"

# Record test results  
~/trinity-record-test.sh "my-template" "redlight" "Brand Colors" 1 "Gradient validated"
```

---

## 🗂️ Template Categories

### 1. Core Development Templates
- `README-TEMPLATE.md` - Perfect README for any repo
- `DEPLOYMENT-GUIDE-TEMPLATE.md` - Complete deployment docs
- `SCRIPT-TEMPLATE.sh` - Bash scripts with menu mode
- `PYTHON-SERVICE-TEMPLATE.py` - Flask/FastAPI service skeleton
- `DOCKER-TEMPLATE/` - Dockerfile + docker-compose templates
- `GITHUB-ACTIONS-TEMPLATE/` - CI/CD workflow templates

### 2. Platform Integration Templates

#### Google Drive Templates
- `google-drive/PROJECT-TEMPLATE/` - Complete project structure
- `google-drive/DOCS-TEMPLATE.gdoc` - Documentation template
- `google-drive/SPREADSHEET-TEMPLATE.gsheet` - Data tracking
- `google-drive/SLIDES-TEMPLATE.gslides` - Presentation deck
- `google-drive/FORM-TEMPLATE.gform` - User input forms

#### Notion Templates
- `notion/PROJECT-DASHBOARD-TEMPLATE` - Project management
- `notion/WIKI-TEMPLATE` - Documentation wiki
- `notion/ROADMAP-TEMPLATE` - Product roadmap
- `notion/MEETING-NOTES-TEMPLATE` - Meeting tracker
- `notion/AGENT-PROFILE-TEMPLATE` - Agent documentation

#### GitHub Templates
- `github/ISSUE-TEMPLATES/` - Bug, feature, docs templates
- `github/PR-TEMPLATE.md` - Pull request template
- `github/REPO-TEMPLATE/` - Complete repo structure
- `github/WORKFLOWS-TEMPLATE/` - GitHub Actions workflows
- `github/SECURITY-TEMPLATE/` - Security policy, CODEOWNERS

#### Linear/Jira/Asana Templates
- `task-management/PROJECT-TEMPLATE` - Project structure
- `task-management/SPRINT-TEMPLATE` - Sprint planning
- `task-management/EPIC-TEMPLATE` - Epic/milestone template
- `task-management/TASK-TEMPLATE` - Task breakdown

#### Airtable Templates
- `airtable/CRM-TEMPLATE` - Customer relationship management
- `airtable/CONTACTS-TEMPLATE` - Contact database
- `airtable/DEALS-TEMPLATE` - Sales pipeline
- `airtable/PROJECTS-TEMPLATE` - Project tracking
- `airtable/INVENTORY-TEMPLATE` - Asset/resource tracking

### 3. Domain & Deployment Templates

#### Cloudflare Templates
- `cloudflare/WORKER-TEMPLATE.js` - Cloudflare Worker skeleton
- `cloudflare/PAGES-TEMPLATE/` - Static site structure
- `cloudflare/DNS-TEMPLATE.json` - DNS configuration
- `cloudflare/ZERO-TRUST-TEMPLATE.json` - Security rules
- `cloudflare/WRANGLER-TEMPLATE.toml` - Worker config

#### Railway Templates
- `railway/SERVICE-TEMPLATE.toml` - Railway service config
- `railway/NIXPACKS-TEMPLATE.toml` - Build configuration
- `railway/SECRETS-TEMPLATE.env` - Environment variables
- `railway/HEALTH-CHECK-TEMPLATE.py` - Health endpoint

#### Vercel Templates
- `vercel/PROJECT-TEMPLATE/` - Next.js/React app
- `vercel/VERCEL-JSON-TEMPLATE.json` - Deployment config
- `vercel/SERVERLESS-TEMPLATE/` - Serverless functions
- `vercel/ENV-TEMPLATE.local` - Environment setup

### 4. Subdomain Templates (5,216 Sites)

#### Per-Domain Subdomain Structure
```
subdomain-templates/
├── LANDING-PAGE-TEMPLATE.html     # Generic landing page
├── API-SUBDOMAIN-TEMPLATE/        # API service page
├── DASHBOARD-SUBDOMAIN-TEMPLATE/  # Dashboard app page
├── DOCS-SUBDOMAIN-TEMPLATE/       # Documentation site
├── AUTH-SUBDOMAIN-TEMPLATE/       # Auth service page
├── PAYMENT-SUBDOMAIN-TEMPLATE/    # Payment integration page
├── AGENT-SUBDOMAIN-TEMPLATE/      # Agent portal page
└── QUANTUM-SUBDOMAIN-TEMPLATE/    # Quantum computing page
```

#### Domain-Specific Templates (16 Domains × 364 Subdomains)
- `blackroad-io/` - Main platform templates
- `lucidia-earth/` - Lucidia OS templates
- `blackroadai-com/` - AI-focused templates
- `blackroadquantum-com/` - Quantum computing templates
- *(13 more domains...)*

### 5. Integration Templates (15+ Platforms)

```
integrations/
├── stripe/
│   ├── CHECKOUT-TEMPLATE.html
│   ├── WEBHOOK-HANDLER-TEMPLATE.py
│   └── PRODUCT-SETUP-TEMPLATE.sh
├── clerk/
│   ├── AUTH-TEMPLATE.html
│   ├── USER-PROFILE-TEMPLATE.tsx
│   └── MIDDLEWARE-TEMPLATE.ts
├── resend/
│   ├── EMAIL-TEMPLATE.html
│   └── SEND-TEMPLATE.py
├── asana/
│   ├── PROJECT-TEMPLATE.json
│   └── TASK-AUTOMATION-TEMPLATE.py
├── notion/
│   ├── DATABASE-TEMPLATE.json
│   └── PAGE-SYNC-TEMPLATE.py
└── (13 more platforms...)
```

---

## 🚀 Quick Start: Using Templates

### Example 1: Create New Repo from Template

```bash
# Copy the complete repo template
cp -r templates/github/REPO-TEMPLATE/ ../my-new-repo/

# Customize with your project name
cd ../my-new-repo
./setup-from-template.sh "My New Project" "https://github.com/BlackRoad-OS/my-new-repo"

# Result: Complete repo with:
# - README.md (filled in)
# - .github/workflows/ (CI/CD ready)
# - Dockerfile + docker-compose.yml
# - Railway config
# - Vercel config
# - All ready to deploy!
```

### Example 2: Deploy New Subdomain from Template

```bash
# Generate subdomain page from template
python3 generate-subdomain-from-template.py \
  --domain="blackroad.io" \
  --subdomain="quantum-api" \
  --template="API-SUBDOMAIN-TEMPLATE" \
  --title="Quantum Computing API" \
  --description="Access quantum algorithms via REST API"

# Deploy to Cloudflare Pages
cd subdomain-pages-blackroad-io/quantum-api
wrangler pages deploy . --project-name=quantum-api-blackroad-io

# Result: Live at quantum-api.blackroad.io in < 1 minute!
```

### Example 3: Create Google Drive Project from Template

```bash
# Authenticate with Google Drive
python3 blackroad-google-drive.py auth

# Create project from template
python3 create-google-drive-project.py \
  --template="PROJECT-TEMPLATE" \
  --name="Q4 2025 Product Launch" \
  --folder="BlackRoad OS/Projects/2025/"

# Result: Complete folder structure with:
# - Project charter document
# - Timeline spreadsheet
# - Team roster
# - Meeting notes template
# - Roadmap slides
```

### Example 4: Set Up Notion Workspace from Template

```bash
# Import Notion templates
python3 blackroad-notion-service.py import-templates \
  --workspace="BlackRoad OS" \
  --templates="templates/notion/"

# Create new project from template
curl -X POST http://localhost:9700/api/integrations/notion/projects \
  -H "Content-Type: application/json" \
  -d '{
    "template": "PROJECT-DASHBOARD-TEMPLATE",
    "name": "Agent Recall System v2",
    "team": ["Alexa", "Lucidia", "Cecilia"]
  }'

# Result: Complete Notion workspace with:
# - Project dashboard
# - Task database
# - Documentation pages
# - Team wiki
# - Meeting notes section
```

---

## 📦 Template Distribution

### Auto-Sync to All 43 Repos

```bash
# Sync all templates to all repos
./sync-templates-to-all-repos.sh

# What it does:
# 1. Copies latest templates/ directory to all 43 repos
# 2. Runs customization scripts per repo
# 3. Creates PR in each repo with updated templates
# 4. Auto-merges if CI passes
```

### Auto-Deploy to All 5,216 Subdomains

```bash
# Generate all subdomain pages from templates
python3 generate-all-subdomains-from-templates.py

# Deploy all to Cloudflare Pages
./deploy-all-subdomains-pages.sh

# What it does:
# 1. Generates 364 subdomain pages per domain (16 domains)
# 2. Customizes each page with domain-specific branding
# 3. Deploys to Cloudflare Pages
# 4. Updates DNS routing
# 5. Verifies all 5,216 sites are live
```

### Auto-Import to All Integration Platforms

```bash
# Import templates to all platforms
./import-templates-to-all-platforms.sh

# What it does:
# - Google Drive: Creates template library
# - Notion: Imports all page templates
# - GitHub: Creates template repositories
# - Linear: Imports project/task templates
# - Jira: Imports issue templates
# - Asana: Imports project templates
# - Airtable: Creates base templates
# - (15+ total platforms)
```

---

## 🎨 Template Customization

### Variables System

All templates support variable substitution:

```bash
# Variables defined in template-vars.yaml
PROJECT_NAME: "My Awesome Project"
DOMAIN: "blackroad.io"
SUBDOMAIN: "api"
REPO_URL: "https://github.com/BlackRoad-OS/my-awesome-project"
AUTHOR: "Alexa Louise Amundson"
YEAR: "2025"
STRIPE_ENABLED: true
CLERK_ENABLED: true

# Usage in templates:
# README-TEMPLATE.md contains: {{PROJECT_NAME}}
# After processing: My Awesome Project
```

### Conditional Sections

```html
<!-- In HTML templates -->
{{#if STRIPE_ENABLED}}
<script src="https://js.stripe.com/v3/"></script>
{{/if}}

{{#if CLERK_ENABLED}}
<script src="https://clerk.dev/v3/"></script>
{{/if}}
```

### Dynamic Content

```python
# In Python templates
# {{GENERATED_ROUTES}}
# Auto-generates Flask routes based on config

# {{GENERATED_MODELS}}
# Auto-generates SQLAlchemy models from schema

# {{GENERATED_TESTS}}
# Auto-generates pytest tests from endpoints
```

---

## 🔄 Template Update Workflow

### When Templates Change

```bash
# 1. Update master templates in blackroad-sandbox/templates/
vim templates/README-TEMPLATE.md

# 2. Run template sync
./sync-templates-to-all-repos.sh

# 3. Verify changes
./verify-template-sync.sh

# 4. Deploy updated subdomains
./deploy-updated-subdomains.sh

# Result: All 43 repos + 5,216 sites updated automatically!
```

---

## 📊 Template Analytics

### Track Template Usage

```bash
# See which templates are most used
./template-analytics.sh

# Output:
Template                          Usage Count  Last Used
--------------------------------  -----------  --------------------
README-TEMPLATE.md                43 repos     2025-12-12 10:30:00
API-SUBDOMAIN-TEMPLATE            872 sites    2025-12-12 09:15:00
PYTHON-SERVICE-TEMPLATE.py        28 repos     2025-12-11 14:22:00
NOTION/PROJECT-DASHBOARD          156 projects 2025-12-10 16:45:00
```

---

## 🎯 Master Template Catalog

### Complete List (200+ Templates)

1. **Development** (25 templates)
   - README, Dockerfile, docker-compose, package.json, requirements.txt, etc.

2. **CI/CD** (15 templates)
   - GitHub Actions workflows, Railway configs, Vercel configs, etc.

3. **Documentation** (20 templates)
   - User guides, API docs, architecture diagrams, etc.

4. **Google Drive** (30 templates)
   - Docs, Sheets, Slides, Forms across all project types

5. **Notion** (25 templates)
   - Dashboards, wikis, databases, pages, etc.

6. **GitHub** (20 templates)
   - Issues, PRs, repos, workflows, security, etc.

7. **Task Management** (15 templates)
   - Linear, Jira, Asana project/task templates

8. **Airtable** (10 templates)
   - CRM, contacts, deals, projects, inventory

9. **Cloudflare** (20 templates)
   - Workers, Pages, DNS, Zero Trust, etc.

10. **Railway** (10 templates)
    - Service configs, health checks, secrets, etc.

11. **Vercel** (10 templates)
    - Next.js apps, serverless functions, configs

12. **Subdomains** (5,216 variations)
    - 364 templates × 16 domains = complete coverage

13. **Integrations** (15 templates)
    - Stripe, Clerk, Resend, all 15 platforms

---

## 🚀 Template Deployment Commands

### Deploy Everything

```bash
# ONE COMMAND TO RULE THEM ALL
./deploy-all-templates-everywhere.sh

# What it does:
# ✅ Syncs templates to all 43 GitHub repos
# ✅ Imports templates to Google Drive
# ✅ Imports templates to Notion
# ✅ Imports templates to Linear/Jira/Asana
# ✅ Imports templates to Airtable
# ✅ Generates all 5,216 subdomain pages
# ✅ Deploys all subdomains to Cloudflare Pages
# ✅ Updates all Railway services
# ✅ Updates all Vercel projects
# ✅ Verifies all deployments
# ✅ Generates usage report

# Time: ~15 minutes
# Result: EVERYTHING updated across ALL platforms!
```

---

## 📚 Template Documentation

Each template includes:

1. **Header Comment**
   ```
   # ============================================================================
   # Template: README-TEMPLATE.md
   # Purpose: Perfect README for any BlackRoad OS repository
   # Variables: PROJECT_NAME, DESCRIPTION, REPO_URL, AUTHOR
   # Last Updated: 2025-12-12
   # ============================================================================
   ```

2. **Usage Instructions**
   - How to use the template
   - Required variables
   - Optional customizations
   - Example output

3. **Customization Guide**
   - Which sections to customize
   - Which to keep as-is
   - Best practices

4. **Examples**
   - Real-world examples from existing repos
   - Before/after comparisons

---

## 🎉 Template Benefits

### Developer Experience
- **10x faster** project setup
- **Zero boilerplate** writing
- **Consistent quality** across all projects
- **Always up-to-date** with latest practices

### Team Collaboration
- **Shared knowledge** embedded in templates
- **Onboarding time** cut from days to minutes
- **Code review** faster with consistent structure
- **Documentation** always complete

### Deployment Speed
- **New subdomain**: < 1 minute
- **New repo**: < 5 minutes
- **New integration**: < 2 minutes
- **Complete project**: < 15 minutes

### Maintenance
- **One update** propagates everywhere
- **No drift** between projects
- **Automated sync** keeps everything current
- **Version control** for all templates

---

## 🔥 Advanced Template Features

### Template Inheritance

```yaml
# base-service-template.yaml
base: PYTHON-SERVICE-TEMPLATE
extends:
  - auth-mixin
  - database-mixin
  - stripe-mixin
  - clerk-mixin
```

### Template Composition

```bash
# Combine multiple templates
./compose-template.sh \
  --base="PYTHON-SERVICE-TEMPLATE" \
  --add="AUTH-MIXIN" \
  --add="STRIPE-MIXIN" \
  --add="WEBSOCKET-MIXIN" \
  --output="my-custom-service.py"
```

### Template Generation

```bash
# Generate new template from existing code
./generate-template.sh \
  --from="blackroad-agent-orchestrator.py" \
  --name="AGENT-SERVICE-TEMPLATE" \
  --extract-patterns
```

---

## 📖 Template Index

See `TEMPLATE-INDEX.md` for complete catalog of all 200+ templates with:
- Description
- Usage examples
- Variables
- Customization options
- Related templates
- Example output

---

## 🎯 Next Steps

1. **Browse Templates**: `ls -R templates/`
2. **Use a Template**: Copy & customize
3. **Create New Template**: Follow the template-template 😉
4. **Share Template**: PR to blackroad-sandbox/templates/
5. **Deploy Templates**: Run sync scripts

**The goal**: Never write boilerplate again. Ever. 🚀

---

## 📞 Template Support

- **Issues**: Use GitHub template issue template 😄
- **Questions**: blackroad.systems@gmail.com
- **Contributions**: PR welcome for new templates!

---

**Remember**: A perfect template is one you never have to think about. It just works. ✨

---

## 🚦 See Also

- **Trinity Integration Guide**: `TRINITY-INTEGRATION-GUIDE.md` - Complete guide on using GreenLight, YellowLight, and RedLight with templates
- **Trinity System**: `.trinity/README.md` - Full Light Trinity documentation
- **Template Index**: `TEMPLATE-INDEX.md` - Complete template catalog
- **Copy-Paste Library**: `COPY-PASTE-COMMANDS-LIBRARY.md` - Command reference
