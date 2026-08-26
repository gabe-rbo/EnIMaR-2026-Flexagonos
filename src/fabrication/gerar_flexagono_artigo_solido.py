"""
Script de Geração do Flexágono com as Funções do Artigo em Cores Sólidas (Teorema Universal).
Desenvolvido para o EnIMaR 2026 e Artigo de Pesquisa.

Cada face representa exatamente uma das classes universais de funções invariantes do Teorema 5.1 do artigo:
- Face 1: Classe (0, 4) — J1(z) = z^4 (Órbifold C/C4) em 6 Setores Sólidos
- Face 2: Classe (1, 1) — J2(z) = exp(pi*i*z) - 1 (Faixa Periódica Conforme) em Grade Cartesiana
- Face 3: Classe (1, 2) — J3(z) = cos(pi*z) (Cosseno Invariante por Inversão C2) em Mosaico de Truchet
- Face 4: Classe (2, 2) — J4(z) = wp(z; 2*Z[i]) (Weierstrass Quadrado Lemniscático) em Tabuleiro de Xadrez
- Face 5: Classe (2, 3) — J5(z) = wp'(z; 2*Z[zeta3]) (Derivada de Weierstrass Triangular) em Alvos Concêntricos
- Face 6: Classe (2, 4) — J6(z) = wp(z; 2*Z[i])^2 (Quadrado de Weierstrass Quártico) em Favos de Mel

Gera todas as faces em 4K UHD (3840x3840 px) e as pranchas em 4840x4840 px.
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "core"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "visualization"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "fabrication"))

from domain_coloring import (
    DomainColoringEngine,
    PALETTE_SOLID_6,
    generate_cartesian_grid_texture,
    generate_checkerboard_texture,
    generate_concentric_targets_texture,
    generate_truchet_texture,
    generate_honeycomb_texture
)
from flexagon_domain_faces import gerar_planificacao_tetraflexagono
from wpgen import WP


def criar_painel_artigo(
    faces: dict,
    output_path: Path
):
    """Cria um painel comparativo 2x3 em alta resolução com as 6 funções fundamentais do artigo."""
    titles = {
        'face1': "Face 1: Classe (0, 4) — J1(z) = z^4 [Órbifold C/C4]",
        'face2': "Face 2: Classe (1, 1) — J2(z) = exp(pi*i*z) - 1 [Posto 1, C1]",
        'face3': "Face 3: Classe (1, 2) — J3(z) = cos(pi*z) [Posto 1, C2]",
        'face4': "Face 4: Classe (2, 2) — J4(z) = ℘(z; 2Z[i]) [Lemniscático, j=1728]",
        'face5': "Face 5: Classe (2, 3) — J5(z) = ℘'(z; 2Z[ζ3]) [Equianarmônico, j=0]",
        'face6': "Face 6: Classe (2, 4) — J6(z) = ℘(z; 2Z[i])^2 [Simetria p4 Quártica]"
    }

    face_w, face_h = 900, 900
    margin = 40
    header_h = 60
    panel_w = margin * 3 + face_w * 3
    panel_h = margin * 3 + (face_h + header_h) * 2

    panel = Image.new('RGB', (panel_w, panel_h), (242, 245, 250))
    draw = ImageDraw.Draw(panel)

    keys = ['face1', 'face2', 'face3', 'face4', 'face5', 'face6']

    for idx, key in enumerate(keys):
        row = idx // 3
        col = idx % 3
        x = margin + col * (face_w + margin)
        y = margin + row * (face_h + header_h + margin)

        title = titles.get(key, key)
        draw.text((x + 12, y + 16), title, fill=(15, 30, 55))

        face_img = faces[key].resize((face_w, face_h), Image.Resampling.LANCZOS)
        panel.paste(face_img, (x, y + header_h))
        draw.rectangle([(x, y + header_h), (x + face_w, y + header_h + face_h)], outline=(180, 195, 215), width=3)

    panel.save(output_path, "PNG")
    print(f"Painel comparativo das funções do artigo salvo em: {output_path}")


def main():
    out_dir = PROJECT_ROOT / "grafica" / "flexagono_artigo_solido"
    faces_dir = out_dir / "faces"
    faces_dir.mkdir(parents=True, exist_ok=True)

    resolution = (3840, 3840)
    print(">>> 1. Configurando Instâncias das Funções Elípticas de Weierstrass do Artigo...")

    # Reticulados fundamentais do Teorema 5.1
    # 1. Reticulado Lemniscático / Quadrado: Lambda_quad = 2 * Z[i] (w1 = 2, w2 = 2i)
    wp_quad = WP(2.0, 2.0j)

    # 2. Reticulado Equianarmônico / Triangular: Lambda_hex = 2 * Z[zeta_3] (w1 = 2, w2 = 1 + sqrt(3)j)
    wp_hex = WP(2.0, 1.0 + 1j * np.sqrt(3.0))

    faces = {}

    print(">>> 2. Renderizando as 6 Faces das Funções do Artigo em 4K UHD (3840x3840)...")

    # Face 1: Classe (0, 4) — J1(z) = z^4
    print(" - [1/6] Renderizando Face 1: Classe (0, 4) J1(z) = z^4 (6 Setores Sólidos)...")
    def f1(z):
        return z**4
    eng1 = DomainColoringEngine(func=f1, x_range=(-2.0, 2.0), y_range=(-2.0, 2.0), resolution=resolution)
    faces['face1'] = eng1.render(mode='solid_sectors', n_sectors=6, palette=PALETTE_SOLID_6)

    # Face 2: Classe (1, 1) — J2(z) = exp(pi*i*z) - 1
    print(" - [2/6] Renderizando Face 2: Classe (1, 1) J2(z) = exp(pi*i*z) - 1 (Grade Cartesiana)...")
    def f2(z):
        return np.exp(1j * np.pi * z) - 1.0
    eng2 = DomainColoringEngine(func=f2, x_range=(-2.0, 2.0), y_range=(-2.0, 2.0), resolution=resolution)
    faces['face2'] = eng2.render(mode='cartesian_grid', u_range=(-3.0, 3.0), v_range=(-3.0, 3.0), border_mode='wrap')

    # Face 3: Classe (1, 2) — J3(z) = cos(pi*z)
    print(" - [3/6] Renderizando Face 3: Classe (1, 2) J3(z) = cos(pi*z) (Mosaico de Truchet)...")
    def f3(z):
        return np.cos(np.pi * z)
    eng3 = DomainColoringEngine(func=f3, x_range=(-2.0, 2.0), y_range=(-2.0, 2.0), resolution=resolution)
    faces['face3'] = eng3.render(mode='truchet', u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap')

    # Face 4: Classe (2, 2) — J4(z) = wp(z; 2*Z[i])
    print(" - [4/6] Renderizando Face 4: Classe (2, 2) J4(z) = ℘(z; 2Z[i]) (Tabuleiro de Xadrez)...")
    def f4(z):
        z_safe = np.where(np.abs(z) < 1e-12, 1e-12, z)
        return wp_quad(z_safe)
    eng4 = DomainColoringEngine(func=f4, x_range=(-2.0, 2.0), y_range=(-2.0, 2.0), resolution=resolution)
    faces['face4'] = eng4.render(mode='checkerboard', u_range=(-4.0, 4.0), v_range=(-4.0, 4.0), border_mode='wrap')

    # Face 5: Classe (2, 3) — J5(z) = wp'(z; 2*Z[zeta3])
    print(" - [5/6] Renderizando Face 5: Classe (2, 3) J5(z) = ℘'(z; 2Z[ζ3]) (Alvos Concêntricos)...")
    def f5(z):
        z_safe = np.where(np.abs(z) < 1e-12, 1e-12, z)
        return wp_hex.deriv(z_safe)
    eng5 = DomainColoringEngine(func=f5, x_range=(-2.0, 2.0), y_range=(-2.0, 2.0), resolution=resolution)
    faces['face5'] = eng5.render(mode='concentric_targets', n_rings=10, u_range=(-6.0, 6.0), v_range=(-6.0, 6.0), border_mode='wrap')

    # Face 6: Classe (2, 4) — J6(z) = wp(z; 2*Z[i])^2
    print(" - [6/6] Renderizando Face 6: Classe (2, 4) J6(z) = ℘(z; 2Z[i])^2 (Favos de Mel Hexagonais)...")
    def f6(z):
        z_safe = np.where(np.abs(z) < 1e-12, 1e-12, z)
        p_val = wp_quad(z_safe)
        return p_val**2
    eng6 = DomainColoringEngine(func=f6, x_range=(-2.0, 2.0), y_range=(-2.0, 2.0), resolution=resolution)
    faces['face6'] = eng6.render(mode='honeycomb', u_range=(-8.0, 8.0), v_range=(-8.0, 8.0), border_mode='wrap')

    # Salvando as 6 faces individuais em 4K
    face_paths = []
    for i in range(1, 7):
        key = f'face{i}'
        p = faces_dir / f"face{i}.png"
        faces[key].save(p, "PNG")
        face_paths.append(str(p))
        print(f"   [OK] Salva {key} (4K UHD): {p}")

    print(">>> 3. Gerando Painel Comparativo das Funções do Artigo...")
    painel_path = out_dir / "painel_6_faces_artigo.png"
    criar_painel_artigo(faces, painel_path)

    print(">>> 4. Montando Planificações de Impressão (Tetraflexágono do Artigo 4840x4840)...")
    frontal_path = out_dir / "Plano_Frontal_ArtigoSolido.png"
    traseiro_path = out_dir / "Plano_Traseiro_ArtigoSolido.png"
    gerar_planificacao_tetraflexagono(
        faces_paths=face_paths,
        output_frontal=frontal_path,
        output_traseiro=traseiro_path,
        grafica=True,
        scale_factor=2
    )

    # README da seção
    readme_path = out_dir / "README.md"
    readme_content = """# Flexágono das Funções do Artigo (Teorema Universal da Invariância)

