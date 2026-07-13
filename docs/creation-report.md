# Thinker Skill v2 Creation and Upgrade Report

> Version: 2.0.0  
> Build status: **STATIC DESIGN VALIDATION PASSED 10/10 — RUNTIME BEHAVIORAL BENCHMARK NOT EXECUTED IN THIS ENVIRONMENT**

## Executive summary

Thinker v2 applies the accepted redesign recommendations to reduce orchestration tax while preserving disciplined critical thinking. The package now routes work to LIGHT, STANDARD, or DEEP depth; selects specialist agents only when a material lane test shows they can change the decision; uses operational six-gate names; adds anti-ceremony and user-burden validation; and includes a 30-case, 120-run behavioral benchmark protocol.

| Finding | Evidence / basis | Decision impact | Confidence | Recommended action |
|---|---|---|---|---|
| Fixed-depth reasoning was too expensive for simple problems | Previous default orchestration favored a five-lane wave | High | High | Use LIGHT/STANDARD/DEEP routing and select the lowest safe mode |
| Specialist lanes should be conditional, not a quota | Many cases do not need all five analytical methods | High | High | Apply the material lane test before every spawn |
| “Master thinker” is better treated as work, not a person label | Operational gate language is clearer and less status-laden | Medium | High | Use Baseline, Challenge, Structure, Test, Integrate, Decide & Learn while retaining source mapping |
| Final validation must detect over-analysis as well as under-analysis | Extra questions and agents can burden users without changing decisions | High | High | Validate mode proportionality, lane materiality, user burden, and anti-ceremony |
| Static correctness does not prove decision improvement | Package structure and prompts cannot establish behavioral lift | High | High | Run the 30-case × 4-variant benchmark before claiming empirical production quality |
| Model roles should be explicit and auditable | Aliases or inherited models make role-level policy harder to inspect | High | High | Pin Sonnet 5 for the floor and Opus 4.8 for high-complexity synthesis/final gates |

## Package architecture

```text
Sonnet 5 Thinker skill
  -> extract supplied facts
  -> route LIGHT / STANDARD / DEEP
  -> probe only decision-critical unknowns
  -> material lane test
  -> selected Sonnet 5 specialist lanes in parallel
  -> coordinator only when complexity warrants it
  -> Sonnet 5 inline synthesis for LIGHT/simple STANDARD
     or Opus 4.8 synthesis for DEEP/conflicted work
  -> docs/thinker-<slug>.md
  -> independent parallel Opus 4.8 validator + adversary
  -> repair and rerun both when rejected
  -> Opus 4.8 arbiter on persistent material disagreement
  -> VALIDATED or fail-closed VALIDATION BLOCKED
```

## Detailed redesign

### 1. Adaptive depth routing

Three modes were added:

| Mode | Problem profile | Questions | Lane guidance | Synthesis |
|---|---|---:|---:|---|
| LIGHT | Narrow, reversible, low downside, adequate facts | 0-3 | 0-1 | Sonnet 5 inline |
| STANDARD | Moderate ambiguity/impact, multiple options, uncertain evidence | 0-5 grouped | 2-3 | Sonnet 5; Opus 4.8 when conflict/coupling remains |
| DEEP | Severe downside, difficult to reverse, regulated/high-stakes, systemic or severely conflicted | 0-5 initial plus one focused high-stakes follow-up | 3-5 | Opus 4.8 xhigh |

Routing chooses the lowest mode that remains safe. New evidence can escalate the mode; de-escalation requires evidence that removes the reason for higher depth.

### 2. Adaptive lane selection

The previous fixed default five-lane wave was removed. The skill now asks two questions for every candidate specialist:

1. Is the lane's core analytical question unresolved?
2. Could a plausible answer materially change diagnosis, option ranking, risk, or action?

A lane runs only when both are true. The report records selected and skipped lanes with a materiality rationale.

The five available methods remain:

- problem framing
- systems expansion
- evidence challenge
- critical-few prioritization
- consequence analysis

Parallelism is therefore a tool for independence and coverage rather than a measure of sophistication.

### 3. Six operational gates

The six source levels are retained but expressed as work gates:

| Gate | Source level |
|---|---|
| Baseline | Level 1 — Unreflective thinker |
| Challenge | Level 2 — Challenged thinker |
| Structure | Level 3 — Beginning thinker |
| Test | Level 4 — Practicing thinker |
| Integrate | Level 5 — Advanced thinker |
| Decide & Learn | Level 6 — Master thinker |

All six gates apply in every mode. LIGHT compresses them; DEEP requires substantive evidence and conflict resolution.

### 4. Five-pitfall repair controls

Each common problem-solving pitfall now has explicit signals and repair controls. The systems expansion repair also requires returning to the **smallest decision-relevant boundary**, which prevents the cure for narrow framing from becoming an unbounded stakeholder map.

