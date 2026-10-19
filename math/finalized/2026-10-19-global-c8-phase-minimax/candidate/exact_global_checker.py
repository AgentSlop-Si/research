#!/usr/bin/env python3
"""New exact checks for the global cyclic-shift commutator proof.

The universal inequalities are proved analytically in PROOF.md; this script
checks symbolic identities and the boundary witness in characteristic zero.
No prior script, local phase derivative, or phase search is run or imported.
"""
import json
from pathlib import Path
import sympy as sp
from sympy.polys.domains import QQ

checks = {}

def check(name, truth):
    checks[name] = bool(truth)
    if not truth:
        raise AssertionError(name)

n = 8
S = sp.zeros(n)
for j in range(n):
    S[(j + 1) % n, j] = 1
St = S.T
h = sp.symbols('h0:8')
b = sp.symbols('b0:8', nonzero=True)
C = sp.Matrix(n, n, lambda j, k: h[(j + k) % n])
B = sp.diag(*b)
Bi = sp.diag(*(1 / x for x in b))
Ksym = St * Bi * St * B
Gamma = sp.prod(b[::2]) / sp.prod(b[1::2])
check('symbolic_cyclic_Hankel_shift_relation', C * S == St * C)
expected_action = sp.zeros(n)
for j in range(n):
    expected_action[(j - 2) % n, j] = b[j] / b[(j - 1) % n]
check('symbolic_weighted_two_step_shift', Ksym == expected_action)
expected_fourth = sp.diag(*(Gamma if j % 2 == 0 else 1 / Gamma for j in range(n)))
check('symbolic_two_parity_cycle_products', (Ksym ** 4 - expected_fourth).applyfunc(sp.cancel) == sp.zeros(n))
x = sp.Symbol('x')
cp = Ksym.charpoly(x).as_expr()
check('symbolic_characteristic_polynomial', sp.cancel(cp - (x**4-Gamma)*(x**4-1/Gamma)) == 0)
check('symbolic_reverse_shift_is_not_forward_shift', C * S != S * C)

# For |t| < theta < pi/2 the difference below is positive:
# sin(theta)^2 - |exp(i*t)-cos(theta)|^2
# = 2*cos(theta)*(cos(t)-cos(theta)).
u, v = sp.symbols('u v', real=True)
check('scalar_centering_squared_gap_identity', sp.expand((1-u**2) - (1+u**2-2*u*v) - 2*u*(v-u)) == 0)

# Independent exact boundary-witness calculation in Q[z]/(z^16+1).
field = QQ.algebraic_field(sp.exp(sp.I * sp.pi / 16))
z = field.unit
zero = field.zero
one = field.one

def matzero():
    return [[zero for _ in range(n)] for _ in range(n)]

def ident():
    return [[one if j == k else zero for k in range(n)] for j in range(n)]

def mul(A, B):
    out = matzero()
    for j in range(n):
        for l in range(n):
            if A[j][l]:
                for k in range(n):
                    if B[l][k]:
                        out[j][k] += A[j][l] * B[l][k]
    return out

def scale(A, a):
    return [[a * t for t in row] for row in A]

def add(A, B):
    return [[a + b for a, b in zip(row, col)] for row, col in zip(A, B)]

def sub(A, B):
    return add(A, scale(B, -one))

def transpose(A):
    return [list(row) for row in zip(*A)]

def conj(a):
    # SymPy ANP.to_list stores the power-basis coefficients in descending order.
    coeffs = a.to_list()
    return sum((field.convert(c) * z ** (-(len(coeffs)-1-j)) for j, c in enumerate(coeffs)), zero)

def star(A):
    return transpose([[conj(t) for t in row] for row in A])

def rank(A):
    A = [row[:] for row in A]
    r = 0
    for k in range(n):
        pivot = next((j for j in range(r, n) if A[j][k]), None)
        if pivot is None:
            continue
        A[r], A[pivot] = A[pivot], A[r]
        p = A[r][k]
        A[r] = [a/p for a in A[r]]
        for j in range(r+1, n):
            p = A[j][k]
            if p:
                A[j] = [a-p*c for a, c in zip(A[j], A[r])]
        r += 1
    return r

