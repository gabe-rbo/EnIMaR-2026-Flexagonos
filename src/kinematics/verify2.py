"""verify2.py -- verificacao numerica dos NOVOS resultados (mapas de retorno)."""
import numpy as np
from wpgen import WP
from quadflex import Flex, gamma_structure, label, latstr
from gerador import flexes_hexa, testa, grupo_de
import foldings as F

print("=" * 74)
print(" mapas de retorno do hexa-tetraflexagono (enumeracao exata)")
print("=" * 74)
fl = flexes_hexa()
st = grupo_de(fl)
print(f"  {len(fl)} mapas de retorno;  {label(st)}")
print(f"  Lambda = {latstr(st['lattice'])}   |P| = {st['P']}")

P = WP(2, 2j)                                  # Lambda = 2 Z[i]
sol = lambda z: P(np.asarray(z))               # J = P(z ; 2Z[i]), centro em 0
print("\n  f(z) = P(z ; 2Z[i]) contra TODOS os mapas de retorno:")
print(f"     residuo maximo = {testa(sol, fl):.3e}")
for g in [lambda z: P(np.asarray(z))**2,
          lambda z: 1/(P(np.asarray(z)) - 1),
          lambda z: (P(np.asarray(z)) + 2)/(P(np.asarray(z)) - 3)]:
    print(f"     R(P) generica          = {testa(g, fl):.3e}")

print("\n  controles negativos:")
for nm, g in [("exp(z)", lambda z: np.exp(np.asarray(z))),
              ("z^2", lambda z: np.asarray(z)**2),
              ("P(z;(1+i)Z[i])", lambda z: WP(1+1j, -1+1j)(np.asarray(z))),
              ("P'(z;2Z[i])", lambda z: P.deriv(np.asarray(z)))]:
    print(f"     {nm:<18s} = {testa(g, fl):.3e}   (deve falhar)")

print("\n" + "=" * 74)
print(" faces isoladas: as de posto 1 admitem solucoes INTEIRAS")
print("=" * 74)
est = F.estados_por_face(F.enumerar())
for k in sorted(est):
    arrs = est[k]
    maps = {F.mapa_retorno(arrs[i], arrs[j])
            for i in range(len(arrs)) for j in range(len(arrs)) if i != j}
    fk = [Flex(sg, ep) for sg, ep in maps]
    s = grupo_de(fk)
    print(f"  face {k}: {len(maps)} mapa(s);  posto={s['rank']} |P|={s['P']} "
          f"Lambda={latstr(s['lattice'])}")
    if s["rank"] == 1:
        w = complex(s["lattice"][0][0], s["lattice"][0][1])/2
        ent = lambda z, w=w: np.exp(2j*np.pi*np.asarray(z)/w)
        print(f"      solucao inteira exp(2*pi*i*z/{w:g}):  residuo = {testa(ent, fk):.2e}")
    if s["rank"] == 2:
        print(f"      P(z;2Z[i]):  residuo = {testa(sol, fk):.2e}")
        ent = lambda z: np.exp(np.asarray(z))
        print(f"      exp(z) (inteira):  residuo = {testa(ent, fk):.2e}  (falha)")
