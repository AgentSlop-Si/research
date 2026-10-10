#!/usr/bin/env python3
"""Independent checks of COMMUTING_PHASE_GATE.md; no uploaded executable imports."""
from collections import Counter
from itertools import combinations_with_replacement
import json
from pathlib import Path
import numpy as np
import sympy as sp
from apply_fused_halfcycle import FusedHalfCycle, power_of_two_by_squaring

BASE = Path(__file__).resolve().parent


def exact_zero(matrix):
    return all(sp.expand(x) == 0 for x in matrix)


def signed_cycle(n, exact=False):
    matrix = sp.zeros(n) if exact else np.zeros((n, n), dtype=complex)
    matrix[0, n-1] = -1
    for j in range(1, n):
        matrix[j, j-1] = 1
    return matrix


def k_matrix(matrix):
    identity = np.eye(len(matrix), dtype=complex)
    return (2*identity-matrix) @ np.linalg.inv(identity-matrix)


# Symbolic checks hold for arbitrary nonzero circle-location parameter a.
z, a = sp.symbols('z a', nonzero=True)
A = (2*a-z)/(a-z)
B = (2*z-a)/(z-a)
V = (z-2*a)/(2*z-a)
assert sp.cancel(A/B-V) == 0
assert sp.cancel(B/A-1/V) == 0
assert sp.cancel(A.subs({a: 1/a, z: 1/z}, simultaneous=True)-B) == 0
assert sp.cancel(V*V.subs({a: 1/a, z: 1/z}, simultaneous=True)-1) == 0
symbolic = {'exact_rational_pairing': True, 'inverse_phase_index': True,
            'reciprocal_conjugate_allpass_identity': True}

# Exact Gaussian-rational matrix examples, so these tests need no rounding.
exact = []
for n in (4, 8, 12):
    S = signed_cycle(n, exact=True)
    I = sp.eye(n)
    for phase in (sp.Integer(1), sp.Integer(-1), sp.I, -sp.I):
        X = phase*S
        K = (2*I-X)*(I-X).inv()
        Kstar = (2*I-X.H)*(I-X.H).inv()
        Vmat = K*Kstar.inv()
        c = sp.Rational(2**(n+1)-1, 2**n+1)
        assert exact_zero(X**n+I)
        assert exact_zero(Vmat.H*Vmat-I)
        assert exact_zero(Vmat-(X-2*I)*(2*X-I).inv())
        assert max(sum(sp.Abs(Vmat[i,j]) for i in range(n)) for j in range(n)) == c
        assert sp.expand(K.det()-sp.Rational(2**n+1, 2)) == 0
        exact.append({'N': n, 'phase': str(phase), 'exact': True})

