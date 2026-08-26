"""
rotflex.py
==========
TEOREMA DAS RETAS DE DOBRA (ver artigo).  As unicas retas ao longo das quais um
hexagono de 6 triangulos equilateros se pode dobrar sao as suas 3 diagonais
longas --- e TODAS passam pelo centro O.  Logo, para dois estados de um
hexaflexagono que exibam a mesma face, cada A_j pertence ao grupo diedral que
fixa O; sendo directo, e uma ROTACAO EM TORNO DE O.  Em coordenadas do tile:

        A_j = rotacao de w^{e}  <=>  sigma(j) = j + eps_j   (mod 6).

Este ficheiro filtra o censo combinatorio de hexaflex_an.py por essa condicao.
"""
import sys
from collections import defaultdict
import hexaflex_an as A, zclass as Z, flexgeral as FG

FACE6 = FG.face_hexagonal()


def e_rotacao(sig, eps):
    return all(sig[j] == (j + eps[j]) % 6 for j in range(6))


def analisa(N, nome):
    est, aps = A.aparencias(N)
    porface = defaultdict(list)
    for idx, S, arr in aps: porface[S].append((idx, arr))
    mult = {S: v for S, v in porface.items() if len(v) > 1}
    flexes = set()
    for S, lst in mult.items():
        for a in range(len(lst)):
            for b in range(len(lst)):
                if a != b:
                    m = A.retorno(lst[a][1], lst[b][1])
                    if m != (tuple(range(6)), (0,)*6): flexes.add(m)
    rot = {m for m in flexes if e_rotacao(*m)}
    print("=" * 74); print(f" {nome}"); print("=" * 74)
    print(f"  dobraduras planas: {len(est)};  aparencias: {len(aps)}")
    print(f"  mapas de retorno combinatorios      : {len(flexes)}")
    print(f"  ... que sao rotacoes em torno de O  : {len(rot)}   <-- os unicos possiveis")
    cnt = defaultdict(int)
    for m in flexes:
        st = A.gamma([m]); cnt[(st['rank'], st['P'])] += 1
    print(f"  classes dos combinatorios: {dict(sorted(cnt.items()))}")
    cnt = defaultdict(int)
    for m in rot:
        st = A.gamma([m]); cnt[(st['rank'], st['P'])] += 1
    print(f"  classes das rotacoes     : {dict(sorted(cnt.items()))}")
    st = A.gamma(rot) if rot else dict(rank=0, P=1, lattice=[])
    nm, sol = Z.CLASSES.get((st['rank'], st['P']), ('?', '?'))
    print(f"\n  GRUPO Gamma (teorema das retas de dobra): posto={st['rank']}"
          f"  |P|={st['P']}  -> {nm}")
    print(f"     SOLUCOES: {sol}")
    return st


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    nomes = {10: "TRI-HEXAFLEXAGONO (3 faces)", 19: "HEXA-HEXAFLEXAGONO (6 faces)"}
    analisa(N, nomes.get(N, f"tira de {N}"))
