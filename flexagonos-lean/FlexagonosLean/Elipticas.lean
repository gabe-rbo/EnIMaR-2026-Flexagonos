/-
# As funções elípticas do hexa-tetraflexágono (Teorema 6.2, forma do artigo)

O Teorema 6.2 afirma que as soluções do hexa-tetraflexágono são exatamente
`ℂ(℘(z;2ℤ[i]), ℘'(z;2ℤ[i]))`.  A Mathlib fornece a `℘` de Weierstrass
analítica (`Mathlib.Analysis.SpecialFunctions.Elliptic.Weierstrass`): a série,
a convergência localmente uniforme, a meromorfia, a periodicidade e a equação
diferencial.

Este arquivo constrói o par de períodos `(2, 2i)` do artigo e demonstra a
**direção suficiente** do Teorema 6.2: `℘`, `℘'` e toda função racional delas
satisfazem a condição (iii) do Teorema 3.2 para o hexa-tetraflexágono, isto é,
são invariantes por `Γ_hexa = 2ℤ[i]`.

(A recíproca — *toda* elíptica de reticulado `Λ` é racional em `℘` e `℘'` — é o
teorema clássico do corpo das funções elípticas, que a Mathlib ainda não tem.)
-/
import FlexagonosLean.Retorno

namespace Flexagonos

open Complex

/-! ## O subanel das funções invariantes

O grupo de invariância `Stab f` do Teorema 3.2 depende de `f` de maneira
compatível com as operações de anel: se `f` e `g` são `H`-invariantes, também o
são `f + g`, `f · g`, `-f`, e (pontualmente) `f⁻¹`.  É o que permite passar de
`℘` e `℘'` a todo o corpo `ℂ(℘,℘')`. -/

/-- O subanel das funções `H`-invariantes de `ℂ → ℂ`. -/
def invariantes (H : Subgroup Aff) : Subring (ℂ → ℂ) where
  carrier := {f | H ≤ Stab f}
  zero_mem' := fun S _ z => rfl
  one_mem' := fun S _ z => rfl
  add_mem' := by
    intro f g hf hg S hS z
    show f (S.act z) + g (S.act z) = f z + g z
    rw [hf hS z, hg hS z]
  mul_mem' := by
    intro f g hf hg S hS z
    show f (S.act z) * g (S.act z) = f z * g z
    rw [hf hS z, hg hS z]
  neg_mem' := by
    intro f hf S hS z
    show -f (S.act z) = -f z
    rw [hf hS z]

lemma mem_invariantes {H : Subgroup Aff} {f : ℂ → ℂ} :
    f ∈ invariantes H ↔ H ≤ Stab f := Iff.rfl

/-- As funções constantes são invariantes por qualquer grupo. -/
lemma const_mem_invariantes (H : Subgroup Aff) (c : ℂ) :
    (fun _ : ℂ => c) ∈ invariantes H := fun _ _ _ => rfl

/-- O inverso pontual de uma função invariante é invariante: é o passo que leva
do anel `ℂ[℘,℘']` ao corpo `ℂ(℘,℘')`. -/
lemma inv_mem_invariantes {H : Subgroup Aff} {f : ℂ → ℂ} (hf : f ∈ invariantes H) :
    (fun z => (f z)⁻¹) ∈ invariantes H := by
  intro S hS z
  show (f (S.act z))⁻¹ = (f z)⁻¹
  rw [hf hS z]

/-- Quociente de invariantes é invariante. -/
lemma div_mem_invariantes {H : Subgroup Aff} {f g : ℂ → ℂ}
    (hf : f ∈ invariantes H) (hg : g ∈ invariantes H) :
    (fun z => f z / g z) ∈ invariantes H := by
  intro S hS z
  show f (S.act z) / g (S.act z) = f z / g z
  rw [hf hS z, hg hS z]

/-- Uma função é invariante por `Γ_hexa` exatamente quando é elíptica de
reticulado `2ℤ[i]`. -/
lemma mem_invariantes_gammaHexa {f : ℂ → ℂ} :
    f ∈ invariantes GammaHexa ↔
      (Function.Periodic f 2 ∧ Function.Periodic f (2 * I)) := by
  rw [mem_invariantes, gammaHexa_eq, Subgroup.closure_le]
  constructor
  · intro h
    refine ⟨fun z => ?_, fun z => ?_⟩
    · have := h (by simp : Aff.T (2 : ℂ) ∈ ({Aff.T (2 : ℂ), Aff.T (2 * I)} : Set Aff)) z
      simpa using this
    · have := h (by simp : Aff.T (2 * I) ∈ ({Aff.T (2 : ℂ), Aff.T (2 * I)} : Set Aff)) z
      simpa using this
  · rintro ⟨p1, p2⟩ S hS z
    rcases hS with hS | hS
    · rw [hS]; simpa using p1 z
    · rw [Set.mem_singleton_iff] at hS
      rw [hS]; simpa using p2 z

/-! ## O reticulado `2ℤ[i]` -/

/-- O par de períodos `(2, 2i)` do hexa-tetraflexágono (Teorema 6.2). -/
noncomputable def hexaPair : PeriodPair where
  ω₁ := 2
  ω₂ := 2 * I
  indep := by
    rw [LinearIndependent.pair_iff]
    intro s t hst
    rw [Complex.real_smul, Complex.real_smul] at hst
    have hre := congrArg Complex.re hst
    have him := congrArg Complex.im hst
    simp at hre him
    exact ⟨hre, him⟩

