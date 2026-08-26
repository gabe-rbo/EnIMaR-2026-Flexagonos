# EnIMaR 2026: Funções Complexas Flexionáveis e Coloração de Domínio

Projeto de pesquisa e materiais didáticos para o **Encontro de Inverno de Matemática Recreativa (EnIMaR 2026)** e submissão de artigo científico.

O projeto investiga a conexão entre a **cinemática e simetria de flexágonos** (tetraflexágonos e hexaflexágonos) e a **invariância de funções meromorfas**, integrando técnicas modernas de **Coloração de Domínio (Domain Coloring)** e visualização geométrica.

---

## Estrutura do Repositório

```
.
├── src/                  # Código-fonte Python modularizado por domínio
│   ├── core/             # Teoria matemática, aritmética exata e invariância Γ
│   ├── kinematics/       # Cinemática de flexão, modelo de camadas e grafos
│   ├── visualization/    # Motor de Coloração de Domínio (HSV, Sólidas, Pullback)
│   ├── fabrication/      # Montagem de pranchas gráficas para corte e dobra
│   └── catalog/          # Geradores de catálogos automatizados de soluções
│
├── grafica/              # Arquivos prontos para impressão e corte na gráfica
│   ├── flexagono_coloracao_dominio/  # 6 faces da mesma função + plano frontal/traseiro
│   ├── flexagono_curvas_polares/     # Flexágono de curvas polares (#5)
│   └── catalogos_pdf/                # PDFs dos catálogos de soluções
│
├── pesquisa/             # Artigo científico, materiais do evento e literatura
│   ├── artigo/           # Código-fonte LaTeX completo (28 pp.) e figuras
│   ├── enimar2026/       # Resumos, templates LaTeX e notas da orientadora
│   ├── notebooks/        # Cadernos Jupyter didáticos e exploratórios
│   └── referencias/      # Acervo de artigos e livros em PDF classificados
│
└── tests/                # Suíte de testes unitários automatizados
```

---

## Instalação e Ambiente

O projeto utiliza Python 3.10+ com ambiente virtual (`.venv`):

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Instalar dependências (caso necessário)
pip install -r requirements.txt
```

### Executar Testes
```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

---

## Principais Recursos

### 1. Coloração de Domínio Aprimorada
- **Cores Sólidas:** Discretização angular em $N$ setores sem gradientes contínuos.
- **Mapeamento Conforme de Imagem no Plano $w$ (*Image Pullback*):** Projeção $f^*(I)(z) = I(f(z))$ para qualquer imagem ou padrão cartesiano/polar.
- **Estilo Elias Wegert:** Gráficos com curvas de nível de módulo e raios isocromáticos (*Enhanced Phase Plots*).

### 2. Geração Automatizada de Flexágonos
- Geração instantânea de pranchas com sangrias gráficas e marcas de registro vetoriais:
```bash
python src/fabrication/flexagon_domain_faces.py
```
As pranchas são salvas diretamente em [`grafica/flexagono_coloracao_dominio/`](grafica/flexagono_coloracao_dominio/).
