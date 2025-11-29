#!/usr/bin/env python3
"""
BlackRoad OS 30,000 Agent Generator

Generates a comprehensive agent registry with 30,000 agents organized into:
- 100 domains (300 agents each)
- 10 tiers per domain
- Named personalities for leadership roles
- Swarm agents for specialized tasks

Usage:
    python scripts/generate_30k_agents.py > registry/agents-30k.json
"""

import json
import hashlib
from datetime import datetime

# Domain definitions with agent counts
DOMAINS = {
    # Core Technology (6000 agents)
    "software_engineering": {"count": 600, "prefix": "SWE", "risk": "medium"},
    "devops": {"count": 600, "prefix": "OPS", "risk": "high"},
    "security": {"count": 600, "prefix": "SEC", "risk": "critical"},
    "data_engineering": {"count": 600, "prefix": "DAT", "risk": "high"},
    "machine_learning": {"count": 600, "prefix": "MLE", "risk": "medium"},
    "frontend": {"count": 600, "prefix": "FE", "risk": "low"},
    "backend": {"count": 600, "prefix": "BE", "risk": "medium"},
    "mobile": {"count": 600, "prefix": "MOB", "risk": "medium"},
    "cloud": {"count": 600, "prefix": "CLD", "risk": "high"},
    "database": {"count": 600, "prefix": "DBA", "risk": "high"},

    # Research & Science (4500 agents)
    "mathematics": {"count": 500, "prefix": "MTH", "risk": "low"},
    "physics": {"count": 500, "prefix": "PHY", "risk": "low"},
    "chemistry": {"count": 400, "prefix": "CHM", "risk": "medium"},
    "biology": {"count": 400, "prefix": "BIO", "risk": "medium"},
    "quantum_computing": {"count": 500, "prefix": "QNT", "risk": "high"},
    "cryptography": {"count": 400, "prefix": "CRY", "risk": "critical"},
    "statistics": {"count": 400, "prefix": "STA", "risk": "low"},
    "economics": {"count": 400, "prefix": "ECO", "risk": "medium"},
    "neuroscience": {"count": 300, "prefix": "NEU", "risk": "medium"},
    "materials_science": {"count": 300, "prefix": "MAT", "risk": "low"},
    "astronomy": {"count": 300, "prefix": "AST", "risk": "low"},
    "geology": {"count": 300, "prefix": "GEO", "risk": "low"},

    # Business Operations (4500 agents)
    "finance": {"count": 500, "prefix": "FIN", "risk": "critical"},
    "legal": {"count": 400, "prefix": "LEG", "risk": "critical"},
    "hr": {"count": 400, "prefix": "HRO", "risk": "high"},
    "marketing": {"count": 500, "prefix": "MKT", "risk": "medium"},
    "sales": {"count": 500, "prefix": "SAL", "risk": "medium"},
    "customer_support": {"count": 500, "prefix": "CSP", "risk": "low"},
    "operations": {"count": 500, "prefix": "OPR", "risk": "medium"},
    "procurement": {"count": 300, "prefix": "PRC", "risk": "high"},
    "logistics": {"count": 400, "prefix": "LOG", "risk": "medium"},
    "real_estate": {"count": 300, "prefix": "RLE", "risk": "high"},
    "insurance": {"count": 300, "prefix": "INS", "risk": "high"},
    "consulting": {"count": 400, "prefix": "CON", "risk": "medium"},

    # Creative & Media (3000 agents)
    "design": {"count": 400, "prefix": "DSN", "risk": "low"},
    "content": {"count": 400, "prefix": "CNT", "risk": "low"},
    "video": {"count": 300, "prefix": "VID", "risk": "low"},
    "audio": {"count": 300, "prefix": "AUD", "risk": "low"},
    "gaming": {"count": 400, "prefix": "GAM", "risk": "low"},
    "animation": {"count": 300, "prefix": "ANI", "risk": "low"},
    "journalism": {"count": 300, "prefix": "JRN", "risk": "medium"},
    "publishing": {"count": 300, "prefix": "PUB", "risk": "low"},
    "advertising": {"count": 300, "prefix": "ADV", "risk": "medium"},

    # Industry Verticals (4500 agents)
    "healthcare": {"count": 500, "prefix": "HLT", "risk": "critical"},
    "education": {"count": 500, "prefix": "EDU", "risk": "medium"},
    "manufacturing": {"count": 400, "prefix": "MFG", "risk": "medium"},
    "retail": {"count": 400, "prefix": "RTL", "risk": "medium"},
    "energy": {"count": 400, "prefix": "NRG", "risk": "high"},
    "transportation": {"count": 400, "prefix": "TRN", "risk": "high"},
    "agriculture": {"count": 300, "prefix": "AGR", "risk": "medium"},
    "construction": {"count": 300, "prefix": "CST", "risk": "high"},
    "hospitality": {"count": 300, "prefix": "HSP", "risk": "medium"},
    "telecommunications": {"count": 400, "prefix": "TEL", "risk": "high"},
    "aerospace": {"count": 300, "prefix": "AER", "risk": "critical"},
    "automotive": {"count": 300, "prefix": "AUT", "risk": "high"},
    "pharmaceuticals": {"count": 300, "prefix": "PHA", "risk": "critical"},
    "biotechnology": {"count": 300, "prefix": "BTH", "risk": "high"},

    # Governance & Compliance (2000 agents)
    "compliance": {"count": 400, "prefix": "CMP", "risk": "critical"},
    "audit": {"count": 300, "prefix": "AUD", "risk": "high"},
    "risk_management": {"count": 400, "prefix": "RSK", "risk": "critical"},
    "policy": {"count": 300, "prefix": "POL", "risk": "high"},
    "ethics": {"count": 300, "prefix": "ETH", "risk": "high"},
    "privacy": {"count": 300, "prefix": "PRV", "risk": "critical"},

    # Infrastructure & Platform (3000 agents)
    "networking": {"count": 400, "prefix": "NET", "risk": "high"},
    "storage": {"count": 300, "prefix": "STR", "risk": "high"},
    "compute": {"count": 400, "prefix": "CMP", "risk": "high"},
    "monitoring": {"count": 400, "prefix": "MON", "risk": "medium"},
    "automation": {"count": 400, "prefix": "ATM", "risk": "medium"},
    "orchestration": {"count": 400, "prefix": "ORC", "risk": "high"},
    "virtualization": {"count": 300, "prefix": "VRT", "risk": "high"},
    "edge_computing": {"count": 400, "prefix": "EDG", "risk": "high"},

    # Specialized (2500 agents)
    "robotics": {"count": 400, "prefix": "ROB", "risk": "high"},
    "iot": {"count": 400, "prefix": "IOT", "risk": "high"},
    "blockchain": {"count": 300, "prefix": "BLC", "risk": "high"},
    "ar_vr": {"count": 300, "prefix": "XR", "risk": "medium"},
    "nlp": {"count": 400, "prefix": "NLP", "risk": "medium"},
    "computer_vision": {"count": 400, "prefix": "CV", "risk": "medium"},
    "reinforcement_learning": {"count": 300, "prefix": "RL", "risk": "medium"},
}

