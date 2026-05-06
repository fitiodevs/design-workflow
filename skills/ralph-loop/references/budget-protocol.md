# Ralph — budget protocol

## `budget.yaml` schema (project root)

```yaml
# Hard caps. Loop halts at 100%; warns at 80%.
max_tokens_per_loop: 200000        # cumulative input+output across ticks within one --loop run
max_minutes_per_loop: 30           # wall-clock since loop start
max_usd_per_day: 5.00              # rolling 24h window from first tick of the day
max_iterations_per_loop: 50        # ticks within one --loop run

# Per-tier overrides (optional)
tiers:
  watch:
    max_tokens_per_loop: 50000
    max_minutes_per_loop: 10
  mechanical:
    max_tokens_per_loop: 150000
    max_minutes_per_loop: 20
  composer:
    max_tokens_per_loop: 300000
    max_minutes_per_loop: 60
```

## Tracker

`scripts/ralph_budget.py`:

- Reads `budget.yaml` once per loop start.
- Maintains in-memory cumulative counters (tokens, USD, ticks).
- Computes `minutes_elapsed` from loop start.
- Per-tick: queries the spawned skill's input/output token counts (when available; else estimate from text length / 4).
- Writes per-tick budget snapshot to audit log entry.

## Threshold actions

| Threshold | Action |
|-----------|--------|
| 80% any cap | Append `warn` entry to audit log; print to stderr |
| 100% any cap | Halt with `halt_reason: budget_exceeded:<which>` |
| 110% (overshoot, race) | Halt + emit critical entry; investigate next session |

## Cost estimate (rough)

- Tier 1 Watch: ~5K tokens/tick × ~10 ticks/day = 50K tokens/day ≈ $0.40/day at Sonnet rate.
- Tier 2 Mechanical: ~30K tokens/tick × 5-10 ticks/run weekly = 150-300K weekly ≈ $1-2/week.
- Tier 3 Composer: ~50-200K tokens/run depending on tasks.md size.

`max_usd_per_day: 5.00` is conservative; OSS adopters often need $1; enterprise sets to $20+.

## Anti-patterns

- ❌ Mutating `budget.yaml` from inside Ralph (e.g. raising caps when nearing limit). Budget is human-set; loop respects.
- ❌ Soft caps that "skip a tick" instead of halting. Halt is intentional — 100% means stop.
- ❌ Sharing budget across loops by accident (e.g. forgetting to reset counter on `--loop` restart). Each `--loop` invocation is a fresh budget window.
