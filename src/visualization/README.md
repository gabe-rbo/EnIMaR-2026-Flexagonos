# Subpacote `src/visualization`: Motor de Coloração de Domínio e Gráficos

Este módulo implementa o motor avançado de **Coloração de Domínio (Domain Coloring)** e a renderização de gráficos complexos.

---

## Arquivos e Responsabilidades

- **`domain_coloring.py`**: Motor unificado de coloração de domínio de funções complexas:
  - *HSV Contínuo:* Matiz por argumento $\arg(w)$, modulação suave de brilho e destaque de singularidades.
  - *Cores Sólidas:* Discretização em $N$ setores angulares planos (6, 12, 4 cores) sem gradientes contínuos.
  - *Xadrez Polar:* Ladrilhamento em setores e anéis concêntricos de $\log|w|$ com cores contrastantes.
  - *Pullback Conforme de Imagem:* Projeção de texturas arbitrárias do plano $w$ de volta no plano $z$ via $f^*(I)(z) = I(f(z))$ com modos `wrap`, `mirror`, `clamp` e `constant`.
  - *Estilo Elias Wegert:* Linhas de nível isomodulares e raios de fase por funções dente-de-serra (*sawtooth*).
- **`figuras.py`**: Gerador das 12 figuras geométricas e diagramas do artigo para compilação em LaTeX.
- **`diagrama.py` & `diag.py`**: Renderizador do diagrama de flexão com os retratos de fase encaixados.

---

## Exemplo de Uso Rápido

```python
from src.visualization.domain_coloring import DomainColoringEngine, PALETTE_SOLID_6

def f(z):
    return (z - 1) / (z**2 + z + 1)

engine = DomainColoringEngine(func=f, x_range=(-2, 2), y_range=(-2, 2))

# 1. Cores Sólidas (6 setores)
img_solida = engine.render(mode='solid_sectors', n_sectors=6)

# 2. Pullback de Imagem do plano w
img_pullback = engine.render(mode='custom_image', texture="caminho/textura.png", border_mode='wrap')

# 3. Conjunto das 6 faces coordenadas
faces = engine.generate_six_flexagon_faces()
```
