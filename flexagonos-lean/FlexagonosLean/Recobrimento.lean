/-
# A seção do recobrimento `ℂ → ℂ*` (Teorema 4.1, linha posto 1, `n = 1`)

O Teorema 4.1 do artigo afirma, na linha `(posto 1, n = 1)`, que as funções
`Γ`-invariantes são exatamente as da forma `h(e^{2πi(z-p)/ω})`.  A implicação
fácil é imediata; este arquivo demonstra a recíproca, que é a construção da
seção do recobrimento `q_ω : ℂ → ℂ*`, `q_ω(z) = e^{2πi z/ω}`.

A dificuldade é que `Complex.log` tem corte no eixo real negativo, de modo que
a fórmula `h(w) = f(ω log w / 2πi)` não é obviamente holomorfa ali.  A saída é
que essa **mesma** `h` admite uma segunda expressão, com o logaritmo do ponto
antípoda, válida no complementar do corte oposto; as duas expressões coincidem
porque `f` é `ω`-periódica, e os dois abertos cobrem `ℂ*`.

Com isto o **Teorema 6.1** fica na forma exata do artigo:
`f(z) = h(e^{iπz})`, com `h` holomorfa em `ℂ*` arbitrária.
-/
import FlexagonosLean.Flexagonos

namespace Flexagonos

open Complex

variable {ω : ℂ}

/-! ## O recobrimento -/

/-- O recobrimento `q_ω(z) = e^{2πi z/ω}` de `ℂ*` pelo plano. -/
noncomputable def q (ω : ℂ) (z : ℂ) : ℂ := Complex.exp (2 * (Real.pi : ℂ) * I * z / ω)

lemma q_ne_zero (ω z : ℂ) : q ω z ≠ 0 := Complex.exp_ne_zero _

lemma two_pi_I_ne_zero : (2 : ℂ) * (Real.pi : ℂ) * I ≠ 0 :=
  mul_ne_zero (mul_ne_zero two_ne_zero (Complex.ofReal_ne_zero.2 Real.pi_ne_zero))
    Complex.I_ne_zero

/-- Iterar a periodicidade sobre `ℤ`. -/
private lemma per_int {f : ℂ → ℂ} (hper : Function.Periodic f ω) (n : ℤ) (u : ℂ) :
    f (u + n * ω) = f u := (hper.int_mul n) u

