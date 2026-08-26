import foldings as F, flexgrafo as X
from collections import defaultdict
folds = F.enumerar()
# --- estado montado: comparar (a,s) a menos de composicao global (8 simetrias)
alvo = {(0,0):(2,0),(0,1):(0,1),(0,2):(0,1),(0,3):(2,0),(1,0):(2,1),
        (1,3):(2,1),(2,0):(2,1),(2,3):(2,1),(3,0):(2,0),(3,1):(0,1),
        (3,2):(0,1),(3,3):(2,0)}
GLOB = [(a, s, (0,0)) for a in range(4) for s in range(2)]
achados = []
for k,(bits,g,pos) in enumerate(folds):
    for h in GLOB:
        if all(F.comp(h, g[i])[:2] == alvo[c] for i,c in enumerate(F.RING)):
            achados.append(k); break
print("estado montado, indices:", achados)
est, adj = X.grafo(folds)
vis=set(); comps=[]
for i in range(len(folds)):
    if i in vis: continue
    c = X.componente(adj, i, len(folds)); comps.append(sorted(c)); vis|=c
comps.sort(key=len, reverse=True)
print("componentes:", [len(c) for c in comps])
for c in comps:
    faces = F.estados_por_face([folds[i] for i in c])
    print(f"  comp de {len(c)} estados: faces exibiveis {sorted(faces)} "
          f"(arranjos {[len(faces[k]) for k in sorted(faces)]})"
          f"  contem montado: {any(a in c for a in achados)}")
