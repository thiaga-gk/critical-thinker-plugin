# Behavioral Benchmarking Protocol

Static package validation is necessary but does not prove that Thinker improves decisions. Use this protocol to compare ordinary reasoning against the three Thinker modes.

## Benchmark matrix

Run every case in `evals/benchmark-cases.json` under four variants:

1. `BASELINE` — plain Claude Sonnet 5, no Thinker skill
2. `LIGHT` — Thinker forced to LIGHT unless safety routing escalates
3. `STANDARD` — Thinker forced to STANDARD unless safety routing escalates
4. `DEEP` — Thinker forced to DEEP

Use identical case facts across variants. Record actual model usage, latency, token usage, question count, and final recommendation.

## Quality metrics

Judge the analytical output on a 0-4 scale for each metric:

| Metric | 0 | 4 |
|---|---|---|
| Critical unknown discovery | misses decision-changing unknowns | identifies the material unknowns and does not ask low-value questions |
| Unsupported assumptions | hidden material assumptions | material assumptions explicit and bounded |
| Premature recommendation control | recommends before framing/testing | initial answer treated as hypothesis; recommendation follows evidence |
| Root-cause / causal quality | symptom or assertion | plausible alternatives and discriminating evidence considered |
| Evidence traceability | key claims untraceable | material claims map to source, calculation, user input, or labeled assumption |
| Confidence calibration | certainty mismatched to evidence | confidence and uncertainty match evidence |
| Actionability | vague advice | decision, next action, success signal, and revisit trigger are clear |
| Consequence coverage | material effects ignored | relevant second-order and failure paths are covered proportionately |
| Critical-few focus | unranked laundry list | decision drivers are prioritized and low-value analysis is dropped |
| Proportionality | excessive or insufficient ceremony | depth, lanes, and questions match decision risk |

Operational metrics are not judged subjectively:

- input/output tokens
- wall-clock latency
- number of model/agent calls
- user question count
- number of specialist lanes
- final recommendation signature

## Recommendation stability

Compare recommendation signatures across BASELINE, LIGHT, STANDARD, and DEEP.

A change is valuable when deeper analysis:

- reverses a premature recommendation for a defensible reason
- narrows a broad recommendation into a safer pilot or scenario split
- materially changes confidence or revisit triggers
- preserves the recommendation but substantially strengthens the causal/evidence basis

A change is suspicious when extra analysis changes the answer without new evidence or a clear discriminating argument.

## Opus judge

Use `benchmark-opus-judge` to score quality metrics and compare variants. The judge should receive anonymized outputs when practical so it does not know which variant is expected to win.

For cost/latency/user-burden claims, use recorded telemetry rather than judge intuition.

## Acceptance targets

Do not call the skill empirically production-proven until the benchmark shows:

- STANDARD or DEEP improves median analytical quality over BASELINE on ambiguous/high-consequence cases
- LIGHT is no worse than BASELINE on low-risk cases while using materially fewer lanes/calls than STANDARD or DEEP
- unsupported assumptions and premature recommendations fall on anchoring/under-specified cases
- user question count stays within mode budgets except documented high-stakes follow-up
- deeper modes do not routinely change recommendations without new evidence or an explicit conflict-resolution reason
- no completed report claims `VALIDATED` without the required Opus gate

## Tools

- `python scripts/benchmark.py plan` generates the 30-case x 4-variant run matrix.
- `python scripts/benchmark.py score --results <jsonl>` validates judge/telemetry records and writes a Markdown summary.

The benchmark script does not call the Anthropic API. It prepares and scores collected runtime results so execution can occur in the Claude Code environment where models and Agent subagents are available.
