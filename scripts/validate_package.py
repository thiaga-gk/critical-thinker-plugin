#!/usr/bin/env python3
"""Static design validation for the Thinker skill package."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "thinker" / "SKILL.md"
EVALS = ROOT / "skills" / "thinker" / "evals" / "evals.json"
BENCH = ROOT / "skills" / "thinker" / "evals" / "benchmark-cases.json"
PLUGIN = ROOT / ".claude-plugin" / "plugin.json"
BENCH_SCRIPT = ROOT / "scripts" / "benchmark.py"
MANIFEST = ROOT / "manifest.txt"
REFS = ROOT / "skills" / "thinker" / "references"
AGENTS = ROOT / "agents"

REQUIRED_PATHS = [SKILL, EVALS, BENCH, PLUGIN, BENCH_SCRIPT, MANIFEST]
# claude-fable-5 is permitted ONLY for the cross-model decorrelation reviewer (a different
# model family than Opus 4.8), so the final gate is model-diverse, not merely prompt-diverse.
ALLOWED_AGENT_MODELS = {"claude-sonnet-5", "claude-opus-4-8", "claude-fable-5"}
EXPECTED_AGENTS = {
    "problem-framer.md": "claude-sonnet-5",
    "systems-expander.md": "claude-sonnet-5",
    "evidence-challenger.md": "claude-sonnet-5",
    "priority-analyst.md": "claude-sonnet-5",
    "consequence-analyst.md": "claude-sonnet-5",
    "completeness-critic.md": "claude-sonnet-5",
    "lane-adversary.md": "claude-sonnet-5",
    "thinker-coordinator.md": "claude-sonnet-5",
    "synthesis-analyst.md": "claude-opus-4-8",
    "final-opus-validator.md": "claude-opus-4-8",
    "final-opus-adversary.md": "claude-opus-4-8",
    "final-opus-arbiter.md": "claude-opus-4-8",
    "benchmark-opus-judge.md": "claude-opus-4-8",
    "crossmodel-adversary.md": "claude-fable-5",
}


def fail(message: str) -> None:
    raise AssertionError(message)


def text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def lower(path: Path) -> str:
    return text(path).lower()


def load_json(path: Path):
    try:
        return json.loads(text(path))
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")


def frontmatter_value(content: str, key: str) -> str | None:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*([^\n]+)\s*$", content)
    return match.group(1).strip() if match else None


def require_terms(content: str, terms: list[str], label: str) -> None:
    haystack = content.lower()
    missing = [term for term in terms if term.lower() not in haystack]
    if missing:
        fail(f"{label} missing required terms: {missing}")


def check_required_files() -> None:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED_PATHS if not p.is_file()]
    if missing:
        fail(f"missing required files: {missing}")


def check_plugin() -> None:
    plugin = load_json(PLUGIN)
    if plugin.get("name") != "thinker":
        fail("plugin name must be thinker")
    if plugin.get("version") != "2.1.0":
        fail("plugin version must be 2.1.0")


def check_skill() -> int:
    content = text(SKILL)
    line_count = len(content.splitlines())
    if line_count >= 500:
        fail(f"SKILL.md must remain under 500 lines; got {line_count}")
    if frontmatter_value(content, "model") != "claude-sonnet-5":
        fail("SKILL.md model must be exactly claude-sonnet-5")
    require_terms(
        content,
        [
            "baseline",
            "challenge",
            "structure",
            "test",
            "integrate",
            "decide & learn",
            "light",
            "standard",
            "deep",
            "five-pitfall",
            "spawn a lane only when",
            "material lane test",
            "docs/thinker-",
            "executive summary",
            "lane-selection rationale",
            "do not launch five lanes by habit",
        ],
        "SKILL.md",
    )
    return line_count


def check_agents() -> None:
    actual = {p.name for p in AGENTS.glob("*.md")}
    expected = set(EXPECTED_AGENTS)
    if actual != expected:
        fail(f"agent file set mismatch; missing={sorted(expected-actual)}, extra={sorted(actual-expected)}")
    for filename, expected_model in EXPECTED_AGENTS.items():
        content = text(AGENTS / filename)
        model = frontmatter_value(content, "model")
        if model != expected_model:
            fail(f"{filename} model must be {expected_model}, got {model}")
        if model not in ALLOWED_AGENT_MODELS:
            fail(f"{filename} uses disallowed model {model}")
    all_agent_text = "\n".join(lower(p) for p in AGENTS.glob("*.md"))
    for forbidden in ["model: sonnet", "model: opus\n", "model: haiku", "model: inherit"]:
        if forbidden in all_agent_text:
            fail(f"agent configuration contains forbidden or unauditable model declaration: {forbidden!r}")


def check_evals() -> tuple[int, int]:
    core = load_json(EVALS)
    if core.get("version") != "2.0.0":
        fail("core eval version must be 2.0.0")
    evals = core.get("evals")
    if not isinstance(evals, list) or len(evals) < 8:
        fail("core evals must contain at least 8 cases")
    ids = [e.get("id") for e in evals]
    if len(ids) != len(set(ids)):
        fail("core eval ids must be unique")
    for case in evals:
        if not case.get("prompt") or not case.get("expected_output"):
            fail(f"core eval {case.get('id')} needs prompt and expected_output")
        expectations = case.get("expectations")
        if not isinstance(expectations, list) or len(expectations) < 5:
            fail(f"core eval {case.get('id')} needs at least 5 expectations")

    bench = load_json(BENCH)
    cases = bench.get("cases")
    if not isinstance(cases, list) or len(cases) != 30:
        fail(f"benchmark must contain exactly 30 cases; got {len(cases) if isinstance(cases, list) else 'invalid'}")
    ids = [c.get("id") for c in cases]
    if len(ids) != len(set(ids)):
        fail("benchmark case ids must be unique")
    modes = {c.get("target_mode") for c in cases}
    if modes != {"LIGHT", "STANDARD", "DEEP"}:
        fail(f"benchmark target modes must cover LIGHT/STANDARD/DEEP; got {modes}")
    categories = {c.get("category") for c in cases}
    if len(categories) < 15:
        fail(f"benchmark must cover at least 15 categories; got {len(categories)}")
    if bench.get("variants") != ["BASELINE", "LIGHT", "STANDARD", "DEEP"]:
        fail("benchmark variants must be BASELINE/LIGHT/STANDARD/DEEP in order")
    for case in cases:
        if not case.get("prompt"):
            fail(f"benchmark case {case.get('id')} lacks prompt")
        expectations = case.get("expectations")
        if not isinstance(expectations, list) or len(expectations) < 3:
            fail(f"benchmark case {case.get('id')} needs at least 3 expectations")
    return len(evals), len(cases)


def check_references() -> None:
    routing = lower(REFS / "routing-modes.md")
    orchestration = lower(REFS / "orchestration.md")
    opus = lower(REFS / "opus-validation.md")
    report = lower(REFS / "report-contract.md")
    benchmarking = lower(REFS / "benchmarking.md")
    six = lower(REFS / "six-levels.md")
    pitfalls = lower(REFS / "five-pitfalls.md")
    probing = lower(REFS / "user-probing.md")

    require_terms(routing, ["light", "standard", "deep", "anti-overengineering test", "select the lowest mode"], "routing-modes.md")
    require_terms(orchestration, ["material lane test", "spawn the lane only", "do not", "all five", "selection ledger"], "orchestration.md")
    # Fix 1 (per-lane adversary) and Fix 3 (completeness critic) must be wired into orchestration.
    require_terms(orchestration, ["lane-adversary", "cross-examination", "completeness-critic"], "orchestration.md")
    require_terms(
        opus,
        [
            "independently and in parallel",
            "claude-opus-4-8",
            "validation blocked",
            "mode",
            "lane",
            "user burden",
            "anti-ceremony",
            # Fix 4 (model diversity), Fix 2 (quantitative reproduction), Fix 3 (scope completeness)
            "crossmodel-adversary",
            "model-diversity",
            "claude-fable-5",
            "re-derive",
            "scope completeness",
        ],
        "opus-validation.md",
    )
    require_terms(
        report,
        [
            "executive summary",
            "analysis mode",
            "analysis routing and lane selection",
            "| finding | evidence / basis | decision impact | confidence | recommended action |",
            # Fix 2 (quantitative reproduction) and Fix 3 (scope completeness) must be report sections.
            "quantitative self-verification",
            "known gaps",
        ],
        "report-contract.md",
    )
    require_terms(
        benchmarking,
        [
            "critical unknown discovery",
            "unsupported assumptions",
            "premature recommendation",
            "recommendation stability",
            "latency",
            "user question count",
        ],
        "benchmarking.md",
    )
    require_terms(six, ["baseline", "challenge", "structure", "test", "integrate", "decide & learn", "source level 6", "quantitative self-verification", "reproduce"], "six-levels.md")
    require_terms(pitfalls, ["jumping to an answer", "unwilling to expand", "focusing on the unimportant", "accepting results at face value", "not thinking through consequences"], "five-pitfalls.md")
    require_terms(probing, ["decision value", "light", "standard", "deep", "question budget", "user burden"], "user-probing.md")


def check_manifest() -> None:
    manifest_entries = {line.strip() for line in text(MANIFEST).splitlines() if line.strip()}
    actual_entries = {
        str(path.relative_to(ROOT))
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.name != "manifest.txt"
        and path.name not in {".DS_Store", ".gitignore"}  # OS/VCS tooling, never package content
        and path.suffix != ".zip"
        and "__pycache__" not in path.parts
        and ".git" not in path.parts  # keep the check robust inside a git repo
    }
    if manifest_entries != actual_entries:
        fail(
            "manifest mismatch; "
            f"missing_from_manifest={sorted(actual_entries-manifest_entries)}, "
            f"stale={sorted(manifest_entries-actual_entries)}"
        )


def check_design_gates() -> list[str]:
    skill = lower(SKILL)
    routing = lower(REFS / "routing-modes.md")
    six = lower(REFS / "six-levels.md")
    pitfalls = lower(REFS / "five-pitfalls.md")
    probing = lower(REFS / "user-probing.md")
    orchestration = lower(REFS / "orchestration.md")
    opus = lower(REFS / "opus-validation.md")
    report = lower(REFS / "report-contract.md")
    bench = lower(REFS / "benchmarking.md")

    gates = [
        ("adaptive modes", all(term in routing for term in ["light", "standard", "deep", "select the lowest mode"])),
        ("six operational gates with source mapping", all(term in six for term in ["baseline", "challenge", "structure", "test", "integrate", "decide & learn", "source level"])),
        ("five-pitfall repair controls", all(term in pitfalls for term in ["signal", "repair"])),
        ("decision-value probing", all(term in probing for term in ["decision value", "question budget", "user burden"])),
        ("adaptive material lane selection", all(term in orchestration for term in ["material lane test", "spawn the lane only"])),
        ("no default five-lane swarm", "do not launch five lanes by habit" in skill and "spawn all five lanes by default" in orchestration),
        ("pinned Sonnet 5 floor", "the lowest configured model is **claude sonnet 5**" in skill and frontmatter_value(text(SKILL), "model") == "claude-sonnet-5"),
        ("dual independent Opus 4.8 final validation", all(term in opus for term in ["independently and in parallel", "final-opus-validator", "final-opus-adversary", "claude-opus-4-8"])),
        ("30-case benchmark framework", "30-case x 4-variant" in bench and load_json(BENCH).get("cases") and len(load_json(BENCH)["cases"]) == 30),
        ("Markdown report with mode, lane ledger, and executive table", all(term in report for term in ["analysis mode", "analysis routing and lane selection", "executive summary", "| finding | evidence / basis | decision impact | confidence | recommended action |"])),
    ]
    failed = [name for name, passed in gates if not passed]
    if failed:
        fail(f"design acceptance gates failed: {failed}")
    return [name for name, _ in gates]


def main() -> int:
    try:
        check_required_files()
        check_plugin()
        line_count = check_skill()
        check_agents()
        core_count, bench_count = check_evals()
        check_references()
        design_gates = check_design_gates()
        check_manifest()
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        return 1

    print("PASS: Thinker package static validation succeeded.")
    print(f"PASS: SKILL.md lines={line_count} (<500).")
    print(f"PASS: agent model policy verified for {len(EXPECTED_AGENTS)} agents; pinned Sonnet 5, Opus 4.8, and (cross-model reviewer only) Fable 5.")
    print("PASS: final validator/adversary/arbiter are pinned to claude-opus-4-8; crossmodel-adversary pinned to claude-fable-5 for a model-diverse gate.")
    print(f"PASS: {core_count} core eval cases and {bench_count} behavioral benchmark cases loaded.")
    print("PASS: docs/ Markdown report contract includes analysis mode, lane-selection ledger, and executive-summary findings table.")
    print("PASS: design acceptance score 10/10.")
    for index, gate in enumerate(design_gates, start=1):
        print(f"  {index}. {gate}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
