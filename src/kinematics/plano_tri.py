"""
plano_tri.py -- confronto entre a Figura A.1 do manual e o plano gerado por
`tritetraflexagonos.py`.

A Figura A.1 e o modelo IMPRESSO do flexagono de 3 faces: duas metades numa
folha, com uma linha de dobra vertical.  Extraida pixel a pixel, ela e um
OCTOMINO (8 celulas por metade), nao um hexomino: alem dos 6 quadradinhos com
figura ha quadradinhos BRANCOS, que sao as abas de cola mencionadas no roteiro
de montagem ("cole a face do quadrado branco, a qual deve estar encarando
outro").
"""

# ---- Figura A.1 (extraida de Manual_Flexas.pdf, p.21), grade 5 linhas x 4 col.
#      X = quadradinho com figura ; W = quadradinho branco (aba) ; . = vazio
A1 = ["..X.W.",   # placeholder substituido abaixo
      ]
A1 = [
    ['.', 'X', 'W', '.'],
    ['.', 'X', 'X', '.'],
    ['X', 'X', 'X', 'X'],
    ['X', 'W', 'W', 'X'],
    ['X', 'W', 'X', 'X'],
]
DOBRA_COL = 2          # linha de dobra vertical entre as colunas 1 e 2

def metades():
    esq = {(r, c): A1[r][c] for r in range(5) for c in range(2) if A1[r][c] != '.'}
    dir_ = {(r, c): A1[r][c] for r in range(5) for c in range(2, 4) if A1[r][c] != '.'}
    # dobrar a metade direita sobre a esquerda: c -> 3 - c
    dir_dobrada = {(r, 3 - c): v for (r, c), v in dir_.items()}
    return esq, dir_dobrada


# ---- plano gerado pelo codigo (grade 2 linhas x 5 colunas) -------------------
# posicoes de colagem lidas de tritetraflexagonos.py
FRENTE_CODIGO = {(0, 0): 'E2', (0, 1): 'E1', (0, 2): 'F2',
                 (1, 2): 'F3', (1, 3): 'V3', (1, 4): 'V4'}
TRASEIRO_CODIGO = {(0, 2): 'E4', (0, 3): 'E3', (0, 4): 'F4',
                   (1, 1): 'V1', (1, 2): 'V2', (1, 4): 'F1'}


def rot90_ccw_5x2_para_2x5(cells):
    """A.1 usa 5 linhas x 2 colunas; o codigo usa 2 linhas x 5 colunas.
       (r,c) -> (1-c, r)"""
    return {(1 - c, r): v for (r, c), v in cells.items()}


if __name__ == "__main__":
    esq, dirf = metades()
    print("Figura A.1, metade ESQUERDA (5x2):")
    for r in range(5):
        print("   " + " ".join(esq.get((r, c), '.') for c in range(2)))
    print("Figura A.1, metade DIREITA dobrada sobre a esquerda:")
    for r in range(5):
        print("   " + " ".join(dirf.get((r, c), '.') for c in range(2)))

    print("\nas duas metades ocupam as MESMAS celulas?",
          set(esq) == set(dirf), " -> ", len(esq), "celulas cada")
    print("pares (frente/verso) de cada quadradinho:")
    for k in sorted(esq):
        print(f"   {k}:  {esq[k]} / {dirf[k]}")
    nb = sum(1 for k in esq if esq[k] == 'W') + sum(1 for k in dirf if dirf[k] == 'W')
    print(f"\nlados com figura = {2*len(esq) - nb}   (necessarios: 3 faces x 4 = 12)")

    print("\n--- confronto com o codigo -------------------------------------")
    ce = rot90_ccw_5x2_para_2x5(esq)
    dir_bruta = {(r, c - 2): A1[r][c] for r in range(5)
                 for c in range(2, 4) if A1[r][c] != '.'}
    cd = rot90_ccw_5x2_para_2x5(dir_bruta)
    print("A.1 metade esquerda girada 90 ccw  (2x5):")
    for r in range(2):
        print("   " + " ".join(ce.get((r, c), '.') for c in range(5)))
    print("plano FRONTAL do codigo (X onde ha figura):")
    for r in range(2):
        print("   " + " ".join('X' if (r, c) in FRENTE_CODIGO else '.' for c in range(5)))
    ok1 = {k for k, v in ce.items() if v == 'X'} == set(FRENTE_CODIGO)
    print("   coincide?", ok1)

    print("A.1 metade direita girada 90 ccw   (2x5):")
    for r in range(2):
        print("   " + " ".join(cd.get((r, c), '.') for c in range(5)))
    print("plano TRASEIRO do codigo:")
    for r in range(2):
        print("   " + " ".join('X' if (r, c) in TRASEIRO_CODIGO else '.' for c in range(5)))
    ok2 = {k for k, v in cd.items() if v == 'X'} == set(TRASEIRO_CODIGO)
    print("   coincide?", ok2)

    print("\nCONCLUSAO:", "o codigo reproduz exatamente o modelo publicado."
          if (ok1 and ok2) else "ha divergencia.")
