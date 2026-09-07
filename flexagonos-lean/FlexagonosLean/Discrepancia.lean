/-
# O grupo de discrepância (Seção 3 do artigo)

Definição 3.1 e Lema 3.4.
-/
import FlexagonosLean.Flex

namespace Flexagonos

open Complex

/-- O conjunto dos geradores `A_k⁻¹ ∘ A_j` de uma família de peças. -/
def geradores (A : Fin 4 → Aff) : Set Aff := {S | ∃ j k, S = (A k)⁻¹ * A j}

/-- **Definição 3.1.** O *grupo de discrepância* de uma família de peças
`(A_j)_j` é `⟨A_k⁻¹ ∘ A_j : 1 ≤ j,k ≤ 4⟩`. -/
def GammaOf (A : Fin 4 → Aff) : Subgroup Aff := Subgroup.closure (geradores A)

/-- O grupo de discrepância `Γ_Φ` de um flex. -/
noncomputable def Flex.Gamma (Φ : Flex) : Subgroup Aff := GammaOf Φ.A

lemma gerador_mem (A : Fin 4 → Aff) (j k : Fin 4) : (A k)⁻¹ * A j ∈ GammaOf A :=
  Subgroup.subset_closure ⟨j, k, rfl⟩

lemma GammaOf_le {A : Fin 4 → Aff} {H : Subgroup Aff}
    (h : ∀ j k, (A k)⁻¹ * A j ∈ H) : GammaOf A ≤ H := by
  refine Subgroup.closure_le _ |>.2 ?_
  rintro S ⟨j, k, rfl⟩
  exact h j k

/-- Se todas as peças pertencem a um subgrupo `H`, o mesmo vale para `Γ`. -/
lemma GammaOf_le_of_mem {A : Fin 4 → Aff} {H : Subgroup Aff} (h : ∀ j, A j ∈ H) :
    GammaOf A ≤ H :=
  GammaOf_le fun j k => H.mul_mem (H.inv_mem (h k)) (h j)

/-- `Γ` é gerado apenas pelos quatro elementos `A_1⁻¹ A_j`, pois
`A_k⁻¹ A_j = (A_1⁻¹ A_k)⁻¹ (A_1⁻¹ A_j)`. -/
theorem GammaOf_eq_closure_base (A : Fin 4 → Aff) :
    GammaOf A = Subgroup.closure {S | ∃ j, S = (A 0)⁻¹ * A j} := by
  apply le_antisymm
  · refine GammaOf_le fun j k => ?_
    have hj : (A 0)⁻¹ * A j ∈ Subgroup.closure {S | ∃ j, S = (A 0)⁻¹ * A j} :=
      Subgroup.subset_closure ⟨j, rfl⟩
    have hk : (A 0)⁻¹ * A k ∈ Subgroup.closure {S | ∃ j, S = (A 0)⁻¹ * A j} :=
      Subgroup.subset_closure ⟨k, rfl⟩
    have : (A k)⁻¹ * A j = ((A 0)⁻¹ * A k)⁻¹ * ((A 0)⁻¹ * A j) := by group
    rw [this]
    exact Subgroup.mul_mem _ (Subgroup.inv_mem _ hk) hj
  · rw [Subgroup.closure_le]
    rintro S ⟨j, rfl⟩
    exact gerador_mem A j 0

/-- **Lema 3.4.** `Γ` não vê um fator comum à esquerda: se `ρ` é uma isometria
direta qualquer, a família `(ρ ∘ A_j)_j` tem o mesmo grupo de discrepância.

Em particular, se `ρ(z) = i^u z` preserva `Q`, então `Γ_{ρ∘Φ} = Γ_Φ`: as
ambiguidades de convenção sobre "como o flexágono é segurado" são irrelevantes. -/
theorem GammaOf_left_mul (ρ : Aff) (A : Fin 4 → Aff) :
    GammaOf (fun j => ρ * A j) = GammaOf A := by
  unfold GammaOf geradores
  congr 1
  ext S
  constructor
  · rintro ⟨j, k, rfl⟩
    exact ⟨j, k, by group⟩
  · rintro ⟨j, k, rfl⟩
    exact ⟨j, k, by group⟩

end Flexagonos
