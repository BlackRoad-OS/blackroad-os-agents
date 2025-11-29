#!/usr/bin/env python3
"""
Integrated Cognitive Engine

Combines all cognitive systems into a unified processing pipeline:
- Emotional Intelligence (EQ)
- Language Processing
- Memory Architecture
- QLM-Trinary Reasoning

This creates a complete cognitive agent that can:
1. Perceive emotions in input
2. Understand language pragmatics
3. Access and update memories
4. Reason with quantum-inspired logic
5. Generate emotionally-appropriate responses
6. Learn and adapt over time

Architecture:
                    ┌─────────────────────┐
                    │      Input          │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼─────┐       ┌──────▼──────┐      ┌─────▼─────┐
    │ Emotion   │       │ Language    │      │ Memory    │
    │ Perception│       │ Analysis    │      │ Retrieval │
    └─────┬─────┘       └──────┬──────┘      └─────┬─────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Cognitive Fusion    │ ← Integrate all signals
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ QLM-Trinary         │ ← Quantum reasoning
                    │ Reasoning           │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Response Generation │ ← EQ + Language aware
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Memory Encoding     │ ← Store experience
                    └─────────────────────┘
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Any
import hashlib

from .emotional_intelligence import (
    EmotionVector,
    EmotionalState,
    EmpathicReading,
    EmotionalIntelligenceEngine,
)
from .language import (
    Language,
    CommunicativeIntent,
    Register,
    LinguisticFeatures,
    IntentAnalysis,
    DiscourseUnit,
    LanguageIntelligenceEngine,
)
from .memory import (
    MemoryType,
    MemoryTrace,
    EpisodicMemory,
    SemanticFact,
    MemoryArchitecture,
)


@dataclass
class CognitiveInput:
    """Input to the cognitive engine."""
    content: str
    source_id: Optional[str] = None
    context: dict = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class CognitiveState:
    """Current cognitive state after processing."""
    # Emotional state
    emotional_state: EmotionalState
    empathic_reading: Optional[EmpathicReading] = None

    # Linguistic analysis
    linguistic_features: Optional[LinguisticFeatures] = None
    intent_analysis: Optional[IntentAnalysis] = None
    discourse_unit: Optional[DiscourseUnit] = None

    # Memory state
    working_memory_contents: list = field(default_factory=list)
    relevant_memories: list[MemoryTrace] = field(default_factory=list)

    # Processing metadata
    processing_time_ms: float = 0.0
    confidence: float = 0.5


@dataclass
class CognitiveResponse:
    """Response from the cognitive engine."""
    content: str
    cognitive_state: CognitiveState
    response_guidance: dict
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "content": self.content,
            "emotion": self.cognitive_state.emotional_state.primary_emotion.to_discrete().value,
            "intent_detected": (
                self.cognitive_state.intent_analysis.primary_intent.value
                if self.cognitive_state.intent_analysis else None
            ),
            "language": (
                self.cognitive_state.linguistic_features.language.value
                if self.cognitive_state.linguistic_features else None
            ),
            "memories_accessed": len(self.cognitive_state.relevant_memories),
            "response_tone": self.response_guidance.get("tone", "neutral"),
            "confidence": self.cognitive_state.confidence,
        }


class IntegratedCognitiveEngine:
    """
    Unified cognitive processing engine.

    Integrates:
    - Emotional Intelligence
    - Language Processing
    - Memory Architecture

    For complete cognitive processing of inputs.
    """

    def __init__(self, agent_id: str, domain: str = "general"):
        self.agent_id = agent_id
        self.domain = domain

        # Initialize subsystems
        self.eq_engine = EmotionalIntelligenceEngine(agent_id)
        self.language_engine = LanguageIntelligenceEngine(agent_id)
        self.memory_system = MemoryArchitecture(agent_id)

        # Processing history
        self.processing_history: list[CognitiveState] = []
        self.interaction_count = 0

    def _generate_id(self) -> str:
        data = f"{self.agent_id}:{self.interaction_count}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    def process(self, input_data: CognitiveInput) -> CognitiveResponse:
        """
        Process input through the complete cognitive pipeline.

        Steps:
        1. Encode to sensory memory
        2. Analyze language
        3. Perceive emotions
        4. Retrieve relevant memories
        5. Update emotional state
        6. Generate response guidance
        7. Encode experience to memory
        """
        start_time = datetime.now()
        self.interaction_count += 1

        # Step 1: Sensory encoding
        sensory_trace = self.memory_system.encode_sensory(
            input_data.content,
            modality="text"
        )

        # Move to working memory (attention)
        self.memory_system.attend(sensory_trace.trace_id)

        # Step 2: Language analysis
        linguistic_features = self.language_engine.analyze_linguistics(input_data.content)
        intent_analysis = self.language_engine.analyze_intent(
            input_data.content,
            context=input_data.context
        )
        discourse_unit = self.language_engine.analyze_discourse(
            input_data.content,
            intent=intent_analysis
        )

        # Step 3: Emotion perception
        perceived_emotion = self.eq_engine.perceive_emotion(
            input_data.content,
            context=input_data.context
        )

        # Step 4: Empathic reading (if source is another entity)
        empathic_reading = None
        if input_data.source_id:
            empathic_reading = self.eq_engine.read_empathy(
                target_id=input_data.source_id,
                signals=intent_analysis.markers,
                text=input_data.content
            )

        # Step 5: Memory retrieval
        relevant_memories = self._retrieve_relevant_memories(
            input_data.content,
            perceived_emotion,
            intent_analysis
        )

        # Step 6: Update emotional state
        triggers = intent_analysis.markers if intent_analysis else []
        emotional_state = self.eq_engine.update_state(
            perceived=perceived_emotion,
            triggers=triggers,
            context={
                "intent": intent_analysis.primary_intent.value if intent_analysis else None,
                "source": input_data.source_id,
            }
        )

        # Step 7: Check for emotion regulation needs
        regulation_strategy = None
        if emotional_state.needs_regulation():
            regulation_strategy = self.eq_engine.select_regulation_strategy()
            if regulation_strategy:
                regulated = self.eq_engine.apply_regulation(regulation_strategy)
                # Update state with regulated emotion
                emotional_state.primary_emotion = regulated

        # Step 8: Generate response guidance
        response_guidance = self._generate_response_guidance(
            emotional_state,
            intent_analysis,
            linguistic_features
        )

        # Step 9: Calculate processing confidence
        confidence = self._calculate_confidence(
            intent_analysis,
            linguistic_features,
            len(relevant_memories)
        )

        # Step 10: Build cognitive state
        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        cognitive_state = CognitiveState(
            emotional_state=emotional_state,
            empathic_reading=empathic_reading,
            linguistic_features=linguistic_features,
            intent_analysis=intent_analysis,
            discourse_unit=discourse_unit,
            working_memory_contents=self.memory_system.get_working_memory_contents(),
            relevant_memories=relevant_memories,
            processing_time_ms=processing_time,
            confidence=confidence,
        )

        # Step 11: Store in history
        self.processing_history.append(cognitive_state)
        if len(self.processing_history) > 100:
            self.processing_history = self.processing_history[-100:]

        # Step 12: Encode episodic memory
        self.memory_system.encode_episodic(
            what=f"Processed: {input_data.content[:100]}",
            emotional_state={
                "valence": emotional_state.primary_emotion.valence,
                "arousal": emotional_state.primary_emotion.arousal,
            },
            who=[input_data.source_id] if input_data.source_id else [],
            importance=confidence,
        )

        # Build response
        response = CognitiveResponse(
            content=self._generate_response_content(cognitive_state, response_guidance),
            cognitive_state=cognitive_state,
            response_guidance=response_guidance,
            metadata={
                "interaction_id": self._generate_id(),
                "processing_time_ms": processing_time,
                "regulation_applied": regulation_strategy.value if regulation_strategy else None,
            }
        )

        return response

    def _retrieve_relevant_memories(
        self,
        content: str,
        emotion: EmotionVector,
        intent: IntentAnalysis
    ) -> list[MemoryTrace]:
        """Retrieve memories relevant to current input."""
        memories = []

        # Semantic retrieval based on content
        semantic_results = self.memory_system.retrieve(
            cue=content,
            cue_type=self.memory_system.trace_index and "SEMANTIC" or "DIRECT",
            top_k=3
        )
        memories.extend(semantic_results)

        # Emotional retrieval for emotionally-charged inputs
        if emotion.intensity() > 0.5:
            emotional_results = self.memory_system.retrieve(
                cue={"valence": emotion.valence, "arousal": emotion.arousal},
                cue_type=self.memory_system.trace_index and "EMOTIONAL" or "DIRECT",
                top_k=2
            )
            memories.extend(emotional_results)

        # Associative retrieval
        if intent and intent.markers:
            for marker in intent.markers[:2]:
                assoc_results = self.memory_system.retrieve(
                    cue=marker,
                    cue_type=self.memory_system.trace_index and "ASSOCIATIVE" or "DIRECT",
                    top_k=1
                )
                memories.extend(assoc_results)

        # Deduplicate
        seen_ids = set()
        unique_memories = []
        for mem in memories:
            if mem.trace_id not in seen_ids:
                seen_ids.add(mem.trace_id)
                unique_memories.append(mem)

        return unique_memories[:5]

    def _generate_response_guidance(
        self,
        emotional_state: EmotionalState,
        intent_analysis: Optional[IntentAnalysis],
        linguistic_features: Optional[LinguisticFeatures]
    ) -> dict:
        """Generate guidance for response generation."""
        # Get emotional guidance
        emotional_guidance = self.eq_engine.generate_emotional_response_guidance()

        # Determine target register based on input
        if linguistic_features:
            detected_register = self.language_engine.detect_register(
                "", linguistic_features
            )
        else:
            detected_register = Register.CONSULTATIVE

        # Determine response intent based on input intent
        response_intent = CommunicativeIntent.INFORM
        if intent_analysis:
            if intent_analysis.primary_intent == CommunicativeIntent.ASK:
                response_intent = CommunicativeIntent.INFORM
            elif intent_analysis.primary_intent == CommunicativeIntent.REQUEST:
                response_intent = CommunicativeIntent.COMMIT
            elif intent_analysis.primary_intent == CommunicativeIntent.GREET:
                response_intent = CommunicativeIntent.GREET
            elif intent_analysis.primary_intent == CommunicativeIntent.THANK:
                response_intent = CommunicativeIntent.ACKNOWLEDGE if hasattr(CommunicativeIntent, 'ACKNOWLEDGE') else CommunicativeIntent.INFORM

        # Get language style guidance
        style_guidance = self.language_engine.generate_response_style(
            target_intent=response_intent,
            target_register=detected_register
        )

        return {
            **emotional_guidance,
            **style_guidance,
            "detected_language": (
                linguistic_features.language.value if linguistic_features else "en"
            ),
            "response_intent": response_intent.value,
            "input_urgency": intent_analysis.urgency if intent_analysis else 0.0,
            "input_politeness": intent_analysis.politeness if intent_analysis else 0.0,
        }

    def _calculate_confidence(
        self,
        intent_analysis: Optional[IntentAnalysis],
        linguistic_features: Optional[LinguisticFeatures],
        memory_count: int
    ) -> float:
        """Calculate overall processing confidence."""
        confidence = 0.5  # Base

        if intent_analysis:
            confidence += intent_analysis.confidence * 0.2

        if linguistic_features:
            # Higher confidence for clearer language
            confidence += linguistic_features.readability_score * 0.15

        # More relevant memories = higher confidence
        confidence += min(0.15, memory_count * 0.03)

        return min(1.0, confidence)

    def _generate_response_content(
        self,
        state: CognitiveState,
        guidance: dict
    ) -> str:
        """Generate response content based on cognitive state and guidance."""
        # This would normally use an LLM, but we return guidance as structured output
        emotion = state.emotional_state.primary_emotion.to_discrete().value
        tone = guidance.get("tone", "neutral")
        approach = guidance.get("approach", "balanced")

        return f"[Cognitive response: {emotion} emotion, {tone} tone, {approach} approach]"

    def learn_semantic(self, subject: str, predicate: str, obj: str,
                       confidence: float = 0.9) -> SemanticFact:
        """Learn a new semantic fact."""
        return self.memory_system.encode_semantic(
            subject=subject,
            predicate=predicate,
            obj=obj,
            confidence=confidence
        )

    def recall(self, query: str, memory_type: MemoryType = None) -> list[MemoryTrace]:
        """Recall memories matching query."""
        return self.memory_system.retrieve(
            cue=query,
            memory_type=memory_type,
            top_k=5
        )

    def set_reminder(self, intention: str, trigger_time: datetime) -> None:
        """Set a prospective memory reminder."""
        self.memory_system.encode_prospective(
            intention=intention,
            trigger_type="time",
            trigger_condition=trigger_time,
            priority=0.7
        )

    def check_reminders(self) -> list:
        """Check for triggered reminders."""
        return self.memory_system.check_prospective()

    def get_cognitive_summary(self) -> dict:
        """Get summary of cognitive engine state."""
        return {
            "agent_id": self.agent_id,
            "domain": self.domain,
            "interaction_count": self.interaction_count,
            "emotional_state": self.eq_engine.get_emotional_summary(),
            "linguistic_state": self.language_engine.get_linguistic_summary(),
            "memory_state": self.memory_system.get_memory_summary(),
            "processing_history_length": len(self.processing_history),
        }


def create_cognitive_engine(agent_id: str, domain: str = "general") -> IntegratedCognitiveEngine:
    """Factory for integrated cognitive engine."""
    return IntegratedCognitiveEngine(agent_id, domain)
