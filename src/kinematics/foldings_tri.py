"""
foldings_tri.py
===============
Enumeracao exata das dobraduras planas do TRI-TETRAFLEXAGONO.

O plano e o octomino extraido da Figura A.1 de [manual] (ver plano_tri.py),
com a numeracao do gerador de planos do Projeto Visitas:

   celulas (linha, coluna) numa grade 2x5:
        a=(0,0)  b=(0,1)  c=(0,2)  d=(0,3)  e=(0,4)
                          f=(1,2)  g=(1,3)  h=(1,4)

   lados:   a: E2 / branco        e: branco / F1
            b: E1 / V1            f: F3 / E4
            c: F2 / V2            g: V3 / E3
            d: branco / branco    h: V4 / F4

   RASGO: das 9 adjacencias da grade, duas --- c|d e d|g --- sao CORTES (o
   rasgo do tri-tetraflexagono classico).  O que sobra e uma TIRA de 8 celulas

        a - b - c - f - g - h - e - d ,

   com a celula branca d pendurada na ponta.  A tira e a colagem foram
   determinadas por necessidade fisica em busca_tri.py: das tres tiras
   hamiltonianas possiveis e de todas as colagens branco-com-branco, so a tira
   acima exibe as TRES faces com o topo das quatro pilhas, e reproduz o
   diagrama do EnIMaR (F com 2 arranjos, V e E com 1).

   colagem: o verso branco de a e colado ao verso branco de d -- sao as duas
   PONTAS da tira.  (As outras duas colagens compativeis, a-e e d-e, dao
   exactamente os mesmos arranjos e o mesmo grupo.)
"""
from itertools import product
from collections import defaultdict
from foldings import (comp, apply, ID, REF, ref_vert, ref_horiz, zadd, zmul, IP)

CELL = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
POS = {'a': (0, 0), 'b': (0, 1), 'c': (0, 2), 'd': (0, 3), 'e': (0, 4),
       'f': (1, 2), 'g': (1, 3), 'h': (1, 4)}
TIRA = ['a', 'b', 'c', 'f', 'g', 'h', 'e', 'd']
HINGES = [(TIRA[i], TIRA[i + 1]) for i in range(7)]
CORTES = [('c', 'd'), ('d', 'g')]              # o rasgo

# lado -> (face, quadrante);  None = quadradinho branco
FRENTE = {'a': ('E', 2), 'b': ('E', 1), 'c': ('F', 2), 'd': None,
          'e': None,     'f': ('F', 3), 'g': ('V', 3), 'h': ('V', 4)}
VERSO = {'a': None,      'b': ('V', 1), 'c': ('V', 2), 'd': None,
         'e': ('F', 1),  'f': ('E', 4), 'g': ('E', 3), 'h': ('F', 4)}
COLA = ('a', 'd', 'vv')   # verso de a colado ao verso de d


def centro(cel):
    r, c = POS[cel]; return (2*c + 1, -(2*r + 1))


def ref_aresta(A, B):
    (r1, c1), (r2, c2) = POS[A], POS[B]
    if r1 == r2: return ref_vert(2*max(c1, c2))
    return ref_horiz(-2*max(r1, r2))


def enumerar():
    refs = {h: ref_aresta(*h) for h in HINGES}
    arv = list(HINGES)          # a tira ja e uma arvore geradora
    extras = []
    saida = []
    for g0 in (ID, REF):
        for bits in product((0, 1), repeat=len(arv)):
            g = {'a': g0}
            for (A, B), t in zip(arv, bits):
                g[B] = comp(g[A], refs[(A, B)]) if t else g[A]
            ok = True
            for (A, B) in extras:                      # coerencia dos ciclos
                if g[B] != g[A] and g[B] != comp(g[A], refs[(A, B)]):
                    ok = False; break
            if not ok: continue
            pos = {c: apply(g[c], centro(c)) for c in CELL}
            # restricao de colagem (verso de A com verso de B: caras opostas)
            A, B, t = COLA
            if pos[A] != pos[B]: continue
            dA = (g[A][1] == 0) if t[0] == 'v' else (g[A][1] == 1)
            dB = (g[B][1] == 0) if t[1] == 'v' else (g[B][1] == 1)
            if dA == dB: continue
            d = defaultdict(list)
            for c in CELL: d[pos[c]].append(c)
            if len(d) != 4: continue
            xs = sorted({p[0] for p in d}); ys = sorted({p[1] for p in d})
            if len(xs) != 2 or len(ys) != 2: continue
            if xs[1]-xs[0] != 2 or ys[1]-ys[0] != 2: continue
            saida.append((g, pos, xs, ys))
    return saida


def quadrante(p, xs, ys):
    dir_ = p[0] == xs[1]; cima = p[1] == ys[1]
    return 1 if (dir_ and cima) else 2 if (not dir_ and cima) else 3 if not dir_ else 4


def arranjos_por_face(folds):
    out = defaultdict(set)
    for g, pos, xs, ys in folds:
        vis = defaultdict(dict)
        for c in CELL:
            a, s, _ = g[c]
            lado = (FRENTE if s == 0 else VERSO)[c]
            if lado is None: continue
            face, quad = lado
            vis[face][quad] = (quadrante(pos[c], xs, ys), a)
        for face, arr in vis.items():
            if len(arr) == 4 and len({v[0] for v in arr.values()}) == 4:
                out[face].add(tuple(arr[j] for j in (1, 2, 3, 4)))
    return {k: sorted(v) for k, v in out.items()}


def mapa_retorno(arrS, arrSl):
    sigma = {}; eps = {}
    for j in range(4):
        qS, aS = arrS[j]; qL, aL = arrSl[j]
        sigma[qS] = qL; eps[qS] = (aL - aS) % 4
    return tuple(sigma[q] for q in (1, 2, 3, 4)), tuple(eps[q] for q in (1, 2, 3, 4))


if __name__ == "__main__":
    from quadflex import Flex, gamma_structure, label, latstr, covol
    folds = enumerar()
    print(f"dobraduras planas do octomino (com a colagem) sobre o quadrado 2x2:"
          f" {len(folds)}")
    arr = arranjos_por_face(folds)
    NOME = {0: '1', 1: 'i', 2: '-1', 3: '-i'}
    gens = []
    for k in sorted(arr):
        print(f"\nface {k}: {len(arr[k])} arranjo(s) exibivel(is)")
        maps = set()
        for i in range(len(arr[k])):
            for j in range(len(arr[k])):
                if i != j: maps.add(mapa_retorno(arr[k][i], arr[k][j]))
        for sg, ep in sorted(maps):
            Phi = Flex(sg, ep); st = gamma_structure(Phi); gens += Phi.gamma_gens()
            print(f"   retorno sigma={sg} eps=({','.join(NOME[e] for e in ep)})  "
                  f"posto={st['rank']} |P|={st['P']} Lambda={latstr(st['lattice'])}")
        if not maps: print("   (nenhum mapa de retorno nao trivial)")

    class G:
        def __init__(s, g): s._g = sorted(set(g))
        def gamma_gens(s): return s._g
    st = gamma_structure(G(gens))
    print("\nGRUPO CONJUNTO do tri-tetraflexagono:")
    print(f"   {label(st)}")
    if st["rank"]:
        print(f"   Lambda = {latstr(st['lattice'])}"
              + (f"  covol={covol(st['lattice'])}" if st['rank'] == 2 else "")
              + f"   |P| = {st['P']}")
