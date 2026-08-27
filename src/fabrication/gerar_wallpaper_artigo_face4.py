"""
Script de Geração do Wallpaper 4K UHD para Desktop (16:9 - 3840x2160 px)
da Face 4 do Flexágono do Artigo (Função Elíptica de Weierstrass em Tabuleiro de Xadrez).

Aumenta a área de tesselagem para cobrir o monitor com múltiplos períodos do reticulado
lemniscático Lambda = 2*Z[i], exibindo uma tapeçaria infinita de singularidades conformes.

Salva em: grafica/flexagono_artigo_solido/wallpaper_desktop_face4_4k.png
"""

import sys
from pathlib import Path
import numpy as np

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "core"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "visualization"))

from domain_coloring import DomainColoringEngine
from wpgen import WP


def main():
    out_dir = PROJECT_ROOT / "grafica" / "flexagono_artigo_solido"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(">>> 1. Configurando Função Elíptica de Weierstrass wp(z; 2*Z[i])...")
    wp_quad = WP(2.0, 2.0j)

    def f4(z):
        z_safe = np.where(np.abs(z) < 1e-12, 1e-12, z)
        return wp_quad(z_safe)

    # Resolução 4K UHD para Desktop
    res_desktop = (3840, 2160)
    aspect_ratio = 3840.0 / 2160.0  # 16/9 = 1.777...

    # Expandindo a escala de tesselagem:
    # A face original tinha y_span = 2.0 (1 período).
    # Com y_span = 4.0, temos 4 períodos verticais e 4 * (16/9) = ~7.11 períodos horizontais,
    # cobrindo a tela toda com um mosaico periódico rico de polos e células de xadrez.
    y_span = 4.0
    x_span = y_span * aspect_ratio

    print(f">>> 2. Renderizando Wallpaper 4K UHD com Tesselagem Expandida ({res_desktop[0]}x{res_desktop[1]} px)...")
    print(f"       Domínio Complexo: x in [{-x_span:.2f}, {x_span:.2f}], y in [{-y_span:.2f}, {y_span:.2f}]")

    engine = DomainColoringEngine(
        func=f4,
        x_range=(-x_span, x_span),
        y_range=(-y_span, y_span),
        resolution=res_desktop
    )

    img_wallpaper = engine.render(
        mode='checkerboard',
        u_range=(-4.0, 4.0),
        v_range=(-4.0, 4.0),
        border_mode='wrap'
    )

    output_path = out_dir / "wallpaper_desktop_face4_4k.png"
    img_wallpaper.save(output_path, "PNG")
    print(f">>> SUCESSO! Wallpaper 4K salvo em:\n{output_path}")


if __name__ == '__main__':
    main()
