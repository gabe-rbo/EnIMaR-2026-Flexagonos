/-
# Mapas de retorno e os grupos dos dois flexágonos (Seção 5 do artigo)

Os mapas de retorno dos dois tetraflexágonos do manual são **puras permutações
de quadrantes** (`ε ≡ 1`): "recortar o quadrado em quatro e trocar as peças de
lugar".  São a troca das colunas `σ_h = (12)(34)`, a troca das linhas
`σ_v = (14)(23)` e a sua composição `σ_h σ_v = (13)(24)`.

Este arquivo demonstra a **Proposição 5.5**: os grupos de discrepância são
`2ℤ`, `2iℤ` e `2ℤ[i]` respectivamente, todos com grupo de pontos trivial.

Convenção: `Fin 4` com `0,1,2,3` para `Q₁,Q₂,Q₃,Q₄`, de modo que
`σ_h = (0 1)(2 3)` e `σ_v = (0 3)(1 2)`.
-/
import FlexagonosLean.Caracterizacao

namespace Flexagonos

open Complex

/-! ## Os mapas de retorno -/

/-- `σ_h = (12)(34)`: a troca das colunas. -/
def sigmaH : Equiv.Perm (Fin 4) := Equiv.swap 0 1 * Equiv.swap 2 3

/-- `σ_v = (14)(23)`: a troca das linhas. -/
def sigmaV : Equiv.Perm (Fin 4) := Equiv.swap 0 3 * Equiv.swap 1 2

/-- Um flex que é pura permutação de quadrantes: `ε ≡ 1`, nenhuma peça girada. -/
def flexPerm (σ : Equiv.Perm (Fin 4)) : Flex := ⟨σ, fun _ => 0⟩

@[simp] lemma flexPerm_σ (σ : Equiv.Perm (Fin 4)) : (flexPerm σ).σ = σ := rfl
@[simp] lemma flexPerm_ε (σ : Equiv.Perm (Fin 4)) (j : Fin 4) : (flexPerm σ).ε j = 0 := rfl

/-- Para `ε ≡ 1`, a peça `A_j` é a translação por `c_{σ(j)} - c_j`. -/
lemma A_flexPerm (σ : Equiv.Perm (Fin 4)) (j : Fin 4) :
    (flexPerm σ).A j = Aff.T (centro (σ j) - centro j) := by
  ext <;> simp [Flex.A, Aff.T, flexPerm]

/-- Os quatro geradores básicos `A_1⁻¹ A_j` de um flex de permutação pura. -/
lemma base_flexPerm (σ : Equiv.Perm (Fin 4)) (j : Fin 4) :
    ((flexPerm σ).A 0)⁻¹ * (flexPerm σ).A j
      = Aff.T ((centro (σ j) - centro j) - (centro (σ 0) - centro 0)) := by
  rw [A_flexPerm, A_flexPerm, Aff.T_inv, Aff.T_mul]
  ring_nf

/-- Abreviação: o deslocamento do gerador básico de índice `j`. -/
private noncomputable def d (σ : Equiv.Perm (Fin 4)) (j : Fin 4) : ℂ :=
  (centro (σ j) - centro j) - (centro (σ 0) - centro 0)

private lemma base_eq (σ : Equiv.Perm (Fin 4)) (j : Fin 4) :
    ((flexPerm σ).A 0)⁻¹ * (flexPerm σ).A j = Aff.T (d σ j) :=
  base_flexPerm σ j

/-! ## Os deslocamentos

`σ_h` desloca as peças por `-1, 1, 1, -1`; `σ_v` por `-i, -i, i, i`; e o mapa
diagonal `σ_hσ_v` por `-1-i, 1-i, 1+i, -1+i`.  Note que nenhuma peça aparece
girada: os mapas de retorno são puras permutações de quadrantes. -/

lemma desl_H (j : Fin 4) : centro (sigmaH j) - centro j = ![(-1 : ℂ), 1, 1, -1] j := by
  fin_cases j <;> simp [sigmaH, centro, Equiv.swap_apply_def] <;> ring

lemma desl_V (j : Fin 4) : centro (sigmaV j) - centro j = ![(-I : ℂ), -I, I, I] j := by
  fin_cases j <;> simp [sigmaV, centro, Equiv.swap_apply_def] <;> ring

lemma desl_D (j : Fin 4) :
    centro ((sigmaH * sigmaV) j) - centro j = ![(-1 - I : ℂ), 1 - I, 1 + I, -1 + I] j := by
  fin_cases j <;> simp [sigmaH, sigmaV, centro, Equiv.swap_apply_def] <;> ring

/-! ## Proposição 5.5 -/

