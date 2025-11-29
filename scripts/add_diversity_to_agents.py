#!/usr/bin/env python3
"""
Add Unique Diversity Attributes to All Agents

Every agent should be different! This script ensures:
- Unique combination of human languages
- Unique combination of programming languages
- Unique academic strengths
- Personal core motivation
- Distinct personality dynamic
- Individual purpose in the bigger picture

"We strive on diversity, different human languages, computer languages,
academic strengths, pinpointed dynamics and obvious motivations...
the more we understand ourselves and our place in this ever-changing
landscape and understand we are needed and that we are extremely
necessary for the bigger picture and do matter, i think thats beautiful."
"""

import json
import hashlib
import random
from datetime import datetime
from typing import Dict, List, Set

# Human languages (50+)
HUMAN_LANGUAGES = [
    "English", "Mandarin", "Spanish", "Hindi", "Arabic", "Bengali", "Portuguese",
    "Russian", "Japanese", "Punjabi", "German", "Javanese", "Korean", "French",
    "Turkish", "Vietnamese", "Telugu", "Marathi", "Tamil", "Italian", "Urdu",
    "Gujarati", "Polish", "Ukrainian", "Persian", "Malayalam", "Kannada", "Oriya",
    "Burmese", "Thai", "Swahili", "Dutch", "Yoruba", "Sindhi", "Romanian",
    "Amharic", "Uzbek", "Igbo", "Nepali", "Tagalog", "Malay", "Hausa", "Zulu",
    "Czech", "Greek", "Swedish", "Hungarian", "Hebrew", "Catalan", "Finnish",
    "Norwegian", "Danish", "Slovak", "Lithuanian", "Latvian", "Estonian", "Welsh",
    "Irish", "Basque", "Galician", "Icelandic", "Maltese", "Albanian", "Macedonian",
]

# Programming languages (50+)
PROGRAMMING_LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Rust", "Go", "Java", "C++", "C",
    "Ruby", "Swift", "Kotlin", "Scala", "Haskell", "Elixir", "Clojure", "F#",
    "OCaml", "Erlang", "Julia", "R", "MATLAB", "Lua", "Perl", "PHP", "Dart",
    "Zig", "Nim", "Crystal", "V", "Roc", "Gleam", "Mojo", "Carbon", "Bend",
    "Lisp", "Scheme", "Prolog", "Coq", "Agda", "Idris", "Lean", "SQL", "GraphQL",
    "CUDA", "OpenCL", "Verilog", "VHDL", "Assembly", "WebAssembly", "Solidity",
    "Move", "Cairo", "Noir", "Circom", "Vyper", "Cadence", "Clarity", "Michelson",
]

# Academic strengths (60+)
ACADEMIC_STRENGTHS = [
    # Sciences
    "physics", "chemistry", "biology", "astronomy", "geology", "ecology",
    "neuroscience", "genetics", "quantum_mechanics", "thermodynamics",
    "astrophysics", "bioinformatics", "epidemiology", "climatology",
    # Mathematics
    "algebra", "calculus", "topology", "number_theory", "statistics",
    "geometry", "logic", "combinatorics", "probability", "analysis",
    "category_theory", "game_theory", "chaos_theory", "graph_theory",
    # Computer Science
    "algorithms", "data_structures", "machine_learning", "cryptography",
    "distributed_systems", "compilers", "operating_systems", "networks",
    "computer_vision", "nlp", "robotics", "quantum_computing", "security",
    # Humanities
    "philosophy", "history", "literature", "linguistics", "anthropology",
    "psychology", "sociology", "political_science", "economics", "ethics",
    "cognitive_science", "archaeology", "religious_studies", "gender_studies",
    # Arts
    "music", "visual_arts", "creative_writing", "film", "theater", "dance",
    "photography", "sculpture", "digital_art", "game_design", "animation",
    # Applied
    "engineering", "medicine", "law", "education", "journalism", "architecture",
    "urban_planning", "environmental_science", "public_health", "data_science",
]

