# flexagonos-lean

Formalização em Lean 4 + Mathlib dos teoremas do artigo *Funções complexas
flexionáveis* (projeto EnIMaR, UFMG).

```bash
lake exe cache get
lake build
lake env lean Audit.lean   # verifica que nada depende de `sorryAx`
```

Toolchain: `leanprover/lean4:v4.33.0`, Mathlib `v4.33.0`.

## Mapa artigo → Lean

| Artigo | Lean | Arquivo |
|---|---|---|
| Def. 2.1 (flex de quadrantes) | `Flex` | `Flex.lean` |
| Prop. 2.3 (`𝓕 ≅ μ₄ ≀ S₄`, `\|𝓕\| = 6144`) | `Flex.card_flex` | `Flex.lean` |
| eq. (2.1) (`A_j`) | `Flex.A`, `Flex.A_act` | `Flex.lean` |
| Def. 2.4 (flexionável) | `Flexionavel` | `Caracterizacao.lean` |
| Def. 3.1 (`Γ_Φ`) | `GammaOf`, `Flex.Gamma` | `Discrepancia.lean` |
| **Teo. 3.2 (Caracterização)**, `f` inteira | `caracterizacao`, `flexionavel_iff` | `Caracterizacao.lean` |
| **Teo. 3.2, `f` meromorfa** | `caracterizacaoMer`, `flexionavelMer_iff` | `Meromorfo.lean` |
| Princípio da identidade meromorfo | `eventuallyEq_nhdsNE_of_meromorphicOn`, `eqOn_of_meromorphicNFOn` | `Meromorfo.lean` |
| Teo. 3.2, última afirmação | `stab_flexionado` | `Caracterizacao.lean` |
| Lema 3.4 (fator comum à esquerda) | `GammaOf_left_mul` | `Discrepancia.lean` |
| **Prop. 3.5 (`Γ_Φ ≤ μ₄ ⋉ ½ℤ[i]`)** | `gamma_le_G0`, `translacao_mem_MeioZi` | `Discreto.lean` |
| Teo. 4.1, posto 2 (Liouville) | `const_of_biperiodic` | `Liouville.lean` |
| **Teo. 4.1, posto 1 `n=1`** | `periodic_iff_secao` | `Recobrimento.lean` |
| **Prop. 5.5** (`2ℤ`, `2iℤ`, `2ℤ[i]`) | `gamma_H`, `gamma_V`, `gammaTri_eq`, `gammaHexa_eq` | `Retorno.lean` |
| **Teo. 6.1 (tri)**, forma final | `tri_forma_final` (`f = h∘e^{iπz}`) | `Recobrimento.lean` |
| Teo. 6.1, soluções inteiras | `tri`, `tri_de_h`, `tri_admite_inteira_nao_constante` | `Flexagonos.lean` |
| **Teo. 6.2 (hexa)** | `hexa_iff`, `hexa_sem_inteiras_nao_constantes`, `hexa_faces_isoladas` | `Flexagonos.lean` |
| **Teo. 6.2, `ℂ(℘,℘')` ⊆ soluções** | `wp_mem_invariantes`, `wp'_mem_invariantes`, `invariantes` | `Elipticas.lean` |
| **Teo. 6.1 / 6.2 meromorfos** | `triMer`, `hexaMer_iff` | `FlexagonosMer.lean` |
| **`℘` é solução do hexa** | `wp_flexionavelHexa`, `wp'_flexionavelHexa`, `wp_not_const` | `FlexagonosMer.lean` |
| Obs. 6.3 (a dicotomia) | `dicotomia`, `dicotomia_mer`, `hexa_dicotomia_completa` | `Flexagonos.lean`, `FlexagonosMer.lean` |
| **Lema 10.1** (as seis retas geram `W`) | `W.closure_retasAdmissiveis` | `RetasDobra.lean` |
| **Teo. 10.2 (retas de dobra)** | `retas_de_dobra`, `discrepancia_mem_closure` | `TeoremaRetas.lean` |
| **Cor. 10.3** (`W⁺ = p2`, `Λ ⊆ 2ℤ[i]`, `\|P\| ≤ 2`) | `W.toAff_mem_p2`, `translacao_mem_DoisZi`, `ponto_eq_pm_one` | `TeoremaRetas.lean` |
| **Cor. 10.4** (hexágono, `W⁺ = C₃`, Gardner) | `Whex.card_Whex`, `Whex.card_Wplus`, `Whex.gardner` | `TeoremaRetas.lean` |
| **Teo. 12.1 (fórmula de paridade)** | `Dinf.tbit_emod_two`, `W.rotBit_emod_four`, `W.sideBit_emod_two` | `Paridade.lean` |
| **Cor. 12.2 (fórmula dos intervalos)** | `rot`, `rot_eq_two_mul_parity` | `Paridade.lean` |
| **Prop. 12.3** (25 das 81 coordenadas) | `card_validas` | `Paridade.lean` |
| **Teo. 12.4** (o arranjo é função de `u`) | `assinatura_unica_faces_3456`, `faces_12_diagonal`, `assinaturas_faces_12`, `excepcional_unica` | `Paridade.lean` |

## Decisões de modelagem

**Categoria.** O Teorema 3.2 está demonstrado nas duas categorias: para `f`
inteira (`Caracterizacao.lean`) e para `f` meromorfa (`Meromorfo.lean`), e
`flexionavelMer_iff_flexionavel` mostra que as duas noções coincidem quando `f`
é inteira.  A demonstração é a do artigo, sem alteração: princípio da
identidade duas vezes (em `U` e depois em `ℂ`).

