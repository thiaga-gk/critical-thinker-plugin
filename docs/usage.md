# Using Thinker v2

## Basic invocation

Give Thinker the problem, decision, or current proposed answer. It extracts available facts before asking for more.

```text
Use Thinker on this problem. My current recommendation is to cut price by 20%, but challenge it. Ask only questions that could change the decision and write the final Markdown report under docs/.
```

You do not need to pre-select a mode. The skill routes to the lowest depth that is still safe.

## What to expect by mode

### LIGHT

For narrow, reversible, adequately specified decisions. Expect zero to three questions, normally no specialist agent or at most one, all six gates compressed, and a direct decision with a simple revisit trigger.

Example:

```text
Use Thinker to decide whether our eight-person team should move the weekly sync from Monday to Tuesday. The change is reversible and six people already said either day works.
```

### STANDARD

For moderate ambiguity, multiple options, uncertain evidence, or cross-team effects. Expect a compact grouped question round only when needed and two to three materially selected analytical lanes in parallel.

Example:

```text
Use Thinker on rising churn. Sales says price is the cause and wants a blanket discount. We have not segmented churn by cohort or reason.
```

### DEEP

For severe downside, difficult-to-reverse commitments, regulated/high-stakes work, urgent security or safety uncertainty, or strong evidence conflict. Expect three to five selected lanes, substantive evidence reconciliation, Opus synthesis, and dual independent Opus validation.

Example:

```text
Use Thinker to evaluate outsourcing our regulated customer-verification process. Subprocessors, residency, audit rights, incident response, accuracy by segment, and exit capability are not reconciled.
```

## Questions are selected by decision value

Thinker does not ask a generic discovery questionnaire. It first extracts supplied information and then asks only when an answer could materially change:

- the diagnosis
- option ranking
- risk
- recommended action

For a non-critical unknown, Thinker may proceed with a labeled assumption and state how a different answer would change the conclusion.

For high-stakes medical, legal, financial, safety, or security facts, it does not silently assume missing decision-critical information.

## Adaptive specialist lanes

Thinker has five methods available but does not launch all five by default:

| Lane | Typical trigger |
|---|---|
| Problem framing | A person, cause, or solution is already being blamed or assumed |
| Systems expansion | Interfaces, incentives, upstream/downstream effects, or local optimization matter |
| Evidence challenge | Metrics, reports, dashboards, causal claims, or conflicting signals drive the decision |
| Priority analysis | Too many issues or options compete and the critical few are unclear |
| Consequence analysis | Rollout, irreversibility, high downside, incentives, or delayed effects matter |

Every report includes a compact lane-selection ledger showing which methods ran and why skipped methods were unnecessary.

## The six work gates

Thinker applies all six, at depth proportional to the mode:

1. **Baseline** — capture the current first answer as a hypothesis.
2. **Challenge** — expose assumptions, blind spots, framing errors, and contradictions.
3. **Structure** — create a neutral problem statement, success criteria, hypotheses, and evidence plan.
4. **Test** — verify data, seek disconfirmation, and revise.
5. **Integrate** — combine system context, the critical few, options, trade-offs, and consequences.
6. **Decide & Learn** — make a calibrated decision with monitoring, reversibility, and revisit triggers.

## Final report status

The report path defaults to:

```text
docs/thinker-<problem-slug>.md
```

Possible statuses are:

- `VALIDATED` — both independent Opus validators approve, or the Opus arbiter approves after independent review. The certifier prefers `claude-opus-4-8` and may run on a recorded Opus-tier fallback (`claude-opus-4-7` → `claude-opus-4-6` → `claude-opus-4-5`) when 4.8 is unavailable.
- `DRAFT — REPAIR REQUIRED` — a blocking defect remains.
- `VALIDATION BLOCKED` — no Opus-tier model can run, or the actual final-gate model cannot be confirmed.

Thinker must not relabel blocked validation as `VALIDATED` using Sonnet or an unknown fallback. Per-role fallback chains are in `skills/thinker/references/model-map.md`.

## Run the benchmark plan

```bash
python scripts/benchmark.py plan
```

The command generates a 30-case × 4-variant matrix for:

```text
BASELINE vs LIGHT vs STANDARD vs DEEP
```

Collect each runtime output, blind Opus judge scores, and telemetry. Then summarize the results:

```bash
python scripts/benchmark.py score --results path/to/results.jsonl
```

See `docs/benchmarking.md` for the JSONL format and interpretation guardrails.

## Validate the package

```bash
python scripts/validate_package.py
```

The validator checks ten package-design gates and reports a static design acceptance score. A `10/10` result means the package satisfies its declared architecture and contracts; it does not substitute for the behavioral benchmark.
