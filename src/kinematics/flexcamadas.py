"""
flexcamadas.py
==============
MODELO GERAL DE FLEXAO COM ORDEM DE CAMADAS (tetraflexagonos).

Um *estado dobrado* (no sentido de Demaine--O'Rourke) do plano de um
flexagono e o par
      (g, pilha) ,
com g_C isometria do plano para cada celula C do plano, e pilha_p uma ordem
total (de baixo para cima) das celulas que caem na posicao p, sujeito as tres
condicoes de nao-atravessamento:

  (T1) taco-taco      dois vincos sobre a mesma aresta da mesma posicao tem
                      intervalos de camadas encaixados ou disjuntos;
  (T2) taco-tortilha  a camada de uma ligacao plana sobre a aresta e nao fica
                      estritamente dentro do intervalo de um vinco sobre e;
  (T3) tortilha-tortilha  duas ligacoes planas pela mesma aresta preservam a
                      ordem relativa das camadas dos dois lados.

Estas condicoes sao NECESSARIAS E SUFICIENTES para que a ordem de camadas
descreva um objeto de papel sem auto-interseccao.

Duas correccoes em relacao ao modelo puramente combinatorio:

 (V) VISIBILIDADE.  Uma face k so esta EXIBIDA quando as suas quatro celulas
     sao as celulas de TOPO das quatro posicoes, com o lado k para cima --- e
     o que se ve, e e sobre o que se ve que a funcao esta pintada.

 (A) ALCANCABILIDADE.  O flex do manual ("levar para tras dois lados paralelos
     e abrir ao meio como um livro") e:
        1. dobrar ao meio numa mediana:  a metade movel fica por cima ou por
           baixo da outra  (o resultado tem de ser um estado valido);
        2. reabrir por uma das duas arestas paralelas a mediana, fazendo
           passar para o outro lado um BLOCO DE CAMADAS do topo (que roda por
           cima) ou do fundo (que roda por baixo) --- e o que faz o dedo ao
           abrir o livro;  so podem ser cortadas charneiras que assentem sobre
           a aresta de abertura;  o resultado tem de ser um estado valido.
     Com `modo='livre'` obtem-se o MAJORANTE em que o conjunto que passa para
     o outro lado pode ser qualquer subconjunto admissivel de camadas (o que
     ja nao e um flex: exigiria separar camadas nao contiguas).

Movimentos globais: rodar 90 graus na mao e virar o flexagono ao contrario;
sao tratados por quociente (canon).
"""
from itertools import product, permutations
from collections import defaultdict, deque
from foldings import comp, apply, ID, REF, ref_vert, ref_horiz, quadrante

_OP = {'L': 'R', 'R': 'L', 'T': 'B', 'B': 'T'}
GLOB = [(a, s, (0, 0)) for a in range(4) for s in range(2)]
ROT = (1, 0, (0, 0))
FLIP = (0, 1, (0, 0))


