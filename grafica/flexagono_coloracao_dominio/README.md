# Flexágono de Coloração de Domínio Clássico (Wegert, HSV e Mapeamentos Conformes)

Este flexágono explora a mesma função complexa modelo sob **6 lentes de visualização distintas**, integrando técnicas clássicas de retrato de fase contínuo, curvas de nível de Elias Wegert e *pullbacks* conformes no plano $w$.

---

## 📐 Função Complexa Modelo

A função adotada para todas as 6 faces é a função racional clássica com $1$ zero e $2$ polos:
$$f(z) = \frac{z - 1}{z^2 + z + 1}$$

### Propriedades Analíticas:
- **Zeros:** $z_0 = 1$ (simples, no eixo real positivo).
- **Polos:** $z_1 = e^{i 2\pi/3} = -\frac{1}{2} + i\frac{\sqrt{3}}{2}$ e $z_2 = e^{-i 2\pi/3} = -\frac{1}{2} - i\frac{\sqrt{3}}{2}$ (dois polos simples formando um par conjugado no círculo unitário).
- **Comportamento Assintótico:** Quando $|z| \to \infty$, $f(z) \sim \frac{1}{z} \to 0$.
- **Domínio de Avaliação:** $x \in [-2.2, 2.2]$, $y \in [-2.2, 2.2]$ com malha $4\text{K UHD}$ ($3840 \times 3840$ pontos, totalizando $14.745.600$ avaliações numéricas).

---

## 🎨 As 6 Faces de Visualização

```
+---------------------------------------------------------------------------------------------------+
|  FACE 1: HSV Contínuo        |  FACE 2: 6 Cores Sólidas      |  FACE 3: Estilo Wegert Enhanced    |
|  Matiz por arg(w) suave      |  Setores de 60° puros         |  Curvas de nível |w| e raios arg(w)|
|------------------------------+-------------------------------+------------------------------------|
|  FACE 4: Grade Cartesiana    |  FACE 5: Círculos Concêntricos|  FACE 6: Cores Complementares     |
|  Pullback ortogonal em w     |  Pullback de anéis de módulo  |  Rotação angular de 180°           |
+---------------------------------------------------------------------------------------------------+
```

### 🔹 Face 1: Retrato de Fase Contínuo (HSV Padrão)
- **Método:** $\text{Matiz} = \frac{\arg(f(z))}{2\pi} \pmod 1$, $\text{Saturação} = 1.0$, $\text{Valor} = \text{modulação logarítmica suave}$.
- **Interpretação:** Vórtice no sentido anti-horário (Vermelho $\to$ Amarelo $\to$ Verde $\to$ Ciano $\to$ Azul $\to$ Magenta) ao redor do zero $z=1$, e vórtices no sentido horário ao redor dos polos $z_1, z_2$.

### 🔹 Face 2: 6 Setores Angulares Sólidos
- **Método:** Setores de $60^\circ$ puros:
  $$\text{Cor}(\theta) = \begin{cases}
  \text{Vermelho} & 0^\circ \le \theta < 60^\circ \\
  \text{Amarelo} & 60^\circ \le \theta < 120^\circ \\
  \text{Verde} & 120^\circ \le \theta < 180^\circ \\
  \text{Ciano} & 180^\circ \le \theta < 240^\circ \\
  \text{Azul} & 240^\circ \le \theta < 300^\circ \\
  \text{Magenta} & 300^\circ \le \theta < 360^\circ
  \end{cases}$$
- **Interpretação:** Discretização angular sem gradientes, tornando as fronteiras de fase nítidas.

### 🔹 Face 3: Estilo Elias Wegert (*Enhanced Phase Plot*)
- **Método:** Modulação de luminância por função dente-de-serra (*sawtooth*):
  $$L(z) = 0.5 + 0.5 \cdot \operatorname{saw}\bigl(n_m \log_2 |f(z)|\bigr) \cdot \operatorname{saw}\bigl(n_\phi \arg f(z)\bigr)$$
- **Interpretação:** As linhas escuras formam curvas de nível isomodulares e raios de argumento constante ortogonais, evidenciando a conformidade do mapeamento.

### 🔹 Face 4: Grade Cartesiana no Plano $w$ (*Pullback Conforme*)
- **Método:** Projeção $f^*(I)(z) = I(f(z))$ onde $I(u, v)$ é uma malha ortogonal com eixos coordenados no plano $w$.
- **Interpretação:** Demonstra geometricamente como a função $f(z)$ deforma o plano complexo preservando todos os ângulos retos locais.

### 🔹 Face 5: Círculos Concêntricos no Plano $w$ (*Pullback de Magnitude*)
- **Método:** Pullback de 8 anéis concêntricos coloridos centrados na origem $w=0$.
- **Interpretação:** As curvas circulares de $|w| = r_k$ são deformadas no plano $z$ em curvas de Cassini / ovais ao redor do zero e dos polos.

### 🔹 Face 6: Paleta de Cores Complementares (Fase Rotacionada em $180^\circ$)
- **Método:** Retrato contínuo com deslocamento de matiz de meia-volta: $\theta' = \arg(f(z)) + \pi$.
- **Interpretação:** Inverte as cores complementares (Vermelho $\leftrightarrow$ Ciano, Verde $\leftrightarrow$ Magenta, Azul $\leftrightarrow$ Amarelo).

---

## 🖨️ Arquivos Prontos para Impressão Gráfica

- **Painel Comparativo 2×3:** [`painel_6_faces_domain_coloring.png`](painel_6_faces_domain_coloring.png)
- **Plano Frontal (Frente 4840×4840 px):** [`Plano_Frontal_DomainColoring.png`](Plano_Frontal_DomainColoring.png)
- **Plano Traseiro (Verso 4840×4840 px):** [`Plano_Traseiro_DomainColoring.png`](Plano_Traseiro_DomainColoring.png)
- **Faces Individuais 4K UHD (3840×3840 px):** Em [`faces/`](faces/): `face1.png` até `face6.png`.

---

## 🛠️ Script de Regeneração
```bash
python src/fabrication/flexagon_domain_faces.py
```
