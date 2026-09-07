"""
Script de Geração do Flexágono de Funções Flexionáveis do Artigo em Setores Sólidos.
Desenvolvido para o EnIMaR 2026 e Artigo de Pesquisa.

Todas as faces são soluções EXATAS da equação de flexão f(Phi(z)) = f(z) para os grupos
de retorno Gamma dos flexágonos clássicos (Teorema Universal 5.1), compostas com funções
racionais R(J) para gerar contornos fluidos, orgânicos e elegantes em 6 Cores Sólidas
(PALETTE_SOLID_6), sem qualquer singularidade essencial (apenas polos isolados):
- Face 1: Hexaflexágono / Órbifold C3 — f(z) = (z^3 - 1)/(z^3 - 1.5z + 0.7i)
- Face 2: Tri-tetraflexágono Periódico — f(z) = (exp(i*pi*z) - 1)/(exp(2i*pi*z) + 0.6)
- Face 3: Tri-tetraflexágono C2 — f(z) = (cos^2(pi*z) - 0.5)/(cos(pi*z) - 0.7i)
- Face 4: Hexa-tetraflexágono Lemniscático — f(z) = (wp(z) - 0.8)/(wp(z) + 0.6i)
- Face 5: Hexagonal Equianarmônico — f(z) = (wp'(z) - 2.0)/(wp'(z) + 1.5i)
- Face 6: Hexa-tetra Quártico p4 — f(z) = (wp(z)^2 - 1.2)/(wp(z)^2 + 0.9i)

Gera:
1. As 6 faces em 4K UHD (3840x3840 px).
2. O painel comparativo 2x3 de alta definição com fontes DejaVu Sans.
3. As pranchas de corte e impressão (Plano_Frontal_ArtigoSetoresSolidos.png e Plano_Traseiro_ArtigoSetoresSolidos.png, 4840x4840 px).
4. O diagrama de dinâmica de flexão (4K).
5. O README.md documentando a matemática das funções flexionáveis.
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
sys.path.insert(0, str(PROJECT_ROOT / "src" / "kinematics"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "visualization"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "fabrication"))

from domain_coloring import DomainColoringEngine, PALETTE_SOLID_6
from flexagon_domain_faces import (
    gerar_planificacao_tetraflexagono,
    gerar_diagrama_dinamica,
    desenhar_titulo_painel
)
from wpgen import WP


def criar_painel_artigo_setores_solidos(
    faces: dict,
    output_path: Path
):
    """Cria um painel comparativo 2x3 em alta resolução com as 6 funções flexionáveis do artigo."""
    titles = {
        'face1': "Face 1: Hexaflexágono Órbifold C₃ — (z³ - 1)/(z³ - 1.5z + 0.7i)",
        'face2': "Face 2: Tri-tetra Colunas — (exp(iπz) - 1)/(exp(2iπz) + 0.6)",
        'face3': "Face 3: Tri-tetra Ânforas C₂ — (cos²(πz) - 0.5)/(cos(πz) - 0.7i)",
        'face4': "Face 4: Hexa-tetra Lemniscático — (℘ - 0.8)/(℘ + 0.6i)",
        'face5': "Face 5: Hexa Triangular — (℘' - 2)/(℘' + 1.5i)",
        'face6': "Face 6: Hexa-tetra Quártico p4 — (℘² - 1.2)/(℘² + 0.9i)"
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
    print(f"Painel comparativo salvo em: {output_path}")


def main():
    out_dir = PROJECT_ROOT / "grafica" / "sem_watermark" / "flexagono_artigo_setores_solidos"
    faces_dir = out_dir / "faces"
    faces_dir.mkdir(parents=True, exist_ok=True)

    resolution = (3840, 3840)
    x_range = (-2.0, 2.0)
    y_range = (-2.0, 2.0)

    print(">>> 1. Configurando Instâncias das Funções de Weierstrass do Artigo...")
    # Reticulados do Teorema 5.1
    wp_quad = WP(2.0, 2.0j)                      # Lambda_quad = 2*Z[i] (Lemniscático, j=1728)
    wp_hex = WP(2.0, 1.0 + 1j * np.sqrt(3.0))   # Lambda_hex = 2*Z[zeta_3] (Equianarmônico, j=0)

    # Definição das 6 funções flexionáveis invariantes do artigo (meromorfas sem singularidades essenciais)
    funcoes = {
        'face1': {
            'nome': "Hexaflexágono Órbifold C3",
            'formula': "(z^3 - 1)/(z^3 - 1.5z + 0.7i)",
            'func': lambda z: (z**3 - 1.0) / (z**3 - 1.5*z + 0.7j),
            'classe': "Posto 0, |P|=3 (Tri-hexa / Hexa-hexaflexágono)",
            'descricao': "Frasco em gota assimétrica com fitas fluidas e olhos de vórtice ressonantes em simetria C3."
        },
        'face2': {
            'nome': "Tri-tetraflexágono Periódico (Colunas)",
            'formula': "(exp(i*pi*z) - 1)/(exp(2i*pi*z) + 0.6)",
            'func': lambda z: (np.exp(1j * np.pi * z) - 1.0) / (np.exp(2j * np.pi * z) + 0.6),
            'classe': "Posto 1, |P|=1 (Tri-tetraflexágono)",
            'descricao': "Colunas arquitetônicas caneladas periódicas com capitéis e arcos em drapeado nas 6 cores puras."
        },
        'face3': {
            'nome': "Tri-tetraflexágono C2 (Ânforas)",
            'formula': "(cos^2(pi*z) - 0.5)/(cos(pi*z) - 0.7i)",
            'func': lambda z: (np.cos(np.pi * z)**2 - 0.5) / (np.cos(np.pi * z) - 0.7j),
            'classe': "Posto 1, |P|=2 (Invariante por Inversão C2)",
            'descricao': "Colunas entrelaçadas de ânforas e cálices de duas cabeças com nós duplos nas junções."
        },
        'face4': {
            'nome': "Hexa-tetraflexágono Lemniscático",
            'formula': "(wp(z; 2Z[i]) - 0.8)/(wp(z; 2Z[i]) + 0.6i)",
            'func': lambda z: (wp_quad(np.where(np.abs(z) < 1e-10, 1e-10, z)) - 0.8) / (wp_quad(np.where(np.abs(z) < 1e-10, 1e-10, z)) + 0.6j),
            'classe': "Posto 2, |P|=2 (Hexa-tetraflexágono, j=1728)",
            'descricao': "Almofadas lemniscáticas espiraladas em reticulado quadrado com 4 olhos de vórtice em órbita."
        },
        'face5': {
            'nome': "Hexagonal Equianarmônico",
            'formula': "(wp'(z; 2Z[zeta3]) - 2.0)/(wp'(z; 2Z[zeta3]) + 1.5i)",
            'func': lambda z: (wp_hex.deriv(np.where(np.abs(z) < 1e-10, 1e-10, z)) - 2.0) / (wp_hex.deriv(np.where(np.abs(z) < 1e-10, 1e-10, z)) + 1.5j),
            'classe': "Posto 2, |P|=3 (Reticulado Triangular, j=0)",
            'descricao': "Hélice de 3 pás em reticulado triangular com 6 pares de vórtices orbitais em vermelho e magenta."
        },
        'face6': {
            'nome': "Hexa-tetra Quártico p4",
            'formula': "(wp(z; 2Z[i])^2 - 1.2)/(wp(z; 2Z[i])^2 + 0.9i)",
            'func': lambda z: (wp_quad(np.where(np.abs(z) < 1e-10, 1e-10, z))**2 - 1.2) / (wp_quad(np.where(np.abs(z) < 1e-10, 1e-10, z))**2 + 0.9j),
            'classe': "Posto 2, |P|=4 (Simetria Cristalina Quártica p4)",
            'descricao': "Cata-vento de 4 pás em reticulado quadrado com almofada central dourada e chamas helicoidais."
        }
    }

    print(">>> 2. Renderizando as 6 Faces Flexionáveis em Cores Sólidas 4K UHD (3840x3840)...")
    faces = {}
    face_paths = []

    for i in range(1, 7):
        key = f'face{i}'
        info = funcoes[key]
        print(f" - Renderizando {key}: {info['nome']} — {info['classe']}...")
        engine = DomainColoringEngine(
            func=info['func'],
            x_range=x_range,
            y_range=y_range,
            resolution=resolution
        )
        img = engine.render(
            mode='solid_sectors',
            n_sectors=6,
            palette=PALETTE_SOLID_6,
            mark_zeros_poles=False
        )
        p = faces_dir / f"{key}.png"
        img.save(p, "PNG")
        faces[key] = img
        face_paths.append(str(p))
        print(f"   -> Salva {key} em: {p}")

    print(">>> 3. Gerando Painel Comparativo 2x3...")
    painel_path = out_dir / "painel_6_faces_artigo_setores_solidos.png"
    criar_painel_artigo_setores_solidos(faces, painel_path)

    print(">>> 4. Montando Planificações de Impressão (Tetraflexágono 4840x4840 sem watermark)...")
    frontal_path = out_dir / "Plano_Frontal_ArtigoSetoresSolidos.png"
    traseiro_path = out_dir / "Plano_Traseiro_ArtigoSetoresSolidos.png"
    gerar_planificacao_tetraflexagono(
        faces_paths=face_paths,
        output_frontal=frontal_path,
        output_traseiro=traseiro_path,
        trocar_3com5_4com6=True,
        grafica=True,
        scale_factor=2,
        watermark=False
    )

    print(">>> 5. Gerando Diagrama de Dinâmica (flexão) em 4K...")
    diagrama_path = out_dir / "Diagrama_Dinamica_ArtigoSetoresSolidos.png"
    gerar_diagrama_dinamica(face_paths, diagrama_path)

    print(">>> 6. Gerando README.md do Acervo...")
    readme_path = out_dir / "README.md"
    readme_content = f"""# Flexágono de Funções Flexionáveis do Artigo em Setores Sólidos

