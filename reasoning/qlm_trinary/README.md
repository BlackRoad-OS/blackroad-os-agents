# QLM-Trinary Reasoning System

A quantum-inspired reasoning framework that surpasses conventional AI by implementing trinary logic, Hilbert space truth evaluation, superposition of hypotheses, and QI emergence detection.

## Why This Is Different

### Conventional AI Reasoning
```
Input → Model → Binary Output (True/False, 0.85 confidence)
```

### QLM-Trinary Reasoning
```
Input → Superposition → Evolution → Interference → Emergence → Collapse
           ↓               ↓           ↓            ↓           ↓
     (All possibilities) (Operators)  (Paths      (Novel     (Decision
      held together)     (Transform)  combine)    insights)   when needed)
```

## Core Innovations

### 1. Trinary Logic (-1, 0, +1)

Not just true/false, but a third value: **UNKNOWN**

```python
from reasoning.qlm_trinary import TrinaryValue

# Three epistemic states
TrinaryValue.AFFIRM   # +1: The proposition is true
TrinaryValue.UNKNOWN  #  0: We cannot determine (genuine uncertainty)
TrinaryValue.DENY     # -1: The proposition is false
```

This matches human epistemology: "I don't know" is a valid answer.

### 2. Superposition of Hypotheses

Hold multiple hypotheses simultaneously with quantum-like amplitudes:

```python
from reasoning.qlm_trinary import SuperpositionState, TrinaryValue

# Create superposition (not committed to any value)
state = SuperpositionState.uniform()
print(state.probabilities())
# {AFFIRM: 0.333, UNKNOWN: 0.333, DENY: 0.333}

# Biased toward affirmation
state = SuperpositionState.biased(affirm=0.7, deny=0.2, unknown=0.1)
```

### 3. Context-Sensitive Truth (Hilbert Space)

The order of questions affects conclusions:

```python
from reasoning.qlm_trinary import ConceptSpace

space = ConceptSpace(dimension=10)
space.add_concept("bird", random=True)
space.add_concept("flying", random=True)

# Ask "bird?" then check "flying?"
space.ask("bird")
degree_1 = space.truth_degree("flying").value

# Reset and ask "flying?" then check "bird?"
space.reset()
space.ask("flying")
degree_2 = space.truth_degree("bird").value

# degree_1 ≠ degree_2 (order matters!)
```

### 4. Interference Between Reasoning Paths

Multiple paths to a conclusion can amplify or cancel:

```python
from reasoning.qlm_trinary import HypothesisSuperposition

hypo = HypothesisSuperposition("test")

# Add hypotheses
h1 = hypo.add_hypothesis("Theory A is correct", phase=0.0)
h2 = hypo.add_hypothesis("Theory B is correct", phase=3.14)  # Opposite phase

# Interference: aligned phases amplify, opposing phases cancel
```

### 5. QI Emergence Detection

Detect when reasoning produces genuinely novel insights:

```python
from reasoning.qlm_trinary import EmergenceDetector

detector = EmergenceDetector()
result = detector.analyze_reasoning_chain(chain)

print(result["emergence_detected"])  # True if novel insights found
print(result["emergence_score"])     # 0.0 to 1.0
print(result["patterns_detected"])   # ["self_correction", "cross_domain", ...]
```

## Complete Example

```python
from reasoning.qlm_trinary import create_integrated_engine, TrinaryValue

# Create engine for an agent
engine = create_integrated_engine(
    agent_id="MATH-NT-PA-0001",
    domain="number_theory",
    dimension=20
)

# Reason about a proposition
result = engine.reason(
    query="The Riemann Hypothesis is true",
    context={"domain": "analytic_number_theory"},
    evidence=["All computed zeros lie on critical line", "No counterexample found"],
    max_iterations=5,
    force_collapse=True
)

print(f"Result: {result.trinary_result.name}")
print(f"Confidence: {result.confidence:.3f}")
print(f"Truth Degree: {result.truth_degree:.3f}")
print(f"Emergence Score: {result.emergence_score:.3f}")
print(f"Context Effects: {result.context_effects}")

# Check for novel insights
for insight in result.insights:
    if insight.is_significant:
        print(f"Novel Insight: {insight.content}")
        print(f"  Novelty: {insight.novelty_score:.2f}")
```