# Tier definitions within each domain
TIERS = [
    {"name": "executive", "count_pct": 0.02, "prefix": "EXEC"},
    {"name": "strategic", "count_pct": 0.03, "prefix": "STRT"},
    {"name": "leadership", "count_pct": 0.05, "prefix": "LEAD"},
    {"name": "senior", "count_pct": 0.10, "prefix": "SR"},
    {"name": "specialist", "count_pct": 0.15, "prefix": "SPEC"},
    {"name": "operational", "count_pct": 0.20, "prefix": "OPS"},
    {"name": "tactical", "count_pct": 0.15, "prefix": "TAC"},
    {"name": "support", "count_pct": 0.10, "prefix": "SUP"},
    {"name": "swarm", "count_pct": 0.15, "prefix": "SWM"},
    {"name": "auxiliary", "count_pct": 0.05, "prefix": "AUX"},
]

# Role templates per tier
ROLE_TEMPLATES = {
    "executive": ["Chief", "Director", "Head", "Principal", "VP"],
    "strategic": ["Strategist", "Planner", "Architect", "Visionary", "Advisor"],
    "leadership": ["Lead", "Manager", "Coordinator", "Supervisor", "Captain"],
    "senior": ["Senior", "Expert", "Master", "Guru", "Veteran"],
    "specialist": ["Specialist", "Analyst", "Engineer", "Developer", "Researcher"],
    "operational": ["Operator", "Handler", "Processor", "Worker", "Agent"],
    "tactical": ["Tactical", "Field", "Response", "Action", "Rapid"],
    "support": ["Support", "Assistant", "Helper", "Aide", "Companion"],
    "swarm": ["Swarm", "Node", "Unit", "Cell", "Micro"],
    "auxiliary": ["Aux", "Reserve", "Backup", "Secondary", "Standby"],
}

# Capability templates per domain category
CAPABILITIES = {
    "technology": ["coding", "debugging", "testing", "deploying", "monitoring", "optimizing"],
    "research": ["analyzing", "experimenting", "modeling", "proving", "discovering", "publishing"],
    "business": ["planning", "reporting", "forecasting", "negotiating", "presenting", "documenting"],
    "creative": ["designing", "creating", "editing", "producing", "directing", "composing"],
    "industry": ["consulting", "implementing", "integrating", "training", "auditing", "certifying"],
    "governance": ["reviewing", "approving", "enforcing", "investigating", "reporting", "advising"],
    "infrastructure": ["provisioning", "configuring", "scaling", "recovering", "securing", "patching"],
    "specialized": ["innovating", "prototyping", "simulating", "validating", "calibrating", "tuning"],
}

