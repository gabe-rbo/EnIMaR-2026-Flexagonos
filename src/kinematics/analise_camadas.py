"""
analise_camadas.py
==================
Resposta a pergunta (a): que arranjos de cada face sao FISICAMENTE
alcancaveis, e que grupo de discrepancia resulta.

Tudo e lido num REFERENCIAL FIXO do plano: os arranjos comparados sao os de
estados que existem de facto na orbita, e nao imagens do mesmo estado lidas
em referenciais rodados (isso conjugaria Gamma por rotacoes de 90 graus e
inflacionaria o grupo).  A orbita e fechada por {id, meia-volta, os dois
espelhos}, mas NAO por rotacoes de um quarto de volta --- um tetraflexagono
nunca volta rodado 90 graus.
"""
import pickle, io, os
from collections import defaultdict
import flexcamadas as X
import foldings as F
from quadflex import Flex, gamma_structure, label, latstr

NOME = {0: '1', 1: 'i', 2: '-1', 3: '-i'}


class _G:
    def __init__(s, x): s._g = sorted(set(x))
    def gamma_gens(s): return s._g


def arranjos(P, estados):
    out = defaultdict(set)
    for e in estados:
        r = P.exibida(*e)
        if r: out[r[0]].add(r[1])
    return out


def grupo(arr):
    gens = []; maps = defaultdict(set)
    for k, S in arr.items():
        L = sorted(S)
        for i in range(len(L)):
            for j in range(len(L)):
                if i != j:
                    m = F.mapa_retorno(L[i], L[j]); maps[k].add(m)
                    gens += Flex(*m).gamma_gens()
    return gamma_structure(_G(gens)), maps


def todos_estados(P):
    out = []
    for g in P.dobraduras():
        for o in P.ordens_validas(g): out.append(P.normaliza(g, o))
    # fechar pelas simetrias globais para ter o espaco completo
    tot = set()
    for e in out: tot |= set(P.imagens(e))
    return sorted(tot)


def componentes(P, estados, livre=False):
    rest = set(estados); comps = []
    while rest:
        s = next(iter(rest))
        vis, _ = X.orbita_fixa(P, [s], livre)
        comps.append(vis & set(estados)); rest -= vis
    return sorted(comps, key=len, reverse=True)


if __name__ == "__main__":
    buf = io.StringIO()
    def Pr(*a): print(*a); print(*a, file=buf)

    # ------------------------------------------------------------ hexa
    P = X.HEXA
    Pr("=" * 74)
    Pr(" HEXA-TETRAFLEXAGONO -- alcancabilidade no modelo com camadas")
    Pr("=" * 74)
    tot = todos_estados(P)
    orb = pickle.load(open("../saidas/orbita_fixa.pkl", "rb"))[0]
    liv = pickle.load(open("../saidas/orbita_livre.pkl", "rb"))[0]
    livf = set()
    for e in liv: livf |= set(P.imagens(e))
    aT, aO, aL = arranjos(P, tot), arranjos(P, orb), arranjos(P, livf)
    Pr(f"  estados dobrados validos (referencial fixo): {len(tot)}")
    Pr(f"  orbita do estado montado pelo flex:          {len(orb)}")
    Pr("")
    Pr(f"  {'face':>6} {'combinatorio':>13} {'FLEX':>6} {'majorante livre':>16}")
    for k in sorted(aT):
        Pr(f"  {k:>6} {len(aT[k]):>13} {len(aO.get(k,())):>6} {len(aL.get(k,())):>16}")
    for nome, a in (("combinatorio (todos os estados)", aT),
                    ("FLEX (modelo com camadas)", aO),
                    ("majorante de abertura livre", aL)):
        st, mp = grupo(a)
        eps = {e for k in mp for _, e in mp[k]}
        Pr("")
        Pr(f"  {nome}:")
        Pr(f"     {label(st).strip()}")
        Pr(f"     Lambda = {latstr(st['lattice'])}   |P| = {st['P']}   posto = {st['rank']}")
        Pr(f"     todos os eps constantes? {all(len(set(e)) == 1 for e in eps)}")

    # ------------------------------------------------------------- tri
    T = X.TRI
    Pr("")
    Pr("=" * 74)
    Pr(" TRI-TETRAFLEXAGONO -- alcancabilidade no modelo com camadas")
    Pr("=" * 74)
    tt = todos_estados(T)
    Pr(f"  estados dobrados validos: {len(tt)}")
    comps = componentes(T, tt)
    Pr(f"  componentes do grafo de flexao: {[len(c) for c in comps]}")
    for i, c in enumerate(comps):
        a = arranjos(T, c)
        if not a: continue
        st, _ = grupo(a)
        Pr(f"     comp {i} ({len(c)} estados): faces "
           f"{ {k: len(v) for k, v in sorted(a.items())} }   {label(st).strip()}"
           f"   Lambda = {latstr(st['lattice'])}  |P| = {st['P']}")
    princ = [c for c in comps if len(arranjos(T, c)) == 3]
    Pr("")
    if princ:
        a = arranjos(T, princ[0]); st, mp = grupo(a)
        Pr("  COMPONENTE DO FLEXAGONO (exibe as tres faces):")
        Pr(f"     arranjos: { {k: len(v) for k, v in sorted(a.items())} }")
        Pr(f"     {label(st).strip()}")
        Pr(f"     Lambda = {latstr(st['lattice'])}   |P| = {st['P']}   posto = {st['rank']}")
        eps = {e for k in mp for _, e in mp[k]}
        Pr(f"     todos os eps constantes? {all(len(set(e)) == 1 for e in eps)}")
    open("../saidas/camadas.txt", "w").write(buf.getvalue())
