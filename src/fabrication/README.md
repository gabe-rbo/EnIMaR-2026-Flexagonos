# Subpacote `src/fabrication`: Engenharia de Corte, Facas e Planificações

Este módulo é responsável por transformar as imagens das faces em **pranchas de impressão profissionais prontas para gráfica**.

---

## Arquivos e Responsabilidades

- **`flexagon_domain_faces.py`**: Pipeline unificado para gerar as 6 faces da coloração de domínio, montar o painel comparativo 2×3 e compilar as pranchas `Plano_Frontal_DomainColoring.png` e `Plano_Traseiro_DomainColoring.png` em [`grafica/flexagono_coloracao_dominio/`](../../grafica/flexagono_coloracao_dominio/).
- **`GeradorDeFacas.py`**: Geração vetorial de marcas de registro (cruzes e círculos nos cantos e centro), linhas de corte e vincos pontilhados para a faca de corte.
- **`tetraflexagonos.py`**: Montador paramétrico de planificações frontal e traseira para tetraflexágonos com cálculo de sangrias e interpolação Lanczos.
- **`tritetraflexagonos.py`**: Montador de planificações para o tri-tetraflexágono.

---

## Execução

Para gerar o kit completo do flexágono de domínio colorido:
```bash
python src/fabrication/flexagon_domain_faces.py
```
