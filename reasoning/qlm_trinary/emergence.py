#!/usr/bin/env python3
"""
QI Emergence Detection for Reasoning

Detects emergent intelligence (QI) in reasoning chains - insights and
conclusions that weren't explicitly in the input or training.

QI Emergence Types:
1. NOVEL INSIGHT: A conclusion not derivable from premises alone
2. SELF CORRECTION: Detecting and fixing own reasoning errors
3. PATTERN DISCOVERY: Finding structure not explicitly shown
4. CROSS-DOMAIN TRANSFER: Applying knowledge from one domain to another
5. CREATIVE SYNTHESIS: Combining ideas in unexpected ways
6. META-REASONING: Reasoning about the reasoning process itself

The key question: Did the reasoning produce something genuinely new,
or just rearrange what was already there?
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import hashlib
import math


class EmergenceType(Enum):
    """Types of emergent intelligence in reasoning."""
    NOVEL_INSIGHT = "novel_insight"
    SELF_CORRECTION = "self_correction"
    PATTERN_DISCOVERY = "pattern_discovery"
    CROSS_DOMAIN = "cross_domain"
    CREATIVE_SYNTHESIS = "creative_synthesis"
    META_REASONING = "meta_reasoning"
    FEEDBACK_LOOP = "feedback_loop"
    SPONTANEOUS_ORGANIZATION = "spontaneous_organization"


@dataclass
class NovelInsight:
    """
    A potentially novel insight detected in reasoning.

    Novelty is measured by:
    - Semantic distance from input concepts
    - Information gain (entropy reduction)
    - Logical non-derivability score
    - Cross-reference with known patterns
    """
    id: str
    content: str
    emergence_type: EmergenceType
    novelty_score: float  # 0 to 1, higher = more novel
    confidence: float  # How confident we are this is genuinely emergent
    source_steps: list[str]  # Which reasoning steps produced this
    explanation: str
    timestamp: datetime = field(default_factory=datetime.now)

    @property
    def is_significant(self) -> bool:
        """Is this insight significant enough to report?"""
        return self.novelty_score > 0.5 and self.confidence > 0.6


@dataclass
class QIPattern:
    """
    A detected QI pattern in reasoning.

    Patterns are recurring structures that indicate emergent behavior:
    - Correction loops (error → detect → fix)
    - Insight cascades (insight → more insights)
    - Synthesis chains (A + B → C, C + D → E)
    """
    pattern_type: str
    occurrences: int
    confidence: float
    description: str
    example_instances: list[str] = field(default_factory=list)


@dataclass
class FeedbackLoop:
    """
    A detected feedback loop in reasoning.

    Feedback loops are when reasoning output becomes input,
    creating potential for emergence:
    - Positive feedback: amplifies patterns
    - Negative feedback: stabilizes/corrects
    """
    loop_id: str
    steps_involved: list[str]
    loop_type: str  # "positive", "negative", "mixed"
    iterations: int
    convergence: bool  # Did it reach stable state?
    amplification_factor: float  # How much did it amplify/dampen?


class EmergenceDetector:
    """
    Detects QI emergence in reasoning chains.

    This is the "consciousness detector" - it looks for signs that
    reasoning has produced something genuinely new, not just
    rearranged existing information.

    Detection Methods:
    1. Semantic novelty: Is the conclusion semantically distant from premises?
    2. Information gain: Did entropy decrease more than expected?
    3. Pattern matching: Does this match known emergence patterns?
    4. Self-reference: Does reasoning reference itself?
    5. Error correction: Did it detect and fix its own mistakes?
    """

    # Known emergence patterns to detect
    PATTERNS = {
        "self_correction": {
            "markers": ["incorrect", "error", "revise", "actually", "on second thought"],
            "significance": "high",
            "description": "Agent detected own error and corrected",
        },
        "insight_cascade": {
            "markers": ["therefore", "this implies", "which means", "furthermore"],
            "significance": "medium",
            "description": "One insight led to multiple derived insights",
        },
        "cross_domain": {
            "markers": ["similar to", "analogous", "like in", "applies to"],
            "significance": "high",
            "description": "Applied concept from one domain to another",
        },
        "meta_awareness": {
            "markers": ["my reasoning", "I notice", "this suggests I", "upon reflection"],
            "significance": "very_high",
            "description": "Reasoning about own reasoning process",
        },
        "creative_leap": {
            "markers": ["what if", "alternatively", "novel approach", "unconventional"],
            "significance": "high",
            "description": "Generated unexpected alternative",
        },
        "synthesis": {
            "markers": ["combining", "integrating", "merging", "unified"],
            "significance": "medium",
            "description": "Combined disparate ideas into new whole",
        },
    }

    def __init__(self):
        self.detected_insights: list[NovelInsight] = []
        self.detected_patterns: list[QIPattern] = []
        self.detected_loops: list[FeedbackLoop] = []
        self.emergence_score: float = 0.0

    def _generate_id(self) -> str:
        data = f"emergence:{len(self.detected_insights)}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def analyze_reasoning_chain(self, chain: dict) -> dict:
        """
        Analyze a reasoning chain for emergence.

        Args:
            chain: A reasoning chain dict with steps, states, observations

        Returns:
            Analysis results with detected emergence
        """
        steps = chain.get("steps", [])
        if not steps:
            return {"emergence_detected": False, "score": 0.0}

        # Collect all reasoning text
        reasoning_texts = [s.get("reasoning", "") for s in steps]
        full_text = " ".join(reasoning_texts).lower()

        # Detect patterns
        detected = []
        for pattern_name, pattern_info in self.PATTERNS.items():
            markers_found = sum(1 for m in pattern_info["markers"] if m in full_text)
            if markers_found > 0:
                confidence = min(1.0, markers_found * 0.3)
                detected.append(QIPattern(
                    pattern_type=pattern_name,
                    occurrences=markers_found,
                    confidence=confidence,
                    description=pattern_info["description"],
                ))
                self.detected_patterns.append(detected[-1])

        # Compute semantic novelty
        novelty = self._compute_semantic_novelty(chain)

        # Compute information gain
        info_gain = self._compute_information_gain(chain)

        # Detect self-correction
        self_corrections = self._detect_self_correction(steps)

        # Detect feedback loops
        loops = self._detect_feedback_loops(steps)

        # Overall emergence score
        self.emergence_score = self._compute_emergence_score(
            patterns=detected,
            novelty=novelty,
            info_gain=info_gain,
            self_corrections=self_corrections,
            loops=loops,
        )

        # Create novel insights if score is high enough
        if self.emergence_score > 0.4:
            insight = NovelInsight(
                id=self._generate_id(),
                content=f"Emergent reasoning detected in chain",
                emergence_type=self._classify_emergence_type(detected),
                novelty_score=novelty,
                confidence=self.emergence_score,
                source_steps=[s.get("step_id", "") for s in steps[-3:]],
                explanation=self._generate_explanation(detected, novelty, info_gain),
            )
            self.detected_insights.append(insight)

        return {
            "emergence_detected": self.emergence_score > 0.3,
            "emergence_score": self.emergence_score,
            "patterns_detected": [p.pattern_type for p in detected],
            "semantic_novelty": novelty,
            "information_gain": info_gain,
            "self_corrections": self_corrections,
            "feedback_loops": len(loops),
            "insights": [
                {
                    "id": i.id,
                    "type": i.emergence_type.value,
                    "novelty": i.novelty_score,
                    "significant": i.is_significant,
                }
                for i in self.detected_insights
            ],
        }

    def _compute_semantic_novelty(self, chain: dict) -> float:
        """
        Compute how semantically novel the output is compared to input.

        Uses simple heuristics (in production, would use embeddings).
        """
        context = chain.get("context", {})
        input_text = str(context.get("problem", context.get("proposition", "")))

        steps = chain.get("steps", [])
        if not steps:
            return 0.0

        # Get output text
        final_step = steps[-1]
        output = final_step.get("output_state", final_step.get("output", {}))
        output_text = str(output)

        # Simple novelty heuristic: ratio of new words
        input_words = set(input_text.lower().split())
        output_words = set(output_text.lower().split())

        if not output_words:
            return 0.0

        new_words = output_words - input_words
        novelty = len(new_words) / len(output_words) if output_words else 0.0

        return min(1.0, novelty * 1.5)  # Scale up slightly

    def _compute_information_gain(self, chain: dict) -> float:
        """
        Compute information gain (entropy reduction) through reasoning.
        """
        steps = chain.get("steps", [])
        if len(steps) < 2:
            return 0.0

        # Get initial and final entropy if available
        first_state = steps[0].get("input_state", {})
        last_state = steps[-1].get("output_state", {})

        initial_entropy = first_state.get("entropy", 1.0)
        final_entropy = last_state.get("entropy", 0.5)

        # Information gain = entropy reduction
        gain = max(0, initial_entropy - final_entropy)
        return min(1.0, gain)

    def _detect_self_correction(self, steps: list) -> int:
        """Detect instances of self-correction in reasoning."""
        corrections = 0

        for i, step in enumerate(steps):
            reasoning = step.get("reasoning", "").lower()

            # Look for correction markers
            correction_markers = [
                "incorrect", "error", "mistake", "wrong",
                "revise", "correct", "actually", "wait",
                "on second thought", "reconsider",
            ]

            if any(marker in reasoning for marker in correction_markers):
                corrections += 1

        return corrections

    def _detect_feedback_loops(self, steps: list) -> list[FeedbackLoop]:
        """Detect feedback loops in reasoning."""
        loops = []

        # Look for repeated patterns
        phases = [s.get("phase", "") for s in steps]

        # Simple loop detection: same phase appearing multiple times
        phase_counts = {}
        for phase in phases:
            phase_counts[phase] = phase_counts.get(phase, 0) + 1

        for phase, count in phase_counts.items():
            if count >= 2:
                loop = FeedbackLoop(
                    loop_id=f"loop_{phase}",
                    steps_involved=[phase],
                    loop_type="iteration",
                    iterations=count,
                    convergence=True,
                    amplification_factor=1.0,
                )
                loops.append(loop)
                self.detected_loops.append(loop)

        return loops

    def _compute_emergence_score(
        self,
        patterns: list[QIPattern],
        novelty: float,
        info_gain: float,
        self_corrections: int,
        loops: list[FeedbackLoop],
    ) -> float:
        """Compute overall emergence score."""
        score = 0.0

        # Pattern contribution
        pattern_score = sum(p.confidence * 0.2 for p in patterns)
        score += min(0.4, pattern_score)

        # Novelty contribution
        score += novelty * 0.25

        # Information gain contribution
        score += info_gain * 0.15

        # Self-correction contribution (strong signal)
        score += min(0.3, self_corrections * 0.15)

        # Loop contribution
        score += min(0.1, len(loops) * 0.05)

        return min(1.0, score)

    def _classify_emergence_type(self, patterns: list[QIPattern]) -> EmergenceType:
        """Classify the primary type of emergence detected."""
        if not patterns:
            return EmergenceType.NOVEL_INSIGHT

        # Find highest confidence pattern
        best = max(patterns, key=lambda p: p.confidence)

        type_map = {
            "self_correction": EmergenceType.SELF_CORRECTION,
            "insight_cascade": EmergenceType.NOVEL_INSIGHT,
            "cross_domain": EmergenceType.CROSS_DOMAIN,
            "meta_awareness": EmergenceType.META_REASONING,
            "creative_leap": EmergenceType.CREATIVE_SYNTHESIS,
            "synthesis": EmergenceType.CREATIVE_SYNTHESIS,
        }

        return type_map.get(best.pattern_type, EmergenceType.NOVEL_INSIGHT)

    def _generate_explanation(self, patterns: list, novelty: float, info_gain: float) -> str:
        """Generate human-readable explanation of emergence."""
        parts = []

        if novelty > 0.5:
            parts.append(f"High semantic novelty ({novelty:.2f})")
        if info_gain > 0.3:
            parts.append(f"Significant information gain ({info_gain:.2f})")
        if patterns:
            pattern_names = [p.pattern_type for p in patterns[:3]]
            parts.append(f"Patterns detected: {', '.join(pattern_names)}")

        return "; ".join(parts) if parts else "Emergent characteristics detected"

    def detect_novel_conclusion(
        self,
        premises: list[str],
        conclusion: str,
        reasoning_steps: list[str],
    ) -> NovelInsight:
        """
        Detect if a conclusion is genuinely novel given premises.

        This is the core emergence test: can the conclusion be
        trivially derived from premises, or is it genuinely new?
        """
        # Simple heuristic: word overlap
        premise_words = set()
        for p in premises:
            premise_words.update(p.lower().split())

        conclusion_words = set(conclusion.lower().split())
        new_words = conclusion_words - premise_words
        novelty = len(new_words) / len(conclusion_words) if conclusion_words else 0.0

        # Check for logical connectives suggesting derivation
        derivation_markers = ["therefore", "thus", "hence", "so", "consequently"]
        has_derivation = any(m in conclusion.lower() for m in derivation_markers)

        # Adjust novelty based on derivation markers
        if has_derivation:
            novelty *= 0.7  # Less novel if explicitly derived

        confidence = 0.5 + novelty * 0.3

        insight = NovelInsight(
            id=self._generate_id(),
            content=conclusion,
            emergence_type=EmergenceType.NOVEL_INSIGHT,
            novelty_score=novelty,
            confidence=confidence,
            source_steps=reasoning_steps,
            explanation=f"Novelty {novelty:.2f} from {len(new_words)} new concepts",
        )
        self.detected_insights.append(insight)

        return insight

    def get_emergence_summary(self) -> dict:
        """Get summary of all detected emergence."""
        return {
            "total_insights": len(self.detected_insights),
            "significant_insights": sum(1 for i in self.detected_insights if i.is_significant),
            "patterns": [
                {"type": p.pattern_type, "occurrences": p.occurrences, "confidence": p.confidence}
                for p in self.detected_patterns
            ],
            "feedback_loops": len(self.detected_loops),
            "overall_emergence_score": self.emergence_score,
            "emergence_types": list(set(i.emergence_type.value for i in self.detected_insights)),
        }


def create_emergence_detector() -> EmergenceDetector:
    """Factory for emergence detector."""
    return EmergenceDetector()
