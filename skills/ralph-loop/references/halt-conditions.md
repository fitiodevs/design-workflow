# Ralph — halt conditions (canonical enumeration)

Checked at start of each tick (in this order; first match wins):

1. **`.design-spec/halt` file exists** → halt_reason: `halt_file`. Exit immediately, no further checks.
2. **Budget exceeded** → halt_reason: `budget_exceeded:<which>` (`tokens|minutes|usd|iterations`).
3. **SIGTERM / SIGINT received** → halt_reason: `external_signal`. Checkpoint state, exit.

Checked during a tick (after a skill spawn):

4. **Verify fail 2× consecutive on same task** → halt_reason: `verify_fail_2x:<task_id>`. Tier 3 only.
5. **Skill returned `requires_human: true`** → halt_reason: `requires_human:<reason>`.
6. **GitHub branch protection blocks push** → halt_reason: `branch_protection`. Tier 2/3.
7. **Cycle detected** (same operator+file within 3 ticks) → halt_reason: `cycle_detected`.
8. **Phase gate failure mid-tick** (e.g. tasks.md status reverted) → halt_reason: `gate_failure`.

## Halt action (always the same)

1. Append final entry to audit log (`loop-log/<date>.jsonl`).
2. Print one-line summary to stderr.
3. Exit code:
   - `0` if halt was intentional and clean (halt_file, budget_exceeded with no partial work).
   - `1` if halt was unsafe (cycle, gate failure, partial work without commit).
4. Do NOT auto-revert partial work. Idempotent re-run is the recovery path.

## Recovery

After any halt:

1. Inspect last `loop-log/<date>.jsonl` entry.
2. Address halt cause (e.g. fix flutter analyze errors; raise budget; review cycle).
3. Optionally remove `.design-spec/halt`.
4. Re-run `ralph_tick.py` with same args. Idempotency contract makes this safe.
