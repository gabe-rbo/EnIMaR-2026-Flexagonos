/-
# Os teoremas para os dois flexágonos (Seção 6 do artigo)

Teorema 6.1 (tri-tetraflexágono) e Teorema 6.2 (hexa-tetraflexágono), e a
dicotomia entre eles:

> *As faces que o roteiro de flexão visita uma única vez são tolerantes; as que
> ele revisita são rígidas.*

No tri só a face da frente reaparece, e reaparece ao longo de **um** eixo: o
grupo tem posto `1` e sobram funções inteiras.  No hexa as faces `1` e `2`
reaparecem ao longo de **dois** eixos, e duas translações independentes obrigam
a função a ter polos.
-/
import FlexagonosLean.Retorno
import FlexagonosLean.Liouville

namespace Flexagonos

open Complex

/-! ## Tradução: flexionável ⟺ periódica -/

/-- Flexionável no mapa de retorno `σ_h` ⟺ `2`-periódica. -/
theorem flexionavel_H_iff (f : ℂ → ℂ) (hf : Differentiable ℂ f) :
    Flexionavel (flexPerm sigmaH) f ↔ Function.Periodic f 2 := by
  rw [flexionavel_iff _ _ hf, gamma_H, Subgroup.closure_le]
  constructor
  · intro h z
    have := h (Set.mem_singleton _) z
    simpa using this
  · intro h S hS z
    rw [Set.mem_singleton_iff] at hS
    subst hS
    simpa using h z

/-- Flexionável no mapa de retorno `σ_v` ⟺ `2i`-periódica. -/
theorem flexionavel_V_iff (f : ℂ → ℂ) (hf : Differentiable ℂ f) :
    Flexionavel (flexPerm sigmaV) f ↔ Function.Periodic f (2 * I) := by
  rw [flexionavel_iff _ _ hf, gamma_V, Subgroup.closure_le]
  constructor
  · intro h z
    have := h (Set.mem_singleton _) z
    simpa using this
  · intro h S hS z
    rw [Set.mem_singleton_iff] at hS
    subst hS
    simpa using h z

/-! ## As soluções inteiras exibidas no artigo -/

/-- `e^{iπz}`: a solução inteira mais simples do tri-tetraflexágono (e das faces
`3` e `6` do hexa). -/
noncomputable def solH : ℂ → ℂ := fun z => Complex.exp ((Real.pi : ℂ) * I * z)

/-- `e^{πz}`: a solução inteira das faces `4` e `5` do hexa. -/
noncomputable def solV : ℂ → ℂ := fun z => Complex.exp ((Real.pi : ℂ) * z)

lemma differentiable_solH : Differentiable ℂ solH :=
  Complex.differentiable_exp.comp ((differentiable_const _).mul differentiable_id)

lemma differentiable_solV : Differentiable ℂ solV :=
  Complex.differentiable_exp.comp ((differentiable_const _).mul differentiable_id)

lemma periodic_solH : Function.Periodic solH 2 := by
  intro z
  have h : (Real.pi : ℂ) * I * (z + 2) = (Real.pi : ℂ) * I * z + 2 * (Real.pi : ℂ) * I := by
    ring
  simp only [solH, h, Complex.exp_add, Complex.exp_two_pi_mul_I, mul_one]

lemma periodic_solV : Function.Periodic solV (2 * I) := by
  intro z
  have h : (Real.pi : ℂ) * (z + 2 * I) = (Real.pi : ℂ) * z + 2 * (Real.pi : ℂ) * I := by
    ring
  simp only [solV, h, Complex.exp_add, Complex.exp_two_pi_mul_I, mul_one]

lemma solH_not_const : ¬ ∀ z w : ℂ, solH z = solH w := by
  intro h
  have h01 := h 0 1
  rw [show solH 0 = 1 by simp [solH],
      show solH 1 = -1 by simp [solH, Complex.exp_pi_mul_I]] at h01
  norm_num at h01

/-! ## Teorema 6.1 -/

/-- **Teorema 6.1 (Tri-tetraflexágono).**  Uma função inteira é flexionável nas
três faces do tri-tetraflexágono se e somente se ela é `2`-periódica.

(No artigo, essa condição é reescrita como `f(z) = h(e^{iπz})` com `h` meromorfa
em `ℂ*` arbitrária.  A implicação `f = h ∘ e^{iπ·} ⟹ f` é `2`-periódica é
imediata; a recíproca é a construção da seção do recobrimento `ℂ → ℂ*`.) -/
theorem tri (f : ℂ → ℂ) (hf : Differentiable ℂ f) :
    Flexionavel (flexPerm sigmaH) f ↔ Function.Periodic f 2 :=
  flexionavel_H_iff f hf

/-- Toda função da forma `h(e^{iπz})` com `h` inteira é flexionável no tri. -/
theorem tri_de_h (h : ℂ → ℂ) (hh : Differentiable ℂ h) :
    Flexionavel (flexPerm sigmaH) (h ∘ solH) := by
  refine (tri _ (hh.comp differentiable_solH)).2 fun z => ?_
  simp only [Function.comp_apply, periodic_solH z]

