/-
# Flexes de quadrantes (Seção 2 do artigo)

Definição 2.1, a estrutura de grupo `𝓕 ≅ μ₄ ≀ S₄` e a contagem `|𝓕| = 6144`
(Proposição 2.3).

Convenção de índices: o artigo numera os quadrantes `1,2,3,4` no sentido
cartesiano; aqui usamos `Fin 4` com `0,1,2,3` correspondendo a `Q₁,Q₂,Q₃,Q₄`.
-/
import FlexagonosLean.Mu4

namespace Flexagonos

open Complex

/-- Os centros dos quatro quadrantes:
`c₁ = (1+i)/2`, `c₂ = (-1+i)/2`, `c₃ = (-1-i)/2`, `c₄ = (1-i)/2`. -/
noncomputable def centro : Fin 4 → ℂ :=
  ![(1 + I) / 2, (-1 + I) / 2, (-1 - I) / 2, (1 - I) / 2]

@[simp] lemma centro_zero : centro 0 = (1 + I) / 2 := rfl
@[simp] lemma centro_one : centro 1 = (-1 + I) / 2 := rfl
@[simp] lemma centro_two : centro 2 = (-1 - I) / 2 := rfl
@[simp] lemma centro_three : centro 3 = (1 - I) / 2 := rfl

/-- **Definição 2.1.** Um *flex de quadrantes* é o dado de uma permutação `σ`
dos quatro quadrantes e de uma rotação `ε_j ∈ μ₄` para cada quadrante.

A aplicação `Φ : Q → Q` correspondente é `Φ|_{Q̊_j} = A_j`, com
`A_j(z) = ε_j (z - c_j) + c_{σ(j)}` (ver `Flex.A`). -/
@[ext]
structure Flex where
  /-- A permutação dos quadrantes. -/
  σ : Equiv.Perm (Fin 4)
  /-- A rotação de cada quadrante, como expoente de `i`. -/
  ε : Fin 4 → ZMod 4

namespace Flex

/-! ## A estrutura de produto entrelaçado

O produto é exatamente a lei do produto entrelaçado `μ₄ ≀ S₄` exibida na
demonstração da Proposição 2.3:
`(σ;ε) ∘ (σ';ε') = (σσ'; (ε_{σ'(j)} ε'_j)_j)`. -/

instance : Mul Flex := ⟨fun Φ Ψ => ⟨Φ.σ * Ψ.σ, fun j => Φ.ε (Ψ.σ j) + Ψ.ε j⟩⟩
instance : One Flex := ⟨⟨1, fun _ => 0⟩⟩
instance : Inv Flex := ⟨fun Φ => ⟨Φ.σ⁻¹, fun j => -Φ.ε (Φ.σ⁻¹ j)⟩⟩

@[simp] lemma mul_σ (Φ Ψ : Flex) : (Φ * Ψ).σ = Φ.σ * Ψ.σ := rfl
@[simp] lemma mul_ε (Φ Ψ : Flex) (j : Fin 4) : (Φ * Ψ).ε j = Φ.ε (Ψ.σ j) + Ψ.ε j := rfl
@[simp] lemma one_σ : (1 : Flex).σ = 1 := rfl
@[simp] lemma one_ε (j : Fin 4) : (1 : Flex).ε j = 0 := rfl
@[simp] lemma inv_σ (Φ : Flex) : Φ⁻¹.σ = Φ.σ⁻¹ := rfl
@[simp] lemma inv_ε (Φ : Flex) (j : Fin 4) : Φ⁻¹.ε j = -Φ.ε (Φ.σ⁻¹ j) := rfl

instance : Group Flex where
  mul_assoc Φ Ψ Χ := by
    ext j
    · simp [mul_assoc]
    · simp [add_assoc]
  one_mul Φ := by ext j <;> simp
  mul_one Φ := by ext j <;> simp
  inv_mul_cancel Φ := by ext j <;> simp

/-! ## Cardinalidade -/

/-- A bijeção `Φ ↦ (σ, ε)` da demonstração da Proposição 2.3. -/
def equivProd : Flex ≃ Equiv.Perm (Fin 4) × (Fin 4 → ZMod 4) where
  toFun Φ := (Φ.σ, Φ.ε)
  invFun p := ⟨p.1, p.2⟩
  left_inv _ := rfl
  right_inv _ := rfl

instance : Fintype Flex := Fintype.ofEquiv _ equivProd.symm
instance : DecidableEq Flex := fun _ _ => decidable_of_iff _ equivProd.apply_eq_iff_eq

/-- **Proposição 2.3.** `|𝓕| = 4^4 · 4! = 6144`. -/
theorem card_flex : Fintype.card Flex = 6144 := by
  rw [Fintype.card_congr equivProd, Fintype.card_prod, Fintype.card_perm]
  simp [Nat.factorial]

/-! ## As peças `A_j` -/

/-- A peça `A_j(z) = ε_j (z - c_j) + c_{σ(j)} = ε_j z + β_j`, com
`β_j = c_{σ(j)} - ε_j c_j`  (equação (2.1) do artigo). -/
noncomputable def A (Φ : Flex) (j : Fin 4) : Aff :=
  ⟨zeta (Φ.ε j), centro (Φ.σ j) - (zeta (Φ.ε j) : ℂ) * centro j⟩

@[simp] lemma A_a (Φ : Flex) (j : Fin 4) : (Φ.A j).a = zeta (Φ.ε j) := rfl
@[simp] lemma A_b (Φ : Flex) (j : Fin 4) :
    (Φ.A j).b = centro (Φ.σ j) - (zeta (Φ.ε j) : ℂ) * centro j := rfl

/-- `A_j` leva o centro `c_j` no centro `c_{σ(j)}`. -/
@[simp] lemma A_act_centro (Φ : Flex) (j : Fin 4) :
    (Φ.A j).act (centro j) = centro (Φ.σ j) := by
  simp only [Aff.act_apply, A_a, A_b]
  ring

lemma A_act (Φ : Flex) (j : Fin 4) (z : ℂ) :
    (Φ.A j).act z = (zeta (Φ.ε j) : ℂ) * (z - centro j) + centro (Φ.σ j) := by
  simp only [Aff.act_apply, A_a, A_b]
  ring

end Flex

end Flexagonos
