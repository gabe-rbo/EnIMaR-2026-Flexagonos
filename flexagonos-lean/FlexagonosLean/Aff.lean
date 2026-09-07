/-
# Isometrias diretas do plano complexo

Formalização do artigo *Funções complexas flexionáveis* (projeto EnIMaR).

Este arquivo constrói o grupo `Aff` das aplicações `z ↦ a·z + b` com `a` uma
unidade de `ℂ`.  É o ambiente onde vivem as peças `A_j` de um flex
(Definição 2.1 do artigo) e o grupo de discrepância `Γ_Φ` (Definição 3.1).

Optamos por uma estrutura própria em vez de `AffineMap` porque precisamos de
uma estrutura de **grupo** (com inversos) e de igualdade decidida pelos dois
coeficientes.
-/
import Mathlib

namespace Flexagonos

open Complex

/-- Uma isometria direta (mais geralmente, uma semelhança direta) do plano:
a aplicação `z ↦ a·z + b`. -/
@[ext]
structure Aff where
  /-- A parte linear, uma unidade de `ℂ`. -/
  a : ℂˣ
  /-- A translação. -/
  b : ℂ

namespace Aff

instance : Mul Aff := ⟨fun f g => ⟨f.a * g.a, (f.a : ℂ) * g.b + f.b⟩⟩
instance : One Aff := ⟨⟨1, 0⟩⟩
instance : Inv Aff := ⟨fun f => ⟨f.a⁻¹, -((f.a⁻¹ : ℂˣ) : ℂ) * f.b⟩⟩

@[simp] lemma mul_a (f g : Aff) : (f * g).a = f.a * g.a := rfl
@[simp] lemma mul_b (f g : Aff) : (f * g).b = (f.a : ℂ) * g.b + f.b := rfl
@[simp] lemma one_a : (1 : Aff).a = 1 := rfl
@[simp] lemma one_b : (1 : Aff).b = 0 := rfl
@[simp] lemma inv_a (f : Aff) : f⁻¹.a = f.a⁻¹ := rfl
@[simp] lemma inv_b (f : Aff) : f⁻¹.b = -((f.a⁻¹ : ℂˣ) : ℂ) * f.b := rfl

instance : Group Aff where
  mul_assoc f g h := by ext <;> simp [mul_assoc] <;> ring
  one_mul f := by ext <;> simp
  mul_one f := by ext <;> simp
  inv_mul_cancel f := by ext <;> simp

/-- A aplicação do plano determinada por `f : Aff`. -/
def act (f : Aff) (z : ℂ) : ℂ := (f.a : ℂ) * z + f.b

lemma act_apply (f : Aff) (z : ℂ) : f.act z = (f.a : ℂ) * z + f.b := rfl

@[simp] lemma act_one (z : ℂ) : (1 : Aff).act z = z := by simp [act]

/-- `act` é um antihomomorfismo à direita: a composição corresponde ao produto. -/
@[simp] lemma act_mul (f g : Aff) (z : ℂ) : (f * g).act z = f.act (g.act z) := by
  simp [act]; ring

@[simp] lemma act_inv_act (f : Aff) (z : ℂ) : f⁻¹.act (f.act z) = z := by
  have := act_mul f⁻¹ f z
  simpa using this.symm

@[simp] lemma act_act_inv (f : Aff) (z : ℂ) : f.act (f⁻¹.act z) = z := by
  have := act_mul f f⁻¹ z
  simpa using this.symm

/-- Uma translação. -/
def T (w : ℂ) : Aff := ⟨1, w⟩

@[simp] lemma T_a (w : ℂ) : (T w).a = 1 := rfl
@[simp] lemma T_b (w : ℂ) : (T w).b = w := rfl
@[simp] lemma T_act (w z : ℂ) : (T w).act z = z + w := by simp [T, act, add_comm]

@[simp] lemma T_zero : T 0 = 1 := by ext <;> simp [T]

lemma T_mul (w v : ℂ) : T w * T v = T (w + v) := by
  ext <;> simp [T, add_comm]

@[simp] lemma T_inv (w : ℂ) : (T w)⁻¹ = T (-w) := by
  ext <;> simp [T]

/-- Toda `f : Aff` é diferenciável (holomorfa) em `ℂ`. -/
lemma differentiable_act (f : Aff) : Differentiable ℂ f.act := by
  unfold act
  fun_prop

end Aff

end Flexagonos
