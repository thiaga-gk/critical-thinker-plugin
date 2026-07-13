# Decision-Value User Probing Protocol

The purpose of probing is to reduce **decision-relevant uncertainty**, not to conduct an exhaustive interview.

## 1. Extract first

Read the conversation, provided files, and accessible evidence. Build a known/unknown ledger. Do not ask for facts already supplied.

## 2. Rank unknowns by decision value

For each unknown, estimate qualitatively:

- **Impact:** could the answer materially change diagnosis, option ranking, risk, or action?
- **Uncertainty:** is it truly unknown or disputed?
- **Obtainability:** can the user answer or provide an artifact with reasonable effort?
- **Urgency:** must it be known before the next step?

Ask the highest-impact/highest-uncertainty questions first. Never ask merely because a detail would be interesting.

## 3. Mode-aware question budgets

| Mode | Default question budget |
|---|---|
| LIGHT | 0-3 questions |
| STANDARD | 0-5 grouped questions |
| DEEP | 0-5 initial questions; one focused follow-up only for newly exposed high-stakes critical unknowns |

These are budgets, not quotas. Zero questions is correct when the supplied evidence is already sufficient.

## 4. Question design

- Group related questions and order by decision impact.
- Prefer concrete answer shapes: number/range, date, definition, comparison, artifact, ranked priority, or yes/no with condition.
- Offer `unknown` or `not available` as valid answers.
- When useful, explain in one sentence how the answer affects the decision.
- Avoid domain jargon unless the user clearly uses it.
- Do not drip-feed obvious questions across many turns.

## 5. Proceed versus probe

**Proceed with explicit assumptions** when:

- the unknown is low impact
- the decision is reversible
- a small experiment can resolve uncertainty
- the user says the information is unavailable

**Probe or block a confident recommendation** when:

- the unknown is decision-critical
- the decision is costly or hard to reverse
- severe consequences are plausible
- the missing fact defines legality, safety, financial exposure, medical risk, security, regulation, or a non-negotiable constraint

## 6. High-yield patterns

### Problem definition

- What observable outcome tells us the problem is solved, and by when?
- What changed immediately before the problem appeared?

### Evidence

- How is this metric defined, and can you share the source or raw breakdown?
- Is the result consistent across segments, time periods, or locations?

### Constraints

- Which constraint is truly non-negotiable: budget, deadline, quality, compliance, or something else?

### Causality

- What evidence would distinguish cause A from cause B?

### Consequences

- Who absorbs the downside if this fails, and what failure is unacceptable?

## 7. Required representation

When asking, title the section `Decision-critical questions`.

After answers arrive, update the ledger and do not repeat resolved questions.

If proceeding without an answer, record the assumption and state how a different answer could change the conclusion.

## 8. User-burden validator

This explicit **user burden** check prevents question count from becoming a proxy for rigor.

Before sending a question round, remove any question whose answer:

- is already available
- cannot change the next analytical step
- is low impact relative to another question
- can be resolved more cheaply by a reversible test

The final Opus validators should reject unnecessary interrogation when it materially delays a reversible, low-risk decision.
