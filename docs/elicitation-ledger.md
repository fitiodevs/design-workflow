# Elicitation ledger — weak-supervision evidence across runs

> Adapted from claude-code-harness (`docs/sandbagging-aware-weak-supervision.md`,
> MIT). Not a model trainer — a per-project append-only ledger that lets
> reviewers persist evidence so the next generator run doesn't repeat known
> failures.

## Why this exists

Júri auditing today is good. The problem is that the **diagnosis evaporates
between sessions** — next time Clara mocks the same screen, she has no idea
what Júri said last week about `hero number bodyMedium em vez de displayLarge`.
The generator silently repeats the slop, Júri scores it again, the loop never
converges.

The ledger fixes this: reviewers append structured evidence; generators read
it as preamble. Same target → same trip-ups surfaced before the first paint.

## Storage

Per-project, append-only:

```
.design-spec/state/elicitation/<YYYY-MM-DD>.jsonl
```

One event per line. Each event conforms to schema `elicitation-event.v1`,
defined inline in `scripts/elicitation.py`. The ledger is local to the project
that is being designed — never the design-workflow repo itself.

## Event kinds

| `kind` | Who writes | When |
|---|---|---|
| `judge_verdict` | Júri (theme-critique), Lupa (theme-audit) | After a critique/audit reaches a verdict (`APPROVE` / `REQUEST_CHANGES` / `NEUTRAL`). One per run. |
| `counterexample` | Júri, Lupa | One per P0/P1 issue with concrete `file:line` evidence + named slop pattern. |
| `eval_result` | Lupa | Rolled-up audit metrics (violation counts, WCAG pass-rates). |
| `weak_label` | Any reviewer | Inconclusive observation worth recording without committing to severity. |
| `capability_probe` | Discovery (Júri `/juri` no args) | A discovery question presented to the user. Optional, low signal. |

## Required fields

| Field | Notes |
|---|---|
| `schema_version` | Always `"elicitation-event.v1"`. Auto-filled. |
| `kind` | One of the 5 above. |
| `ts` | ISO UTC timestamp. Auto-filled. |
| `target` | Path or feature slug — what is being judged. Substring-matched when reading, so `lib/features/coupons` matches `lib/features/coupons/page.dart`. |
| `source` | Skill name (`theme-critique`, `theme-audit`, etc.). |
| `summary` | One-line human-readable summary. |
| `severity` | `critical` / `major` / `minor` / `info`. Required for `counterexample`. |
| `verdict` | `APPROVE` / `REQUEST_CHANGES` / `NEUTRAL`. Required for `judge_verdict`. |
| `evidence_refs` | List of `file:line` references. Required for `counterexample`. |
| `slop_pattern` | Kebab-case name from `craft/anti-ai-slop.md` cardinal sins (or a new pattern you mint). Required for `counterexample`. |
| `privacy_tags` | Defaults to `["do_not_train"]`. Override only when explicitly authorized. |

## CLI

The script ships inside each consuming skill (`${CLAUDE_SKILL_DIR}/scripts/elicitation.py`).
Repo-root source-of-truth: `scripts/elicitation.py`. Synced via `scripts/_sync.sh`.

### Append (reviewer side)

```bash
python "${CLAUDE_SKILL_DIR}/scripts/elicitation.py" append judge_verdict \
  --target lib/features/coupons/coupon_detail_page.dart \
  --source theme-critique \
  --severity major --verdict REQUEST_CHANGES \
  --summary "Nielsen 21/40 — celebração tratada como listagem" \
  --evidence "lib/features/coupons/coupon_detail_page.dart:42-89" \
  --extra '{"score": 21, "rating": "needs work"}'
```

```bash
python "${CLAUDE_SKILL_DIR}/scripts/elicitation.py" append counterexample \
  --target lib/features/coupons/coupon_detail_page.dart \
  --source theme-critique \
  --severity major \
  --summary "Hero number bodyMedium em vez de displayLarge" \
  --evidence "lib/features/coupons/coupon_detail_page.dart:67" \
  --slop-pattern flat-hero-no-hierarchy
```

### Read / summarize (generator side)

```bash
# Human-readable preamble — drop into Clara/Arquiteto thought process
python "${CLAUDE_SKILL_DIR}/scripts/elicitation.py" summarize \
  --target lib/features/coupons --days 30

# Machine-readable for filtering
python "${CLAUDE_SKILL_DIR}/scripts/elicitation.py" read \
  --target lib/features/coupons --kind counterexample --days 30
```

The `summarize` output is ready to inject into the generator's preamble:

```
### Prior evidence on `lib/features/coupons` (last 30d)

- **Last verdict** (theme-critique, 2026-05-12): `REQUEST_CHANGES` — Nielsen 21/40 — celebração tratada como listagem
- **Recurring slop patterns:** flat-hero-no-hierarchy ×3, hardcoded-color ×2

**Counterexamples to avoid** (5 total, showing top 5):
  - [major] Hero number bodyMedium em vez de displayLarge · pattern: `flat-hero-no-hierarchy` · refs: …:67
  - [major] Accent color hardcoded como #6366f1 · pattern: `hardcoded-color` · refs: …:142
  - …

> Treat counterexamples above as slop traps. If the new output would repeat
> any pattern, revise before delivering.
```

## Skills currently wired

| Skill | Role | Where in flow |
|---|---|---|
| `theme-critique` (Júri) | Writer | Step 5.2 — after handoff write, append `judge_verdict` + 1 `counterexample` per P0/P1 issue. |
| `theme-audit` (Lupa) | Writer | Step 5 — append `eval_result` rollup + `counterexample` for top 5 offenders. |
| `frontend-design` (Clara) | Reader | Pre-flight before Step 1 — `summarize` for target, treat counterexamples as slop traps. |
| `theme-port` (Arquiteto) | Reader | Tier 5 of pre-flight context check — `summarize`, fail port if recurring `hardcoded-color` and Step 3 doesn't bind to semantic role. |

Extending to other skills (Brasa, Calma, Lâmina, Pena, Jack) is straightforward: add the sync entry in `scripts/_sync.sh` and the same `append` / `summarize` pattern in the SKILL.md.

## Anti-patterns

- ❌ Persisting P2/P3 issues as counterexamples. Sinal alto, ruído baixo — só P0/P1.
- ❌ Inventing slop pattern names ad-hoc. Reuse names from `craft/anti-ai-slop.md` when possible; if minting, keep kebab-case + ≤3 words.
- ❌ Reading the ledger and ignoring it. If you read evidence and proceed without revising, you've just confirmed the regression.
- ❌ Forwarding the ledger to external systems without explicit privacy flag override. Default is `do_not_train` and that is intentional.

## What this is NOT

- Not a model trainer. No SFT, no RLHF, no hidden capability evals.
- Not a replacement for the handoff system (`.claude/handoffs/*.yaml`). Handoffs are protocol between agents in a single session. The ledger is across sessions.
- Not a build-time gate. Empty ledger → no failure. The pattern is additive.
