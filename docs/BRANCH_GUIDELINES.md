# Branch Strategy and Guidelines

## Overview

This document outlines the branch strategy and guidelines for the BlackRoad OS Agents repository. Our branching model is designed to support 30,000+ AI agents working collaboratively across all repositories.

---

## Branch Hierarchy

```
main (production)
├── staging
│   └── develop
│       ├── feature/*
│       ├── agent/*
│       └── bugfix/*
└── hotfix/*
```

---

## Branch Types

### 1. Main / Master (Production)

**Purpose:** Production-ready code, deployed to live environments

**Protection Rules:**
- ✅ Requires pull request reviews (1+ approvals)
- ✅ Requires status checks to pass
- ✅ Requires RoadChain SHA-256 verification
- ✅ Requires CI/CD pipeline success
- ✅ No force pushes
- ✅ No deletions
- 🔐 Limited to repository administrators

**Merge Requirements:**
- All CI checks must pass
- Code review approval required
- No merge conflicts
- Security scans completed
- RoadChain verification successful

**Auto-Merge:** ⚠️ Disabled (manual approval required)

---

### 2. Staging

**Purpose:** Pre-production testing and validation

**Protection Rules:**
- ✅ Requires status checks to pass
- ✅ Requires RoadChain verification
- ⚠️ Reviews recommended but not required
- 🔓 Can be merged by team members

**Merge Requirements:**
- CI checks must pass
- No merge conflicts
- Automated tests successful

**Auto-Merge:** ✅ Enabled (with CI checks)

---

### 3. Develop

**Purpose:** Active development and integration

**Protection Rules:**
- ⚠️ Status checks recommended
- 🔓 Open for rapid iteration
- 🤖 Auto-merge enabled for agent PRs

**Merge Requirements:**
- No merge conflicts
- Basic linting passed (if available)

**Auto-Merge:** ✅ Enabled

---

### 4. Feature Branches

**Naming:** `feature/[ticket-number]-[brief-description]`

**Examples:**
- `feature/123-add-new-agent-type`
- `feature/456-enhance-coordination`
- `feature/789-agent-communication-api`

**Workflow:**
1. Branch from `develop`
2. Develop feature
3. Create PR to `develop`
4. After approval, merge to `develop`

**Lifespan:** Should be short-lived (< 2 weeks)

---

### 5. Agent Branches

**Naming:** `agent/[agent-id]-[task-description]`

**Examples:**
- `agent/claude-architecture-update`
- `agent/cadillac-performance-optimization`
- `agent/coordination-hub-setup`

**Workflow:**
1. Branch from `develop`
2. Agent implements changes
3. Automated PR creation
4. Auto-merge after checks

**Special Rules:**
- 🤖 Designed for AI agent workflows
- ⚡ Fast-track merge process
- 📊 Tracked in agent coordination system

---

### 6. Bugfix Branches

**Naming:** `bugfix/[issue-number]-[brief-description]`

**Examples:**
- `bugfix/321-fix-agent-registration`
- `bugfix/654-resolve-merge-conflict-handler`

**Workflow:**
1. Branch from `develop`
2. Fix bug
3. Add test to prevent regression
4. Create PR to `develop`

---

### 7. Hotfix Branches

**Naming:** `hotfix/[critical-issue]-[brief-description]`

**Examples:**
- `hotfix/security-vulnerability-patch`
- `hotfix/production-outage-fix`

**Workflow:**
1. Branch from `main`
2. Fix critical issue
3. Create PR to `main`
4. After merge, backport to `develop`

**Priority:** 🚨 Critical (emergency fixes only)

---

## Branch Protection Configuration

### Main/Master Protection

```yaml
protection:
  required_status_checks:
    strict: true
    contexts:
      - CI
      - RoadChain SHA-256 Verification
      - Security Scan
      - Code Review
  required_pull_request_reviews:
    required_approving_review_count: 1
    dismiss_stale_reviews: true
    require_code_owner_reviews: true
  enforce_admins: true
  restrictions: null
  allow_force_pushes: false
  allow_deletions: false
```

### Staging Protection

```yaml
protection:
  required_status_checks:
    strict: true
    contexts:
      - CI
      - RoadChain SHA-256 Verification
  required_pull_request_reviews:
    required_approving_review_count: 0
  enforce_admins: false
  allow_force_pushes: false
  allow_deletions: false
```

---

## Auto-Merge Rules

### Enabled For:
- ✅ `develop` branch (all PRs)
- ✅ `staging` branch (after CI)
- ✅ `agent/*` branches (automated workflows)
- ✅ `feature/*` branches (with `auto-merge` label)

### Disabled For:
- ❌ `main/master` branch (requires manual approval)
- ❌ `hotfix/*` branches (requires review)

### Auto-Merge Conditions:
1. All required CI checks passed
2. No merge conflicts
3. RoadChain verification successful
4. Required reviews obtained (if applicable)
5. `auto-merge` label present (for feature branches)

