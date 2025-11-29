#!/usr/bin/env python3
"""
Advanced Language Processing System

A comprehensive language intelligence framework that provides:
- Multi-language understanding and generation
- Pragmatic analysis (intent, context, implicature)
- Discourse coherence and structure
- Register and style adaptation
- Semantic frame extraction
- Cross-lingual transfer capabilities

This goes beyond simple NLP to model true language understanding:
1. Pragmatics: What is really being communicated?
2. Discourse: How do utterances relate to each other?
3. Register: What style is appropriate for this context?
4. Semantics: What are the deep meaning structures?

Architecture:
                    ┌─────────────────────┐
                    │    Input Text       │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Linguistic Analysis │
                    ├─────────────────────┤
                    │ • Lexical           │
                    │ • Syntactic         │
                    │ • Semantic          │
                    │ • Pragmatic         │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼─────┐       ┌──────▼──────┐      ┌─────▼─────┐
    │ Intent    │       │ Discourse   │      │ Register  │
    │ Analysis  │       │ Structure   │      │ Detection │
    └─────┬─────┘       └──────┬──────┘      └─────┬─────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Frame Semantics     │ ← Deep meaning
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Generation Control  │ ← Style/register
                    └─────────────────────┘
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import hashlib
import re


class Language(Enum):
    """Supported languages with ISO codes."""
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    DUTCH = "nl"
    RUSSIAN = "ru"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    ARABIC = "ar"
    HINDI = "hi"
    TURKISH = "tr"
    POLISH = "pl"
    VIETNAMESE = "vi"
    THAI = "th"
    INDONESIAN = "id"
    SWEDISH = "sv"
    NORWEGIAN = "no"
    DANISH = "da"
    FINNISH = "fi"
    GREEK = "el"
    HEBREW = "he"
    CZECH = "cs"
    ROMANIAN = "ro"
    HUNGARIAN = "hu"
    UKRAINIAN = "uk"
    CATALAN = "ca"
    BASQUE = "eu"


class CommunicativeIntent(Enum):
    """Speech act / communicative intent categories."""
    # Assertives (stating)
    ASSERT = "assert"
    INFORM = "inform"
    EXPLAIN = "explain"
    DESCRIBE = "describe"
    REPORT = "report"
    CLARIFY = "clarify"

    # Directives (requesting)
    REQUEST = "request"
    COMMAND = "command"
    ASK = "ask"
    SUGGEST = "suggest"
    ADVISE = "advise"
    WARN = "warn"

    # Commissives (promising)
    PROMISE = "promise"
    OFFER = "offer"
    COMMIT = "commit"
    REFUSE = "refuse"

    # Expressives (expressing)
    THANK = "thank"
    APOLOGIZE = "apologize"
    CONGRATULATE = "congratulate"
    COMPLAIN = "complain"
    GREET = "greet"
    FAREWELL = "farewell"

    # Declaratives (declaring)
    DECLARE = "declare"
    DEFINE = "define"
    NAME = "name"

    # Meta-communicative
    CONFIRM = "confirm"
    DENY = "deny"
    AGREE = "agree"
    DISAGREE = "disagree"
    HEDGE = "hedge"


class Register(Enum):
    """Language register / formality levels."""
    FROZEN = "frozen"       # Fixed, ritualistic (legal, religious)
    FORMAL = "formal"       # Professional, academic
    CONSULTATIVE = "consultative"  # Professional but interactive
    CASUAL = "casual"       # Informal, friendly
    INTIMATE = "intimate"   # Close relationships


class DiscourseRelation(Enum):
    """Relations between discourse units (RST-inspired)."""
    # Presentational
    BACKGROUND = "background"
    ELABORATION = "elaboration"
    SUMMARY = "summary"
    RESTATEMENT = "restatement"

    # Subject matter
    CAUSE = "cause"
    RESULT = "result"
    PURPOSE = "purpose"
    CONDITION = "condition"
    CONTRAST = "contrast"
    COMPARISON = "comparison"
    CONCESSION = "concession"
    TEMPORAL = "temporal"
    SEQUENCE = "sequence"

    # Multinuclear
    CONJUNCTION = "conjunction"
    DISJUNCTION = "disjunction"
    LIST = "list"

    # Dialogue-specific
    QUESTION_ANSWER = "question_answer"
    ACKNOWLEDGMENT = "acknowledgment"
    CORRECTION = "correction"


class SemanticRole(Enum):
    """Thematic / semantic roles (simplified FrameNet)."""
    AGENT = "agent"           # Who does the action
    PATIENT = "patient"       # Who/what is affected
    THEME = "theme"           # What is moved/located
    EXPERIENCER = "experiencer"  # Who experiences
    BENEFICIARY = "beneficiary"  # Who benefits
    INSTRUMENT = "instrument"    # What is used
    LOCATION = "location"        # Where
    SOURCE = "source"            # Where from
    GOAL = "goal"                # Where to
    TIME = "time"                # When
    MANNER = "manner"            # How
    CAUSE = "cause"              # Why
    PURPOSE = "purpose"          # For what
    DEGREE = "degree"            # How much


@dataclass
class LinguisticFeatures:
    """Extracted linguistic features from text."""
    language: Language
    word_count: int
    sentence_count: int
    avg_sentence_length: float
    vocabulary_richness: float  # Type-token ratio
    formality_score: float      # -1 (informal) to +1 (formal)
    complexity_score: float     # 0 to 1
    readability_score: float    # 0 to 1 (higher = easier)
    question_count: int
    exclamation_count: int
    personal_pronouns: int
    passive_voice_ratio: float


@dataclass
class IntentAnalysis:
    """Analysis of communicative intent."""
    primary_intent: CommunicativeIntent
    secondary_intents: list[CommunicativeIntent]
    confidence: float
    illocutionary_force: float  # Strength of intent
    directness: float           # Direct vs. indirect speech act
    politeness: float           # -1 (impolite) to +1 (polite)
    urgency: float              # 0 to 1
    markers: list[str]          # Linguistic markers detected


@dataclass
class DiscourseUnit:
    """A unit of discourse with its relations."""
    unit_id: str
    text: str
    intent: CommunicativeIntent
    relations_to: dict[str, DiscourseRelation]  # unit_id -> relation
    is_nucleus: bool  # In RST, nucleus is more important
    topic: Optional[str] = None
    focus: Optional[str] = None


@dataclass
class SemanticFrame:
    """A semantic frame extracted from text."""
    frame_name: str
    trigger: str              # The word/phrase that evokes the frame
    roles: dict[SemanticRole, str]  # Role -> filler
    confidence: float
    source_text: str


@dataclass
class LanguageProfile:
    """Agent's language profile and capabilities."""
    agent_id: str
    native_languages: list[Language] = field(default_factory=lambda: [Language.ENGLISH])
    proficient_languages: list[Language] = field(default_factory=lambda: list(Language))
    preferred_register: Register = Register.CONSULTATIVE
    communication_style: str = "clear and helpful"
    vocabulary_domains: list[str] = field(default_factory=lambda: ["general"])
    personality_markers: dict[str, float] = field(default_factory=dict)
    adaptation_enabled: bool = True


