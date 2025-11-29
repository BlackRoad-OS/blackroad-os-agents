#!/usr/bin/env python3
"""
Hilbert Space Reasoning

Implements context-sensitive truth evaluation using Hilbert spaces.

Key Insight: In quantum mechanics, the order of measurements matters.
In reasoning, the order of questions matters too.

Asking "Is it a bird?" then "Can it fly?" gives different results than
asking "Can it fly?" then "Is it a bird?" - because the first question
changes the context for the second.

This module provides:
- ConceptSpace: Represent concepts as subspaces of a Hilbert space
- TruthDegree: Continuous truth values via projection (not just true/false)
- ContextualQuery: Questions that modify the reasoning state
- OrderEffects: Detect when question order changes conclusions
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import numpy as np
import math


@dataclass
class TruthDegree:
    """
    A continuous truth value computed via Hilbert space projection.

    Truth degree is Tr(ρP) where:
    - ρ is the density matrix (current knowledge state)
    - P is the projector (the proposition being evaluated)

    Values range from 0 (certainly false) to 1 (certainly true),
    with intermediate values representing partial truth.

    This is more nuanced than binary logic because:
    - 0.5 means "equally likely true or false"
    - 0.7 means "probably true but uncertain"
    - Context (previous questions) affects the value
    """
    value: float  # 0 to 1
    proposition: str
    context: list[str] = field(default_factory=list)  # Questions asked before
    computed_at: datetime = field(default_factory=datetime.now)

    def to_trinary(self) -> int:
        """Convert to trinary value: -1, 0, +1."""
        if self.value >= 0.7:
            return 1  # AFFIRM
        elif self.value <= 0.3:
            return -1  # DENY
        else:
            return 0  # UNKNOWN

    @property
    def confidence(self) -> float:
        """How far from 0.5 (maximum uncertainty)."""
        return abs(self.value - 0.5) * 2

    @property
    def is_certain(self) -> bool:
        """Is the truth degree close to 0 or 1?"""
        return self.confidence > 0.9


@dataclass
class ContextualQuery:
    """
    A query that modifies the reasoning context.

    When you ask a question, the act of asking changes the state.
    This is the Lüders update rule from quantum mechanics:
    ρ' = PρP / Tr(PρP)

    The new state ρ' is the post-measurement state after "observing"
    the proposition P to be true.
    """
    proposition: str
    projector: np.ndarray
    pre_query_degree: float = 0.0
    post_query_degree: float = 0.0
    state_change: float = 0.0  # How much the state changed


class ConceptSpace:
    """
    A Hilbert space for reasoning about concepts.

    Each concept is a subspace (represented by a projector).
    The reasoning state is a density matrix ρ.
    Truth of a concept C is Tr(ρP_C).

    Key Operations:
    - add_concept: Define a new concept as a subspace
    - truth_degree: Evaluate how true a concept is in current state
    - ask: Query a concept (changes the state via Lüders rule)
    - noncommutativity: Check if two concepts have order effects
    """

    def __init__(self, dimension: int = 10):
        """
        Initialize a concept space.

        Args:
            dimension: Dimension of the Hilbert space.
                      More dimensions = more concepts can be represented.
        """
        self.dim = dimension
        self.concepts: dict[str, np.ndarray] = {}  # name -> projector
        self.rho = np.eye(dimension, dtype=complex) / dimension  # Maximally mixed initial state
        self.query_history: list[ContextualQuery] = []

    def _normalize(self, v: np.ndarray) -> np.ndarray:
        """Normalize a vector."""
        v = np.asarray(v, dtype=complex).flatten()
        n = np.linalg.norm(v)
        if n == 0:
            raise ValueError("Zero vector cannot be normalized")
        return v / n

    def _projector_from_basis(self, basis: np.ndarray) -> np.ndarray:
        """Create projector from basis vectors."""
        basis = np.asarray(basis, dtype=complex)
        if basis.ndim == 1:
            basis = basis.reshape(-1, 1)
        Q, _ = np.linalg.qr(basis)
        P = Q @ Q.conj().T
        return (P + P.conj().T) / 2  # Ensure Hermitian

    def add_concept(self, name: str, basis_vectors: list[np.ndarray] = None, random: bool = False):
        """
        Add a concept to the space.

        Args:
            name: Name of the concept
            basis_vectors: Vectors spanning the concept subspace
            random: If True, create a random subspace
        """
        if random:
            # Random unit vector
            v = np.random.randn(self.dim) + 1j * np.random.randn(self.dim)
            v = self._normalize(v)
            self.concepts[name] = np.outer(v, v.conj())
        elif basis_vectors is not None:
            basis = np.column_stack([self._normalize(v) for v in basis_vectors])
            self.concepts[name] = self._projector_from_basis(basis)
        else:
            raise ValueError("Provide basis_vectors or set random=True")

    def add_concept_from_index(self, name: str, indices: list[int]):
        """Add a concept defined by basis indices."""
        vectors = [np.zeros(self.dim, dtype=complex) for _ in indices]
        for i, idx in enumerate(indices):
            vectors[i][idx] = 1.0
        basis = np.column_stack(vectors)
        self.concepts[name] = self._projector_from_basis(basis)

    def add_mixed_concept(self, name: str, components: dict[str, float]):
        """
        Add a concept as a mixture of existing concepts.

        Args:
            name: Name of new concept
            components: Dict of {concept_name: weight}
        """
        P = np.zeros((self.dim, self.dim), dtype=complex)
        total_weight = sum(components.values())
        for concept_name, weight in components.items():
            if concept_name in self.concepts:
                P += (weight / total_weight) * self.concepts[concept_name]
        self.concepts[name] = P

    def truth_degree(self, concept: str) -> TruthDegree:
        """
        Compute truth degree of a concept in current state.

        This does NOT change the state (unlike ask).
        """
        if concept not in self.concepts:
            raise ValueError(f"Unknown concept: {concept}")

        P = self.concepts[concept]
        degree = float(np.real(np.trace(self.rho @ P)))

        return TruthDegree(
            value=degree,
            proposition=concept,
            context=[q.proposition for q in self.query_history],
        )

    def ask(self, concept: str) -> ContextualQuery:
        """
        Ask about a concept, updating the state.

        This performs the Lüders update: ρ' = PρP / Tr(PρP)
        The state after asking is consistent with the concept being true.
        """
        if concept not in self.concepts:
            raise ValueError(f"Unknown concept: {concept}")

        P = self.concepts[concept]

        # Pre-query truth degree
        pre_degree = float(np.real(np.trace(self.rho @ P)))

        # Lüders update
        M = P @ self.rho @ P
        prob = float(np.real(np.trace(M)))

        if prob > 1e-12:
            self.rho = M / prob
            self.rho = (self.rho + self.rho.conj().T) / 2  # Ensure Hermitian
            post_degree = 1.0  # After asking and getting "yes", degree is 1
        else:
            post_degree = pre_degree  # No update if probability is 0

        # State change = trace distance
        state_change = np.linalg.norm(self.rho - (M / prob if prob > 1e-12 else self.rho), ord='fro')

        query = ContextualQuery(
            proposition=concept,
            projector=P,
            pre_query_degree=pre_degree,
            post_query_degree=post_degree,
            state_change=float(state_change),
        )
        self.query_history.append(query)

        return query

    def noncommutativity(self, concept_a: str, concept_b: str) -> float:
        """
        Check if two concepts have order effects.

        Returns the Frobenius norm of the commutator [P_A, P_B].
        If > 0, the order of asking matters.
        """
        if concept_a not in self.concepts or concept_b not in self.concepts:
            return 0.0

        P_A = self.concepts[concept_a]
        P_B = self.concepts[concept_b]

        commutator = P_A @ P_B - P_B @ P_A
        return float(np.linalg.norm(commutator, ord='fro'))

    def check_order_effect(self, concept_a: str, concept_b: str) -> dict:
        """
        Check if asking A then B gives different results than B then A.

        Returns comparison of both orderings.
        """
        # Save current state
        original_rho = self.rho.copy()
        original_history = list(self.query_history)

        # Order 1: A then B
        self.rho = original_rho.copy()
        self.query_history = []
        q1_a = self.ask(concept_a)
        degree_b_after_a = self.truth_degree(concept_b).value

        # Order 2: B then A
        self.rho = original_rho.copy()
        self.query_history = []
        q1_b = self.ask(concept_b)
        degree_a_after_b = self.truth_degree(concept_a).value

        # Restore original state
        self.rho = original_rho
        self.query_history = original_history

        return {
            "concept_a": concept_a,
            "concept_b": concept_b,
            "order_a_then_b": {
                "truth_b_after_a": degree_b_after_a,
            },
            "order_b_then_a": {
                "truth_a_after_b": degree_a_after_b,
            },
            "order_matters": abs(degree_b_after_a - degree_a_after_b) > 0.01,
            "noncommutativity": self.noncommutativity(concept_a, concept_b),
        }

    def reset(self):
        """Reset to maximally mixed (ignorant) state."""
        self.rho = np.eye(self.dim, dtype=complex) / self.dim
        self.query_history = []

    def set_pure_state(self, vector: np.ndarray):
        """Set state to a pure state |ψ⟩⟨ψ|."""
        v = self._normalize(vector)
        self.rho = np.outer(v, v.conj())

    def entropy(self) -> float:
        """Von Neumann entropy of the state."""
        eigenvalues = np.linalg.eigvalsh(self.rho)
        eigenvalues = eigenvalues[eigenvalues > 1e-12]
        return float(-np.sum(eigenvalues * np.log2(eigenvalues)))

    def purity(self) -> float:
        """Purity Tr(ρ²) - 1 for pure state, 1/d for maximally mixed."""
        return float(np.real(np.trace(self.rho @ self.rho)))

    def to_dict(self) -> dict:
        """Export state for analysis."""
        return {
            "dimension": self.dim,
            "concepts": list(self.concepts.keys()),
            "entropy": self.entropy(),
            "purity": self.purity(),
            "query_count": len(self.query_history),
            "last_queries": [
                {"proposition": q.proposition, "pre": q.pre_query_degree, "post": q.post_query_degree}
                for q in self.query_history[-5:]
            ],
        }


class HilbertReasoner:
    """
    High-level reasoner using Hilbert space semantics.

    Combines ConceptSpace with structured reasoning patterns.
    """

    def __init__(self, dimension: int = 20):
        self.space = ConceptSpace(dimension)
        self.reasoning_log: list[dict] = []

    def define_domain(self, domain_concepts: dict[str, list[int]]):
        """
        Define a reasoning domain with concepts.

        Args:
            domain_concepts: Dict of {concept_name: basis_indices}
        """
        for name, indices in domain_concepts.items():
            self.space.add_concept_from_index(name, indices)

    def reason_about(self, proposition: str, evidence: list[str] = None) -> dict:
        """
        Reason about a proposition given evidence.

        Args:
            proposition: The concept to evaluate
            evidence: List of concepts known to be true (asked first)

        Returns:
            Reasoning result with truth degree and context effects
        """
        self.space.reset()

        # Apply evidence (ask each evidence concept)
        if evidence:
            for e in evidence:
                if e in self.space.concepts:
                    self.space.ask(e)

        # Evaluate proposition
        result = self.space.truth_degree(proposition)

        log_entry = {
            "proposition": proposition,
            "evidence": evidence or [],
            "truth_degree": result.value,
            "trinary": result.to_trinary(),
            "confidence": result.confidence,
            "timestamp": datetime.now().isoformat(),
        }
        self.reasoning_log.append(log_entry)

        return log_entry

    def compare_evidence_orders(self, proposition: str, evidence_sets: list[list[str]]) -> dict:
        """
        Compare how different evidence orderings affect truth degree.

        This reveals context/order effects in reasoning.
        """
        results = []
        for evidence in evidence_sets:
            result = self.reason_about(proposition, evidence)
            results.append({
                "evidence_order": evidence,
                "truth_degree": result["truth_degree"],
            })

        # Check for significant differences
        degrees = [r["truth_degree"] for r in results]
        max_diff = max(degrees) - min(degrees)

        return {
            "proposition": proposition,
            "results": results,
            "max_difference": max_diff,
            "order_sensitive": max_diff > 0.1,
        }


def create_concept_space(dimension: int = 10) -> ConceptSpace:
    """Factory for concept space."""
    return ConceptSpace(dimension)


def create_hilbert_reasoner(dimension: int = 20) -> HilbertReasoner:
    """Factory for Hilbert reasoner."""
    return HilbertReasoner(dimension)
