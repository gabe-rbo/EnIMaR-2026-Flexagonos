# Subpacote `src/kinematics`: Cinemática de Dobras, Camadas e Grafos

Este módulo modela o comportamento físico e combinatório dos flexágonos enquanto objetos tridimensionais de papel dobrado.

---

## Arquivos e Responsabilidades

### Modelo de Camadas (Layered Folding)
- **`camadas.py` & `flexcamadas.py`**: Modelo com camadas sob as condições de Justin (não auto-intersecção).
- **`hexcamadas.py`**: Modelo de camadas para o reticulado triangular $\mathbb{Z}[\omega]$ e flexão de pinça (*pinch flex*).
- **`run_camadas.py` & `run_hexcamadas.py`**: Cálculo da órbita do estado montado com suporte a checkpoints.
- **`run_livre.py`**: Simulação da órbita no majorante de abertura livre.
- **`analise_camadas.py`**: Análise dos arranjos alcançáveis e determinação de $\Gamma$.

### Decomposição Combinatória & Grafos
- **`componentes.py`**: Decomposição exaustiva do espaço de 216.768 estados dobrados (identificação da ilha principal de 19.200 estados e dos 20.404 grãos menores).
- **`paridade.py`**: Caracterização combinatória dos arranjos a partir do vetor de coordenadas de dobra $u \in \{0,1,2\}^4$.
- **`flexgrafo.py` & `mecanica.py`**: Grafos de transição de estados e mapas de retorno.
- **`flexes_realizados.py`**: Enumeração dos mapas de retorno fisicamente realizáveis.

### Dobraduras e Redes Específicas
- **`foldings.py`**: As 70 dobraduras do hexa-tetraflexágono.
- **`foldings_tri.py` & `busca_tri.py`**: As 6 dobraduras do tri-tetraflexágono (tira rasgada + colagem).
- **`rotflex.py` & `hexaflex.py` & `hexaflex_an.py`**: Cinemática e teorema das retas de dobra para hexaflexágonos.
- **`censo_hex.py`**: Censo triangular em blocos.
- **`plano_tri.py` & `flexagon_sim.py`**: Simulação da dobradura e extração de figuras do manual.

### Verificadores e Testes de Resíduo
- **`verify2.py`**: Verificação numérica das soluções (resíduos $\approx 10^{-15}$).
- **`verify_camadas.py`**: 42 testes exatos de tetraflexágonos e componentes.
- **`verify_geral.py`**: 23 testes gerais ($W^+$, hexaflexágonos, $C_{12}$, catálogos).
