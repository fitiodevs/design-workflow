# Feature: wireframe-sketch (DEFERRED to v1.5+)

> Lo-fi exploration skill: hand-drawn wireframes (graph paper / marker tone / annotations) for layout exploration before committing to Clara's hi-fi mockups. Forks `nexu-io/open-design`'s wireframe-sketch with attribution + adds Esboço/Sketcher persona + ties to `craft/state-coverage.md` for tab variants.

**Status:** Deferred (split out from `multi-stack-adapter` 2026-05-06)
**Original target:** v1.4.0 (bundled with adapter)
**New target:** v1.5+ (no firm date — pull forward when there's a real consumer need)
**Reason for split:** wireframe-sketch is orthogonal to stack support. User urgency on Next.js/Tailwind warranted pulling adapter forward to v1.2.0; carrying wireframe-sketch along would have bloated v1.2 unnecessarily.

---

## Summary

Adds a new skill `wireframe-sketch/` that emits a single `.html` file with N tabs (default 4) showing lo-fi layout variants. Use case: before committing to Clara's hi-fi (`/frontend-design`), the designer wants to sketch 4-tab variants in 30 seconds — what's the layout? where's the main affordance? Lo-fi forces decisions about hierarchy that hi-fi can hide behind polish.

**Pairs naturally with:**
- `craft/state-coverage.md` — each tab can preview a different state (empty / populated / error).
- `/frontend-design` (Clara) downstream — pick the chosen sketch tab manually, then prompt Clara for hi-fi.

## What was already designed (carried over from old `adapter-and-wireframe/spec.md` REQ-E)

- **REQ-E.1** Fork `skills/wireframe-sketch/SKILL.md` from open-design with full attribution header.
- **REQ-E.2** Update body to reference our craft (`craft/state-coverage.md`) and our pipeline (after sketch, route to `/frontend-design` for hi-fi).
- **REQ-E.3** Persona: Esboço (PT) / Sketcher (EN). New persona row in `docs/personas.md`.
- **REQ-E.4** Triggers: `/wireframe-sketch`, `/Esboço`, `/Sketcher`, "lo-fi mockup", "wireframe", "esboço", "rascunho da tela".
- Output path: `.design-spec/wireframes/<feature>/<timestamp>.html`.
- Anti-pattern: wireframe is NOT a substitute for Clara — wireframe is for layout exploration; Clara is for typography/microcopy/refinement.

## What needs to be re-decided when revived

- Does it integrate with the adapter system? Probably not — wireframe is HTML-output regardless of target stack (you sketch, you don't port directly to Flutter/JSX). But verify when scoping.
- Open-design's source SHA at fork time (capture during T-00).
- Multi-tab convention: how many default? open-design ships 4; ours might be different.

## How to revive

1. Confirm a real user need (someone asks for it, or `/frontend-design` users complain about jumping straight to hi-fi).
2. Re-promote this stub: `cp spec.md → spec.md` and design.md/tasks.md from the old `adapter-and-wireframe/` v1.4 plan (preserved in git history at commit `<TBD>`).
3. Pick a target version (probably one slot after whatever's currently next).
4. Fork upstream + ship.

## Pointer to original plan (preserved)

The full requirements + tasks for wireframe-sketch lived in `.specs/features/adapter-and-wireframe/{spec,design,tasks}.md` before the split. To recover them, check git history before commit that retargets adapter to v1.2.0 (search `git log --all --diff-filter=D --name-only -- '.specs/features/adapter-and-wireframe/*'`).
