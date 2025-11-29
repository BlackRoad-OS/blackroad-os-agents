#!/usr/bin/env python3
"""
Advanced Memory Architecture

A comprehensive cognitive memory system inspired by human memory research:

1. SENSORY MEMORY: Ultra-short-term buffer for raw inputs
2. WORKING MEMORY: Active processing space with limited capacity
3. EPISODIC MEMORY: Autobiographical events with temporal context
4. SEMANTIC MEMORY: Facts, concepts, and relationships
5. PROCEDURAL MEMORY: Skills and how-to knowledge
6. PROSPECTIVE MEMORY: Future intentions and reminders

Key Features:
- Memory consolidation (short-term → long-term)
- Associative retrieval (spreading activation)
- Forgetting curves (decay and interference)
- Memory reconstruction (not perfect playback)
- Emotional enhancement of memory
- Cross-memory integration

Architecture:
                    ┌─────────────────────┐
                    │   Sensory Input     │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │   Sensory Buffer    │ ← ~500ms retention
                    └──────────┬──────────┘
                               │ attention
                    ┌──────────▼──────────┐
                    │   Working Memory    │ ← ~7±2 items, ~30s
                    ├─────────────────────┤
                    │ Central Executive   │
                    │ Phonological Loop   │
                    │ Visuospatial Pad    │
                    │ Episodic Buffer     │
                    └──────────┬──────────┘
                               │ rehearsal/encoding
          ┌────────────────────┼────────────────────┐
          │                    │                    │
    ┌─────▼─────┐       ┌──────▼──────┐      ┌─────▼─────┐
    │ Episodic  │       │ Semantic    │      │Procedural │
    │ Memory    │       │ Memory      │      │ Memory    │
    │(Events)   │       │(Facts)      │      │(Skills)   │
    └───────────┘       └─────────────┘      └───────────┘
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Prospective Memory  │ ← Future intentions
                    └─────────────────────┘
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Any
import hashlib
import math
import heapq


class MemoryType(Enum):
    """Types of memory in the cognitive architecture."""
    SENSORY = "sensory"
    WORKING = "working"
    EPISODIC = "episodic"
    SEMANTIC = "semantic"
    PROCEDURAL = "procedural"
    PROSPECTIVE = "prospective"


class MemoryStrength(Enum):
    """Strength of memory consolidation."""
    FLEETING = "fleeting"     # Will decay quickly
    WEAK = "weak"             # May be forgotten
    MODERATE = "moderate"     # Reasonably stable
    STRONG = "strong"         # Well consolidated
    PERMANENT = "permanent"   # Core knowledge


class RetrievalCue(Enum):
    """Types of retrieval cues for memory access."""
    DIRECT = "direct"         # Direct key lookup
    TEMPORAL = "temporal"     # Time-based retrieval
    SEMANTIC = "semantic"     # Meaning-based retrieval
    EPISODIC = "episodic"     # Context-based retrieval
    EMOTIONAL = "emotional"   # Affect-based retrieval
    ASSOCIATIVE = "associative"  # Spreading activation


@dataclass
class MemoryTrace:
    """
    A single memory trace in the system.

    Memory traces are the fundamental units of storage.
    They decay over time but can be strengthened through rehearsal.
    """
    trace_id: str
    memory_type: MemoryType
    content: Any
    encoding_context: dict
    strength: float = 1.0            # 0 to 1, decays over time
    emotional_valence: float = 0.0   # -1 to +1
    emotional_arousal: float = 0.0   # 0 to 1
    associations: list[str] = field(default_factory=list)  # IDs of related traces
    access_count: int = 0
    last_access: datetime = field(default_factory=datetime.now)
    created_at: datetime = field(default_factory=datetime.now)
    tags: list[str] = field(default_factory=list)

    def decay(self, elapsed_seconds: float, decay_rate: float = 0.1) -> float:
        """
        Apply memory decay based on Ebbinghaus forgetting curve.

        R = e^(-t/S) where t is time and S is stability
        """
        stability = self.strength * 10  # Higher strength = slower decay
        retention = math.exp(-elapsed_seconds / (3600 * stability))  # Hourly decay
        self.strength *= retention
        return self.strength

    def reinforce(self, amount: float = 0.2) -> float:
        """Strengthen memory through rehearsal or re-access."""
        self.strength = min(1.0, self.strength + amount)
        self.access_count += 1
        self.last_access = datetime.now()
        return self.strength

    def is_accessible(self, threshold: float = 0.1) -> bool:
        """Can this memory be retrieved?"""
        return self.strength >= threshold


@dataclass
class EpisodicMemory:
    """
    An episodic memory - a specific event in time and space.

    Episodic memories are autobiographical and include:
    - What happened
    - When it happened
    - Where it happened
    - Who was involved
    - How it felt
    """
    episode_id: str
    what: str                        # Event description
    when: datetime                   # Timestamp
    where: Optional[str] = None      # Location/context
    who: list[str] = field(default_factory=list)  # Participants
    emotional_state: dict = field(default_factory=dict)
    sensory_details: dict = field(default_factory=dict)
    preceding_event: Optional[str] = None  # What happened before
    following_event: Optional[str] = None  # What happened after
    importance: float = 0.5          # 0 to 1
    vividness: float = 0.5           # 0 to 1 (detail level)
    confidence: float = 0.8          # Memory accuracy confidence


@dataclass
class SemanticFact:
    """
    A semantic memory - factual knowledge without temporal context.

    Semantic memories are decontextualized facts:
    - Concepts and definitions
    - Relationships between concepts
    - General world knowledge
    """
    fact_id: str
    subject: str
    predicate: str
    object: str
    confidence: float = 0.9
    source: Optional[str] = None
    category: Optional[str] = None
    related_facts: list[str] = field(default_factory=list)
    contradicts: list[str] = field(default_factory=list)


@dataclass
class ProceduralSkill:
    """
    A procedural memory - how to do something.

    Procedural memories are implicit and action-oriented:
    - Steps to perform a task
    - Conditions for each step
    - Expected outcomes
    """
    skill_id: str
    name: str
    description: str
    steps: list[dict]  # Each step: {action, conditions, expected_result}
    proficiency: float = 0.5  # 0 to 1
    practice_count: int = 0
    last_used: datetime = field(default_factory=datetime.now)
    prerequisites: list[str] = field(default_factory=list)
    domain: str = "general"


@dataclass
class ProspectiveItem:
    """
    A prospective memory - intention for the future.

    Prospective memories are "remember to" items:
    - Time-based (do X at time T)
    - Event-based (do X when Y happens)
    """
    item_id: str
    intention: str
    trigger_type: str  # "time" or "event"
    trigger_condition: Any  # datetime or event pattern
    priority: float = 0.5
    created_at: datetime = field(default_factory=datetime.now)
    completed: bool = False
    reminded_count: int = 0


@dataclass
class WorkingMemorySlot:
    """A slot in working memory's limited capacity."""
    slot_id: str
    content: Any
    source_type: MemoryType
    source_id: Optional[str] = None
    activation: float = 1.0  # Decays quickly
    entered_at: datetime = field(default_factory=datetime.now)


