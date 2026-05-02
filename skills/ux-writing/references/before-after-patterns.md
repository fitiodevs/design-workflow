# Before/after copy patterns by category

Reference library for `/pena` (`/ux-writing`) Step 4 (report assembly). Each section gives the pattern + ✅ examples + ❌ counter-examples in pt-BR. Adapt to your project's `docs/product.md` §4.

## Títulos de página (root tabs)
- Noun phrase, sentence case, sem pontuação final.
- ✅ "Corridas", "Extrato", "Cupons" — ❌ "Suas corridas", "Histórico de atividades"

## Títulos de seção
- Sentence case. Específico ao conteúdo.
- ✅ "Extrato", "Em destaque" — ❌ "Suas atividades recentes", "Confira também"

## CTAs primários
- Imperativo + objeto quando não óbvio. 1–4 palavras.
- ✅ "Resgatar", "Iniciar corrida", "Ver cupom" — ❌ "Clique aqui", "OK", "Continuar"

## Erros inline (validação)
- `[Campo] [requisito específico]`. Sem "Por favor".
- ✅ "Senha precisa ter 8 caracteres" — ❌ "Por favor, insira uma senha válida"

## Erros sistêmicos (snackbar/modal)
- `[O que falhou]. [Por quê, se conhecido]. [O que fazer].`
- ✅ "GPS impreciso. Aguarde 30s em área aberta." — ❌ "Algo deu errado, tente novamente"

## Mensagens de sucesso
- Passado + resultado concreto. Breve.
- ✅ "Check-in feito. +100 pontos." — ❌ "Parabéns! Seu check-in foi registrado com sucesso!"

## Empty states
- Explica o vazio + convida à ação sem condescendência.
- ✅ "Nenhuma corrida ainda. Saia pra correr e ganhe seus primeiros pontos." — ❌ "Você não tem nenhuma atividade registrada ainda. Que tal começar agora?"

## Confirmações destrutivas
- Transparente, sem manipulação. Consequência clara.
- ✅ "Remover corrida? Isso apaga o histórico desta atividade. Não tem como desfazer." — ❌ "Tem certeza que deseja excluir?"

## Placeholders
- Só para inputs com formato específico (email, CPF). Nunca como substituto de label.
- ✅ `hint: 'nome@exemplo.com'` — ❌ `hint: 'Digite seu e-mail aqui'`

## Tom por estado emocional do usuário

Não é intuição — é protocolo:

| Estado | Contexto típico | Tom | Exemplo |
|---|---|---|---|
| **Rotina** (recorrente) | Check-in, abrir app | Eficiente, zero coaching | "+100 pontos." |
| **Conquista** | Cupom desbloqueado, meta batida | Direto, número em destaque | "Cupom Whey desbloqueado. 3.000 pontos." |
| **Erro recuperável** | GPS falhou, conexão caiu | Calmo, solução no mesmo texto | "GPS impreciso. Tente em área aberta." |
| **Erro bloqueante** | Sessão expirada, plano cancelado | Sério, transparente, saída clara | "Acesso expirado. Renove o plano pra continuar." |
| **Iniciante** (semana 1) | Onboarding, first empty state | Convidativo, sem jargão técnico | "Nenhuma corrida ainda. Saia pra correr e ganhe seus primeiros pontos." |
| **Ação destrutiva** | Delete conta, cancelar corrida | Neutro, consequência clara | "Apagar corrida? O histórico desta atividade é removido permanentemente." |
