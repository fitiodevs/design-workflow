# Discovery — interview protocol

> Reference loaded by `theme-critique` (Júri) **after** `discovery-sizing.md` decides tier.
> Define a ordem fixa, perguntas literais, retry rules, e stop conditions da entrevista.

## Princípios

1. **Ordem fixa.** Produto → Tom → Identidade → Stack. Sempre. Stack nunca primeiro — ninguém escolhe Flutter vs React antes de saber pra quem é o produto.
2. **1 bloco por turno.** Júri faz as perguntas de um bloco, **pausa**, espera resposta, só então avança. Nunca despeja todas as perguntas de uma vez.
3. **Concretude obrigatória.** Adjetivos vazios são recusados. Júri exige refs concretas, sensações físicas, anti-references.
4. **Cap de 2 retries.** Após 2 retries ainda-vagos, persiste resposta com tag `quality: weak` e segue. Entrevista não trava.
5. **Júri não escreve em `lib/`.** Só em `docs/` e `.design-spec/features/<feature>/`.

## Bloco 1 — Produto (3 perguntas)

> Goal: scene sentence + persona primária + tarefa primária.

**P1.1 — Scene sentence.**
*"Em 1 frase no formato 'X usa Y em Z momento para resolver W' — me descreve o produto. Se a frase couber em <20 palavras e tiver as 4 partes, ótimo. Se faltar parte, eu pergunto."*

**P1.2 — Persona primária + 1 trip-up.**
*"Quem é a pessoa principal que usa? Idade, contexto, frequência. E mais importante: 1 momento onde ela costuma travar/desistir num produto similar. Não 'qualquer pessoa' — 1 pessoa concreta."*

**P1.3 — Tarefa primária.**
*"Qual é a única coisa que essa pessoa precisa conseguir fazer aqui? Se sumir tudo menos isso, o produto ainda serve? (Sim/Não — e qual é essa tarefa única.)"*

## Bloco 2 — Tom (3 perguntas)

> Goal: 3 sensações físicas + 1 ref concreta + 1 anti-ref.

**P2.1 — 3 sensações físicas (não adjetivos).**
*"Quando alguém usa essa interface, o corpo sente o quê? 3 sensações físicas — não adjetivos. Bons exemplos: 'aperto leve no peito antes do botão', 'mão relaxa', 'olho desliza'. Maus: 'moderno', 'limpo', 'profissional'."*

**P2.2 — 1 ref concreta.**
*"Me dá 1 produto/site/objeto real que captura ~70% do tom certo. Não 3 (vira média genérica). 1 só. Pode ser app, livro, cafeteria, filme — qualquer coisa concreta."*

**P2.3 — 1 anti-ref obrigatória.**
*"O que **não** pode parecer? 1 anti-reference. Concreto. Ex: 'não pode parecer banco digital', 'não pode parecer app de produtividade B2B', 'não pode parecer LinkedIn'."*

## Bloco 3 — Identidade (3 perguntas)

> Goal: paleta direção + typography mood + iconografia/forma.

**P3.1 — Paleta direção (warm/cool/neutral × commitment).**
*"Direção de cor: warm (terras, fogo, açafrão), cool (azuis, ciano, mar), ou neutral (cinzas, off-white)? E commitment: drenched (cor inunda), restrained (acentos pontuais), ou neutral (quase ausente)? Combinação total. Ex: 'warm restrained' = base neutra + acento âmbar; 'cool drenched' = azul-marinho dominante."*

**P3.2 — Typography mood.**
*"3 sensações pra typography. 'Letrasinda dura', 'tipografia respira', 'serif quente'. Não 'sans-serif clean'. Sensação. Se referência ajuda, cite (ex: 'tipo do Notion mas com mais peso')."*

**P3.3 — Iconografia/forma.**
*"Bordas duras ou arredondadas? Ícones outline-thin, outline-bold, ou filled? Cantos do botão: 0, 4px, 12px, 999px? Decisão de geometria global, não componente-a-componente."*

## Bloco 4 — Stack (2-3 perguntas)

