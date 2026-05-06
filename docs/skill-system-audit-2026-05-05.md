# Skill System Audit — 2026-05-05

Sessão de revisão e materialização das skills locais (`~/.claude/skills/`) e
gap-analysis contra o repo público `github.com/fitiodevs/design-workflow`.

---

## 1. Estado inicial encontrado

### 1.1 Repo público `design-workflow`

- Último commit: `8d5e617 docs: add ROADMAP with v0.2-v0.6 backlog + recurring sweep idea`
- **Zero tags** (sem `pre-alignment`, sem `v0.1.0`)
- **Sem `.specs/`** — a spec de 38 tasks de alignment **nunca foi pushed**
- 13 skills (sem prefixo `fitio-`):

  ```
  frontend-design   theme-audit     theme-bolder
  theme-create      theme-critique  theme-distill
  theme-extend      theme-motion    theme-port
  theme-prompt      theme-quieter   theme-sandbox
  ux-writing
  ```

### 1.2 Local `~/.claude/skills/` (antes da sessão)

17 dirs:

```
caveman           fitio-atlas-save      fitio-promote
fitio-status      fitio-theme-audit     fitio-theme-create
fitio-theme-extend fitio-theme-port     fitio-theme-prompt
fitio-theme-sandbox fitio-ux-writing    frontend-design  (← global)
generator-pallete pallete-color        graphify
tlc-closure       tlc-spec-driven
```

### 1.3 Descompasso `CLAUDE.md` global × disco

`CLAUDE.md` anunciava 21 skills + 12 personas, mas **6 dirs não existiam**
fisicamente — eram "fantasmas" registrados só no `CLAUDE.md` e como
`docs/personas/*.md`:

| Persona | Skill anunciada | Dir físico | Repo público |
|---------|-----------------|------------|--------------|
| Júri    | `fitio-theme-critique` | ❌ | ✅ `theme-critique` |
| Brasa   | `fitio-theme-bolder`   | ❌ | ✅ `theme-bolder` |
| Calma   | `fitio-theme-quieter`  | ❌ | ✅ `theme-quieter` |
| Lâmina  | `fitio-theme-distill`  | ❌ | ✅ `theme-distill` |
| Jack    | `fitio-theme-motion`   | ❌ | ✅ `theme-motion` |
| Clara   | `fitio-frontend-design`| ❌ | ✅ `frontend-design` |

Resultado: invocar `/Júri`, `/Brasa`, `/Calma`, `/Lâmina`, `/Jack` ou `/Clara`
caía no fallback de routing — nenhuma das skills rodava de fato.

---

## 2. Decisões da sessão

### 2.1 Cortes propostos pelo usuário (NÃO executados ainda)

Pendentes — aguardam decisão pós-alignment ou em sessão futura:

- `fitio-theme-prompt` — remover (sub-skill chamada só pelo sandbox)
- `fitio-theme-sandbox` — remover (Stitch MCP não usado desde 2026-04-28)
- Atlas trio (`fitio-status`, `fitio-promote`, `fitio-atlas-save`) — avaliar
  unificação numa única `/atlas <subcommand>`

### 2.2 Materialização das 6 ghost skills (EXECUTADO)

Caminho escolhido: copiar do repo `design-workflow` → renomear pra
`fitio-<name>` no disco local. Mantém prefixo `fitio-` que o `CLAUDE.md` já
referenciava, sem forçar rename de tudo.

Conflito resolvido: `~/.claude/skills/frontend-design/` (global, 89 linhas) foi
**deletado** em favor de `fitio-frontend-design/` (Clara, vinda do repo) — não
faz sentido manter dois mockup-generators.

---

## 3. Ações executadas

```bash
SRC=/tmp/design-workflow-check/skills
DST=~/.claude/skills

cp -r $SRC/theme-critique  $DST/fitio-theme-critique
cp -r $SRC/theme-bolder    $DST/fitio-theme-bolder
cp -r $SRC/theme-quieter   $DST/fitio-theme-quieter
cp -r $SRC/theme-distill   $DST/fitio-theme-distill
cp -r $SRC/theme-motion    $DST/fitio-theme-motion
cp -r $SRC/frontend-design $DST/fitio-frontend-design

rm -rf $DST/frontend-design   # global antigo
```

**Resultado:** 22 skills físicas (17 → +6 novas → −1 global removido).

**Validação no harness:** as 6 skills foram reconhecidas no mesmo turno, sem
restart do Claude Code. `/Júri`, `/Brasa`, `/Calma`, `/Lâmina`, `/Jack`,
`/Clara` agora resolvem para a skill real.

---

## 4. Débitos identificados (entram na fase de alignment)

### 4.1 Frontmatter divergente

