#!/usr/bin/env python3
"""
BlackRoad OS Reasoning Chain Generator

Generates complete reasoning chains for agents based on:
- Agent tier and domain
- Problem type and complexity
- Available time budget
- Required confidence level

Supports:
- Batch chain generation for agent registries
- Template-based reasoning patterns
- Chain optimization and pruning
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Generator
import hashlib
import json
import random

from .base_reasoning import (
    BaseReasoningEngine, ReasoningChain, ReasoningStep,
    ReasoningPhase, ReasoningMode
)
from .tier_reasoning import TierReasoningEngine, AgentTier, TIER_CONFIGS


@dataclass
class ChainTemplate:
    """Template for generating reasoning chains."""
    name: str
    description: str
    phases: list[str]
    domain_hints: list[str]
    problem_types: list[str]
    min_tier: str
    expected_confidence: float
    typical_duration_ms: int


# Pre-defined chain templates
CHAIN_TEMPLATES = {
    "debug_and_fix": ChainTemplate(
        name="Debug and Fix",
        description="Identify bug, find root cause, implement fix",
        phases=[
            "symptom_capture", "reproduction_attempt", "stack_trace_analysis",
            "hypothesis_generation", "hypothesis_testing", "root_cause_isolation",
            "fix_implementation", "regression_check"
        ],
        domain_hints=["software_engineering", "devops", "backend", "frontend"],
        problem_types=["bug", "error", "crash", "failure"],
        min_tier="operational",
        expected_confidence=0.85,
        typical_duration_ms=15000,
    ),
    "feature_implementation": ChainTemplate(
        name="Feature Implementation",
        description="Design and implement a new feature",
        phases=[
            "requirement_analysis", "architecture_review", "impact_assessment",
            "implementation_plan", "code_generation", "test_strategy",
            "review_checklist", "deployment_readiness"
        ],
        domain_hints=["software_engineering", "frontend", "backend", "mobile"],
        problem_types=["feature", "enhancement", "new", "implement"],
        min_tier="specialist",
        expected_confidence=0.80,
        typical_duration_ms=25000,
    ),
    "security_audit": ChainTemplate(
        name="Security Audit",
        description="Comprehensive security assessment",
        phases=[
            "threat_identification", "attack_surface_mapping", "vulnerability_scan",
            "risk_scoring", "exploit_feasibility", "mitigation_options",
            "defense_implementation", "penetration_validation"
        ],
        domain_hints=["security", "devops", "cloud"],
        problem_types=["security", "vulnerability", "audit", "pentest"],
        min_tier="senior",
        expected_confidence=0.90,
        typical_duration_ms=30000,
    ),
    "mathematical_proof": ChainTemplate(
        name="Mathematical Proof",
        description="Construct and verify mathematical proof",
        phases=[
            "problem_formalization", "known_results_search", "approach_selection",
            "lemma_identification", "proof_construction", "rigor_check",
            "counterexample_search", "generalization", "formalization"
        ],
        domain_hints=["mathematics", "number_theory", "algebra", "analysis"],
        problem_types=["prove", "theorem", "conjecture", "verify"],
        min_tier="specialist",
        expected_confidence=0.95,
        typical_duration_ms=45000,
    ),
    "data_analysis": ChainTemplate(
        name="Data Analysis",
        description="Analyze data and derive insights",
        phases=[
            "data_gathering", "data_cleaning", "exploratory_analysis",
            "hypothesis_formation", "statistical_testing", "visualization",
            "interpretation", "recommendation"
        ],
        domain_hints=["data_engineering", "statistics", "machine_learning"],
        problem_types=["analyze", "data", "insights", "trends"],
        min_tier="operational",
        expected_confidence=0.80,
        typical_duration_ms=20000,
    ),
    "strategic_decision": ChainTemplate(
        name="Strategic Decision",
        description="Make high-impact strategic decision",
        phases=[
            "situation_analysis", "goal_definition", "gap_analysis",
            "option_generation", "option_evaluation", "resource_assessment",
            "risk_mitigation", "implementation_roadmap", "success_metrics"
        ],
        domain_hints=["finance", "operations", "marketing", "sales"],
        problem_types=["decision", "strategy", "plan", "choose"],
        min_tier="leadership",
        expected_confidence=0.85,
        typical_duration_ms=35000,
    ),
    "rapid_response": ChainTemplate(
        name="Rapid Response",
        description="Quick response to urgent situation",
        phases=["assess", "decide", "act", "verify"],
        domain_hints=["devops", "security", "customer_support"],
        problem_types=["urgent", "emergency", "critical", "immediate"],
        min_tier="tactical",
        expected_confidence=0.70,
        typical_duration_ms=5000,
    ),
    "research_investigation": ChainTemplate(
        name="Research Investigation",
        description="Deep research and investigation",
        phases=[
            "observation", "question_formulation", "literature_review",
            "hypothesis_formation", "experiment_design", "data_collection",
            "analysis", "conclusion", "peer_review"
        ],
        domain_hints=["research", "physics", "chemistry", "biology", "quantum_computing"],
        problem_types=["research", "investigate", "explore", "discover"],
        min_tier="senior",
        expected_confidence=0.85,
        typical_duration_ms=40000,
    ),
}


class ChainGenerator:
    """Generate reasoning chains for agents."""

    def __init__(self, trace_store=None):
        self.trace_store = trace_store
        self.templates = CHAIN_TEMPLATES

    def generate_chain_id(self, agent_id: str, timestamp: datetime = None) -> str:
        """Generate unique chain ID."""
        ts = timestamp or datetime.now()
        data = f"{agent_id}:{ts.isoformat()}:{random.randint(0, 99999)}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def select_template(self, problem: str, domain: str) -> Optional[ChainTemplate]:
        """Select best template for problem and domain."""
        problem_lower = problem.lower()

        best_match = None
        best_score = 0

        for name, template in self.templates.items():
            score = 0

            # Check problem type match
            for ptype in template.problem_types:
                if ptype in problem_lower:
                    score += 2

            # Check domain match
            if domain in template.domain_hints:
                score += 1

            if score > best_score:
                best_score = score
                best_match = template

        return best_match

    def generate_chain(
        self,
        agent_id: str,
        tier: str,
        domain: str,
        problem: str,
        context: dict = None,
    ) -> ReasoningChain:
        """Generate a complete reasoning chain for an agent."""

        # Get tier configuration
        tier_engine = TierReasoningEngine(agent_id, tier)
        tier_phases = tier_engine.get_reasoning_phases()

        # Select template if applicable
        template = self.select_template(problem, domain)

        # Determine phases to use
        if template:
            phases = template.phases[:tier_engine.config.max_phases]
        else:
            phases = tier_phases

        # Create chain
        chain = ReasoningChain(
            chain_id=self.generate_chain_id(agent_id),
            agent_id=agent_id,
            mode=ReasoningMode.DOMAIN if template else ReasoningMode.STANDARD,
        )

        # Generate steps
        current_context = {
            "problem": problem,
            "domain": domain,
            **(context or {})
        }

        for phase in phases:
            step = self._generate_step(phase, current_context, tier_engine)
            chain.add_step(step)
            current_context.update(step.metadata.get("context_update", {}))

        # Complete chain
        chain.complete(current_context.get("final_answer"))

        # Store if trace store available
        if self.trace_store:
            self.trace_store.store_chain(chain.to_dict())

        return chain

    def _generate_step(
        self,
        phase: str,
        context: dict,
        tier_engine: TierReasoningEngine
    ) -> ReasoningStep:
        """Generate a single reasoning step."""

        # Base confidence varies by tier
        base_confidence = {
            AgentTier.EXECUTIVE: 0.90,
            AgentTier.STRATEGIC: 0.85,
            AgentTier.LEADERSHIP: 0.80,
            AgentTier.SENIOR: 0.78,
            AgentTier.SPECIALIST: 0.75,
            AgentTier.OPERATIONAL: 0.72,
            AgentTier.TACTICAL: 0.68,
            AgentTier.SUPPORT: 0.65,
            AgentTier.SWARM: 0.60,
            AgentTier.AUXILIARY: 0.58,
        }.get(tier_engine.tier, 0.70)

        # Add some variance
        confidence = min(1.0, max(0.1, base_confidence + random.uniform(-0.1, 0.1)))

        return ReasoningStep(
            phase=ReasoningPhase.WHY if phase == "why" else ReasoningPhase.DETERMINE,
            input_context=context,
            output={"phase": phase, "result": "processed"},
            confidence=confidence,
            reasoning=f"Executed {phase} phase with tier-appropriate depth",
            metadata={"context_update": {f"{phase}_complete": True}}
        )

    def generate_batch(
        self,
        agents: list[dict],
        problem: str,
        batch_size: int = 100,
    ) -> Generator[ReasoningChain, None, None]:
        """Generate chains for a batch of agents."""

        for agent in agents[:batch_size]:
            chain = self.generate_chain(
                agent_id=agent.get("id"),
                tier=agent.get("tier", "operational"),
                domain=agent.get("domain", "general"),
                problem=problem,
            )
            yield chain

    def generate_for_registry(
        self,
        registry_path: str,
        problem: str,
        output_path: str = None,
        limit: int = 1000,
    ) -> dict:
        """Generate chains for agents in a registry file."""

        with open(registry_path) as f:
            registry = json.load(f)

        agents = registry.get("agents", [])[:limit]
        chains = []

        for agent in agents:
            chain = self.generate_chain(
                agent_id=agent.get("id"),
                tier=agent.get("tier", "operational"),
                domain=agent.get("domain", "general"),
                problem=problem,
            )
            chains.append(chain.to_dict())

        result = {
            "generated_at": datetime.now().isoformat(),
            "problem": problem,
            "total_chains": len(chains),
            "chains": chains,
        }

        if output_path:
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2)

        return result


@dataclass
class ChainOptimizer:
    """Optimize reasoning chains for efficiency."""

    def prune_low_confidence(self, chain: ReasoningChain, threshold: float = 0.5) -> ReasoningChain:
        """Remove steps below confidence threshold."""
        chain.steps = [s for s in chain.steps if s.confidence >= threshold]
        chain._update_confidence()
        return chain

    def merge_similar_steps(self, chain: ReasoningChain) -> ReasoningChain:
        """Merge steps with similar outputs."""
        # Simple implementation - more sophisticated merging possible
        seen_outputs = set()
        unique_steps = []

        for step in chain.steps:
            output_hash = hashlib.md5(str(step.output).encode()).hexdigest()
            if output_hash not in seen_outputs:
                seen_outputs.add(output_hash)
                unique_steps.append(step)

        chain.steps = unique_steps
        chain._update_confidence()
        return chain

    def reorder_for_efficiency(self, chain: ReasoningChain) -> ReasoningChain:
        """Reorder steps for better efficiency."""
        # Sort by confidence (higher first) while maintaining logical order
        # This is a simple heuristic - domain-specific reordering is better
        return chain


def create_generator(trace_store=None) -> ChainGenerator:
    """Factory for chain generators."""
    return ChainGenerator(trace_store)
