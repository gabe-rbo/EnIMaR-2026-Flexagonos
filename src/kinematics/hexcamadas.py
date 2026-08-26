"""
hexcamadas.py
=============
Modelo com camadas para HEXAFLEXAGONOS (o analogo triangular de
flexcamadas.py).  Estado dobrado = (isometria por folha, ordem total das
folhas em cada um dos 6 ladrilhos) sujeito as condicoes de Justin; uma face
so esta EXIBIDA quando os seis lados visiveis sao os das folhas de TOPO.

A tira tem N triangulos, o ultimo colado no primeiro (mesma posicao, camadas
contiguas).
"""
from itertools import permutations, product
from collections import defaultdict
import hexaflex as H

W, wmul, wconj, wadd, wsub = H.W, H.wmul, H.wconj, H.wadd, H.wsub
_OP = None


def apply6(g, z6):
    """imagem de um ponto dado em coordenadas x6 (t de g esta em x3)."""
    a, s, t = g
    return wadd(wmul(W[a], wconj(z6) if s else z6), (2*t[0], 2*t[1]))


def dados(N):
    cel, cent, hin = H.tira(N)
    hinges = [(m, m+1) for m in range(N-1)]
    meio6 = []
    for m in range(N-1):
        com = [P for P in cel[m] if P in cel[m+1]]
        assert len(com) == 2
        P, Q = com
        meio6.append((3*(P[0]+Q[0]), 3*(Q[1]+P[1])))
    return cel, cent, hinges, meio6


def estrutura(N, g, tile, meio6, pos):
    tacos = defaultdict(list); tort = defaultdict(list)
    for h in range(N-1):
        i, j = h, h+1
        q = apply6(g[i], meio6[h])
        lado = wsub(q, (2*pos[i][0], 2*pos[i][1]))
        if tile[i] == tile[j]:
            tacos[(tile[i], lado)].append((i, j))
        else:
            q2 = apply6(g[j], meio6[h])
            lado2 = wsub(q2, (2*pos[j][0], 2*pos[j][1]))
            tort[(tile[i], lado)].append((i, j))
            tort[(tile[j], lado2)].append((j, i))
    return tacos, tort


def valida(tacos, tort, nivel):
    for ch, pares in tacos.items():
        iv = [tuple(sorted((nivel[u], nivel[v]))) for u, v in pares]
        for a in range(len(iv)):
            for b in range(a+1, len(iv)):
                (l1, h1), (l2, h2) = iv[a], iv[b]
                if l1 < l2 < h1 < h2 or l2 < l1 < h2 < h1: return False
        for lo, hi in iv:
            for w, _ in tort.get(ch, ()):
                if lo < nivel[w] < hi: return False
    for ch, pares in tort.items():
        for a in range(len(pares)):
            for b in range(a+1, len(pares)):
                u, u2 = pares[a]; v, v2 = pares[b]
                if (nivel[u] < nivel[v]) != (nivel[u2] < nivel[v2]): return False
    return True


def ordens(N, g, tile, tacos, tort, cola):
    """cola: None, 'igual' (s iguais) ou 'oposto' (s opostos) para 0 <-> N-1."""
    porp = defaultdict(list)
    for i in range(N): porp[tile[i]].append(i)
    ts = sorted(porp); out = []
    for esc in product(*[permutations(porp[t]) for t in ts]):
        nv = {}
        for t, o in zip(ts, esc):
            for k, c in enumerate(o): nv[c] = k
        if cola is not None:
            if tile[0] != tile[N-1]: return []
            if abs(nv[0] - nv[N-1]) != 1: continue
            mesmo = (g[0][1] == g[N-1][1])
            if cola == 'igual' and not mesmo: continue
            if cola == 'oposto' and mesmo: continue
        if valida(tacos, tort, nv): out.append(tuple(sorted(zip(ts, esc))))
    return out


def estados(N, cola='oposto'):
    cel, cent, hinges, meio6 = dados(N)
    out = []
    for bits, g, pos, v in H.enumerar(N):
        tile = [H.indice_tile(pos[i], v) for i in range(N)]
        if len(set(tile)) != 6: continue
        ta, to = estrutura(N, g, tile, meio6, pos)
        for o in ordens(N, g, tile, ta, to, cola):
            out.append((g, tile, o, v))
    return out


