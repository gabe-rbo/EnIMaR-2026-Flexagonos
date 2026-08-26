"""run_camadas.py -- orbita do estado montado, SEM quociente (referencial fixo).
   Guarda tambem a orbita quocientada pelas 8 simetrias globais."""
import pickle, sys, time, os
from collections import deque
import flexcamadas as X, foldings as F, flexgrafo as G

CK = sys.argv[2] if len(sys.argv) > 2 else "../saidas/orbita_fixa.pkl"
LIM = float(sys.argv[1]) if len(sys.argv) > 1 else 36.0
P = X.HEXA
if os.path.exists(CK):
    vis, fila = pickle.load(open(CK, "rb")); fila = deque(fila)
else:
    folds = F.enumerar(); k0 = G.estado_montado(folds); g = folds[k0][1]
    seeds = [P.normaliza(g, o) for o in P.ordens_validas(g)]
    vis = set(seeds); fila = deque(seeds); print("sementes:", len(seeds))
t0 = time.time(); n = 0
while fila and time.time() - t0 < LIM:
    u = fila.popleft(); n += 1
    for v in P.vizinhos(u):
        if v not in vis: vis.add(v); fila.append(v)
pickle.dump((vis, list(fila)), open(CK, "wb"))
print(f"expandidos {n};  estados {len(vis)};  fila {len(fila)}")
