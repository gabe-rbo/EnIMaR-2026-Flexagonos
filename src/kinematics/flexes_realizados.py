"""
flexes_realizados.py
====================
Os mapas de retorno que os dois tetraflexagonos REALMENTE realizam, lidos da
orbita do modelo com camadas (flexcamadas.py + run_camadas.py).  Fonte unica
para as verificacoes numericas.

HEXA / TRI : "face k" -> Flex representativo (o menor mapa nao trivial)
HEXA_TODOS / TRI_TODOS : "face k" -> lista de todos os mapas realizados
"""
import pickle, os
from collections import defaultdict
import flexcamadas as X, foldings as F
from quadflex import Flex

CK = os.path.join(os.path.dirname(__file__), "../saidas/orbita_fixa.pkl")


def _mapas(P, estados):
    arr = defaultdict(set)
    for e in estados:
        r = P.exibida(*e)
        if r: arr[r[0]].add(r[1])
    out = {}
    for k, S in arr.items():
        L = sorted(S)
        ms = {F.mapa_retorno(L[i], L[j])
              for i in range(len(L)) for j in range(len(L)) if i != j}
        ms = {m for m in ms if m != ((1, 2, 3, 4), (0, 0, 0, 0))}
        if ms: out[f"face {k}"] = sorted(ms)
    return out


HEXA_TODOS = _mapas(X.HEXA, pickle.load(open(CK, "rb"))[0])

_T = X.TRI
_est = sorted({e for g in _T.dobraduras() for o in _T.ordens_validas(g)
               for e in _T.imagens(_T.normaliza(g, o))})
_rest = set(_est); _comps = []
while _rest:
    _s = next(iter(_rest)); _c, _ = X.orbita_fixa(_T, [_s])
    _comps.append(_c & set(_est)); _rest -= _c
_princ = max(_comps, key=lambda c: len({r[0] for e in c for r in [_T.exibida(*e)] if r}))
TRI_TODOS = _mapas(_T, _princ)

from quadflex import gamma_structure


def _melhor(ms):
    """representante: o mapa cujo Gamma e maior (posto, depois |P|)."""
    def chave(m):
        st = gamma_structure(Flex(*m)); return (st["rank"], st["P"], m)
    return Flex(*max(ms, key=chave))


HEXA = {k: _melhor(v) for k, v in HEXA_TODOS.items()}
TRI = {k: _melhor(v) for k, v in TRI_TODOS.items()}

if __name__ == "__main__":
    for nome, d in (("HEXA-TETRAFLEXAGONO", HEXA_TODOS),
                    ("TRI-TETRAFLEXAGONO", TRI_TODOS)):
        print(nome)
        for k in sorted(d): print(f"   {k}: {len(d[k])} mapas; repr. {d[k][0]}")
