/-
# Os Teoremas 6.1 e 6.2 na categoria meromorfa, e `℘` como solução

Com o Teorema 3.2 meromorfo (`Meromorfo.lean`) e a `℘` de Weierstrass
(`Elipticas.lean`), os teoremas dos dois flexágonos passam a valer para funções
meromorfas, e `℘(z;2ℤ[i])` torna-se literalmente uma **solução flexionável** do
hexa-tetraflexágono — não constante, e necessariamente com polos.
-/
import FlexagonosLean.Elipticas
import FlexagonosLean.Meromorfo
import FlexagonosLean.Flexagonos

namespace Flexagonos

open Complex

/-! ## Os dois flexágonos, para funções meromorfas -/

/-- **Teorema 6.1, versão meromorfa.**  Uma função meromorfa é flexionável nas
três faces do tri-tetraflexágono se e somente se é `2`-periódica. -/
theorem triMer (f : ℂ → ℂ) (hf : MerNF f) :
    FlexionavelMer (flexPerm sigmaH) f ↔ Function.Periodic f 2 := by
  rw [flexionavelMer_iff _ _ hf, gamma_H, Subgroup.closure_le]
  constructor
  · intro h z
    have := h (Set.mem_singleton _) z
    simpa using this
  · intro h S hS z
    rw [Set.mem_singleton_iff] at hS
    subst hS
    simpa using h z

/-- "Flexionável em todas as faces do hexa-tetraflexágono", para `f` meromorfa. -/
def FlexionavelMerHexa (f : ℂ → ℂ) : Prop :=
  FlexionavelMer (flexPerm sigmaH) f ∧ FlexionavelMer (flexPerm sigmaV) f ∧
    FlexionavelMer (flexPerm (sigmaH * sigmaV)) f

/-- **Teorema 6.2, versão meromorfa.**  Uma função meromorfa é flexionável em
todas as faces do hexa-tetraflexágono se e somente se é elíptica de reticulado
`Λ = 2ℤ[i]`. -/
theorem hexaMer_iff (f : ℂ → ℂ) (hf : MerNF f) :
    FlexionavelMerHexa f ↔ (Function.Periodic f 2 ∧ Function.Periodic f (2 * I)) := by
  have hGamma : FlexionavelMerHexa f ↔ GammaHexa ≤ Stab f := by
    unfold FlexionavelMerHexa GammaHexa
    rw [flexionavelMer_iff _ _ hf, flexionavelMer_iff _ _ hf, flexionavelMer_iff _ _ hf,
      sup_le_iff, sup_le_iff, and_assoc]
  exact hGamma.trans (mem_invariantes.symm.trans mem_invariantes_gammaHexa)

/-! ## `℘` e `℘'` estão em forma normal

O valor de `℘` num ponto do reticulado é `0` (`weierstrassP_coe`) e a sua ordem
aí é `-2` (`order_weierstrassP`): é exatamente a forma normal.  Para `℘'` a
ordem é `-3`, pela regra da ordem da derivada. -/

theorem merNF_wp : MerNF wp := by
  intro x _
  by_cases hx : x ∈ hexaPair.lattice
  · rw [meromorphicNFAt_iff_analyticAt_or]
    refine Or.inr ⟨hexaPair.meromorphic_weierstrassP x, ?_, ?_⟩
    · have hord : meromorphicOrderAt wp x = ((-2 : ℤ) : WithTop ℤ) := by
        rw [show wp = hexaPair.weierstrassP from rfl, hexaPair.order_weierstrassP x hx]
        norm_num
      rw [hord]
      first
        | exact_mod_cast (by norm_num : (-2 : ℤ) < 0)
        | decide
        | simp
    · exact hexaPair.weierstrassP_coe ⟨x, hx⟩
  · exact (hexaPair.analyticOnNhd_weierstrassP x hx).meromorphicNFAt

