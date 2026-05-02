# Anti-AI-slop checklist + inspirational palette reference

Use this as the Step 7 + closing reference of `/theme-create`. Run the checklist before commit; consult the inspiration table for hue starting points by mood.

## Checklist final (Step 7 of the SKILL)

Antes de commitar a palette, passar por todos os checks:

### Cor
- [ ] NÃO é purple+blue gradient padrão (`#6366F1` → `#8B5CF6`).
- [ ] NÃO é orange+teal (`#F97316` + `#14B8A6`).
- [ ] NÃO usa defaults do Tailwind/Material direto sem modificação.
- [ ] Inspiração rastreável a algo real (brand existente, fotografia, cultura específica).
- [ ] Tem pelo menos UMA cor "inesperada" que distingue do domínio padrão.
- [ ] Saturação varia entre roles (não todos high-sat, não todos muted).
- [ ] `bgBase` não é `#FFFFFF` puro nem `#000000` puro.
- [ ] Dark mode tem personalidade — não é só inversão de light.
- [ ] Distribuição é dominante+accent, não evenly-distributed.

### Tipografia (caso a palette inclua proposta de fonte)
- [ ] NÃO é Inter, Roboto, Arial, Helvetica, Space Grotesk, ou system-ui como fonte principal.
- [ ] Display font tem caráter (serif com swash, geometric com idiossincrasia, mono opinionada).
- [ ] Body font legível em 12-16px no dispositivo (não só em desktop).
- [ ] `fontFamilyFallback` declarado (cobre quando a fonte custom não carrega).

### Execução
- [ ] Implementação combina com a tone declarada (minimal não tem 9 cores, maximalist não tem 3).
- [ ] Differentiation declarada no Step 0 está visualmente expressa em pelo menos 1 token.

## docs/themes ficha template

Para cada palette criada em `/theme-create`, gerar `docs/themes/<theme-name>.md` no formato:

```markdown
# <Theme Name>

<Uma frase de descrição evocativa — 10-20 palavras.>

## Color Palette (light)

- **<Token role>** (`<TokenName>`): `#XXXXXX` — <papel em uma frase>
- **<Token role>**: `#XXXXXX` — <papel>
- **<Accent>**: `#XXXXXX` — <papel>
- **<Background>**: `#XXXXXX` — <papel>

## Color Palette (dark)

- **<mesma estrutura, hexes do dark>**

## Typography

- **Headers**: <font + fallback>
- **Body**: <font + fallback>

## Best Used For

<Frase descrevendo contextos onde esse tema brilha — ex: "Sub-brand competitivo, eventos branded, telas de leaderboard com energia visual alta.">

## Anti-patterns evitados

- <O que esse tema explicitamente NÃO faz — ex: "Não usa purple-on-white nem Inter, evitando tech-SaaS genérico.">

## Inspiração

<Referência rastreável real — ex: "Sinalização de pista de atletismo (lane lines amarelas + concrete cinza)", "Capa do álbum X de Y", "Bandeira de Z".>
```

Esse formato é navegável (vira tabela de conteúdo de `docs/themes/index.md`) e força documentação anti-slop (campos "Anti-patterns evitados" e "Inspiração" são obrigatórios).

## Inspirational palettes by mood (domain-agnostic — do NOT copy literally)

Use these as a starting point for hue exploration. **Name the result after its character, not the hue.**

| Mood | Hue dominante | Saturação | Exemplo de aplicação |
|------|---------------|-----------|---------|
| Energia / competição | 350-20 (vermelho/coral) ou 55-75 (amarelo) | Alta | Arena, corrida, duelo |
| Confiança / serenidade | 200-250 (azul) | Média | Healthcare, finance |
| Sofisticação / premium | 270-310 (roxo/magenta) ou neutros | Baixa | Luxo, assinatura |
| Natureza / saudável | 120-160 (verde) | Média-alta | Nutrição, bem-estar |
| Warmth / comunidade | 20-50 (laranja/âmbar) | Média | Social, indicação |
| Tech edge | 180-220 (ciano/azul) com dark base | Alta | Dev tools, power users |
| Editorial / printed | 0 + 1 saturated jewel | Baixa-média | Long-form, magazine |
| Brutalist / signage | 60 (yellow) + 0 (black) + concrete | Extrema | Industrial, hi-vis |
