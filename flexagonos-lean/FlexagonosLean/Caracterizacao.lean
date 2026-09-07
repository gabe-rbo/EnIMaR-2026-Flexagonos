/-
# O teorema de caracterização (Seção 3 do artigo)

Teorema 3.2: `f` é `Φ`-flexionável ⟺ as quatro determinações `f ∘ A_j⁻¹`
coincidem ⟺ `f` é invariante por `Γ_Φ`.

Trabalhamos com `f` **inteira** (`Differentiable ℂ f`).  Esta é a versão
suficiente para os Teoremas 6.1 e 6.2 (Seção `Flexagonos`), cujo conteúdo é
precisamente a existência ou inexistência de soluções inteiras.
-/
import FlexagonosLean.Discrepancia

namespace Flexagonos

open Complex Set

/-! ## Os quadrantes -/

/-- Extremos horizontais dos quatro quadrantes. -/
def xlo : Fin 4 → ℝ := ![0, -1, -1, 0]
/-- Extremos horizontais dos quatro quadrantes. -/
def xhi : Fin 4 → ℝ := ![1, 0, 0, 1]
/-- Extremos verticais dos quatro quadrantes. -/
def ylo : Fin 4 → ℝ := ![0, 0, -1, -1]
/-- Extremos verticais dos quatro quadrantes. -/
def yhi : Fin 4 → ℝ := ![1, 1, 0, 0]

/-- O interior `Q̊_j` do `j`-ésimo quadrante:
`Q̊₁ = (0,1)²`, `Q̊₂ = (-1,0)×(0,1)`, `Q̊₃ = (-1,0)²`, `Q̊₄ = (0,1)×(-1,0)`. -/
def quad (j : Fin 4) : Set ℂ :=
  {z | z.re ∈ Ioo (xlo j) (xhi j) ∧ z.im ∈ Ioo (ylo j) (yhi j)}

/-- O quadrado `Q = [-1,1]²`. -/
def Q : Set ℂ := {z | z.re ∈ Icc (-1 : ℝ) 1 ∧ z.im ∈ Icc (-1 : ℝ) 1}

lemma isOpen_quad (j : Fin 4) : IsOpen (quad j) :=
  (isOpen_Ioo.preimage Complex.continuous_re).inter
    (isOpen_Ioo.preimage Complex.continuous_im)

/-- Um ponto explícito do interior de cada quadrante (o seu centro). -/
noncomputable def ponto (j : Fin 4) : ℂ := ⟨(xlo j + xhi j) / 2, (ylo j + yhi j) / 2⟩

lemma ponto_mem_quad (j : Fin 4) : ponto j ∈ quad j := by
  fin_cases j <;>
    refine ⟨⟨?_, ?_⟩, ⟨?_, ?_⟩⟩ <;>
    norm_num [ponto, quad, xlo, xhi, ylo, yhi]

lemma nonempty_quad (j : Fin 4) : (quad j).Nonempty := ⟨ponto j, ponto_mem_quad j⟩

lemma quad_subset_Q (j : Fin 4) : quad j ⊆ Q := by
  intro z hz
  have h1 : (-1 : ℝ) ≤ xlo j := by fin_cases j <;> norm_num [xlo]
  have h2 : xhi j ≤ 1 := by fin_cases j <;> norm_num [xhi]
  have h3 : (-1 : ℝ) ≤ ylo j := by fin_cases j <;> norm_num [ylo]
  have h4 : yhi j ≤ 1 := by fin_cases j <;> norm_num [yhi]
  exact ⟨⟨h1.trans hz.1.1.le, hz.1.2.le.trans h2⟩, ⟨h3.trans hz.2.1.le, hz.2.2.le.trans h4⟩⟩

/-! ## Flexionabilidade -/

/-- **Definição 2.4** (versão holomorfa).  `f` é *`Φ`-flexionável* se existe uma
vizinhança aberta e conexa `U ⊇ Q` e uma função `G` holomorfa em `U` com
`G = f ∘ A_j⁻¹` em `Q̊_{σ(j)}`, para `j = 1,2,3,4`. -/
def Flexionavel (Φ : Flex) (f : ℂ → ℂ) : Prop :=
  ∃ U : Set ℂ, ∃ G : ℂ → ℂ,
    IsOpen U ∧ IsPreconnected U ∧ Q ⊆ U ∧ AnalyticOnNhd ℂ G U ∧
      ∀ j : Fin 4, EqOn G (f ∘ (Φ.A j)⁻¹.act) (quad (Φ.σ j))

/-- O grupo de invariância de `f`: `{S : f ∘ S = f}`.  Que seja um subgrupo é o
passo (ii) ⇒ (iii) da demonstração do Teorema 3.2. -/
def Stab (f : ℂ → ℂ) : Subgroup Aff where
  carrier := {S | ∀ z, f (S.act z) = f z}
  one_mem' := by intro z; simp
  mul_mem' := by
    intro S T hS hT z
    simp only [Aff.act_mul]
    rw [hS, hT]
  inv_mem' := by
    intro S hS z
    have h := hS (S⁻¹.act z)
    rw [Aff.act_act_inv] at h
    exact h.symm

lemma mem_Stab {f : ℂ → ℂ} {S : Aff} : S ∈ Stab f ↔ ∀ z, f (S.act z) = f z := Iff.rfl

/-! ## O teorema -/

