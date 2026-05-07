# Design schools — execution paths

> Companion to `design-systems-schools/`. Explains how to read each school's 7-column execution-path matrix and which external tools to pair with the path you pick.

**Last validated:** 2026-05-07. Tools change; recommendations rot. Re-validate at quarterly cadence.

---

## How to read the 7-column matrix

Every school's `SCHOOL.md` ships an `## Execution-path matrix` with 7 scenario columns rated ★★★ / ★★☆ / ★☆☆ and a recommended approach per scenario.

| Column | What it measures | What ★★★ means |
|---|---|---|
| **Flutter UI** | Fit for app UI emitted by `theme-port` / `theme-extend` / `theme-motion`. | The school's discipline translates well to Flutter widgets; the look survives the framework's idioms. |
| **HTML mockup** | Fit for static HTML emitted by `frontend-design --school <slug>`. | The school is most legible in CSS-driven HTML — typography and spacing render natively. |
| **PPT** | Fit for keynote / board / launch decks. | The school's print legacy is dense in this format; HTML→PPT export reproduces the discipline cleanly. |
| **PDF** | Fit for long-form printable artifacts (annual reports, white papers, monographs). | The school *was invented* for print. HTML→PDF export is high-fidelity. |
| **Infographic** | Fit for static, dense data-explanation graphics. | Tufte-aligned data visualization is core to the school's vocabulary. |
| **Cover** | Fit for book / album / magazine / event-poster covers. | The school is imagery-strong and the "one big move" register works in cover proportions. |
| **AI-image-gen** | Fit for generative-image tools (Midjourney, Stable Diffusion XL, Sora, Runway). | The school's vocabulary is well-represented in generative-model training data; prompts using the Prompt DNA produce on-style outputs. |

**Ratings are not quality judgments** — every school is "good" for its strong scenarios. ★☆☆ means "doing this requires fighting the school"; ★★★ means "the school was made for this".

---

## When HTML path (in our pipeline) vs external tool

The design-workflow pipeline ships HTML and Flutter natively. The 5 other scenarios route to external tools:

| Path | Source | Tool | Output |
|---|---|---|---|
| Flutter UI | `frontend-design --school` → `theme-port --from-html` | (in-pipeline) | `lib/features/<feature>/presentation/widgets/<name>.dart` |
| HTML mockup | `frontend-design --school` | (in-pipeline) | `<feature>.html` (tweaks-ready) |
| PPT | the HTML mockup as source | **Marp** or **Slidev** with the school's CSS as theme | `.html`/`.pdf` slide deck |
| PDF | the HTML mockup as source | **Pandoc** (HTML→PDF), **Typst**, or **Prince** | `.pdf` |
| Infographic | the HTML mockup as source | **Puppeteer** / **Playwright** screenshot to PNG/SVG | `.png` / `.svg` |
| Cover | the HTML mockup as source | Puppeteer screenshot → bring into Figma / Affinity for final touch | `.png` / `.pdf` |
| AI-image-gen | the school's `## Prompt DNA` section as the prompt | **Midjourney**, **Stable Diffusion XL**, **Runway** (video), **Sora** (video) | `.png` / `.mp4` |

The pattern is **HTML-as-canonical-source**. We invest in `frontend-design --school` because it's the source for almost every downstream scenario. Don't try to author PPT or PDF directly; emit HTML, then convert.

---

## Recommended external tools (with last-validated date)

### Slide decks (PPT scenario)

