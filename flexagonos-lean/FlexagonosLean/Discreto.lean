/-
# Discretude do grupo de discrepância (Proposição 3.5)

`Γ_Φ ≤ μ₄ ⋉ ½ℤ[i]` para todo flex de quadrantes `Φ`.

A demonstração do artigo é: `2c_j ∈ ℤ[i]` e `ε_j ∈ μ₄`, logo `2β_j ∈ ℤ[i]`;
o conjunto `{z ↦ ε z + t/2 : ε ∈ μ₄, t ∈ ℤ[i]}` é um grupo (pois `μ₄ ℤ[i] = ℤ[i]`)
que contém todos os `A_j`, e portanto todos os `A_k⁻¹ A_j`.

A classificação subsequente (grupo cíclico finito, friso, ou cristalográfico
`p1`/`p2`/`p4`) usa a classificação dos subgrupos discretos das isometrias
diretas do plano, que não está disponível na Mathlib; formalizamos aqui a
contenção, que é o que os teoremas seguintes usam.
-/
import FlexagonosLean.Discrepancia

namespace Flexagonos

open Complex

/-- O reticulado `½ℤ[i] ⊂ ℂ`. -/
def MeioZi : AddSubgroup ℂ where
  carrier := {z | ∃ m n : ℤ, z = (m + n * I) / 2}
  zero_mem' := ⟨0, 0, by norm_num⟩
  add_mem' := by
    rintro _ _ ⟨m, n, rfl⟩ ⟨m', n', rfl⟩
    exact ⟨m + m', n + n', by push_cast; ring⟩
  neg_mem' := by
    rintro _ ⟨m, n, rfl⟩
    exact ⟨-m, -n, by push_cast; ring⟩

lemma mem_MeioZi {z : ℂ} : z ∈ MeioZi ↔ ∃ m n : ℤ, z = (m + n * I) / 2 := Iff.rfl

/-- `μ₄ · ℤ[i] = ℤ[i]`: multiplicar por `i` preserva `½ℤ[i]`. -/
lemma uI_mul_mem_MeioZi {z : ℂ} (hz : z ∈ MeioZi) : (uI : ℂ) * z ∈ MeioZi := by
  obtain ⟨m, n, rfl⟩ := hz
  refine ⟨-n, m, ?_⟩
  have hI : Complex.I * Complex.I = -1 := Complex.I_mul_I
  rw [uI_val]
  push_cast
  linear_combination ((n : ℂ) / 2) * hI

lemma uI_pow_mul_mem_MeioZi (k : ℕ) {z : ℂ} (hz : z ∈ MeioZi) :
    ((uI ^ k : ℂˣ) : ℂ) * z ∈ MeioZi := by
  induction k with
  | zero => simpa using hz
  | succ k ih =>
      have h : ((uI ^ (k + 1) : ℂˣ) : ℂ) * z = (uI : ℂ) * (((uI ^ k : ℂˣ) : ℂ) * z) := by
        push_cast [pow_succ]; ring
      rw [h]
      exact uI_mul_mem_MeioZi ih

lemma zeta_mul_mem_MeioZi (u : ZMod 4) {z : ℂ} (hz : z ∈ MeioZi) :
    ((zeta u : ℂˣ) : ℂ) * z ∈ MeioZi :=
  uI_pow_mul_mem_MeioZi _ hz

/-- O grupo `μ₄ ⋉ ½ℤ[i]` das aplicações `z ↦ i^u z + t/2`, `t ∈ ℤ[i]`. -/
noncomputable def G0 : Subgroup Aff where
  carrier := {S | (∃ u : ZMod 4, S.a = zeta u) ∧ S.b ∈ MeioZi}
  one_mem' := ⟨⟨0, by simp⟩, MeioZi.zero_mem⟩
  mul_mem' := by
    rintro S T ⟨⟨u, hu⟩, hb⟩ ⟨⟨v, hv⟩, hb'⟩
    refine ⟨⟨u + v, ?_⟩, ?_⟩
    · rw [Aff.mul_a, hu, hv, zeta_add]
    · rw [Aff.mul_b, hu]
      exact MeioZi.add_mem (zeta_mul_mem_MeioZi u hb') hb
  inv_mem' := by
    rintro S ⟨⟨u, hu⟩, hb⟩
    have ha : ((S.a⁻¹ : ℂˣ) : ℂ) = ((zeta (-u) : ℂˣ) : ℂ) := by rw [zeta_neg, hu]
    refine ⟨⟨-u, ?_⟩, ?_⟩
    · rw [Aff.inv_a, hu, zeta_neg]
    · rw [Aff.inv_b, ha, neg_mul]
      exact MeioZi.neg_mem (zeta_mul_mem_MeioZi _ hb)

lemma centro_mem_MeioZi (j : Fin 4) : centro j ∈ MeioZi := by
  have h0 : centro 0 ∈ MeioZi := ⟨1, 1, by rw [centro_zero]; push_cast; ring⟩
  have h1 : centro 1 ∈ MeioZi := ⟨-1, 1, by rw [centro_one]; push_cast; ring⟩
  have h2 : centro 2 ∈ MeioZi := ⟨-1, -1, by rw [centro_two]; push_cast; ring⟩
  have h3 : centro 3 ∈ MeioZi := ⟨1, -1, by rw [centro_three]; push_cast; ring⟩
  fin_cases j <;> assumption

/-- Cada peça `A_j` já pertence a `μ₄ ⋉ ½ℤ[i]`: é o cálculo `2β_j ∈ ℤ[i]`. -/
theorem A_mem_G0 (Φ : Flex) (j : Fin 4) : Φ.A j ∈ G0 :=
  ⟨⟨Φ.ε j, rfl⟩,
    MeioZi.sub_mem (centro_mem_MeioZi _) (zeta_mul_mem_MeioZi _ (centro_mem_MeioZi j))⟩

/-- **Proposição 3.5.** `Γ_Φ ≤ μ₄ ⋉ ½ℤ[i]` para todo `Φ ∈ 𝓕`. -/
theorem gamma_le_G0 (Φ : Flex) : Φ.Gamma ≤ G0 :=
  GammaOf_le_of_mem (A_mem_G0 Φ)

/-- Corolário: o reticulado de translações satisfaz `Λ_Φ ⊆ ½ℤ[i]`. -/
theorem translacao_mem_MeioZi (Φ : Flex) {w : ℂ} (h : Aff.T w ∈ Φ.Gamma) : w ∈ MeioZi :=
  (gamma_le_G0 Φ h).2

end Flexagonos
