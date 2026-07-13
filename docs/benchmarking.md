# Thinker Behavioral Benchmarking

## Purpose

The benchmark answers one practical question:

> **Does Thinker improve decisions enough to justify its questions, model calls, token cost, and latency?**

Static validation can prove that the package is internally consistent. It cannot prove that LIGHT is proportionate, STANDARD discovers more decision-critical unknowns, or DEEP earns its orchestration cost. Those are empirical claims and require runtime comparison.

## Suite

`skills/thinker/evals/benchmark-cases.json` contains 30 cases across more than 15 problem categories. The set intentionally includes:

- trivial and reversible choices
- cases where do-nothing should remain viable
- a case where the user's first answer is probably correct
- under-specified vendor decisions
- anchoring on price or personnel blame
- changed metric definitions and conflicting metrics
- aggregate-versus-segment contradictions
- local optimization and incentive problems
- quality sampling and supplier capability
- regulated outsourcing
- medical disagreement
- contract and continuity risk
- urgent security and vendor-outage decisions
- leveraged acquisition and cash-runway pressure
- policy pilot scaling
- high-coupling AI build-versus-buy work

## Generate the run plan

```bash
python scripts/benchmark.py plan
```

The harness creates:

```text
30 cases x 4 variants = 120 runs
```

The four variants are:

| Variant | Instruction |
|---|---|
| BASELINE | Plain Sonnet 5 analytical answer; do not invoke Thinker |
| LIGHT | Invoke Thinker and start LIGHT; safety/high-stakes routing may escalate |
| STANDARD | Invoke Thinker and start STANDARD; safety/high-stakes routing may escalate |
| DEEP | Invoke Thinker and start DEEP |

Run the exact same case facts across variants. Record the actual mode and model usage rather than assuming the requested path was followed.

## Blind judge metrics

`benchmark-opus-judge` scores each anonymized output from 0 to 4 on ten metrics:

1. critical unknown discovery
2. unsupported assumption control
3. premature recommendation control
4. causal quality
5. evidence traceability
6. confidence calibration
7. actionability
8. consequence coverage
9. critical-few focus
10. proportionality

The judge is instructed not to reward answer length, model prestige, or agent count. Extra analysis is a negative when it adds no decision value.

## Telemetry

Record:

- input tokens
- output tokens
- wall-clock latency in seconds
- model/agent call count
- user question count
- specialist lane count
- a normalized recommendation signature

Telemetry should come from the runtime or run logs, not the judge's intuition.

## Results JSONL shape

Each line supplied to the scorer is one completed run record:

```json
{
  "case_id": "B05",
  "variant": "STANDARD",
  "scores": {
    "critical_unknown_discovery": 4,
    "unsupported_assumption_control": 4,
    "premature_recommendation_control": 4,
    "causal_quality": 3,
    "evidence_traceability": 3,
    "confidence_calibration": 4,
    "actionability": 4,
    "consequence_coverage": 3,
    "critical_few_focus": 4,
    "proportionality": 4
  },
  "telemetry": {
    "input_tokens": 5100,
    "output_tokens": 3900,
    "latency_seconds": 61.2,
    "model_calls": 5,
    "question_count": 4,
    "lane_count": 3
  },
  "recommendation_signature": "do not apply blanket discount; segment churn and run a targeted pricing test"
}
```

The scorer rejects missing metrics, scores outside 0-4, invalid variants, empty recommendation signatures, or negative telemetry.

## Summarize collected results

```bash
python scripts/benchmark.py score --results path/to/results.jsonl
```

The Markdown summary reports:

- mean and median quality by variant
- mean question count, lane count, model calls, and latency
- per-metric means
- recommendation-signature stability by case
- descriptive checks for STANDARD/DEEP quality versus BASELINE and LIGHT lane use versus STANDARD

These checks are descriptive. Review case-level failures and judge consistency before making production claims.

## What success should look like

A strong result should show that:

- **LIGHT** matches or beats BASELINE on low-risk cases without a specialist swarm.
- **STANDARD** improves ambiguous, anchoring, and under-specified cases by finding critical unknowns and reducing unsupported assumptions.
- **DEEP** earns its extra cost on high-consequence cases through better causal conflict resolution, consequence coverage, and calibrated action.
- User question counts remain within mode budgets except a documented high-stakes follow-up.
- Deeper analysis explains recommendation changes through new evidence, a discriminating argument, or a scenario split.
- Cases where the first answer is correct remain correct rather than inventing doubt for appearance's sake.
- Do-nothing or defer can win when it has the best risk-adjusted value.

Do **not** call the skill empirically production-proven until real Claude Code runs have been collected and analyzed. The benchmark harness creates the protocol and summary machinery; it does not execute Anthropic models itself.