/-- **Teorema 6.1, segunda parte.**  Existem soluções inteiras não constantes
para o tri-tetraflexágono — a mais simples é `f(z) = e^{iπz}`. -/
theorem tri_admite_inteira_nao_constante :
    ∃ f : ℂ → ℂ, Differentiable ℂ f ∧ Flexionavel (flexPerm sigmaH) f ∧
      ¬ ∀ z w : ℂ, f z = f w :=
  ⟨solH, differentiable_solH, (tri solH differentiable_solH).2 periodic_solH, solH_not_const⟩

/-! ## Teorema 6.2 -/

/-- "Flexionável em todas as faces do hexa-tetraflexágono": nos três mapas de
retorno `σ_h`, `σ_v` e `σ_hσ_v`. -/
def FlexionavelHexa (f : ℂ → ℂ) : Prop :=
  Flexionavel (flexPerm sigmaH) f ∧ Flexionavel (flexPerm sigmaV) f ∧
    Flexionavel (flexPerm (sigmaH * sigmaV)) f

/-- **Teorema 6.2, primeira parte.**  Uma função inteira é flexionável em todas
as faces do hexa-tetraflexágono se e somente se ela é elíptica de reticulado
`Λ = 2ℤ[i]`, isto é, periódica de períodos `2` e `2i`. -/
theorem hexa_iff (f : ℂ → ℂ) (hf : Differentiable ℂ f) :
    FlexionavelHexa f ↔ (Function.Periodic f 2 ∧ Function.Periodic f (2 * I)) := by
  have hGamma : FlexionavelHexa f ↔ GammaHexa ≤ Stab f := by
    unfold FlexionavelHexa GammaHexa
    rw [flexionavel_iff _ _ hf, flexionavel_iff _ _ hf, flexionavel_iff _ _ hf,
      sup_le_iff, sup_le_iff, and_assoc]
  rw [hGamma, gammaHexa_eq, Subgroup.closure_le]
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

/-- **Teorema 6.2, segunda parte.**  *Nenhuma função inteira não constante* é
flexionável em todas as faces do hexa-tetraflexágono.

É o teorema de Liouville: as faces `1` e `2` sozinhas já forçam duas translações
independentes, e uma função inteira duplamente periódica é limitada. -/
theorem hexa_sem_inteiras_nao_constantes (f : ℂ → ℂ) (hf : Differentiable ℂ f)
    (h : FlexionavelHexa f) : ∀ z w : ℂ, f z = f w := by
  obtain ⟨p1, p2⟩ := (hexa_iff f hf).1 h
  exact const_of_biperiodic hf p1 p2

/-- **Teorema 6.2, terceira parte.**  Já as faces `3,4,5,6`, tomadas
isoladamente, são satisfeitas por funções inteiras: `e^{iπz}` nas faces `3` e
`6`, `e^{πz}` nas faces `4` e `5`. -/
theorem hexa_faces_isoladas :
    (Flexionavel (flexPerm sigmaH) solH ∧ ¬ ∀ z w : ℂ, solH z = solH w) ∧
    (Flexionavel (flexPerm sigmaV) solV ∧ ¬ ∀ z w : ℂ, solV z = solV w) := by
  refine ⟨⟨(flexionavel_H_iff solH differentiable_solH).2 periodic_solH, solH_not_const⟩,
    ⟨(flexionavel_V_iff solV differentiable_solV).2 periodic_solV, ?_⟩⟩
  intro h
  have h01 := h 0 1
  have e0 : solV 0 = 1 := by simp [solV]
  have e1 : solV 1 = ((Real.exp Real.pi : ℝ) : ℂ) := by
    rw [Complex.ofReal_exp]
    simp [solV]
  rw [e0, e1] at h01
  have h1 : Real.exp Real.pi = 1 := by exact_mod_cast h01.symm
  have h2 : Real.pi + 1 ≤ Real.exp Real.pi := Real.add_one_le_exp Real.pi
  linarith [Real.pi_pos]

/-! ## A dicotomia -/

/-- **A dicotomia (Observação 6.3).**  O tri-tetraflexágono admite soluções
inteiras não constantes; o hexa-tetraflexágono não admite nenhuma.

A rigidez não vem de o flexágono ser complicado; vem de ele ter uma face que
volta por dois caminhos. -/
theorem dicotomia :
    (∃ f : ℂ → ℂ, Differentiable ℂ f ∧ Flexionavel (flexPerm sigmaH) f ∧
        ¬ ∀ z w : ℂ, f z = f w) ∧
    (∀ f : ℂ → ℂ, Differentiable ℂ f → FlexionavelHexa f → ∀ z w : ℂ, f z = f w) :=
  ⟨tri_admite_inteira_nao_constante, hexa_sem_inteiras_nao_constantes⟩

end Flexagonos
