#!/usr/bin/env python3
"""
catalogo.py -- constroi, para cada flexagono, o diretorio

    funcoes-flexionaveis-<nome_do_flexagono>/
        001/  face1.png ... faceN.png     (imagens para o gerador de planos)
              mecanica.png                (diagrama de flexao com as imagens)
              formula.txt / formula.tex
        002/  ...
        catalogo.pdf                      (duas colunas por pagina)
        indice.json

Cada item e uma funcao da familia completa de solucoes daquele flexagono,
verificada numericamente antes de ser desenhada.

Uso:  python3 catalogo.py --flexagono hexa --n 24 --tamanho 1240
      python3 catalogo.py --todos
"""
import argparse, json, os, subprocess, shutil
import numpy as np
from PIL import Image

from mecanica import SPECS, flexes, grupo
from fractions import Fraction as _Fr


def _bonito(a):
    """multiplica por i^k para deixar a forma mais simples (real positivo)."""
    cands = [a*(1j**k) for k in range(4)]
    def chave(x):
        return (0 if abs(x.imag) < 1e-9 and x.real > 0 else
                1 if abs(x.real) < 1e-9 and x.imag > 0 else
                2 if x.real > 0 else 3, abs(x.imag), abs(x.real))
    return sorted(cands, key=chave)[0]


def latex_lattice(B):
    """forma LaTeX bonita do reticulado (B em unidades de 1/2)."""
    if not B: return r"\{0\}"
    vs = [complex(_Fr(v[0], 2), _Fr(v[1], 2)) for v in B]
    def s(x):
        re, im = x.real, x.imag
        f = lambda t: (f"{t:.0f}" if abs(t - round(t)) < 1e-9 else f"{t:g}")
        if abs(im) < 1e-9: return f(re)
        if abs(re) < 1e-9: return (f(im) + "i") if abs(abs(im)-1) > 1e-9 else ("i" if im > 0 else "-i")
        return f"({f(re)}{'+' if im > 0 else '-'}{f(abs(im))}i)"
    if len(vs) == 2:
        a, b = vs
        for cand in (a, b, -a, -b):
            if abs(cand*1j - b) < 1e-9 or abs(cand*1j + b) < 1e-9 or \
               abs(cand*1j - a) < 1e-9 or abs(cand*1j + a) < 1e-9:
                pass
        # tenta alpha Z[i]
        for alpha in (a, b, -a, -b, a+b, a-b):
            if abs(alpha) < 1e-9: continue
            if all(abs((v/alpha).real - round((v/alpha).real)) < 1e-9 and
                   abs((v/alpha).imag - round((v/alpha).imag)) < 1e-9 for v in vs) \
               and abs(abs(a*b.conjugate()).imag if False else 1) > 0:
                # verifica que alpha Z[i] tem o mesmo covolume
                import numpy as _np
                cov = abs((a.conjugate()*b).imag)
                if abs(cov - abs(alpha)**2) < 1e-9:
                    alpha = _bonito(alpha)
                    return (s(alpha) if abs(alpha - 1) > 1e-9 else "") \
                        + r"\,\mathbb{Z}[i]"
        return s(vs[0]) + r"\mathbb{Z} + " + s(vs[1]) + r"\mathbb{Z}"
    return s(_bonito(vs[0])) + r"\,\mathbb{Z}"
from quadflex import label, latstr, covol
from gerador import Familia, retrato, malha, testa
from diagrama import desenha


# ------------------------------------------------------------------ formulas
def latex_rat(zer, pol, c):
    def num(x):
        re, im = x.real, x.imag
        if abs(im) < 5e-2: return f"{re:.1f}"
        if abs(re) < 5e-2: return f"{im:.1f}i"
        return f"({re:.1f}{'+' if im >= 0 else '-'}{abs(im):.1f}i)"
    N = "".join(f"(J{'-' if True else ''}{num(a)})".replace("--", "+")
                for a in zer) or "1"
    D = "".join(f"(J-{num(b)})".replace("--", "+") for b in pol)
    cc = num(c)
    return f"{cc}\\tfrac{{{N}}}{{{D}}}" if D else f"{cc}\\,{N}"


