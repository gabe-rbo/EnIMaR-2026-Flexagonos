/-
# O teorema das retas de dobra (Teorema 10.2) e os seus dois corolários

Teorema 10.2, Corolário 10.3 (caso quadrado: `Λ ⊆ 2ℤ[i]`, `|P| ≤ 2`) e
Corolário 10.4 (caso hexagonal: `W⁺ = C₃`, a cota de Gardner).

Todo o contraste entre os dois corolários tem uma causa só, e é geométrica: no
quadrado há retas admissíveis que **não** passam pelo centro (os quatro lados),
e a composição de duas reflexões paralelas produz as translações e, com elas, o
posto `2`; no hexágono todas passam pelo centro, e o grupo colapsa para
rotações.
-/
import FlexagonosLean.RetasDobra

namespace Flexagonos

open Complex

/-! ## Estados e flexes

Modelamos a componente de isometrias de um estado dobrado.  Um passo de flex
— dobrar ou reabrir ao longo de uma reta admissível — substitui `g_C` por
`r ∘ g_C` nas células que se movem e deixa as outras onde estavam. -/

/-- A componente de isometrias de um estado dobrado: a isometria de cada célula. -/
def Estado (C G : Type*) := C → G

/-- Um passo de flex ao longo de uma reta admissível: as células que se movem
sofrem `r` à esquerda, as outras ficam. -/
def PassoFlex {C G : Type*} [Group G] (R : Set G) (g g' : Estado C G) : Prop :=
  ∃ r ∈ R, ∀ c, g' c = r * g c ∨ g' c = g c

/-- Estados ligados por uma sequência de flexes. -/
def LigadoPorFlexes {C G : Type*} [Group G] (R : Set G) :
    Estado C G → Estado C G → Prop :=
  Relation.ReflTransGen (PassoFlex R)

/-- Ao longo de uma sequência de flexes, cada folha sofre uma isometria de
`W(D) = ⟨reflexões nas retas admissíveis⟩`.  É a primeira metade da
demonstração do Teorema 10.2. -/
theorem discrepancia_mem_closure {C G : Type*} [Group G] {R : Set G} {g g' : Estado C G}
    (h : LigadoPorFlexes R g g') : ∀ c, g' c * (g c)⁻¹ ∈ Subgroup.closure R := by
  induction h with
  | refl => intro c; simp
  | tail _ hbc ih =>
      intro c
      obtain ⟨r, hr, hcells⟩ := hbc
      rcases hcells c with hc | hc
      · rw [hc, mul_assoc]
        exact Subgroup.mul_mem _ (Subgroup.subset_closure hr) (ih c)
      · rw [hc]; exact ih c

/-! ## O teorema -/

/-- **Teorema 10.2 (teorema das retas de dobra).**  Se dois estados ligados por
flexes exibem a mesma face, então a discrepância de cada folha está em
`W⁺(D)`: em `W(D)` porque só se dobrou por retas admissíveis, e *direta* porque
a folha mostra o mesmo lado para cima nos dois estados.

Pela definição de mapa de retorno, `A_j` é exatamente essa discrepância para a
folha que ocupa o ladrilho `j`; logo `Γ_Φ ≤ W⁺(D)`. -/
theorem retas_de_dobra {C : Type*} {R : Set W} {g g' : Estado C W}
    (h : LigadoPorFlexes R g g') {c : C}
    (hlado : W.orient (g' c) = W.orient (g c)) :
    g' c * (g c)⁻¹ ∈ Subgroup.closure R ⊓ W.Wplus := by
  rw [Subgroup.mem_inf]
  refine ⟨discrepancia_mem_closure h c, ?_⟩
  show W.orient (g' c * (g c)⁻¹) = false
  rw [W.orient_mul, W.orient_inv, hlado]
  cases W.orient (g c) <;> rfl

/-- A forma que usaremos no quadrado: as seis retas admissíveis geram tudo, de
modo que a única informação que sobra é a orientação. -/
theorem retas_de_dobra_quadrado {C : Type*} {g g' : Estado C W}
    (h : LigadoPorFlexes W.retasAdmissiveis g g') {c : C}
    (hlado : W.orient (g' c) = W.orient (g c)) :
    g' c * (g c)⁻¹ ∈ W.Wplus :=
  (retas_de_dobra h hlado).2

/-! ## Corolário 10.3: o caso quadrado -/

/-- O reticulado `2ℤ[i]`. -/
def DoisZi : AddSubgroup ℂ where
  carrier := {z | ∃ m n : ℤ, z = 2 * m + 2 * n * I}
  zero_mem' := ⟨0, 0, by norm_num⟩
  add_mem' := by
    rintro _ _ ⟨m, n, rfl⟩ ⟨m', n', rfl⟩
    exact ⟨m + m', n + n', by push_cast; ring⟩
  neg_mem' := by
    rintro _ ⟨m, n, rfl⟩
    exact ⟨-m, -n, by push_cast; ring⟩

lemma mem_DoisZi {z : ℂ} : z ∈ DoisZi ↔ ∃ m n : ℤ, z = 2 * m + 2 * n * I := Iff.rfl

lemma neg_mem_DoisZi {z : ℂ} (hz : z ∈ DoisZi) : -z ∈ DoisZi := DoisZi.neg_mem hz

/-- O grupo cristalográfico `p2`: as translações de `2ℤ[i]` e as meias-voltas
em torno dos pontos de `ℤ[i]`. -/
def p2 : Subgroup Aff where
  carrier := {S | (S.a = 1 ∨ S.a = -1) ∧ S.b ∈ DoisZi}
  one_mem' := ⟨Or.inl rfl, DoisZi.zero_mem⟩
  mul_mem' := by
    rintro S T ⟨hSa, hSb⟩ ⟨hTa, hTb⟩
    refine ⟨?_, ?_⟩
    · rcases hSa with h | h <;> rcases hTa with h' | h' <;>
        simp [Aff.mul_a, h, h']
    · rw [Aff.mul_b]
      refine DoisZi.add_mem ?_ hSb
      rcases hSa with h | h
      · rw [h]; simpa using hTb
      · rw [h]
        have : ((-1 : ℂˣ) : ℂ) * T.b = -T.b := by simp
        rw [this]
        exact DoisZi.neg_mem hTb
  inv_mem' := by
    rintro S ⟨hSa, hSb⟩
    refine ⟨?_, ?_⟩
    · rcases hSa with h | h <;> simp [Aff.inv_a, h]
    · rw [Aff.inv_b]
      rcases hSa with h | h
      · rw [h]
        have : -((((1 : ℂˣ))⁻¹ : ℂˣ) : ℂ) * S.b = -S.b := by simp
        rw [this]
        exact DoisZi.neg_mem hSb
      · rw [h]
        have : -((((-1 : ℂˣ))⁻¹ : ℂˣ) : ℂ) * S.b = S.b := by simp
        rw [this]
        exact hSb

/-- A isometria de `W⁺` vista em `Aff`: uma translação por `2ℤ[i]` se as duas
componentes são translações, uma meia-volta em torno de um ponto de `ℤ[i]` se as
duas são reflexões. -/
noncomputable def W.toAff (w : W) : Aff :=
  ⟨if w.1.flip then -1 else 1, 2 * ((w.1.t : ℂ) + (w.2.t : ℂ) * I)⟩

/-- `toAff` calcula de facto a ação de `W⁺` no plano. -/
theorem W.toAff_act (w : W) (hw : w ∈ W.Wplus) (z : ℂ) : (W.toAff w).act z = W.act w z := by
  rw [W.mem_Wplus_iff] at hw
  cases hf : w.1.flip
  · have hf2 : w.2.flip = false := by rw [← hw, hf]
    apply Complex.ext <;>
      simp [W.toAff, Aff.act, W.act, Dinf.act, sgn, hf, hf2] <;> ring
  · have hf2 : w.2.flip = true := by rw [← hw, hf]
    apply Complex.ext <;>
      simp [W.toAff, Aff.act, W.act, Dinf.act, sgn, hf, hf2] <;> ring

/-- **Corolário 10.3 (caso quadrado).**  A imagem de `W⁺` em `Aff` está contida
no grupo cristalográfico `p2`.

Em consequência, num tetraflexágono `Λ ⊆ 2ℤ[i]` e `|P| ≤ 2`: das nove classes
do Teorema 4.1 só `p1` e `p2` (e as degeneradas de posto menor) podem ocorrer. -/
theorem W.toAff_mem_p2 (w : W) : W.toAff w ∈ p2 := by
  refine ⟨?_, ⟨w.1.t, w.2.t, ?_⟩⟩
  · by_cases h : w.1.flip <;> simp [W.toAff, h]
  · show (2 : ℂ) * ((w.1.t : ℂ) + (w.2.t : ℂ) * I)
        = 2 * (w.1.t : ℂ) + 2 * (w.2.t : ℂ) * I
    ring

/-- **Corolário 10.3, forma usável.**  Se `Γ ≤ p2`, o seu reticulado de
translações está contido em `2ℤ[i]`. -/
theorem translacao_mem_DoisZi {Γ : Subgroup Aff} (hΓ : Γ ≤ p2) {w : ℂ}
    (h : Aff.T w ∈ Γ) : w ∈ DoisZi := (hΓ h).2

/-- **Corolário 10.3, forma usável.**  Se `Γ ≤ p2`, o seu grupo de pontos está
contido em `{±1}`: `|P| ≤ 2`, e nenhum tetraflexágono volta rodado `90°`. -/
theorem ponto_eq_pm_one {Γ : Subgroup Aff} (hΓ : Γ ≤ p2) {S : Aff}
    (h : S ∈ Γ) : S.a = 1 ∨ S.a = -1 := (hΓ h).1

/-! ## Corolário 10.4: o caso hexagonal

As três diagonais longas do hexágono fazem `60°` entre si e **todas passam pelo
centro** `O`, logo `W` é o grupo diedral de ordem `6` que fixa `O`, e
`W⁺ = C₃`.  Nenhum hexaflexágono força funções elípticas. -/

/-- O grupo `W` do hexágono: `⟨k, false⟩` é a rotação por `2πk/3` em torno do
centro, `⟨k, true⟩` a reflexão correspondente. -/
@[ext]
structure Whex where
  /-- A rotação, em terços de volta. -/
  rot : ZMod 3
  /-- `true` se inverte a orientação. -/
  flip : Bool
deriving DecidableEq

namespace Whex

instance : Mul Whex :=
  ⟨fun a b => ⟨a.rot + (if a.flip then -b.rot else b.rot), xor a.flip b.flip⟩⟩
instance : One Whex := ⟨⟨0, false⟩⟩
instance : Inv Whex := ⟨fun a => ⟨if a.flip then a.rot else -a.rot, a.flip⟩⟩

@[simp] lemma mul_rot (a b : Whex) :
    (a * b).rot = a.rot + (if a.flip then -b.rot else b.rot) := rfl
@[simp] lemma mul_flip (a b : Whex) : (a * b).flip = xor a.flip b.flip := rfl
@[simp] lemma one_rot : (1 : Whex).rot = 0 := rfl
@[simp] lemma one_flip : (1 : Whex).flip = false := rfl
@[simp] lemma inv_rot (a : Whex) : a⁻¹.rot = if a.flip then a.rot else -a.rot := rfl
@[simp] lemma inv_flip (a : Whex) : a⁻¹.flip = a.flip := rfl

instance : Group Whex where
  mul_assoc a b c := by
    ext
    · cases ha : a.flip <;> cases hb : b.flip <;> simp [ha, hb] <;> ring
    · simp [Bool.xor_assoc]
  one_mul a := by ext <;> simp
  mul_one a := by ext <;> simp
  inv_mul_cancel a := by ext <;> cases ha : a.flip <;> simp [ha]

instance : Fintype Whex :=
  Fintype.ofEquiv (ZMod 3 × Bool)
    { toFun := fun p => ⟨p.1, p.2⟩
      invFun := fun a => (a.rot, a.flip)
      left_inv := fun _ => rfl
      right_inv := fun _ => rfl }

/-- `W(hexágono)` é o diedral de ordem `6`. -/
theorem card_Whex : Fintype.card Whex = 6 := by
  rw [Fintype.card_congr
    ({ toFun := fun a : Whex => (a.rot, a.flip)
       invFun := fun p => ⟨p.1, p.2⟩
       left_inv := fun _ => rfl
       right_inv := fun _ => rfl } : Whex ≃ ZMod 3 × Bool)]
  simp

/-- `W⁺(hexágono) = C₃`: só as rotações. -/
def Wplus : Subgroup Whex where
  carrier := {a | a.flip = false}
  one_mem' := rfl
  mul_mem' := by
    intro a b ha hb
    show (a * b).flip = false
    rw [mul_flip, show a.flip = false from ha, show b.flip = false from hb]
    rfl
  inv_mem' := by
    intro a ha
    show a⁻¹.flip = false
    rwa [inv_flip]

instance : DecidablePred (· ∈ Wplus) := fun a => decidable_of_iff (a.flip = false) Iff.rfl

/-- **Corolário 10.4 (caso hexagonal).**  `W⁺` tem exatamente três elementos:
as rotações de `0`, `120°` e `240°` em torno do centro. -/
theorem card_Wplus : Fintype.card Wplus = 3 := by
  first
    | decide
    | (rw [Fintype.card_subtype]; decide)
    | rfl

/-- **A cota de Gardner.**  Como os mapas de retorno de uma face de um
hexaflexágono estão em `W⁺`, que tem três elementos, *cada face aparece em no
máximo três arranjos*.  É exatamente o que Gardner observou experimentalmente
em 1956: o limite `3` é um teorema, não um acidente do hexa-hexa. -/
theorem gardner (s : Finset Whex) (hs : ∀ w ∈ s, w ∈ Wplus) : s.card ≤ 3 := by
  have hsub : s ⊆ Finset.univ.filter (· ∈ Wplus) :=
    fun w hw => Finset.mem_filter.2 ⟨Finset.mem_univ w, hs w hw⟩
  have hcard : (Finset.univ.filter (· ∈ Wplus)).card = 3 := by decide
  calc s.card ≤ (Finset.univ.filter (· ∈ Wplus)).card := Finset.card_le_card hsub
    _ = 3 := hcard

/-- Nenhum hexaflexágono força funções elípticas: `Γ ≤ W⁺` é um grupo **finito**
de rotações em torno de `O`, logo o seu reticulado de translações é trivial e
sobram soluções inteiras. -/
theorem hexaflexagono_finito (Γ : Subgroup Whex) : Nat.card Γ ≤ 6 := by
  have : Nat.card Γ ≤ Nat.card Whex := Subgroup.card_le_card_group Γ
  simpa [Nat.card_eq_fintype_card, card_Whex] using this

end Whex

end Flexagonos
