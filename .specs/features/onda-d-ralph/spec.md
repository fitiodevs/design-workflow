# Feature: onda-d-ralph

> Onda D — autonomy layer. New `ralph-loop/` skill with 3 tiers (Watch / Mechanical / Composer), budget enforcement, audit log, halt switch, GH Actions integration.

**Source plan:** `docs/design-spec-driven-plan.md` §5 Onda D + REQ-D1..REQ-D10.

## REQs (concise)

- REQ-D1 Skill scaffolding (thin orchestrator).
- REQ-D2 Tier 1 Watch — read-only audit + critique.
- REQ-D3 Tier 2 Mechanical — deterministic fixes only, opens PR draft.
- REQ-D4 Tier 3 Composer — executes approved sequence; halt 2-fail / requires_human / branch protection / halt file / budget.
- REQ-D5 Halt: `.design-spec/halt` file, budget exhaustion, SIGTERM.
- REQ-D6 Budget: `budget.yaml` with caps; tracker per call.
- REQ-D7 Audit log: append-only `loop-log/<date>.jsonl`.
- REQ-D8 Idempotency + cycle detection.
- REQ-D9 3 GH Actions workflows.
- REQ-D10 Persona injection per iteration.

## Acceptance

- [ ] ralph-loop/ valid per quick_validate.
- [ ] ralph_tick.py + ralph_budget.py present and runnable.
- [ ] 3 workflow templates in skills/ralph-loop/workflows/ (rename to .github/workflows/ on adopt).
- [ ] budget.yaml example.
- [ ] STATE.md updated.
