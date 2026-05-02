---
name: ship
description: Ship phase orchestrator. Reads approved tasks.md and executes tasks one by one — spawn skill, run verify, on pass commit with `Refs feature/T-id` footer, on fail halt cleanly. Always closes with `/theme-audit` and `/theme-critique` re-run, appended to ship-log.md. Refuses to start when tasks.md is not approved. Supports `--interactive` for human-confirm between tasks. Triggered by `/design-spec ship`, `/ship`, "execute the tasks", "shipa a feature".
---

# Skill: ship (`/design-spec ship`) — Ship phase, executes tasks.md

## Triggers

- **English:** `/design-spec ship <feature>`, `/ship`, "execute the tasks", "ship feature X"
- **Português:** `/design-spec ship <feature>`, `/ship`, "shipa a feature", "executa o tasks.md"
- **Natural language:** after tasks.md is approved.

## Phase gate (REQ-B3)

```
1. Read .design-spec/features/<feature>/tasks.md
2. If frontmatter.status != "approved" → halt with message naming current status.
3. Else proceed.
```

## Modes

| Mode                     | Behavior                                                                 |
|--------------------------|--------------------------------------------------------------------------|
| default                  | Auto-execute task-by-task; halt on first verify fail.                    |
| `--interactive`          | Pause for "y" confirmation between tasks (use when stakes high).        |
| `--dry-run`              | Print plan + verify commands; do not execute or commit.                  |

## Workflow per task

```
For each task T-NN in tasks.md (in dependency order):
  1. If task.skill not in canonical list → halt with "Coverage gap T-NN".
  2. Spawn task.skill with brief built from task.task + compose context.
  3. Wait for skill to return.
  4. Run each item in task.verify:
     - On any verify FAIL: halt; persist state; report failure with command + output.
     - On all PASS: continue.
  5. git add <touched files>
  6. git commit -m "<task.task>" with footer:
       Refs: <feature>/<T-NN>
       REQ: <REQ-id> (if present in task.refs)
  7. Mark task in tasks.md as `status: done`; persist.
  8. Move to next task whose blocks are all done.

After all tasks done:
  9. Run /theme-audit on touched paths.
 10. Run /theme-critique on the primary screen.
 11. Append both outputs to .design-spec/features/<feature>/ship-log.md.
 12. Update tasks.md frontmatter to status: consumed.
 13. Echo summary + audit/critique findings.
```

## Halt conditions

Ship halts cleanly (no partial corruption, state always recoverable) when:

- Verify fails for any task.
- Skill returns `requires_human: true`.
- `.design-spec/halt` file exists (Onda D kill switch — checked before each task).
- Budget exceeded (Onda D).
- User Ctrl-C / SIGTERM.
- Any task references a skill not in the canonical list.

On halt:

1. Current task marked `status: blocked` with reason.
2. ship-log.md gets a halt entry.
3. Echo to user: "Halted at T-NN: <reason>. To resume: fix and re-run `/design-spec ship <feature>` (will skip done tasks)."

## Atomic commits with REQ-ID (REQ-B5)

Every task → exactly 1 commit. Commit message format:

```
<imperative one-liner from task.task>

[optional body if multi-line context useful]

Refs: <feature>/<T-NN>
REQ: <REQ-id when present>
Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
```

**Squash forbidden during Ship** (REQ-B5.3) — preserves rollback granularity. If two tasks really should have been one, fix the tasks.md and re-run sequence; don't squash post-hoc.

## Resume semantics

Re-running `/design-spec ship <feature>` after a halt:

- Reads tasks.md.
- Skips tasks already `status: done`.
- Resumes at the first `pending` task whose blocks are all done.
- A `blocked` task remains blocked until human flips it back to `pending` (with optional reason in the body).

## ship-log.md format

```markdown
---
feature: <slug>
phase: ship
started: <iso>
ended: <iso>  # filled at completion or halt
final_status: completed | halted
---

## Run log

- T-01 — done — <commit-sha> — <duration>
- T-02 — done — <commit-sha> — <duration>
- T-03 — blocked — verify fail (`flutter analyze` → 3 issues) — <ts>

## Final audit
[output of /theme-audit on touched paths]

## Final critique
[output of /theme-critique on primary screen]
```

## Anti-patterns

- ❌ Auto-merge PR after Ship completes. Ship opens commits; merge is human (also locked in REQ-D4.4 for Ralph).
- ❌ Squash merge during Ship.
- ❌ Skip `/theme-audit` + `/theme-critique` final pair to "save time" — that's the verification.
- ❌ Continue past a halt by force-flipping `blocked → pending` without fixing the cause.
- ❌ Run Ship on a tasks.md that lists invented skill names (gate catches this; do not bypass).
