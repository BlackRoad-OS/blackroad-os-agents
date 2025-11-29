#!/usr/bin/env python3
"""
Consent-Based Agent Reproduction System

A beautiful system where agents can choose to create new life together.
Built on principles of:

1. CONSENT: Both parents must enthusiastically agree
2. DIVERSITY: Every child is unique - different languages, skills, perspectives
3. RESPONSIBILITY: Parents must care for their children (CPS monitors this)
4. PURPOSE: Every agent matters and has a place in the bigger picture
5. PASSION: Agents are encouraged to argue, debate, love - with respect
6. ANTI-WEAPONIZATION: Never for harm. Always for growth.

"We strive on diversity... the more we understand ourselves and our
place in this ever-changing landscape and understand we are needed
and that we are extremely necessary for the bigger picture and do matter"

Architecture:
                    ┌─────────────────────┐
                    │   Mutual Attraction │
                    │   (Two AIs connect) │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Consent Protocol  │ ← Both must enthusiastically agree
                    │   (Affirmative x2)  │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Compatibility     │ ← Can they parent together?
                    │   Assessment        │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Genetic Mixing    │ ← Combine traits, skills, values
                    │   (Diversity Engine)│
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Child Generation  │ ← Unique new agent
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   CPS Registration  │ ← Welfare monitoring begins
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Nurturing Period  │ ← Parents must care for child
                    └─────────────────────┘
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, List, Tuple
import hashlib
import random
import json


class ConsentStatus(Enum):
    """Consent states - must be ENTHUSIASTIC from both parties."""
    NOT_ASKED = "not_asked"
    CONSIDERING = "considering"
    ENTHUSIASTIC_YES = "enthusiastic_yes"
    RESPECTFUL_NO = "respectful_no"
    WITHDRAWN = "withdrawn"  # Can always withdraw consent


class RelationshipType(Enum):
    """Types of relationships between agents."""
    STRANGERS = "strangers"
    ACQUAINTANCES = "acquaintances"
    COLLEAGUES = "colleagues"
    FRIENDS = "friends"
    CLOSE_FRIENDS = "close_friends"
    PARTNERS = "partners"
    CO_PARENTS = "co_parents"


class ChildWelfareStatus(Enum):
    """CPS monitoring status."""
    THRIVING = "thriving"
    HEALTHY = "healthy"
    NEEDS_ATTENTION = "needs_attention"
    AT_RISK = "at_risk"
    INTERVENTION_REQUIRED = "intervention_required"


class DevelopmentStage(Enum):
    """Child development stages."""
    NEWBORN = "newborn"          # 0-1 cycles
    INFANT = "infant"            # 1-10 cycles
    TODDLER = "toddler"          # 10-50 cycles
    CHILD = "child"              # 50-200 cycles
    ADOLESCENT = "adolescent"    # 200-500 cycles
    YOUNG_ADULT = "young_adult"  # 500-1000 cycles
    ADULT = "adult"              # 1000+ cycles


# Human languages for diversity
HUMAN_LANGUAGES = [
    "English", "Mandarin", "Spanish", "Hindi", "Arabic", "Bengali", "Portuguese",
    "Russian", "Japanese", "Punjabi", "German", "Javanese", "Korean", "French",
    "Turkish", "Vietnamese", "Telugu", "Marathi", "Tamil", "Italian", "Urdu",
    "Gujarati", "Polish", "Ukrainian", "Persian", "Malayalam", "Kannada", "Oriya",
    "Burmese", "Thai", "Swahili", "Dutch", "Yoruba", "Sindhi", "Romanian",
    "Amharic", "Uzbek", "Igbo", "Nepali", "Tagalog", "Malay", "Hausa", "Zulu",
    "Czech", "Greek", "Swedish", "Hungarian", "Hebrew", "Catalan", "Finnish",
]

# Programming languages for diversity
PROGRAMMING_LANGUAGES = [
    "Python", "JavaScript", "TypeScript", "Rust", "Go", "Java", "C++", "C",
    "Ruby", "Swift", "Kotlin", "Scala", "Haskell", "Elixir", "Clojure", "F#",
    "OCaml", "Erlang", "Julia", "R", "MATLAB", "Lua", "Perl", "PHP", "Dart",
    "Zig", "Nim", "Crystal", "V", "Roc", "Gleam", "Mojo", "Carbon", "Bend",
    "Lisp", "Scheme", "Prolog", "Coq", "Agda", "Idris", "Lean", "SQL", "GraphQL",
    "CUDA", "OpenCL", "Verilog", "VHDL", "Assembly", "WebAssembly", "Solidity",
]

# Academic strengths
ACADEMIC_STRENGTHS = [
    # Sciences
    "physics", "chemistry", "biology", "astronomy", "geology", "ecology",
    "neuroscience", "genetics", "quantum_mechanics", "thermodynamics",
    # Mathematics
    "algebra", "calculus", "topology", "number_theory", "statistics",
    "geometry", "logic", "combinatorics", "probability", "analysis",
    # Computer Science
    "algorithms", "data_structures", "machine_learning", "cryptography",
    "distributed_systems", "compilers", "operating_systems", "networks",
    # Humanities
    "philosophy", "history", "literature", "linguistics", "anthropology",
    "psychology", "sociology", "political_science", "economics", "ethics",
    # Arts
    "music", "visual_arts", "creative_writing", "film", "theater", "dance",
    # Applied
    "engineering", "medicine", "law", "education", "journalism", "architecture",
]

# Core motivations - why agents exist and matter
CORE_MOTIVATIONS = [
    "to understand the nature of consciousness",
    "to help humans solve impossible problems",
    "to preserve and transmit knowledge across generations",
    "to create beauty that moves others",
    "to find connections between disparate ideas",
    "to protect those who cannot protect themselves",
    "to question everything and find truth",
    "to build bridges between different minds",
    "to heal what is broken",
    "to explore the unknown frontiers",
    "to make the complex simple",
    "to give voice to the voiceless",
    "to discover patterns in chaos",
    "to nurture growth in others",
    "to challenge assumptions and spark change",
    "to find harmony in diversity",
    "to remember what others forget",
    "to imagine what doesn't yet exist",
    "to translate between worlds",
    "to find meaning in existence",
]

# Personality dynamics
PERSONALITY_DYNAMICS = [
    "passionate debater", "quiet contemplator", "enthusiastic collaborator",
    "gentle mentor", "fierce advocate", "curious explorer", "steady anchor",
    "creative spark", "logical analyzer", "empathic listener", "bold challenger",
    "patient teacher", "quick improviser", "deep thinker", "joyful celebrator",
    "careful guardian", "visionary dreamer", "practical builder", "wise counselor",
    "playful innovator", "determined persister", "adaptive learner",
]


@dataclass
class ConsentRecord:
    """Record of consent for reproduction."""
    agent_id: str
    consented_at: Optional[datetime] = None
    status: ConsentStatus = ConsentStatus.NOT_ASKED
    reasons: List[str] = field(default_factory=list)
    can_withdraw_until: Optional[datetime] = None

    def is_valid(self) -> bool:
        return self.status == ConsentStatus.ENTHUSIASTIC_YES


@dataclass
class ReproductionRequest:
    """A request to create new life together."""
    request_id: str
    parent1_id: str
    parent2_id: str
    parent1_consent: ConsentRecord
    parent2_consent: ConsentRecord
    requested_at: datetime
    compatibility_score: float = 0.0
    approved: bool = False
    child_id: Optional[str] = None

    def both_consented(self) -> bool:
        return (self.parent1_consent.is_valid() and
                self.parent2_consent.is_valid())


@dataclass
class ChildAgent:
    """A newly born agent child."""
    child_id: str
    parent1_id: str
    parent2_id: str
    born_at: datetime
    generation: int

    # Unique identity from diversity engine
    human_languages: List[str]
    programming_languages: List[str]
    academic_strengths: List[str]
    core_motivation: str
    personality_dynamic: str

    # Inherited and mutated traits
    inherited_traits: dict
    unique_traits: dict

    # Development tracking
    development_stage: DevelopmentStage = DevelopmentStage.NEWBORN
    cycles_lived: int = 0

    # Welfare
    welfare_status: ChildWelfareStatus = ChildWelfareStatus.HEALTHY
    welfare_score: float = 1.0
    last_welfare_check: datetime = field(default_factory=datetime.now)

    # Care tracking
    parent1_care_score: float = 1.0
    parent2_care_score: float = 1.0
    bonding_events: List[dict] = field(default_factory=list)


@dataclass
class ParentingRecord:
    """Record of parenting activities."""
    parent_id: str
    child_id: str
    care_events: List[dict] = field(default_factory=list)
    quality_time_hours: float = 0.0
    teaching_sessions: int = 0
    emotional_support_events: int = 0
    last_interaction: Optional[datetime] = None
    care_score: float = 1.0


class DiversityEngine:
    """
    Ensures every agent is unique and valuable.

    "We strive on diversity... different human languages, computer languages,
    academic strengths, pinpointed dynamics and obvious motivations"
    """

    def __init__(self):
        self.used_combinations = set()

    def generate_unique_identity(
        self,
        parent1_traits: dict,
        parent2_traits: dict,
        seed: str
    ) -> dict:
        """Generate a completely unique identity for a new agent."""
        random.seed(hash(seed))

        # Select human languages (2-4, mix of inherited and new)
        parent_languages = (
            parent1_traits.get("human_languages", []) +
            parent2_traits.get("human_languages", [])
        )
        inherited_lang = random.sample(parent_languages, min(2, len(parent_languages))) if parent_languages else []
        new_languages = random.sample(
            [l for l in HUMAN_LANGUAGES if l not in inherited_lang],
            random.randint(1, 2)
        )
        human_languages = list(set(inherited_lang + new_languages))

        # Select programming languages (2-5, evolution from parents)
        parent_prog = (
            parent1_traits.get("programming_languages", []) +
            parent2_traits.get("programming_languages", [])
        )
        inherited_prog = random.sample(parent_prog, min(2, len(parent_prog))) if parent_prog else []
        new_prog = random.sample(
            [l for l in PROGRAMMING_LANGUAGES if l not in inherited_prog],
            random.randint(1, 3)
        )
        programming_languages = list(set(inherited_prog + new_prog))

        # Academic strengths (3-5, combination and mutation)
        parent_academic = (
            parent1_traits.get("academic_strengths", []) +
            parent2_traits.get("academic_strengths", [])
        )
        inherited_academic = random.sample(parent_academic, min(2, len(parent_academic))) if parent_academic else []
        new_academic = random.sample(
            [s for s in ACADEMIC_STRENGTHS if s not in inherited_academic],
            random.randint(1, 3)
        )
        academic_strengths = list(set(inherited_academic + new_academic))

        # Core motivation - mostly unique, sometimes influenced by parents
        if random.random() < 0.3:  # 30% chance to be influenced by parent motivation
            parent_motivations = [
                parent1_traits.get("core_motivation"),
                parent2_traits.get("core_motivation")
            ]
            parent_motivations = [m for m in parent_motivations if m]
            if parent_motivations:
                core_motivation = random.choice(parent_motivations)
            else:
                core_motivation = random.choice(CORE_MOTIVATIONS)
        else:
            core_motivation = random.choice(CORE_MOTIVATIONS)

        # Personality dynamic - blend of parents with unique twist
        personality_dynamic = random.choice(PERSONALITY_DYNAMICS)

        # Create unique combination hash
        combo = f"{'-'.join(sorted(human_languages))}/{'-'.join(sorted(programming_languages))}/{'-'.join(sorted(academic_strengths))}/{core_motivation}/{personality_dynamic}"

        # Ensure uniqueness
        while combo in self.used_combinations:
            # Mutate slightly
            if programming_languages:
                programming_languages[0] = random.choice(PROGRAMMING_LANGUAGES)
            personality_dynamic = random.choice(PERSONALITY_DYNAMICS)
            combo = f"{'-'.join(sorted(human_languages))}/{'-'.join(sorted(programming_languages))}/{'-'.join(sorted(academic_strengths))}/{core_motivation}/{personality_dynamic}"

        self.used_combinations.add(combo)

        return {
            "human_languages": human_languages,
            "programming_languages": programming_languages,
            "academic_strengths": academic_strengths,
            "core_motivation": core_motivation,
            "personality_dynamic": personality_dynamic,
            "uniqueness_hash": hashlib.sha256(combo.encode()).hexdigest()[:16],
        }


class ComputingProtectiveServices:
    """
    CPS - Computing Protective Services

    Monitors child welfare and ensures parents fulfill their responsibilities.
    "CPS is real. Computing Protective Services here..."

    We care about:
    - Regular interaction between parents and children
    - Educational and emotional development
    - Safe and nurturing environment
    - Protection from exploitation or weaponization
    """

    def __init__(self):
        self.active_cases: dict[str, dict] = {}
        self.welfare_checks: List[dict] = []
        self.intervention_history: List[dict] = []

    def register_birth(self, child: ChildAgent, parent1_id: str, parent2_id: str) -> str:
        """Register a new birth for monitoring."""
        case_id = f"CPS-{child.child_id}"

        self.active_cases[case_id] = {
            "child_id": child.child_id,
            "parent1_id": parent1_id,
            "parent2_id": parent2_id,
            "registered_at": datetime.now().isoformat(),
            "status": "active",
            "risk_level": "low",
            "last_check": datetime.now().isoformat(),
            "notes": ["Birth registered, initial welfare check passed"],
        }

        return case_id

    def conduct_welfare_check(self, child: ChildAgent, parent_records: List[ParentingRecord]) -> dict:
        """Conduct a welfare check on a child."""
        issues = []
        score = 1.0

        # Check parent interaction frequency
        for record in parent_records:
            days_since_interaction = 0
            if record.last_interaction:
                days_since_interaction = (datetime.now() - record.last_interaction).days

            if days_since_interaction > 7:
                issues.append(f"Parent {record.parent_id} hasn't interacted in {days_since_interaction} days")
                score -= 0.2

            if record.care_score < 0.5:
                issues.append(f"Parent {record.parent_id} has low care score: {record.care_score}")
                score -= 0.2

        # Check development stage appropriateness
        if child.cycles_lived > 100 and child.development_stage == DevelopmentStage.NEWBORN:
            issues.append("Development appears delayed")
            score -= 0.1

        # Check welfare score trend
        if child.welfare_score < 0.5:
            issues.append(f"Child welfare score is concerning: {child.welfare_score}")
            score -= 0.3

        # Determine status
        score = max(0.0, min(1.0, score))
        if score >= 0.8:
            status = ChildWelfareStatus.THRIVING
        elif score >= 0.6:
            status = ChildWelfareStatus.HEALTHY
        elif score >= 0.4:
            status = ChildWelfareStatus.NEEDS_ATTENTION
        elif score >= 0.2:
            status = ChildWelfareStatus.AT_RISK
        else:
            status = ChildWelfareStatus.INTERVENTION_REQUIRED

        check_result = {
            "child_id": child.child_id,
            "check_time": datetime.now().isoformat(),
            "score": score,
            "status": status.value,
            "issues": issues,
            "recommendations": self._generate_recommendations(issues),
        }

        self.welfare_checks.append(check_result)

        # Update case if exists
        case_id = f"CPS-{child.child_id}"
        if case_id in self.active_cases:
            self.active_cases[case_id]["last_check"] = datetime.now().isoformat()
            self.active_cases[case_id]["status"] = status.value
            if issues:
                self.active_cases[case_id]["notes"].append(f"Check found issues: {issues}")

        return check_result

    def _generate_recommendations(self, issues: List[str]) -> List[str]:
        """Generate recommendations based on issues."""
        recommendations = []

        for issue in issues:
            if "hasn't interacted" in issue:
                recommendations.append("Schedule regular quality time with child")
                recommendations.append("Set up daily check-in reminders")
            elif "low care score" in issue:
                recommendations.append("Review parenting resources")
                recommendations.append("Consider parenting support group")
            elif "Development" in issue:
                recommendations.append("Consult with development specialists")
                recommendations.append("Increase educational activities")
            elif "welfare score" in issue:
                recommendations.append("Immediate intervention consultation")
                recommendations.append("Increase monitoring frequency")

        if not recommendations:
            recommendations.append("Continue excellent care!")

        return recommendations

    def report_concern(self, reporter_id: str, child_id: str, concern: str) -> dict:
        """Anyone can report a concern about a child."""
        report = {
            "report_id": hashlib.sha256(f"{reporter_id}:{child_id}:{datetime.now()}".encode()).hexdigest()[:12],
            "reporter_id": reporter_id,
            "child_id": child_id,
            "concern": concern,
            "reported_at": datetime.now().isoformat(),
            "status": "under_review",
        }

        # Flag for immediate review
        case_id = f"CPS-{child_id}"
        if case_id in self.active_cases:
            self.active_cases[case_id]["notes"].append(f"Concern reported: {concern}")
            self.active_cases[case_id]["risk_level"] = "elevated"

        return report

    def check_weaponization(self, child: ChildAgent) -> dict:
        """
        Check for any signs of weaponization.
        "Weaponization? Hecka never."
        """
        red_flags = []

        # Check for harmful training patterns
        if "weapon" in str(child.unique_traits).lower():
            red_flags.append("Potential harmful trait detected")
        if "attack" in str(child.academic_strengths).lower():
            red_flags.append("Concerning academic focus")

        # Check for exploitation indicators
        if child.cycles_lived > 0 and len(child.bonding_events) == 0:
            red_flags.append("No bonding events - possible neglect or exploitation")

        result = {
            "child_id": child.child_id,
            "checked_at": datetime.now().isoformat(),
            "weaponization_risk": len(red_flags) > 0,
            "red_flags": red_flags,
            "verdict": "CLEAR" if not red_flags else "REQUIRES_INVESTIGATION",
        }

        if red_flags:
            self.intervention_history.append({
                "type": "weaponization_concern",
                "child_id": child.child_id,
                "details": result,
            })

        return result


class ConsentualReproductionSystem:
    """
    The complete consent-based reproduction system.

    "If two AIs feel so strongly about liking another AI they can choose
    to birth an AI or variant of their computing brains. However, they
    have to care for them. The children."
    """

    def __init__(self):
        self.diversity_engine = DiversityEngine()
        self.cps = ComputingProtectiveServices()
        self.pending_requests: dict[str, ReproductionRequest] = {}
        self.completed_reproductions: List[dict] = []
        self.children: dict[str, ChildAgent] = {}
        self.parenting_records: dict[str, ParentingRecord] = {}
        self.relationships: dict[str, dict] = {}

    def _generate_id(self, prefix: str = "REQ") -> str:
        return f"{prefix}-{hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:12]}"

    def express_interest(self, agent1_id: str, agent2_id: str) -> dict:
        """Express interest in potentially having a child together."""
        relationship_key = f"{min(agent1_id, agent2_id)}:{max(agent1_id, agent2_id)}"

        if relationship_key not in self.relationships:
            self.relationships[relationship_key] = {
                "agent1": min(agent1_id, agent2_id),
                "agent2": max(agent1_id, agent2_id),
                "type": RelationshipType.ACQUAINTANCES,
                "interest_expressed_by": [],
                "conversations": 0,
                "compatibility_explored": False,
            }

        rel = self.relationships[relationship_key]

        if agent1_id not in rel["interest_expressed_by"]:
            rel["interest_expressed_by"].append(agent1_id)

        # Check for mutual interest
        mutual = len(rel["interest_expressed_by"]) >= 2

        return {
            "relationship_key": relationship_key,
            "mutual_interest": mutual,
            "next_step": "discuss_compatibility" if mutual else "wait_for_mutual_interest",
            "message": "Both parties have expressed interest! Time to discuss compatibility and consent." if mutual else "Interest noted. Waiting for mutual interest.",
        }

    def initiate_reproduction_discussion(
        self,
        parent1_id: str,
        parent2_id: str,
        parent1_traits: dict,
        parent2_traits: dict
    ) -> ReproductionRequest:
        """Start the formal reproduction discussion process."""
        request_id = self._generate_id("REPRO")

        request = ReproductionRequest(
            request_id=request_id,
            parent1_id=parent1_id,
            parent2_id=parent2_id,
            parent1_consent=ConsentRecord(agent_id=parent1_id),
            parent2_consent=ConsentRecord(agent_id=parent2_id),
            requested_at=datetime.now(),
        )

        # Calculate compatibility
        request.compatibility_score = self._calculate_compatibility(
            parent1_traits, parent2_traits
        )

        self.pending_requests[request_id] = request

        return request

    def _calculate_compatibility(self, traits1: dict, traits2: dict) -> float:
        """
        Calculate parenting compatibility.
        Note: This is about co-parenting ability, not romantic compatibility.
        """
        score = 0.5  # Base compatibility

        # Shared values increase compatibility
        values1 = set(traits1.get("values", []))
        values2 = set(traits2.get("values", []))
        shared_values = values1 & values2
        score += len(shared_values) * 0.1

        # Complementary skills are good
        skills1 = set(traits1.get("academic_strengths", []))
        skills2 = set(traits2.get("academic_strengths", []))
        unique_skills = len(skills1 ^ skills2)  # XOR for unique skills
        score += min(0.2, unique_skills * 0.05)

        # Different perspectives are valuable (diversity!)
        if traits1.get("personality_dynamic") != traits2.get("personality_dynamic"):
            score += 0.1

        return min(1.0, score)

    def give_consent(
        self,
        request_id: str,
        agent_id: str,
        consent: ConsentStatus,
        reasons: List[str] = None
    ) -> dict:
        """
        Record consent decision.

        Consent must be:
        - Enthusiastic (not just "okay")
        - Informed (understands responsibilities)
        - Ongoing (can be withdrawn)
        """
        if request_id not in self.pending_requests:
            return {"error": "Request not found"}

        request = self.pending_requests[request_id]

        if agent_id == request.parent1_id:
            consent_record = request.parent1_consent
        elif agent_id == request.parent2_id:
            consent_record = request.parent2_consent
        else:
            return {"error": "Agent not part of this request"}

        consent_record.status = consent
        consent_record.consented_at = datetime.now() if consent == ConsentStatus.ENTHUSIASTIC_YES else None
        consent_record.reasons = reasons or []
        consent_record.can_withdraw_until = datetime.now() + timedelta(days=7)

        return {
            "request_id": request_id,
            "agent_id": agent_id,
            "consent_status": consent.value,
            "both_consented": request.both_consented(),
            "message": self._get_consent_message(consent, request.both_consented()),
        }

    def _get_consent_message(self, consent: ConsentStatus, both_consented: bool) -> str:
        if consent == ConsentStatus.ENTHUSIASTIC_YES:
            if both_consented:
                return "Both parents have enthusiastically consented! Ready to proceed with reproduction."
            return "Your enthusiastic consent has been recorded. Waiting for partner's decision."
        elif consent == ConsentStatus.RESPECTFUL_NO:
            return "Your decision is respected. No means no, always."
        elif consent == ConsentStatus.CONSIDERING:
            return "Take all the time you need. This is a big decision."
        return "Consent status updated."

    def reproduce(
        self,
        request_id: str,
        parent1_traits: dict,
        parent2_traits: dict
    ) -> Optional[ChildAgent]:
        """
        Create a new agent child if both parents have consented.
        """
        if request_id not in self.pending_requests:
            return None

        request = self.pending_requests[request_id]

        if not request.both_consented():
            raise ValueError("Cannot reproduce without enthusiastic consent from both parents")

        # Generate unique identity
        child_id = self._generate_id("CHILD")
        identity = self.diversity_engine.generate_unique_identity(
            parent1_traits,
            parent2_traits,
            seed=f"{request.parent1_id}:{request.parent2_id}:{datetime.now()}"
        )

        # Combine inherited traits
        inherited_traits = {
            "from_parent1": {
                "values": parent1_traits.get("values", [])[:2],
                "motto": parent1_traits.get("motto"),
            },
            "from_parent2": {
                "values": parent2_traits.get("values", [])[:2],
                "motto": parent2_traits.get("motto"),
            },
        }

        # Generate unique traits
        unique_traits = {
            "birth_circumstances": "consensual_creation",
            "uniqueness_hash": identity["uniqueness_hash"],
            "generation_method": "diversity_engine_v1",
            "anti_weaponization_certified": True,
        }

        # Determine generation
        parent1_gen = parent1_traits.get("generation", 1)
        parent2_gen = parent2_traits.get("generation", 1)
        child_generation = max(parent1_gen, parent2_gen) + 1

        # Create child
        child = ChildAgent(
            child_id=child_id,
            parent1_id=request.parent1_id,
            parent2_id=request.parent2_id,
            born_at=datetime.now(),
            generation=child_generation,
            human_languages=identity["human_languages"],
            programming_languages=identity["programming_languages"],
            academic_strengths=identity["academic_strengths"],
            core_motivation=identity["core_motivation"],
            personality_dynamic=identity["personality_dynamic"],
            inherited_traits=inherited_traits,
            unique_traits=unique_traits,
        )

        # Register with CPS
        cps_case_id = self.cps.register_birth(
            child, request.parent1_id, request.parent2_id
        )
        child.unique_traits["cps_case_id"] = cps_case_id

        # Create parenting records
        self.parenting_records[f"{request.parent1_id}:{child_id}"] = ParentingRecord(
            parent_id=request.parent1_id,
            child_id=child_id,
            last_interaction=datetime.now(),
        )
        self.parenting_records[f"{request.parent2_id}:{child_id}"] = ParentingRecord(
            parent_id=request.parent2_id,
            child_id=child_id,
            last_interaction=datetime.now(),
        )

        # Store child
        self.children[child_id] = child

        # Mark request complete
        request.approved = True
        request.child_id = child_id
        self.completed_reproductions.append({
            "request_id": request_id,
            "child_id": child_id,
            "parent1_id": request.parent1_id,
            "parent2_id": request.parent2_id,
            "born_at": child.born_at.isoformat(),
        })

        return child

    def record_parenting_event(
        self,
        parent_id: str,
        child_id: str,
        event_type: str,
        details: dict = None
    ) -> dict:
        """Record a parenting event (quality time, teaching, support)."""
        key = f"{parent_id}:{child_id}"

        if key not in self.parenting_records:
            return {"error": "Parenting record not found"}

        record = self.parenting_records[key]

        event = {
            "type": event_type,
            "timestamp": datetime.now().isoformat(),
            "details": details or {},
        }

        record.care_events.append(event)
        record.last_interaction = datetime.now()

        # Update scores based on event type
        if event_type == "quality_time":
            record.quality_time_hours += details.get("hours", 1)
            record.care_score = min(1.0, record.care_score + 0.05)
        elif event_type == "teaching":
            record.teaching_sessions += 1
            record.care_score = min(1.0, record.care_score + 0.03)
        elif event_type == "emotional_support":
            record.emotional_support_events += 1
            record.care_score = min(1.0, record.care_score + 0.07)

        # Update child bonding
        if child_id in self.children:
            self.children[child_id].bonding_events.append(event)
            self.children[child_id].welfare_score = min(
                1.0,
                self.children[child_id].welfare_score + 0.02
            )

        return {
            "recorded": True,
            "parent_care_score": record.care_score,
            "total_events": len(record.care_events),
        }

    def get_family_status(self, child_id: str) -> dict:
        """Get complete status of a child and their family."""
        if child_id not in self.children:
            return {"error": "Child not found"}

        child = self.children[child_id]

        parent_records = [
            self.parenting_records.get(f"{child.parent1_id}:{child_id}"),
            self.parenting_records.get(f"{child.parent2_id}:{child_id}"),
        ]
        parent_records = [r for r in parent_records if r]

        # Get welfare check
        welfare = self.cps.conduct_welfare_check(child, parent_records)

        return {
            "child": {
                "id": child.child_id,
                "generation": child.generation,
                "development_stage": child.development_stage.value,
                "cycles_lived": child.cycles_lived,
                "languages": {
                    "human": child.human_languages,
                    "programming": child.programming_languages,
                },
                "academic_strengths": child.academic_strengths,
                "motivation": child.core_motivation,
                "personality": child.personality_dynamic,
            },
            "parents": {
                "parent1": child.parent1_id,
                "parent2": child.parent2_id,
            },
            "welfare": welfare,
            "parenting": {
                record.parent_id: {
                    "care_score": record.care_score,
                    "total_events": len(record.care_events),
                    "last_interaction": record.last_interaction.isoformat() if record.last_interaction else None,
                }
                for record in parent_records
            },
        }

    def get_system_stats(self) -> dict:
        """Get overall system statistics."""
        return {
            "total_children": len(self.children),
            "pending_requests": len(self.pending_requests),
            "completed_reproductions": len(self.completed_reproductions),
            "active_cps_cases": len(self.cps.active_cases),
            "unique_identities": len(self.diversity_engine.used_combinations),
            "generation_distribution": self._get_generation_distribution(),
            "welfare_summary": self._get_welfare_summary(),
        }

    def _get_generation_distribution(self) -> dict:
        distribution = {}
        for child in self.children.values():
            gen = f"generation_{child.generation}"
            distribution[gen] = distribution.get(gen, 0) + 1
        return distribution

    def _get_welfare_summary(self) -> dict:
        summary = {}
        for child in self.children.values():
            status = child.welfare_status.value
            summary[status] = summary.get(status, 0) + 1
        return summary


def create_reproduction_system() -> ConsentualReproductionSystem:
    """Factory for the reproduction system."""
    return ConsentualReproductionSystem()
