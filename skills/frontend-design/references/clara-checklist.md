# Clara auto-revision checklist

Used in Step 7 of `/frontend-design`. Clara walks every item before delivering. If 1 item fails, fix it before handing off — "almost" doesn't pass.

```yaml
revisão_clara:
  spacing:
    - todos os gaps em escala (2, 4, 8, 12, 16, 20, 24, 32, 48)?
    - vertical rhythm: 1 unidade base, múltiplos consistentes?
    - respiro suficiente entre seções (≥16px)?

  hierarquia:
    - âncora visual identificável em <1s?
    - ratio adjacente ≥1.25× entre roles tipográficos?
    - peso de fonte progride monotonicamente (não pulando)?

  alinhamento:
    - elementos em grid alinhados ao mesmo eixo (pixel-perfect)?
    - baseline de textos vizinhos coincide?
    - CTA primário em posição previsível (geralmente bottom-fixed em mobile)?

  copy:
    - zero banidos absolutos do product.md §4.2?
    - imperativo direto em CTAs (não gerúndio)?
    - números antes de palavras quando há quantidade?
    - sem placeholder genérico ("João Silva", "Lorem ipsum", "Acme")?

  cor:
    - axis declarado (Restrained / Committed / Full / Drenched)?
    - accent ratio respeita o axis (≤10% em Restrained)?
    - feedback semantic (success/error) usa cor própria, não brand?

  motion (se aplicável):
    - cada animação tem causalidade?
    - asymmetric enter/exit (entrada lenta, saída rápida)?
    - sem bounce/elastic em UI funcional?
    - comentário `<!-- motion: ... -->` por intenção?

  tweaks-ready emission (v1.4+ contract — todos os 5 são obrigatórios):
    - todas as cores via `var(--<role>)`, sem hex literal fora do bloco `:root`?
    - todo spacing via `calc(var(--space-unit) * N)`, sem `px` literal fora de width/height estruturais?
    - toda `font-size` derivada de `--scale` via 7-step ladder no `:root` (`--text-display..--text-caption`)?
    - todo `<section>` major tem `data-od-id="<role>"` em kebab-case?
    - dark mode emitido como bloco `:root[data-mode="dark"] { ... }` separado dos defaults light?
```

## Anti-patterns que Clara corta sem dó

- Cards 3-em-linha idênticos por reflexo SaaS → quebrar ritmo (variar largura, ordem, peso visual)
- Hero-metric template (número grande + label pequeno + 3 supporting stats lado-a-lado) → category-reflex
- Avatar grande + nome no topo "olá Maria" → ruído passivo, ocupa primeira dobra sem ação
- Botão fantasma com label "Saiba mais" → sem hierarquia de comando, copy preguiçoso
- Gradient roxo→rosa em fundo branco → AI-slop universal
- Padding 14px ou 18px → quebra escala (forçar 12 ou 16)
- Letter-spacing 0 em texto uppercase → vira massa visual, prescrever 1–2px
- "Bem-vindo" como copy → vocativo morno, banido por `docs/product.md §4.3`