I = ident()
root_two = z**4 + z**-4
F = [[root_two/4 * z**((-4*j*k) % 32) for k in range(n)] for j in range(n)]
qexp = [0, 2, 0, 10, 0, 2, 0, 10]
Q = [[z**qexp[j] if j == k else zero for k in range(n)] for j in range(n)]
P = scale(Q, z)
A = mul(P, P)
B = mul(Q, Q)
C = mul(mul(F, A), F)
M = mul(C, B)
S = [[one if j == (k+1) % n else zero for k in range(n)] for j in range(n)]
T = mul(mul(star(B), S), B)
K = mul(mul(mul(M, T), star(M)), star(T))
shift_K = mul(mul(mul(star(S), star(B)), star(S)), B)
check('exact_F_unitary', mul(F, star(F)) == I)
check('exact_M_unitary', mul(M, star(M)) == I)
check('exact_witness_intertwining', mul(mul(M, T), star(M)) == star(S))
check('exact_witness_commutator_shift_identity', K == shift_K)
check('exact_witness_cycle_product_minus_one', sp.prod([B[j][j] for j in range(0, n, 2)]) / sp.prod([B[j][j] for j in range(1, n, 2)]) == -one)
check('exact_witness_K_fourth_power_minus_I', mul(mul(mul(K, K), K), K) == scale(I, -one))
m_spectrum = [(2, 4), (-2, 2), (14, 2)]
k_spectrum = [(4, 2), (-4, 2), (12, 2), (-12, 2)]
check('exact_witness_M_eigenvalues_with_multiplicity', all(n-rank(sub(M, scale(I, z**e))) == d for e, d in m_spectrum))
check('exact_witness_K_eigenvalues_with_multiplicity', all(n-rank(sub(K, scale(I, z**e))) == d for e, d in k_spectrum))
V = mul(mul(P, F), Q)
W = mul(transpose(V), V)
check('exact_W_M_similarity', mul(mul(star(Q), W), Q) == M)
i = z**8
Y = scale(sub(V, [[conj(t) for t in row] for row in V]), one/(2*i))
s = (z-z**-1)/(2*i)
c = (z+z**-1)/2
YtY = mul(transpose(Y), Y)
check('exact_witness_Y_squared_singular_values', n-rank(sub(YtY, scale(I, s*s))) == 6 and n-rank(sub(YtY, scale(I, c*c))) == 2)
ReW = scale(add(W, [[conj(t) for t in row] for row in W]), one/2)
check('exact_YtY_ReW_identity', YtY == scale(sub(I, ReW), one/2))

# Destructive controls on direction, endpoint multiplicity, and sharpness.
controls = {
    'wrong_forward_commutator_rejected': K != mul(mul(mul(S, star(B)), S), B),
    'incorrect_witness_M_multiplicity_rejected': n-rank(sub(M, scale(I, z**2))) != 6,
    'closed_arc_at_most_two_claim_rejected': sum(d for e, d in k_spectrum if abs(e) <= 4) == 4,
    'closed_original_arc_at_most_five_claim_rejected': sum(d for e, d in m_spectrum if abs(e) <= 2) == 6,
}
check('all_destructive_controls_passed', all(controls.values()))
result = {
    'status': 'PASS',
    'scope': 'Symbolic arbitrary-variable shift identities and exact boundary witness; analytic inequalities in PROOF.md prove the global universal statement.',
    'arithmetic': 'Rational-function identities over Q(b0,...,b7,h0,...,h7), and characteristic-zero Q[z]/(z^16+1).',
    'checks': checks,
    'negative_controls': controls,
    'witness_M_spectrum': [{'eigenvalue': f'z^{e}', 'multiplicity': d} for e, d in m_spectrum],
    'witness_K_spectrum': [{'eigenvalue': f'z^{e}', 'multiplicity': d} for e, d in k_spectrum],
    'global_value': 'sin(pi/16)',
}
path = Path(__file__).with_name('EXACT_GLOBAL_CHECKS.json')
path.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
