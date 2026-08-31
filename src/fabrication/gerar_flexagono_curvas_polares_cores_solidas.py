"""
Script de Geração do Flexágono de Curvas Polares em Cores Sólidas (Borboleta, Estrela, Rosáceas,
Flor de Lótus). Desenvolvido para o EnIMaR 2026.

As 6 curvas e o esquema de cores reproduzem exatamente `pesquisa/notebooks/imagens_curvas_polares.ipynb`
(células individuais de renderização de cada face) — fonte de verdade confirmada com a Aniura.

Gera:
1. As 6 imagens individuais em 4K UHD (3840x3840 px).
2. O painel comparativo 2x3 com todas as 6 curvas anotadas.
3. As pranchas de impressão gráfica com sangrias e marcas de registro (Plano Frontal e Plano Traseiro).
"""

import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "visualization"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "fabrication"))

from flexagon_domain_faces import gerar_planificacao_tetraflexagono, gerar_diagrama_dinamica, desenhar_titulo_painel

RESOLUCAO_4K = 3840
FIGSIZE_POL = 9.6  # polegadas; FIGSIZE_POL * DPI = RESOLUCAO_4K
DPI = RESOLUCAO_4K / FIGSIZE_POL


def _nova_figura_polar(facecolor: str):
    fig, ax = plt.subplots(figsize=(FIGSIZE_POL, FIGSIZE_POL), subplot_kw={'projection': 'polar'})
    fig.set_facecolor(facecolor)
    return fig, ax


def _finalizar_e_salvar(fig, ax, output_path: Path, rorigin=None, rmax=None):
    if rorigin is not None:
        ax.set_rorigin(rorigin)
    if rmax is not None:
        ax.set_rmax(rmax)
    ax.axis("off")
    ax.set_xticklabels([])
    ax.set_yticklabels([])
    ax.grid(False)
    fig.savefig(output_path, dpi=DPI, facecolor=fig.get_facecolor())
    plt.close(fig)


def gerar_face_borboleta(output_path: Path):
    """Face 1 — Borboleta: r = (e^sen(theta) - 2cos(4theta) + sen^5((2theta-pi)/24)) / 2.3"""
    fig, ax = _nova_figura_polar('dodgerblue')
    theta = np.linspace(0, 24 * np.pi, 2000)
    r = (np.exp(np.sin(theta)) - 2 * np.cos(4 * theta) + np.sin((2 * theta - np.pi) / 24) ** 5) / 2.3
    ax.fill(theta + (r < 0) * np.pi, np.abs(r), color='dodgerblue', lw=1)
    ax.fill(theta, r, lw=2, color='fuchsia')
    ax.fill(theta + np.pi, -r, lw=2, color='fuchsia')
    ax.plot(theta, r, lw=1, color='lightcyan')
    ax.plot(theta + np.pi, -r, lw=1, color='lightcyan')
    _finalizar_e_salvar(fig, ax, output_path, rorigin=-0.5)


def gerar_face_estrela(output_path: Path):
    """Face 2 — Estrela: r = sen^2(1.2 theta) + cos^3(6 theta)"""
    fig, ax = _nova_figura_polar('magenta')
    theta = np.linspace(0, 10 * np.pi, 1000)
    r = np.sin(1.2 * theta) ** 2 + np.cos(6 * theta) ** 3
    ax.plot(theta + (r < 0) * np.pi, np.abs(r), lw=2, color='lavender')
    ax.fill(theta + (r < 0) * np.pi, np.abs(r), lw=2, color='cornflowerblue')
    _finalizar_e_salvar(fig, ax, output_path, rorigin=0)


def gerar_face_rosacea_3petalas(output_path: Path):
    """Face 3 — Rosácea de três pétalas: r = 2cos(3 theta)"""
    fig, ax = _nova_figura_polar('blue')
    theta = np.linspace(0, np.pi, 700)
    r = 2 * np.cos(3 * theta)
    ax.fill(theta + (r < 0) * np.pi, np.abs(r), color='mediumseagreen')
    _finalizar_e_salvar(fig, ax, output_path, rorigin=0)