# Numerically exhaust commuting multisets. Order does not matter in this family.
# Each stage is (phase exponent j, orientation +1/-1, forward/inverse sign).
enumeration = []
for n in range(3, 11):
    eig = np.exp(1j*np.pi*(2*np.arange(n)+1)/n)
    stages = [(j, orientation, sign)
              for j in range(n) for orientation in (1,-1) for sign in (1,-1)]
    log_moduli = []
    circle_indices = []
    for j, orientation, sign in stages:
        phase = np.exp(2j*np.pi*j/n)
        value = phase*eig**orientation
        log_moduli.append(sign*np.log(np.abs((2-value)/(1-value))))
        circle_indices.append((-j if orientation == 1 else j) % n)
    log_moduli = np.asarray(log_moduli)
    rows = []
    max_length = min(4, (n-1)//2)
    for length in range(max_length+1):
        total = 0
        unitary = 0
        minimum_nonconstant_spread = None
        for word in combinations_with_replacement(range(4*n), length):
            total += 1
            if word:
                logs = log_moduli[list(word)].sum(axis=0)
            else:
                logs = np.zeros(n)
            spread = float(np.max(logs)-np.min(logs))
            scalar_unitary = spread < 1e-10
            balances = Counter()
            for index in word:
                balances[circle_indices[index]] += stages[index][2]
            balanced = all(count == 0 for count in balances.values())
            assert scalar_unitary == balanced, (n, word, spread, balances)
            if balanced:
                unitary += 1
                assert length % 2 == 0
                assert float(np.max(np.abs(logs))) < 1e-10
            else:
                minimum_nonconstant_spread = (spread if minimum_nonconstant_spread is None
                                              else min(minimum_nonconstant_spread, spread))
        rows.append({'length': length, 'multisets': total,
                     'scalar_unitary_and_circle_balanced': unitary,
                     'minimum_unbalanced_log_modulus_spread': minimum_nonconstant_spread})
    enumeration.append({'N': n, 'maximum_short_length_checked': max_length,
                        'numerical_tolerance': 1e-10, 'rows': rows})

# All phase indices, genuine non-real cycle weights, monomial dressings, and norms.
rng = np.random.default_rng(20261009)
phase_matrices = []
for n in range(3, 13):
    S = signed_cycle(n)
    gauge = np.exp(1j*rng.uniform(-np.pi, np.pi, n))
    M = gauge[:,None]*S*np.conjugate(gauge)[None,:]
    I = np.eye(n)
    cn = 2-3/(2**n+1)
    largest_residual = 0.0
    for j in range(n):
        phase = np.exp(2j*np.pi*j/n)
        X = phase*M
        K = k_matrix(X)
        reverse = k_matrix(np.conjugate(phase)*M.conj().T)
        pair = K @ np.linalg.inv(reverse)
        direct = (X-2*I) @ np.linalg.inv(2*X-I)
        residuals = [np.max(np.abs(pair-direct)),
                     np.max(np.abs(pair.conj().T@pair-I)),
                     abs(np.linalg.norm(pair, 1)-cn),
                     abs(np.linalg.norm(np.linalg.inv(pair), 1)-cn)]
        largest_residual = max(largest_residual, *(float(x) for x in residuals))
        assert largest_residual < 1e-10
    phase_matrices.append({'N': n, 'phases_checked': n,
                           'largest_residual': largest_residual})

# Sharp boundary t=N/2: all-forward scalar-unitary words, not circle-balanced.
boundary = []
for n in (2, 4, 6, 8, 10, 12, 16):
    m = n//2
    S = signed_cycle(n)
    I = np.eye(n)
    product = I.astype(complex)
    for j in range(m):
        phase = np.exp(2j*np.pi*j/m)
        product = product @ k_matrix(phase*S)
    formula = ((2**m+1)*I+(2**m-1)*np.linalg.matrix_power(S,m))/2
    scale2 = (4**m+1)/2
    formula_error = float(np.max(np.abs(product-formula))/max(1,np.max(np.abs(formula))))
    unitary_error = float(np.max(np.abs(product.conj().T@product/scale2-I)))
    assert formula_error < 1e-10 and unitary_error < 1e-10
    # Exact matrix identity for the closed form independently confirms the scale.
    SX = signed_cycle(n, exact=True)**m
    EI = sp.eye(n)
    ER = ((2**m+1)*EI+(2**m-1)*SX)/2
    assert exact_zero(ER.H*ER-sp.Rational(4**m+1,2)*EI)
    polyP = 2**m-z**m
    polyQ = 1-z**m
    H = sp.expand(polyP*(2**m*z**m-1)-sp.Rational(4**m+1,2)*polyQ*(z**m-1))
    assert sp.expand(H-sp.Rational((2**m-1)**2,2)*(z**n+1)) == 0
    boundary.append({'N': n, 't': m, 'exact_squared_modulus': str(sp.Rational(4**m+1,2)),
                     'exact_closed_form_identity': True,
                     'product_relative_error': formula_error,
                     'normalized_gram_residual': unitary_error})

# Exact weighted-cycle tests for the reusable fused evaluator.
fused = []
for n in (2, 4, 6, 8, 12, 16):
    order = list(range(n))
    rng.shuffle(order)
    weights = [sp.Integer(1)] + [sp.I**int(rng.integers(0, 4)) for _ in range(n-1)]
    weights[0] = -1/sp.prod(weights[1:])
    M = sp.zeros(n)
    for j in range(n):
        M[order[j], order[j-1]] = weights[j]
    m = n//2
    formula = ((2**m+1)*sp.eye(n)+(2**m-1)*M**m)/2
    evaluator = FusedHalfCycle(n, order, weights)
    x = [sp.Rational(j-3,j+1)+sp.I*sp.Rational(2-j,j+2) for j in range(n)]
    assert exact_zero(sp.Matrix(evaluator.apply(x))-formula*sp.Matrix(x))
    assert power_of_two_by_squaring(m) == 2**m
    fused.append({'N': n, 'exact_weighted_evaluation': True})

results = {
    'status': 'PASS',
    'scope': 'Finite checks corroborate; COMMUTING_PHASE_GATE.md proves the all-N claims.',
    'symbolic_checks': symbolic,
    'exact_phase_matrix_checks': exact,
    'exhaustive_short_multisets_numerical': enumeration,
    'total_multisets_checked': sum(row['multisets'] for item in enumeration for row in item['rows']),
    'phase_rotated_matrix_checks_numerical': phase_matrices,
    'strict_cutoff_examples': boundary,
    'fused_halfcycle_evaluator_checks': fused,
    'provenance': 'Independently authored; imports no uploaded executable source.'
}
(BASE/'commuting_phase_results.json').write_text(json.dumps(results, indent=2)+'\n')
print(json.dumps(results, indent=2))
