"""Independent phase-eliminant implementation; no uploaded source imported.

Only Python standard library. Dense coefficient lists use ascending powers.
Bareiss divisions are checked for zero remainder. Optional geometric evaluation
uses a Karatsuba convolution and never asks for extra field roots.
"""
from dataclasses import dataclass


@dataclass
class Ledger:
    field_additions: int = 0
    field_multiplications: int = 0
    field_inversions: int = 0
    exact_divisions: int = 0
    max_polynomial_degree: int = 0
    max_numerator_degree: int = 0
    max_minor_degree: int = 0


class Polynomials:
    def __init__(self, prime, ledger=None):
        self.p = prime
        self.ledger = ledger or Ledger()

    def trim(self, a):
        while a and a[-1] == 0:
            a.pop()
        self.ledger.max_polynomial_degree = max(self.ledger.max_polynomial_degree, len(a)-1)
        return a

    def add(self, a, b, sign=1):
        self.ledger.field_additions += max(len(a), len(b))
        return self.trim([((a[i] if i < len(a) else 0) + sign * (b[i] if i < len(b) else 0)) % self.p for i in range(max(len(a), len(b)))])

    def scale(self, a, c):
        self.ledger.field_multiplications += len(a)
        return self.trim([(x*c) % self.p for x in a])

    def mul(self, a, b):
        if not a or not b:
            return []
        c = [0] * (len(a)+len(b)-1)
        for i, x in enumerate(a):
            if x:
                for j, y in enumerate(b):
                    if y:
                        c[i+j] = (c[i+j] + x*y) % self.p
                        self.ledger.field_multiplications += 1
                        self.ledger.field_additions += 1
        return self.trim(c)

    def karatsuba(self, a, b, cutoff=24):
        if not a or not b:
            return []
        if min(len(a),len(b)) <= cutoff:
            return self.mul(a,b)
        n = max(len(a),len(b))
        h = (n+1)//2
        a0,a1,b0,b1 = a[:h],a[h:],b[:h],b[h:]
        z0 = self.karatsuba(a0,b0,cutoff)
        z2 = self.karatsuba(a1,b1,cutoff)
        z1 = self.karatsuba(self.add(a0,a1),self.add(b0,b1),cutoff)
        z1 = self.add(self.add(z1,z0,-1),z2,-1)
        return self.add(self.add(z0,[0]*h+z1),[0]*(2*h)+z2)

    def inverse(self, c):
        assert c % self.p
        self.ledger.field_inversions += 1
        return pow(c,-1,self.p)

    def exact_divide(self, numerator, denominator, inverse_lead):
        assert denominator
        self.ledger.exact_divisions += 1
        self.ledger.max_numerator_degree = max(self.ledger.max_numerator_degree,len(numerator)-1)
        if not numerator:
            return []
        rem = numerator[:]
        if len(rem) < len(denominator):
            raise ArithmeticError('nonzero remainder')
        quo = [0]*(len(rem)-len(denominator)+1)
        for k in range(len(quo)-1,-1,-1):
            c = rem[k+len(denominator)-1] * inverse_lead % self.p
            self.ledger.field_multiplications += 1
            quo[k] = c
            if c:
                for j,v in enumerate(denominator):
                    rem[k+j] = (rem[k+j]-c*v) % self.p
                    self.ledger.field_additions += 1
                    self.ledger.field_multiplications += 1
        if any(rem):
            raise ArithmeticError('nonzero remainder')
        return self.trim(quo)


def degree_bound(rank):
    return rank*(rank+1)*(rank+2)//6


