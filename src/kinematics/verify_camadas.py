"""
verify_camadas.py -- verificacao do modelo com camadas e do teorema das retas
de dobra.  Todos os testes sao exatos (aritmetica inteira).
"""
import pickle
from collections import defaultdict
import flexcamadas as X, foldings as F
from quadflex import Flex, gamma_structure, latstr, covol

ok = []
def t(nome, cond):
    ok.append(bool(cond)); print(f"  [{'OK ' if cond else 'FALHA'}] {nome}")

P = X.HEXA
orb = pickle.load(open("../saidas/orbita_fixa.pkl", "rb"))[0]
print("=" * 74); print(" VERIFICACAO -- modelo com camadas"); print("=" * 74)

t("orbita nao vazia (19200 estados)", len(orb) == 19200)
t("todo estado da orbita e um estado dobrado valido",
  all(P.ok(g, dict(pil)) for g, pil in orb))
t("toda posicao tem pelo menos uma celula e as 4 formam um bloco 2x2",
  all(len(pil) == 4 and sorted({p[0] for p, _ in pil}) == [-1, 1]
      and sorted({p[1] for p, _ in pil}) == [-1, 1] for _, pil in orb))
t("as 12 celulas estao distribuidas pelas 4 posicoes, sem repeticao",
  all(sorted(c for _, cs in pil for c in cs) == list(range(12)) for _, pil in orb))

amostra = sorted(orb)[:250]
t("a orbita e fechada pelos flexes (amostra de 250)",
  all(v in orb for u in amostra for v in P.vizinhos(u)))
t("todo vizinho gerado e valido (amostra)",
  all(P.ok(*(v[0], dict(v[1]))) for u in amostra for v in P.vizinhos(u)))

arr = defaultdict(set)
for e in orb:
    r = P.exibida(*e)
    if r: arr[r[0]].add(r[1])
t("faces 1 e 2 com 3 arranjos essenciais (6 = 3 x meia-volta)",
  len(arr[1]) == 6 and len(arr[2]) == 6)
t("faces 3..6 com 2 arranjos essenciais (4 = 2 x meia-volta)",
  all(len(arr[k]) == 4 for k in (3, 4, 5, 6)))

maps = set()
for k, S in arr.items():
    L = sorted(S)
    maps |= {F.mapa_retorno(L[i], L[j])
             for i in range(len(L)) for j in range(len(L)) if i != j}
t("teorema das retas de dobra: todo A_j esta em W+ (eps em {1,-1})",
  all(set(e) <= {0, 2} for _, e in maps))
t("todo mapa de retorno alcancavel tem eps CONSTANTE",
  all(len(set(e)) == 1 for _, e in maps))

gens = []
for sg, ep in maps: gens += Flex(sg, ep).gamma_gens()
class _G:
    def __init__(s, x): s._g = sorted(set(x))
    def gamma_gens(s): return s._g
st = gamma_structure(_G(gens))
t("Gamma tem posto 2 e |P| = 1", st["rank"] == 2 and st["P"] == 1)
t("Lambda = 2Z[i]: covolume 4 e 2, 2i pertencem ao reticulado",
  covol(st["lattice"]) == 4
  and all(any(x % 4 == 0 for x in v) for v in st["lattice"])
  and all(v[0] % 4 == 0 and v[1] % 4 == 0 for v in st["lattice"]))
print(f"     Lambda = {latstr(st['lattice'])}")

# ---------------------------------------------------------------- tri
T = X.TRI
est = sorted({e for g in T.dobraduras() for o in T.ordens_validas(g)
              for e in T.imagens(T.normaliza(g, o))})
rest = set(est); comps = []
while rest:
    s0 = next(iter(rest)); c, _ = X.orbita_fixa(T, [s0]); comps.append(c & set(est)); rest -= c
princ = [c for c in comps if len({P0 for e in c for P0 in [T.exibida(*e)] if P0}) >= 3]
t("tri-tetraflexagono: existe componente que exibe as 3 faces", len(princ) >= 1)
a = defaultdict(set)
for e in princ[0]:
    r = T.exibida(*e)
    if r: a[r[0]].add(r[1])
t("tri: F com 2 arranjos essenciais, V e E com 1 (diagrama do EnIMaR)",
  len(a['F']) == 4 and len(a['V']) == 2 and len(a['E']) == 2)
gens = []
for k, S in a.items():
    L = sorted(S)
    for i in range(len(L)):
        for j in range(len(L)):
            if i != j: gens += Flex(*F.mapa_retorno(L[i], L[j])).gamma_gens()
