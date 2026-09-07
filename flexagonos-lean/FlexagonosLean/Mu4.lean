/-
# O grupo `μ₄` das rotações de ordem 4

`μ₄ = {1, i, -1, -i}` é o grupo de rotações que aparece na Definição 2.1 do
artigo: a restrição `ε_j ∈ μ₄` é forçada pelo facto de `A_j` levar um quadrado
do reticulado em outro.

Parametrizamos `μ₄` por `ZMod 4` via `zeta u = i^u`; isto torna a aritmética do
grupo de pontos decidível e faz `zeta` um homomorfismo de `(ZMod 4, +)` em `ℂˣ`.
-/
import FlexagonosLean.Aff

namespace Flexagonos

open Complex

/-- A unidade imaginária vista como unidade do anel `ℂ`. -/
noncomputable def uI : ℂˣ :=
  ⟨Complex.I, -Complex.I, by simp [Complex.I_mul_I], by simp [Complex.I_mul_I]⟩

@[simp] lemma uI_val : (uI : ℂ) = Complex.I := rfl

@[simp] lemma uI_pow_four : uI ^ 4 = 1 := by
  ext
  simp [uI, pow_succ, Complex.I_mul_I]

lemma uI_pow_mod (n : ℕ) : uI ^ (n % 4) = uI ^ n := by
  conv_rhs => rw [← Nat.div_add_mod n 4]
  rw [pow_add, pow_mul, uI_pow_four, one_pow, one_mul]

/-- `zeta u = i^u`, a parametrização de `μ₄` por `ZMod 4`. -/
noncomputable def zeta (u : ZMod 4) : ℂˣ := uI ^ u.val

@[simp] lemma zeta_zero : zeta 0 = 1 := by simp [zeta]

lemma zeta_add (u v : ZMod 4) : zeta (u + v) = zeta u * zeta v := by
  simp only [zeta, ZMod.val_add, ← pow_add]
  exact uI_pow_mod _

lemma zeta_neg (u : ZMod 4) : zeta (-u) = (zeta u)⁻¹ := by
  rw [eq_inv_iff_mul_eq_one, ← zeta_add, neg_add_cancel, zeta_zero]

lemma zeta_sub (u v : ZMod 4) : zeta (u - v) = zeta u * (zeta v)⁻¹ := by
  rw [sub_eq_add_neg, zeta_add, zeta_neg]

/-- `zeta` como homomorfismo de monoides de `Multiplicative (ZMod 4)` em `ℂˣ`. -/
noncomputable def zetaHom : Multiplicative (ZMod 4) →* ℂˣ where
  toFun u := zeta (Multiplicative.toAdd u)
  map_one' := zeta_zero
  map_mul' u v := zeta_add _ _

lemma zeta_pow_four (u : ZMod 4) : (zeta u) ^ 4 = 1 := by
  rw [zeta, ← pow_mul, mul_comm, pow_mul, uI_pow_four, one_pow]

end Flexagonos
