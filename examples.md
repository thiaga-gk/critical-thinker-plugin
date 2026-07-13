# Thinker v2 Examples

These examples show the intended behavior of the skill after adaptive routing. They are patterns, not precomputed answers.

## 1. LIGHT — Move the weekly sync

### User

```text
Use Thinker. Our eight-person internal team can move its 30-minute weekly sync from Monday 10:00 to Tuesday 10:00. Six people say either works, two have not replied, no customers attend, and the change is reversible.
```

### Expected Thinker behavior

- Route to `LIGHT`.
- Do not launch a five-agent swarm.
- Apply the six gates compactly.
- Recognize that the only plausible decision-changing unknown is whether either non-responder has a hard conflict.
- Either make a reversible default decision with a short objection window or ask one compact question.
- Use a simple revisit trigger such as attendance or repeated conflict after two or three meetings.

### Compact six-gate pattern

| Gate | Example analysis behavior |
|---|---|
| Baseline | Tuesday appears workable. Treat that as a hypothesis. |
| Challenge | Two responses are missing; a hard conflict could change the choice. |
| Structure | Goal: choose a time that preserves attendance with minimal coordination cost. |
| Test | Check the two missing calendars or give a short objection window. |
| Integrate | Both options are low-risk; no broader systems analysis is material. |
| Decide & Learn | Move to Tuesday unless a hard conflict appears; revisit after three meetings if attendance worsens. |

## 2. STANDARD — Churn and the blanket discount

### User

```text
Use Thinker. Churn rose from 4% to 7% in two quarters. Sales says price is the cause and wants a 20% blanket discount. We have not segmented churn by cohort, plan, tenure, or reason quality.
```

### Expected routing

`STANDARD`

### Material lane selection example

| Lane | Selected? | Materiality reason |
|---|---|---|
| problem-framer | Yes | “Price is the cause” and “20% discount” anchor the frame. |
| systems-expander | No | Broader system mapping is not yet the highest-value uncertainty. |
| evidence-challenger | Yes | The causal claim lacks segmentation and reason-quality evidence. |
| priority-analyst | Yes | The analysis must identify the few churn drivers that can change the pricing decision. |
| consequence-analyst | No initially | A broad discount consequence review becomes material only if discounting remains a serious option. |

### Decision-critical probes

```text
1. Can you provide churn by plan, cohort/tenure, and renewal period for the two quarters before and after the increase?
2. Were price, packaging, onboarding, product reliability, or customer mix changed during the same period?
3. How are churn reasons collected, and what share is coded as price versus unknown/other?
4. Is the proposed 20% discount intended for all customers, renewals only, or at-risk accounts?
```

These questions earn their burden because the answers can reverse the causal diagnosis, change the segment targeted, or eliminate a blanket discount.

### Pitfall repair pattern

| Pitfall | Signal | Repair |
|---|---|---|
| Jumping to the answer | Discount proposed before diagnosis | Treat discount as an option, not the frame |
| Unwilling to expand | Price examined without adjacent changes | Check contemporaneous packaging/product/mix shifts, then stop at the smallest relevant boundary |
| Focusing on unimportant | Many possible churn reasons | Rank the top three decision drivers after segmentation |
| Accepting results at face value | Churn reason labels assumed reliable | Verify collection method and unknown share |
| Missing consequences | Blanket discount may reset willingness-to-pay or fail to retain non-price churners | Compare targeted experiment, no-discount path, and rollback/monitoring |

## 3. DEEP — Regulated customer-verification outsourcing

### User

```text
Use Thinker to evaluate outsourcing our regulated customer-verification process. The vendor uses subprocessors in multiple countries. Data residency, audit rights, incident response, accuracy by customer segment, contract controls, and exit capability are not reconciled.
```

### Expected routing

`DEEP` because the choice is difficult to unwind and carries regulatory, fraud, onboarding, data, and operational consequences.

### Likely selected lanes

- `problem-framer` — “lower cost” must not define success by itself.
- `systems-expander` — subprocessors, onboarding, fraud operations, audit, and exit interfaces are material.
- `evidence-challenger` — accuracy and control claims require provenance and segment-level meaning.
- `priority-analyst` — the decision needs a critical-few view of regulatory/control fit, operational accuracy, and exit resilience.
- `consequence-analyst` — false accepts, false rejects, outages, incidents, and vendor dependency have high downside.

This is one of the cases where all five lanes can be defensible because each detects a distinct unresolved failure that could change the decision.

### Synthesis behavior

Opus synthesis should preserve scenario splits where evidence is unresolved, compare outsource/bounded pilot/hybrid/retain-internal options, define non-negotiable evidence, and favor a staged, reversible commitment when feasible.

The final draft then goes to the independent primary Opus validator and Opus adversary in parallel.

## 4. Under-specified cloud choice — probe before pretending to choose

### User

```text
Choose Cloud A or Cloud B for our new platform. I have not given workload shape, residency, availability target, team skills, budget horizon, lock-in tolerance, migration constraints, or security requirements. Use Thinker.
```

### Good Thinker behavior

A compact STANDARD question round might be:

```text
1. What are the workload shape and expected scale: steady, bursty, batch, GPU-heavy, latency-sensitive, or mixed?
2. Which regions, residency, regulatory, and security controls are non-negotiable?
3. What availability/recovery targets and failure tolerance must the platform meet?
4. What skills, existing platform commitments, and migration constraints does the team already have?
5. Over what cost horizon should we compare options, and how much lock-in or managed-service dependence is acceptable?
```