def normalized_matrix(window, rank, p):
    assert rank >= 1 and len(window) == 2*rank+1
    assert window[rank] % p != 0
    return [[([0]*((i-j)*(i-j-1)//2)+[window[rank+i-j]%p]) if window[rank+i-j]%p else [] for j in range(rank+1)] for i in range(rank+1)]


def phase_eliminant(window, rank, p, ledger=None):
    """Return P(t), where det(raw H)=t^E P. Assumes prime p.

    Costs O(rank^3 (D+1)^2) field operations with this schoolbook backend,
    O(rank) scalar inversions, and O(rank^2 (D+1)) storage.
    """
    ring = Polynomials(p,ledger)
    b = normalized_matrix(window,rank,p)
    previous = [1]
    n = rank+1
    D = degree_bound(rank)
    for k in range(n-1):
        pivot = b[k][k]
        assert pivot and pivot[0] == pow(window[rank],k+1,p)
        inverse_lead = 1 if previous == [1] else ring.inverse(previous[-1])
        for i in range(k+1,n):
            for j in range(k+1,n):
                numerator = ring.add(ring.mul(pivot,b[i][j]),ring.mul(b[i][k],b[k][j]),-1)
                b[i][j] = ring.exact_divide(numerator,previous,inverse_lead)
                ring.ledger.max_minor_degree = max(ring.ledger.max_minor_degree,len(b[i][j])-1)
                assert len(b[i][j])-1 <= D
        for i in range(k+1,n):
            b[i][k] = []
        previous = pivot
    determinant = b[-1][-1]
    if rank*(rank+1)//2 % 2:
        determinant = ring.scale(determinant,-1)
    assert determinant[0] == pow(-1,rank*(rank+1)//2,p)*pow(window[rank],rank+1,p)%p
    return determinant


def evaluate(coefficients,t,p):
    out = 0
    for c in reversed(coefficients):
        out = (out*t+c)%p
    return out


def geometric_values(coefficients,q,order,p,ledger=None):
    """All P(q^a), 0 <= a < order, with q of the supplied exact order.

    First reduce modulo t^order-1; then use a triangular-number chirp
    convolution with Karatsuba. This is a standard evaluation reduction,
    not an O(N) unrestricted Fourier transform.
    """
    assert order >= 1 and q % p
    ring = Polynomials(p,ledger)
    folded = [0]*order
    for j,c in enumerate(coefficients):
        folded[j%order] = (folded[j%order]+c)%p
        ring.ledger.field_additions += 1
    ring.trim(folded)
    if not folded:
        return [0]*order
    m = len(folded)
    # Build q^e for 0 <= e < order, including all setup work.
    powers = [1]*order
    for i in range(1,order):
        powers[i] = powers[i-1]*q%p
        ring.ledger.field_multiplications += 1
    assert powers[-1]*q%p == 1
    left = [folded[j]*powers[(j*(j+1)//2)%order]%p for j in range(m)]
    ring.ledger.field_multiplications += m
    right = [powers[(-(d*(d-1)//2))%order] for d in range(-(m-1),order)]
    product = ring.karatsuba(left,right)
    # A trimmed product represents omitted coefficients by zero.
    result = [(product[a+m-1] if a+m-1 < len(product) else 0)*powers[(a*(a-1)//2)%order]%p for a in range(order)]
    ring.ledger.field_multiplications += order
    return result


def phase_eliminant_toeplitz(window,rank,p,ledger=None):
    """P via nonsymmetric Levinson recursion in F_p[t]/(t^(D+1)).

    Every leading determinant has nonzero constant. One scalar inversion is
    reused for every formal-series inverse. With Karatsuba, the arithmetic
    bound is O(rank^2 (D+1)^log_2(3)); live storage is O(rank*(D+1)).
    """
    assert rank >= 1 and len(window)==2*rank+1 and window[rank]%p
    ring = Polynomials(p,ledger)
    limit = degree_bound(rank)+1
    inverse_center = ring.inverse(window[rank]%p)

    def trunc(poly,n=limit):
        return ring.trim(poly[:n])

    def product(a,b,n=limit):
        return trunc(ring.karatsuba(a,b),n)

    def inverse_series(f):
        assert f and f[0]==window[rank]%p
        g = [inverse_center]
        precision = 1
        while precision < limit:
            precision = min(2*precision,limit)
            residual = ring.add([2%p],product(f[:precision],g,precision),-1)
            g = product(g,residual,precision)
        return g

    diagonals = {d:([0]*(d*(d-1)//2)+[window[rank+d]%p] if window[rank+d]%p else []) for d in range(-rank,rank+1)}
    u,v = [[1]],[[1]]
    error = diagonals[0]
    determinant = error
    for k in range(1,rank+1):
        positive = diagonals[k][:]
        negative = diagonals[-k][:]
        for j in range(1,k):
            positive = ring.add(positive,product(diagonals[k-j],u[j]))
            negative = ring.add(negative,product(diagonals[j-k],v[j]))
        reciprocal = inverse_series(error)
        alpha = ring.scale(product(positive,reciprocal),-1)
        beta = ring.scale(product(negative,reciprocal),-1)
        unew,vnew = [[1]],[[1]]
        for j in range(1,k):
            unew.append(ring.add(u[j],product(alpha,v[k-j])))
            vnew.append(ring.add(v[j],product(beta,u[k-j])))
        unew.append(alpha)
        vnew.append(beta)
        u,v = unew,vnew
        error = ring.add(error,product(alpha,negative))
        assert error[0] == window[rank]%p
        determinant = product(determinant,error)
    if rank*(rank+1)//2%2:
        determinant = ring.scale(determinant,-1)
    assert len(determinant)<=limit
    return determinant
