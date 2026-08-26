"""
Script de Geração das 6 Faces de Coloração de Domínio e Montagem de Planificação de Flexágono.
Desenvolvido para o EnIMaR 2026.

Gera:
1. As 6 imagens individuais em alta resolução (1124x1124 px).
2. O painel comparativo 2x3 com todas as 6 visões anotadas.
3. As pranchas de impressão gráfica com sangrias e marcas de registro (Plano Frontal e Plano Traseiro).
"""

import os
import sys
from pathlib import Path
from typing import Callable, Optional
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import cv2

# Garantir importações locais
CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "visualization"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "fabrication"))

from domain_coloring import DomainColoringEngine, PALETTE_SOLID_6


def criar_marcas_registro(img: Image.Image, tamanho=(4840, 4840), margem=56, cor="black", scale=2) -> Image.Image:
    """Cria marcas de registro vetoriais nos cantos e no centro para alinhamento gráfico em alta definição."""
    img = img.convert("RGBA")
    draw = ImageDraw.Draw(img)

    comprimento_marca = 20 * scale
    espessura = max(2, 2 * scale)
    offset_cruz = 15 * scale

    cantos = [
        (margem, margem),
        (tamanho[0] - margem, margem),
        (margem, tamanho[1] - margem),
        (tamanho[0] - margem, tamanho[1] - margem)
    ]

    for x, y in cantos:
        draw.line([(x - comprimento_marca, y), (x + comprimento_marca, y)], fill=cor, width=espessura)
        draw.line([(x, y - comprimento_marca), (x, y + comprimento_marca)], fill=cor, width=espessura)

    cx, cy = tamanho[0] // 2, tamanho[1] // 2
    draw.line([(cx - offset_cruz, cy), (cx + offset_cruz, cy)], fill=cor, width=espessura)
    draw.line([(cx, cy - offset_cruz), (cx, cy + offset_cruz)], fill=cor, width=espessura)

    raio_circulo = 10 * scale
    draw.ellipse([(cx - raio_circulo, cy - raio_circulo), (cx + raio_circulo, cy + raio_circulo)], outline=cor, width=espessura)
    return img


def paste_triangle_directly(img_triangulada: Image.Image, img_colada: Image.Image, orientation='bottom-right', position=(0, 0), tri_size=(116, 116)) -> Image.Image:
    """Cola um triângulo com transparência sobre uma imagem de fundo em alta resolução."""
    fg = img_triangulada.convert('RGBA')
    bg = img_colada.convert('RGBA')

    w, h = tri_size
    mask = Image.new('L', (w, h), 0)
    draw = ImageDraw.Draw(mask)

    if orientation == 'bottom-right':
        points = [(0, 0), (0, h), (w, h)]
    elif orientation == 'bottom-left':
        points = [(w, 0), (0, h), (w, h)]
    elif orientation == 'top-right':
        points = [(0, 0), (w, 0), (w, h)]
    elif orientation == 'top-left':
        points = [(0, 0), (w, 0), (0, h)]
    else:
        raise ValueError(f"Orientação inválida: {orientation}")

    draw.polygon(points, fill=255)
    fg.putalpha(mask)
    bg.paste(fg, position, fg)
    return bg


