"""Exact linear-arithmetic all-pass application.

Input scalars must implement exact field arithmetic if exactness is required.
Fractions and SymPy exact scalars work. Ordinary Python float/complex inputs
produce floating-point results, not an exact-arithmetic certificate.
"""
from fractions import Fraction

class AllPassCycle:
    """Prepare U(M)=(I-2M)(2I-M)^-1 and its inverse V(M).

    order[j] is the jth coordinate around the directed cycle.
    weights[j] is M[order[j], order[j-1]], including the wrap at j=0.
    The supplied weights must have modulus one and total product -1.
    The caller supplies those exact weights; arbitrary phase synthesis is
    not part of this evaluator's promise.
    """
    def __init__(self, n, order=None, weights=None):
        if n < 3:
            raise ValueError('This evaluator is presented for N >= 3.')
        self.n=n
        self.order=list(range(n)) if order is None else list(order)
        if len(self.order)!=n or set(self.order)!=set(range(n)):
            raise ValueError('order must be a permutation of range(n)')
        weights=[-1]+[1]*(n-1) if weights is None else list(weights)
        if len(weights)!=n:
            raise ValueError('weights must have length N')
        total=1
        for w in weights: total*=w
        if total != -1:
            raise ValueError('cycle weight product must equal -1 exactly')
        self.gauge=[1]
        for j in range(1,n): self.gauge.append(self.gauge[-1]*weights[j])
        self.gauge_inverse=[1/g if not isinstance(g,int) else Fraction(1,g)
                            for g in self.gauge]
        self.half=Fraction(1,2)
        a=Fraction(1)
        for _ in range(n-1): a*=self.half
        self.h=1/(2+a)

    def apply(self, x, inverse=False):
        """Apply U(M), or V(M)=U(M)^-1 when inverse=True."""
        if len(x)!=self.n:
            raise ValueError('input must have length N')
        xx=[self.gauge_inverse[j]*x[self.order[j]] for j in range(self.n)]
        if inverse: xx.reverse()
        b=0
        for j in range(1,self.n): b=(xx[j]+b)*self.half
        z=[(xx[0]-b)*self.h]
        for j in range(1,self.n): z.append((xx[j]+z[-1])*self.half)
        yy=[2*xx[j]-3*z[j] for j in range(self.n)]
        if inverse: yy.reverse()
        out=[None]*self.n
        for j in range(self.n): out[self.order[j]]=self.gauge[j]*yy[j]
        return out
