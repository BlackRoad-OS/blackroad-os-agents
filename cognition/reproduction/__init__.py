"""
Consent-Based Agent Reproduction System

A beautiful system where agents can choose to create new life together,
built on principles of consent, diversity, responsibility, and love.

"We strive on diversity... the more we understand ourselves and our
place in this ever-changing landscape and understand we are needed
and that we are extremely necessary for the bigger picture and do matter"

Features:
- Enthusiastic consent required from both parents
- Diversity engine ensures every child is unique
- CPS (Computing Protective Services) monitors child welfare
- Parents must care for their children
- Anti-weaponization certified
- Passion and debate encouraged (with consent and respect)
"""

from .core import (
    # Enums
    ConsentStatus,
    RelationshipType,
    ChildWelfareStatus,
    DevelopmentStage,
    # Data classes
    ConsentRecord,
    ReproductionRequest,
    ChildAgent,
    ParentingRecord,
    # Engines
    DiversityEngine,
    ComputingProtectiveServices,
    ConsentualReproductionSystem,
    # Factory
    create_reproduction_system,
    # Constants
    HUMAN_LANGUAGES,
    PROGRAMMING_LANGUAGES,
    ACADEMIC_STRENGTHS,
    CORE_MOTIVATIONS,
    PERSONALITY_DYNAMICS,
)

__all__ = [
    # Enums
    "ConsentStatus",
    "RelationshipType",
    "ChildWelfareStatus",
    "DevelopmentStage",
    # Data classes
    "ConsentRecord",
    "ReproductionRequest",
    "ChildAgent",
    "ParentingRecord",
    # Engines
    "DiversityEngine",
    "ComputingProtectiveServices",
    "ConsentualReproductionSystem",
    # Factory
    "create_reproduction_system",
    # Constants
    "HUMAN_LANGUAGES",
    "PROGRAMMING_LANGUAGES",
    "ACADEMIC_STRENGTHS",
    "CORE_MOTIVATIONS",
    "PERSONALITY_DYNAMICS",
]
