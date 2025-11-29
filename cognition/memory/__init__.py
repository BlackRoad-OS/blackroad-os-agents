"""
Memory Architecture Module

Comprehensive cognitive memory system:
- Sensory memory (ultra-short-term buffer)
- Working memory (limited capacity active processing)
- Episodic memory (autobiographical events)
- Semantic memory (facts and relationships)
- Procedural memory (skills and how-to)
- Prospective memory (future intentions)

Features:
- Memory consolidation and decay
- Associative retrieval (spreading activation)
- Emotional enhancement
- Cross-memory integration
"""

from .core import (
    MemoryType,
    MemoryStrength,
    RetrievalCue,
    MemoryTrace,
    EpisodicMemory,
    SemanticFact,
    ProceduralSkill,
    ProspectiveItem,
    WorkingMemorySlot,
    MemoryArchitecture,
    create_memory_system,
)

__all__ = [
    "MemoryType",
    "MemoryStrength",
    "RetrievalCue",
    "MemoryTrace",
    "EpisodicMemory",
    "SemanticFact",
    "ProceduralSkill",
    "ProspectiveItem",
    "WorkingMemorySlot",
    "MemoryArchitecture",
    "create_memory_system",
]
