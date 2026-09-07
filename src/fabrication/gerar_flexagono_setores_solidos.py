"""
Script de Geração do Flexágono de Funções Racionais Orgânicas em Cores Sólidas (Setores Angulares).
Desenvolvido para o EnIMaR 2026.

Todas as faces são coloridas exclusivamente em 6 Cores Sólidas (PALETTE_SOLID_6),
seguindo a mesma linguagem visual fluida, elegante e intrigante da Face 1 do flexágono
de cores sólidas original, com pontos de sela (críticos) e vórtices assimétricos.
Nenhuma face contém singularidades essenciais (todas são funções puramente racionais):
- Face 1: Tríade Canônica — f(z) = (z - 1)/(z^2 + z + 1)
- Face 2: Aerofólio Ondulante — f(z) = (z^3 - 1)/(z^3 - 3z + 1)
- Face 3: Triquetra em Crescente — f(z) = (z^3 - 1.5z + 1)/(z^4 + z^2 + 1)
- Face 4: Escudo Quártico Torcido — f(z) = (z^4 - z + 0.5)/(z^3 + 1)
- Face 5: Flor Quíntupla Assimétrica — f(z) = (z^5 - 2z^2 + 1)/(z^4 + 1.5z + 1)
- Face 6: Mandala de Paisley — f(z) = (z^3 - 1)(z^2 + 0.5z + 1)/(z^4 - z^2 + 1.2)

Gera:
1. As 6 faces em 4K UHD (3840x3840 px).
2. O painel comparativo 2x3 de alta definição.
3. As pranchas de corte e impressão (Plano_Frontal_SetoresSolidos.png e Plano_Traseiro_SetoresSolidos.png, 4840x4840 px).
4. O diagrama de dinâmica de flexão (4K).
5. O README.md documentando a matemática e especificações.
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


def criar_painel_setores_solidos(
    faces: dict,
    output_path: Path
):
    """Cria um painel comparativo 2x3 em alta resolução com as 6 faces em cores sólidas."""
    titles = {
        'face1': "Face 1: Tríade Canônica — (z - 1)/(z² + z + 1)",
        'face2': "Face 2: Aerofólio Ondulante — (z³ - 1)/(z³ - 3z + 1)",
        'face3': "Face 3: Triquetra em Crescente — (z³ - 1.5z + 1)/(z⁴ + z² + 1)",
        'face4': "Face 4: Escudo Quártico Torcido — (z⁴ - z + 0.5)/(z³ + 1)",
        'face5': "Face 5: Flor Quíntupla — (z⁵ - 2z² + 1)/(z⁴ + 1.5z + 1)",
        'face6': "Face 6: Mandala de Paisley — (z³ - 1)(z² + 0.5z + 1)/(z⁴ - z² + 1.2)"
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
    out_dir = PROJECT_ROOT / "grafica" / "sem_watermark" / "flexagono_setores_solidos"
    faces_dir = out_dir / "faces"
    faces_dir.mkdir(parents=True, exist_ok=True)

    resolution = (3840, 3840)
    x_range = (-2.2, 2.2)
    y_range = (-2.2, 2.2)

    # Definição das 6 funções racionais intrigantes e elegantes (sem singularidades essenciais)
    funcoes = {
        'face1': {
            'nome': "Tríade Canônica",
            'formula': "(z - 1)/(z^2 + z + 1)",
            'func': lambda z: (z - 1.0) / (z**2 + z + 1.0),
            'zeros': "z = 1 (ordem 1)",
            'polos': "z = e^{±2πi/3} = -1/2 ± i√3/2 (ordem 1)",
            'descricao': "A clássica Face 1 com 1 zero e 2 polos, originando pétalas fluidas e assimétricas."
        },
        'face2': {
            'nome': "Aerofólio Ondulante",
            'formula': "(z^3 - 1)/(z^3 - 3z + 1)",
            'func': lambda z: (z**3 - 1.0) / (z**3 - 3.0*z + 1.0),
            'zeros': "z = 1, e^{±2πi/3} (ordem 1)",
            'polos': "3 raízes de z^3 - 3z + 1 = 0",
            'descricao': "Corpo hidrodinâmico em forma de gota/aerofólio com cauda ondulante e vórtices alternados."
        },
        'face3': {
            'nome': "Triquetra em Crescente",
            'formula': "(z^3 - 1.5z + 1)/(z^4 + z^2 + 1)",
            'func': lambda z: (z**3 - 1.5*z + 1.0) / (z**4 + z**2 + 1.0),
            'zeros': "3 raízes de z^3 - 1.5z + 1 = 0",
            'polos': "z = e^{±πi/3}, e^{±2πi/3} (ordem 1)",
            'descricao': "Asa em crescente vermelho à direita com gotas cintilantes internas e canal em ampulheta."
        },
        'face4': {
            'nome': "Escudo Quártico Torcido",
            'formula': "(z^4 - z + 0.5)/(z^3 + 1)",
            'func': lambda z: (z**4 - z + 0.5) / (z**3 + 1.0),
            'zeros': "4 raízes de z^4 - z + 0.5 = 0",
            'polos': "z = -1, e^{±πi/3} (ordem 1)",
            'descricao': "Escudo alado central com pétalas sinuosas, redemoinho lateral e ondas orgânicas fluindo pelas bordas."
        },
        'face5': {
            'nome': "Flor Quíntupla Assimétrica",
            'formula': "(z^5 - 2z^2 + 1)/(z^4 + 1.5z + 1)",
            'func': lambda z: (z**5 - 2.0*z**2 + 1.0) / (z**4 + 1.5*z + 1.0),
            'zeros': "5 raízes de z^5 - 2z^2 + 1 = 0",
            'polos': "4 raízes de z^4 + 1.5z + 1 = 0",
            'descricao': "Dois núcleos entrelaçados em escudo, flor de pétalas duplas à direita e cúpula sinuosa à esquerda."
        },
        'face6': {
            'nome': "Mandala de Paisley",
            'formula': "(z^3 - 1)(z^2 + 0.5z + 1)/(z^4 - z^2 + 1.2)",
            'func': lambda z: ((z**3 - 1.0)*(z**2 + 0.5*z + 1.0)) / (z**4 - z**2 + 1.2),
            'zeros': "z = 1, e^{±2πi/3}, -0.25 ± i√15/4",
            'polos': "4 polos de z^4 - z^2 + 1.2 = 0",
            'descricao': "Duas gotas de Paisley perfeitamente entrelaçadas à esquerda, escudo central e pétalas estendidas à direita."
        }
    }

    print(">>> 1. Renderizando as 6 Faces Orgânicas em Cores Sólidas 4K UHD (3840x3840)...")
    faces = {}
    face_paths = []

    for i in range(1, 7):
        key = f'face{i}'
        info = funcoes[key]
        print(f" - Renderizando {key}: {info['nome']} — f(z) = {info['formula']}...")
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

    print(">>> 2. Gerando Painel Comparativo 2x3...")
    painel_path = out_dir / "painel_6_faces_setores_solidos.png"
    criar_painel_setores_solidos(faces, painel_path)

    print(">>> 3. Montando Planificações de Impressão (Tetraflexágono 4840x4840 sem watermark)...")
    frontal_path = out_dir / "Plano_Frontal_SetoresSolidos.png"
    traseiro_path = out_dir / "Plano_Traseiro_SetoresSolidos.png"
    gerar_planificacao_tetraflexagono(
        faces_paths=face_paths,
        output_frontal=frontal_path,
        output_traseiro=traseiro_path,
        trocar_3com5_4com6=True,
        grafica=True,
        scale_factor=2,
        watermark=False
    )

    print(">>> 4. Gerando Diagrama de Dinâmica (flexão) em 4K...")
    diagrama_path = out_dir / "Diagrama_Dinamica_SetoresSolidos.png"
    gerar_diagrama_dinamica(face_paths, diagrama_path)

    print(">>> 5. Gerando README.md do Acervo...")
    readme_path = out_dir / "README.md"
    readme_content = f"""# Flexágono de Funções Racionais Orgânicas em Cores Sólidas (Setores Angulares)

