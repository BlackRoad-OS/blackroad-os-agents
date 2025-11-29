#!/usr/bin/env python3
"""
QLM-Trinary Core Reasoning Engine

The foundation of quantum-inspired reasoning with three-valued logic.

Key Concepts:
- TrinaryValue: -1 (deny), 0 (unknown), +1 (affirm)
- SuperpositionState: Multiple values held simultaneously with amplitudes
- ReasoningObservation: Collapse superposition to definite value

This replaces binary confidence scores with a richer epistemic model:
- Instead of "80% confident it's true"
- We have "amplitude 0.7 for affirm, 0.2 for unknown, 0.1 for deny"

The key insight: The "unknown" state is not ignorance—it's a valid
epistemic position that preserves uncertainty until resolution.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional
import hashlib
import math
import numpy as np


class TrinaryValue(Enum):
    """
    Three-valued logic: the foundation of QLM reasoning.

    DENY (-1): The proposition is false / rejected / negated
    UNKNOWN (0): We cannot determine truth value / suspended judgment
    AFFIRM (+1): The proposition is true / accepted / confirmed

    This mirrors:
    - Łukasiewicz three-valued logic
    - SQL's NULL semantics
    - Kleene's strong logic
    - Human epistemic states (yes/no/I don't know)
    """
    DENY = -1
    UNKNOWN = 0
    AFFIRM = 1

    @classmethod
    def from_confidence(cls, confidence: float) -> "TrinaryValue":
        """Convert binary confidence to trinary value."""
        if confidence >= 0.7:
            return cls.AFFIRM
        elif confidence <= 0.3:
            return cls.DENY
        else:
            return cls.UNKNOWN

    def to_confidence(self) -> float:
        """Convert trinary to rough confidence equivalent."""
        return {
            TrinaryValue.DENY: 0.1,
            TrinaryValue.UNKNOWN: 0.5,
            TrinaryValue.AFFIRM: 0.9,
        }[self]

    def __neg__(self) -> "TrinaryValue":
        """Negation: affirm ↔ deny, unknown stays unknown."""
        return TrinaryValue(-self.value) if self != TrinaryValue.UNKNOWN else self

    def __and__(self, other: "TrinaryValue") -> "TrinaryValue":
        """Trinary AND (Kleene strong): min of values."""
        return TrinaryValue(min(self.value, other.value))

    def __or__(self, other: "TrinaryValue") -> "TrinaryValue":
        """Trinary OR (Kleene strong): max of values."""
        return TrinaryValue(max(self.value, other.value))

    def __xor__(self, other: "TrinaryValue") -> "TrinaryValue":
        """Trinary XOR: different signs = affirm, same = deny, any unknown = unknown."""
        if self == TrinaryValue.UNKNOWN or other == TrinaryValue.UNKNOWN:
            return TrinaryValue.UNKNOWN
        return TrinaryValue.AFFIRM if self != other else TrinaryValue.DENY


@dataclass
class Amplitude:
    """
    Complex amplitude for a trinary value in superposition.

    Uses polar form (magnitude, phase) for intuitive manipulation.
    Phase represents "reasoning direction" - how we arrived at this value.
    """
    magnitude: float = 0.0
    phase: float = 0.0  # radians

    @property
    def complex(self) -> complex:
        """Convert to complex number."""
        return self.magnitude * (math.cos(self.phase) + 1j * math.sin(self.phase))

    @property
    def probability(self) -> float:
        """Born rule: |amplitude|² is probability."""
        return self.magnitude ** 2

    @classmethod
    def from_complex(cls, c: complex) -> "Amplitude":
        """Create from complex number."""
        return cls(magnitude=abs(c), phase=math.atan2(c.imag, c.real))

    def __mul__(self, other: "Amplitude") -> "Amplitude":
        """Multiply amplitudes (combine reasoning paths)."""
        return Amplitude(
            magnitude=self.magnitude * other.magnitude,
            phase=self.phase + other.phase
        )

    def __add__(self, other: "Amplitude") -> "Amplitude":
        """Add amplitudes (interference)."""
        c = self.complex + other.complex
        return Amplitude.from_complex(c)


@dataclass
class SuperpositionState:
    """
    A reasoning state in superposition across trinary values.

    Instead of committing to a single truth value, we maintain
    amplitudes for all three possibilities. This captures:
    - Uncertainty (not knowing which is correct)
    - Ambiguity (evidence for multiple values)
    - Context-dependence (value depends on how we observe)

    The state is normalized: sum of probabilities = 1
    """
    amplitudes: dict[TrinaryValue, Amplitude] = field(default_factory=dict)
    context: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        # Initialize missing amplitudes
        for v in TrinaryValue:
            if v not in self.amplitudes:
                self.amplitudes[v] = Amplitude(0.0, 0.0)
        self._normalize()

    def _normalize(self):
        """Normalize so probabilities sum to 1."""
        total = sum(a.probability for a in self.amplitudes.values())
        if total > 0:
            factor = 1.0 / math.sqrt(total)
            for v in self.amplitudes:
                self.amplitudes[v] = Amplitude(
                    self.amplitudes[v].magnitude * factor,
                    self.amplitudes[v].phase
                )

    @classmethod
    def pure(cls, value: TrinaryValue, context: dict = None) -> "SuperpositionState":
        """Create a pure state (100% one value)."""
        amps = {v: Amplitude(1.0 if v == value else 0.0, 0.0) for v in TrinaryValue}
        return cls(amplitudes=amps, context=context or {})

    @classmethod
    def uniform(cls, context: dict = None) -> "SuperpositionState":
        """Create maximally uncertain state (equal probability for all)."""
        mag = 1.0 / math.sqrt(3)
        amps = {v: Amplitude(mag, 0.0) for v in TrinaryValue}
        return cls(amplitudes=amps, context=context or {})

    @classmethod
    def biased(cls, affirm: float, deny: float, unknown: float, context: dict = None) -> "SuperpositionState":
        """Create state with specific probability weights."""
        total = affirm + deny + unknown
        amps = {
            TrinaryValue.AFFIRM: Amplitude(math.sqrt(affirm / total), 0.0),
            TrinaryValue.DENY: Amplitude(math.sqrt(deny / total), 0.0),
            TrinaryValue.UNKNOWN: Amplitude(math.sqrt(unknown / total), 0.0),
        }
        return cls(amplitudes=amps, context=context or {})

    def probability(self, value: TrinaryValue) -> float:
        """Get probability of a specific value."""
        return self.amplitudes[value].probability

    def probabilities(self) -> dict[TrinaryValue, float]:
        """Get all probabilities."""
        return {v: self.probability(v) for v in TrinaryValue}

    def most_likely(self) -> TrinaryValue:
        """Get most probable value (without collapsing)."""
        return max(TrinaryValue, key=lambda v: self.probability(v))

    def entropy(self) -> float:
        """Shannon entropy of the state (0 = certain, log(3) = maximally uncertain)."""
        h = 0.0
        for v in TrinaryValue:
            p = self.probability(v)
            if p > 0:
                h -= p * math.log2(p)
        return h

    def coherence(self) -> float:
        """
        Measure of quantum coherence (off-diagonal elements in density matrix).
        Higher coherence = more "quantum-like" behavior possible.
        """
        # Construct density matrix
        rho = np.zeros((3, 3), dtype=complex)
        amps = [self.amplitudes[v].complex for v in TrinaryValue]
        for i in range(3):
            for j in range(3):
                rho[i, j] = amps[i] * np.conj(amps[j])

        # Coherence = sum of off-diagonal magnitudes
        coherence = sum(abs(rho[i, j]) for i in range(3) for j in range(3) if i != j)
        return float(coherence)

    def interfere(self, other: "SuperpositionState", weight: float = 0.5) -> "SuperpositionState":
        """
        Interfere two superposition states.

        This is the quantum magic: combining reasoning paths can
        amplify or cancel probabilities depending on phase alignment.
        """
        new_amps = {}
        for v in TrinaryValue:
            a1 = self.amplitudes[v]
            a2 = other.amplitudes[v]
            # Weighted superposition with phase effects
            combined = Amplitude.from_complex(
                (1 - weight) * a1.complex + weight * a2.complex
            )
            new_amps[v] = combined

        merged_context = {**self.context, **other.context}
        return SuperpositionState(amplitudes=new_amps, context=merged_context)

    def apply_operator(self, operator: np.ndarray) -> "SuperpositionState":
        """Apply a 3x3 unitary operator to evolve the state."""
        vec = np.array([self.amplitudes[v].complex for v in TrinaryValue])
        new_vec = operator @ vec

        new_amps = {
            v: Amplitude.from_complex(new_vec[i])
            for i, v in enumerate(TrinaryValue)
        }
        return SuperpositionState(amplitudes=new_amps, context=self.context.copy())

    def to_dict(self) -> dict:
        return {
            "probabilities": {v.name: self.probability(v) for v in TrinaryValue},
            "phases": {v.name: self.amplitudes[v].phase for v in TrinaryValue},
            "entropy": self.entropy(),
            "coherence": self.coherence(),
            "context": self.context,
        }


@dataclass
class ReasoningObservation:
    """
    Observation/measurement that collapses superposition to definite value.

    In quantum mechanics, observation collapses the wave function.
    In QLM reasoning, making a decision collapses superposition of hypotheses.

    The observation records:
    - Which value was obtained
    - What the superposition was before collapse
    - The probability of this outcome
    - What triggered the observation
    """
    observed_value: TrinaryValue
    pre_observation_state: SuperpositionState
    observation_probability: float
    observation_type: str  # "decision", "evidence", "timeout", "forced"
    observer: str  # agent_id or "operator"
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict = field(default_factory=dict)

    @classmethod
    def collapse(
        cls,
        state: SuperpositionState,
        observation_type: str = "decision",
        observer: str = "system",
        force_value: TrinaryValue = None,
    ) -> tuple["ReasoningObservation", TrinaryValue]:
        """
        Collapse a superposition to a definite value.

        If force_value is given, collapse to that value (Lüders projection).
        Otherwise, sample according to Born rule probabilities.
        """
        if force_value is not None:
            value = force_value
            prob = state.probability(value)
        else:
            # Sample according to probabilities
            probs = [state.probability(v) for v in TrinaryValue]
            idx = np.random.choice(3, p=probs)
            value = list(TrinaryValue)[idx]
            prob = probs[idx]

        observation = cls(
            observed_value=value,
            pre_observation_state=state,
            observation_probability=prob,
            observation_type=observation_type,
            observer=observer,
        )

        return observation, value


@dataclass
class TrinaryReasoningStep:
    """A single step in a QLM-Trinary reasoning chain."""
    step_id: str
    phase: str
    input_state: SuperpositionState
    output_state: SuperpositionState
    operator_applied: Optional[str] = None
    observation: Optional[ReasoningObservation] = None
    reasoning: str = ""
    timestamp: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict:
        return {
            "step_id": self.step_id,
            "phase": self.phase,
            "input_state": self.input_state.to_dict(),
            "output_state": self.output_state.to_dict(),
            "operator_applied": self.operator_applied,
            "observation": {
                "value": self.observation.observed_value.name,
                "probability": self.observation.observation_probability,
                "type": self.observation.observation_type,
            } if self.observation else None,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat(),
        }


class QLMTrinaryEngine:
    """
    The core QLM-Trinary reasoning engine.

    This engine maintains reasoning in superposition as long as possible,
    only collapsing when:
    - A decision must be made
    - Evidence strongly favors one value
    - Time/resource constraints require commitment

    Key operations:
    - initialize: Start with a question/proposition
    - evolve: Apply reasoning operators
    - observe: Collapse to decision
    - branch: Create parallel reasoning paths
    - interfere: Combine parallel paths (may amplify or cancel)
    """

    # Standard reasoning operators (3x3 unitary matrices)
    OPERATORS = {
        # Hadamard-like: creates superposition from pure state
        "SUPERPOSE": np.array([
            [1, 1, 1],
            [1, np.exp(2j*np.pi/3), np.exp(4j*np.pi/3)],
            [1, np.exp(4j*np.pi/3), np.exp(2j*np.pi/3)],
        ]) / np.sqrt(3),

        # Shift operator: rotates affirm→unknown→deny→affirm
        "DOUBT": np.array([
            [0, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
        ], dtype=complex),

        # Phase operator: adds reasoning "direction"
        "REFLECT": np.diag([1, 1, -1]).astype(complex),

        # Identity: no change
        "IDENTITY": np.eye(3, dtype=complex),

        # Amplify affirm
        "STRENGTHEN": np.array([
            [1, 0.3, 0],
            [0, 0.7, 0],
            [0, 0, 1],
        ], dtype=complex),

        # Amplify deny
        "CHALLENGE": np.array([
            [1, 0, 0],
            [0, 0.7, 0],
            [0, 0.3, 1],
        ], dtype=complex),
    }

    def __init__(self, agent_id: str, domain: str = "general"):
        self.agent_id = agent_id
        self.domain = domain
        self.current_state: Optional[SuperpositionState] = None
        self.steps: list[TrinaryReasoningStep] = []
        self.branches: dict[str, SuperpositionState] = {}
        self.observations: list[ReasoningObservation] = []

    def _generate_step_id(self) -> str:
        data = f"{self.agent_id}:{len(self.steps)}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def initialize(self, proposition: str, prior: SuperpositionState = None) -> SuperpositionState:
        """
        Initialize reasoning about a proposition.

        If no prior is given, start with uniform uncertainty (maximum entropy).
        """
        if prior is None:
            self.current_state = SuperpositionState.uniform(context={"proposition": proposition})
        else:
            prior.context["proposition"] = proposition
            self.current_state = prior

        return self.current_state

    def evolve(self, operator: str, reasoning: str = "") -> SuperpositionState:
        """
        Apply a reasoning operator to evolve the state.

        Operators are unitary transformations that preserve total probability
        but redistribute amplitudes across trinary values.
        """
        if self.current_state is None:
            raise ValueError("Must initialize before evolving")

        op_matrix = self.OPERATORS.get(operator, self.OPERATORS["IDENTITY"])
        new_state = self.current_state.apply_operator(op_matrix)

        step = TrinaryReasoningStep(
            step_id=self._generate_step_id(),
            phase="evolve",
            input_state=self.current_state,
            output_state=new_state,
            operator_applied=operator,
            reasoning=reasoning,
        )
        self.steps.append(step)
        self.current_state = new_state

        return new_state

    def condition(self, evidence: TrinaryValue, strength: float = 0.5) -> SuperpositionState:
        """
        Condition the state on evidence (soft measurement).

        Unlike full observation, this nudges probabilities toward evidence
        without fully collapsing the superposition.
        """
        if self.current_state is None:
            raise ValueError("Must initialize before conditioning")

        # Amplify amplitude of evidence value
        new_amps = {}
        for v in TrinaryValue:
            amp = self.current_state.amplitudes[v]
            if v == evidence:
                new_amps[v] = Amplitude(amp.magnitude * (1 + strength), amp.phase)
            else:
                new_amps[v] = Amplitude(amp.magnitude * (1 - strength * 0.3), amp.phase)

        new_state = SuperpositionState(
            amplitudes=new_amps,
            context={**self.current_state.context, "evidence": evidence.name}
        )

        step = TrinaryReasoningStep(
            step_id=self._generate_step_id(),
            phase="condition",
            input_state=self.current_state,
            output_state=new_state,
            reasoning=f"Conditioned on {evidence.name} with strength {strength}",
        )
        self.steps.append(step)
        self.current_state = new_state

        return new_state

    def branch(self, name: str) -> str:
        """
        Create a parallel reasoning branch.

        This allows exploring multiple reasoning paths simultaneously
        before deciding which to commit to.
        """
        if self.current_state is None:
            raise ValueError("Must initialize before branching")

        self.branches[name] = SuperpositionState(
            amplitudes={v: Amplitude(a.magnitude, a.phase) for v, a in self.current_state.amplitudes.items()},
            context={**self.current_state.context, "branch": name}
        )
        return name

    def switch_branch(self, name: str) -> SuperpositionState:
        """Switch to a different reasoning branch."""
        if name not in self.branches:
            raise ValueError(f"Branch {name} does not exist")
        self.current_state = self.branches[name]
        return self.current_state

    def interfere_branches(self, names: list[str], weights: list[float] = None) -> SuperpositionState:
        """
        Interfere multiple branches together.

        This is where quantum-like effects emerge: paths that align
        (similar phases) amplify each other; paths that oppose cancel.
        """
        if weights is None:
            weights = [1.0 / len(names)] * len(names)

        states = [self.branches[n] for n in names]
        result = states[0]
        for state, weight in zip(states[1:], weights[1:]):
            result = result.interfere(state, weight)

        step = TrinaryReasoningStep(
            step_id=self._generate_step_id(),
            phase="interfere",
            input_state=self.current_state,
            output_state=result,
            reasoning=f"Interfered branches: {names}",
        )
        self.steps.append(step)
        self.current_state = result

        return result

    def observe(
        self,
        observation_type: str = "decision",
        force_value: TrinaryValue = None
    ) -> tuple[TrinaryValue, float]:
        """
        Collapse the superposition to a definite value.

        Returns the observed value and the probability of that outcome.
        """
        if self.current_state is None:
            raise ValueError("Must initialize before observing")

        observation, value = ReasoningObservation.collapse(
            state=self.current_state,
            observation_type=observation_type,
            observer=self.agent_id,
            force_value=force_value,
        )
        self.observations.append(observation)

        # Create pure state from observation
        new_state = SuperpositionState.pure(value, context=self.current_state.context)

        step = TrinaryReasoningStep(
            step_id=self._generate_step_id(),
            phase="observe",
            input_state=self.current_state,
            output_state=new_state,
            observation=observation,
            reasoning=f"Collapsed to {value.name} with probability {observation.observation_probability:.3f}",
        )
        self.steps.append(step)
        self.current_state = new_state

        return value, observation.observation_probability

    def get_chain(self) -> dict:
        """Get the complete reasoning chain."""
        return {
            "agent_id": self.agent_id,
            "domain": self.domain,
            "steps": [s.to_dict() for s in self.steps],
            "final_state": self.current_state.to_dict() if self.current_state else None,
            "observations": [
                {
                    "value": o.observed_value.name,
                    "probability": o.observation_probability,
                    "type": o.observation_type,
                }
                for o in self.observations
            ],
            "branches": list(self.branches.keys()),
        }


def create_qlm_engine(agent_id: str, domain: str = "general") -> QLMTrinaryEngine:
    """Factory function to create a QLM-Trinary reasoning engine."""
    return QLMTrinaryEngine(agent_id, domain)