private lemma analytic_comp {f : ℂ → ℂ} (hf : Differentiable ℂ f) (S : Aff)
    {U : Set ℂ} (hU : IsOpen U) : AnalyticOnNhd ℂ (f ∘ S.act) U :=
  ((hf.comp S.differentiable_act).differentiableOn).analyticOnNhd hU

/-- **Teorema 3.2 (Caracterização).**  Seja `f` inteira e `Φ` um flex de
quadrantes.  São equivalentes:

1. `f` é `Φ`-flexionável;
2. as quatro determinações coincidem: `f ∘ A_1⁻¹ = ⋯ = f ∘ A_4⁻¹` em `ℂ`;
3. `f ∘ S = f` para todo `S ∈ Γ_Φ`. -/
theorem caracterizacao (Φ : Flex) (f : ℂ → ℂ) (hf : Differentiable ℂ f) :
    List.TFAE
      [ Flexionavel Φ f,
        ∀ j k : Fin 4, ∀ z, f ((Φ.A j)⁻¹.act z) = f ((Φ.A k)⁻¹.act z),
        Φ.Gamma ≤ Stab f ] := by
  tfae_have 1 → 2 := by
    rintro ⟨U, G, hUo, hUc, hQU, hG, hEq⟩ j k z
    -- Cada `f ∘ A_j⁻¹` é holomorfa em todo o plano.
    have hAnU : ∀ m : Fin 4, AnalyticOnNhd ℂ (f ∘ (Φ.A m)⁻¹.act) U :=
      fun m => analytic_comp hf _ hUo
    have hAnV : ∀ m : Fin 4, AnalyticOnNhd ℂ (f ∘ (Φ.A m)⁻¹.act) univ :=
      fun m => analytic_comp hf _ isOpen_univ
    -- Princípio da identidade em `U`: `G = f ∘ A_m⁻¹` em todo `U`.
    have key : ∀ m : Fin 4, EqOn G (f ∘ (Φ.A m)⁻¹.act) U := by
      intro m
      obtain ⟨z₀, hz₀⟩ := nonempty_quad (Φ.σ m)
      have hz₀U : z₀ ∈ U := hQU (quad_subset_Q _ hz₀)
      refine hG.eqOn_of_preconnected_of_eventuallyEq (hAnU m) hUc hz₀U ?_
      exact Filter.eventuallyEq_of_mem ((isOpen_quad _).mem_nhds hz₀) (hEq m)
    -- Logo as determinações coincidem em `U`, ...
    obtain ⟨z₀, hz₀⟩ := nonempty_quad (Φ.σ j)
    have hz₀U : z₀ ∈ U := hQU (quad_subset_Q _ hz₀)
    have hjkU : EqOn (f ∘ (Φ.A j)⁻¹.act) (f ∘ (Φ.A k)⁻¹.act) U :=
      fun w hw => (key j hw).symm.trans (key k hw)
    -- ... e, de novo pelo princípio da identidade, em todo o plano.
    have : EqOn (f ∘ (Φ.A j)⁻¹.act) (f ∘ (Φ.A k)⁻¹.act) univ :=
      (hAnV j).eqOn_of_preconnected_of_eventuallyEq (hAnV k) isPreconnected_univ
        (mem_univ z₀) (Filter.eventuallyEq_of_mem (hUo.mem_nhds hz₀U) hjkU)
    exact this (mem_univ z)
  tfae_have 2 → 3 := by
    intro h2
    refine GammaOf_le (H := Stab f) fun j k => ?_
    intro w
    rw [Aff.act_mul]
    have h := h2 j k ((Φ.A j).act w)
    rw [Aff.act_inv_act] at h
    exact h.symm
  tfae_have 3 → 1 := by
    intro h3
    refine ⟨univ, f ∘ (Φ.A 0)⁻¹.act, isOpen_univ, isPreconnected_univ, subset_univ _,
      analytic_comp hf _ isOpen_univ, ?_⟩
    intro j z _
    have hmem : (Φ.A 0)⁻¹ * Φ.A j ∈ Φ.Gamma := gerador_mem _ j 0
    have h := h3 hmem ((Φ.A j)⁻¹.act z)
    rw [Aff.act_mul, Aff.act_act_inv] at h
    simpa only [Function.comp_apply] using h
  tfae_finish

/-- A forma que usaremos: `f` é `Φ`-flexionável se e só se é `Γ_Φ`-invariante. -/
theorem flexionavel_iff (Φ : Flex) (f : ℂ → ℂ) (hf : Differentiable ℂ f) :
    Flexionavel Φ f ↔ Φ.Gamma ≤ Stab f :=
  (caracterizacao Φ f hf).out 0 2

/-- A última afirmação do Teorema 3.2: o flexionado `Φ_*f = f ∘ A_1⁻¹` tem
grupo de invariância `A_1 Γ_Φ A_1⁻¹`. -/
theorem stab_flexionado (Φ : Flex) (f : ℂ → ℂ) (h : Φ.Gamma ≤ Stab f) :
    ∀ S ∈ Φ.Gamma, (Φ.A 0 * S * (Φ.A 0)⁻¹) ∈ Stab (f ∘ (Φ.A 0)⁻¹.act) := by
  intro S hS z
  simp only [Function.comp_apply, Aff.act_mul, Aff.act_inv_act]
  exact h hS ((Φ.A 0)⁻¹.act z)

end Flexagonos
