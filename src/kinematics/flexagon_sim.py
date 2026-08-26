"""
Simulacao combinatoria/geometrica da dobradura dos flexagonos quadrados
do manual "Papel, quadrados misteriosos e ... matematica" (Milanes & Ribeiro, UFMG 2025).

Modelo: cada celula (quadradinho) do plano e uma folha (leaf).
Colocacao atual  = isometria do plano  z -> a*z + b   (face para cima)
                                       z -> a*conj(z)+b (face para baixo)
com a em mu_4 = {1,i,-1,-i}.
Ordem de empilhamento = lista global de baixo para cima.
Dobra "para tras" (mountain): a aba vai para BAIXO da parte fixa, com a ordem interna invertida.
"""
from fractions import Fraction as F
import itertools, json

# ---------- aritmetica exata em Q(i) ----------
class G:  # gaussian rational
    __slots__ = ('re','im')
    def __init__(self, re=0, im=0):
        self.re = F(re); self.im = F(im)
    def __add__(s,o): o=g(o); return G(s.re+o.re, s.im+o.im)
    def __radd__(s,o): return g(o)+s
    def __sub__(s,o): o=g(o); return G(s.re-o.re, s.im-o.im)
    def __rsub__(s,o): return g(o)-s
    def __neg__(s): return G(-s.re,-s.im)
    def __mul__(s,o):
        o=g(o); return G(s.re*o.re - s.im*o.im, s.re*o.im + s.im*o.re)
    def __rmul__(s,o): return g(o)*s
    def conj(s): return G(s.re,-s.im)
    def norm(s): return s.re*s.re + s.im*s.im
    def inv(s):
        n = s.norm(); assert n != 0
        return G(s.re/n, -s.im/n)
    def __truediv__(s,o): return s*g(o).inv()
    def __eq__(s,o): o=g(o); return s.re==o.re and s.im==o.im
    def __hash__(s): return hash((s.re,s.im))
    def __repr__(s):
        def f(x): return str(x)
        if s.im==0: return f(s.re)
        if s.re==0: return f(s.im)+"i"
        return f"({f(s.re)}{'+' if s.im>0 else '-'}{f(abs(s.im))}i)"
def g(x):
    if isinstance(x,G): return x
    if isinstance(x,complex): return G(F(x.real).limit_denominator(10**6),F(x.imag).limit_denominator(10**6))
    return G(x,0)
I = G(0,1); ONE = G(1,0); ZERO = G(0,0)

# ---------- isometrias  z -> a*z+b  (c=False)  ou  a*conj(z)+b (c=True) ----------
class Iso:
    __slots__=('a','b','c')
    def __init__(self,a=ONE,b=ZERO,c=False): self.a=g(a); self.b=g(b); self.c=c
    def __call__(self,z):
        z=g(z); return self.a*(z.conj() if self.c else z) + self.b
    def compose(self,other):   # self o other
        # self(other(z)) = a1*( (a2 z^(c2) + b2)^(c1) ) + b1
        a1,b1,c1 = self.a,self.b,self.c
        a2,b2,c2 = other.a,other.b,other.c
        if c1:
            return Iso(a1*a2.conj(), a1*b2.conj()+b1, not c2)
        return Iso(a1*a2, a1*b2+b1, c2)
    def __repr__(s): return f"z->{s.a}*{'conj(z)' if s.c else 'z'}+{s.b}"

def refl_vert(X):  # reflexao na reta x = X :  z -> 2X - conj(z)
    return Iso(G(-1,0), G(2*F(X),0), True)
def refl_horiz(Y): # reflexao na reta y = Y :  z -> conj(z) + 2iY
    return Iso(ONE, G(0,2*F(Y)), True)

