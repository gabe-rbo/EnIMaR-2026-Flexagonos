# Subpacote `src/catalog`: Geradores de Catálogos de Funções

Este módulo automatiza a catalogação sistemática e certificada das soluções de funções complexas flexionáveis.

---

## Arquivos e Responsabilidades

- **`catalogo.py`**: Montador dos catálogos para tetraflexágonos (tri-tetra e hexa-tetra). Gera as pastas com cada função `NNN/`, contendo `faceK.png`, `mecanica.png` (diagrama de flexão) e compilação de `catalogo.pdf`.
- **`catalogo_hex.py`**: Montador dos catálogos para hexaflexágonos (tri-hexa e hexa-hexa), garantindo a formatação adequada de fórmulas e retratos de fase.

---

## Execução

```bash
# Gerar catálogo do tri-tetraflexágono
python src/catalog/catalogo.py --flexagono tri -n 12

# Gerar catálogo do hexa-tetraflexágono
python src/catalog/catalogo.py --flexagono hexa -n 8

# Gerar catálogo de hexaflexágonos
python src/catalog/catalogo_hex.py 12 900
```
