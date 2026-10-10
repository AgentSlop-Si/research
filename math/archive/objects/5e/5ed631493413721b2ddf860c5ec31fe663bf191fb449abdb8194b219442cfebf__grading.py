"""Sparse grading and exact related-query transport for the finite q-kernel.

This is not a fresh fast transform. The first H_q(C) action is external and paid.
"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'fft_qweyl_boundary_research'))
from fixed_kernel import Counted
from operators import prepare_sparse


def prepare_grading(field, n, q):
    sparse = prepare_sparse(field, n, q)
    c = Counted(field)
    powers = [field.one]
    for _ in range(1, n):
        powers.append(c.mul(powers[-1], q))
    w = sparse.upper + [sparse.corner]
    r = [c.mul(powers[i], w[i]) for i in range(n)]
    d1 = [c.mul(r[i], c.sub(field.one, sparse.diagonal[(i+1)%n])) for i in range(n)]
    d2 = [c.neg(c.mul(r[i], w[(i+1)%n])) for i in range(n)]
    # Product r_i=1 is a proved precondition for a valid primitive root.
    prefix = [field.one]
    for value in r:
        prefix.append(c.mul(prefix[-1], value))
    inverse_r = [field.zero]*n
    suffix = field.one
    for i in range(n-1, -1, -1):
        inverse_r[i] = c.mul(prefix[i], suffix)
        suffix = c.mul(suffix, r[i])
    m = n//2
    h0 = field.one
    for value in r[:m]:
        h0 = c.mul(h0, value)
    h = [h0]
    for i in range(n-1):
        h.append(c.mul(c.mul(h[-1], inverse_r[i]), r[(i+m)%n]))
    half = c.inv(field.integer(2))
    total = dict(sparse.preparation)
    for key, value in c.count.items():
        total[key] = total.get(key, 0)+value
    return dict(n=n, q=q, r=r, inverse_r=inverse_r, d1=d1, d2=d2,
                h=h, half=half, preparation=total)


def apply_r(field, plan, x, inverse=False):
    n = plan['n']
    if len(x) != n:
        raise ValueError('wrong vector length')
    if inverse:
        return [field.mul(plan['inverse_r'][(i-1)%n], x[(i-1)%n]) for i in range(n)]
    return [field.mul(plan['r'][i], x[(i+1)%n]) for i in range(n)]


def apply_d(field, plan, x):
    n = plan['n']
    if len(x) != n:
        raise ValueError('wrong vector length')
    out = []
    for i in range(n):
        value = field.mul(plan['d2'][i], x[(i+2)%n])
        if i != n-1:
            value = field.add(value, field.mul(plan['d1'][i], x[(i+1)%n]))
        out.append(value)
    return out


def split_pairs(field, plan, x):
    """Coordinates in the +1/-1 eigenspaces of R^(N/2)."""
    n = plan['n']; m = n//2
    if len(x) != n:
        raise ValueError('wrong vector length')
    plus, minus = [], []
    for i in range(m):
        value = field.mul(plan['h'][i], x[i+m])
        plus.append(field.mul(plan['half'], field.add(x[i], value)))
        minus.append(field.mul(plan['half'], field.sub(x[i], value)))
    return plus+minus


def join_pairs(field, plan, x):
    n = plan['n']; m = n//2
    if len(x) != n:
        raise ValueError('wrong vector length')
    return ([field.add(x[i], x[i+m]) for i in range(m)] +
        [field.mul(plan['h'][i+m], field.sub(x[i], x[i+m])) for i in range(m)])
