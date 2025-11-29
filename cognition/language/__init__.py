"""
Language Intelligence Module

Provides comprehensive language processing capabilities:
- Multi-language detection and support (30+ languages)
- Pragmatic analysis (intent, context, implicature)
- Discourse structure and coherence
- Register and style adaptation
- Semantic frame extraction
"""

from .core import (
    Language,
    CommunicativeIntent,
    Register,
    DiscourseRelation,
    SemanticRole,
    LinguisticFeatures,
    IntentAnalysis,
    DiscourseUnit,
    SemanticFrame,
    LanguageProfile,
    LanguageIntelligenceEngine,
    create_language_engine,
)

__all__ = [
    "Language",
    "CommunicativeIntent",
    "Register",
    "DiscourseRelation",
    "SemanticRole",
    "LinguisticFeatures",
    "IntentAnalysis",
    "DiscourseUnit",
    "SemanticFrame",
    "LanguageProfile",
    "LanguageIntelligenceEngine",
    "create_language_engine",
]
