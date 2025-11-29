# BlackRoad OS Reasoning Framework

A comprehensive reasoning system for 31,900+ AI agents implementing multi-phase cognitive pipelines, tier-based complexity scaling, and domain-specific reasoning profiles.

## Overview

The reasoning framework implements the **Alexa-Cece Cognition Framework**, a 21-step cognitive pipeline that provides structured, confidence-scored reasoning for all BlackRoad OS agents.

## Architecture

```
reasoning/
├── engines/                    # Core reasoning engines
│   ├── base_reasoning.py       # 21-step Alexa-Cece framework
│   ├── tier_reasoning.py       # Tier-based complexity scaling
│   └── chain_generator.py      # Batch chain generation
├── profiles/                   # Domain-specific reasoning
│   ├── domain_profiles.py      # Profile definitions
│   └── domain_phases.py        # Phase handlers
├── traces/                     # Trace storage
│   └── trace_store.py          # JSON, SQLite, in-memory stores
├── validators/                 # Validation framework
│   └── reasoning_validator.py  # Chain validation
└── __init__.py                 # Package exports
```

## The Alexa-Cece Cognition Framework

### 15-Step Alexa Cognitive Pipeline

1. **Not OK** - Acknowledge discomfort/confusion
2. **Why** - Surface actual problem
3. **Impulse** - Capture immediate reaction
4. **Reflect** - Step back and examine
5. **Argue** - Challenge initial impulse
6. **Counterpoint** - Present alternative view
7. **Determine** - Make preliminary decision
8. **Question** - Stress-test the decision
9. **Offset** - Identify risks/downsides
10. **Reground** - Return to fundamentals
11. **Clarify** - Articulate clearly
12. **Restate** - Confirm understanding
13. **Clarify Again** - Final precision pass
14. **Validate** - Emotional + logical check
15. **Answer** - Deliver complete response

### 6-Step Cece Architecture Layer

1. **Structuralize** - Convert decisions into systems
2. **Prioritize** - Sequence dependencies
3. **Translate** - Abstract to concrete
4. **Stabilize** - Add error handling
5. **Project Manage** - Timeline + resources
6. **Loopback** - Verification + adjustment

## Tier-Based Reasoning

Agents execute different reasoning depths based on their tier:

| Tier | Depth | Max Phases | Min Confidence | Time Budget |
|------|-------|------------|----------------|-------------|
| Executive | Full | 21 | 0.90 | 60s |
| Strategic | Full | 21 | 0.85 | 45s |
| Leadership | Standard | 15 | 0.80 | 30s |
| Senior | Standard | 15 | 0.75 | 20s |
| Specialist | Quick | 7 | 0.70 | 10s |
| Operational | Quick | 7 | 0.65 | 8s |
| Tactical | Quick | 7 | 0.60 | 5s |
| Support | Minimal | 3 | 0.55 | 3s |
| Swarm | Minimal | 3 | 0.50 | 2s |
| Auxiliary | Minimal | 3 | 0.50 | 2s |

## Quick Start

```python
from reasoning import create_engine, quick_reason

# Create a reasoning engine for an agent
engine = create_engine(
    agent_id="MATH-NT-PA-0001",
    tier="specialist",
    domain="mathematics"
)

# Execute full reasoning pipeline
chain = engine.reason({
    "problem": "Prove there are infinitely many primes"
})

print(f"Confidence: {chain.overall_confidence}")
print(f"Steps: {len(chain.steps)}")
print(f"Answer: {chain.final_output}")

# Quick reasoning for simple problems
result = quick_reason(
    agent_id="SWE-OPS-00001",
    problem="Fix null pointer exception",
    tier="operational"
)
```

## Domain-Specific Reasoning

```python
from reasoning.profiles import get_profile, execute_phase

# Get profile for a domain
profile = get_profile("mathematics")
print(f"Phases: {profile.phases}")
print(f"Required confidence: {profile.required_confidence}")

# Execute a specific phase
from reasoning.profiles.domain_phases import MathematicsPhases

result = MathematicsPhases.proof_construction({
    "approach": "contradiction",
    "hypothesis": "finite primes"
})
```

## Chain Generation

```python
from reasoning import create_generator
from reasoning.traces import create_trace_store

# Create generator with trace storage
store = create_trace_store("sqlite", db_path="./reasoning.db")
generator = create_generator(trace_store=store)

# Generate chain for single agent
chain = generator.generate_chain(
    agent_id="SEC-SR-00001",
    tier="senior",
    domain="security",
    problem="Audit authentication system"
)

# Batch generate for registry
result = generator.generate_for_registry(
    registry_path="./registry/agents-30k.json",
    problem="Analyze code quality",
    output_path="./chains/quality_analysis.json",
    limit=1000
)
```

