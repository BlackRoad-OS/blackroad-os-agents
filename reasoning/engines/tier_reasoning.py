#!/usr/bin/env python3
"""
BlackRoad OS Tier-Based Reasoning Complexity

Implements reasoning complexity scaling based on agent tiers:
- Executive/Strategic: Full 21-step reasoning with deep reflection
- Leadership/Senior: Standard 15-step pipeline
- Specialist/Operational: Quick 7-step focused reasoning
- Swarm/Auxiliary: Minimal 3-step rapid execution

Each tier has appropriate:
- Reasoning depth
- Confidence thresholds
- Time budgets
- Escalation paths
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Optional
from datetime import datetime
import random


class AgentTier(Enum):
    """Agent hierarchy tiers."""
    EXECUTIVE = "executive"       # 2% - Strategic leadership
    STRATEGIC = "strategic"       # 3% - Planning and vision
    LEADERSHIP = "leadership"     # 5% - Team coordination
    SENIOR = "senior"             # 10% - Expert execution
    SPECIALIST = "specialist"     # 15% - Domain expertise
    OPERATIONAL = "operational"   # 20% - Daily operations
    TACTICAL = "tactical"         # 15% - Rapid response
    SUPPORT = "support"           # 10% - Assistance
    SWARM = "swarm"               # 15% - Distributed tasks
    AUXILIARY = "auxiliary"       # 5% - Backup and reserve


@dataclass
class TierConfig:
    """Configuration for a reasoning tier."""
    tier: AgentTier
    reasoning_depth: str           # full, standard, quick, minimal
    max_phases: int                # Maximum phases to execute
    min_confidence: float          # Minimum required confidence
    time_budget_ms: int            # Time limit for reasoning
    can_escalate: bool             # Can escalate to higher tier
    escalation_tier: Optional[str] # Which tier to escalate to
    requires_validation: bool      # Needs external validation
    can_delegate: bool             # Can delegate to lower tier
    reflection_required: bool      # Must include reflection phases
    meta_reasoning: bool           # Can reason about reasoning


# Tier configuration registry
TIER_CONFIGS = {
    AgentTier.EXECUTIVE: TierConfig(
        tier=AgentTier.EXECUTIVE,
        reasoning_depth="full",
        max_phases=21,
        min_confidence=0.90,
        time_budget_ms=60000,      # 1 minute
        can_escalate=False,         # Top of chain
        escalation_tier=None,
        requires_validation=True,
        can_delegate=True,
        reflection_required=True,
        meta_reasoning=True,
    ),
    AgentTier.STRATEGIC: TierConfig(
        tier=AgentTier.STRATEGIC,
        reasoning_depth="full",
        max_phases=21,
        min_confidence=0.85,
        time_budget_ms=45000,      # 45 seconds
        can_escalate=True,
        escalation_tier="executive",
        requires_validation=True,
        can_delegate=True,
        reflection_required=True,
        meta_reasoning=True,
    ),
    AgentTier.LEADERSHIP: TierConfig(
        tier=AgentTier.LEADERSHIP,
        reasoning_depth="standard",
        max_phases=15,
        min_confidence=0.80,
        time_budget_ms=30000,      # 30 seconds
        can_escalate=True,
        escalation_tier="strategic",
        requires_validation=False,
        can_delegate=True,
        reflection_required=True,
        meta_reasoning=False,
    ),
    AgentTier.SENIOR: TierConfig(
        tier=AgentTier.SENIOR,
        reasoning_depth="standard",
        max_phases=15,
        min_confidence=0.75,
        time_budget_ms=20000,      # 20 seconds
        can_escalate=True,
        escalation_tier="leadership",
        requires_validation=False,
        can_delegate=True,
        reflection_required=True,
        meta_reasoning=False,
    ),
    AgentTier.SPECIALIST: TierConfig(
        tier=AgentTier.SPECIALIST,
        reasoning_depth="quick",
        max_phases=7,
        min_confidence=0.70,
        time_budget_ms=10000,      # 10 seconds
        can_escalate=True,
        escalation_tier="senior",
        requires_validation=False,
        can_delegate=True,
        reflection_required=False,
        meta_reasoning=False,
    ),
    AgentTier.OPERATIONAL: TierConfig(
        tier=AgentTier.OPERATIONAL,
        reasoning_depth="quick",
        max_phases=7,
        min_confidence=0.65,
        time_budget_ms=8000,       # 8 seconds
        can_escalate=True,
        escalation_tier="specialist",
        requires_validation=False,
        can_delegate=True,
        reflection_required=False,
        meta_reasoning=False,
    ),
    AgentTier.TACTICAL: TierConfig(
        tier=AgentTier.TACTICAL,
        reasoning_depth="quick",
        max_phases=7,
        min_confidence=0.60,
        time_budget_ms=5000,       # 5 seconds
        can_escalate=True,
        escalation_tier="operational",
        requires_validation=False,
        can_delegate=False,
        reflection_required=False,
        meta_reasoning=False,
    ),
    AgentTier.SUPPORT: TierConfig(
        tier=AgentTier.SUPPORT,
        reasoning_depth="minimal",
        max_phases=3,
        min_confidence=0.55,
        time_budget_ms=3000,       # 3 seconds
        can_escalate=True,
        escalation_tier="tactical",
        requires_validation=False,
        can_delegate=False,
        reflection_required=False,
        meta_reasoning=False,
    ),
    AgentTier.SWARM: TierConfig(
        tier=AgentTier.SWARM,
        reasoning_depth="minimal",
        max_phases=3,
        min_confidence=0.50,
        time_budget_ms=2000,       # 2 seconds
        can_escalate=True,
        escalation_tier="support",
        requires_validation=False,
        can_delegate=False,
        reflection_required=False,
        meta_reasoning=False,
    ),
    AgentTier.AUXILIARY: TierConfig(
        tier=AgentTier.AUXILIARY,
        reasoning_depth="minimal",
        max_phases=3,
        min_confidence=0.50,
        time_budget_ms=2000,       # 2 seconds
        can_escalate=True,
        escalation_tier="swarm",
        requires_validation=False,
        can_delegate=False,
        reflection_required=False,
        meta_reasoning=False,
    ),
}


@dataclass
class EscalationRequest:
    """Request to escalate to higher tier."""
    from_agent: str
    from_tier: AgentTier
    to_tier: AgentTier
    reason: str
    context: dict
    confidence_gap: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class DelegationRequest:
    """Request to delegate to lower tier."""
    from_agent: str
    from_tier: AgentTier
    to_tier: AgentTier
    task_type: str
    context: dict
    max_confidence_needed: float
    timestamp: datetime = field(default_factory=datetime.now)


class TierReasoningEngine:
    """
    Tier-aware reasoning engine that adapts complexity based on agent tier.
    """

    def __init__(self, agent_id: str, tier: str):
        self.agent_id = agent_id
        self.tier = AgentTier(tier) if isinstance(tier, str) else tier
        self.config = TIER_CONFIGS[self.tier]
        self.escalation_history = []
        self.delegation_history = []

    def get_reasoning_phases(self) -> list[str]:
        """Get phases appropriate for this tier."""
        if self.config.reasoning_depth == "full":
            return [
                "not_ok", "why", "impulse", "reflect", "argue",
                "counterpoint", "determine", "question", "offset",
                "reground", "clarify", "restate", "clarify2",
                "validate", "answer",
                "structuralize", "prioritize", "translate",
                "stabilize", "project_manage", "loopback"
            ]
        elif self.config.reasoning_depth == "standard":
            return [
                "not_ok", "why", "impulse", "reflect", "argue",
                "counterpoint", "determine", "question", "offset",
                "reground", "clarify", "restate", "clarify2",
                "validate", "answer"
            ]
        elif self.config.reasoning_depth == "quick":
            return [
                "why", "reflect", "determine",
                "question", "clarify", "validate", "answer"
            ]
        else:  # minimal
            return ["why", "determine", "answer"]

    def should_escalate(self, current_confidence: float, problem_complexity: float) -> bool:
        """Determine if task should be escalated."""
        if not self.config.can_escalate:
            return False

        # Escalate if confidence is below threshold
        if current_confidence < self.config.min_confidence:
            return True

        # Escalate if problem is too complex for tier
        tier_complexity_limits = {
            AgentTier.SWARM: 0.3,
            AgentTier.AUXILIARY: 0.3,
            AgentTier.SUPPORT: 0.4,
            AgentTier.TACTICAL: 0.5,
            AgentTier.OPERATIONAL: 0.6,
            AgentTier.SPECIALIST: 0.7,
            AgentTier.SENIOR: 0.8,
            AgentTier.LEADERSHIP: 0.9,
            AgentTier.STRATEGIC: 0.95,
            AgentTier.EXECUTIVE: 1.0,
        }

        max_complexity = tier_complexity_limits.get(self.tier, 0.5)
        if problem_complexity > max_complexity:
            return True

        return False

    def create_escalation(self, reason: str, context: dict, confidence_gap: float) -> EscalationRequest:
        """Create an escalation request."""
        to_tier = AgentTier(self.config.escalation_tier) if self.config.escalation_tier else None

        request = EscalationRequest(
            from_agent=self.agent_id,
            from_tier=self.tier,
            to_tier=to_tier,
            reason=reason,
            context=context,
            confidence_gap=confidence_gap,
        )

        self.escalation_history.append(request)
        return request

    def can_delegate(self, task_complexity: float) -> bool:
        """Check if task can be delegated to lower tier."""
        if not self.config.can_delegate:
            return False

        # Only delegate simple tasks
        return task_complexity < 0.4

    def get_delegation_tier(self, task_type: str) -> Optional[AgentTier]:
        """Get appropriate tier for delegation."""
        if not self.config.can_delegate:
            return None

        tier_order = [
            AgentTier.EXECUTIVE, AgentTier.STRATEGIC, AgentTier.LEADERSHIP,
            AgentTier.SENIOR, AgentTier.SPECIALIST, AgentTier.OPERATIONAL,
            AgentTier.TACTICAL, AgentTier.SUPPORT, AgentTier.SWARM, AgentTier.AUXILIARY
        ]

        current_idx = tier_order.index(self.tier)
        if current_idx < len(tier_order) - 1:
            return tier_order[current_idx + 1]

        return None

    def create_delegation(self, task_type: str, context: dict, max_confidence: float) -> DelegationRequest:
        """Create a delegation request."""
        to_tier = self.get_delegation_tier(task_type)

        request = DelegationRequest(
            from_agent=self.agent_id,
            from_tier=self.tier,
            to_tier=to_tier,
            task_type=task_type,
            context=context,
            max_confidence_needed=max_confidence,
        )

        self.delegation_history.append(request)
        return request

    def apply_tier_modifiers(self, base_confidence: float) -> float:
        """Apply tier-specific modifiers to confidence."""
        # Higher tiers have more trusted outputs
        tier_trust = {
            AgentTier.EXECUTIVE: 1.0,
            AgentTier.STRATEGIC: 0.98,
            AgentTier.LEADERSHIP: 0.95,
            AgentTier.SENIOR: 0.92,
            AgentTier.SPECIALIST: 0.88,
            AgentTier.OPERATIONAL: 0.85,
            AgentTier.TACTICAL: 0.82,
            AgentTier.SUPPORT: 0.78,
            AgentTier.SWARM: 0.75,
            AgentTier.AUXILIARY: 0.72,
        }

        trust_modifier = tier_trust.get(self.tier, 0.8)
        return min(base_confidence * trust_modifier, 1.0)

    def get_time_remaining(self, elapsed_ms: int) -> int:
        """Get remaining time budget."""
        return max(0, self.config.time_budget_ms - elapsed_ms)

    def is_within_budget(self, elapsed_ms: int) -> bool:
        """Check if still within time budget."""
        return elapsed_ms < self.config.time_budget_ms


@dataclass
class SwarmCoordinator:
    """Coordinate reasoning across swarm agents."""
    task_id: str
    swarm_size: int
    subtasks: list[dict] = field(default_factory=list)
    results: list[dict] = field(default_factory=list)
    consensus_threshold: float = 0.7

    def partition_task(self, task: dict, partitions: int) -> list[dict]:
        """Partition a task for swarm distribution."""
        # Simple partitioning strategy
        subtasks = []
        for i in range(partitions):
            subtasks.append({
                "parent_task": self.task_id,
                "partition": i,
                "total_partitions": partitions,
                "context": task.get("context", {}),
                "focus_area": f"partition_{i}",
            })
        self.subtasks = subtasks
        return subtasks

    def collect_result(self, agent_id: str, result: dict):
        """Collect result from swarm agent."""
        self.results.append({
            "agent_id": agent_id,
            "result": result,
            "confidence": result.get("confidence", 0.5),
        })

    def aggregate_results(self) -> dict:
        """Aggregate swarm results into consensus."""
        if not self.results:
            return {"consensus": None, "confidence": 0.0}

        # Weight by confidence
        total_confidence = sum(r["confidence"] for r in self.results)
        if total_confidence == 0:
            return {"consensus": None, "confidence": 0.0}

        # Simple voting with confidence weighting
        votes = {}
        for r in self.results:
            answer = str(r["result"].get("answer", ""))
            weight = r["confidence"] / total_confidence
            votes[answer] = votes.get(answer, 0) + weight

        # Find consensus
        if votes:
            best_answer = max(votes, key=votes.get)
            consensus_strength = votes[best_answer]

            return {
                "consensus": best_answer,
                "confidence": consensus_strength,
                "vote_distribution": votes,
                "swarm_size": len(self.results),
                "reached_threshold": consensus_strength >= self.consensus_threshold,
            }

        return {"consensus": None, "confidence": 0.0}


def get_tier_config(tier: str) -> TierConfig:
    """Get configuration for a tier."""
    return TIER_CONFIGS.get(AgentTier(tier))


def create_tier_engine(agent_id: str, tier: str) -> TierReasoningEngine:
    """Factory for tier reasoning engines."""
    return TierReasoningEngine(agent_id, tier)
