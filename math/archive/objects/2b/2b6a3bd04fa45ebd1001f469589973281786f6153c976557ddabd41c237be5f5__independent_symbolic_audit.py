#!/usr/bin/env python3
"""Fresh inert-input symbolic audit. No uploaded executable is used.

Rebuilds the inherited polynomial generators from the defining recurrences,
then verifies all gate minors in Q[z]/(z^4+1)[h0,h1,h2,h6].
Requires Python 3 and SymPy. All paths are relative to this file.
"""
from pathlib import Path
from itertools import combinations
import json, time
import sympy as sp
from sympy.polys.rings import ring

HERE = Path(__file__).resolve().parent
started = time.monotonic()
zz = sp.Symbol('z')
FIELD = sp.QQ.alg_field_from_poly(sp.Poly(zz**4 + 1, zz), alias='z')
R, h0, h1, h2, h6 = ring('h0,h1,h2,h6', FIELD)
ZERO, ONE = R.zero, R.one
z = R.ground_new(FIELD.unit)


def det(rows):
    """Exterior-product determinant, with exact sparse polynomial arithmetic."""
    n = len(rows)
    assert all(len(row) == n for row in rows)
    state = {0: ONE}
    for row in rows:
        nxt = {}
        for mask, value in state.items():
            for col, entry in enumerate(row):
                if entry and not (mask & (1 << col)):
                    key = mask | (1 << col)
                    sign = -1 if (mask >> (col + 1)).bit_count() % 2 else 1
                    nxt[key] = nxt.get(key, ZERO) + sign * value * entry
        state = {key: value for key, value in nxt.items() if value}
    return state.get((1 << n) - 1, ZERO)


def scalar_coefficients(value):
    assert not any(any(mon) for mon in value)
    c = value.get((0, 0, 0, 0), FIELD.zero)
    coeffs = list(reversed(c.to_list()))
    return [str(v) for v in (coeffs + [0] * 4)[:4]]


def record(poly):
    terms = []
    for mon, c in sorted(poly.items(), key=lambda kv: (sum(kv[0]), kv[0])):
        coeffs = (list(reversed(c.to_list())) + [0] * 4)[:4]
        assert all(not v or v.denominator == 1 for v in coeffs)
        terms.append([[j for j, exponent in enumerate(mon) for _ in range(exponent)],
                      [int(v) for v in coeffs]])
    return {'term_count': len(poly), 'degree': max(map(sum, poly), default=0), 'terms': terms}


def parse_record(data):
    terms = {}
    for indices, coefficients in data['terms']:
        exponents = [0] * 4
        for index in indices:
            exponents[index] += 1
        assert tuple(exponents) not in terms
        terms[tuple(exponents)] = sum((int(c) * FIELD.unit**i for i, c in enumerate(coefficients)), FIELD.zero)
    return R.from_dict(terms)


def reduce_mod(poly, prime, root, parameters=(0, 0, 0, 0)):
    result = 0
    for exponents, c in poly.items():
        value = 0
        for coefficient in c.to_list():
            value = (value * root + int(coefficient.numerator) * pow(int(coefficient.denominator), -1, prime)) % prime
        for parameter, exponent in zip(parameters, exponents):
            value = value * pow(parameter, exponent, prime) % prime
        result = (result + value) % prime
    return result


# The upper sequence obeys the three-mode recurrence with roots 1,z^-1,z^-2.
frequencies = [ONE, z**7, z**6]
e1 = sum(frequencies, ZERO)
e2 = sum((frequencies[i] * frequencies[j] for i, j in combinations(range(3), 2)), ZERO)
e3 = frequencies[0] * frequencies[1] * frequencies[2]
H = [h0, h1, h2]
while len(H) < 6:
    H.append(e1 * H[-1] - e2 * H[-2] + e3 * H[-3])
H += [h6, ONE]

# Write the pre-rescaling lower generator as L=c+t*a+beta*b.
c, a, b = [ZERO] * 8, [ZERO] * 8, [ZERO] * 8
for k in range(1, 7):
    inverse_character = z**((-k) % 8)
    c[k] = z - inverse_character
    a[k] = inverse_character - ONE
    b[k] = (z - ONE) * (H[k] - h0) + (h0 - ONE) * a[k]
