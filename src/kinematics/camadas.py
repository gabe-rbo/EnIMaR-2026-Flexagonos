"""
camadas.py
==========
Realizabilidade fisica de uma dobradura plana: existe ordenacao de camadas sem
auto-interseccao do papel?

Como nenhuma celula atravessa uma dobra (cada celula cai inteira numa posicao),
as condicoes de Justin reduzem-se a tres:

  * um *taco* sobre a aresta e da posicao P: par de celulas vizinhas no plano,
    dobradas na aresta comum, que caem ambas em P;
  * uma *tortilha* sobre e: celula de P ligada SEM dobra a uma celula da
    posicao vizinha atraves de e.

  (T1) taco-taco     : dois tacos sobre a mesma aresta da mesma posicao tem
                       intervalos de camadas encaixados ou disjuntos.
  (T2) taco-tortilha : a camada de uma tortilha sobre e nao fica estritamente
                       dentro do intervalo de um taco sobre e.
  (T3) folha-folha   : duas ligacoes planas pela mesma aresta preservam a ordem
                       relativa das camadas dos dois lados.

A dobradura e realizavel sse existe ordem total das camadas em cada posicao
satisfazendo (T1)-(T3).  A busca e exaustiva.
"""
from itertools import permutations, product
from collections import defaultdict
import foldings as F


def _lado(gi, A, B, pos_i):
    (r1, c1), (r2, c2) = A, B
    if r1 == r2: m = (2*max(c1, c2), -(2*r1 + 1))
    else:        m = (2*c1 + 1, -2*max(r1, r2))
    q = F.apply(gi, m)
    dx, dy = q[0] - pos_i[0], q[1] - pos_i[1]
    return ('L' if dx < 0 else 'R') if dx else ('B' if dy < 0 else 'T')


_OP = {'L': 'R', 'R': 'L', 'T': 'B', 'B': 'T'}


def estrutura(cells, hinges, g, pos):
    tacos, tort = defaultdict(list), defaultdict(list)
    for i, j in hinges:
        A, B = cells[i], cells[j]
        lado = _lado(g[i], A, B, pos[i])
        if pos[i] == pos[j]:
            tacos[(pos[i], lado)].append((i, j))
        else:
            tort[(pos[i], lado)].append((i, j))
            tort[(pos[j], _OP[lado])].append((j, i))
    return tacos, tort


def realizavel(cells, hinges, g, pos, devolver=False):
    porpos = defaultdict(list)
    for i in range(len(cells)): porpos[pos[i]].append(i)
    posicoes = sorted(porpos)
    tacos, tort = estrutura(cells, hinges, g, pos)
    for escolha in product(*[list(permutations(porpos[p])) for p in posicoes]):
        niv = {}
        for p, ordem in zip(posicoes, escolha):
            for k, c in enumerate(ordem): niv[c] = k
        ok = True
        for ch, pares in tacos.items():                       # (T1)
            iv = [tuple(sorted((niv[u], niv[v]))) for u, v in pares]
            for a in range(len(iv)):
                for b in range(a+1, len(iv)):
                    (l1, h1), (l2, h2) = iv[a], iv[b]
                    if (l1 < l2 < h1 < h2) or (l2 < l1 < h2 < h1): ok = False
                    if not ok: break
                if not ok: break
            if not ok: break
        if ok:
            for ch, pares in tacos.items():                   # (T2)
                for u, v in pares:
                    lo, hi = sorted((niv[u], niv[v]))
                    for w, _ in tort.get(ch, []):
                        if lo < niv[w] < hi: ok = False; break
                    if not ok: break
                if not ok: break
        if ok:
            for ch, pares in tort.items():                    # (T3)
                for a in range(len(pares)):
                    for b in range(a+1, len(pares)):
                        u, u2 = pares[a]; v, v2 = pares[b]
                        if (niv[u] < niv[v]) != (niv[u2] < niv[v2]): ok = False; break
                    if not ok: break
                if not ok: break
        if ok: return (True, escolha) if devolver else True
    return (False, None) if devolver else False


