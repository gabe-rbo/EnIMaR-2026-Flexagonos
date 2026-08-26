#!/usr/bin/env python3
"""
gerador.py -- gera TODAS as imagens flexionaveis possiveis para um flexagono
              (ou para um flex de quadrantes arbitrario).

Dado um conjunto de flexes  Phi_1,...,Phi_m  (as faces de um flexagono, ou um
unico flex), o programa
  1. calcula exatamente  Gamma = < Gamma_{Phi_1}, ..., Gamma_{Phi_m} >;
  2. classifica  Gamma  (posto do reticulado x ordem do grupo de pontos);
  3. constroi o GERADOR do corpo das solucoes -- o "Hauptmodul" J da orbifold
     C/Gamma -- de modo que TODA solucao meromorfa e  f = R(J)  com R racional
     (no caso posto 2 / |P|=1 sao duas:  f = R1(P) + R2(P) P');
  4. sorteia funcoes racionais R, VERIFICA numericamente que a f resultante e
     mesmo flexionavel, e salva o retrato de fase.

O passo 3 e o ponto: a familia gerada nao e uma colecao de exemplos, e uma
parametrizacao completa do conjunto das solucoes.

Uso:
    python3 gerador.py --flexagono hexa --n 6 --tamanho 1600 --saida ../out/faces
    python3 gerador.py --flexagono tri  --n 3
    python3 gerador.py --flex "3,4,1,2;1,1,1,1"        # sigma ; eps (potencias de i)
    python3 gerador.py --classes                        # um exemplar de cada classe
"""
import argparse, json, os, sys
import numpy as np
from PIL import Image

from quadflex import (Flex, gamma_structure, label, latstr, covol, all_flexes)
from wpgen import WP

IPOWc = [1, 1j, -1, -1j]
C = {1: 0.5+0.5j, 2: -0.5+0.5j, 3: -0.5-0.5j, 4: 0.5-0.5j}


# ====================================================================== flexes
class _Gens:
    def __init__(self, gens): self._g = sorted(set(gens))
    def gamma_gens(self): return self._g


def grupo_de(flexes):
    gens = []
    for Phi in flexes: gens += Phi.gamma_gens()
    return gamma_structure(_Gens(gens))


def flexes_hexa():
    """mapas de retorno do hexa-tetraflexagono (foldings.py, enumeracao exata)."""
    import foldings as F
    est = F.estados_por_face(F.enumerar())
    out = []
    for k in sorted(est):
        arrs = est[k]
        for i in range(len(arrs)):
            for j in range(len(arrs)):
                if i != j:
                    sg, ep = F.mapa_retorno(arrs[i], arrs[j])
                    out.append(Flex(sg, ep))
    return out


def flexes_tri():
    """tri-tetraflexagono: as 3 faces, com o flex lido das pre-rotacoes do
       gerador de planos do Projeto Visitas (hipotese explicita, ver artigo)."""
    E1, EM1 = 0, 2
    return [Flex((1, 2, 3, 4), (EM1, E1, E1, EM1)),
            Flex((1, 2, 3, 4), (EM1, EM1, E1, E1)),
            Flex((1, 2, 3, 4), (E1, E1, EM1, EM1))]


