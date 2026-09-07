/-
# O Teorema 3.2 na categoria meromorfa

O artigo enuncia o Teorema 3.2 para `f` **meromorfa**; a formalização anterior
trabalhava com `f` inteira, que basta para o conteúdo dos Teoremas 6.1 e 6.2
(a existência ou inexistência de soluções inteiras) mas não permite dizer que
`℘` é flexionável.  Este arquivo remove essa limitação.

## A questão dos valores nos polos

Na Mathlib uma função meromorfa é uma função genuína `ℂ → ℂ`, com um valor
arbitrário ("lixo") em cada polo.  Duas funções meromorfas que coincidem num
aberto coincidem, portanto, apenas **fora de um conjunto discreto** — nos polos
os valores podem divergir.  Para que as igualdades (ii) e (iii) do Teorema 3.2
sejam igualdades de funções, e não apenas fora dos polos, trabalhamos com o
representante canónico: a *forma normal* (`MeromorphicNFOn`), que toma o valor
`0` em cada polo.  Toda função meromorfa tem um e um só representante nesta
forma, de modo que não há perda de generalidade — é exatamente a escolha
implícita quando se fala do *corpo* das funções meromorfas.

Note-se que a função `G` da Definição 2.4 **não** precisa de estar em forma
normal: só `f` precisa.
-/
import FlexagonosLean.Caracterizacao

namespace Flexagonos

open Complex Set Filter Topology

/-! ## Princípio da identidade para funções meromorfas -/

/-- **Princípio da identidade, forma "a menos dos polos".**  Duas funções
meromorfas num aberto pré-conexo `U` que coincidem num aberto não vazio
`V ⊆ U` coincidem, perto de cada ponto de `U`, fora desse ponto.

A demonstração é a habitual: o conjunto onde a diferença tem ordem `⊤` é
aberto e fechado em `U` (`MeromorphicOn.isClopen_setOfPred_meromorphicOrderAt_eq_top`)
e não é vazio, logo é tudo. -/
theorem eventuallyEq_nhdsNE_of_meromorphicOn {U V : Set ℂ} {F G : ℂ → ℂ}
    (hUc : IsPreconnected U) (hF : MeromorphicOn F U) (hG : MeromorphicOn G U)
    (hV : IsOpen V) (hVU : V ⊆ U) (hVne : V.Nonempty) (hFG : EqOn F G V)
    {u : ℂ} (hu : u ∈ U) : F =ᶠ[𝓝[≠] u] G := by
  have hsub : MeromorphicOn (F - G) U := fun x hx => (hF x hx).sub (hG x hx)
  have hclopen : IsClopen {w : U | meromorphicOrderAt (F - G) w = ⊤} :=
    hsub.isClopen_setOfPred_meromorphicOrderAt_eq_top
  have hpc : PreconnectedSpace U := Subtype.preconnectedSpace hUc
  obtain ⟨v, hvV⟩ := hVne
  have hvU : v ∈ U := hVU hvV
  have hvS : (⟨v, hvU⟩ : U) ∈ {w : U | meromorphicOrderAt (F - G) w = ⊤} := by
    show meromorphicOrderAt (F - G) v = ⊤
    rw [meromorphicOrderAt_eq_top_iff]
    have h0 : ∀ᶠ z in 𝓝 v, (F - G) z = 0 := by
      filter_upwards [hV.mem_nhds hvV] with z hz
      simp [Pi.sub_apply, hFG hz]
    exact h0.filter_mono nhdsWithin_le_nhds
  have huniv := hclopen.eq_univ ⟨⟨v, hvU⟩, hvS⟩
  have hmem : (⟨u, hu⟩ : U) ∈ {w : U | meromorphicOrderAt (F - G) w = ⊤} := by
    rw [huniv]; trivial
  have hord : meromorphicOrderAt (F - G) u = ⊤ := hmem
  rw [meromorphicOrderAt_eq_top_iff] at hord
  filter_upwards [hord] with z hz
  simpa [Pi.sub_apply, sub_eq_zero] using hz

/-- **Princípio da identidade, forma pontual.**  Para funções em forma normal
a coincidência num aberto não vazio propaga-se, ponto a ponto, a todo o aberto
pré-conexo — inclusive nos polos. -/
theorem eqOn_of_meromorphicNFOn {U V : Set ℂ} {F G : ℂ → ℂ}
    (hUc : IsPreconnected U) (hF : MeromorphicNFOn F U) (hG : MeromorphicNFOn G U)
    (hV : IsOpen V) (hVU : V ⊆ U) (hVne : V.Nonempty) (hFG : EqOn F G V) :
    EqOn F G U := by
  intro u hu
  have h := eventuallyEq_nhdsNE_of_meromorphicOn hUc hF.meromorphicOn hG.meromorphicOn
    hV hVU hVne hFG hu
  exact (((hF hu).eventuallyEq_nhdsNE_iff_eventuallyEq_nhds (hG hu)).1 h).eq_of_nhds

/-! ## Funções meromorfas em forma normal -/

/-- Uma função meromorfa em todo o plano, **em forma normal**: o representante
canónico, que toma o valor `0` nos polos. -/
abbrev MerNF (f : ℂ → ℂ) : Prop := MeromorphicNFOn f Set.univ

/-- Toda função inteira está em forma normal: a teoria holomorfa é um caso
particular desta. -/
lemma merNF_of_differentiable {f : ℂ → ℂ} (hf : Differentiable ℂ f) : MerNF f :=
  fun x _ => (hf.differentiableOn.analyticOnNhd isOpen_univ x (mem_univ x)).meromorphicNFAt

lemma Aff.analyticAt_act (S : Aff) (x : ℂ) : AnalyticAt ℂ S.act x := by
  show AnalyticAt ℂ (fun z => (S.a : ℂ) * z + S.b) x
  fun_prop