class MemoryArchitecture:
    """
    Complete cognitive memory system.

    Implements a multi-store memory architecture with:
    - Sensory buffers
    - Working memory with limited capacity
    - Long-term stores (episodic, semantic, procedural)
    - Prospective memory for intentions
    - Consolidation and retrieval processes
    """

    WORKING_MEMORY_CAPACITY = 7  # Miller's magical number

    def __init__(self, agent_id: str):
        self.agent_id = agent_id

        # Memory stores
        self.sensory_buffer: list[MemoryTrace] = []  # Very short term
        self.working_memory: list[WorkingMemorySlot] = []  # Limited capacity
        self.episodic_store: dict[str, EpisodicMemory] = {}
        self.semantic_store: dict[str, SemanticFact] = {}
        self.procedural_store: dict[str, ProceduralSkill] = {}
        self.prospective_store: dict[str, ProspectiveItem] = {}

        # Trace index for all memories
        self.trace_index: dict[str, MemoryTrace] = {}

        # Association network (spreading activation)
        self.associations: dict[str, list[tuple[str, float]]] = {}  # id -> [(id, weight)]

        # Statistics
        self.total_encodings = 0
        self.total_retrievals = 0
        self.retrieval_failures = 0

    def _generate_id(self) -> str:
        data = f"{self.agent_id}:{self.total_encodings}:{datetime.now().isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:12]

    # =========== ENCODING ===========

    def encode_sensory(self, content: Any, modality: str = "text") -> MemoryTrace:
        """
        Encode raw input into sensory buffer.

        Sensory memory is very brief (~500ms for visual, ~3s for auditory).
        Only attended items move to working memory.
        """
        trace = MemoryTrace(
            trace_id=self._generate_id(),
            memory_type=MemoryType.SENSORY,
            content=content,
            encoding_context={"modality": modality},
            strength=1.0,
        )

        self.sensory_buffer.append(trace)
        self.trace_index[trace.trace_id] = trace
        self.total_encodings += 1

        # Sensory buffer is very limited
        if len(self.sensory_buffer) > 20:
            old = self.sensory_buffer.pop(0)
            if old.trace_id in self.trace_index:
                del self.trace_index[old.trace_id]

        return trace

    def attend(self, trace_id: str) -> Optional[WorkingMemorySlot]:
        """
        Move item from sensory buffer to working memory through attention.

        This is the gateway from perception to cognition.
        """
        trace = self.trace_index.get(trace_id)
        if not trace or trace.memory_type != MemoryType.SENSORY:
            return None

        # Check working memory capacity
        if len(self.working_memory) >= self.WORKING_MEMORY_CAPACITY:
            # Remove least activated item
            self.working_memory.sort(key=lambda s: s.activation)
            evicted = self.working_memory.pop(0)
            # Evicted item may be forgotten or consolidated
            self._try_consolidate(evicted)

        slot = WorkingMemorySlot(
            slot_id=self._generate_id(),
            content=trace.content,
            source_type=MemoryType.SENSORY,
            source_id=trace.trace_id,
        )

        self.working_memory.append(slot)
        trace.reinforce(0.3)

        return slot

    def encode_episodic(self, what: str, emotional_state: dict = None,
                        who: list[str] = None, where: str = None,
                        importance: float = 0.5) -> EpisodicMemory:
        """
        Encode an episodic memory - a specific event.
        """
        episode = EpisodicMemory(
            episode_id=self._generate_id(),
            what=what,
            when=datetime.now(),
            where=where,
            who=who or [],
            emotional_state=emotional_state or {},
            importance=importance,
        )

        self.episodic_store[episode.episode_id] = episode
        self.total_encodings += 1

        # Create trace
        trace = MemoryTrace(
            trace_id=episode.episode_id,
            memory_type=MemoryType.EPISODIC,
            content=episode,
            encoding_context={"what": what, "where": where},
            strength=0.5 + importance * 0.5,
            emotional_valence=emotional_state.get("valence", 0) if emotional_state else 0,
            emotional_arousal=emotional_state.get("arousal", 0) if emotional_state else 0,
        )
        self.trace_index[trace.trace_id] = trace

        return episode

    def encode_semantic(self, subject: str, predicate: str, obj: str,
                        confidence: float = 0.9, category: str = None) -> SemanticFact:
        """
        Encode a semantic fact - decontextualized knowledge.
        """
        fact = SemanticFact(
            fact_id=self._generate_id(),
            subject=subject,
            predicate=predicate,
            object=obj,
            confidence=confidence,
            category=category,
        )

        self.semantic_store[fact.fact_id] = fact
        self.total_encodings += 1

        # Create trace
        trace = MemoryTrace(
            trace_id=fact.fact_id,
            memory_type=MemoryType.SEMANTIC,
            content=fact,
            encoding_context={"subject": subject, "predicate": predicate},
            strength=confidence,
            tags=[subject, predicate, obj, category] if category else [subject, predicate, obj],
        )
        self.trace_index[trace.trace_id] = trace

        # Auto-associate with related facts
        self._build_semantic_associations(fact)

        return fact

    def encode_procedural(self, name: str, description: str,
                          steps: list[dict], domain: str = "general") -> ProceduralSkill:
        """
        Encode a procedural skill - how to do something.
        """
        skill = ProceduralSkill(
            skill_id=self._generate_id(),
            name=name,
            description=description,
            steps=steps,
            domain=domain,
        )

        self.procedural_store[skill.skill_id] = skill
        self.total_encodings += 1

        # Create trace
        trace = MemoryTrace(
            trace_id=skill.skill_id,
            memory_type=MemoryType.PROCEDURAL,
            content=skill,
            encoding_context={"name": name, "domain": domain},
            strength=0.3,  # Skills start weak, strengthen with practice
            tags=[name, domain],
        )
        self.trace_index[trace.trace_id] = trace

        return skill

    def encode_prospective(self, intention: str, trigger_type: str,
                           trigger_condition: Any, priority: float = 0.5) -> ProspectiveItem:
        """
        Encode a prospective memory - future intention.
        """
        item = ProspectiveItem(
            item_id=self._generate_id(),
            intention=intention,
            trigger_type=trigger_type,
            trigger_condition=trigger_condition,
            priority=priority,
        )

        self.prospective_store[item.item_id] = item
        self.total_encodings += 1

        return item

    # =========== RETRIEVAL ===========

    def retrieve(self, cue: Any, cue_type: RetrievalCue = RetrievalCue.DIRECT,
                 memory_type: MemoryType = None, top_k: int = 5) -> list[MemoryTrace]:
        """
        Retrieve memories using a cue.

        Different cue types activate different retrieval pathways.
        """
        self.total_retrievals += 1
        results = []

        if cue_type == RetrievalCue.DIRECT:
            # Direct key lookup
            if cue in self.trace_index:
                trace = self.trace_index[cue]
                if trace.is_accessible():
                    trace.reinforce(0.1)
                    results.append(trace)

        elif cue_type == RetrievalCue.SEMANTIC:
            # Search by semantic content
            cue_lower = str(cue).lower()
            for trace_id, trace in self.trace_index.items():
                if memory_type and trace.memory_type != memory_type:
                    continue
                # Check tags and content
                if any(cue_lower in tag.lower() for tag in trace.tags):
                    if trace.is_accessible():
                        results.append(trace)
                elif cue_lower in str(trace.content).lower():
                    if trace.is_accessible():
                        results.append(trace)

        elif cue_type == RetrievalCue.TEMPORAL:
            # Retrieve by time
            if isinstance(cue, datetime):
                target_time = cue
            elif isinstance(cue, str):
                # Parse relative time like "yesterday", "last week"
                target_time = self._parse_relative_time(cue)
            else:
                target_time = datetime.now()

            for trace_id, trace in self.trace_index.items():
                if memory_type and trace.memory_type != memory_type:
                    continue
                # Check temporal proximity
                time_diff = abs((trace.created_at - target_time).total_seconds())
                if time_diff < 86400:  # Within a day
                    if trace.is_accessible():
                        trace.encoding_context["time_proximity"] = time_diff
                        results.append(trace)

        elif cue_type == RetrievalCue.EMOTIONAL:
            # Retrieve by emotional similarity
            if isinstance(cue, dict):
                target_valence = cue.get("valence", 0)
                target_arousal = cue.get("arousal", 0)
            else:
                target_valence, target_arousal = 0, 0

            for trace_id, trace in self.trace_index.items():
                if memory_type and trace.memory_type != memory_type:
                    continue
                # Calculate emotional distance
                dist = math.sqrt(
                    (trace.emotional_valence - target_valence)**2 +
                    (trace.emotional_arousal - target_arousal)**2
                )
                if dist < 0.5 and trace.is_accessible():
                    trace.encoding_context["emotional_distance"] = dist
                    results.append(trace)

        elif cue_type == RetrievalCue.ASSOCIATIVE:
            # Spreading activation from cue
            results = self._spreading_activation(str(cue), top_k)

        # Sort by strength and return top-k
        results.sort(key=lambda t: t.strength, reverse=True)
        results = results[:top_k]

        if not results:
            self.retrieval_failures += 1

        return results

    def retrieve_episodic(self, query: str = None, time_range: tuple = None,
                          who: str = None, top_k: int = 5) -> list[EpisodicMemory]:
        """Retrieve episodic memories with filters."""
        results = []

        for episode in self.episodic_store.values():
            # Apply filters
            if query and query.lower() not in episode.what.lower():
                continue
            if time_range:
                if episode.when < time_range[0] or episode.when > time_range[1]:
                    continue
            if who and who not in episode.who:
                continue

            # Check if trace is accessible
            trace = self.trace_index.get(episode.episode_id)
            if trace and trace.is_accessible():
                results.append(episode)

        # Sort by importance and recency
        results.sort(key=lambda e: (e.importance, e.when), reverse=True)
        return results[:top_k]

    def retrieve_semantic(self, subject: str = None, predicate: str = None,
                          category: str = None, top_k: int = 10) -> list[SemanticFact]:
        """Retrieve semantic facts with filters."""
        results = []

        for fact in self.semantic_store.values():
            if subject and subject.lower() not in fact.subject.lower():
                continue
            if predicate and predicate.lower() not in fact.predicate.lower():
                continue
            if category and fact.category != category:
                continue

            trace = self.trace_index.get(fact.fact_id)
            if trace and trace.is_accessible():
                results.append(fact)

        results.sort(key=lambda f: f.confidence, reverse=True)
        return results[:top_k]

    def retrieve_procedural(self, name: str = None, domain: str = None) -> list[ProceduralSkill]:
        """Retrieve procedural skills."""
        results = []

        for skill in self.procedural_store.values():
            if name and name.lower() not in skill.name.lower():
                continue
            if domain and skill.domain != domain:
                continue

            trace = self.trace_index.get(skill.skill_id)
            if trace and trace.is_accessible():
                results.append(skill)

        results.sort(key=lambda s: s.proficiency, reverse=True)
        return results

    def check_prospective(self, current_time: datetime = None,
                          current_event: str = None) -> list[ProspectiveItem]:
        """Check for prospective memories that should be triggered."""
        if current_time is None:
            current_time = datetime.now()

        triggered = []

        for item in self.prospective_store.values():
            if item.completed:
                continue

            if item.trigger_type == "time":
                if isinstance(item.trigger_condition, datetime):
                    if current_time >= item.trigger_condition:
                        triggered.append(item)
                        item.reminded_count += 1

            elif item.trigger_type == "event":
                if current_event and item.trigger_condition in current_event:
                    triggered.append(item)
                    item.reminded_count += 1

        return triggered

    # =========== WORKING MEMORY ===========

    def update_working_memory(self, content: Any, source_type: MemoryType = MemoryType.WORKING) -> WorkingMemorySlot:
        """Add item to working memory, managing capacity."""
        if len(self.working_memory) >= self.WORKING_MEMORY_CAPACITY:
            # Decay all items
            for slot in self.working_memory:
                slot.activation *= 0.9

            # Remove lowest activation
            self.working_memory.sort(key=lambda s: s.activation)
            evicted = self.working_memory.pop(0)
            self._try_consolidate(evicted)

        slot = WorkingMemorySlot(
            slot_id=self._generate_id(),
            content=content,
            source_type=source_type,
            activation=1.0,
        )

        self.working_memory.append(slot)
        return slot

    def rehearse(self, slot_id: str) -> bool:
        """Rehearse item in working memory to maintain it."""
        for slot in self.working_memory:
            if slot.slot_id == slot_id:
                slot.activation = min(1.0, slot.activation + 0.3)
                slot.entered_at = datetime.now()
                return True
        return False

    def get_working_memory_contents(self) -> list[Any]:
        """Get current contents of working memory."""
        return [slot.content for slot in self.working_memory]

    # =========== CONSOLIDATION ===========

    def _try_consolidate(self, slot: WorkingMemorySlot):
        """
        Try to consolidate working memory item to long-term storage.

        Not all items make it to long-term memory.
        """
        # Higher activation = higher chance of consolidation
        if slot.activation < 0.3:
            return  # Too weak, forgotten

        # Determine appropriate long-term store
        content = slot.content

        if isinstance(content, dict):
            if "what" in content and "when" in content:
                # Looks like an episodic memory
                self.encode_episodic(
                    what=content.get("what", str(content)),
                    emotional_state=content.get("emotional_state"),
                    importance=slot.activation,
                )
            elif "subject" in content and "predicate" in content:
                # Looks like a semantic fact
                self.encode_semantic(
                    subject=content["subject"],
                    predicate=content["predicate"],
                    obj=content.get("object", ""),
                    confidence=slot.activation,
                )

    def consolidate_all(self):
        """Run consolidation process on all working memory."""
        for slot in list(self.working_memory):
            self._try_consolidate(slot)

    # =========== ASSOCIATIONS ===========

    def create_association(self, id1: str, id2: str, weight: float = 0.5):
        """Create bidirectional association between memories."""
        if id1 not in self.associations:
            self.associations[id1] = []
        if id2 not in self.associations:
            self.associations[id2] = []

        # Add or update association
        self.associations[id1].append((id2, weight))
        self.associations[id2].append((id1, weight))

        # Also update trace associations
        if id1 in self.trace_index:
            self.trace_index[id1].associations.append(id2)
        if id2 in self.trace_index:
            self.trace_index[id2].associations.append(id1)

    def _build_semantic_associations(self, fact: SemanticFact):
        """Build associations for semantic facts based on shared concepts."""
        for other_id, other_fact in self.semantic_store.items():
            if other_id == fact.fact_id:
                continue

            # Check for shared concepts
            shared = 0
            if fact.subject == other_fact.subject:
                shared += 0.5
            if fact.subject == other_fact.object:
                shared += 0.3
            if fact.object == other_fact.subject:
                shared += 0.3
            if fact.object == other_fact.object:
                shared += 0.2
            if fact.category == other_fact.category:
                shared += 0.2

            if shared > 0:
                self.create_association(fact.fact_id, other_id, min(1.0, shared))

    def _spreading_activation(self, start_cue: str, max_results: int) -> list[MemoryTrace]:
        """
        Retrieve memories through spreading activation.

        Activation spreads from cue through association network.
        """
        # Find starting nodes
        activated = {}

        for trace_id, trace in self.trace_index.items():
            if start_cue.lower() in str(trace.content).lower():
                activated[trace_id] = trace.strength
            elif any(start_cue.lower() in tag.lower() for tag in trace.tags):
                activated[trace_id] = trace.strength * 0.8

        # Spread activation
        for _ in range(3):  # 3 rounds of spreading
            new_activation = {}
            for trace_id, activation in activated.items():
                if trace_id in self.associations:
                    for neighbor_id, weight in self.associations[trace_id]:
                        if neighbor_id in self.trace_index:
                            spread = activation * weight * 0.5
                            current = new_activation.get(neighbor_id, 0)
                            new_activation[neighbor_id] = max(current, spread)

            # Merge
            for trace_id, activation in new_activation.items():
                if trace_id not in activated:
                    activated[trace_id] = activation

        # Return top results
        sorted_ids = sorted(activated.items(), key=lambda x: x[1], reverse=True)
        results = []
        for trace_id, _ in sorted_ids[:max_results]:
            trace = self.trace_index.get(trace_id)
            if trace and trace.is_accessible():
                results.append(trace)

        return results

    # =========== MAINTENANCE ===========

    def decay_all(self, elapsed_seconds: float = 3600):
        """Apply decay to all memories."""
        for trace in self.trace_index.values():
            trace.decay(elapsed_seconds)

    def forget(self, threshold: float = 0.05):
        """Remove memories below threshold (simulates forgetting)."""
        to_remove = []
        for trace_id, trace in self.trace_index.items():
            if trace.strength < threshold:
                to_remove.append(trace_id)

        for trace_id in to_remove:
            # Remove from appropriate store
            trace = self.trace_index[trace_id]
            if trace.memory_type == MemoryType.EPISODIC:
                self.episodic_store.pop(trace_id, None)
            elif trace.memory_type == MemoryType.SEMANTIC:
                self.semantic_store.pop(trace_id, None)
            elif trace.memory_type == MemoryType.PROCEDURAL:
                self.procedural_store.pop(trace_id, None)

            del self.trace_index[trace_id]

    def practice_skill(self, skill_id: str) -> bool:
        """Practice a procedural skill to improve proficiency."""
        if skill_id not in self.procedural_store:
            return False

        skill = self.procedural_store[skill_id]
        skill.practice_count += 1
        skill.proficiency = min(1.0, skill.proficiency + 0.1)
        skill.last_used = datetime.now()

        # Also strengthen the trace
        if skill_id in self.trace_index:
            self.trace_index[skill_id].reinforce(0.2)

        return True

    def _parse_relative_time(self, time_str: str) -> datetime:
        """Parse relative time strings."""
        now = datetime.now()
        time_str = time_str.lower()

        if "yesterday" in time_str:
            return now - timedelta(days=1)
        elif "last week" in time_str:
            return now - timedelta(weeks=1)
        elif "last month" in time_str:
            return now - timedelta(days=30)
        elif "today" in time_str:
            return now
        elif "hour ago" in time_str:
            return now - timedelta(hours=1)

        return now

    # =========== SUMMARY ===========

    def get_memory_summary(self) -> dict:
        """Get summary of memory system state."""
        accessible_traces = sum(1 for t in self.trace_index.values() if t.is_accessible())

        return {
            "agent_id": self.agent_id,
            "working_memory": {
                "capacity": self.WORKING_MEMORY_CAPACITY,
                "current_load": len(self.working_memory),
                "utilization": len(self.working_memory) / self.WORKING_MEMORY_CAPACITY,
            },
            "long_term": {
                "episodic_count": len(self.episodic_store),
                "semantic_count": len(self.semantic_store),
                "procedural_count": len(self.procedural_store),
                "prospective_count": len(self.prospective_store),
            },
            "traces": {
                "total": len(self.trace_index),
                "accessible": accessible_traces,
                "associations": sum(len(a) for a in self.associations.values()),
            },
            "statistics": {
                "total_encodings": self.total_encodings,
                "total_retrievals": self.total_retrievals,
                "retrieval_success_rate": (
                    (self.total_retrievals - self.retrieval_failures) / max(1, self.total_retrievals)
                ),
            },
        }


def create_memory_system(agent_id: str) -> MemoryArchitecture:
    """Factory for memory architecture."""
    return MemoryArchitecture(agent_id)
