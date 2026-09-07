/-
# A caracterização combinatória (Seção 12 do artigo)

Teorema 12.1 (fórmula de paridade), Corolário 12.2 (fórmula dos intervalos),
Proposição 12.3 (uma charneira solta por bloco) e Teorema 12.4 (o arranjo de
cada face é função de `u`).

O ponto da seção é que a busca exaustiva nos `216 768` estados dobrados é
**dispensável**: o arranjo de cada face lê-se de quatro dígitos ternários.
Aqui isso fica literal — todos os enunciados sobre o anel são decididos por
`decide` sobre as `81` coordenadas.

## Fidelidade das definições

As definições concretas deste arquivo (tabela das faces, quais charneiras são
verticais, o passeio ao longo da tira, `posicoes`, `assinatura`, `exibivel`)
foram conferidas contra `src/paridade.py` do projeto: reproduzem-no exatamente
nas `81` coordenadas e nas `6` faces.  É a precaução que a modelagem exige,
porque aqui são as *definições* que carregam o conteúdo.
-/
import FlexagonosLean.RetasDobra

namespace Flexagonos

/-! ## Teorema 12.1: a fórmula de paridade

As retas de dobra são `x ∈ ℤ` e `y ∈ ℤ`, logo `W ≅ D∞ × D∞` age separadamente
em `x` e em `y` e cada `g_L` escreve-se `(u_L, v_L)`.  Uma isometria `(u,v)` é
uma rotação de `180°` exatamente quando `u` e `v` são ambas reflexões, e é
direta quando ambas são do mesmo tipo. -/

namespace Dinf

/-- O bit `t_x(L)`: vale `1` quando a componente inverte a reta. -/
def tbit (d : Dinf) : ℤ := if d.flip then 1 else 0

/-- **Teorema 12.1 (fórmula de paridade).**  A paridade da coluna que a folha
ocupa na face determina, junto com a coluna que ela ocupa no plano, o bit de
inversão: `t_x ≡ κ + c (mod 2)`.

Daqui saem as duas fórmulas do enunciado do artigo: a parte de rotação é
`a_L = 2 t_x(L) ≡ 2(κ_L + c_L) (mod 4)` e o lado visível é
`s_L = t_x(L) + t_y(L)`. -/
theorem tbit_emod_two (d : Dinf) (c : ℤ) :
    d.tbit % 2 = (cellImage d c + c) % 2 := by
  cases hd : d.flip <;> simp [tbit, cellImage, hd] <;> omega

end Dinf

namespace W

/-- A parte de rotação de `(u,v) ∈ W`, em quartos de volta: `0` se as
componentes não invertem, `2` (meia-volta) se invertem. -/
def rotBit (w : W) : ℤ := 2 * w.1.tbit

/-- O lado visível de `(u,v) ∈ W`. -/
def sideBit (w : W) : ℤ := w.1.tbit + w.2.tbit

/-- **Teorema 12.1, forma completa.**  A rotação e o lado visível de cada folha
leem-se das paridades das colunas e das linhas. -/
theorem rotBit_emod_four (w : W) (c : ℤ) :
    w.rotBit % 4 = 2 * ((Dinf.cellImage w.1 c + c) % 2) % 4 := by
  cases hd : w.1.flip <;>
    simp [rotBit, Dinf.tbit, Dinf.cellImage, hd] <;> omega

theorem sideBit_emod_two (w : W) (c r : ℤ) :
    w.sideBit % 2 = ((Dinf.cellImage w.1 c + c) + (Dinf.cellImage w.2 r + r)) % 2 := by
  cases h1 : w.1.flip <;> cases h2 : w.2.flip <;>
    simp [sideBit, Dinf.tbit, Dinf.cellImage, h1, h2] <;> omega

end W

/-! ## O anel de doze quadradinhos

As doze charneiras repartem-se em quatro blocos de três paralelas,
`(0,1,2)`, `(3,4,5)`, `(6,7,8)`, `(9,10,11)`.  Os blocos `0` e `2` são as
charneiras **verticais**; os blocos `1` e `3` as horizontais. -/

/-- Uma coordenada `u = (u₁,u₂,u₃,u₄) ∈ {0,1,2}⁴` (Proposição 12.3). -/
abbrev Coord := Fin 3 × Fin 3 × Fin 3 × Fin 3

/-- O valor de `u` no bloco `i`. -/
def uAt (u : Coord) : ℕ → ℕ
  | 0 => u.1.val
  | 1 => u.2.1.val
  | 2 => u.2.2.1.val
  | _ => u.2.2.2.val

/-- A charneira `h` é vertical quando está nos blocos `0` ou `2`. -/
def vertical (h : ℕ) : Bool := h / 3 == 0 || h / 3 == 2

/-- A charneira `h` está **dobrada** em `u`: todas menos a solta do seu bloco.
É a Proposição 12.3 — dobrar quatro células numa janela de duas obriga a que
exatamente uma charneira de cada bloco fique solta. -/
def dobrada (u : Coord) (h : ℕ) : Bool := !(uAt u (h / 3) == h % 3)

/-- As charneiras percorridas ao ir da peça em `base` à peça em `i` ao longo do
anel. -/
def passos (base i : ℕ) : List ℕ :=
  (List.range ((i + 12 - base) % 12)).map (fun s => (base + s) % 12)

