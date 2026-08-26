"""
quadflex.py  --  Teoria geral dos *flexes de quadrantes* do quadrado Q=[-1,1]^2.

Um flex e uma bijecao Phi de Q (definida fora dos eixos), isometria DIRETA em
cada quadrante aberto, que permuta os quadrantes:

      Phi|_{Q_j}(z) = A_j(z) = eps_j (z - c_j) + c_{sigma(j)} ,
      eps_j em mu_4 = {1,i,-1,-i},   sigma em S_4 .

Q_1=[0,1]^2 , Q_2=[-1,0]x[0,1] , Q_3=[-1,0]^2 , Q_4=[0,1]x[-1,0]
c_1=(1+i)/2 , c_2=(-1+i)/2 , c_3=(-1-i)/2 , c_4=(1-i)/2 .

Grupo dos flexes:  F = mu_4 wr S_4 ,  |F| = 4^4 * 4! = 6144.

TEOREMA (ver artigo):  para f meromorfa em C,
   f o Phi^{-1} se estende a uma funcao meromorfa numa vizinhanca de Q
   <=>  f e invariante por  Gamma_Phi := < A_k^{-1} A_j : 1<=j,k<=4 >.

Toda a aritmetica e exata: os elementos de Gamma_Phi tem a forma
   z |-> i^a z + t/2 ,  a em Z/4 ,  t em Z[i] ,
representados pelo par (a, t) com t = (tx,ty) inteiros.
"""
from itertools import permutations, product
from math import gcd
from collections import Counter

# ---------------------------------------------------------------- Z[i] exato
def zmul(u, v):                      # (a+bi)(c+di)
    return (u[0]*v[0] - u[1]*v[1], u[0]*v[1] + u[1]*v[0])

IPOW = [(1, 0), (0, 1), (-1, 0), (0, -1)]        # i^0, i^1, i^2, i^3

# 2*c_j  em Z[i]
TWOC = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}


# ------------------------------ grupo  mu_4 |x (1/2)Z[i] : elemento (a, t)
def comp(g, h):                      # g o h
    a1, t1 = g; a2, t2 = h
    return ((a1 + a2) % 4, tuple(x + y for x, y in zip(zmul(IPOW[a1], t2), t1)))


def inv(g):
    a, t = g
    ai = (-a) % 4
    r = zmul(IPOW[ai], t)
    return (ai, (-r[0], -r[1]))


IDG = (0, (0, 0))


# ---------------------------------------------------------------- reticulados
def hnf(rows):
    """Base de Hermite do Z-modulo de Z^2 gerado pelas linhas."""
    rows = [list(r) for r in rows if any(r)]
    if not rows: return []
    piv = 0
    for col in range(2):
        k = next((i for i in range(piv, len(rows)) if rows[i][col] != 0), None)
        if k is None: continue
        rows[piv], rows[k] = rows[k], rows[piv]
        again = True
        while again:
            again = False
            for i in range(piv + 1, len(rows)):
                if rows[i][col] != 0:
                    q = rows[i][col] // rows[piv][col]
                    rows[i] = [rows[i][t] - q * rows[piv][t] for t in range(2)]
                    if rows[i][col] != 0:
                        rows[piv], rows[i] = rows[i], rows[piv]
                        again = True
        piv += 1
    return [tuple(r) for r in rows if any(r)]


# ---------------------------------------------------------------- flexes
class Flex:
    __slots__ = ("sigma", "eps", "A")

    def __init__(self, sigma, eps):
        self.sigma = sigma            # tupla (sigma(1),...,sigma(4))
        self.eps = eps                # tupla de indices a_j em Z/4
        self.A = []
        for j in (1, 2, 3, 4):
            a = eps[j - 1]
            t = tuple(x - y for x, y in zip(TWOC[sigma[j - 1]],
                                            zmul(IPOW[a], TWOC[j])))
            self.A.append((a, t))     # A_j : z -> i^a z + t/2

    def gamma_gens(self):
        out = set()
        for j in range(4):
            for k in range(4):
                g = comp(inv(self.A[k]), self.A[j])
                if g != IDG: out.add(g)
        return sorted(out)

    def __repr__(self):
        nm = {0: "1", 1: "i", 2: "-1", 3: "-i"}
        return f"Flex(sigma={self.sigma}, eps=({','.join(nm[e] for e in self.eps)}))"


