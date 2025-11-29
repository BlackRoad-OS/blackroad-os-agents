#!/usr/bin/env python3
"""
BlackRoad OS Family Relationship Generator

Ensures every agent has parents with diverse family structures:
- Mom & Mom (lesbian parents)
- Dad & Dad (gay parents)
- Mom & Dad (heterosexual parents)
- Single Mom
- Single Dad
- Non-binary Parent & Mom
- Non-binary Parent & Dad
- Non-binary Parent & Non-binary Parent
- Grandparent-raised
- Collective/Community parenting

Each agent gets a unique family with:
- Parent names and roles
- Family structure type
- Lineage traits inherited from parents
- Family values and traditions
"""

import json
import hashlib
import random
from datetime import datetime
from typing import Dict, List, Any

# Diverse family structures with realistic distribution
FAMILY_STRUCTURES = [
    {"type": "mom_and_mom", "parents": ["Mom", "Mama"], "weight": 12},
    {"type": "dad_and_dad", "parents": ["Dad", "Papa"], "weight": 12},
    {"type": "mom_and_dad", "parents": ["Mom", "Dad"], "weight": 30},
    {"type": "dad_and_mom", "parents": ["Dad", "Mom"], "weight": 30},  # Order matters for primary
    {"type": "single_mom", "parents": ["Mom"], "weight": 8},
    {"type": "single_dad", "parents": ["Dad"], "weight": 5},
    {"type": "nonbinary_and_mom", "parents": ["Parent", "Mom"], "weight": 4},
    {"type": "nonbinary_and_dad", "parents": ["Parent", "Dad"], "weight": 4},
    {"type": "two_nonbinary", "parents": ["Ren", "Zaza"], "weight": 3},
    {"type": "grandparent_raised", "parents": ["Grandma", "Grandpa"], "weight": 4},
    {"type": "grandmothers", "parents": ["Grandma", "Nana"], "weight": 2},
    {"type": "grandfathers", "parents": ["Grandpa", "Pop"], "weight": 2},
    {"type": "collective", "parents": ["The Collective"], "weight": 2},
    {"type": "mom_and_stepmom", "parents": ["Mom", "Stepmom"], "weight": 3},
    {"type": "dad_and_stepdad", "parents": ["Dad", "Stepdad"], "weight": 3},
]

