"""
multiproto.py
=============
FACES COM MAIS DE UM PROTOTIPO.

Se a face e ladrilhada por varias formas, um flex tem de respeitar as classes
de congruencia: sigma permuta ladrilhos dentro de cada classe e eps_j percorre
a co-classe das rotacoes que levam T_j em T_{sigma(j)}.  O grupo dos flexes
deixa de ser um produto entrelacado, mas o teorema de caracterizacao nao muda
(a sua prova so usa o principio da identidade).  O que muda e a aritmetica:
misturando um quadrado (C_4) com um triangulo equilatero (C_3) aparecem
rotacoes de ordem 12, e a restricao cristalografica passa a ter dentes:

  * se todos os A_j tem um ponto fixo comum p, entao Gamma = C_N (N qualquer!)
    e as solucoes sao f(z) = h((z-p)^N);
  * caso contrario Gamma contem uma translacao nao nula; se |P| em {1,2,3,4,6}
    e um dos nove casos cristalograficos; se |P| nao esta nessa lista, Gamma
    e DENSO e so as constantes sobrevivem.

Num flexagono de verdade o Teorema das retas de dobra da Gamma <= W^+(D) <=
Sym^+(T), que e cristalografico: o caso denso nunca acontece.  Ele e um
fenomeno dos flexes ABSTRATOS.

Aritmetica exata em Z[zeta_12], base {1, z, z^2, z^3}, z^4 = z^2 - 1.
"""
from fractions import Fraction
from itertools import product
from collections import Counter

N12 = 12
def zmulz(v):                      # multiplicacao por zeta
    a, b, c, d = v
    return (-d, a, b + d, c)
ZP = [(1, 0, 0, 0)]
for _ in range(11): ZP.append(zmulz(ZP[-1]))


def mul(u, v):
    """produto em Z[zeta_12] (u escrito na base, v idem)."""
    r = (0, 0, 0, 0)
    for k in range(4):
        if v[k] == 0: continue
        w = u
        for _ in range(k): w = zmulz(w)
        r = tuple(x + v[k]*y for x, y in zip(r, w))
    return r


def add(u, v): return tuple(x + y for x, y in zip(u, v))
def sub(u, v): return tuple(x - y for x, y in zip(u, v))
def neg(u): return tuple(-x for x in u)
def zpow(a, v): return mul(ZP[a % 12], v)
ZERO = (0, 0, 0, 0)


def resolve(m, t):
    """resolve (multiplicacao por m) * p = t em Q(zeta_12); None se singular."""
    M = [[Fraction(0)]*4 for _ in range(4)]
    for k in range(4):
        e = [0]*4; e[k] = 1
        col = mul(m, tuple(e))
        for i in range(4): M[i][k] = Fraction(col[i])
    b = [Fraction(x) for x in t]
    for col in range(4):
        piv = next((r for r in range(col, 4) if M[r][col] != 0), None)
        if piv is None: return None
        M[col], M[piv] = M[piv], M[col]; b[col], b[piv] = b[piv], b[col]
        pv = M[col][col]
        M[col] = [x/pv for x in M[col]]; b[col] /= pv
        for r in range(4):
            if r != col and M[r][col] != 0:
                f = M[r][col]
                M[r] = [x - f*y for x, y in zip(M[r], M[col])]
                b[r] -= f*b[col]
    return tuple(b)


# --------------------------------------------------- a face: 1 quadrado + 2 triangulos
i_ = ZP[3]
c_S = add((3, 0, 0, 0), (0, 0, 0, 3))                     # 6*(1+i)/2
c_T1 = tuple(2*x for x in add(add((1, 0, 0, 0), (0, 0, 0, 3)),
                              add((0, 0, 0, 3), ZP[2])))  # 2*(i + (1+i) + (i+z^2))/... 
c_T1 = tuple(2*x for x in add(add((1, 0, 0, 0), ZP[2]), (0, 0, 0, 6)))
c_T2 = tuple(2*x for x in add((1, 0, 0, 0), ZP[10]))
CENT = [c_S, c_T1, c_T2]
STAB = [[0, 3, 6, 9], [0, 4, 8], [0, 4, 8]]     # rotacoes proprias de cada ladrilho
TROCA = [2, 6, 10]                              # rotacoes que levam T1 em T2


def flexes():
    for sw in (False, True):
        sig = [0, 1, 2] if not sw else [0, 2, 1]
        opc = [STAB[0], STAB[1] if not sw else TROCA, STAB[2] if not sw else TROCA]
        for eps in product(*opc): yield tuple(sig), eps


def gamma(sig, eps):
    A = [(eps[j], sub(CENT[sig[j]], zpow(eps[j], CENT[j]))) for j in range(3)]
    def inv(g):
        a, t = g; return ((-a) % 12, neg(zpow(-a, t)))
    def comp(g, h):
        a, t = g; b, u = h; return ((a + b) % 12, add(zpow(a, u), t))
    gens = []
    for j in range(3):
        for k in range(3):
            g = comp(inv(A[k]), A[j])
            if g != (0, ZERO): gens.append(g)
    return A, gens


