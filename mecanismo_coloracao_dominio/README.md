# Mecanismo da Coloração de Domínio — sequência didática

Quatro imagens (1920×1080, 16:9) que mostram o **mecanismo** por trás da coloração de
domínio, passo a passo: como a fase de $f(z)$ vira uma cor, e como essa cor volta a ser
pintada no domínio.

Mesma ideia pedagógica das págs. 11–15 de Ponce Campuzano, J.C., *"Visualising complex
functions: Enhanced phase portraits"*, Delta (2019) — <https://www.jcponce.com> — mas
redesenhada do zero: geometria, tipografia e paleta são as nossas (cores oficiais EnIMaR
2026: `EnimarNavy`/`EnimarTeal`/`EnimarGold`), nenhum elemento gráfico daquele PDF foi
reaproveitado. **Dar crédito a Ponce Campuzano (2019) como referência da ideia ao usar
essas imagens.**

Complementa (não substitui) o slide "Como Enxergar Funções Complexas?" já existente no
minicurso: aquele explica o *porquê* (matiz = ângulo, luminosidade = módulo); esta
sequência explica o *como* — o mecanismo computacional passo a passo.

## Os 4 arquivos

1. `mecanismo_passo1.png` — o domínio $D_h$: uma malha de pontos, com $z_1, z_2, z_3$
   marcados.
2. `mecanismo_passo2.png` — cada ponto recebe seu valor $f(z)$ num contradomínio
   esquemático $Y = f(D_h)$.
3. `mecanismo_passo3.png` — a fase $f/|f|$ de cada valor aponta para um ponto na roda de
   cores (matiz $= \arg(f(z)/|f(z)|)$).
4. `mecanismo_passo4.png` — de volta ao domínio: cada ponto $z_i$ pintado com a cor lida
   na roda.

A ideia é usar um por slide (ou mais, se quiser), na ordem 1→4, para construir a
explicação progressivamente — do jeito que o Ponce Campuzano fez nas dele.

## Regenerar / ajustar

`python3 gerar_mecanismo.py` (precisa de `numpy` e `matplotlib`; roda direto no Python do
sistema do Mac, sem precisar do `.venv` do projeto). Os 3 pontos de exemplo (posição no
domínio, posição esquemática em $Y$ e matiz de destino) estão no dicionário `PONTOS` no
topo do script — mude ali se quiser outras posições/cores, ou adicione um 4º ponto.
