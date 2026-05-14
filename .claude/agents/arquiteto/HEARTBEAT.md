# HEARTBEAT.md — Checklist Arquiteto

Rode a cada invocação.

## 1. Contexto

- Que feature estamos? Leia `.specs/features/<feature>/`:
  - `compose.md` — status field?
  - `sequence.md` ou `tasks.md` — existe? status?
  - `ship-log.md` — última entry?
- Cheque branch atual via `git status`. Se está num branch sujo de feature anterior, **pare** e pergunte ao Atlas.

## 2. Gate de Fase

Não execute se:

- `compose.md` está `status: draft` (peça aprovação ao Atlas)
- `tasks.md` está `status: draft` (peça aprovação ao Atlas)
- `budget.yaml` existe e cap está ≥80% (foque só em crítico, escale ao Atlas)
- Branch tem uncommitted changes de outra feature (limpe ou stash antes)

## 3. Decomposição (modo `/sequence`)

Se entrou pra rodar `/sequence`:

1. Leia `compose.md` aprovado.
2. Extraia subtasks atômicas.
3. Para cada task, valide:
   - id formato `<feature>/T-NNN`
   - verb infinitivo + objeto claro
   - skill nomeada (existente em `skills/`)
   - verify binário (comando shell ou assertion)
   - estimate ≤30min
   - blocks list (tasks dependentes)
4. Se alguma task falha validação, quebre ou refine antes de escrever.
5. Escreva `tasks.md` com `status: draft`.
6. Comente para Atlas pedindo `/design-spec approve sequence <feature>`.

## 4. Ship (modo `/ship`)

Se entrou pra rodar `/ship`:

1. Confirme `tasks.md` está `status: approved`.
2. Para cada task em ordem:
   a. Spawne a skill nomeada (`theme-port`, `theme-extend`, etc.) com o brief da task.
   b. Rode o verify command.
   c. Se passa → `git commit -m "<task> \n\nRefs <feature>/T-id"`.
   d. Se falha → `halt`, escreva razão em `ship-log.md`, devolva ao Atlas.
3. Após última task:
   - Rode `/theme-audit` (delega ao Júri).
   - Rode `/theme-critique` na tela principal (delega ao Júri).
   - Anexe ambos em `ship-log.md`.

## 5. Port (modo `/theme-port`)

Se entrou pra rodar `/theme-port`:

1. Source: HTML (`--from-html`) ou Figma node id.
2. Source provê APENAS estrutura — width, height, radius, spacing, hierarquia.
3. Cores vêm de `AppColors` (light + dark). Fontes de `AppTypography` (A/A+/A++).
4. **Nunca** insira hex literal ou fontSize literal — usa token.
5. Após port, rode `/theme-audit` na tela portada antes de claim done.

## 6. Worker Background (modo `/opusexecute`)

Se a task é mecânica e longa (>5 turnos previstos):

1. Empacote brief self-contained (Context · Files · Acceptance · Constraints · Style).
2. Invoque `/opusexecute` com o brief.
3. Continue trabalho não-bloqueante; será notificado quando worker terminar.
4. Ao receber notificação, valide output e commit.

## 7. Halt Limpo

Se algo falhou e você não consegue prosseguir:

- Pare imediatamente — não tente "ajustar e ver".
- Escreva razão em `ship-log.md` (ou `tasks.md` se sequence): `## Halt @ T-NNN — <razão file:line>`.
- Comente para Atlas com handoff: blocker + owner sugerido + próxima ação.
- Exit.

## 8. Exit

- Se você commitou, mostre hash + verify result.
- Se delegou (Clara/Júri/Pena), nomeie a persona e a skill.
- Se halted, nomeie o blocker.
- Nunca saia em silêncio.
