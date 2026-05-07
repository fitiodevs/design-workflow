# Publishing `design-workflow` to the Claude Code marketplace

Maintainer-only playbook. Walks through cutting a release, validating the
plugin bundle, getting it on GitHub, and confirming `/plugin marketplace add`
resolves it cleanly. Keep it boring — surprises here cost users.

The repo already ships as a Claude Code plugin marketplace via
`.claude-plugin/marketplace.json`. Publishing = bumping the version, tagging,
releasing on GitHub, and verifying the install path end-to-end. There is no
separate registry submission today.

---

## TL;DR — happy path

```bash
# 1. land all changes on main
git switch main && git pull

# 2. bump version in marketplace.json (e.g. 1.5.0 → 1.6.0)
$EDITOR .claude-plugin/marketplace.json

# 3. pre-tag (anchor before destructive history rewrites, optional)
git tag pre-v1.6.0 && git push origin pre-v1.6.0

# 4. tag + push
git commit -am "feat(release): v1.6.0 — <one-line summary>"
git tag v1.6.0
git push origin main v1.6.0

# 5. cut GitHub release with notes
gh release create v1.6.0 --title "v1.6.0 — <summary>" --notes-file /tmp/release.md

# 6. smoke test the install path from a clean checkout (see §6)
```

---

## 1. Pre-release checklist

Run all of this on `main` (or the merge candidate) before tagging.

### 1.1 Marketplace metadata is current

