"""censo_hex.py -- censo do grupo de flexes hexagonal, por blocos com
checkpoint (o workspace nao mantem processos entre chamadas)."""
import json, os, sys
from itertools import permutations, product
from collections import Counter, defaultdict
import flexgeral as FG, zclass as Z

FACE = FG.face_hexagonal()
PERMS = [p for p in permutations(range(6)) if p[0] == 0]     # 120
ARQ = "../saidas/censo_hex.json"


def carrega():
    if os.path.exists(ARQ):
        d = json.load(open(ARQ))
        return d["feitos"], Counter({tuple(map(int, k.split(","))): v
                                     for k, v in d["cnt"].items()}), \
               {int(P): Counter({int(k): v for k, v in c.items()})
                for P, c in d["lats"].items()}
    return 0, Counter(), defaultdict(Counter)


def salva(feitos, cnt, lats):
    json.dump({"feitos": feitos,
               "cnt": {",".join(map(str, k)): v for k, v in cnt.items()},
               "lats": {str(P): {str(k): v for k, v in c.items()}
                        for P, c in lats.items()}}, open(ARQ, "w"))


if __name__ == "__main__":
    bloco = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    feitos, cnt, lats = carrega()
    lats = defaultdict(Counter, lats)
    fim = min(feitos + bloco, len(PERMS))
    for idx in range(feitos, fim):
        sg = PERMS[idx]
        for eps in product(*[FACE.rot[(j, sg[j])] for j in range(6)]):
            st = FACE.estrutura(sg, eps)
            cnt[(st["rank"], st["P"])] += 1
            if st["rank"] == 2:
                B = st["lattice"]
                lats[st["P"]][abs(B[0][0]*B[1][1] - B[0][1]*B[1][0])] += 1
    salva(fim, cnt, lats)
    print(f"permutacoes {feitos}..{fim-1} de {len(PERMS)}  "
          f"({sum(cnt.values())} flexes reduzidos)")
    if fim == len(PERMS):
        F = 6                                  # fator da reducao sigma(0)=0
        tot = sum(cnt.values())*F
        print("=" * 78)
        print(f" CENSO: hexaflexagonos -- face = hexagono de 6 triangulos")
        print(f" |F| = 6! * 3^6 = {tot}")
        print("=" * 78)
        print(f"{'posto':>5} {'|P|':>4} {'#flexes':>9} {'%':>7}   tipo / solucoes")
        for ch in sorted(cnt):
            nm, sol = Z.CLASSES.get(ch, ("?", "?"))
            print(f"{ch[0]:>5} {ch[1]:>4} {cnt[ch]*F:>9} "
                  f"{100*cnt[ch]/sum(cnt.values()):6.2f}%   {nm:<6s} {sol}")
        it = sum(v for k, v in cnt.items() if k[0] < 2)*F
        print(f"\n  admitem solucao INTEIRA nao constante: {it} "
              f"({100*it/tot:.2f}%)")
        print(f"  forcam polos (posto 2): {tot-it} ({100*(tot-it)/tot:.2f}%)")
        print("\n  covolumes (unidades de 1/9), por |P|:")
        for P in sorted(lats):
            print(f"     |P|={P}: "
                  + str({k: v*F for k, v in sorted(lats[P].items())}))