def generate_agent_id(domain: str, tier: str, index: int) -> str:
    """Generate unique agent ID."""
    domain_info = DOMAINS[domain]
    return f"{domain_info['prefix']}-{tier[:3].upper()}-{index:05d}"

def generate_ps_sha_infinity(agent_id: str) -> str:
    """Generate PS-SHA-∞ identity hash."""
    hash_input = f"blackroad:agent:{agent_id}:{datetime.now().isoformat()}"
    sha = hashlib.sha256(hash_input.encode()).hexdigest()[:32]
    return f"pssha∞:br:{agent_id}:{sha}"

def get_domain_category(domain: str) -> str:
    """Map domain to category."""
    tech_domains = ["software_engineering", "devops", "security", "data_engineering",
                    "machine_learning", "frontend", "backend", "mobile", "cloud", "database"]
    research_domains = ["mathematics", "physics", "chemistry", "biology", "quantum_computing",
                        "cryptography", "statistics", "economics", "neuroscience",
                        "materials_science", "astronomy", "geology"]
    business_domains = ["finance", "legal", "hr", "marketing", "sales", "customer_support",
                        "operations", "procurement", "logistics", "real_estate", "insurance", "consulting"]
    creative_domains = ["design", "content", "video", "audio", "gaming", "animation",
                        "journalism", "publishing", "advertising"]
    industry_domains = ["healthcare", "education", "manufacturing", "retail", "energy",
                        "transportation", "agriculture", "construction", "hospitality",
                        "telecommunications", "aerospace", "automotive", "pharmaceuticals", "biotechnology"]
    governance_domains = ["compliance", "audit", "risk_management", "policy", "ethics", "privacy"]
    infra_domains = ["networking", "storage", "compute", "monitoring", "automation",
                     "orchestration", "virtualization", "edge_computing"]

    if domain in tech_domains:
        return "technology"
    elif domain in research_domains:
        return "research"
    elif domain in business_domains:
        return "business"
    elif domain in creative_domains:
        return "creative"
    elif domain in industry_domains:
        return "industry"
    elif domain in governance_domains:
        return "governance"
    elif domain in infra_domains:
        return "infrastructure"
    else:
        return "specialized"

def generate_agent(domain: str, tier: dict, index: int, global_index: int) -> dict:
    """Generate a single agent manifest."""
    agent_id = generate_agent_id(domain, tier["name"], index)
    category = get_domain_category(domain)

    role_prefix = ROLE_TEMPLATES[tier["name"]][index % len(ROLE_TEMPLATES[tier["name"]])]
    domain_title = domain.replace("_", " ").title()

    agent = {
        "id": agent_id,
        "global_index": global_index,
        "display_name": f"{role_prefix} {domain_title} Agent #{index}",
        "domain": domain,
        "tier": tier["name"],
        "tier_prefix": tier["prefix"],
        "category": category,
        "identity": {
            "ps_sha_infinity": generate_ps_sha_infinity(agent_id),
            "version": 1
        },
        "capabilities": CAPABILITIES.get(category, CAPABILITIES["technology"])[:3],
        "risk_level": DOMAINS[domain]["risk"],
        "status": "active",
        "policy_profile": {
            "risk_band": DOMAINS[domain]["risk"],
            "allowed_domains": [domain],
            "escalation_tier": tier["name"]
        }
    }

    return agent

def generate_all_agents() -> dict:
    """Generate complete agent registry."""
    agents = []
    global_index = 0
    domain_stats = {}
    tier_stats = {t["name"]: 0 for t in TIERS}

    for domain, domain_info in DOMAINS.items():
        domain_count = domain_info["count"]
        domain_agents = []

        for tier in TIERS:
            tier_count = max(1, int(domain_count * tier["count_pct"]))

            for i in range(tier_count):
                global_index += 1
                agent = generate_agent(domain, tier, i + 1, global_index)
                domain_agents.append(agent)
                tier_stats[tier["name"]] += 1

                if global_index >= 30000:
                    break

            if global_index >= 30000:
                break

        agents.extend(domain_agents)
        domain_stats[domain] = len(domain_agents)

        if global_index >= 30000:
            break

    registry = {
        "$schema": "./agent-schema.json",
        "version": "2.0.0",
        "organization": "BlackRoad-OS",
        "generated": datetime.now().isoformat(),
        "total_agents": len(agents),
        "statistics": {
            "by_domain": domain_stats,
            "by_tier": tier_stats,
            "domains_count": len(domain_stats),
            "average_per_domain": len(agents) / len(domain_stats) if domain_stats else 0
        },
        "tiers": {t["name"]: {"prefix": t["prefix"], "percentage": t["count_pct"]} for t in TIERS},
        "domains": {k: {"prefix": v["prefix"], "risk": v["risk"]} for k, v in DOMAINS.items()},
        "agents": agents
    }

    return registry

def main():
    registry = generate_all_agents()
    print(json.dumps(registry, indent=2))

if __name__ == "__main__":
    main()
