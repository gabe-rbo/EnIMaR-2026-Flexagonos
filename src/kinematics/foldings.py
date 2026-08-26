"""
foldings.py
===========
Enumeracao EXATA de todas as dobraduras planas do anel de 12 quadradinhos do
hexa-tetraflexagono sobre um quadrado 2x2, e extraccao dos *mapas de retorno*
de cada face.

Ideia.  Uma dobradura plana e uma atribuicao, a cada quadradinho C, de uma
isometria g_C do plano, tal que quadradinhos vizinhos C ~ C' com aresta comum e
satisfazem  g_{C'} = g_C  (sem dobra)  ou  g_{C'} = g_C o ref_e  (dobra na
aresta e).  Como o plano e um ciclo de 12 quadradinhos, basta escolher
g da primeira celula e um vetor de 12 bits (dobra / nao dobra) e verificar
que o ciclo fecha.

Mapa de retorno.  A face k so pode ser exibida numa dobradura em que os seus 4
quadradinhos ocupem as 4 posicoes distintas do quadrado 2x2 com o lado k para
cima.  Se ha dois estados S, S' assim, o desenho pintado para ficar certo em S
aparece em S' rearranjado por um flex de quadrantes bem definido --- e esse
rearranjo NAO depende de nenhuma convencao de como se desenha o verso do papel
(o fator de convencao cancela na razao entre os dois estados).

Isometrias em coordenadas DOBRADAS (inteiros de Gauss):
    g = (a, s, b)  :  z |-> i^a * conj^s(z) + b .
Centro do quadradinho (r,c):  (2c+1) - (2r+1) i .
"""
from itertools import product
from collections import defaultdict

# ---------------------------------------------------------------- Z[i]
def zmul(u, v): return (u[0]*v[0] - u[1]*v[1], u[0]*v[1] + u[1]*v[0])
def zconj(u):   return (u[0], -u[1])
def zadd(u, v): return (u[0]+v[0], u[1]+v[1])
IP = [(1, 0), (0, 1), (-1, 0), (0, -1)]

def comp(g, h):
    """g o h, com g=(a,s,b), h=(a2,s2,b2)."""
    a, s, b = g; a2, s2, b2 = h
    if s == 0:
        return ((a + a2) % 4, s2, zadd(zmul(IP[a], b2), b))
    return ((a - a2) % 4, 1 - s2, zadd(zmul(IP[a], zconj(b2)), b))

def apply(g, z):
    a, s, b = g
    return zadd(zmul(IP[a], zconj(z) if s else z), b)

ID = (0, 0, (0, 0))

def ref_vert(Xd):   # reta x = Xd/2 (coords dobradas: x = Xd) -> z |-> 2Xd - conj z
    return (2, 1, (2*Xd, 0))
def ref_horiz(Yd):  # reta y = Yd -> z |-> conj z + 2i Yd
    return (0, 1, (0, 2*Yd))

# ---------------------------------------------------------------- o anel
RING = [(0,0),(0,1),(0,2),(0,3),(1,3),(2,3),(3,3),(3,2),(3,1),(3,0),(2,0),(1,0)]
def centro(cel):
    r, c = cel; return (2*c + 1, -(2*r + 1))

def aresta_entre(A, B):
    """reflexao na aresta comum dos quadradinhos vizinhos A, B."""
    (r1, c1), (r2, c2) = A, B
    if r1 == r2:                      # vizinhos horizontais
        X = 2*max(c1, c2)             # x = max(c) em coords dobradas = 2*max(c)
        return ref_vert(X)
    Y = -2*max(r1, r2)
    return ref_horiz(Y)

# ---- faces: manual, Figuras 1.2 e 1.3 (numero da face e quadrante)
# frente do papel
FRENTE = {(0,0):(4,3), (0,1):(2,1), (0,2):(6,2), (0,3):(6,1),
          (1,3):(2,2), (2,3):(4,2), (3,3):(4,1), (3,2):(2,3),
          (3,1):(6,4), (3,0):(6,3), (2,0):(2,4), (1,0):(4,4)}
# verso: celula da frente (r,c) tem no verso a celula (r,3-c) do plano traseiro
_TRAS = {(0,0):(5,4), (0,1):(1,1), (0,2):(3,1), (0,3):(3,2),
         (1,3):(1,2), (2,3):(5,1), (3,3):(5,2), (3,2):(1,3),
         (3,1):(3,3), (3,0):(3,4), (2,0):(1,4), (1,0):(5,3)}
