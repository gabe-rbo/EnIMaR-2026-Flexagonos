"""
Script de Geração do Flexágono Exclusivo de Cores Sólidas e Padrões Geométricos (Pullback).
Desenvolvido para o EnIMaR 2026.

Gera:
1. As 6 faces em cores sólidas / padrões geométricos (1124x1124 px).
2. O painel comparativo 2x3.
3. As pranchas de corte e impressão (Plano_Frontal_CoresSolidas.png e Plano_Traseiro_CoresSolidas.png).
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "visualization"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "fabrication"))

from domain_coloring import DomainColoringEngine, PALETTE_SOLID_6
from flexagon_domain_faces import gerar_planificacao_tetraflexagono


def criar_painel_comparativo_solidas(
    faces: dict,
    output_path: Path
):
    """Cria um mosaico comparativo 2x3 com as 6 faces de cores sólidas e legendas."""
    titles = {
        'face1': "Face 1: 6 Setores Angulares Puros",
        'face2': "Face 2: Grade Cartesiana Ortogonal",
        'face3': "Face 3: Tabuleiro de Xadrez Conforme",
        'face4': "Face 4: Xadrez Polar Sólido",
        'face5': "Face 5: Alvos Concêntricos Sólidos",
        'face6': "Face 6: Mosaico de Truchet Conforme"
    }

    face_w, face_h = 600, 600
    margin = 30
    header_h = 50
    panel_w = margin * 3 + face_w * 3
    panel_h = margin * 3 + (face_h + header_h) * 2

    panel = Image.new('RGB', (panel_w, panel_h), (245, 247, 250))
    draw = ImageDraw.Draw(panel)

    keys = ['face1', 'face2', 'face3', 'face4', 'face5', 'face6']

    for idx, key in enumerate(keys):
        row = idx // 3
        col = idx % 3
        x = margin + col * (face_w + margin)
        y = margin + row * (face_h + header_h + margin)

        title = titles.get(key, key)
        draw.text((x + 10, y + 12), title, fill=(20, 35, 60))

        face_img = faces[key].resize((face_w, face_h), Image.Resampling.LANCZOS)
        panel.paste(face_img, (x, y + header_h))
        draw.rectangle([(x, y + header_h), (x + face_w, y + header_h + face_h)], outline=(190, 205, 225), width=2)

    panel.save(output_path, "PNG")
    print(f"Painel comparativo salvo em: {output_path}")


def main():
    out_dir = PROJECT_ROOT / "grafica" / "flexagono_cores_solidas"
    faces_dir = out_dir / "faces"
    faces_dir.mkdir(parents=True, exist_ok=True)

    print(">>> 1. Configurando Motor de Coloração de Domínio (Cores Sólidas)...")
    # Função modelo clássica rica em zeros e polos: f(z) = (z-1)/(z^2 + z + 1)
    def f(z):
        return (z - 1.0) / (z**2 + z + 1.0)

    engine = DomainColoringEngine(
        func=f,
        x_range=(-2.2, 2.2),
        y_range=(-2.2, 2.2),
        resolution=(3840, 3840)
    )

    print(">>> 2. Renderizando as 6 Faces em Cores Sólidas e Pullbacks em 4K UHD (3840x3840)...")
    faces = engine.generate_six_solid_faces(
        custom_palette=PALETTE_SOLID_6,
        texture_u_range=(-2.5, 2.5),
        texture_v_range=(-2.5, 2.5),
        texture_mode='wrap'
    )

    face_paths = []
    for i in range(1, 7):
        key = f'face{i}'
        p = faces_dir / f"face{i}.png"
        faces[key].save(p, "PNG")
        face_paths.append(str(p))
        print(f" - Salva {key} (4K): {p}")

    print(">>> 3. Gerando Painel Comparativo 2x3...")
    painel_path = out_dir / "painel_6_faces_cores_solidas.png"
    criar_painel_comparativo_solidas(faces, painel_path)

    print(">>> 4. Montando Planificações de Impressão (Tetraflexágono de Cores Sólidas 4840x4840)...")
    frontal_path = out_dir / "Plano_Frontal_CoresSolidas.png"
    traseiro_path = out_dir / "Plano_Traseiro_CoresSolidas.png"
    gerar_planificacao_tetraflexagono(
        faces_paths=face_paths,
        output_frontal=frontal_path,
        output_traseiro=traseiro_path,
        grafica=True,
        scale_factor=2
    )

    # Gerar também o README da pasta
    readme_path = out_dir / "README.md"
    readme_content = f"""# Flexágono de Cores Sólidas e Padrões Geométricos

Flexágono da mesma função $f(z) = \\frac{{z-1}}{{z^2+z+1}}$ gerado com 6 visões puramente em **Cores Sólidas, Discretização e Pullbacks Conformes** (sem gradientes contínuos).

---

## As 6 Faces

1. **Face 1 — 6 Setores Angulares Sólidos:** Discretização de $\\arg(w)$ em 6 cores puras (Vermelho, Amarelo, Verde, Ciano, Azul, Magenta).
2. **Face 2 — Grade Cartesiana Ortogonal:** Pullback da malha cartesiana no plano $w$, evidenciando a conformidade e a preservação de ângulos retos.
3. **Face 3 — Tabuleiro de Xadrez Conforme:** Tabuleiro de xadrez cartesiano de alto contraste deformado pelas singularidades.
4. **Face 4 — Xadrez Polar Sólido:** Discretização combinada de anéis concêntricos $\\log|w|$ e raios angulares.
5. **Face 5 — Alvos Concêntricos Sólidos:** Anéis concêntricos coloridos mapeados para as curvas de nível de magnitude.
6. **Face 6 — Mosaico de Truchet Conforme:** Padrão de arcos e rosetas de Truchet com cores sólidas (ligação com o artigo de Truchet/Hall et al. 2020).

---

## Arquivos de Impressão para a Gráfica

- **Painel Geral:** [`painel_6_faces_cores_solidas.png`](painel_6_faces_cores_solidas.png)
- **Plano Frontal (Frente):** [`Plano_Frontal_CoresSolidas.png`](Plano_Frontal_CoresSolidas.png)
- **Plano Traseiro (Verso):** [`Plano_Traseiro_CoresSolidas.png`](Plano_Traseiro_CoresSolidas.png)
"""
    readme_path.write_text(readme_content, encoding="utf-8")

    print(f"\n>>> SUCESSO! Todos os arquivos gráficos de Cores Sólidas foram gerados em:\n{out_dir}")


if __name__ == '__main__':
    main()
