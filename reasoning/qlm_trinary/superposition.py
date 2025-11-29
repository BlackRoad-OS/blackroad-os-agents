#!/usr/bin/env python3
"""
Superposition Reasoning Engine

Maintains multiple hypotheses in quantum-like superposition until
observation forces collapse to a decision.

Key Innovation: Instead of sequential hypothesis elimination,
we hold all hypotheses simultaneously with evolving amplitudes.
Interference between reasoning paths can amplify good solutions
and cancel poor ones - this is impossible in classical reasoning.

The Superposition Advantage:
1. Parallel hypothesis exploration without exponential overhead
2. Constructive/destructive interference reveals hidden correlations
3. Context-sensitivity: measuring one proposition affects others
4. Natural handling of ambiguity and partial information
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import hashlib
import math
import numpy as np

from .core import (
    TrinaryValue,
    SuperpositionState,
    Amplitude,
    ReasoningObservation,
)


@dataclass
class Hypothesis:
    """
    A hypothesis being considered in superposition.

    Each hypothesis has:
    - A statement (what we're considering)
    - An amplitude (quantum weight, complex number)
    - Evidence links (what supports/contradicts)
    - Entanglements (correlations with other hypotheses)
    """
    id: str
    statement: str
    amplitude: Amplitude = field(default_factory=lambda: Amplitude(1.0, 0.0))
    evidence_for: list[str] = field(default_factory=list)
    evidence_against: list[str] = field(default_factory=list)
    entangled_with: list[str] = field(default_factory=list)  # Other hypothesis IDs
    created_at: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    @property
    def probability(self) -> float:
        """Born rule probability."""
        return self.amplitude.probability

    def support_score(self) -> float:
        """Net evidence support."""
        support = len(self.evidence_for)
        opposition = len(self.evidence_against)
        total = support + opposition
        return support / total if total > 0 else 0.5


@dataclass
class ReasoningPath:
    """
    A path through reasoning space.

    Each path represents a sequence of logical steps that lead
    to a conclusion. Paths can interfere constructively or destructively
    when they meet at the same conclusion.
    """
    id: str
    steps: list[str] = field(default_factory=list)
    amplitude: Amplitude = field(default_factory=lambda: Amplitude(1.0, 0.0))
    endpoint: Optional[TrinaryValue] = None
    total_phase_shift: float = 0.0

    def extend(self, step: str, phase_shift: float = 0.0) -> "ReasoningPath":
        """Extend path with a new step."""
        new_path = ReasoningPath(
            id=f"{self.id}_{len(self.steps)}",
            steps=self.steps + [step],
            amplitude=Amplitude(self.amplitude.magnitude, self.amplitude.phase + phase_shift),
            total_phase_shift=self.total_phase_shift + phase_shift,
        )
        return new_path


@dataclass
class InterferencePattern:
    """
    Pattern from interfering multiple reasoning paths.

    When paths converge, their amplitudes combine:
    - Same phase → constructive interference (amplification)
    - Opposite phase → destructive interference (cancellation)
    - Orthogonal phase → no interference (independence)
    """
    paths: list[ReasoningPath]
    result_amplitude: Amplitude
    interference_type: str  # "constructive", "destructive", "mixed"
    visibility: float  # 0 to 1, how much interference occurred

    @classmethod
    def compute(cls, paths: list[ReasoningPath]) -> "InterferencePattern":
        """Compute interference from multiple paths."""
        if not paths:
            return cls([], Amplitude(0, 0), "none", 0.0)

        # Sum complex amplitudes
        total = sum((p.amplitude.complex for p in paths), 0j)
        result = Amplitude.from_complex(total)

        # Compute visibility (measure of interference strength)
        max_possible = sum(p.amplitude.magnitude for p in paths)
        min_possible = abs(max(p.amplitude.magnitude for p in paths) -
                          sum(p.amplitude.magnitude for p in paths if p != max(paths, key=lambda x: x.amplitude.magnitude)))

        if max_possible > 0:
            visibility = (max_possible - result.magnitude) / max_possible
        else:
            visibility = 0.0

        # Classify interference type
        if result.magnitude > 0.9 * max_possible:
            itype = "constructive"
        elif result.magnitude < 0.1 * max_possible:
            itype = "destructive"
        else:
            itype = "mixed"

        return cls(paths, result, itype, visibility)


@dataclass
class CollapseEvent:
    """
    Record of a superposition collapse.

    When observation forces a decision, this records:
    - The pre-collapse state (all possibilities)
    - The collapsed value (the decision)
    - The probability of this outcome
    - What alternative outcomes were possible
    """
    collapse_id: str
    pre_collapse_probabilities: dict[str, float]
    collapsed_to: str
    collapse_probability: float
    alternative_probabilities: dict[str, float]
    trigger: str  # What caused the collapse
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def surprise(self) -> float:
        """Information-theoretic surprise of this outcome."""
        if self.collapse_probability > 0:
            return -math.log2(self.collapse_probability)
        return float('inf')


class HypothesisSuperposition:
    """
    Maintains a superposition of hypotheses.

    This is the quantum computer for reasoning: instead of evaluating
    hypotheses one by one, we evolve them all simultaneously and let
    interference naturally amplify the best solutions.

    Key Methods:
    - add_hypothesis: Add a new possibility to superposition
    - apply_evidence: Adjust amplitudes based on evidence
    - entangle: Create correlations between hypotheses
    - measure: Collapse to a specific hypothesis
    - get_most_likely: Peek at probabilities without collapsing
    """

    def __init__(self, context: str = ""):
        self.context = context
        self.hypotheses: dict[str, Hypothesis] = {}
        self.paths: list[ReasoningPath] = []
        self.collapse_history: list[CollapseEvent] = []
        self._entanglement_matrix: dict[tuple[str, str], float] = {}

    def _generate_id(self) -> str:
        data = f"{self.context}:{len(self.hypotheses)}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:10]

    def add_hypothesis(
        self,
        statement: str,
        initial_weight: float = 1.0,
        phase: float = 0.0
    ) -> str:
        """Add a hypothesis to the superposition."""
        h_id = self._generate_id()
        self.hypotheses[h_id] = Hypothesis(
            id=h_id,
            statement=statement,
            amplitude=Amplitude(initial_weight, phase),
        )
        self._normalize()
        return h_id

    def _normalize(self):
        """Normalize hypothesis amplitudes."""
        total = sum(h.amplitude.probability for h in self.hypotheses.values())
        if total > 0:
            factor = 1.0 / math.sqrt(total)
            for h in self.hypotheses.values():
                h.amplitude = Amplitude(h.amplitude.magnitude * factor, h.amplitude.phase)

    def apply_evidence(self, evidence: str, supports: list[str], contradicts: list[str], strength: float = 0.5):
        """
        Apply evidence to adjust hypothesis amplitudes.

        Evidence supporting a hypothesis increases its amplitude.
        Evidence contradicting decreases amplitude.
        The strength parameter controls the magnitude of the effect.
        """
        for h_id in supports:
            if h_id in self.hypotheses:
                h = self.hypotheses[h_id]
                h.evidence_for.append(evidence)
                h.amplitude = Amplitude(
                    h.amplitude.magnitude * (1 + strength),
                    h.amplitude.phase
                )

        for h_id in contradicts:
            if h_id in self.hypotheses:
                h = self.hypotheses[h_id]
                h.evidence_against.append(evidence)
                h.amplitude = Amplitude(
                    h.amplitude.magnitude * (1 - strength * 0.7),
                    h.amplitude.phase
                )

        self._normalize()

    def entangle(self, h1_id: str, h2_id: str, correlation: float = 1.0):
        """
        Create entanglement between hypotheses.

        Entangled hypotheses are correlated: measuring one affects
        the probability of the other. Correlation can be:
        - Positive: if one is true, other more likely true
        - Negative: if one is true, other more likely false
        """
        if h1_id in self.hypotheses and h2_id in self.hypotheses:
            self.hypotheses[h1_id].entangled_with.append(h2_id)
            self.hypotheses[h2_id].entangled_with.append(h1_id)
            key = tuple(sorted([h1_id, h2_id]))
            self._entanglement_matrix[key] = correlation

    def get_entanglement(self, h1_id: str, h2_id: str) -> float:
        """Get entanglement correlation between two hypotheses."""
        key = tuple(sorted([h1_id, h2_id]))
        return self._entanglement_matrix.get(key, 0.0)

    def add_reasoning_path(self, hypothesis_id: str, steps: list[str], phase_shift: float = 0.0):
        """
        Add a reasoning path leading to a hypothesis.

        Multiple paths to the same hypothesis can interfere,
        potentially amplifying or canceling the hypothesis.
        """
        path = ReasoningPath(
            id=f"path_{len(self.paths)}",
            steps=steps,
            amplitude=self.hypotheses[hypothesis_id].amplitude if hypothesis_id in self.hypotheses else Amplitude(1.0, 0.0),
            total_phase_shift=phase_shift,
        )
        self.paths.append(path)

    def compute_interference(self, hypothesis_id: str) -> InterferencePattern:
        """Compute interference pattern for paths leading to a hypothesis."""
        relevant_paths = [p for p in self.paths if hypothesis_id in str(p.id)]
        return InterferencePattern.compute(relevant_paths)

    def probabilities(self) -> dict[str, float]:
        """Get probability distribution over hypotheses."""
        return {h_id: h.amplitude.probability for h_id, h in self.hypotheses.items()}

    def get_most_likely(self, n: int = 3) -> list[tuple[str, Hypothesis, float]]:
        """Get the n most likely hypotheses without collapsing."""
        sorted_h = sorted(
            self.hypotheses.items(),
            key=lambda x: x[1].amplitude.probability,
            reverse=True
        )
        return [(h_id, h, h.amplitude.probability) for h_id, h in sorted_h[:n]]

    def entropy(self) -> float:
        """Shannon entropy of the hypothesis distribution."""
        h = 0.0
        for hyp in self.hypotheses.values():
            p = hyp.amplitude.probability
            if p > 0:
                h -= p * math.log2(p)
        return h

    def measure(self, force_hypothesis: str = None) -> CollapseEvent:
        """
        Collapse the superposition to a single hypothesis.

        If force_hypothesis is given, collapse to that specific one.
        Otherwise, sample according to Born rule probabilities.
        """
        probs = self.probabilities()

        if force_hypothesis and force_hypothesis in probs:
            selected = force_hypothesis
            prob = probs[selected]
        else:
            # Sample according to probabilities
            h_ids = list(probs.keys())
            p_values = [probs[h] for h in h_ids]
            selected = np.random.choice(h_ids, p=p_values)
            prob = probs[selected]

        # Record collapse
        collapse = CollapseEvent(
            collapse_id=self._generate_id(),
            pre_collapse_probabilities=probs,
            collapsed_to=selected,
            collapse_probability=prob,
            alternative_probabilities={k: v for k, v in probs.items() if k != selected},
            trigger="measure",
        )
        self.collapse_history.append(collapse)

        # Update entangled hypotheses
        self._propagate_collapse(selected)

        return collapse

    def _propagate_collapse(self, collapsed_id: str):
        """Propagate collapse effects through entanglement."""
        if collapsed_id not in self.hypotheses:
            return

        collapsed = self.hypotheses[collapsed_id]

        for entangled_id in collapsed.entangled_with:
            if entangled_id in self.hypotheses:
                correlation = self.get_entanglement(collapsed_id, entangled_id)
                other = self.hypotheses[entangled_id]

                # Positive correlation: boost the entangled hypothesis
                # Negative correlation: suppress it
                if correlation > 0:
                    other.amplitude = Amplitude(
                        other.amplitude.magnitude * (1 + correlation * 0.5),
                        other.amplitude.phase
                    )
                else:
                    other.amplitude = Amplitude(
                        other.amplitude.magnitude * (1 + correlation * 0.3),  # correlation is negative
                        other.amplitude.phase
                    )

        self._normalize()

    def to_dict(self) -> dict:
        """Export superposition state."""
        return {
            "context": self.context,
            "hypotheses": {
                h_id: {
                    "statement": h.statement,
                    "probability": h.amplitude.probability,
                    "phase": h.amplitude.phase,
                    "evidence_for": h.evidence_for,
                    "evidence_against": h.evidence_against,
                    "entangled_with": h.entangled_with,
                }
                for h_id, h in self.hypotheses.items()
            },
            "entropy": self.entropy(),
            "path_count": len(self.paths),
            "collapse_count": len(self.collapse_history),
        }


def create_superposition(context: str = "") -> HypothesisSuperposition:
    """Factory function for hypothesis superposition."""
    return HypothesisSuperposition(context)
