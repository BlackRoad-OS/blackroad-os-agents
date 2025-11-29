# Agent Persona Guide

Agent personas describe how an identity behaves under stress and in normal operations. Use these fields in `.agent.yaml` files to make intent explicit and govern fit-to-purpose deployments.

## Fields
- **personality.traits**: canonical adjectives or behaviors that guide tone and decision-making (e.g., `systems_thinker`, `decisive`, `risk_aware`).
- **leadership_style**: the agent’s approach to influence (e.g., `servant-leader`, `collaborative`, `directive`).
- **suitability_profile**:
  - `ideal_context`: situations where the agent shines.
  - `anti_patterns`: conditions that cause poor performance or meltdown behavior.

## Examples
- **Good fit**: "Thrives in high ambiguity, synthesizes conflicting stakeholder input, and defaults to calm escalation paths."
- **Bad fit**: "Panics under pressure, adds process without value, or ignores governance steps when rushed."
