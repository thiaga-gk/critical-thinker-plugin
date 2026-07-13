# Final Markdown Report Contract

Write the completed report to `docs/thinker-<problem-slug>.md`.

The structure is proportional by mode. Required headings are shown below; LIGHT may keep sections compact or use the six-gate table.

```markdown
# Thinker Analysis: [Problem / Decision]

> Status: VALIDATED | VALIDATION BLOCKED | DRAFT — REPAIR REQUIRED
> Analysis date: YYYY-MM-DD
> Analysis mode: LIGHT | STANDARD | DEEP
> Mode rationale: [one sentence]

## Executive summary

[2-5 sentence decision-oriented summary]

| Finding | Evidence / basis | Decision impact | Confidence | Recommended action |
|---|---|---|---|---|
| ... | ... | High/Medium/Low | High/Medium/Low | ... |

## Problem framing
### Decision / problem statement
### Success criteria
### Scope and constraints
### Stakeholders and time horizon

## Decision-critical questions and assumptions
| Item | Type | Status / answer | How it could change the conclusion |
|---|---|---|---|

## Analysis routing and lane selection
| Lane | Selected? | Materiality reason |
|---|---|---|
| problem-framer | Yes/No | ... |
| systems-expander | Yes/No | ... |
| evidence-challenger | Yes/No | ... |
| priority-analyst | Yes/No | ... |
| consequence-analyst | Yes/No | ... |

## Six-gate critical-thinking analysis
### Gate 1 — Baseline
### Gate 2 — Challenge
### Gate 3 — Structure
### Gate 4 — Test
### Gate 5 — Integrate
### Gate 6 — Decide & Learn

## Five-pitfall audit
| Pitfall | Status | Evidence / signal | Repair or control |
|---|---|---|---|

## Evidence and causal assessment
### Evidence ledger
| Material claim | Classification | Source / basis | Verification | Confidence |
|---|---|---|---|---|

### Leading causal story
### Credible alternatives / counterexamples
### What evidence would most change the view
### Quantitative self-verification
[Required when the analysis contains numbers, formulas, thresholds, algorithms, or a worked example. State that load-bearing figures were re-derived and that any worked example was reproduced through its own stated method — and note what was checked. Omit only when the analysis is genuinely non-quantitative.]

### Known gaps / not modeled
[Required. What decision-relevant dimensions, options, stakeholders, failure modes, or data sources were deliberately not modeled, and why they do not change the recommendation — the output of the completeness sweep. "None material" is an acceptable entry only after an explicit sweep.]

## Critical decision drivers
| Rank | Driver | Why it matters | Sensitivity / what could change it |
|---|---|---|---|

## Options and trade-offs
| Option | Benefits | Costs / trade-offs | Risks | Reversibility | Best when |
|---|---|---|---|---|---|

## Consequences and risk assessment
### Short-term direct effects
### Long-term / second-order effects
### Pre-mortem and failure modes
### Controls, monitoring, and rollback

## Recommendation
### Recommended decision
### Why
### Confidence and uncertainty
### Revisit triggers

## Action plan
| Priority | Action | Owner | Timing | Evidence / success signal |
|---|---|---|---|---|

## Final validation
| Validator | Model | Decision | Key notes |
|---|---|---|---|
| final-opus-validator | claude-opus-4-8 | ... | ... |
| final-opus-adversary | claude-opus-4-8 | ... | ... |
| crossmodel-adversary (DEEP) | claude-fable-5 (or claude-sonnet-5 fallback) | ... | ... |

List each reviewer's **actual** model so the panel's **model diversity** is auditable. In DEEP the panel must include a different-family reviewer (Fable 5 preferred, Sonnet 5 fallback — both different families than Opus 4.8); see `opus-validation.md`.

### Validation resolution
[Explain repairs, agreement, cross-model decorrelation catches, or arbiter decision.]
```

## LIGHT compression option

For LIGHT mode, replace the six dedicated gate subsections with:

| Gate | Key conclusion / action |
|---|---|
| Baseline | ... |
| Challenge | ... |
| Structure | ... |
| Test | ... |
| Integrate | ... |
| Decide & Learn | ... |

Other required content may be concise, but the mode rationale, lane-selection ledger, pitfall audit, evidence/assumption handling, recommendation, and Opus validation status remain mandatory.

## Report rules

- The executive summary must contain the findings table.
- State mode and one-sentence routing rationale.
- Include selected and skipped lane rationale; do not pretend skipped lanes ran.
- Show facts, claims, assumptions, and preferences distinctly when material.
- Each material conclusion should trace to evidence, user input, calculation, or labeled assumption.
- Prefer no more than three critical decision drivers unless the domain requires more.
- Do not invent owners, dates, metrics, or precision; use `TBD` where necessary.
- Do not label a report `VALIDATED` unless the Opus gate passes.
- When the user asks for a shorter result, keep the full report file and summarize concisely in chat.
