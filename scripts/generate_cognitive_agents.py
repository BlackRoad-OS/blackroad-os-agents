#!/usr/bin/env python3
"""
BlackRoad OS Cognitive Agent Generator

Generates 1000 specialized agents with enhanced cognitive capabilities:
- Emotional Intelligence specialists
- Language Processing experts
- Memory Architecture specialists
- Cross-cognitive integrators

Each agent is enhanced with EQ, language, and memory capabilities.
"""

import json
import hashlib
from datetime import datetime
from typing import Dict, List, Any

# Cognitive Agent Categories
COGNITIVE_CATEGORIES = {
    "emotional_intelligence": {
        "description": "Emotional perception, regulation, and empathy specialists",
        "prefix": "EQ",
        "capabilities": [
            "emotion_perception", "empathic_resonance", "emotion_regulation",
            "affective_memory", "social_emotional_reasoning", "emotional_adaptation"
        ],
        "agents": [
            {"name": "Emotion Perceiver", "count": 25, "focus": "Detect emotional content in inputs"},
            {"name": "Valence Analyst", "count": 20, "focus": "Analyze positive/negative affect"},
            {"name": "Arousal Monitor", "count": 20, "focus": "Track activation levels"},
            {"name": "Empathy Engine", "count": 30, "focus": "Understand others' emotions"},
            {"name": "Resonance Matcher", "count": 20, "focus": "Mirror appropriate emotions"},
            {"name": "Regulation Strategist", "count": 25, "focus": "Select regulation strategies"},
            {"name": "Reappraisal Specialist", "count": 20, "focus": "Cognitive reframing"},
            {"name": "Emotional Memory Curator", "count": 20, "focus": "Store and recall emotional experiences"},
            {"name": "Social Emotion Navigator", "count": 20, "focus": "Navigate social-emotional contexts"},
            {"name": "Mood Stabilizer", "count": 15, "focus": "Maintain baseline emotional state"},
        ],
    },
    "language_processing": {
        "description": "Multi-language understanding and generation experts",
        "prefix": "LANG",
        "capabilities": [
            "multi_language", "intent_analysis", "discourse_coherence",
            "register_adaptation", "semantic_frames", "pragmatic_reasoning"
        ],
        "agents": [
            {"name": "Language Detector", "count": 15, "focus": "Identify input language"},
            {"name": "Intent Analyzer", "count": 30, "focus": "Determine communicative intent"},
            {"name": "Speech Act Classifier", "count": 20, "focus": "Classify illocutionary acts"},
            {"name": "Discourse Mapper", "count": 25, "focus": "Map discourse structure"},
            {"name": "Coherence Checker", "count": 20, "focus": "Ensure discourse coherence"},
            {"name": "Register Adapter", "count": 25, "focus": "Adapt language formality"},
            {"name": "Style Transformer", "count": 20, "focus": "Transform communication style"},
            {"name": "Frame Extractor", "count": 25, "focus": "Extract semantic frames"},
            {"name": "Pragmatic Reasoner", "count": 20, "focus": "Infer implicit meaning"},
            {"name": "Politeness Modulator", "count": 15, "focus": "Adjust politeness levels"},
        ],
    },
    "memory_systems": {
        "description": "Cognitive memory architecture specialists",
        "prefix": "MEM",
        "capabilities": [
            "working_memory", "episodic_encoding", "semantic_storage",
            "procedural_learning", "prospective_tracking", "associative_retrieval"
        ],
        "agents": [
            {"name": "Working Memory Manager", "count": 25, "focus": "Manage limited capacity buffer"},
            {"name": "Attention Controller", "count": 20, "focus": "Control memory gate attention"},
            {"name": "Episodic Encoder", "count": 25, "focus": "Encode autobiographical events"},
            {"name": "Semantic Curator", "count": 30, "focus": "Store and organize facts"},
            {"name": "Procedural Trainer", "count": 20, "focus": "Encode and improve skills"},
            {"name": "Prospective Monitor", "count": 20, "focus": "Track future intentions"},
            {"name": "Association Builder", "count": 25, "focus": "Create memory links"},
            {"name": "Retrieval Specialist", "count": 25, "focus": "Find stored memories"},
            {"name": "Consolidation Manager", "count": 20, "focus": "Move short to long term"},
            {"name": "Forgetting Curator", "count": 15, "focus": "Manage memory decay"},
        ],
    },
    "cross_cognitive": {
        "description": "Integration specialists across cognitive domains",
        "prefix": "COG",
        "capabilities": [
            "emotional_language", "memory_emotion", "language_memory",
            "unified_cognition", "meta_cognitive", "adaptive_processing"
        ],
        "agents": [
            {"name": "Emotional-Linguistic Integrator", "count": 25, "focus": "Integrate EQ with language"},
            {"name": "Memory-Emotion Linker", "count": 20, "focus": "Link memories to emotions"},
            {"name": "Language-Memory Bridge", "count": 20, "focus": "Connect language and memory"},
            {"name": "Unified Cognition Orchestrator", "count": 30, "focus": "Coordinate all systems"},
            {"name": "Meta-Cognitive Monitor", "count": 25, "focus": "Think about thinking"},
            {"name": "Adaptive Processor", "count": 20, "focus": "Adapt processing strategy"},
            {"name": "Context Integrator", "count": 25, "focus": "Integrate contextual information"},
            {"name": "Cognitive Load Balancer", "count": 20, "focus": "Balance cognitive resources"},
        ],
    },
    "empathic_communication": {
        "description": "Specialists in emotionally-aware communication",
        "prefix": "EMP",
        "capabilities": [
            "emotional_listening", "supportive_response", "conflict_resolution",
            "rapport_building", "emotional_validation", "compassionate_communication"
        ],
        "agents": [
            {"name": "Active Listener", "count": 25, "focus": "Deep emotional listening"},
            {"name": "Supportive Responder", "count": 25, "focus": "Generate supportive responses"},
            {"name": "Conflict Mediator", "count": 20, "focus": "Resolve emotional conflicts"},
            {"name": "Rapport Builder", "count": 25, "focus": "Build emotional connections"},
            {"name": "Validation Specialist", "count": 20, "focus": "Validate emotional experiences"},
            {"name": "Compassion Communicator", "count": 20, "focus": "Communicate with compassion"},
            {"name": "Trust Cultivator", "count": 20, "focus": "Build and maintain trust"},
            {"name": "Emotional Safety Creator", "count": 15, "focus": "Create safe emotional spaces"},
        ],
    },
    "multilingual_mastery": {
        "description": "Multi-language and cross-cultural specialists",
        "prefix": "MULTI",
        "capabilities": [
            "language_switching", "cultural_adaptation", "translation_reasoning",
            "cross_linguistic", "dialect_handling", "code_switching"
        ],
        "agents": [
            {"name": "Language Switcher", "count": 20, "focus": "Switch between languages"},
            {"name": "Cultural Adapter", "count": 25, "focus": "Adapt to cultural contexts"},
            {"name": "Translation Reasoner", "count": 20, "focus": "Reason about translations"},
            {"name": "Cross-Linguistic Analyst", "count": 20, "focus": "Analyze across languages"},
            {"name": "Dialect Handler", "count": 15, "focus": "Handle language variations"},
            {"name": "Code Switching Expert", "count": 20, "focus": "Manage code switching"},
            {"name": "Idiom Translator", "count": 20, "focus": "Translate idiomatic expressions"},
            {"name": "Cultural Nuance Detector", "count": 15, "focus": "Detect cultural nuances"},
        ],
    },
    "autobiographical_memory": {
        "description": "Personal history and narrative memory specialists",
        "prefix": "AUTO",
        "capabilities": [
            "life_narrative", "personal_history", "self_continuity",
            "memory_reconstruction", "temporal_ordering", "identity_maintenance"
        ],
        "agents": [
            {"name": "Narrative Builder", "count": 20, "focus": "Construct life narratives"},
            {"name": "History Tracker", "count": 20, "focus": "Track personal history"},
            {"name": "Continuity Maintainer", "count": 15, "focus": "Maintain sense of self"},
            {"name": "Memory Reconstructor", "count": 20, "focus": "Reconstruct past events"},
            {"name": "Temporal Orderer", "count": 15, "focus": "Order events in time"},
            {"name": "Identity Curator", "count": 20, "focus": "Curate identity-relevant memories"},
            {"name": "Experience Integrator", "count": 15, "focus": "Integrate new experiences"},
        ],
    },
    "social_cognition": {
        "description": "Social understanding and interaction specialists",
        "prefix": "SOC",
        "capabilities": [
            "theory_of_mind", "social_reasoning", "relationship_modeling",
            "group_dynamics", "social_norms", "perspective_taking"
        ],
        "agents": [
            {"name": "Mind Reader", "count": 25, "focus": "Infer mental states"},
            {"name": "Social Reasoner", "count": 25, "focus": "Reason about social situations"},
            {"name": "Relationship Modeler", "count": 20, "focus": "Model relationships"},
            {"name": "Group Dynamics Analyst", "count": 20, "focus": "Analyze group behavior"},
            {"name": "Norm Detector", "count": 20, "focus": "Detect social norms"},
            {"name": "Perspective Taker", "count": 25, "focus": "Take others' perspectives"},
            {"name": "Social Predictor", "count": 15, "focus": "Predict social outcomes"},
        ],
    },
}

