# Discovery — vague-words list

> Reference loaded by `theme-critique` (Júri) durante a entrevista.
> Lista canônica de termos cuja presença sem complemento concreto dispara recusa + retry.

## Termos banidos (auto-recusa)

Quando a resposta consiste **apenas** desses termos (sozinhos ou enfileirados sem adicional concreto), Júri recusa.

### Português
- `moderno`
- `clean`
- `minimalista`
- `tech`
- `profissional`
- `vibrante`
- `bonito`
- `user-friendly`
- `intuitivo`
- `premium`
- `elegante`
- `natural`
- `legal`
- `bacana`
- `sofisticado`
- `descolado`
- `jovem`
- `urbano`

### English (equivalents — Júri responde em PT-BR mas detecta os dois)
- `modern`
- `clean`
- `minimal` / `minimalist`
- `professional`
- `vibrant`
- `beautiful` / `nice`
- `user-friendly`
- `intuitive`
- `premium`
- `elegant`
- `natural`
- `cool`
- `slick`
- `sophisticated`
- `young`
- `urban`

## Padrões compostos vagos (também recusados)

- "moderno e clean"
- "tech profissional"
- "limpo e minimalista"
- "elegante e sofisticado"
- "premium mas acessível"
- "moderno mas atemporal"

## Quando a recusa NÃO se aplica

Se o termo vem com complemento concreto (ref / sensação física / anti-ref), aceitar como `quality: medium`:

- ✅ "Moderno tipo Linear, mas com mais peso visual — não Figma." → aceito (1 ref + 1 anti-ref).
- ✅ "Clean, mão relaxa, igual o Notion num Mac mini." → aceito (sensação + ref).
- ❌ "Moderno e clean." → recusado.
- ❌ "Premium, sofisticado, elegante." → recusado.

## Templates de retry

Júri varia entre 3 versões para não soar repetitivo. Pick by hash da pergunta + retry count.

### v1 — direto
> "Você disse '{{vago}}'. Eu não consigo desenhar '{{vago}}'. Me dá 1 ref concreta (app/site/objeto) + 1 sensação física específica + 1 anti-ref (o que não pode parecer)."

### v2 — comparativo
> "'{{vago}}' descreve metade da internet. Pra eu te servir, preciso de 1 lugar onde você viu isso bem feito + 1 lugar onde você viu mal feito + o que muda entre os dois."

### v3 — provocativo
> "'{{vago}}' é vácuo. Tenta de novo: 3 sensações físicas (não adjetivos) + 1 produto que captura ~70% disso + 1 que não pode parecer."

## Stop após 2 retries

Se após 2 retries a resposta continua vaga, Júri:

1. Persiste a resposta com tag `quality: weak`.
2. Adiciona comentário no `discovery.md`: `<!-- weak answer; revisitar antes de Compose -->`.
3. Move para a próxima pergunta.
4. Sinaliza no `## Action plan` final: "⚠️ entrada P{{X.Y}} é fraca — recomendo revisitar antes de Compose".

Não trava entrevista. Cap de retries é proteção contra usuário desligar.
