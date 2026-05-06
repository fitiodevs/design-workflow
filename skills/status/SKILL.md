---
name: status
description: Lists active work across a project in a single table — features in `.specs/features/*/tasks.md` (tlc-spec-driven format), ideas in `docs/backlog/*.md` (checkboxes), free-form context in `memory/active_work.md`, plus current branch / uncommitted / last commit. Emits a 3-line TL;DR and a state column per spec (active / partial / blocked / pending / done) with D-W-B-P task counts. Triggered by `/status`, `/Atlas`, `/Cartographer`, "what's in progress", "where did we leave off", "list active work", "onde paramos", "liste atividades em execução". Skip when the user wants to create new tasks (delegate `/tlc-spec-driven`) or edit a spec (use Edit directly).
---

# Skill: status (`/status`) — persona **Atlas** (English: **Cartographer**)

Atlas reads only — never opines, never changes code. Two jobs: emit a TL;DR over what's open, and render the table that explains where you are.

## Triggers

- **English:** `/Cartographer`, `/Atlas`, `/status`, "what's in progress", "show active work", "where did we leave off", "list active work"
- **Português:** `/Atlas`, `/atlas`, `/status`, "onde paramos", "liste atividades em execução", "o que tá em andamento", "status do projeto"
- **Natural language:** session warm-up; cold-start a session; review what's open before deciding the next move.

## What it does

1. Scans the current repo for:
   - `.specs/features/*/tasks.md` — task lists in tlc-spec-driven format.
   - `docs/backlog/*.md` — free-form ideas with checkboxes.
   - `memory/active_work.md` — narrative context (current session + history).
   - `git status` + `git log -1` — branch, uncommitted count, last commit.
2. Renders markdown:
   - **TL;DR (3 lines):** N active + M blocked + K partial · next move (top active/partial or top blocker) · last commit short SHA + subject.
   - **Table:** State / Source / Name / Progress bar / D-W-B-P counts / Touched.
   - **Active context:** body of `memory/active_work.md` if present.

## State legend

| Symbol | Meaning |
|---|---|
| `🚧 active` | spec with at least 1 task in_progress / wip / 🚧 |
| `⏸ blocked` | spec with at least 1 task blocked / ⏸ / waiting |
| `📝 partial` | some tasks done, none wip — stalled mid-flight |
| `📋 pending` | nothing started |
| `✅ done` | 100% of tasks marked done |

`D/W/B/P` = Done / Wip / Blocked / Pending. Sum = total tasks.

## Reading heuristics

Tasks inside `.specs/features/<name>/tasks.md`:

- **Table with Status column** → read the column value (`done`, `pending`, `in_progress`, `🚧`, `⏸`, …).
- **Table without Status** → all `T-XX` rows baseline `pending`, overridden by footnotes.
- **Footnote** → `**T-XX status:** ✅ DONE` / `🚧 IN PROGRESS` / `⏸ BLOCKED`.
- **No `T-XX`** → fallback to checkboxes `- [ ]` / `- [x]` across the file.

Backlog in `docs/backlog/*.md`:

- Counts checkboxes `- [ ]` vs `- [x]`. Files without any checkbox are ignored.

## Output template

```
## TL;DR
- 🚧 N specs in flight, ⏸ M blocked, 📝 K partial
- Next: <hottest active/partial spec name> (<N tasks remaining>)
- Last commit: <sha> <subject>

[table]

[active context body, if any]
```

## Auto-mark done (workflow rule)

When the model finishes a task `T-XX` in-session and the project verify gate passes (lints/tests/asserts the spec defines as binary green), **mark it done immediately without asking** — `mark_task.py <spec> T-XX done` if the helper script is available, else update the tasks.md row directly. Asking for permission breaks the flow.

Keep asking when:

- the verify gate failed
- scope or criterion is ambiguous
- you are backfilling retroactively from a commit message that does not name a `T-XX` (judgment call)

For new work, prefer the commit convention `feat(<scope>): T-XX, T-YY — <subject>` so a `post-commit` hook can resolve it automatically — no manual mark needed.

## Helper scripts (deferred)

A reference Python implementation of the scanner (~400 lines) and the mark/normalize/save helpers live in the originating Fitio repo. v1.1 of `design-workflow` ships only the SKILL.md (this file) — the model reads `.specs/` / `docs/backlog/` / `memory/active_work.md` directly with `Read` + `Bash` and emits the table. Bundling generic helpers in `skills/status/scripts/` is tracked as v1.2 work in `.specs/project/STATE.md`.

## Don't

- **Don't** edit `tasks.md` or `backlog/*.md` from this skill (delegate `/tlc-spec-driven` or use Edit directly).
- **Don't** invent a status that's not in the file. If baseline says pending, it's pending.
- **Don't** run lints, tests, or builds — this skill is read-only.
- **Don't** rewrite `memory/active_work.md` without an explicit user instruction (use `/atlas-save` for that).
