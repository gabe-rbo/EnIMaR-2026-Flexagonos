"""run_hexcamadas.py -- orbitas do grafo de flexao com camadas dos
   hexaflexagonos; le os arranjos alcancaveis e o grupo Gamma."""
import sys, time, pickle, os
from collections import deque, defaultdict
import hexcamadas as HC, hexaflex_an as A, rotflex as R, zclass as Z


def orbita(X, seed, segundos=None, limite=None):
    vis = {seed}; fila = deque([seed]); t0 = time.time()
    while fila:
        if segundos and time.time()-t0 > segundos: return vis, False
        if limite and len(vis) > limite: return vis, False
        u = fila.popleft()
        for w in X.vizinhos(u):
            if w not in vis: vis.add(w); fila.append(w)
    return vis, True


def analisa(N, nome, segundos=None, limite=None):
    X = HC.Hexa(N)
    eg = HC.estados_geom(N, 'oposto')
    print("=" * 74); print(f" {nome}: grafo de flexao COM CAMADAS"); print("=" * 74)
    print(f"  estados dobrados hexagonais de partida: {len(eg)}")
    vistos = set(); res = []
    for e0, v0 in eg:
        if e0 in vistos: continue
        o, completa = orbita(X, e0, segundos, limite)
        vistos |= o
        hx = [e for e in o if HC.hexagonal(e[1])]
        vis = defaultdict(list)
        for g, pil in hx:
            v = HC.hexagonal(pil); arr = {}
            for c, cs in pil:
                i = cs[-1]
                arr[(0 if i == N-1 else i, g[i][1])] = (HC.H.indice_tile(c, v), g[i][0])
            if len(arr) == 6: vis[frozenset(arr)].append(arr)
        fl = set()
        for S, lst in vis.items():
            for a in range(len(lst)):
                for b in range(len(lst)):
                    if a != b:
                        m = A.retorno(lst[a], lst[b])
                        if m != (tuple(range(6)), (0,)*6): fl.add(m)
        st = A.gamma(fl) if fl else dict(rank=0, P=1)
        nrot = sum(1 for m in fl if R.e_rotacao(*m))
        res.append((len(o), len(hx), len(vis), len(fl), nrot,
                    (st['rank'], st['P']), completa))
    print(f"  {'orbita':>8}{'hexag.':>8}{'faces':>7}{'mapas':>7}{'rotacoes':>10}"
          f"  Gamma")
    todos = set()
    from collections import Counter
    cont = Counter(res)
    for L, h, f, m, nr, st, comp in sorted(cont, key=lambda z: -z[0]):
        todos.add(st)
        print(f"  {L:>8}{h:>8}{f:>7}{m:>7}{nr:>10}   posto {st[0]} |P| {st[1]}"
              f"   x{cont[(L,h,f,m,nr,st,comp)]} componentes"
              + ("" if comp else "   (parcial)"))
    print(f"\n  TODOS os mapas de retorno alcancaveis sao rotacoes em torno de O: "
          f"{all(m == nr for _, _, _, m, nr, _, _ in res)}")
    print(f"  classes (posto,|P|) que ocorrem: {sorted(todos)}")
    for c in sorted(todos):
        print(f"     {c} -> {Z.CLASSES.get(c)}")


if __name__ == "__main__":
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    seg = float(sys.argv[2]) if len(sys.argv) > 2 else None
    analisa(N, {10: "TRI-HEXAFLEXAGONO", 19: "HEXA-HEXAFLEXAGONO"}.get(N, str(N)), seg)
