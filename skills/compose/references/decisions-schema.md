# Decisions schema (decisions.md)

> Single source of truth for project-level design decisions across phases (compose / sequence / ship / refining).

## File location

`.design-spec/project/decisions.md`

## YAML schema (per entry)

```yaml
- id: D-<seq>           # zero-padded 3-digit sequence (D-001, D-002, ...)
  decision: <string>    # one line, present tense ("axis = drenched warm")
  reason: <string>      # tied to discovery answer / audit signal / persona
  date: <YYYY-MM-DD>
  phase: <compose | sequence | ship | refine>
  feature: <slug>
  supersedes: <D-id|null>  # null when first; D-id when overriding
  locked_by: <skill-name>  # who wrote this; e.g. compose, /theme-create
```

## Lifecycle

1. **Write.** Compose / Sequence / Ship phases write entries when locking axis, token semantic intent, scope.
2. **Read.** Refining skills (`/theme-bolder`, `/theme-quieter`, `/theme-distill`, `/theme-motion`) MUST read `decisions.md` before proposing a change.
3. **Conflict.** When a refining proposal contradicts a locked decision, the skill MUST surface the conflict to the user before acting:
   > "Proposed: drop saturation -20%. Conflict: D-007 locked axis=drenched (Maria persona, peak-end at coupon unlock). Confirm override (creates D-NNN supersedes D-007) or cancel?"
4. **Supersede.** Override creates new entry with `supersedes` pointing at the prior id; prior is not deleted (audit trail).

## Example file

```markdown
# Project decisions — <project>

> Auto-managed by compose / sequence / ship phases and refining skills.
> Edit manually only to fix typos; logical changes go through the supersede mechanism.

## Decisions

- id: D-001
  decision: "axis = drenched warm"
  reason: "Maria persona requires visceral reward at peak-end (discovery P3.1)"
  date: 2026-05-02
  phase: compose
  feature: coupon-unlocked
  supersedes: null
  locked_by: compose

- id: D-002
  decision: "feedbackSuccess = warm-amber instead of green"
  reason: "Banco-digital anti-ref in product.md §7; green reads finance-cold"
  date: 2026-05-02
  phase: compose
  feature: coupon-unlocked
  supersedes: null
  locked_by: /theme-create
```

## Anti-patterns

- ❌ Editing an existing entry's `decision` or `reason` text — always supersede instead (audit trail).
- ❌ Deleting entries — supersedes preserve history; deletion erases the why.
- ❌ Writing without `reason` field — every decision must trace to discovery / audit / persona.
- ❌ Reusing `id` after supersede — sequence is monotonic.
