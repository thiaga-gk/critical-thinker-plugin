# Thinker Agent Skill Plugin

Thinker v2 is an adaptive critical-thinking skill for Claude Code. It applies the six levels of critical thinking as operational work gates, actively repairs five common problem-solving pitfalls, probes only for decision-critical unknowns, and uses the **smallest amount of disciplined reasoning that can still catch a decision-relevant failure**.

The skill is designed for root-cause analysis, ambiguous decisions, conflicting evidence, option comparison, project recovery, operational failures, architecture choices, vendor decisions, and costly or difficult-to-reverse commitments.

## What changed in v2

- Added **LIGHT / STANDARD / DEEP** routing so trivial decisions do not pay the same orchestration cost as high-consequence ones.
- Replaced the fixed five-lane default with an explicit **material lane test**. A specialist runs only when a plausible answer from that lane could change diagnosis, option ranking, risk, or action.
- Renamed the six operational stages to **Baseline, Challenge, Structure, Test, Integrate, Decide & Learn** while retaining the source-framework mapping.
- Added **anti-overengineering** and **user-burden** checks to final validation.
- Raised the configured model floor to the pinned `claude-sonnet-5`; high-complexity synthesis and final certification use pinned `claude-opus-4-8` agents.
- Added a **30-case behavioral benchmark** and a 4-variant BASELINE/LIGHT/STANDARD/DEEP run harness.
- Added a blind `benchmark-opus-judge` so length, model prestige, and agent count are not treated as quality signals.
- Expanded the report contract with the analysis mode, mode rationale, adaptive lane-selection ledger, and executive-summary findings table.

## What changed in v2.2

