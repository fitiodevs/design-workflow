# Installation

## Option A — install.sh (manual)

```bash
git clone https://github.com/fitiodevs/design-workflow.git ~/code/design-workflow
cd ~/code/design-workflow
./install.sh
```

`install.sh` copies each `skills/<name>/` directory into `~/.claude/skills/<name>/`, preserving the `LICENSE.txt` next to each `SKILL.md`.

To uninstall:

```bash
./uninstall.sh
```

## Option B — Claude Code plugin marketplace

```
/plugin marketplace add fitiodevs/design-workflow
/plugin install design-workflow@design-workflow-marketplace
```

After install, invoke any skill by name in Claude Code:

```
/theme-audit
/Lupa
/theme-critique
/Júri
```

## Project setup

Drop `config.example.yaml` at your project root as `.design-workflow.yaml` and adjust paths. See [customizing.md](customizing.md).

## Verifying

In Claude Code, run:

```
/theme-audit
```

You should see Auditor (Lupa) sweep `lib/` for hardcoded tokens and report violations. If you get "skill not found", verify `~/.claude/skills/theme-audit/` exists and `SKILL.md` has a valid frontmatter.

## Updating

```bash
cd ~/code/design-workflow
git pull
./install.sh        # re-runs the copy with latest changes
```

## Removing a single skill

```bash
rm -rf ~/.claude/skills/<skill-name>
```

The skill folders are independent — removing one doesn't break others, but skills that delegate to a removed sibling will fall back to inline behaviour.
