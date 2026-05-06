# Feature: onda-b-workflow

> Onda B — wraps atomic operators with phase gates. Compose / Sequence / Ship as orchestration skills. Decisions tracking. Atomic commits with REQ-ID.

**Status:** Draft → Implementing
**Owner:** fitiodev
**Created:** 2026-05-02
**Sized:** Large
**Source plan:** `docs/design-spec-driven-plan.md` REQ-B1..REQ-B5

## Requirements (sumarizadas — plan é fonte completa)

- **REQ-B1** `/design-spec compose <feature>` reads approved discovery.md → emits `compose.md` (palette + 1-3 mockups + Clara review). Refuses if discovery.md status ≠ approved.
- **REQ-B2** `/design-spec sequence <feature>` reads approved compose.md → emits `tasks.md` with atomic tasks each with `verify:` block (binary pass/fail).
- **REQ-B3** `/design-spec ship <feature>` executes tasks task-by-task; runs verify between; halts on fail.
- **REQ-B4** `decisions.md` schema `{id, decision, reason, date, supersedes?}`; refining skills consult it before acting.
- **REQ-B5** Atomic commits with `Refs: <feature>/<task-id>` footer. Squash forbidden during Ship.

## Acceptance

- [ ] 3 new skills under `skills/{compose,sequence,ship}/` valid per quick_validate.
- [ ] Phase gate refuses unapproved input.
- [ ] `decisions.md` schema documented + read-protocol for refining skills.
- [ ] STATE.md ganha Onda B section.
