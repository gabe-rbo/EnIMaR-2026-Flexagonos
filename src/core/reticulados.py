"""
reticulados.py -- resposta a pergunta em aberto (c): quais reticulados
Lambda subset (1/2)Z[i] ocorrem como reticulado de translacoes de Gamma_Phi?
"""
from collections import Counter, defaultdict
from fractions import Fraction as Fr
from quadflex import all_flexes, gamma_structure, hnf


def como_alpha_Zi(B):
    """se Lambda = alpha Z[i], devolve alpha (em unidades de 1/2); senao None."""
    if len(B) != 2: return None
    a = complex(B[0][0], B[0][1]); b = complex(B[1][0], B[1][1])
    cov = abs((a.conjugate()*b).imag)
    for alpha in (a, b, a+b, a-b, -a, -b):
        if abs(alpha) < 1e-9: continue
        if abs(cov - abs(alpha)**2) > 1e-9: continue
        ok = True
        for v in (a, b):
            q = v/alpha
            if abs(q.real-round(q.real)) > 1e-9 or abs(q.imag-round(q.imag)) > 1e-9:
                ok = False; break
        if ok: return alpha
    return None


def canon(alpha):
    """alpha a menos de multiplicacao por i^k, com Re>0 e Im>=0."""
    c = [alpha*(1j**k) for k in range(4)]
    c = [x for x in c if x.real > 1e-9 or (abs(x.real) < 1e-9 and x.imag > 0)]
    c = [x for x in c if x.imag >= -1e-9]
    x = sorted(c, key=lambda t: (abs(t.imag), -t.real))[0]
    return (round(x.real, 6), round(x.imag, 6))


if __name__ == "__main__":
    lat = Counter(); porP = defaultdict(Counter); naoZi = Counter()
    total2 = 0
    for Phi in all_flexes():
        st = gamma_structure(Phi)
        if st["rank"] != 2: continue
        total2 += 1
        B = tuple(st["lattice"])
        lat[B] += 1
        al = como_alpha_Zi(st["lattice"])
        if al is None:
            naoZi[(B, st["P"])] += 1
        porP[st["P"]][canon(al) if al is not None else None] += 1

    print(f"flexes com Gamma de posto 2: {total2}")
    print(f"reticulados distintos que ocorrem: {len(lat)}")
    print(f"quantos NAO sao da forma alpha.Z[i]: {sum(naoZi.values())}"
          f"  ({len(naoZi)} reticulados distintos)\n")

    print("por ordem do grupo de pontos |P|, os alpha (em unidades de 1/2) tais")
    print("que Lambda = alpha.Z[i]   (alpha a menos de multiplicacao por i):")
    for P in sorted(porP):
        chaves = [k for k in porP[P] if k is not None]
        print(f"\n  |P| = {P}:  {sum(porP[P][k] for k in chaves)} flexes, "
              f"{len(chaves)} valores de alpha")
        for k in sorted(chaves, key=lambda t: (t[0]**2+t[1]**2, t[0])):
            a = complex(k[0], k[1])/2
            n = (a*a.conjugate()).real
            texto = f"{a.real:g}" if abs(a.imag) < 1e-9 else \
                    (f"{a.imag:g}i" if abs(a.real) < 1e-9 else
                     f"{a.real:g}{'+' if a.imag>0 else '-'}{abs(a.imag):g}i")
            print(f"      alpha = {texto:<10s}  N(alpha) = {n:g}"
                  f"   -> {porP[P][k]} flexes")
        if None in porP[P]:
            print(f"      (nao-alpha.Z[i]): {porP[P][None]} flexes")

    print("\nreticulados que NAO sao da forma alpha.Z[i] (base de Hermite, "
          "em unidades de 1/2):")
    for (B, P), n in sorted(naoZi.items(), key=lambda kv: -kv[1]):
        vs = [f"({v[0]}{'+' if v[1] >= 0 else '-'}{abs(v[1])}i)/2" for v in B]
        cov = abs(Fr(B[0][0]*B[1][1] - B[0][1]*B[1][0], 4))
        print(f"   |P|={P}  {vs}  covol={cov}   -> {n} flexes")
