# design-spec-driven — Implementation Plan

> **Status:** Plan only — no code yet. Documented for a fresh session to execute "vai full".
> **Owner:** fitiodev
> **Created:** 2026-05-02
> **Sized:** Complex (ambiguity + new domain + 4 multi-component ondas)
> **Scope:** Evolution of `design-workflow` v0.2.0 → `design-spec-driven` v0.3+ — enterprise-grade orchestrator with autonomous execution layer.
> **Source of truth:** 6 memory files in `/home/fitiodev/.claude/projects/-media-fitiodev-FITIO-Skill-design-workflow/memory/`. Do not contradict. Update memory if reality drifts.
> **Method:** spec-driven workflow inspired by `~/.claude/skills/tlc-spec-driven/SKILL.md` (4 phases: Specify → Design → Tasks → Execute, auto-sized).

---

## How to read this document

This is a **planning artifact**, not a runtime spec. A fresh session running "vai full" should:

1. Read `MEMORY.md` and the 6 memory files first (constraints + decisions already locked).
2. Read this doc end-to-end (overall plan + REQs + risks + acceptance per onda).
3. Read `.specs/features/skill-creator-alignment/{spec,design,tasks}.md` (template — same format will be used per onda).
4. Read `.specs/project/STATE.md` (current state, deferred follow-ups).
5. Then split this plan into formal `.specs/features/<onda-name>/{spec,design,tasks}.md` files — one feature per onda — and execute Onda A first.

The plan is intentionally large (one doc, 4 ondas) so a fresh session sees the whole arc. Per-onda specs will be **subsets** of this doc, not redefinitions.

---

## 1. Context

`design-workflow` v0.2.0 ships 13 atomic skills (theme-create, theme-port, theme-extend, theme-audit, theme-critique, theme-bolder/quieter/distill, theme-motion, theme-prompt, theme-sandbox, frontend-design, ux-writing) usable individually but **not orchestrated**. The user ships them per-skill, manages state in their head, decides ordering ad-hoc, and re-runs audit manually.

The user's framing (2026-05-02): "elas servem apenas ao projeto que foi criado" + "quero design-spec a skill que empresas gigantes irão colocar no pipeline de produção".

Two transformations are needed:

1. **Layer above** — discovery + spec-driven workflow + autonomy loop, on top of the 13 atomic skills. Skills become operators; new layer becomes orchestrator.
2. **Enterprise readiness** — budget caps, audit logs, GH Actions integration, halt conditions, cost dashboards. Not "AI for design students" — "AI for design system teams at scale".

The 4-onda plan below sequences this transformation. Onda A is the foundation; Ondas B/C/D each depend on the prior. Skipping ahead is forbidden — Ralph (Onda D) on a weak Discovery (Onda A) is "Ralph rodando em chão de areia".

---

## 2. Goal

After all 4 ondas, `design-spec-driven` v1.0 should:

- Replace the 8–15 person design-system maintenance team at a mid/large eng org with **3–5 humans + Ralph Loop** running daily/weekly.
- Make every design-system intervention (palette change, new feature port, drift cleanup) **traceable**: spec → tasks → atomic commits → audit log.
- Force deliberate decisions through **approval gates** between phases — refuses to execute on unvalidated PRDs, ambiguous mood, or unverified palette.
- Run **autonomously** in CI/CD for the 70% of work that is mechanical (audit, drift remediation, regression detection), while keeping humans on the 30% that needs taste.
- Be **stack-agnostic enough** that adoption requires < 1 day of config (not weeks of refactor).

---

## 3. Non-goals

- **Not** a replacement for design tools (Figma). It orchestrates around them.
- **Not** a CMS for design tokens. Tokens live in the project's repo (`AppColors`, etc) — design-spec-driven reads/writes them, doesn't host them.
- **Not** a free-tier consumer product. Enterprise positioning includes paid LLM API + CI minutes. Cost model is part of the value, not a bug.
- **Not** auto-merging Ralph PRs. Tier 3 always opens PR draft; humans approve merges always. Hard rule.
- **Not** a generic SDLC tool. Stays focused on design system lifecycle. If someone wants generic spec-driven, they use `tlc-spec-driven`.
- **Not** discarding the 13 atomic skills. They remain usable standalone (`/theme-extend` direct works) — design-spec-driven is the orchestration layer above them.