class FamiliaTeX(Familia):
    """acrescenta a forma LaTeX da funcao sorteada."""

    def sortear_tex(self, rng, grau=1):
        am = self.amostra_J()

        def pick(k):
            idx = rng.integers(0, len(am), k)
            jit = 1 + 0.15*(rng.normal(0, 1, k) + 1j*rng.normal(0, 1, k))
            return am[idx]*jit

        def rat():
            dz = int(rng.integers(0, grau+1)); dp = int(rng.integers(0, grau+1))
            if dz == 0 and dp == 0: dz = 1
            zer = pick(dz); pol = pick(dp)
            c = complex(rng.normal(0, 1), rng.normal(0, 1))

            def R(X):
                out = np.full_like(np.asarray(X, dtype=complex), c)
                for a in zer: out = out*(X-a)
                for b in pol:
                    with np.errstate(divide='ignore', invalid='ignore'):
                        out = out/(X-b)
                return out
            return R, latex_rat(zer, pol, c)

        fase = complex(np.exp(2j*np.pi*rng.random()))
        pf = "" if abs(fase-1) < 1e-9 else \
             f"({fase.real:.2f}{'+' if fase.imag >= 0 else '-'}{abs(fase.imag):.2f}i)\\,"
        # devolve (f de z, f dos valores ja calculados de J, texto LaTeX)
        if self.ngen == 1:
            R, t = rat()
            return ((lambda z: fase*R(self.J(z))),
                    (lambda Jv, Jl: fase*R(Jv)), pf + t)
        R1, t1 = rat(); R2, t2 = rat()
        return ((lambda z: fase*(R1(self.J(z)) + R2(self.J(z))*self.Jlinha(z))),
                (lambda Jv, Jl: fase*(R1(Jv) + R2(Jv)*Jl)),
                pf + f"\\left[{t1} + \\left({t2}\\right)\\wp'\\right]")

    def tex_J(self):
        r, n = self.rank, self.n
        p = self.p
        ps = "" if abs(p) < 1e-9 else \
            (f" - ({p.real:.1f}{'+' if p.imag >= 0 else '-'}{abs(p.imag):.1f}i)")
        if r == 0 and n == 1: return "J = z"
        if r == 0: return f"J = (z{ps})^{{{n}}}"
        if r == 1 and n == 1:
            w = self.omega
            return (f"J = \\exp\\!\\left(\\frac{{2\\pi i\\,(z{ps})}}"
                    f"{{{w.real:.0f}{'' if abs(w.imag)<1e-9 else f'{w.imag:+.0f}i'}}}\\right)")
        if r == 1:
            w = self.omega
            return (f"J = \\cos\\!\\left(\\frac{{2\\pi (z{ps})}}"
                    f"{{{w.real:.0f}{'' if abs(w.imag)<1e-9 else f'{w.imag:+.0f}i'}}}\\right)")
        if r == 2 and n == 1: return "J = \\wp(z;\\Lambda),\\ \\wp'=\\wp'(z;\\Lambda)"
        if r == 2 and n == 2: return f"J = \\wp(z{ps};\\Lambda)"
        return f"J = \\wp(z{ps};\\Lambda)^2"


