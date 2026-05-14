# Tools

Skills que você invoca diretamente:

- `/sequence` — decompõe `compose.md` aprovado em `tasks.md` atômico
- `/ship` — executa `tasks.md` aprovado task-a-task, commit por task
- `/ship --interactive` — confirma cada task com usuário antes de commitar
- `/theme-port` — porta Figma frame para widget Flutter
- `/theme-port --from-html <path>` — porta HTML mockup para widget Flutter
- `/opusexecute` — dispatcha worker Sonnet em background para tarefa mecânica longa
- `/ralph-loop` — loop autônomo de manutenção de design-system (tiers: watch / mechanical / composer)
- `/ralph watch|mechanical|composer` — atalho de tier específico

Comandos shell que você confia para verify:

- `pnpm test` / `flutter test` — suite de testes
- `dart analyze` / `flutter analyze` — static check
- `pnpm -r typecheck` — typecheck cross-package
- `pnpm build` — build produção
- `git diff --stat HEAD~1` — confirmar escopo do commit

Skills que você **não invoca** (delega):

- Mockup novo / palette / motion / densidade → Clara
- Crítica Nielsen / audit / WCAG → Júri
- Fluxo / IA / jornada → Flow
- Copy / microcópia → Pena
- Aprovar phase / save sessão / promote backlog → Atlas

(Adicione notas conforme acumula flags e edge cases.)
