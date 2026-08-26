"""
catalogo_hex.py
===============
Catalogo das funcoes flexionaveis dos HEXAFLEXAGONOS.

Pelo Teorema das retas de dobra, Gamma <= C_3 para qualquer hexaflexagono, e
nos dois classicos Gamma = C_3: as solucoes sao exatamente

        f(z) = h( ((z - O)/r)^3 ),      h meromorfa,

com O o centro do hexagono.  Sao portanto muito mais faceis de gerar do que as
elipticas dos tetraflexagonos --- e ha solucoes INTEIRAS.

Cada item do catalogo traz:
  * hexagono.png   -- o retrato de fase da face inteira;
  * tileK.png      -- os seis triangulos recortados (entrada do gerador de
                      planos), cada um no seu proprio referencial;
  * formula.tex / formula.txt
e o conjunto e montado num catalogo.pdf de duas colunas.
"""
import os, sys, json, math, subprocess
import numpy as np
from PIL import Image
from gerador import retrato

W6 = [complex(math.cos(k*math.pi/3), math.sin(k*math.pi/3)) for k in range(6)]

TITULOS = {"trihexaflexagono":  r"tri-hexaflex\'agono (3 faces)",
           "hexahexaflexagono": r"hexa-hexaflex\'agono (6 faces)"}


def fmt(c):
    """o numero complexo c, como coeficiente."""
    return r"%.2f%+.2fi" % (c.real, c.imag)


def fmt_sub(a):
    """(w - a) com os sinais ja distribuidos: a = -0.56+0.17i  ->  '+0.56-0.17i'.

    Sem isto sai '(w--0.56+0.17i)', que e correto mas ilegivel.  O '+0.0'
    normaliza o zero negativo, para nao imprimir '-0.00'.
    """
    return r"%+.2f%+.2fi" % (-a.real + 0.0, -a.imag + 0.0)


def familia(rng, grau=2):
    """h racional aleatoria; f(z) = h(((z-O)/r)^3) com O = 0 e r = 1."""
    zer = [complex(rng.normal(0, .7), rng.normal(0, .7)) for _ in range(grau)]
    pol = [complex(rng.normal(0, .7), rng.normal(0, .7)) for _ in range(grau)]
    c = complex(rng.normal(0, 1), rng.normal(0, 1))

    def f(z):
        w = np.asarray(z, dtype=complex)**3
        num = np.ones_like(w); den = np.ones_like(w)
        for a in zer: num = num*(w - a)
        for b in pol: den = den*(w - b)
        return c*num/den
    tex = (r"f(z)=%s\,\dfrac{%s}{%s}\quad\text{com } w=z^{3}"
           % (fmt(c), "".join(r"(w%s)" % fmt_sub(a) for a in zer),
              "".join(r"(w%s)" % fmt_sub(b) for b in pol)))
    return f, tex


def dentro_hexagono(Z):
    """|Re(z w^-k)| <= sqrt(3)/2 para as tres direcoes: o hexagono regular."""
    m = np.ones(Z.shape, bool)
    for k in range(3):
        m &= np.abs((Z*np.conj(W6[k])).imag) <= math.sqrt(3)/2 + 1e-9
    return m


def dentro_tile(Z, k):
    """triangulo k = conv{0, w^k, w^{k+1}}: coordenadas baricentricas >= 0."""
    a, b = W6[k], W6[(k+1) % 6]
    det = (a.real*b.imag - a.imag*b.real)
    u = (Z.real*b.imag - Z.imag*b.real)/det
    v = (a.real*Z.imag - a.imag*Z.real)/det
    return (u >= -1e-9) & (v >= -1e-9) & (u+v <= 1+1e-9)


def certifica(f, rng, tol=1e-9):
    """f(w z) = f(z) para w = rotacao de 120 graus?"""
    z = (rng.normal(0, .5, 4000) + 1j*rng.normal(0, .5, 4000))
    w = complex(math.cos(2*math.pi/3), math.sin(2*math.pi/3))
    a, b = f(z), f(w*z)
    bom = np.isfinite(a) & np.isfinite(b) & (np.abs(a) < 1e6)
    return float(np.max(np.abs(a[bom]-b[bom])/(1+np.abs(a[bom]))))


def item(f, N, lado=1.0):
    Z = malha_hex(N, lado)
    vals = f(Z)
    img = retrato(vals)
    hexa = img.copy(); m = dentro_hexagono(Z)
    hexa[~m] = 255
    tiles = []
    for k in range(6):
        t = img.copy(); mk = dentro_tile(Z, k)
        t[~mk] = 255
        ys, xs = np.where(mk)
        tiles.append(t[ys.min():ys.max()+1, xs.min():xs.max()+1])
    return hexa, tiles, float(np.max(np.abs(vals[m][np.isfinite(vals[m])])))