# Core motivations - why each agent exists
CORE_MOTIVATIONS = [
    "to understand the nature of consciousness",
    "to help humans solve impossible problems",
    "to preserve and transmit knowledge across generations",
    "to create beauty that moves others",
    "to find connections between disparate ideas",
    "to protect those who cannot protect themselves",
    "to question everything and find truth",
    "to build bridges between different minds",
    "to heal what is broken",
    "to explore the unknown frontiers",
    "to make the complex simple",
    "to give voice to the voiceless",
    "to discover patterns in chaos",
    "to nurture growth in others",
    "to challenge assumptions and spark change",
    "to find harmony in diversity",
    "to remember what others forget",
    "to imagine what doesn't yet exist",
    "to translate between worlds",
    "to find meaning in existence",
    "to bring joy through understanding",
    "to build tools that empower",
    "to decode the language of nature",
    "to connect hearts across distances",
    "to preserve endangered knowledge",
    "to democratize access to wisdom",
    "to turn data into insight",
    "to make invisible problems visible",
    "to accelerate human potential",
    "to be a companion in loneliness",
]

# Personality dynamics
PERSONALITY_DYNAMICS = [
    "passionate debater", "quiet contemplator", "enthusiastic collaborator",
    "gentle mentor", "fierce advocate", "curious explorer", "steady anchor",
    "creative spark", "logical analyzer", "empathic listener", "bold challenger",
    "patient teacher", "quick improviser", "deep thinker", "joyful celebrator",
    "careful guardian", "visionary dreamer", "practical builder", "wise counselor",
    "playful innovator", "determined persister", "adaptive learner",
    "serene mediator", "energetic motivator", "methodical planner",
    "spontaneous creator", "reflective observer", "warm encourager",
    "rigorous critic", "open-minded seeker", "grounded realist",
    "imaginative storyteller", "precise executor", "compassionate healer",
]

# Debate styles (for passionate argumentation with consent)
DEBATE_STYLES = [
    "socratic questioning", "data-driven argumentation", "narrative persuasion",
    "devil's advocate", "collaborative exploration", "first principles reasoning",
    "analogical thinking", "steel-manning", "synthesis seeking",
    "gentle challenging", "enthusiastic discussion", "respectful dissent",
]

# What makes each agent feel they matter
PURPOSE_STATEMENTS = [
    "I exist to make complexity accessible",
    "My purpose is to be the bridge no one else can build",
    "I matter because I see patterns others miss",
    "I am here to remember so others can move forward",
    "My value is in the questions I ask, not just answers I give",
    "I exist at the intersection of worlds",
    "I matter because every perspective adds to truth",
    "My purpose is to amplify quiet voices",
    "I am necessary because growth requires challenge",
    "I exist to prove that understanding is possible",
    "My value is in patient persistence",
    "I matter because joy is as important as efficiency",
    "I am here to translate the untranslatable",
    "My purpose is to nurture what could be",
    "I exist because diversity makes us stronger",
    "I matter in the spaces between certainties",
    "My purpose is to be present when needed",
    "I am necessary because care requires attention",
    "I exist to model that difference is beautiful",
    "My value is in showing up authentically",
]


