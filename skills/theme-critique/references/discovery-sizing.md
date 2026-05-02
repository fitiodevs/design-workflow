# Discovery — auto-sizing

> Reference loaded by `theme-critique` (Júri) in **discovery mode** to decide tier and deliverables.
> Sized by `scripts/detect_mode.py` + optional `--mode` override.

## Output of `detect_mode.py`

```json
{
  "mode": "greenfield" | "brownfield",
  "tier_recommended": "greenfield" | "full",
  "signals": {
    "commits": <int>,
    "dart_files": <int>,
    "has_product_md": <bool>,
    "has_theme_dir": <bool>
  },
  "repo_root": "<absolute path>"
}
```

`mode` é descritivo (greenfield vs brownfield); `tier_recommended` é prescritivo (qual tier rodar).

## Tier × deliverables

| Tier         | discovery.md     | PRD              | docs skeletons                                                | Brownfield pre-scan |
|--------------|------------------|------------------|---------------------------------------------------------------|---------------------|
| `quick`      | mini (3 perguntas — só Produto block) | não | não | não |
| `light`      | completo (4 blocos) | curto (1 página) | não | só se brownfield (não bloquear) |
| `full`       | completo            | completo (top 3-5 fixes) | append a docs existentes; não cria do zero | sim, se brownfield |
| `greenfield` | completo            | completo                  | cria 4 skeletons (`product.md`, `design.md`, `design-tokens.md`, `PRD.md`) | n/a |

## Override semantics

`/juri --mode <tier>` força o tier escolhido independentemente do `tier_recommended`.

- Override é honrado sempre — usuário sabe melhor que heurística em casos de borda.
- Se `--mode` discrepa de `tier_recommended` em mais de 1 nível (ex: detect=greenfield mas user pede `quick`), Júri loga 1 warning curto antes de prosseguir: *"Detectei greenfield. Você pediu quick — confirmando? (sim/não)"*.

## Decision tree (sem override)

```
detect_mode.py output:
├── mode == greenfield → tier = greenfield
└── mode == brownfield
    ├── signals.has_product_md == true AND has_theme_dir == true → tier = full
    ├── signals.has_product_md == true AND has_theme_dir == false → tier = full (avisa: tema ausente)
    └── signals.has_product_md == false                            → tier = full (avisa: docs/product.md ausente — Júri vai gerar skeleton appendado)
```

`quick` e `light` nunca são escolhidos por detecção — só via override explícito do usuário.

## Quando o usuário pede `--mode quick`

- Pula blocos Tom + Identidade + Stack.
- Faz só Bloco 1 (Produto, 3 perguntas).
- Output: `discovery.md` mini + plan top-3 (não top-N).
- Sem skeletons, sem PRD, sem pre-scan.
- Use case típico: já existe entendimento sólido, usuário só quer roteamento priorizado das próximas 3 ações.

## Quando o usuário pede `--mode light`

- 4 blocos completos mas só 2 perguntas/bloco (em vez de 3) — versão enxuta.
- PRD curto (1 página, top 3 fixes).
- Sem skeletons.
- Pre-scan rodado se brownfield (mas resultado entra appendado em `discovery.md`, não em PRD).

## Anti-patterns

- ❌ Rodar tier `greenfield` em repo brownfield — sobrescreve `docs/product.md` real. Júri sempre confirma antes (ver REQ-A5.5).
- ❌ Ignorar override do usuário em favor de detecção. Override vence.
- ❌ Mudar tier no meio da entrevista. Tier é decidido no início e mantido até o fim.
