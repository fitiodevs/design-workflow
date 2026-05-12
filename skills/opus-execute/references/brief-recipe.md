# Brief-recipe — anatomia de um brief auto-contido pra sub-agente

Sub-agente despachado via `Agent` tool roda em **contexto fresco** — não vê a conversa Opus. Toda decisão, constraint, arquivo relevante tem que ir no brief explicitamente. Se você não escreveria isso pra um colega humano por mensagem sem follow-up, o brief não tá pronto.

## As 5 seções obrigatórias

Ordem fixa. Pular qualquer uma força o sub-agente a inventar — output sai enviesado pro genérico LLM ("AI default").

### 1. Context

**O quê é, por que está sendo feito, qual a parte que importa.**

1–3 frases. Não conta a história inteira da conversa; conta o suficiente pra orientar a decisão se o sub-agente tiver dúvida.

**Bad:**
> Implementa o modal novo.

**Good:**
> Modal de confirmação de resgate de cupom — substitui o `showDialog` atual em `coupons/page.dart:142`. Decidi AlertDialog em vez de bottom sheet porque a ação é destrutiva e o padrão do app é `AppDialog` pra destruição. Já existe `AppDialog` em `lib/core/widgets/`.

Por quê o "good" funciona: o sub-agente sabe (a) o que substituir, (b) qual padrão usar, (c) por quê — então se precisar tomar uma micro-decisão de UX, decide na mesma direção.

### 2. Files

**Cada arquivo que o sub-agente vai tocar OU precisa ler, com role explícita.**

Convenção: `<path>:<role>`. Roles canônicos:

- `edit` — vai modificar
- `create` — vai criar do zero
- `read-only` — leitura pra entender contexto/conventions
- `reference-only` — leitura pra copiar padrão (ex: outro widget que já implementa o que está sendo replicado)

**Bad:**
> Os arquivos da feature de cupom e talvez o tema.

**Good:**
> - `lib/features/coupons/presentation/pages/coupon_detail_page.dart:edit`
> - `lib/core/widgets/app_dialog.dart:reference-only`
> - `lib/features/coupons/presentation/controllers/coupon_controller.dart:read-only` (vai chamar `redeem()`)
> - `docs/design-tokens.md:read-only`

Por quê o "good" funciona: o sub-agente abre só esses, não fica fuçando o repo inteiro. Read budget previsível.

### 3. Acceptance

**Como o sub-agente sabe que terminou. Critérios observáveis, idealmente com comando de validação.**

Lista de bullets. Cada bullet é binário (pass/fail), não fofo.

**Bad:**
> Funcionar bem e seguir o design.

**Good:**
> - `flutter analyze` retorna `No issues found!`
> - Modal renderiza em light e dark sem overflow
> - Tap fora do modal não fecha (modal é destrutivo, exige escolha)
> - CTA primário "Resgatar agora" chama `couponController.redeem(coupon.id)`
> - CTA secundário "Cancelar" só fecha o modal (sem side effect)
> - Copy em pt-BR: "Resgatar agora", "Cancelar", título "Confirmar resgate?"

Por quê o "good" funciona: sub-agente pode rodar `flutter analyze` e auto-verificar a 1ª. Os outros são checagens manuais que o user pode rodar quando a notificação chegar.

### 4. Constraints

**Convenções, anti-patterns, regras do CLAUDE.md aplicáveis. Explícitas — mesmo que pareçam óbvias.**

Por quê não pular: o sub-agente não tem CLAUDE.md memorizado da conversa Opus — ele pode até abrir o arquivo, mas pode também escolher o atalho. Lista o que importa.

**Bad:**
> Seguir o tema e as convenções do projeto.

**Good:**
> - Usar `AppDialog` (do `lib/core/widgets/`) — NÃO Material `AlertDialog` nem `showDialog` raw.
> - Cores via `context.colors.semanticRole`, NUNCA `Color(0xFF...)` ou `Colors.X`.
> - Copy pt-BR segue `docs/product.md` §4.5 — arco "Querer → Pegar → É seu". Banidos: "Mirar", "Comprar", "Resgatar como missão".
> - Sem `print()` — usa `AppLogger.info/warning/error`.
> - Sem comentários explicando o que o código faz; só por quê quando não-óbvio.

