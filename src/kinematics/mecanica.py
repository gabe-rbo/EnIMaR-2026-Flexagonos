"""
mecanica.py
===========
A *mecanica* dos dois flexagonos: quais arranjos de cada face sao efetivamente
exibidos, os mapas de retorno que dai resultam, e o diagrama de flexao.

Convencao de letras (a mesma do diagrama do artigo do EnIMaR):

        a | b            e a numeracao cartesiana dos quadrantes:
        --+--                   2 | 1
        c | d                   --+--
                                3 | 4
    logo   a = Q2 ,  b = Q1 ,  c = Q3 ,  d = Q4 .

Um *arranjo* de uma face e a palavra de 4 letras que se le no diagrama:
"abcd" e o arranjo de referencia, "badc" a troca esquerda-direita,
"cdab" a troca cima-baixo, "dcba" a diagonal.

Fontes:
  * hexa-tetraflexagono: diagrama de flexao do artigo do EnIMaR (transcrito
    abaixo);  confirmado pela enumeracao exata de foldings.py, que produz
    esses arranjos entre as suas dobraduras planas.
  * tri-tetraflexagono: enumeracao exata de foldings_tri.py.
"""
from quadflex import Flex, gamma_structure, label, latstr, covol

LETRA_Q = {'a': 2, 'b': 1, 'c': 3, 'd': 4}
Q_LETRA = {v: k for k, v in LETRA_Q.items()}
POS_LETRA = ['a', 'b', 'c', 'd']          # posicoes na ordem TL, TR, BL, BR


def arranjo_para_mapa(w):
    """peca -> quadrante cartesiano que ela ocupa."""
    return {peca: LETRA_Q[POS_LETRA[i]] for i, peca in enumerate(w)}


def retorno(w1, w2):
    m1 = arranjo_para_mapa(w1); m2 = arranjo_para_mapa(w2)
    sigma = {m1[p]: m2[p] for p in 'abcd'}
    return Flex(tuple(sigma[q] for q in (1, 2, 3, 4)), (0, 0, 0, 0))


class _G:
    def __init__(s, g): s._g = sorted(set(g))
    def gamma_gens(s): return s._g


def flexes(spec):
    out = []
    for k, ws in spec["arranjos"].items():
        for i in range(len(ws)):
            for j in range(len(ws)):
                if i != j: out.append(retorno(ws[i], ws[j]))
    return out


def grupo(spec):
    gens = []
    for Phi in flexes(spec): gens += Phi.gamma_gens()
    return gamma_structure(_G(gens))


# ===========================================================================
#  HEXA-TETRAFLEXAGONO  (6 faces)
# ===========================================================================
HEXA = {
    "nome": "hexatetraflexagono",
    "titulo": "hexa-tetraflex\\'agono (6 faces)",
    "faces": [1, 2, 3, 4, 5, 6],
    "arranjos": {
        1: ["abcd", "badc", "cdab"],
        2: ["abcd", "badc", "cdab"],
        3: ["abcd", "badc"],
        6: ["abcd", "badc"],
        4: ["abcd", "cdab"],
        5: ["abcd", "cdab"],
    },
    # (x, y) em unidades de caixa; 's' cheia, 'd' tracejada
    # grade: coluna * 1.45 , linha * 1.55   (mesma disposicao do diagrama
    # do artigo do EnIMaR)
    "nos": {
        "3:abcd": (2*1.45, 2*1.55, 's'), "1:cdab": (3*1.45, 2*1.55, 'd'),
        "4:abcd": (4*1.45, 2*1.55, 's'), "3:badc": (5*1.45, 2*1.55, 'd'),
        "5:abcd": (0*1.45, 1*1.55, 's'), "1:badc": (1*1.45, 1*1.55, 'd'),
        "1:abcd": (2*1.45, 1*1.55, 's'), "2:abcd": (3*1.45, 1*1.55, 'd'),
        "2:badc": (4*1.45, 1*1.55, 's'), "4:cdab": (5*1.45, 1*1.55, 'd'),
        "6:abcd": (0*1.45, 0*1.55, 's'), "5:cdab": (1*1.45, 0*1.55, 'd'),
        "2:cdab": (2*1.45, 0*1.55, 's'), "6:badc": (3*1.45, 0*1.55, 'd'),
    },
    "arestas": [
        ("1:abcd", "3:abcd", 's', False),
        ("2:cdab", "1:abcd", 's', False),
        ("1:abcd", "1:badc", 'b', False),
        ("1:cdab", "4:abcd", 'b', True),
        ("1:cdab", "2:abcd", 'd', False),
        ("2:badc", "2:abcd", 'b', False),
        ("4:abcd", "2:badc", 's', False),
        ("4:cdab", "3:badc", 'd', True),
        ("2:abcd", "6:badc", 'd', False),
        ("5:abcd", "6:abcd", 's', False),
        ("5:cdab", "1:badc", 'd', False),
        ("5:cdab", "2:cdab", 'b', True),
    ],
}

# ===========================================================================
#  TRI-TETRAFLEXAGONO  (3 faces: F = frente, V = verso, E = escondida)
# ===========================================================================
TRI = {
    "nome": "tritetraflexagono",
    "titulo": "tri-tetraflex\\'agono (3 faces)",
    "faces": ["F", "V", "E"],
    "arranjos": {"F": ["abcd", "badc"], "V": ["abcd"], "E": ["abcd"]},
    "nos": {
        "F:abcd": (0.0, 0.0, 's'), "V:abcd": (1.45, 0.0, 'd'),
        "E:abcd": (2.90, 0.0, 's'), "F:badc": (4.35, 0.0, 'd'),
    },
    "arestas": [
        ("F:abcd", "V:abcd", 'b', False),
        ("V:abcd", "E:abcd", 'b', False),
        ("E:abcd", "F:badc", 'b', False),
    ],
}

SPECS = {"hexa": HEXA, "tri": TRI}


if __name__ == "__main__":
    for chave, spec in SPECS.items():
        print("=" * 74)
        print(f" {chave.upper()} -- {spec['nome']}")
        print("=" * 74)
        for k in spec["faces"]:
            ws = spec["arranjos"][k]
            print(f"  face {k}: arranjos {ws}")
            for i in range(len(ws)):
                for j in range(i+1, len(ws)):
                    Phi = retorno(ws[i], ws[j]); st = gamma_structure(Phi)
                    print(f"      {ws[i]} -> {ws[j]}: sigma={Phi.sigma}  "
                          f"posto={st['rank']} Lambda={latstr(st['lattice'])}")
            stk = grupo({"arranjos": {k: ws}})
            print(f"      Gamma da face: {label(stk)}  "
                  f"Lambda={latstr(stk['lattice'])}")
        st = grupo(spec)
        print(f"\n  GRUPO CONJUNTO: {label(st)}")
        print(f"    Lambda = {latstr(st['lattice'])}"
              + (f"  covol={covol(st['lattice'])}" if st['rank'] == 2 else "")
              + f"   |P| = {st['P']}\n")
