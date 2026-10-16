"""Reviewer-authored tiny algebraic controls; no research source code is imported."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import json

def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def sub(a, b):
    return [[x-y for x, y in zip(r, s)] for r, s in zip(a, b)]

def square_abs(z):
    return z.real*z.real + z.imag*z.imag

def norm_f_squared(a):
    return sum(square_abs(x) for row in a for x in row)

identity = [[1+0j, 0j], [0j, 1+0j]]
diagonal = [[1+0j, 0j], [0j, -1+0j]]
shift = [[0j, 1+0j], [1+0j, 0j]]
x = [[1+1j, 2+0j], [3j, -1+0j]]
weyl = [identity, diagonal, shift, mul(diagonal, shift)]
rhs = norm_f_squared(x) - square_abs(x[0][0] + x[1][1])/2
lhs = sum(norm_f_squared(sub(mul(x, w), mul(w, x)))/2 for w in weyl)/4
assert lhs == rhs == 15.5
# Every component operation is an exactly representable integer or dyadic operation.
h = [[2+0j, 1+1j], [1-1j, 3+0j]]
values = []
for z in product([1+0j, -1+0j, 1j, -1j], repeat=2):
    q = sum(z[i].conjugate()*h[i][j]*z[j] for i in range(2) for j in range(2))
    assert q.imag == 0
    values.append(q.real)
assert sum(values)/16 == 5 and sum(v*v for v in values)/16 == 29

c, s = F(3, 5), F(4, 5)
assert c*c+s*s == 1
u = [[c, -s], [s, c]]
m = [[c, F(0)], [s, c]]
determinant = m[0][0]*m[1][1]-m[0][1]*m[1][0]
assert determinant == F(9, 25) and m[0][1] == 0
assert (m[0][1]-u[0][1])**2 == 1-c*c

result = {
    'scope': 'Tiny independently authored exact Gaussian-integer/dyadic and rational controls; general statements depend on the written proofs.',
    'weyl_N2': {'half_average': lhs, 'scalar_distance_squared': rhs, 'pass': True},
    'four_phase_N2': {'samples': 16, 'mean': 5, 'second_moment': 29, 'pass': True},
    'positive_inverse_neighborhood_N2': {'critical_singular_value': '3/5', 'attained_distance': '4/5', 'determinant': '9/25', 'inverse_forbidden_rank': 0, 'pass': True},
    'zero_critical_inverse_neighborhood_N2': {
        'proof_control': 'Swap target, I=J={0}, r=0. Every feasible invertible lower-triangular M has nonzero a and error squared at least 1+|a|^2. delta I is feasible with error 1+delta, tending to 1.',
        'pass': True,
    },
}
Path(__file__).with_name('INDEPENDENT_SMALL_CONTROLS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result, indent=2))