# ============================================================ solucao generica
class Familia:
    """parametrizacao completa das solucoes de um Gamma dado."""

    def __init__(self, st):
        self.st = st
        self.rank = st["rank"]; self.n = st["P"]
        self.p = 0.0+0j
        if st.get("centers"):
            cx, cy = st["centers"][0]
            self.p = complex(float(cx), float(cy))
        if self.rank == 2:
            b = st["lattice"]
            self.w1 = complex(b[0][0], b[0][1])/2
            self.w2 = complex(b[1][0], b[1][1])/2
            self.wp = WP(self.w1, self.w2)
        elif self.rank == 1:
            v = st["lattice"][0]
            self.omega = complex(v[0], v[1])/2
        self._am = None
        self.desc, self.ngen = self._descricao()

    def _descricao(self):
        r, n = self.rank, self.n
        if r == 0 and n == 1: return "toda funcao meromorfa (Gamma trivial)", 1
        if r == 0: return f"f = R(J),  J = (z-p)^{n},  p={self.p:g}", 1
        if r == 1 and n == 1:
            return f"f = R(J),  J = exp(2*pi*i*(z-p)/w),  w={self.omega:g}", 1
        if r == 1:
            return f"f = R(J),  J = cos(2*pi*(z-p)/w),  w={self.omega:g}, p={self.p:g}", 1
        if r == 2 and n == 1:
            return "f = R1(P) + R2(P)*P'  (P de Weierstrass do reticulado)", 2
        if r == 2 and n == 2:
            return f"f = R(J),  J = P(z-p),  p={self.p:g}", 1
        return f"f = R(J),  J = P(z-p)^2,  p={self.p:g}  (reticulado quadrado)", 1

    # ---- geradores da orbifold
    def J(self, z):
        z = np.asarray(z, dtype=complex)
        r, n = self.rank, self.n
        if r == 0 and n == 1: return z
        if r == 0: return (z - self.p)**n
        if r == 1 and n == 1: return np.exp(2j*np.pi*(z - self.p)/self.omega)
        if r == 1: return np.cos(2*np.pi*(z - self.p)/self.omega)
        if r == 2 and n == 1: return self.wp(z - self.p)
        if r == 2 and n == 2: return self.wp(z - self.p)
        return self.wp(z - self.p)**2

    def Jlinha(self, z):
        return self.wp.deriv(np.asarray(z, dtype=complex) - self.p)

    # ---- amostragem de R
    def amostra_J(self, N=140):
        """valores tipicos de J no quadrado -- usados para ancorar os zeros e
        polos de R DENTRO da imagem (senao o retrato fica quase constante)."""
        if getattr(self, "_am", None) is not None: return self._am
        x = np.linspace(-1, 1, N, endpoint=False) + 1.0/N
        X, Y = np.meshgrid(x, -x)
        v = np.asarray(self.J(X + 1j*Y)).ravel()
        v = v[np.isfinite(v)]
        r = np.abs(v)
        v = v[(r > np.quantile(r, 0.02)) & (r < np.quantile(r, 0.98))]
        self._am = v
        return v

    def sortear(self, rng, grau=2, escala=3.0):
        am = self.amostra_J()
        def pick(k):
            if len(am) == 0:
                return rng.normal(0, escala, k) + 1j*rng.normal(0, escala, k)
            idx = rng.integers(0, len(am), k)
            jit = 1 + 0.15*(rng.normal(0, 1, k) + 1j*rng.normal(0, 1, k))
            return am[idx]*jit
        def rat(rng):
            dz = rng.integers(0, grau+1); dp = rng.integers(0, grau+1)
            if dz == 0 and dp == 0: dz = 1
            zer = pick(dz); pol = pick(dp)
            c = complex(rng.normal(0, 1), rng.normal(0, 1))
            txt = (f"{c:.3g}"
                   + "".join(f"*(X-{a:.3g})" for a in zer)
                   + ("/" + "".join(f"(X-{b:.3g})" for b in pol) if dp else ""))
            def R(X):
                out = np.full_like(np.asarray(X, dtype=complex), c)
                for a in zer: out = out*(X-a)
                for b in pol:
                    with np.errstate(divide='ignore', invalid='ignore'):
                        out = out/(X-b)
                return out
            return R, txt
        fase = np.exp(2j*np.pi*rng.random())
        if self.ngen == 1:
            R, txt = rat(rng)
            return (lambda z: fase*R(self.J(z))), f"R(J) com R(X)={txt}"
        R1, t1 = rat(rng); R2, t2 = rat(rng)
        return ((lambda z: fase*(R1(self.J(z)) + R2(self.J(z))*self.Jlinha(z))),
                f"R1(P)+R2(P)P' com R1={t1} , R2={t2}")


# ================================================================= verificacao
def quadrante_np(z):
    return np.where(z.real >= 0, np.where(z.imag >= 0, 1, 4),
                    np.where(z.imag >= 0, 2, 3))


def testa(f, flexes, npts=1500, tol=1e-7, seed=0):
    """max_j |f o A_1^-1 - f o A_j^-1| sobre todos os flexes."""
    rng = np.random.default_rng(seed)
    w = rng.uniform(-.95, .95, npts) + 1j*rng.uniform(-.95, .95, npts)
    pior = 0.0
    for Phi in flexes:
        a = {j: IPOWc[Phi.eps[j-1]] for j in (1, 2, 3, 4)}
        b = {j: C[Phi.sigma[j-1]] - a[j]*C[j] for j in (1, 2, 3, 4)}
        br = [f((w - b[j])/a[j]) for j in (1, 2, 3, 4)]
        for k in (1, 2, 3):
            d = np.abs(br[0]-br[k])/(1+np.abs(br[0]))
            d = d[np.isfinite(d)]
            if d.size: pior = max(pior, float(d.max()))
    return pior


# =================================================================== desenho
def hsv2rgb(h, s, v):
    h = (h % 1.0)*6.0; i = np.floor(h).astype(int); fr = h - i
    p = v*(1-s); q = v*(1-s*fr); t = v*(1-s*(1-fr)); i = i % 6
    sel = lambda *a: np.select([i == k for k in range(6)], a)
    return sel(v, q, p, p, t, v), sel(t, v, v, q, p, p), sel(p, p, t, v, v, q)


