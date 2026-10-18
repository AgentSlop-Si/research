"""Fresh exact controls for rank-two rigidity and D_N^2<12N tilings.

No previous author/reviewer checker is imported or executed. All rank tests use
exact characteristic-zero cyclotomic arithmetic unless explicitly labeled as
a finite-field negative control. Finite tests supplement the written proof.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import hashlib
import json
import math
import sympy as sp
from sympy.polys.matrices import DomainMatrix

HERE = Path(__file__).resolve().parent
OUT = {'status': 'PASS', 'sympy_version': sp.__version__,
       'independence': 'Fresh checker, with no prior source/review checker imported or executed.'}


def divisors(n):
    small = [d for d in range(1, math.isqrt(n)+1) if n % d == 0]
    return sorted(set(small + [n//d for d in small]))


def constants(n):
    ds = divisors(n)
    D = min(d+n//d for d in ds)
    E = min(2*d+n//d for d in ds if d < n)
    assert E > D
    return ds, D, E


class Roots:
    def __init__(self, n):
        self.n = n
        self.K = sp.QQ.cyclotomic_field(n)
        z = self.K.from_sympy(self.K.ext)
        self.powers = [self.K.one]
        for _ in range(1, n):
            self.powers.append(self.powers[-1]*z)
        assert self.powers[-1]*z == self.K.one
        assert all(self.powers[n//p] != self.K.one for p in sp.factorint(n))

    def rank_exponents(self, exps):
        a, b = len(exps), len(exps[0])
        matrix = [[self.powers[e % self.n] for e in row] for row in exps]
        return int(DomainMatrix(matrix, (a, b), self.K).rank())


def projective_counts(exps, n):
    rows = {tuple((e-row[0]) % n for e in row) for row in exps}
    cols = {tuple((exps[i][j]-exps[0][j]) % n for i in range(len(exps)))
            for j in range(len(exps[0]))}
    return len(rows), len(cols)


def check_rigidity(exps, n, rank):
    a, b = len(exps), len(exps[0])
    rc, cc = projective_counts(exps, n)
    if rank == 1:
        assert (rc, cc) == (1, 1)
    if rank == 2:
        assert rc == 2 or cc == 2
        if rc == 2:
            assert a+2*b < 2*(a+b)
        if cc == 2:
            assert 2*a+b < 2*(a+b)
    return rc, cc


# Exhaustive exact Fourier rectangles at all N=2,...,7.
fourier_summary = {}
for n in range(2, 8):
    roots = Roots(n)
    ds, D, E = constants(n)
    subsets = [[j for j in range(n) if mask >> j & 1] for mask in range(1, 1 << n)]
    ranks = Counter()
    class_cases = Counter()
    rank_two_density_equalities = 0
    for R in subsets:
        for C in subsets:
            a, b = len(R), len(C)
            exps = [[(-k*j) % n for j in C] for k in R]
            r = roots.rank_exponents(exps)
            ranks[r] += 1
            rc, cc = check_rigidity(exps, n, r)
            assert a*b <= n*r
            if r == 2:
                assert n*2*(a+b) >= E*a*b > D*a*b
                if n*2*(a+b) == E*a*b:
                    rank_two_density_equalities += 1
                assert any((a <= 2*d and b <= n//d) or
                           (b <= 2*d and a <= n//d) for d in ds if d < n)
                class_cases['both' if rc == cc == 2 else 'rows' if rc == 2 else 'columns'] += 1
                if rc == 2:
                    h_gcd = math.gcd(n, *(j-C[0] for j in C))
                    # H has order N/gcd; K has order gcd.
                    assert len({k % (n//h_gcd) for k in R}) == 2
                    assert a <= 2*h_gcd and b <= n//h_gcd
                if cc == 2:
                    k_gcd = math.gcd(n, *(k-R[0] for k in R))
                    assert len({j % (n//k_gcd) for j in C}) == 2
                    assert b <= 2*k_gcd and a <= n//k_gcd
            if D*D < 12*n:
                gap = n*r*(a+b)-D*a*b
                assert gap >= 0
                if r >= 2:
                    assert gap > 0
                if gap == 0:
                    assert r == 1 and a*b == n and a+b == D
    assert rank_two_density_equalities > 0
    fourier_summary[n] = {'rectangles': len(subsets)**2,
                          'ranks': dict(sorted(ranks.items())),
                          'rank_two_projective_cases': dict(class_cases),
                          'rank_two_density_equalities': rank_two_density_equalities}
    print('exact Fourier', n, fourier_summary[n], flush=True)
OUT['exact_fourier_exhaustive'] = fourier_summary


# Non-Fourier tests: exhaustive normalized root-of-unity matrices.
# First row and first column are 1, with all remaining exponents independent.
generic_summary = {}
for q, a, b in [(4, 3, 3), (3, 3, 4), (5, 3, 3), (4, 4, 3)]:
    roots = Roots(q)
    ranks, cases = Counter(), Counter()
    for flat in product(range(q), repeat=(a-1)*(b-1)):
        exps = [[0]*b]
        for i in range(a-1):
            exps.append([0] + list(flat[i*(b-1):(i+1)*(b-1)]))
        r = roots.rank_exponents(exps)
        ranks[r] += 1
        rc, cc = check_rigidity(exps, q, r)
        if r == 2:
            cases['both' if rc == cc == 2 else 'rows' if rc == 2 else 'columns'] += 1
    key = f'{q}_roots_{a}x{b}'
    generic_summary[key] = {'matrices': q**((a-1)*(b-1)),
                            'ranks': dict(sorted(ranks.items())),
                            'rank_two_projective_cases': dict(cases)}
    print('exact generic', key, generic_summary[key], flush=True)
OUT['exact_non_fourier_exhaustive'] = generic_summary


# Integer-only envelope checks. A shape is checked as a relaxation,
# not mislabeled as an existing Fourier rectangle.
scalar = {'rank_two_maximum_N': 400, 'rank_two_divisor_envelope_shapes': 0,
          'higher_rank_maximum_N': 500, 'rank_at_least_three_shapes': 0,
          'balanced_lengths': 0}
for n in range(2, scalar['rank_two_maximum_N']+1):
    ds, D, E = constants(n)
    for d in ds[:-1]:
        for a in range(1, 2*d+1):
            for b in range(1, n//d+1):
                assert n*2*(a+b) >= E*a*b > D*a*b
                scalar['rank_two_divisor_envelope_shapes'] += 1
for n in range(2, scalar['higher_rank_maximum_N']+1):
    ds, D, E = constants(n)
    if D*D >= 12*n:
        continue
    scalar['balanced_lengths'] += 1
    for a in range(3, n+1):
        for b in range(a, n+1):
            r = max(3, (a*b+n-1)//n)
            if r <= a:
                assert n*r*(a+b) > D*a*b
                scalar['rank_at_least_three_shapes'] += 1
OUT['exact_scalar_controls'] = scalar
print('scalar controls', scalar, flush=True)


# Structured large-N rank certificates: equality of row directions is verified
# entrywise modulo N; a nonvanishing 2x2 minor proves the rank is exactly 2.
# This avoids substituting numerical SVD ranks for exact complex ranks.
large = {}
x = sp.Symbol('x')
for n, d, expected_D, expected_E, square_size in [(343, 7, 56, 63, 26), (847, 11, 88, 99, 41)]:
    ds, D, E = constants(n)
    assert (D, E) == (expected_D, expected_E)
    assert D*D < E*E < 12*n
    K = [t*(n//d) for t in range(d)]
    R = K + [1+t*(n//d) for t in range(d)]
    C = [s*d for s in range(n//d)]
    exps = [[(-k*j) % n for j in C] for k in R]
    rc, cc = projective_counts(exps, n)
    assert rc == 2
    minor_exponent = (-d) % n
    assert minor_exponent != 0
    cyclotomic = sp.Poly(sp.cyclotomic_poly(n, x), x, domain=sp.QQ)
    minor_remainder = sp.rem(sp.Poly(x**minor_exponent-1, x, domain=sp.QQ), cyclotomic)
    assert not minor_remainder.is_zero
    area, cost = len(R)*len(C), 2*(len(R)+len(C))
    assert area == 2*n and n*cost == E*area
    assert E-D == d and (E-D)*area == n*cost-D*area
    assert square_size**2 <= 2*n
    assert n*4*square_size < D*square_size**2
    assert not any(square_size <= 2*e and square_size <= n//e for e in ds[:-1])

    # Full disjoint target-optimal tiling and entry coverage.
    row_parts = [[u+t*(n//d) for t in range(d)] for u in range(n//d)]
    col_parts = [[v+s*d for s in range(n//d)] for v in range(d)]
    covered = bytearray(n*n)
    total_cost, tiles = 0, 0
    for A in row_parts:
        for B in col_parts:
            assert len(A)*len(B) == n and len(A)+len(B) == D
            assert all((k-A[0])*(j-B[0]) % n == 0 for k in A for j in B)
            for k in A:
                for j in B:
                    pos = k*n+j
                    assert covered[pos] == 0
                    covered[pos] = 1
            total_cost += len(A)+len(B)
            tiles += 1
    assert all(covered) and tiles == n and total_cost == n*D
    assert set(R) == set(row_parts[0]) | set(row_parts[1])
    assert C == col_parts[0]
    merged_cost = total_cost-2*D+cost
    assert merged_cost == total_cost+2*d
    assert n*(merged_cost-total_cost) == (E-D)*area
    large[n] = {
        'divisors': ds, 'D': D, 'E2': E, 'optimum': n*D,
        'higher_rank_density_penalty': str(sp.Rational(d, n)),
        'rank_two_example': {'rows': R, 'columns': C, 'actual_rank': 2,
             'rank_certificate': 'Exactly two projective row classes and a nonzero cyclotomic 2x2 minor.',
             'projective_row_classes': rc, 'projective_column_classes': cc,
             'minor_polynomial': f'x^{minor_exponent}-1',
             'minor_remainder_degree': int(minor_remainder.degree()),
             'shape': [len(R), len(C)], 'area': area, 'cost': cost},
        'excluded_relaxed_square_rank_two_shape': [square_size, square_size],
        'actual_rank_lower_bound_for_square_shape': 3,
        'optimal_partition': {'tiles': tiles, 'covered_entries': len(covered), 'cost': total_cost},
        'globally_sharp_penalty_tiling': {'rank_one_tiles': n-2, 'rank_two_tiles': 1,
            'higher_rank_area': area, 'total_cost': merged_cost, 'excess': 2*d}}
    print('large exact certificates', n, total_cost, 'tiles', tiles, flush=True)
OUT['large_target_controls'] = large


# A negative control over F_23: nonzero roots have no complex unit-circle
# geometry. The same exponent matrix has complex rank 3, field rank 2, and
# three projective row classes and column classes.
n, q, z = 11, 23, 2
R, C = [0, 1, 3], [0, 2, 7]
exps = [[(-k*j) % n for j in C] for k in R]
Kq = sp.GF(q)
M = [[Kq(pow(z, e, q)) for e in row] for row in exps]
finite_rank = int(DomainMatrix(M, (3, 3), Kq).rank())
complex_rank = Roots(n).rank_exponents(exps)
assert (finite_rank, complex_rank) == (2, 3)
assert projective_counts(exps, n) == (3, 3)
OUT['finite_field_negative_control'] = {'N': n, 'field': q, 'root': z,
    'rows': R, 'columns': C, 'finite_field_rank': finite_rank,
    'complex_rank': complex_rank, 'projective_row_classes': 3,
    'projective_column_classes': 3,
    'meaning': 'Rank-two unit-modulus rigidity is not a finite-field assertion.'}
print('finite field negative control passed', flush=True)


# Exact limit of the naive rank-three analogue. This unit-modulus matrix
# has rank 3 but four projective classes on both sides. It is not asserted
# to be a cyclic Fourier rectangle.
rank_three_exps = [[0, 2, 1, 3], [3, 0, 2, 1],
                  [1, 3, 0, 2], [2, 1, 3, 0]]
assert Roots(4).rank_exponents(rank_three_exps) == 3
assert projective_counts(rank_three_exps, 4) == (4, 4)
A = sp.Matrix([[sp.I**e for e in row] for row in rank_three_exps])
assert A.det() == 0 and A[:3, :3].det() == 2-2*sp.I
OUT['rank_three_naive_extension_negative_control'] = {
    'exponents_mod_4': rank_three_exps, 'complex_rank': 3,
    'projective_row_classes': 4, 'projective_column_classes': 4,
    'upper_left_3x3_determinant': '2-2i',
    'meaning': 'The at-most-r projective-class analogue is false for general unit-modulus rank-three matrices; no Fourier counterexample is asserted.'}
print('rank three naive extension negative control passed', flush=True)

censuses = {}
for maximum in [1000, 10000]:
    new, residual = [], []
    for n in range(2, maximum+1):
        ds, D, E = constants(n)
        p = max(sp.factorint(n))
        dominant = n//p < p
        old = D*D < 8*n or dominant
        current = D*D < 12*n or dominant
        if current and not old:
            new.append(n)
        if not current:
            residual.append(n)
    censuses[maximum] = {'new_lengths': new, 'new_count': len(new),
                        'residual_lengths': residual, 'residual_count': len(residual)}
assert censuses[1000]['new_lengths'] == [343, 847]
assert censuses[1000]['residual_lengths'] == []
assert censuses[10000]['new_count'] == 44
assert censuses[10000]['residual_count'] == 25
assert censuses[10000]['residual_lengths'][0] == 1331
OUT['finite_domain_censuses'] = censuses
print('census', {n: (c['new_count'], c['residual_count']) for n, c in censuses.items()}, flush=True)

# Confirm precisely which rank is the next obstruction at N=1331.
ds, D, E = constants(1331)
assert D == 132 and 12*1331 < D*D < 16*1331 and E > D
OUT['next_boundary'] = {'N': 1331, 'D': D, 'E2': E,
    'D_squared': D*D, '12N': 12*1331, '16N': 16*1331,
    'optimum_upper_bound': 1331*D, 'first_unresolved_tile_rank': 3,
    'status': 'Outside combined accepted and author-proved domains; no full optimum claimed.'}

paths = {
 'accepted_bounded_report': '../dependencies/accepted_bounded_report.md',
 'accepted_bounded_review': '../dependencies/accepted_bounded_review.md',
 'accepted_dominant_report': '../dependencies/accepted_dominant_report.md',
 'accepted_dominant_review': '../dependencies/accepted_dominant_review.md',
}
source_hashes = {}
for label, value in paths.items():
    path = HERE/value
    data = path.read_bytes()
    source_hashes[label] = {'path': value, 'bytes': len(data),
                            'sha256': hashlib.sha256(data).hexdigest()}
OUT['source_hashes'] = source_hashes
(HERE/'RESULTS.json').write_text(json.dumps(OUT, indent=2)+'\n')
(HERE/'SOURCES.json').write_text(json.dumps({
 'scope': 'Self-contained complex rank-two rigidity and D_N^2<12N extension; no external writes.',
 'new_mathematical_inputs': 'All new mathematical assertions are proved in REPORT.md; no new external theorem is used.',
 'accepted_local_dependencies': source_hashes,
 'external_search_note': 'A public keyword search did not identify a needed source; no search result is used as mathematical evidence.',
 'novelty_claim': 'None.'}, indent=2)+'\n')
print('ALL CONTROLS PASSED', flush=True)