def gerar_planificacao_tetraflexagono(
    faces_paths: list,
    output_frontal: Path,
    output_traseiro: Path,
    grafica: bool = True,
    scale_factor: int = 2
):
    """
    Monta as planificações frontal e traseira do tetraflexágono de 6 faces em ULTRA ALTA DEFINIÇÃO (4K+).
    """
    scale = scale_factor
    base_seg = 562 * scale
    sangria = 58 * scale
    margem_corte = 28 * scale

    if grafica:
        tamanho = (base_seg + sangria) * 2
        tamanho_plano = (base_seg * 4 + sangria * 2 + margem_corte * 2, base_seg * 4 + sangria * 2 + margem_corte * 2)
        distancia_borda = margem_corte + sangria
        ajuste = sangria
    else:
        tamanho = base_seg * 2
        tamanho_plano = (tamanho * 2 + margem_corte * 2 + sangria, tamanho * 2 + margem_corte * 2 + sangria)
        distancia_borda = margem_corte * 2
        ajuste = 0

    imgs = [Image.open(p).convert('RGB').resize((tamanho, tamanho), Image.Resampling.LANCZOS) for p in faces_paths]
    img1, img2, img3, img4, img5, img6 = imgs

    # Quadrantes cortados e rotacionados conforme a cinemática do tetraflexágono
    img1F1 = img1.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(180)
    img1F2 = img1.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2))
    img1F3 = img1.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(180)
    img1F4 = img1.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste))

    img2F1 = img2.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(180)
    img2F2 = img2.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2))
    img2F3 = img2.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(180)
    img2F4 = img2.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste))

    img3F1 = img3.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(180)
    img3F2 = img3.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2)).rotate(180)
    img3F3 = img3.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(180)
    img3F4 = img3.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste)).rotate(180)

    img4F1 = img4.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(270)
    img4F2 = img4.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2)).rotate(270)
    img4F3 = img4.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(270)
    img4F4 = img4.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste)).rotate(270)

    img5F1 = img5.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2)).rotate(90)
    img5F2 = img5.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2)).rotate(90)
    img5F3 = img5.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste)).rotate(90)
    img5F4 = img5.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste)).rotate(90)

    img6F1 = img6.crop((tamanho / 2, 0 + ajuste, tamanho - ajuste, tamanho / 2))
    img6F2 = img6.crop((0 + ajuste, 0 + ajuste, tamanho / 2, tamanho / 2))
    img6F3 = img6.crop((0 + ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste))
    img6F4 = img6.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho - ajuste))

    PlanoFrontal = Image.new('RGB', tamanho_plano, color='white')
    PlanoTraseiro = Image.new('RGB', tamanho_plano, color='white')

    # Montando Plano Frontal
    PlanoFrontal.paste(img4F3, (distancia_borda, distancia_borda))
    PlanoFrontal.paste(img2F1, (distancia_borda + int(tamanho / 2) - ajuste, distancia_borda))
    PlanoFrontal.paste(img6F2, (distancia_borda + tamanho - 2 * ajuste, distancia_borda))
    PlanoFrontal.paste(img6F1, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda))
    PlanoFrontal.paste(img2F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + int(tamanho / 2) - ajuste))
    PlanoFrontal.paste(img4F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + tamanho - 2 * ajuste))
    PlanoFrontal.paste(img4F1, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
    PlanoFrontal.paste(img2F3, (distancia_borda + tamanho - 2 * ajuste, distancia_borda + int(tamanho * 3 / 2 - 3 * ajuste)))
    PlanoFrontal.paste(img6F4, (distancia_borda + int(tamanho / 2) - ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
    PlanoFrontal.paste(img6F3, (distancia_borda, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
    PlanoFrontal.paste(img2F4, (distancia_borda, distancia_borda + tamanho - 2 * ajuste))
    PlanoFrontal.paste(img4F4, (distancia_borda, distancia_borda + int(tamanho / 2) - ajuste))

    # Montando Plano Traseiro
    PlanoTraseiro.paste(img5F4, (distancia_borda, distancia_borda))
    PlanoTraseiro.paste(img1F1, (distancia_borda + int(tamanho / 2) - ajuste, distancia_borda))
    PlanoTraseiro.paste(img3F1, (distancia_borda + tamanho - 2 * ajuste, distancia_borda))
    PlanoTraseiro.paste(img3F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda))
    PlanoTraseiro.paste(img1F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + int(tamanho / 2) - ajuste))
    PlanoTraseiro.paste(img5F1, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + tamanho - 2 * ajuste))
    PlanoTraseiro.paste(img5F2, (distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
    PlanoTraseiro.paste(img1F3, (distancia_borda + tamanho - 2 * ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
    PlanoTraseiro.paste(img3F3, (distancia_borda + int(tamanho / 2) - ajuste, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
    PlanoTraseiro.paste(img3F4, (distancia_borda, distancia_borda + int(tamanho * 3 / 2) - 3 * ajuste))
    PlanoTraseiro.paste(img1F4, (distancia_borda, distancia_borda + tamanho - 2 * ajuste))
    PlanoTraseiro.paste(img5F3, (distancia_borda, distancia_borda + int(tamanho / 2) - ajuste))

    if grafica:
        # Sangrias do plano frontal
        B24F3 = img4.crop((0, tamanho / 2, ajuste, tamanho - ajuste)).rotate(270, expand=True)
        B34F3 = img4.crop((0, tamanho - ajuste, tamanho / 2, tamanho)).rotate(270, expand=True)
        B32F1 = img2.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(180, expand=True)
        B12F1 = img2.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(180, expand=True)
        B16F2 = img6.crop((ajuste, 0, tamanho / 2, ajuste))
        B36F2 = img6.crop((ajuste, tamanho / 2, tamanho / 2, tamanho / 2 + ajuste))
        B16F1 = img6.crop((tamanho / 2, 0, tamanho, ajuste))
        B46F1 = img6.crop((tamanho - ajuste, ajuste, tamanho, tamanho / 2))
        B42F2 = img2.crop((tamanho / 2, ajuste, tamanho / 2 + ajuste, tamanho / 2))
        B22F2 = img2.crop((0, ajuste, ajuste, tamanho / 2))
        B14F2 = img4.crop((ajuste, 0, tamanho / 2, ajuste)).rotate(270, expand=True)
        B14F1 = img4.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(270, expand=True)
        B34F2 = img4.crop((ajuste, tamanho / 2, tamanho / 2, tamanho / 2 + ajuste)).rotate(270, expand=True)
        B44F1 = img4.crop((tamanho - ajuste, 0, tamanho, tamanho / 2)).rotate(270, expand=True)
        B32F3 = img2.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho)).rotate(180, expand=True)
        B12F3 = img2.crop((ajuste, tamanho / 2 - ajuste, tamanho / 2, tamanho / 2)).rotate(180, expand=True)
        B16F4 = img6.crop((tamanho / 2, tamanho / 2 - ajuste, tamanho - ajuste, tamanho / 2))
        B36F4 = img6.crop((tamanho / 2, tamanho - ajuste, tamanho - ajuste, tamanho))
        B26F3 = img6.crop((0, tamanho / 2, ajuste, tamanho - ajuste))
        B36F3 = img6.crop((0, tamanho - ajuste, tamanho / 2, tamanho))
        B22F4 = img2.crop((tamanho / 2 - ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste))
        B42F4 = img2.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho - ajuste))
        B14F4 = img4.crop((tamanho / 2, tamanho / 2 - ajuste, tamanho - ajuste, tamanho / 2)).rotate(270, expand=True)
        B34F4 = img4.crop((tamanho / 2, tamanho - ajuste, tamanho - ajuste, tamanho)).rotate(270, expand=True)

        # Sangrias do plano traseiro
        B45F4 = img5.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho - ajuste)).rotate(90, expand=True)
        B15F4 = img5.crop((tamanho / 2, tamanho / 2 - ajuste, tamanho, tamanho / 2)).rotate(90, expand=True)
        B31F1 = img1.crop((tamanho / 2 - ajuste, 0, tamanho - ajuste, ajuste)).rotate(180)
        B11F1 = img1.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(180)
        B33F1 = img3.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(180)
        B13F1 = img3.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(180)
        B33F2 = img3.crop((0, tamanho / 2, tamanho / 2, tamanho / 2 + ajuste)).rotate(180)
        B23F2 = img3.crop((0, ajuste, ajuste, tamanho / 2)).rotate(180)
        B41F2 = img1.crop((tamanho / 2, ajuste, tamanho / 2 + ajuste, tamanho / 2))
        B21F2 = img1.crop((0, ajuste, ajuste, tamanho / 2))
        B35F1 = img5.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(90, expand=True)
        B35F2 = img5.crop((0, tamanho / 2, tamanho / 2, tamanho / 2 + ajuste)).rotate(90, expand=True)
        B15F1 = img5.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(90, expand=True)
        B25F2 = img5.crop((0, ajuste, ajuste, tamanho / 2)).rotate(90, expand=True)
        B11F3 = img1.crop((ajuste, tamanho / 2 - ajuste, tamanho / 2, tamanho / 2)).rotate(180)
        B31F3 = img1.crop((0, tamanho - ajuste, tamanho / 2 - ajuste, tamanho)).rotate(180)
        B33F3 = img3.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho)).rotate(180)
        B13F3 = img3.crop((ajuste, tamanho / 2 - ajuste, tamanho / 2, tamanho / 2)).rotate(180)
        B43F4 = img3.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho - ajuste)).rotate(180)
        B13F4 = img3.crop((tamanho / 2, tamanho / 2 - ajuste, tamanho, tamanho / 2)).rotate(180)
        B21F4 = img1.crop((tamanho / 2 - ajuste, tamanho / 2, tamanho / 2, tamanho - ajuste))
        B41F4 = img1.crop((tamanho - ajuste, tamanho / 2, tamanho, tamanho - ajuste))
        B15F3 = img5.crop((ajuste, tamanho / 2 - ajuste, tamanho / 2, tamanho / 2)).rotate(90, expand=True)
        B35F3 = img5.crop((ajuste, tamanho - ajuste, tamanho / 2, tamanho)).rotate(90, expand=True)

        tri_dim = (ajuste, ajuste)

        # Colagem de bordas no plano frontal
        PlanoFrontal.paste(B24F3, (margem_corte + ajuste, margem_corte))
        PlanoFrontal.paste(B34F3, (margem_corte, margem_corte))
        PlanoFrontal.paste(B32F1, (margem_corte + base_seg + ajuste, margem_corte))
        PlanoFrontal.paste(B12F1, (margem_corte + base_seg + ajuste, margem_corte + base_seg + ajuste))
        PlanoFrontal.paste(B16F2, (margem_corte + 2 * base_seg + ajuste, margem_corte))
        PlanoFrontal.paste(B36F2, (margem_corte + 2 * base_seg + ajuste, margem_corte + base_seg + ajuste))
        PlanoFrontal.paste(B16F1, (margem_corte + 3 * base_seg + ajuste, margem_corte))
        PlanoFrontal.paste(B46F1, (margem_corte + 4 * base_seg + ajuste, margem_corte + ajuste))
        PlanoFrontal.paste(B42F2, (margem_corte + 4 * base_seg + ajuste, margem_corte + base_seg + ajuste))

        B36F2_q = B36F2.crop((base_seg - ajuste, 0, base_seg, ajuste))
        B22F2 = paste_triangle_directly(B36F2_q, B22F2, 'top-left', tri_size=tri_dim)
        PlanoFrontal.paste(B22F2, (margem_corte + 3 * base_seg, margem_corte + base_seg + ajuste))

        PlanoFrontal.paste(B14F2, (margem_corte + 4 * base_seg + ajuste, margem_corte + 2 * base_seg + ajuste))
        PlanoFrontal.paste(B14F1, (margem_corte + 4 * base_seg + ajuste, margem_corte + 3 * base_seg + ajuste))
        PlanoFrontal.paste(B34F2, (margem_corte + 3 * base_seg         , margem_corte + 2 * base_seg + ajuste))
        PlanoFrontal.paste(B44F1, (margem_corte + 3 * base_seg + ajuste, margem_corte + 4 * base_seg + ajuste))

        B34F2_q = B34F2.crop((0, base_seg - ajuste, ajuste, base_seg))
        B32F3 = paste_triangle_directly(B34F2_q, B32F3, 'top-right', position=(base_seg - ajuste, 0), tri_size=tri_dim)
        PlanoFrontal.paste(B32F3, (base_seg * 2 + margem_corte + ajuste, margem_corte + base_seg * 3))

        PlanoFrontal.paste(B12F3, (base_seg * 2 + margem_corte + ajuste, margem_corte + base_seg * 4 + ajuste))
        PlanoFrontal.paste(B16F4, (base_seg * 1 + margem_corte + ajuste, margem_corte + base_seg * 3))
        PlanoFrontal.paste(B36F4, (base_seg * 1 + margem_corte + ajuste, margem_corte + base_seg * 4 + ajuste))
        PlanoFrontal.paste(B26F3, (margem_corte, margem_corte + base_seg * 3 + ajuste))
        PlanoFrontal.paste(B36F3, (margem_corte, margem_corte + base_seg * 4 + ajuste))
        PlanoFrontal.paste(B22F4, (margem_corte, margem_corte + base_seg * 2 + ajuste))

        B16F4_q = B16F4.crop((0, 0, ajuste, ajuste))
        B42F4 = paste_triangle_directly(B16F4_q, B42F4, 'bottom-left', position=(0, base_seg - ajuste), tri_size=tri_dim)
        PlanoFrontal.paste(B42F4, (base_seg * 1 + margem_corte + ajuste, margem_corte + base_seg * 2 + ajuste))

        PlanoFrontal.paste(B34F4, (margem_corte, margem_corte + base_seg * 1 + ajuste))

        B12F1_q = B12F1.crop((0, 0, ajuste, ajuste))
        B14F4 = paste_triangle_directly(B12F1_q, B14F4, 'top-right', tri_size=tri_dim)
        PlanoFrontal.paste(B14F4, (margem_corte + base_seg + ajuste, margem_corte + base_seg + ajuste))

        # Colagem de bordas no plano traseiro
        PlanoTraseiro.paste(B45F4, (margem_corte + ajuste, margem_corte))
        PlanoTraseiro.paste(B15F4, (margem_corte, margem_corte))
        PlanoTraseiro.paste(B31F1, (margem_corte + base_seg + ajuste, margem_corte))
        PlanoTraseiro.paste(B11F1, (margem_corte + base_seg + ajuste, margem_corte + base_seg + ajuste))
        PlanoTraseiro.paste(B33F1, (margem_corte + 2 * base_seg + ajuste, margem_corte))
        PlanoTraseiro.paste(B13F1, (margem_corte + 2 * base_seg + ajuste, margem_corte + base_seg + ajuste))
        PlanoTraseiro.paste(B33F2, (margem_corte + 3 * base_seg + ajuste, margem_corte))
        PlanoTraseiro.paste(B23F2, (margem_corte + 4 * base_seg + ajuste, margem_corte + ajuste))
        PlanoTraseiro.paste(B41F2, (margem_corte + 4 * base_seg + ajuste, margem_corte + base_seg + ajuste))

        B13F1_q = B13F1.crop((base_seg - ajuste, 0, base_seg, ajuste))
        B21F2 = paste_triangle_directly(B13F1_q, B21F2, 'top-left', tri_size=tri_dim)
        PlanoTraseiro.paste(B21F2, (margem_corte + 3 * base_seg, margem_corte + base_seg + ajuste))

        PlanoTraseiro.paste(B35F1, (margem_corte + 4 * base_seg + ajuste, margem_corte + 2 * base_seg + ajuste))
        PlanoTraseiro.paste(B35F2, (margem_corte + 4 * base_seg + ajuste, margem_corte + 3 * base_seg + ajuste))
        PlanoTraseiro.paste(B15F1, (margem_corte + 3 * base_seg         , margem_corte + 2 * base_seg + ajuste))
        PlanoTraseiro.paste(B25F2, (margem_corte + 3 * base_seg + ajuste, margem_corte + 4 * base_seg + ajuste))

        B15F1_q = B15F1.crop((0, base_seg - ajuste, ajuste, base_seg))
        B31F3 = paste_triangle_directly(B15F1_q, B31F3, 'top-right', position=(base_seg - ajuste, 0), tri_size=tri_dim)
        PlanoTraseiro.paste(B31F3, (base_seg * 2 + margem_corte + ajuste, margem_corte + base_seg * 3))

        PlanoTraseiro.paste(B11F3, (base_seg * 2 + margem_corte + ajuste, margem_corte + base_seg * 4 + ajuste))
        PlanoTraseiro.paste(B33F3, (base_seg * 1 + margem_corte + ajuste, margem_corte + base_seg * 3))
        PlanoTraseiro.paste(B13F3, (base_seg * 1 + margem_corte + ajuste, margem_corte + base_seg * 4 + ajuste))
        PlanoTraseiro.paste(B43F4, (margem_corte, margem_corte + base_seg * 3 + ajuste))
        PlanoTraseiro.paste(B13F4, (margem_corte, margem_corte + base_seg * 4 + ajuste))
        PlanoTraseiro.paste(B21F4, (margem_corte, margem_corte + base_seg * 2 + ajuste))

        B33F3_q = B33F3.crop((0, 0, ajuste, ajuste))
        B41F4 = paste_triangle_directly(B33F3_q, B41F4, 'bottom-left', position=(0, base_seg - ajuste), tri_size=tri_dim)
        PlanoTraseiro.paste(B41F4, (base_seg * 1 + margem_corte + ajuste, margem_corte + base_seg * 2 + ajuste))

        PlanoTraseiro.paste(B15F3, (margem_corte, margem_corte + base_seg * 1 + ajuste))

        B11F1_q = B11F1.crop((0, 0, ajuste, ajuste))
        B35F3 = paste_triangle_directly(B11F1_q, B35F3, 'top-right', tri_size=tri_dim)
        PlanoTraseiro.paste(B35F3, (margem_corte + base_seg + ajuste, margem_corte + base_seg + ajuste))

        PlanoFrontal = criar_marcas_registro(PlanoFrontal, tamanho=tamanho_plano, margem=margem_corte, scale=scale)
        PlanoTraseiro = criar_marcas_registro(PlanoTraseiro, tamanho=tamanho_plano, margem=margem_corte, scale=scale)

    PlanoFrontal.save(output_frontal, "PNG")
    PlanoTraseiro.save(output_traseiro, "PNG")
    print(f"Planificação salva:\n - {output_frontal}\n - {output_traseiro}")


