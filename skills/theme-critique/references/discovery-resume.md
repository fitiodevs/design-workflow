# Discovery — resume protocol

> Reference loaded by `theme-critique` (Júri) when user invokes `/juri --resume <feature>`.
> Define como retomar entrevista parcial sem corromper estado nem perder respostas válidas.

## Pré-condições (validação strict)

Júri **só retoma** quando todas estas condições passam:

1. **Arquivo existe.** `.design-spec/features/<feature>/discovery.md` é encontrado.
2. **Frontmatter parseable.** YAML válido entre `---` markers.
3. **Status compatível.** `status: in_progress` (não `draft` virgem, não `approved`, não `consumed`).
4. **Idade ≤14 dias.** `created` field ≤ 14 dias atrás (alinha com REQ-C1.3 que será implementada em Onda C; em Onda A, simplesmente warning se >14d, ainda retoma).
5. **Pelo menos 1 bloco completo.** Senão é mais barato recomeçar.

## Mensagens de erro user-facing

Quando a validação falha, Júri responde com 1 das 5 mensagens abaixo (não tenta retomar, não corrige silenciosamente):

### Erro 1 — file ausente
> "Não encontrei `.design-spec/features/{{feature}}/discovery.md`. Confere se o slug tá certo, ou roda `/juri` (sem args) pra começar nova discovery."

### Erro 2 — frontmatter inválido
> "Frontmatter de `discovery.md` quebrado — provável edição manual. Cola o arquivo aqui pra eu olhar, ou apaga e roda `/juri` de novo."

### Erro 3 — status errado
> "`discovery.md` está com `status: {{status_atual}}`. Resume só funciona em `in_progress`. Se quer recomeçar, apaga e roda `/juri`. Se quer revisar uma já aprovada, abre o arquivo direto."

### Erro 4 — idade >14 dias
> "Esta discovery foi criada {{X}} dias atrás. Recomendação: rodar `/juri` em modo `light` pra atualizar contexto antes de continuar — produto/persona costumam ter mexido."
>
> *(em Onda A, oferecer "continuar mesmo assim" como segunda opção; em Onda C ficará mais firme)*

### Erro 5 — parse de blocos falha
> "Consegui ler o frontmatter mas não consigo identificar onde a entrevista parou. Possível formato corrompido. Me cola o arquivo aqui ou apaga e recomeça com `/juri`."

## Algoritmo "find first incomplete block"

Após validação OK, Júri parsa o markdown:

```
1. Localiza todas as seções `## Block N — <name>`.
2. Para cada seção, lê metadata `**status:** complete|in_progress|pending`.
3. Retorna a primeira seção com `status != complete`.
4. Dentro dessa seção, identifica a primeira pergunta `### PN.M — <name>` sem resposta capturada.
5. Retoma fazendo aquela pergunta literal (de `discovery-protocol.md`).
```

Se todas as seções estão `complete` mas o arquivo ainda é `status: in_progress` no frontmatter, Júri assume que o último passo (gerar plan + escrever skeletons) falhou e retoma daí.

## Output ao retomar

Antes de fazer a próxima pergunta, Júri ecoa um summary curto:

```
Retomando discovery: {{feature_slug}}
- Tier: {{tier}}
- Mode: {{mode}}
- Criado: {{created}} ({{X dias atrás}})
- Blocos completos: {{N}}/{{4}}
- Próximo: Block {{X}} — {{nome_bloco}}, pergunta {{P.X.Y}}.

[primeira pergunta do bloco em aberto]
```

## Side effects do resume

- **Não** apaga seções existentes.
- **Não** muda `quality: weak` para outro valor.
- **Atualiza** `frontmatter.updated_at` se o campo existir; cria se não.
- **Persiste** após cada nova resposta (incremental, não no fim).

## Quando resume falha mid-flow

Se durante o resume o usuário disser "para" ou `--bail`, Júri:

1. Persiste o que foi capturado nas perguntas novas.
2. Mantém `status: in_progress`.
3. Imprime: "Pausado. Retoma com `/juri --resume {{feature}}`."
4. Sai sem efeito colateral em `lib/`.
