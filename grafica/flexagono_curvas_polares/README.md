# Flexágono de Gráficos de Curvas Polares (Opção nº 5 Selecionada)

Este flexágono foi gerado a partir de equações matemáticas em **coordenadas polares $(r, \theta)$**, explorando simetrias rotacionais, pétalas e harmônicos que se articulam e combinam durante os ciclos de dobra do flexágono.

Esta é a **Opção nº 5** recomendada pela Profa. Aniura Milanés Barrientos para o orçamento de impressão gráfica e oficinas do EnIMaR 2026.

---

## 📐 As 6 Equações Polares Utilizadas

| Face | Nome da Curva | Equação Polar $r(\theta)$ | Domínio Angular $\theta$ | Cor do Fundo e Traço |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Curva da Borboleta (Temple Fay)** | $r = \frac{e^{\sin\theta} - 2\cos(4\theta) + \sin^5\left(\frac{2\theta - \pi}{24}\right)}{2.3}$ | $\theta \in [0, 24\pi]$ | Azul Dodger / Branco |
| **2** | **Curva Estrela Harmônica** | $r = \sin^2(1.2\theta) + \cos^3(6\theta)$ | $\theta \in [0, 10\pi]$ | Magenta / Lavanda |
| **3** | **Rosácea de Três Pétalas ($C_3$)** | $r = 2\cos(3\theta)$ | $\theta \in [0, \pi]$ | Azul Royal / Branco |
| **4** | **Rosácea de Quatro Pétalas ($C_4$)** | $r = 2\sin(2\theta)$ | $\theta \in [0, 2\pi]$ | Verde Esmeralda / Branco |
| **5** | **Flor de Lótus Polar** | $r = \sin(\theta) + \sin^3\left(\frac{5\theta}{2}\right)$ | $\theta \in [0, 4\pi]$ | Azul Céu / Branco |
| **6** | **Rosácea Fracionária Harmônica** | $r = 2\cos\left(\frac{6\theta}{5}\right)$ | $\theta \in [0, 10\pi]$ | Verde Mar / Branco |

---

## 🔄 Cinemática e Ciclos de Dobra

O arquivo [`dinamica_flexa.png`](dinamica_flexa.png) ilustra o **diagrama de Tuckerman** e o grafo de transições entre os estados dobrados, mostrando como cada curva polar é decomposta em quatro quadrantes triangulares e recombinada a cada flexão (*pinch flex*).

---

## 🖨️ Arquivos Gráficos na Pasta

- **Grade Geral de Referência:** [`flexagono_grade_n6.png`](flexagono_grade_n6.png)
- **Mosaico 2×3:** [`flexagono_grade_2x3.png`](flexagono_grade_2x3.png)
- **Grafo da Dinâmica de Dobra:** [`dinamica_flexa.png`](dinamica_flexa.png)
- **Faces Individuais:** Na pasta [`faces/`](faces/): arquivos `flexagono_Face_1_n6.png` até `flexagono_Face_6_n6.png`.

---

## 📓 Caderno Jupyter de Origem
As curvas e parametrizações foram desenvolvidas no caderno interativo:
[`pesquisa/notebooks/imagens_curvas_polares.ipynb`](../../pesquisa/notebooks/imagens_curvas_polares.ipynb).
