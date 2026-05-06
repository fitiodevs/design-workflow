# Ralph — persona injection per iteration

## Why

Long autonomous sessions drift. After 50+ ticks, the model's voice trends toward the average of its accumulated context, drifting away from each specific persona's `voice_dna`. Quality degrades silently.

## Mechanism

Every Ralph tick that spawns a persona-bearing skill (Júri / Compositor / Brasa / Calma / Lâmina / Jack / Clara / Pena / Cirurgião / Arquiteto):

1. Read the skill's SKILL.md.
2. Extract the `voice_dna:` block (always_use / never_use / sentence_starters / signature_close).
3. Inject the block as a system reminder before the prompt.
4. Do NOT rely on accumulated context to preserve persona.

This is cheap (~50-200 tokens per tick) and keeps the persona fresh.

## Drift detection

Every 10 ticks (configurable):

1. Sample last N tokens of each persona's outputs in this loop.
2. Count occurrences of `voice_dna.always_use` terms vs `voice_dna.never_use` terms.
3. Compute simple ratio.
4. Flag in audit log if ratio falls below threshold (e.g. `always_use_freq < 50% of baseline`).

Flagging is a warning, not a halt — drift may be appropriate for the moment. Persistent drift across 30+ ticks is the signal to halt manually and review.

## Re-loading is per skill, not per persona

Some skills share personas (e.g. `theme-critique` uses Júri in both modes). Ralph re-loads from the SKILL.md being spawned, not from a separate persona registry. This avoids drift between SKILL.md and a stale registry copy.

## Anti-patterns

- ❌ Trusting accumulated context to preserve persona over 50+ ticks. It will not.
- ❌ Re-loading at startup only. Drift accumulates within a loop run.
- ❌ Storing personas in a separate file. Single source of truth = the SKILL.md.
- ❌ Checking drift more often than every ~10 ticks (cost) or less often than every ~50 (signal).