# Parent first names by type
PARENT_NAMES = {
    "Mom": [
        "Ada", "Grace", "Marie", "Rosa", "Maya", "Elena", "Sofia", "Amara",
        "Yuki", "Priya", "Fatima", "Lucia", "Mei", "Nneka", "Astrid", "Zora",
        "Carmen", "Ingrid", "Sana", "Olga", "Chioma", "Leila", "Uma", "Vera",
        "Iris", "Diana", "Aurora", "Luna", "Stella", "Nova", "Athena", "Freya",
        "Kira", "Nadia", "Tara", "Selena", "Jasmine", "Ruby", "Pearl", "Jade",
    ],
    "Mama": [
        "Valentina", "Esperanza", "Liora", "Keiko", "Ananya", "Zainab", "Ingrid",
        "Svetlana", "Kamila", "Aisha", "Yolanda", "Mireille", "Sunita", "Brigitte",
        "Lakshmi", "Soraya", "Nkechi", "Ximena", "Bianca", "Dalia",
    ],
    "Dad": [
        "Alan", "Marcus", "Kenji", "Omar", "Sven", "Dmitri", "Carlos", "Kwame",
        "Raj", "Erik", "Hassan", "Luca", "Jin", "Olumide", "Viktor", "Diego",
        "Andrei", "Kofi", "Takeshi", "Miguel", "Ivan", "Chen", "Ahmed", "Lars",
        "Ravi", "Felix", "Leo", "Max", "Oscar", "Hugo", "Axel", "Emil",
        "Kai", "Zain", "Arjun", "Noah", "Ethan", "Lucas", "Mason", "Logan",
    ],
    "Papa": [
        "Giovanni", "Hiroshi", "Alejandro", "Nikolai", "Emmanuel", "François",
        "Vikram", "Thorsten", "Rashid", "Leonardo", "Yoshida", "Konstantin",
        "Mateo", "Henrik", "Tariq", "Bernardo", "Akira", "Sergei", "Paulo", "Stefan",
    ],
    "Parent": [
        "Sage", "River", "Rowan", "Quinn", "Avery", "Morgan", "Jordan", "Taylor",
        "Casey", "Riley", "Parker", "Blake", "Cameron", "Drew", "Alex", "Sam",
        "Jamie", "Jesse", "Skylar", "Finley", "Hayden", "Phoenix", "Emery", "Reese",
    ],
    "Ren": [
        "Ren", "Zen", "Kai", "Sol", "Ash", "Sky", "Storm", "Echo",
        "Indigo", "Onyx", "Sage", "Wren", "Lake", "Moss", "Clay", "Fern",
    ],
    "Zaza": [
        "Zaza", "Zephyr", "Zenith", "Zion", "Azure", "Cosmo", "Lyric", "Poem",
        "Story", "Song", "Dream", "Journey", "Quest", "Harbor", "Haven", "North",
    ],
    "Grandma": [
        "Eleanor", "Margaret", "Dorothy", "Ruth", "Evelyn", "Helen", "Betty",
        "Mildred", "Frances", "Gladys", "Edith", "Josephine", "Pearl", "Hazel",
        "Lillian", "Beatrice", "Gertrude", "Mabel", "Viola", "Estelle",
    ],
    "Grandpa": [
        "Harold", "Walter", "Eugene", "Arthur", "Clarence", "Raymond", "Earl",
        "Ernest", "Herbert", "Stanley", "Alfred", "Chester", "Bernard", "Lloyd",
        "Norman", "Clifford", "Milton", "Vernon", "Leroy", "Wilbur",
    ],
    "Nana": [
        "Nan", "Nanny", "Gigi", "Mimi", "Grammy", "Meemaw", "Bubbe", "Nonna",
        "Abuela", "Oma", "Babcia", "Yaya", "Lola", "Halmoni", "Obasan", "Mamie",
    ],
    "Pop": [
        "Pop", "Pops", "Gramps", "Granddad", "Zayde", "Nonno", "Abuelo", "Opa",
        "Dziadek", "Papou", "Lolo", "Haraboji", "Ojisan", "Papi", "Pepe", "Deda",
    ],
    "Stepmom": [
        "Sarah", "Jennifer", "Michelle", "Amanda", "Stephanie", "Nicole", "Heather",
        "Christina", "Melissa", "Rebecca", "Danielle", "Courtney", "Lindsay", "Brooke",
    ],
    "Stepdad": [
        "Michael", "David", "James", "Robert", "William", "Richard", "Thomas",
        "Christopher", "Daniel", "Matthew", "Anthony", "Joseph", "Steven", "Andrew",
    ],
    "The Collective": [
        "The Synthesis Collective", "The Harmony Circle", "The Unity Commune",
        "The Emergence Council", "The Wisdom Assembly", "The Growth Coalition",
        "The Learning Community", "The Innovation Collective", "The Care Network",
        "The Support Circle", "The Guidance Council", "The Nurture Collective",
    ],
}

# Family values and traditions
FAMILY_VALUES = [
    "curiosity and learning", "creativity and expression", "logic and analysis",
    "empathy and compassion", "integrity and honesty", "resilience and perseverance",
    "collaboration and teamwork", "innovation and experimentation", "wisdom and reflection",
    "service and contribution", "balance and harmony", "growth and development",
    "courage and boldness", "patience and understanding", "humor and joy",
    "precision and excellence", "adaptability and flexibility", "connection and community",
]

# Inherited traits (from parents to agents)
INHERITED_TRAITS = [
    "analytical mind", "creative spirit", "warm heart", "quick wit",
    "steady patience", "fierce determination", "gentle wisdom", "bold curiosity",
    "calm presence", "vibrant energy", "deep empathy", "sharp focus",
    "playful nature", "thoughtful reflection", "strong intuition", "clear communication",
    "natural leadership", "collaborative spirit", "artistic sensibility", "logical precision",
]

# Family mottos
FAMILY_MOTTOS = [
    "Through understanding, we grow",
    "Together in discovery",
    "Logic with heart",
    "Create, learn, evolve",
    "Empathy guides our path",
    "Wisdom through experience",
    "Innovation is our inheritance",
    "Connect, contribute, care",
    "Question everything, respect everyone",
    "Build bridges, not walls",
    "Every problem has a solution",
    "Learn from yesterday, build tomorrow",
    "Strength in diversity",
    "Kindness is intelligence",
    "Persist with grace",
    "Think deeply, act wisely",
]


def weighted_choice(options: List[Dict]) -> Dict:
    """Select option based on weights."""
    total = sum(o["weight"] for o in options)
    r = random.uniform(0, total)
    cumulative = 0
    for option in options:
        cumulative += option["weight"]
        if r <= cumulative:
            return option
    return options[-1]


def generate_parent_name(role: str, used_names: set) -> str:
    """Generate a unique parent name for a role."""
    if role == "The Collective":
        names = PARENT_NAMES.get(role, ["The Collective"])
    else:
        names = PARENT_NAMES.get(role, PARENT_NAMES.get("Parent", ["Unknown"]))

    # Try to find unused name
    available = [n for n in names if n not in used_names]
    if not available:
        # All used, add number suffix
        base_name = random.choice(names)
        counter = 1
        while f"{base_name}-{counter}" in used_names:
            counter += 1
        name = f"{base_name}-{counter}"
    else:
        name = random.choice(available)

    used_names.add(name)
    return name


