---
name: clickup-sync
description: Sincroniza `.specs/features/<feature>/` com ClickUp (lista Developer Agent, id 901113393648). Cada feature vira task pai com subtasks por T-NN, status flui local→ClickUp via hook PostToolUse. Triggers `/sync-clickup`, "sync clickup", "manda spec pro clickup", "backfill specs", "spec não tá no clickup". Skip pra editar spec.md direto ou rodar /ship.
---

# clickup-sync — manual sync, backfill e drift check

O hook `.claude/hooks/persona-sync.sh` (bloco 3) já dispara o worker
`scripts/clickup/sync_spec.py` automaticamente sempre que o usuário salva
`spec.md` ou `tasks.md` em `.specs/features/<feature>/`. Esta skill é o
**manual override** pra casos onde o hook não rodou (após `git pull`,
backfill inicial, drift detectado, ou diagnóstico).

## Pré-condições

1. Token ClickUp em `.clickup-token` (na raiz do repo, `.gitignore` cobre) ou
   env `CLICKUP_API_TOKEN`. Sem token, worker exit 0 silencioso — não trava
   o Claude Code mas também não syncroniza.
2. Python 3 + `pyyaml` + `requests` no sistema (já disponíveis).

## Comandos

### `/sync-clickup` (default)

Detecta a feature da branch atual (procura `.specs/features/<name>/` que casa
com o nome da branch ou com o último arquivo editado em git status) e roda
sync incremental.

```bash
python3 scripts/clickup/sync_spec.py <feature>
```

### `/sync-clickup --all`

Backfill: itera **todas** as features em `.specs/features/*/` e cria/atualiza
tasks no ClickUp. Idempotente — features sem mudança ficam no-op (hash match).
Esperado em first run: 25+ tasks pai criadas, ~200 subtasks. Leva ~4min com
rate-limit.

```bash
python3 scripts/clickup/sync_spec.py --all
```

### `/sync-clickup --dry-run <feature>`

Mostra os payloads JSON que seriam POSTados, sem chamar a API. Use pra
debugar parser ou validar que título/status estão certos antes de subir
de verdade.

```bash
python3 scripts/clickup/sync_spec.py --dry-run ritmo
```

### `/sync-clickup --check`

Valida todas as specs sem tocar no ClickUp. Lista shippable vs blocked com
motivo por linha. Use antes de `--all` pra prever bloqueios. Regra de
shippable: tasks parseáveis ≥1 **e** título no frontmatter **e** descrição
narrativa ≥40 chars. Specs bloqueadas ficam só locais até serem enriquecidas.

```bash
python3 scripts/clickup/sync_spec.py --check
python3 scripts/clickup/sync_spec.py --check <feature>
```

Para forçar uma spec incompleta a subir mesmo assim (raro):
`python3 scripts/clickup/sync_spec.py --force <feature>`.

### `/sync-clickup --status`

Tabela de estado de sync por feature: `parent_task_id`, número de subtasks,
último `last_synced`. Útil pra encontrar drift ou specs nunca sincronizadas.

```bash
python3 scripts/clickup/sync_spec.py --status
```

## Quando NÃO usar

- **Pra editar spec.md ou tasks.md** → use Edit/Write direto; o hook syncroniza
  automaticamente.
- **Pra fechar um T-NN como done** → use `/ship` ou Edit no `tasks.md`; a
  mudança de status no markdown é o source-of-truth.
- **Pra criar nova feature spec** → delegue `/tlc-spec-driven` ou `/promote`.
  Esta skill só sincroniza specs existentes.

## Como interpretar o output

- `✓ <feature>` — sincronizou com mudanças.
- `· <feature>` — no-op (hash bate com estado anterior).
- `✗ <feature>: <erro>` — falhou, geralmente token inválido ou rate limit
  exaurido. Olhe `/tmp/clickup-sync-<feature>.log` pra detalhe.

## Anatomia do mapping persistido

Cada feature ganha `.specs/features/<feature>/.clickup.yml` **committado** no
git pra que todos os devs apontem pro mesmo task ClickUp:

```yaml
parent_task_id: abc123
parent_url: https://app.clickup.com/t/abc123
subtasks:
  T-01: def456
  T-02: ghi789
last_synced: 2026-05-19T14:30:00Z
content_hash: a3f5d2c1...
subtask_learnings_hash:
  T-01: 5e8a9b...
```

Não edite à mão. Se precisa resetar uma feature (recriar do zero no ClickUp),
delete o `.clickup.yml` e rode `/sync-clickup <feature>`.

## Learning capture

Quando uma T-NN vira `done`, o worker procura no último commit que tem
`Refs feature/T-id` um bloco `## Learning` no footer:

```
## Learning
- Pegou-me: <gotcha não-óbvio>
- Reusei: <path:line que poupou trabalho>
- Pra próxima: <dica concreta>
```

Se ao menos 1 chave tem conteúdo real, vira comment na subtask do ClickUp.
Vazio ou placeholder ("ok", "done", "n/a") → silencioso. Idempotente via
hash em `.clickup.yml`.