def classifica(sig, eps):
    A, gens = gamma(sig, eps)
    if not gens: return ("trivial", 1, None)
    P = 0
    for a, _ in gens: P = a if P == 0 else __import__("math").gcd(P, a)
    P = __import__("math").gcd(P, 12)
    Nord = 12 // P if P else 1
    # ponto fixo comum dos A_j ?
    pf = set(); bom = True
    for a, t in A:
        if a % 12 == 0:
            if t != ZERO: bom = False; break
        else:
            p = resolve(sub((1, 0, 0, 0), ZP[a % 12]), t)
            if p is None: bom = False; break
            pf.add(p)
    finito = bom and len(pf) <= 1
    if finito: return ("C_%d" % Nord, Nord, "h((z-p)^%d)" % Nord)
    if Nord in (1, 2, 3, 4, 6): return ("cristalografico |P|=%d" % Nord, Nord, "uma das 9 classes")
    return ("DENSO (|P|=%d)" % Nord, Nord, "so as constantes")


if __name__ == "__main__":
    print("=" * 74)
    print(" FACE COM DOIS PROTOTIPOS: 1 quadrado (C_4) + 2 triangulos (C_3)")
    print("=" * 74)
    cnt = Counter(); ex = {}
    tot = 0
    for sig, eps in flexes():
        tot += 1
        nome, N, sol = classifica(sig, eps)
        chave = nome.split(" ")[0] if "DENSO" not in nome else "DENSO"
        cnt[(chave, N, sol)] += 1
        ex.setdefault((chave, N, sol), (sig, eps))
    print(f"  flexes possiveis: {tot}   (sigma respeita as classes de congruencia)")
    print(f"  {'tipo de Gamma':<24}{'|P|':>5}{'quantos':>9}   solucoes")
    for (nome, N, sol), q in sorted(cnt.items(), key=lambda z: (-z[1], str(z[0]))):
        print(f"  {nome:<24}{N:>5}{q:>9}   {sol}")
    print()
    print("  exemplos:")
    for k, v in sorted(ex.items(), key=lambda z: str(z[0])):
        print(f"     {str(k[0]):<24} sigma={v[0]} eps={v[1]}")
    print("""
  Conclusao.  Com dois prototipos a restricao cristalografica deixa de ser
  automatica: ela so vale quando Gamma tem translacoes.  Ficam entao possiveis
   (i) grupos ciclicos finitos C_N com N arbitrario (aqui realizam-se
       N = 1,2,3,4,6), cujas solucoes h((z-p)^N) incluem inteiras; e
   (ii) grupos DENSOS --- 32 dos 72 flexes ---, em que so as constantes
       sobrevivem: a face fica RIGIDA DEMAIS.  Mais prototipos = mais rigidez.
  Nenhum dos dois ocorre num flexagono de verdade: pelo Teorema das retas de
  dobra, Gamma <= W^+(D) <= Sym^+(T), que e um grupo cristalografico.""")


# =============================================== a RODA: 2 quadrados + 3 triangulos
# Em torno de um vertice p cabem 90+60+90+60+60 = 360 graus.  Numeramos os
# inicios angulares em unidades de 30 graus: quadrados em s=0 e s=5,
# triangulos em s=3, s=8, s=10.  Centroide (sobre d=6):
#    quadrado(s) = zeta^s * 3(1+zeta^3)      triangulo(s) = zeta^s * 2(1+zeta^2)
RODA_S = [0, 5, 3, 8, 10]                 # dois quadrados, depois tres triangulos
RODA_TIPO = ['Q', 'Q', 'T', 'T', 'T']
RODA_C = [zpow(s, (3, 0, 0, 3) if t == 'Q' else tuple(2*x for x in add((1, 0, 0, 0), ZP[2])))
          for s, t in zip(RODA_S, RODA_TIPO)]
RODA_SIM = {'Q': [0, 3, 6, 9], 'T': [0, 4, 8]}


def roda_flexes():
    """sigma permuta quadrados entre si e triangulos entre si; eps_j esta na
    co-classe (s_sigma(j) - s_j) + simetria do ladrilho."""
    from itertools import permutations
    for pq in permutations(range(2)):
        for pt in permutations(range(2, 5)):
            sig = list(pq) + list(pt)
            opc = [[(RODA_S[sig[j]] - RODA_S[j] + e) % 12
                    for e in RODA_SIM[RODA_TIPO[j]]] for j in range(5)]
            for eps in product(*opc): yield tuple(sig), tuple(eps)


def roda_classifica(sig, eps):
    A = [(eps[j], sub(RODA_C[sig[j]], zpow(eps[j], RODA_C[j]))) for j in range(5)]
    def inv(g):
        a, t = g; return ((-a) % 12, neg(zpow(-a, t)))
    def comp(g, h):
        a, t = g; b, u = h; return ((a + b) % 12, add(zpow(a, u), t))
    import math
    gens = [comp(inv(A[k]), A[j]) for j in range(5) for k in range(5)]
    gens = [g for g in gens if g != (0, ZERO)]
    if not gens: return ("trivial", 1)
    Pd = 0
    for a, _ in gens: Pd = math.gcd(Pd, a)
    Pd = math.gcd(Pd, 12); N = 12 // Pd if Pd else 1
    pf = set(); bom = True
    for a, t in A:
        if a % 12 == 0:
            if t != ZERO: bom = False; break
        else:
            q = resolve(sub((1, 0, 0, 0), ZP[a % 12]), t)
            if q is None: bom = False; break
            pf.add(q)
    if bom and len(pf) <= 1: return ("C_%d" % N, N)
    return (("cristalografico" if N in (1, 2, 3, 4, 6) else "DENSO"), N)


def roda_censo():
    c = Counter(); ex = {}
    for sig, eps in roda_flexes():
        nome, N = roda_classifica(sig, eps)
        c[(nome.split('_')[0] if nome.startswith('C_') else nome, N)] += 1
        ex.setdefault((nome, N), (sig, eps))
    return c, ex
