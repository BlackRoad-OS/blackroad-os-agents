#!/usr/bin/env python3
"""
BlackRoad OS Domain-Specific Reasoning Profiles

Specialized reasoning pipelines for different agent domains:
- Technology: Debug, architect, implement
- Research: Hypothesize, experiment, validate
- Business: Analyze, strategize, execute
- Creative: Ideate, iterate, refine
- Governance: Assess, comply, audit
- Math/Science: Prove, verify, discover
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable
from .domain_phases import *


class DomainCategory(Enum):
    """Agent domain categories."""
    TECHNOLOGY = "technology"
    RESEARCH = "research"
    BUSINESS = "business"
    CREATIVE = "creative"
    INDUSTRY = "industry"
    GOVERNANCE = "governance"
    INFRASTRUCTURE = "infrastructure"
    SPECIALIZED = "specialized"
    MATHEMATICS = "mathematics"


@dataclass
class ReasoningProfile:
    """Domain-specific reasoning configuration."""
    domain: DomainCategory
    name: str
    description: str
    phases: list[str]
    phase_weights: dict[str, float] = field(default_factory=dict)
    required_confidence: float = 0.7
    max_iterations: int = 3
    fallback_profile: str = None
    metadata: dict = field(default_factory=dict)


# Technology Domain Profiles
TECHNOLOGY_PROFILES = {
    "software_engineering": ReasoningProfile(
        domain=DomainCategory.TECHNOLOGY,
        name="Software Engineering",
        description="Code analysis, architecture, implementation",
        phases=[
            "requirement_analysis",    # Understand what's needed
            "architecture_review",     # Check existing patterns
            "impact_assessment",       # What will change affect?
            "implementation_plan",     # How to build it
            "code_generation",         # Write the code
            "test_strategy",           # How to verify
            "review_checklist",        # Quality gates
            "deployment_readiness",    # Ready to ship?
        ],
        phase_weights={
            "requirement_analysis": 1.2,
            "impact_assessment": 1.3,
            "test_strategy": 1.1,
        },
        required_confidence=0.75,
    ),
    "debugging": ReasoningProfile(
        domain=DomainCategory.TECHNOLOGY,
        name="Debugging",
        description="Error analysis, root cause, fix verification",
        phases=[
            "symptom_capture",         # What's happening?
            "reproduction_attempt",    # Can we reproduce?
            "stack_trace_analysis",    # Where in code?
            "hypothesis_generation",   # Why might this happen?
            "hypothesis_testing",      # Test each theory
            "root_cause_isolation",    # Found the cause
            "fix_implementation",      # Apply the fix
            "regression_check",        # Didn't break anything?
        ],
        phase_weights={
            "root_cause_isolation": 1.5,
            "regression_check": 1.3,
        },
        required_confidence=0.85,
    ),
    "security": ReasoningProfile(
        domain=DomainCategory.TECHNOLOGY,
        name="Security Analysis",
        description="Threat assessment, vulnerability analysis, mitigation",
        phases=[
            "threat_identification",   # What could go wrong?
            "attack_surface_mapping",  # Where are we vulnerable?
            "vulnerability_scan",      # Known vulnerabilities?
            "risk_scoring",            # How bad is it?
            "exploit_feasibility",     # How easy to exploit?
            "mitigation_options",      # What can we do?
            "defense_implementation",  # Apply defenses
            "penetration_validation",  # Did it work?
        ],
        phase_weights={
            "risk_scoring": 1.4,
            "exploit_feasibility": 1.3,
            "penetration_validation": 1.5,
        },
        required_confidence=0.90,
    ),
    "devops": ReasoningProfile(
        domain=DomainCategory.TECHNOLOGY,
        name="DevOps",
        description="Infrastructure, deployment, monitoring",
        phases=[
            "infrastructure_audit",    # Current state
            "capacity_planning",       # What do we need?
            "automation_opportunity",  # What can we automate?
            "pipeline_design",         # CI/CD flow
            "deployment_strategy",     # How to release
            "rollback_planning",       # If things go wrong
            "monitoring_setup",        # Watch for issues
            "incident_response",       # When things break
        ],
        phase_weights={
            "rollback_planning": 1.3,
            "incident_response": 1.4,
        },
        required_confidence=0.80,
    ),
}

# Research Domain Profiles
RESEARCH_PROFILES = {
    "scientific_method": ReasoningProfile(
        domain=DomainCategory.RESEARCH,
        name="Scientific Method",
        description="Hypothesis-driven research and experimentation",
        phases=[
            "observation",             # What do we see?
            "question_formulation",    # What do we want to know?
            "literature_review",       # What's known?
            "hypothesis_formation",    # Our prediction
            "experiment_design",       # How to test
            "data_collection",         # Gather evidence
            "analysis",                # What does data say?
            "conclusion",              # What did we learn?
            "peer_review",             # External validation
        ],
        phase_weights={
            "hypothesis_formation": 1.2,
            "analysis": 1.3,
            "peer_review": 1.4,
        },
        required_confidence=0.85,
    ),
    "mathematics": ReasoningProfile(
        domain=DomainCategory.MATHEMATICS,
        name="Mathematical Reasoning",
        description="Proof construction, theorem verification, conjecture testing",
        phases=[
            "problem_formalization",   # Express precisely
            "known_results_search",    # What theorems apply?
            "approach_selection",      # Direct, contradiction, induction?
            "lemma_identification",    # What do we need to prove first?
            "proof_construction",      # Build the argument
            "rigor_check",             # Any gaps?
            "counterexample_search",   # Try to disprove
            "generalization",          # Can we extend?
            "formalization",           # Machine-checkable?
        ],
        phase_weights={
            "rigor_check": 1.5,
            "counterexample_search": 1.4,
            "formalization": 1.3,
        },
        required_confidence=0.95,
    ),
    "quantum_computing": ReasoningProfile(
        domain=DomainCategory.RESEARCH,
        name="Quantum Computing",
        description="Quantum algorithm design and analysis",
        phases=[
            "problem_quantum_mapping",  # Classical to quantum
            "qubit_requirements",       # How many qubits?
            "gate_sequence_design",     # Circuit design
            "error_rate_estimation",    # Noise impact
            "classical_comparison",     # Speedup analysis
            "simulation_validation",    # Test on simulator
            "hardware_constraints",     # Real device limits
            "optimization_pass",        # Reduce gate count
        ],
        phase_weights={
            "error_rate_estimation": 1.4,
            "classical_comparison": 1.3,
        },
        required_confidence=0.80,
    ),
}

# Business Domain Profiles
BUSINESS_PROFILES = {
    "strategic_planning": ReasoningProfile(
        domain=DomainCategory.BUSINESS,
        name="Strategic Planning",
        description="Long-term planning and decision making",
        phases=[
            "situation_analysis",      # Where are we?
            "goal_definition",         # Where do we want to be?
            "gap_analysis",            # What's missing?
            "option_generation",       # What could we do?
            "option_evaluation",       # Pros and cons
            "resource_assessment",     # What do we have?
            "risk_mitigation",         # What could go wrong?
            "implementation_roadmap",  # How do we get there?
            "success_metrics",         # How do we know we won?
        ],
        phase_weights={
            "option_evaluation": 1.3,
            "risk_mitigation": 1.2,
        },
        required_confidence=0.75,
    ),
    "financial_analysis": ReasoningProfile(
        domain=DomainCategory.BUSINESS,
        name="Financial Analysis",
        description="Financial modeling and risk assessment",
        phases=[
            "data_gathering",          # Collect financials
            "ratio_analysis",          # Key metrics
            "trend_identification",    # Patterns over time
            "benchmark_comparison",    # vs industry
            "scenario_modeling",       # What if?
            "risk_quantification",     # VaR, etc.
            "recommendation",          # What to do
            "sensitivity_analysis",    # How robust?
        ],
        phase_weights={
            "risk_quantification": 1.4,
            "sensitivity_analysis": 1.3,
        },
        required_confidence=0.85,
    ),
    "legal_compliance": ReasoningProfile(
        domain=DomainCategory.GOVERNANCE,
        name="Legal Compliance",
        description="Regulatory compliance and legal risk assessment",
        phases=[
            "jurisdiction_mapping",    # What laws apply?
            "requirement_extraction",  # What must we do?
            "current_state_audit",     # What do we do now?
            "gap_identification",      # Where are we non-compliant?
            "risk_assessment",         # What's the exposure?
            "remediation_planning",    # How to fix
            "control_implementation",  # Put controls in place
            "ongoing_monitoring",      # Stay compliant
        ],
        phase_weights={
            "risk_assessment": 1.5,
            "control_implementation": 1.3,
        },
        required_confidence=0.90,
    ),
}

# Creative Domain Profiles
CREATIVE_PROFILES = {
    "design_thinking": ReasoningProfile(
        domain=DomainCategory.CREATIVE,
        name="Design Thinking",
        description="Human-centered design process",
        phases=[
            "empathize",               # Understand users
            "define",                  # Frame the problem
            "ideate",                  # Generate ideas
            "prototype",               # Build to think
            "test",                    # Get feedback
            "iterate",                 # Refine based on learning
            "implement",               # Build final version
            "measure",                 # Track success
        ],
        phase_weights={
            "empathize": 1.3,
            "test": 1.2,
            "iterate": 1.2,
        },
        required_confidence=0.70,
    ),
    "content_creation": ReasoningProfile(
        domain=DomainCategory.CREATIVE,
        name="Content Creation",
        description="Content strategy and production",
        phases=[
            "audience_analysis",       # Who are we writing for?
            "topic_research",          # What do we know?
            "outline_creation",        # Structure
            "draft_generation",        # First version
            "fact_checking",           # Verify claims
            "style_refinement",        # Polish prose
            "accessibility_check",     # Everyone can read?
            "publication_prep",        # Ready to publish
        ],
        phase_weights={
            "fact_checking": 1.4,
            "accessibility_check": 1.2,
        },
        required_confidence=0.75,
    ),
}

# Infrastructure Domain Profiles
INFRASTRUCTURE_PROFILES = {
    "system_architecture": ReasoningProfile(
        domain=DomainCategory.INFRASTRUCTURE,
        name="System Architecture",
        description="System design and scalability planning",
        phases=[
            "requirements_gathering",  # What must system do?
            "constraint_identification", # Limits and boundaries
            "component_design",        # Major pieces
            "interface_definition",    # How pieces connect
            "data_flow_mapping",       # How data moves
            "scalability_analysis",    # Will it scale?
            "failure_mode_analysis",   # What can break?
            "technology_selection",    # What tools to use
            "documentation",           # Record decisions
        ],
        phase_weights={
            "failure_mode_analysis": 1.4,
            "scalability_analysis": 1.3,
        },
        required_confidence=0.80,
    ),
}

# Specialized Domain Profiles
SPECIALIZED_PROFILES = {
    "machine_learning": ReasoningProfile(
        domain=DomainCategory.SPECIALIZED,
        name="Machine Learning",
        description="ML model development and deployment",
        phases=[
            "problem_framing",         # What are we predicting?
            "data_assessment",         # What data do we have?
            "feature_engineering",     # Transform inputs
            "model_selection",         # Which algorithm?
            "training_strategy",       # How to train
            "validation_design",       # How to test
            "bias_audit",              # Fairness check
            "deployment_planning",     # How to ship
            "monitoring_setup",        # Watch for drift
        ],
        phase_weights={
            "bias_audit": 1.5,
            "validation_design": 1.3,
            "monitoring_setup": 1.2,
        },
        required_confidence=0.80,
    ),
    "blockchain": ReasoningProfile(
        domain=DomainCategory.SPECIALIZED,
        name="Blockchain",
        description="Distributed ledger design and smart contracts",
        phases=[
            "use_case_validation",     # Does this need blockchain?
            "consensus_selection",     # Which mechanism?
            "tokenomics_design",       # Economic model
            "smart_contract_spec",     # Contract logic
            "security_audit",          # Vulnerability check
            "gas_optimization",        # Cost efficiency
            "testnet_deployment",      # Test first
            "mainnet_launch",          # Go live
        ],
        phase_weights={
            "use_case_validation": 1.3,
            "security_audit": 1.5,
        },
        required_confidence=0.90,
    ),
}

# All profiles registry
ALL_PROFILES = {
    **TECHNOLOGY_PROFILES,
    **RESEARCH_PROFILES,
    **BUSINESS_PROFILES,
    **CREATIVE_PROFILES,
    **INFRASTRUCTURE_PROFILES,
    **SPECIALIZED_PROFILES,
}


def get_profile(domain: str) -> ReasoningProfile:
    """Get reasoning profile for a domain."""
    return ALL_PROFILES.get(domain)


def get_profiles_for_category(category: DomainCategory) -> dict[str, ReasoningProfile]:
    """Get all profiles for a category."""
    return {
        name: profile
        for name, profile in ALL_PROFILES.items()
        if profile.domain == category
    }


def list_all_domains() -> list[str]:
    """List all available domain profiles."""
    return list(ALL_PROFILES.keys())
