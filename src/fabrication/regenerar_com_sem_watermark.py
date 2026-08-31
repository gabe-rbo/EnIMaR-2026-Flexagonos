"""
Reorganiza grafica/ em duas subpastas — com_watermark/ e sem_watermark/ — e regenera
painéis (com a correção de fonte para caracteres especiais), planos de impressão e
diagramas de dinâmica para cada flexágono, reaproveitando as faces já renderizadas
(sem recomputar nada matematicamente pesado).

- com_watermark/: os 5 flexágonos que a Aniura pediu para imprimir (curvas polares,
  os DOIS candidatos de coloração de domínio — para ela escolher — galeria sólida e
  artigo sólido), com watermark=True (assinatura "Feito na UFMG" + logo no verso).
- sem_watermark/: arquivo completo dos 7 flexágonos válidos (os 5 acima + cores_solidas
  + a pasta antiga flexagono_coloracao_dominio), com watermark=False.
  (flexagono_curvas_polares antigo, contaminado, é propositalmente ignorado — decisão
  já tomada com o Gabe.)

Desenvolvido para o EnIMaR 2026.
"""

import sys
import shutil
from pathlib import Path

from PIL import Image

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "core"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "kinematics"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "visualization"))
sys.path.insert(0, str(PROJECT_ROOT / "src" / "fabrication"))

from flexagon_domain_faces import (
    gerar_planificacao_tetraflexagono,
    gerar_diagrama_dinamica,
    criar_painel_comparativo,
)
from gerar_flexagono_artigo_solido import criar_painel_artigo
from gerar_flexagono_cores_solidas import criar_painel_comparativo_solidas
from gerar_flexagono_galeria_solida import criar_painel_galeria
from gerar_flexagono_curvas_polares_cores_solidas import criar_painel_comparativo_curvas_polares

GRAFICA = PROJECT_ROOT / "grafica"

# (pasta, funcao_painel, nome_arquivo_painel, sufixo_plano, nome_arquivo_diagrama, incluir_em_com_watermark)
RECEITAS = [
    ("flexagono_artigo_solido", criar_painel_artigo,
     "painel_6_faces_artigo.png", "ArtigoSolido", "Diagrama_Dinamica_ArtigoSolido.png", True),
    ("flexagono_cores_solidas", criar_painel_comparativo_solidas,
     "painel_6_faces_cores_solidas.png", "CoresSolidas", "Diagrama_Dinamica_CoresSolidas.png", False),
    ("flexagono_galeria_solida", criar_painel_galeria,
     "painel_6_faces_galeria.png", "GaleriaSolida", "Diagrama_Dinamica_GaleriaSolida.png", True),
    ("flexagonos_curvas_polares_cores_solidas", criar_painel_comparativo_curvas_polares,
     "painel_6_faces_curvas_polares.png", "CurvasPolares", "Diagrama_Dinamica_CurvasPolares.png", True),
    ("flexagono_coloracao_dominio_candidato_A_sin1z", criar_painel_comparativo,
     "painel_6_faces_domain_coloring.png", "DomainColoring", "Diagrama_Dinamica_DomainColoring.png", True),
    ("flexagono_coloracao_dominio_candidato_B_racional", criar_painel_comparativo,
     "painel_6_faces_domain_coloring.png", "DomainColoring", "Diagrama_Dinamica_DomainColoring.png", True),
    ("flexagono_coloracao_dominio", criar_painel_comparativo,
     "painel_6_faces_domain_coloring.png", "DomainColoring", "Diagrama_Dinamica_DomainColoring.png", False),
]


def processar(nome_pasta, painel_fn, painel_nome, sufixo_plano, diagrama_nome, watermark, dest_root):
    src_dir = GRAFICA / nome_pasta
    faces_dir = src_dir / "faces"
    dest_dir = dest_root / nome_pasta
    dest_faces_dir = dest_dir / "faces"
    dest_faces_dir.mkdir(parents=True, exist_ok=True)

    face_paths = []
    faces_imgs = {}
    for i in range(1, 7):
        key = f"face{i}"
        src_p = faces_dir / f"{key}.png"
        dst_p = dest_faces_dir / f"{key}.png"
        if not dst_p.exists():
            shutil.copy2(src_p, dst_p)
        faces_imgs[key] = Image.open(src_p).convert("RGB")
        face_paths.append(str(dst_p))

    print("  -> Painel comparativo (fonte corrigida)...")
    painel_path = dest_dir / painel_nome
    painel_fn(faces_imgs, painel_path)

    print(f"  -> Planificacao de impressao (watermark={watermark})...")
    frontal_path = dest_dir / f"Plano_Frontal_{sufixo_plano}.png"
    traseiro_path = dest_dir / f"Plano_Traseiro_{sufixo_plano}.png"
    gerar_planificacao_tetraflexagono(
        faces_paths=face_paths,
        output_frontal=frontal_path,
        output_traseiro=traseiro_path,
        trocar_3com5_4com6=True,
        grafica=True,
        scale_factor=2,
        watermark=watermark,
    )

    print("  -> Diagrama de dinamica (4K)...")
    diagrama_path = dest_dir / diagrama_nome
    gerar_diagrama_dinamica(face_paths, diagrama_path)

    src_readme = src_dir / "README.md"
    if src_readme.exists():
        shutil.copy2(src_readme, dest_dir / "README.md")

    print(f"  OK: {dest_dir}")


def main():
    com_dir = GRAFICA / "com_watermark"
    sem_dir = GRAFICA / "sem_watermark"
    com_dir.mkdir(exist_ok=True)
    sem_dir.mkdir(exist_ok=True)

    for nome_pasta, painel_fn, painel_nome, sufixo_plano, diagrama_nome, incluir_com in RECEITAS:
        print(f"\n=== {nome_pasta} ===")
        print(" [sem_watermark]")
        processar(nome_pasta, painel_fn, painel_nome, sufixo_plano, diagrama_nome, False, sem_dir)
        if incluir_com:
            print(" [com_watermark]")
            processar(nome_pasta, painel_fn, painel_nome, sufixo_plano, diagrama_nome, True, com_dir)

    print("\n>>> SUCESSO! grafica/com_watermark/ e grafica/sem_watermark/ regenerados.")


if __name__ == '__main__':
    main()