### 5. Style

**Estilo de output: verbosidade, comentários, formato da resposta final do sub-agente.**

1–3 bullets curtos. Sobrescreve defaults só onde for diferente.

**Good:**
> - Sem comentários no código. Sem TODOs.
> - Sem mensagem de resumo no fim — o diff fala.
> - Se houver decisão arquitetural que mudei do brief, sinaliza com 1 linha no final.

Por quê útil: sub-agente default pode encher de comentários defensivos e fechar com 3 parágrafos de "What I changed". Pra fluxo de batch dispatches, isso vira ruído.

## Template em branco

```markdown
## Context
<1-3 frases>

## Files
- <path>:<role>
- <path>:<role>

## Acceptance
- <bullet>
- <bullet>

## Constraints
- <bullet>
- <bullet>

## Style
- <bullet>
```

Copia, preenche, dispara via `Agent`.

---

## Mapping `tasks.md` → brief (primary flow)

When dispatching via `--from-task <feature>/T-<id>`, the brief is **derived** from `.specs/features/<feature>/{spec,design,tasks}.md` — not written from scratch. The structured fields in tasks.md map cleanly onto the 5 recipe sections:

| Brief section | tasks.md source | spec/design source |
|---|---|---|
| **Context** | `What` (1ª linha) | + 1–2 frases do problema/requisito em `spec.md` |
| **Files** | `Where` paths (`:edit` ou `:create`) + `Reuses` (`:reference-only`) | — |
| **Acceptance** | `Done when` checklist + `Verify` command | — |
| **Constraints** | — | decisões relevantes de `design.md` + CLAUDE.md baseline |
| **Style** | `Commit` (vira "When done, suggest commit message: <verbatim>") | — |

### Exemplo concreto

**tasks.md entry** (de `.specs/features/cadastro-convidado/tasks.md`):

```markdown
### T1: Adicionar campo `isGuest` ao `UserModel`

**What**: Adicionar `final bool isGuest` ao `UserModel` (constructor, `fromSnap`, `toMap`).
**Where**: `lib/app/shared/models/user_model.dart`
**Depends on**: Nenhuma
**Reuses**: padrão de `senhaDefinida` (bool nullable → default false)
**Requirement**: GUEST-01, GUEST-08, GUEST-10

**Done when**:

- [ ] Campo `isGuest` adicionado ao constructor com `this.isGuest = false`
- [ ] `fromSnap`: `isGuest: snapshot['isGuest'] ?? false`
- [ ] `toMap()`: `'isGuest': isGuest`
- [ ] `flutter analyze` passa sem warnings neste arquivo

**Verify**:

`​`​`bash
flutter analyze lib/app/shared/models/user_model.dart
`​`​`

**Commit**: `feat(guest): add isGuest field to UserModel`
```

**Brief emitido pra Sonnet:**

```markdown
## Context
Adicionar `final bool isGuest` ao `UserModel` (constructor, `fromSnap`, `toMap`). Faz parte da feature cadastro-convidado — usuários criam convidados temporários antes de signup completo; o flag distingue user real de convidado. Requirements GUEST-01 / GUEST-08 / GUEST-10 do spec.

## Files
- `lib/app/shared/models/user_model.dart`:edit
- `lib/app/shared/models/user_model.dart`:reference-only (campo `senhaDefinida` — padrão a copiar)

## Acceptance
- Campo `isGuest` adicionado ao constructor com `this.isGuest = false`
- `fromSnap`: `isGuest: snapshot['isGuest'] ?? false`
- `toMap()`: `'isGuest': isGuest`
- `flutter analyze` passa sem warnings neste arquivo
- Validate: `flutter analyze lib/app/shared/models/user_model.dart` retorna `No issues found!`

## Constraints
- Padrão a reusar: `senhaDefinida` (bool nullable → default false). Faça idêntico.
- Sem `Color(0xFF...)`, sem `print()`, sem TODOs (regras do CLAUDE.md).
- pt-BR para qualquer copy; identifiers em inglês.
- Não escreva comentários explicando o que o código faz.

## Style
- Sem mensagem de resumo no fim — o diff fala.
- Quando terminar, sugira commit message: `feat(guest): add isGuest field to UserModel`
- Se desviar do brief, sinalize com 1 linha no fim explicando por quê.
```