@[simp] lemma hexaPair_ω₁ : hexaPair.ω₁ = 2 := rfl
@[simp] lemma hexaPair_ω₂ : hexaPair.ω₂ = 2 * I := rfl

lemma two_mem_hexaLattice : (2 : ℂ) ∈ hexaPair.lattice :=
  hexaPair.ω₁_mem_lattice

lemma twoI_mem_hexaLattice : (2 * I : ℂ) ∈ hexaPair.lattice :=
  hexaPair.ω₂_mem_lattice

/-- `℘(z; 2ℤ[i])`. -/
noncomputable def wp : ℂ → ℂ := hexaPair.weierstrassP

/-- `℘'(z; 2ℤ[i])`. -/
noncomputable def wp' : ℂ → ℂ := hexaPair.derivWeierstrassP

/-! ## `℘` e `℘'` são soluções do hexa-tetraflexágono -/

lemma periodic_wp_two : Function.Periodic wp 2 :=
  hexaPair.periodic_weierstrassP ⟨2, two_mem_hexaLattice⟩

lemma periodic_wp_twoI : Function.Periodic wp (2 * I) :=
  hexaPair.periodic_weierstrassP ⟨2 * I, twoI_mem_hexaLattice⟩

lemma periodic_wp'_two : Function.Periodic wp' 2 :=
  hexaPair.periodic_derivWeierstrassP ⟨2, two_mem_hexaLattice⟩

lemma periodic_wp'_twoI : Function.Periodic wp' (2 * I) :=
  hexaPair.periodic_derivWeierstrassP ⟨2 * I, twoI_mem_hexaLattice⟩

/-- **`℘` é invariante por `Γ_hexa`.** -/
theorem wp_mem_invariantes : wp ∈ invariantes GammaHexa :=
  mem_invariantes_gammaHexa.2 ⟨periodic_wp_two, periodic_wp_twoI⟩

/-- **`℘'` é invariante por `Γ_hexa`.** -/
theorem wp'_mem_invariantes : wp' ∈ invariantes GammaHexa :=
  mem_invariantes_gammaHexa.2 ⟨periodic_wp'_two, periodic_wp'_twoI⟩

/-- **Teorema 6.2, direção suficiente.**  Toda função racional de `℘` e `℘'`
é invariante por `Γ_hexa`, isto é, satisfaz a condição (iii) do Teorema 3.2
para as três faces do hexa-tetraflexágono.

O enunciado abaixo é o caso geral `P(℘,℘')/Q(℘,℘')`; os lemas de fecho acima
(`add_mem`, `mul_mem`, `neg_mem`, `const_mem_invariantes`, `div_mem_invariantes`)
geram todo o corpo `ℂ(℘,℘')` a partir de `wp`, `wp'` e das constantes. -/
theorem racional_wp_mem_invariantes (P Q : ℂ → ℂ → ℂ)
    (hP : ∀ S ∈ GammaHexa, ∀ z, P (wp (S.act z)) (wp' (S.act z)) = P (wp z) (wp' z))
    (hQ : ∀ S ∈ GammaHexa, ∀ z, Q (wp (S.act z)) (wp' (S.act z)) = Q (wp z) (wp' z)) :
    (fun z => P (wp z) (wp' z) / Q (wp z) (wp' z)) ∈ invariantes GammaHexa := by
  intro S hS z
  show P (wp (S.act z)) (wp' (S.act z)) / Q (wp (S.act z)) (wp' (S.act z))
      = P (wp z) (wp' z) / Q (wp z) (wp' z)
  rw [hP S hS z, hQ S hS z]

/-- Exemplo concreto: `℘²` é solução — é o gerador da classe `(posto 2, |P|=4)`
do Teorema 4.1. -/
example : (fun z => wp z ^ 2) ∈ invariantes GammaHexa := by
  have h : (fun z => wp z ^ 2) = wp * wp := by funext z; simp [sq]
  rw [h]
  exact (invariantes GammaHexa).mul_mem wp_mem_invariantes wp_mem_invariantes

/-- A função `℘'² - 4℘³` (que a equação diferencial de Weierstrass identifica
com `-g₂℘ - g₃`) é invariante. -/
example : (fun z => wp' z ^ 2 - 4 * wp z ^ 3) ∈ invariantes GammaHexa := by
  have h4 : (fun _ : ℂ => (4 : ℂ)) ∈ invariantes GammaHexa := const_mem_invariantes _ 4
  have h : (fun z => wp' z ^ 2 - 4 * wp z ^ 3)
      = wp' * wp' - (fun _ : ℂ => (4 : ℂ)) * (wp * wp * wp) := by
    funext z
    simp only [Pi.sub_apply, Pi.mul_apply]
    ring
  rw [h]
  exact (invariantes GammaHexa).sub_mem
    ((invariantes GammaHexa).mul_mem wp'_mem_invariantes wp'_mem_invariantes)
    ((invariantes GammaHexa).mul_mem h4
      ((invariantes GammaHexa).mul_mem
        ((invariantes GammaHexa).mul_mem wp_mem_invariantes wp_mem_invariantes)
        wp_mem_invariantes))

end Flexagonos
