# Ship — halt protocol

> What ship does when something stops it from continuing safely.

## Halt triggers (canonical list)

1. **Verify fail.** Any verify item in a task returns non-zero / asserts false.
2. **Skill returns `requires_human: true`.** Atomic skill flagged ambiguity.
3. **`.design-spec/halt` exists.** Kill switch (Onda D).
4. **Budget exceeded.** Token / minutes / USD threshold from `budget.yaml` (Onda D).
5. **External signal.** SIGTERM / Ctrl-C / CI cancellation.
6. **Coverage gap.** Task names a skill not in canonical list.
7. **Approval drift.** Phase gate failed mid-flight (rare; e.g. someone reverted compose.md status).

## Halt sequence (always the same)

1. Mark current task `status: blocked` in tasks.md with `block_reason: <one-line>`.
2. Append entry to `ship-log.md` describing what happened.
3. Update ship-log frontmatter `final_status: halted`, `ended: <iso>`.
4. Do NOT auto-revert the partial work — it's safer to leave the half-edit visible than to silently undo.
5. Echo to user:
   ```
   Halted at T-NN: <reason>.
   Last commit: <sha>.
   To inspect:  cat .design-spec/features/<feature>/ship-log.md
   To resume:   /design-spec ship <feature>  (skips done tasks)
   To redirect: edit tasks.md, set blocked task status: pending, fix the cause, re-run.
   ```

## Resume after halt

- Re-run `/design-spec ship <feature>`.
- Tasks with `status: done` are skipped.
- The first `pending` task with all `blocks` done is the next executed.
- A task with `status: blocked` stays blocked until a human flips it.

## Idempotency contract

The current task's partial work may have been committed (if commit happened before verify ran) OR may be uncommitted (if verify failed before commit). On resume:

- If committed: ship checks if the commit produced what verify expects; if yes, marks done and moves on.
- If uncommitted: ship re-runs the skill (assuming it's idempotent — REQ-D8.3 enforces this for Ralph).

Skills MUST be idempotent — running them twice on the same input produces the same effect (no double inserts, no duplicate widgets). When this contract is broken, halt is unsafe to resume; user must manually clean up.

## When halt is NOT used

- Single verify warning (not error): note in ship-log, proceed.
- Skill returned slow but correct: continue; budget tracker may halt later if overall threshold breached.
- Network blip retrying: skill-level retry, not ship-level halt.
