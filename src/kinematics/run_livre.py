"""run_livre.py -- BFS no MAJORANTE (abertura livre)."""
import pickle, sys, time, os
from collections import deque
import flexcamadas as X, foldings as F, flexgrafo as G

CK = "../saidas/orbita_livre.pkl"
LIM = float(sys.argv[1]) if len(sys.argv) > 1 else 38.0
if os.path.exists(CK):
    vis, fila = pickle.load(open(CK, "rb")); fila = deque(fila)
else:
    folds = F.enumerar(); k0 = G.estado_montado(folds); g = folds[k0][1]
    seeds = {X.canon(X.normaliza(g, o)) for o in X.ordens_validas(g)}
    vis = set(seeds); fila = deque(seeds); print("sementes:", len(seeds))
t0 = time.time(); n = 0
while fila and time.time() - t0 < LIM:
    u = fila.popleft(); n += 1
    for v in X.vizinhos2(u, livre=True):
        c = X.canon(v)
        if c not in vis: vis.add(c); fila.append(c)
pickle.dump((vis, list(fila)), open(CK, "wb"))
print(f"expandidos {n};  classes {len(vis)};  fila {len(fila)}")
