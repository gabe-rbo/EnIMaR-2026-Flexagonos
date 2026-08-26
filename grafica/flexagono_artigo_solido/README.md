# Flexágono das Funções do Artigo Científico (Teorema Universal da Invariância)

Este flexágono foi concebido com uma correspondência estrita e unívoca com o **artigo de pesquisa ("Funções Complexas Flexionáveis")**.

Cada uma das 6 faces representa **uma das soluções geradoras canônicas (*Hauptmodul*) do Teorema da Classificação Universal (Teorema 5.1)**, renderizada em **Cores Sólidas e Resolução Nativa 4K UHD** ($3840 \times 3840$ px).

---

## 📐 Fundamento Teórico do Artigo

Dada uma face de um flexágono e seu mapa de retorno cinemático $\Phi$, uma função meromorfa $f: \mathbb{C} \to \hat{\mathbb{C}}$ pode ser pintada na face de modo que a função se preserve após as flexões se e somente se $f$ é invariante sob um subgrupo discreto do plano:
$$\Gamma_\Phi \le W^+(D) \le C_n \ltimes \frac{1}{d}\mathcal{O}_n$$
onde $\mathcal{O}_n$ é o anel de inteiros algébricos ($\mathbb{Z}[i]$ para polióminos quadrados e $\mathbb{Z}[\zeta_3]$ para triângulos).

O **Teorema da Classificação Universal** divide todas as soluções possíveis em **9 classes fundamentais**, determinadas pelo posto do reticulado de translações ($\operatorname{posto}\Lambda \in \{0, 1, 2\}$) e pela ordem do grupo de rotações pontuais ($|P| \in \{1, 2, 3, 4, 6\}$).

---

## 🎨 As 6 Faces e suas Respectivas Funções do Artigo

```
+---------------------------------------------------------------------------------------------------+
|  FACE 1: Classe (0, 4)       |  FACE 2: Classe (1, 1)        |  FACE 3: Classe (1, 2)             |
|  J₁(z) = z⁴                  |  J₂(z) = exp(π i z) - 1       |  J₃(z) = cos(π z)                  |
|  [6 Setores Angulares]       |  [Grade Cartesiana Ortogonal] |  [Mosaico de Arcos de Truchet]     |
|------------------------------+-------------------------------+------------------------------------|
|  FACE 4: Classe (2, 2)       |  FACE 5: Classe (2, 3)        |  FACE 6: Classe (2, 4)             |
|  J₄(z) = ℘(z; 2ℤ[i])         |  J₅(z) = ℘'(z; 2ℤ[ζ₃])        |  J₆(z) = ℘(z; 2ℤ[i])²              |
|  [Tabuleiro de Xadrez]       |  [Alvos Concêntricos (10 An.)]|  [Favos de Mel Hexagonais]         |
+---------------------------------------------------------------------------------------------------+
```

---

### Detalhamento Matemático Face a Face

### 🔹 Face 1: Classe $(0, 4)$ — Rotação Quártica Pura
- **Função:** $J_1(z) = z^4$
- **Classificação:** $\operatorname{posto}\Lambda = 0$, $|P| = 4$, Órbifold $\mathbb{C}/C_4$.
- **Grupo de Simetria:** Grupo cíclico $C_4$ gerado pela rotação de $90^\circ$ ($z \mapsto iz$).
- **Propriedade Matemática:** É uma função inteira polinomial com zero de multiplicidade 4 no centro do tetraflexágono. Os quatro quadrantes da dobra giram e coincidem perfeitamente.
- **Estilo Gráfico:** **6 Setores Angulares Sólidos** (discretização pura de $\arg(w)$ em 6 cores: Vermelho, Amarelo, Verde, Ciano, Azul e Magenta).

---

### 🔹 Face 2: Classe $(1, 1)$ — Faixa Periódica Conforme
- **Função:** $J_2(z) = \exp(\pi i z) - 1$
- **Classificação:** $\operatorname{posto}\Lambda = 1$, $|P| = 1$, Órbifold $\mathbb{C}/\mathbb{Z}$.
- **Grupo de Simetria:** Grupo infinito de translações unidimensionais gerado por $z \mapsto z + 2$.
- **Propriedade Matemática:** Função inteira sem polos. Ilustra o **Teorema 2.4 de Elias Wegert** para faixas periódicas conformes horizontais.
- **Estilo Gráfico:** **Grade Cartesiana Ortogonal no plano $w$ (Pullback)**, exibindo a deformação exponencial com preservação de ângulos retos e eixos rubros destacados.

---