# ------------------------------------------------------------------ catalogo
def constroi(chave, n_itens, tamanho, semente, grau, raiz, dpi=105):
    spec = SPECS[chave]
    fl = flexes(spec)
    st = grupo(spec)
    fam = FamiliaTeX(st)
    pasta = os.path.join(raiz, f"funcoes-flexionaveis-{spec['nome']}")
    os.makedirs(pasta, exist_ok=True)

    print(f"=== {spec['nome']} ===")
    print(f"  {len(fl)} mapas de retorno;  {label(st)}")
    print(f"  Lambda = {latstr(st['lattice'])};  familia: {fam.desc}")

    faces = spec["faces"]
    Z = malha(tamanho)
    # J e J' no grid, calculados UMA vez (nao dependem do item sorteado)
    Jg = np.asarray(fam.J(Z))
    Jl = np.asarray(fam.Jlinha(Z)) if fam.ngen == 2 else None
    rng = np.random.default_rng(semente)
    indice = {"flexagono": spec["nome"], "classe": label(st),
              "reticulado": latstr(st["lattice"]),
              "familia_tex": fam.tex_J(), "itens": []}

    feitos = 0; tent = 0
    while feitos < n_itens and tent < 80*n_itens:
        tent += 1
        # uma funcao por FACE (todas da mesma familia -> todas flexionaveis)
        fs, texs, gfs = [], [], []
        ok = True
        for _ in faces:
            f, gf, t = fam.sortear_tex(rng, grau=grau)
            try:
                err = testa(f, fl, npts=600)
            except Exception:
                ok = False; break
            if not np.isfinite(err) or err > 1e-7: ok = False; break
            fs.append((f, err)); gfs.append(gf); texs.append(t)
        if not ok: continue
        # desenha e filtra por riqueza cromatica
        imgs = {}
        bom = True
        for k, gf in zip(faces, gfs):
            vals = gf(Jg, Jl)
            img = retrato(vals)
            v = vals[::9, ::9].ravel(); v = v[np.isfinite(v)]
            if v.size < 80: bom = False; break
            h = (np.angle(v)/(2*np.pi)) % 1.0
            if (np.histogram(h, bins=24, range=(0, 1))[0] > 0).mean() < 0.8 \
               or img.reshape(-1, 3).std(0).mean() < 25:
                bom = False; break
            imgs[k] = img
        if not bom: continue

        feitos += 1
        sub = os.path.join(pasta, f"{feitos:03d}")
        os.makedirs(sub, exist_ok=True)
        for k in faces:
            Image.fromarray(imgs[k]).save(os.path.join(sub, f"face{k}.png"))
        pequenas = {k: np.array(Image.fromarray(v).resize((420, 420),
                    Image.LANCZOS)) for k, v in imgs.items()}
        desenha(spec, pequenas, os.path.join(sub, "mecanica.png"), dpi=dpi)
        with open(os.path.join(sub, "formula.tex"), "w") as fh:
            for k, t in zip(faces, texs):
                fh.write(f"face {k}: $f_{{{k}}} = {t}$\n")
        with open(os.path.join(sub, "formula.txt"), "w") as fh:
            fh.write(f"{spec['nome']} -- item {feitos:03d}\n")
            fh.write(f"familia: {fam.desc}\n")
            for k, t, (f, e) in zip(faces, texs, fs):
                fh.write(f"face {k}: f = {t}   (residuo {e:.2e})\n")
        indice["itens"].append(
            {"id": f"{feitos:03d}",
             "faces": {str(k): t for k, t in zip(faces, texs)},
             "residuo_max": max(e for _, e in fs)})
        print(f"  [{feitos:03d}] residuo max = {max(e for _,e in fs):.2e}")

    with open(os.path.join(pasta, "indice.json"), "w") as fh:
        json.dump(indice, fh, indent=1, ensure_ascii=False)
    return pasta, spec, fam, st, indice