Esse brief é literal — 28 linhas, totalmente auto-contido, validável binariamente.

### O que o mapping NÃO faz

- **NÃO inclui o `tasks.md` inteiro no brief.** Sonnet recebe só o necessário pra T1, não as outras 19 tasks da feature. O ponto da delegação é manter o contexto Sonnet pequeno.
- **NÃO copia o spec.md inteiro como Constraints.** Filtra: pega só as decisões que tocam os arquivos em `Where`. Para uma task que mexe em UserModel, a constraint "use Riverpod controllers" do design.md é ruído.
- **NÃO valida `Depends on` automaticamente em paralelo.** Se T-05 depende de T-04, e usuário pede `--range T-04..T-05`, o skill faz T-04 com `--blocking` e T-05 em background DEPOIS — surfaceando o plano e pedindo confirmação. Nunca silently re-ordena.

### Quando o tasks.md está "magro demais" pra dispatch direto

Se a task carece de `Where` ou `Verify`, **o skill recusa o dispatch** e pede pra você completar o task entry antes. Razão: brief magro produz output magro. Melhor consertar a fonte da verdade (tasks.md) do que improvisar no dispatch.

Sintomas de task magra:
- `Where: a definir` ou ausente
- `Done when:` com só "funciona" / "passa"
- `Verify:` ausente ou vago ("rodar testes")

Nesses casos, a skill responde: *"Task T-X tem `Verify` vazio. Quer que eu te ajude a expandir a task em `tasks.md` antes de despachar?"* — e o trabalho de refinar vira mais uma volta de conversa com Opus.

## Checklist antes de dispatchar

Antes de chamar `Agent`, releia o brief e responda mentalmente:

1. Se eu fosse o sub-agente e abrisse só esses 4 blocos, conseguiria começar a editar **agora**? Sem perguntar nada?
2. O acceptance tem critério binário (pass/fail), ou é vaporware ("funcionar bem")?
3. Algum constraint do CLAUDE.md/produto que vale mas não está listado?
4. Algum arquivo precisa ser lido mas não está em Files?
5. O Context explica **por quê**, não só **o quê**?

Se qualquer resposta é "não" ou "talvez", refina o brief. O custo de refinar é 1 minuto; o custo de dispatchar brief ruim é o tempo do sub-agente + cleanup + re-dispatch.

## Quando o brief não cabe no template

Se o brief ficou >2000 chars, considere:

- **Quebrar em N dispatches** menores, cada um auto-contido. Sub-agentes em paralelo entregam mais rápido.
- **Mover constraint comum pra um arquivo** referenciado em Files (ex: `docs/dispatch-conventions.md`). Sub-agente lê uma vez, brief encolhe.
- **Verificar se o trabalho é mesmo delegável.** Brief gigante geralmente significa escopo gigante, e escopo gigante geralmente significa que precisa de back-and-forth — caso em que delegar é o anti-pattern.

## Anti-recipes

Casos onde o brief parecia OK mas Sonnet entregou ruim. Lições:

### "Implementa o que conversamos"

O sub-agente não viu a conversa. Cada decisão da conversa vira 1 bullet no brief. Se você tem preguiça de transcrever, não delega.

### "Segue o padrão dos outros arquivos"

Qual padrão? Qual arquivo? Sub-agente vai abrir 3 arquivos aleatórios e copiar o padrão do primeiro. Liste 1 arquivo `reference-only` específico.

### "Faz tipo o do outro feature"

Mesmo problema acima. Cite o widget exato + path.

### "Não esquece dos testes"

OK, mas quais testes? Em que arquivo? Com qual framework? Adiciona em Files: `test/features/coupons/coupon_detail_test.dart:create` + em Acceptance: `flutter test test/features/coupons/coupon_detail_test.dart passa`.
