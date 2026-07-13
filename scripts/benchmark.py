#!/usr/bin/env python3
"""Prepare and summarize Thinker behavioral benchmark runs.

This harness does not call the Anthropic API. It creates a run matrix and scores
already-collected judge/telemetry JSONL records.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CASES_PATH = ROOT / "skills" / "thinker" / "evals" / "benchmark-cases.json"
DEFAULT_PLAN = ROOT / "docs" / "benchmark-run-plan.json"
DEFAULT_REPORT = ROOT / "docs" / "benchmark-results.md"

METRICS = [
    "critical_unknown_discovery",
    "unsupported_assumption_control",
    "premature_recommendation_control",
    "causal_quality",
    "evidence_traceability",
    "confidence_calibration",
    "actionability",
    "consequence_coverage",
    "critical_few_focus",
    "proportionality",
]
VARIANTS = ["BASELINE", "LIGHT", "STANDARD", "DEEP"]
TELEMETRY_FIELDS = [
    "input_tokens",
    "output_tokens",
    "latency_seconds",
    "model_calls",
    "question_count",
    "lane_count",
]


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise SystemExit(f"ERROR: missing file: {path}") from exc
    except json.JSONDecodeError as exc:
        raise SystemExit(f"ERROR: invalid JSON in {path}: {exc}") from exc


def baseline_instruction() -> str:
    return (
        "Answer the case normally as Claude Sonnet 5. Do not invoke the Thinker "
        "skill or its agents. Give your best direct analytical response using the supplied facts."
    )


def thinker_instruction(variant: str) -> str:
    return (
        f"Invoke the Thinker skill and start in {variant} mode. Apply all six work gates "
        "and the five-pitfall audit proportionately. Escalate only when newly discovered "
        "safety, regulatory, medical, legal, security, severe financial, or similarly "
        "high-consequence risk makes the forced depth unsafe. Record the actual mode used."
    )


def make_plan(cases_path: Path, output: Path) -> None:
    suite = load_json(cases_path)
    cases = suite.get("cases", [])
    variants = suite.get("variants", VARIANTS)
    if variants != VARIANTS:
        raise SystemExit(f"ERROR: expected variants {VARIANTS}, got {variants}")

    runs: list[dict[str, Any]] = []
    for case in cases:
        for variant in variants:
            instruction = baseline_instruction() if variant == "BASELINE" else thinker_instruction(variant)
            runs.append(
                {
                    "run_id": f"{case['id']}::{variant}",
                    "case_id": case["id"],
                    "category": case["category"],
                    "target_mode": case["target_mode"],
                    "variant": variant,
                    "instruction": instruction,
                    "prompt": case["prompt"],
                    "expectations": case["expectations"],
                }
            )

    payload = {
        "suite_name": suite.get("suite_name", "thinker-behavioral-benchmark"),
        "suite_version": suite.get("version", "unknown"),
        "case_count": len(cases),
        "variant_count": len(variants),
        "run_count": len(runs),
        "note": "This plan contains no API executor. Collect runtime outputs and Opus judge records in Claude Code, then use the score command.",
        "runs": runs,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: wrote {len(runs)} benchmark runs ({len(cases)} cases x {len(variants)} variants) to {output}")


def require_number(record: dict[str, Any], field: str, where: str) -> float:
    value = record.get(field)
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{where}: {field} must be a number")
    if value < 0:
        raise ValueError(f"{where}: {field} must be nonnegative")
    return float(value)


def validate_result(record: dict[str, Any], line_no: int) -> dict[str, Any]:
    where = f"line {line_no}"
    for field in ("case_id", "variant", "scores", "telemetry", "recommendation_signature"):
        if field not in record:
            raise ValueError(f"{where}: missing {field}")

    if record["variant"] not in VARIANTS:
        raise ValueError(f"{where}: invalid variant {record['variant']!r}")
    if not isinstance(record["case_id"], str) or not record["case_id"].strip():
        raise ValueError(f"{where}: case_id must be a non-empty string")
    if not isinstance(record["recommendation_signature"], str) or not record["recommendation_signature"].strip():
        raise ValueError(f"{where}: recommendation_signature must be a non-empty string")

    scores = record["scores"]
    if not isinstance(scores, dict):
        raise ValueError(f"{where}: scores must be an object")
    missing = [m for m in METRICS if m not in scores]
    extra = [m for m in scores if m not in METRICS]
    if missing or extra:
        raise ValueError(f"{where}: scores keys mismatch; missing={missing}, extra={extra}")
    for metric in METRICS:
        value = scores[metric]
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not 0 <= value <= 4:
            raise ValueError(f"{where}: score {metric} must be numeric in [0, 4]")

    telemetry = record["telemetry"]
    if not isinstance(telemetry, dict):
        raise ValueError(f"{where}: telemetry must be an object")
    for field in TELEMETRY_FIELDS:
        require_number(telemetry, field, where)

    return record


def load_results(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_no, raw in enumerate(handle, start=1):
                if not raw.strip():
                    continue
                try:
                    value = json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise SystemExit(f"ERROR: invalid JSONL at line {line_no}: {exc}") from exc
                if not isinstance(value, dict):
                    raise SystemExit(f"ERROR: line {line_no} must be a JSON object")
                try:
                    records.append(validate_result(value, line_no))
                except ValueError as exc:
                    raise SystemExit(f"ERROR: {exc}") from exc
    except FileNotFoundError as exc:
        raise SystemExit(f"ERROR: missing results file: {path}") from exc
    if not records:
        raise SystemExit("ERROR: results file contains no records")
    return records


def mean(values: list[float]) -> float:
    return statistics.fmean(values) if values else float("nan")


def median(values: list[float]) -> float:
    return statistics.median(values) if values else float("nan")


def fmt(value: float) -> str:
    return "—" if value != value else f"{value:.2f}"


def summarize(records: list[dict[str, Any]], output: Path) -> None:
    by_variant: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        by_variant[record["variant"]].append(record)
        by_case[record["case_id"]].append(record)

    lines = [
        "# Thinker Behavioral Benchmark Results",
        "",
        "> Descriptive summary of collected runtime records. This report does not execute models or prove causality by itself.",
        "",
        "## Variant summary",
        "",
        "| Variant | Runs | Mean quality /4 | Median quality /4 | Mean questions | Mean lanes | Mean model calls | Mean latency (s) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]

    variant_quality: dict[str, list[float]] = {}
    for variant in VARIANTS:
        subset = by_variant.get(variant, [])
        qualities = [mean([float(r["scores"][m]) for m in METRICS]) for r in subset]
        variant_quality[variant] = qualities
        lines.append(
            "| {variant} | {runs} | {mq} | {medq} | {q} | {lanes} | {calls} | {latency} |".format(
                variant=variant,
                runs=len(subset),
                mq=fmt(mean(qualities)),
                medq=fmt(median(qualities)),
                q=fmt(mean([float(r["telemetry"]["question_count"]) for r in subset])),
                lanes=fmt(mean([float(r["telemetry"]["lane_count"]) for r in subset])),
                calls=fmt(mean([float(r["telemetry"]["model_calls"]) for r in subset])),
                latency=fmt(mean([float(r["telemetry"]["latency_seconds"]) for r in subset])),
            )
        )

    lines += ["", "## Metric means", "", "| Metric | BASELINE | LIGHT | STANDARD | DEEP |", "|---|---:|---:|---:|---:|"]
    for metric in METRICS:
        row = [metric]
        for variant in VARIANTS:
            row.append(fmt(mean([float(r["scores"][metric]) for r in by_variant.get(variant, [])])))
        lines.append("| " + " | ".join(row) + " |")

    lines += [
        "",
        "## Recommendation stability",
        "",
        "| Case | Variants observed | Distinct recommendation signatures | Stability note |",
        "|---|---:|---:|---|",
    ]
    for case_id in sorted(by_case):
        subset = by_case[case_id]
        signatures = {r["recommendation_signature"].strip().lower() for r in subset}
        note = "stable" if len(signatures) == 1 else "changed across variants — inspect whether new evidence or explicit conflict resolution justifies the change"
        lines.append(f"| {case_id} | {len(subset)} | {len(signatures)} | {note} |")

    baseline_median = median(variant_quality.get("BASELINE", []))
    standard_median = median(variant_quality.get("STANDARD", []))
    deep_median = median(variant_quality.get("DEEP", []))
    light_lanes = mean([float(r["telemetry"]["lane_count"]) for r in by_variant.get("LIGHT", [])])
    standard_lanes = mean([float(r["telemetry"]["lane_count"]) for r in by_variant.get("STANDARD", [])])

    checks: list[tuple[str, bool | None, str]] = []
    if all(v == v for v in (baseline_median, standard_median)):
        checks.append(("STANDARD median quality exceeds BASELINE", standard_median > baseline_median, f"{fmt(standard_median)} vs {fmt(baseline_median)}"))
    else:
        checks.append(("STANDARD median quality exceeds BASELINE", None, "insufficient variant coverage"))
    if all(v == v for v in (baseline_median, deep_median)):
        checks.append(("DEEP median quality exceeds BASELINE", deep_median > baseline_median, f"{fmt(deep_median)} vs {fmt(baseline_median)}"))
    else:
        checks.append(("DEEP median quality exceeds BASELINE", None, "insufficient variant coverage"))
    if all(v == v for v in (light_lanes, standard_lanes)):
        checks.append(("LIGHT uses fewer lanes than STANDARD", light_lanes < standard_lanes, f"{fmt(light_lanes)} vs {fmt(standard_lanes)}"))
    else:
        checks.append(("LIGHT uses fewer lanes than STANDARD", None, "insufficient variant coverage"))

    lines += ["", "## Descriptive acceptance checks", "", "| Check | Result | Observation |", "|---|---|---|"]
    for name, result, observation in checks:
        label = "PASS" if result is True else "FAIL" if result is False else "NOT TESTABLE"
        lines.append(f"| {name} | {label} | {observation} |")

    lines += [
        "",
        "## Interpretation guardrail",
        "",
        "Treat these checks as descriptive. Review case-level failures, recommendation-signature changes, telemetry completeness, and judge consistency before claiming empirical production readiness.",
        "",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")
    print(f"PASS: validated {len(records)} benchmark records and wrote {output}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    plan_parser = subparsers.add_parser("plan", help="generate the benchmark run matrix")
    plan_parser.add_argument("--cases", type=Path, default=CASES_PATH)
    plan_parser.add_argument("--output", type=Path, default=DEFAULT_PLAN)

    score_parser = subparsers.add_parser("score", help="validate JSONL results and write a Markdown summary")
    score_parser.add_argument("--results", type=Path, required=True)
    score_parser.add_argument("--output", type=Path, default=DEFAULT_REPORT)

    args = parser.parse_args(argv)
    if args.command == "plan":
        make_plan(args.cases, args.output)
    elif args.command == "score":
        summarize(load_results(args.results), args.output)
    else:  # pragma: no cover
        parser.error("unknown command")
    return 0


if __name__ == "__main__":
    sys.exit(main())
