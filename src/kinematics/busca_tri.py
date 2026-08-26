"""
busca_tri.py
============
Determinacao do plano do TRI-TETRAFLEXAGONO por necessidade fisica.

O octomino da Figura A.1 tem 9 adjacencias de grade; num flexagono a folha e
uma TIRA (caminho) e as adjacencias restantes sao CORTES (o rasgo).  Ha tres
caminhos hamiltonianos possiveis (a tem grau 1, logo e ponta).  A colagem une
dois lados BRANCOS.  Procuramos a combinacao (tira, colagem) em que o modelo
com camadas exibe as tres faces e reproduz o diagrama do EnIMaR
(F com 2 arranjos, V e E com 1).
"""
from collections import defaultdict
import flexcamadas as X
import foldings_tri as T0
import foldings as F

CAMINHOS = {
    "a-b-c-d-e-h-g-f": ['a', 'b', 'c', 'd', 'e', 'h', 'g', 'f'],
    "a-b-c-f-g-d-e-h": ['a', 'b', 'c', 'f', 'g', 'd', 'e', 'h'],
    "a-b-c-f-g-h-e-d": ['a', 'b', 'c', 'f', 'g', 'h', 'e', 'd'],
    "(todas as 9 charneiras)": None,
}
BRANCO = {'a': ['v'], 'e': ['f'], 'd': ['v', 'f']}
COLAS = []
for A, la in BRANCO.items():
    for B, lb in BRANCO.items():
        if A >= B: continue
        for x in la:
            for y in lb: COLAS.append((A, B, x + y))

ADJ = [('a','b'),('b','c'),('c','d'),('d','e'),('f','g'),('g','h'),
       ('c','f'),('d','g'),('e','h')]


def testar(nome, cam, cola):
    if cam is None: hin = ADJ
    else: hin = [(cam[i], cam[i+1]) for i in range(7)]
    P = X.Plano("tri", {c: T0.POS[c] for c in T0.CELL}, hin,
                T0.FRENTE, T0.VERSO, cola=[cola])
    ds = P.dobraduras()
    est = []
    for g in ds:
        for o in P.ordens_validas(g): est.append(P.canon(P.normaliza(g, o)))
    est = sorted(set(est))
    vis = defaultdict(set)
    for e in est:
        for im in P.imagens(e):
            r = P.exibida(*im)
            if r: vis[r[0]].add(r[1])
    return P, ds, est, {k: len(v)//4 for k, v in vis.items()}


if __name__ == "__main__":
    print(f"{'tira':<26}{'colagem':<14}{'dobrad.':>8}{'estados':>9}   faces exibidas")
    bons = []
    for nome, cam in CAMINHOS.items():
        for cola in COLAS:
            P, ds, est, vis = testar(nome, cam, cola)
            marca = ""
            if set(vis) == {'F', 'V', 'E'}:
                marca = "  <== exibe as 3 faces"
                bons.append((nome, cola, vis))
            print(f"{nome:<26}{cola[0]+'-'+cola[1]+' '+cola[2]:<14}"
                  f"{len(ds):>8}{len(est):>9}   {dict(sorted(vis.items()))}{marca}")
    print()
    print("candidatos que exibem as tres faces:")
    for n, c, v in bons: print("   ", n, c, v)