def gerar_face_rosaceas_4petalas(output_path: Path):
    """Face 4 — Rosáceas de quatro pétalas: r = 2cos(2 theta) (azul) sobreposta a r = cos(2 theta) (vermelho)"""
    fig, ax = _nova_figura_polar('mediumseagreen')
    theta = np.linspace(0, 2 * np.pi, 500)
    r = 2 * np.cos(2 * theta)
    ax.fill(theta + (r < 0) * np.pi, np.abs(r), color='blue')
    r = np.cos(2 * theta)
    ax.fill(theta + (r < 0) * np.pi, np.abs(r), color='red')
    _finalizar_e_salvar(fig, ax, output_path, rorigin=0)


def gerar_face_flor_de_lotus(output_path: Path):
    """Face 5 — Flor de lótus: r = sen(theta) + sen^3(5theta/2), deslocada verticalmente em -0.7"""
    fig, ax = _nova_figura_polar('dodgerblue')
    theta = np.linspace(0, 4 * np.pi, 1000)
    r = np.sin(theta) + np.sin(5 * theta / 2) ** 3
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    y_deslocado = y + (-0.7)
    r_novo = np.sqrt(x ** 2 + y_deslocado ** 2)
    theta_novo = np.arctan2(y_deslocado, x) % (2 * np.pi)
    ax.plot(theta_novo, r_novo, lw=2, color='lavender')
    ax.fill(theta_novo, r_novo, lw=1, color='violet')
    _finalizar_e_salvar(fig, ax, output_path, rorigin=0)


def gerar_face_rosacea_fracionaria(output_path: Path):
    """Face 6 — Rosácea com fração no coeficiente: r = 2cos(2.05 theta)"""
    fig, ax = _nova_figura_polar('mediumseagreen')
    theta = np.linspace(-np.pi, 20 * np.pi / 2.05 + np.pi, 1000)
    r = 2 * np.cos(2.05 * theta)
    ax.plot(theta + (r < 0) * np.pi, np.abs(r), color='lightskyblue', lw=2)
    _finalizar_e_salvar(fig, ax, output_path, rorigin=0, rmax=2.1)


GERADORES_FACES = [
    ("face1", "Borboleta", gerar_face_borboleta),
    ("face2", "Estrela", gerar_face_estrela),
    ("face3", "Rosácea de 3 Pétalas", gerar_face_rosacea_3petalas),
    ("face4", "Rosáceas de 4 Pétalas", gerar_face_rosaceas_4petalas),
    ("face5", "Flor de Lótus", gerar_face_flor_de_lotus),
    ("face6", "Rosácea Fracionária", gerar_face_rosacea_fracionaria),
]


def criar_painel_comparativo_curvas_polares(faces: dict, output_path: Path):
    """Cria um mosaico comparativo 2x3 com as 6 curvas polares e legendas."""
    titles = {chave: f"Face {chave[-1]}: {nome}" for chave, nome, _ in GERADORES_FACES}

    face_w, face_h = 600, 600
    margin = 30
    header_h = 50
    panel_w = margin * 3 + face_w * 3
    panel_h = margin * 3 + (face_h + header_h) * 2

    panel = Image.new('RGB', (panel_w, panel_h), (245, 247, 250))
    draw = ImageDraw.Draw(panel)

    keys = [chave for chave, _, _ in GERADORES_FACES]

    for idx, key in enumerate(keys):
        row = idx // 3
        col = idx % 3
        x = margin + col * (face_w + margin)
        y = margin + row * (face_h + header_h + margin)

        title = titles.get(key, key)
        desenhar_titulo_painel(draw, title, (x + 10, y + 12), largura_max=face_w - 20, tamanho_inicial=18, cor=(20, 35, 60))

        face_img = faces[key].resize((face_w, face_h), Image.Resampling.LANCZOS)
        panel.paste(face_img, (x, y + header_h))
        draw.rectangle([(x, y + header_h), (x + face_w, y + header_h + face_h)], outline=(190, 205, 225), width=2)

    panel.save(output_path, "PNG")
    print(f"Painel comparativo salvo em: {output_path}")


