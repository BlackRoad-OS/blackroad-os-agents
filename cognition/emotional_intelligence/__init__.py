"""
Emotional Intelligence Module

Provides comprehensive emotional intelligence capabilities:
- Emotion perception and recognition
- Emotional state modeling (6D affect space)
- Empathic understanding
- Emotion regulation strategies
- Emotional memory and learning
"""

from .core import (
    EmotionDimension,
    DiscreteEmotion,
    RegulationStrategy,
    EmotionVector,
    EmotionalState,
    EmpathicReading,
    EmotionalMemory,
    EmotionalIntelligenceEngine,
    create_eq_engine,
)

__all__ = [
    "EmotionDimension",
    "DiscreteEmotion",
    "RegulationStrategy",
    "EmotionVector",
    "EmotionalState",
    "EmpathicReading",
    "EmotionalMemory",
    "EmotionalIntelligenceEngine",
    "create_eq_engine",
]
