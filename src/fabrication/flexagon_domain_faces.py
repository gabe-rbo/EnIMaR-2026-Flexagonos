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
# kinematics/mecanica.py e visualization/diagrama.py usam import "bare" (from mecanica import ...,
# from quadflex import ...) entre si, então seus diretórios precisam estar diretamente no sys.path
# (não só como subpacote de "src"), igual ao core/quadflex.py de que mecanica.py depende.
sys.path.insert(0, str(PROJECT_ROOT / "src" / "kinematics"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "core"))

from domain_coloring import DomainColoringEngine, PALETTE_SOLID_6

# Caminho do logo do EnIMaR usado na assinatura automática (watermark).
LOGO_ENIMAR_PATH = PROJECT_ROOT / "pesquisa" / "enimar2026" / "templates_latex" / "Enimarlogo.png"

# Bounding boxes (em frações do plano, x0,y0,x1,y1) da assinatura "Feito na UFMG por" + logo,
# medidas a partir de Plano_Traseiro_Scarpet_grafica.xcf (referência da Aniura, canvas 2905x2905:
# texto em offset≈(308,1912) tamanho 466x55px; logo em offset≈(311,1975) tamanho 354x89px) e
# reaproveitadas aqui como frações independentes de resolução. Ficam na coluna esquerda do anel,
# faixa inferior, fora do buraco central (que no nosso plano de 4840x4840 cai em
# x,y ∈ [0.2678, 0.7322]). Ajustar aqui se o posicionamento precisar de retoque fino.
ASSINATURA_TEXTO_BBOX_FRAC = (0.106, 0.658, 0.266, 0.690)
ASSINATURA_LOGO_BBOX_FRAC = (0.107, 0.694, 0.230, 0.711)
ASSINATURA_TEXTO = "Feito na UFMG por"


def _obter_fonte_serifada_italica(tamanho_px: int) -> "ImageFont.FreeTypeFont":
    """Carrega a fonte serifada itálica (DejaVu Serif Italic, embutida no matplotlib) para a
    assinatura do watermark. Cai para a fonte padrão do PIL se a busca falhar por qualquer motivo
    (mantém a geração funcionando mesmo sem matplotlib disponível)."""
    try:
        import matplotlib
        fonte_path = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / "DejaVuSerif-Italic.ttf"
        return ImageFont.truetype(str(fonte_path), size=tamanho_px)
    except Exception:
        return ImageFont.load_default()


def _obter_fonte_sans(tamanho_px: int, negrito: bool = True) -> "ImageFont.FreeTypeFont":
    """Carrega uma fonte sans-serif com cobertura Unicode completa (acentos do português, letras
    gregas, símbolos matemáticos como ℘) para títulos de painéis comparativos. Usa DejaVu Sans,
    já embutida no matplotlib — o PIL sozinho (`ImageFont.load_default()`) usa uma fonte bitmap
    minúscula sem esses glifos, que aparecem como uma caixa com um X/quadrado dentro ("tofu") no
    lugar de qualquer acento ou símbolo fora do ASCII básico. Cai para a fonte padrão do PIL se a
    busca falhar por qualquer motivo (mantém a geração funcionando mesmo sem matplotlib)."""
    try:
        import matplotlib
        nome_arquivo = "DejaVuSans-Bold.ttf" if negrito else "DejaVuSans.ttf"
        fonte_path = Path(matplotlib.get_data_path()) / "fonts" / "ttf" / nome_arquivo
        return ImageFont.truetype(str(fonte_path), size=tamanho_px)
    except Exception:
        return ImageFont.load_default()


def desenhar_titulo_painel(
    draw: "ImageDraw.ImageDraw",
    texto: str,
    pos: tuple,
    largura_max: int,
    tamanho_inicial: int = 20,
    cor: tuple = (20, 35, 60),
    negrito: bool = True,
) -> None:
    """Desenha o título de uma célula de painel comparativo com `_obter_fonte_sans` (corrige os
    glifos "tofu" que apareciam com a fonte padrão do PIL para acentos/símbolos), encolhendo o
    tamanho da fonte automaticamente até o texto caber em `largura_max` pixels — os títulos variam
    bastante de comprimento entre os painéis (de "Face 1: Borboleta" a fórmulas inteiras com
    símbolos de Weierstrass), então um tamanho fixo não serve para todos."""
    tamanho = tamanho_inicial
    fonte = _obter_fonte_sans(tamanho, negrito=negrito)
    while tamanho > 8:
        bbox = draw.textbbox((0, 0), texto, font=fonte)
        if (bbox[2] - bbox[0]) <= largura_max:
            break
        tamanho -= 1
        fonte = _obter_fonte_sans(tamanho, negrito=negrito)
    draw.text(pos, texto, fill=cor, font=fonte)