def retrato(w):
    w = np.asarray(w, dtype=complex)
    bad = ~np.isfinite(w); w = np.where(bad, 0, w)
    arg = np.angle(w); mod = np.abs(w)
    H = (arg/(2*np.pi)) % 1.0
    lm = np.log2(mod + 1e-300); sm = lm - np.floor(lm)
    sp = (arg*6/(2*np.pi)) % 1.0
    V = np.clip(0.55 + 0.32*sm**0.6, 0, 1)
    S = np.clip(1.0 - 0.28*(1-(1-np.abs(2*sp-1))**8), 0, 1)
    r, g, b = hsv2rgb(H, S, V)
    rgb = np.stack([r, g, b], -1)
    rgb[bad] = 1.0; rgb[mod > 1e12] = 1.0; rgb[mod < 1e-12] = 0.0
    return (np.clip(rgb, 0, 1)*255).astype(np.uint8)


def malha(N):
    x = np.linspace(-1, 1, N, endpoint=False) + 1.0/N
    X, Y = np.meshgrid(x, -x)
    return X + 1j*Y


# ====================================================================== main
def gerar(flexes, nome, n, tamanho, saida, semente, grau, tol=1e-7, maxtent=60):
    st = grupo_de(flexes)
    fam = Familia(st)
    print(f"=== {nome} ===")
    print(f"  {len(flexes)} flex(es);  {label(st)}")
    if st["rank"]:
        print(f"  Lambda = {latstr(st['lattice'])}"
              + (f"  covol={covol(st['lattice'])}" if st["rank"] == 2 else ""))
    print(f"  familia completa de solucoes:  {fam.desc}")
    os.makedirs(saida, exist_ok=True)
    Z = malha(tamanho)
    rng = np.random.default_rng(semente)
    manifesto = {"flexagono": nome, "classe": label(st),
                 "reticulado": latstr(st["lattice"]), "familia": fam.desc,
                 "imagens": []}
    feitas = 0; tent = 0
    while feitas < n and tent < maxtent*n:
        tent += 1
        f, txt = fam.sortear(rng, grau=grau)
        try:
            err = testa(f, flexes)
        except Exception:
            continue
        if not np.isfinite(err) or err > tol:
            continue
        img = retrato(f(Z))
        # descarta imagens quase constantes
        vals = f(Z[::7, ::7]).ravel()
        vals = vals[np.isfinite(vals)]
        if vals.size < 100: continue
        hues = (np.angle(vals)/(2*np.pi)) % 1.0
        cob = (np.histogram(hues, bins=24, range=(0, 1))[0] > 0).mean()
        if cob < 0.85 or img.reshape(-1, 3).std(0).mean() < 25:
            continue
        feitas += 1
        cam = os.path.join(saida, f"{nome}_face{feitas}.png")
        Image.fromarray(img).save(cam)
        print(f"  [{feitas}/{n}] residuo={err:.2e}  {txt[:78]}")
        manifesto["imagens"].append({"arquivo": os.path.basename(cam),
                                     "formula": txt, "residuo": err})
    with open(os.path.join(saida, f"{nome}_manifesto.json"), "w") as fh:
        json.dump(manifesto, fh, indent=1, ensure_ascii=False)
    print(f"  -> {feitas} imagens em {saida} ({tent} tentativas)")
    return st


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--flexagono", choices=["hexa", "tri"], default=None)
    ap.add_argument("--flex", default=None, help='"s1,s2,s3,s4;e1,e2,e3,e4" '
                    "(eps em potencias de i: 0=1, 1=i, 2=-1, 3=-i)")
    ap.add_argument("--classes", action="store_true",
                    help="gera um exemplar de cada uma das 8 classes de flex")
    ap.add_argument("-n", type=int, default=6)
    ap.add_argument("--tamanho", type=int, default=1400)
    ap.add_argument("--saida", default="../out/gerador")
    ap.add_argument("--semente", type=int, default=20260814)
    ap.add_argument("--grau", type=int, default=2)
    a = ap.parse_args()

    if a.classes:
        vistos = {}
        for Phi in all_flexes():
            st = gamma_structure(Phi)
            vistos.setdefault((st["rank"], st["P"]), Phi)
        for key in sorted(vistos):
            gerar([vistos[key]], f"classe_posto{key[0]}_P{key[1]}",
                  min(a.n, 3), a.tamanho, a.saida, a.semente, a.grau)
        return
    if a.flex:
        sg, ep = a.flex.split(";")
        Phi = Flex(tuple(int(x) for x in sg.split(",")),
                   tuple(int(x) for x in ep.split(",")))
        gerar([Phi], "flex", a.n, a.tamanho, a.saida, a.semente, a.grau)
        return
    if a.flexagono == "tri":
        gerar(flexes_tri(), "tri", a.n, a.tamanho, a.saida, a.semente, a.grau)
    else:
        gerar(flexes_hexa(), "hexa", a.n, a.tamanho, a.saida, a.semente, a.grau)


if __name__ == "__main__":
    main()
