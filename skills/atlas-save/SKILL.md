---
name: atlas-save
description: Saves the current session as a curated written handoff for the next session. Combines deterministic capture (git state of every linked repo plus Atlas snapshot plus WIP/blocked tasks plus recent commits) with LLM-curated content (decisions, bugs and lessons, open questions, sentiment, resume playbook). Default output lands in `memory/sessions/` as a dated markdown file (internal memory only); Obsidian vault sync is opt-in via the `OBSIDIAN_VAULT` env var or a `.atlas-save.yaml` config file. Updates `memory/active_work.md` with a pointer. Triggered by `/save-session`, `/atlas-save`, "Atlas, save the session", "salva a sessão", "fecha o handoff", "guarda contexto pra próxima", or naturally at the end of a complex working session.
---

# Skill: atlas-save (`/save-session`) — persona **Atlas Cronista** (English: **Cartographer Chronicler**)

Atlas Cronista does not replace the conversation transcript — it writes a **curated handoff** the next session can read in 30 seconds and resume exactly where you stopped. Goes way beyond keyword retrieval (à la context-mode): decisions, lessons, and the playbook are *curated*, not searched.

## Triggers

- **English:** `/save-session`, `/atlas-save`, "Atlas, save the session", "save the handoff", "park context for next time"
- **Português:** `/save-session`, `/atlas-save`, "Atlas, salva a sessão", "fecha o handoff", "guarda contexto pra próxima", "salva onde paramos"
- **Natural language:** end of a 2+ hour working session with multiple decisions; before context window pressure; user signals "good place to stop".

## Where the file lands

| Mode | Where | Trigger |
|---|---|---|
| **Default — internal memory only** | `<repo>/memory/sessions/YYYY-MM-DD-HHMM-<slug>.md` | always |
| **Opt-in — Obsidian vault mirror** | `<vault>/<folder>/<filename>.md` (Obsidian-native frontmatter) | `OBSIDIAN_VAULT` env var set, OR `.atlas-save.yaml` declares `obsidian.vault_path` |

Default mode is opt-out friendly: zero filesystem footprint outside the repo. Vault mirror is for users that already maintain a knowledge garden — declare it once and every save also lands there.

## Procedure

### Step 1 — Deterministic capture (skip-if-trivial)

> **Default: skip.** Git state, commits, atlas snapshot, and open tasks are all recoverable in ~4 bash calls (`git status`, `git log`, `/status`, `ls .specs/`) at the start of the next session for ~500 tokens. Writing them into the handoff costs ~6-8k tokens of dense markdown **now** to register data that will be in `git`/`ls` in 1 hour. **Never worth it.**
>
> **Include only if non-derivable** — e.g. the user wants a frozen snapshot before a destructive operation, or the session crossed a state that no longer exists in git (uncommitted work that was discarded). In those cases, write only the specific datum that won't survive.

If you do capture, read directly with `Bash`/`Read`. The four sections an LLM can fill from grep + git alone — and which the next session can rebuild for free:

- §1 Repo state — branch, last commit, uncommitted count per repo.
- §2 Commits in this session — `git log --oneline --since=<marker>`.
- §3 Atlas snapshot — `/status`-style WIP/blocked across specs.
- §4 Open tasks — `T-XX` rows in `in_progress` / `blocked`.

The handoff's **value** is in Step 2 below.

### Step 2 — Curated enrichment (LLM judgment)

Replace each placeholder with real content drawn from the conversation context:

#### §5 — Decisions made

Format: `**[chosen]** vs [rejected alternative] — [why]`. Example:

```markdown
- **Symlink-based cross-repo sync** vs context-mode install — local-dev only, single source of truth, no hook collision with persona-sync.
- **Split tasks per repo** vs multi-tag — forces healthy decomposition, simpler hook.
- **Manual /promote interactive** vs auto-promote on `status: ready` — anti-AI-slop, user reviews before commit.
```

#### §6 — Bugs + lessons

Each bug: **symptom → root cause → fix (commit) → lesson**. The lesson is the part the next session needs to avoid repeating.

```markdown
1. **Hook read git log of canon, not the invoking repo** (mark_task.py)
   - Symptom: T-01 of supabase stayed pending despite the right commit
   - Root cause: `Path(__file__).resolve()` follows symlink → REPO always points at canon → `subprocess.git -C REPO` reads the wrong git log
   - Fix: `cwd=Path.cwd()` (commit `52de871d`)
   - Lesson: scripts reached via symlink **must NEVER** use `__file__` to detect context. Use CWD.
```

