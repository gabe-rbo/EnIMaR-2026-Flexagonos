/-
# O modelo com camadas e o teorema das retas de dobra (Seção 10 do artigo)

Lema 10.1 (retas admissíveis), Teorema 10.2 (teorema das retas de dobra) e o
Corolário 10.3 (caso quadrado): num tetraflexágono `Λ ⊆ 2ℤ[i]` e `|P| ≤ 2`.

## A observação que organiza o arquivo

A demonstração do Teorema 10.2 usa apenas a **componente de isometrias** de um
estado dobrado: cada dobra e cada abertura substitui `g_C` por `r_ℓ ∘ g_C` nas
células que se movem, e exibir a mesma face nos dois estados obriga a
discrepância a preservar a orientação.  As ordens de camadas e as três
condições de não-atravessamento de Justin fazem parte da definição de estado
dobrado — modelam papel sem auto-intersecção — mas **não intervêm neste
teorema**.  Formalizamos, portanto, a componente de isometrias, que é onde
está todo o conteúdo.

## O grupo

Como as retas de dobra do quadrado são `x ∈ ℤ` e `y ∈ ℤ`, o grupo `W` gerado
pelas suas reflexões age separadamente nas duas coordenadas:
`W ≅ D∞ × D∞`.  É a observação da demonstração do Teorema 12.1, e é ela que
torna todo este capítulo elementar.
-/
import FlexagonosLean.Discreto

namespace Flexagonos

open Complex

/-! ## O grupo diedral infinito -/

/-- O sinal de uma componente: `+1` para translação, `-1` para reflexão. -/
def sgn (s : Bool) : ℤ := if s then -1 else 1

@[simp] lemma sgn_false : sgn false = 1 := rfl
@[simp] lemma sgn_true : sgn true = -1 := rfl

lemma sgn_xor (s t : Bool) : sgn (xor s t) = sgn s * sgn t := by
  cases s <;> cases t <;> simp [sgn]

@[simp] lemma sgn_mul_self (s : Bool) : sgn s * sgn s = 1 := by cases s <;> simp [sgn]

/-- `D∞`, o grupo gerado pelas reflexões nos pontos inteiros da reta.
O elemento `⟨s, n⟩` age por `x ↦ ±x + 2n`: `⟨false, n⟩` é a translação por `2n`
e `⟨true, n⟩` é a reflexão no ponto `n`. -/
@[ext]
structure Dinf where
  /-- `true` se a componente inverte a reta. -/
  flip : Bool
  /-- O parâmetro de translação, em unidades de `2`. -/
  t : ℤ
deriving DecidableEq

namespace Dinf

instance : Mul Dinf := ⟨fun d e => ⟨xor d.flip e.flip, sgn d.flip * e.t + d.t⟩⟩
instance : One Dinf := ⟨⟨false, 0⟩⟩
instance : Inv Dinf := ⟨fun d => ⟨d.flip, -(sgn d.flip * d.t)⟩⟩

@[simp] lemma mul_flip (d e : Dinf) : (d * e).flip = xor d.flip e.flip := rfl
@[simp] lemma mul_t (d e : Dinf) : (d * e).t = sgn d.flip * e.t + d.t := rfl
@[simp] lemma one_flip : (1 : Dinf).flip = false := rfl
@[simp] lemma one_t : (1 : Dinf).t = 0 := rfl
@[simp] lemma inv_flip (d : Dinf) : d⁻¹.flip = d.flip := rfl
@[simp] lemma inv_t (d : Dinf) : d⁻¹.t = -(sgn d.flip * d.t) := rfl

instance : Group Dinf where
  mul_assoc d e f := by
    ext
    · simp [Bool.xor_assoc]
    · simp [sgn_xor]; ring
  one_mul d := by ext <;> simp
  mul_one d := by ext <;> simp
  inv_mul_cancel d := by ext <;> simp

/-- A ação de `D∞` na reta: `x ↦ ±x + 2n`. -/
def act (d : Dinf) (x : ℝ) : ℝ := (sgn d.flip : ℝ) * x + 2 * d.t

@[simp] lemma act_one (x : ℝ) : (1 : Dinf).act x = x := by simp [act]

@[simp] lemma act_mul (d e : Dinf) (x : ℝ) : (d * e).act x = d.act (e.act x) := by
  simp [act, sgn_xor]
  push_cast
  ring

/-- A translação por `2n`. -/
def trans (n : ℤ) : Dinf := ⟨false, n⟩

/-- A reflexão no ponto inteiro `n`. -/
def refl (n : ℤ) : Dinf := ⟨true, n⟩

