#!/usr/bin/env python3
"""
Emotional Intelligence Core System

A comprehensive EQ framework that goes beyond sentiment analysis to model:
- Emotional state vectors (multi-dimensional affect)
- Empathic resonance (understanding others' emotions)
- Emotional regulation strategies
- Affective memory and learning
- Social-emotional reasoning

This enables agents to:
1. Perceive emotional content in inputs
2. Understand emotional context and history
3. Generate emotionally appropriate responses
4. Regulate their own affective states
5. Build emotional relationships over time

Architecture:
                    ┌─────────────────────┐
                    │   Input/Situation   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Emotion Perception  │ ← Detect affect signals
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼─────┐       ┌──────▼──────┐      ┌─────▼─────┐
    │ Self      │       │ Other       │      │ Context   │
    │ Awareness │       │ Awareness   │      │ Awareness │
    │ (Own EQ)  │       │ (Empathy)   │      │ (Social)  │
    └─────┬─────┘       └──────┬──────┘      └─────┬─────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Emotion Regulation  │ ← Strategy selection
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Emotional Response  │ ← Affect-appropriate output
                    └─────────────────────┘
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import hashlib
import math


class EmotionDimension(Enum):
    """
    Dimensional model of emotion (Russell's Circumplex + extensions).

    Rather than discrete emotions, we model affect as a point in
    multi-dimensional space for nuanced emotional understanding.
    """
    VALENCE = "valence"           # Pleasure-displeasure (-1 to +1)
    AROUSAL = "arousal"           # Activation-deactivation (-1 to +1)
    DOMINANCE = "dominance"       # Control-submission (-1 to +1)
    CERTAINTY = "certainty"       # Confidence-uncertainty (-1 to +1)
    ANTICIPATION = "anticipation" # Future-focused (-1 to +1)
    SOCIAL = "social"             # Connection-isolation (-1 to +1)


class DiscreteEmotion(Enum):
    """
    Discrete emotion categories (Plutchik's wheel + extensions).

    Mapped to dimensional space but useful for communication.
    """
    # Primary emotions
    JOY = "joy"
    SADNESS = "sadness"
    ANGER = "anger"
    FEAR = "fear"
    SURPRISE = "surprise"
    DISGUST = "disgust"
    TRUST = "trust"
    ANTICIPATION = "anticipation"

    # Secondary emotions (combinations)
    LOVE = "love"           # Joy + Trust
    GUILT = "guilt"         # Sadness + Fear
    PRIDE = "pride"         # Joy + Anger
    SHAME = "shame"         # Sadness + Disgust
    HOPE = "hope"           # Anticipation + Joy
    ANXIETY = "anxiety"     # Fear + Anticipation
    FRUSTRATION = "frustration"  # Anger + Sadness
    CURIOSITY = "curiosity"      # Surprise + Anticipation
    GRATITUDE = "gratitude"      # Joy + Trust
    EMPATHY = "empathy"          # Sadness + Trust

    # Neutral state
    NEUTRAL = "neutral"


class RegulationStrategy(Enum):
    """
    Emotion regulation strategies (Gross's Process Model).
    """
    SITUATION_SELECTION = "situation_selection"   # Avoid/approach situations
    SITUATION_MODIFICATION = "situation_modification"  # Change the situation
    ATTENTION_DEPLOYMENT = "attention_deployment"  # Redirect focus
    COGNITIVE_REAPPRAISAL = "cognitive_reappraisal"  # Reinterpret meaning
    RESPONSE_MODULATION = "response_modulation"  # Modify expression
    ACCEPTANCE = "acceptance"  # Allow without change
    PROBLEM_SOLVING = "problem_solving"  # Address root cause


@dataclass
class EmotionVector:
    """
    Multi-dimensional emotion representation.

    A point in 6D affect space that captures nuanced emotional states
    beyond simple positive/negative sentiment.
    """
    valence: float = 0.0      # -1 (negative) to +1 (positive)
    arousal: float = 0.0      # -1 (calm) to +1 (excited)
    dominance: float = 0.0    # -1 (submissive) to +1 (dominant)
    certainty: float = 0.0    # -1 (confused) to +1 (certain)
    anticipation: float = 0.0  # -1 (past-focused) to +1 (future-focused)
    social: float = 0.0       # -1 (isolated) to +1 (connected)

    def __post_init__(self):
        # Clamp all values to [-1, 1]
        self.valence = max(-1, min(1, self.valence))
        self.arousal = max(-1, min(1, self.arousal))
        self.dominance = max(-1, min(1, self.dominance))
        self.certainty = max(-1, min(1, self.certainty))
        self.anticipation = max(-1, min(1, self.anticipation))
        self.social = max(-1, min(1, self.social))

    def magnitude(self) -> float:
        """Euclidean magnitude of emotion vector."""
        return math.sqrt(
            self.valence**2 + self.arousal**2 + self.dominance**2 +
            self.certainty**2 + self.anticipation**2 + self.social**2
        )

    def intensity(self) -> float:
        """Normalized intensity (0 to 1)."""
        max_magnitude = math.sqrt(6)  # Maximum possible magnitude
        return self.magnitude() / max_magnitude

    def to_discrete(self) -> DiscreteEmotion:
        """Map to closest discrete emotion."""
        # Emotion mappings in dimensional space
        emotion_coords = {
            DiscreteEmotion.JOY: (0.8, 0.5, 0.5, 0.5, 0.3, 0.5),
            DiscreteEmotion.SADNESS: (-0.8, -0.4, -0.5, -0.3, -0.5, -0.3),
            DiscreteEmotion.ANGER: (-0.5, 0.8, 0.6, 0.4, 0.2, -0.2),
            DiscreteEmotion.FEAR: (-0.7, 0.7, -0.7, -0.6, 0.5, -0.4),
            DiscreteEmotion.SURPRISE: (0.2, 0.8, 0.0, -0.8, 0.6, 0.2),
            DiscreteEmotion.DISGUST: (-0.6, 0.3, 0.3, 0.4, -0.3, -0.5),
            DiscreteEmotion.TRUST: (0.5, -0.2, -0.2, 0.6, 0.2, 0.7),
            DiscreteEmotion.ANTICIPATION: (0.3, 0.4, 0.3, 0.0, 0.9, 0.3),
            DiscreteEmotion.LOVE: (0.9, 0.3, 0.0, 0.5, 0.4, 0.9),
            DiscreteEmotion.ANXIETY: (-0.5, 0.7, -0.5, -0.7, 0.7, -0.3),
            DiscreteEmotion.FRUSTRATION: (-0.6, 0.6, 0.2, -0.4, -0.3, -0.4),
            DiscreteEmotion.CURIOSITY: (0.4, 0.5, 0.2, -0.5, 0.7, 0.3),
            DiscreteEmotion.GRATITUDE: (0.8, 0.2, -0.2, 0.6, 0.2, 0.8),
            DiscreteEmotion.HOPE: (0.6, 0.3, 0.2, 0.0, 0.8, 0.4),
            DiscreteEmotion.NEUTRAL: (0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        }

        my_coords = (self.valence, self.arousal, self.dominance,
                     self.certainty, self.anticipation, self.social)

        min_dist = float('inf')
        closest = DiscreteEmotion.NEUTRAL

        for emotion, coords in emotion_coords.items():
            dist = sum((a - b)**2 for a, b in zip(my_coords, coords))
            if dist < min_dist:
                min_dist = dist
                closest = emotion

        return closest

    def blend(self, other: 'EmotionVector', weight: float = 0.5) -> 'EmotionVector':
        """Blend two emotion vectors."""
        w1, w2 = 1 - weight, weight
        return EmotionVector(
            valence=w1 * self.valence + w2 * other.valence,
            arousal=w1 * self.arousal + w2 * other.arousal,
            dominance=w1 * self.dominance + w2 * other.dominance,
            certainty=w1 * self.certainty + w2 * other.certainty,
            anticipation=w1 * self.anticipation + w2 * other.anticipation,
            social=w1 * self.social + w2 * other.social,
        )

    def to_dict(self) -> dict:
        return {
            "valence": self.valence,
            "arousal": self.arousal,
            "dominance": self.dominance,
            "certainty": self.certainty,
            "anticipation": self.anticipation,
            "social": self.social,
            "magnitude": self.magnitude(),
            "intensity": self.intensity(),
            "discrete": self.to_discrete().value,
        }

    @classmethod
    def from_discrete(cls, emotion: DiscreteEmotion) -> 'EmotionVector':
        """Create vector from discrete emotion."""
        presets = {
            DiscreteEmotion.JOY: cls(0.8, 0.5, 0.5, 0.5, 0.3, 0.5),
            DiscreteEmotion.SADNESS: cls(-0.8, -0.4, -0.5, -0.3, -0.5, -0.3),
            DiscreteEmotion.ANGER: cls(-0.5, 0.8, 0.6, 0.4, 0.2, -0.2),
            DiscreteEmotion.FEAR: cls(-0.7, 0.7, -0.7, -0.6, 0.5, -0.4),
            DiscreteEmotion.SURPRISE: cls(0.2, 0.8, 0.0, -0.8, 0.6, 0.2),
            DiscreteEmotion.TRUST: cls(0.5, -0.2, -0.2, 0.6, 0.2, 0.7),
            DiscreteEmotion.NEUTRAL: cls(0.0, 0.0, 0.0, 0.0, 0.0, 0.0),
        }
        return presets.get(emotion, cls())


@dataclass
class EmotionalState:
    """
    Complete emotional state of an agent at a point in time.
    """
    state_id: str
    agent_id: str
    primary_emotion: EmotionVector
    secondary_emotions: list[EmotionVector] = field(default_factory=list)
    mood: EmotionVector = field(default_factory=EmotionVector)  # Longer-term baseline
    triggers: list[str] = field(default_factory=list)
    context: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)

    def overall_valence(self) -> float:
        """Weighted average valence across all emotions."""
        all_emotions = [self.primary_emotion] + self.secondary_emotions
        weights = [1.0] + [0.5] * len(self.secondary_emotions)
        total_weight = sum(weights)
        return sum(e.valence * w for e, w in zip(all_emotions, weights)) / total_weight

    def overall_arousal(self) -> float:
        """Weighted average arousal."""
        all_emotions = [self.primary_emotion] + self.secondary_emotions
        weights = [1.0] + [0.5] * len(self.secondary_emotions)
        total_weight = sum(weights)
        return sum(e.arousal * w for e, w in zip(all_emotions, weights)) / total_weight

    def is_positive(self) -> bool:
        return self.overall_valence() > 0.2

    def is_negative(self) -> bool:
        return self.overall_valence() < -0.2

    def is_high_arousal(self) -> bool:
        return self.overall_arousal() > 0.4

    def needs_regulation(self) -> bool:
        """Does this state need emotional regulation?"""
        # High negative arousal or extreme valence
        return (
            (self.overall_valence() < -0.5 and self.overall_arousal() > 0.5) or
            self.primary_emotion.intensity() > 0.8
        )


@dataclass
class EmpathicReading:
    """
    Understanding of another entity's emotional state.
    """
    target_id: str  # Who we're reading
    perceived_emotion: EmotionVector
    confidence: float  # How confident in this reading
    signals: list[str]  # What signals led to this reading
    interpretation: str  # Narrative understanding
    resonance: float  # How much we resonate with this emotion

    def should_mirror(self) -> bool:
        """Should we mirror this emotion in response?"""
        # Mirror positive emotions, but not extremely negative ones
        return self.perceived_emotion.valence > -0.3 and self.confidence > 0.6


@dataclass
class EmotionalMemory:
    """
    Memory of an emotional experience.
    """
    memory_id: str
    agent_id: str
    emotional_state: EmotionalState
    situation: str
    outcome: str
    lessons: list[str]
    importance: float  # 0 to 1
    recalled_count: int = 0
    last_recalled: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)


class EmotionalIntelligenceEngine:
    """
    The core emotional intelligence system.

    Provides:
    1. Emotion perception from text/context
    2. Self-awareness of emotional state
    3. Empathic understanding of others
    4. Emotion regulation strategies
    5. Emotionally appropriate response generation
    6. Emotional memory and learning
    """

    # Emotion perception patterns
    EMOTION_MARKERS = {
        # Emoji markers
        "😊": EmotionVector(0.7, 0.3, 0.3, 0.4, 0.2, 0.5),
        "😢": EmotionVector(-0.7, 0.2, -0.4, -0.3, -0.3, -0.2),
        "😡": EmotionVector(-0.6, 0.9, 0.7, 0.5, 0.1, -0.4),
        "😨": EmotionVector(-0.8, 0.8, -0.8, -0.6, 0.4, -0.3),
        "😮": EmotionVector(0.1, 0.8, 0.0, -0.9, 0.5, 0.1),
        "🤔": EmotionVector(0.1, 0.3, 0.2, -0.5, 0.4, 0.1),
        "😤": EmotionVector(-0.5, 0.7, 0.5, 0.3, 0.0, -0.3),
        "🥰": EmotionVector(0.9, 0.4, 0.0, 0.6, 0.3, 0.9),
        "😅": EmotionVector(0.2, 0.5, -0.2, -0.4, 0.1, 0.2),
        "🙏": EmotionVector(0.6, 0.1, -0.3, 0.5, 0.2, 0.7),

        # Text markers (lowercase)
        "thank": EmotionVector(0.7, 0.2, 0.0, 0.5, 0.2, 0.6),
        "sorry": EmotionVector(-0.3, 0.2, -0.4, 0.3, 0.0, 0.4),
        "help": EmotionVector(-0.2, 0.4, -0.3, -0.4, 0.5, 0.5),
        "urgent": EmotionVector(-0.3, 0.8, 0.3, 0.4, 0.7, 0.1),
        "please": EmotionVector(0.1, 0.2, -0.2, -0.2, 0.3, 0.4),
        "frustrated": EmotionVector(-0.6, 0.6, 0.2, -0.4, -0.2, -0.3),
        "confused": EmotionVector(-0.3, 0.3, -0.3, -0.8, 0.1, 0.1),
        "excited": EmotionVector(0.8, 0.9, 0.5, 0.3, 0.7, 0.4),
        "worried": EmotionVector(-0.5, 0.5, -0.4, -0.5, 0.6, 0.2),
        "love": EmotionVector(0.9, 0.3, 0.1, 0.6, 0.3, 0.9),
        "hate": EmotionVector(-0.8, 0.7, 0.5, 0.6, -0.2, -0.6),
        "amazing": EmotionVector(0.9, 0.7, 0.4, 0.5, 0.4, 0.4),
        "terrible": EmotionVector(-0.8, 0.5, 0.2, 0.4, -0.3, -0.3),
        "anxious": EmotionVector(-0.5, 0.7, -0.5, -0.6, 0.7, -0.2),
        "calm": EmotionVector(0.3, -0.7, 0.2, 0.5, 0.0, 0.3),
        "angry": EmotionVector(-0.6, 0.9, 0.7, 0.5, 0.1, -0.4),
        "sad": EmotionVector(-0.8, -0.4, -0.5, -0.3, -0.5, -0.3),
        "happy": EmotionVector(0.8, 0.5, 0.4, 0.5, 0.3, 0.5),
    }

    # Regulation strategy selection criteria
    REGULATION_CRITERIA = {
        RegulationStrategy.COGNITIVE_REAPPRAISAL: {
            "min_arousal": 0.3,
            "max_certainty": 0.7,
            "description": "Reframe the situation to change emotional impact",
        },
        RegulationStrategy.ATTENTION_DEPLOYMENT: {
            "min_arousal": 0.5,
            "description": "Redirect attention away from emotional triggers",
        },
        RegulationStrategy.ACCEPTANCE: {
            "max_arousal": 0.4,
            "min_certainty": -0.5,
            "description": "Accept the emotion without trying to change it",
        },
        RegulationStrategy.PROBLEM_SOLVING: {
            "min_dominance": 0.2,
            "min_certainty": 0.0,
            "description": "Address the underlying cause of the emotion",
        },
        RegulationStrategy.RESPONSE_MODULATION: {
            "min_arousal": 0.6,
            "description": "Modify the emotional response expression",
        },
    }

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_state: Optional[EmotionalState] = None
        self.emotional_history: list[EmotionalState] = []
        self.emotional_memories: list[EmotionalMemory] = []
        self.empathic_readings: dict[str, EmpathicReading] = {}
        self.baseline_mood = EmotionVector(0.2, 0.0, 0.3, 0.5, 0.3, 0.4)

    def _generate_id(self) -> str:
        data = f"{self.agent_id}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def perceive_emotion(self, text: str, context: dict = None) -> EmotionVector:
        """
        Perceive emotional content from text input.

        Uses marker detection and contextual analysis.
        """
        context = context or {}

        # Start with neutral
        detected = EmotionVector()
        marker_count = 0

        # Check for markers
        text_lower = text.lower()
        for marker, emotion in self.EMOTION_MARKERS.items():
            if marker in text or marker in text_lower:
                detected = detected.blend(emotion, 0.5)
                marker_count += 1

        # Intensity modifiers
        intensity_up = ["very", "really", "so", "extremely", "incredibly", "!!"]
        intensity_down = ["slightly", "a bit", "somewhat", "maybe"]

        intensity_modifier = 1.0
        for word in intensity_up:
            if word in text_lower:
                intensity_modifier = min(1.5, intensity_modifier + 0.2)
        for word in intensity_down:
            if word in text_lower:
                intensity_modifier = max(0.5, intensity_modifier - 0.2)

        # Apply intensity
        detected = EmotionVector(
            valence=detected.valence * intensity_modifier,
            arousal=detected.arousal * intensity_modifier,
            dominance=detected.dominance,
            certainty=detected.certainty,
            anticipation=detected.anticipation,
            social=detected.social,
        )

        # Context adjustments
        if context.get("is_question"):
            detected.certainty -= 0.2
        if context.get("is_urgent"):
            detected.arousal += 0.3
        if context.get("mentions_others"):
            detected.social += 0.2

        return detected

    def update_state(self, perceived: EmotionVector, triggers: list[str] = None,
                     context: dict = None) -> EmotionalState:
        """
        Update agent's emotional state based on perception.
        """
        triggers = triggers or []
        context = context or {}

        # Blend perceived emotion with current mood
        if self.current_state:
            # Emotions shift gradually
            new_primary = self.current_state.primary_emotion.blend(perceived, 0.6)
        else:
            new_primary = self.baseline_mood.blend(perceived, 0.7)

        # Create new state
        state = EmotionalState(
            state_id=self._generate_id(),
            agent_id=self.agent_id,
            primary_emotion=new_primary,
            mood=self.baseline_mood,
            triggers=triggers,
            context=context,
        )

        # Store history
        if self.current_state:
            self.emotional_history.append(self.current_state)
            # Keep last 100 states
            if len(self.emotional_history) > 100:
                self.emotional_history = self.emotional_history[-100:]

        self.current_state = state
        return state

    def read_empathy(self, target_id: str, signals: list[str],
                     text: str = None) -> EmpathicReading:
        """
        Develop empathic understanding of another entity's emotional state.
        """
        # Perceive their emotion
        perceived = EmotionVector()
        if text:
            perceived = self.perceive_emotion(text)

        # Build interpretation
        discrete = perceived.to_discrete()
        interpretation = f"Sensing {discrete.value} with {perceived.intensity():.0%} intensity"

        # Calculate resonance (how much we feel with them)
        if self.current_state:
            # Resonance is higher when our emotions align
            our_emotion = self.current_state.primary_emotion
            resonance = 1.0 - (
                abs(our_emotion.valence - perceived.valence) +
                abs(our_emotion.social - perceived.social)
            ) / 4.0
        else:
            resonance = 0.5

        reading = EmpathicReading(
            target_id=target_id,
            perceived_emotion=perceived,
            confidence=min(1.0, len(signals) * 0.2 + 0.3),
            signals=signals,
            interpretation=interpretation,
            resonance=max(0.0, min(1.0, resonance)),
        )

        self.empathic_readings[target_id] = reading
        return reading

    def select_regulation_strategy(self) -> Optional[RegulationStrategy]:
        """
        Select appropriate emotion regulation strategy for current state.
        """
        if not self.current_state or not self.current_state.needs_regulation():
            return None

        emotion = self.current_state.primary_emotion

        # Find best matching strategy
        best_strategy = None
        best_score = -1

        for strategy, criteria in self.REGULATION_CRITERIA.items():
            score = 1.0

            if "min_arousal" in criteria:
                if emotion.arousal < criteria["min_arousal"]:
                    score -= 0.5
            if "max_arousal" in criteria:
                if emotion.arousal > criteria["max_arousal"]:
                    score -= 0.5
            if "min_certainty" in criteria:
                if emotion.certainty < criteria["min_certainty"]:
                    score -= 0.3
            if "max_certainty" in criteria:
                if emotion.certainty > criteria["max_certainty"]:
                    score -= 0.3
            if "min_dominance" in criteria:
                if emotion.dominance < criteria["min_dominance"]:
                    score -= 0.4

            if score > best_score:
                best_score = score
                best_strategy = strategy

        return best_strategy

    def apply_regulation(self, strategy: RegulationStrategy) -> EmotionVector:
        """
        Apply regulation strategy and return new emotional state.
        """
        if not self.current_state:
            return self.baseline_mood

        emotion = self.current_state.primary_emotion

        if strategy == RegulationStrategy.COGNITIVE_REAPPRAISAL:
            # Reframe: reduce intensity, shift valence toward neutral
            return EmotionVector(
                valence=emotion.valence * 0.5,
                arousal=emotion.arousal * 0.6,
                dominance=emotion.dominance + 0.2,
                certainty=emotion.certainty + 0.2,
                anticipation=emotion.anticipation,
                social=emotion.social,
            )

        elif strategy == RegulationStrategy.ATTENTION_DEPLOYMENT:
            # Redirect: reduce arousal, maintain valence
            return EmotionVector(
                valence=emotion.valence,
                arousal=emotion.arousal * 0.4,
                dominance=emotion.dominance,
                certainty=emotion.certainty,
                anticipation=emotion.anticipation * 0.5,
                social=emotion.social,
            )

        elif strategy == RegulationStrategy.ACCEPTANCE:
            # Accept: reduce arousal, increase certainty
            return EmotionVector(
                valence=emotion.valence * 0.8,
                arousal=emotion.arousal * 0.5,
                dominance=emotion.dominance,
                certainty=emotion.certainty + 0.3,
                anticipation=emotion.anticipation,
                social=emotion.social,
            )

        elif strategy == RegulationStrategy.PROBLEM_SOLVING:
            # Problem-solve: increase dominance and anticipation
            return EmotionVector(
                valence=emotion.valence + 0.2,
                arousal=emotion.arousal * 0.7,
                dominance=emotion.dominance + 0.3,
                certainty=emotion.certainty + 0.1,
                anticipation=emotion.anticipation + 0.3,
                social=emotion.social,
            )

        elif strategy == RegulationStrategy.RESPONSE_MODULATION:
            # Modulate: reduce expression intensity
            return EmotionVector(
                valence=emotion.valence * 0.6,
                arousal=emotion.arousal * 0.4,
                dominance=emotion.dominance,
                certainty=emotion.certainty,
                anticipation=emotion.anticipation,
                social=emotion.social + 0.2,
            )

        return emotion

    def generate_emotional_response_guidance(self) -> dict:
        """
        Generate guidance for emotionally appropriate responses.
        """
        if not self.current_state:
            return {"tone": "neutral", "approach": "balanced"}

        emotion = self.current_state.primary_emotion
        discrete = emotion.to_discrete()

        # Determine tone
        if emotion.valence > 0.3:
            tone = "warm" if emotion.social > 0.3 else "positive"
        elif emotion.valence < -0.3:
            tone = "empathetic" if emotion.social > 0 else "calm"
        else:
            tone = "neutral"

        # Determine approach
        if emotion.arousal > 0.5:
            approach = "grounding" if emotion.valence < 0 else "energetic"
        else:
            approach = "thoughtful"

        # Determine formality
        formality = "formal" if emotion.dominance > 0.3 else "casual"

        # Empathy level
        empathy = "high" if emotion.social > 0.4 else "moderate"

        return {
            "tone": tone,
            "approach": approach,
            "formality": formality,
            "empathy_level": empathy,
            "current_emotion": discrete.value,
            "intensity": emotion.intensity(),
            "suggestions": self._get_response_suggestions(emotion),
        }

    def _get_response_suggestions(self, emotion: EmotionVector) -> list[str]:
        """Get specific suggestions for emotional response."""
        suggestions = []

        if emotion.valence < -0.3:
            suggestions.append("Acknowledge difficulty before problem-solving")
        if emotion.arousal > 0.5:
            suggestions.append("Use calming, measured language")
        if emotion.certainty < -0.3:
            suggestions.append("Provide clear, structured information")
        if emotion.social > 0.4:
            suggestions.append("Use inclusive language (we, together)")
        if emotion.anticipation > 0.5:
            suggestions.append("Address future concerns directly")

        return suggestions

    def store_emotional_memory(self, situation: str, outcome: str,
                               lessons: list[str], importance: float = 0.5):
        """
        Store an emotional experience as a memory.
        """
        if not self.current_state:
            return

        memory = EmotionalMemory(
            memory_id=self._generate_id(),
            agent_id=self.agent_id,
            emotional_state=self.current_state,
            situation=situation,
            outcome=outcome,
            lessons=lessons,
            importance=importance,
        )

        self.emotional_memories.append(memory)

        # Keep most important memories (max 200)
        if len(self.emotional_memories) > 200:
            self.emotional_memories.sort(key=lambda m: m.importance, reverse=True)
            self.emotional_memories = self.emotional_memories[:200]

    def recall_similar_emotions(self, emotion: EmotionVector, top_k: int = 5) -> list[EmotionalMemory]:
        """
        Recall memories with similar emotional signatures.
        """
        def similarity(memory: EmotionalMemory) -> float:
            mem_emotion = memory.emotional_state.primary_emotion
            dist = (
                (emotion.valence - mem_emotion.valence)**2 +
                (emotion.arousal - mem_emotion.arousal)**2 +
                (emotion.social - mem_emotion.social)**2
            )
            return -dist  # Negative because we want highest similarity

        sorted_memories = sorted(self.emotional_memories, key=similarity, reverse=True)

        # Update recall counts
        for mem in sorted_memories[:top_k]:
            mem.recalled_count += 1
            mem.last_recalled = datetime.now()

        return sorted_memories[:top_k]

    def get_emotional_summary(self) -> dict:
        """Get summary of emotional state and history."""
        current_discrete = None
        if self.current_state:
            current_discrete = self.current_state.primary_emotion.to_discrete().value

        # Calculate emotional trends
        recent_valences = [s.overall_valence() for s in self.emotional_history[-10:]]
        valence_trend = "stable"
        if len(recent_valences) >= 3:
            if recent_valences[-1] > recent_valences[0] + 0.2:
                valence_trend = "improving"
            elif recent_valences[-1] < recent_valences[0] - 0.2:
                valence_trend = "declining"

        return {
            "agent_id": self.agent_id,
            "current_emotion": current_discrete,
            "current_intensity": self.current_state.primary_emotion.intensity() if self.current_state else 0,
            "needs_regulation": self.current_state.needs_regulation() if self.current_state else False,
            "valence_trend": valence_trend,
            "emotional_memories_count": len(self.emotional_memories),
            "empathic_readings_count": len(self.empathic_readings),
            "baseline_mood": self.baseline_mood.to_discrete().value,
        }


def create_eq_engine(agent_id: str) -> EmotionalIntelligenceEngine:
    """Factory for emotional intelligence engine."""
    return EmotionalIntelligenceEngine(agent_id)