### 🔹 Face 3: Classe $(1, 2)$ — Inversão e Simetria Par
- **Função:** $J_3(z) = \cos(\pi z) = \frac{e^{i\pi z} + e^{-i\pi z}}{2}$
- **Classificação:** $\operatorname{posto}\Lambda = 1$, $|P| = 2$, Órbifold $\mathbb{C}/D_1$.
- **Grupo de Simetria:** Grupo diédrico infinito gerado pela translação $z \mapsto z + 2$ e pela reflexão/inversão central $z \mapsto -z$.
- **Propriedade Matemática:** Função par periódica com zeros simples nos pontos semi-inteiros $z = \pm \frac{1}{2}, \pm \frac{3}{2}, \dots$.
- **Estilo Gráfico:** **Mosaico de Arcos de Truchet no plano $w$ (Pullback)**, criando laços e rosetas suaves que se conectam simetricamente sobre as dobras (ligação com o artigo de Truchet / Hall et al. 2020).

---

### 🔹 Face 4: Classe $(2, 2)$ — Função Elíptica Lemniscática
- **Função:** $J_4(z) = \wp(z; 2\mathbb{Z}[i])$
- **Classificação:** $\operatorname{posto}\Lambda = 2$, $|P| = 2$, Reticulado de Gauss $\Lambda = 2\mathbb{Z}[i]$.
- **Invariantes Modulares:** $g_3 = 0$, $j(\tau) = 1728$, $\tau = i$.
- **Propriedade Matemática:** Função duplamente periódica clássica de Weierstrass calculada via funções teta de Jacobi $\vartheta_n(v, q)$. Possui um polo duplo de ordem 2 em cada vértice do reticulado quadrado. Não admite soluções inteiras (força a presença de polos).
- **Estilo Gráfico:** **Tabuleiro de Xadrez de Alto Contraste (Pullback)**, cujos quadrados pretos e brancos são distorcidos conformalmente ao redor do polo duplo central.

---

### 🔹 Face 5: Classe $(2, 3)$ — Derivada de Weierstrass Equianarmônica
- **Função:** $J_5(z) = \wp'(z; 2\mathbb{Z}[\zeta_3])$
- **Classificação:** $\operatorname{posto}\Lambda = 2$, $|P| = 3$, Reticulado Triangular de Eisenstein $\Lambda = 2\mathbb{Z}[\zeta_3]$.
- **Invariantes Modulares:** $g_2 = 0$, $j(\tau) = 0$, $\tau = e^{i\pi/3}$.
- **Propriedade Matemática:** A derivada $\wp'$ satisfaz $\wp'(\zeta_3 z) = \zeta_3^{-3}\wp'(z) = \wp'(z)$, sendo estritamente invariante por rotações de $120^\circ$ ($C_3$). Possui um polo triplo de ordem 3 na origem.
- **Estilo Gráfico:** **Alvos de 10 Anéis Concêntricos em Cores Sólidas (Pullback)**, revelando as curvas de nível isomodulares $|\wp'| = \text{const}$ em 3 pétalas simétricas.

---

### 🔹 Face 6: Classe $(2, 4)$ — Quadrado da Função Elíptica Quártica
- **Função:** $J_6(z) = \wp(z; 2\mathbb{Z}[i])^2$
- **Classificação:** $\operatorname{posto}\Lambda = 2$, $|P| = 4$, Grupo Cristalográfico Plano $p4$.
- **Invariantes Modulares:** $\Lambda = 2\mathbb{Z}[i]$, $g_3 = 0$, $j(\tau) = 1728$.
- **Propriedade Matemática:** Como $\wp(iz) = -\wp(z)$, o quadrado $\wp^2$ elimina o sinal negativo e torna-se invariante por rotações de $90^\circ$ ($C_4$). Possui um polo quádruplo de ordem 4 em cada nó do reticulado.
- **Estilo Gráfico:** **Tesselação de Favos de Mel Hexagonais no plano $w$ (Pullback)**, gerando 4 vórtices hexagonais coloridos e entrelaçados nos quatro cantos da célula fundamental.

---

## 🖨️ Arquivos Gerados para Impressão Gráfica em 4K UHD

Todos os arquivos foram gerados em **alta definição** e estão prontos para gráfica:

1. **Painel Comparativo Anotado:**
   [`painel_6_faces_artigo.png`](painel_6_faces_artigo.png) *(Visão 2×3 com legendas de cada classe do teorema)*
2. **Prancha de Impressão Frontal (Frente):**
   [`Plano_Frontal_ArtigoSolido.png`](Plano_Frontal_ArtigoSolido.png) *(Resolução $4840 \times 4840$ px com sangrias de 58 px e cruzes de corte)*
3. **Prancha de Impressão Traseira (Verso):**
   [`Plano_Traseiro_ArtigoSolido.png`](Plano_Traseiro_ArtigoSolido.png) *(Resolução $4840 \times 4840$ px com sangrias e marcas de registro)*
4. **Imagens Individuais 4K UHD das Faces:**
   Na pasta [`faces/`](faces/): `face1.png` até `face6.png` ($3840 \times 3840$ px, 14,7 milhões de pontos avaliados por face).

---

## 🛠️ Como Reproduzir / Reexecutar
```bash
# Ativar virtualenv
source .venv/bin/activate

# Executar renderização 4K
python src/fabrication/gerar_flexagono_artigo_solido.py
```