st = gamma_structure(_G(gens))
t("tri: Gamma de posto 1, |P| = 1", st["rank"] == 1 and st["P"] == 1)

# ------------------------------------------------- hexaflexagonos (rotflex)
import rotflex as R
for N, esperado in ((10, 1), (19, 3)):
    est2, aps = R.A.aparencias(N)
    pf = defaultdict(list)
    for idx, S, ar in aps: pf[S].append((idx, ar))
    fl = set()
    for S, lst in pf.items():
        if len(lst) < 2: continue
        for i in range(len(lst)):
            for j in range(len(lst)):
                if i != j:
                    m = R.A.retorno(lst[i][1], lst[j][1])
                    if m != (tuple(range(6)), (0,)*6): fl.add(m)
    rot = {m for m in fl if R.e_rotacao(*m)}
    stt = R.A.gamma(rot) if rot else dict(rank=0, P=1)
    t(f"hexaflexagono N={N}: Gamma finito de ordem {esperado}",
      stt["rank"] == 0 and stt["P"] == esperado)

print()
print(f"  {sum(ok)}/{len(ok)} testes passaram")

# ===================================================== caracterizacao combinatoria
print()
print("=" * 74); print(" VERIFICACAO -- caracterizacao combinatoria (paridade.py)")
print("=" * 74)
import paridade as PD
from collections import defaultdict as _dd
_real = _dd(set)
for _g in P.dobraduras():
    for _o in P.ordens_validas(_g):
        _r = P.exibida(_g, _o)
        if not _r: continue
        _rot = [q[1] for q in _r[1]]
        _real[_r[0]].add(tuple((x - _rot[0]) % 4 for x in _rot))
_prev = _dd(set)
for _u in PD.validas():
    for _k in range(1, 7):
        if PD.exibivel(_u, _k): _prev[_k].add(PD.assinatura(_u, _k))
t("25 coordenadas u = (u1,u2,u3,u4) de 81", len(PD.validas()) == 25)
t("uma unica charneira solta por bloco em todas as dobraduras",
  all(len(u) == 4 for u in PD.validas()))
t("as assinaturas previstas SO por u coincidem com as 216768 exaustivas",
  all(_real[k] == _prev[k] for k in _real))
t("faces 3-6: assinatura unica (logo eps constante, automaticamente)",
  all(len(_prev[k]) == 1 for k in (3, 4, 5, 6)))
t("faces 1 e 2: duas assinaturas, exibiveis so na diagonal u1 = u3",
  all(len(_prev[k]) == 2 for k in (1, 2))
  and all(u[0] == u[2] for u in PD.validas() if PD.exibivel(u, 1)))
t("a assinatura excepcional da face 1 vive so em u1 = u3 = 2",
  {(u[0], u[2]) for u in PD.validas()
   if PD.exibivel(u, 1) and PD.assinatura(u, 1) == (0, 0, 0, 0)} == {(2, 2)})
print()
print(f"  {sum(ok)}/{len(ok)} testes passaram (total)")

# ================================================ a regra dos extremos
print()
print("=" * 74); print(" VERIFICACAO -- a regra dos extremos"); print("=" * 74)
def _coord(pil):
    _pos = {}
    for c, cs in pil:
        for i in cs: _pos[i] = c
    _b = [1 if _pos[i] == _pos[(i+1) % 12] else 0 for i in range(12)]
    _u = []
    for R in PD.RUNS:
        z = [h for h in R if _b[h] == 0]
        if len(z) != 1: return None
        _u.append(R.index(z[0]))
    return tuple(_u)


def _indices(pil):
    """posicao (0 = primeira, 1 = meio, 2 = ultima) da folha de topo dentro do
       seu arco, para os quatro pats em ordem ciclica."""
    _pos = {}
    for c, cs in pil:
        for i in cs: _pos[i] = c
    soltas = [h for h in range(12) if _pos[h] != _pos[(h+1) % 12]]
    if len(soltas) != 4: return None
    d = dict(pil); out = []
    for a in range(4):
        i = (soltas[a] + 1) % 12; fim = soltas[(a+1) % 4]; arc = []
        while True:
            arc.append(i)
            if i == fim: break
            i = (i + 1) % 12
        out.append(arc.index(d[_pos[arc[0]]][-1]))
    return tuple(out)


_ALL = set()
for _g in P.dobraduras():
    for _o in P.ordens_validas(_g): _ALL |= set(P.imagens((_g, _o)))
t("216768 estados dobrados, orbita contida neles",
  len(_ALL) == 216768 and orb <= _ALL)
