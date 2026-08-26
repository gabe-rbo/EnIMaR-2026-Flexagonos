# Flexágono de Cores Sólidas e Padrões Geométricos (Mesma Função, 6 Lentes Sólidas)

Neste flexágono, a mesma função complexa modelo $f(z) = \frac{z-1}{z^2+z+1}$ é renderizada através de **6 esquemas puramente em Cores Sólidas, Discretização e Padrões Geométricos (*Pullback Conforme*)**, sem nenhum gradiente contínuo.

---

## 📐 Função Complexa Avaliada

$$f(z) = \frac{z - 1}{z^2 + z + 1}$$

- **Zero:** $z = 1$ (ordem 1).
- **Polos:** $z = e^{\pm i 2\pi/3} = -\frac{1}{2} \pm i\frac{\sqrt{3}}{2}$ (ordem 1).
- **Domínio no Plano $z$:** $x \in [-2.2, 2.2]$, $y \in [-2.2, 2.2]$ ($3840 \times 3840$ px, 4K UHD).
- **Domínio da Textura no Plano $w$:** $u \in [-2.5, 2.5]$, $v \in [-2.5, 2.5]$.

---

## 🎨 As 6 Faces em Cores Sólidas

| Face | Nome do Esquema | Padrão Geométrico no Plano $w$ | Propriedade Visual / Teórica |
| :---: | :--- | :--- | :--- |
| **1** | **6 Setores Angulares Puros** | Discretização de $\arg(w)$ em setores de $60^\circ$ | 6 cores sólidas (Vermelho, Amarelo, Verde, Ciano, Azul, Magenta) convergindo no zero e nos polos sem gradientes |
| **2** | **Grade Cartesiana Ortogonal** | Malha quadrada regular com eixos $u=0, v=0$ destacados | Deformação ortogonal conforme, preservando ângulos retos locais nas interseções de linhas |
| **3** | **Tabuleiro de Xadrez Conforme** | Ladrilhamento em xadrez cartesiano bicolor (alto contraste) | Quadrados pretos e brancos sólidos que se deformam em curvas conformes hiperbólicas |
| **4** | **Xadrez Polar Sólido** | 12 setores angulares $\times$ anéis logarítmicos $\log|w|$ | Ladrilhamento polar alternado com paridade de cores (preto e branco sólido) |
| **5** | **Alvos Concêntricos Sólidos** | 8 anéis concêntricos coloridos $r_k \le |w| < r_{k+1}$ | Curvas de nível de magnitude $|f(z)| = \text{const}$ em faixas de cores sólidas puras |
| **6** | **Mosaico de Arcos de Truchet** | Mosaico de arcos circulares e rosetas de Truchet | Linhas sólidas de Truchet conectando-se em nós e laços contínuos sobre o plano conforme |

---

## 🖨️ Arquivos Prontos para Impressão Gráfica (4K UHD)

- **Painel Comparativo 2×3:** [`painel_6_faces_cores_solidas.png`](painel_6_faces_cores_solidas.png)
- **Plano Frontal (Frente 4840×4840 px):** [`Plano_Frontal_CoresSolidas.png`](Plano_Frontal_CoresSolidas.png)
- **Plano Traseiro (Verso 4840×4840 px):** [`Plano_Traseiro_CoresSolidas.png`](Plano_Traseiro_CoresSolidas.png)
- **Faces Individuais 4K UHD (3840×3840 px):** Em [`faces/`](faces/): `face1.png` até `face6.png`.

---

## 🛠️ Script de Regeneração
```bash
python src/fabrication/gerar_flexagono_cores_solidas.py
```
