# 4 Quality Standards — full filter

Used in Step 3 of `/pena` (`/ux-writing`). Every UI string passes through these 4 questions before reaching the report.

| Standard | Pergunta | Benchmark |
|---|---|---|
| **Purposeful** | Ajuda o usuário a agir ou entender o que ganhou? | Se não, corta. |
| **Concise** | Usa o mínimo de palavras sem perder significado? | CTA: 1-4 palavras. Erro: ≤18 palavras. Body: ≤14 palavras por frase. |
| **Conversational** | Leria em voz alta sem soar robótico? | Voz ativa 85%. Sem gerúndio em CTA ("Entrar", não "Entrando"). |
| **Clear** | Unambíguo, específico, sem jargão? | Verbo específico ("Resgatar" ≠ "Usar"). Número antes da palavra ("+100 pontos"). |

## Severity scale

### P0 — Banidos absolutos (`docs/product.md` §4.2)

Violação P0 = string tem que ser reescrita, sem negociação:

| Padrão proibido | Exemplo violação | Fix |
|---|---|---|
| Vocativo clichê | "atleta!", "campeão!", "guerreiro!" | Remover vocativo. |
| Filler motivacional | "Continue assim", "Você está indo bem", "Jornada fitness" | Número real + resultado. |
| Eufemismo de erro | "Algo deu errado, tente novamente" | O que falhou + como resolver. |
| Gerúndio em CTA | "Salvando...", "Carregando" em botão estático | Imperativo: "Salvar", "Carregar". |
| AI-slop lista §4.2 | "Eleve seu", "Conquiste seus objetivos", "Próximo nível" | Direto, sem coaching. |

### P1 — Viola as 4 quality standards

- String >18 palavras num erro → muito longa.
- CTA genérico ("OK", "Confirmar" sem objeto) → verbo + objeto específico.
- Palavra antes do número ("pontos: 100") → inverter ("100 pontos").
- Passive voice em mensagem de ação ("Foi salvo") → ativo ("Salvo").

### P2 — Inconsistência terminológica

- "check-in" vs "checkin" vs "entrada" no mesmo app.
- "pontos" vs "pts" vs "moedas" misturados.
- Nome do mesmo recurso variando entre telas.

### P3 — Polish

- Data sem formato relativo quando caberia "hoje às 14:30".
- Placeholder que já está no label (redundante).
- Título de seção em maiúsculas onde sentence case seria suficiente.

## Length benchmarks

| Tipo | Ideal | Máximo |
|---|---|---|
| CTA / botão | 1–3 palavras | 6 palavras |
| Título de página | 1–2 palavras | 4 palavras |
| Título de seção | 2–4 palavras | 6 palavras |
| Erro inline | 5–10 palavras | 15 palavras |
| Erro sistêmico | 8–15 palavras | 20 palavras |
| Mensagem sucesso | 3–8 palavras | 12 palavras |
| Empty state (linha 1) | 3–6 palavras | 8 palavras |
| Empty state (linha 2) | 6–12 palavras | 18 palavras |
| Frase de body text | ≤14 palavras | — (90% compreensão) |

> **Rule of thumb:** 8 words/sentence = 100% comprehension. 14 = 90%. Above 20 = rewrite.