def criar_painel_comparativo(
    faces: dict,
    output_path: Path,
    titles: Optional[dict] = None
):
    """Cria um mosaico comparativo 2x3 com as 6 faces renderizadas e anotações."""
    if titles is None:
        titles = {
            'face1': "Face 1: Fase Contínua (HSV Padrão)",
            'face2': "Face 2: Cores Sólidas (6 Setores)",
            'face3': "Face 3: Estilo Wegert (Enhanced)",
            'face4': "Face 4: Grade Cartesiana no Plano w",
            'face5': "Face 5: Círculos Concêntricos (Pullback)",
            'face6': "Face 6: Cores Complementares (Rot. 180°)"
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

        # Título
        title = titles.get(key, key)
        draw.text((x + 10, y + 10), title, fill=(30, 40, 60))

        # Imagem redimensionada
        face_img = faces[key].resize((face_w, face_h), Image.Resampling.LANCZOS)
        panel.paste(face_img, (x, y + header_h))
        # Borda sutil
        draw.rectangle([(x, y + header_h), (x + face_w, y + header_h + face_h)], outline=(200, 210, 225), width=2)

    panel.save(output_path, "PNG")
    print(f"Painel comparativo salvo em: {output_path}")


def main():
    """Gera todas as faces e planificações para a função modelo f(z) = (z-1)/(z^2+z+1)."""
    out_dir = PROJECT_ROOT / "grafica" / "flexagono_coloracao_dominio"
    faces_dir = out_dir / "faces"
    faces_dir.mkdir(parents=True, exist_ok=True)

    print(">>> 1. Configurando Motor de Coloração de Domínio...")
    # Função modelo clássica com 1 zero e 2 polos
    def f(z):
        return (z - 1.0) / (z**2 + z + 1.0)

    engine = DomainColoringEngine(
        func=f,
        x_range=(-2.2, 2.2),
        y_range=(-2.2, 2.2),
        resolution=(3840, 3840)
    )

    print(">>> 2. Renderizando as 6 Faces do Flexágono em 4K UHD (3840x3840)...")
    faces = engine.generate_six_flexagon_faces(
        custom_palette=PALETTE_SOLID_6,
        texture_u_range=(-2.5, 2.5),
        texture_v_range=(-2.5, 2.5)
    )

    face_paths = []
    for i in range(1, 7):
        key = f'face{i}'
        p = faces_dir / f"face{i}.png"
        faces[key].save(p, "PNG")
        face_paths.append(str(p))
        print(f" - Salva {key} (4K): {p}")

    print(">>> 3. Gerando Painel Comparativo 2x3...")
    painel_path = out_dir / "painel_6_faces_domain_coloring.png"
    criar_painel_comparativo(faces, painel_path)

    print(">>> 4. Montando Planificações de Impressão (Tetraflexágono em Ultra-Alta Definição 4840x4840)...")
    frontal_path = out_dir / "Plano_Frontal_DomainColoring.png"
    traseiro_path = out_dir / "Plano_Traseiro_DomainColoring.png"
    gerar_planificacao_tetraflexagono(
        faces_paths=face_paths,
        output_frontal=frontal_path,
        output_traseiro=traseiro_path,
        grafica=True,
        scale_factor=2
    )

    print(f"\n>>> SUCESSO! Todos os arquivos gráficos foram gerados em:\n{out_dir}")


if __name__ == '__main__':
    main()
