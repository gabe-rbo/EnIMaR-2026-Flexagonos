"""
wgrupo.py
=========
Calculo de W^+(D) FACE A FACE (Teorema das retas de dobra).

Uma reta e ADMISSIVEL para a face D quando contem arestas do ladrilhamento (a
dobra nao vinca nenhum ladrilho) e a sua reflexao preserva o ladrilhamento.
W(D) = grupo gerado por essas reflexoes; W^+(D) = a sua parte direta, gerada
pelos PRODUTOS de duas reflexoes.  O Teorema das retas de dobra da
Gamma <= W^+(D), o que fixa de antemao que classes das nove podem ocorrer.

Calculam-se duas versoes:
  * CONFINADA  -- so as retas interiores a D (o flexagono nunca se abre para
                  fora da face; e o caso dos hexaflexagonos);
  * LIVRE      -- todas as retas do reticulado que tocam D (o flexagono pode
                  abrir-se por um lado e deslizar; e o caso dos
                  tetraflexagonos).
Gamma esta sempre entre as duas.
"""
from fractions import Fraction
import zclass as Z

A4, A6 = Z.Anel(4), Z.Anel(6)


# ------------------------------------------------------------ reticulado quadrado
def quad_retas(cells, livre):
    """cells = celulas (r,c) da face.  Retas: x = k (verticais), y = k."""
    xs = sorted({c for r, c in cells} | {c+1 for r, c in cells})
    ys = sorted({-r for r, c in cells} | {-r-1 for r, c in cells})
    if not livre:
        xs = [k for k in xs if any(c+1 <= k for r, c in cells)
              and any(c >= k for r, c in cells)]
        ys = [k for k in ys if any(-r-1 >= k for r, c in cells)
              and any(-r <= k for r, c in cells)]
    return xs, ys


def quad_W(cells, livre=True):
    """geradores de W^+ no anel Z[i] com denominador d=1."""
    xs, ys = quad_retas(cells, livre)
    g = []
    for i in range(len(xs)):
        for j in range(len(xs)):
            if i != j: g.append((0, (2*(xs[i]-xs[j]), 0)))
    for i in range(len(ys)):
        for j in range(len(ys)):
            if i != j: g.append((0, (0, 2*(ys[i]-ys[j]))))
    for a in xs:
        for b in ys: g.append((2, (2*a, 2*b)))
    return Z.estrutura(A4, sorted(set(g))) if g else dict(rank=0, P=1, lattice=[])


# --------------------------------------------------------- reticulado triangular
import hexaflex as H


def tri_retas(cents, livre):
    """cents = centroides x3 dos triangulos da face.  Devolve (u, P)."""
    import hexcamadas as HC
    R = HC.retas(cents)
    if livre: return R
    out = {}
    for (u, off), P in R.items():
        P3 = (3*P[0], 3*P[1])
        s = {(1 if HC.lado_reta(c, u, P3) > 0 else
              -1 if HC.lado_reta(c, u, P3) < 0 else 0) for c in cents}
        if 1 in s and -1 in s: out[(u, off)] = P
    return out


def tri_W(cents, livre=True):
    R = list(tri_retas(cents, livre).items())
    g = []
    for i in range(len(R)):
        for j in range(len(R)):
            if i == j: continue
            (u1, _), P1 = R[i]; (u2, _), P2 = R[j]
            c = H.comp(H.refl(P1, u1), H.refl(P2, u2))
            assert c[1] == 0
            if (c[0], c[2]) != (0, (0, 0)): g.append((c[0], c[2]))
    return Z.estrutura(A6, sorted(set(g))) if g else dict(rank=0, P=1, lattice=[])


# ------------------------------------------------------------------- biblioteca
QUAD = {
    "quadrado 2x2 (tetraflexagonos)": [(0, 0), (0, 1), (1, 0), (1, 1)],
    "domino 1x2": [(0, 0), (0, 1)],
    "tira 1x3": [(0, 0), (0, 1), (0, 2)],
    "rectangulo 2x3": [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (1, 2)],
    "quadrado 3x3": [(r, c) for r in range(3) for c in range(3)],
    "tromino L": [(0, 0), (0, 1), (1, 0)],
}
def _hexcent():
    return [H.wadd((0, 0), r) for r in H.REF_TILES]
TRI = {
    "hexagono de 6 triangulos (hexaflexagonos)": _hexcent(),
    "losango (2 triangulos)": _hexcent()[:2],
    "trapezio (3 triangulos)": _hexcent()[:3],
    "meio-hexagono + 1": _hexcent()[:4],
}


def linha(nome, st_conf, st_livre):
    def s(st):
        return f"posto {st['rank']}, |P| = {st['P']}"
    return f"  {nome:<42} confinada: {s(st_conf):<22} livre: {s(st_livre)}"


if __name__ == "__main__":
    print("=" * 92)
    print(" W^+(D) FACE A FACE   (Gamma <= W^+(D) pelo Teorema das retas de dobra)")
    print("=" * 92)
    print("\n reticulado QUADRADO:")
    for nome, cells in QUAD.items():
        print(linha(nome, quad_W(cells, False), quad_W(cells, True)))
    print("\n reticulado TRIANGULAR:")
    for nome, cents in TRI.items():
        print(linha(nome, tri_W(cents, False), tri_W(cents, True)))
    print("""
 Leitura: a coluna CONFINADA e o grupo quando o flexagono nunca se abre para
 fora da face --- e o caso do hexagono, cujas retas admissiveis passam todas
 pelo centro, donde W^+ = C_6 e Gamma finito.  A coluna LIVRE e o grupo quando
 ele pode abrir-se por um lado e deslizar --- e o caso do quadrado, onde duas
 reflexoes paralelas dao uma translacao e o posto sobe a 2.""")