class LanguageIntelligenceEngine:
    """
    Comprehensive language understanding and generation system.

    Provides:
    1. Deep linguistic analysis
    2. Intent and pragmatic understanding
    3. Discourse structure modeling
    4. Register/style detection and adaptation
    5. Semantic frame extraction
    6. Multi-language support
    """

    # Intent markers
    INTENT_MARKERS = {
        CommunicativeIntent.REQUEST: ["please", "could you", "would you", "can you", "help"],
        CommunicativeIntent.ASK: ["?", "what", "who", "where", "when", "why", "how", "which"],
        CommunicativeIntent.COMMAND: ["do", "make", "run", "execute", "create", "delete", "must"],
        CommunicativeIntent.INFORM: ["is", "are", "was", "were", "the", "this", "that"],
        CommunicativeIntent.EXPLAIN: ["because", "since", "therefore", "thus", "so", "means"],
        CommunicativeIntent.SUGGEST: ["maybe", "perhaps", "consider", "might", "should"],
        CommunicativeIntent.THANK: ["thank", "thanks", "appreciate", "grateful"],
        CommunicativeIntent.APOLOGIZE: ["sorry", "apologize", "excuse", "forgive"],
        CommunicativeIntent.GREET: ["hello", "hi", "hey", "good morning", "good afternoon"],
        CommunicativeIntent.FAREWELL: ["bye", "goodbye", "see you", "take care", "later"],
        CommunicativeIntent.AGREE: ["yes", "yeah", "agree", "correct", "right", "exactly"],
        CommunicativeIntent.DISAGREE: ["no", "disagree", "wrong", "incorrect", "but"],
        CommunicativeIntent.CONFIRM: ["confirm", "verify", "sure", "certainly", "definitely"],
        CommunicativeIntent.WARN: ["warning", "careful", "caution", "danger", "risk", "beware"],
        CommunicativeIntent.PROMISE: ["will", "promise", "guarantee", "commit", "swear"],
    }

    # Formality markers
    FORMAL_MARKERS = [
        "therefore", "however", "furthermore", "moreover", "consequently",
        "regarding", "concerning", "pursuant", "hereby", "whereas",
        "shall", "would", "could", "might", "ought",
    ]

    INFORMAL_MARKERS = [
        "gonna", "wanna", "gotta", "kinda", "sorta", "yeah", "yep", "nope",
        "hey", "cool", "awesome", "like", "stuff", "things", "ok", "okay",
        "lol", "btw", "fyi", "asap", "idk", "tbh",
    ]

    # Language detection patterns (simplified)
    LANGUAGE_PATTERNS = {
        Language.ENGLISH: r'\b(the|and|is|are|was|were|have|has|will|would)\b',
        Language.SPANISH: r'\b(el|la|los|las|es|son|está|están|que|de)\b',
        Language.FRENCH: r'\b(le|la|les|est|sont|que|de|du|des|un|une)\b',
        Language.GERMAN: r'\b(der|die|das|ist|sind|haben|werden|und|oder)\b',
        Language.ITALIAN: r'\b(il|la|lo|gli|le|è|sono|che|di|da)\b',
        Language.PORTUGUESE: r'\b(o|a|os|as|é|são|que|de|do|da)\b',
        Language.DUTCH: r'\b(de|het|een|is|zijn|van|en|in|op|te)\b',
        Language.CHINESE: r'[\u4e00-\u9fff]',
        Language.JAPANESE: r'[\u3040-\u309f\u30a0-\u30ff]',
        Language.KOREAN: r'[\uac00-\ud7af]',
        Language.ARABIC: r'[\u0600-\u06ff]',
        Language.RUSSIAN: r'[\u0400-\u04ff]',
    }

    def __init__(self, agent_id: str, profile: LanguageProfile = None):
        self.agent_id = agent_id
        self.profile = profile or LanguageProfile(
            agent_id=agent_id,
            native_languages=[Language.ENGLISH],
            proficient_languages=list(Language),
            preferred_register=Register.CONSULTATIVE,
            communication_style="clear and helpful",
            vocabulary_domains=["general"],
        )
        self.discourse_history: list[DiscourseUnit] = []
        self.frame_memory: list[SemanticFrame] = []

    def _generate_id(self) -> str:
        data = f"{self.agent_id}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def detect_language(self, text: str) -> Language:
        """Detect the language of input text."""
        text_lower = text.lower()

        # Check script-based languages first
        for lang, pattern in self.LANGUAGE_PATTERNS.items():
            if lang in [Language.CHINESE, Language.JAPANESE, Language.KOREAN,
                        Language.ARABIC, Language.RUSSIAN]:
                if re.search(pattern, text):
                    return lang

        # Check word-based patterns
        scores = {}
        for lang, pattern in self.LANGUAGE_PATTERNS.items():
            if lang not in [Language.CHINESE, Language.JAPANESE, Language.KOREAN,
                            Language.ARABIC, Language.RUSSIAN]:
                matches = len(re.findall(pattern, text_lower))
                scores[lang] = matches

        if scores:
            return max(scores, key=scores.get)

        return Language.ENGLISH  # Default

    def analyze_linguistics(self, text: str) -> LinguisticFeatures:
        """Extract linguistic features from text."""
        language = self.detect_language(text)

        # Basic counts
        words = text.split()
        word_count = len(words)

        # Sentence detection (simplified)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_count = max(1, len(sentences))

        avg_sentence_length = word_count / sentence_count

        # Vocabulary richness (type-token ratio)
        unique_words = set(w.lower() for w in words)
        vocabulary_richness = len(unique_words) / max(1, word_count)

        # Formality score
        text_lower = text.lower()
        formal_count = sum(1 for m in self.FORMAL_MARKERS if m in text_lower)
        informal_count = sum(1 for m in self.INFORMAL_MARKERS if m in text_lower)
        total_markers = formal_count + informal_count
        if total_markers > 0:
            formality_score = (formal_count - informal_count) / total_markers
        else:
            formality_score = 0.0

        # Complexity (based on word length and sentence length)
        avg_word_length = sum(len(w) for w in words) / max(1, word_count)
        complexity_score = min(1.0, (avg_word_length - 3) / 5 + (avg_sentence_length - 10) / 20)
        complexity_score = max(0.0, complexity_score)

        # Readability (inverse of complexity)
        readability_score = 1.0 - complexity_score

        # Counts
        question_count = text.count('?')
        exclamation_count = text.count('!')

        # Personal pronouns
        personal = ["i", "me", "my", "we", "us", "our", "you", "your"]
        personal_pronouns = sum(1 for w in words if w.lower() in personal)

        # Passive voice (simplified detection)
        passive_patterns = [
            r'\b(is|are|was|were|been|being)\s+\w+ed\b',
            r'\b(is|are|was|were|been|being)\s+\w+en\b',
        ]
        passive_count = sum(len(re.findall(p, text_lower)) for p in passive_patterns)
        passive_voice_ratio = passive_count / max(1, sentence_count)

        return LinguisticFeatures(
            language=language,
            word_count=word_count,
            sentence_count=sentence_count,
            avg_sentence_length=avg_sentence_length,
            vocabulary_richness=vocabulary_richness,
            formality_score=formality_score,
            complexity_score=complexity_score,
            readability_score=readability_score,
            question_count=question_count,
            exclamation_count=exclamation_count,
            personal_pronouns=personal_pronouns,
            passive_voice_ratio=passive_voice_ratio,
        )

    def analyze_intent(self, text: str, context: dict = None) -> IntentAnalysis:
        """Analyze communicative intent of text."""
        context = context or {}
        text_lower = text.lower()

        # Score each intent
        intent_scores = {}
        detected_markers = {}

        for intent, markers in self.INTENT_MARKERS.items():
            score = 0
            found_markers = []
            for marker in markers:
                if marker in text_lower:
                    score += 1
                    found_markers.append(marker)
            if score > 0:
                intent_scores[intent] = score
                detected_markers[intent] = found_markers

        # Determine primary and secondary intents
        if intent_scores:
            sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
            primary_intent = sorted_intents[0][0]
            secondary_intents = [i[0] for i in sorted_intents[1:3]]
            confidence = min(1.0, sorted_intents[0][1] / 3)
            markers = detected_markers.get(primary_intent, [])
        else:
            primary_intent = CommunicativeIntent.INFORM
            secondary_intents = []
            confidence = 0.3
            markers = []

        # Directness (questions and hedges are less direct)
        directness = 1.0
        if text.endswith('?'):
            directness -= 0.3
        hedges = ["maybe", "perhaps", "possibly", "might", "could"]
        if any(h in text_lower for h in hedges):
            directness -= 0.2

        # Politeness
        politeness = 0.0
        polite_markers = ["please", "thank", "kindly", "would you", "could you"]
        impolite_markers = ["must", "now", "immediately", "!"]
        for m in polite_markers:
            if m in text_lower:
                politeness += 0.2
        for m in impolite_markers:
            if m in text_lower:
                politeness -= 0.1
        politeness = max(-1, min(1, politeness))

        # Urgency
        urgency = 0.0
        urgent_markers = ["urgent", "asap", "immediately", "now", "quickly", "hurry", "!"]
        for m in urgent_markers:
            if m in text_lower:
                urgency += 0.2
        urgency = min(1.0, urgency)

        # Illocutionary force (how strongly the intent is expressed)
        illocutionary_force = confidence * (1 + urgency) / 2

        return IntentAnalysis(
            primary_intent=primary_intent,
            secondary_intents=secondary_intents,
            confidence=confidence,
            illocutionary_force=illocutionary_force,
            directness=directness,
            politeness=politeness,
            urgency=urgency,
            markers=markers,
        )

    def detect_register(self, text: str, features: LinguisticFeatures = None) -> Register:
        """Detect the register/formality level of text."""
        if features is None:
            features = self.analyze_linguistics(text)

        formality = features.formality_score

        if formality > 0.6:
            return Register.FORMAL
        elif formality > 0.2:
            return Register.CONSULTATIVE
        elif formality > -0.2:
            return Register.CASUAL
        else:
            return Register.INTIMATE

    def analyze_discourse(self, text: str, intent: IntentAnalysis = None) -> DiscourseUnit:
        """Analyze text as a discourse unit and relate to history."""
        if intent is None:
            intent = self.analyze_intent(text)

        unit = DiscourseUnit(
            unit_id=self._generate_id(),
            text=text,
            intent=intent.primary_intent,
            relations_to={},
            is_nucleus=True,
        )

        # Detect relations to previous units
        if self.discourse_history:
            prev = self.discourse_history[-1]

            # Detect relation type
            text_lower = text.lower()

            if text_lower.startswith(("because", "since", "as")):
                unit.relations_to[prev.unit_id] = DiscourseRelation.CAUSE
            elif text_lower.startswith(("therefore", "so", "thus", "hence")):
                unit.relations_to[prev.unit_id] = DiscourseRelation.RESULT
            elif text_lower.startswith(("but", "however", "although", "though")):
                unit.relations_to[prev.unit_id] = DiscourseRelation.CONTRAST
            elif text_lower.startswith(("also", "and", "moreover", "furthermore")):
                unit.relations_to[prev.unit_id] = DiscourseRelation.CONJUNCTION
            elif text_lower.startswith(("for example", "such as", "like")):
                unit.relations_to[prev.unit_id] = DiscourseRelation.ELABORATION
            elif prev.intent == CommunicativeIntent.ASK:
                unit.relations_to[prev.unit_id] = DiscourseRelation.QUESTION_ANSWER
            elif text_lower.startswith(("first", "then", "next", "finally")):
                unit.relations_to[prev.unit_id] = DiscourseRelation.SEQUENCE
            else:
                unit.relations_to[prev.unit_id] = DiscourseRelation.ELABORATION

        self.discourse_history.append(unit)

        # Keep history manageable
        if len(self.discourse_history) > 50:
            self.discourse_history = self.discourse_history[-50:]

        return unit

    def extract_semantic_frames(self, text: str) -> list[SemanticFrame]:
        """Extract semantic frames from text."""
        frames = []

        # Simplified frame extraction using patterns
        frame_patterns = {
            "TRANSFER": {
                "triggers": ["give", "send", "transfer", "pass", "deliver"],
                "roles": {
                    SemanticRole.AGENT: r'(\w+)\s+(?:gives?|sends?|transfers?)',
                    SemanticRole.THEME: r'(?:gives?|sends?|transfers?)\s+(\w+)',
                    SemanticRole.BENEFICIARY: r'to\s+(\w+)',
                }
            },
            "CREATION": {
                "triggers": ["create", "make", "build", "generate", "produce"],
                "roles": {
                    SemanticRole.AGENT: r'(\w+)\s+(?:creates?|makes?|builds?)',
                    SemanticRole.THEME: r'(?:creates?|makes?|builds?)\s+(\w+)',
                }
            },
            "MOTION": {
                "triggers": ["go", "move", "travel", "run", "walk"],
                "roles": {
                    SemanticRole.AGENT: r'(\w+)\s+(?:goes?|moves?|travels?)',
                    SemanticRole.GOAL: r'to\s+(\w+)',
                    SemanticRole.SOURCE: r'from\s+(\w+)',
                }
            },
            "COMMUNICATION": {
                "triggers": ["say", "tell", "ask", "explain", "describe"],
                "roles": {
                    SemanticRole.AGENT: r'(\w+)\s+(?:says?|tells?|asks?)',
                    SemanticRole.THEME: r'(?:that|about)\s+(.+?)(?:\.|$)',
                    SemanticRole.BENEFICIARY: r'(?:tells?|asks?)\s+(\w+)',
                }
            },
            "CHANGE": {
                "triggers": ["change", "modify", "update", "transform", "convert"],
                "roles": {
                    SemanticRole.AGENT: r'(\w+)\s+(?:changes?|modifies?)',
                    SemanticRole.PATIENT: r'(?:changes?|modifies?)\s+(\w+)',
                }
            },
        }

        text_lower = text.lower()

        for frame_name, frame_def in frame_patterns.items():
            for trigger in frame_def["triggers"]:
                if trigger in text_lower:
                    roles = {}
                    for role, pattern in frame_def["roles"].items():
                        match = re.search(pattern, text_lower)
                        if match:
                            roles[role] = match.group(1)

                    if roles:  # Only add if we found at least one role
                        frame = SemanticFrame(
                            frame_name=frame_name,
                            trigger=trigger,
                            roles=roles,
                            confidence=min(1.0, len(roles) / 3),
                            source_text=text,
                        )
                        frames.append(frame)
                        self.frame_memory.append(frame)
                    break  # One frame per trigger set

        return frames

    def adapt_to_register(self, text: str, target_register: Register) -> str:
        """Adapt text to a target register (simplified)."""
        current = self.detect_register(text)

        if current == target_register:
            return text

        # Simplified adaptations
        if target_register == Register.FORMAL:
            # Make more formal
            replacements = {
                "can't": "cannot",
                "won't": "will not",
                "don't": "do not",
                "gonna": "going to",
                "wanna": "want to",
                "gotta": "have to",
                "yeah": "yes",
                "nope": "no",
                "ok": "acceptable",
                "cool": "satisfactory",
            }
            for old, new in replacements.items():
                text = re.sub(rf'\b{old}\b', new, text, flags=re.IGNORECASE)

        elif target_register == Register.CASUAL:
            # Make more casual
            replacements = {
                "cannot": "can't",
                "will not": "won't",
                "do not": "don't",
                "going to": "gonna",
            }
            for old, new in replacements.items():
                text = re.sub(rf'\b{old}\b', new, text, flags=re.IGNORECASE)

        return text

    def generate_response_style(self, target_intent: CommunicativeIntent,
                                 target_register: Register) -> dict:
        """Generate style guidance for response generation."""
        style = {
            "register": target_register.value,
            "intent": target_intent.value,
            "guidelines": [],
        }

        # Intent-based guidelines
        if target_intent == CommunicativeIntent.INFORM:
            style["guidelines"].append("Use declarative sentences")
            style["guidelines"].append("Present facts clearly")
        elif target_intent == CommunicativeIntent.REQUEST:
            style["guidelines"].append("Use polite language")
            style["guidelines"].append("Be specific about what is needed")
        elif target_intent == CommunicativeIntent.EXPLAIN:
            style["guidelines"].append("Use causal connectors (because, therefore)")
            style["guidelines"].append("Break down complex ideas")
        elif target_intent == CommunicativeIntent.SUGGEST:
            style["guidelines"].append("Use hedging language (perhaps, might)")
            style["guidelines"].append("Present options not commands")

        # Register-based guidelines
        if target_register == Register.FORMAL:
            style["guidelines"].append("Avoid contractions")
            style["guidelines"].append("Use complete sentences")
            style["guidelines"].append("Avoid slang and colloquialisms")
        elif target_register == Register.CASUAL:
            style["guidelines"].append("Contractions are fine")
            style["guidelines"].append("Conversational tone")
        elif target_register == Register.CONSULTATIVE:
            style["guidelines"].append("Professional but friendly")
            style["guidelines"].append("Balance formality with warmth")

        return style

    def get_linguistic_summary(self) -> dict:
        """Get summary of linguistic processing."""
        return {
            "agent_id": self.agent_id,
            "native_languages": [l.value for l in self.profile.native_languages],
            "proficient_languages": len(self.profile.proficient_languages),
            "preferred_register": self.profile.preferred_register.value,
            "discourse_units_tracked": len(self.discourse_history),
            "semantic_frames_extracted": len(self.frame_memory),
            "vocabulary_domains": self.profile.vocabulary_domains,
        }


def create_language_engine(agent_id: str) -> LanguageIntelligenceEngine:
    """Factory for language intelligence engine."""
    return LanguageIntelligenceEngine(agent_id)