@[simp] lemma Aff.deriv_act (S : Aff) (x : ℂ) : deriv S.act x = (S.a : ℂ) := by
  show deriv (fun z => (S.a : ℂ) * z + S.b) x = (S.a : ℂ)
  simp

/-- A forma normal é preservada por composição com uma isometria direta — é o
que permite falar das quatro determinações `f ∘ A_j⁻¹`. -/
lemma merNF_comp (S : Aff) {f : ℂ → ℂ} (hf : MerNF f) : MerNF (f ∘ S.act) := by
  intro x _
  rw [meromorphicNFAt_comp_iff_of_deriv_ne_zero (S.analyticAt_act x)
    (by rw [S.deriv_act]; exact S.a.ne_zero)]
  exact hf (mem_univ _)

/-! ## O teorema -/

/-- **Definição 2.4**, na forma do artigo: `f` meromorfa é *`Φ`-flexionável* se
existe uma vizinhança aberta e conexa `U ⊇ Q` e uma função `G` meromorfa em `U`
com `G = f ∘ A_j⁻¹` em `Q̊_{σ(j)}`, para `j = 1,2,3,4`. -/
def FlexionavelMer (Φ : Flex) (f : ℂ → ℂ) : Prop :=
  ∃ U : Set ℂ, ∃ G : ℂ → ℂ,
    IsOpen U ∧ IsPreconnected U ∧ Q ⊆ U ∧ MeromorphicOn G U ∧
      ∀ j : Fin 4, EqOn G (f ∘ (Φ.A j)⁻¹.act) (quad (Φ.σ j))

/-- **Teorema 3.2 (Caracterização), versão meromorfa.**  Seja `f` meromorfa em
`ℂ` (em forma normal) e `Φ` um flex de quadrantes.  São equivalentes:

1. `f` é `Φ`-flexionável;
2. as quatro determinações coincidem: `f ∘ A_1⁻¹ = ⋯ = f ∘ A_4⁻¹` em `ℂ`;
3. `f ∘ S = f` para todo `S ∈ Γ_Φ`. -/
theorem caracterizacaoMer (Φ : Flex) (f : ℂ → ℂ) (hf : MerNF f) :
    List.TFAE
      [ FlexionavelMer Φ f,
        ∀ j k : Fin 4, ∀ z, f ((Φ.A j)⁻¹.act z) = f ((Φ.A k)⁻¹.act z),
        Φ.Gamma ≤ Stab f ] := by
  have hcomp : ∀ m : Fin 4, MerNF (f ∘ (Φ.A m)⁻¹.act) := fun m => merNF_comp _ hf
  tfae_have 1 → 2 := by
    rintro ⟨U, G, hUo, hUc, hQU, hG, hEq⟩ j k z
    -- Em `U`, `G` coincide com cada determinação a menos dos polos.
    have key : ∀ m : Fin 4, ∀ u ∈ U, G =ᶠ[𝓝[≠] u] (f ∘ (Φ.A m)⁻¹.act) := by
      intro m u hu
      obtain ⟨z₀, hz₀⟩ := nonempty_quad (Φ.σ m)
      exact eventuallyEq_nhdsNE_of_meromorphicOn hUc hG
        (fun x _ => (hcomp m (mem_univ x)).meromorphicAt)
        (isOpen_quad _) (fun w hw => hQU (quad_subset_Q _ hw)) ⟨z₀, hz₀⟩ (hEq m) hu
    -- Como as determinações estão em forma normal, coincidem *pontualmente* em `U`.
    have hjkU : EqOn (f ∘ (Φ.A j)⁻¹.act) (f ∘ (Φ.A k)⁻¹.act) U := by
      intro u hu
      have h := (key j u hu).symm.trans (key k u hu)
      exact (((hcomp j (mem_univ u)).eventuallyEq_nhdsNE_iff_eventuallyEq_nhds
        (hcomp k (mem_univ u))).1 h).eq_of_nhds
    -- E, de novo pelo princípio da identidade, em todo o plano.
    obtain ⟨z₀, hz₀⟩ := nonempty_quad (Φ.σ j)
    have hUne : U.Nonempty := ⟨z₀, hQU (quad_subset_Q _ hz₀)⟩
    exact eqOn_of_meromorphicNFOn isPreconnected_univ (hcomp j) (hcomp k)
      hUo (subset_univ U) hUne hjkU (mem_univ z)
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
      (hcomp 0).meromorphicOn, ?_⟩
    intro j z _
    have hmem : (Φ.A 0)⁻¹ * Φ.A j ∈ Φ.Gamma := gerador_mem _ j 0
    have h := h3 hmem ((Φ.A j)⁻¹.act z)
    rw [Aff.act_mul, Aff.act_act_inv] at h
    simpa only [Function.comp_apply] using h
  tfae_finish

/-- A forma que usaremos: `f` meromorfa é `Φ`-flexionável se e só se é
`Γ_Φ`-invariante. -/
theorem flexionavelMer_iff (Φ : Flex) (f : ℂ → ℂ) (hf : MerNF f) :
    FlexionavelMer Φ f ↔ Φ.Gamma ≤ Stab f :=
  (caracterizacaoMer Φ f hf).out 0 2

/-- Coerência com a versão holomorfa: para `f` inteira, as duas noções de
flexionabilidade coincidem. -/
theorem flexionavelMer_iff_flexionavel (Φ : Flex) (f : ℂ → ℂ) (hf : Differentiable ℂ f) :
    FlexionavelMer Φ f ↔ Flexionavel Φ f := by
  rw [flexionavelMer_iff Φ f (merNF_of_differentiable hf), flexionavel_iff Φ f hf]

end Flexagonos