@[simp] lemma trans_zero : trans 0 = 1 := rfl

lemma trans_mul (m n : ℤ) : trans m * trans n = trans (m + n) := by
  ext <;> simp [trans] <;> ring

@[simp] lemma trans_inv (n : ℤ) : (trans n)⁻¹ = trans (-n) := by
  ext <;> simp [trans]

lemma trans_zpow (n : ℤ) : (trans 1) ^ n = trans n := by
  refine Int.induction_on n rfl (fun k ih => ?_) (fun k ih => ?_)
  · rw [zpow_add_one, ih, trans_mul]
  · rw [zpow_sub_one, ih, trans_inv, trans_mul]
    congr 1

lemma refl_eq (n : ℤ) : refl n = trans n * refl 0 := by
  ext <;> simp [refl, trans]

/-- A imagem da célula `[c, c+1]` sob `d`, como índice inteiro. -/
def cellImage (d : Dinf) (c : ℤ) : ℤ :=
  if d.flip then -c - 1 + 2 * d.t else c + 2 * d.t

/-- **O ingrediente aritmético da fórmula de paridade (Teorema 12.1).**
A paridade da coluna ocupada muda exatamente quando a componente inverte:
se `d` é translação, a célula `[c, c+1]` vai para `[c+2m, c+1+2m]` e a paridade
não muda; se inverte, vai para `[-c-1+2m, -c+2m]` e a paridade troca. -/
lemma cellImage_emod_two (d : Dinf) (c : ℤ) :
    cellImage d c % 2 = (c + (if d.flip then 1 else 0)) % 2 := by
  cases hd : d.flip <;> simp [cellImage, hd] <;> omega

end Dinf

/-! ## `W(Q) = D∞ × D∞` -/

/-- `W(Q)`, o grupo gerado pelas reflexões nas retas admissíveis do quadrado.
Age separadamente nas duas coordenadas. -/
abbrev W := Dinf × Dinf

namespace W

/-- A ação de `W` no plano. -/
def act (w : W) (z : ℂ) : ℂ := ⟨w.1.act z.re, w.2.act z.im⟩

@[simp] lemma act_re (w : W) (z : ℂ) : (w.act z).re = w.1.act z.re := rfl
@[simp] lemma act_im (w : W) (z : ℂ) : (w.act z).im = w.2.act z.im := rfl

/-- A orientação: `false` para as isometrias diretas, `true` para as inversas.
Uma isometria `(u,v)` é direta exatamente quando `u` e `v` são do mesmo tipo —
ambas translações (a identidade) ou ambas reflexões (uma meia-volta). -/
def orient (w : W) : Bool := xor w.1.flip w.2.flip

@[simp] lemma orient_one : orient 1 = false := rfl

lemma orient_mul (w v : W) : orient (w * v) = xor (orient w) (orient v) := by
  obtain ⟨⟨a, _⟩, ⟨b, _⟩⟩ := w
  obtain ⟨⟨c, _⟩, ⟨d, _⟩⟩ := v
  cases a <;> cases b <;> cases c <;> cases d <;> rfl

@[simp] lemma orient_inv (w : W) : orient w⁻¹ = orient w := rfl

/-- `W⁺(Q)`, o subgrupo das isometrias diretas. -/
def Wplus : Subgroup W where
  carrier := {w | orient w = false}
  one_mem' := rfl
  mul_mem' := by
    intro w v hw hv
    show orient (w * v) = false
    rw [orient_mul, show orient w = false from hw, show orient v = false from hv]
    rfl
  inv_mem' := by
    intro w hw
    show orient w⁻¹ = false
    rwa [orient_inv]

lemma mem_Wplus {w : W} : w ∈ Wplus ↔ orient w = false := Iff.rfl

lemma mem_Wplus_iff {w : W} : w ∈ Wplus ↔ w.1.flip = w.2.flip := by
  rw [mem_Wplus, orient]
  cases w.1.flip <;> cases w.2.flip <;> simp

/-! ## As seis retas admissíveis (Lema 10.1) -/

/-- A reflexão na reta vertical `x = a`. -/
def reflV (a : ℤ) : W := (Dinf.refl a, 1)

/-- A reflexão na reta horizontal `y = b`. -/
def reflH (b : ℤ) : W := (1, Dinf.refl b)

/-- As seis retas admissíveis do quadrado `2×2`: as duas medianas `x=0`, `y=0`
e os quatro lados `x=±1`, `y=±1` (Lema 10.1). -/
def retasAdmissiveis : Set W :=
  {reflV 0, reflV 1, reflV (-1), reflH 0, reflH 1, reflH (-1)}