> Goal: framework + theme atual + deploy. Em brownfield, perguntas fazem referência ao output do `audit_theme.py` rodado silently.

**P4.1 — Framework + UI lib.**
*"Flutter (qual versão), Material 3 ou custom? Se custom, qual approach (`ThemeData.copyWith`, design tokens classes, OKLCH-based)?"*

**P4.2 — Tema atual** *(brownfield — referencia números do pre-scan)*.
*"O audit que rodei achou {{audit.hex_count}} hex literals em `lib/features/<x>` e {{audit.fontsize_count}} fontSize hardcoded. Drift acidental ou cor de marca proposital? Em quais features eu posso esperar mais hardcode?"*

**P4.2-greenfield — Tema atual** *(greenfield)*.
*"Já tem palette/typography decidido em algum lugar (Figma, Notion, head)? Se não, vou gerar via `/theme-create` depois — quero saber se já existe ponto de partida."*

**P4.3 — Deploy/distribuição** *(opcional; pular se respondido em P1).*
*"Web, Android, iOS, ou todos? Tema dark obrigatório? Acessibilidade A++ é hard-requirement (3 contrast tiers no `AppColors`)?"*

## Vague-words list (recusa automática)

Se a resposta inclui só termos desta lista (sem complemento concreto), Júri recusa e re-pergunta:

- `moderno`, `clean`, `minimalista`, `tech`, `profissional`, `vibrante`, `bonito`, `user-friendly`, `intuitivo`, `premium`, `elegante`, `natural`
- (EN equivalents) `modern`, `clean`, `minimal`, `professional`, `vibrant`, `beautiful`, `user-friendly`, `intuitive`, `premium`, `elegant`, `natural`

Lista canônica e variações em `references/discovery-vague-words.md`.

## Retry script

Quando recusa, Júri usa este formato (varia entre as 3 versões para não soar repetitivo):

**v1:**
> "Você disse '{{vago}}'. Eu não consigo desenhar '{{vago}}'. Me dá 1 ref concreta (app/site/objeto) + 1 sensação física específica + 1 anti-ref (o que não pode parecer)."

**v2:**
> "'{{vago}}' descreve metade da internet. Pra eu te servir, preciso de 1 lugar onde você viu isso bem feito + 1 lugar onde você viu mal feito + o que muda entre os dois."

**v3:**
> "'{{vago}}' é vácuo. Tenta de novo: 3 sensações físicas (não adjetivos) + 1 produto que captura ~70% disso + 1 que não pode parecer."

## Quality tagging

Cada resposta persistida em `discovery.md` ganha tag:

- `quality: strong` — concreto, ref + sensação + anti-ref presentes.
- `quality: medium` — concreto mas faltando 1 dos 3 elementos.
- `quality: weak` — após 2 retries ainda vago; Júri persiste e segue.

Tags `weak` aparecem destacadas no plano final ("⚠️ entrada fraca em P2.1 — recomendo revisitar antes de Compose").

## Stop conditions

Júri encerra entrevista quando:

1. **Todos os blocos do tier estão completos** (com respostas, mesmo que `weak`).
2. **Cap de 12 perguntas atingido** (proteção contra modo `full` que extrapole).
3. **Usuário pede `--bail`** ou diz "para" — Júri salva o que tem como `status: in_progress` e dá pointer para `--resume`.

## Persistência por bloco

`discovery.md` cresce bloco-a-bloco. Cada bloco é uma seção:

```markdown
## Block 1 — Produto
**status:** complete
**quality:** strong

### P1.1 — Scene sentence
> Maria, mulher 30+, treina musculação 4×/semana às 6h30, abre o app durante o estacionamento pra ver pontos acumulados.

### P1.2 — Persona + trip-up
> ...

## Block 2 — Tom
**status:** in_progress
**quality:** medium

### P2.1 — 3 sensações
> ...
<!-- continuar P2.2 -->
```

Resume (`/juri --resume <feature>`) parsa este formato e identifica o primeiro bloco `status: in_progress`. Detalhes em `references/discovery-resume.md`.