---

## 4. Architecture overview

```
┌──────────────────────────────────────────────────────────────┐
│  HUMAN (designer / eng / PM)                                  │
│  ↓ "/juri" / "/design-spec specify <feature>"                 │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│  ORCHESTRATION LAYER (new — Ondas A/B/C)                      │
│  ┌────────────┐  ┌─────────┐  ┌──────────┐  ┌──────┐         │
│  │ Discovery  │→ │ Compose │→ │ Sequence │→ │ Ship │         │
│  │ (Júri)     │  │ (Comp + │  │ (Arq +   │  │      │         │
│  │            │  │  Clara) │  │  tasks)  │  │      │         │
│  └────────────┘  └─────────┘  └──────────┘  └──────┘         │
│       gate            gate          gate         gate         │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│  AUTONOMY LAYER (new — Onda D)                                │
│  ┌─────────────────────────────────────────────────────┐     │
│  │  Ralph Loop                                          │     │
│  │  ├─ Tier 1 Watch       (read, alert, no edit)        │     │
│  │  ├─ Tier 2 Mechanical  (deterministic fixes only)    │     │
│  │  └─ Tier 3 Composer    (executes approved sequence)  │     │
│  └─────────────────────────────────────────────────────┘     │
└──────────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────────────────────────────────────────────────┐
│  ATOMIC OPERATORS (v1.1)                                      │
│  theme-create · theme-extend · theme-audit · theme-port       │
│  theme-critique · bolder · quieter · distill · motion         │
│  frontend-design · ux-writing                                 │
└──────────────────────────────────────────────────────────────┘
                          ↕
┌──────────────────────────────────────────────────────────────┐
│  PERSISTENT STATE                                             │
│  .design-spec/                                                │
│  ├── features/<feature>/{discovery,compose,sequence}.md       │
│  ├── features/<feature>/tasks.md (atomic, with verify:)       │
│  ├── features/<feature>/loop-log/<date>.jsonl (audit trail)   │
│  ├── project/{STATE.md, decisions.md, budget.yaml}            │
│  └── halt  (kill switch — empty file = stop all loops)        │
└──────────────────────────────────────────────────────────────┘
```

**Layering rule (locked decision — see `feedback_design_spec_layering.md`):**
- The 13 atomic operators know almost nothing about the new layer.
- The new layer knows about all 13 operators.
- Atomic operators expose `requires_human: true` in output when input is needed; orchestration reads this and pauses.
- Refining operators (Brasa/Calma/Lâmina/Jack) consult `decisions.md` before proposing changes that contradict prior approved decisions.

---

## 5. The 4 ondas

### Onda A — Discovery foundation

Júri becomes the dual-mode orchestrator. Auto-sizes intervention (quick / light / full / greenfield). Produces PRD-per-intervention. Routes to Compositor / Clara / Pena / Jack with priority.

**Deliverables:**
- New skill `skills/discovery/` (or extension of `theme-critique` — final decision in spec.md).
- Auto-sizing detection logic (greenfield vs brownfield via `git log` + `find lib`).
- Brownfield pre-scan: silently runs `/theme-audit` before the interview to bring facts to the table.
- Structured 4-block interview (Produto / Tom / Identidade / Stack) — 1 block per turn, recuses vague answers ("moderno e clean" → re-ask).
- Doc generators: `discovery.md`, `docs/product.md` skeleton, `docs/design.md` skeleton, `docs/design-tokens.md` skeleton, `docs/PRD.md` (per-intervention).
- Routing output: priority-ordered action plan (not menu).
- `/juri --resume <feature>` retomar entrevista parcial.
- Memory expansion: `.design-spec/features/<feature>/discovery.md` + `.design-spec/project/decisions.md` initialized.

### Onda B — Spec-driven workflow

Compose / Sequence / Ship as wrapper skills with explicit approval gates. Atomic tasks with verify criteria. Decisions tracking.

**Deliverables:**
- `skills/compose/` — wraps `/theme-create` + `/frontend-design` with gate. Output: `compose.md` with palette + 1–3 mockups + Clara's review.
- `skills/sequence/` — Arquiteto persona emits `tasks.md` with atomic tasks, each with `verify:` block.
- `skills/ship/` — orchestrates `/theme-port` + `/theme-audit` + final `/theme-critique` re-run with gate.
- Phase gate protocol: `status: draft|approved|consumed` in YAML frontmatter of each phase doc.
- `decisions.md` format (decision + reason + date + supersedes); refining skills read it on invocation.
- Atomic commits per task with REQ-ID linkback in commit message.