/-- As fibras do recobrimento são as classes módulo `ωℤ`. -/
lemma q_eq_q_iff (hω : ω ≠ 0) (z z' : ℂ) :
    q ω z = q ω z' ↔ ∃ n : ℤ, z = z' + n * ω := by
  rw [q, q, Complex.exp_eq_exp_iff_exists_int]
  constructor
  · rintro ⟨n, hn⟩
    field_simp at hn
    exact ⟨n, by linear_combination hn⟩
  · rintro ⟨n, rfl⟩
    exact ⟨n, by field_simp⟩

/-! ## A seção -/

/-- A seção `h(w) = f(ω · log w / 2πi)`. -/
noncomputable def secao (ω : ℂ) (f : ℂ → ℂ) (w : ℂ) : ℂ :=
  f (Complex.log w * ω / (2 * (Real.pi : ℂ) * I))

/-- O ramo principal é de facto uma seção de `q_ω`. -/
lemma q_ramo_principal (hω : ω ≠ 0) {w : ℂ} (hw : w ≠ 0) :
    q ω (Complex.log w * ω / (2 * (Real.pi : ℂ) * I)) = w := by
  rw [q]
  have harg : 2 * (Real.pi : ℂ) * I * (Complex.log w * ω / (2 * (Real.pi : ℂ) * I)) / ω
      = Complex.log w := by
    field_simp
  rw [harg, Complex.exp_log hw]

/-- O ramo girado, obtido do logaritmo do ponto antípoda, é a outra seção. -/
lemma q_ramo_girado (hω : ω ≠ 0) {w : ℂ} (hw : w ≠ 0) :
    q ω (Complex.log (-w) * ω / (2 * (Real.pi : ℂ) * I) + ω / 2) = w := by
  have hnw : -w ≠ 0 := neg_ne_zero.2 hw
  rw [q]
  have harg : 2 * (Real.pi : ℂ) * I *
      (Complex.log (-w) * ω / (2 * (Real.pi : ℂ) * I) + ω / 2) / ω
      = Complex.log (-w) + (Real.pi : ℂ) * I := by
    field_simp
  rw [harg, Complex.exp_add, Complex.exp_log hnw, Complex.exp_pi_mul_I]
  ring

/-- **A propriedade que define a seção.**  Para *qualquer* `z` na fibra de `w`,
`secao ω f w = f z`.  É aqui que a periodicidade de `f` entra: a ambiguidade da
escolha do logaritmo é exatamente `ωℤ`, e `f` não a vê. -/
theorem secao_apply (hω : ω ≠ 0) {f : ℂ → ℂ} (hper : Function.Periodic f ω) {w z : ℂ}
    (hz : q ω z = w) : secao ω f w = f z := by
  have hw : w ≠ 0 := hz ▸ q_ne_zero ω z
  have h1 : q ω (Complex.log w * ω / (2 * (Real.pi : ℂ) * I)) = q ω z := by
    rw [q_ramo_principal hω hw, hz]
  obtain ⟨n, hn⟩ := (q_eq_q_iff hω _ _).1 h1
  rw [secao, hn]
  exact per_int hper n z

/-- A seção é holomorfa em todo `ℂ*` — inclusive sobre o corte do ramo
principal, onde se usa o ramo girado. -/
theorem differentiableAt_secao (hω : ω ≠ 0) {f : ℂ → ℂ} (hf : Differentiable ℂ f)
    (hper : Function.Periodic f ω) {w : ℂ} (hw : w ≠ 0) :
    DifferentiableAt ℂ (secao ω f) w := by
  by_cases hs : w ∈ Complex.slitPlane
  · -- Fora do corte, a própria fórmula que define `secao` é holomorfa.
    have hlog : DifferentiableAt ℂ Complex.log w := Complex.differentiableAt_log hs
    exact DifferentiableAt.comp w (hf _) ((hlog.mul_const ω).div_const _)
  · -- Sobre o corte: `w` é real negativo, logo `-w` está no plano fendido.
    have hs' : w.re ≤ 0 ∧ w.im = 0 := by
      rw [Complex.mem_slitPlane_iff] at hs
      push_neg at hs
      exact ⟨hs.1, hs.2⟩
    have hre : w.re < 0 := by
      rcases lt_or_eq_of_le hs'.1 with h | h
      · exact h
      · exfalso
        exact hw (by apply Complex.ext <;> simp [h, hs'.2])
    have hns : -w ∈ Complex.slitPlane := by
      rw [Complex.mem_slitPlane_iff]
      left
      simpa using hre
    -- A seção coincide, perto de `w`, com a expressão do ramo girado.
    set g : ℂ → ℂ := fun v => f (Complex.log (-v) * ω / (2 * (Real.pi : ℂ) * I) + ω / 2) with hg
    have hEq : secao ω f =ᶠ[nhds w] g := by
      filter_upwards [isOpen_ne.mem_nhds hw] with v hv
      exact secao_apply hω hper (q_ramo_girado hω hv)
    have hgd : DifferentiableAt ℂ g w := by
      have hneg : DifferentiableAt ℂ (fun v : ℂ => -v) w := differentiable_neg.differentiableAt
      have hlog : DifferentiableAt ℂ (fun v : ℂ => Complex.log (-v)) w :=
        DifferentiableAt.comp w (Complex.differentiableAt_log hns) hneg
      exact DifferentiableAt.comp w (hf _) (((hlog.mul_const ω).div_const _).add_const _)
    exact hgd.congr_of_eventuallyEq hEq

/-! ## Teorema 4.1, linha `(posto 1, n = 1)` -/

/-- **Teorema 4.1, linha `(posto 1, n = 1)`.**  Uma função inteira é
`ω`-periódica se e somente se é da forma `h(e^{2πi z/ω})` com `h` holomorfa em
`ℂ*`.  (`h` percorre todas as funções holomorfas do argumento indicado.) -/
theorem periodic_iff_secao (hω : ω ≠ 0) (f : ℂ → ℂ) (hf : Differentiable ℂ f) :
    Function.Periodic f ω ↔
      ∃ h : ℂ → ℂ, (∀ w : ℂ, w ≠ 0 → DifferentiableAt ℂ h w) ∧ ∀ z : ℂ, f z = h (q ω z) := by
  constructor
  · intro hper
    exact ⟨secao ω f, fun w hw => differentiableAt_secao hω hf hper hw,
      fun z => (secao_apply hω hper rfl).symm⟩
  · rintro ⟨h, -, hfh⟩ z
    rw [hfh, hfh]
    congr 1
    rw [q, q]
    have harg : 2 * (Real.pi : ℂ) * I * (z + ω) / ω
        = 2 * (Real.pi : ℂ) * I * z / ω + 2 * (Real.pi : ℂ) * I := by
      field_simp
    rw [harg, Complex.exp_add, Complex.exp_two_pi_mul_I, mul_one]

/-! ## A forma final do Teorema 6.1 -/

lemma q_two_eq_solH (z : ℂ) : q 2 z = solH z := by
  rw [q, solH]
  congr 1
  ring

/-- **Teorema 6.1, na forma do artigo.**  Uma função inteira é flexionável nas
três faces do tri-tetraflexágono se e somente se

`f(z) = h(e^{iπz})`,   com `h` holomorfa em `ℂ*` arbitrária.

O espaço das soluções é, portanto, de dimensão infinita. -/
theorem tri_forma_final (f : ℂ → ℂ) (hf : Differentiable ℂ f) :
    Flexionavel (flexPerm sigmaH) f ↔
      ∃ h : ℂ → ℂ, (∀ w : ℂ, w ≠ 0 → DifferentiableAt ℂ h w) ∧
        ∀ z : ℂ, f z = h (solH z) := by
  rw [tri f hf, periodic_iff_secao (two_ne_zero) f hf]
  simp only [q_two_eq_solH]

end Flexagonos