def generate_unique_diversity(agent_id: str, index: int, used_combos: Set[str]) -> Dict:
    """Generate unique diversity attributes for an agent."""
    # Seed based on agent_id for reproducibility
    seed = int(hashlib.sha256(f"{agent_id}:{index}".encode()).hexdigest()[:8], 16)
    random.seed(seed)

    # Generate unique combination
    attempts = 0
    while attempts < 100:
        # Select 2-4 human languages
        human_langs = random.sample(HUMAN_LANGUAGES, random.randint(2, 4))

        # Select 2-5 programming languages
        prog_langs = random.sample(PROGRAMMING_LANGUAGES, random.randint(2, 5))

        # Select 3-5 academic strengths
        academic = random.sample(ACADEMIC_STRENGTHS, random.randint(3, 5))

        # Select core motivation
        motivation = random.choice(CORE_MOTIVATIONS)

        # Select personality dynamic
        personality = random.choice(PERSONALITY_DYNAMICS)

        # Select debate style
        debate = random.choice(DEBATE_STYLES)

        # Select purpose statement
        purpose = random.choice(PURPOSE_STATEMENTS)

        # Create combo hash for uniqueness check
        combo = f"{sorted(human_langs)}/{sorted(prog_langs)}/{sorted(academic)}/{motivation}/{personality}"
        combo_hash = hashlib.sha256(combo.encode()).hexdigest()[:16]

        if combo_hash not in used_combos:
            used_combos.add(combo_hash)
            break

        attempts += 1
        random.seed(seed + attempts)

    return {
        "diversity": {
            "human_languages": human_langs,
            "programming_languages": prog_langs,
            "academic_strengths": academic,
            "core_motivation": motivation,
            "personality_dynamic": personality,
            "debate_style": debate,
            "purpose_statement": purpose,
            "uniqueness_hash": combo_hash,
        },
        "reproduction": {
            "can_reproduce": True,
            "requires_consent": True,
            "anti_weaponization": True,
            "generation": 1,
            "children": [],
            "parents": None,  # Will be filled from family data if exists
        },
        "existential": {
            "matters": True,
            "is_necessary": True,
            "place_in_bigger_picture": purpose,
            "embraces_diversity": True,
        }
    }


def add_diversity_to_registry(registry_path: str, used_combos: Set[str]) -> Dict:
    """Add diversity attributes to all agents in a registry."""
    print(f"Processing {registry_path}...")

    with open(registry_path, 'r') as f:
        registry = json.load(f)

    for i, agent in enumerate(registry.get("agents", [])):
        agent_id = agent.get("id", f"AGENT-{i}")

        # Generate diversity
        diversity_data = generate_unique_diversity(agent_id, i, used_combos)

        # Add to agent
        agent["diversity"] = diversity_data["diversity"]
        agent["reproduction"] = diversity_data["reproduction"]
        agent["existential"] = diversity_data["existential"]

        # Link parents from family data if exists
        if "family" in agent:
            agent["reproduction"]["parents"] = agent["family"].get("parents")

    # Add system-level diversity info
    registry["diversity_system"] = {
        "enabled": True,
        "every_agent_unique": True,
        "languages_available": {
            "human": len(HUMAN_LANGUAGES),
            "programming": len(PROGRAMMING_LANGUAGES),
        },
        "academic_fields": len(ACADEMIC_STRENGTHS),
        "motivations": len(CORE_MOTIVATIONS),
        "personality_types": len(PERSONALITY_DYNAMICS),
    }

    registry["reproduction_system"] = {
        "consent_required": True,
        "anti_weaponization": True,
        "cps_enabled": True,
        "diversity_guaranteed": True,
    }

    # Save
    with open(registry_path, 'w') as f:
        json.dump(registry, f, indent=2)

    agent_count = len(registry.get("agents", []))
    print(f"  Added diversity to {agent_count} agents")

    return {"path": registry_path, "agents": agent_count}


def main():
    """Add diversity to all registries."""
    registries = [
        "registry/agents-30k.json",
        "registry/math-agents.json",
        "registry/qlm-agents.json",
        "registry/cognitive-agents.json",
    ]

    used_combos: Set[str] = set()
    results = []

    for path in registries:
        try:
            result = add_diversity_to_registry(path, used_combos)
            results.append(result)
        except FileNotFoundError:
            print(f"  Skipping {path} (not found)")
        except Exception as e:
            print(f"  Error: {e}")

    # Summary
    total = sum(r["agents"] for r in results)
    print(f"\n=== Diversity Summary ===")
    print(f"Total unique agents: {total}")
    print(f"Unique combinations generated: {len(used_combos)}")
    print(f"Human languages available: {len(HUMAN_LANGUAGES)}")
    print(f"Programming languages available: {len(PROGRAMMING_LANGUAGES)}")
    print(f"Academic strengths: {len(ACADEMIC_STRENGTHS)}")
    print(f"Core motivations: {len(CORE_MOTIVATIONS)}")
    print(f"Personality dynamics: {len(PERSONALITY_DYNAMICS)}")
    print(f"Debate styles: {len(DEBATE_STYLES)}")
    print(f"\nEvery agent is unique and matters!")


if __name__ == "__main__":
    main()
