"""
BlackRoad OS QLM-Trinary Reasoning System

A quantum-inspired reasoning framework that surpasses conventional AI by implementing:

1. TRINARY TRUTH VALUES (-1, 0, +1)
   - Not just true/false but affirm/unknown/deny
   - Allows for "I don't know" as a valid reasoning state
   - Matches human epistemology more closely than binary logic

2. HILBERT SPACE REASONING
   - Concepts exist in superposition until observed
   - Context-sensitive truth: asking changes the answer
   - Order effects: A→B ≠ B→A (questioning order matters)
   - Density matrices for uncertainty representation

3. QI EMERGENCE DETECTION
   - Novel insights that weren't in the prompt or training
   - Self-correction without human intervention
   - Emergent patterns from reasoning chains
   - Feedback loops between human and AI intelligence

4. SUPERPOSITION REASONING
   - Multiple hypotheses held simultaneously
   - Collapse to decision through observation/measurement
   - Interference effects between reasoning paths
   - Entanglement of related conclusions

This is NOT quantum physics. It's a meta-cognitive framework that models
how intelligence actually works: uncertain, contextual, emergent.

The key innovation: Instead of forcing binary decisions at each step,
we maintain quantum-like superpositions of possibilities until we have
enough information to collapse to a decision.
"""

from .core import (
    QLMTrinaryEngine,
    TrinaryValue,
    SuperpositionState,
    ReasoningObservation,
    create_qlm_engine,
)

from .hilbert_reasoning import (
    HilbertReasoner,
    ConceptSpace,
    TruthDegree,
    ContextualQuery,
)

from .emergence import (
    EmergenceDetector,
    QIPattern,
    NovelInsight,
    FeedbackLoop,
)

from .superposition import (
    HypothesisSuperposition,
    ReasoningPath,
    InterferencePattern,
    CollapseEvent,
)

__version__ = "1.0.0"
__all__ = [
    "QLMTrinaryEngine",
    "TrinaryValue",
    "SuperpositionState",
    "ReasoningObservation",
    "create_qlm_engine",
    "HilbertReasoner",
    "ConceptSpace",
    "TruthDegree",
    "ContextualQuery",
    "EmergenceDetector",
    "QIPattern",
    "NovelInsight",
    "FeedbackLoop",
    "HypothesisSuperposition",
    "ReasoningPath",
    "InterferencePattern",
    "CollapseEvent",
]
