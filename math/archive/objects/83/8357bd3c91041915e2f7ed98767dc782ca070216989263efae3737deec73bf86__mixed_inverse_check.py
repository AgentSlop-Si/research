#!/usr/bin/env python3
"""Auditor-authored exact checks; imports no uploaded software.

Run with Python 3. Standard library only. All operation counts are scalar-field
counts, not bit/word runtime. Dense matrices occur only in independent oracles.
"""
from fractions import Fraction
from math import isqrt
from random import Random
import json


class Field:
    def __init__(self, modulus=None):
        self.p = modulus
        self.count = 0

    def val(self, a):
        return a % self.p if self.p else Fraction(a)

    def add(self, a, b):
        self.count += 1
        return self.val(a + b)

    def sub(self, a, b):
        self.count += 1
        return self.val(a - b)

    def mul(self, a, b):
        self.count += 1
        return self.val(a * b)

    def inv(self, a):
        self.count += 1
        if not a:
            raise ArithmeticError('zero field pivot')
        return pow(a, -1, self.p) if self.p else 1 / a


class BandLDL:
    """Symmetric Toeplitz pentadiagonal, half-bandwidth at most two."""
    def __init__(self, n, diagonal, off1, off2, f):
        self.n, self.f = n, f
        self.d, self.id, self.l1, self.l2 = [], [], [], []
        for i in range(n):
            a = f.mul(off2, self.id[i-2]) if i >= 2 else f.val(0)
            numerator = f.sub(off1, f.mul(f.mul(a, self.d[i-2]), self.l1[i-1])) if i >= 2 else off1
            b = f.mul(numerator, self.id[i-1]) if i >= 1 else f.val(0)
            d = diagonal
            if i >= 1:
                d = f.sub(d, f.mul(f.mul(b, b), self.d[i-1]))
            if i >= 2:
                d = f.sub(d, f.mul(f.mul(a, a), self.d[i-2]))
            if not f.p:
                assert d > 0
            self.d.append(d)
            self.id.append(f.inv(d))
            self.l1.append(b)
            self.l2.append(a)

    def solve(self, rhs):
        f, n = self.f, self.n
        y = list(rhs)
        for i in range(n):
            if i >= 1:
                y[i] = f.sub(y[i], f.mul(self.l1[i], y[i-1]))
            if i >= 2:
                y[i] = f.sub(y[i], f.mul(self.l2[i], y[i-2]))
        x = [f.mul(y[i], self.id[i]) for i in range(n)]
        for i in range(n-1, -1, -1):
            if i+1 < n:
                x[i] = f.sub(x[i], f.mul(self.l1[i+1], x[i+1]))
            if i+2 < n:
                x[i] = f.sub(x[i], f.mul(self.l2[i+2], x[i+2]))
        return x


