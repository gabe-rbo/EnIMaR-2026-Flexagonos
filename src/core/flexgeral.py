"""
flexgeral.py
============
TEORIA GERAL dos flexes de uma face poligonal ladrilhada por polignos
congruentes.  Cobre de uma so vez tetraflexagonos (face = quadrado 2x2 de
quadradinhos, n = 4) e hexaflexagonos (face = hexagono de 6 triangulos,
n = 6), e qualquer outro caso futuro: basta descrever a face.

Um FLEX de uma face com tiles T_1,...,T_m e uma bijecao que e isometria direta
em cada tile aberto e permuta os tiles:

    Phi|_{T_j} = A_j(z) = eps_j (z - c_j) + c_{sigma(j)},

onde eps_j percorre as rotacoes que levam a FORMA de T_j na de T_{sigma(j)}:
um coset do grupo de rotacoes do tile.  O grupo dos flexes tem ordem
m! * |Rot(tile)|^m.

Pela restricao cristalografica o grupo de rotacoes da tesselacao e C_n com
n em {1,2,3,4,6}; os centros dos tiles estao em (1/d) Z[zeta_n].  Logo

    Gamma_Phi = < A_k^{-1} A_j >  esta contido em  C_n |x (1/d) Z[zeta_n],

que e discreto.  Consequencias (ver artigo):
  * a classificacao por (posto do reticulado, ordem do grupo de pontos) e a
    mesma para todos os flexagonos;
  * se o posto e 2 e |P| >= 3, entao Lambda e um ideal de Z[zeta_n] e a curva
    C/Lambda tem multiplicacao complexa:  j = 1728 (n=4) ou j = 0 (n=3,6).
"""
from itertools import permutations, product
from collections import Counter, defaultdict
import zclass as Z


class Face:
    """d, centroides (inteiros, sobre o denominador d) e rotacoes admissiveis."""

    def __init__(self, n, d, centros, rot_permitidas):
        self.A = Z.Anel(n); self.n = n; self.d = d
        self.c = list(centros)                 # lista de (p,q) sobre d
        self.m = len(self.c)
        self.rot = rot_permitidas              # (j,k) -> lista de expoentes de zeta

    def A_j(self, j, k, e):
        """A_j = zeta^e (z - c_j) + c_k ; devolve (e, beta) com beta sobre d."""
        zc = self.A.zpow(e, self.c[j])
        return (e % self.n, (self.c[k][0] - zc[0], self.c[k][1] - zc[1]))

    def flexes(self, reduzido=False):
        """reduzido=True: fixa sigma(0)=0.  Pos-compor com a rotacao global
        rho_u (que leva o tile k no tile k+u) preserva Gamma (Lema) e permite
        essa normalizacao; a acao e livre, logo cada classe tem exatamente
        m/|orbita| = n_rot representantes e os contadores multiplicam-se por
        esse fator."""
        for sg in permutations(range(self.m)):
            if reduzido and sg[0] != 0: continue
            opcoes = [self.rot[(j, sg[j])] for j in range(self.m)]
            for eps in product(*opcoes):
                yield sg, eps

    def gamma_gens(self, sg, eps):
        As = [self.A_j(j, sg[j], eps[j]) for j in range(self.m)]
        out = set()
        for j in range(self.m):
            for k in range(self.m):
                g = Z.comp(self.A, Z.inv(self.A, As[k]), As[j])
                if g != Z.ident(): out.add(g)
        return sorted(out)

    def estrutura(self, sg, eps):
        return Z.estrutura(self.A, self.gamma_gens(sg, eps))


# --------------------------------------------------------------- faces padrao
def face_quadrada():
    """quadrado 2x2 de quadradinhos; centros (+-1 +- i)/2 ; n = 4, d = 2.
       ordem cartesiana Q1..Q4."""
    c = [(1, 1), (-1, 1), (-1, -1), (1, -1)]      # sobre d = 2, base {1, i}
    rot = {(j, k): [0, 1, 2, 3] for j in range(4) for k in range(4)}
    return Face(4, 2, c, rot)


def face_hexagonal():
    """hexagono de 6 triangulos equilateros; tile k = {0, w^k, w^{k+1}},
       centro (w^k + w^{k+1})/3 ; n = 6, d = 3.
       A rotacao que leva o tile j no tile k e w^{k-j}; o tile tem grupo de
       rotacoes C_3, logo eps_j em w^{k-j} * {1, w^2, w^4}."""
    A = Z.Anel(6)
    c = []
    for k in range(6):
        a = A.zpow(k, (1, 0)); b = A.zpow(k + 1, (1, 0))
        c.append((a[0] + b[0], a[1] + b[1]))       # sobre d = 3
    rot = {(j, k): [(k - j) % 6, (k - j + 2) % 6, (k - j + 4) % 6]
           for j in range(6) for k in range(6)}
    return Face(6, 3, c, rot)


# --------------------------------------------------------------- censo
def censo(face, nome, reduzido=False, fator=1):
    cnt = Counter(); ex = {}; lats = defaultdict(Counter)
    tot = 0
    for sg, eps in face.flexes(reduzido=reduzido):
        st = face.estrutura(sg, eps)
        tot += 1
        if tot % 20000 == 0: print(f"   ... {tot} flexes", flush=True)
        ch = (st["rank"], st["P"])
        cnt[ch] += 1
        ex.setdefault(ch, (sg, eps, st))
        if st["rank"] == 2:
            B = st["lattice"]
            cov = abs(B[0][0]*B[1][1] - B[0][1]*B[1][0])
            lats[st["P"]][cov] += 1
    tot *= fator
    for k in list(cnt): cnt[k] *= fator
    for P in lats:
        for k in list(lats[P]): lats[P][k] *= fator
    print("=" * 78)
    print(f" CENSO: {nome}   (|F| = {tot} = {face.m}! * "
          f"{len(face.rot[(0,0)])}^{face.m})")
    print("=" * 78)
    print(f"{'posto':>5} {'|P|':>4} {'#flexes':>9} {'%':>7}   tipo / solucoes")
    for ch in sorted(cnt):
        nomecl, sol = Z.CLASSES.get(ch, ("?", "?"))
        print(f"{ch[0]:>5} {ch[1]:>4} {cnt[ch]:>9} {100*cnt[ch]/tot:6.2f}%   "
              f"{nomecl:<10s} {sol}")
    inteiras = sum(v for k, v in cnt.items() if k[0] < 2)
    print(f"\n  admitem solucao INTEIRA nao constante (posto <= 1): {inteiras}"
          f"  ({100*inteiras/tot:.2f}%)")
    print(f"  forcam polos (posto 2):                            {tot-inteiras}"
          f"  ({100*(tot-inteiras)/tot:.2f}%)")
    print("\n  covolumes do reticulado (em unidades de 1/d^2), por |P|:")
    for P in sorted(lats):
        print(f"     |P|={P}: {dict(sorted(lats[P].items()))}")
    return cnt, ex


if __name__ == "__main__":
    censo(face_quadrada(), "tetraflexagonos -- face = quadrado 2x2")
    print(flush=True)
    censo(face_hexagonal(), "hexaflexagonos -- face = hexagono de 6 triangulos",
          reduzido=True, fator=6)