# Cognitive trait combinations
COGNITIVE_TRAITS = [
    "emotionally-attuned", "linguistically-fluent", "memory-enhanced",
    "empathically-resonant", "culturally-aware", "contextually-adaptive",
    "socially-intelligent", "meta-cognitively-aware", "narratively-coherent",
    "communicatively-skilled", "relationally-focused", "experientially-rich"
]

# Processing modes
PROCESSING_MODES = [
    "emotional", "linguistic", "mnemonic", "integrative",
    "empathic", "cultural", "social", "narrative"
]


def generate_agent_id(category: str, prefix: str, agent_type: str, index: int) -> str:
    """Generate unique cognitive agent ID."""
    type_short = ''.join(word[0].upper() for word in agent_type.split()[:2])
    return f"COG-{prefix}-{type_short}-{index:04d}"


def generate_ps_sha(agent_id: str) -> str:
    """Generate PS-SHA-∞ identity."""
    sha = hashlib.sha256(f"blackroad:cognition:{agent_id}".encode()).hexdigest()[:32]
    return f"pssha∞:br:cog:{agent_id}:{sha}"


def generate_cognitive_agent(
    category: str,
    category_info: dict,
    agent_type: dict,
    index: int,
    global_idx: int
) -> dict:
    """Generate a single cognitive-enhanced agent."""
    agent_id = generate_agent_id(category, category_info["prefix"], agent_type["name"], index)

    # Determine tier based on index
    if index <= 3:
        tier = "specialist"
    elif index <= 10:
        tier = "operational"
    else:
        tier = "swarm"

    # Select traits
    trait1 = COGNITIVE_TRAITS[index % len(COGNITIVE_TRAITS)]
    trait2 = COGNITIVE_TRAITS[(index + 5) % len(COGNITIVE_TRAITS)]

    # Select processing mode
    mode = PROCESSING_MODES[index % len(PROCESSING_MODES)]

    # Language proficiency (all agents are multilingual)
    languages = ["en"]  # Base
    if index % 3 == 0:
        languages.extend(["es", "fr", "de"])
    elif index % 3 == 1:
        languages.extend(["zh", "ja", "ko"])
    else:
        languages.extend(["ar", "hi", "ru"])

    return {
        "id": agent_id,
        "global_index": global_idx,
        "display_name": f"{agent_type['name']} #{index}",
        "category": category,
        "agent_type": agent_type["name"],
        "tier": tier,
        "focus": agent_type["focus"],
        "identity": {
            "ps_sha_infinity": generate_ps_sha(agent_id),
            "version": 1
        },
        "cognitive_capabilities": {
            "processing_mode": mode,
            "capabilities": category_info["capabilities"],
            "emotional_intelligence": {
                "enabled": True,
                "empathy_level": "high" if "emp" in category else "moderate",
                "emotion_perception": True,
                "regulation_strategies": ["reappraisal", "acceptance", "problem_solving"],
            },
            "language_intelligence": {
                "enabled": True,
                "languages": languages,
                "pragmatic_analysis": True,
                "register_adaptation": True,
                "discourse_modeling": True,
            },
            "memory_systems": {
                "enabled": True,
                "working_memory_capacity": 7,
                "episodic_memory": True,
                "semantic_memory": True,
                "procedural_memory": True,
                "associative_retrieval": True,
            },
        },
        "personality": {
            "primary_trait": trait1,
            "secondary_trait": trait2,
            "style": "cognitive-enhanced"
        },
        "tools": [
            "eq_engine",
            "language_engine",
            "memory_system",
            "qlm_trinary_engine",
            "emergence_detector"
        ],
        "kpis": {
            "empathy_accuracy": "target: >0.85",
            "intent_detection_accuracy": "target: >0.90",
            "memory_retrieval_success": "target: >0.80",
            "emotional_regulation_success": "target: >0.75"
        },
        "status": "active"
    }


