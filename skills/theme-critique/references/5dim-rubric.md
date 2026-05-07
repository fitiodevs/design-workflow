> **Sourced from:** https://github.com/nexu-io/open-design/blob/9c64ef1b2bb2cffafb0ad6167d6a3831bdc0ba11/skills/critique/SKILL.md (§§"The 5 dimensions" + "Scoring discipline")
> **Upstream attribution:** [huashu-design](https://github.com/alchaincyf/huashu-design) (Apache-2.0) by @alchaincyf
> **License:** Apache-2.0 (open-design fork) | Apache-2.0 (huashu-design)
> **Local path:** `skills/theme-critique/references/5dim-rubric.md`
> **Last sync:** 2026-05-07 at 9c64ef1b2bb2cffafb0ad6167d6a3831bdc0ba11

---

# 5-dimension critique rubric

> Loaded by `skills/theme-critique/SKILL.md` when `--mode 5dim` is invoked. Otherwise inert. Forked verbatim from upstream — local edits limited to this header.

## The 5 dimensions

> Each dimension is independent — a deck can be 9/10 on Innovation but
> 4/10 on Hierarchy and the report should say so plainly. Don't average
> away interesting failures.

### 1. Philosophy consistency · 哲学一致性

> Does the artifact pick a clear *direction* and stick to it through
> every micro-decision (chrome / kicker / spacing / accent)?

**Evidence to look for:**
- Is there one declared design direction (e.g. Monocle / WIRED /
  Kinfolk) or is it three styles in a trench coat?
- Does the chrome / kicker vocabulary stay in one register, or does
  page 3 say "Vol.04 · Spring" and page 7 say "BUT WAIT 🔥"?
- Are accent / serif / mono used by the same rule throughout?

**0–4** Three styles fighting each other. **5–6** One direction but
half the elements drift. **7–8** Coherent, occasional drift on edge
pages. **9–10** Every element argues for the same thesis.

### 2. Visual hierarchy · 视觉层级

> Can a stranger figure out what to read first, second, third — without
> being told?

**Evidence to look for:**
- Is the largest type clearly the most important thing on each page?
- Do mono / serif / sans roles match the information's *role* (meta /
  body / display)?
- Lots of "loud" elements competing? Or a clear primary + secondary +
  tertiary tier?

**0–4** Everything shouts. **5–6** Hierarchy works on hero pages but
breaks on body. **7–8** Clear tiers, occasional collision. **9–10** Eye
moves with zero friction.

### 3. Detail execution · 细节执行

> The 90/10 stuff — alignment, leading, kerning at large sizes, image
> framing, foot/chrome polish, edge-case spacing.

**Evidence to look for:**
- Big-stat pages: does the number sit on a baseline, or float?
- Left/right column tops aligned in `grid-2-7-5`?
- `frame-img` + caption proportions consistent across pages?
- Mono labels: same letter-spacing? same uppercase rule?
- Any orphaned `<br>` causing 1-character lines?

**0–4** Visible tape and string. **5–6** Most pages clean, 1–2
ragged. **7–8** Polished, expert eye finds 2–3 misses. **9–10**
Magazine-grade — the kind of detail that makes printed-by-hand
typographers nod.

### 4. Functionality · 功能性

> Does the artifact *work* for its intended use? Click targets, nav,
> readability at presentation distance, copy-paste-ability for code
> blocks, mobile fallback if relevant.

**Evidence to look for:**
- Deck: keyboard / wheel / touch nav all working? Iframe scroll
  fallback?
- Landing: CTA above the fold? Phone number tappable on mobile?
- Runbook: code blocks copyable, mono font, no smart quotes?
- Critical info readable from 4m away (large screen presentation)?

**0–4** Visually fine but doesn't accomplish its job. **5–6** Core
flow works, edge cases broken. **7–8** Robust through normal use.
**9–10** Defensively engineered — handles iframe / fullscreen / paste
/ print without flinching.

### 5. Innovation · 创新性

> Does this push past the median? Is there one element that makes
> people lean in?

**Evidence to look for:**
- One *unexpected* layout / motion / typographic move that wasn't
  required?
- Or 100% safe — could be any deck/landing from any agency?
- Is the innovation *earned* (matches direction) or grafted on
  (random WebGL on a Kinfolk slow-living deck)?

**0–4** Generic AI-slop median. **5–6** Competent and unmemorable.
**7–8** One memorable moment, the rest solid. **9–10** Multiple
moves you'd steal — but each one obviously serves the thesis.

## Scoring discipline (read before you score)

- **Always cite evidence** — "scored 4 because hero page mixes
  Playfair display with Inter sans on the same line" beats "feels
  inconsistent". Numbers without evidence get rejected.
- **Don't average up** — if Hierarchy is 5 because page 3 is broken,
  don't bump to 7 because pages 1 and 2 are fine. The score is the
  *worst sustained band*.
- **Don't grade-inflate** — a 7 means *strong*, not *acceptable*. If
  every score is 7+, you're not reviewing critically.
- **Innovation is allowed to be low** — 5/10 is fine for production
  deliverables. Don't punish *appropriate* conservatism.

