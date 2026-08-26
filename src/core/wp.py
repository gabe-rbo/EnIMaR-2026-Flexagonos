"""
wp.py -- funcao de Weierstrass para reticulados QUADRADOS  L = w Z[i]  (caso
lemniscatico, tau = i, g_3 = 0), por funcoes theta de Jacobi.  Vetorizado.

Com periodos 2w1 = w e 2w2 = i w :  tau = i,  q = e^{i pi tau} = e^{-pi}.

  P(z) = (pi/(2w1))^2 [ th2(0)^2 th3(0)^2 (th4(v)/th1(v))^2 - (th2(0)^4+th3(0)^4)/3 ],
  v = pi z /(2 w1).
"""
import numpy as np

QDEF = np.exp(-np.pi)          # q para tau = i


def _th(n, v, q, N=25):
    """Funcoes theta de Jacobi th_n(v,q), v array complexo."""
    v = np.asarray(v, dtype=complex)
    if n == 1:
        s = np.zeros_like(v)
        for k in range(N):
            s += (-1)**k * q**(k*(k+1)) * np.sin((2*k+1)*v)
        return 2*q**0.25*s
    if n == 2:
        s = np.zeros_like(v)
        for k in range(N):
            s += q**(k*(k+1)) * np.cos((2*k+1)*v)
        return 2*q**0.25*s
    if n == 3:
        s = np.ones_like(v)
        for k in range(1, N):
            s += 2*q**(k*k)*np.cos(2*k*v)
        return s
    if n == 4:
        s = np.ones_like(v)
        for k in range(1, N):
            s += 2*(-1)**k*q**(k*k)*np.cos(2*k*v)
        return s
    raise ValueError(n)


class WPSquare:
    """P(.;L) para L = w Z[i]."""

    def __init__(self, w):
        self.w = complex(w)
        self.w1 = self.w/2
        self.q = QDEF
        z0 = np.array([0.0+0j])
        self.t2 = complex(_th(2, z0, self.q)[0])
        self.t3 = complex(_th(3, z0, self.q)[0])
        self.const = (self.t2**4 + self.t3**4)/3
        self.scale = (np.pi/(2*self.w1))**2

    def __call__(self, z):
        z = np.asarray(z, dtype=complex)
        v = np.pi*z/(2*self.w1)
        t1 = _th(1, v, self.q); t4 = _th(4, v, self.q)
        with np.errstate(divide='ignore', invalid='ignore'):
            r = (t4/t1)**2
        return self.scale*(self.t2**2*self.t3**2*r - self.const)

    def deriv(self, z, h=1e-6):
        z = np.asarray(z, dtype=complex)
        return (self(z+h) - self(z-h))/(2*h)


def wp_direct(z, w, N=60):
    """soma direta de Eisenstein (lenta, para conferencia)."""
    z = complex(z); w = complex(w)
    lat = [w*(m + 1j*n) for m in range(-N, N+1) for n in range(-N, N+1)
           if not (m == 0 and n == 0)]
    s = 1/z**2
    for lam in lat:
        s += 1/(z-lam)**2 - 1/lam**2
    return s