a[7] = z - ONE
f = [z, z**2, z**3]
s1 = sum(f, ZERO)
s2 = sum((f[i] * f[j] for i, j in combinations(range(3), 2)), ZERO)
s3 = f[0] * f[1] * f[2]


def tail_recurrence(values, k):
    return values[k + 3] - s1 * values[k + 2] + s2 * values[k + 1] - s3 * values[k]


aa, bb, cc = [tail_recurrence(values, 3) for values in (a, b, c)]
dd, ee, ff = [tail_recurrence(values, 4) for values in (a, b, c)]
Delta = aa * ee - bb * dd
T = bb * ff - cc * ee
Vcoef = cc * dd - aa * ff
U = H[:7] + [ZERO]
L = [Delta * c[k] + T * a[k] + Vcoef * b[k] for k in range(8)]
assert tail_recurrence(L, 3) == tail_recurrence(L, 4) == ZERO

Y = {}
for j, height in ((1, 5), (2, 5), (4, 4), (5, 5)):
    Y[j] = [[z**((i * j) % 8),
             sum((U[k] * z**((i * k) % 8) for k in range(j)), ZERO),
             sum((L[k] * z**((i * k) % 8) for k in range(j + 1, 8)), ZERO)]
            for i in range(height)]
eta = [(-1)**i * det(Y[4][:i] + Y[4][i + 1:]) for i in range(4)]
ell = [sum((eta[i] * Y[1][i][j] for i in range(4)), ZERO) for j in range(3)]
K = ([Y[1][i] + [-x for x in Y[2][i]] + [ZERO] * 3 for i in range(5)] +
     [Y[1][i] + [ZERO] * 3 + [-x for x in Y[5][i]] for i in range(5)] +
     [ell + [ZERO] * 6])
DB = det(Y[2][:3])
DH = det([Y[1][i] + Y[5][i] for i in range(5)] + [ell + [ZERO] * 3])
Dhat = -DB * DH
expected = json.loads((HERE / 'input_data' / 'prior_independent_polynomials.json').read_text())
polys = {'Delta': Delta, 'T': T, 'V': Vcoef, 'M': L[7], 'DB': DB, 'DH': DH, 'Dhat': Dhat}
for name, poly in polys.items():
    assert poly == parse_record(expected[name]), name
print('Independently rebuilt generators and inherited factors match exactly.', flush=True)

# Reconstruct the spectral-tail coordinates directly from its first three terms.
tail_basis = [[z**((r * k) % 8) for r in (1, 2, 3)] for k in (3, 4, 5)]
tail_denom = det(tail_basis)
tail_numerators = []
for j in range(3):
    replaced = [[L[k] if col == j else tail_basis[row][col] for col in range(3)]
                for row, k in enumerate((3, 4, 5))]
    tail_numerators.append(det(replaced))
assert tail_denom
for k in range(3, 8):
    assert tail_denom * L[k] == sum((tail_numerators[r - 1] * z**((r * k) % 8) for r in (1, 2, 3)), ZERO)

V = [[z**((i * j) % 8) for j in range(3)] for i in range(5)]
subspace_checks = 0
for j in (1, 2):
    for col in range(3):
        for rows in combinations(range(5), 4):
            assert not det([V[i] + [Y[j][i][col]] for i in rows])
            subspace_checks += 1
vd0 = det(V[:3])
minor_data = []
for rows in combinations(range(5), 3):
    vd = det([V[i] for i in rows])
    yd = det([Y[2][i] for i in rows])
    assert vd and yd and yd * vd0 == DB * vd
    minor_data.append({'top_rows': list(rows), 'vandermonde': scalar_coefficients(vd)})
print('All 30 subspace determinants and 10 Plucker identities pass.', flush=True)

zero_minors, nonzero_minors = [], []
for rows in combinations(range(11), 9):
    determinant = det([K[i] for i in rows])
    allowed = set(range(5, 11)).issubset(rows) and len(set(rows).intersection(range(5))) == 3
    if allowed:
        top_rows = [i for i in rows if i < 5]
        target = -det([Y[2][i] for i in top_rows]) * DH
        assert determinant == target and determinant
        assert determinant * vd0 == Dhat * det([V[i] for i in top_rows])
        nonzero_minors.append(list(rows))
    else:
        assert not determinant, rows
        zero_minors.append(list(rows))
