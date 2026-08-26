"""
wpgen.py -- funcao de Weierstrass P e P' para um reticulado QUALQUER de posto 2,
via funcoes teta de Jacobi, com reducao de Gauss da base (garante |q| pequeno).
Vetorizado em numpy.
"""
import numpy as np


# ------------------------------------------------------------------ reticulado
def gauss_reduce(w1, w2):
    """base reduzida de Gauss: |w1| <= |w2| e |Re(w2/w1)| <= 1/2."""
    w1, w2 = complex(w1), complex(w2)
    while True:
        if abs(w2) < abs(w1):
            w1, w2 = w2, w1
        m = round((w2/w1).real)
        if m == 0:
            break
        w2 = w2 - m*w1
        if abs(w2) >= abs(w1):
            break
    if abs(w2) < abs(w1):
        w1, w2 = w2, w1
    if (w2/w1).imag < 0:
        w2 = -w2
    return w1, w2


def theta_series(n, v, q, N=None):
    v = np.asarray(v, dtype=complex)
    if N is None:
        N = max(8, int(np.ceil(np.sqrt(40/max(1e-12, -np.log(abs(q)))))) + 6)
    if n == 1:
        s = np.zeros_like(v)
        for k in range(N):
            s = s + (-1)**k * q**(k*(k+1)) * np.sin((2*k+1)*v)
        return 2*q**0.25*s
    if n == 2:
        s = np.zeros_like(v)
        for k in range(N):
            s = s + q**(k*(k+1)) * np.cos((2*k+1)*v)
        return 2*q**0.25*s
    if n == 3:
        s = np.ones_like(v)
        for k in range(1, N):
            s = s + 2*q**(k*k)*np.cos(2*k*v)
        return s
    if n == 4:
        s = np.ones_like(v)
        for k in range(1, N):
            s = s + 2*(-1)**k*q**(k*k)*np.cos(2*k*v)
        return s
    raise ValueError(n)


def dtheta_series(n, v, q, N=None):
    """derivada em v."""
    v = np.asarray(v, dtype=complex)
    if N is None:
        N = max(8, int(np.ceil(np.sqrt(40/max(1e-12, -np.log(abs(q)))))) + 6)
    if n == 1:
        s = np.zeros_like(v)
        for k in range(N):
            s = s + (-1)**k * q**(k*(k+1)) * (2*k+1)*np.cos((2*k+1)*v)
        return 2*q**0.25*s
    if n == 4:
        s = np.zeros_like(v)
        for k in range(1, N):
            s = s - 2*(-1)**k*q**(k*k)*2*k*np.sin(2*k*v)
        return s
    raise ValueError(n)


class WP:
    """P(.;Lambda) para Lambda = w1 Z + w2 Z (posto 2)."""

    def __init__(self, w1, w2):
        w1, w2 = gauss_reduce(w1, w2)
        self.w1, self.w2 = w1, w2
        self.tau = w2/w1
        assert self.tau.imag > 1e-9, "base degenerada"
        self.q = np.exp(1j*np.pi*self.tau)
        z0 = np.array([0.0+0j])
        self.t2 = complex(theta_series(2, z0, self.q)[0])
        self.t3 = complex(theta_series(3, z0, self.q)[0])
        self.k = (np.pi/w1)**2
        self.const = (self.t2**4 + self.t3**4)/3

    def __call__(self, z):
        z = np.asarray(z, dtype=complex)
        v = np.pi*z/self.w1
        t1 = theta_series(1, v, self.q); t4 = theta_series(4, v, self.q)
        with np.errstate(divide='ignore', invalid='ignore'):
            r = (t4/t1)**2
        return self.k*(self.t2**2*self.t3**2*r - self.const)

    def deriv(self, z):
        z = np.asarray(z, dtype=complex)
        v = np.pi*z/self.w1
        t1 = theta_series(1, v, self.q); t4 = theta_series(4, v, self.q)
        d1 = dtheta_series(1, v, self.q); d4 = dtheta_series(4, v, self.q)
        with np.errstate(divide='ignore', invalid='ignore'):
            out = 2*(np.pi/self.w1)*self.k*self.t2**2*self.t3**2 * \
                  (t4/t1)*(d4*t1 - t4*d1)/t1**2
        return out


def wp_direct(z, w1, w2, N=80):
    """soma de Eisenstein (lenta) para conferencia."""
    z = complex(z)
    s = 1/z**2
    for m in range(-N, N+1):
        for n in range(-N, N+1):
            if m == 0 and n == 0: continue
            lam = m*w1 + n*w2
            s += 1/(z-lam)**2 - 1/lam**2
    return s


if __name__ == "__main__":
    for (w1, w2) in [(2, 2j), (1+1j, -1+1j), (2, 1+3j), (1, 1j)]:
        P = WP(w1, w2)
        z = 0.31+0.17j
        a = complex(P(np.array([z]))[0]); b = wp_direct(z, complex(w1), complex(w2), 90)
        h = 1e-5
        da = complex(P.deriv(np.array([z]))[0])
        num = (complex(P(np.array([z+h]))[0]) - complex(P(np.array([z-h]))[0]))/(2*h)
        print(f"w=({w1},{w2})  tau={P.tau:.4f}  |q|={abs(P.q):.4f}   "
              f"P: dif={abs(a-b):.2e}   P': dif={abs(da-num):.2e}")
