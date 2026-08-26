# Artigo Científico: Funções Complexas Flexionáveis

Este diretório contém o manuscrito científico completo sobre a classificação e caracterização das funções meromorfas flexionáveis.

---

## Estrutura

- **`flexagons.tex`**: Código-fonte principal em LaTeX.
- **`flexagons.pdf`**: Versão compilada do artigo (28 páginas, 26 figuras).
- **`fig/`**: Figuras geométricas, retratos de fase, mapas de retorno e diagramas de grafos gerados pelo script `src/visualization/figuras.py`.

---

## Teorema Central

Dada uma função meromorfa $f: \mathbb{C} \to \hat{\mathbb{C}}$ e um flexágono com mapa de retorno $\Phi$, $f \circ \Phi^{-1}$ permanece meromorfa se e somente se $f$ é invariante pelo grupo cristalográfico plano $\Gamma_\Phi \le W^+(D) \le C_n \ltimes \frac{1}{d}\mathcal{O}_n$.

A classificação completa estabelece 9 classes fundamentais com Hauptmodul explícito (incluindo funções elípticas $\wp$ e $\wp'$ nos casos de posto 2).

---

## Compilação

Para recompilar o artigo:
```bash
pdflatex flexagons.tex
```