# ------------------------------------------------------------------ PDF
CABECA = r"""\documentclass[10pt,a4paper]{article}
\usepackage[T1]{fontenc}\usepackage[utf8]{inputenc}
\usepackage{amsmath,amssymb}\usepackage{graphicx}
\usepackage[margin=1.5cm]{geometry}
\usepackage{multicol}\usepackage[dvipsnames]{xcolor}
\setlength{\columnsep}{14pt}
\pagestyle{empty}
\begin{document}
\begin{center}
{\Large\bfseries Fun\c{c}\~oes complexas flexion\'aveis}\\[2pt]
{\large TITULO}\\[6pt]
\parbox{0.86\textwidth}{\small\centering
Cada item mostra o \emph{diagrama de flex\~ao} do flex\'agono com os retratos de
fase encaixados: cada caixa \'e a face indicada, no arranjo em que ela aparece
naquele estado. Todas as fun\c{c}\~oes pertencem \`a fam\'ilia completa de
solu\c{c}\~oes deste flex\'agono --- CLASSE ---, com RETIC\ e FAMJ.
Cada imagem foi verificada
numericamente antes de ser desenhada.}
\end{center}
\vspace{4pt}
\begin{multicols}{2}
"""

RODAPE = r"""\end{multicols}
\end{document}
"""


def gera_pdf(pasta, spec, fam, st, indice, saida_nome="catalogo.pdf"):
    corpo = []
    for it in indice["itens"]:
        linhas = [r"{\bfseries %s}\par\vspace{1pt}" % it["id"]]
        for k, t in it["faces"].items():
            linhas.append(r"\resizebox{\linewidth}{!}{$f_{%s}=%s$}\par" % (k, t))
        linhas.append(r"\vspace{3pt}\includegraphics[width=\linewidth]"
                      r"{%s/mecanica.png}\par\vspace{11pt}" % it["id"])
        corpo.append("\n".join(linhas))
    CLASSES = {(0, 1): "todas as fun\\c{c}\\~oes meromorfas",
               (1, 1): "as fun\\c{c}\\~oes peri\\'odicas",
               (1, 2): "as fun\\c{c}\\~oes de um cosseno",
               (2, 1): "as fun\\c{c}\\~oes el\\'ipticas do reticulado",
               (2, 2): "as fun\\c{c}\\~oes el\\'ipticas pares",
               (2, 4): "as fun\\c{c}\\~oes el\\'ipticas $C_4$-invariantes"}
    ret = latex_lattice(st["lattice"])
    tex = (CABECA.replace("TITULO", spec["titulo"])
                 .replace("CLASSE", CLASSES.get((st["rank"], st["P"]), "?"))
                 .replace("RETIC", ("$\\Lambda = " + ret + "$")
                          if st["rank"] else "$\\Gamma$ trivial")
                 .replace("FAMJ", "$" + fam.tex_J() + "$")
           + "\n\n".join(corpo) + RODAPE)
    caminho = os.path.join(pasta, "catalogo.tex")
    open(caminho, "w").write(tex)
    for _ in range(2):
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "catalogo.tex"],
                       cwd=pasta, stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    pdf = os.path.join(pasta, "catalogo.pdf")
    for ext in (".aux", ".log", ".out"):
        p = os.path.join(pasta, "catalogo" + ext)
        try:
            if os.path.exists(p): os.remove(p)
        except OSError:
            pass          # o volume montado pode nao permitir remocao
    return pdf if os.path.exists(pdf) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--flexagono", choices=list(SPECS), default="hexa")
    ap.add_argument("--todos", action="store_true")
    ap.add_argument("-n", type=int, default=16)
    ap.add_argument("--tamanho", type=int, default=1240)
    ap.add_argument("--semente", type=int, default=2026)
    ap.add_argument("--grau", type=int, default=1)
    ap.add_argument("--raiz", default="../out")
    a = ap.parse_args()
    alvos = list(SPECS) if a.todos else [a.flexagono]
    for chave in alvos:
        pasta, spec, fam, st, ind = constroi(
            chave, a.n, a.tamanho, a.semente, a.grau, a.raiz)
        pdf = gera_pdf(pasta, spec, fam, st, ind)
        print(f"  -> {pasta}")
        print(f"  -> {pdf}")


if __name__ == "__main__":
    main()
