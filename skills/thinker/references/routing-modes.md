# Adaptive Depth Routing: LIGHT, STANDARD, DEEP

The purpose of routing is to spend reasoning effort where it changes the decision. **All six work gates and all five pitfall checks still apply in every mode.** Mode changes the depth and orchestration, not the intellectual disciplines.

## Routing rule

Select the lowest mode that is still safe for the decision.

### LIGHT

Use LIGHT only when all of the following are broadly true:

- downside is low to moderate
- decision is easy to reverse or cheaply test
- problem boundary is narrow
- facts are mostly adequate and not materially conflicting
- no regulated, medical, legal, safety, security, or major financial exposure is central
- there is no credible path where a wrong answer causes disproportionate harm

Typical examples: meeting cadence, low-risk process tweaks, reversible feature defaults, naming conventions, small pilots with clear rollback.

**Execution budget**

| Dimension | LIGHT default |
|---|---|
| Questions | 0-3 |
| Specialist lanes | 0-1, often inline |
| Six gates | concise; usually 1-2 sentences each |
| Synthesis | Sonnet 5 inline |
| Final validation | dual independent Opus 4.8 gate |

### STANDARD

Use STANDARD when any meaningful ambiguity or moderate consequence remains, especially:

- multiple viable options exist
- evidence quality or metric meaning is uncertain
- a proposed solution may be anchoring the frame
- cross-team dependencies or system interfaces matter
- causal diagnosis is not obvious
- medium cost, customer impact, or organizational consequences are plausible

**Execution budget**

| Dimension | STANDARD default |
|---|---|
| Questions | 0-5 grouped |
| Specialist lanes | 2-3 selected adaptively and run in parallel |
| Six gates | full but concise |
| Synthesis | Sonnet 5 if lanes align; Opus 4.8 if conflicts/coupling remain |
| Final validation | dual independent Opus 4.8 gate |

### DEEP

Use DEEP when one or more of these triggers is present:

- decision is costly or hard to reverse
- severe safety, legal, medical, security, regulatory, financial, or reputational consequences are plausible
- evidence materially conflicts or key sources are unreliable
- the problem spans multiple systems, business units, incentives, or long time horizons
- a wrong answer is likely to produce second-order harm or perverse incentives
- urgent action is required despite major uncertainty
- the decision involves a broad rollout, large capital commitment, personnel action with significant consequences, or policy change

**Execution budget**

| Dimension | DEEP default |
|---|---|
| Questions | 0-5 initial; one focused follow-up only for newly exposed high-stakes unknowns |
| Specialist lanes | 3-5 selected adaptively and run in parallel |
| Coordinator | recommended for multi-domain/context-heavy work |
| Six gates | substantive evidence, counterexamples, and conflict resolution |
| Synthesis | Opus 4.8 `synthesis-analyst`, xhigh effort |
| Final validation | dual Opus 4.8; arbiter on persistent material disagreement |

## Fast routing test

Ask in this order:

1. **Could a wrong answer cause severe or hard-to-reverse harm?** If yes -> DEEP.
2. **Are decision-driving facts materially disputed, unreliable, or absent?** If severe -> DEEP; otherwise STANDARD.
3. **Does the answer depend on multiple systems, incentives, or stakeholders?** If strongly coupled -> DEEP; otherwise STANDARD.
4. **Are there multiple plausible causal stories or viable options?** -> STANDARD.
5. **Is the decision narrow, reversible, and adequately specified?** -> LIGHT.

## Escalation and de-escalation

Escalate immediately when new evidence reveals higher consequence, systemic coupling, or material conflict.

De-escalate only when the reason for the higher mode has been removed by evidence. Do not de-escalate merely to save tokens after a high-risk trigger is discovered.

## Anti-overengineering test

Before spawning an agent or adding a section, ask:

> What decision-relevant failure could this step detect that the current analysis has not already covered?

If the answer is unclear, do not add the step.

The final validators should reject a LIGHT or STANDARD report that uses obviously unnecessary multi-agent ceremony without a materiality rationale.
