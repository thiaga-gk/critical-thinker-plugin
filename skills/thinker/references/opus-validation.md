# Opus 4.8 Final Validation Gate

The final gate is independent from the draft author. It catches both **under-analysis** and **over-analysis**: premature closure, weak evidence, hidden assumptions, missed consequences, unnecessary lanes, and excessive user burden.

## Required validators

Run independently and in parallel on the exact same candidate report and evidence/assumption ledger:

1. `final-opus-validator` — coverage, evidence, logic, proportionality, and report-contract review (`claude-opus-4-8`)
2. `final-opus-adversary` — hostile counterexample, failure-path, anchoring, and premature-closure review (`claude-opus-4-8`)
3. `crossmodel-adversary` — **required in DEEP** (and in high-consequence STANDARD): the same adversarial review on a **different model family** (`claude-fable-5`)

Do not show any validator another's output before all complete.

## Model-diversity requirement

Two reviewers on the same model are only *prompt*-diverse: they share the model family's blind spots, so a defect both miss can pass. Therefore the final panel must be **model-diverse** — at least one required reviewer runs on a different model family than the Opus 4.8 certifier.

- The primary certifier is `final-opus-validator`, preferring `claude-opus-4-8` and, when 4.8 is unavailable, falling back **within the Opus tier** (`claude-opus-4-7` → `claude-opus-4-6` → `claude-opus-4-5`) and recording the actual version. It is fail-closed **at the tier**: it never certifies on Sonnet, Fable, Haiku, or an unauditable model, and if no Opus-tier model can run the status is `VALIDATION BLOCKED`. The ordered chains for every role are in `references/model-map.md`.
- The decorrelation reviewer is `crossmodel-adversary`, **preferably on `claude-fable-5`**; if Fable 5 is unavailable, **fall back to `claude-sonnet-5`** (invoke the same reviewer with a Sonnet 5 model override). Sonnet 5 is still a different family than Opus 4.8 — so it preserves decorrelation — and it is the always-available floor model. Whichever model runs, the reviewer reports its actual model so the diversity is auditable. Its rejection is a veto that forces repair or arbitration exactly like an Opus rejection — its *agreement* is not what certifies, but its *disagreement* cannot be ignored.
- Because Sonnet 5 is always available, a model-diverse gate should effectively always be achievable. Record `MODEL DIVERSITY UNAVAILABLE` only in the rare event that **neither** Fable 5 nor Sonnet 5 can run.

## Mandatory validation dimensions

Each validator explicitly assesses:

1. the selected LIGHT/STANDARD/DEEP mode matches decision risk, ambiguity, and reversibility
2. selected lanes pass the material lane test and skipped lanes are defensible
3. user questions were decision-critical and proportional to mode
4. all six operational gates are substantively satisfied at proportional depth
5. all five pitfalls were tested and detected pitfalls repaired
6. material facts and current claims are traceable and not fabricated
7. the causal story distinguishes symptoms, correlation, mechanism, and cause appropriately
8. credible alternative explanations or options are considered
9. the analysis identifies the critical few rather than an unranked list
10. consequences include relevant short/long, direct/indirect, positive/negative effects and incentives
11. the recommendation matches evidence and calibrated confidence
12. reversibility, rollback, monitoring, and revisit triggers fit decision risk
13. the report follows the Markdown contract, including mode, lane ledger, and executive-summary findings table
14. the workflow did not add obvious ceremony whose result could not change the decision
15. **quantitative self-verification**: every load-bearing number, formula, threshold, and worked example reproduces — the validator **re-derives the numbers the recommendation depends on** and confirms any worked example is reproducible by the report's own stated method; a figure that does not reconcile, or an example the method cannot produce, is a blocking defect
16. **scope completeness**: no decision-relevant dimension, option, stakeholder, failure mode, or data source is missing entirely, and the problem is not framed more narrowly than the user's actual decision — attack absence, not only what is present

## Validator decision format

```markdown
DECISION: APPROVE | REJECT
MODEL: [the Opus-tier model actually run — claude-opus-4-8, or a recorded fallback version per model-map.md]

## Blocking defects
- [none, or numbered defects]

## Important non-blocking improvements
- ...

## Proportionality re-check
| Check | Pass? | Note |
|---|---|---|
| Mode choice | ... | ... |
| Lane materiality | ... | ... |
| User burden | ... | ... |
| Anti-ceremony | ... | ... |

## Pitfall re-check
| Pitfall | Pass? | Note |
|---|---|---|

## Six-gate re-check
| Gate | Pass? | Note |
|---|---|---|

## Confidence
high / medium / low — reason
```

A validator must reject when a defect could reasonably change diagnosis, recommendation, risk, or user action. It may also reject egregious over-orchestration that materially wastes time or burdens the user without adding decision value.

## Repair loop

If either validator rejects:

1. Consolidate blocking defects without diluting them.
2. Return defects and the report to synthesis.
3. Repair the analysis, routing, lane rationale, user-question handling, or report as needed.
4. Update the evidence/assumption ledger.
5. Rerun **all** required reviewers independently (both Opus validators, plus the cross-model adversary in DEEP).

Do not rerun only the rejecting reviewer; a repair can create defects elsewhere. A repair frequently introduces a *new* defect (a common failure mode across repair cycles), which is exactly why every reviewer reruns and why the quantitative-reproduction and completeness dimensions are re-checked each pass.

## Disagreement and arbiter

After one repair pass, if any two required reviewers disagree — including the cross-model adversary rejecting while the Opus reviewers approve — or their blocking classifications materially conflict, run `final-opus-arbiter` on:

- the candidate report
- evidence/assumption ledger
- all reviewer outputs

The arbiter independently inspects the report before resolving the disagreement. A cross-model rejection is treated as a first-class signal, not a minority to be outvoted — the arbiter must engage its specific defect, because a different-family reviewer catching what the Opus panel missed is the whole point of model diversity. Decision: `APPROVE`, `REJECT`, or `REPAIR_AND_REVALIDATE`.

## Final status

- `VALIDATED`: both Opus validators approve, or the Opus arbiter approves after independent review. The certifier may be a recorded Opus-tier fallback version (e.g. `VALIDATED (certifier: claude-opus-4-7)`) — never below the Opus tier.
- `DRAFT — REPAIR REQUIRED`: validator or arbiter rejects and repair is incomplete.
- `VALIDATION BLOCKED`: **no Opus-tier model** (`claude-opus-4-8` → `claude-opus-4-7` → `claude-opus-4-6` → `claude-opus-4-5`) can run, the gate repeatedly fails, or the actual final-gate model cannot be confirmed.

Never convert a blocked status into `VALIDATED` with Sonnet or an unknown fallback.
