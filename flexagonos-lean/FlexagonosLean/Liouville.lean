/-
# Liouville: posto 2 mata as soluções inteiras

A última linha da demonstração do Teorema 4.1 e a afirmação central do
Teorema 6.2: *uma função inteira duplamente periódica é limitada, logo
constante.*

Isolamos aqui o argumento, com o reticulado `Λ = 2ℤ[i]` que ocorre no
hexa-tetraflexágono.
-/
import FlexagonosLean.Aff

namespace Flexagonos

open Complex Set

/-- Redução ao domínio fundamental `[0,2) × [0,2)`. -/
private lemma exists_repr {f : ℂ → ℂ} (h1 : Function.Periodic f 2)
    (h2 : Function.Periodic f (2 * I)) (z : ℂ) :
    ∃ w : ℂ, f z = f w ∧ |w.re| ≤ 2 ∧ |w.im| ≤ 2 := by
  set n : ℤ := ⌊z.re / 2⌋ with hn
  set m : ℤ := ⌊z.im / 2⌋ with hm
  refine ⟨z - (n : ℂ) * 2 - (m : ℂ) * (2 * I), ?_, ?_, ?_⟩
  · rw [h2.sub_int_mul_eq m, h1.sub_int_mul_eq n]
  · have hre : (z - (n : ℂ) * 2 - (m : ℂ) * (2 * I)).re = z.re - 2 * n := by
      simp; ring
    rw [hre, abs_le]
    have h₁ : (n : ℝ) ≤ z.re / 2 := by exact_mod_cast Int.floor_le (z.re / 2)
    have h₂ : z.re / 2 < (n : ℝ) + 1 := by exact_mod_cast Int.lt_floor_add_one (z.re / 2)
    constructor <;> linarith
  · have him : (z - (n : ℂ) * 2 - (m : ℂ) * (2 * I)).im = z.im - 2 * m := by
      simp; ring
    rw [him, abs_le]
    have h₁ : (m : ℝ) ≤ z.im / 2 := by exact_mod_cast Int.floor_le (z.im / 2)
    have h₂ : z.im / 2 < (m : ℝ) + 1 := by exact_mod_cast Int.lt_floor_add_one (z.im / 2)
    constructor <;> linarith

/-- **Liouville para funções duplamente periódicas.**  Uma função inteira
periódica de períodos `2` e `2i` é constante.

É a razão pela qual, no posto `2`, "toda solução não trivial tem polos": o
retrato de fase precisa exibir singularidades (Corolário 4.3). -/
theorem const_of_biperiodic {f : ℂ → ℂ} (hf : Differentiable ℂ f)
    (h1 : Function.Periodic f 2) (h2 : Function.Periodic f (2 * I)) :
    ∀ z w, f z = f w := by
  -- `f` é limitada, pois toda `z` é congruente a um ponto de um compacto.
  obtain ⟨C, hC⟩ :=
    (isCompact_closedBall (0 : ℂ) 4).exists_bound_of_continuousOn
      hf.continuous.continuousOn
  have hbound : ∀ z, ‖f z‖ ≤ C := by
    intro z
    obtain ⟨w, hw, hre, him⟩ := exists_repr h1 h2 z
    have hnorm : ‖w‖ ≤ 4 := by
      calc ‖w‖ ≤ |w.re| + |w.im| := Complex.norm_le_abs_re_add_abs_im w
        _ ≤ 4 := by linarith
    have : w ∈ Metric.closedBall (0 : ℂ) 4 := by
      simpa [Metric.mem_closedBall, dist_eq_norm] using hnorm
    rw [hw]
    exact hC w this
  have hb : Bornology.IsBounded (range f) := by
    rw [isBounded_iff_forall_norm_le]
    exact ⟨C, by rintro x ⟨z, rfl⟩; exact hbound z⟩
  exact fun z w => hf.apply_eq_apply_of_bounded hb z w

end Flexagonos