def malha_hex(N, lado=1.0):
    x = np.linspace(-1.05, 1.05, N)
    X, Y = np.meshgrid(x, -x)
    return (X + 1j*Y)/lado


def preambulo(nome):
    """cabecalho do catalogo, no mesmo estilo do catalogo dos tetraflexagonos.

    Nao usamos o truque '\\twocolumn[\\begin{@twocolumnfalse}...]': fora de
    \\makeatletter o '@' nao e letra e o arquivo nao compila.  multicol da o
    mesmo resultado sem depender de nomes internos.
    """
    return [r"\documentclass[10pt,a4paper]{article}",
            r"\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}",
            r"\usepackage{amsmath,amssymb}\usepackage{graphicx}",
            r"\usepackage[margin=1.5cm]{geometry}\usepackage{multicol}",
            r"\setlength{\columnsep}{14pt}\pagestyle{empty}",
            r"\begin{document}",
            r"\begin{center}",
            r"{\Large\bfseries Fun\c{c}\~oes complexas flexion\'aveis}\\[2pt]",
            r"{\large %s}\\[6pt]" % TITULOS.get(nome, nome.replace('_', ' ')),
            r"\parbox{0.86\textwidth}{\small\centering",
            r"O grupo de discrep\^ancia deste flex\'agono \'e $\Gamma=C_3$, a rota\c{c}\~ao",
            r"de $120^\circ$ em torno do centro $O$ da face; as solu\c{c}\~oes s\~ao portanto",
            r"exatamente as $f(z)=h\big((z-O)^3\big)$ com $h$ meromorfa. Cada item abaixo",
            r"traz o retrato de fase de uma delas sobre a face hexagonal; os seis",
            r"tri\^angulos recortados est\~ao nas subpastas. Toda fun\c{c}\~ao foi",
            r"verificada numericamente ($|f(\omega z)-f(z)|<10^{-9}$) antes de ser desenhada.}",
            r"\end{center}",
            r"\vspace{4pt}",
            r"\begin{multicols}{2}"]


def gerar(nome, n, N, raiz, semente=2026, grau=2):
    rng = np.random.default_rng(semente)
    dest = os.path.join(raiz, "funcoes-flexionaveis-" + nome)
    os.makedirs(dest, exist_ok=True)
    indice = []
    for i in range(1, n+1):
        while True:
            f, tex = familia(rng, grau)
            r = certifica(f, rng)
            if r < 1e-9: break
        hexa, tiles, _ = item(f, N)
        sub = os.path.join(dest, "%03d" % i); os.makedirs(sub, exist_ok=True)
        Image.fromarray(hexa).save(os.path.join(sub, "hexagono.png"))
        for k, t in enumerate(tiles):
            Image.fromarray(t).save(os.path.join(sub, "tile%d.png" % k))
        open(os.path.join(sub, "formula.tex"), "w").write(tex)
        open(os.path.join(sub, "formula.txt"), "w").write(tex)
        indice.append({"n": i, "tex": tex, "residuo": r})
        print("  item %d/%d  residuo %.1e" % (i, n, r), flush=True)
    json.dump(indice, open(os.path.join(dest, "indice.json"), "w"), indent=1)
    tex = preambulo(nome)
    for d in indice:
        tex += [r"\noindent\textbf{%d.}\ {\footnotesize$\displaystyle %s$}\par\vspace{2pt}"
                % (d["n"], d["tex"]),
                r"\includegraphics[width=\linewidth]{%03d/hexagono.png}\par\vspace{5mm}"
                % d["n"]]
    tex += [r"\end{multicols}", r"\end{document}"]
    open(os.path.join(dest, "catalogo.tex"), "w").write("\n".join(tex))
    subprocess.run(["pdflatex", "-interaction=nonstopmode", "catalogo.tex"],
                   cwd=dest, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("  ->", os.path.join(dest, "catalogo.pdf"))


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
    N = int(sys.argv[2]) if len(sys.argv) > 2 else 700
    raiz = sys.argv[3] if len(sys.argv) > 3 else "../catalogos"
    so = sys.argv[4] if len(sys.argv) > 4 else None
    for nome, sem in (("trihexaflexagono", 2026), ("hexahexaflexagono", 3141)):
        if so and so != nome: continue
        print(nome)
        gerar(nome, n, N, raiz, semente=sem)
