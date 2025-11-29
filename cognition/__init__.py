"""
BlackRoad OS Cognition Module

A comprehensive cognitive architecture providing:

1. EMOTIONAL INTELLIGENCE
   - 6D emotion vectors (valence, arousal, dominance, certainty, anticipation, social)
   - Empathic resonance and understanding
   - Emotion regulation strategies
   - Emotional memory and learning

2. LANGUAGE INTELLIGENCE
   - 30+ language support
   - Pragmatic analysis (intent, context)
   - Discourse coherence
   - Register/style adaptation
   - Semantic frame extraction

3. MEMORY ARCHITECTURE
   - Working memory (limited capacity)
   - Episodic memory (events)
   - Semantic memory (facts)
   - Procedural memory (skills)
   - Prospective memory (intentions)
   - Associative retrieval

These systems integrate with the QLM-Trinary reasoning engine
to create agents that think, feel, communicate, and remember.
"""

from .emotional_intelligence import (
    EmotionVector,
    EmotionalState,
    EmpathicReading,
    EmotionalIntelligenceEngine,
    create_eq_engine,
)

from .language import (
    Language,
    CommunicativeIntent,
    Register,
    LinguisticFeatures,
    IntentAnalysis,
    LanguageIntelligenceEngine,
    create_language_engine,
)

from .memory import (
    MemoryType,
    MemoryTrace,
    EpisodicMemory,
    SemanticFact,
    ProceduralSkill,
    MemoryArchitecture,
    create_memory_system,
)

__all__ = [
    # Emotional Intelligence
    "EmotionVector",
    "EmotionalState",
    "EmpathicReading",
    "EmotionalIntelligenceEngine",
    "create_eq_engine",
    # Language
    "Language",
    "CommunicativeIntent",
    "Register",
    "LinguisticFeatures",
    "IntentAnalysis",
    "LanguageIntelligenceEngine",
    "create_language_engine",
    # Memory
    "MemoryType",
    "MemoryTrace",
    "EpisodicMemory",
    "SemanticFact",
    "ProceduralSkill",
    "MemoryArchitecture",
    "create_memory_system",
]
