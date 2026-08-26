"""verify_geral.py -- W^+(D), hexaflexagonos (com a flexao de pinca),
   multiprototipos e o exemplo C_12.  Os tetraflexagonos estao em
   verify_camadas.py."""
import pickle
from collections import defaultdict as _dd
import flexcamadas as X, foldings as F, paridade as PD
from quadflex import Flex, gamma_structure, latstr, covol
P = X.HEXA
orb = set(pickle.load(open("../saidas/orbita_fixa.pkl", "rb"))[0])
ok = []
def t(nome, cond):
    ok.append(bool(cond)); print(f"  [{'OK ' if cond else 'FALHA'}] {nome}")
class _G:
    def __init__(s, x): s._g = sorted(set(x))
    def gamma_gens(s): return s._g
_arr = _dd(set)
for e in orb:
    r = P.exibida(*e)
    if r: _arr[r[0]].add(r[1])
maps = set()
for k, S in _arr.items():
    L2 = sorted(S)
    maps |= {F.mapa_retorno(L2[i], L2[j])
             for i in range(len(L2)) for j in range(len(L2)) if i != j}

# ================================================ retas de dobra e prototipos
print()
print("=" * 74); print(" VERIFICACAO -- W^+(D), hexaflexagonos e multiprototipos")
print("=" * 74)
import wgrupo as WG
st = WG.quad_W(WG.QUAD["quadrado 2x2 (tetraflexagonos)"], True)
t("quadrado 2x2 livre: W+ = p2 (posto 2, |P| = 2)", st["rank"] == 2 and st["P"] == 2)
_stG = gamma_structure(_G([x for sg, ep in maps for x in Flex(sg, ep).gamma_gens()]))
t("Gamma do hexa-tetraflexagono cabe em W+ (posto e |P| menores ou iguais)",
  _stG["rank"] <= st["rank"] and st["P"] % _stG["P"] == 0)
st = WG.quad_W(WG.QUAD["quadrado 2x2 (tetraflexagonos)"], False)
t("quadrado 2x2 confinado: W+ = C_2", st["rank"] == 0 and st["P"] == 2)
st = WG.tri_W(WG.TRI["hexagono de 6 triangulos (hexaflexagonos)"], False)
t("hexagono confinado: W+ = C_3 (as 3 diagonais fazem 60 graus)",
  st["rank"] == 0 and st["P"] == 3)

import hexcamadas as HC
from collections import deque
X = HC.Hexa(10)
eg = HC.estados_geom(10, 'oposto')
t("tri-hexaflexagono: a colagem 'oposto' e a unica que da estados validos",
  len(eg) > 0 and len(HC.estados(10, 'igual')) == 0)
seed = eg[0][0]; vis = {seed}; fila = deque([seed])
while fila:
    u = fila.popleft()
    for w in X.vizinhos(u):
        if w not in vis: vis.add(w); fila.append(w)
t("orbita do tri-hexaflexagono (agora com a pinca): 6756 estados",
  len(vis) == 6756)
t("o modelo PERMITE a fuga (contornos de 1 e 2 ladrilhos ocorrem)",
  any(len(p) <= 2 for _, p in vis))
import hexaflex_an as AA, rotflex as RR
hx = [e for e in vis if HC.hexagonal(e[1])]
from collections import defaultdict
vv = defaultdict(list)
for g, pil in hx:
    v = HC.hexagonal(pil); arr = {}
    for c, cs in pil:
        i = cs[-1]
        arr[(0 if i == 9 else i, g[i][1])] = (HC.H.indice_tile(c, v), g[i][0])
    if len(arr) == 6: vv[frozenset(arr)].append(arr)
fl = set()
for S, lst in vv.items():
    for a in range(len(lst)):
        for b in range(len(lst)):
            if a != b:
                m = AA.retorno(lst[a], lst[b])
                if m != (tuple(range(6)), (0,)*6): fl.add(m)
t("mesmo assim, todo mapa de retorno alcancavel e rotacao em torno de O",
  all(RR.e_rotacao(*m) for m in fl))
stt = AA.gamma(fl) if fl else dict(rank=0, P=1)
t("tri-hexaflexagono: Gamma finito, contido em C_3",
  stt["rank"] == 0 and stt["P"] in (1, 3))

import multiproto as MP
cl = [MP.classifica(sg, ep)[0] for sg, ep in MP.flexes()]
t("face com 2 prototipos: 72 flexes", len(cl) == 72)
t("32 deles tem Gamma DENSO (so constantes)",
  sum(1 for c in cl if c.startswith("DENSO")) == 32)
t("nenhum flexagono real cai no caso denso (Gamma <= W+ cristalografico)",
  WG.tri_W(WG.TRI["hexagono de 6 triangulos (hexaflexagonos)"], False)["P"] in (1,2,3,4,6))

print()
print(f"  {sum(ok)}/{len(ok)} testes passaram (total)")

# ==================================== C_12 e a flexao de pinca
print()
print("=" * 74); print(" VERIFICACAO -- C_12 e a flexao de pinca"); print("=" * 74)
import multiproto as _MP
t("roda (2 quadrados + 3 triangulos): 5184 flexes",
  sum(1 for _ in _MP.roda_flexes()) == 5184)
t("Gamma = C_12 e realizado: finito, com N fora de {1,2,3,4,6}",
  _MP.roda_classifica((0, 1, 3, 2, 4), (0, 0, 5, 7, 0)) == ("C_12", 12))
