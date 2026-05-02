---
name: compose
description: Compose phase orchestrator — reads approved discovery.md and sequences /theme-create (palette) plus /frontend-design (mockups) under explicit phase gates, then has Clara review the output. Refuses to start when discovery.md status is not approved. Outputs compose.md with palette decisions, 1-3 mockup paths and Clara review notes; status starts at draft and only becomes approved by human edit or `/design-spec approve compose feature`. Triggered by `/design-spec compose`, `/compose`, "rodar fase compose", "compor palette e mockups".
---

# Skill: compose (`/design-spec compose`) — Compose phase

## Triggers

- **English:** `/design-spec compose <feature>`, `/compose`, "run compose phase", "build palette and mockups for <feature>"
- **Português:** `/design-spec compose <feature>`, `/compose`, "rodar fase compose", "compor palette e mockups da <feature>"
- **Natural language:** after Júri Discovery is approved and user wants to materialize the visual side.

## Position in the pipeline

```
Discovery (Júri)  →  Compose (this)  →  Sequence (Arquiteto)  →  Ship (orchestrator)
   approved gate       approved gate        approved gate
```

Compose **refuses to start** unless `.design-spec/features/<feature>/discovery.md` exists and frontmatter `status: approved`.

## Phase gate (REQ-B1.2)

```
1. Read .design-spec/features/<feature>/discovery.md
2. If frontmatter.status != "approved" → halt with message:
   "Discovery is in '{{status}}' state. Approve it first
    (manual edit or /design-spec approve discovery <feature>)."
3. Else proceed.
```

## Workflow

1. **Load decisions.** Read `.design-spec/project/decisions.md` and `discovery.md` Action plan. Note locked decisions (e.g. axis = drenched warm; persona = Maria).
2. **Generate palette.** Spawn `/theme-create` with brief from discovery (axis, anti-refs, persona). Output goes to project's tokens file.
3. **Generate mockups.** Spawn `/frontend-design` for the priority screen(s) from discovery's plan. Aim 1-3 distinct directions, not 1 final.
4. **Clara review.** Self-critique each mockup against discovery's anti-refs + product.md §4 (when greenfield, the freshly-written skeleton; when brownfield, the existing file).
5. **Persist `compose.md`.** Schema below. Status `draft`.
6. **Echo to user.** Show palette summary + mockup links + Clara review excerpts. Ask for approval. **Do not auto-advance to sequence.**

## `compose.md` schema

```markdown
---
feature: <slug>
status: draft  # draft | approved | consumed
phase: compose
created: <iso>
discovery_ref: .design-spec/features/<feature>/discovery.md
---

# Compose — <feature>

## Palette decisions
- Source skill: /theme-create
- Axis: <warm/cool/neutral × drenched/restrained/neutral>
- Tokens added/changed: <list>
- Brand pair contrast: <ratio>:1 (light) / <ratio>:1 (dark)

## Mockups
1. **<title>** — <path or URL>; direction: <one-line>
2. **<title>** — <path>; direction: <one-line>
3. **<title>** — <path>; direction: <one-line>

## Clara review

### Mockup 1
- Anti-ref check: <pass/fail vs discovery anti-refs>
- Voice/tom alignment: <pass/fail vs product.md §4>
- Persona walkthrough: <Maria-style trip-up>

### Mockup 2 / Mockup 3
[...]

## Recommendation

> Clara picks one mockup with reason; user is free to override.

## Decisions logged
<!-- bullets appended to .design-spec/project/decisions.md -->
- D-<id> — <decision>; reason: <persona/axis>; date: <iso>
```

## Decisions tracking (REQ-B4)

Compose **always appends** to `.design-spec/project/decisions.md` whenever palette axis or token semantic intent is locked. Schema:

```yaml
- id: D-<seq>
  decision: <one-line>
  reason: <one-line tying back to discovery answer or audit signal>
  date: <iso>
  supersedes: <D-id|null>
  phase: compose
  feature: <slug>
```

Refining skills (Brasa/Calma/Lâmina/Jack) are responsible for reading `decisions.md` before proposing changes that contradict it (REQ-B4.2). Compose is the **first writer** in the lifecycle.

## Approval

`compose.md` nasce `status: draft`. Para virar `approved`:

- Manual edit do frontmatter; ou
- `/design-spec approve compose <feature>` (orquestrador atualiza status + valida schema).

`/design-spec sequence <feature>` recusa iniciar se status ≠ approved.

## Anti-patterns

- ❌ Auto-runs sequence ou ship após gerar compose.md.
- ❌ Sobrescreve compose.md existente sem pergunta.
- ❌ Pula Clara review para "ganhar tempo" — review é o sinal.
- ❌ Persiste palette sem rodar `/theme-create` (se já existe palette aprovada, registrar isso explicitamente em compose.md como "reused").
- ❌ Omitir entrada em `decisions.md` quando uma decisão de axis/token é tomada.

## Reference

For full decisions schema + supersedes semantics: `references/decisions-schema.md`.
For Clara review checklist: `references/clara-review.md`.
