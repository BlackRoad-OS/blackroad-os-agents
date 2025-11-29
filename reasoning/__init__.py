"""
BlackRoad OS Reasoning Framework

A comprehensive reasoning system for 31,900+ AI agents implementing:
- Multi-phase cognitive pipelines (Alexa-Cece Framework)
- Tier-based complexity scaling
- Domain-specific reasoning profiles
- Persistent trace storage
- Chain validation and optimization

Usage:
    from reasoning import ReasoningEngine, create_engine

    # Create engine for an agent
    engine = create_engine("MATH-NT-PA-0001", tier="specialist", domain="mathematics")

    # Execute reasoning
    chain = engine.reason({"problem": "Prove the infinitude of primes"})

    # Validate result
    from reasoning.validators import validate_chain
    result = validate_chain(chain.to_dict())
"""

from .engines.base_reasoning import (
    BaseReasoningEngine,
    ReasoningChain,
    ReasoningStep,
    ReasoningPhase,
    ReasoningMode,
    ConfidenceLevel,
    create_engine,
    quick_reason,
)

from .engines.tier_reasoning import (
    TierReasoningEngine,
    AgentTier,
    TierConfig,
    TIER_CONFIGS,
    EscalationRequest,
    DelegationRequest,
    SwarmCoordinator,
    create_tier_engine,
    get_tier_config,
)

from .engines.chain_generator import (
    ChainGenerator,
    ChainTemplate,
    ChainOptimizer,
    CHAIN_TEMPLATES,
    create_generator,
)

__version__ = "1.0.0"
__all__ = [
    # Base reasoning
    "BaseReasoningEngine",
    "ReasoningChain",
    "ReasoningStep",
    "ReasoningPhase",
    "ReasoningMode",
    "ConfidenceLevel",
    "create_engine",
    "quick_reason",
    # Tier reasoning
    "TierReasoningEngine",
    "AgentTier",
    "TierConfig",
    "TIER_CONFIGS",
    "EscalationRequest",
    "DelegationRequest",
    "SwarmCoordinator",
    "create_tier_engine",
    "get_tier_config",
    # Chain generation
    "ChainGenerator",
    "ChainTemplate",
    "ChainOptimizer",
    "CHAIN_TEMPLATES",
    "create_generator",
]
