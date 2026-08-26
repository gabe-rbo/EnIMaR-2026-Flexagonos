"""componentes.py -- decomposicao COMPLETA do grafo de flexao em componentes.
   Roda por pedacos com checkpoint (limite de 45 s do device)."""
import pickle, os, sys, time
from collections import deque, Counter
import flexcamadas as X
P = X.HEXA
CK = "../saidas/componentes.pkl"
LIM = float(sys.argv[1]) if len(sys.argv) > 1 else 36.0

if os.path.exists(CK):
    resto, tam = pickle.load(open(CK, "rb"))
else:
    orb = set(pickle.load(open("../saidas/orbita_fixa.pkl", "rb"))[0])
    ALL = set()
    for g in P.dobraduras():
        for o in P.ordens_validas(g): ALL |= set(P.imagens((g, o)))
    resto = ALL - orb
    tam = Counter({len(orb): 1})
    print("estados fora da ilha:", len(resto))
    pickle.dump((resto, tam), open(CK, "wb"))
    raise SystemExit(0)

t0 = time.time()
while resto and time.time() - t0 < LIM:
    s = next(iter(resto))
    vis = {s}; fila = deque([s])
    while fila:
        u = fila.popleft()
        for v in P.vizinhos(u):
            if v not in vis: vis.add(v); fila.append(v)
    tam[len(vis)] += 1
    resto -= vis
pickle.dump((resto, tam), open(CK, "wb"))
print(f"faltam {len(resto)} estados;  componentes ja fechadas: {sum(tam.values())}")
print("tamanhos:", dict(sorted(tam.items())))