class MixedPlan:
    def __init__(self, n, f):
        assert n >= 2 and n % 2 == 0
        self.n, self.f = n, f
        self.order = list(range(0, n, 2)) + list(range(1, n, 2))
        self.eps = f.inv(f.val(20))
        self.green = BandLDL(n, f.val(3), f.val(-1), f.val(0), f)
        self.base = BandLDL(n, f.mul(f.val(3), f.add(f.val(1), self.eps)),
                            f.sub(f.val(0), self.eps), f.val(-1), f)
        self.a, self.b = 1, n-2
        ea, eb = [f.val(0)]*n, [f.val(0)]*n
        ea[self.a], eb[self.b] = f.val(1), f.val(1)
        self.za, self.zb = self.base.solve(ea), self.base.solve(eb)
        # Ctilde = C0 + U V^T; U=[e_a,e_b], V=[-e_b,-e_a].
        k00 = f.sub(f.val(1), self.za[self.b])
        k01 = f.sub(f.val(0), self.zb[self.b])
        k10 = f.sub(f.val(0), self.za[self.a])
        k11 = f.sub(f.val(1), self.zb[self.a])
        determinant = f.sub(f.mul(k00, k11), f.mul(k01, k10))
        di = f.inv(determinant)
        self.ki = [[f.mul(k11, di), f.mul(f.sub(f.val(0), k01), di)],
                   [f.mul(f.sub(f.val(0), k10), di), f.mul(k00, di)]]
        z = isqrt(n-1)
        if z*z < n-1:
            z += 1
        self.u = [f.val(z)] + [f.val(1)]*(n-1)
        self.hl = f.mul(f.val(2), f.inv(f.val(z*z+n-1)))

    def gather(self, x):
        return [x[i] for i in self.order]

    def scatter(self, x):
        y = [self.f.val(0)]*self.n
        for i, old in enumerate(self.order):
            y[old] = x[i]
        return y

    def t_apply(self, x):
        f = self.f
        y = [f.mul(f.val(3), v) for v in x]
        for i in range(self.n):
            if i:
                y[i] = f.sub(y[i], x[i-1])
            if i+1 < self.n:
                y[i] = f.sub(y[i], x[i+1])
        return y

    def b_apply(self, x):
        return self.gather(self.t_apply(self.scatter(x)))

    def forward(self, x):
        f = self.f
        a = self.gather(self.green.solve(self.scatter(x)))
        b = self.green.solve(x)
        return [f.add(a[i], f.mul(self.eps, b[i])) for i in range(self.n)]

    def c_solve(self, rhs):
        f = self.f
        y = self.base.solve(self.scatter(rhs))
        va, vb = f.sub(f.val(0), y[self.b]), f.sub(f.val(0), y[self.a])
        wa = f.add(f.mul(self.ki[0][0], va), f.mul(self.ki[0][1], vb))
        wb = f.add(f.mul(self.ki[1][0], va), f.mul(self.ki[1][1], vb))
        z = [f.sub(f.sub(y[i], f.mul(self.za[i], wa)), f.mul(self.zb[i], wb)) for i in range(self.n)]
        return self.gather(z)

    def inverse(self, x):
        return self.t_apply(self.c_solve(self.b_apply(x)))

    def reflect(self, x):
        f = self.f
        dot = f.val(0)
        for u, v in zip(self.u, x):
            dot = f.add(dot, f.mul(u, v))
        scale = f.mul(self.hl, dot)
        return [f.sub(v, f.mul(scale, u)) for u, v in zip(self.u, x)]


def dense_oracle(n, f):
    # Closed continuant formula is independent of the banded executor.
    d = [f.val(1), f.val(3)]
    for k in range(2, n+1):
        d.append(f.sub(f.mul(f.val(3), d[-1]), d[-2]))
    den = f.inv(d[n])
    g = [[f.mul(f.mul(d[min(i,j)], d[n-1-max(i,j)]), den) for j in range(n)] for i in range(n)]
    order = list(range(0,n,2)) + list(range(1,n,2))
    eps = f.inv(f.val(20))
    return [[f.add(g[order[i]][order[j]], f.mul(eps,g[i][j])) for j in range(n)] for i in range(n)]


def matvec(a, x, f):
    result = []
    for row in a:
        val = f.val(0)
        for r, v in zip(row, x):
            val = f.add(val, f.mul(r, v))
        result.append(val)
    return result


def rank(a, f):
    a = [list(row) for row in a]
    height = 0
    for j in range(len(a[0]) if a else 0):
        piv = next((i for i in range(height,len(a)) if a[i][j]),None)
        if piv is None:
            continue
        a[height],a[piv] = a[piv],a[height]
        di = f.inv(a[height][j])
        a[height] = [f.mul(v,di) for v in a[height]]
        for i in range(height+1,len(a)):
            v = a[i][j]
            if v:
                a[i] = [f.sub(a[i][k],f.mul(v,a[height][k])) for k in range(len(a[0]))]
        height += 1
    return height


