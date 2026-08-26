"""
paridade.py
===========
CARACTERIZACAO COMBINATORIA dos arranjos, sem geometria e sem busca.

Tres factos (demonstrados no artigo, verificados aqui):

 (P1) FORMULA DE PARIDADE.  Numa dobradura plana do anel sobre o quadrado
      2x2, a parte de rotacao de cada folha e
              a_L = 2 ( kappa_L + c_L )   (mod 4),
      onde kappa_L e a coluna que a folha ocupa na face (0 ou 1) e c_L e a
      coluna que ela ocupa no plano.  Analogamente para as linhas e o lado.

 (P2) FORMULA DOS INTERVALOS.  Logo, para duas pecas de uma mesma face,
              a_j - a_{j'} = 2 * #{charneiras VERTICAIS dobradas entre elas},
      contadas ao longo da tira.  O vetor de rotacoes de um arranjo le-se
      dos bits de dobra --- nenhuma isometria e precisa.

 (P3) UMA CHARNEIRA SOLTA POR BLOCO.  As 12 charneiras do anel dividem-se em
      quatro blocos de tres paralelas, (0,1,2), (3,4,5), (6,7,8), (9,10,11).
      Dobrar 4 celulas numa janela de 2 obriga a que EXACTAMENTE UMA charneira
      de cada bloco fique solta.  Uma dobradura e portanto um ponto
              u = (u1,u2,u3,u4) in {0,1,2}^4 ,
      e das 81 possibilidades ocorrem 25.

Daqui sai tudo: as posicoes, as rotacoes e o arranjo de cada face saem de u.
Um flex vertical troca (u1,u3) --- ou fixa ambos, ou muda ambos ---, e um
horizontal troca (u2,u4).
"""
from itertools import product
from collections import defaultdict
import foldings as F

RUNS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)]
UHIN = set(RUNS[0]) | set(RUNS[2])          # charneiras verticais
VHIN = set(RUNS[1]) | set(RUNS[3])
FACES = {}
for i, cel in enumerate(F.RING):
    for lado, tab in ((0, F.FRENTE), (1, F.VERSO)):
        fc, q = tab[cel]
        FACES.setdefault(fc, {})[q] = (i, lado)


def bits(u):
    """u -> vetor de 12 bits (1 = charneira dobrada)."""
    b = [1]*12
    for R, k in zip(RUNS, u): b[R[k]] = 0
    return b


def caminho(u):
    """passeio INTEIRO das colunas e das linhas ao longo do anel.
       Numa charneira solta a coluna anda +-1 e a orientacao fica; numa
       charneira dobrada a coluna fica e a orientacao inverte."""
    b = bits(u)
    kap = [0]*13; rho = [0]*13; tx = 0; ty = 0
    for h in range(12):
        i = h
        if h in UHIN:
            if b[h]: kap[i+1] = kap[i]; tx ^= 1
            else:    kap[i+1] = kap[i] + (1 if tx == 0 else -1)
            rho[i+1] = rho[i]
        else:
            if b[h]: rho[i+1] = rho[i]; ty ^= 1
            else:    rho[i+1] = rho[i] + (1 if ty == 0 else -1)
            kap[i+1] = kap[i]
    return kap, rho, tx, ty


def colunas(u):
    """kappa_L e rho_L (0/1) na face, a menos de troca global."""
    kap, rho, _, _ = caminho(u)
    k0 = min(kap[:12]); r0 = min(rho[:12])
    return [k - k0 for k in kap[:12]], [r - r0 for r in rho[:12]]


def posicoes(u, face):
    """(kappa, rho) de cada peca da face, so com os bits de dobra: kappa e a
    paridade do numero de charneiras VERTICAIS SOLTAS entre a peca 1 e a peca
    j ao longo da tira; rho a mesma coisa com as horizontais."""
    b = bits(u)
    ordem = [FACES[face][q][0] for q in (1, 2, 3, 4)]
    base = ordem[0]; out = []
    for i in ordem:
        k = r = 0; h = base
        while h != i:
            if h in UHIN and not b[h]: k ^= 1
            if h in VHIN and not b[h]: r ^= 1
            h = (h + 1) % 12
        out.append((k, r))
    return tuple(out)


def exibivel(u, face):
    """a face ocupa as quatro posicoes?"""
    return len(set(posicoes(u, face))) == 4


def assinatura(u, face):
    """FORMULA DOS INTERVALOS (P2): vetor de rotacoes da face, a menos de
    constante, calculado SO com os bits de dobra --- sem geometria nenhuma.
    A peca j roda 2 * #{charneiras verticais dobradas entre a peca 1 e a
    peca j, ao longo da tira} (mod 4)."""
    b = bits(u)
    ordem = [FACES[face][q][0] for q in (1, 2, 3, 4)]
    base = ordem[0]; out = []
    for i in ordem:
        n = 0; h = base
        while h != i:
            if h in UHIN and b[h]: n += 1
            h = (h + 1) % 12
        out.append((2*n) % 4)
    return tuple(out)


VALIDAS = None


def validas():
    """as coordenadas u que correspondem a dobraduras planas do anel sobre o
    quadrado 2x2.  Le-se da enumeracao exacta (70 dobraduras, instantanea);
    o ponto e que a partir daqui NADA mais depende de geometria."""
    global VALIDAS
    if VALIDAS is None:
        V = set()
        for bits_, g, pos in F.enumerar():
            b = [1 if pos[i] == pos[(i+1) % 12] else 0 for i in range(12)]
            u = []
            for R in RUNS:
                z = [h for h in R if b[h] == 0]
                if len(z) != 1: u = None; break
                u.append(R.index(z[0]))
            if u: V.add(tuple(u))
        VALIDAS = sorted(V)
    return VALIDAS


if __name__ == "__main__":
    V = validas()
    print("=" * 74)
    print(" CARACTERIZACAO COMBINATORIA: o arranjo de cada face le-se em u")
    print("=" * 74)
    print(f"  coordenadas u = (u1,u2,u3,u4) que dao uma dobradura: {len(V)} de 81")
    print()
    print("  face : assinaturas de rotacao que ocorrem (vetor a menos de constante)")
    for k in sorted(FACES):
        cl = defaultdict(list)
        for u in V: cl[assinatura(u, k)].append(u)
        print(f"    {k}: " + "   ".join(f"{c} em {len(v)} coords" for c, v in sorted(cl.items())))
    print()
    print()
    print("  a assinatura de cada face em funcao de (u1,u3) [verticais] :")
    for k in sorted(FACES):
        cl = defaultdict(set)
        for u in V: cl[assinatura(u, k)].add((u[0], u[2]))
        print(f"    face {k}: " + "  ".join(f"{c} <- u1,u3 in {sorted(v)}"
                                            for c, v in sorted(cl.items())))