# ---------- flexagono ----------
class Flexagon:
    def __init__(self, cells, faces_front, faces_back):
        """cells: lista de (r,c) do plano 4x4 (r=0 no topo).
           faces_front[(r,c)] = numero da face na frente do papel
           faces_back[(r,c)]  = numero da face no verso"""
        self.cells = list(cells)
        self.ff = faces_front; self.fb = faces_back
        # centro da celula (r,c) no plano:  x=c+1/2 , y=-(r+1/2)
        self.place = {cell: Iso() for cell in self.cells}    # identidade
        self.order = list(self.cells)                        # de baixo para cima
    def center0(self, cell):
        r,c = cell; return G(F(2*c+1,2), F(-(2*r+1),2))
    def center(self, cell):
        return self.place[cell](self.center0(cell))
    def flipped(self, cell):
        return self.place[cell].c
    def fold(self, kind, coord, keep, behind=True):
        """kind 'v': reta x=coord; kind 'h': reta y=coord.
           keep = 'left'/'right' ou 'below'/'above' : lado que NAO se move."""
        R = refl_vert(coord) if kind=='v' else refl_horiz(coord)
        moving=[]
        for cell in self.cells:
            z = self.center(cell)
            if kind=='v':
                mv = (z.re > F(coord)) if keep=='left' else (z.re < F(coord))
            else:
                mv = (z.im < F(coord)) if keep=='above' else (z.im > F(coord))
            if mv: moving.append(cell)
        for cell in moving:
            self.place[cell] = R.compose(self.place[cell])
        stat = [x for x in self.order if x not in moving]
        mov  = [x for x in self.order if x in moving]
        self.order = (mov[::-1] + stat) if behind else (stat + mov[::-1])
    def footprint(self, cell):
        z = self.center(cell)
        return (z.re, z.im)
    def stacks(self):
        d = {}
        for cell in self.order:      # de baixo para cima
            d.setdefault(self.footprint(cell), []).append(cell)
        return {k: v[::-1] for k,v in d.items()}   # agora de cima para baixo
    def visible(self):
        """(posicao) -> (celula, face mostrada, rotacao da celula)"""
        out={}
        for pos, st in self.stacks().items():
            top = st[0]
            P = self.place[top]
            face = self.fb[top] if P.c else self.ff[top]
            out[pos] = (top, face, P)
        return out
    def show(self):
        st = self.stacks()
        xs = sorted({k[0] for k in st}); ys = sorted({k[1] for k in st}, reverse=True)
        lines=[]
        for y in ys:
            row=[]
            for x in xs:
                if (x,y) in st:
                    top = st[(x,y)][0]; P=self.place[top]
                    row.append(str(self.fb[top] if P.c else self.ff[top]))
                else: row.append('.')
            lines.append(' '.join(row))
        return '\n'.join(lines)

# ------- dados do manual (figuras 1.2 e 1.3) -------
front = {(0,0):4,(0,1):2,(0,2):6,(0,3):6,
         (1,0):4,(1,3):2,
         (2,0):2,(2,3):4,
         (3,0):6,(3,1):6,(3,2):2,(3,3):4}
back  = {(0,0):3,(0,1):3,(0,2):1,(0,3):5,
         (1,0):1,(1,3):5,
         (2,0):5,(2,3):1,
         (3,0):5,(3,1):1,(3,2):3,(3,3):3}

fx = Flexagon(front.keys(), front, back)
print("=== plano inicial (frente) ===");  print(fx.show())
# passo 1: dobrar a linha de cima (r=0) para tras; charneira y = -1
fx.fold('h', -1, keep='below'); print("\n=== passo 1 ==="); print(fx.show())
# passo 2: dobrar a coluna da direita (c=3) para tras; charneira x = 3
fx.fold('v', 3, keep='left');   print("\n=== passo 2 ==="); print(fx.show())
# passo 3: dobrar a linha de baixo (r=3) para tras; charneira y = -3
fx.fold('h', -3, keep='above'); print("\n=== passo 3 ==="); print(fx.show())
# passo 4: dobrar a coluna da esquerda (c=0) para tras; charneira x = 1
fx.fold('v', 1, keep='right');  print("\n=== passo 4 ==="); print(fx.show())

# ---------- passo 5: "desenrolar e enrolar ao contrario" a pilha superior esquerda ----------
st = fx.stacks()
poss = sorted(st.keys(), key=lambda p:(-p[1],p[0]))
print("\n=== pilhas apos passo 4 (de cima para baixo) ===")
for p in poss:
    print(p, [(c, fx.fb[c] if fx.place[c].c else fx.ff[c], fx.place[c].a, fx.place[c].c) for c in st[p]])

TL = poss[0]                       # canto superior esquerdo
blk = st[TL]                       # de cima para baixo
low = [c for c in fx.order if c in blk]      # de baixo para cima
rest= [c for c in fx.order if c not in blk]
# inverter a ordem do rolo
new_blk = low[::-1]
newpos = {}
idx=0
fx.order = [c for c in fx.order]
# reconstruir: substituir as ocorrencias de blk na ordem global pela ordem invertida
seq = iter(new_blk)
fx.order = [next(seq) if c in blk else c for c in fx.order]
print("\n=== estado montado (face visivel) ===")
print(fx.show())
