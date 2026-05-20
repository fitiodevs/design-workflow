# Onboarding — design-workflow

Mapa de "quando você quer X, invoque Y" — para alguém novo entender o squad em 30 segundos.

## Tabela completa

| Fase | Quando você quer... | Slash command | Persona | Output / artefato |
|---|---|---|---|---|
| **Palette** | Criar palette nova do zero | `/theme-create` | Compositor / Clara | `AppColors` Dart class + ficha em `docs/themes/<slug>.md` |
| **Palette** | Palette inspirada em marca (Stripe, Linear, etc.) | `/theme-create --inspired-by <slug>` | Compositor | mesma estrutura + `rationale.md` |
| **Palette** | Palette guiada por filosofia (Müller-Brockmann, Pentagram) | `/theme-create --inspired-by-school <slug>` | Compositor | mesma estrutura + constraint trace |
| **Palette** | Listar bibliotecas disponíveis (brands ou schools) | `/theme-create --browse [<category>]` | Compositor | terminal output |
| **Tokens** | Adicionar token semântico (cor, type, spacing, radius) | `/theme-extend` | Cirurgião | `AppColors` + `docs/design-tokens.md` |
| **Mockup** | Criar mockup HTML production-grade | `/frontend-design` | Clara | `mockups/<feature>-<variant>.html` |
| **Mockup** | Explorar variantes via panel de knobs CSS | `/tweaks <path>.html` | Tweaker | `<path>.tweaks.html` (sibling) |
| **Motion** | Adicionar/tunar animação (justificada por lens) | `/theme-motion` | Jack | tokens motion + widget animado |
| **Refinement** | Tela aggressive/saturated demais | `/theme-quieter` | Calma | tela refinada (lower commitment) |
| **Refinement** | Tela bland/timid/AI-safe | `/theme-bolder` | Brasa | tela amplificada (higher commitment) |
| **Refinement** | Tela com >4 decision points | `/theme-distill` | Lâmina | tela simplificada (progressive disclosure) |
| **Audit** | Hardcoded colors, fontes, off-scale, WCAG | `/theme-audit` | Lupa | terminal report + `audit-<date>.md` |
| **Audit** | Nielsen 10 / cognitive load / AI-slop verdict | `/theme-critique <path>` | Design-Júri | YAML caveman ou HTML radar (`--mode 5dim`) |
| **Audit** | Discovery (greenfield/brownfield interview) | `/theme-critique` (sem args) | Design-Júri | `.specs/features/<f>/discovery.md` + skeletons |
| **Copy** | Reescrita de label/CTA/empty state/error | `/ux-writing` | Pena-UX | before/after com strings Dart pasteable |
| **Flow** | Auditar jornada cross-tela (reachability, IA) | `/flow` | Flow | `docs/flows/audit-<date>.md` + YAML handoff |
| **Flow** | Gerar tasks de fix da jornada | `/flow --dispatch` | Flow | `docs/flows/audit-sequence-<date>.md` |
| **Port** | HTML mockup → Flutter/RN/Next widgets | `/theme-port --from-html <path>` | UI-Architect | widgets nativos em `lib/`/`components/` |
| **Port** | Figma frame → widgets | `/theme-port <figma-url>` | UI-Architect | widgets nativos |

## Pipeline típico

```
/theme-audit                              → baseline
/theme-create --browse                    → escolhe inspiração
/theme-create --inspired-by <slug>        → palette
/frontend-design                          → mockup HTML
/tweaks mockups/<f>.html                  → explora variantes
/theme-critique mockups/<f>.html          → review formal
/theme-port --from-html mockups/<f>.html  → widgets nativos
/theme-audit                              → valida pós-port
```

## Quando o port faz parte de um spec de produto

Se você usa este plugin junto com [product-workflow](https://github.com/fitiodevs/product-workflow), o port típico vira uma task dentro de `.specs/features/<feature>/tasks.md`:

```
# product-workflow side
/sequence <feature>      # Arquiteto cria task "T-NN: port mockup X.html → widgets"
/ship <feature>          # Arquiteto invoca /theme-port no momento certo
```

Sem product-workflow, você invoca `/theme-port` direto e o port acontece imediatamente.

## Personas — referência rápida

| Persona | EN alias | Skills que owna |
|---|---|---|
| Clara | Designer | `/theme-create`, `/frontend-design`, `/tweaks`, `/theme-extend`, `/theme-motion`, `/theme-quieter`, `/theme-bolder`, `/theme-distill` |
| Design-Júri | Design Critic | `/theme-critique`, `/theme-audit` |
| Flow | Flow | `/flow` |
| Pena-UX | UX Writer | `/ux-writing` |
| UI-Architect | Arquiteto-UI | `/theme-port` |

Aliases portugueses (`/Lupa`, `/Compositor`, `/Júri`, `/Brasa`, `/Calma`, `/Lâmina`, `/Jack`) também funcionam — todos apontam pro mesmo operator.

## Skills stack-agnostic (rodam em qualquer projeto)

- `/theme-critique`
- `/theme-create`
- `/frontend-design`
- `/ux-writing`

Skills que emitem código nativo (`/theme-port`, `/theme-extend`, `/theme-motion`, `/theme-audit`) usam o **stack adapter** declarado em `.design-workflow.yaml` (`flutter` | `nextjs-tailwind` | `react-native`). Default: `flutter`.

## Onde ler mais

- [README.md](../README.md) — visão geral + install
- [docs/personas.md](personas.md) — todos os aliases (PT/EN) por skill
- Cada skill tem seu próprio `SKILL.md` em `skills/<name>/` com workflow, schema e anti-patterns.
