# Model map and fallback policy

Frontmatter `model:` on `SKILL.md` and every agent pins the **preferred** model for
that role. Some environments will not have that exact model or version. When a
preferred model cannot run, the coordinator invokes the same agent with a **runtime
model override** taken from the ordered fallback chain below, and records the
**actual** model that ran so the report stays auditable.

This generalizes a pattern the skill already uses: `crossmodel-adversary` is pinned to
`claude-fable-5` but runs on `claude-sonnet-5` when Fable 5 is unavailable. The
frontmatter pin is never edited to a fallback value — the pin is the *preference*, the
chain is the *degradation path*, and the runtime override is what changes.

## Two invariants every fallback must preserve

1. **Capability floor.** Never drop a role below its tier. Never substitute Haiku,
   `inherit`, an unknown model, or any model below Sonnet for any configured role.
2. **Model diversity.** The decorrelation reviewer (`crossmodel-adversary`) must always
   run on a **different model family than the certifier's actual model**. Its fallback
   chain is therefore constrained to be **non-Opus**.

## The map

Model IDs are current Anthropic IDs: Opus tier `claude-opus-4-8 → claude-opus-4-7 →
claude-opus-4-6 → claude-opus-4-5`; Sonnet tier `claude-sonnet-5 → claude-sonnet-4-6 →
claude-sonnet-4-5`; different-family `claude-fable-5` (and `claude-mythos-5` where the
workspace has it). `claude-opus-4-1` is intentionally excluded (retires 2026-08-05).

| Role | Agents | Preferred | Fallback chain (in order) | Exhausted-chain outcome |
|---|---|---|---|---|
| **Floor** | SKILL routing/intake/probing, `problem-framer`, `systems-expander`, `evidence-challenger`, `priority-analyst`, `consequence-analyst`, `lane-adversary`, `completeness-critic`, `thinker-coordinator` | `claude-sonnet-5` | `claude-sonnet-4-6` → `claude-sonnet-4-5` | Never below Sonnet tier; never Haiku or `inherit`. If no Sonnet-tier model can run, halt the run rather than drop to Haiku. |
| **Synthesis** (not a certifier) | `synthesis-analyst` | `claude-opus-4-8` | `claude-opus-4-7` → `claude-opus-4-6` → `claude-opus-4-5` → `claude-sonnet-5` (recorded downgrade) | Sonnet-5 synthesis is the STANDARD inline path and is acceptable here; record the actual model. |
| **Certifier** (fail-closed) | `final-opus-validator`, `final-opus-adversary`, `final-opus-arbiter`, `benchmark-opus-judge` | `claude-opus-4-8` | `claude-opus-4-7` → `claude-opus-4-6` → `claude-opus-4-5` | If **no Opus-tier model** can run: `VALIDATION BLOCKED — OPUS UNAVAILABLE`. Never certify on Sonnet, Fable, Haiku, or an unauditable model. |
| **Decorrelation** (different family) | `crossmodel-adversary` | `claude-fable-5` (or `claude-mythos-5` where present) | `claude-sonnet-5` → `claude-sonnet-4-6` | If neither a Fable- nor a Sonnet-family model can run: `MODEL DIVERSITY UNAVAILABLE`. **Never** fall back to any Opus model — that collapses diversity against the Opus certifier. |

## Recording the actual model

Whatever model actually runs, the agent reports it on its `MODEL:` line, and the
report's Final validation table lists each reviewer's actual model. A certifier that ran
on an Opus-tier fallback version is still a valid `VALIDATED` — for example,
`VALIDATED (certifier: claude-opus-4-7)`. The audit requirement is that the **tier** and
the panel's **model diversity** stay visible, not that one specific version ran.