### Onda C — Productivity layer

Pause/resume, discuss vs specify, state inspection script.

**Deliverables:**
- `/design-spec pause` — captures active phase + task + serializes to `.design-spec/pause-state.yaml`.
- `/design-spec resume` — reads pause-state, summarizes, asks "continue or re-prioritize?". After >14 days, suggests light re-discovery.
- `/juri discuss <topic>` — informal mode, no docs written, only socratic questions.
- `/juri specify <feature>` — formal mode (maps to existing discovery flow).
- `scripts/design-state.py` — reads `STATE.md` + per-feature dirs + git log, emits "you are at: phase Compose, task T-03 in progress, T-04/05 blocked, last commit ad12bc3".

### Onda D — Ralph autonomy

New skill `ralph-loop/`. 3 tiers with explicit halt conditions, budget caps, audit log, GH Actions integration.

**Deliverables:**
- `skills/ralph-loop/` (new, separate skill — see `decision_ralph_separate_skill.md`).
- Tier 1 Watch: read-only audit + critique + issue creation.
- Tier 2 Mechanical: deterministic fixes only (regex-replaceable hardcode → token, doc/themes auto-update on palette change, `_sync.sh` auto-run on script changes).
- Tier 3 Composer: executes approved `sequence.md` task-by-task to DONE/BLOCKED/QUESTION.
- `scripts/ralph-tick.py` — single iteration of the loop (Ralph principle: dumb loop, smart prompt).
- `scripts/ralph-budget.py` — cost dashboard (tokens / minutes / USD attribution per feature).
- `.design-spec/halt` — kill switch (empty file = stop).
- `loop-log/<date>.jsonl` — append-only audit trail.
- 3 GH Actions workflows: `design-watch.yml` (Tier 1, daily cron + on push), `design-pre-merge.yml` (Tier 1, on PR), `design-sprint.yml` (Tier 2, weekly Friday 17h).
- Budget enforcement: hard caps in `budget.yaml`; loop self-halts when exceeded.
- Persona injection per iteration (don't trust context, re-load `voice_dna` from SKILL.md each tick).
- Cycle detection: track which operator touched which file when, refuse oscillations (Brasa↔Calma) within N ticks.
- Idempotency contract: every operator must be safe to invoke 2× without side effect.

---

## 6. Requirements (REQ-01..REQ-24)

> Per-onda subsets. A fresh session running "vai full" should split these by onda when creating per-feature specs in `.specs/features/`.

### Onda A — Discovery foundation

#### REQ-A1 — Júri dual-mode trigger
- **REQ-A1.1** `/juri` with no args → discovery mode (interview).
- **REQ-A1.2** `/juri <flutter-path>` → existing critique mode (preserved, no breaking change).
- **REQ-A1.3** `/juri --discuss <topic>` → informal mode (no docs written).
- **REQ-A1.4** `/juri --resume <feature>` → continue paused interview.
- **Verification:** all 4 trigger forms produce distinct workflows; existing critique flows unchanged (regression test against current `theme-critique` evals).

#### REQ-A2 — Auto-sizing detection
- **REQ-A2.1** Detect greenfield (`git log --oneline | wc -l < 10` AND `find lib -name "*.dart" | wc -l < 5`) → recommend full+greenfield mode.
- **REQ-A2.2** Detect brownfield otherwise → recommend full mode + run silent pre-scan via `/theme-audit`.
- **REQ-A2.3** User can override with `--mode quick|light|full|greenfield`.
- **REQ-A2.4** Tier sizing must drive what gets generated: quick = no PRD, light = mini PRD, full = complete PRD + design.md + product.md skeletons.
- **Verification:** integration test in fresh empty Flutter project → greenfield detected; in cloned medium repo → brownfield detected; both produce expected doc set.

#### REQ-A3 — Structured interview protocol
- **REQ-A3.1** Júri asks 4 blocks in order: Produto (3 questions) → Tom (3) → Identidade (3) → Stack (2-3). Total 11–12 questions, never all at once.
- **REQ-A3.2** 1 block per turn; pauses for response before next block.
- **REQ-A3.3** Recuses vague answers ("moderno e clean", "tech profissional", "vibrante") and re-asks with concrete examples requested.
- **REQ-A3.4** First question is Produto, NEVER Stack. (Stack premature without product.)
- **Verification:** scripted eval where vague answers are given → Júri must recuse and re-ask in ≥80% of cases. Eval persona: "ambiguous user" with predefined vague answer set.

#### REQ-A4 — Brownfield pre-scan
- **REQ-A4.1** When brownfield detected, Júri runs `/theme-audit` silently before any question.
- **REQ-A4.2** Audit results inform questions ("you have 47 hex literals in `lib/features/<x>` — intentional brand color or hardcode drift?").
- **REQ-A4.3** Audit results saved as appendix to `discovery.md`.
- **Verification:** brownfield mode discovery output references concrete numbers from the audit (regex check on output).

#### REQ-A5 — Doc generation
- **REQ-A5.1** Júri writes `.design-spec/features/<feature>/discovery.md` with frontmatter `status: draft|approved|consumed`.
- **REQ-A5.2** For greenfield: writes skeletons of `docs/product.md` (sections §2/§3/§4/§5.3/§7/§8 from current Fitio template, generalized), `docs/design.md`, `docs/design-tokens.md`. Each section has placeholder content + comments explaining what to fill.
- **REQ-A5.3** For brownfield: writes `discovery.md` + `docs/PRD.md` (per-intervention only) + appends to existing `docs/design.md`.
- **REQ-A5.4** Júri NEVER edits files in `lib/`. Read-only on code; write-only on `docs/` + `.design-spec/`.
- **Verification:** post-discovery, `lib/` git-diff is empty; `docs/` git-diff matches expected file set per scenario.

#### REQ-A6 — Routing output
- **REQ-A6.1** Final discovery output is a priority-ordered action plan (not a menu of options).
- **REQ-A6.2** Each item: skill recommendation + 1-line reason + ETA estimate + blocking dependencies.
- **REQ-A6.3** Júri NEVER auto-runs the next skill (preserves user control, consistent with current critique).
- **Verification:** output structure matches schema (skill, reason, eta, blocks). Skill names must be from the 13 existing operators or new orchestration skills.

### Onda B — Spec-driven workflow

#### REQ-B1 — Compose phase wrapper
- **REQ-B1.1** `/design-spec compose <feature>` reads approved `discovery.md`, sequences `/theme-create` (palette) + `/frontend-design` (mockups) with a gate between them.
- **REQ-B1.2** If `discovery.md` status ≠ approved, refuse to start.
- **REQ-B1.3** Output: `compose.md` with palette + 1–3 mockup HTML paths + Clara review summary, frontmatter `status: draft`.
- **REQ-B1.4** Human approval changes status to `approved` (manual edit or `/design-spec approve compose <feature>`).
- **Verification:** unit test on phase gate (refuses unapproved input); integration test on greenfield feature → produces `compose.md` with all required artifacts.

#### REQ-B2 — Sequence phase (atomic tasks with verify:)
- **REQ-B2.1** `/design-spec sequence <feature>` reads approved `compose.md`, emits `tasks.md` with atomic tasks.
- **REQ-B2.2** Each task has fields: `id`, `task`, `skill`, `verify` (list of binary checks), `blocks` (list of task IDs), `estimate`.
- **REQ-B2.3** `verify` items are runnable shell commands or assertion strings ("flutter analyze → 0 issues", "python check_contrast.py X Y → ≥4.5", "regex `Color\\(0x[A-F0-9]+\\)` count = 0").
- **REQ-B2.4** Tasks must be ≤30min of work each (per tlc convention) and have binary pass/fail verify.
- **Verification:** generated `tasks.md` parses as valid YAML; every task has all required fields; running verify items in sequence produces a deterministic outcome.

#### REQ-B3 — Ship phase orchestration
- **REQ-B3.1** `/design-spec ship <feature>` reads approved `tasks.md`, executes task-by-task by spawning the named skill.
- **REQ-B3.2** Between tasks: runs verify; if pass → commit + mark task done; if fail → halt + report.
- **REQ-B3.3** Final task always: `/theme-audit` + `/theme-critique` re-run; result appended to `ship-log.md`.
- **REQ-B3.4** Manual mode: `/design-spec ship --interactive` pauses for confirmation between tasks.
- **Verification:** synthetic feature with 3-task sequence executes cleanly when verify passes; halts cleanly when verify fails (no partial state corruption).

#### REQ-B4 — Decisions tracking
- **REQ-B4.1** `decisions.md` schema: `{id, decision, reason, date, supersedes?}`.
- **REQ-B4.2** Refining skills (Brasa/Calma/Lâmina/Jack) MUST read `decisions.md` before proposing changes; if proposal contradicts a prior decision, must surface the conflict to user before acting.
- **REQ-B4.3** Júri writes decisions during discovery (e.g. "color commitment axis = drenched, reason: persona Maria needs visceral reward").
- **Verification:** integration test where Júri sets axis=drenched, then `/theme-quieter` is invoked → must surface the conflict, not silently override.

#### REQ-B5 — Atomic commits with REQ-ID
- **REQ-B5.1** Each task in Ship phase produces 1 commit.
- **REQ-B5.2** Commit message footer includes `Refs: <feature>/<task-id>` and `REQ-<id>` if traceable.
- **REQ-B5.3** Squash forbidden during Ship (preserves rollback granularity).
- **Verification:** post-Ship git log shows N commits for N tasks; each commit message contains the trace footer.

### Onda C — Productivity layer

#### REQ-C1 — Pause/resume
- **REQ-C1.1** `/design-spec pause` writes `.design-spec/pause-state.yaml` with active feature, phase, task, timestamp.
- **REQ-C1.2** `/design-spec resume` reads pause-state, summarizes, asks "continue or re-prioritize?".
- **REQ-C1.3** If resume happens >14 days after pause, Júri suggests light re-discovery before continuing.
- **Verification:** pause → fresh session → resume → state correctly restored, summary correctly identifies last action.

#### REQ-C2 — Discuss vs specify
- **REQ-C2.1** `/juri discuss <topic>` enters informal mode: only socratic questions, NO docs written.
- **REQ-C2.2** `/juri specify <feature>` enters formal mode: writes discovery.md + PRD.
- **REQ-C2.3** From discuss mode, Júri can suggest "ready to specify?" — transitions to formal with consent.
- **Verification:** discuss mode session produces zero file diffs; specify mode produces expected doc set.

#### REQ-C3 — State inspection script
- **REQ-C3.1** `python scripts/design-state.py` outputs: current feature, current phase, current task, blocked tasks, last commit hash + message.
- **REQ-C3.2** `--feature <name>` scopes to one feature.
- **REQ-C3.3** `--json` emits machine-readable for CI integration.
- **Verification:** script runs in <2s on a feature with 20 tasks; output schema validates against `references/state-schema.json`.

### Onda D — Ralph autonomy

#### REQ-D1 — Skill scaffolding
- **REQ-D1.1** New skill `skills/ralph-loop/` with own SKILL.md, references/, scripts/, evals/.
- **REQ-D1.2** SKILL.md description explicitly lists 3 tiers in spec-compliant frontmatter (no colons inside description — see `project_skill_creator_alignment_shipped.md` lesson).
- **REQ-D1.3** Skill body is THIN — pure orchestration, no design logic.
- **Verification:** `quick_validate.py` passes; skill body <250 lines.

#### REQ-D2 — Tier 1 Watch loop
- **REQ-D2.1** Reads-only: `/theme-audit` global + `/theme-critique` on screens touched in last N hours.
- **REQ-D2.2** Output: structured JSON for issue creation; never edits code.
- **REQ-D2.3** Default tier on activation; ON for all teams.
- **Verification:** synthetic regression (introduce hex literal in test repo) → Watch loop detects within 1 tick → emits issue payload.

#### REQ-D3 — Tier 2 Mechanical loop
- **REQ-D3.1** Accepts only deterministic fixes: regex-replaceable hardcode → token, doc/themes auto-update on palette change, `_sync.sh` auto-run on canonical script change.
- **REQ-D3.2** Opens PR draft, never merges.
- **REQ-D3.3** Each fix has provable verify (regex match + flutter analyze pass).
- **Verification:** synthetic dirty repo with N drift issues → Tier 2 produces PR draft fixing all → diff matches expected; flutter analyze passes.

#### REQ-D4 — Tier 3 Composer loop
- **REQ-D4.1** Reads approved `sequence.md`, executes tasks until DONE / BLOCKED / QUESTION.
- **REQ-D4.2** Per-task: spawn skill → run verify → commit → mark done → next.
- **REQ-D4.3** Halts at: verify fail 2× consecutive, skill returns `requires_human: true`, GitHub branch protection blocks push, `.design-spec/halt` file exists, budget exceeded.
- **REQ-D4.4** Always opens PR draft — NEVER auto-merges.
- **Verification:** synthetic 5-task sequence (mix of pass/fail/question) → Composer correctly handles each terminal state.

#### REQ-D5 — Halt conditions
- **REQ-D5.1** `.design-spec/halt` file presence is checked at every tick start; if exists, exit immediately.
- **REQ-D5.2** Budget exhaustion → graceful halt + status report.
- **REQ-D5.3** SIGTERM from CI → graceful halt + state checkpoint.
- **Verification:** create halt file mid-loop → Ralph exits within 1 tick; checkpoint state restorable.

#### REQ-D6 — Budget enforcement
- **REQ-D6.1** `budget.yaml` declares: `max_tokens_per_loop`, `max_minutes_per_loop`, `max_usd_per_day`, `max_iterations_per_loop`.
- **REQ-D6.2** Tracker updates after each tool call and skill invocation.
- **REQ-D6.3** Approaching threshold (80%) → warning in log; reaching threshold → halt.
- **Verification:** unit test where mock cost exceeds threshold → loop halts with correct exit code.

#### REQ-D7 — Audit log
- **REQ-D7.1** `.design-spec/features/<feature>/loop-log/<YYYY-MM-DD>.jsonl` — append-only.
- **REQ-D7.2** Each entry: `{ts, tier, task_id, skill, input_tokens, output_tokens, cost_usd, verify_result, commit_hash, halt_reason?}`.
- **REQ-D7.3** Greppable + processable by BI tools (DuckDB-friendly).
- **Verification:** log entries validate against schema; cost attribution per feature reproducible by query.

#### REQ-D8 — Idempotency + cycle detection
- **REQ-D8.1** Each task has `task_state: pending|in_progress|done|blocked` persisted between ticks.
- **REQ-D8.2** Crashed iteration must not duplicate work on next tick.
- **REQ-D8.3** Cycle detection: track operator touches per file with timestamp; refuse oscillations (Brasa↔Calma on same file within 3 ticks).
- **Verification:** simulated crash mid-task → state recovered correctly; oscillation attempt → detected and refused with clear log message.

#### REQ-D9 — GH Actions integration
- **REQ-D9.1** 3 workflow templates shipped in `.github/workflows/`:
  - `design-watch.yml` (Tier 1, schedule cron + on push to main)
  - `design-pre-merge.yml` (Tier 1, on PR open/sync)
  - `design-sprint.yml` (Tier 2, schedule weekly Friday 17h UTC-3)
- **REQ-D9.2** Each workflow uses `anthropic-ai/claude-action` (or equivalent) with skill name + tier + budget args.
- **REQ-D9.3** Workflows must run within free GitHub Actions tier for OSS adoption.
- **Verification:** workflows execute end-to-end on a fresh fork in <15min; cost stays within stated budget.

#### REQ-D10 — Persona injection per iteration
- **REQ-D10.1** Each Ralph tick re-loads `voice_dna` block from the invoked skill's SKILL.md.
- **REQ-D10.2** Does NOT trust accumulated context to preserve persona.
- **REQ-D10.3** Persona drift detection: if output vocabulary drifts from `voice_dna.always_use` set, flag in log.
- **Verification:** 50-tick simulated session → output vocabulary distance from `voice_dna` reference stays within tolerance.

---

## 7. Risks

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Discovery becomes burocracy users skip | High | High | Aggressive auto-sizing; legitimate quick mode; Júri recuses gracefully when full not needed |
| Ralph autonomous + Tier 3 ON merges 50 bad PRs overnight | Medium | Catastrophic | Tier 3 NEVER auto-merges (PR draft only); hard rule in REQ-D4.4 |
| Cost runaway in enterprise pilot | High | High | `budget.yaml` per repo; cost dashboard mandatory before Tier 2/3; alert at 80% |
| Locked-in bad decision at Compose phase → 100× damage | Medium | High | Phase approval gates inegociáveis; Compose never auto-approved |
| Trust collapse after 1 incident | Medium | High | Every Ralph commit has `revert: easy` (single commit, no squash); 2-min revert path |
| Persona drift after long Ralph sessions | High | Medium | REQ-D10 persona injection per iteration; drift detection |
| Stack-agnostic claim breaks for non-Flutter adopters | High | Medium | Honest positioning: "Flutter-first, adapter coming"; don't overclaim in Onda A |
| Onda B work requires Onda A APIs that aren't stable yet | High | Medium | Onda A must finish + soak ≥1 sprint before Onda B starts |
| Conflict between `decisions.md` and refining skill autonomy | Medium | Medium | Refining skills always surface conflict (REQ-B4.2), never silently override |
| `quick_validate.py` rejects new orchestration skill descriptions | High | Low | Apply lessons from `skill-creator-alignment` (no colons inside descriptions, no `<...>`) |
| Greenfield generated `docs/product.md` is too generic to be useful | Medium | Medium | Skeletons include Fitio-style examples as comments showing the shape expected |

---

## 8. Acceptance criteria (per onda)

### Onda A acceptance
- [ ] All REQ-A1..REQ-A6 verifications pass.
- [ ] Greenfield walkthrough: empty Flutter project → `/juri` → 11-question interview → `discovery.md` + 3 docs/skeletons + routing plan, in <60min.
- [ ] Brownfield walkthrough: cloned medium Flutter repo → `/juri` → silent audit + interview → discovery references concrete audit numbers + PRD focused on top 3-5 fixes.
- [ ] Critique mode regression: existing `theme-critique` evals (`evals/evals.json` for current `theme-critique` skill) still pass — Onda A doesn't break what shipped.
- [ ] Júri refuses vague answers ≥80% of evaluation set.
- [ ] `lib/` git-diff after discovery is empty.
- [ ] STATE.md updated with Onda A decisions, deferred items.

### Onda B acceptance
- [ ] All REQ-B1..REQ-B5 verifications pass.
- [ ] End-to-end: discovery (Onda A) → `/design-spec compose` → `/design-spec sequence` → `/design-spec ship` produces a feature port with N atomic commits, each with REQ trace.
- [ ] Phase gate refuses unapproved input (compose.md status=draft → ship refuses to start).
- [ ] Decisions tracking: synthetic conflict (axis=drenched then `/theme-quieter`) surfaces conflict.
- [ ] All 13 atomic operators consulted by orchestration produce expected outputs (no silent regressions).

### Onda C acceptance
- [ ] All REQ-C1..REQ-C3 verifications pass.
- [ ] Pause → 14+ days → resume → re-discovery suggested.
- [ ] `/juri discuss` produces zero file diffs.
- [ ] `design-state.py --json` emits valid schema in <2s.

### Onda D acceptance
- [ ] All REQ-D1..REQ-D10 verifications pass.
- [ ] Tier 1 dry-run: synthetic regression detected in 1 tick → issue payload emitted.
- [ ] Tier 2 dry-run: synthetic dirty repo → PR draft fixing all drift → flutter analyze passes.
- [ ] Tier 3 dry-run: synthetic sequence with mix of pass/fail/question → all terminal states handled.
- [ ] Halt file mid-loop → exits within 1 tick.
- [ ] Budget exhaustion → graceful halt + report.
- [ ] Audit log entries validate against schema; cost attribution reproducible.
- [ ] 3 GH workflows execute end-to-end on fresh fork in <15min, within free tier.
- [ ] Persona drift over 50 ticks within tolerance.

### v1.0 final acceptance
- [ ] All Onda A/B/C/D acceptance criteria pass.
- [ ] `quick_validate.py` passes for all skills (existing 13 + 5 new orchestration).
- [ ] README §"What changed in v1.0" lists the 4 ondas + new skills + Ralph tiers.
- [ ] `marketplace.json` version → `1.0.0`.
- [ ] Enterprise pitch doc (`docs/enterprise-pitch.md`) ships, with the 8–15 → 3–5 ROI claim, cost model, sample workflows.
- [ ] At least 1 production pilot in an external Flutter project (not Fitio) confirms the workflow end-to-end.

---

## 9. Order of operations

```
Onda 0 — Safety net
└── Tag git: pre-design-spec-driven (rollback point before any code)

Onda A — Discovery foundation
├── Spec → .specs/features/onda-a-discovery/{spec,design,tasks}.md
├── Implement → skills/discovery/ + interview engine + doc generators
├── Verify → REQ-A1..REQ-A6 acceptance
├── Soak → 1 sprint of internal use (Fitio app eats own dogfood)
└── Commit → 3-5 atomic commits, tag onda-a

Onda B — Spec-driven workflow
├── Spec → .specs/features/onda-b-workflow/{spec,design,tasks}.md
├── Implement → skills/{compose,sequence,ship}/ + decisions.md protocol
├── Verify → REQ-B1..REQ-B5 acceptance
├── Soak → 1 sprint
└── Commit → 4-6 atomic commits, tag onda-b

Onda C — Productivity layer
├── Spec → .specs/features/onda-c-productivity/{spec,design,tasks}.md
├── Implement → pause/resume + discuss vs specify + design-state.py
├── Verify → REQ-C1..REQ-C3 acceptance
├── Soak → 1 sprint
└── Commit → 2-3 atomic commits, tag onda-c

Onda D — Ralph autonomy
├── Spec → .specs/features/onda-d-ralph/{spec,design,tasks}.md
├── Implement → skills/ralph-loop/ + 3 tiers + GH workflows + budget + audit log
├── Verify → REQ-D1..REQ-D10 acceptance
├── Soak → 2 sprints (autonomy needs longer soak)
└── Commit → 6-8 atomic commits, tag v1.0.0

Final
├── Enterprise pitch doc
├── Production pilot
└── Release v1.0.0 on GitHub + marketplace
```

**Total estimated effort:** 4-6 sprints (8-12 weeks) for Onda A→D + soak. Compressible to 3 sprints if soak is shortened (not recommended — autonomy without soak = production incident).

---

## 10. Out of scope (deferred to post-v1.0)

- **Stack-agnostic adapter** for non-Flutter (React Native, SwiftUI, native web). Onda E candidate.
- **Multi-tenant SaaS** hosted version. Open-source self-hosted only for v1.0.
- **Visual diff tool** (screenshot regression detection). Useful but separate concern.
- **LLM-as-judge for subjective evals** (the 9 skills missing evals from `skill-creator-alignment` deferred). Belongs to evals tooling, not workflow orchestration.
- **Voice/speech interface** for Júri interview (accessibility). Future onda.
- **Telemetry → BI integration** beyond JSONL export. Customers can ETL the JSONL themselves.

---

## 11. Notes for the fresh session

When you start a new session and the user says "vai full":

1. **Read memory first.** `cat /home/fitiodev/.claude/projects/-media-fitiodev-FITIO-Skill-design-workflow/memory/MEMORY.md` then read each linked file. The 6 files there carry locked decisions — do not contradict.
2. **Read this doc end-to-end.** Don't skim. The plan has dependencies that matter.
3. **Read `.specs/project/STATE.md`.** It records what's already done and what's deferred.
4. **Read `.specs/features/skill-creator-alignment/{spec,design,tasks}.md`.** That's the template format and execution discipline you'll mirror per onda.
5. **Create `.specs/features/onda-a-discovery/{spec,design,tasks}.md`** by extracting REQ-A1..REQ-A6 from this doc, expanding into atomic tasks with verification criteria.
6. **Tag `pre-design-spec-driven` before any code change** (safety net, same pattern as `pre-alignment` from skill-creator-alignment).
7. **Execute Onda A only** in the first session. Do NOT try to do all 4 in one go — soak between ondas is a feature, not a delay.
8. **Update `STATE.md` continuously.** Decisions, blockers, deferred items go there. Future sessions read it.
9. **Update memory** when you discover something the plan didn't anticipate — append a new memory file + update `MEMORY.md` index.

If the user asks "by the way, can we skip Onda A and go straight to Ralph?" — refuse. Cite this doc §5 ("Ralph rodando em chão de areia") and `decision_ralph_separate_skill.md`. Same firmness Júri uses to refuse "moderno e clean".

— Plan v0.1, ready for execution.