theorem order_wp' {x : ℂ} (hx : x ∈ hexaPair.lattice) :
    meromorphicOrderAt wp' x = ((-3 : ℤ) : WithTop ℤ) := by
  have h2 : meromorphicOrderAt hexaPair.weierstrassP x = ((-2 : ℤ) : WithTop ℤ) := by
    rw [hexaPair.order_weierstrassP x hx]; norm_num
  have h := meromorphicOrderAt_deriv_eq_sub_one (𝕜 := ℂ) (n := -2) (by norm_num) h2
  rw [hexaPair.deriv_weierstrassP] at h
  rw [show wp' = hexaPair.derivWeierstrassP from rfl, h]
  norm_num

theorem merNF_wp' : MerNF wp' := by
  intro x _
  by_cases hx : x ∈ hexaPair.lattice
  · rw [meromorphicNFAt_iff_analyticAt_or]
    refine Or.inr ⟨hexaPair.meromorphic_derivWeierstrassP x, ?_, ?_⟩
    · rw [order_wp' hx]
      first
        | exact_mod_cast (by norm_num : (-3 : ℤ) < 0)
        | decide
        | simp
    · exact hexaPair.derivWeierstrassP_coe ⟨x, hx⟩
  · exact (hexaPair.analyticOnNhd_derivWeierstrassP x hx).meromorphicNFAt

/-! ## `℘` é uma solução do hexa-tetraflexágono -/

/-- **`℘(z; 2ℤ[i])` é flexionável em todas as faces do hexa-tetraflexágono.** -/
theorem wp_flexionavelHexa : FlexionavelMerHexa wp :=
  (hexaMer_iff wp merNF_wp).2 ⟨periodic_wp_two, periodic_wp_twoI⟩

/-- **`℘'(z; 2ℤ[i])` também.** -/
theorem wp'_flexionavelHexa : FlexionavelMerHexa wp' :=
  (hexaMer_iff wp' merNF_wp').2 ⟨periodic_wp'_two, periodic_wp'_twoI⟩

/-- `℘` não é constante: tem um polo na origem — que, como observa o artigo,
cai exatamente no cruzamento dos dois cortes, escondendo-se na dobra. -/
theorem wp_not_const : ¬ ∀ z w : ℂ, wp z = wp w := by
  intro h
  have hconst : wp = fun _ : ℂ => wp 0 := funext fun z => h z 0
  have hcont : ContinuousAt hexaPair.weierstrassP 0 := by
    rw [show hexaPair.weierstrassP = wp from rfl, hconst]
    exact continuousAt_const
  exact hexaPair.not_continuousAt_weierstrassP 0 (Submodule.zero_mem _) hcont

/-! ## A dicotomia, na sua forma completa -/

/-- **O Teorema 6.2 na sua forma final.**  O hexa-tetraflexágono *tem* soluções
não constantes — `℘` é uma delas — mas **nenhuma** delas é inteira: toda
solução não trivial tem polos.

É o contraste com o tri-tetraflexágono, cuja solução mais simples, `e^{iπz}`, é
inteira.  A rigidez não vem de o flexágono ser complicado; vem de ele ter uma
face que volta por dois caminhos. -/
theorem hexa_dicotomia_completa :
    (∃ f : ℂ → ℂ, MerNF f ∧ FlexionavelMerHexa f ∧ ¬ ∀ z w : ℂ, f z = f w) ∧
    (∀ f : ℂ → ℂ, Differentiable ℂ f → FlexionavelMerHexa f → ∀ z w : ℂ, f z = f w) := by
  refine ⟨⟨wp, merNF_wp, wp_flexionavelHexa, wp_not_const⟩, ?_⟩
  intro f hf hflex
  obtain ⟨p1, p2⟩ := (hexaMer_iff f (merNF_of_differentiable hf)).1 hflex
  exact const_of_biperiodic hf p1 p2

/-- A dicotomia entre os dois flexágonos, agora na categoria meromorfa dos dois
lados: o tri admite solução **inteira** não constante, o hexa admite solução
meromorfa não constante mas nenhuma inteira. -/
theorem dicotomia_mer :
    (∃ f : ℂ → ℂ, Differentiable ℂ f ∧ FlexionavelMer (flexPerm sigmaH) f ∧
        ¬ ∀ z w : ℂ, f z = f w) ∧
    (∃ f : ℂ → ℂ, MerNF f ∧ FlexionavelMerHexa f ∧ ¬ ∀ z w : ℂ, f z = f w) ∧
    (∀ f : ℂ → ℂ, Differentiable ℂ f → FlexionavelMerHexa f → ∀ z w : ℂ, f z = f w) := by
  refine ⟨⟨solH, differentiable_solH, ?_, solH_not_const⟩, hexa_dicotomia_completa.1,
    hexa_dicotomia_completa.2⟩
  exact (triMer solH (merNF_of_differentiable differentiable_solH)).2 periodic_solH

end Flexagonos
