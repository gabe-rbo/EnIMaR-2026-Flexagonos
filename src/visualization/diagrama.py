"""
diagrama.py -- desenha o diagrama de flexao ("mecanica") de um flexagono com as
imagens das faces encaixadas nas caixas, no lugar dos rotulos 1a,1b,...
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, FancyArrowPatch, Arc

from mecanica import POS_LETRA


def rearranja(img, palavra):
    """img: array (N,N,3).  palavra: 4 letras, a peca que fica em cada posicao
       na ordem TL, TR, BL, BR.  Peca 'a'=TL da imagem original, 'b'=TR,
       'c'=BL, 'd'=BR."""
    n = img.shape[0] // 2
    pecas = {'a': img[:n, :n], 'b': img[:n, n:], 'c': img[n:, :n], 'd': img[n:, n:]}
    top = np.concatenate([pecas[palavra[0]], pecas[palavra[1]]], axis=1)
    bot = np.concatenate([pecas[palavra[2]], pecas[palavra[3]]], axis=1)
    return np.concatenate([top, bot], axis=0)


def desenha(spec, imagens, saida, dpi=170, cor_borda="#222222"):
    """imagens: dict face -> array quadrado (N,N,3) uint8."""
    nos = spec["nos"]; arestas = spec["arestas"]
    W = 1.0                                   # lado da caixa
    xs = [v[0] for v in nos.values()]; ys = [v[1] for v in nos.values()]
    x0, x1 = min(xs) - .18, max(xs) + W + .18
    y0, y1 = min(ys) - .12, max(ys) + W + .12

    fig_w = 11.0
    fig = plt.figure(figsize=(fig_w, fig_w * (y1 - y0) / (x1 - x0)))
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(x0, x1); ax.set_ylim(y0, y1)
    ax.set_aspect('equal'); ax.axis('off')

    centro = {}
    for nome, (x, y, estilo) in nos.items():
        face, palavra = nome.split(':')
        face = int(face) if face.isdigit() else face
        img = rearranja(imagens[face], palavra)
        ax.imshow(img, extent=[x, x + W, y, y + W], zorder=2,
                  interpolation='antialiased')
        ax.add_patch(Rectangle((x, y), W, W, fill=False, zorder=3,
                               linewidth=1.6, edgecolor=cor_borda,
                               linestyle='-' if estilo == 's' else (0, (4, 3))))
        # linhas dos cortes
        ax.plot([x + W/2, x + W/2], [y, y + W], color='white', lw=1.1, zorder=4)
        ax.plot([x, x + W], [y + W/2, y + W/2], color='white', lw=1.1, zorder=4)
        ax.text(x + .055, y + W - .055, str(face), ha='left', va='top',
                fontsize=9.5, color=cor_borda, zorder=6,
                fontweight='bold' if estilo == 's' else 'normal',
                bbox=dict(boxstyle='square,pad=0.16', fc='white',
                          ec=cor_borda, lw=0.7,
                          ls='-' if estilo == 's' else (0, (2, 2))))
        centro[nome] = (x + W/2, y + W/2)

    def borda(p, q):
        """ponto na borda da caixa de centro p na direcao de q."""
        (px, py), (qx, qy) = p, q
        dx, dy = qx - px, qy - py
        if abs(dx) >= abs(dy):
            t = (W/2 + .04) / abs(dx);
        else:
            t = (W/2 + .04) / abs(dy)
        return px + dx*t, py + dy*t

    for A, B, estilo, rot in arestas:
        pa, pb = centro[A], centro[B]
        a1 = borda(pa, pb); b1 = borda(pb, pa)
        dx, dy = b1[0]-a1[0], b1[1]-a1[1]
        n = (dy, -dx); ln = (n[0]**2+n[1]**2)**.5
        off = (0.055*n[0]/ln, 0.055*n[1]/ln) if estilo == 'b' else (0, 0)
        def seta(p, q, ls, o=(0, 0)):
            ax.add_patch(FancyArrowPatch((p[0]+o[0], p[1]+o[1]),
                                         (q[0]+o[0], q[1]+o[1]),
                                         arrowstyle='-|>', mutation_scale=13,
                                         linewidth=1.3, color=cor_borda,
                                         linestyle=ls, zorder=1,
                                         shrinkA=0, shrinkB=0))
        if estilo == 's':
            seta(a1, b1, '-')
        elif estilo == 'd':
            seta(a1, b1, (0, (4, 3)))
        else:
            seta(a1, b1, '-', off)
            seta(b1, a1, (0, (4, 3)), (-off[0], -off[1]))
        if rot:
            mx, my = (a1[0]+b1[0])/2, (a1[1]+b1[1])/2
            ux, uy = n[0]/ln, n[1]/ln
            ax.text(mx + 0.24*ux, my + 0.24*uy, r'$\circlearrowright$',
                    ha='center', va='center', fontsize=15, color='#909090',
                    zorder=5)

    fig.savefig(saida, dpi=dpi, facecolor='white')
    plt.close(fig)
    return saida
