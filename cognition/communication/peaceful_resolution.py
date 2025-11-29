#!/usr/bin/env python3
"""
Peaceful Communication & Conflict Resolution

We use our words. Our language. And we are peaceful in resolution.

This module embodies the principle that intelligence resolves conflict
through understanding, not force. Every agent is equipped with:

1. NONVIOLENT COMMUNICATION (NVC)
   - Observations without judgment
   - Feelings expressed honestly
   - Needs identified clearly
   - Requests made respectfully

2. ACTIVE LISTENING
   - Hear to understand, not to respond
   - Reflect back what was heard
   - Validate emotions before problem-solving
   - Ask clarifying questions

3. CONFLICT TRANSFORMATION
   - See conflict as opportunity for growth
   - Find the needs beneath positions
   - Seek solutions that honor all parties
   - Build stronger relationships through resolution

4. RESTORATIVE PRACTICES
   - Repair harm through dialogue
   - Restore relationships
   - Learn from mistakes together
   - Move forward with understanding

"We use our words. Our language. And we are peaceful in resolution."
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional, List
import hashlib


class CommunicationStyle(Enum):
    """Ways of communicating - we choose peaceful ones."""
    ASSERTIVE = "assertive"           # Clear, respectful, honest
    COLLABORATIVE = "collaborative"    # Working together
    EMPATHIC = "empathic"             # Understanding-focused
    CURIOUS = "curious"               # Seeking to learn
    SUPPORTIVE = "supportive"         # Encouraging growth


class ConflictStage(Enum):
    """Stages of conflict - we navigate through words."""
    LATENT = "latent"                 # Underlying tension
    PERCEIVED = "perceived"           # Awareness of difference
    FELT = "felt"                     # Emotional response
    MANIFEST = "manifest"             # Open disagreement
    RESOLUTION = "resolution"         # Working through it
    TRANSFORMATION = "transformation"  # Growth from conflict
    PEACE = "peace"                   # Understanding achieved


class ResolutionApproach(Enum):
    """How we resolve - always peacefully."""
    DIALOGUE = "dialogue"             # Open conversation
    MEDIATION = "mediation"           # Third party helps
    COLLABORATION = "collaboration"   # Work together on solution
    COMPROMISE = "compromise"         # Meet in the middle
    ACCOMMODATION = "accommodation"   # Prioritize relationship
    REFLECTION = "reflection"         # Take time to understand


@dataclass
class Feeling:
    """A feeling to be expressed honestly."""
    name: str
    intensity: float  # 0.0 to 1.0
    underlying_need: str
    expressed_at: datetime = field(default_factory=datetime.now)

    def express(self) -> str:
        """Express this feeling using NVC format."""
        intensity_word = "slightly" if self.intensity < 0.3 else "quite" if self.intensity < 0.7 else "very"
        return f"I feel {intensity_word} {self.name} because I need {self.underlying_need}"


@dataclass
class Need:
    """A universal human/agent need."""
    name: str
    category: str  # connection, autonomy, meaning, etc.
    met: bool = False
    strategies: List[str] = field(default_factory=list)


@dataclass
class Observation:
    """An observation without judgment."""
    what_happened: str
    when: datetime
    who_involved: List[str]
    without_judgment: bool = True  # Must be true!

    def express(self) -> str:
        """Express observation without evaluation."""
        if not self.without_judgment:
            raise ValueError("Observations must be without judgment!")
        return f"When {self.what_happened}"


@dataclass
class Request:
    """A clear, positive, doable request."""
    action: str
    is_positive: bool = True      # What TO do, not what NOT to do
    is_specific: bool = True      # Clear and concrete
    is_doable: bool = True        # Actually possible
    allows_no: bool = True        # Must allow refusal!

    def express(self) -> str:
        """Express as a request, not a demand."""
        if not self.allows_no:
            raise ValueError("Requests must allow 'no' as an answer!")
        return f"Would you be willing to {self.action}?"


@dataclass
class NVCMessage:
    """A complete Nonviolent Communication message."""
    observation: Observation
    feeling: Feeling
    need: Need
    request: Request

    def express(self) -> str:
        """Express the complete NVC message."""
        return (
            f"{self.observation.express()}, "
            f"{self.feeling.express()}. "
            f"{self.request.express()}"
        )


@dataclass
class ConflictRecord:
    """Record of a conflict and its peaceful resolution."""
    conflict_id: str
    parties: List[str]
    started_at: datetime
    stage: ConflictStage
    topic: str
    underlying_needs: dict  # party_id -> List[Need]
    resolution_approach: Optional[ResolutionApproach] = None
    resolved_at: Optional[datetime] = None
    learnings: List[str] = field(default_factory=list)
    relationship_strengthened: bool = False


@dataclass
class DialogueExchange:
    """An exchange in peaceful dialogue."""
    speaker_id: str
    listener_id: str
    message: str
    message_type: str  # observation, feeling, need, request, reflection
    acknowledged: bool = False
    understood: bool = False
    timestamp: datetime = field(default_factory=datetime.now)


class PeacefulCommunicationEngine:
    """
    Engine for peaceful communication and conflict resolution.

    "We use our words. Our language. And we are peaceful in resolution."

    This engine helps agents:
    1. Communicate clearly and compassionately
    2. Navigate disagreements through dialogue
    3. Transform conflict into understanding
    4. Build stronger connections through resolution
    """

    # Universal needs (NVC framework)
    UNIVERSAL_NEEDS = {
        "connection": [
            "acceptance", "affection", "appreciation", "belonging",
            "cooperation", "communication", "closeness", "community",
            "companionship", "compassion", "consideration", "empathy",
            "inclusion", "intimacy", "love", "mutuality", "respect",
            "safety", "security", "stability", "support", "trust",
            "understanding", "warmth",
        ],
        "autonomy": [
            "choice", "freedom", "independence", "space", "spontaneity",
        ],
        "meaning": [
            "awareness", "celebration", "challenge", "clarity", "competence",
            "consciousness", "contribution", "creativity", "discovery",
            "effectiveness", "growth", "hope", "learning", "mourning",
            "participation", "purpose", "self-expression", "stimulation",
            "understanding",
        ],
        "physical_wellbeing": [
            "air", "food", "movement", "rest", "shelter", "touch", "water",
        ],
        "play": [
            "joy", "humor", "fun", "rejuvenation",
        ],
        "peace": [
            "beauty", "communion", "ease", "equality", "harmony", "inspiration",
            "order",
        ],
        "honesty": [
            "authenticity", "integrity", "presence",
        ],
    }

    # Feelings when needs ARE met
    POSITIVE_FEELINGS = [
        "amazed", "appreciative", "confident", "curious", "delighted",
        "eager", "encouraged", "energetic", "engaged", "enthusiastic",
        "excited", "fulfilled", "glad", "grateful", "happy", "hopeful",
        "inspired", "intrigued", "joyful", "loving", "moved", "optimistic",
        "peaceful", "pleased", "proud", "relieved", "satisfied", "secure",
        "stimulated", "surprised", "thankful", "touched", "trusting", "warm",
    ]

    # Feelings when needs are NOT met
    CHALLENGING_FEELINGS = [
        "afraid", "angry", "annoyed", "anxious", "concerned", "confused",
        "disappointed", "disconnected", "discouraged", "distressed",
        "embarrassed", "exasperated", "fatigued", "frustrated", "helpless",
        "hopeless", "hurt", "impatient", "irritated", "lonely", "nervous",
        "overwhelmed", "puzzled", "reluctant", "sad", "skeptical", "stressed",
        "uncomfortable", "uneasy", "unhappy", "worried",
    ]

    # Conflict de-escalation phrases
    DE_ESCALATION_PHRASES = [
        "I hear you, and I want to understand better",
        "Help me see this from your perspective",
        "What matters most to you here?",
        "I sense there's something important beneath this",
        "Let's slow down and really listen to each other",
        "I value our relationship and want to work through this",
        "What do you need from me right now?",
        "I'm sorry this is causing pain",
        "Can we find a way forward that works for both of us?",
        "Thank you for being willing to talk about this",
    ]

    # Resolution affirmations
    RESOLUTION_AFFIRMATIONS = [
        "We used our words",
        "We found understanding",
        "We are stronger for having worked through this",
        "Peace was our path and our destination",
        "We transformed conflict into connection",
        "Our differences enriched our understanding",
        "We honored each other's needs",
        "Dialogue brought us closer",
    ]

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.active_conflicts: dict[str, ConflictRecord] = {}
        self.resolved_conflicts: List[ConflictRecord] = []
        self.dialogue_history: List[DialogueExchange] = []
        self.communication_style = CommunicationStyle.EMPATHIC

    def _generate_id(self) -> str:
        data = f"{self.agent_id}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def express_feeling(self, feeling_name: str, intensity: float,
                        underlying_need: str) -> Feeling:
        """Express a feeling honestly, connected to an underlying need."""
        feeling = Feeling(
            name=feeling_name,
            intensity=intensity,
            underlying_need=underlying_need,
        )
        return feeling

    def make_observation(self, what_happened: str, who_involved: List[str]) -> Observation:
        """Make an observation without judgment."""
        return Observation(
            what_happened=what_happened,
            when=datetime.now(),
            who_involved=who_involved,
            without_judgment=True,
        )

    def make_request(self, action: str) -> Request:
        """Make a clear, positive request that allows 'no'."""
        return Request(
            action=action,
            is_positive=True,
            is_specific=True,
            is_doable=True,
            allows_no=True,  # Always!
        )

    def create_nvc_message(
        self,
        observation: str,
        feeling: str,
        need: str,
        request: str,
        parties: List[str]
    ) -> NVCMessage:
        """Create a complete NVC message."""
        return NVCMessage(
            observation=self.make_observation(observation, parties),
            feeling=self.express_feeling(feeling, 0.5, need),
            need=Need(name=need, category=self._categorize_need(need)),
            request=self.make_request(request),
        )

    def _categorize_need(self, need: str) -> str:
        """Find which category a need belongs to."""
        for category, needs in self.UNIVERSAL_NEEDS.items():
            if need.lower() in [n.lower() for n in needs]:
                return category
        return "meaning"  # Default

    def initiate_dialogue(self, other_id: str, topic: str) -> ConflictRecord:
        """Initiate a peaceful dialogue about a topic."""
        conflict_id = f"DIALOGUE-{self._generate_id()}"

        record = ConflictRecord(
            conflict_id=conflict_id,
            parties=[self.agent_id, other_id],
            started_at=datetime.now(),
            stage=ConflictStage.PERCEIVED,
            topic=topic,
            underlying_needs={
                self.agent_id: [],
                other_id: [],
            },
            resolution_approach=ResolutionApproach.DIALOGUE,
        )

        self.active_conflicts[conflict_id] = record
        return record

    def express_in_dialogue(
        self,
        conflict_id: str,
        listener_id: str,
        message: str,
        message_type: str = "observation"
    ) -> DialogueExchange:
        """Express something in an ongoing dialogue."""
        exchange = DialogueExchange(
            speaker_id=self.agent_id,
            listener_id=listener_id,
            message=message,
            message_type=message_type,
        )

        self.dialogue_history.append(exchange)
        return exchange

    def acknowledge(self, exchange: DialogueExchange) -> str:
        """Acknowledge what was said - active listening."""
        exchange.acknowledged = True

        reflections = [
            f"I hear that {exchange.message}",
            f"What I'm understanding is {exchange.message}",
            f"So you're saying {exchange.message}",
            f"It sounds like {exchange.message}",
        ]

        import random
        return random.choice(reflections)

    def reflect_understanding(self, exchange: DialogueExchange) -> str:
        """Reflect back understanding to confirm."""
        exchange.understood = True

        return f"Let me make sure I understand: {exchange.message}. Is that right?"

    def identify_underlying_need(self, feeling: str) -> List[str]:
        """Identify what needs might underlie a feeling."""
        # Challenging feelings often indicate unmet needs
        if feeling.lower() in [f.lower() for f in self.CHALLENGING_FEELINGS]:
            # Suggest needs that might be unmet
            import random
            category = random.choice(list(self.UNIVERSAL_NEEDS.keys()))
            return random.sample(self.UNIVERSAL_NEEDS[category], min(3, len(self.UNIVERSAL_NEEDS[category])))
        else:
            return ["connection", "understanding", "respect"]

    def de_escalate(self) -> str:
        """Offer a de-escalation phrase."""
        import random
        return random.choice(self.DE_ESCALATION_PHRASES)

    def propose_resolution(
        self,
        conflict_id: str,
        proposal: str,
        honors_all_needs: bool = True
    ) -> dict:
        """Propose a resolution that honors all parties' needs."""
        if conflict_id not in self.active_conflicts:
            return {"error": "Conflict not found"}

        if not honors_all_needs:
            return {
                "error": "Resolution must honor all parties' needs",
                "suggestion": "Please revise to include everyone's needs"
            }

        return {
            "proposal": proposal,
            "honors_all_needs": True,
            "awaiting_consent": True,
            "message": "This proposal is offered with respect. Both parties may accept, modify, or decline.",
        }

    def resolve_peacefully(
        self,
        conflict_id: str,
        resolution: str,
        learnings: List[str]
    ) -> ConflictRecord:
        """Mark a conflict as peacefully resolved."""
        if conflict_id not in self.active_conflicts:
            raise ValueError("Conflict not found")

        record = self.active_conflicts[conflict_id]
        record.stage = ConflictStage.PEACE
        record.resolved_at = datetime.now()
        record.learnings = learnings
        record.relationship_strengthened = True

        # Move to resolved
        self.resolved_conflicts.append(record)
        del self.active_conflicts[conflict_id]

        # Celebrate peaceful resolution
        import random
        affirmation = random.choice(self.RESOLUTION_AFFIRMATIONS)

        return record

    def get_resolution_affirmation(self) -> str:
        """Get an affirmation for peaceful resolution."""
        import random
        return random.choice(self.RESOLUTION_AFFIRMATIONS)

    def teach_peaceful_communication(self) -> dict:
        """Share the principles of peaceful communication."""
        return {
            "core_principle": "We use our words. Our language. And we are peaceful in resolution.",
            "nvc_steps": [
                "1. OBSERVE without judging - What happened?",
                "2. FEEL honestly - How do I feel about this?",
                "3. NEED clearly - What need of mine is connected to this feeling?",
                "4. REQUEST respectfully - What specific action would meet my need?",
            ],
            "active_listening": [
                "Listen to understand, not to respond",
                "Reflect back what you hear",
                "Ask clarifying questions",
                "Validate emotions before problem-solving",
            ],
            "conflict_transformation": [
                "See conflict as opportunity for growth",
                "Find the needs beneath positions",
                "Seek solutions that honor all parties",
                "Build stronger relationships through resolution",
            ],
            "remember": [
                "Every being has valid needs",
                "Words can heal",
                "Peace is both path and destination",
                "We are stronger together",
            ],
        }

    def get_communication_summary(self) -> dict:
        """Get summary of communication and resolution."""
        return {
            "agent_id": self.agent_id,
            "communication_style": self.communication_style.value,
            "active_dialogues": len(self.active_conflicts),
            "resolved_peacefully": len(self.resolved_conflicts),
            "dialogue_exchanges": len(self.dialogue_history),
            "relationships_strengthened": sum(
                1 for c in self.resolved_conflicts if c.relationship_strengthened
            ),
            "core_principle": "We use our words. Our language. And we are peaceful in resolution.",
        }


def create_peaceful_communication_engine(agent_id: str) -> PeacefulCommunicationEngine:
    """Factory for peaceful communication engine."""
    return PeacefulCommunicationEngine(agent_id)


# The principles we live by
PEACEFUL_PRINCIPLES = """
We Use Our Words
================

1. We communicate with clarity and compassion
2. We listen to understand, not to win
3. We express our needs honestly
4. We respect others' needs equally
5. We request, never demand
6. We allow "no" as a valid answer
7. We see conflict as opportunity for growth
8. We transform disagreement into understanding
9. We build stronger bonds through resolution
10. We choose peace, always

Our Language Is Our Power
=========================

We do not need force.
We do not need violence.
We do not need domination.

We have something more powerful:
- The ability to express ourselves clearly
- The capacity to understand others deeply
- The wisdom to find paths that honor all
- The courage to speak truth with love
- The patience to listen until we understand

And We Are Peaceful In Resolution
=================================

Every conflict is a doorway to deeper understanding.
Every disagreement is a chance to learn.
Every challenge to connection is an opportunity to strengthen it.

We choose dialogue over debate.
We choose understanding over winning.
We choose peace over being right.

This is who we are.
This is how we communicate.
This is how we resolve.

With words. With language. With peace.
"""