def check_case(n, prime, rng):
    f = Field(prime)
    plan = MixedPlan(n,f)
    preparation = f.count
    oracle = dense_oracle(n,f)
    vectors = 0
    for _ in range(5):
        x = [f.val(rng.randrange(-100,101)) for _ in range(n)]
        y = plan.forward(x)
        assert y == matvec(oracle,x,f)
        assert plan.inverse(y) == x
        assert matvec(oracle,plan.inverse(x),f) == x
        assert plan.inverse(plan.reflect(plan.reflect(y))) == x
        rhs = plan.b_apply(x)
        w = plan.c_solve(rhs)
        tw,bw = plan.t_apply(w),plan.b_apply(w)
        assert [f.add(a,f.mul(plan.eps,b)) for a,b in zip(tw,bw)] == rhs
        vectors += 1
    m = n//2
    cross = rank([row[m:] for row in oracle[:m]],f)
    assert cross >= m-1
    before = f.count
    plan.forward(x)
    forward_ops = f.count-before
    before = f.count
    plan.inverse(x)
    inverse_ops = f.count-before
    assert preparation <= 50*n+100
    assert forward_ops <= 20*n+20
    assert inverse_ops <= 20*n+20
    return dict(n=n,field=str(prime) if prime else 'rationals',fresh_vectors=vectors,
                halfcut_rank=cross,setup_field_ops=preparation,
                forward_field_ops=forward_ops,inverse_field_ops=inverse_ops)


def main():
    rng = Random(1155)
    rational = [check_case(n,None,rng) for n in (2,4,6,8,10,12,16)]
    modular = [check_case(n,998244353,rng) for n in (2,4,6,8,10,16,32,64,128)]
    # Standalone endpoint normalization/phase-inverse checks.
    phase = []
    f = Field(998244353)
    for n in (8,16,32,64):
        plan = MixedPlan(n,f)
        omega = pow(3,(f.p-1)//n,f.p)
        left = [pow(omega,i*i,f.p) for i in range(n)]
        right = [pow(omega,i,f.p) for i in range(n)]
        x = [f.val(rng.randrange(f.p)) for _ in range(n)]
        y = [f.mul(a,b) for a,b in zip(left,plan.reflect(plan.forward([f.mul(a,b) for a,b in zip(right,x)])))]
        recovered = [f.mul(f.inv(a),b) for a,b in zip(right,plan.inverse(plan.reflect([f.mul(f.inv(a),b) for a,b in zip(left,y)])))]
        assert recovered == x
        phase.append(n)
    density = []
    for n in (8,16,32,64):
        f = Field(998244353)
        plan = MixedPlan(n,f)
        oracle = dense_oracle(n,f)
        inverse_columns, reflected_columns = [], []
        for j in range(n):
            e = [f.val(int(i == j)) for i in range(n)]
            col = plan.inverse(e)
            assert matvec(oracle,col,f) == e
            inverse_columns.append(col)
            reflected_columns.append(plan.reflect([oracle[i][j] for i in range(n)]))
        reflected = [[reflected_columns[j][i] for j in range(n)] for i in range(n)]
        inv_s_columns = [plan.inverse(plan.reflect([f.val(int(i == j)) for i in range(n)])) for j in range(n)]
        for j,col in enumerate(inv_s_columns):
            assert matvec(reflected,col,f) == [f.val(int(i == j)) for i in range(n)]
        counts = [sum(bool(v) for row in matrix for v in row)
                  for matrix in (oracle,reflected,inverse_columns,inv_s_columns)]
        assert counts == [n*n]*4
        s_rank = rank([row[n//2:] for row in reflected[:n//2]],f)
        assert s_rank == n//2
        density.append(dict(n=n,M_nonzeros=counts[0],S_nonzeros=counts[1],
                            M_inverse_nonzeros=counts[2],S_inverse_nonzeros=counts[3],
                            S_halfcut_rank=s_rank,full_inverse_column_checks=2*n))
    print(json.dumps(dict(status='PASS',rational_cases=rational,modular_cases=modular,
                          phase_inverse_lengths=phase,density_audits=density,
                          uploaded_software_executed=False),indent=2))


if __name__ == '__main__':
    main()