Coleção de 6 faces puramente coloridas em **Cores Sólidas (6 Setores Angulares de 60°)**, concebidas com a mesma linguagem visual fluida, elegante e intrigante da **Face 1 de referência do flexágono de cores sólidas** ($f_1(z) = \\frac{{z-1}}{{z^2+z+1}}$).

Em vez de distribuições rígidas ou puramente radiais (como raízes da unidade puras), as funções utilizam **interações não-lineares entre zeros, polos e pontos de sela (críticos)**. Isso gera contornos sinuosos, pétalas em forma de gota (*teardrops*), asas em crescente e vórtices entrelaçados.

**Nenhuma face contém singularidades essenciais**: todas as funções são **estritamente racionais** ($P(z)/Q(z)$), possuindo apenas zeros e polos isolados de ordem finita.

---

## 🎨 As 6 Faces e suas Funções Matemáticas

| Face | Nome / Geometria | Função $f(z)$ | Zeros / Polos Principais | Características Visuais |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Tríade Canônica** *(Face 1 original)* | $f_1(z) = \\frac{{z - 1}}{{z^2 + z + 1}}$ | Zeros: $z = 1$<br>Polos: $z = e^{{\\pm 2\\pi i/3}}$ | A clássica Face 1 com 1 zero e 2 polos, originando pétalas fluidas e assimétricas. |
| **2** | **Aerofólio Ondulante** | $f_2(z) = \\frac{{z^3 - 1}}{{z^3 - 3z + 1}}$ | Zeros: $z = 1, e^{{\\pm 2\\pi i/3}}$<br>Polos: raízes de $z^3 - 3z + 1 = 0$ | Corpo hidrodinâmico em forma de gota/aerofólio com cauda ondulante e vórtices alternados. |
| **3** | **Triquetra em Crescente** | $f_3(z) = \\frac{{z^3 - 1.5z + 1}}{{z^4 + z^2 + 1}}$ | Zeros: raízes de $z^3 - 1.5z + 1 = 0$<br>Polos: $z = e^{{\\pm \\pi i/3}}, e^{{\\pm 2\\pi i/3}}$ | Asa em crescente vermelho à direita com gotas cintilantes internas e canal em ampulheta. |
| **4** | **Escudo Quártico Torcido** | $f_4(z) = \\frac{{z^4 - z + 0.5}}{{z^3 + 1}}$ | Zeros: 4 raízes de $z^4 - z + 0.5 = 0$<br>Polos: $z = -1, e^{{\\pm \\pi i/3}}$ | Escudo alado central com pétalas sinuosas, redemoinho lateral e ondas orgânicas fluindo pelas bordas. |
| **5** | **Flor Quíntupla Assimétrica** | $f_5(z) = \\frac{{z^5 - 2z^2 + 1}}{{z^4 + 1.5z + 1}}$ | Zeros: 5 raízes de $z^5 - 2z^2 + 1 = 0$<br>Polos: 4 raízes de $z^4 + 1.5z + 1 = 0$ | Dois núcleos entrelaçados em escudo, flor de pétalas duplas à direita e cúpula sinuosa à esquerda. |
| **6** | **Mandala de Paisley** | $f_6(z) = \\frac{{(z^3 - 1)(z^2 + 0.5z + 1)}}{{z^4 - z^2 + 1.2}}$ | Zeros: 5 raízes no plano<br>Polos: 4 polos de $z^4 - z^2 + 1.2 = 0$ | Duas gotas de Paisley perfeitamente entrelaçadas à esquerda, escudo central e pétalas estendidas à direita. |