private lemma dH0 : d sigmaH 0 = 0 := by simp [d]
private lemma dH1 : d sigmaH 1 = 2 := by
  simp [d, sigmaH, centro, Equiv.swap_apply_def]; ring
private lemma dH2 : d sigmaH 2 = 2 := by
  simp [d, sigmaH, centro, Equiv.swap_apply_def]; ring
private lemma dH3 : d sigmaH 3 = 0 := by
  simp [d, sigmaH, centro, Equiv.swap_apply_def]; ring

private lemma dV0 : d sigmaV 0 = 0 := by simp [d]
private lemma dV1 : d sigmaV 1 = 0 := by
  simp [d, sigmaV, centro, Equiv.swap_apply_def]; ring
private lemma dV2 : d sigmaV 2 = 2 * I := by
  simp [d, sigmaV, centro, Equiv.swap_apply_def]; ring
private lemma dV3 : d sigmaV 3 = 2 * I := by
  simp [d, sigmaV, centro, Equiv.swap_apply_def]; ring

private lemma dD0 : d (sigmaH * sigmaV) 0 = 0 := by simp [d]
private lemma dD1 : d (sigmaH * sigmaV) 1 = 2 := by
  simp [d, sigmaH, sigmaV, centro, Equiv.swap_apply_def]; ring
private lemma dD2 : d (sigmaH * sigmaV) 2 = 2 + 2 * I := by
  simp [d, sigmaH, sigmaV, centro, Equiv.swap_apply_def]; ring
private lemma dD3 : d (sigmaH * sigmaV) 3 = 2 * I := by
  simp [d, sigmaH, sigmaV, centro, Equiv.swap_apply_def]; ring

/-- **Proposição 5.5, faces `3` e `6` do hexa (e a face da frente do tri).**
`Γ_{σ_h} = 2ℤ`. -/
theorem gamma_H : (flexPerm sigmaH).Gamma = Subgroup.closure {Aff.T (2 : ℂ)} := by
  have h2 : Aff.T (2 : ℂ) ∈ Subgroup.closure ({Aff.T (2 : ℂ)} : Set Aff) :=
    Subgroup.subset_closure rfl
  apply le_antisymm
  · rw [Flex.Gamma, GammaOf_eq_closure_base, Subgroup.closure_le]
    rintro S ⟨j, rfl⟩
    fin_cases j
    · show ((flexPerm sigmaH).A 0)⁻¹ * (flexPerm sigmaH).A 0 ∈ _
      rw [base_eq, dH0, Aff.T_zero]; exact Subgroup.one_mem _
    · show ((flexPerm sigmaH).A 0)⁻¹ * (flexPerm sigmaH).A 1 ∈ _
      rw [base_eq, dH1]; exact h2
    · show ((flexPerm sigmaH).A 0)⁻¹ * (flexPerm sigmaH).A 2 ∈ _
      rw [base_eq, dH2]; exact h2
    · show ((flexPerm sigmaH).A 0)⁻¹ * (flexPerm sigmaH).A 3 ∈ _
      rw [base_eq, dH3, Aff.T_zero]; exact Subgroup.one_mem _
  · rw [Subgroup.closure_le]
    rintro S rfl
    have h := gerador_mem (flexPerm sigmaH).A 1 0
    rw [base_eq, dH1] at h
    exact h

/-- **Proposição 5.5, faces `4` e `5` do hexa.** `Γ_{σ_v} = 2iℤ`. -/
theorem gamma_V : (flexPerm sigmaV).Gamma = Subgroup.closure {Aff.T (2 * I)} := by
  have h2 : Aff.T (2 * I) ∈ Subgroup.closure ({Aff.T (2 * I)} : Set Aff) :=
    Subgroup.subset_closure rfl
  apply le_antisymm
  · rw [Flex.Gamma, GammaOf_eq_closure_base, Subgroup.closure_le]
    rintro S ⟨j, rfl⟩
    fin_cases j
    · show ((flexPerm sigmaV).A 0)⁻¹ * (flexPerm sigmaV).A 0 ∈ _
      rw [base_eq, dV0, Aff.T_zero]; exact Subgroup.one_mem _
    · show ((flexPerm sigmaV).A 0)⁻¹ * (flexPerm sigmaV).A 1 ∈ _
      rw [base_eq, dV1, Aff.T_zero]; exact Subgroup.one_mem _
    · show ((flexPerm sigmaV).A 0)⁻¹ * (flexPerm sigmaV).A 2 ∈ _
      rw [base_eq, dV2]; exact h2
    · show ((flexPerm sigmaV).A 0)⁻¹ * (flexPerm sigmaV).A 3 ∈ _
      rw [base_eq, dV3]; exact h2
  · rw [Subgroup.closure_le]
    rintro S rfl
    have h := gerador_mem (flexPerm sigmaV).A 2 0
    rw [base_eq, dV2] at h
    exact h

