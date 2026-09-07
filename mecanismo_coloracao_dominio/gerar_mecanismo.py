# -*- coding: utf-8 -*-
"""
gerar_mecanismo.py
===================
Sequência didática de 4 imagens que ilustra o MECANISMO da coloração de domínio
(domain coloring): grade no domínio -> valores f(z) num contradomínio esquemático Y ->
fase f/|f| lida na roda de cores -> pintura de volta no domínio.

Mesma ideia pedagógica das págs. 11-15 de:
    Ponce Campuzano, J.C. "Visualising complex functions: Enhanced phase portraits."
    Delta (2019). https://www.jcponce.com
mas redesenhada do zero, com identidade visual própria (paleta EnIMaR 2026) e SEM
copiar nenhum elemento gráfico daquele PDF.

Gera 4 PNGs em 1920x1080 (16:9), um por "passo" da explicação:
    passo 1: só a grade D_h com 3 pontos marcados.
    passo 2: + setas de f levando os pontos para o contradomínio esquemático Y.
    passo 3: + setas da fase levando os pontos de Y até a roda de cores.
    passo 4: igual ao passo 3, mas os pontos do domínio já aparecem pintados.
"""
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.patches import FancyArrowPatch, Rectangle, Circle

# ---------------------------------------------------------------------------
# Paleta oficial EnIMaR 2026 (a mesma do main.tex da apresentação)
# ---------------------------------------------------------------------------
NAVY = "#142D55"
TEAL = "#008891"
GOLD = "#D48F18"
TEXTO = "#1E232A"
FUNDO_GRADE = "#F5F7FA"

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["text.color"] = TEXTO
plt.rcParams["axes.edgecolor"] = TEXTO

OUT_DIR = Path(__file__).resolve().parent
LARGURA_PX, ALTURA_PX = 1920, 1080
DPI = 160
FIGSIZE = (LARGURA_PX / DPI, ALTURA_PX / DPI)

# ---------------------------------------------------------------------------
# Geometria fixa da cena (coordenadas de dados, iguais nos 4 passos)
# ---------------------------------------------------------------------------
GRADE_X0, GRADE_X1 = 0.3, 4.3          # quadrado do domínio D_h
GRADE_Y0, GRADE_Y1 = 0.3, 4.3
N_LINHAS_GRADE = 11                     # linhas internas (malha fina)

Y_CENTRO = (7.6, 2.3)
Y_RAIO = 1.35

RODA_CENTRO = (12.1, 2.3)
RODA_R_EXT = 1.5
RODA_R_INT = 1.05

# Três pontos de exemplo: posição no domínio, posição esquemática em Y, matiz (graus, HSV)
PONTOS = [
    dict(nome="z_1", cor_pt=NAVY, xy_dom=(1.15, 3.55), xy_Y=(7.15, 2.95), matiz=118),   # vai dar verde
    dict(nome="z_2", cor_pt=NAVY, xy_dom=(1.00, 1.05), xy_Y=(8.15, 1.75), matiz=222),   # vai dar azul
    dict(nome="z_3", cor_pt=NAVY, xy_dom=(3.15, 2.15), xy_Y=(7.55, 1.95), matiz=352),   # vai dar vermelho
]


def cor_hsv(matiz_graus, sat=0.85, val=0.95):
    return mcolors.hsv_to_rgb((matiz_graus / 360.0, sat, val))


def desenhar_grade(ax):
    """Desenha o quadrado do domínio D_h com uma malha fina, estilo papel milimetrado."""
    ax.add_patch(Rectangle((GRADE_X0, GRADE_Y0), GRADE_X1 - GRADE_X0, GRADE_Y1 - GRADE_Y0,
                            facecolor=FUNDO_GRADE, edgecolor=NAVY, linewidth=2.2, zorder=1))
    xs = np.linspace(GRADE_X0, GRADE_X1, N_LINHAS_GRADE)
    ys = np.linspace(GRADE_Y0, GRADE_Y1, N_LINHAS_GRADE)
    for x in xs[1:-1]:
        ax.plot([x, x], [GRADE_Y0, GRADE_Y1], color=NAVY, linewidth=0.5, alpha=0.35, zorder=2)
    for y in ys[1:-1]:
        ax.plot([GRADE_X0, GRADE_X1], [y, y], color=NAVY, linewidth=0.5, alpha=0.35, zorder=2)
    ax.text((GRADE_X0 + GRADE_X1) / 2, GRADE_Y0 - 0.42, r"$D_h$",
            fontsize=22, color=NAVY, ha="center", va="top", style="italic")


def desenhar_Y(ax):
    ax.add_patch(Circle(Y_CENTRO, Y_RAIO, facecolor="white", edgecolor=NAVY,
                         linewidth=2.2, zorder=1))
    ax.text(Y_CENTRO[0], Y_CENTRO[1] - Y_RAIO - 0.42, r"$Y = f(D_h)$",
            fontsize=22, color=NAVY, ha="center", va="top", style="italic")