### Propriedades Matemáticas:
- **Ausência de Singularidades Essenciais:** Funções racionais $P(z)/Q(z)$ possuem apenas singularidades polares isoladas de ordem finita em $\\mathbb{{C}}$ (e em $\\hat{{\\mathbb{{C}}}}$). Não há acúmulo infinito de oscilações nem comportamento caótico picardiano.
- **Setores Angulares Sólidos:** A fase $\\arg(w) \\in [0, 2\\pi)$ é particionada em 6 intervalos de $60^\\circ$ mapeados para a paleta pura:
  1. $[0^\\circ, 60^\\circ)$: **Vermelho** `rgb(230, 25, 25)`
  2. $[60^\\circ, 120^\\circ)$: **Amarelo** `rgb(245, 185, 0)`
  3. $[120^\\circ, 180^\\circ)$: **Verde** `rgb(25, 175, 45)`
  4. $[180^\\circ, 240^\\circ)$: **Ciano** `rgb(0, 200, 230)`
  5. $[240^\\circ, 300^\\circ)$: **Azul** `rgb(30, 70, 225)`
  6. $[300^\\circ, 360^\\circ)$: **Magenta** `rgb(210, 30, 210)`
- **Comportamento Topológico e Pontos Críticos:** Em pontos onde $f'(z) = 0$ (pontos de sela da fase), as fronteiras entre os setores de cor bifurcam e curvam-se suavemente, gerando as belas formas orgânicas observadas.

---

## 🖨️ Arquivos Gráficos Prontos para Impressão e Montagem

- **Painel Comparativo 2x3:** [`painel_6_faces_setores_solidos.png`](painel_6_faces_setores_solidos.png) ($2820 \\times 2040$ px)
- **Plano Frontal (Frente):** [`Plano_Frontal_SetoresSolidos.png`](Plano_Frontal_SetoresSolidos.png) ($4840 \\times 4840$ px, alta definição gráfica)
- **Plano Traseiro (Verso):** [`Plano_Traseiro_SetoresSolidos.png`](Plano_Traseiro_SetoresSolidos.png) ($4840 \\times 4840$ px, alta definição gráfica)
- **Diagrama de Dinâmica (flexão 4K):** [`Diagrama_Dinamica_SetoresSolidos.png`](Diagrama_Dinamica_SetoresSolidos.png)
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