_ext = {}
for _u0 in ((0, 0, 0, 0), (1, 1, 1, 1), (2, 2, 2, 2)):
    _A = {_indices(e[1]) for e in _ALL if _coord(e[1]) == _u0}
    _O = {_indices(e[1]) for e in orb if _coord(e[1]) == _u0}
    _ext[_u0] = (_A, _O)
t("nas tres coordenadas simetricas existem os 81 padroes de topo",
  all(len(a) == 81 for a, _ in _ext.values()))
t("em u=(1,1,1,1) (charneiras soltas ao meio) a flexao alcanca os 81",
  len(_ext[(1, 1, 1, 1)][1]) == 81)
t("em u=(2,2,2,2) alcanca 8: ULTIMA folha no topo em dois pats OPOSTOS",
  len(_ext[(2, 2, 2, 2)][1]) == 8
  and all(tuple(1 if x == 2 else 0 for x in p_) in ((1, 0, 1, 0), (0, 1, 0, 1))
          for p_ in _ext[(2, 2, 2, 2)][1]))
t("em u=(0,0,0,0) alcanca 8: PRIMEIRA folha no topo em dois pats OPOSTOS",
  len(_ext[(0, 0, 0, 0)][1]) == 8
  and all(tuple(1 if x == 0 else 0 for x in p_) in ((1, 0, 1, 0), (0, 1, 0, 1))
          for p_ in _ext[(0, 0, 0, 0)][1]))
_fu = _dd(set)
for e in orb:
    _r = P.exibida(*e)
    if _r: _fu[_r[0]].add(_coord(e[1]))
t("a face 1 nunca e exibida em u=(2,2,2,2) (precisaria das quatro ultimas)",
  (2, 2, 2, 2) not in _fu[1] and PD.assinatura((2, 2, 2, 2), 1) == (0, 0, 0, 0))
t("a face 2 nunca e exibida em u=(0,0,0,0) (o enunciado espelhado)",
  (0, 0, 0, 0) not in _fu[2] and PD.assinatura((0, 0, 0, 0), 2) == (0, 0, 0, 0))
t("logo cada face so aparece com UMA assinatura -> |P| = 1",
  all(len({PD.assinatura(u_, k) for u_ in _fu[k]}) == 1 for k in _fu))
print()
print(f"  {sum(ok)}/{len(ok)} testes passaram (total)")

# ============================================ as componentes do grafo de flexao
print()
print("=" * 74); print(" VERIFICACAO -- o grafo de flexao e DESCONEXO"); print("=" * 74)
_alvo = None
for _g in P.dobraduras():
    for _o in P.ordens_validas(_g):
        for _e in P.imagens((_g, _o)):
            _r = P.exibida(*_e)
            if _r and _r[0] == 1 and _coord(_e[1]) == (2, 2, 2, 2): _alvo = _e; break
        if _alvo: break
    if _alvo: break
t("existe estado dobrado que exibe o arranjo excepcional da face 1", _alvo is not None)
import flexcamadas as _FC
_comp, _fila = _FC.orbita_fixa(P, [_alvo], segundos=25)
t("a sua componente e minuscula (20 estados) e esta completa",
  len(_comp) == 20 and not _fila)
t("e disjunta da componente do flexagono montado (19200 estados)",
  not (_comp & orb) and len(orb) == 19200)
_fc = {P.exibida(*e)[0] for e in _comp if P.exibida(*e)}
t("nessa componente so a face 1 se exibe, e so em u=(2,2,2,2)",
  _fc == {1} and all(_coord(e[1]) == (2, 2, 2, 2)
                     for e in _comp if P.exibida(*e)))
print()
print(f"  {sum(ok)}/{len(ok)} testes passaram (total)")

# ================================ a decomposicao COMPLETA em componentes
print()
print("=" * 74); print(" VERIFICACAO -- classificacao completa das componentes")
print("=" * 74)
import pickle as _pk
_resto, _tam = _pk.load(open("../saidas/componentes.pkl", "rb"))
t("a decomposicao esta completa (0 estados por fechar)", len(_resto) == 0)
t("os tamanhos somam os 216768 estados",
  sum(k*v for k, v in _tam.items()) == 216768)
t("ha exatamente 20405 componentes", sum(_tam.values()) == 20405)
t("uma so ilha, de 19200 estados", _tam[19200] == 1 and max(_tam) == 19200)
t("a maior das outras tem 200 estados", sorted(_tam)[-2] == 200)
t("todos os tamanhos sao multiplos de 4", all(k % 4 == 0 for k in _tam))
t("CRITERIO: componente com mais de 200 estados <=> e o flexagono",
  all(k <= 200 for k in _tam if k != 19200))
print()
print(f"  {sum(ok)}/{len(ok)} testes passaram (total)")
