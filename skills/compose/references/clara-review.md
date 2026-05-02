# Clara review checklist (compose phase)

> Quick rubric Clara applies to each mockup produced in Compose. Output goes into `compose.md` per-mockup section.

## 4-axis quick check

For each mockup:

1. **Anti-ref check.** List discovery `anti-references`. For each, mark Pass/Fail with 1 specific reason. Failure of any anti-ref → mockup is rejected (not just flagged).
2. **Voice/tom alignment.** Compare mockup copy + visual hierarchy against `product.md §4` (banidos absolutos, vocativo, scene sensations from P2). Cite ≥1 evidence.
3. **Persona walkthrough.** Walk persona primária (from discovery P1.2) through the primary task (P1.3). Identify the moment of friction or peak-end emotion. Be concrete (file:line if web mock; element name if Figma/HTML).
4. **Axis fidelity.** Does the mockup's color commitment match `decisions.md` D-id locked axis (drenched/restrained × warm/cool/neutral)? If not, suggest concrete delta.

## Output format (per mockup, in compose.md)

```markdown
### Mockup N — <title>
- Anti-ref check: <Pass/Fail> — <if fail, which anti-ref + why>
- Voice/tom: <Pass/Fail> — <evidence>
- Persona walkthrough (<persona>): <one paragraph; concrete trip-up or peak>
- Axis fidelity: <Pass/Fail> — <delta if fail>
- Verdict: <ship | revise | reject>
```

## Verdict rules

- **ship**: 4/4 axes pass.
- **revise**: 3/4 pass with deltas listed; one round of refinement recommended.
- **reject**: ≤2 axes pass OR any anti-ref Fail. Mockup discarded — do not bring forward to Sequence.

## Ranking among mockups

After reviewing 1–3 mockups, Clara picks one with a 1-line reason. User can override; the pick is recommendation, not decision.

## Anti-patterns

- ❌ "Looks good" verdicts. Every axis needs concrete evidence.
- ❌ Skipping persona walkthrough because mockup is generic — that's the sign you need it most.
- ❌ Auto-passing axis fidelity without checking `decisions.md`.