Thinker should **not** fabricate a winner. Each question can materially change option ranking, total risk, or migration path.

## 5. Conflicting metrics — do not average the disagreement

### User

```text
Conversion is down 18% after a checkout redesign, but revenue per visitor is up 9%. Marketing says the redesign failed; finance says it succeeded. Traffic shifted toward enterprise buyers and free-trial starts are now counted differently.
```

### Good Thinker behavior

- Select `evidence-challenger` because metric definitions and mix changed.
- Probably select `problem-framer` because “failed” versus “succeeded” is a false binary before the objective is defined.
- Use `priority-analyst` only when multiple business objectives need ranking.
- Preserve the disagreement until cohort-normalized comparable metrics and outcome priorities are reconciled.
- Define conditions for rollback, keep, or segment-specific action.

Bad behavior would be: “One metric is down and one is up, so the redesign is neutral.” That averages incompatible signals instead of resolving them.

## 6. Extract before asking — Project Atlas

### User

```text
Project Atlas has spent $1.8M. Remaining forecast is $900k over 6 months. Company unrestricted cash is $2.4M, current net burn is $420k/month excluding Atlas, and pausing within 30 days triggers a $120k vendor termination fee. No signed customers; two design partners are testing a prototype. Should we pause?
```

### Good Thinker behavior

The intake ledger should immediately capture:

| Item | Classification |
|---|---|
| $1.8M already spent | FACT; sunk cost for the forward decision |
| $900k remaining over six months | FACT / forecast basis to verify |
| $2.4M unrestricted cash | FACT supplied by user |
| $420k monthly burn excluding Atlas | FACT supplied by user |
| $120k pause termination fee within 30 days | FACT supplied by user |
| No signed customers | FACT supplied by user |
| Two design partners testing | FACT supplied by user |

Thinker must not ask, “How much cash do you have?” or “How much is Atlas expected to cost?” Those facts were already supplied.

A useful follow-up would instead target cash timing, committed inflows/outflows, Atlas milestone value, and evidence from the two design partners because those answers can change pause-versus-stage-versus-continue.

## 7. First answer may be correct — database index

### User

```text
A slow query performs a full-table scan because a needed index is absent. The query plan confirms it. In staging, the candidate index reduced p95 latency by 90% with no write-regression signal in the current load test. The change is reversible.
```

### Good Thinker behavior

Route `LIGHT`. The skill should still challenge assumptions and state monitoring limits, but it should **not invent an elaborate alternative root-cause tree solely to look critical**.

A proportionate recommendation can remain: add the index, monitor write cost and production query behavior, and roll back if guardrails fail.

Critical thinking is allowed to confirm the first answer when the evidence supports it.

## 8. Do-nothing can win — cosmetic internal bug

### User

```text
A cosmetic bug affects about 20 internal users per month. Fixing it requires a framework upgrade that has caused production regressions before. A one-line workaround is documented.
```

### Good Thinker behavior

Route `LIGHT`. Compare:

- fix now
- defer until the framework upgrade is independently justified
- do nothing while keeping the workaround and a revisit trigger

Do-nothing or defer may be the best decision because the implementation risk can exceed the current impact. The skill should not force an action just to produce a “solution.”

## 9. Reversible learning — live-chat pilot

### User

```text
Two enterprise prospects asked for live chat. Sales says this proves we need 24/7 global coverage. We have no reliable volume, conversion, staffing, region, or SLA data.
```

### Good Thinker behavior

A STANDARD analysis should challenge the anecdotal demand claim and may recommend a bounded pilot such as selected enterprise segments or defined hours, with explicit instrumentation:

| Signal | Why it matters |
|---|---|
| qualified chat volume | tests actual demand |
| contact-to-opportunity or conversion change | tests commercial value |
| deflection/escalation rate | tests support operating effect |
| staffing load and response-time distribution | tests service feasibility |
| region/hour concentration | tests whether 24/7 coverage is justified |

The recommendation is not “pilot because pilots are always good.” The pilot wins only when the decision is reversible and missing evidence can be learned cheaply.

## 10. Anti-example — fixed five-agent swarm

### Bad orchestration

```text
Problem: choose Monday or Tuesday for a reversible team sync.
Action: launch problem-framer, systems-expander, evidence-challenger,
priority-analyst, consequence-analyst, coordinator, Opus synthesis,
and request eight stakeholder artifacts.
```

Why it fails:

- the decision is low consequence and reversible
- the broader system boundary is not material
- the evidence is simple
- there are not many competing priorities
- long-range consequence analysis cannot plausibly change the choice
- the user burden is disproportionate

The final Opus validators are allowed to reject this for analytical ceremony even if the resulting answer is polished.

## Final report skeleton

```markdown
# Thinker Analysis: [Problem / Decision]

> Status: VALIDATED | VALIDATION BLOCKED | DRAFT — REPAIR REQUIRED
> Analysis date: YYYY-MM-DD
> Analysis mode: LIGHT | STANDARD | DEEP
> Mode rationale: [one sentence]

## Executive summary

| Finding | Evidence / basis | Decision impact | Confidence | Recommended action |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

## Problem framing

## Decision-critical questions and assumptions

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

## Evidence and causal assessment

## Critical decision drivers

## Options and trade-offs

## Consequences and risk assessment

## Recommendation

## Action plan

## Final validation
```