- **Model map with per-role fallbacks** (`references/model-map.md`): frontmatter `model:` is now the *preferred* model, and each role has an ordered fallback chain applied as a runtime override when the preferred model or version is unavailable — for environments that lack a specific model. Two invariants hold: a **capability floor** (never below the role's tier; never Haiku/`inherit`) and **model diversity** (the cross-model reviewer stays a different family than the certifier).
- **Opus-tier certifier fallback**: the final certifier prefers `claude-opus-4-8` and now falls back **within the Opus tier** (`claude-opus-4-7` → `claude-opus-4-6` → `claude-opus-4-5`), recording the actual version (e.g. `VALIDATED (certifier: claude-opus-4-7)`). It stays fail-closed — `VALIDATION BLOCKED` only when no Opus-tier model can run — and never certifies on Sonnet, Fable, or Haiku.
- **Auditable actual models**: every certifier records the model it actually ran on; the decorrelation reviewer's chain (`claude-fable-5` → `claude-sonnet-5` → `claude-sonnet-4-6`) is constrained to non-Opus so diversity never collapses.
- The package validator enforces the map (documented fallback IDs, in-tier certifier, non-Opus decorrelation) while keeping all frontmatter pins exact.

## What changed in v2.1

Four fixes that move verification earlier and decorrelate the final gate — motivated by cases where a draft passed its own self-graded gates yet a defect only surfaced at (or slipped past) the final review:

- **Per-lane cross-examination** (`lane-adversary`, Sonnet 5): each decision-critical lane finding is attacked by an independent cheap skeptic *before* synthesis, so weak or face-value claims fail fast instead of only at the end.
- **Quantitative self-verification gate** (Test gate): whenever the analysis contains numbers, formulas, thresholds, or a worked example, they must be traced/re-derived and the example reproduced through its **own** stated method. Validators independently re-derive the load-bearing numbers.
- **Completeness critic** (`completeness-critic`, Sonnet 5, mandatory in DEEP): a lane that attacks what is **missing** — unmodeled dimensions, absent options/stakeholders, unasked decision-critical questions, wrong-scope framing — since correctness checking never finds a dimension that was never modeled. The report gains a required "known gaps / not modeled" section.
- **Model-diverse final gate** (`crossmodel-adversary`, `claude-fable-5` → `claude-sonnet-5` fallback): a required different-family reviewer in DEEP so blind spots correlated within one model family do not pass unchallenged. The Opus 4.8 certifier remains fail-closed; the cross-model reviewer's rejection forces repair/arbitration.

## Install (local plugin)

Thinker runs as a **local Claude Code plugin** — no marketplace required.

Clone the repository, then launch Claude Code with the plugin directory loaded:

```bash
git clone https://github.com/thiaga-gk/critical-thinker-plugin.git
claude --plugin-dir ./critical-thinker-plugin
```

`--plugin-dir` points at the folder containing `.claude-plugin/plugin.json` (the repo root); if you already have the repo, just pass its path. After editing plugin files, run `/reload-plugins` inside Claude Code to pick up changes without restarting.

## Usage

Ask Claude to use Thinker on a problem or decision — the skill routes to the lowest safe depth (LIGHT / STANDARD / DEEP) itself:

```text
Use Thinker on this problem. Challenge my current answer, ask only questions that could change the decision, and write the final report under docs/.
```

You can also invoke the skill explicitly with `/thinker:thinker`.

See [`docs/usage.md`](docs/usage.md) for detailed usage, what to expect in each mode, and worked examples; see [`examples.md`](examples.md) for invocation patterns and anti-examples.

## Analysis modes

| Mode | Use when | Questions | Specialist lanes | Synthesis |
|---|---|---:|---:|---|
| LIGHT | Narrow, reversible, low downside, adequate facts | 0-3 | 0-1 | Sonnet 5 inline |
| STANDARD | Moderate ambiguity, multiple options, uncertain evidence, cross-team effects | 0-5 grouped | 2-3 adaptive | Sonnet 5; Opus 4.8 when conflict/coupling remains |
| DEEP | High downside, hard-to-reverse, regulated/high-stakes, severe conflict or systemic coupling | 0-5 initial; one focused high-stakes follow-up | 3-5 adaptive | Opus 4.8 xhigh |

All modes still apply all six work gates and all five pitfall checks. Mode changes depth and orchestration, not the disciplines.

## Model policy

| Role | Pinned model |
|---|---|
| Skill, routing, intake, probing | `claude-sonnet-5` |
| Specialist lanes | `claude-sonnet-5` |
| Per-lane cross-examiner (`lane-adversary`) | `claude-sonnet-5` |
| Completeness critic (`completeness-critic`) | `claude-sonnet-5` |
| Coordinator | `claude-sonnet-5` |
| High-complexity synthesis | `claude-opus-4-8` |
| Primary final validator | `claude-opus-4-8` |
| Adversarial final validator | `claude-opus-4-8` |
| Cross-model adversary (DEEP, decorrelation) | `claude-fable-5` → `claude-sonnet-5` fallback |
| Validation arbiter | `claude-opus-4-8` |
| Blind benchmark judge | `claude-opus-4-8` |

Final validation fails closed **at the Opus tier**. The certifier prefers `claude-opus-4-8` and may fall back within the Opus tier (`claude-opus-4-7` → `claude-opus-4-6` → `claude-opus-4-5`), recording the actual version (e.g. `VALIDATED (certifier: claude-opus-4-7)`); only when no Opus-tier model can run — or the actual final-gate model cannot be confirmed — does the report say `VALIDATION BLOCKED`. Sonnet is never accepted as a substitute **certifier**. The cross-model decorrelation reviewer prefers `claude-fable-5` and **falls back to `claude-sonnet-5` → `claude-sonnet-4-6`** (never Opus) — so a model-diverse gate is effectively always achievable; the report records `MODEL DIVERSITY UNAVAILABLE` only if neither can run. Per-role fallback chains and the two invariants (capability floor, model diversity) are in `skills/thinker/references/model-map.md`.

## Output

The default final report path is:

```text
docs/thinker-<problem-slug>.md
```

The report includes a tabulated executive summary, problem frame, decision-critical assumptions, routing and lane-selection ledger, six-gate analysis, five-pitfall audit, evidence and causal assessment, critical decision drivers, options, consequences, recommendation, action plan, and final validation record.

## Behavioral benchmark

Generate the 30-case × 4-variant run matrix:

```bash
python scripts/benchmark.py plan
```

After collecting runtime outputs and blind Opus judge records as JSONL:

```bash
python scripts/benchmark.py score --results path/to/results.jsonl
```

The harness tracks quality, question burden, lane count, model calls, token use, latency, and recommendation stability. It deliberately does **not** call the Anthropic API itself.

See [`docs/benchmarking.md`](docs/benchmarking.md) for the runtime protocol and record shape.

## Static package validation

```bash
python scripts/validate_package.py
```

The validator checks ten package-design acceptance gates, model pinning (including the Fable 5 cross-model reviewer), adaptive routing, material lane selection, per-lane cross-examination and completeness wiring, quantitative-reproduction and scope-completeness report sections, 8 core evals, 30 benchmark cases, the model-diverse Opus validation policy, and the Markdown report contract.

A `10/10` result from this script is a **static design acceptance score**, not proof of empirical decision quality. Runtime behavioral benchmarking is required before claiming production-proven performance.

## Package map

```text
thinker-skill-plugin/
├── .claude-plugin/
│   └── plugin.json
├── README.md
├── examples.md
├── agents/
│   ├── problem-framer.md
│   ├── systems-expander.md
│   ├── evidence-challenger.md
│   ├── priority-analyst.md
│   ├── consequence-analyst.md
│   ├── completeness-critic.md
│   ├── lane-adversary.md
│   ├── thinker-coordinator.md
│   ├── synthesis-analyst.md
│   ├── final-opus-validator.md
│   ├── final-opus-adversary.md
│   ├── crossmodel-adversary.md
│   ├── final-opus-arbiter.md
│   └── benchmark-opus-judge.md
├── docs/
│   ├── architecture.md
│   ├── benchmarking.md
│   ├── creation-report.md
│   └── usage.md
├── scripts/
│   ├── benchmark.py
│   └── validate_package.py
└── skills/
    └── thinker/
        ├── SKILL.md
        ├── evals/
        │   ├── evals.json
        │   └── benchmark-cases.json
        └── references/
            ├── routing-modes.md
            ├── user-probing.md
            ├── six-levels.md
            ├── five-pitfalls.md
            ├── orchestration.md
            ├── report-contract.md
            ├── opus-validation.md
            ├── model-map.md
            └── benchmarking.md
```

See [`examples.md`](examples.md) for worked invocation patterns and anti-examples.
