"""
flexgrafo.py
============
Pergunta em aberto (a): quais dobraduras planas sao ALCANCAVEIS por flexao a
partir do estado montado?

Formalizacao do flex ("levar para tras dois lados paralelos e abrir ao meio
como um livro", manual p.6).  Dobrar o quadrado 2x2 ao meio numa das duas
medianas produz um retangulo 1x2; reabrir devolve o estado de partida OU outro.
Logo:

  DEFINICAO.  Dois estados S, S' estao ligados por um flex na mediana L se a
  meia-dobra de S por L e a meia-dobra de S' por L coincidem (e S != S').

A meia-dobra e de novo uma dobradura plana: se R_L e a reflexao na mediana,
    g'_C = R_L o g_C   para as celulas do lado que se move,   g'_C = g_C  nas
outras.  As relacoes de charneira sao preservadas (duas celulas vizinhas em
posicoes opostas a L passam a ocupar a mesma posicao, dobradas na aresta
comum), de modo que g' e uma dobradura plana legitima do plano sobre um 1x2.

Isto e um MAJORANTE da alcancabilidade fisica (nao verificamos que a reabertura
separa as camadas no lugar certo).  Se ja o majorante exclui um arranjo, ele
esta excluido.
"""
from collections import defaultdict, deque
import foldings as F

RV = (2, 1, (0, 0))          # reflexao em x = 0   (z -> -conj z)
RH = (0, 1, (0, 0))          # reflexao em y = 0   (z -> conj z)


def normaliza(g, pos):
    """translada para que o bloco 2x2 fique centrado na origem."""
    xs = sorted({p[0] for p in pos}); ys = sorted({p[1] for p in pos})
    dx = -(xs[0] + xs[1])//2; dy = -(ys[0] + ys[1])//2
    t = (0, 0, (dx, dy))
    return tuple(F.comp(t, gi) for gi in g), tuple(F.zadd(p, (dx, dy)) for p in pos)


def meia_dobra(g, pos, eixo, lado):
    """eixo 'v' (mediana vertical) ou 'h'; lado = +1 move o lado positivo."""
    R = RV if eixo == 'v' else RH
    out = []
    for gi, p in zip(g, pos):
        coord = p[0] if eixo == 'v' else p[1]
        out.append(F.comp(R, gi) if (coord > 0) == (lado > 0) else gi)
    return tuple(out)


GLOB = [(a, s, (0, 0)) for a in range(4) for s in range(2)]


def canon(g):
    """forma canonica de uma dobradura a menos de isometria global do plano
       (rotacoes de 90 graus, reflexoes e translacoes)."""
    melhor = None
    for h in GLOB:
        gg = tuple(F.comp(h, gi) for gi in g)
        bs = [x[2] for x in gg]
        dx = -min(b[0] for b in bs); dy = -min(b[1] for b in bs)
        gg = tuple((a, s, (b[0] + dx, b[1] + dy)) for a, s, b in gg)
        if melhor is None or gg < melhor: melhor = gg
    return melhor


def grafo(folds):
    """arestas do grafo de flexao entre dobraduras planas."""
    est = [normaliza(g, pos) for _, g, pos in folds]
    chaves = defaultdict(list)
    for idx, (g, pos) in enumerate(est):
        for eixo in ('v', 'h'):
            for lado in (+1, -1):
                chaves[canon(meia_dobra(g, pos, eixo, lado))].append(idx)
    adj = defaultdict(set)
    for grupo in chaves.values():
        for a in grupo:
            for b in grupo:
                if a != b: adj[a].add(b)
    return est, adj


def componente(adj, inicio, n):
    vis = {inicio}; fila = deque([inicio])
    while fila:
        u = fila.popleft()
        for v in adj.get(u, ()):
            if v not in vis: vis.add(v); fila.append(v)
    return vis


def estado_montado(folds):
    """indice da dobradura que corresponde ao estado montado de flexagon_sim."""
    alvo_raw = {(0,0):(2,0),(0,1):(0,1),(0,2):(0,1),(0,3):(2,0),(1,0):(2,1),
                (1,3):(2,1),(2,0):(2,1),(2,3):(2,1),(3,0):(2,0),(3,1):(0,1),
                (3,2):(0,1),(3,3):(2,0)}
    for k, (_, g, pos) in enumerate(folds):
        if all((g[i][0] - g[0][0]) % 4 == (alvo_raw[c][0] - alvo_raw[(0,0)][0]) % 4
               and g[i][1] == alvo_raw[c][1] ^ (g[0][1] ^ alvo_raw[(0,0)][1])
               for i, c in enumerate(F.RING)):
            return k
    return None


if __name__ == "__main__":
    from quadflex import Flex, gamma_structure, label, latstr

    class G:
        def __init__(s, x): s._g = sorted(set(x))
        def gamma_gens(s): return s._g

    folds = F.enumerar()
    est, adj = grafo(folds)
    print("=" * 74)
    print(" HEXA-TETRAFLEXAGONO -- grafo de flexao")
    print("=" * 74)
    print(f"  dobraduras planas: {len(folds)}")
    # componentes conexas
    vistos = set(); comps = []
    for i in range(len(folds)):
        if i in vistos: continue
        c = componente(adj, i, len(folds)); comps.append(c); vistos |= c
    comps.sort(key=len, reverse=True)
    print(f"  componentes conexas: {len(comps)}  tamanhos: {[len(c) for c in comps]}")

    k0 = estado_montado(folds)
    print(f"  estado montado: indice {k0}")
    alvo = next(c for c in comps if k0 in c)
    print(f"  componente do estado montado: {len(alvo)} estados")

    sub = [folds[i] for i in sorted(alvo)]
    at = F.estados_por_face(folds); av = F.estados_por_face(sub)
    print("\n  arranjos exibiveis (todas -> alcancaveis):")
    for k in sorted(at):
        print(f"     face {k}: {len(at[k])} -> {len(av.get(k, []))}")

    NOME = {0:'1',1:'i',2:'-1',3:'-i'}
    gens = []; eps_vistos = set()
    print("\n  mapas de retorno alcancaveis:")
    for k in sorted(av):
        arrs = av[k]
        maps = {F.mapa_retorno(arrs[i], arrs[j])
                for i in range(len(arrs)) for j in range(len(arrs)) if i != j}
        print(f"     face {k}: {len(arrs)} arranjos, {len(maps)} mapas")
        for sg, ep in sorted(maps):
            eps_vistos.add(ep); gens += Flex(sg, ep).gamma_gens()
            st = gamma_structure(Flex(sg, ep))
            print(f"        sigma={sg} eps=({','.join(NOME[e] for e in ep)})"
                  f"  posto={st['rank']} Lambda={latstr(st['lattice'])}")
    st = gamma_structure(G(gens))
    print(f"\n  GRUPO CONJUNTO: {label(st)}")
    print(f"     Lambda = {latstr(st['lattice'])}   |P| = {st['P']}")
    print(f"  todos os eps triviais? {eps_vistos == {(0,0,0,0)}}")
