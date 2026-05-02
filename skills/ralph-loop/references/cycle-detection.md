# Ralph — cycle detection

## Why

Refining skills can oscillate: `/theme-bolder` → `/theme-quieter` → `/theme-bolder` on the same file is a sign of either (a) the persona is unstable or (b) the underlying decision is unsettled. Either way, Ralph should refuse to participate.

## Tracking

Every Ralph tick that spawns a skill records:

```python
{
  "ts": "<iso>",
  "tier": "<watch|mechanical|composer>",
  "operator": "<skill-name>",
  "files_touched": ["lib/.../foo.dart", ...],
  "task_id": "T-NN",
  "tick_index": <int>
}
```

In a sliding window of the last 3 ticks (configurable: `cycle_window: 3` in `budget.yaml`).

## Detection rule

For each tick:

1. Look at the last 3 ticks (window).
2. Group by file path.
3. Per file, list the operators that touched it (in order).
4. If the sequence contains a known oscillation pattern, halt.

Known oscillation patterns:

- `/theme-bolder` then `/theme-quieter` (or reverse) on the same file within window.
- `/theme-distill` then `/theme-create` (re-introducing tokens just removed).
- Any operator appearing 3 times within the window on the same file.

## Halt action

```jsonl
{
  "ts": "<iso>",
  "tier": "composer",
  "halt_reason": "cycle_detected",
  "operators": ["/theme-bolder", "/theme-quieter"],
  "file": "lib/features/coupon-unlocked/page.dart",
  "tick_window": 3
}
```

Exit code 1 (unsafe — needs human review of the underlying decision).

## Recovery

1. Inspect `decisions.md` for the locked axis/scope on the file's feature.
2. If decision is genuinely contested, supersede with a new entry — `cycle_detected` becomes evidence the prior decision was unsettled.
3. If decision is clear and one of the operators was in error, remove the offending step from `tasks.md` and re-run.
4. If oscillation is intentional (rare; e.g. testing two versions), bump `cycle_window: 0` temporarily — but log why in `decisions.md`.

## Anti-patterns

- ❌ Bypassing cycle detection by renaming files between ticks. The detector tracks file content hash too if `cycle_strict: true` (default off).
- ❌ Setting `cycle_window: 0` permanently. The window exists for a reason.
- ❌ Treating cycle detection as the canonical signal that two skills are wrong. Often the signal is upstream — in `decisions.md` or `compose.md`.