def aplicar_assinatura_ufmg(plano_traseiro: Image.Image, tamanho_plano: tuple) -> Image.Image:
    """Cola a assinatura 'Feito na UFMG por' + logo do EnIMaR no Plano Traseiro, na posição
    definida por ASSINATURA_TEXTO_BBOX_FRAC / ASSINATURA_LOGO_BBOX_FRAC. Automatiza o que hoje a
    Aniura cola manualmente no GIMP em cada plano traseiro antes de mandar para a gráfica."""
    plano_traseiro = plano_traseiro.convert("RGBA")
    largura_plano, altura_plano = tamanho_plano

    # --- Texto ---
    tx0, ty0, tx1, ty1 = ASSINATURA_TEXTO_BBOX_FRAC
    caixa_texto_w = int((tx1 - tx0) * largura_plano)
    caixa_texto_h = int((ty1 - ty0) * altura_plano)

    # Ajusta o tamanho da fonte para caber tanto na altura quanto na largura da caixa: parte de uma
    # estimativa pela altura e escala pela largura medida de verdade (a fonte itálica larga faz o
    # texto completo estourar a largura antes de estourar a altura).
    tamanho_fonte = max(int(caixa_texto_h * 0.85), 1)
    fonte = _obter_fonte_serifada_italica(tamanho_fonte)
    medidor = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    bbox_txt = medidor.textbbox((0, 0), ASSINATURA_TEXTO, font=fonte)
    texto_w = bbox_txt[2] - bbox_txt[0]
    if texto_w > caixa_texto_w:
        tamanho_fonte = max(int(tamanho_fonte * (caixa_texto_w / texto_w) * 0.97), 1)
        fonte = _obter_fonte_serifada_italica(tamanho_fonte)
        bbox_txt = medidor.textbbox((0, 0), ASSINATURA_TEXTO, font=fonte)

    texto_w, texto_h = bbox_txt[2] - bbox_txt[0], bbox_txt[3] - bbox_txt[1]
    camada_texto = Image.new("RGBA", (caixa_texto_w, caixa_texto_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(camada_texto)
    pos_texto = ((caixa_texto_w - texto_w) // 2 - bbox_txt[0], (caixa_texto_h - texto_h) // 2 - bbox_txt[1])
    draw.text(pos_texto, ASSINATURA_TEXTO, font=fonte, fill=(30, 30, 30, 255))
    plano_traseiro.alpha_composite(camada_texto, (int(tx0 * largura_plano), int(ty0 * altura_plano)))

    # --- Logo ---
    if LOGO_ENIMAR_PATH.exists():
        lx0, ly0, lx1, ly1 = ASSINATURA_LOGO_BBOX_FRAC
        caixa_logo_w = int((lx1 - lx0) * largura_plano)
        caixa_logo_h = int((ly1 - ly0) * altura_plano)
        logo = Image.open(LOGO_ENIMAR_PATH).convert("RGBA")
        escala_logo = min(caixa_logo_w / logo.width, caixa_logo_h / logo.height)
        novo_tam = (max(1, int(logo.width * escala_logo)), max(1, int(logo.height * escala_logo)))
        logo = logo.resize(novo_tam, Image.Resampling.LANCZOS)
        pos_logo_x = int(lx0 * largura_plano) + (caixa_logo_w - novo_tam[0]) // 2
        pos_logo_y = int(ly0 * altura_plano) + (caixa_logo_h - novo_tam[1]) // 2
        plano_traseiro.alpha_composite(logo, (pos_logo_x, pos_logo_y))
    else:
        print(f"AVISO: logo do EnIMaR não encontrado em {LOGO_ENIMAR_PATH}, assinatura gerada só com texto.")

    return plano_traseiro.convert("RGB")


def gerar_diagrama_dinamica(
    faces_paths: list,
    output_path: Path,
    resolucao_alvo_px: int = 3840,
    tamanho_face_px: int = 900,
) -> Path:
    """Gera, em ~4K UHD, o diagrama de flexão ("dinâmica") do hexa-tetraflexágono usando as 6
    imagens de face reais do flexágono gerado (não rótulos genéricos).

    O diagrama mostra os 14 estados planos que o flexágono efetivamente assume ao ser flexionado
    (nós), ligados pelas flexões possíveis entre eles (setas cheias = corte "principal" entre as
    duas metades; tracejadas = corte secundário; setas duplas = "book flex" nos dois sentidos, com
    ↻ indicando giro de 180°). Cada nó mostra a face correspondente já reagrupada no arranjo de
    quadrantes (TL/TR/BL/BR) daquele estado específico — é a mesma leitura da Figura 34 do artigo
    de referência (Hall, Almeida & Teixeira, Bridges 2018) e do `esquema_flex.tex` usado no
    minicurso, só que com a arte de verdade no lugar dos rótulos abstratos "1a, 1b, ...".

    Importante: `faces_paths` deve estar na numeração "de conteúdo" (face1..face6, a mesma ordem
    passada a `gerar_planificacao_tetraflexagono` ANTES do `trocar_3com5_4com6`) — o diagrama de
    flexão (`src/kinematics/mecanica.py::HEXA`) já usa essa numeração nativamente, então não há
    troca a aplicar aqui (ver docstring de `gerar_planificacao_tetraflexagono` para o contexto
    completo da troca 3↔5/4↔6, que é específica da montagem do plano de impressão).

    Args:
        faces_paths: lista com os caminhos das 6 imagens de face, na ordem face1..face6 (numeração
            de conteúdo, igual à usada em `gerar_planificacao_tetraflexagono`).
        output_path: caminho de saída do PNG do diagrama.
        resolucao_alvo_px: largura alvo em pixels da imagem final (default 3840 = 4K UHD, mesma
            convenção horizontal usada nas faces individuais do projeto). A altura é derivada
            automaticamente pela geometria fixa do diagrama (grade de 6 colunas × 3 linhas), então
            a imagem final não é quadrada.
        tamanho_face_px: resolução (quadrada) para a qual cada face é reamostrada antes de entrar
            no diagrama — não precisa bater com a resolução original da face (tipicamente 4K); um
            valor bem menor já basta porque cada face ocupa só uma fração da largura final.
    """
    from mecanica import HEXA
    from diagrama import desenha

    imagens = {}
    for i, p in enumerate(faces_paths, start=1):
        img = Image.open(p).convert("RGB").resize((tamanho_face_px, tamanho_face_px), Image.Resampling.LANCZOS)
        imagens[i] = np.array(img)

    fig_w_polegadas = 11.0  # fixo dentro de diagrama.desenha(); escalamos o dpi para bater a largura alvo
    dpi = resolucao_alvo_px / fig_w_polegadas
    desenha(HEXA, imagens, str(output_path), dpi=dpi)
    print(f"Diagrama de dinâmica salvo em: {output_path}")
    return output_path


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
    trocar_3com5_4com6: bool,
    grafica: bool = True,
    scale_factor: int = 2,
    watermark: bool = False
):
    """
    Monta as planificações frontal e traseira do tetraflexágono de 6 faces em ULTRA ALTA DEFINIÇÃO (4K+).

    Args:
        faces_paths: lista com os caminhos das 6 imagens de face, na ordem face1..face6 (a
            numeração "de conteúdo": face1/face2 são as faces "hub" que abrem em dois eixos;
            {face3, face6} formam uma família de posições e {face4, face5} formam outra).
        output_frontal: caminho de saída do Plano Frontal (faces pares: 2, 4, 6).
        output_traseiro: caminho de saída do Plano Traseiro (faces ímpares: 1, 3, 5).
        trocar_3com5_4com6: **obrigatório**. Controla qual convenção de posicionamento físico é
            usada para colar as faces 3, 4, 5 e 6 no plano (as faces 1 e 2 nunca mudam de posição
            — já são consistentes nas duas convenções).

            O gerador original desta função posicionava as faces numa ordem que NÃO bate com a
            numeração usada no artigo de referência (Hall, Almeida & Teixeira, "Exploring symmetry
            in rosettes of Truchet tiles", Bridges 2018 — Figura 33) nem com o `Manual_Flexas.pdf`
            do projeto (Figuras 1.2/1.3): no plano gerado com `trocar_3com5_4com6=False`, a face
            que fisicamente cai na posição "3" do artigo é na verdade a nossa face 5 (e vice-versa,
            no Verso), e a posição "4" do artigo é a nossa face 6 (e vice-versa, na Frente). Ou
            seja, as posições das faces 3↔5 (verso) e 4↔6 (frente) ficam trocadas em relação à
            convenção do artigo.

            O diagrama de flexão do projeto (`src/kinematics/mecanica.py::HEXA`, renderizado em
            `esquema_flex.tex`/`diagrama.py`, usado no minicurso do EnIMaR) já segue a convenção do
            artigo — bate célula a célula com a Figura 34. Isso significa que um plano gerado com
            `trocar_3com5_4com6=False` fica **inconsistente** com esse diagrama: ao montar o
            flexágono físico seguindo o diagrama de flexão, as faces 3/5 e 4/6 não aparecem nas
            posições que o diagrama indica.

            - `trocar_3com5_4com6=True`: aplica a troca (`img3,img5 = img5,img3` no Verso;
              `img4,img6 = img6,img4` na Frente) e produz o plano na convenção do artigo/manual —
              a mesma do diagrama de flexão já usado no minicurso. **Usar sempre que o plano for
              impresso ou apresentado junto com esse diagrama** — é o caso de todo o material atual
              do EnIMaR 2026.
            - `trocar_3com5_4com6=False`: mantém o comportamento original (pré-correção), com a
              numeração física INCONSISTENTE com o diagrama de flexão e com o artigo. Existe só
              para reproduzir planos antigos já impressos/em circulação com essa numeração; não
              deve ser usado para gerar material novo.
        grafica: se True, inclui sangrias de corte e marcas de registro para impressão profissional.
        scale_factor: fator de escala do canvas (2 = pranchas de 4840x4840px).
        watermark: se True, cola automaticamente no Verso (`PlanoTraseiro`) a assinatura
            "Feito na UFMG por" + logo do EnIMaR, no canto inferior esquerdo do anel (fora do
            buraco central), reproduzindo o que hoje é colado manualmente no GIMP. Não afeta o
            Plano Frontal. Ver constantes `ASSINATURA_TEXTO_BBOX_FRAC` / `ASSINATURA_LOGO_BBOX_FRAC`
            para ajustar posição/tamanho.
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

    if trocar_3com5_4com6:
        # Realinha a numeração física com a convenção do artigo (Hall, Almeida & Teixeira,
        # Bridges 2018, Fig. 33) e do diagrama de flexão (esquema_flex.tex / mecanica.py::HEXA):
        # a face 3 do conteúdo vai para a posição que a face 5 ocupava no plano, e vice-versa
        # (Verso); o mesmo para 4 e 6 (Frente). Ver docstring acima.
        img3, img5 = img5, img3
        img4, img6 = img6, img4

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
        B12F1 = img2.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(180, expand=True)
        B32F1 = img2.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(180, expand=True)
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
        B11F1 = img1.crop((tamanho / 2 - ajuste, 0, tamanho - ajuste, ajuste)).rotate(180)
        B31F1 = img1.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(180)
        B13F1 = img3.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(180)
        B33F1 = img3.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(180)
        B33F2 = img3.crop((0, tamanho / 2, tamanho / 2, tamanho / 2 + ajuste)).rotate(180)
        B23F2 = img3.crop((0, ajuste, ajuste, tamanho / 2)).rotate(180)
        B41F2 = img1.crop((tamanho / 2, ajuste, tamanho / 2 + ajuste, tamanho / 2))
        B21F2 = img1.crop((0, ajuste, ajuste, tamanho / 2))
        B15F1 = img5.crop((tamanho / 2, 0, tamanho - ajuste, ajuste)).rotate(90, expand=True)
        B35F2 = img5.crop((0, tamanho / 2, tamanho / 2, tamanho / 2 + ajuste)).rotate(90, expand=True)
        B35F1 = img5.crop((tamanho / 2, tamanho / 2, tamanho - ajuste, tamanho / 2 + ajuste)).rotate(90, expand=True)
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

        if watermark:
            PlanoTraseiro = aplicar_assinatura_ufmg(PlanoTraseiro, tamanho_plano=tamanho_plano)

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
            'face6': "Face 6: Tabuleiro de Xadrez Conforme"
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
        desenhar_titulo_painel(draw, title, (x + 10, y + 10), largura_max=face_w - 20, tamanho_inicial=18, cor=(30, 40, 60))

        # Imagem redimensionada
        face_img = faces[key].resize((face_w, face_h), Image.Resampling.LANCZOS)
        panel.paste(face_img, (x, y + header_h))
        # Borda sutil
        draw.rectangle([(x, y + header_h), (x + face_w, y + header_h + face_h)], outline=(200, 210, 225), width=2)

    panel.save(output_path, "PNG")
    print(f"Painel comparativo salvo em: {output_path}")


# Candidatos para substituir a função atual de flexagono_coloracao_dominio, f(z) = (z-1)/(z^2+z+1)
# — que é EXATAMENTE a mesma função já usada em flexagono_cores_solidas (só que com outro conjunto
# de 6 renderizações). Os dois candidatos abaixo são gerados lado a lado, em pastas separadas, para
# comparação visual antes de promover um deles a grafica/flexagono_coloracao_dominio/ definitivo.
CANDIDATOS_COLORACAO_DOMINIO = {
    "candidato_A_sin1z": {
        "nome_dir": "flexagono_coloracao_dominio_candidato_A_sin1z",
        "descricao": "f(z) = sin(1/z) — singularidade essencial na origem",
        "func": lambda z: np.sin(1.0 / np.where(z == 0, 1e-15, z)),
        "x_range": (-2.2, 2.2),
        "y_range": (-2.2, 2.2),
    },
    "candidato_B_racional": {
        "nome_dir": "flexagono_coloracao_dominio_candidato_B_racional",
        "descricao": "f(z) = z^5 / (z^4 - 1) — zero de ordem 5 na origem, 4 polos simples nas raízes quartas da unidade",
        "func": lambda z: z**5 / (z**4 - 1.0),
        "x_range": (-2.0, 2.0),
        "y_range": (-2.0, 2.0),
    },
}


def gerar_candidato_coloracao_dominio(chave: str, config: dict) -> Path:
    """Gera as 6 faces, painel comparativo e planos de impressão de um candidato de
    flexagono_coloracao_dominio, em grafica/<nome_dir>/ (pasta separada da atual, para comparação)."""
    out_dir = PROJECT_ROOT / "grafica" / config["nome_dir"]
    faces_dir = out_dir / "faces"
    faces_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=== {chave}: {config['descricao']} ===")
    print(">>> 1. Configurando Motor de Coloração de Domínio...")
    engine = DomainColoringEngine(
        func=config["func"],
        x_range=config["x_range"],
        y_range=config["y_range"],
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
        trocar_3com5_4com6=True,
        grafica=True,
        scale_factor=2,
        watermark=True
    )

    print(">>> 5. Gerando Diagrama de Dinâmica (flexão) em 4K...")
    diagrama_path = out_dir / "Diagrama_Dinamica_DomainColoring.png"
    gerar_diagrama_dinamica(face_paths, diagrama_path)

    print(f">>> SUCESSO! {chave} gerado em:\n{out_dir}")
    return painel_path


def main():
    """Gera os dois candidatos de flexagono_coloracao_dominio (ver CANDIDATOS_COLORACAO_DOMINIO)
    para comparação visual, sem tocar na pasta grafica/flexagono_coloracao_dominio/ atual."""
    paineis = {}
    for chave, config in CANDIDATOS_COLORACAO_DOMINIO.items():
        paineis[chave] = gerar_candidato_coloracao_dominio(chave, config)

    print("\n>>> Painéis comparativos para decisão:")
    for chave, painel in paineis.items():
        print(f" - {chave}: {painel}")


if __name__ == '__main__':
    main()
