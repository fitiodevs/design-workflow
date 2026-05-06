# Nielsen 10 heuristics — scoring rubric (0–4)

Used in Step 4 (report assembly) of `/theme-critique`. Each heuristic gets one integer score 0–4. Total /40 maps to a recommendation band.

## Bandas de recomendação

- **36–40 ship** — Pode mergear. Polish opcional.
- **28–35 polish** — Mergeável após 1 round de ajustes.
- **20–27 needs work** — Não merge ainda; lista P0/P1 deve fechar antes.
- **<20 redesign** — Voltar pro Figma / `/theme-port` re-run.

> Júri scoring discipline: score 4 é raro como score 0. **Maioria das telas vive em 20–32**. Não dar score 3+ por default. Bandas existem pra ser usadas.

## As 10 heurísticas + critério de scoring

### 1. Visibility of System Status
- **0** — Sem feedback de loading, erro ou estado em ações críticas.
- **2** — Feedback existe mas atrasado/genérico (ex: spinner sem contexto).
- **4** — Cada ação tem feedback imediato e específico (loading state, success snackbar, error message com causa).

### 2. Match System / Real World
- **0** — Jargão técnico ou termos do backend vazando ("session_id failed", "auth_state").
- **2** — Maioria pt-BR mas com 1-2 termos técnicos.
- **4** — Linguagem da audiência. Zero jargão. Convenções do domínio (ex: "check-in" se a audiência usa).

### 3. User Control & Freedom
- **0** — Sem undo, sem cancel, sem back. Ação destrutiva sem confirmação.
- **2** — Algumas ações têm escape; ações destrutivas confirmam mas sem possibilidade de undo.
- **4** — Toda ação destrutiva confirma + descreve consequência. Cancel sempre disponível. Undo onde possível.

### 4. Consistency & Standards
- **0** — Mesmo conceito nomeado de 3 formas diferentes; CTAs com convenções inconsistentes entre telas.
- **2** — Algumas inconsistências menores (terminologia, ícones).
- **4** — Convenções estáveis em todo o app. Mesmo verbo pra mesma ação.

### 5. Error Prevention
- **0** — Validação só no submit; usuário descobre erro depois de digitar tudo.
- **2** — Validação inline existe mas só em alguns campos.
- **4** — Validação inline em tempo real. Limites/restrições visíveis antes da ação. Confirm modals em destrutivas.

### 6. Recognition over Recall
- **0** — Usuário precisa lembrar valor de tela anterior; sem auto-complete; sem labels persistentes.
- **2** — Algumas pistas visuais; auto-complete em alguns inputs.
- **4** — Tudo visível ou recuperável de 1 tap. Auto-complete onde aplicável. Labels persistem (não somem ao digitar).

### 7. Flexibility & Efficiency
- **0** — Sem atalhos, sem batch actions, sem favoritos/recentes.
- **2** — Existe progressive disclosure mas iniciante e expert seguem mesmo caminho.
- **4** — Iniciante tem caminho guiado; expert tem atalhos (search, recents, favorites, batch).

### 8. Aesthetic & Minimalist
- **0** — Tela carregada (>4 opções por decisão); cards aninhados; cor sem hierarquia; AI-slop visual.
- **2** — Hierarquia presente mas com ruído; alguns elementos não earned its pixel.
- **4** — Cada elemento tem propósito. Hierarquia clara em <1s. Color commitment axis decidido e respeitado.

### 9. Error Recovery
- **0** — Erros sem solução. "Algo deu errado, tente novamente."
- **2** — Erros descrevem o problema mas não a solução.
- **4** — Erro = problema + causa + ação de recovery. Linguagem humana, sem código de erro cru.

### 10. Help & Documentation
- **0** — Sem help inline; sem tooltips; sem links para docs em features complexas.
- **2** — Help existe mas escondido em menu raro.
- **4** — Help contextual (tooltip, "?" inline, empty state guia). Ajuda chega quando o usuário precisa, não num menu separado.

## Severidade de issues (P0–P3)

- **P0** — Bloqueia tarefa primária. Não pode shippar.
- **P1** — Causa dificuldade significativa. Polish antes de shippar.
- **P2** — Anoyance com workaround. Backlog.
- **P3** — Polish puro. Nice-to-have.

## Cognitive load threshold

>4 opções visíveis em ponto de decisão = flag (Step 5 do critique).

## Naming convention

- Heurísticas Nielsen: nomes oficiais em inglês, **não traduzir** no relatório (convenção UX).
- Roteamento de fix → skill seguinte: P0 estrutural → `/theme-port`; cor blanda → `/theme-bolder`; cor agressiva → `/theme-quieter`; carregada → `/theme-distill`; WCAG fail → `/theme-extend`; palette inteira ruim → `/theme-create`.