Neste flexágono, **cada uma das 6 faces é rigorosamente uma das soluções fundamentais do Teorema Universal de Classificação (Teorema 5.1 do artigo)**, renderizada em **Cores Sólidas e 4K UHD** (3840×3840 px).

---

## Tabela de Correspondência com o Artigo Científico

| Face | Classe no Artigo | Hauptmodul / Função Invariante | Reticulado $\\Lambda$ e Grupo | Padrão em Cores Sólidas |
| :---: | :---: | :--- | :--- | :--- |
| **1** | **$(0, 4)$** | $J_1(z) = z^4$ | Posto $0$, Grupo Cíclico $C_4$ | **6 Setores Angulares Puros** |
| **2** | **$(1, 1)$** | $J_2(z) = \\exp(\\pi i z) - 1$ | Posto $1$, Translação $\\mathbb{Z}$ | **Grade Cartesiana Ortogonal** |
| **3** | **$(1, 2)$** | $J_3(z) = \\cos(\\pi z)$ | Posto $1$, Inversão $C_2$ ($D_1$) | **Mosaico de Arcos de Truchet** |
| **4** | **$(2, 2)$** | $J_4(z) = \\wp(z; 2\\mathbb{Z}[i])$ | Posto $2$, $\\mathbb{Z}[i]$ ($g_3=0, j=1728$) | **Tabuleiro de Xadrez Conforme** |
| **5** | **$(2, 3)$** | $J_5(z) = \\wp'(z; 2\\mathbb{Z}[\\zeta_3])$ | Posto $2$, $\\mathbb{Z}[\\zeta_3]$ ($g_2=0, j=0$) | **Alvos Concêntricos (10 Anéis)** |
| **6** | **$(2, 4)$** | $J_6(z) = \\wp(z; 2\\mathbb{Z}[i])^2$ | Posto $2$, Simetria Quártica $p4$ | **Favos de Mel Hexagonais** |

---

## Arquivos Prontos para a Gráfica

- **Painel Geral:** [`painel_6_faces_artigo.png`](painel_6_faces_artigo.png)
- **Plano Frontal (Frente 4840x4840):** [`Plano_Frontal_ArtigoSolido.png`](Plano_Frontal_ArtigoSolido.png)
- **Plano Traseiro (Verso 4840x4840):** [`Plano_Traseiro_ArtigoSolido.png`](Plano_Traseiro_ArtigoSolido.png)
"""
    readme_path.write_text(readme_content, encoding="utf-8")

    print(f"\n>>> SUCESSO! Todos os arquivos do Flexágono do Artigo foram gerados em:\n{out_dir}")


if __name__ == '__main__':
    main()
