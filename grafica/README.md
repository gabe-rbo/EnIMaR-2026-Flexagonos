# Diretório `grafica`: Acervo Geral de Pranchas e Flexágonos Prontos para Impressão

Este diretório armazena todos os produtos finais gerados pelo projeto destinados à **impressão gráfica profissional** (alta definição, com sangrias de corte e cruzes vetoriais de registro), montagem física e oficinas do **EnIMaR 2026**.

---

## 🗂️ Estrutura Atual

```
grafica/
├── com_watermark/   # 🖨️ OS 5 FLEXÁGONOS PARA A GRÁFICA — com assinatura "Feito na UFMG" + logo no verso
├── sem_watermark/   # 📦 Acervo completo (7 flexágonos válidos) — sem assinatura, para arquivo/catálogo
├── flexagono_curvas_polares/   # ⚠️ Pasta antiga/contaminada — NÃO USAR (ver nota abaixo)
└── catalogos_pdf/               # 📚 Catálogos Sistemáticos em PDF (Tetra e Hexaflexágonos)
```

O diretório foi reorganizado nessa estrutura de duas coleções para deixar claro, de forma
inequívoca, qual arquivo vai para a gráfica (com a assinatura da UFMG no verso, como a Aniura
pediu) e qual é só o acervo interno/arquivo.

### `com_watermark/` — os 5 flexágonos que vão para a gráfica

Exatamente os que a Aniura pediu no e-mail, cada um com painel comparativo (fonte corrigida —
sem mais caixas com "X" nos caracteres especiais), Plano Frontal, Plano Traseiro **com a
assinatura "Feito na UFMG por" + logo do EnIMaR no verso**, e diagrama de dinâmica em 4K:

| Pasta | Conteúdo |
| :--- | :--- |
| `flexagonos_curvas_polares_cores_solidas/` | Curvas polares clássicas (Borboleta, Estrela, Rosáceas, Flor de Lótus) |
| `flexagono_coloracao_dominio_candidato_A_sin1z/` | Coloração de domínio — candidato A: $f(z)=\sin(1/z)$ |
| `flexagono_coloracao_dominio_candidato_B_racional/` | Coloração de domínio — candidato B: $f(z)=z^5/(z^4-1)$ |
| `flexagono_galeria_solida/` | Galeria de 6 geometrias heterogêneas em cores sólidas |
| `flexagono_artigo_solido/` | As 6 classes universais do Teorema 5.1 do artigo |

Os dois candidatos de coloração de domínio (A e B) estão incluídos os dois, lado a lado, por
decisão do Gabe — a ideia é a Aniura escolher visualmente qual vai para a versão final antes da
impressão (ou imprimir os dois, se preferir).

### `sem_watermark/` — acervo completo (arquivo/catálogo)

Os mesmos 5 flexágonos acima **mais** `flexagono_cores_solidas/` e o `flexagono_coloracao_dominio/`
antigo (função repetida de `cores_solidas`, mantido só por completude), todos sem a assinatura da
UFMG no verso — para catálogo, referência e reimpressões futuras sem marca fixa.

### `flexagono_curvas_polares/` (pasta antiga, intocada)

As imagens de face nessa pasta estão contaminadas (na verdade são renders de coloração de domínio
de $f(z)=z^6+1$, sem relação com as curvas polares descritas no README interno). Decisão tomada
com o Gabe: **pular esta pasta** — o flexágono de curvas polares correto foi refeito do zero a
partir do notebook fonte e está em `sem_watermark/` e `com_watermark/` como
`flexagonos_curvas_polares_cores_solidas/`.

---

## 📐 Especificações Técnicas de Impressão
- **Formato das Pranchas:** Quadradas ($4840 \times 4840$ px, proporção 1:1).
- **Sangria (*Bleed*):** $58\text{ px} \times 2 = 116\text{ px}$ por segmento.
- **Margem de Segurança:** $56\text{ px}$ nas bordas externas.
- **Marcas de Registro:** Vetoriais com cruzes de corte nos 4 cantos e no centro óptico.
- **Numeração das faces:** convenção do artigo (Hall, Almeida & Teixeira, Bridges 2018, Fig. 33) e
  do `Manual_Flexas.pdf`, mesma do diagrama de dinâmica de flexão.
