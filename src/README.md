# Pacote `src`: Módulos de Código-Fonte

Este diretório contém toda a lógica computacional do projeto, dividida em subpacotes temáticos:

---

## Estrutura de Subpacotes

| Subpacote | Descrição |
| :--- | :--- |
| [`core/`](core/) | Estruturas algébricas em $\mathbb{Z}[i]$ e $\mathbb{Z}[\zeta_3]$, cálculo das funções $\wp$ e $\wp'$ de Weierstrass, classificação das 9 famílias e invariância $\Gamma$. |
| [`kinematics/`](kinematics/) | Cinemática de dobras de papel, simulação de camadas segundo condições de Justin, busca de componentes de flexão e paridades. |
| [`visualization/`](visualization/) | Motor de **Coloração de Domínio (Domain Coloring)** (HSV suave, cores sólidas, pullback conforme de imagens $w \to I(u,v)$, estilo Wegert) e geradores de gráficos. |
| [`fabrication/`](fabrication/) | Geração de pranchas para impressão gráfica com sangrias, marcas de registro vetoriais e montagem de redes de tetraflexágonos e hexaflexágonos. |
| [`catalog/`](catalog/) | Geradores automatizados e certificados dos catálogos sistemáticos de funções para flexágonos. |

---

## Importação e Uso

Todos os submódulos podem ser importados a partir do diretório raiz:

```python
from src.visualization.domain_coloring import DomainColoringEngine, PALETTE_SOLID_6
from src.core.zclass import ZClass
from src.fabrication.flexagon_domain_faces import gerar_planificacao_tetraflexagono
```
