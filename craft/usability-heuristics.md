> **Adapted from:** [`wondelai/skills` → `ux-heuristics`](https://github.com/wondelai/skills) (MIT), distilling Steve Krug's *Don't Make Me Think* and the dark-patterns literature.
> **License:** MIT
> **Local path:** `craft/usability-heuristics.md`
> **Note:** Authored for this repo (not auto-synced). **Deliberately does NOT restate Nielsen's 10 heuristics** — `theme-critique` (Olavo) owns the Nielsen 0–4 scoring and `docs/flow-heuristics.md` owns the journey set. This file adds the two things those don't cover: Krug's scanning laws and a dark-patterns taxonomy. Edits here are safe.

---

# Usability heuristics craft rules — scanning & dark patterns

Two additions to the Nielsen 10 that Olavo already scores and the flow
heuristics Flavio already runs. Krug's premise: **users scan, satisfice,
and muddle through** — they do not read, optimize, or learn the system.
Design for the scanner.

## Krug's three laws

**1. Don't make me think.**
Every screen should be self-evident — a glance answers "what is this and
what do I do here?". Each question the UI forces the user to resolve
(*"is this clickable?" "where am I?" "what does this label mean?"*) spends
a little goodwill. Eliminate questions; don't decorate around them.
- Make clickable things look clickable; make non-clickable things not.
- Name things what they are. A clever label that needs a second look
  failed the law.
- Show where the user is (active tab, breadcrumb, screen title).

**2. Clicks don't matter — confidence per click does.**
Step *count* is the wrong metric; *certainty* is the right one. Three
obvious, confident taps beat one tap the user hesitates over. Don't
collapse a flow into fewer mystery steps. (Mirrors Jobs' "steps-to-value"
but corrects the naïve version — reduce hesitation, not just hops.)

**3. Cut half the words. Then cut half again.**
Most interface copy is filler — happy talk and instructions nobody reads.
Removing it surfaces the content that matters and shortens the scan.
Pairs with `ux-writing` (Pena): the rewrite usually *deletes* before it
improves.

## Severity scale (when reporting a usability issue)

Score each issue 0–4 by impact, then weight by frequency × persistence:

| Severity | Meaning |
|---|---|
| 0 | not a usability problem |
| 1 | cosmetic — fix if time permits |
| 2 | minor — low priority |
| 3 | major — important to fix, raises failure rate |
| 4 | catastrophic — blocks task completion, fix before ship |

Frequency (how many users hit it) and persistence (does it bite once or
every time) escalate a nominal severity. A "minor" issue on the primary
flow's every use is not minor. This is the calibration Olavo's P0–P3 map
should fold into when scoring.

## Dark-patterns taxonomy (never ship these)

Usability used *against* the user. These fail the floor regardless of how
"clean" the screen looks — extends the ethical boundaries already in
`anti-ai-slop.md`.

- **Roach motel** — easy to get in, hard to get out (one-tap signup,
  buried/contact-us-only cancellation). Cancellation deserves the same
  craft as onboarding.
- **Confirmshaming** — guilt-laden decline copy ("No thanks, I hate
  saving money"). Decline options stay neutral.
- **Forced continuity** — silent charge after a trial with no reminder.
- **Hidden costs / drip pricing** — fees revealed only at the last step.
- **Misdirection & false hierarchy** — the manipulative choice styled as
  the primary button; the honest choice as faint text. (This is
  `visual-hierarchy.md`'s levers turned malicious.)
- **Preselected opt-ins** — consent/marketing checkboxes on by default.
- **Trick questions / double negatives** in toggles and consent.
- **Nagging** — repeated interruption until the user gives in.
- **Obstruction** — inserting steps to discourage a legitimate action.

Rule: if a pattern's goal is to make the user do something *they
wouldn't choose with full clarity*, it's a dark pattern — cut it, even
if it lifts a metric. A short-term conversion bought with a dark pattern
is a long-term trust debt.

## Common mistakes (lint these)

- Optimizing **click count** while raising hesitation per click.
- Clever labels that fail "self-evident at a glance".
- No visible **"you are here"** signal (active state, title, breadcrumb).
- Instructional/filler copy that survives the "cut half the words" pass.
- A consent or marketing **opt-in preselected**.
- The manipulative option styled as the primary action.
- Cancellation/offboarding harder than signup (roach motel).
