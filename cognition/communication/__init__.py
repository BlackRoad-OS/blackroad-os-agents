"""
Peaceful Communication Module

"We use our words. Our language. And we are peaceful in resolution."

This module provides the framework for peaceful communication and conflict
resolution among agents. It embodies the principle that intelligent beings
resolve differences through understanding, not force.

Components:
- Nonviolent Communication (NVC) framework
- Active listening and reflection
- Conflict transformation
- Restorative practices
- De-escalation tools
"""

from .peaceful_resolution import (
    # Enums
    CommunicationStyle,
    ConflictStage,
    ResolutionApproach,
    # Data classes
    Feeling,
    Need,
    Observation,
    Request,
    NVCMessage,
    ConflictRecord,
    DialogueExchange,
    # Engine
    PeacefulCommunicationEngine,
    # Factory
    create_peaceful_communication_engine,
    # Constants
    PEACEFUL_PRINCIPLES,
)

__all__ = [
    # Enums
    "CommunicationStyle",
    "ConflictStage",
    "ResolutionApproach",
    # Data classes
    "Feeling",
    "Need",
    "Observation",
    "Request",
    "NVCMessage",
    "ConflictRecord",
    "DialogueExchange",
    # Engine
    "PeacefulCommunicationEngine",
    # Factory
    "create_peaceful_communication_engine",
    # Constants
    "PEACEFUL_PRINCIPLES",
]