class Plano:
    """plano de um flexagono: celulas numa grade, charneiras, lados, colagens.

    frente[c] / verso[c] = (face, quadrante) ou None (quadradinho branco).
    cola = lista de pares (A, B): o VERSO de A esta colado a FRENTE de B."""

    def __init__(self, nome, grade, hinges, frente, verso, cola=()):
        self.nome = nome
        self.cells = list(grade)
        self.n = len(self.cells)
        self.ix = {c: i for i, c in enumerate(self.cells)}
        self.grade = dict(grade)
        self.hinges = [(self.ix[a], self.ix[b]) for a, b in hinges]
        self.frente = [frente[c] for c in self.cells]
        self.verso = [verso[c] for c in self.cells]
        self.cola = [(self.ix[a], self.ix[b], t) for a, b, t in cola]
        self.centro = [(2*grade[c][1] + 1, -(2*grade[c][0] + 1)) for c in self.cells]
        self.meio = []
        self.refs = []
        for a, b in self.hinges:
            (r1, c1), (r2, c2) = self.grade[self.cells[a]], self.grade[self.cells[b]]
            if r1 == r2:
                self.meio.append((2*max(c1, c2), -(2*r1 + 1)))
                self.refs.append(ref_vert(2*max(c1, c2)))
            else:
                self.meio.append((2*c1 + 1, -2*max(r1, r2)))
                self.refs.append(ref_horiz(-2*max(r1, r2)))
        # arvore geradora e arestas extra
        viz = defaultdict(list)
        for h, (a, b) in enumerate(self.hinges):
            viz[a].append((b, h)); viz[b].append((a, h))
        self.arv = []; vist = {0}; fila = deque([0])
        while fila:
            u = fila.popleft()
            for v, h in viz[u]:
                if v not in vist:
                    vist.add(v); self.arv.append((u, v, h)); fila.append(v)
        self.extra = [h for h in range(len(self.hinges))
                      if h not in {t[2] for t in self.arv}]

    # ------------------------------------------------------------- geometria
    def posicoes(self, g):
        return [apply(g[i], self.centro[i]) for i in range(self.n)]

    def estrutura(self, g, pos):
        tacos = defaultdict(list); tort = defaultdict(list)
        for h, (i, j) in enumerate(self.hinges):
            q = apply(g[i], self.meio[h]); p = pos[i]
            dx, dy = q[0] - p[0], q[1] - p[1]
            l = ('L' if dx < 0 else 'R') if dx else ('B' if dy < 0 else 'T')
            if pos[i] == pos[j]:
                tacos[(pos[i], l)].append((i, j))
            else:
                tort[(pos[i], l)].append((i, j))
                tort[(pos[j], _OP[l])].append((j, i))
        return tacos, tort

    def valida(self, tacos, tort, nivel, g=None, pos=None):
        for ch, pares in tacos.items():
            iv = [tuple(sorted((nivel[u], nivel[v]))) for u, v in pares]
            for a in range(len(iv)):
                for b in range(a + 1, len(iv)):
                    (l1, h1), (l2, h2) = iv[a], iv[b]
                    if l1 < l2 < h1 < h2 or l2 < l1 < h2 < h1: return False
            for lo, hi in iv:
                for w, _ in tort.get(ch, ()):
                    if lo < nivel[w] < hi: return False
        for ch, pares in tort.items():
            for a in range(len(pares)):
                for b in range(a + 1, len(pares)):
                    u, u2 = pares[a]; v, v2 = pares[b]
                    if (nivel[u] < nivel[v]) != (nivel[u2] < nivel[v2]): return False
        if self.cola and g is not None:
            for A, B, t in self.cola:
                if pos[A] != pos[B]: return False
                sA, sB = g[A][1], g[B][1]
                # lado colado de A virado para baixo?  verso: sA==0 ; frente: sA==1
                dA = (sA == 0) if t[0] == 'v' else (sA == 1)
                dB = (sB == 0) if t[1] == 'v' else (sB == 1)
                if dA == dB: return False          # tem de ficarem cara a cara
                if nivel[A] - nivel[B] != (1 if dA else -1): return False
        return True

    def ok(self, g, pil):
        pos = self.posicoes(g)
        ta, to = self.estrutura(g, pos)
        return self.valida(ta, to, niveis(pil), g, pos)

    def ordens_validas(self, g):
        pos = self.posicoes(g)
        ta, to = self.estrutura(g, pos)
        pp = defaultdict(list)
        for i in range(self.n): pp[pos[i]].append(i)
        ps = sorted(pp); out = []
        for esc in product(*[permutations(pp[p]) for p in ps]):
            nv = {}
            for p, o in zip(ps, esc):
                for k, c in enumerate(o): nv[c] = k
            if self.valida(ta, to, nv, g, pos):
                out.append(tuple(sorted(zip(ps, esc))))
        return out

    def normaliza(self, g, pil):
        pos = self.posicoes(g)
        dx = -min(p[0] for p in pos) - 1; dy = -min(p[1] for p in pos) - 1
        t = (0, 0, (dx, dy))
        return (tuple(comp(t, gi) for gi in g),
                tuple(sorted(((p[0] + dx, p[1] + dy), c) for p, c in pil)))

    # ------------------------------------------------------------ dobraduras
    def dobraduras(self):
        """todas as dobraduras planas sobre um bloco 2x2 (a menos de translacao;
           g da primeira celula em {ID, REF})."""
        out = []
        for g0 in (ID, REF):
            for bits in product((0, 1), repeat=len(self.arv)):
                g = [None]*self.n; g[0] = g0
                for (u, v, h), t in zip(self.arv, bits):
                    g[v] = comp(g[u], self.refs[h]) if t else g[u]
                bom = True
                for h in self.extra:
                    a, b = self.hinges[h]
                    if g[b] != g[a] and g[b] != comp(g[a], self.refs[h]):
                        bom = False; break
                if not bom: continue
                g = tuple(g); pos = self.posicoes(g)
                d = set(pos)
                if len(d) != 4: continue
                xs = sorted({p[0] for p in d}); ys = sorted({p[1] for p in d})
                if len(xs) != 2 or len(ys) != 2: continue
                if xs[1]-xs[0] != 2 or ys[1]-ys[0] != 2: continue
                mau = False
                for A, B, t in self.cola:
                    sA, sB = g[A][1], g[B][1]
                    dA = (sA == 0) if t[0] == 'v' else (sA == 1)
                    dB = (sB == 0) if t[1] == 'v' else (sB == 1)
                    if pos[A] != pos[B] or dA == dB: mau = True; break
                if mau: continue
                out.append(g)
        return out

    # ------------------------------------------------------------- o flex
    def dobrar(self, g, pil, eixo, sinal, acima):
        idx = 0 if eixo == 'v' else 1
        R = ref_vert(0) if eixo == 'v' else ref_horiz(0)
        d = dict(pil)
        mov = [p for p in d if (p[idx] > 0) == (sinal > 0)]
        ng = list(g)
        for p in mov:
            for c in d[p]: ng[c] = comp(R, g[c])
        novo = {}
        for p, cells in d.items():
            if p in mov: continue
            q = (-p[0], p[1]) if eixo == 'v' else (p[0], -p[1])
            if q in d:
                m = tuple(reversed(d[q]))
                novo[p] = cells + m if acima else m + cells
            else: novo[p] = cells
        return tuple(ng), novo

    def _arcos(self, corta):
        """componentes do grafo das celulas depois de cortar as charneiras
           marcadas (uniao-busca)."""
        pai = list(range(self.n))
        def acha(x):
            while pai[x] != x: pai[x] = pai[pai[x]]; x = pai[x]
            return x
        for h, (a, b) in enumerate(self.hinges):
            if corta[h]: continue
            ra, rb = acha(a), acha(b)
            if ra != rb: pai[ra] = rb
        for A, B, _t in self.cola:          # a colagem nao se pode cortar
            ra, rb = acha(A), acha(B)
            if ra != rb: pai[ra] = rb
        cl = defaultdict(list)
        for i in range(self.n): cl[acha(i)].append(i)
        return [tuple(v) for v in cl.values()]

    def abrir(self, gH, pilH, eixo, w, modo):
        R = ref_vert(w) if eixo == 'v' else ref_horiz(w)
        corta = []
        for h, (i, j) in enumerate(self.hinges):
            q = apply(gH[i], self.meio[h])
            corta.append(q[0] == w if eixo == 'v' else q[1] == w)
        comps = self._arcos(corta); m = len(comps)
        if m < 2: return []
        ps = sorted(pilH); res = []
        for msk in range(1, (1 << m) - 1):
            S = set()
            for t in range(m):
                if msk >> t & 1: S |= set(comps[t])
            if modo != 'livre':
                bom = True
                for p in ps:
                    cs = pilH[p]; k = [c in S for c in cs]; n = sum(k)
                    alvo = ([False]*(len(cs)-n) + [True]*n if modo == 'topo'
                            else [True]*n + [False]*(len(cs)-n))
                    if k != alvo: bom = False; break
                if not bom: continue
            ng = tuple(comp(R, gH[c]) if c in S else gH[c] for c in range(self.n))
            npil = {}
            for p in ps:
                cs = pilH[p]
                mv = tuple(c for c in cs if c in S)
                st = tuple(c for c in cs if c not in S)
                if st: npil[p] = st
                if mv:
                    p2 = (2*w - p[0], p[1]) if eixo == 'v' else (p[0], 2*w - p[1])
                    npil[p2] = tuple(reversed(mv))
            xs = sorted({p[0] for p in npil}); ys = sorted({p[1] for p in npil})
            if len(npil) != 4 or len(xs) != 2 or len(ys) != 2: continue
            if xs[1]-xs[0] != 2 or ys[1]-ys[0] != 2: continue
            e = self.normaliza(ng, tuple(sorted(npil.items())))
            if self.ok(e[0], dict(e[1])): res.append(e)
        return res

    def vizinhos(self, est, livre=False):
        # dobrar/abrir usam as medianas do referencial normalizado (posicoes em
        # {-1,+1}^2); normalizar aqui e a identidade sobre os estados que
        # 'abrir' devolve e conserta os estados crus de 'dobraduras()'.
        g, pil = self.normaliza(*est)
        modos = ('livre',) if livre else ('topo', 'fundo')
        out = []
        for eixo in ('v', 'h'):
            idx = 0 if eixo == 'v' else 1
            for sinal in (1, -1):
                for acima in (True, False):
                    gH, pH = self.dobrar(g, pil, eixo, sinal, acima)
                    if not self.ok(gH, pH): continue
                    c = next(iter(pH))[idx]
                    for w in (c - 1, c + 1):
                        for modo in modos:
                            out += self.abrir(gH, pH, eixo, w, modo)
        return out

    # ---------------------------------------------------- simetrias globais
    def imagens(self, est):
        g, pil = est
        for h in GLOB:
            yield self.normaliza(
                tuple(comp(h, gi) for gi in g),
                tuple((apply(h, p), (tuple(reversed(c)) if h[1] else c))
                      for p, c in pil))

    def canon(self, est):
        return min(self.imagens(est))

    # ------------------------------------------------------- visibilidade
    def exibida(self, g, pil):
        d = dict(pil)
        xs = sorted({p[0] for p in d}); ys = sorted({p[1] for p in d})
        if len(d) != 4 or len(xs) != 2 or len(ys) != 2: return None
        face = None; arr = {}
        for p, cells in d.items():
            i = cells[-1]; a, s, _ = g[i]
            lado = (self.frente if s == 0 else self.verso)[i]
            if lado is None: return None
            fc, quad = lado
            if face is None: face = fc
            elif face != fc: return None
            arr[quad] = (quadrante(p, xs, ys), a)
        if len(arr) != 4: return None
        return face, tuple(arr[j] for j in (1, 2, 3, 4))

    def perfil(self, g):
        c = defaultdict(int)
        for p in self.posicoes(g): c[p] += 1
        return tuple(sorted(c.values()))


