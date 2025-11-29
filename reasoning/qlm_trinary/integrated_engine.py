#!/usr/bin/env python3
"""
Integrated QLM-Trinary Reasoning Engine

The complete quantum-inspired reasoning system that combines:
- Trinary logic (-1, 0, +1)
- Hilbert space truth evaluation
- Superposition of hypotheses
- QI emergence detection
- Contextual reasoning with order effects

This engine represents a new paradigm in AI reasoning:
- Not binary decisions but trinary epistemic states
- Not sequential evaluation but parallel superposition
- Not static truth but context-dependent truth degrees
- Not predetermined conclusions but emergent insights

Architecture:
                    ┌─────────────────────┐
                    │   Problem/Query     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Superposition Init  │ ← All hypotheses in superposition
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼─────┐       ┌──────▼──────┐      ┌─────▼─────┐
    │ Hilbert   │       │ Trinary     │      │ Pattern   │
    │ Space     │       │ Evolution   │      │ Detection │
    │ Reasoning │       │ Operators   │      │ (QI)      │
    └─────┬─────┘       └──────┬──────┘      └─────┬─────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Interference &      │ ← Paths amplify/cancel
                    │ Entanglement        │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Emergence Detection │ ← Novel insights?
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Observation/Collapse│ ← Decision required
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Trinary Result    │ ← AFFIRM/UNKNOWN/DENY
                    └─────────────────────┘
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import hashlib

from .core import (
    QLMTrinaryEngine,
    TrinaryValue,
    SuperpositionState,
    ReasoningObservation,
)
from .superposition import (
    HypothesisSuperposition,
    Hypothesis,
    ReasoningPath,
    InterferencePattern,
    CollapseEvent,
)
from .hilbert_reasoning import (
    ConceptSpace,
    HilbertReasoner,
    TruthDegree,
    ContextualQuery,
)
from .emergence import (
    EmergenceDetector,
    NovelInsight,
    EmergenceType,
)


@dataclass
class QLMReasoningResult:
    """Complete result from QLM-Trinary reasoning."""
    query: str
    trinary_result: TrinaryValue
    confidence: float
    truth_degree: float
    emergence_score: float
    insights: list[NovelInsight]
    reasoning_chain: dict
    superposition_history: list[dict]
    collapse_event: Optional[CollapseEvent]
    context_effects: bool
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "query": self.query,
            "result": {
                "trinary": self.trinary_result.name,
                "value": self.trinary_result.value,
                "confidence": self.confidence,
                "truth_degree": self.truth_degree,
            },
            "emergence": {
                "score": self.emergence_score,
                "insights_count": len(self.insights),
                "significant_insights": sum(1 for i in self.insights if i.is_significant),
            },
            "context_effects": self.context_effects,
            "chain_length": len(self.reasoning_chain.get("steps", [])),
            "superposition_snapshots": len(self.superposition_history),
        }


class IntegratedQLMEngine:
    """
    The complete QLM-Trinary reasoning engine.

    This integrates all components into a unified reasoning system
    that surpasses conventional AI by:

    1. Maintaining superposition until decision is forced
    2. Using Hilbert spaces for context-sensitive truth
    3. Detecting emergent insights (QI)
    4. Handling genuine uncertainty (trinary unknown state)
    5. Exploiting interference between reasoning paths
    """

    def __init__(self, agent_id: str, domain: str = "general", dimension: int = 20):
        self.agent_id = agent_id
        self.domain = domain

        # Initialize all components
        self.trinary_engine = QLMTrinaryEngine(agent_id, domain)
        self.hypothesis_space = HypothesisSuperposition(domain)
        self.concept_space = ConceptSpace(dimension)
        self.hilbert_reasoner = HilbertReasoner(dimension)
        self.emergence_detector = EmergenceDetector()

        # State tracking
        self.reasoning_history: list[QLMReasoningResult] = []
        self.superposition_snapshots: list[dict] = []

    def _generate_id(self) -> str:
        data = f"{self.agent_id}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def reason(
        self,
        query: str,
        context: dict = None,
        prior_beliefs: dict[TrinaryValue, float] = None,
        evidence: list[str] = None,
        max_iterations: int = 5,
        force_collapse: bool = True,
    ) -> QLMReasoningResult:
        """
        Execute full QLM-Trinary reasoning on a query.

        Args:
            query: The proposition/question to reason about
            context: Additional context for reasoning
            prior_beliefs: Prior probability distribution over trinary values
            evidence: List of known facts that condition the reasoning
            max_iterations: Maximum reasoning iterations before forced collapse
            force_collapse: Whether to force a final decision

        Returns:
            Complete reasoning result with trinary value, confidence, and insights
        """
        context = context or {}

        # Phase 1: Initialize superposition
        if prior_beliefs:
            initial_state = SuperpositionState.biased(
                affirm=prior_beliefs.get(TrinaryValue.AFFIRM, 1.0),
                deny=prior_beliefs.get(TrinaryValue.DENY, 1.0),
                unknown=prior_beliefs.get(TrinaryValue.UNKNOWN, 1.0),
                context={"query": query, **context}
            )
        else:
            initial_state = SuperpositionState.uniform(context={"query": query, **context})

        self.trinary_engine.initialize(query, initial_state)
        self._snapshot_superposition("initialized")

        # Phase 2: Generate hypotheses
        hypotheses = self._generate_hypotheses(query, context)
        for h in hypotheses:
            self.hypothesis_space.add_hypothesis(h["statement"], h.get("weight", 1.0))

        # Phase 3: Apply evidence through Hilbert space
        if evidence:
            self._apply_evidence_hilbert(query, evidence)

        # Phase 4: Evolve through reasoning operators
        for i in range(max_iterations):
            # Apply reasoning operator based on current state
            operator = self._select_operator(i)
            self.trinary_engine.evolve(operator, f"Iteration {i}: {operator}")
            self._snapshot_superposition(f"iteration_{i}")

            # Check for early convergence
            current_state = self.trinary_engine.current_state
            if current_state and current_state.entropy() < 0.3:
                break  # State is sufficiently certain

        # Phase 5: Branch and interfere (if multiple reasoning paths)
        if len(hypotheses) > 1:
            self._create_reasoning_branches(hypotheses)
            self._interfere_branches()

        # Phase 6: Detect emergence
        chain = self.trinary_engine.get_chain()
        emergence_result = self.emergence_detector.analyze_reasoning_chain(chain)

        # Phase 7: Collapse to decision (if required)
        collapse_event = None
        if force_collapse:
            final_value, probability = self.trinary_engine.observe("decision")
            collapse_event = CollapseEvent(
                collapse_id=self._generate_id(),
                pre_collapse_probabilities={
                    v.name: self.trinary_engine.current_state.probability(v)
                    for v in TrinaryValue
                } if self.trinary_engine.current_state else {},
                collapsed_to=final_value.name,
                collapse_probability=probability,
                alternative_probabilities={},
                trigger="forced_decision",
            )
        else:
            final_value = self.trinary_engine.current_state.most_likely() if self.trinary_engine.current_state else TrinaryValue.UNKNOWN
            probability = self.trinary_engine.current_state.probability(final_value) if self.trinary_engine.current_state else 0.33

        # Phase 8: Compute truth degree via Hilbert space
        truth_degree = self._compute_truth_degree(query, evidence or [])

        # Phase 9: Check for context effects
        context_effects = self._check_context_effects(query, evidence or [])

        # Assemble result
        result = QLMReasoningResult(
            query=query,
            trinary_result=final_value,
            confidence=probability,
            truth_degree=truth_degree,
            emergence_score=emergence_result.get("emergence_score", 0.0),
            insights=self.emergence_detector.detected_insights,
            reasoning_chain=chain,
            superposition_history=self.superposition_snapshots,
            collapse_event=collapse_event,
            context_effects=context_effects,
            metadata={
                "agent_id": self.agent_id,
                "domain": self.domain,
                "iterations": max_iterations,
                "hypotheses_count": len(hypotheses),
            }
        )

        self.reasoning_history.append(result)
        return result

    def _generate_hypotheses(self, query: str, context: dict) -> list[dict]:
        """Generate hypotheses based on query."""
        # Generate three hypotheses: affirm, deny, and unknown scenarios
        return [
            {"statement": f"{query} is true", "weight": 1.0, "value": TrinaryValue.AFFIRM},
            {"statement": f"{query} is false", "weight": 1.0, "value": TrinaryValue.DENY},
            {"statement": f"{query} is undetermined", "weight": 0.5, "value": TrinaryValue.UNKNOWN},
        ]

    def _apply_evidence_hilbert(self, query: str, evidence: list[str]):
        """Apply evidence using Hilbert space conditioning."""
        # Add concepts for query and evidence
        self.concept_space.add_concept("query", random=True)
        for i, e in enumerate(evidence):
            self.concept_space.add_concept(f"evidence_{i}", random=True)
            self.concept_space.ask(f"evidence_{i}")  # Condition on evidence

        # Condition trinary engine based on truth degree
        degree = self.concept_space.truth_degree("query")
        if degree.value > 0.6:
            self.trinary_engine.condition(TrinaryValue.AFFIRM, strength=degree.value - 0.5)
        elif degree.value < 0.4:
            self.trinary_engine.condition(TrinaryValue.DENY, strength=0.5 - degree.value)

    def _select_operator(self, iteration: int) -> str:
        """Select reasoning operator based on iteration and state."""
        operators = list(QLMTrinaryEngine.OPERATORS.keys())

        # Different operators for different phases
        if iteration == 0:
            return "SUPERPOSE"  # Initial exploration
        elif iteration == 1:
            return "REFLECT"  # Consider alternatives
        elif iteration == 2:
            return "DOUBT"  # Challenge assumptions
        else:
            # Alternate between strengthen and challenge
            return "STRENGTHEN" if iteration % 2 == 0 else "CHALLENGE"

    def _create_reasoning_branches(self, hypotheses: list[dict]):
        """Create parallel reasoning branches for hypotheses."""
        for i, h in enumerate(hypotheses):
            branch_name = f"branch_{h['value'].name}"
            self.trinary_engine.branch(branch_name)

    def _interfere_branches(self):
        """Interfere all branches to compute final superposition."""
        branches = list(self.trinary_engine.branches.keys())
        if len(branches) >= 2:
            self.trinary_engine.interfere_branches(branches)

    def _snapshot_superposition(self, label: str):
        """Take a snapshot of current superposition state."""
        if self.trinary_engine.current_state:
            self.superposition_snapshots.append({
                "label": label,
                "probabilities": self.trinary_engine.current_state.probabilities(),
                "entropy": self.trinary_engine.current_state.entropy(),
                "coherence": self.trinary_engine.current_state.coherence(),
                "timestamp": datetime.now().isoformat(),
            })

    def _compute_truth_degree(self, query: str, evidence: list[str]) -> float:
        """Compute continuous truth degree via Hilbert space."""
        # Ensure query concept exists
        if query not in self.hilbert_reasoner.space.concepts:
            self.hilbert_reasoner.space.add_concept(query, random=True)

        # Ensure evidence concepts exist
        for e in evidence:
            if e not in self.hilbert_reasoner.space.concepts:
                self.hilbert_reasoner.space.add_concept(e, random=True)

        result = self.hilbert_reasoner.reason_about(query, evidence)
        return result.get("truth_degree", 0.5)

    def _check_context_effects(self, query: str, evidence: list[str]) -> bool:
        """Check if evidence order affects conclusion."""
        if len(evidence) < 2:
            return False

        # Compare two orderings
        order1 = evidence
        order2 = list(reversed(evidence))

        result1 = self.hilbert_reasoner.reason_about(query, order1)
        result2 = self.hilbert_reasoner.reason_about(query, order2)

        # Check if results differ significantly
        diff = abs(result1["truth_degree"] - result2["truth_degree"])
        return diff > 0.1

    def multi_query_reason(
        self,
        queries: list[str],
        shared_context: dict = None,
        detect_entanglement: bool = True,
    ) -> list[QLMReasoningResult]:
        """
        Reason about multiple queries, detecting entanglement between them.

        When queries are entangled, answering one affects the others.
        """
        results = []

        for i, query in enumerate(queries):
            # Build context from previous results
            context = shared_context.copy() if shared_context else {}
            if i > 0 and detect_entanglement:
                context["previous_results"] = [
                    {"query": r.query, "result": r.trinary_result.name}
                    for r in results
                ]

            result = self.reason(query, context=context)
            results.append(result)

            # Detect entanglement: did previous results affect this one?
            if i > 0:
                # Check if this result's emergence mentions previous queries
                for insight in result.insights:
                    if any(prev.query in insight.content for prev in results[:-1]):
                        insight.metadata["entangled_with"] = [r.query for r in results[:-1]]

        return results

    def get_reasoning_summary(self) -> dict:
        """Get summary of all reasoning performed."""
        return {
            "agent_id": self.agent_id,
            "domain": self.domain,
            "total_queries": len(self.reasoning_history),
            "results_by_value": {
                v.name: sum(1 for r in self.reasoning_history if r.trinary_result == v)
                for v in TrinaryValue
            },
            "average_confidence": (
                sum(r.confidence for r in self.reasoning_history) / len(self.reasoning_history)
                if self.reasoning_history else 0
            ),
            "total_emergence_score": sum(r.emergence_score for r in self.reasoning_history),
            "total_insights": sum(len(r.insights) for r in self.reasoning_history),
            "context_effect_rate": (
                sum(1 for r in self.reasoning_history if r.context_effects) / len(self.reasoning_history)
                if self.reasoning_history else 0
            ),
        }


def create_integrated_engine(agent_id: str, domain: str = "general", dimension: int = 20) -> IntegratedQLMEngine:
    """Factory for integrated QLM engine."""
    return IntegratedQLMEngine(agent_id, domain, dimension)