- **[Marp](https://marp.app/)** (last validated 2026-05-07) — Markdown-driven slides; theme via CSS. Best when the deck is content-heavy and you want git-friendly source. Pair with the school's CSS as `<style>` in the front-matter.
- **[Slidev](https://sli.dev/)** (last validated 2026-05-07) — Vue-based; supports interactive slides. Best when the deck has live demos or animated transitions. School CSS as a custom theme.
- **[Reveal.js](https://revealjs.com/)** (last validated 2026-05-07) — Pure HTML/JS slides. Best when the deck IS a website (TED talk format). Heavier than Marp but more flexible.

For Müller-Brockmann / Editorial / Pentagram / Atelier-Zero (all ★★★ on PPT): Marp + the school's CSS produces immediately credible decks.
For Memphis / Sagmeister-Walsh (★★☆): Slidev's interactive support helps reproduce the energy.
For Brutalism / Active Theory / Locomotive (★☆☆): consider whether the artifact really needs to be a deck — record a screencast of the live HTML instead.

### PDFs (PDF scenario)

- **[Pandoc](https://pandoc.org/)** (last validated 2026-05-07) — HTML→PDF via wkhtmltopdf or weasyprint. Best for general PDFs; mature and cross-platform.
- **[Typst](https://typst.app/)** (last validated 2026-05-07) — Modern academic PDF authoring; not HTML-driven but the syntax is more LaTeX-replacement-friendly. Best for whitepapers / academic essays.
- **[Prince](https://www.princexml.com/)** (last validated 2026-05-07) — Commercial PDF renderer with the highest fidelity for CSS Print Media. Best when the PDF is the deliverable and your client demands print-grade.
- **[Paged.js](https://pagedjs.org/)** (last validated 2026-05-07) — Open-source CSS-Paged-Media implementation; runs in the browser. Best for in-browser PDF preview before export.

For Müller-Brockmann / Editorial / Pentagram / IA / Takram / Atelier-Zero (all ★★★ on PDF): Pandoc or Prince produces print-grade output. Set `@page` rules in CSS for paper size / margins / page breaks.
For Kenya Hara (★★★): same tools, but be ready to tune the spacing — Hara's `ma` translates well to print but the default web-line-heights are too tight.

### Infographics

- **[Puppeteer](https://pptr.dev/)** / **[Playwright](https://playwright.dev/)** (last validated 2026-05-07) — Headless-browser screenshot. Best for converting HTML to high-res PNG/SVG. The pattern: render HTML at 2x or 3x device pixel ratio, screenshot, output.
- **[D3.js](https://d3js.org/)** (last validated 2026-05-07) — Programmatic data-driven SVG. Best when the data is complex and the school is Takram or Müller-Brockmann.
- **[Observable Plot](https://observablehq.com/plot)** (last validated 2026-05-07) — D3 made declarative. Lower learning curve.

For Müller-Brockmann / Editorial / Takram (all ★★★ on Infographic): D3 or Observable Plot driven by the school's typography + color tokens, screenshot via Puppeteer.
For Memphis (★★☆): pattern-fills work in SVG; D3's `<pattern>` element is the hook.

### Covers

- **[Puppeteer](https://pptr.dev/)** screenshot of HTML, then **[Figma](https://www.figma.com/)** or **[Affinity Publisher](https://affinity.serif.com/publisher/)** for final touches (bleed, color profile, vector type).
- For book covers specifically: **[Adobe InDesign](https://www.adobe.com/products/indesign.html)** when the deliverable is going to print spec.

For Memphis / Sagmeister-Walsh / Pentagram / Atelier-Zero (all ★★★ on Cover): the HTML emit + screenshot path works well; final touches in Figma.

### AI-image-gen

- **[Midjourney](https://www.midjourney.com/)** (last validated 2026-05-07) — strongest at painterly / artistic / Sagmeister-and-Memphis registers; weaker at Müller-Brockmann reduction.
- **[Stable Diffusion XL](https://stability.ai/sdxl)** (last validated 2026-05-07) — local-runnable, more controllable. Good for batch generation per school's prompt DNA.
- **[Runway Gen-3](https://runwayml.com/)** / **[Sora](https://openai.com/sora/)** (last validated 2026-05-07) — video generation; pairs with Active Theory and Locomotive (kinetic schools).
- **[FLUX](https://blackforestlabs.ai/)** (last validated 2026-05-07) — newer image model with strong typography rendering.

For Memphis / Sagmeister-Walsh / Active Theory (all ★★★ on AI-image-gen): paste the school's `## Prompt DNA` paragraphs verbatim into the model; supplement with project-specific subject keywords. The Prompt DNA is the source-of-truth.
For Müller-Brockmann / Information Architects / Kenya Hara / Takram (all ★☆☆): don't bother — generative models default to ornament; the school's reduction principle is alien to them. Hand-author or skip.

---

## How a marketing user would use this doc end-to-end

Scenario: a fintech startup needs an annual report PDF. The brand should feel disciplined, data-respectful, premium-print register.

1. **Pick a school.** Read `design-systems-schools/README.md`; the Print-strong category includes Müller-Brockmann, Kenya Hara, Editorial, Atelier-Zero. Müller-Brockmann is the canonical fit for an annual report (corporate, grid-locked, data-respectful).
2. **Read the school's matrix.** PDF column is ★★★ — strong fit. Recommended approach: "use HTML → Pandoc or Typst with grid-locked layout."
3. **Generate the palette.** `/theme-create --inspired-by-school muller-brockmann` — produces a constraint-respecting `AppColors` (or in this case, CSS variables for the HTML).
4. **Generate the mockup.** `/frontend-design --school muller-brockmann "fintech annual report 2026 — 16-page layout, hero metrics, board section, financial tables, audit appendix"` — Clara emits HTML respecting the school's prompt DNA.
5. **Refine via tweaks** if needed: `/tweaks <html-path>` — explore knobs without re-prompting.
6. **Export to PDF.** `pandoc input.html -o annual-report.pdf --css mb.css --pdf-engine=weasyprint` — or Typst, or Prince. The HTML's `@page` rules + the school's CSS produce print-grade output.
7. **Critique before delivering.** `/theme-critique --mode 5dim annual-report.html` — radar-chart review against the 5dim rubric; identify what to fix.

Same pattern for any of the 7 scenarios: pick school → check matrix → generate palette + HTML → convert via the recommended external tool.

---

## What we will *not* ship in-repo

Deliberate non-goals (per `.specs/project/STATE.md` D-25):

- No PPT generator (Marp / Slidev are the recommended path).
- No PDF generator (Pandoc / Typst / Prince are the recommended path).
- No infographic generator (Puppeteer + D3 / Observable Plot are the recommended path).
- No cover generator (HTML + Figma is the path).
- No AI-image-generator wrapper (Midjourney / SDXL / Runway are the path).

The design-workflow ships HTML and Flutter natively. Everything else is a routing recommendation.

---

## Re-validation cadence

Quarterly. Tools change; new ones launch (FLUX appeared after the v1.5 spec was drafted); existing ones deprecate. The "Last validated" footer per recommendation invites re-checking. When a tool changes meaningfully, edit the bullet and bump the date.
