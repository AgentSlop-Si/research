"""Legal cyclic regularization; no free Fourier or limiting macro.

The radix-2 evaluator is a reference implementation for a regular parameter.
It is NOT a faster evaluator of the singular target H_q(C).
"""
from collections import Counter


class Counted:
    def __init__(self, field):
        self.field, self.count = field, Counter()
    def __getattr__(self, name): return getattr(self.field, name)
    def mul(self, a, b):
        self.count['mul'] += 1
        return self.field.mul(a, b)
    def add(self, a, b):
        self.count['add'] += 1
        return self.field.add(a, b)
    def sub(self, a, b):
        self.count['sub'] += 1
        return self.field.sub(a, b)
    def inv(self, a):
        self.count['inverse'] += 1
        return self.field.inv(a)
    def neg(self, a):
        self.count['neg'] += 1
        return self.field.neg(a)


def fft(field, x, powers):
    """Every butterfly, including unit twiddles, charged by supplied field.

The prepared powers use the positive root convention. Recursive slicing
performs O(N log N) word copies; this is charged asymptotically, not hidden.
"""
    n = len(x)
    if n == 1: return list(x)
    even = fft(field, x[::2], powers[::2])
    odd = fft(field, x[1::2], powers[::2])
    out = [field.zero]*n
    for k in range(n//2):
        value = field.mul(powers[k], odd[k])
        out[k], out[k+n//2] = field.add(even[k], value), field.sub(even[k], value)
    return out


def cyclic_h_values(field, n, powers, alpha, inverse_n):
    """O(N) values H_q(alpha*q^j) via the inhomogeneous orbit recurrence.

alpha is nonzero. H(qz)=(1-z)H(z)+z^N/N. The full orbit's multiplier
is 1-alpha^N; this determines the starting value without a DFT.
"""
    alpha_n = field.one
    for _ in range(n): alpha_n = field.mul(alpha_n, alpha)
    forcing = field.mul(alpha_n, inverse_n)
    factors = [field.sub(field.one, field.mul(alpha, power)) for power in powers]
    value = field.zero
    for factor in factors:
        value = field.add(field.mul(factor, value), forcing)
    value = field.mul(value, field.inv(alpha_n))
    values = [value]
    for factor in factors[:-1]:
        value = field.add(field.mul(factor, value), forcing)
        values.append(value)
    return values


def prepare(field, n, q, t, alpha):
    """Given q,t,alpha with alpha^N+t^N=1 and t*alpha !=0.

Parameter/root discovery is NOT included; the regularization requires an
N-th root in the working field or an extension. All prepared arrays are O(N).
"""
    if n < 2 or n & (n-1): raise ValueError('power-of-two N >= 2')
    if t == field.zero or alpha == field.zero:
        raise ValueError('nonzero regular parameters required')
    if field.add(field.power(t,n),field.power(alpha,n)) != field.one:
        raise ValueError('alpha^N+t^N must equal 1')
    c = Counted(field)
    powers = [field.one]
    for _ in range(n-1): powers.append(c.mul(powers[-1],q))
    qi = [powers[-j % n] for j in range(n)]
    ni = c.inv(field.integer(n))
    # W is the old upper weighted shift completed with its essential corner.
    weights = [c.sub(q,qi[i]) for i in range(n-1)] + [c.neg(c.mul(q,ni))]
    # V=-W U^-1. Its cyclic edge product equals 1.
    v = [c.neg(c.mul(weights[i],powers[(i+1)%n])) for i in range(n)]
    g = [field.one]
    for weight in v[:-1]: g.append(c.mul(g[-1],c.inv(weight)))
    gi = [c.inv(value) for value in g]
    ai = c.inv(alpha)
    d = [field.one]
    for k in range(1,n):
        factor = c.sub(field.one,c.mul(t,qi[k]))
        d.append(c.mul(c.mul(d[-1],factor),ai))
    di = [c.inv(value) for value in d]
    hv = cyclic_h_values(c,n,powers,alpha,ni)
    hdiag = [hv[-j % n] for j in range(n)]
    return dict(n=n,q=q,t=t,alpha=alpha,powers=powers,qi=qi,ni=ni,
                v=v,g=g,gi=gi,d=d,di=di,hdiag=hdiag,preparation=dict(c.count))


def apply_regularized(field, plan, x):
    """H_q(C_t)x with FOUR explicit length-N FFTs and five diagonals.

C_t=(I-tV)U. This routine refuses the singular t^N=1 target in preparation.
"""
    c = Counted(field)
    def diagonal(values, vector): return [c.mul(a,b) for a,b in zip(values,vector)]
    def forward(vector): return fft(c,vector,plan['powers'])
    def backward(vector):
        raw = fft(c,vector,plan['qi'])
        return [c.mul(plan['ni'],value) for value in raw]
    x = diagonal(plan['gi'],x)
    x = backward(diagonal(plan['di'],forward(x)))
    x = diagonal(plan['hdiag'],x)
    x = backward(diagonal(plan['d'],forward(x)))
    x = diagonal(plan['g'],x)
    return x, dict(c.count)
