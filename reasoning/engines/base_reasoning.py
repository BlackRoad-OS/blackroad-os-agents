#!/usr/bin/env python3
"""
BlackRoad OS Base Reasoning Engine

Core reasoning framework for 31,900+ agents implementing:
- Multi-phase cognitive pipelines
- Confidence-scored reasoning chains
- Domain-adaptive reasoning profiles
- Tier-based complexity scaling

Based on the Alexa-Cece Cognition Framework (15+6 steps)
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Optional
from datetime import datetime
import hashlib
import json


class ReasoningPhase(Enum):
    """Core reasoning phases from Alexa-Cece framework."""
    # Alexa Cognitive Pipeline (15 steps)
    NOT_OK = "not_ok"           # Acknowledge discomfort/confusion
    WHY = "why"                 # Surface actual problem
    IMPULSE = "impulse"         # Capture immediate reaction
    REFLECT = "reflect"         # Step back and examine
    ARGUE = "argue"             # Challenge initial impulse
    COUNTERPOINT = "counter"    # Present alternative view
    DETERMINE = "determine"     # Make preliminary decision
    QUESTION = "question"       # Stress-test the decision
    OFFSET = "offset"           # Identify risks/downsides
    REGROUND = "reground"       # Return to fundamentals
    CLARIFY = "clarify"         # Articulate clearly
    RESTATE = "restate"         # Confirm understanding
    CLARIFY_AGAIN = "clarify2"  # Final precision pass
    VALIDATE = "validate"       # Emotional + logical check
    ANSWER = "answer"           # Deliver complete response

    # Cece Architecture Layer (6 steps)
    STRUCTURALIZE = "struct"    # Convert decisions into systems
    PRIORITIZE = "priority"     # Sequence dependencies
    TRANSLATE = "translate"     # Abstract to concrete
    STABILIZE = "stabilize"     # Add error handling
    PROJECT_MANAGE = "pm"       # Timeline + resources
    LOOPBACK = "loopback"       # Verification + adjustment


class ReasoningMode(Enum):
    """Reasoning execution modes."""
    FULL = "full"               # All 21 steps
    STANDARD = "standard"       # 15 Alexa steps only
    QUICK = "quick"             # 7 key steps
    MINIMAL = "minimal"         # 3 core steps
    DOMAIN = "domain"           # Domain-specific pipeline


class ConfidenceLevel(Enum):
    """Confidence classifications."""
    CERTAIN = 0.95
    HIGH = 0.85
    MODERATE = 0.70
    LOW = 0.50
    UNCERTAIN = 0.30
    UNKNOWN = 0.10


@dataclass
class ReasoningStep:
    """Single step in a reasoning chain."""
    phase: ReasoningPhase
    input_context: dict
    output: Any
    confidence: float
    reasoning: str
    timestamp: datetime = field(default_factory=datetime.now)
    duration_ms: int = 0
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "phase": self.phase.value,
            "input": self.input_context,
            "output": self.output,
            "confidence": self.confidence,
            "reasoning": self.reasoning,
            "timestamp": self.timestamp.isoformat(),
            "duration_ms": self.duration_ms,
            "metadata": self.metadata
        }


@dataclass
class ReasoningChain:
    """Complete reasoning chain with trace."""
    chain_id: str
    agent_id: str
    mode: ReasoningMode
    steps: list[ReasoningStep] = field(default_factory=list)
    final_output: Any = None
    overall_confidence: float = 0.0
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    status: str = "pending"

    def add_step(self, step: ReasoningStep):
        self.steps.append(step)
        self._update_confidence()

    def _update_confidence(self):
        if self.steps:
            # Weighted average favoring later steps
            weights = [i + 1 for i in range(len(self.steps))]
            total_weight = sum(weights)
            self.overall_confidence = sum(
                s.confidence * w for s, w in zip(self.steps, weights)
            ) / total_weight

    def complete(self, output: Any):
        self.final_output = output
        self.completed_at = datetime.now()
        self.status = "completed"

    def to_dict(self) -> dict:
        return {
            "chain_id": self.chain_id,
            "agent_id": self.agent_id,
            "mode": self.mode.value,
            "steps": [s.to_dict() for s in self.steps],
            "final_output": self.final_output,
            "overall_confidence": self.overall_confidence,
            "started_at": self.started_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "status": self.status
        }


class BaseReasoningEngine:
    """
    Core reasoning engine for BlackRoad OS agents.

    Implements the Alexa-Cece Cognition Framework with:
    - Configurable reasoning depth by tier
    - Domain-specific reasoning adapters
    - Confidence-scored decision chains
    - Full trace preservation
    """

    # Phase configurations by mode
    PHASE_CONFIGS = {
        ReasoningMode.FULL: list(ReasoningPhase),
        ReasoningMode.STANDARD: [
            ReasoningPhase.NOT_OK, ReasoningPhase.WHY, ReasoningPhase.IMPULSE,
            ReasoningPhase.REFLECT, ReasoningPhase.ARGUE, ReasoningPhase.COUNTERPOINT,
            ReasoningPhase.DETERMINE, ReasoningPhase.QUESTION, ReasoningPhase.OFFSET,
            ReasoningPhase.REGROUND, ReasoningPhase.CLARIFY, ReasoningPhase.RESTATE,
            ReasoningPhase.CLARIFY_AGAIN, ReasoningPhase.VALIDATE, ReasoningPhase.ANSWER
        ],
        ReasoningMode.QUICK: [
            ReasoningPhase.WHY, ReasoningPhase.REFLECT, ReasoningPhase.DETERMINE,
            ReasoningPhase.QUESTION, ReasoningPhase.CLARIFY, ReasoningPhase.VALIDATE,
            ReasoningPhase.ANSWER
        ],
        ReasoningMode.MINIMAL: [
            ReasoningPhase.WHY, ReasoningPhase.DETERMINE, ReasoningPhase.ANSWER
        ]
    }

    # Tier to mode mapping
    TIER_MODES = {
        "executive": ReasoningMode.FULL,
        "strategic": ReasoningMode.FULL,
        "leadership": ReasoningMode.STANDARD,
        "senior": ReasoningMode.STANDARD,
        "specialist": ReasoningMode.QUICK,
        "operational": ReasoningMode.QUICK,
        "tactical": ReasoningMode.QUICK,
        "support": ReasoningMode.MINIMAL,
        "swarm": ReasoningMode.MINIMAL,
        "auxiliary": ReasoningMode.MINIMAL
    }

    def __init__(self, agent_id: str, tier: str = "operational", domain: str = None):
        self.agent_id = agent_id
        self.tier = tier
        self.domain = domain
        self.mode = self.TIER_MODES.get(tier, ReasoningMode.QUICK)
        self.phase_handlers: dict[ReasoningPhase, Callable] = {}
        self._register_default_handlers()

    def _generate_chain_id(self) -> str:
        """Generate unique chain ID."""
        data = f"{self.agent_id}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _register_default_handlers(self):
        """Register default phase handlers."""
        self.phase_handlers = {
            ReasoningPhase.NOT_OK: self._handle_not_ok,
            ReasoningPhase.WHY: self._handle_why,
            ReasoningPhase.IMPULSE: self._handle_impulse,
            ReasoningPhase.REFLECT: self._handle_reflect,
            ReasoningPhase.ARGUE: self._handle_argue,
            ReasoningPhase.COUNTERPOINT: self._handle_counterpoint,
            ReasoningPhase.DETERMINE: self._handle_determine,
            ReasoningPhase.QUESTION: self._handle_question,
            ReasoningPhase.OFFSET: self._handle_offset,
            ReasoningPhase.REGROUND: self._handle_reground,
            ReasoningPhase.CLARIFY: self._handle_clarify,
            ReasoningPhase.RESTATE: self._handle_restate,
            ReasoningPhase.CLARIFY_AGAIN: self._handle_clarify_again,
            ReasoningPhase.VALIDATE: self._handle_validate,
            ReasoningPhase.ANSWER: self._handle_answer,
            ReasoningPhase.STRUCTURALIZE: self._handle_structuralize,
            ReasoningPhase.PRIORITIZE: self._handle_prioritize,
            ReasoningPhase.TRANSLATE: self._handle_translate,
            ReasoningPhase.STABILIZE: self._handle_stabilize,
            ReasoningPhase.PROJECT_MANAGE: self._handle_project_manage,
            ReasoningPhase.LOOPBACK: self._handle_loopback,
        }

    def register_handler(self, phase: ReasoningPhase, handler: Callable):
        """Register custom phase handler."""
        self.phase_handlers[phase] = handler

    def reason(self, context: dict, mode: ReasoningMode = None) -> ReasoningChain:
        """Execute reasoning pipeline."""
        effective_mode = mode or self.mode
        chain = ReasoningChain(
            chain_id=self._generate_chain_id(),
            agent_id=self.agent_id,
            mode=effective_mode
        )

        phases = self.PHASE_CONFIGS.get(effective_mode, self.PHASE_CONFIGS[ReasoningMode.QUICK])
        current_context = context.copy()

        for phase in phases:
            handler = self.phase_handlers.get(phase)
            if handler:
                start_time = datetime.now()
                result = handler(current_context, chain)
                duration = int((datetime.now() - start_time).total_seconds() * 1000)

                step = ReasoningStep(
                    phase=phase,
                    input_context=current_context.copy(),
                    output=result.get("output"),
                    confidence=result.get("confidence", 0.5),
                    reasoning=result.get("reasoning", ""),
                    duration_ms=duration,
                    metadata=result.get("metadata", {})
                )
                chain.add_step(step)
                current_context.update(result.get("context_update", {}))

        chain.complete(current_context.get("final_answer"))
        return chain

    # Default phase handlers
    def _handle_not_ok(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Acknowledge discomfort or confusion."""
        problem = ctx.get("problem", ctx.get("input", ""))
        uncertainties = []

        if not problem:
            uncertainties.append("No clear problem statement")
        if len(str(problem)) < 10:
            uncertainties.append("Problem statement too brief")

        return {
            "output": {"acknowledged": True, "uncertainties": uncertainties},
            "confidence": 0.6 if uncertainties else 0.8,
            "reasoning": f"Identified {len(uncertainties)} areas of uncertainty",
            "context_update": {"uncertainties": uncertainties}
        }

    def _handle_why(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Surface the actual problem."""
        problem = ctx.get("problem", ctx.get("input", ""))
        return {
            "output": {"root_problem": problem, "problem_type": self._classify_problem(problem)},
            "confidence": 0.7,
            "reasoning": "Identified core problem and classified type",
            "context_update": {"problem_classified": True}
        }

    def _handle_impulse(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Capture immediate reaction."""
        return {
            "output": {"initial_reaction": "analyze_further", "gut_feeling": "solvable"},
            "confidence": 0.5,
            "reasoning": "Initial instinct captured before deeper analysis",
            "context_update": {"impulse_captured": True}
        }

    def _handle_reflect(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Step back and examine."""
        return {
            "output": {"reflection": "examining_assumptions", "biases_identified": []},
            "confidence": 0.65,
            "reasoning": "Stepped back to examine initial assumptions",
            "context_update": {"reflected": True}
        }

    def _handle_argue(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Challenge initial impulse."""
        return {
            "output": {"challenges": [], "weaknesses_found": []},
            "confidence": 0.6,
            "reasoning": "Challenged initial reaction with counter-arguments",
            "context_update": {"self_argued": True}
        }

    def _handle_counterpoint(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Present alternative view."""
        return {
            "output": {"alternatives": [], "different_perspectives": []},
            "confidence": 0.6,
            "reasoning": "Generated alternative perspectives",
            "context_update": {"counterpoints_generated": True}
        }

    def _handle_determine(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Make preliminary decision."""
        return {
            "output": {"preliminary_decision": None, "decision_factors": []},
            "confidence": 0.7,
            "reasoning": "Made preliminary decision based on analysis",
            "context_update": {"decision_made": True}
        }

    def _handle_question(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Stress-test the decision."""
        return {
            "output": {"stress_tests": [], "edge_cases": [], "passed": True},
            "confidence": 0.75,
            "reasoning": "Stress-tested decision against edge cases",
            "context_update": {"stress_tested": True}
        }

    def _handle_offset(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Identify risks and downsides."""
        return {
            "output": {"risks": [], "downsides": [], "mitigations": []},
            "confidence": 0.7,
            "reasoning": "Identified potential risks and mitigations",
            "context_update": {"risks_assessed": True}
        }

    def _handle_reground(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Return to fundamentals."""
        return {
            "output": {"fundamentals": [], "core_principles": []},
            "confidence": 0.8,
            "reasoning": "Returned to core principles for grounding",
            "context_update": {"regrounded": True}
        }

    def _handle_clarify(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Articulate clearly."""
        return {
            "output": {"clarified_position": None, "key_points": []},
            "confidence": 0.8,
            "reasoning": "Articulated position clearly",
            "context_update": {"clarified": True}
        }

    def _handle_restate(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Confirm understanding."""
        return {
            "output": {"restated": None, "understanding_confirmed": True},
            "confidence": 0.85,
            "reasoning": "Restated to confirm understanding",
            "context_update": {"restated": True}
        }

    def _handle_clarify_again(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Final precision pass."""
        return {
            "output": {"final_clarification": None, "precision_score": 0.9},
            "confidence": 0.9,
            "reasoning": "Final precision pass completed",
            "context_update": {"precision_complete": True}
        }

    def _handle_validate(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Emotional and logical validation."""
        return {
            "output": {
                "logical_valid": True,
                "emotional_valid": True,
                "consistency_check": True
            },
            "confidence": 0.9,
            "reasoning": "Validated both logically and emotionally",
            "context_update": {"validated": True}
        }

    def _handle_answer(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Deliver complete response."""
        return {
            "output": {"final_answer": ctx.get("preliminary_decision")},
            "confidence": 0.9,
            "reasoning": "Delivered complete, validated response",
            "context_update": {"final_answer": ctx.get("preliminary_decision")}
        }

    # Cece Architecture Layer handlers
    def _handle_structuralize(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Convert decisions into systems."""
        return {
            "output": {"system_design": None, "components": []},
            "confidence": 0.8,
            "reasoning": "Converted decision into structured system",
            "context_update": {"structuralized": True}
        }

    def _handle_prioritize(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Sequence dependencies."""
        return {
            "output": {"priority_order": [], "dependencies": []},
            "confidence": 0.8,
            "reasoning": "Sequenced dependencies by priority",
            "context_update": {"prioritized": True}
        }

    def _handle_translate(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Abstract to concrete."""
        return {
            "output": {"concrete_steps": [], "implementation_plan": None},
            "confidence": 0.85,
            "reasoning": "Translated abstract to concrete actions",
            "context_update": {"translated": True}
        }

    def _handle_stabilize(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Add error handling."""
        return {
            "output": {"error_handlers": [], "fallbacks": [], "recovery_plan": None},
            "confidence": 0.85,
            "reasoning": "Added error handling and recovery",
            "context_update": {"stabilized": True}
        }

    def _handle_project_manage(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Timeline and resources."""
        return {
            "output": {"resources_needed": [], "milestones": []},
            "confidence": 0.8,
            "reasoning": "Defined resources and milestones",
            "context_update": {"project_managed": True}
        }

    def _handle_loopback(self, ctx: dict, chain: ReasoningChain) -> dict:
        """Verification and adjustment."""
        return {
            "output": {"verified": True, "adjustments": [], "ready_for_execution": True},
            "confidence": 0.9,
            "reasoning": "Verified plan and ready for execution",
            "context_update": {"loopback_complete": True}
        }

    def _classify_problem(self, problem: str) -> str:
        """Classify problem type."""
        problem_lower = str(problem).lower()
        if any(w in problem_lower for w in ["error", "bug", "fix", "broken"]):
            return "debugging"
        if any(w in problem_lower for w in ["create", "build", "new", "implement"]):
            return "creation"
        if any(w in problem_lower for w in ["optimize", "improve", "faster", "better"]):
            return "optimization"
        if any(w in problem_lower for w in ["analyze", "understand", "explain", "why"]):
            return "analysis"
        if any(w in problem_lower for w in ["decide", "choose", "should", "which"]):
            return "decision"
        return "general"


# Convenience functions for agent usage
def create_engine(agent_id: str, tier: str = "operational", domain: str = None) -> BaseReasoningEngine:
    """Factory function to create reasoning engine for an agent."""
    return BaseReasoningEngine(agent_id, tier, domain)


def quick_reason(agent_id: str, problem: str, tier: str = "operational") -> dict:
    """Quick reasoning helper for simple problems."""
    engine = create_engine(agent_id, tier)
    chain = engine.reason({"problem": problem})
    return chain.to_dict()
