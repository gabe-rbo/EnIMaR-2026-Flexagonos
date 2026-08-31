"""
Script de Geração do Flexágono "Galeria Matemática de Cores Sólidas".
Desenvolvido para o EnIMaR 2026.

Cada uma das 6 faces representa um objeto matemático e padrão geométrico COMPLETAMENTE DIFERENTE:
- Face 1: Estrela Floral de 6 Raízes da Unidade (f(z) = z^6 - 1) em 6 Setores Sólidos
- Face 2: Espirais Periódicas de Wegert (f(z) = exp(z) - 1) em Grade Cartesiana Conforme
- Face 3: Labirinto de Nós e Arcos de Truchet (f(z) = (z^2 - 1)/(z^2 + 1)) em Mosaico de Truchet
- Face 4: Lâminas Hiperbólicas de Joukowsky (f(z) = 0.5*(z + 1/z)) em Tabuleiro de Xadrez
- Face 5: Alvo Conforme de Triplo Polo (f(z) = (z^3 - 1)/(z^3 + 1)) em 10 Anéis Concêntricos
- Face 6: Tesselação de Favos de Mel (f(z) = (z^4 + 1)/(z^4 - 1)) em Ladrilhamento Hexagonal

Gera em 4K UHD (3840x3840) e pranchas gráficas em 4840x4840.
"""

import sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
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
from flexagon_domain_faces import gerar_planificacao_tetraflexagono, gerar_diagrama_dinamica, desenhar_titulo_painel


