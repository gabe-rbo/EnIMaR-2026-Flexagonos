# Subpacote `src/core`: Álgebra, Invariância e Funções Especiais

Este módulo implementa a fundamentação matemática exata das **funções complexas flexionáveis**.

---

## Arquivos e Responsabilidades

- **`zclass.py`**: Aritmética exata nos anéis de inteiros quadráticos $\mathbb{Z}[i]$ (quadrados) e $\mathbb{Z}[\zeta_3]$ (triângulos). Estruturação do grupo $\Gamma$ e das 9 classes de Hauptmodul.
- **`wp.py` & `wpgen.py`**: Avaliação de alta precisão das funções elípticas de Weierstrass $\wp(z)$ e $\wp'(z)$ através de funções teta de Jacobi sobre reticulados arbitrários.
- **`gerador.py`**: Gerador certificado da família completa de funções complexas flexionáveis.
- **`reticulados.py`**: Os 86 reticulados planos e suas 4 classes de homotetia.
- **`wgrupo.py`**: Cálculo do grupo $W^+(D)$ gerado pelas reflexões em retas de dobra admissíveis para polióminos e poliamantes.
- **`multiproto.py`**: Análise de faces com múltiplos protótipos (incluindo o caso denso e realização de $C_{12}$).
- **`flexgeral.py`**: Teoria geral de ladrilhamentos, grupos de flexes e censo combinatório.
- **`quadflex.py`**: Implementação e enumeração dos 6.144 flexes quadrados.
