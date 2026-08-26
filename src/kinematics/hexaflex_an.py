"""
hexaflex_an.py
==============
Analise de um hexaflexagono de tira reta com N triangulos (o ultimo colado no
primeiro).  As FACES nao sao postuladas: uma face e um conjunto de 6 lados de
celula que ocupa os 6 tiles do hexagono; os estados que exibem o MESMO conjunto
dao os mapas de retorno.  Dai sai Gamma e o corpo das solucoes.
"""
import sys
from collections import defaultdict
from itertools import product
import hexaflex as H
import zclass as Z
import flexgeral as FG

A6 = Z.Anel(6)
FACE6 = FG.face_hexagonal()


def aparencias(N):
    """(estado) -> lista de aparencias; aparencia = (frozenset de lados,
       dict lado -> (tile, rot))."""
    est = H.enumerar(N)
    saida = []
    for idx, (bits, g, pos, v) in enumerate(est):
        pt = defaultdict(list)
        for i in range(N):
            cel = 0 if i == N-1 else i
            pt[H.indice_tile(pos[i], v)].append(((cel, g[i][1]), g[i][0]))
        if len(pt) != 6: continue
        for esc in product(*[pt[t] for t in range(6)]):
            lados = [l for l, a in esc]
            if len(set(lados)) != 6: continue
            arr = {l: (t, a) for t, (l, a) in enumerate(esc)}
            saida.append((idx, frozenset(lados), arr))
    return est, saida


def retorno(arrA, arrB):
    sig, eps = {}, {}
    for l, (tA, aA) in arrA.items():
        tB, aB = arrB[l]
        sig[tA] = tB; eps[tA] = (aB - aA) % 6
    return tuple(sig[t] for t in range(6)), tuple(eps[t] for t in range(6))


def gamma(gens_flex):
    gens = set()
    for sig, eps in gens_flex:
        As = [FACE6.A_j(j, sig[j], eps[j]) for j in range(6)]
        for j in range(6):
            for k in range(6):
                g = Z.comp(A6, Z.inv(A6, As[k]), As[j])
                if g != Z.ident(): gens.add(g)
    return Z.estrutura(A6, sorted(gens))


def analisa(N, nome):
    est, aps = aparencias(N)
    print("=" * 74)
    print(f" {nome}: tira de {N} triangulos, colagem 1<->{N}")
    print("=" * 74)
    print(f"  dobraduras planas sobre um hexagono : {len(est)}")
    print(f"  aparencias (escolha de 1 folha por tile) : {len(aps)}")
    porface = defaultdict(list)
    for idx, S, arr in aps: porface[S].append((idx, arr))
    mult = {S: v for S, v in porface.items() if len(v) > 1}
    print(f"  conjuntos de 6 lados exibiveis        : {len(porface)}")
    print(f"  ... exibiveis em MAIS DE UMA aparencia: {len(mult)}")

    flexes = set()
    for S, lst in mult.items():
        for a in range(len(lst)):
            for b in range(len(lst)):
                if a == b: continue
                sig, eps = retorno(lst[a][1], lst[b][1])
                if (sig, eps) != (tuple(range(6)), (0,)*6):
                    flexes.add((sig, eps))
    print(f"  mapas de retorno nao triviais         : {len(flexes)}")
    if flexes:
        cnt = defaultdict(int)
        for sig, eps in flexes:
            st = Z.estrutura(A6, [Z.comp(A6, Z.inv(A6, FACE6.A_j(k, sig[k], eps[k])),
                                          FACE6.A_j(j, sig[j], eps[j]))
                                  for j in range(6) for k in range(6)
                                  if Z.comp(A6, Z.inv(A6, FACE6.A_j(k, sig[k], eps[k])),
                                            FACE6.A_j(j, sig[j], eps[j])) != Z.ident()])
            cnt[(st["rank"], st["P"])] += 1
        print(f"  classes dos mapas individuais: {dict(sorted(cnt.items()))}")
    st = gamma(flexes) if flexes else dict(rank=0, P=1, lattice=[])
    nomecl, sol = Z.CLASSES.get((st["rank"], st["P"]), ("?", "?"))
    print(f"\n  GRUPO CONJUNTO Gamma: posto={st['rank']} |P|={st['P']}"
          f"  -> {nomecl}")
    print(f"     reticulado (em unidades de 1/3) = {st['lattice']}")
    print(f"     SOLUCOES: {sol}")
    return st


if __name__ == "__main__":
    analisa(10, "TRI-HEXAFLEXAGONO (3 faces)")
    print()
    if len(sys.argv) > 1 and sys.argv[1] == "todos":
        analisa(19, "HEXA-HEXAFLEXAGONO (6 faces)")
