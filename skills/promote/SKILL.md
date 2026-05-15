---
name: promote
description: Promotes a free-form markdown file under `docs/backlog/` into a structured spec triplet under `.specs/features/` (spec, design, tasks), then suggests `/tlc-spec-driven` to refine the structure and `/tlc-closure` to verify dependency closure. Reads optional YAML frontmatter (repo, priority, status) and refuses to promote unless the status field is set to ready. Decomposes the body into requirements, design decisions, and atomic 30-minute tasks. Triggered by `/promote`, `/promote-backlog`, "promove o backlog pra spec", "turn this backlog into a spec". Skip when the user wants a spec from scratch (delegate `/tlc-spec-driven`) or to edit an existing spec (use Edit directly).
---

# Skill: promote (`/promote`) — persona **Atlas Promote** (English: **Cartographer Promote**)

Atlas Promote converts a loose backlog markdown into the canonical 3-file spec triplet that the rest of the design-spec-driven pipeline (`/design-spec sequence`, `/design-spec ship`) expects. **Not deterministic** — needs LLM judgment to decompose narrative prose into actionable `T-XX` rows.

After promotion, Atlas Promote **always recommends** `/tlc-spec-driven specify <name>` to fill gaps in the generated `spec.md` and `design.md`, and `/tlc-closure` to walk the task dependency graph and surface loose ends before execution.

## Triggers

- **English:** `/promote <name>`, `/promote-backlog <name>`, "turn this backlog into a spec", "promote the X backlog"
- **Português:** `/promote <name>`, `/promote-backlog <name>`, "promove o backlog X pra spec", "vira spec essa ideia"
- **Natural language:** an idea has matured in `docs/backlog/` and needs a structured plan; the user wants to enter the design-spec-driven flow.

## Inputs accepted

- `<name>` (no `.md` extension) → looks up `docs/backlog/<name>.md`
- Full path to any `.md` under `docs/backlog/`

## Frontmatter expected

The backlog file should ideally carry YAML frontmatter:

```markdown
---
title: Coupon Wishlist Multi Mission
status: ready          # 'idea' | 'discussing' | 'ready'
priority: P0           # P0 | P1 | P2 | P3
repo: <optional>       # only if you split work across multiple repos in a monorepo;
                       # tasks can override this individually
---
```

Rules:

- **`status: ready` is required.** If missing or set to `idea`/`discussing`, stop and ask the user to update it first.
- **`priority` is optional** — defaults to P2 if absent.
- **`repo` is optional** — only meaningful when the project spans multiple repos. If absent, no Repo column in `tasks.md`.

## Procedure

1. **Read** the entire `docs/backlog/<name>.md`.
2. **Validate frontmatter** (`status: ready` required).
3. **Decompose the body** into the canonical 3-file structure:
   - **`spec.md`** ← context + requirements (`REQ-XX`) + acceptance criteria. Source: "Why" / "Problem" / "Goal" sections.
   - **`design.md`** ← technical decisions (`D1`, `D2`, …). Source: "How" / "Approach" / "Solution" sections.
   - **`tasks.md`** ← table with columns `ID | Title | Prio | Type | Depends | Status` (plus `Repo` if frontmatter declares one). Each `- [ ]` checkbox in the backlog becomes a `T-XX` candidate. Each task inherits frontmatter `repo` if present; override per task when the work obviously belongs in a different repo.
4. **Create** `.specs/features/<name>/` (mkdir -p).
5. **Write** the three files.
6. **Archive the backlog:** `mv docs/backlog/<name>.md docs/backlog/_promoted/<name>.md`. Prepend a line: `> Promoted to .specs/features/<name>/ on YYYY-MM-DD`.
7. **Show diff** to the user — table of generated `T-XX` rows. Ask for review before any commit.
8. **Never auto-commit.** User reviews, edits if needed, commits when satisfied. Suggested message: `feat(specs): promote <name> from backlog — N tasks`.
9. **Recommend the lifecycle next steps:**
   - `/tlc-spec-driven specify <name>` — fills gaps in spec/design via 4-phase adaptive interview.
   - `/tlc-closure <name>` — walks the task graph, lists touchpoints (callers, providers, tests, routes), generates closure subtasks, runs auto-RalphLoop until zero loose ends.

## Decomposition heuristics

| Signal in backlog | Becomes |
|---|---|
| `## Requirements` or `## Acceptance` | direct content for `spec.md` |
| `## Design` or `## How` | direct content for `design.md` |
| `## Tasks` or `## TODO` with `- [ ]` | one `T-XX` per checkbox |
| Bare list without checkboxes | decompose into `T-XX` rows by inferring sensible grouping |
| Pure narrative prose | emit a single vague `T-01: Implement <feature>` row + flag the spec as "needs human refinement before execution" |

**Rule of thumb:** one task = one atomic commit. If the description fits in a commit subject, it's a task. If not, break into sub-tasks.

## Monorepo split

If the backlog clearly touches multiple repos, **split into per-repo tasks** — e.g. `T-01 (supabase): apply migration`, `T-02 (app): wire repository`, `T-03 (studio): add analytics card`. Don't multi-tag.

This only applies when the project's `repo` frontmatter declares multiple repos. Single-repo projects skip this entirely.

## Output template (on success)

```
✅ Promoted: <name>

Created:
  .specs/features/<name>/spec.md       (<N> requirements)
  .specs/features/<name>/design.md     (<M> design decisions)
  .specs/features/<name>/tasks.md      (<K> tasks)

Archived:
  docs/backlog/_promoted/<name>.md     (was docs/backlog/<name>.md)

Recommended next steps:
  1. /tlc-spec-driven specify <name>   — fill gaps in spec.md + design.md
  2. /tlc-closure <name>               — walk the task graph, find loose ends
  3. Review + commit: `feat(specs): promote <name> from backlog — <K> tasks`
```

If `tlc-spec-driven` and `tlc-closure` skills are not installed, the recommended message degrades to `Review the generated files manually before sequencing — or install /tlc-closure (which auto-bootstraps /tlc-spec-driven and /graphify) for verified dependency closure.`

## Don't

- **Don't** promote without `status: ready` in the frontmatter.
- **Don't** auto-commit. User reviews first.
- **Don't** invent requirements that aren't in the backlog. If the doc is thin, generate a thin spec with a `needs refinement` flag.
- **Don't** delete the original backlog — move to `_promoted/` to preserve the trail.
- **Don't** force a `Repo` column when the project is single-repo.

## Invocation examples

```
/promote coupon-wishlist-multi-mission
/promote-backlog adtech-gym-boost
"promove o backlog adtech pra spec"
"turn cupom-wishlist into a real spec"
```