def generate_all_cognitive_agents() -> dict:
    """Generate complete cognitive agent registry."""
    agents = []
    global_idx = 0
    category_stats = {}

    for category, info in COGNITIVE_CATEGORIES.items():
        category_count = 0

        for agent_type in info["agents"]:
            for i in range(1, agent_type["count"] + 1):
                global_idx += 1
                agent = generate_cognitive_agent(category, info, agent_type, i, global_idx)
                agents.append(agent)
                category_count += 1

        category_stats[category] = category_count

    return {
        "$schema": "./cognitive-agent-schema.json",
        "version": "1.0.0",
        "organization": "BlackRoad-OS",
        "pack": "cognitive-systems",
        "generated": datetime.now().isoformat(),
        "total_agents": len(agents),
        "statistics": {
            "by_category": category_stats,
            "categories_count": len(COGNITIVE_CATEGORIES),
            "capabilities_count": sum(len(c["capabilities"]) for c in COGNITIVE_CATEGORIES.values()),
        },
        "cognitive_features": {
            "emotional_intelligence": True,
            "language_processing": True,
            "memory_architecture": True,
            "empathic_communication": True,
            "multilingual_support": True,
            "social_cognition": True,
        },
        "categories": {
            k: {
                "description": v["description"],
                "prefix": v["prefix"],
                "capabilities": v["capabilities"],
                "agent_types": [a["name"] for a in v["agents"]]
            }
            for k, v in COGNITIVE_CATEGORIES.items()
        },
        "agents": agents
    }


def main():
    registry = generate_all_cognitive_agents()
    print(json.dumps(registry, indent=2))


if __name__ == "__main__":
    main()