assert len(zero_minors) == 45 and len(nonzero_minors) == 10
print('All 55 maximal minors independently computed: 45 zero, 10 proportional.', flush=True)

S = [[ZERO for _ in range(5)] for _ in range(5)]
for mon, coefficient in DB.items():
    indices = [j for j, exponent in enumerate(mon) for _ in range(exponent)]
    assert 1 <= len(indices) <= 2
    if len(indices) == 1:
        indices.append(4)
    i, j = indices
    value = R.ground_new(coefficient)
    if i == j:
        S[i][i] += value
    else:
        S[i][j] += value / 2
        S[j][i] += value / 2
four_minor = det([row[:4] for row in S[:4]])
assert four_minor and not det(S)
assert all(not S[i][j] for i in (2, 3, 4) for j in (2, 3, 4))
matrix_mod = [[reduce_mod(v, 12289, 8246) for v in row] for row in S]
assert reduce_mod(four_minor, 12289, 8246) == 11251
certificate = json.loads((HERE / 'input_data' / 'COLLAPSE_CERTIFICATE.json').read_text())
assert matrix_mod == certificate['DB_irreducibility']['homogeneous_quadratic_form_matrix']
assert [r['vandermonde'] for r in minor_data] == [[str(v) for v in r[1]] for r in certificate['exact_gate_collapse']['vandermonde_constants']]
print('Quadric matrix has exact rank four; modular minor 11251 reproduced.', flush=True)

# Small useful refinement: its unique projective singular point is affine
# and lies on h0=h1=0, outside the inherited regular h0!=0 chart.
Bdet = S[0][2] * S[1][3] - S[0][3] * S[1][2]
assert Bdet and four_minor == Bdet**2
vertex_h2 = (-S[0][4] * S[1][3] + S[0][3] * S[1][4]) / Bdet
vertex_h6 = (-S[0][2] * S[1][4] + S[0][4] * S[1][2]) / Bdet
vertex = [ZERO, ZERO, vertex_h2, vertex_h6, ONE]
assert all(not sum((S[i][j] * vertex[j] for j in range(5)), ZERO) for i in range(5))

# Record the actual proportionality constants, not only cross products.
for entry in minor_data:
    rows = entry['top_rows']
    entry['minor_ratio_to_selected'] = scalar_coefficients(det([V[i] for i in rows]) / vd0)

result = {
    'uploaded_code_executed': False,
    'arithmetic': 'Q[z]/(z^4+1)[h0,h1,h2,h6]; all reconstructed polynomial coefficients integral',
    'independent_reconstruction_matches': {name: {'terms': len(poly), 'degree': max(map(sum, poly), default=0)} for name, poly in polys.items()},
    'tail_recurrence_identities': 2,
    'spectral_tail_coordinate_identities': 5,
    'subspace_determinants': subspace_checks,
    'plucker_identities': len(minor_data),
    'zero_maximal_minors': zero_minors,
    'nonzero_proportional_maximal_minors': nonzero_minors,
    'vandermonde_constants': minor_data,
    'homogeneous_DB_matrix_exact': [[scalar_coefficients(v) for v in row] for row in S],
    'homogeneous_DB_matrix_mod12289': matrix_mod,
    'upper_left_4x4_minor_exact': scalar_coefficients(four_minor),
    'upper_left_4x4_minor_mod12289': 11251,
    'homogeneous_DB_rank_over_Qz_and_C': 4,
    'unique_affine_singular_point': {'h0': ['0'] * 4, 'h1': ['0'] * 4,
                                    'h2': scalar_coefficients(vertex_h2),
                                    'h6': scalar_coefficients(vertex_h6)},
    'DB_smooth_on_h0_nonzero_chart': True,
    'elapsed_seconds': round(time.monotonic() - started, 3),
}
(HERE / 'symbolic_results.json').write_text(json.dumps(result, indent=2) + '\n')
(HERE / 'reconstructed_polynomials.json').write_text(json.dumps({name: record(poly) for name, poly in polys.items()}, indent=2) + '\n')
print(json.dumps({k: v for k, v in result.items() if k in ('elapsed_seconds', 'homogeneous_DB_rank_over_Qz_and_C')}, indent=2), flush=True)