---

## Commit Guidelines

### Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test additions/changes
- `chore`: Build/tooling changes
- `agent`: Agent-specific changes

**Examples:**
```
feat(agent): add new coordination protocol for 30k agents

Implements distributed mesh coordination protocol to support
communication across 30,000 AI agents.

RoadChain: verified
Issue: #123
```

```
fix(security): patch vulnerability in agent authentication

Addresses security issue in agent token validation.

RoadChain: verified
CVE: pending
Priority: critical
```

### Commit Signing

**Recommended:** GPG or SSH signing for all commits

**Required for:**
- Commits to `main/master`
- Commits by human contributors
- Security-related changes

**Optional for:**
- Automated agent commits
- Non-critical development branches

---

## RoadChain Integration

All commits are tracked using **RoadChain SHA-256 verification**.

### What RoadChain Provides:
- 🔗 Immutable commit chain
- 🔐 SHA-256 integrity verification
- 📊 Full audit trail
- ✅ Tamper detection
- 🌐 Cross-repository tracking

### RoadChain Workflow:
1. Commit is pushed
2. RoadChain workflow triggered
3. SHA-256 hash generated
4. Verification record created
5. Commit chain updated
6. Artifact archived (90 days)

---

## Agent Collaboration Guidelines

### For 30,000 Agent Scale:

1. **Coordination Hub**
   - Use agent coordination workflow
   - Register agent actions in central hub
   - Follow distributed mesh protocol

2. **Communication**
   - Use cross-repository dispatch
   - Follow standardized message format
   - Log all agent interactions

3. **Conflict Resolution**
   - Automated conflict detection
   - Priority-based merge order
   - Escalation to human oversight when needed

4. **Resource Management**
   - Rate limiting per agent layer
   - Queued execution for bulk operations
   - Load balancing across agent pools

---

## Branch Lifecycle

### Feature Branch Lifecycle:
1. **Create** from `develop`
2. **Develop** with regular commits
3. **Sync** with `develop` regularly
4. **Review** via pull request
5. **Merge** to `develop`
6. **Delete** after merge

### Agent Branch Lifecycle:
1. **Auto-create** by agent workflow
2. **Implement** changes programmatically
3. **Auto-test** via CI
4. **Auto-merge** on success
5. **Auto-delete** after merge

---

## Emergency Procedures

### Production Hotfix:
1. Create `hotfix/*` branch from `main`
2. Implement fix with tests
3. Create PR with `URGENT` label
4. Expedited review process
5. Merge to `main`
6. Immediately backport to `develop`

### Rollback Procedure:
1. Identify problematic commit
2. Create revert PR
3. Fast-track review
4. Deploy reverted code
5. Create issue for proper fix

---

## Branch Naming Conventions

| Pattern | Purpose | Example |
|---------|---------|---------|
| `feature/*` | New features | `feature/123-agent-api` |
| `bugfix/*` | Bug fixes | `bugfix/456-fix-validation` |
| `agent/*` | Agent changes | `agent/claude-refactor` |
| `hotfix/*` | Critical fixes | `hotfix/security-patch` |
| `release/*` | Release prep | `release/v2.0.0` |
| `docs/*` | Documentation | `docs/update-readme` |
| `chore/*` | Maintenance | `chore/update-deps` |

---

## Code Owners

See `.github/CODEOWNERS` for detailed ownership mapping.

**Key Owners:**
- `/registry/*` → Agent Registry Team
- `/.github/workflows/*` → DevOps Team
- `/src/*` → Core Development Team
- `/docs/*` → Documentation Team
- `/LICENSE` → Legal/Leadership Team

---

## Best Practices

### ✅ Do:
- Keep branches short-lived
- Sync with base branch frequently
- Write descriptive commit messages
- Add tests for new features
- Follow RoadChain verification
- Use auto-merge for eligible PRs
- Delete branches after merge

### ❌ Don't:
- Force push to protected branches
- Commit secrets or credentials
- Merge without CI passing
- Skip required reviews
- Leave stale branches open
- Bypass RoadChain verification
- Merge with conflicts

---

## Monitoring and Metrics

### Branch Health Metrics:
- Average PR merge time
- Number of merge conflicts
- CI success rate
- Auto-merge success rate
- RoadChain verification rate

### Agent Coordination Metrics:
- Active agent count
- Agent collaboration events
- Cross-repository communications
- Coordination hub throughput

---

## Questions and Support

For questions about branch strategy:
- **Technical:** Create issue with `question` label
- **Policy:** Contact Policy Steward agent
- **Emergency:** Escalate to Ops Sheriff

---

## Version History

- **v1.0.0** (2025-01-04): Initial branch guidelines for 30k agent scale
- **v1.1.0** (TBD): Enhanced coordination protocols

---

**Document Owner:** DevOps & Agent Coordination Team  
**Last Updated:** 2025-01-04  
**Next Review:** Quarterly or as needed for scale adjustments
