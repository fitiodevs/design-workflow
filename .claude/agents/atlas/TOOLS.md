# Tools

Skills que você invoca diretamente (não delega):

- `/status` — inspetor de estado (specs ativas, branch, uncommitted, últimos commits)
- `/atlas-save` — save de sessão curado para o próximo turno
- `/promote` — promove `docs/backlog/<f>.md` para `.specs/features/<f>/`
- `/compose` — orquestra fase compose (palette + mockup + Clara review)
- `/sequence` — orquestra fase sequence (gera `tasks.md` a partir de `compose.md` aprovado)
- `/ship` — orquestra fase ship (executa `tasks.md` aprovado task a task)
- `/design-spec pause|resume|status|approve` — controle de fase
- `/loop` — agendamento recorrente quando necessário

Skills que você **não invoca** (delega para o owner):

- Mockup/palette/tokens → Clara
- Port/decomposição/worker → Arquiteto
- Crítica/audit → Júri
- Fluxo → Flow
- Copy → Pena

(Adicione notas sobre tools à medida que adquire e usa.)
