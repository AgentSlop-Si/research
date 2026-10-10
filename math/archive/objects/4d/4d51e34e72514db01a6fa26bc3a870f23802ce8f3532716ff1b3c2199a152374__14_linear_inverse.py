"""Exact O(N)-work inverse for the supplied parity-mixed Green operator.

M = P T^{-1} P^T + epsilon T^{-1}; epsilon = 1/20 (default).
N even, T = tridiag(-1, 3, -1), arithmetic in F_998244353.

This is a NEW mathematical observation about the baseline stage. It does
not compute a Fourier transform, and its dense inverse does not imply
computational hardness.
"""

MOD = 998244353


def inv(a, p=MOD):
    a %= p
    if not a:
        raise ZeroDivisionError('zero pivot modulo p')
    return pow(a, p-2, p)


def interleave_order(n):
    assert n % 2 == 0 and n >= 4
    m = n // 2
    return [v for k in range(m) for v in (k, m+k)]


def tridiagonal_multiply(x, p=MOD):
    n = len(x)
    return [((3*x[i]) - (x[i-1] if i else 0) -
             (x[i+1] if i+1 < n else 0)) % p for i in range(n)]


class PentadiagonalLDLT:
    """Linear-time exact LDL^T factorization of SPD pentadiagonal K0.

    K0 has diagonal 3(1+eps), first offdiagonals -eps, second offdiagonals -1.
    Its real SPD property ensures no zero rational pivots. Audit finite
    field nonzero pivots separately; modular vanishing remains possible.
    """

    def __init__(self, n, eps, p=MOD):
        self.n, self.p = n, p
        self.d = [0]*n
        self.dinv = [0]*n
        self.l1 = [0]*n
        self.l2 = [0]*n
        diag = 3*(1+eps)%p
        for i in range(n):
            if i >= 2:
                self.l2[i] = -self.dinv[i-2] % p
            if i >= 1:
                subtract = (self.l2[i]*self.d[i-2]*self.l1[i-1] if i>=2 else 0)
                self.l1[i] = (-eps-subtract)*self.dinv[i-1] % p
            delta = diag
            if i >= 1:
                delta -= self.l1[i]*self.l1[i]*self.d[i-1]
            if i >= 2:
                delta -= self.l2[i]*self.l2[i]*self.d[i-2]
            self.d[i] = delta % p
            self.dinv[i] = inv(self.d[i], p)

    def solve(self, b):
        assert len(b) == self.n
        n,p = self.n,self.p
        z=[0]*n
        for i in range(n):
            z[i] = (b[i]-(self.l1[i]*z[i-1] if i>=1 else 0)
                     -(self.l2[i]*z[i-2] if i>=2 else 0))%p
        x=[z[i]*self.dinv[i]%p for i in range(n)]
        for i in range(n-1,-1,-1):
            x[i] = (x[i]-(self.l1[i+1]*x[i+1] if i+1<n else 0)
                      -(self.l2[i+2]*x[i+2] if i+2<n else 0))%p
        return x


class ParityGreenInverse:
    """Precompute O(N) coefficients, apply M^{-1} in O(N) field operations."""

    def __init__(self, n, eps=None, p=MOD):
        assert n % 2 == 0 and n >= 4
        self.n, self.p = n, p
        if eps is None:
            eps = inv(20,p)
        self.eps = eps%p
        self.order = interleave_order(n)
        self.band = PentadiagonalLDLT(n, self.eps, p)
        self.a,self.b = 1,n-2
        e1=[int(i==self.a) for i in range(n)]
        e2=[int(i==self.b) for i in range(n)]
        self.w1=self.band.solve(e1)
        self.w2=self.band.solve(e2)
        aa = self.w1[self.a]
        ab = self.w2[self.a]-1
        ba = self.w1[self.b]-1
        bb = self.w2[self.b]
        self.coeff=(aa%p, ab%p,ba%p,bb%p)
        self.det_inv=inv(aa*bb-ab*ba,p)

    def solve_k(self, v):
        """Apply (Q (T+eps PTP^T) Q^T)^{-1} via rank-two update."""
        p=self.p
        z=self.band.solve(v)
        aa,ab,ba,bb=self.coeff
        za,zb=z[self.a],z[self.b]
        t1=(bb*za-ab*zb)*self.det_inv %p
        t2=(aa*zb-ba*za)*self.det_inv %p
        return [(z[i]-t1*self.w1[i]-t2*self.w2[i])%p for i in range(self.n)]

    def apply(self,x):
        assert len(x) == self.n
        p=self.p
        # Q x is the vector in interleaved parity coordinates.
        xp=[x[i]%p for i in self.order]
        # M^{-1}=T (T+eps PTP^T)^{-1} PTP^T.
        # Conjugate by Q=P^T: Q M^{-1} Q^T=(Q T Q^T) K'^{-1} T.
        b=tridiagonal_multiply(xp,p)
        z=self.solve_k(b)
        # Q^T z: scatter back to original coordinates.
        original=[0]*self.n
        for i,j in enumerate(self.order):
            original[j]=z[i]
        return tridiagonal_multiply(original,p)


def apply_parity_mixed_fast(x,eps=None,p=MOD):
    """Original M fast executor (independent from the inverse implementation)."""
    n=len(x)
    m=n//2
    order=list(range(0,n,2))+list(range(1,n,2))
    from green_solver_standalone import tri_solve  # independent reference
    if eps is None:
        eps=inv(20,p)
    y=[0]*n
    for i,j in enumerate(order): y[j]=x[i]
    yg=tri_solve(y,p)
    mixed1=[yg[j] for j in order]
    mixed2=tri_solve(x,p)
    return [(a+eps*b)%p for a,b in zip(mixed1,mixed2)]
