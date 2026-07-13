# Adaptive Parallel Orchestration Protocol

Parallelism exists to reduce anchoring and improve coverage—not to maximize agent count.

## Common problem brief

Before delegation, create one compact brief containing:

- neutral problem statement
- desired outcome or decision
- known facts with source labels
- claims, assumptions, and preferences
- constraints and time horizon
- stakeholders
- current proposed solution or attributed cause, if any
- unresolved questions
- selected mode and routing rationale

Give selected lanes the same factual core. Add lane-specific tasks, but do not disclose another lane's conclusion until independent work is complete.

## Material lane test

For each candidate lane, answer both questions:

1. Is the lane's core analytical question still unresolved?
2. Could a plausible answer materially change the diagnosis, option ranking, risk, or next action?

Spawn the lane only when both answers are yes.

## Lane trigger matrix

| Lane | Spawn when | Usually skip when |
|---|---|---|
| `problem-framer` | a solution/person/cause is already blamed; frame is ambiguous; symptom-vs-cause risk exists | the decision is neutrally stated and causal framing is not material |
| `systems-expander` | cross-team interfaces, upstream/downstream effects, incentives, feedback loops, or local optimization may change the answer | boundary is narrow and independent |
| `evidence-challenger` | metrics, dashboards, reports, model outputs, causal claims, external evidence, or conflicting signals drive the decision | facts are simple, directly observed, and not disputed |
| `priority-analyst` | many issues/options compete; resources are constrained; ranking or sensitivity matters | there are one or two obvious drivers and no prioritization ambiguity |
| `consequence-analyst` | rollout, irreversibility, high downside, incentives, stakeholder harm, or delayed effects matter | the action is cheap, easily reversible, and low consequence |
| `completeness-critic` | the analysis could be internally correct yet model the wrong or too few things — unmodeled dimensions, absent options/stakeholders, unasked decision-critical questions | LIGHT, well-bounded problems where the scope is obviously complete. **Mandatory in DEEP.** |

## Mode-aware lane budgets

- **LIGHT:** 0-1 lane. Prefer inline execution when the lane's method is simple.
- **STANDARD:** 2-3 selected lanes, dispatched in parallel.
- **DEEP:** 3-5 selected lanes, dispatched in parallel. Use `thinker-coordinator` when context or cross-lane conflicts would otherwise overload the parent.

A mode budget is a default, not a target. Do not add a lane just to hit a number.

## Selection ledger

Record this before delegation:

| Lane | Selected? | Materiality reason |
|---|---|---|
| problem-framer | Yes/No | ... |
| systems-expander | Yes/No | ... |
| evidence-challenger | Yes/No | ... |
| priority-analyst | Yes/No | ... |
| consequence-analyst | Yes/No | ... |
| completeness-critic | Yes/No | ... (Yes in DEEP) |

The final report includes a compact version of this ledger.

## Lane output contract

Each lane returns:

```markdown
## Findings
...

## Basis
- FACT / SOURCE / REASONING: ...

## Assumptions
- ...

## Contradictions or counterexamples
- ...

## Decision-critical questions
1. ...

## Confidence
medium — because ...
```

Do not request private chain-of-thought. Require concise findings and reasoning/evidence basis.

## Per-lane adversarial cross-examination

Verification must not be deferred entirely to the final Opus gate. A lane's author and its findings are the same perspective; a decision-critical claim can look sound until an *independent* skeptic attacks it. Catch that early and cheaply.

- After a lane returns, run `lane-adversary` (Sonnet 5, cheap) on **each lane that produced a decision-critical finding**, before merge/synthesis. It receives only that lane's output and the common brief.
- The adversary refutes each decision-critical finding, flags claims (including the lane's **own** numbers or reasoning) accepted at face value, names the strongest counterexample, and returns a verdict per finding: `stands`, `weak`, or `refuted`.
- A `weak` finding may not drive the recommendation until its fastest resolving check is done; a `refuted` finding is dropped or reworked. Record the outcome.
- **Mode budget:** DEEP cross-examines every material lane; STANDARD cross-examines only findings that would change the recommendation; LIGHT does it inline (state the refutation in one line). This is a fast pass, not a second analysis — do not let it balloon.

## Completeness sweep (what is missing)

Correctness checking cannot find a dimension that was never modeled. Before synthesis in DEEP (and whenever scope completeness is uncertain in STANDARD), run `completeness-critic` to attack **absence**: unmodeled dimensions, missing options/stakeholders, unasked decision-critical questions, uncovered failure modes, unused evidence, and whether the problem itself is framed too narrowly.

Feed its material gaps back into probing (a newly exposed decision-critical unknown), lane selection (a gap a lane should close), or the report's explicit "known gaps / not modeled" section. Do not treat an immaterial gap as a finding.

## Merge protocol

1. Normalize duplicates.
2. Preserve materially different causal stories.
3. Identify conflicts resolvable by checking facts.
4. For unresolved conflicts, design a discriminating test or scenario split.
5. Rank findings by decision impact, not by how many agents mention them.
6. Identify analysis steps that can now be dropped as low-value.
7. Send the compact consolidated packet to synthesis when needed.

## Coordinator use

Use `thinker-coordinator` in DEEP mode or complex STANDARD mode when:

- three or more lanes return substantial findings
- the problem spans multiple domains or systems
- the parent context is crowded
- multiple lane disagreements require evidence resolution

The coordinator chooses or confirms selected lanes; it must not blindly dispatch all five.

## Anti-patterns

Do not:

- spawn all five lanes by default
- use agent voting as a truth mechanism
- average conflicting recommendations
- ask two lanes nearly identical questions
- let a coordinator become a second author that duplicates synthesis
- preserve a lane because it was expensive to run after its findings prove low-impact

The right orchestration is the **smallest set of independent analytical methods that can still catch decision-relevant failure**.