**Valores nos polos.** Na Mathlib uma função meromorfa é uma função genuína
`ℂ → ℂ`, com um valor arbitrário em cada polo; duas funções meromorfas que
coincidem num aberto coincidem, portanto, apenas fora de um conjunto discreto.
Para que as igualdades (ii) e (iii) do Teorema 3.2 sejam igualdades de funções,
`f` é tomada em **forma normal** (`MerNF`, i.e. `MeromorphicNFOn f univ`): o
representante canónico, que vale `0` nos polos.  Como toda função meromorfa tem
um e um só representante nesta forma, não há perda de generalidade — é a
escolha implícita quando se fala do *corpo* das funções meromorfas.  A função
`G` da Definição 2.4 não precisa de estar em forma normal; só `f` precisa.

**`μ₄`.** Parametrizado por `ZMod 4` via `zeta u = i^u`, o que torna o grupo de
pontos decidível e faz `zeta` um homomorfismo.

**Índices.** O artigo numera os quadrantes `1,2,3,4`; aqui `Fin 4` com
`0,1,2,3`, de modo que `σ_h = (0 1)(2 3)` e `σ_v = (0 3)(1 2)`.

**Geradores de `Γ`.** `GammaOf_eq_closure_base` reduz os 16 geradores
`A_k⁻¹A_j` aos 4 geradores `A_1⁻¹A_j`, via `A_k⁻¹A_j = (A_1⁻¹A_k)⁻¹(A_1⁻¹A_j)`.

## O que ainda não está formalizado, e por quê

**Correção.** Uma versão anterior deste README afirmava que a `℘` de Weierstrass
analítica não existia na Mathlib. **Isso estava errado**: ela está em
`Mathlib/Analysis/SpecialFunctions/Elliptic/Weierstrass.lean`, com a série, a
convergência localmente uniforme, a analiticidade em `ℂ ∖ Λ`, a meromorfia, a
ordem nos pontos do reticulado, a periodicidade, `g₂`, `g₃` e a equação
diferencial `℘'² = 4℘³ - g₂℘ - g₃`. `Elipticas.lean` usa-a.

Restam duas lacunas, agora bem localizadas.

**1. O teorema do corpo das funções elípticas.** É a **única** lacuna que
separa esta formalização do enunciado do Teorema 6.2 tal como está no artigo.
Está demonstrado que `f` meromorfa é flexionável no hexa **se e só se** é
elíptica de reticulado `2ℤ[i]` (`hexaMer_iff`), e que `℘`, `℘'` e toda função
racional delas são soluções (`wp_flexionavelHexa`, `invariantes`). Falta a
recíproca clássica: *toda* elíptica de reticulado `Λ` é racional em `℘` e `℘'`.
Isso exige a teoria de divisores de funções elípticas — contagem de zeros e
polos no paralelogramo fundamental via princípio do argumento — e não está na
Mathlib.

**2. Os resultados de *busca* da Seção 10 e da Seção 12.**  As Seções 10 e 12
estão formalizadas (ver a tabela acima) *exceto* três enunciados que são
resultados de computador:

* Teo. 10.5 — os `216 768` estados dobrados e a órbita de `19 200`;
* Teo. 12.5 — a **regra dos extremos**;
* Teo. 12.6 — a classificação das `20 405` componentes do grafo de flexão.

Não há caminho honesto para eles em Lean hoje.  `native_decide` acrescentaria
`Lean.ofReduceBool` à lista de axiomas (esta formalização não usa nenhum
axioma além de `propext`, `Classical.choice` e `Quot.sound`), e uma travessia
de grafo sobre `216 768` estados está muito além do que a redução do kernel
aguenta.  O que muda a resposta é o Teorema 12.5: se a regra dos extremos
tiver demonstração à mão, os outros dois passam a ser mera verificação
computacional, que um artigo pode legitimamente deixar fora do Lean.  Note-se
que `Paridade.lean` chega exatamente ao ponto onde o artigo diz "resta um único
bit" (`assinaturas_faces_12`, `excepcional_unica`): é esse bit que a regra dos
extremos decide.

**Uma nota sobre o Teo. 10.2.**  A sua demonstração usa apenas a componente de
*isometrias* de um estado dobrado — as ordens de camadas e as três condições de
não-atravessamento de Justin não intervêm.  Foi isso que tornou a Seção 10
formalizável sem modelar papel sem auto-intersecção.

**Uma nota sobre a Seção 12.**  Aqui são as *definições* que carregam o
conteúdo, e o Lean não pega uma definição errada.  As definições concretas de
`Paridade.lean` foram por isso conferidas contra `src/paridade.py` do projeto:
reproduzem-no exatamente nas `81` coordenadas e nas `6` faces.  (O primeiro
critério que tentámos para as `25` coordenadas válidas — uma janela de largura
`2` no passeio das colunas — dava `24` e um conjunto errado; o correto é
`(u₁=1 ↔ u₃=1) ∧ (u₂=1 ↔ u₄=1)`, que dá `5×5 = 25`.)

Também não formalizada: a classificação dos subgrupos discretos das isometrias
diretas do plano (a segunda metade da Prop. 3.5); só a contenção
`Γ_Φ ≤ μ₄ ⋉ ½ℤ[i]` está provada, que é o que os teoremas seguintes usam.