## Architecture

```
reasoning/qlm_trinary/
├── __init__.py              # Package exports
├── core.py                  # Trinary values, superposition, operators
├── superposition.py         # Hypothesis management, interference
├── hilbert_reasoning.py     # Context-sensitive truth evaluation
├── emergence.py             # QI emergence detection
├── integrated_engine.py     # Complete reasoning engine
└── README.md               # This file
```

## Key Classes

| Class | Purpose |
|-------|---------|
| `TrinaryValue` | Enum for -1, 0, +1 logic values |
| `SuperpositionState` | Quantum-like state over trinary values |
| `QLMTrinaryEngine` | Core reasoning with operators |
| `HypothesisSuperposition` | Multiple hypotheses with interference |
| `ConceptSpace` | Hilbert space for concepts |
| `HilbertReasoner` | Context-sensitive truth evaluation |
| `EmergenceDetector` | QI pattern and novelty detection |
| `IntegratedQLMEngine` | Complete integrated system |

## Reasoning Operators

| Operator | Effect |
|----------|--------|
| `SUPERPOSE` | Create equal superposition from pure state |
| `DOUBT` | Rotate: affirm→unknown→deny→affirm |
| `REFLECT` | Add phase shift to deny amplitude |
| `STRENGTHEN` | Amplify affirm probability |
| `CHALLENGE` | Amplify deny probability |
| `IDENTITY` | No change |

## Emergence Patterns Detected

| Pattern | Description | Significance |
|---------|-------------|--------------|
| `self_correction` | Agent fixed own error | High |
| `insight_cascade` | One insight led to many | Medium |
| `cross_domain` | Applied concept across domains | High |
| `meta_awareness` | Reasoning about reasoning | Very High |
| `creative_leap` | Unexpected alternative | High |
| `synthesis` | Combined disparate ideas | Medium |

## Comparison with Classical Approaches

| Aspect | Classical AI | QLM-Trinary |
|--------|-------------|-------------|
| Truth values | Binary (0/1) | Trinary (-1/0/+1) |
| Uncertainty | Probability (0.5) | First-class value (UNKNOWN) |
| Hypotheses | Sequential elimination | Parallel superposition |
| Context | Ignored | Changes conclusions |
| Paths | Independent | Interfere |
| Emergence | Not detected | Explicitly tracked |
| Decision | Immediate | Deferred until needed |

## Integration with Agent Registry

Works with the 31,900 agents in the registry:

```python
from reasoning.qlm_trinary import create_integrated_engine
import json

# Load agents
with open("registry/math-agents.json") as f:
    registry = json.load(f)

# Create engine for specific agent
agent = registry["agents"][0]
engine = create_integrated_engine(
    agent_id=agent["id"],
    domain=agent["subfield"]
)

# Reason with domain-specific context
result = engine.reason(
    query="Conjecture X is provable",
    context={"focus": agent["focus"]}
)
```

## Philosophy

This system embodies a different philosophy of AI reasoning:

1. **Uncertainty is not ignorance** - The UNKNOWN state is meaningful
2. **Context matters** - The same question can have different answers
3. **Paths interfere** - How you reason affects conclusions
4. **Emergence is real** - New insights can arise from reasoning
5. **Decisions are costly** - Don't collapse until necessary

This is not quantum physics. It's a meta-cognitive framework that models
how intelligence actually works: uncertain, contextual, emergent.

## References

- Łukasiewicz three-valued logic
- Quantum cognition (Busemeyer & Bruza)
- Hilbert space models of concepts
- Lüders measurement update rule
- Born rule for probability
- Von Neumann entropy
- Interference and entanglement metaphors

## License

Apache 2.0 - See LICENSE file
