---
name: productivity
description: Productivity helpers for design-spec-driven workflow. Provides /design-spec pause to checkpoint active feature/phase/task to pause-state.yaml, /design-spec resume to summarize and continue, /design-spec status to print state inspector output, and /design-spec approve "phase feature" convenience for flipping draft to approved. Suggests light re-discovery when resume happens after 14 days. Triggered by `/design-spec pause`, `/design-spec resume`, `/design-spec status`, `/design-spec approve`, "pausa o trabalho", "retoma de onde parei".
---

# Skill: productivity (`/design-spec pause | resume | status | approve`)

## Triggers

- **English:** `/design-spec pause`, `/design-spec resume`, `/design-spec status`, `/design-spec approve <phase> <feature>`, "pause the workflow", "where are we?", "approve compose/sequence/tasks", "resume from where we stopped"
- **Português:** `/design-spec pause`, `/design-spec resume`, `/design-spec status`, `/design-spec approve <fase> <feature>`, "pausa o trabalho", "retoma o que parou", "qual o estado", "aprova compose/sequence/tasks"
- **Natural language:** end-of-day checkpoint; cold-start a session; review what's open.

## Subcommands

### `/design-spec pause`

Captures current state to `.design-spec/pause-state.yaml`:

```yaml
paused_at: <iso>
active_feature: <slug>
active_phase: discovery | compose | sequence | ship
active_task: T-NN | null
last_commit: <sha>
notes: <one-line free text from user, optional>
```

Writes the file. Echoes a summary + "Resume any time with `/design-spec resume`."

### `/design-spec resume`

Reads `pause-state.yaml`. Computes `now - paused_at`:

- **<14 days:** prints summary + asks "continue current task or re-prioritize?". User picks.
- **≥14 days:** prints summary + suggests "Recommend running `/juri --mode light` to update context — product/persona shift faster than a fortnight."

Resume does **not** auto-execute. It only orients. User decides the next command.

### `/design-spec status`

Wrapper around `python scripts/design_state.py`. Print prose by default; pass `--json` for machine output. See script for full schema.

### `/design-spec approve <phase> <feature>`

Convenience to flip frontmatter `status: draft → approved` on `.design-spec/features/<feature>/<phase>.md`. Validates schema before flipping. Refuses if file missing or status already `approved`/`consumed`.

Phase ⊂ {`discovery`, `compose`, `sequence`} (no `ship` — Ship doesn't have an approval gate; tasks.md is the gate).

## State files

```
.design-spec/
├── pause-state.yaml          # written by pause; deleted by resume after consume
├── features/<feature>/
│   ├── discovery.md
│   ├── compose.md
│   └── tasks.md
└── project/
    ├── decisions.md
    └── STATE.md (link)
```

## Anti-patterns

- ❌ Auto-resume after pause without user intent.
- ❌ Approve via this skill if the file is missing — refuse, point at the right phase to run.
- ❌ Modify approved files. Approval is one-way until `consumed` (which is set by the next phase reading it).
- ❌ Pause without writing the user's notes when given. Notes are the cheapest context preservation.
- ❌ Auto-execute resume's "continue" choice. Always confirm.

## Reference

- pause-state schema: `references/pause-state-schema.md`
- approve protocol: `references/approve-protocol.md`