#### §7 — Open questions

Hanging points that need a decision or investigation next session. Each one with enough context to resume.

#### §8 — Sentiment + momentum

One line. Honest. Critical for the next session to calibrate tone.

```markdown
> User in flow — closed cupom-acquisition + cupom-wishlist 100%, validated cross-repo Atlas end-to-end, next is emulator smoke. Keep momentum, avoid big redesigns.
```

#### §9 — Resume playbook

3–5 concrete copy-paste steps. No passive voice ("should be done") — imperative verbs. Include shell commands when applicable.

```markdown
1. `cd <repo> && /status` → confirm post-session state
2. Boot emulator: `emulator -avd Pixel_8_API35 -gpu auto -no-snapshot &`
3. Wait for adb device, run `flutter run -d emulator-5554`
4. Smoke nova-ui T-20: validate PointsHero, MilestoneTrack, GpsStrip, FeedCta, PartnerPickerSheet
5. If OK → mark T-20 done. If bug → debug and add to §6 of next session.
```

### Step 3 — Write to disk

```
<repo>/memory/sessions/<YYYY-MM-DD-HHMM-slug>.md
```

If `OBSIDIAN_VAULT` is set or `.atlas-save.yaml` declares `obsidian.vault_path`, also `cp` the file to that location. Add Obsidian-native frontmatter (`tags: [atlas, session-handoff, <project>]`, `created: <iso>`).

### Step 4 — Update `memory/active_work.md`

Append a **pointer + 2–3 line summary** at the top. **Don't** duplicate the body — it lives in the session file; `active_work.md` is the index.

```markdown
# Session 2026-05-05 (Atlas + nova-ui smoke)

**Full handoff:** [sessions/2026-05-05-1145-mapbox-diego.md](sessions/2026-05-05-1145-mapbox-diego.md)

**TL;DR:** cupom-acquisition 100% + cupom-wishlist 100% + Atlas Cronista skill created. Next: emulator smoke T-20 nova-ui.

---

# Session 2026-05-04 — closed and pushed

[...prior history...]
```

If `active_work.md` exceeds ~200 lines, suggest rotation: archive old history into `memory/active_work_archive_YYYY-MM.md`.

### Step 5 — Confirm

Print to user:

```
✅ Session saved: memory/sessions/2026-05-05-1145-mapbox-diego.md
   ↳ Mirrored to: <obsidian-vault>/Atlas/2026-05-05-1145-mapbox-diego.md   (only if vault configured)

Captured:
  • 3 decisions, 2 bugs+lessons, 4 open questions, 5-step playbook
```

**Target size: ~80 lines.** If you wrote more than ~120 lines, you are duplicating data that lives in git/disk. Cut Step 1 sections.

## Optional config — `.atlas-save.yaml`

Drop a YAML file at the repo root to declare cross-repo capture or Obsidian export:

```yaml
repos:
  - path: .                      # current repo (always implicit)
  - path: ../api                 # extra repos to capture in §1
  - path: ../infra
obsidian:
  vault_path: /Users/me/Vault    # absent = no Obsidian mirror
  folder: Atlas/sessions         # within the vault
```

Without this file, atlas-save captures only the current repo and writes only to `memory/sessions/`.

## Anti-patterns

- **Don't** dump the transcript — the handoff is curated, not a copy.
- **Don't** duplicate git/disk** — `git status`, `git log`, `ls .specs/` recover for free next session. Writing them to markdown costs 6-8k tokens **now** for zero new information. Skip Step 1 unless the data won't survive in git.
- **Don't** be vague — "discussion about features" is useless. Concrete: spec names, `T-XX` ids, commit shas.
- **Don't** invent a decision that wasn't taken — if there was none, write `_no architectural decision this session_`.
- **Don't** default-positive the sentiment line — if the user voiced frustration, record it. The next session needs to know.
- **Don't** forget the `active_work.md` pointer — without the index entry, the session file becomes an orphan.
- **Don't** auto-commit — `memory/` is local by design. The user decides what to push.

## Philosophy (vs context-mode)

context-mode solves "I have 50 KB of tool output, index it for retrieval later". Atlas Cronista solves "I have 2 hours of decisions, bugs, and momentum — distill them into one page that rebuilds context in 30 seconds". Different problems — Atlas wins at **session-level handoff**, context-mode wins at **event-level retrieval**. For long-running specs, cross-repo work, and judgment-heavy decisions, session handoff is what matters.