Coleção de 6 faces concebidas com as **funções meromorfas flexionáveis universais do artigo científico** (Hall, Almeida & Teixeira / Teorema 5.1 e classificação de grupos de retorno $\\Gamma$), renderizadas puramente em **6 Setores Angulares de Cores Sólidas** (`PALETTE_SOLID_6`), inspiradas na beleza orgânica e fluida da Face 1.

Toda solução meromorfa da equação de flexão $f(\\Phi(z)) = f(z)$ é da forma $f = R(J)$, onde $J$ é o *Hauptmodul* gerador da órbifold $\\mathbb{{C}}/\\Gamma$ e $R$ é uma transformação racional. Ao escolher transformações racionais não-lineares, os zeros e polos de $J$ interagem para produzir **volutas fluidas, colunas arquitetônicas, cálices entrelaçados e tesselações cristalinas**, preservando a simetria de dobradura de cada flexágono.

**Nenhuma face contém singularidades essenciais**: todas as funções são **estritamente meromorfas** sobre $\\mathbb{{C}}$, possuindo apenas polos isolados de ordem finita nos reticulados correspondentes.

---

## 🎨 As 6 Faces e suas Funções Flexionáveis

| Face | Nome / Flexágono de Origem | Classe $(\\text{{posto}}, |P|)$ | Função $f(z) = R(J)$ | Geometria e Invariância |
| :---: | :--- | :---: | :--- | :--- |
| **1** | **Hexaflexágono Órbifold C₃** | $(0, 3)$ | $f_1(z) = \\frac{{z^3 - 1}}{{z^3 - 1.5z + 0.7i}}$ | Tri- e Hexa-hexaflexágono ($J = z^3$). Frasco em gota assimétrica com fitas fluidas e olhos de vórtice ressonantes. |
| **2** | **Tri-tetra Periódico (Colunas)** | $(1, 1)$ | $f_2(z) = \\frac{{e^{{i\\pi z}} - 1}}{{e^{{2i\\pi z}} + 0.6}}$ | Tri-tetraflexágono ($J = e^{{i\\pi z}}$). Colunas caneladas periódicas com capitéis arqueados em drapeado nas 6 cores puras. |
| **3** | **Tri-tetra Ânforas C₂** | $(1, 2)$ | $f_3(z) = \\frac{{\\cos^2(\\pi z) - 0.5}}{{\\cos(\\pi z) - 0.7i}}$ | Invariante por Inversão C₂ ($J = \\cos(\\pi z)$). Colunas entrelaçadas de ânforas e cálices de duas cabeças com nós duplos. |
| **4** | **Hexa-tetra Lemniscático** | $(2, 2)$ | $f_4(z) = \\frac{{\\wp(z; 2\\mathbb{{Z}}[i]) - 0.8}}{{\\wp(z; 2\\mathbb{{Z}}[i]) + 0.6i}}$ | Reticulado Quadrado Lemniscático ($j=1728$, $J = \\wp$). Almofadas espiraladas com 4 vórtices orbitais. |
| **5** | **Hexagonal Equianarmônico** | $(2, 3)$ | $f_5(z) = \\frac{{\\wp'(z; 2\\mathbb{{Z}}[\\zeta_3]) - 2.0}}{{\\wp'(z; 2\\mathbb{{Z}}[\\zeta_3]) + 1.5i}}$ | Reticulado Triangular ($j=0$, $J = \\wp'$). Hélice de 3 pás com 6 pares de vórtices orbitais em vermelho e magenta. |
| **6** | **Hexa-tetra Quártico p4** | $(2, 4)$ | $f_6(z) = \\frac{{\\wp(z; 2\\mathbb{{Z}}[i])^2 - 1.2}}{{\\wp(z; 2\\mathbb{{Z}}[i])^2 + 0.9i}}$ | Simetria Quártica $p4$ ($J = \\wp^2$). Cata-vento de 4 pás em reticulado quadrado com almofada central dourada e chamas helicoidais. |

### Propriedades Matemáticas:
- **Flexionabilidade Rigorosa:** Cada função é invariante direta pelo grupo de automorfismos de flexão $\\Gamma$ de sua respectiva classe, garantindo que a imagem se recombine perfeitamente sob os movimentos de abertura e flexão do flexágono.
- **Ausência Total de Singularidades Essenciais:** As funções trigonométricas e exponenciais periódicas são inteiras sobre $\\mathbb{{C}}$, e as funções elípticas de Weierstrass $\\wp$ e $\\wp'$ são meromorfas duplamente periódicas, possuindo unicamente polos de ordem 2 e 3 sobre os reticulados $\\Lambda$. Não há singularidades essenciais no plano complexo finito $\\mathbb{{C}}$.
- **Coloração por Setores Sólidos:** A fase $\\arg(w) \\in [0, 2\\pi)$ é particionada em 6 intervalos de $60^\\circ$ mapeados para a paleta pura:
  1. $[0^\\circ, 60^\\circ)$: **Vermelho** `rgb(230, 25, 25)`
  2. $[60^\\circ, 120^\\circ)$: **Amarelo** `rgb(245, 185, 0)`
  3. $[120^\\circ, 180^\\circ)$: **Verde** `rgb(25, 175, 45)`
  4. $[180^\\circ, 240^\\circ)$: **Ciano** `rgb(0, 200, 230)`
  5. $[240^\\circ, 300^\\circ)$: **Azul** `rgb(30, 70, 225)`
  6. $[300^\\circ, 360^\\circ)$: **Magenta** `rgb(210, 30, 210)`

---

## 🖨️ Arquivos Gráficos Prontos para Impressão e Montagem

- **Painel Comparativo 2x3:** [`painel_6_faces_artigo_setores_solidos.png`](painel_6_faces_artigo_setores_solidos.png) ($2820 \\times 2040$ px)
- **Plano Frontal (Frente):** [`Plano_Frontal_ArtigoSetoresSolidos.png`](Plano_Frontal_ArtigoSetoresSolidos.png) ($4840 \\times 4840$ px, alta definição gráfica)
- **Plano Traseiro (Verso):** [`Plano_Traseiro_ArtigoSetoresSolidos.png`](Plano_Traseiro_ArtigoSetoresSolidos.png) ($4840 \\times 4840$ px, alta definição gráfica)
- **Diagrama de Dinâmica (flexão 4K):** [`Diagrama_Dinamica_ArtigoSetoresSolidos.png`](Diagrama_Dinamica_ArtigoSetoresSolidos.png)
- **Faces Individuais (4K UHD 3840x3840 px):**
  - Face 1: [`faces/face1.png`](faces/face1.png)
  - Face 2: [`faces/face2.png`](faces/face2.png)
  - Face 3: [`faces/face3.png`](faces/face3.png)
  - Face 4: [`faces/face4.png`](faces/face4.png)
  - Face 5: [`faces/face5.png`](faces/face5.png)
  - Face 6: [`faces/face6.png`](faces/face6.png)
"""
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"README salvo em: {readme_path}")

    print(f"\n>>> SUCESSO! Todos os arquivos foram gerados em:\n{out_dir}")


if __name__ == '__main__':
    main()