def exibida(N, g, tile, ordem):
    """os 6 lados de topo; devolve (conjunto de lados, arranjo lado->(tile,rot))."""
    arr = {}
    for t, cells in ordem:
        i = cells[-1]
        lado = (0 if i == N-1 else i, g[i][1])
        arr[lado] = (t, g[i][0])
    if len(arr) != 6: return None
    return frozenset(arr), arr


if __name__ == "__main__":
    import sys
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    for cola in ('oposto', 'igual', None):
        est = estados(N, cola)
        vis = defaultdict(list)
        for g, tile, o, v in est:
            r = exibida(N, g, tile, o)
            if r: vis[r[0]].append(r[1])
        mult = {k: v for k, v in vis.items() if len(v) > 1}
        print(f"cola={cola}: {len(est)} estados dobrados; "
              f"{len(vis)} faces exibidas; {len(mult)} em mais de um arranjo")


# ===================================================================== flexes
def ImC(z): return z[1]                     # componente em w  (~ parte imaginaria)


def lado_reta(z, u, P):
    """sinal do lado de z relativo a reta por P com direcao w^u (mesma escala)."""
    return ImC(wmul(W[(-u) % 6], wsub(z, P)))


def tri_vertices(c3):
    """vertices (nao escalados) do triangulo de centroide c3 (x3)."""
    a, b = c3
    if (a - 1) % 3 == 0 and (b - 1) % 3 == 0:
        p = ((a-1)//3, (b-1)//3)
        return [p, (p[0]+1, p[1]), (p[0], p[1]+1)]
    p = ((a-2)//3, (b-2)//3)
    return [(p[0]+1, p[1]), (p[0], p[1]+1), (p[0]+1, p[1]+1)]


def retas(cents):
    """retas do reticulado que contem arestas dos triangulos do footprint;
       (u, offset) -> ponto P (nao escalado) da reta."""
    out = {}
    for c3 in cents:
        V = tri_vertices(c3)
        for k in range(3):
            P, Q = V[k], V[(k+1) % 3]
            d = wsub(Q, P)
            for u in range(3):
                if d == W[u] or d == wsub((0, 0), W[u]):
                    out[(u, lado_reta(P, u, (0, 0)))] = P
                    break
    return out


def normaliza(g, pil):
    cents = [c for c, _ in pil]
    m = min(cents)
    r = (1, 1) if (m[0]-1) % 3 == 0 and (m[1]-1) % 3 == 0 else (2, 2)
    t = ((m[0]-r[0])//3, (m[1]-r[1])//3)
    T = (0, 0, (-3*t[0], -3*t[1]))
    ng = tuple(H.comp(T, gi) for gi in g)
    npil = tuple(sorted(((c[0]-3*t[0], c[1]-3*t[1]), cs) for c, cs in pil))
    return ng, npil


class Hexa:
    def __init__(s, N, cola='oposto', maxtiles=6):
        s.N = N; s.cola = cola; s.maxtiles = maxtiles
        s.cel, s.cent, s.hinges, s.meio6 = dados(N)

    def pos(s, g): return [H.apply(g[i], s.cent[i]) for i in range(s.N)]

    def ok(s, g, pil):
        p = s.pos(g); idx = {}
        for c, cs in (pil.items() if isinstance(pil, dict) else pil):
            for k, i in enumerate(cs): idx[i] = (c, k)
        tile = [idx[i][0] for i in range(s.N)]
        ta, to = estrutura(s.N, g, tile, s.meio6, p)
        nv = {i: idx[i][1] for i in range(s.N)}
        if not valida(ta, to, nv): return False
        if s.cola:
            if tile[0] != tile[s.N-1] or abs(nv[0]-nv[s.N-1]) != 1: return False
            if (g[0][1] == g[s.N-1][1]) != (s.cola == 'igual'): return False
        return True

    def dobrar(s, g, pil, u, P, sinal, acima):
        R = H.refl(P, u)
        d = dict(pil); novo = {}; ng = list(g)
        mov = [c for c in d if (lado_reta(c, u, (3*P[0], 3*P[1])) > 0) == (sinal > 0)
               and lado_reta(c, u, (3*P[0], 3*P[1])) != 0]
        for c in mov:
            for i in d[c]: ng[i] = H.comp(R, g[i])
        for c, cs in d.items():
            if c in mov: continue
            q = None
            for c2 in mov:
                if H.apply(R, c2) == c: q = c2; break
            novo[c] = (cs + tuple(reversed(d[q])) if acima
                       else tuple(reversed(d[q])) + cs) if q else cs
        for c2 in mov:
            im = H.apply(R, c2)
            if im not in novo: novo[im] = tuple(reversed(d[c2]))
        return tuple(ng), novo

    def _arcos(s, corta):
        pai = list(range(s.N))
        def acha(x):
            while pai[x] != x: pai[x] = pai[pai[x]]; x = pai[x]
            return x
        for h, (i, j) in enumerate(s.hinges):
            if corta[h]: continue
            ra, rb = acha(i), acha(j)
            if ra != rb: pai[ra] = rb
        if s.cola:
            ra, rb = acha(0), acha(s.N-1)
            if ra != rb: pai[ra] = rb
        cl = defaultdict(list)
        for i in range(s.N): cl[acha(i)].append(i)
        return [tuple(v) for v in cl.values()]

    def mover(s, g, pil, u, P, modo, acima):
        """MOVIMENTO GERAL: refletir na reta (u,P) um subconjunto S de folhas
        tal que (i) so charneiras sobre a reta separam S do complementar,
        (ii) em cada ladrilho S e um bloco contiguo do topo ou do fundo, e
        (iii) o resultado e um estado dobrado valido.  A dobra ao meio e o
        caso S = tudo o que esta de um lado; a abertura e o caso em que S
        atravessa para o lado vazio; as dobras PARCIAIS (a flexao de pinca)
        sao os casos intermedios."""
        P6 = (6*P[0], 6*P[1])
        corta = [lado_reta(apply6(g[i], s.meio6[h]), u, P6) == 0
                 for h, (i, j) in enumerate(s.hinges)]
        comps = s._arcos(corta)
        if len(comps) < 2 or len(comps) > 12: return []
        R = H.refl(P, u); d = dict(pil); cs_ord = sorted(d); res = []
        for msk in range(1, (1 << len(comps)) - 1):
            S = set()
            for t in range(len(comps)):
                if msk >> t & 1: S |= set(comps[t])
            bom = True
            for c in cs_ord:
                cur = d[c]; k = [x in S for x in cur]; n = sum(k)
                alvo = ([False]*(len(cur)-n) + [True]*n if modo == 'topo'
                        else [True]*n + [False]*(len(cur)-n))
                if k != alvo: bom = False; break
            if not bom: continue
            ng = tuple(H.comp(R, g[i]) if i in S else g[i] for i in range(s.N))
            fica = {}; chega = {}
            for c in cs_ord:
                cur = d[c]
                mv = tuple(x for x in cur if x in S)
                st = tuple(x for x in cur if x not in S)
                if st: fica[c] = st
                if mv: chega[H.apply(R, c)] = tuple(reversed(mv))
            npil = {}
            for c in set(fica) | set(chega):
                a, b = fica.get(c, ()), chega.get(c, ())
                npil[c] = (a + b) if acima else (b + a)
            if len(npil) > s.maxtiles: continue
            e = normaliza(ng, tuple(sorted(npil.items())))
            if s.ok(e[0], dict(e[1])): res.append(e)
        return res

    def virar(s, est):
        """virar o flexagono ao contrario: reflexao global + pilhas invertidas."""
        g, pil = est
        ng = tuple(H.comp(H.REF, gi) for gi in g)
        npil = tuple((H.apply(H.REF, c), tuple(reversed(cs))) for c, cs in pil)
        return normaliza(ng, npil)

    def vizinhos(s, est):
        g, pil = est; cents = [c for c, _ in pil]; out = [s.virar(est)]
        for (u, off), P in retas(cents).items():
            for modo in ('topo', 'fundo'):
                for acima in (True, False):
                    out += s.mover(g, pil, u, P, modo, acima)
        out += pinca(s, est)                 # a dobra simultanea por tres raios
        return out


def estados_geom(N, cola='oposto'):
    """(g, pilhas) com as pilhas indexadas pelo CENTROIDE (x3)."""
    out = []
    cent = H.tira(N)[1]
    for g, tile, o, v in estados(N, cola):
        p = [H.apply(g[i], cent[i]) for i in range(N)]
        pil = {}
        for t, cells in o: pil[p[cells[0]]] = cells
        out.append((normaliza(g, tuple(sorted(pil.items()))), v))
    return out


def hexagonal(pil):
    """o footprint e um hexagono de 6 triangulos em torno de um vertice?"""
    cents = [c for c, _ in pil]
    if len(cents) != 6: return None
    tot = (sum(c[0] for c in cents), sum(c[1] for c in cents))
    if tot[0] % 18 or tot[1] % 18: return None
    v = (tot[0]//18, tot[1]//18)
    alvo = sorted(wadd((3*v[0], 3*v[1]), r) for r in H.REF_TILES)
    return v if sorted(cents) == alvo else None


# ============================================ a FLEXAO DE PINCA (dobra simultanea)
def _radial(v, a):
    """reflexao na reta pelo centro v e pelo vertice comum aos tiles a e a+1."""
    return H.refl(v, (a + 1) % 3)


def pinca(X, est):
    """A flexao de pinca: dobra SIMULTANEA por tres raios alternados --- o que
    um modelo de uma reta de cada vez nao consegue fazer --- seguida da
    abertura simultanea pelos outros tres.  Todas as retas passam pelo centro,
    logo o Teorema das retas de dobra continua a valer."""
    g, pil = est
    v = hexagonal(pil)
    if v is None: return []
    d = dict(pil)
    tile = {H.indice_tile(c, v): c for c in d}
    if len(tile) != 6: return []
    res = []
    for t in (0, 1):
        pares = [((2*k + t) % 6, (2*k + 1 + t) % 6) for k in range(3)]
        for movs in ((0, 0, 0), (1, 1, 1)):     # a pinca dobra as tres no mesmo sentido
            for acimas in product((True, False), repeat=3):   # montanha/vale por par
                ng = list(g); dest = {}; destinos = {}
                for (a, b), m, acima in zip(pares, movs, acimas):
                    src, dst = (a, b) if m == 0 else (b, a)
                    R = _radial(v, a)                     # raio entre a e b
                    for i in d[tile[src]]: ng[i] = H.comp(R, g[i])
                    base = d[tile[dst]]; mv = tuple(reversed(d[tile[src]]))
                    dest[tile[dst]] = base + mv if acima else mv + base
                    destinos[dst] = src
                gH = tuple(ng)
                if len(dest) != 3 or not X.ok(gH, dest): continue
                res += _abre_pinca(X, gH, dest, v, destinos)
    return res


def _abre_pinca(X, gH, pilH, v, destinos):
    """abertura simultanea: cada ladrilho ocupado manda um bloco contiguo de
       camadas pelo seu raio LIVRE (o que nao foi usado na dobra)."""
    ocup = {H.indice_tile(c, v): c for c in pilH}
    escolhas = []
    for k in sorted(ocup):
        cs = pilH[ocup[k]]
        src = destinos[k]
        idx = (k - 1) % 6 if src == (k + 1) % 6 else k     # raio livre
        escolhas.append([(k, idx, n, modo) for n in range(1, len(cs))
                         for modo in ('topo', 'fundo')])
    res = []
    V6 = (6*v[0], 6*v[1])
    for esc in product(*escolhas):
        ng = list(gH); fica = {}; chega = {}; bom = True
        S = set()
        for (k, idx, n, modo) in esc:
            cs = pilH[ocup[k]]
            S |= set(cs[len(cs)-n:] if modo == 'topo' else cs[:n])
        # so charneiras que assentem num raio podem ser cortadas
        for h, (i, j) in enumerate(X.hinges):
            if (i in S) != (j in S):
                q = apply6(gH[i], X.meio6[h])
                if all(lado_reta(q, u_, V6) != 0 for u_ in range(3)): bom = False; break
        if X.cola and ((0 in S) != (X.N - 1 in S)): bom = False
        if not bom: continue
        for (k, idx, n, modo) in esc:
            c = ocup[k]; cs = pilH[c]
            mv, st = ((cs[len(cs)-n:], cs[:len(cs)-n]) if modo == 'topo'
                      else (cs[:n], cs[n:]))
            R = _radial(v, idx)
            for i in mv: ng[i] = H.comp(R, gH[i])
            if st: fica[c] = st
            c2 = H.apply(R, c)
            if c2 in chega: bom = False; break
            chega[c2] = tuple(reversed(mv))
        if not bom: continue
        novo = {}
        for c in set(fica) | set(chega):
            novo[c] = fica.get(c, ()) + chega.get(c, ())
        if len(novo) != 6: continue
        e = normaliza(tuple(ng), tuple(sorted(novo.items())))
        if hexagonal(e[1]) and X.ok(e[0], dict(e[1])): res.append(e)
    return res
