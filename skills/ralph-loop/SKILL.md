---
name: ralph-loop
description: Autonomous design-system maintenance loop with 3 tiers — Tier 1 Watch (read-only audit and critique, emits issues), Tier 2 Mechanical (deterministic fixes only, opens PR draft, never auto-merges), Tier 3 Composer (executes approved sequence.md task by task with halt and resume). Enforces budget caps from budget.yaml, append-only audit log in loop-log JSONL, halt file kill switch, persona injection per iteration, cycle detection. Ships GitHub Actions workflow templates. Triggered by `/ralph`, `/ralph-loop`, `/ralph watch|mechanical|composer`, "run autonomous loop", "spin up Ralph".
---

# Skill: ralph-loop (`/ralph`) — autonomy layer

## Triggers

- **English:** `/ralph`, `/ralph-loop`, `/ralph watch`, `/ralph mechanical`, `/ralph composer`, "run autonomous loop", "start ralph", "spin up watch tier"
- **Português:** `/ralph`, `/ralph-loop`, `/ralph watch|mechanical|composer`, "rodar loop autônomo", "ligar o ralph"
- **Natural language:** mention of CI/CD design system maintenance, daily drift cleanup, autonomous cleanup PR.

## Principle (Ralph)

**Dumb loop, smart prompt, hard halts.** The loop body is trivial — the intelligence is in the per-tier prompt and the halt protocol. Add brains to the prompt, not the loop.

## Position

```
Atomic skills           ← unchanged
Orchestration (B/C)     ← compose / sequence / ship
Autonomy (this)         ← ralph-loop wraps orchestration in cron + budget + halts
```

Ralph never invents new skills — it spawns existing ones. Ralph never approves phases — humans do.

## 3 tiers

### Tier 1 — Watch (read-only)

- Runs `/theme-audit` globally + `/theme-critique` on screens touched in last N hours.
- Emits structured issue payload (JSON) — does NOT edit code.
- Default tier; cheapest; runs daily on cron.
- Halt: never (idempotent reads).

### Tier 2 — Mechanical (deterministic fixes only)

- Accepts only fixes whose verify is provable: regex-replaceable hardcode → token, doc/themes auto-update on palette change, `_sync.sh` re-run on canonical script change.
- Opens **PR draft**, never merges (REQ-D4.4 spirit — Tier 2 also).
- Each fix has its own commit + verify.
- Halt: any verify fail → close PR with reason.

### Tier 3 — Composer (executes approved sequence.md)

- Reads approved `tasks.md` from a feature.
- Wraps `/design-spec ship` per-task; runs verify; commits; opens PR draft.
- **Never auto-merges** (REQ-D4.4, hard rule).
- Halt conditions (REQ-D4.3):
  - Verify fail 2× consecutive on same task.
  - Skill returns `requires_human: true`.
  - GitHub branch protection blocks push.
  - `.design-spec/halt` exists.
  - Budget exceeded.

## Halt switch

`.design-spec/halt` (empty file) checked at start of every tick. If exists → exit immediately. Path is `.gitignore`d so local kill is local.

To stop a remote loop: commit a `halt` file at the path. Ralph reads, exits within 1 tick.

## Budget enforcement

`budget.yaml` (project-root) declares hard caps:

```yaml
max_tokens_per_loop: 200000
max_minutes_per_loop: 30
max_usd_per_day: 5.00
max_iterations_per_loop: 50
```

`scripts/ralph_budget.py` tracks usage per tick + per day; halts at 100%; warns at 80%. See `references/budget-protocol.md`.

## Audit log

Append-only JSONL at `.design-spec/features/<feature>/loop-log/<YYYY-MM-DD>.jsonl`:

```jsonl
{"ts":"2026-05-02T10:00:00Z","tier":"composer","task_id":"T-03","skill":"/theme-port","input_tokens":4200,"output_tokens":1800,"cost_usd":0.027,"verify_result":"pass","commit_hash":"ab12cd3"}
{"ts":"2026-05-02T10:01:00Z","tier":"composer","task_id":"T-04","skill":"/theme-extend","input_tokens":2100,"output_tokens":900,"cost_usd":0.014,"verify_result":"fail","halt_reason":"flutter_analyze_3_issues"}
```

Greppable + DuckDB-friendly. Never rotated by Ralph (ops decision).

## Persona injection per iteration

Each tick re-loads the spawned skill's `voice_dna` block from its SKILL.md. Does not trust accumulated context. Drift detection: vocabulary distance from `voice_dna.always_use` set checked every 10 ticks; flag in log if drifts.

See `references/persona-injection.md`.

## Cycle detection

Tracks (operator, file, ts) tuples. Refuses oscillations within 3 ticks (e.g. `/theme-bolder` then `/theme-quieter` on the same file). Logs:

```jsonl
{"ts":"...","tier":"composer","halt_reason":"cycle_detected","operators":["/theme-bolder","/theme-quieter"],"file":"lib/.../coupon_page.dart"}
```

See `references/cycle-detection.md`.

## Idempotency contract

Every operator MUST be safe to invoke 2× without side effect. Onda D enforces by:

- Tracking `task_state: pending|in_progress|done|blocked` between ticks.
- On crash mid-task, resume reads state and skips work already done.
- New skills must declare `idempotent: true` in SKILL.md frontmatter (Onda D+ enforcement; soft warn now).

## CLI

```bash
# Single tick (used by GH Actions)
python scripts/ralph_tick.py --tier {watch|mechanical|composer} --feature <slug>

# Loop until halt or budget
python scripts/ralph_tick.py --tier composer --feature <slug> --loop

# Inspect budget
python scripts/ralph_budget.py [--feature <slug>] [--day <YYYY-MM-DD>]
```

## GitHub Actions workflows

Templates in `workflows/`:
- `design-watch.yml` — Tier 1, daily cron + on push to main.
- `design-pre-merge.yml` — Tier 1, on PR open/sync.
- `design-sprint.yml` — Tier 2, weekly Friday 17h UTC-3.

Adopters copy to `.github/workflows/` and tweak.

## Anti-patterns

- ❌ Auto-merge from any tier. Hard rule (REQ-D4.4) — Tier 2 and 3 always PR draft.
- ❌ Skip the halt file check at tick start. Halt is fastest exit; check first.
- ❌ Mutate `budget.yaml` from inside Ralph. Budget is human-set.
- ❌ Cross-tier escalation without human (e.g. Watch finding becomes Mechanical run automatically). Each tier is its own decision.
- ❌ Run loop without `voice_dna` re-load (drift over 50+ ticks is real).
- ❌ Loop body with embedded brains. Loop is dumb; prompt is smart.

## References

- `references/budget-protocol.md` — caps, tracker, threshold actions.
- `references/persona-injection.md` — voice_dna re-load mechanics.
- `references/cycle-detection.md` — 3-tick window, file-level tracking.
- `references/halt-conditions.md` — full enumeration.
- `references/audit-log-schema.md` — JSONL schema.
- `workflows/*.yml` — GH Actions templates.