def criar_painel_galeria(
    faces: dict,
    output_path: Path
):
    """Cria um painel comparativo 2x3 em alta resolução com as 6 faces heterogêneas."""
    titles = {
        'face1': "Face 1: Estrela Floral de Raízes (z^6 - 1) — 6 Setores Sólidos",
        'face2': "Face 2: Faixas Periódicas (exp(z) - 1) — Grade Cartesiana",
        'face3': "Face 3: Labirinto Conforme ((z^2-1)/(z^2+1)) — Mosaico de Truchet",
        'face4': "Face 4: Lâminas de Joukowsky (0.5*(z+1/z)) — Xadrez Conforme",
        'face5': "Face 5: Triplo Polo ((z^3-1)/(z^3+1)) — Alvos Concêntricos",
        'face6': "Face 6: Quadrupolo ((z^4+1)/(z^4-1)) — Favos de Mel Hexagonais"
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
        desenhar_titulo_painel(draw, title, (x + 12, y + 16), largura_max=face_w - 24, tamanho_inicial=20, cor=(15, 30, 55))

        face_img = faces[key].resize((face_w, face_h), Image.Resampling.LANCZOS)
        panel.paste(face_img, (x, y + header_h))
        draw.rectangle([(x, y + header_h), (x + face_w, y + header_h + face_h)], outline=(180, 195, 215), width=3)

    panel.save(output_path, "PNG")
    print(f"Painel comparativo da galeria salvo em: {output_path}")


def main():
    out_dir = PROJECT_ROOT / "grafica" / "flexagono_galeria_solida"
    faces_dir = out_dir / "faces"
    faces_dir.mkdir(parents=True, exist_ok=True)

    resolution = (3840, 3840)
    print(">>> 1. Renderizando as 6 Faces Heterogêneas em Cores Sólidas (4K UHD 3840x3840)...")

    faces = {}

    # Face 1: Raízes da Unidade (z^6 - 1)
    print(" - Gerando Face 1: Estrela Floral de Raízes (z^6 - 1)...")
    eng1 = DomainColoringEngine(func=lambda z: z**6 - 1.0, x_range=(-1.8, 1.8), y_range=(-1.8, 1.8), resolution=resolution)
    faces['face1'] = eng1.render(mode='solid_sectors', n_sectors=6, palette=PALETTE_SOLID_6)

    # Face 2: Mapeamento Exponencial Periódico (exp(z) - 1)
    print(" - Gerando Face 2: Espirais Periódicas de Wegert (exp(z) - 1)...")
    eng2 = DomainColoringEngine(func=lambda z: np.exp(z) - 1.0, x_range=(-2.5, 2.5), y_range=(-2.5, 2.5), resolution=resolution)
    faces['face2'] = eng2.render(mode='cartesian_grid', u_range=(-3.0, 3.0), v_range=(-3.0, 3.0), border_mode='wrap')

    # Face 3: Labirinto de Truchet Conforme ((z^2-1)/(z^2+1))
    print(" - Gerando Face 3: Labirinto de Arcos de Truchet ((z^2-1)/(z^2+1))...")
    eng3 = DomainColoringEngine(func=lambda z: (z**2 - 1.0) / (z**2 + 1.0), x_range=(-2.2, 2.2), y_range=(-2.2, 2.2), resolution=resolution)
    faces['face3'] = eng3.render(mode='truchet', u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap')

    # Face 4: Lâminas de Joukowsky (0.5*(z + 1/z))
    print(" - Gerando Face 4: Transformação de Joukowsky em Xadrez (0.5*(z + 1/z))...")
    eng4 = DomainColoringEngine(func=lambda z: 0.5 * (z + 1.0 / np.where(z == 0, 1e-15, z)), x_range=(-2.4, 2.4), y_range=(-2.4, 2.4), resolution=resolution)
    faces['face4'] = eng4.render(mode='checkerboard', u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap')

    # Face 5: Triplo Polo em Alvos Concêntricos ((z^3-1)/(z^3+1))
    print(" - Gerando Face 5: Alvo de Triplo Polo ((z^3-1)/(z^3+1))...")
    eng5 = DomainColoringEngine(func=lambda z: (z**3 - 1.0) / (z**3 + 1.0), x_range=(-2.2, 2.2), y_range=(-2.2, 2.2), resolution=resolution)
    faces['face5'] = eng5.render(mode='concentric_targets', n_rings=10, u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap')

    # Face 6: Quadrupolo em Favos de Mel Hexagonais ((z^4+1)/(z^4-1))
    print(" - Gerando Face 6: Tesselação de Favos de Mel ((z^4+1)/(z^4-1))...")
    eng6 = DomainColoringEngine(func=lambda z: (z**4 + 1.0) / (z**4 - 1.0), x_range=(-2.2, 2.2), y_range=(-2.2, 2.2), resolution=resolution)
    faces['face6'] = eng6.render(mode='honeycomb', u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap')

    # Salvando faces individuais
    face_paths = []
    for i in range(1, 7):
        key = f'face{i}'
        p = faces_dir / f"face{i}.png"
        faces[key].save(p, "PNG")
        face_paths.append(str(p))
        print(f"   [OK] Salva {key} (4K UHD): {p}")

    print(">>> 2. Gerando Painel Comparativo da Galeria...")
    painel_path = out_dir / "painel_6_faces_galeria.png"
    criar_painel_galeria(faces, painel_path)

    print(">>> 3. Montando Planificações de Impressão (Tetraflexágono Galeria 4840x4840)...")
    frontal_path = out_dir / "Plano_Frontal_GaleriaSolida.png"
    traseiro_path = out_dir / "Plano_Traseiro_GaleriaSolida.png"
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
    diagrama_path = out_dir / "Diagrama_Dinamica_GaleriaSolida.png"
    gerar_diagrama_dinamica(face_paths, diagrama_path)

    # README da seção
    readme_path = out_dir / "README.md"
    readme_content = f"""# Flexágono Galeria Matemática de Cores Sólidas

Neste flexágono, **cada uma das 6 faces é um objeto matemático e padrão geométrico completamente diferente**, renderizado em **Cores Sólidas e 4K UHD** (3840×3840 px).

---

## As 6 Faces da Galeria

| Face | Função Matemática | Padrão Geométrico no Plano $w$ | Propriedade Visual / Teórica |
| :---: | :--- | :--- | :--- |
| **1** | $f(z) = z^6 - 1$ | **6 Setores Angulares Puros** | Estrela floral com 6 zeros simétricos na circunferência unitária |
| **2** | $f(z) = \\exp(z) - 1$ | **Grade Cartesiana Ortogonal** | Faixas periódicas horizontais conformes (Teorema 2.4 de Wegert) |
| **3** | $f(z) = \\frac{{z^2 - 1}}{{z^2 + 1}}$ | **Mosaico de Arcos de Truchet** | Labirinto contínuo conectando 2 zeros e 2 polos ortogonais |
| **4** | $f(z) = \\frac{{1}}{{2}}\\left(z + \\frac{{1}}{{z}}\\right)$ | **Tabuleiro de Xadrez** | Transformação de aerofólio de Joukowsky com ramificações em $\\pm 1$ |
| **5** | $f(z) = \\frac{{z^3 - 1}}{{z^3 + 1}}$ | **Alvos Concêntricos (10 Anéis)** | 3 fontes circulares nos zeros e 3 ilhas nos polos |
| **6** | $f(z) = \\frac{{z^4 + 1}}{{z^4 - 1}}$ | **Favos de Mel Hexagonais** | Tesselação hexagonal multicor deformada em quadrupolo $C_4$ |

---

## Arquivos Prontos para a Gráfica

- **Painel Geral:** [`painel_6_faces_galeria.png`](painel_6_faces_galeria.png)
- **Plano Frontal (Frente 4840x4840):** [`Plano_Frontal_GaleriaSolida.png`](Plano_Frontal_GaleriaSolida.png)
- **Plano Traseiro (Verso 4840x4840):** [`Plano_Traseiro_GaleriaSolida.png`](Plano_Traseiro_GaleriaSolida.png)
- **Diagrama de Dinâmica (flexão, 4K):** [`Diagrama_Dinamica_GaleriaSolida.png`](Diagrama_Dinamica_GaleriaSolida.png)
"""
    readme_path.write_text(readme_content, encoding="utf-8")

    print(f"\n>>> SUCESSO! Todos os arquivos da Galeria de Cores Sólidas foram gerados em:\n{out_dir}")


if __name__ == '__main__':
    main()