The prioritization layer prefers no more than three primary decision drivers unless the domain genuinely requires more. Evidence analysis explicitly distinguishes correlation, mechanism, and causal inference. Consequence analysis is proportional and separates decision-relevant failure paths from merely imaginable remote branches.

### 5. Decision-value probing

The probing reference is now mode-aware. Thinker extracts available information before asking and scores unknowns by their ability to change diagnosis, option ranking, risk, or action.

Question budgets are enforced by mode and final validators now inspect user burden. High-stakes missing facts cannot be silently assumed; non-critical unknowns may be carried transparently as assumptions.

### 6. Anti-overengineering validation

Before adding a question, agent, or section, the skill asks:

> What decision-relevant failure could this step detect that the current analysis has not already covered?

When the answer is unclear, the step is omitted.

The two independent Opus validators now check fourteen dimensions, including mode correctness, material lane selection, proportional user questions, and anti-ceremony. A report can fail because it is too elaborate for the decision as well as because it is too shallow.

### 7. Model policy

| Role | Configured model |
|---|---|
| Skill, intake, routing, probing | `claude-sonnet-5` |
| Specialist lanes | `claude-sonnet-5` |
| Coordinator | `claude-sonnet-5` |
| Complex synthesis | `claude-opus-4-8` |
| Primary final validator | `claude-opus-4-8` |
| Adversarial validator | `claude-opus-4-8` |
| Arbiter | `claude-opus-4-8` |
| Blind benchmark judge | `claude-opus-4-8` |

No configured role uses Haiku, `inherit`, a generic family alias, or a model below Sonnet 5.

### 8. Behavioral benchmark

The new benchmark contains 30 cases and four variants:

```text
BASELINE / LIGHT / STANDARD / DEEP
30 cases x 4 variants = 120 runtime runs
```

The suite covers reversible choices, do-nothing wins, a first-answer-correct case, under-specification, anchoring, conflicting data, changed metric definitions, local optimization, incentives, quality risk, regulated outsourcing, medical disagreement, urgent security, financial downside, policy scaling, and high-coupling build-versus-buy decisions.

The blind Opus judge scores ten quality metrics from 0 to 4:

- critical unknown discovery
- unsupported assumption control
- premature recommendation control
- causal quality
- evidence traceability
- confidence calibration
- actionability
- consequence coverage
- critical-few focus
- proportionality

Telemetry separately records input/output tokens, latency, model calls, user question count, lane count, and recommendation signature.

The benchmark harness can generate the full run plan and summarize collected runtime records. It does not call Anthropic models itself.

## Why the redesign is stronger

The v1 concept correctly resisted anchoring, preserved disagreements, and separated synthesis from final validation. Its largest weakness was orchestration tax: a highly structured five-lane pipeline could be justified for a regulatory outsourcing decision but wasteful for a reversible meeting-time choice.

V2 makes the same intellectual disciplines **proportional**. The six gates remain universal; the ceremony does not. Specialist agents are now hypotheses about what analysis could matter, and each must earn execution through a materiality test. The final validators are empowered to reject empty sophistication.

This is the main architectural improvement: Thinker no longer equates more agents with more thinking.

## Static validation result

The package validator checks ten declared design gates:

1. Adaptive LIGHT/STANDARD/DEEP modes.
2. Six operational gates with source-framework mapping.
3. Five-pitfall repair controls.
4. Decision-value probing.
5. Adaptive material lane selection.
6. No default five-lane swarm.
7. Pinned Sonnet 5 model floor.
8. Dual independent Opus 4.8 final validation.
9. 30-case behavioral benchmark framework.
10. Markdown report contract with mode, lane ledger, and executive-summary findings table.

The actual static validation result is:

```text
PASS: Thinker package static validation succeeded.
PASS: SKILL.md lines=208 (<500).
PASS: agent model policy verified for 11 agents; only pinned Sonnet 5 and Opus 4.8 are configured.
PASS: final validator/adversary/arbiter are pinned to claude-opus-4-8.
PASS: 8 core eval cases and 30 behavioral benchmark cases loaded.
PASS: docs/ Markdown report contract includes analysis mode, lane-selection ledger, and executive-summary findings table.
PASS: design acceptance score 10/10.
```

The build process also compiles the Python scripts, validates eight core skill evals, validates exactly 30 behavioral benchmark cases, and confirms that the benchmark plan expands to 120 runs.

## Limitation and honest score

**Package design/static acceptance: 10/10 against the ten explicit gates above.**

**Empirical production quality: not yet scored.** This environment does not expose a Claude Code Agent runtime or Anthropic model endpoint with which to execute the 120-run benchmark and real Opus final reviews. Therefore this report does not claim that Thinker has demonstrated 10/10 decision quality in production.

The benchmark was added specifically to turn that claim into a testable result. The responsible next evidence milestone is to execute the 120 runs, collect blind judge scores and telemetry, inspect recommendation stability, and refine routing thresholds based on observed failures rather than aesthetic preference.
