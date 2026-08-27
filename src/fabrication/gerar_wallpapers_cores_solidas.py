"""
Script de Geração de Wallpapers 4K (Desktop 16:9 e Celular 9:16)
para as Faces 1 (Cores Sólidas) e 5 (Alvos Concêntricos) do Flexágono de Cores Sólidas.

Desenvolvido para o Gabemática / EnIMaR 2026.
"""

import sys
from pathlib import Path
import numpy as np

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "visualization"))

from domain_coloring import DomainColoringEngine, PALETTE_SOLID_6


def main():
    out_dir = PROJECT_ROOT / "grafica" / "flexagono_cores_solidas"
    out_dir.mkdir(parents=True, exist_ok=True)

    # Função modelo clássica
    def f(z):
        return (z - 1.0) / (z**2 + z + 1.0)

    print(">>> 1. Gerando Wallpapers 4K para DESKTOP (16:9 - 3840x2160 px)...")
    res_desktop = (3840, 2160)
    aspect_desk = 3840 / 2160  # 16/9
    y_span = 2.2
    x_span = y_span * aspect_desk
    
    eng_desk = DomainColoringEngine(
        func=f,
        x_range=(-x_span, x_span),
        y_range=(-y_span, y_span),
        resolution=res_desktop
    )

    # Desktop Face 1: 6 Setores Angulares Sólidos
    print(" - Renderizando Desktop Face 1 (Setores Sólidos)...")
    img_desk_face1 = eng_desk.render(mode='solid_sectors', n_sectors=6, palette=PALETTE_SOLID_6)
    p_desk_face1 = out_dir / "wallpaper_desktop_face1_4k.png"
    img_desk_face1.save(p_desk_face1, "PNG")
    print(f"   [OK] Salvo: {p_desk_face1}")

    # Desktop Face 5: Alvos Concêntricos Sólidos
    print(" - Renderizando Desktop Face 5 (Alvos Concêntricos)...")
    img_desk_face5 = eng_desk.render(mode='concentric_targets', n_rings=10, u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap')
    p_desk_face5 = out_dir / "wallpaper_desktop_face5_4k.png"
    img_desk_face5.save(p_desk_face5, "PNG")
    print(f"   [OK] Salvo: {p_desk_face5}")

    print("\n>>> 2. Gerando Wallpapers 4K para CELULAR / SMARTPHONE (9:16 - 2160x3840 px)...")
    res_mobile = (2160, 3840)
    aspect_mob = 3840 / 2160  # 16/9
    x_span_mob = 2.2
    y_span_mob = x_span_mob * aspect_mob

    eng_mob = DomainColoringEngine(
        func=f,
        x_range=(-x_span_mob, x_span_mob),
        y_range=(-y_span_mob, y_span_mob),
        resolution=res_mobile
    )

    # Mobile Face 1: 6 Setores Angulares Sólidos
    print(" - Renderizando Celular Face 1 (Setores Sólidos)...")
    img_mob_face1 = eng_mob.render(mode='solid_sectors', n_sectors=6, palette=PALETTE_SOLID_6)
    p_mob_face1 = out_dir / "wallpaper_celular_face1_4k.png"
    img_mob_face1.save(p_mob_face1, "PNG")
    print(f"   [OK] Salvo: {p_mob_face1}")

    # Mobile Face 5: Alvos Concêntricos Sólidos
    print(" - Renderizando Celular Face 5 (Alvos Concêntricos)...")
    img_mob_face5 = eng_mob.render(mode='concentric_targets', n_rings=10, u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap')
    p_mob_face5 = out_dir / "wallpaper_celular_face5_4k.png"
    img_mob_face5.save(p_mob_face5, "PNG")
    print(f"   [OK] Salvo: {p_mob_face5}")

    print(f"\n>>> SUCESSO! Todos os 4 wallpapers foram gerados em:\n{out_dir}")


if __name__ == '__main__':
    main()
