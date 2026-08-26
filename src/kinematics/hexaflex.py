"""
hexaflex.py
===========
HEXAFLEXAGONOS: dobraduras planas de uma tira de triangulos equilateros sobre
um hexagono de 6 triangulos, e os seus mapas de retorno.

Reticulado triangular Z[w], w = e^{i pi/3}, w^2 = w - 1, conj(a+bw) = (a+b)-bw.
Isometria  g = (a, s, t):  z -> w^a conj^s(z) + t.

Tira reta: celula 2k = {k, k+w, k+1};  celula 2k+1 = {k+w, k+1, k+1+w}.
Hexagono centrado em v: tiles {v, v+w^k, v+w^{k+1}}, k = 0..5.

O tri-hexaflexagono classico usa 10 triangulos, com o ultimo colado no primeiro
(9 celulas efetivas, 18 lados = 3 faces x 6).  As FACES nao sao postuladas: sao
DEDUZIDAS, procurando uma particao dos 18 lados em 3 conjuntos que possam,
cada um, ocupar os 6 tiles simultaneamente nalgum estado.
"""
from itertools import product, combinations
from collections import defaultdict

# --------------------------------------------------------------- Z[w]
def wmul(u, v):
    """(a+bw)(c+dw) = (ac-bd) + (ad+bc+bd) w   pois w^2 = w-1."""
    a, b = u; c, d = v
    return (a*c - b*d, a*d + b*c + b*d)
def wconj(u): return (u[0] + u[1], -u[1])
def wadd(u, v): return (u[0]+v[0], u[1]+v[1])
def wsub(u, v): return (u[0]-v[0], u[1]-v[1])
W = [(1, 0)]
for _ in range(5): W.append(wmul(W[-1], (0, 1)))       # w^0 .. w^5

# --------------------------------------------------------------- isometrias
def comp(g, h):
    a, s, t = g; b, u, r = h
    if s == 0: return ((a+b) % 6, u, wadd(wmul(W[a], r), t))
    return ((a-b) % 6, 1-u, wadd(wmul(W[a], wconj(r)), t))
def apply(g, z):
    a, s, t = g
    return wadd(wmul(W[a], wconj(z) if s else z), t)
ID = (0, 0, (0, 0)); REF = (0, 1, (0, 0))

def refl(P, u_idx):
    """reflexao na reta por P com direcao w^{u_idx} (unidade), escrita em
       coordenadas TRIPLICADAS (os centroides sao guardados x3, e a parte de
       translacao tem de ser escalada do mesmo fator)."""
    a = (2*u_idx) % 6
    t = wsub(P, wmul(W[a], wconj(P)))
    return (a, 1, (3*t[0], 3*t[1]))

# --------------------------------------------------------------- a tira
def tira(N):
    cel, cent, hin = [], [], []
    for m in range(N):
        k = m // 2
        if m % 2 == 0:
            v = [(k, 0), (k, 1), (k+1, 0)]
        else:
            v = [(k, 1), (k+1, 0), (k+1, 1)]
        cel.append(v)
        cent.append((v[0][0]+v[1][0]+v[2][0], v[0][1]+v[1][1]+v[2][1]))  # x3
    for m in range(N-1):
        k = m // 2
        if m % 2 == 0: P, ui = (k, 1), 5          # direcao (1,-1) = w^5
        else:          P, ui = (k+1, 0), 1        # direcao (0,1)  = w^1
        hin.append((m, m+1, refl(P, ui)))
    return cel, cent, hin

# --------------------------------------------------------------- hexagono alvo
REF_TILES = [wadd(W[k], W[(k+1) % 6]) for k in range(6)]      # centroides x3, v=0

def hexagono(cents):
    """os centroides distintos formam um hexagono?  devolve v (x3) ou None."""
    S = sorted(set(cents))
    if len(S) != 6: return None
    tot = (sum(p[0] for p in S), sum(p[1] for p in S))
    if tot[0] % 18 or tot[1] % 18: return None
    v = (tot[0]//18, tot[1]//18)
    alvo = sorted(wadd((3*v[0], 3*v[1]), r) for r in REF_TILES)
    return v if alvo == S else None

def indice_tile(c, v):
    alvo = [wadd((3*v[0], 3*v[1]), r) for r in REF_TILES]
    return alvo.index(c)

# --------------------------------------------------------------- enumeracao
def enumerar(N, cola=True):
    cel, cent, hin = tira(N)
    saida = []
    for g0 in (ID, REF):
        for bits in product((0, 1), repeat=N-1):
            g = [g0]
            for (m, mm, R), b in zip(hin, bits):
                g.append(comp(g[-1], R) if b else g[-1])
            pos = [apply(g[i], cent[i]) for i in range(N)]
            if cola and pos[0] != pos[N-1]: continue
            v = hexagono(pos)
            if v is None: continue
            saida.append((bits, tuple(g), tuple(pos), v))
    return saida

def potenciais_faces(estados, N):
    """conjuntos de 6 lados (celula, s) que ocupam os 6 tiles nalgum estado."""
    pf = set()
    for bits, g, pos, v in estados:
        portile = defaultdict(list)
        for i in range(N):
            portile[indice_tile(pos[i], v)].append(i)
        if len(portile) != 6: continue
        for esc in product(*[portile[t] for t in range(6)]):
            if len(set(esc)) != 6: continue
            pf.add(tuple(sorted((i, g[i][1]) for i in esc)))
    return sorted(pf)

def particoes(pf, lados):
    """particoes de `lados` em 3 faces potenciais."""
    out = []
    L = set(lados)
    for a in pf:
        sa = set(a)
        if not sa <= L: continue
        resto = L - sa
        for b in pf:
            sb = set(b)
            if not sb <= resto: continue
            sc = resto - sb
            if tuple(sorted(sc)) in set(pf): out.append((a, b, tuple(sorted(sc))))
    return out


if __name__ == "__main__":
    N = 10
    est = enumerar(N)
    print(f"tri-hexaflexagono: tira de {N} triangulos, colagem 1<->{N}")
    print(f"  dobraduras planas sobre um hexagono: {len(est)}")
    if est:
        bits, g, pos, v = est[0]
        portile = defaultdict(list)
        for i in range(N): portile[indice_tile(pos[i], v)].append(i)
        print(f"  exemplo: espessuras por tile = "
              f"{sorted(len(x) for x in portile.values())}")
    # lados efetivos: identificamos as celulas coladas 0 e N-1
    ident = {N-1: 0}
    lados = sorted({(ident.get(i, i), s) for i in range(N) for s in (0, 1)})
    print(f"  lados de celula (apos a colagem): {len(lados)}")
    pf = potenciais_faces(est, N)
    print(f"  faces potenciais (6 lados cobrindo os 6 tiles): {len(pf)}")
    parts = particoes(pf, [(i, s) for i in range(N) for s in (0, 1)])
    print(f"  particoes dos lados em 3 faces: {len(parts)}")
