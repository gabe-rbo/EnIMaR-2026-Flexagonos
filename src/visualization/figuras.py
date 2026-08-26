"""
figuras.py -- as figuras geometricas do artigo.
Paleta: azul #2a78d6, laranja #eb6834, tinta #0b0b0b, secundario #52514e
(validada para daltonismo e contraste).
"""
import math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Circle

AZUL, LARANJA, TINTA, SEC, CINZA = "#2a78d6", "#eb6834", "#0b0b0b", "#52514e", "#c9c8c3"
FIG = "../artigo/fig"
os.makedirs(FIG, exist_ok=True)
W6 = [(math.cos(k*math.pi/3), math.sin(k*math.pi/3)) for k in range(6)]


def limpa(ax, lim=1.35):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.axis("off")


# ------------------------------------------------------------ 1. retas de dobra
def retas_de_dobra():
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.6, 3.9))
    # --- quadrado 2x2
    for i in (-1, 0):
        for j in (-1, 0):
            a1.add_patch(Polygon([(i, j), (i+1, j), (i+1, j+1), (i, j+1)],
                                 fc="#f4f3ef", ec=CINZA, lw=.8))
    for x in (-1, 0, 1):
        a1.plot([x, x], [-1.18, 1.18], color=AZUL if x == 0 else LARANJA,
                lw=2.0 if x == 0 else 1.6, ls="-" if x == 0 else (0, (5, 3)))
        a1.plot([-1.18, 1.18], [x, x], color=AZUL if x == 0 else LARANJA,
                lw=2.0 if x == 0 else 1.6, ls="-" if x == 0 else (0, (5, 3)))
    a1.annotate("", xy=(1.0, -1.32), xytext=(-1.0, -1.32),
                arrowprops=dict(arrowstyle="->", color=LARANJA, lw=1.4))
    a1.text(0, -1.5, "$r_{x=1}\\,r_{x=-1}$ = translação de 2",
            ha="center", va="top", color=LARANJA, fontsize=9)
    a1.text(0.06, 1.22, "medianas", color=AZUL, fontsize=9, ha="left")
    a1.text(-1.3, 1.05, "lados", color=LARANJA, fontsize=9, ha="left")
    a1.set_title("quadrado: 6 retas admissíveis", fontsize=10, color=TINTA)
    limpa(a1, 1.6); a1.set_ylim(-1.75, 1.45)
    # --- hexagono
    for k in range(6):
        a, b = W6[k], W6[(k+1) % 6]
        a2.add_patch(Polygon([(0, 0), a, b], fc="#f4f3ef", ec=CINZA, lw=.8))
    for k in range(3):
        x, y = W6[k]
        a2.plot([-1.22*x, 1.22*x], [-1.22*y, 1.22*y], color=AZUL, lw=2.0)
    for k in range(6):
        a, b = W6[k], W6[(k+1) % 6]
        a2.plot([a[0], b[0]], [a[1], b[1]], color=LARANJA, lw=1.6, ls=(0, (2, 2)))
    a2.add_patch(Circle((0, 0), .055, fc=TINTA, ec="none", zorder=5))
    a2.text(.09, .09, "$O$", fontsize=11, color=TINTA)
    a2.text(0, -1.5, "os lados não servem: levariam papel para fora",
            ha="center", va="top", color=LARANJA, fontsize=9)
    a2.set_title("hexágono: 3 diagonais, todas por $O$", fontsize=10, color=TINTA)
    limpa(a2, 1.6); a2.set_ylim(-1.75, 1.45)
    fig.tight_layout()
    fig.savefig(f"{FIG}/retas_dobra.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("retas_dobra.png")


# ------------------------------------------------------------ 2. flexao de pinca
def pinca():
    fig, axs = plt.subplots(1, 4, figsize=(9.6, 2.9))
    pares = [(0, 1), (2, 3), (4, 5)]
    def tri(ax, k, cor, txt=None, alpha=1.0):
        a, b = W6[k], W6[(k+1) % 6]
        ax.add_patch(Polygon([(0, 0), a, b], fc=cor, ec=TINTA, lw=.7, alpha=alpha))
        if txt is not None:
            c = ((a[0]+b[0])/3, (a[1]+b[1])/3)
            ax.text(c[0], c[1], txt, ha="center", va="center", fontsize=9,
                    color="white" if cor != "#f4f3ef" else TINTA)
    # (a) hexagono, com os tres raios de dobra
    for k in range(6):
        tri(axs[0], k, AZUL if k % 2 == 0 else "#f4f3ef", str(k))
    for a, b in pares:
        x, y = W6[b]
        axs[0].plot([0, x], [0, y], color=LARANJA, lw=2.4)
    axs[0].set_title("(a) pinçar por 3 raios", fontsize=9, color=TINTA)
    # (b) tri-dobrado
    for a, b in pares:
        tri(axs[1], b, AZUL, f"{a}/{b}")
    axs[1].set_title("(b) tri-dobrado", fontsize=9, color=TINTA)
    # (c) abrir pelos outros tres raios
    def cen(k):
        a_, b_ = W6[k], W6[(k+1) % 6]
        return ((a_[0]+b_[0])/3, (a_[1]+b_[1])/3)
    for a, b in pares:
        tri(axs[2], b, AZUL, f"{a}/{b}")
        d = (b+1) % 6
        aa, bb = W6[d], W6[(d+1) % 6]
        axs[2].add_patch(Polygon([(0, 0), aa, bb], fc="none", ec=LARANJA,
                                 lw=1.1, ls=(0, (3, 2))))
        xx, yy = W6[d]
        axs[2].plot([0, xx], [0, yy], color=LARANJA, lw=2.4)
        p0, p1 = cen(b), cen(d)
        axs[2].annotate("", xy=(p1[0]*.9, p1[1]*.9), xytext=(p0[0]*.9, p0[1]*.9),
                        arrowprops=dict(arrowstyle="->", color=LARANJA, lw=1.5,
                                        connectionstyle="arc3,rad=-0.35"))
    axs[2].set_title("(c) abrir pelos outros 3", fontsize=9, color=TINTA)
    # (d) hexagono outra vez
    for k in range(6):
        tri(axs[3], k, "#f4f3ef" if k % 2 == 0 else AZUL, str(k))
    axs[3].set_title("(d) hexágono de novo", fontsize=9, color=TINTA)
    for ax in axs:
        ax.add_patch(Circle((0, 0), .05, fc=TINTA, ec="none", zorder=6))
        limpa(ax, 1.25)
    fig.tight_layout()
    fig.savefig(f"{FIG}/pinca.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("pinca.png")


# ------------------------------------------------- 3. o grafo de flexao
def grafo_componentes():
    import pickle, random
    from collections import deque
    import numpy as np
    import flexcamadas as X
    P = X.HEXA
    resto, tam = pickle.load(open("../saidas/componentes.pkl", "rb"))
    orb = set(pickle.load(open("../saidas/orbita_fixa.pkl", "rb"))[0])
    ALL = set()
    for g in P.dobraduras():
        for o in P.ordens_validas(g): ALL |= set(P.imagens((g, o)))
    fora = sorted(ALL - orb); random.seed(3)

    def componente(s):
        vis = {s}; fila = deque([s]); ar = []
        while fila:
            u = fila.popleft()
            for v in P.vizinhos(u):
                if v == u: continue
                ar.append((u, v))
                if v not in vis: vis.add(v); fila.append(v)
        idx = {e: i for i, e in enumerate(sorted(vis))}
        return len(vis), sorted({tuple(sorted((idx[a], idx[b]))) for a, b in ar if b in idx})

    def mola(n, ar, passos=260):
        rng = np.random.default_rng(5)
        p = rng.normal(0, 1, (n, 2))
        for t in range(passos):
            f = np.zeros((n, 2))
            d = p[:, None, :] - p[None, :, :]
            r2 = (d**2).sum(-1) + 1e-3
            f += (d/r2[:, :, None]).sum(1)*0.02
            for a, b in ar:
                v = p[b]-p[a]; f[a] += v*0.06; f[b] -= v*0.06
            p += f*(1-t/passos)*0.5
        p -= p.mean(0); p /= (np.abs(p).max()+1e-9)
        return p

    alvos = []
    for s in fora:
        n, ar = componente(s)
        if n in (4, 8, 20) and not any(n == m for m, _, _ in alvos):
            alvos.append((n, ar, mola(n, ar)))
        if len(alvos) == 3: break
    alvos.sort()

    fig = plt.figure(figsize=(9.4, 3.1))
    for i, (n, ar, p) in enumerate(alvos):
        ax = fig.add_subplot(1, 4, i+1)
        for a, b in ar:
            ax.plot([p[a, 0], p[b, 0]], [p[a, 1], p[b, 1]], color=CINZA, lw=1.0, zorder=1)
        ax.scatter(p[:, 0], p[:, 1], s=42, color=LARANJA, ec="white", lw=.9, zorder=3)
        ax.set_title(f"grão de {n} estados", fontsize=9, color=TINTA)
        limpa(ax, 1.25)
    ax = fig.add_subplot(1, 4, 4)
    ks = sorted(tam)
    ax.scatter([k for k in ks if k != 19200], [tam[k] for k in ks if k != 19200],
               s=30, color=LARANJA, ec="white", lw=.7, zorder=3, label="grãos")
    ax.scatter([19200], [1], s=90, color=AZUL, ec="white", lw=1.0, zorder=4,
               marker="D", label="o flexágono")
    ax.annotate("19200", (19200, 1), textcoords="offset points", xytext=(-4, 10),
                ha="right", fontsize=8, color=AZUL)
    ax.annotate("200", (200, 4), textcoords="offset points", xytext=(2, 8),
                fontsize=8, color=LARANJA)
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlabel("tamanho da componente", fontsize=8, color=SEC)
    ax.set_ylabel("quantas", fontsize=8, color=SEC)
    ax.tick_params(labelsize=7, colors=SEC)
    for sp in ("top", "right"): ax.spines[sp].set_visible(False)
    for sp in ("left", "bottom"): ax.spines[sp].set_color(CINZA)
    ax.grid(True, which="major", color=CINZA, lw=.4, alpha=.6)
    ax.set_axisbelow(True)
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    ax.set_title("as 20 405 componentes", fontsize=9, color=TINTA)
    fig.tight_layout()
    fig.savefig(f"{FIG}/grafo_componentes.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("grafo_componentes.png")


# ------------------------------------------------- 4. uma solucao por flexagono
def quatro_faces(N=520):
    import numpy as np
    from gerador import retrato
    from wp import WPSquare
    fig, axs = plt.subplots(1, 4, figsize=(9.6, 2.9))
    x = np.linspace(-1, 1, N); Xg, Yg = np.meshgrid(x, -x); Z = Xg + 1j*Yg
    c1 = .5+.5j
    # tri-tetra: solucao INTEIRA
    axs[0].imshow(retrato(np.cos(np.pi*(Z-c1))), extent=(-1, 1, -1, 1))
    axs[0].set_title("tri-tetraflexágono\n$\\cos(\\pi(z-c_1))$", fontsize=8.5, color=TINTA)
    # hexa-tetra: eliptica de 2Z[i]
    Pw = WPSquare(2.0)
    axs[1].imshow(retrato(Pw(Z - c1)), extent=(-1, 1, -1, 1))
    axs[1].set_title("hexa-tetraflexágono\n$\\wp(z-c_1;\\,2\\mathbb{Z}[i])$",
                     fontsize=8.5, color=TINTA)
    # os dois hexaflexagonos: h(z^3)
    xx = np.linspace(-1.05, 1.05, N); Xh, Yh = np.meshgrid(xx, -xx); Zh = Xh + 1j*Yh
    m = np.ones(Zh.shape, bool)
    for k in range(3):
        w = complex(math.cos(k*math.pi/3), math.sin(k*math.pi/3))
        m &= np.abs((Zh*np.conj(w)).imag) <= math.sqrt(3)/2 + 1e-9
    for i, (tit, f) in enumerate((
            ("tri-hexaflexágono\n$z^{3}$", lambda z: z**3),
            ("hexa-hexaflexágono\n$(z^{3}-0.3)/(z^{3}+0.5)$",
             lambda z: (z**3 - .3)/(z**3 + .5)))):
        img = retrato(f(Zh)); img[~m] = 255
        axs[2+i].imshow(img, extent=(-1.05, 1.05, -1.05, 1.05))
        axs[2+i].set_title(tit, fontsize=8.5, color=TINTA)
    for ax in axs: ax.axis("off")
    fig.tight_layout()
    fig.savefig(f"{FIG}/quatro_faces.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("quatro_faces.png")


# ------------------------------------------------- 5. a regra dos extremos
def extremos():
    PATS = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)]
    CEN = [(-1, 1), (1, 1), (1, -1), (-1, -1)]          # ciclo das 4 posicoes
    def desenha(ax, topos, titulo, cor_ok):
        for (p, ce, t) in zip(PATS, CEN, topos):
            x0, y0 = ce
            ordem = [i for i in p if i != t] + [t]       # o topo por ultimo
            for lvl, i in enumerate(ordem):
                saida = (i == p[-1])
                ax.add_patch(Polygon([(x0-.55, y0-.30+lvl*.22), (x0+.55, y0-.30+lvl*.22),
                                      (x0+.55, y0-.14+lvl*.22), (x0-.55, y0-.14+lvl*.22)],
                                     fc=(LARANJA if saida else "#f4f3ef"),
                                     ec=TINTA, lw=.7))
                ax.text(x0, y0-.22+lvl*.22, str(i), ha="center", va="center",
                        fontsize=7.5, color="white" if saida else SEC)
            ax.text(x0, y0+.52, "topo: %d%s" % (t, "  (saída)" if t == p[-1] else ""),
                    ha="center", fontsize=7.5,
                    color=cor_ok if t == p[-1] else SEC)
        for k in range(4):
            a, b = CEN[k], CEN[(k+1) % 4]
            ax.annotate("", xy=(b[0]*.72, b[1]*.72), xytext=(a[0]*.72, a[1]*.72),
                        arrowprops=dict(arrowstyle="->", color=CINZA, lw=1.2,
                                        connectionstyle="arc3,rad=0.25"))
        ax.set_title(titulo, fontsize=9.5, color=cor_ok)
        ax.set_xlim(-2, 2); ax.set_ylim(-1.9, 2.0); ax.set_aspect("equal"); ax.axis("off")
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.2, 4.0))
    desenha(a1, (2, 3, 8, 9), "alcançável: saída no topo\nem dois pats OPOSTOS", AZUL)
    desenha(a2, (2, 5, 8, 11), "inalcançável: saída no topo\nnos QUATRO (a face 1)", LARANJA)
    fig.tight_layout()
    fig.savefig(f"{FIG}/extremos.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("extremos.png")


# ------------------------------------------------- 6. os planos de papel
def planos():
    import foldings as F, foldings_tri as T
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(9.2, 3.6))
    RUNCOR = [AZUL, LARANJA, AZUL, LARANJA]
    # (a) o anel de 12 quadradinhos
    for i, (r, c) in enumerate(F.RING):
        a1.add_patch(Polygon([(c, -r), (c+1, -r), (c+1, -r-1), (c, -r-1)],
                             fc="#f4f3ef", ec=CINZA, lw=.8))
        fc, q = F.VERSO[(r, c)]
        a1.text(c+.5, -r-.5, str(i), ha="center", va="center", fontsize=9, color=TINTA)
        if fc == 1:
            a1.add_patch(Polygon([(c+.08, -r-.08), (c+.92, -r-.08),
                                  (c+.92, -r-.92), (c+.08, -r-.92)],
                                 fc="none", ec=AZUL, lw=1.8))
    for h in range(12):
        i, j = h, (h+1) % 12
        (r1, c1), (r2, c2) = F.RING[i], F.RING[j]
        x = (c1+c2)/2+.5; y = -(r1+r2)/2-.5
        a1.plot([x], [y], marker="o", ms=5, color=RUNCOR[h//3], zorder=4)
    a1.text(2, -4.6, "pontos azuis: charneiras verticais (blocos 1 e 3)\n"
                     "pontos laranja: horizontais (blocos 2 e 4)\n"
                     "moldura: as quatro folhas da face 1",
            ha="center", va="top", fontsize=8, color=SEC)
    a1.set_title("hexa-tetraflexágono: o anel de 12", fontsize=10, color=TINTA)
    a1.set_xlim(-.4, 4.4); a1.set_ylim(-5.6, .4); a1.set_aspect("equal"); a1.axis("off")
    # (b) o octomino rasgado
    for cel in T.CELL:
        r, c = T.POS[cel]
        branco = (T.FRENTE[cel] is None and T.VERSO[cel] is None)
        a2.add_patch(Polygon([(c, -r), (c+1, -r), (c+1, -r-1), (c, -r-1)],
                             fc="#e9e8e3" if branco else "#f4f3ef", ec=CINZA, lw=.8))
        a2.text(c+.5, -r-.5, cel, ha="center", va="center", fontsize=10, color=TINTA)
    for (A, B) in T.CORTES:                      # o rasgo
        (r1, c1), (r2, c2) = T.POS[A], T.POS[B]
        if r1 == r2:
            x = max(c1, c2); a2.plot([x, x], [-r1, -r1-1], color=LARANJA, lw=3.4)
        else:
            y = -max(r1, r2); a2.plot([c1, c1+1], [y, y], color=LARANJA, lw=3.4)
    A, B, _ = T.COLA
    for cel, dx in ((A, 0), (B, 0)):
        r, c = T.POS[cel]
        a2.add_patch(Polygon([(c+.06, -r-.06), (c+.94, -r-.06),
                              (c+.94, -r-.94), (c+.06, -r-.94)],
                             fc="none", ec=AZUL, lw=2.0, ls=(0, (3, 2))))
    a2.text(2.5, -2.5, "laranja: o rasgo   ·   azul: a colagem (%s–%s)" % (A, B),
            ha="center", va="top", fontsize=8, color=SEC)
    a2.set_title("tri-tetraflexágono: a tira $a\\,b\\,c\\,f\\,g\\,h\\,e\\,d$",
                 fontsize=10, color=TINTA)
    a2.set_xlim(-.4, 5.4); a2.set_ylim(-3.4, .4); a2.set_aspect("equal"); a2.axis("off")
    fig.tight_layout()
    fig.savefig(f"{FIG}/planos.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("planos.png")


# ------------------------------------------------- 7. a roda de dois prototipos
def roda():
    fig, ax = plt.subplots(figsize=(4.6, 4.4))
    ang = [0, 90, 150, 240, 300]; larg = [90, 60, 90, 60, 60]
    tipo = ["quadrado", "triângulo", "quadrado", "triângulo", "triângulo"]
    for a0, w, t in zip(ang, larg, tipo):
        r = math.radians(a0); r2 = math.radians(a0+w)
        if t == "quadrado":
            v = [(0, 0), (math.cos(r), math.sin(r)),
                 (math.cos(r)+math.cos(r2), math.sin(r)+math.sin(r2)),
                 (math.cos(r2), math.sin(r2))]
        else:
            v = [(0, 0), (math.cos(r), math.sin(r)), (math.cos(r2), math.sin(r2))]
        ax.add_patch(Polygon(v, fc=AZUL if t == "quadrado" else "#f4f3ef",
                             ec=TINTA, lw=.9, alpha=.9))
        cm = math.radians(a0+w/2); rr = .62 if t == "quadrado" else .55
        ax.text(rr*math.cos(cm), rr*math.sin(cm), "$C_4$" if t == "quadrado" else "$C_3$",
                ha="center", va="center", fontsize=10,
                color="white" if t == "quadrado" else SEC)
    ax.annotate("", xy=(.42*math.cos(math.radians(195)), .42*math.sin(math.radians(195))),
                xytext=(.42*math.cos(math.radians(45)), .42*math.sin(math.radians(45))),
                arrowprops=dict(arrowstyle="->", color=LARANJA, lw=2.0,
                                connectionstyle="arc3,rad=-0.45"))
    ax.text(0, -1.55, "$90+60+90+60+60=360$\nA rotação de $150^\\circ$ troca os dois quadrados:\n"
                      "$\\langle 150^\\circ\\rangle=C_{12}$, e as soluções são $h((z-p)^{12})$",
            ha="center", va="top", fontsize=8.5, color=SEC)
    ax.add_patch(Circle((0, 0), .045, fc=TINTA, ec="none", zorder=6))
    ax.set_title("a roda: dois protótipos, $\\Gamma=C_{12}$", fontsize=10, color=TINTA)
    ax.set_xlim(-1.75, 1.75); ax.set_ylim(-2.3, 1.6)
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    fig.savefig(f"{FIG}/roda.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("roda.png")


# ------------------------------------------------- 8. variedade do catalogo
def variedade(N=340, n=8):
    import numpy as np
    from gerador import retrato
    rng = np.random.default_rng(2026)
    xx = np.linspace(-1.05, 1.05, N); Xh, Yh = np.meshgrid(xx, -xx); Z = Xh + 1j*Yh
    m = np.ones(Z.shape, bool)
    for k in range(3):
        w = complex(math.cos(k*math.pi/3), math.sin(k*math.pi/3))
        m &= np.abs((Z*np.conj(w)).imag) <= math.sqrt(3)/2 + 1e-9
    fig, axs = plt.subplots(2, n//2, figsize=(9.6, 5.0))
    for ax in axs.ravel():
        zer = [complex(rng.normal(0, .7), rng.normal(0, .7)) for _ in range(2)]
        pol = [complex(rng.normal(0, .7), rng.normal(0, .7)) for _ in range(2)]
        c = complex(rng.normal(0, 1), rng.normal(0, 1))
        w = Z**3
        num = np.ones_like(w); den = np.ones_like(w)
        for a in zer: num = num*(w-a)
        for b in pol: den = den*(w-b)
        img = retrato(c*num/den); img[~m] = 255
        ax.imshow(img, extent=(-1.05, 1.05, -1.05, 1.05)); ax.axis("off")
    fig.suptitle("oito soluções do catálogo dos hexaflexágonos: $f(z)=h(z^{3})$",
                 fontsize=10, color=TINTA, y=.99)
    fig.tight_layout()
    fig.savefig(f"{FIG}/variedade.png", dpi=190, bbox_inches="tight")
    plt.close(fig); print("variedade.png")


# ------------------------------------------------- 9. o atlas das nove classes
def atlas(N=300):
    """Um retrato de fase do Hauptmodul de cada uma das nove classes."""
    import numpy as np
    from gerador import retrato
    from wpgen import WP
    Wq = WP(2.0, 2.0j)                                    # quadrado: g3=0, j=1728
    z6 = complex(math.cos(math.pi/3), math.sin(math.pi/3))
    Wh = WP(2.0, 2.0*z6)                                  # hexagonal: g2=0, j=0
    L = 1.0
    x = np.linspace(-L, L, N); Xg, Yg = np.meshgrid(x, -x); Z = Xg + 1j*Yg
    itens = [
        (0, "1", "$J=z$: toda $f$ serve",              lambda z: z),
        (0, "n", "$J=(z-p)^n$, aqui $n=3$",            lambda z: z**3),
        (0, "—", "",                                    None),          # vago
        (1, "1", "$J=e^{2\\pi i(z-p)/\\omega}$",       lambda z: np.exp(1j*np.pi*z)),
        (1, "2", "$J=\\cos(2\\pi(z-p)/\\omega)$",      lambda z: np.cos(np.pi*z)),
        (2, "1", "$J=\\wp,\\ \\wp'$ (dois geradores)", lambda z: Wq.deriv(z)),
        (2, "2", "$J=\\wp$",                            lambda z: Wq(z)),
        (2, "3", "$J=\\wp'$, $\\Lambda$ hexagonal",    lambda z: Wh.deriv(z)),
        (2, "4", "$J=\\wp^{2}$, $\\Lambda$ quadrado",  lambda z: Wq(z)**2),
        (2, "6", "$J=\\wp'^{2}$, $\\Lambda$ hexagonal", lambda z: Wh.deriv(z)**2),
    ]
    itens = [i for i in itens if i[3] is not None]
    fig, axs = plt.subplots(3, 3, figsize=(8.1, 8.7))
    for ax, (r, n, tit, f) in zip(axs.ravel(), itens):
        with __import__("numpy").errstate(all="ignore"):
            ax.imshow(retrato(f(Z)), extent=(-L, L, -L, L))
        cor = AZUL if r <= 1 else LARANJA
        ax.set_title("posto $%d$,   $|P|=%s$" % (r, n), fontsize=10.5,
                     color=cor, pad=4)
        ax.set_xlabel(tit, fontsize=8.5, color=SEC, labelpad=4)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values(): sp.set_color(CINZA); sp.set_linewidth(.7)
    fig.text(.5, .012, "azul: existem soluções inteiras não constantes    ·    "
                       "laranja: não existem (posto $2$)",
             ha="center", fontsize=9, color=SEC)
    fig.tight_layout(rect=(0, .028, 1, 1))
    fig.savefig(f"{FIG}/atlas.png", dpi=200, bbox_inches="tight")
    plt.close(fig); print("atlas.png")


# --------------------------------------------- 10. a flexao do tetraflexagono
def flexao_tetra():
    """O análogo quadrado da pinça: dobrar por uma mediana e reabrir pela mesma,
       separando a pilha noutro ponto (é exatamente dobrar/abrir do modelo)."""
    fig, axs = plt.subplots(1, 5, figsize=(11.4, 2.75))
    NOMES = ["$Q_1$", "$Q_2$", "$Q_3$", "$Q_4$"]
    CEN = [(.5, .5), (-.5, .5), (-.5, -.5), (.5, -.5)]
    def quad(ax, k, cor, rot=None, ec=TINTA, ls="-"):
        cx, cy = CEN[k]
        ax.add_patch(Polygon([(cx-.5, cy-.5), (cx+.5, cy-.5),
                              (cx+.5, cy+.5), (cx-.5, cy+.5)],
                             fc=cor, ec=ec, lw=.9, ls=ls))
        ax.text(cx, cy, NOMES[k] if rot is None else rot, ha="center",
                va="center", fontsize=9.5,
                color="white" if cor == AZUL else TINTA)
    # (a) a face e os dois cortes
    for k in range(4):
        quad(axs[0], k, AZUL if k % 2 == 0 else "#f4f3ef")
    for a, b in (((-1, 0), (1, 0)), ((0, -1), (0, 1))):
        axs[0].plot([a[0], b[0]], [a[1], b[1]], color=LARANJA, lw=2.2)
    axs[0].set_title("(a) a face e os cortes", fontsize=9, color=TINTA)
    # (b) dobrar pela mediana vertical
    for k, alv in ((1, 0), (2, 3)):
        cx, cy = CEN[k]
        quad(axs[1], k, "none", " ", ec=CINZA, ls=(0, (3, 2)))
        axs[1].annotate("", xy=CEN[alv], xytext=(cx, cy),
                        arrowprops=dict(arrowstyle="->", color=LARANJA, lw=1.6,
                                        connectionstyle="arc3,rad=-0.4"))
    quad(axs[1], 0, AZUL, "$Q_1$\n$Q_2$")
    quad(axs[1], 3, "#f4f3ef", "$Q_4$\n$Q_3$")
    axs[1].plot([0, 0], [-1.1, 1.1], color=LARANJA, lw=2.4)
    axs[1].set_title("(b) dobrar: duas pilhas", fontsize=9, color=TINTA)
    # (c) reabrir separando a pilha noutro ponto: sobem as folhas de baixo
    for k in range(4):
        quad(axs[2], k, "#fdece4", "$Q'_%d$" % (k+1))
    axs[2].plot([0, 0], [-1.1, 1.1], color=LARANJA, lw=2.4)
    for k in (1, 2):
        cx, cy = CEN[k]
        axs[2].annotate("", xy=(cx, cy), xytext=(-cx, cy),
                        arrowprops=dict(arrowstyle="->", color=LARANJA, lw=1.6,
                                        connectionstyle="arc3,rad=0.4"))
    axs[2].set_title("(c) reabrir: outra face", fontsize=9, color=TINTA)
    # (d) o mapa de retorno diagonal
    for k in range(4):
        quad(axs[3], k, AZUL if k % 2 == 0 else "#f4f3ef")
    for a, b in ((0, 2), (1, 3)):
        axs[3].annotate("", xy=CEN[b], xytext=CEN[a],
                        arrowprops=dict(arrowstyle="<->", color=LARANJA, lw=2.0))
    axs[3].set_title("(d) $\\sigma=(13)(24)$, $\\varepsilon\\equiv1$",
                     fontsize=9, color=TINTA)
    for ax in axs[:4]:
        ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.35, 1.35)
        ax.set_aspect("equal"); ax.axis("off")
    # (e) o reticulado gerado pelas discrepancias
    ax = axs[4]
    for m in range(-2, 3):
        for n in range(-2, 3):
            ax.plot([2*m], [2*n], marker="o", ms=4.2, color=AZUL, zorder=3)
    ax.add_patch(Polygon([(-1, -1), (1, -1), (1, 1), (-1, 1)],
                         fc="none", ec=TINTA, lw=1.1))
    ax.annotate("", xy=(2, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=LARANJA, lw=2.0))
    ax.annotate("", xy=(0, 2), xytext=(0, 0),
                arrowprops=dict(arrowstyle="->", color=LARANJA, lw=2.0))
    ax.text(1.15, -.75, "$2$", color=LARANJA, fontsize=10)
    ax.text(.18, 1.5, "$2i$", color=LARANJA, fontsize=10)
    ax.set_title("(e) $\\Lambda_\\Phi=2\\mathbb{Z}[i]$", fontsize=9, color=TINTA)
    ax.set_xlim(-4.6, 4.6); ax.set_ylim(-4.8, 4.8)
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    fig.savefig(f"{FIG}/flexao_tetra.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("flexao_tetra.png")


# --------------------------------------- 11. as tiras dos dois hexaflexagonos
def tiras():
    """Os planos de papel dos hexaflexágonos, direto de hexaflex.tira(N)."""
    import hexaflex as H
    S3 = math.sqrt(3)/2
    def emb(p): return (p[0] + p[1]*.5, p[1]*S3)
    fig, axs = plt.subplots(2, 1, figsize=(9.6, 3.8))
    for ax, (N, tit) in zip(axs, ((10, "tri-hexaflexágono: $10$ triângulos "
                                      "($9$ + a aba de cola)"),
                                  (19, "hexa-hexaflexágono: $19$ triângulos "
                                       "($18$ + a aba de cola)"))):
        cel, cent, hin = H.tira(N)
        for m, v in enumerate(cel):
            pts = [emb(q) for q in v]
            aba = (m == N-1)
            ax.add_patch(Polygon(pts, fc="#fdece4" if aba else "#f4f3ef",
                                 ec=LARANJA if aba else CINZA,
                                 lw=1.6 if aba else .9,
                                 ls=(0, (3, 2)) if aba else "-"))
            cx = sum(q[0] for q in pts)/3; cy = sum(q[1] for q in pts)/3
            ax.text(cx, cy, str(m), ha="center", va="center", fontsize=7,
                    color=LARANJA if aba else SEC)
        for m in range(N-1):                       # as charneiras interiores
            com = [q for q in cel[m] if q in cel[m+1]]
            (a, b) = [emb(q) for q in com]
            ax.plot([a[0], b[0]], [a[1], b[1]], color=AZUL, lw=1.6, zorder=4)
        p0 = [emb(q) for q in cel[0]]; pN = [emb(q) for q in cel[N-1]]
        c0 = (sum(q[0] for q in p0)/3, sum(q[1] for q in p0)/3)
        cN = (sum(q[0] for q in pN)/3, sum(q[1] for q in pN)/3)
        ax.annotate("", xy=(c0[0], -.28), xytext=(cN[0], -.28),
                    arrowprops=dict(arrowstyle="->", color=LARANJA, lw=1.3,
                                    connectionstyle="arc3,rad=-0.14"))
        ax.set_title(tit, fontsize=9.5, color=TINTA, pad=3)
        ax.set_aspect("equal"); ax.axis("off")
        ax.set_xlim(-.5, 11.3); ax.set_ylim(-.95, 1.05)
    fig.text(.5, .015, "azul: as charneiras   ·   laranja: a aba, colada de "
                       "volta no primeiro triângulo",
             ha="center", fontsize=8.5, color=SEC)
    fig.tight_layout(rect=(0, .05, 1, 1))
    fig.savefig(f"{FIG}/tiras.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("tiras.png")


# ------------------------------- 12. o grafo de flexao do tri-tetraflexagono
def _grafo_tri_dados():
    """(componentes, arestas, rótulo de face) do grafo quociente do TRI."""
    from collections import deque
    import flexcamadas as X
    P = X.TRI
    est = []
    for g in P.dobraduras():
        for o in P.ordens_validas(g): est.append(P.normaliza(g, o))
    todos = set(est); mudou = True
    while mudou:
        mudou = False
        for e in list(todos):
            for f in P.vizinhos(e):
                if f not in todos: todos.add(f); mudou = True
    cls = {}
    for e in todos: cls.setdefault(P.canon(e), []).append(e)
    ch = sorted(cls); idx = {c: i for i, c in enumerate(ch)}
    adj = {i: set() for i in range(len(ch))}
    for c, ms in cls.items():
        for e in ms:
            for f in P.vizinhos(e):
                d = P.canon(f)
                if d != c: adj[idx[c]].add(idx[d]); adj[idx[d]].add(idx[c])
    face = {}
    for c, ms in cls.items():
        fs = set()
        for e in ms:
            r = P.exibida(*e)
            if r: fs.add(r[0])
        face[idx[c]] = "".join(sorted(fs))
    vis = set(); comps = []
    for i in range(len(ch)):
        if i in vis: continue
        q = deque([i]); vis.add(i); c = [i]
        while q:
            u = q.popleft()
            for v in adj[u]:
                if v not in vis: vis.add(v); q.append(v); c.append(v)
        comps.append(sorted(c))
    # o flexágono primeiro: a componente que exibe mais faces
    comps.sort(key=lambda c: (-len({face[i] for i in c if face[i]}),
                              -len(c), c))
    return comps, adj, face, len(ch), sum(len(a) for a in adj.values())//2


def grafo_tri():
    """O grafo INTEIRO do tri-tetraflexágono, a menos das simetrias globais."""
    comps, adj, face, nnos, nar = _grafo_tri_dados()
    COLS = 5
    fig, ax = plt.subplots(figsize=(7.6, 4.2))
    pos = {}
    for ci, comp in enumerate(comps):
        gx, gy = ci % COLS, -.74*(ci//COLS)
        k = len(comp)
        if k == 1:
            pos[comp[0]] = (gx, gy)
        elif k == 2:
            pos[comp[0]] = (gx-.20, gy); pos[comp[1]] = (gx+.20, gy)
        else:
            for t, i in enumerate(comp):
                a = math.pi/2 + 2*math.pi*t/k
                pos[i] = (gx + .26*math.cos(a), gy + .26*math.sin(a))
    for i in adj:
        for j in adj[i]:
            if j <= i: continue
            ax.plot([pos[i][0], pos[j][0]], [pos[i][1], pos[j][1]],
                    color=CINZA, lw=1.4, zorder=1)
    for i in range(nnos):
        r = face[i]
        ax.scatter([pos[i][0]], [pos[i][1]], s=210 if r else 60,
                   color=AZUL if r else LARANJA, ec="white", lw=1.1, zorder=3)
        if r:
            ax.text(pos[i][0], pos[i][1], r, ha="center", va="center",
                    fontsize=8.5, color="white", zorder=4)
    gx, gy = 0, 0
    ax.annotate("o flexágono:\nas três faces", xy=(gx+.30, gy+.24),
                xytext=(gx+.62, gy+.60), fontsize=8.5, color=AZUL,
                arrowprops=dict(arrowstyle="->", color=AZUL, lw=1.1))
    ax.set_title("tri-tetraflexágono: as $%d$ classes de estados dobrados, as "
                 "$%d$ flexões,\ne as $%d$ componentes em que elas se partem"
                 % (nnos, nar, len(comps)), fontsize=10, color=TINTA)
    ax.text(2.0, -2.20, "azul: exibe uma face (F, V, E)   ·   laranja: nenhuma "
                        "face à mostra\nsó a primeira componente é o brinquedo; "
                        "as outras $%d$ são grãos" % (len(comps)-1),
            ha="center", va="top", fontsize=8.5, color=SEC)
    ax.set_xlim(-.75, 4.75); ax.set_ylim(-2.80, 1.05)
    ax.set_aspect("equal"); ax.axis("off")
    fig.tight_layout()
    fig.savefig(f"{FIG}/grafo_tri.png", dpi=210, bbox_inches="tight")
    plt.close(fig); print("grafo_tri.png")


TODAS = [retas_de_dobra, pinca, flexao_tetra, tiras, planos, atlas,
         quatro_faces, variedade, roda, extremos, grafo_tri, grafo_componentes]

if __name__ == "__main__":
    import sys
    alvos = sys.argv[1:]
    for f in TODAS:
        if alvos and f.__name__ not in alvos: continue
        f()