def desenhar_roda_de_cores(ax):
    n_theta = 720
    thetas = np.linspace(0, 2 * np.pi, n_theta)
    for i in range(n_theta - 1):
        th0, th1 = thetas[i], thetas[i + 1]
        cor = plt.cm.hsv(((np.degrees(th0)) % 360) / 360.0)
        wedge_x = [RODA_CENTRO[0] + RODA_R_INT * np.cos(th0), RODA_CENTRO[0] + RODA_R_EXT * np.cos(th0),
                   RODA_CENTRO[0] + RODA_R_EXT * np.cos(th1), RODA_CENTRO[0] + RODA_R_INT * np.cos(th1)]
        wedge_y = [RODA_CENTRO[1] + RODA_R_INT * np.sin(th0), RODA_CENTRO[1] + RODA_R_EXT * np.sin(th0),
                   RODA_CENTRO[1] + RODA_R_EXT * np.sin(th1), RODA_CENTRO[1] + RODA_R_INT * np.sin(th1)]
        ax.fill(wedge_x, wedge_y, color=cor, linewidth=0, zorder=1)
    ax.add_patch(Circle(RODA_CENTRO, RODA_R_EXT, facecolor="none", edgecolor=NAVY, linewidth=1.6, zorder=2))
    ax.add_patch(Circle(RODA_CENTRO, RODA_R_INT, facecolor="none", edgecolor=NAVY, linewidth=1.2, zorder=2))
    ax.text(RODA_CENTRO[0], RODA_CENTRO[1] - RODA_R_EXT - 0.42,
            r"matiz $\,=\,\arg\!\left(\dfrac{f(z)}{|f(z)|}\right)$",
            fontsize=20, color=NAVY, ha="center", va="top", style="italic")


def ponto_na_roda(matiz_graus):
    th = np.radians(matiz_graus)
    r = (RODA_R_INT + RODA_R_EXT) / 2
    return (RODA_CENTRO[0] + r * np.cos(th), RODA_CENTRO[1] + r * np.sin(th))


def seta(ax, p0, p1, cor, curvatura=0.25, largura=2.2, estilo="-|>", z=5):
    fa = FancyArrowPatch(p0, p1, connectionstyle=f"arc3,rad={curvatura}",
                          arrowstyle=estilo, mutation_scale=16, linewidth=largura,
                          color=cor, zorder=z)
    ax.add_patch(fa)


def montar_figura(passo: int, titulo: str, output_path: Path):
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    ax.set_xlim(-0.3, 13.9)
    ax.set_ylim(-0.6, 5.0)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor("white")

    desenhar_grade(ax)
    if passo >= 2:
        desenhar_Y(ax)
    if passo >= 3:
        desenhar_roda_de_cores(ax)

    for p in PONTOS:
        cor_final = cor_hsv(p["matiz"])
        cor_dom = cor_final if passo >= 4 else NAVY
        # ponto no domínio
        ax.plot(*p["xy_dom"], marker="o", markersize=13, markerfacecolor=cor_dom,
                markeredgecolor="white", markeredgewidth=1.4, zorder=6)
        ax.text(p["xy_dom"][0], p["xy_dom"][1] + 0.28, f"${p['nome']}$",
                fontsize=17, color=NAVY, ha="center", va="bottom")

        if passo >= 2:
            seta(ax, p["xy_dom"], p["xy_Y"], TEAL, curvatura=0.30)
            ax.plot(*p["xy_Y"], marker="o", markersize=11, markerfacecolor=TEAL,
                    markeredgecolor="white", markeredgewidth=1.2, zorder=6)

        if passo >= 3:
            alvo = ponto_na_roda(p["matiz"])
            seta(ax, p["xy_Y"], alvo, GOLD, curvatura=0.22)
            ax.plot(*alvo, marker="o", markersize=13, markerfacecolor=tuple(cor_final),
                    markeredgecolor=NAVY, markeredgewidth=1.6, zorder=7)

    if passo >= 2:
        ax.text(4.5, 3.95, r"$f$", fontsize=26, color=TEAL, ha="center", va="center",
                style="italic", weight="bold")

    if passo >= 3:
        ax.text(10.05, 3.75, r"fase $= f/|f|$", fontsize=20, color=GOLD, ha="center",
                va="center", style="italic")

    ax.text(0.0, 4.75, titulo, fontsize=24, color=NAVY, ha="left", va="top", weight="bold")

    fig.tight_layout(pad=0.4)
    fig.savefig(output_path, facecolor="white", bbox_inches="tight", pad_inches=0.15)
    plt.close(fig)
    print("gerado:", output_path)


TITULOS = {
    1: "O domínio $D_h$: uma malha de pontos $z$",
    2: "Cada ponto recebe seu valor $f(z)$",
    3: "A fase de $f(z)$ aponta para uma cor na roda",
    4: "De volta ao domínio: cada ponto pintado com sua cor",
}

if __name__ == "__main__":
    for passo in (1, 2, 3, 4):
        montar_figura(passo, TITULOS[passo], OUT_DIR / f"mecanismo_passo{passo}.png")
