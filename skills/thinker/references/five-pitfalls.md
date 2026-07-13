# Five Problem-Solving Pitfalls and Repair Controls

Run this audit before final synthesis. A pitfall is `not detected`, `detected and repaired`, or `unresolved`. Any decision-critical unresolved pitfall blocks final approval.

## 1. Jumping to an answer too quickly

**Signals**

- a solution appears before a neutral problem statement
- the user's proposed answer is repeated as the default
- assumptions are not explicit
- no causal alternatives or root-cause path exists
- urgency substitutes for understanding

**Repair**

Capture the initial answer in Baseline as a hypothesis. Reframe neutrally, surface assumptions, and identify plausible causal alternatives before durable solutioning.

**Validator question:** Could a different root cause make the proposed solution ineffective or harmful?

## 2. Being unwilling to expand the problem

**Signals**

- only one team, process step, stakeholder, or time horizon is considered
- upstream causes and downstream effects are absent
- local optimization is treated as system improvement
- adjacent constraints or incentives are ignored

**Repair**

Move the boundary one step upstream, downstream, and outward. Inspect interfaces, incentives, and feedback loops. Then return to the **smallest decision-relevant boundary** so the report does not become a systems laundry list.

**Validator question:** What important factor appears when the boundary moves one step upstream, downstream, or outward?

## 3. Focusing on the unimportant

**Signals**

- a long list has no ranking
- effort follows data availability rather than decision impact
- vivid anecdotes dominate broader patterns
- symptoms receive more attention than the critical few causes

**Repair**

Rank by decision impact, evidence strength, controllability, urgency, and reversibility. Use Pareto logic only when supported. Identify no more than three critical decision drivers unless the domain genuinely requires more, and state what is deliberately deprioritized.

**Validator question:** If only three findings remained, would the recommendation stay the same?

## 4. Accepting results at face value

**Signals**

- dashboards, metrics, model outputs, or reports are self-validating
- definitions, denominators, sampling, timestamps, or provenance are missing
- one source carries the key conclusion
- correlation is called cause without a mechanism or design
- no disconfirming evidence is sought
- **your own** numbers, formulas, or worked examples are asserted but never traced/reproduced

**Repair**

Verify provenance, definitions, calculations, timing, consistency, and interpretation. Seek an independent signal or counterexample when feasible. Separate correlation, mechanism, and causal inference. **This applies to the analysis's own quantitative content**: re-derive load-bearing numbers and run any worked example through its own stated method (see the Test-gate quantitative self-verification in `six-levels.md`). Face-value acceptance of your own algorithm is the same pitfall as face-value acceptance of a dashboard.

**Validator question:** What measurement, definition, interpretation, or calculation error — including in the report's *own* numbers — could reverse the conclusion?

## 5. Not thinking through consequences

**Signals**

- implementation is recommended without risks or side effects
- only benefits are described
- delayed, second-order, or stakeholder effects are absent
- incentives may undermine the solution
- rollback, monitoring, or failure triggers are missing

**Repair**

Run a proportional pre-mortem. Inspect short/long, direct/indirect, positive/negative effects; incentives; transition risk; failure paths; monitoring; and rollback.

**Validator question:** Imagine the recommendation failed badly six months later. What is the most credible decision-to-failure path?

## Audit format

| Pitfall | Status | Evidence / signal | Repair or control |
|---|---|---|---|
| Jumping too quickly | ... | ... | ... |
| Narrow problem boundary | ... | ... | ... |
| Focusing on unimportant issues | ... | ... | ... |
| Accepting results at face value | ... | ... | ... |
| Ignoring consequences | ... | ... | ... |

The audit should show real defects and repairs. Do not mark every pitfall `not detected` merely because the final prose is polished.

## Scope-completeness addendum (the sixth blind spot)

The five pitfalls above all critique **what is present**. They do not catch a decision-relevant dimension, option, stakeholder, or question that was **never modeled at all** — a report can pass every pitfall and still answer the wrong or a too-narrow problem. In DEEP mode (and whenever scope completeness is uncertain) run an explicit completeness sweep — the `completeness-critic` lane — that attacks absence, and record its material gaps.

**Validator question:** What decision-relevant dimension, option, stakeholder, failure mode, or data source is missing entirely — such that the analysis is internally correct but scoped wrong?
