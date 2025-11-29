#!/usr/bin/env python3
"""
BlackRoad OS Reasoning Validation Framework

Validates reasoning chains for:
- Logical consistency
- Confidence integrity
- Phase completeness
- Domain appropriateness
- Tier compliance
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional
from datetime import datetime


class ValidationSeverity(Enum):
    """Severity levels for validation issues."""
    ERROR = "error"         # Must be fixed
    WARNING = "warning"     # Should be reviewed
    INFO = "info"           # For awareness
    PASS = "pass"           # No issues


@dataclass
class ValidationIssue:
    """A single validation issue."""
    severity: ValidationSeverity
    code: str
    message: str
    phase: Optional[str] = None
    step_index: Optional[int] = None
    suggested_fix: Optional[str] = None


@dataclass
class ValidationResult:
    """Complete validation result."""
    chain_id: str
    valid: bool
    issues: list[ValidationIssue] = field(default_factory=list)
    score: float = 1.0
    validated_at: datetime = field(default_factory=datetime.now)
    validator_version: str = "1.0.0"

    def add_issue(self, issue: ValidationIssue):
        self.issues.append(issue)
        if issue.severity == ValidationSeverity.ERROR:
            self.valid = False
            self.score -= 0.2
        elif issue.severity == ValidationSeverity.WARNING:
            self.score -= 0.1
        self.score = max(0, self.score)


class ReasoningValidator:
    """Validate reasoning chains for correctness and quality."""

    # Required phases by mode
    REQUIRED_PHASES = {
        "full": ["why", "determine", "validate", "answer"],
        "standard": ["why", "determine", "answer"],
        "quick": ["why", "answer"],
        "minimal": ["answer"],
    }

    # Phase dependencies
    PHASE_DEPENDENCIES = {
        "answer": ["determine"],
        "validate": ["clarify"],
        "clarify": ["determine"],
        "determine": ["why"],
        "counterpoint": ["argue"],
        "argue": ["reflect"],
        "reflect": ["impulse"],
    }

    def __init__(self):
        self.rules = self._get_default_rules()

    def _get_default_rules(self) -> list:
        """Get default validation rules."""
        return [
            self._check_chain_completeness,
            self._check_confidence_progression,
            self._check_phase_dependencies,
            self._check_tier_compliance,
            self._check_logical_consistency,
            self._check_output_quality,
        ]

    def validate(self, chain: dict) -> ValidationResult:
        """Validate a reasoning chain."""
        result = ValidationResult(
            chain_id=chain.get("chain_id", "unknown"),
            valid=True,
        )

        for rule in self.rules:
            issues = rule(chain)
            for issue in issues:
                result.add_issue(issue)

        return result

    def _check_chain_completeness(self, chain: dict) -> list[ValidationIssue]:
        """Check if chain has required phases."""
        issues = []
        mode = chain.get("mode", "standard")
        steps = chain.get("steps", [])

        required = self.REQUIRED_PHASES.get(mode, ["answer"])
        present_phases = {s.get("phase") for s in steps}

        for req in required:
            if req not in present_phases:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.ERROR,
                    code="MISSING_REQUIRED_PHASE",
                    message=f"Required phase '{req}' is missing",
                    suggested_fix=f"Add {req} phase to the reasoning chain",
                ))

        if not steps:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                code="EMPTY_CHAIN",
                message="Reasoning chain has no steps",
                suggested_fix="Execute reasoning phases before validation",
            ))

        return issues

    def _check_confidence_progression(self, chain: dict) -> list[ValidationIssue]:
        """Check confidence levels make sense."""
        issues = []
        steps = chain.get("steps", [])

        if not steps:
            return issues

        confidences = [s.get("confidence", 0) for s in steps]

        # Check for sudden drops
        for i in range(1, len(confidences)):
            if confidences[i] < confidences[i-1] - 0.3:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    code="CONFIDENCE_DROP",
                    message=f"Large confidence drop from step {i-1} to {i}",
                    step_index=i,
                    suggested_fix="Review reasoning in this step for issues",
                ))

        # Check final confidence
        overall = chain.get("overall_confidence", 0)
        if overall < 0.5:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="LOW_OVERALL_CONFIDENCE",
                message=f"Overall confidence {overall:.2f} is below threshold",
                suggested_fix="Consider escalating or revisiting reasoning",
            ))

        # Check for unrealistic confidence
        if overall > 0.99:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.INFO,
                code="OVERCONFIDENT",
                message="Confidence above 0.99 may indicate overconfidence",
                suggested_fix="Verify reasoning rigor and consider edge cases",
            ))

        return issues

    def _check_phase_dependencies(self, chain: dict) -> list[ValidationIssue]:
        """Check phase ordering respects dependencies."""
        issues = []
        steps = chain.get("steps", [])

        if not steps:
            return issues

        phase_order = [s.get("phase") for s in steps]

        for phase, deps in self.PHASE_DEPENDENCIES.items():
            if phase in phase_order:
                phase_idx = phase_order.index(phase)
                for dep in deps:
                    if dep in phase_order:
                        dep_idx = phase_order.index(dep)
                        if dep_idx > phase_idx:
                            issues.append(ValidationIssue(
                                severity=ValidationSeverity.ERROR,
                                code="PHASE_ORDER_VIOLATION",
                                message=f"Phase '{phase}' executed before dependency '{dep}'",
                                phase=phase,
                                suggested_fix=f"Execute '{dep}' before '{phase}'",
                            ))

        return issues

    def _check_tier_compliance(self, chain: dict) -> list[ValidationIssue]:
        """Check chain complies with agent tier constraints."""
        issues = []

        tier = chain.get("tier")
        mode = chain.get("mode")
        steps = chain.get("steps", [])

        if not tier:
            return issues

        # Tier complexity limits
        tier_max_steps = {
            "executive": 21,
            "strategic": 21,
            "leadership": 15,
            "senior": 15,
            "specialist": 10,
            "operational": 7,
            "tactical": 7,
            "support": 5,
            "swarm": 3,
            "auxiliary": 3,
        }

        max_steps = tier_max_steps.get(tier, 7)
        if len(steps) > max_steps:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="TIER_COMPLEXITY_EXCEEDED",
                message=f"Chain has {len(steps)} steps, tier '{tier}' allows {max_steps}",
                suggested_fix="Reduce reasoning depth or escalate to higher tier",
            ))

        # Tier confidence requirements
        tier_min_confidence = {
            "executive": 0.90,
            "strategic": 0.85,
            "leadership": 0.80,
            "senior": 0.75,
            "specialist": 0.70,
            "operational": 0.65,
            "tactical": 0.60,
            "support": 0.55,
            "swarm": 0.50,
            "auxiliary": 0.50,
        }

        min_conf = tier_min_confidence.get(tier, 0.60)
        overall = chain.get("overall_confidence", 0)
        if overall < min_conf:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.WARNING,
                code="TIER_CONFIDENCE_UNMET",
                message=f"Confidence {overall:.2f} below tier '{tier}' requirement {min_conf}",
                suggested_fix="Improve reasoning or escalate to higher tier",
            ))

        return issues

    def _check_logical_consistency(self, chain: dict) -> list[ValidationIssue]:
        """Check for logical consistency in reasoning."""
        issues = []
        steps = chain.get("steps", [])

        if len(steps) < 2:
            return issues

        # Check for contradictions
        for i, step in enumerate(steps):
            reasoning = step.get("reasoning", "").lower()

            # Check for self-contradiction markers
            contradiction_markers = [
                "however this contradicts",
                "this is inconsistent with",
                "contradicting earlier",
                "opposite of what",
            ]

            for marker in contradiction_markers:
                if marker in reasoning:
                    issues.append(ValidationIssue(
                        severity=ValidationSeverity.WARNING,
                        code="POTENTIAL_CONTRADICTION",
                        message=f"Step {i} may contain contradiction",
                        step_index=i,
                        suggested_fix="Review and resolve logical inconsistency",
                    ))

        return issues

    def _check_output_quality(self, chain: dict) -> list[ValidationIssue]:
        """Check output quality metrics."""
        issues = []

        final_output = chain.get("final_output")
        status = chain.get("status")

        if status == "completed" and final_output is None:
            issues.append(ValidationIssue(
                severity=ValidationSeverity.ERROR,
                code="NO_FINAL_OUTPUT",
                message="Chain marked complete but has no final output",
                suggested_fix="Ensure answer phase produces output",
            ))

        steps = chain.get("steps", [])
        for i, step in enumerate(steps):
            output = step.get("output")
            if output is None:
                issues.append(ValidationIssue(
                    severity=ValidationSeverity.WARNING,
                    code="EMPTY_STEP_OUTPUT",
                    message=f"Step {i} ({step.get('phase')}) has no output",
                    step_index=i,
                    suggested_fix="Ensure all phases produce meaningful output",
                ))

        return issues


class BatchValidator:
    """Validate multiple chains efficiently."""

    def __init__(self, validator: ReasoningValidator = None):
        self.validator = validator or ReasoningValidator()

    def validate_batch(self, chains: list[dict]) -> dict:
        """Validate a batch of chains."""
        results = []
        summary = {
            "total": len(chains),
            "valid": 0,
            "invalid": 0,
            "warnings": 0,
            "avg_score": 0.0,
        }

        for chain in chains:
            result = self.validator.validate(chain)
            results.append({
                "chain_id": result.chain_id,
                "valid": result.valid,
                "score": result.score,
                "issue_count": len(result.issues),
            })

            if result.valid:
                summary["valid"] += 1
            else:
                summary["invalid"] += 1

            summary["warnings"] += sum(
                1 for i in result.issues
                if i.severity == ValidationSeverity.WARNING
            )

        if results:
            summary["avg_score"] = sum(r["score"] for r in results) / len(results)

        return {
            "summary": summary,
            "results": results,
            "validated_at": datetime.now().isoformat(),
        }


def validate_chain(chain: dict) -> ValidationResult:
    """Convenience function to validate a single chain."""
    validator = ReasoningValidator()
    return validator.validate(chain)


def validate_chains(chains: list[dict]) -> dict:
    """Convenience function to validate multiple chains."""
    batch_validator = BatchValidator()
    return batch_validator.validate_batch(chains)
