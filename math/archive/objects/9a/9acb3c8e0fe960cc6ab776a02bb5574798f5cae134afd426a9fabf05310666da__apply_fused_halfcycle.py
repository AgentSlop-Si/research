"""Apply the all-forward t=N/2 boundary product in O(N) scalar arithmetic.

The formula is scalar-unitary and two-sparse, not a Fourier algorithm.
Supply exact field scalars for exact results; floating-point input remains
floating-point. Coefficients have Theta(N) bits, so no linear bit-cost claim.
"""
from fractions import Fraction


def power_of_two_by_squaring(exponent):
    """O(log exponent) scalar multiplications; integers are not bounded-word."""
    answer, base = 1, 2
    while exponent:
        if exponent & 1:
            answer *= base
        exponent >>= 1
        if exponent:
            base *= base
    return answer


class FusedHalfCycle:
    """Prepare product_{lambda^(N/2)=1} K(lambda M) for even N.

    order[j] is the jth coordinate around the directed cycle.
    weights[j] is M[order[j],order[j-1]], with the wrap at j=0.
    Supplied weights must be unit modulus with total product -1.
    Preparation uses O(N) scalar operations for the weighted-cycle gauge,
    plus O(log N) scalar multiplications to construct 2^(N/2).
    """
    def __init__(self, n, order=None, weights=None):
        if n < 2 or n % 2:
            raise ValueError('N must be positive and even, with N >= 2')
        self.n = n
        self.m = n//2
        self.order = list(range(n)) if order is None else list(order)
        if len(self.order) != n or set(self.order) != set(range(n)):
            raise ValueError('order must be a permutation of range(N)')
        weights = [-1]+[1]*(n-1) if weights is None else list(weights)
        if len(weights) != n:
            raise ValueError('weights must have length N')
        total = 1
        for weight in weights:
            total *= weight
        if total != -1:
            raise ValueError('cycle weight product must equal -1 exactly')
        self.gauge = [1]
        for j in range(1, n):
            self.gauge.append(self.gauge[-1]*weights[j])
        self.gauge_inverse = [Fraction(1,g) if isinstance(g,int) else 1/g
                              for g in self.gauge]
        a = power_of_two_by_squaring(self.m)
        self.diagonal = Fraction(a+1, 2)
        self.halfcycle = Fraction(a-1, 2)

    def apply(self, x):
        if len(x) != self.n:
            raise ValueError('input must have length N')
        xx = [self.gauge_inverse[j]*x[self.order[j]] for j in range(self.n)]
        output = [None]*self.n
        for j in range(self.n):
            shifted = -xx[j+self.m] if j < self.m else xx[j-self.m]
            value = self.diagonal*xx[j]+self.halfcycle*shifted
            output[self.order[j]] = self.gauge[j]*value
        return output