def main():
    out_dir = PROJECT_ROOT / "grafica" / "flexagonos_curvas_polares_cores_solidas"
    faces_dir = out_dir / "faces"
    faces_dir.mkdir(parents=True, exist_ok=True)

    print(">>> 1. Renderizando as 6 Curvas Polares em 4K UHD (3840x3840)...")
    faces = {}
    face_paths = []
    for chave, nome, gerador in GERADORES_FACES:
        p = faces_dir / f"{chave}.png"
        gerador(p)
        faces[chave] = Image.open(p).convert("RGB")
        face_paths.append(str(p))
        print(f" - Salva {chave} ({nome}, 4K): {p}")

    print(">>> 2. Gerando Painel Comparativo 2x3...")
    painel_path = out_dir / "painel_6_faces_curvas_polares.png"
    criar_painel_comparativo_curvas_polares(faces, painel_path)

    print(">>> 3. Montando Planificações de Impressão (Tetraflexágono em Ultra-Alta Definição 4840x4840)...")
    frontal_path = out_dir / "Plano_Frontal_CurvasPolares.png"
    traseiro_path = out_dir / "Plano_Traseiro_CurvasPolares.png"
    gerar_planificacao_tetraflexagono(
        faces_paths=face_paths,
        output_frontal=frontal_path,
        output_traseiro=traseiro_path,
        trocar_3com5_4com6=True,
        grafica=True,
        scale_factor=2,
        watermark=True
    )

    print(">>> 4. Gerando Diagrama de Dinâmica (flexão) em 4K...")
    diagrama_path = out_dir / "Diagrama_Dinamica_CurvasPolares.png"
    gerar_diagrama_dinamica(face_paths, diagrama_path)

    readme_path = out_dir / "README.md"
    readme_content = """# Flexágono de Curvas Polares em Cores Sólidas

Flexágono com 6 curvas clássicas em coordenadas polares (Borboleta, Estrela, Rosáceas e Flor de
Lótus), reproduzindo exatamente as fórmulas e o esquema de cores de
`pesquisa/notebooks/imagens_curvas_polares.ipynb`.

---

## As 6 Faces

1. **Borboleta** — $r = \\frac{e^{\\sin\\theta} - 2\\cos(4\\theta) + \\sin^5((2\\theta-\\pi)/24)}{2.3}$
2. **Estrela** — $r = \\sin^2(1.2\\theta) + \\cos^3(6\\theta)$
3. **Rosácea de 3 Pétalas** — $r = 2\\cos(3\\theta)$
4. **Rosáceas de 4 Pétalas** — $r = 2\\cos(2\\theta)$ sobreposta a $r = \\cos(2\\theta)$
5. **Flor de Lótus** — $r = \\sin\\theta + \\sin^3(5\\theta/2)$, deslocada verticalmente
6. **Rosácea Fracionária** — $r = 2\\cos(2.05\\theta)$

---

## Arquivos de Impressão para a Gráfica

- **Painel Geral:** [`painel_6_faces_curvas_polares.png`](painel_6_faces_curvas_polares.png)
- **Plano Frontal (Frente):** [`Plano_Frontal_CurvasPolares.png`](Plano_Frontal_CurvasPolares.png)
- **Plano Traseiro (Verso):** [`Plano_Traseiro_CurvasPolares.png`](Plano_Traseiro_CurvasPolares.png)
- **Diagrama de Dinâmica (flexão, 4K):** [`Diagrama_Dinamica_CurvasPolares.png`](Diagrama_Dinamica_CurvasPolares.png)
"""
    readme_path.write_text(readme_content, encoding="utf-8")

    print(f"\n>>> SUCESSO! Todos os arquivos gráficos de Curvas Polares foram gerados em:\n{out_dir}")


if __name__ == '__main__':
    main()
