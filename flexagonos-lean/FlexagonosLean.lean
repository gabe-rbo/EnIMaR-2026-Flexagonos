/-
# Funções complexas flexionáveis — formalização em Lean 4

Formalização dos teoremas do artigo *Funções complexas flexionáveis*
(projeto EnIMaR, UFMG).

## Conteúdo

* `Aff`            — o grupo das isometrias diretas `z ↦ az + b`.
* `Mu4`            — o grupo `μ₄` parametrizado por `ZMod 4`.
* `Flex`           — Definição 2.1 e Proposição 2.3 (`|𝓕| = 6144`).
* `Discrepancia`   — Definição 3.1 (`Γ_Φ`) e Lema 3.4.
* `Caracterizacao` — **Teorema 3.2**, o teorema de caracterização.
* `Discreto`       — **Proposição 3.5** (`Γ_Φ ≤ μ₄ ⋉ ½ℤ[i]`).
* `Liouville`      — o argumento de Liouville do posto 2.
* `Retorno`        — **Proposição 5.5**, os grupos dos dois flexágonos.
* `Flexagonos`     — **Teoremas 6.1 e 6.2** e a dicotomia.
* `Recobrimento`   — a seção de `ℂ → ℂ*`; **Teo. 4.1** (posto 1) e a forma
                     final do **Teorema 6.1**.
* `Meromorfo`      — princípio da identidade meromorfo e o **Teorema 3.2** para
                     funções meromorfas.
* `Elipticas`      — o reticulado `2ℤ[i]`, `℘`, `℘'` e `ℂ(℘,℘') ⊆ soluções`.
* `FlexagonosMer`  — **Teoremas 6.1 e 6.2** meromorfos; `℘` é solução do hexa.
* `RetasDobra`     — `D∞ × D∞`, `W⁺` e o **Lema 10.1** (as seis retas geram `W`).
* `TeoremaRetas`   — **Teorema 10.2** e os Corolários **10.3** (quadrado) e
                     **10.4** (hexágono, a cota de Gardner).
* `Paridade`       — **Teoremas 12.1 e 12.4**, **Cor. 12.2** e **Prop. 12.3**:
                     a caracterização combinatória, decidida sobre as 81
                     coordenadas.
-/
import FlexagonosLean.Aff
import FlexagonosLean.Mu4
import FlexagonosLean.Flex
import FlexagonosLean.Discrepancia
import FlexagonosLean.Caracterizacao
import FlexagonosLean.Discreto
import FlexagonosLean.Liouville
import FlexagonosLean.Retorno
import FlexagonosLean.Flexagonos
import FlexagonosLean.Recobrimento
import FlexagonosLean.Meromorfo
import FlexagonosLean.Elipticas
import FlexagonosLean.FlexagonosMer
import FlexagonosLean.RetasDobra
import FlexagonosLean.TeoremaRetas
import FlexagonosLean.Paridade