VERSO = {(r, c): _TRAS[(r, 3-c)] for (r, c) in FRENTE}


# ---------------------------------------------------------------- enumeracao
REF = (0, 1, (0, 0))          # reflexao global (virar o flexagono do avesso)

def enumerar():
    """Enumera as dobraduras planas a menos de translacao.  g da primeira celula
    percorre {ID, REF}: fixar so ID perderia todos os estados em que o verso do
    papel esta para cima."""
    n = len(RING)
    refs = [aresta_entre(RING[i], RING[(i+1) % n]) for i in range(n)]
    saida = []
    for g0 in (ID, REF):
      for bits in product((0, 1), repeat=n):
        g = [g0]
        ok = True
        for i in range(n):
            nxt = comp(g[-1], refs[i]) if bits[i] else g[-1]
            if i < n - 1:
                g.append(nxt)
            else:
                if nxt != g0: ok = False       # o ciclo tem de fechar
        if not ok: continue
        pos = [apply(g[i], centro(RING[i])) for i in range(n)]
        d = defaultdict(list)
        for i, p in enumerate(pos): d[p].append(i)
        if len(d) != 4: continue
        xs = sorted({p[0] for p in d}); ys = sorted({p[1] for p in d})
        if len(xs) != 2 or len(ys) != 2: continue
        if xs[1]-xs[0] != 2 or ys[1]-ys[0] != 2: continue   # bloco 2x2
        saida.append((bits, tuple(g), tuple(pos)))
    return saida


def quadrante(p, xs, ys):
    """posicao -> indice de quadrante 1..4 (convencao cartesiana)."""
    dir_ = p[0] == xs[1]; cima = p[1] == ys[1]
    return 1 if (dir_ and cima) else 2 if (not dir_ and cima) else 3 if not dir_ else 4


def estados_por_face(folds):
    """para cada face k, lista de (arranjo) onde arranjo[j] = (quadrante, rot)."""
    out = defaultdict(list)
    for bits, g, pos in folds:
        xs = sorted({p[0] for p in pos}); ys = sorted({p[1] for p in pos})
        vis = {}
        for i, cel in enumerate(RING):
            a, s, _ = g[i]
            face, quad = (FRENTE if s == 0 else VERSO)[cel]
            vis.setdefault(face, {})[quad] = (quadrante(pos[i], xs, ys), a)
        for face, arr in vis.items():
            if len(arr) == 4 and len({v[0] for v in arr.values()}) == 4:
                out[face].append(tuple(arr[j] for j in (1, 2, 3, 4)))
    return {k: sorted(set(v)) for k, v in out.items()}


def mapa_retorno(arrS, arrSl):
    """flex (sigma, eps) que leva o arranjo S no arranjo S'.
       sigma(q) = posicao em S' do quadrante que em S ocupava a posicao q."""
    sigma = {}; eps = {}
    for j in range(4):
        qS, aS = arrS[j]; qL, aL = arrSl[j]
        sigma[qS] = qL
        eps[qS] = (aL - aS) % 4
    return tuple(sigma[q] for q in (1, 2, 3, 4)), tuple(eps[q] for q in (1, 2, 3, 4))


if __name__ == "__main__":
    folds = enumerar()
    print(f"dobraduras planas validas do anel sobre o quadrado 2x2: {len(folds)}")
    est = estados_por_face(folds)
    print("\nestados (arranjos distintos) em que cada face pode ser exibida:")
    for k in sorted(est):
        print(f"   face {k}: {len(est[k])} arranjo(s)")
    print("\nmapas de retorno (sigma; eps em potencias de i):")
    nome = {0: '1', 1: 'i', 2: '-1', 3: '-i'}
    todos = {}
    for k in sorted(est):
        arrs = est[k]
        vistos = set()
        for i in range(len(arrs)):
            for j in range(len(arrs)):
                if i == j: continue
                sg, ep = mapa_retorno(arrs[i], arrs[j])
                if (sg, ep) in vistos: continue
                vistos.add((sg, ep))
        todos[k] = sorted(vistos)
        print(f"   face {k}: {len(vistos)} mapa(s) de retorno nao triviais")
        for sg, ep in sorted(vistos)[:8]:
            print(f"       sigma={sg}  eps=({','.join(nome[e] for e in ep)})")
    import json, pickle
    with open("retornos.pkl", "wb") as f: pickle.dump(todos, f)
