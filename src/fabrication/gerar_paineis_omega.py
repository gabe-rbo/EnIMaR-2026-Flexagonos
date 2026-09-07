# -*- coding: utf-8 -*-
"""
gerar_paineis_omega.py
=======================
Gera, para cada flexágono de coloração de domínio (Galeria Sólida, Artigo Sólido), um
painel 3x2 com o "plano ômega" de cada face: a MESMA codificação visual (modo + parâmetros
do DomainColoringEngine) já usada naquela face, só que aplicada à função identidade
f(z) = z em vez da função específica da face — ou seja, o plano w "puro", sem composição
com nenhuma função. É o painel-espelho de painel_6_faces_<nome>.png: mostra o "raw
material" com que cada face foi construída.

Não cobre Curvas Polares: aquele flexágono não usa o DomainColoringEngine (é gerado por
matplotlib, plotando r(theta) diretamente) — não existe um "plano ômega" a extrair.

Roda direto no Python do sistema (mesmas dependências de flexagon_domain_faces.py).
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

PROJECT_ROOT = Path.home() / "mnt" / "EnIMaR"
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "visualization"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "fabrication"))

from domain_coloring import DomainColoringEngine, PALETTE_SOLID_6
from flexagon_domain_faces import desenhar_titulo_painel

RESOLUCAO_FACE = (960, 960)  # menor que os 3840 das faces reais: isto é material de referência/apoio, não de impressão

NOME_ESTILO = {
    'solid_sectors': "6 Setores Sólidos",
    'cartesian_grid': "Grade Cartesiana",
    'truchet': "Mosaico de Truchet",
    'checkerboard': "Xadrez Conforme",
    'concentric_targets': "Alvos Concêntricos",
    'honeycomb': "Favos de Mel Hexagonais",
}

IDENTIDADE = lambda z: z  # noqa: E731 — o "plano ômega": a codificação aplicada a si mesma


def montar_painel_omega(specs: dict, output_path: Path, subtitulo_extra: str = ""):
    """
    specs: dict face_key -> dict(mode=..., kwargs=dict(...), x_range=..., y_range=...)
    Gera o plano ômega de cada face (função identidade + mesmo modo/kwargs) e monta o
    painel 3x2, no mesmo layout visual de criar_painel_galeria/criar_painel_artigo.
    """
    face_w, face_h = 900, 900
    margin = 40
    header_h = 60
    panel_w = margin * 3 + face_w * 3
    panel_h = margin * 3 + (face_h + header_h) * 2
    panel = Image.new('RGB', (panel_w, panel_h), (242, 245, 250))
    draw = ImageDraw.Draw(panel)

    keys = ['face1', 'face2', 'face3', 'face4', 'face5', 'face6']
    for idx, key in enumerate(keys):
        spec = specs[key]
        eng = DomainColoringEngine(func=IDENTIDADE, x_range=spec['x_range'], y_range=spec['y_range'],
                                    resolution=RESOLUCAO_FACE)
        img = eng.render(mode=spec['mode'], **spec.get('kwargs', {}))

        row, col = idx // 3, idx % 3
        x = margin + col * (face_w + margin)
        y = margin + row * (face_h + header_h + margin)

        titulo = f"Face {idx + 1}: plano ω — {NOME_ESTILO.get(spec['mode'], spec['mode'])}{subtitulo_extra}"
        desenhar_titulo_painel(draw, titulo, (x + 12, y + 16), largura_max=face_w - 24,
                                tamanho_inicial=20, cor=(15, 30, 55))

        face_img = img.resize((face_w, face_h), Image.Resampling.LANCZOS)
        panel.paste(face_img, (x, y + header_h))
        draw.rectangle([(x, y + header_h), (x + face_w, y + header_h + face_h)],
                        outline=(180, 195, 215), width=3)

    panel.save(output_path, "PNG")
    print("gerado:", output_path)


# ---------------------------------------------------------------------------
# GALERIA SÓLIDA — mesmos modos/kwargs de gerar_flexagono_galeria_solida.py
# ---------------------------------------------------------------------------
SPECS_GALERIA = {
    'face1': dict(mode='solid_sectors', kwargs=dict(n_sectors=6, palette=PALETTE_SOLID_6),
                  x_range=(-1.8, 1.8), y_range=(-1.8, 1.8)),
    'face2': dict(mode='cartesian_grid', kwargs=dict(u_range=(-3.0, 3.0), v_range=(-3.0, 3.0), border_mode='wrap'),
                  x_range=(-2.5, 2.5), y_range=(-2.5, 2.5)),
    'face3': dict(mode='truchet', kwargs=dict(u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap'),
                  x_range=(-2.2, 2.2), y_range=(-2.2, 2.2)),
    'face4': dict(mode='checkerboard', kwargs=dict(u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap'),
                  x_range=(-2.4, 2.4), y_range=(-2.4, 2.4)),
    'face5': dict(mode='concentric_targets', kwargs=dict(n_rings=10, u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap'),
                  x_range=(-2.2, 2.2), y_range=(-2.2, 2.2)),
    'face6': dict(mode='honeycomb', kwargs=dict(u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap'),
                  x_range=(-2.2, 2.2), y_range=(-2.2, 2.2)),
}

# ---------------------------------------------------------------------------
# ARTIGO SÓLIDO — mesmos modos/kwargs de gerar_flexagono_artigo_solido.py
# ---------------------------------------------------------------------------
SPECS_ARTIGO = {
    'face1': dict(mode='solid_sectors', kwargs=dict(n_sectors=6, palette=PALETTE_SOLID_6),
                  x_range=(-2.0, 2.0), y_range=(-2.0, 2.0)),
    'face2': dict(mode='cartesian_grid', kwargs=dict(u_range=(-3.0, 3.0), v_range=(-3.0, 3.0), border_mode='wrap'),
                  x_range=(-2.0, 2.0), y_range=(-2.0, 2.0)),
    'face3': dict(mode='truchet', kwargs=dict(u_range=(-2.5, 2.5), v_range=(-2.5, 2.5), border_mode='wrap'),
                  x_range=(-2.0, 2.0), y_range=(-2.0, 2.0)),
    'face4': dict(mode='checkerboard', kwargs=dict(u_range=(-4.0, 4.0), v_range=(-4.0, 4.0), border_mode='wrap'),
                  x_range=(-2.0, 2.0), y_range=(-2.0, 2.0)),
    'face5': dict(mode='concentric_targets', kwargs=dict(n_rings=10, u_range=(-6.0, 6.0), v_range=(-6.0, 6.0), border_mode='wrap'),
                  x_range=(-2.0, 2.0), y_range=(-2.0, 2.0)),
    'face6': dict(mode='honeycomb', kwargs=dict(u_range=(-8.0, 8.0), v_range=(-8.0, 8.0), border_mode='wrap'),
                  x_range=(-2.0, 2.0), y_range=(-2.0, 2.0)),
}

if __name__ == "__main__":
    GRAFICA = PROJECT_ROOT / "grafica"

    saida_galeria = Path("/tmp") / "painel_omega_GaleriaSolida.png"
    montar_painel_omega(SPECS_GALERIA, saida_galeria)

    saida_artigo = Path("/tmp") / "painel_omega_ArtigoSolido.png"
    montar_painel_omega(SPECS_ARTIGO, saida_artigo)

    import shutil
    for nome_pasta, arquivo in [
        ("flexagono_galeria_solida", saida_galeria),
        ("flexagono_artigo_solido", saida_artigo),
    ]:
        for wdir in ("com_watermark", "sem_watermark"):
            destino = GRAFICA / wdir / nome_pasta / arquivo.name
            shutil.copyfile(arquivo, destino)
            print("  copiado para:", destino)
