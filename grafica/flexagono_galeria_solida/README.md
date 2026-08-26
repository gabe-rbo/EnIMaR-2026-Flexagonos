# Flexágono Galeria Matemática de Cores Sólidas (6 Funções e Geometrias Heterogêneas)

Neste flexágono, **cada uma das 6 faces é um objeto matemático e padrão geométrico completamente diferente**, renderizado em **Cores Sólidas e 4K UHD** ($3840 \times 3840$ px).

---

## 📐 As 6 Funções e suas Geometrias

```
+---------------------------------------------------------------------------------------------------+
|  FACE 1: Raízes da Unidade   |  FACE 2: Exponencial Wegert   |  FACE 3: Labirinto de Truchet      |
|  f₁(z) = z⁶ - 1              |  f₂(z) = exp(z) - 1           |  f₃(z) = (z² - 1)/(z² + 1)         |
|  [6 Setores Angulares Puros] |  [Grade Cartesiana Ortogonal] |  [Mosaico de Arcos de Truchet]     |
|------------------------------+-------------------------------+------------------------------------|
|  FACE 4: Joukowsky Aerofólio |  FACE 5: Triplo Polo          |  FACE 6: Quadrupolo Hexagonal      |
|  f₄(z) = 0.5 · (z + 1/z)     |  f₅(z) = (z³ - 1)/(z³ + 1)    |  f₆(z) = (z⁴ + 1)/(z⁴ - 1)         |
|  [Tabuleiro de Xadrez]       |  [Alvos Concêntricos (10 An.)]|  [Favos de Mel Hexagonais]         |
+---------------------------------------------------------------------------------------------------+
```

---

### Detalhamento Matemático Face a Face

### 🔹 Face 1: Estrela Floral de Raízes da Unidade
- **Função:** $f_1(z) = z^6 - 1$
- **Zeros:** $z_k = e^{i k \pi / 3}$ para $k = 0, 1, 2, 3, 4, 5$ (6 zeros simples no círculo unitário).
- **Estilo:** **6 Setores Angulares Sólidos** (Vermelho, Amarelo, Verde, Ciano, Azul, Magenta).
- **Aspecto Visual:** Uma estrela floral de 6 pétalas perfeitamente simétricas convergindo no centro.

---

### 🔹 Face 2: Espirais Periódicas de Faixas Conformes
- **Função:** $f_2(z) = \exp(z) - 1$
- **Zeros:** $z_k = 2k\pi i$ ($k \in \mathbb{Z}$, zeros simples periódicos no eixo imaginário).
- **Estilo:** **Grade Cartesiana Ortogonal no plano $w$ (Pullback)**.
- **Aspecto Visual:** Ondulações periódicas infinitas de faixas horizontais conformes (Teorema 2.4 de Wegert), com os eixos coordenados em vermelho.

---

### 🔹 Face 3: Labirinto Conforme de Truchet
- **Função:** $f_3(z) = \frac{z^2 - 1}{z^2 + 1}$
- **Zeros:** $z = \pm 1$ (no eixo real).
- **Polos:** $z = \pm i$ (no eixo imaginário).
- **Estilo:** **Mosaico de Arcos de Truchet no plano $w$ (Pullback)**.
- **Aspecto Visual:** Um labirinto contínuo de arcos e rosetas azuis que fluem e conectam os polos aos zeros ortogonais.

---

### 🔹 Face 4: Transformação de Aerofólio de Joukowsky
- **Função:** $f_4(z) = \frac{1}{2}\left(z + \frac{1}{z}\right)$
- **Pontos Críticos / Ramificações:** $z = \pm 1$ onde $f'(\pm 1) = 0$.
- **Polos:** $z = 0$ (polo simples).
- **Estilo:** **Tabuleiro de Xadrez Cartesiano de Alto Contraste (Pullback)**.
- **Aspecto Visual:** O tabuleiro de xadrez dobra-se em lâminas aerodinâmicas hiperbólicas clássicas da hidrodinâmica conforme.

---

### 🔹 Face 5: Alvo Conforme de Triplo Polo
- **Função:** $f_5(z) = \frac{z^3 - 1}{z^3 + 1}$
- **Zeros:** $z = 1, e^{i 2\pi/3}, e^{-i 2\pi/3}$ (3 zeros de ordem 1).
- **Polos:** $z = -1, e^{i \pi/3}, e^{-i \pi/3}$ (3 polos de ordem 1).
- **Estilo:** **Alvos de 10 Anéis Concêntricos em Cores Sólidas (Pullback)**.
- **Aspecto Visual:** 3 fontes de anéis concêntricos nos zeros e 3 ilhas concêntricas nos polos em simetria de ordem 3.

---

### 🔹 Face 6: Quadrupolo em Tesselação de Favos de Mel
- **Função:** $f_6(z) = \frac{z^4 + 1}{z^4 - 1}$
- **Zeros:** $z = e^{i (2k+1)\pi/4}$ para $k = 0, 1, 2, 3$ (4 raízes quárticas nos vértices do quadrado girado).
- **Polos:** $z = \pm 1, \pm i$ (4 polos nos eixos coordenados).
- **Estilo:** **Tesselação de Favos de Mel Hexagonais Multicoloridos (Pullback)**.
- **Aspecto Visual:** Uma colmeia hexagonal colorida que se comprime e gira em 4 vórtices nos vértices do quadrado unitário.

---

## 🖨️ Arquivos Prontos para a Gráfica (4K UHD)

- **Painel Comparativo 2×3:** [`painel_6_faces_galeria.png`](painel_6_faces_galeria.png)
- **Plano Frontal (Frente 4840×4840 px):** [`Plano_Frontal_GaleriaSolida.png`](Plano_Frontal_GaleriaSolida.png)
- **Plano Traseiro (Verso 4840×4840 px):** [`Plano_Traseiro_GaleriaSolida.png`](Plano_Traseiro_GaleriaSolida.png)
- **Faces Individuais 4K UHD (3840×3840 px):** Em [`faces/`](faces/): `face1.png` até `face6.png`.

---

## 🛠️ Script de Regeneração
```bash
python src/fabrication/gerar_flexagono_galeria_solida.py
```
