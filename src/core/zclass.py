"""
zclass.py
=========
Classificacao EXATA de um grupo Gamma de isometrias diretas do plano da forma

        z |-> zeta^a z + t ,     zeta = e^{2 pi i / n},  t em Q(zeta),

para n = 4 (Z[i]) ou n = 6 (Z[omega], omega = e^{i pi /3}).  E o motor comum a
todos os flexagonos: quadrados, triangulares, e quaisquer outros.

Representacao: t = (p, q)/d  significa  (p + q*zeta)/d  com p,q,d inteiros.
Multiplicacao por zeta na base {1, zeta}: matriz M.
   n=4 : zeta = i,     i*(a+bi) = -b + a i          -> M = [[0,-1],[1,0]]
   n=6 : zeta = omega, w*(a+bw) = -b + (a+b) w      -> M = [[0,-1],[1,1]]
   (omega^2 = omega - 1,  omega^6 = 1)
"""
from fractions import Fraction as Fr
from math import gcd

MULT = {4: ((0, -1), (1, 0)), 6: ((0, -1), (1, 1))}


class Anel:
    """Z[zeta_n] e Q(zeta_n) na base {1, zeta}."""

    def __init__(self, n):
        assert n in MULT, "apenas n = 4 ou 6"
        self.n = n
        self.M = MULT[n]

    def mulz(self, v):                      # multiplica por zeta
        (m00, m01), (m10, m11) = self.M
        return (m00*v[0] + m01*v[1], m10*v[0] + m11*v[1])

    def zpow(self, k, v):
        k %= self.n
        for _ in range(k): v = self.mulz(v)
        return v

    def emb(self, v):
        """imersao em C (float) para conferencia."""
        import cmath
        z = cmath.exp(2j*cmath.pi/self.n)
        return v[0] + v[1]*z


# --------------------------------------------------- elementos de Gamma
# g = (a, t)  com a em Z/n  e  t em (Q(zeta))^  representado por (p,q) sobre um
# denominador COMUM d fixado por quem chama.
def comp(A, g, h):
    """g o h ; g=(a,t), h=(b,u):  z -> zeta^a (zeta^b z + u) + t."""
    a, t = g; b, u = h
    zu = A.zpow(a, u)
    return ((a + b) % A.n, (t[0] + zu[0], t[1] + zu[1]))


def inv(A, g):
    a, t = g
    ai = (-a) % A.n
    zt = A.zpow(ai, t)
    return (ai, (-zt[0], -zt[1]))


def ident(): return (0, (0, 0))


# --------------------------------------------------- reticulados em Z^2
def hnf(rows):
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
            for i in range(piv+1, len(rows)):
                if rows[i][col] != 0:
                    q = rows[i][col] // rows[piv][col]
                    rows[i] = [rows[i][t] - q*rows[piv][t] for t in range(2)]
                    if rows[i][col] != 0:
                        rows[piv], rows[i] = rows[i], rows[piv]; again = True
        piv += 1
    return [tuple(r) for r in rows if any(r)]


def estrutura(A, geradores):
    """geradores: lista de (a, (p,q)) sobre um denominador comum implicito.
       devolve dict com 'P' (ordem do grupo de pontos), 'rank', 'lattice'."""
    gens = [g for g in geradores if g != ident()]
    if not gens:
        return dict(P=1, rank=0, lattice=[], centros=[])
    d = 0
    for a, _ in gens: d = gcd(d, a)
    d = gcd(d, A.n)
    P = sorted({(d*k) % A.n for k in range(A.n // d)}) if d else [0]

    rep = {0: ident()}
    fronteira = [ident()]
    while fronteira:
        novo = []
        for r in fronteira:
            for g in gens:
                h = comp(A, r, g)
                if h[0] not in rep:
                    rep[h[0]] = h; novo.append(h)
        fronteira = novo
    T = []
    for p, r in rep.items():
        for g in gens:
            h = comp(A, r, g)
            s = comp(A, h, inv(A, rep[h[0]]))
            assert s[0] == 0
            if s[1] != (0, 0): T.append(s[1])
    for _ in range(2):
        B = hnf(T)
        for a in P:
            for v in B: T.append(A.zpow(a, v))
    B = hnf(T)
    return dict(P=len(P), rank=len(B), lattice=B, pontos=P)


CLASSES = {
    (0, 1): ("Gamma trivial", "toda f meromorfa"),
    (0, 2): ("C_2", "f = h((z-p)^2)"),
    (0, 3): ("C_3", "f = h((z-p)^3)"),
    (0, 4): ("C_4", "f = h((z-p)^4)"),
    (0, 6): ("C_6", "f = h((z-p)^6)"),
    (1, 1): ("friso p1", "f = h(exp(2 pi i (z-p)/w))"),
    (1, 2): ("friso p2", "f = H(cos(2 pi (z-p)/w))"),
    (2, 1): ("p1", "f em C(P, P')  [eliptica]"),
    (2, 2): ("p2", "f em C(P(z-p))"),
    (2, 3): ("p3", "f em C(P'(z-p)) ; reticulado hexagonal, g2=0, j=0"),
    (2, 4): ("p4", "f em C(P(z-p)^2) ; reticulado quadrado, g3=0, j=1728"),
    (2, 6): ("p6", "f em C(P'(z-p)^2) ; reticulado hexagonal, g2=0, j=0"),
}


def rotulo(st):
    return CLASSES.get((st["rank"], st["P"]), ("?", "?"))