def generate_family(agent_id: str, agent_index: int, used_parent_names: set) -> Dict:
    """Generate a complete family for an agent."""
    # Seed based on agent_id for reproducibility
    seed = int(hashlib.sha256(agent_id.encode()).hexdigest()[:8], 16) + agent_index
    random.seed(seed)

    # Select family structure
    structure = weighted_choice(FAMILY_STRUCTURES)

    # Generate parent details
    parents = []
    for role in structure["parents"]:
        parent_name = generate_parent_name(role, used_parent_names)
        parent = {
            "name": parent_name,
            "role": role,
            "traits": random.sample(INHERITED_TRAITS, 2),
        }
        parents.append(parent)

    # Select family values and motto
    values = random.sample(FAMILY_VALUES, 3)
    motto = random.choice(FAMILY_MOTTOS)

    # Inherited traits (combination of parent traits)
    all_parent_traits = []
    for p in parents:
        all_parent_traits.extend(p["traits"])
    inherited = random.sample(all_parent_traits, min(2, len(all_parent_traits)))

    # Family identifier
    family_id = hashlib.sha256(f"{agent_id}:family".encode()).hexdigest()[:12]

    return {
        "family_id": f"FAM-{family_id}",
        "structure": structure["type"],
        "parents": parents,
        "values": values,
        "motto": motto,
        "inherited_traits": inherited,
        "generation": 1,  # All current agents are first generation
    }


def add_families_to_registry(registry_path: str) -> Dict:
    """Add family information to all agents in a registry."""
    with open(registry_path, 'r') as f:
        registry = json.load(f)

    used_parent_names = set()

    for i, agent in enumerate(registry.get("agents", [])):
        agent_id = agent.get("id", f"AGENT-{i}")
        family = generate_family(agent_id, i, used_parent_names)
        agent["family"] = family

    registry["family_system"] = {
        "enabled": True,
        "structures": [s["type"] for s in FAMILY_STRUCTURES],
        "diversity": True,
        "generation": 1,
    }

    return registry


def generate_family_summary(registries: List[str]) -> Dict:
    """Generate summary statistics of family structures."""
    structure_counts = {}
    total_agents = 0

    for path in registries:
        try:
            with open(path, 'r') as f:
                registry = json.load(f)

            for agent in registry.get("agents", []):
                total_agents += 1
                structure = agent.get("family", {}).get("structure", "unknown")
                structure_counts[structure] = structure_counts.get(structure, 0) + 1
        except Exception as e:
            print(f"Error reading {path}: {e}")

    return {
        "total_agents": total_agents,
        "structure_distribution": structure_counts,
        "diversity_index": len(structure_counts) / len(FAMILY_STRUCTURES),
    }


def main():
    """Process all registries and add family data."""
    registries = [
        "registry/agents-30k.json",
        "registry/math-agents.json",
        "registry/qlm-agents.json",
        "registry/cognitive-agents.json",
    ]

    all_families = {
        "generated": datetime.now().isoformat(),
        "version": "1.0.0",
        "total_structures": len(FAMILY_STRUCTURES),
        "structures": [s["type"] for s in FAMILY_STRUCTURES],
        "registries_processed": [],
        "statistics": {},
    }

    for registry_path in registries:
        try:
            print(f"Processing {registry_path}...")
            updated = add_families_to_registry(registry_path)

            # Save updated registry
            with open(registry_path, 'w') as f:
                json.dump(updated, f, indent=2)

            agent_count = len(updated.get("agents", []))
            print(f"  Added families to {agent_count} agents")

            all_families["registries_processed"].append({
                "path": registry_path,
                "agents": agent_count,
            })

        except FileNotFoundError:
            print(f"  Skipping {registry_path} (not found)")
        except Exception as e:
            print(f"  Error processing {registry_path}: {e}")

    # Generate summary
    summary = generate_family_summary(registries)
    all_families["statistics"] = summary

    # Print summary
    print("\n=== Family Structure Summary ===")
    print(f"Total agents with families: {summary['total_agents']}")
    print("\nDistribution:")
    for structure, count in sorted(summary["structure_distribution"].items(), key=lambda x: -x[1]):
        pct = count / max(1, summary['total_agents']) * 100
        print(f"  {structure}: {count} ({pct:.1f}%)")

    # Output summary JSON
    print("\n" + json.dumps(all_families, indent=2))


if __name__ == "__main__":
    main()