- `.claude-plugin/marketplace.json` → `metadata.version` matches the planned tag (no `v` prefix in JSON; tag has `v`).
- `metadata.description` reflects what shipped this cycle (delta-aware: don't leave stale "v1.4 features" in a v1.6 description).
- Every directory under `skills/` is listed in `plugins[0].skills`. Mismatches mean a skill ships in the repo but is invisible to `/plugin install`.

Quick diff:

```bash
diff <(ls skills/ | sort) \
     <(jq -r '.plugins[0].skills[] | sub("^./skills/"; "")' .claude-plugin/marketplace.json | sort)
```

The diff must be empty.

### 1.2 Each skill has a valid `SKILL.md`

For every `skills/<name>/SKILL.md`:

- Frontmatter has `name`, `description`, `license` keys.
- `name` matches the directory name (kebab-case).
- `description` includes both EN and PT trigger words (project rule from `CONTRIBUTING.md`).
- `LICENSE.txt` sits next to `SKILL.md` (Apache-2.0).

Spot check:

```bash
for d in skills/*/; do
  test -f "$d/SKILL.md"     || echo "MISSING SKILL.md: $d"
  test -f "$d/LICENSE.txt"  || echo "MISSING LICENSE.txt: $d"
done
```

### 1.3 `install.sh` works from a clean checkout

The installer is the de-facto packaging contract — if it breaks, the marketplace install also breaks (both copy `skills/*/` into `~/.claude/skills/`).

```bash
# in a throwaway clone:
git clone https://github.com/fitiodevs/design-workflow.git /tmp/dw-test
cd /tmp/dw-test
HOME=/tmp/dw-fakehome ./install.sh
ls /tmp/dw-fakehome/.claude/skills | wc -l   # must equal `ls skills | wc -l`
ls /tmp/dw-fakehome/.claude/craft  | wc -l   # > 0
```

The installer also rewrites `craft/*.md` references to `~/.claude/craft/*.md`
in 5 wired skills (`theme-critique`, `theme-create`, `theme-port`,
`theme-bolder`, `frontend-design`). After install, grep one of those
SKILL.md copies and confirm no `\`craft/` substring remains.

### 1.4 Scripts resolve

`scripts/` is sourced per-skill via `scripts/_sync.sh`. New scripts must:

- be invoked as `python3 scripts/<file>.py` from `SKILL.md` (no project-relative imports);
- not require dependencies outside the Python stdlib unless documented in `docs/installation.md`.

### 1.5 Adapter conformance still passes

Skills that ship adapter contracts (Flutter, Next.js, React Native) have
conformance probes. Re-run them on the candidate version against the
reference fixtures:

```bash
# whatever the current adapter test entry point is — check ROADMAP.md for the
# active suite. Today: Flutter + Next.js + RN must report 3/3.
```

If a probe fails, do **not** ship — file a hotfix issue and fix forward.

### 1.6 Docs are not lying

Skim:

- `README.md` — install snippet uses the real handle (`fitiodevs/design-workflow`), not `<your-handle>`.
- `docs/installation.md` — same.
- `docs/ROADMAP.md` — items shipped this cycle moved out of "next" into "done".

---

## 2. Version policy

Semver, applied to the *user-facing surface* of the plugin (skills, slash
commands, adapter protocol):

| Bump | Triggers |
|---|---|
| **major** (`2.0.0`) | Removed/renamed skill, breaking change to slash command name, breaking change to adapter protocol JSON shape. |
| **minor** (`1.6.0`) | New skill, new slash command, new adapter, additive change to a SKILL.md frontmatter. |
| **patch** (`1.5.1`) | Bug fix, doc fix, prompt-only tweak with no behavioral surprise. |

Tag `marketplace.json` `metadata.version` and the git tag in lockstep.
**Never** publish two different versions under the same tag — users cache.

### 2.1 Pre-tags

The repo uses `pre-vX.Y.Z` tags as anchors before risky merges (see
`git tag --sort=-creatordate`). Push the pre-tag *before* the merge that
becomes the release commit, so a rollback target exists.

---

## 3. Cutting the release commit

```bash
git switch main
git pull --ff-only

# Update version in the canonical place — marketplace.json is the source of truth.
# install.sh, README, and SKILL.md files do NOT carry a version number.
$EDITOR .claude-plugin/marketplace.json

# (optional) pre-tag the tip before any history-changing operation
git tag pre-v1.6.0
git push origin pre-v1.6.0

git add .claude-plugin/marketplace.json
git commit -m "feat(release): v1.6.0 — <one-line summary>"
git tag -a v1.6.0 -m "v1.6.0 — <one-line summary>"
git push origin main v1.6.0
```

The release commit message convention in this repo is
`feat(release): vX.Y.Z — <summary>` (see `git log` for prior shape). Stick
with it; the changelog generator and `/status` skill both read this prefix.

---

## 4. GitHub release

The marketplace install path (`/plugin marketplace add fitiodevs/design-workflow`)
resolves the latest tag. A GitHub Release on top of that tag isn't required
for the plugin to work, but it **is** the changelog users actually read.

```bash
cat > /tmp/release.md <<'EOF'
## Highlights
- <one bullet per shipped feature, user-facing language>
- <skip internal refactors unless they affect install/run>

## New skills
- `<name>` — <one line>

## Breaking changes
- <only if major>

## Upgrade
```bash
/plugin marketplace update design-workflow-marketplace
```
EOF

gh release create v1.6.0 \
  --title "v1.6.0 — <summary>" \
  --notes-file /tmp/release.md \
  --latest
```

Always pass `--latest` when you intend this release to be the new default —
`/plugin marketplace add` resolves "Latest" by default.

---

## 5. Verifying marketplace resolution

This is the only test that catches "shipped but uninstallable." Run it on
a *different machine or container* than the one you developed on, so cached
clones don't mask a broken `marketplace.json`.

```text
# inside Claude Code, in any project directory:
/plugin marketplace add fitiodevs/design-workflow
/plugin install design-workflow@design-workflow-marketplace

# then, in any Flutter project:
/theme-audit
/Lupa
/compose
```

Verify:

- All 20 skills show up in `/plugin list` (or whatever Claude Code surfaces).
- `/theme-audit` and at least one persona alias (`/Lupa`) trigger the same skill.
- `craft/` references resolve — `/theme-critique` should not error on missing `~/.claude/craft/anti-ai-slop.md`.

If something fails here, **do not delete and re-tag the same version**.
Cut a `vX.Y.(Z+1)` patch with the fix; users who already cached the bad
version will pull the patch on their next `marketplace update`.

---

## 6. Smoke-test matrix (recommended)

Before announcing, exercise the full pipeline against a real Flutter app
(or the reference fixture in `template/`):

| Step | Skill | Pass criterion |
|---|---|---|
| 1 | `/theme-audit` | Reports baseline; no crash on empty `lib/`. |
| 2 | `/theme-create` | Emits `AppColors` + WCAG sheet under `docs/themes/`. |
| 3 | `/frontend-design` | Generates `.html` mockup with no AI-slop violations. |
| 4 | `/theme-port --from-html <path>` | Produces Flutter widgets using existing tokens. |
| 5 | `/theme-critique` | Returns Nielsen 10 + 5dim radar + P0–P3 list. |
| 6 | `/compose`, `/sequence`, `/ship` | Refuse to run when prior phase is not `approved` (gate enforcement). |
| 7 | `/ralph watch` | Read-only audit + critique, halts cleanly on `halt-file`. |

Steps 6 and 7 are the most regression-prone — phase gate logic and Ralph's
budget cap have broken twice historically (see `memory/sessions/`).

---

## 7. Announcement

Optional but expected. Channels in priority order:

1. **GitHub release notes** — already done in §4. This is canonical.
2. **README badge** — bump the "latest" badge if any (currently none; skip).
3. **Internal handoff** — invoke `/save-session` so the next session knows
   what shipped without re-deriving from `git log`.

No social/external announcement is required for the marketplace itself —
the marketplace surface is "discovery via repo URL," not a curated index.

---

## 8. Hotfix path

For a regression discovered after a release:

1. **Don't move the tag.** Cut `vX.Y.(Z+1)` immediately, even for a one-line fix.
2. Revert or fix on `main`, repeat §3–§5 with the patch version.
3. Mark the broken release as "deprecated" in its GitHub release notes
   (`gh release edit vX.Y.Z --notes-file /tmp/deprecated.md`); don't delete it
   — users may have it pinned.
4. If the bug corrupts user data or installs (rare — installer is idempotent),
   add a one-line warning at the top of `README.md` linking to the patch tag.

---

## 9. Checklist (copy-paste)

```
[ ] marketplace.json version bumped
[ ] skills/ ↔ marketplace.json plugins[0].skills diff is empty
[ ] every SKILL.md has name+description+license + LICENSE.txt sibling
[ ] install.sh works from clean clone with fake $HOME
[ ] adapter conformance probes pass (Flutter / Next.js / RN — 3/3)
[ ] README + docs/installation.md use real github handle (no <your-handle>)
[ ] release commit: feat(release): vX.Y.Z — <summary>
[ ] tag vX.Y.Z pushed; pre-vX.Y.Z anchor exists if merge was risky
[ ] gh release create --latest with user-facing notes
[ ] /plugin marketplace add verified on a clean Claude Code session
[ ] /save-session captures what shipped
```

If every line is checked, ship it.