Todas as 6 skills copiadas têm `name:` no frontmatter **sem o prefixo
`fitio-`**:

```yaml
# fitio-theme-critique/SKILL.md
name: theme-critique          # ← divergente do dirname
```

O harness resolve por dirname (funciona), mas é exatamente o item T-frontmatter
da spec de alignment. Decisão a tomar: padronizar `name = dirname` (com
prefixo `fitio-`) ou remover o prefixo dos dirs.

### 4.2 Skills locais Fitio que NÃO estão no repo público

Não foram promovidas pra `design-workflow` (decisão pendente):

- `fitio-status` (Atlas)
- `fitio-promote` (Atlas Promote)
- `fitio-atlas-save` (Atlas Cronista)
- `fitio-theme-prompt` (provavelmente removido em vez de promovido)
- `fitio-theme-sandbox` (idem)
- `caveman`, `graphify`, `tlc-spec-driven`, `tlc-closure` (são tooling, não
  design — provavelmente ficam fora)

### 4.3 Typos no `~/.claude/skills/`

- `generator-pallete/` (não é `generator-palette`)
- `pallete-color/` (não é `palette-color`)

Não estão registradas no `CLAUDE.md`, parecem leftover. Avaliar se
deletam/renomeiam.

### 4.4 Personas fantasma residuais no `CLAUDE.md`

`CLAUDE.md` global ainda lista as 6 skills com suas linhas de persona —
agora elas existem, então as linhas estão **corretas pela primeira vez**.
Nenhuma ação necessária aqui, mas vale revalidar paths nos triggers EN durante
o alignment.

---

## 5. Próximos passos — pra rodar dentro do repo `design-workflow`

### 5.1 Bootstrap (1 sessão curta)

```bash
git clone git@github.com:fitiodevs/design-workflow.git
cd design-workflow
git tag pre-alignment 8d5e617
git push origin pre-alignment
git checkout -b alignment
```

### 5.2 Recriar a spec `skill-creator-alignment`

Spec **não existe em disco** — vivia só na sessão que gerou o plano.
Reconstruir em `.specs/features/skill-creator-alignment/{spec,design,tasks}.md`
via `/tlc-spec-driven`. Escopo das 38 tasks (6 frentes):

1. **Frontmatter** — `name = dirname`, descrições objetivas, sem persona-leak
2. **Brand** — de-Fitiozar (paths `lib/`, `docs/design-clara.md`, etc.)
3. **Disclosure** — license header, attribution
4. **Scripts** — paths relativos, fallback quando script não existe
5. **Evals** — smoke tests por skill (trigger → sample input → expected output)
6. **Triggers EN** — primary EN, alias PT (`/critique` primary, `/Júri` alias)

### 5.3 Rodar alignment

`/tlc-closure` (ou `/tlc-spec-driven`) sobre as 13 skills do repo.
RalphLoop até zero loose ends.

### 5.4 Promoção das locais (após alignment passar)

Decisão por skill:

| Skill local | Destino |
|-------------|---------|
| `fitio-status` | promover como `cartographer` ou descartar (Fitio-only?) |
| `fitio-promote` | idem |
| `fitio-atlas-save` | idem |
| `fitio-theme-prompt` | remover |
| `fitio-theme-sandbox` | remover |
| `caveman` | fora do design-workflow (não é design) |
| `graphify` | fora |
| `tlc-spec-driven` | fora (já tem repo próprio?) |
| `tlc-closure` | fora (já tem repo próprio: `fitiodevs/tlc-closure`) |

### 5.5 Bump versão e publicar

`v0.2.0` com:
- 13 skills aligned
- spec `skill-creator-alignment` em `.specs/`
- tag `pre-alignment` como rollback
- (opcional) Atlas trio promovido

---

## 6. Anexos — frontmatter atual das 6 novas skills

```yaml
# fitio-theme-critique
name: theme-critique
license: Complete terms in LICENSE.txt
description: Crítica de design de uma tela/feature do Fitio. (...)
triggers: [/theme-critique, /Júri, /Juri]

# fitio-theme-bolder
name: theme-bolder
triggers: [/theme-bolder, /Brasa, /brasa]

# fitio-theme-quieter
name: theme-quieter
triggers: [/theme-quieter, /Calma, /calma]

# fitio-theme-distill
name: theme-distill
triggers: [/theme-distill, /Lâmina, /Lamina]

# fitio-theme-motion
name: theme-motion
triggers: [/theme-motion, /Jack, /jack]

# fitio-frontend-design
name: frontend-design
triggers: [/frontend-design, /Clara, /clara]
```

---

**Ponteiro de memória:** este audit substitui parcialmente o memo
`design_workflow_alignment_spec` (que assumia a spec já em disco). A spec
**ainda precisa ser recriada** antes de rodar o alignment.