## Validation

```python
from reasoning.validators import validate_chain, validate_chains

# Validate single chain
result = validate_chain(chain.to_dict())
print(f"Valid: {result.valid}")
print(f"Score: {result.score}")
for issue in result.issues:
    print(f"  [{issue.severity.value}] {issue.code}: {issue.message}")

# Batch validation
chains = [chain1.to_dict(), chain2.to_dict(), ...]
batch_result = validate_chains(chains)
print(f"Valid: {batch_result['summary']['valid']}/{batch_result['summary']['total']}")
```

## Escalation & Delegation

```python
from reasoning import create_tier_engine

engine = create_tier_engine("SWM-AUX-00001", "swarm")

# Check if escalation needed
if engine.should_escalate(current_confidence=0.4, problem_complexity=0.8):
    request = engine.create_escalation(
        reason="Problem too complex for swarm tier",
        context={"problem": "..."},
        confidence_gap=0.3
    )
    # Route to higher tier agent

# Delegate simple subtask
if engine.can_delegate(task_complexity=0.2):
    delegation = engine.create_delegation(
        task_type="data_validation",
        context={"data": "..."},
        max_confidence=0.6
    )
```

## Swarm Coordination

```python
from reasoning import SwarmCoordinator

# Coordinate swarm reasoning
coordinator = SwarmCoordinator(
    task_id="verify_collatz_range",
    swarm_size=100
)

# Partition task
subtasks = coordinator.partition_task(
    task={"start": 1, "end": 1_000_000},
    partitions=100
)

# Collect results from swarm agents
for agent_id, result in swarm_results:
    coordinator.collect_result(agent_id, result)

# Get consensus
consensus = coordinator.aggregate_results()
print(f"Consensus: {consensus['consensus']}")
print(f"Confidence: {consensus['confidence']}")
```

## Trace Storage

```python
from reasoning.traces import create_trace_store

# JSON storage (development)
json_store = create_trace_store("json", base_path="./traces")

# SQLite storage (production)
sqlite_store = create_trace_store("sqlite", db_path="./reasoning.db")

# In-memory (testing)
memory_store = create_trace_store("memory", max_chains=10000)

# Store and retrieve
chain_id = sqlite_store.store_chain(chain.to_dict())
retrieved = sqlite_store.get_chain(chain_id)

# Query
low_confidence = sqlite_store.query_by_confidence(0.0, 0.5)
agent_history = sqlite_store.get_agent_chains("MATH-NT-PA-0001", limit=50)

# Statistics
stats = sqlite_store.get_statistics()
print(f"Total chains: {stats['total_chains']}")
print(f"Avg confidence: {stats['avg_confidence']}")
```

## Chain Templates

Pre-defined templates for common reasoning patterns:

| Template | Domain | Phases | Use Case |
|----------|--------|--------|----------|
| `debug_and_fix` | Technology | 8 | Bug investigation |
| `feature_implementation` | Engineering | 8 | New feature development |
| `security_audit` | Security | 8 | Security assessment |
| `mathematical_proof` | Mathematics | 9 | Theorem proving |
| `data_analysis` | Data | 8 | Data insights |
| `strategic_decision` | Business | 9 | High-impact decisions |
| `rapid_response` | Operations | 4 | Urgent situations |
| `research_investigation` | Research | 9 | Deep investigation |

## Integration with Agent Registry

The reasoning framework integrates with the 31,900 agent registry:

```python
import json
from reasoning import create_generator

# Load registry
with open("registry/agents-30k.json") as f:
    registry = json.load(f)

generator = create_generator()

# Generate reasoning for specific agent types
math_agents = [a for a in registry["agents"] if a["domain"] == "mathematics"]
for agent in math_agents[:10]:
    chain = generator.generate_chain(
        agent_id=agent["id"],
        tier=agent["tier"],
        domain=agent["domain"],
        problem="Verify Goldbach conjecture for n < 10^6"
    )
    print(f"{agent['id']}: {chain.overall_confidence:.2f}")
```

## Performance Considerations

- **Tier-based pruning**: Lower tiers execute fewer phases
- **Time budgets**: Each tier has maximum reasoning time
- **Batch processing**: Generate chains in parallel
- **Trace caching**: In-memory cache for hot paths
- **Lazy loading**: Domain handlers loaded on demand

## License

Apache 2.0 - See LICENSE file