/-- `κ`: a paridade do número de charneiras **verticais soltas** entre as duas
peças ao longo da tira. -/
def kappa (u : Coord) (base i : ℕ) : Bool :=
  ((passos base i).filter (fun h => vertical h && !dobrada u h)).length % 2 == 1

/-- `ρ`: o mesmo com as horizontais. -/
def rho (u : Coord) (base i : ℕ) : Bool :=
  ((passos base i).filter (fun h => !vertical h && !dobrada u h)).length % 2 == 1

/-- **Corolário 12.2 (fórmula dos intervalos).**  A rotação relativa de duas
peças é `2 ·` o número de charneiras **verticais dobradas** entre elas, módulo
`4`.  O vetor de rotações lê-se dos bits de dobra: nenhuma isometria é
necessária. -/
def rot (u : Coord) (base i : ℕ) : ℕ :=
  2 * ((passos base i).filter (fun h => vertical h && dobrada u h)).length % 4

/-- A fórmula dos intervalos só vê a *paridade* do número de charneiras
verticais dobradas — é o conteúdo de `a_j - a_{j'} ≡ 2·#{…} (mod 4)`. -/
theorem rot_eq_two_mul_parity (u : Coord) (base i : ℕ) :
    rot u base i =
      2 * (((passos base i).filter (fun h => vertical h && dobrada u h)).length % 2) := by
  rw [rot]
  omega

/-- A tabela das faces: para cada face `k` (índice `k` = face `k+1`), as quatro
peças do anel que a compõem, nos quadrantes `1,2,3,4`. -/
def faceTab : Fin 6 -> List ℕ :=
  ![[2, 11, 8, 5], [1, 4, 7, 10], [1, 0, 7, 6], [6, 5, 0, 11], [10, 9, 4, 3], [3, 2, 9, 8]]

/-- **Teorema 12.4.**  As posições `(κ_j, ρ_j)` das quatro peças da face `k`. -/
def posicoes (u : Coord) (k : Fin 6) : List (Bool × Bool) :=
  (faceTab k).map (fun i => (kappa u ((faceTab k).headI) i, rho u ((faceTab k).headI) i))

/-- **Teorema 12.4.**  A face `k` é exibível em `u` se e só se as quatro
posições são distintas. -/
def exibivel (u : Coord) (k : Fin 6) : Bool := (posicoes u k).dedup.length == 4

/-- **Teorema 12.4.**  A assinatura de rotações da face `k` em `u`. -/
def assinatura (u : Coord) (k : Fin 6) : List ℕ :=
  (faceTab k).map (fun i => rot u ((faceTab k).headI) i)

/-- As coordenadas que correspondem a dobraduras planas do anel sobre o
quadrado `2×2`: um flex vertical ou fixa `(u₁,u₃)` ou muda as duas, e um
horizontal age do mesmo modo em `(u₂,u₄)`; a coordenada `1` (charneira solta ao
meio do bloco) não se mistura com as coordenadas extremas `0` e `2`. -/
def valida (u : Coord) : Bool :=
  ((uAt u 0 == 1) == (uAt u 2 == 1)) && ((uAt u 1 == 1) == (uAt u 3 == 1))

/-! ## Os enunciados, decididos sobre as 81 coordenadas -/

/-- **Proposição 12.3.**  Das `81` coordenadas `u ∈ {0,1,2}⁴` ocorrem
exatamente `25`. -/
theorem card_validas : (Finset.univ.filter (fun u : Coord => valida u)).card = 25 := by
  decide

/-- **Teorema 12.4 / Corolário.**  As faces `3`, `4`, `5` e `6` têm assinatura
de rotações **única** ao longo de todas as coordenadas válidas: `(0,0,0,0)`.
Não dão trabalho nenhum. -/
theorem assinatura_unica_faces_3456 (u : Coord) (k : Fin 6) (hk : 2 ≤ k.val)
    (hu : valida u = true) (he : exibivel u k = true) :
    assinatura u k = [0, 0, 0, 0] := by
  revert hk hu he
  revert k u
  decide

/-- **Teorema 12.4 / Corolário.**  As faces `1` e `2` só se exibem na
**diagonal** `u₁ = u₃`. -/
theorem faces_12_diagonal (u : Coord) (k : Fin 6) (hk : k.val < 2)
    (hu : valida u = true) (he : exibivel u k = true) :
    uAt u 0 = uAt u 2 := by
  revert hk hu he
  revert k u
  decide

/-- **Teorema 12.4 / Corolário.**  E aí cada uma tem **duas** assinaturas:
a genérica `(0,2,0,2)` e a excepcional `(0,0,0,0)`.  Resta portanto um único
bit — e é ele que a regra dos extremos (Teorema 12.5) decide. -/
theorem assinaturas_faces_12 (u : Coord) (k : Fin 6) (hk : k.val < 2)
    (hu : valida u = true) (he : exibivel u k = true) :
    assinatura u k = [0, 2, 0, 2] ∨ assinatura u k = [0, 0, 0, 0] := by
  revert hk hu he
  revert k u
  decide

/-- A assinatura excepcional de cada uma das faces `1` e `2` ocorre em
**exatamente uma** coordenada válida — a coordenada simétrica extrema.  É aí
que vive todo o resto do problema. -/
theorem excepcional_unica (k : Fin 6) (hk : k.val < 2) :
    (Finset.univ.filter
      (fun u : Coord => valida u && exibivel u k && assinatura u k == [0, 0, 0, 0])).card
      = 1 := by
  revert hk
  revert k
  decide

end Flexagonos