# -------------------------- estrutura de Gamma  (Reidemeister-Schreier exato)
def gamma_structure(flex):
    gens = flex.gamma_gens()
    if not gens:
        return dict(trivial=True, P=1, rank=0, lattice=[], centers=[])

    # grupo de pontos P = < a_j > <= Z/4
    ags = {a for a, _ in gens} | {0}
    d = 0
    for a in ags: d = gcd(d, a)
    d = gcd(d, 4)
    P = [(d * k) % 4 for k in range(4 // d)] if d else [0]
    P = sorted(set(P))
    nP = len(P)

    # representantes de classes laterais: precisamos de r_p com multiplicador p.
    rep = {0: IDG}
    frontier = [IDG]
    while frontier:
        new = []
        for r in frontier:
            for g in gens:
                h = comp(r, g)
                if h[0] not in rep:
                    rep[h[0]] = h
                    new.append(h)
        frontier = new
    assert set(rep) == set(P), (set(rep), set(P))

    # geradores de Schreier do nucleo (= subgrupo das translacoes)
    T = []
    for p, r in rep.items():
        for g in gens:
            h = comp(r, g)
            s = comp(h, inv(rep[h[0]]))
            assert s[0] == 0
            if s[1] != (0, 0): T.append(s[1])
    # fechar sob o grupo de pontos
    for _ in range(2):
        B = hnf(T)
        for a in P:
            for v in B: T.append(zmul(IPOW[a], v))
    B = hnf(T)

    centers = sorted({inv_center(g) for g in gens if g[0] != 0})
    return dict(trivial=False, P=nP, rank=len(B), lattice=B, centers=centers)


def inv_center(g):
    """ponto fixo de z -> i^a z + t/2, em (1/4)Z[i]: devolve (x*4, y*4) inteiros."""
    a, t = g
    # p = (t/2) / (1 - i^a)
    num = (t[0], t[1])
    den = (1 - IPOW[a][0], -IPOW[a][1])
    n2 = den[0] * den[0] + den[1] * den[1]
    # p = num * conj(den) / (2 * n2)
    pr = (num[0] * den[0] + num[1] * den[1])
    pi = (num[1] * den[0] - num[0] * den[1])
    from fractions import Fraction as Fr
    return (Fr(pr, 2 * n2), Fr(pi, 2 * n2))


def label(st):
    if st["trivial"]:
        return "I  : Gamma = {1}          -> toda f meromorfa serve"
    if st["rank"] == 0:
        return f"II : Gamma = C_{st['P']} (rotacao finita) -> f(z)=h((z-p)^{st['P']})"
    if st["rank"] == 1:
        return f"III: Gamma posto 1, |P|={st['P']}   -> f periodica"
    return f"IV : Gamma posto 2, |P|={st['P']}   -> f ELIPTICA (nenhuma inteira nao const.)"


def all_flexes():
    for sg in permutations((1, 2, 3, 4)):
        for e in product(range(4), repeat=4):
            yield Flex(sg, e)


# ---------------------------------------------------------------- main
def latstr(B):
    """B esta em unidades de 1/2 (guardamos t = 2*translacao)."""
    from fractions import Fraction as Fr
    def s(v):
        a, b = Fr(v[0], 2), Fr(v[1], 2)
        if b == 0: return f"{a}"
        if a == 0: return f"{b}i"
        return f"{a}{'+' if b > 0 else '-'}{abs(b)}i"
    return " Z + ".join(s(v) for v in B) + (" Z" if B else "-")


def covol(B):
    from fractions import Fraction as Fr
    if len(B) < 2: return None
    return abs(Fr(B[0][0] * B[1][1] - B[0][1] * B[1][0], 4))


if __name__ == "__main__":
    cnt = Counter(); ex = {}; lats = Counter()
    for Phi in all_flexes():
        st = gamma_structure(Phi)
        key = (st["rank"], st["P"])
        cnt[key] += 1
        ex.setdefault(key, (Phi, st))
        if st["rank"] == 2:
            lats[(covol(st["lattice"]), st["P"])] += 1
    tot = sum(cnt.values())
    print(f"total de flexes de quadrantes |mu_4 wr S_4| = {tot}\n")
    print("CLASSIFICACAO POR (posto do reticulado de translacoes, ordem do grupo de pontos)")
    print("-" * 88)
    print(f"{'posto':>5} {'|P|':>4} {'#flexes':>9} {'%':>7}   solucoes f")
    sol = {(0, 1): "quaisquer (Gamma trivial)",
           (0, 2): "f(z) = h((z-p)^2)                [inteiras existem]",
           (0, 4): "f(z) = h((z-p)^4)                [inteiras existem]",
           (1, 1): "f(z) = h(e^{2 pi i (z-p)/w})     [inteiras existem]",
           (1, 2): "f(z) = H(cos(2 pi (z-p)/w))      [inteiras existem]",
           (2, 1): "f eliptica: C(P, P')             [NENHUMA inteira nao const.]",
           (2, 2): "f eliptica par:  C(P(z-p))       [NENHUMA inteira nao const.]",
           (2, 4): "f = R(P(z-p)^2), retic. quadrado [NENHUMA inteira nao const.]"}
    for key in sorted(cnt):
        n = cnt[key]
        print(f"{key[0]:>5} {key[1]:>4} {n:>9} {100*n/tot:6.2f}%   {sol.get(key,'?')}")
    print("\nexemplos minimos de cada classe:")
    for key in sorted(ex):
        Phi, st = ex[key]
        print(f"  posto={key[0]} |P|={key[1]}: {Phi}")
        print(f"       reticulado = {latstr(st['lattice'])}")
    print("\ncovolumes que ocorrem no posto 2 (|P|, covolume) -> #flexes:")
    for k in sorted(lats, key=lambda k: (k[1], k[0])):
        print(f"   |P|={k[1]}  covol={k[0]}   ->  {lats[k]}")