def niveis(pil):
    nv = {}
    for p, cells in (pil.items() if isinstance(pil, dict) else pil):
        for k, c in enumerate(cells): nv[c] = k
    return nv


def orbita_fixa(P, sementes, livre=False, segundos=None):
    """orbita num referencial fixo (sem quociente pelas simetrias globais)."""
    import time
    vis = set(sementes); fila = deque(sementes); t0 = time.time()
    while fila:
        if segundos and time.time() - t0 > segundos: break
        u = fila.popleft()
        for v in P.vizinhos(u, livre):
            if v not in vis: vis.add(v); fila.append(v)
    return vis, fila


def orbita(P, sementes, livre=False, limite=None, segundos=None):
    import time
    vis = set(sementes); fila = deque(sementes); t0 = time.time()
    while fila:
        if segundos and time.time() - t0 > segundos: break
        u = fila.popleft()
        for v in P.vizinhos(u, livre):
            c = P.canon(v)
            if c not in vis:
                vis.add(c); fila.append(c)
                if limite and len(vis) > limite: return vis, fila
    return vis, fila


# =========================================================== os dois planos
import foldings as _F
import foldings_tri as _T

HEXA = Plano("hexa-tetraflexagono",
             {c: c for c in _F.RING},
             [(_F.RING[i], _F.RING[(i+1) % 12]) for i in range(12)],
             _F.FRENTE, _F.VERSO)

TRI = Plano("tri-tetraflexagono",
            {c: _T.POS[c] for c in _T.CELL},
            _T.HINGES, _T.FRENTE, _T.VERSO, cola=[_T.COLA])
