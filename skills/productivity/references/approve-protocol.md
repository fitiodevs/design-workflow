# `/design-spec approve <phase> <feature>` protocol

## Allowed phases

- `discovery` — flips `discovery.md` status `draft → approved`.
- `compose` — flips `compose.md` status `draft → approved`.
- `sequence` — flips `tasks.md` status `draft → approved` (note: file is `tasks.md`, not `sequence.md`).

`ship` is NOT in the list — Ship has no approval gate (tasks.md approval is the gate).

## Pre-flight checks

Before flipping status:

1. File `.design-spec/features/<feature>/<phase-file>.md` exists.
2. Frontmatter parseable.
3. Current status is `draft` (refuse if `approved`, `consumed`, or `in_progress`).
4. Required fields present per phase schema:
   - **discovery:** all 4 blocks have `status: complete`; Action plan section exists.
   - **compose:** palette + ≥1 mockup + Clara review per mockup + decisions logged.
   - **tasks:** ≥1 task; every task has id/skill/verify/blocks; no invented skills.

## Approval action

- Edit frontmatter `status: draft` → `status: approved`.
- Append `approved_at: <iso>` and `approved_by: <user/email if known else 'human'>`.
- Print summary + "Next: `/design-spec <next-phase> <feature>`".

## Refusal cases

- File missing → "Run `<phase-skill>` first."
- Status not draft → "Already in '<status>'. Re-running approve has no effect."
- Validation fail → list the failing requirement and point at the originating phase.

## Anti-patterns

- ❌ Approve via shell edit when validation would have failed. The convenience exists to enforce checks; bypassing it defeats the gate.
- ❌ Auto-approve in CI without human in loop. Approval is a human decision (REQ-D4.4 spirit).
- ❌ Flip `approved → draft` to "redo" something. Drafts are forward-only; instead, supersede via a new feature/phase or copy to a new feature slug.