private lemma transV_mem : (Dinf.trans 1, (1 : Dinf)) ∈ Subgroup.closure retasAdmissiveis := by
  have h1 : reflV 1 ∈ Subgroup.closure retasAdmissiveis :=
    Subgroup.subset_closure (by simp [retasAdmissiveis])
  have h0 : reflV 0 ∈ Subgroup.closure retasAdmissiveis :=
    Subgroup.subset_closure (by simp [retasAdmissiveis])
  have : reflV 1 * reflV 0 = (Dinf.trans 1, (1 : Dinf)) := by
    ext <;> simp [reflV, Dinf.refl, Dinf.trans]
  rw [← this]
  exact Subgroup.mul_mem _ h1 h0

private lemma transH_mem : ((1 : Dinf), Dinf.trans 1) ∈ Subgroup.closure retasAdmissiveis := by
  have h1 : reflH 1 ∈ Subgroup.closure retasAdmissiveis :=
    Subgroup.subset_closure (by simp [retasAdmissiveis])
  have h0 : reflH 0 ∈ Subgroup.closure retasAdmissiveis :=
    Subgroup.subset_closure (by simp [retasAdmissiveis])
  have : reflH 1 * reflH 0 = ((1 : Dinf), Dinf.trans 1) := by
    ext <;> simp [reflH, Dinf.refl, Dinf.trans]
  rw [← this]
  exact Subgroup.mul_mem _ h1 h0

private lemma fstV_mem (u : Dinf) : (u, (1 : Dinf)) ∈ Subgroup.closure retasAdmissiveis := by
  have hT : ∀ n : ℤ, (Dinf.trans n, (1 : Dinf)) ∈ Subgroup.closure retasAdmissiveis := by
    intro n
    have := Subgroup.zpow_mem _ transV_mem n
    rwa [show ((Dinf.trans 1, (1 : Dinf)) : W) ^ n = (Dinf.trans n, (1 : Dinf)) by
      rw [Prod.pow_def, Dinf.trans_zpow, one_zpow]] at this
  cases hu : u.flip
  · have : u = Dinf.trans u.t := by ext <;> simp [Dinf.trans, hu]
    rw [this]; exact hT _
  · have h0 : reflV 0 ∈ Subgroup.closure retasAdmissiveis :=
      Subgroup.subset_closure (by simp [retasAdmissiveis])
    have : (u, (1 : Dinf)) = (Dinf.trans u.t, (1 : Dinf)) * reflV 0 := by
      ext <;> simp [Dinf.trans, reflV, Dinf.refl, hu]
    rw [this]
    exact Subgroup.mul_mem _ (hT _) h0

private lemma sndH_mem (v : Dinf) : ((1 : Dinf), v) ∈ Subgroup.closure retasAdmissiveis := by
  have hT : ∀ n : ℤ, ((1 : Dinf), Dinf.trans n) ∈ Subgroup.closure retasAdmissiveis := by
    intro n
    have := Subgroup.zpow_mem _ transH_mem n
    rwa [show (((1 : Dinf), Dinf.trans 1) : W) ^ n = ((1 : Dinf), Dinf.trans n) by
      rw [Prod.pow_def, Dinf.trans_zpow, one_zpow]] at this
  cases hv : v.flip
  · have : v = Dinf.trans v.t := by ext <;> simp [Dinf.trans, hv]
    rw [this]; exact hT _
  · have h0 : reflH 0 ∈ Subgroup.closure retasAdmissiveis :=
      Subgroup.subset_closure (by simp [retasAdmissiveis])
    have : ((1 : Dinf), v) = ((1 : Dinf), Dinf.trans v.t) * reflH 0 := by
      ext <;> simp [Dinf.trans, reflH, Dinf.refl, hv]
    rw [this]
    exact Subgroup.mul_mem _ (hT _) h0

/-- **Lema 10.1.**  As seis retas admissíveis do quadrado `2×2` geram `W`.

É daqui que vem o posto `2`: duas retas *paralelas* compõem-se numa translação.
No hexágono todas as retas admissíveis passam pelo centro, e é por isso que lá
o grupo colapsa (Corolário 10.4). -/
theorem closure_retasAdmissiveis : Subgroup.closure retasAdmissiveis = ⊤ := by
  rw [eq_top_iff]
  rintro ⟨u, v⟩ -
  have : (u, v) = (u, (1 : Dinf)) * ((1 : Dinf), v) := by ext <;> simp
  rw [this]
  exact Subgroup.mul_mem _ (fstV_mem u) (sndH_mem v)

end W

end Flexagonos