def filtra_hexa():
    n = len(F.RING)
    hinges = [(i, (i+1) % n) for i in range(n)]
    todas = F.enumerar()
    viav = [t for t in todas
            if realizavel(F.RING, hinges, {i: t[1][i] for i in range(n)},
                          {i: t[2][i] for i in range(n)})]
    return todas, viav


def filtra_tri():
    import foldings_tri as T
    cells = T.CELL
    idx = {c: i for i, c in enumerate(cells)}
    hinges = [(idx[a], idx[b]) for a, b in T.HINGES]
    todas = T.enumerar()
    viav = []
    for g, pos, xs, ys in todas:
        gd = {idx[c]: g[c] for c in cells}
        pd = {idx[c]: pos[c] for c in cells}
        cl = [T.POS[c] for c in cells]
        if realizavel(cl, hinges, gd, pd): viav.append((g, pos, xs, ys))
    return todas, viav


if __name__ == "__main__":
    from quadflex import Flex, gamma_structure, label, latstr
    NOME = {0: '1', 1: 'i', 2: '-1', 3: '-i'}

    class G:
        def __init__(s, x): s._g = sorted(set(x))
        def gamma_gens(s): return s._g

    print("=" * 74)
    print(" HEXA-TETRAFLEXAGONO -- filtro de realizabilidade das camadas")
    print("=" * 74)
    todas, viav = filtra_hexa()
    print(f"  dobraduras planas combinatorias : {len(todas)}")
    print(f"  com ordenacao de camadas valida : {len(viav)}")
    at, av = F.estados_por_face(todas), F.estados_por_face(viav)
    print("\n  arranjos exibiveis por face (combinatorios -> realizaveis):")
    for k in sorted(at):
        print(f"     face {k}: {len(at[k])} -> {len(av.get(k, []))}")
    gens = []; todos_eps = set()
    print("\n  mapas de retorno das dobraduras realizaveis:")
    for k in sorted(av):
        arrs = av[k]
        maps = {F.mapa_retorno(arrs[i], arrs[j])
                for i in range(len(arrs)) for j in range(len(arrs)) if i != j}
        print(f"     face {k}: {len(arrs)} arranjos, {len(maps)} mapas")
        for sg, ep in sorted(maps):
            todos_eps.add(ep)
            Phi = Flex(sg, ep); gens += Phi.gamma_gens()
            st = gamma_structure(Phi)
            print(f"        sigma={sg} eps=({','.join(NOME[e] for e in ep)})"
                  f"  posto={st['rank']} Lambda={latstr(st['lattice'])}")
    st = gamma_structure(G(gens))
    print(f"\n  GRUPO CONJUNTO: {label(st)}")
    print(f"     Lambda = {latstr(st['lattice'])}   |P| = {st['P']}")
    print(f"  todos os eps triviais? {todos_eps == {(0,0,0,0)}}")

    print("\n" + "=" * 74)
    print(" TRI-TETRAFLEXAGONO -- mesmo filtro")
    print("=" * 74)
    import foldings_tri as T
    tt, tv = filtra_tri()
    print(f"  dobraduras planas combinatorias : {len(tt)}")
    print(f"  com ordenacao de camadas valida : {len(tv)}")
    at, av = T.arranjos_por_face(tt), T.arranjos_por_face(tv)
    for k in sorted(at):
        print(f"     face {k}: {len(at[k])} -> {len(av.get(k, []))}")
    gens = []
    for k in sorted(av):
        arrs = av[k]
        for i in range(len(arrs)):
            for j in range(len(arrs)):
                if i != j:
                    sg, ep = T.mapa_retorno(arrs[i], arrs[j])
                    gens += Flex(sg, ep).gamma_gens()
    st = gamma_structure(G(gens))
    print(f"\n  GRUPO CONJUNTO: {label(st)}")
    print(f"     Lambda = {latstr(st['lattice'])}   |P| = {st['P']}")