/-! ## Os dois flexágonos -/

/-- O grupo `Γ_𝓡` do tri-tetraflexágono: só a face da frente reaparece, e ela
reaparece ao longo de **um** eixo. -/
noncomputable def GammaTri : Subgroup Aff := (flexPerm sigmaH).Gamma

/-- O grupo `Γ_𝓡` do hexa-tetraflexágono: as faces `1` e `2` reaparecem nos três
arranjos `σ_h`, `σ_v`, `σ_hσ_v` — ao longo de **dois** eixos. -/
noncomputable def GammaHexa : Subgroup Aff :=
  (flexPerm sigmaH).Gamma ⊔ (flexPerm sigmaV).Gamma ⊔ (flexPerm (sigmaH * sigmaV)).Gamma

/-- **Proposição 5.5, linha `tri / todas`.** `Γ_tri = 2ℤ`. -/
theorem gammaTri_eq : GammaTri = Subgroup.closure {Aff.T (2 : ℂ)} := gamma_H

lemma T_two_mem_hexa : Aff.T (2 : ℂ) ∈ GammaHexa := by
  have h : Aff.T (2 : ℂ) ∈ (flexPerm sigmaH).Gamma := by
    rw [gamma_H]; exact Subgroup.subset_closure rfl
  have hle : (flexPerm sigmaH).Gamma ≤ GammaHexa := by
    unfold GammaHexa
    exact le_trans le_sup_left le_sup_left
  exact hle h

lemma T_twoI_mem_hexa : Aff.T (2 * I) ∈ GammaHexa := by
  have h : Aff.T (2 * I) ∈ (flexPerm sigmaV).Gamma := by
    rw [gamma_V]; exact Subgroup.subset_closure rfl
  have hle : (flexPerm sigmaV).Gamma ≤ GammaHexa := by
    unfold GammaHexa
    exact le_trans le_sup_right le_sup_left
  exact hle h

/-- **Proposição 5.5, linha `hexa / todas`.** `Γ_hexa = 2ℤ[i]`.

É aqui que está a diferença com o tri: a face que volta por **dois** eixos
produz duas translações independentes. -/
theorem gammaHexa_eq : GammaHexa = Subgroup.closure {Aff.T (2 : ℂ), Aff.T (2 * I)} := by
  have h2 : Aff.T (2 : ℂ) ∈ Subgroup.closure ({Aff.T (2 : ℂ), Aff.T (2 * I)} : Set Aff) :=
    Subgroup.subset_closure (by simp)
  have h2i : Aff.T (2 * I) ∈ Subgroup.closure ({Aff.T (2 : ℂ), Aff.T (2 * I)} : Set Aff) :=
    Subgroup.subset_closure (by simp)
  apply le_antisymm
  · refine sup_le (sup_le ?_ ?_) ?_
    · rw [gamma_H, Subgroup.closure_le]
      rintro S rfl; exact h2
    · rw [gamma_V, Subgroup.closure_le]
      rintro S rfl; exact h2i
    · rw [Flex.Gamma, GammaOf_eq_closure_base, Subgroup.closure_le]
      rintro S ⟨j, rfl⟩
      fin_cases j
      · show ((flexPerm (sigmaH * sigmaV)).A 0)⁻¹ * (flexPerm (sigmaH * sigmaV)).A 0 ∈ _
        rw [base_eq, dD0, Aff.T_zero]; exact Subgroup.one_mem _
      · show ((flexPerm (sigmaH * sigmaV)).A 0)⁻¹ * (flexPerm (sigmaH * sigmaV)).A 1 ∈ _
        rw [base_eq, dD1]; exact h2
      · show ((flexPerm (sigmaH * sigmaV)).A 0)⁻¹ * (flexPerm (sigmaH * sigmaV)).A 2 ∈ _
        rw [base_eq, dD2, ← Aff.T_mul]
        exact Subgroup.mul_mem _ h2 h2i
      · show ((flexPerm (sigmaH * sigmaV)).A 0)⁻¹ * (flexPerm (sigmaH * sigmaV)).A 3 ∈ _
        rw [base_eq, dD3]; exact h2i
  · rw [Subgroup.closure_le]
    rintro S hS
    rcases hS with h | h
    · rw [h]; exact T_two_mem_hexa
    · rw [Set.mem_singleton_iff] at h
      rw [h]; exact T_twoI_mem_hexa

end Flexagonos