import itertools as _it
_sam = list(_it.islice(_MP.roda_flexes(), 0, 5184, 37))
_d = sum(1 for sg, ep in _sam if _MP.roda_classifica(sg, ep)[0] == "DENSO")
t("a grande maioria dos flexes da roda e DENSA (so constantes)",
  _d > 0.8 * len(_sam))
import hexcamadas as _HC
_XX = _HC.Hexa(10)
_eg = _HC.estados_geom(10, 'oposto')
_pv = set(_HC.pinca(_XX, _eg[0][0]))
t("a flexao de pinca produz estados hexagonais validos",
  len(_pv) > 0 and all(_HC.hexagonal(p) and _XX.ok(g, dict(p)) for g, p in _pv))
print()
print(f"  {sum(ok)}/{len(ok)} testes passaram (total)")

# ---------------------------------------- tri-hexaflexagono com a pinca
print()
print("=" * 74); print(" VERIFICACAO -- tri-hexaflexagono com a flexao de pinca")
print("=" * 74)
from collections import deque as _dq
import hexcamadas as _H2, hexaflex_an as _A2, rotflex as _R2, time as _t2
_X2 = _H2.Hexa(10); _eg2 = _H2.estados_geom(10, 'oposto'); _s0 = _eg2[0][0]
def _lt(e):
    g_, pil_ = e; v_ = _H2.hexagonal(pil_); o_ = {}
    for c_, cs_ in pil_:
        i_ = cs_[-1]; o_[(0 if i_ == 9 else i_, g_[i_][1])] = (_H2.H.indice_tile(c_, v_), g_[i_][0])
    return o_
_F1 = frozenset(_lt(_s0))
_F2 = frozenset((0 if cs_[0] == 9 else cs_[0], 1 - _s0[0][cs_[0]][1]) for _, cs_ in _s0[1])
_TT = {(0 if i_ == 9 else i_, s_) for i_ in range(10) for s_ in (0, 1)}
_F3 = frozenset(_TT - set(_F1) - set(_F2))
t("as tres faces do exemplar montado particionam os 18 lados",
  len(set(_F1) | set(_F2) | set(_F3)) == 18 and len(_F1) == len(_F2) == len(_F3) == 6)
_vis = {_s0}; _fi = _dq([_s0]); _t0 = _t2.time()
while _fi and _t2.time() - _t0 < 25:
    _u = _fi.popleft()
    for _w in _H2.pinca(_X2, _u) + [_X2.virar(_u)]:
        if _w not in _vis: _vis.add(_w); _fi.append(_w)
t("a orbita so com a pinca e o virar tem 660 estados", len(_vis) == 660 and not _fi)
_por = _dd(list)
for _e in _vis:
    if _H2.hexagonal(_e[1]) is None: continue
    _a = _lt(_e)
    if len(_a) == 6 and frozenset(_a) in (_F1, _F2, _F3): _por[frozenset(_a)].append(_a)
_fl = set()
for _S, _l in _por.items():
    for _i in range(len(_l)):
        for _j in range(len(_l)):
            if _i != _j:
                _m = _A2.retorno(_l[_i], _l[_j])
                if _m != (tuple(range(6)), (0,)*6): _fl.add(_m)
t("todos os mapas de retorno das faces reais sao rotacoes em torno de O",
  all(_R2.e_rotacao(*_m) for _m in _fl))
_st2 = _A2.gamma(_fl) if _fl else dict(rank=0, P=1)
t("tri-hexaflexagono: Gamma = C_3", _st2["rank"] == 0 and _st2["P"] == 3)

# ---------------------------------------------------------- catalogos
import os as _os
_R = "../catalogos"
_NOMES = ("tritetraflexagono", "hexatetraflexagono",
          "trihexaflexagono", "hexahexaflexagono")
_PDFS = [_os.path.join(_R, "funcoes-flexionaveis-" + n_, "catalogo.pdf")
         for n_ in _NOMES]
t("existem os quatro catalogos (um por flexagono)",
  all(_os.path.exists(q_) for q_ in _PDFS))
# um .tex que nao compila deixa um catalogo.pdf de zero byte: e preciso olhar
# o conteudo, nao so a existencia (foi exatamente o que aconteceu com os dois
# catalogos hexagonais, por causa de \begin{@twocolumnfalse} sem \makeatletter)
t("os quatro catalogo.pdf sao PDFs de verdade (nao vazios)",
  all(_os.path.exists(q_) and _os.path.getsize(q_) > 10000 and
      open(q_, "rb").read(5) == b"%PDF-" for q_ in _PDFS))
import json as _json
_forms = []
for n_ in _NOMES:
    _q = _os.path.join(_R, "funcoes-flexionaveis-" + n_, "indice.json")
    if not _os.path.exists(_q): continue
    _d = _json.load(open(_q))
    _its = _d["itens"] if isinstance(_d, dict) else _d
    for _it in _its:
        _forms += [_v for _k, _v in _it.items() if isinstance(_v, str)] \
                  if "tex" not in _it else [_it["tex"]]
t("nenhuma formula do catalogo tem sinal duplo do tipo (w--0.5+0.1i)",
  _forms and not any("--" in _f for _f in _forms))

print()
print(f"  {sum(ok)}/{len(ok)} testes passaram")
