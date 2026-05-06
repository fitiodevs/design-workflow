# pause-state.yaml schema

```yaml
paused_at: <ISO 8601 with timezone, e.g. 2026-05-02T21:30:00Z>
active_feature: <slug>            # required, the feature being worked on
active_phase: discovery | compose | sequence | ship
active_task: T-NN | null          # null when phase != ship or before first task
last_commit: <8-char sha>
notes: |                          # optional, free text from user
  <multi-line>
```

## Lifecycle

1. **Created** by `/design-spec pause`.
2. **Read** by `/design-spec resume`.
3. **Deleted** when user confirms "continue" in resume (file is consumed by the resume act).
4. **Preserved** when user re-prioritizes (resume keeps file but adds `superseded_by` field pointing to the new active feature).

## Validation

- `paused_at` must parse as ISO 8601.
- `active_feature` must match an existing `.design-spec/features/<slug>/` directory.
- `active_phase` must be in the enum.
- `active_task` must match `T-\d+` if present, else null.

If validation fails on resume, productivity skill prints what's wrong and points at manual fix; never silently corrects.
