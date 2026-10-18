"""New independent rational audit, 17 October 2026.

The oracle functions do not call any production numerical helper. They use a
different pi identity, interval Horner polynomial, isqrt with exact squares,
Fraction endpoint powers, and rational complex-distance certificates.
"""
from fractions import Fraction as F
from dataclasses import asdict
from math import factorial, isqrt
from pathlib import Path
import ast
import hashlib
import json

B = 840
UNIT = 1 << B
PI_TERMS = 500
SIN_TERMS = 128
PAIR_LIST = ((0, 0), (1 << 53, (1 << 55) + 1), (0, 1710))
N, M, D = (1 << 55) - 1, 1 << 57, 5
EXPECTED_SOURCE = '73b3bb0bebf41f7a810bf2470e9ae520bdc3e7593516850d8933dd307500091e'


def down(x):
    return x.numerator // x.denominator


def up(x):
    return -((-x.numerator) // x.denominator)


def enclosure(lo, hi):
    assert lo <= hi
    return F(down(lo * UNIT), UNIT), F(up(hi * UNIT), UNIT)


def add(x, y):
    return enclosure(x[0] + y[0], x[1] + y[1])


def neg(x):
    return -x[1], -x[0]


def times(x, y):
    products = [a * b for a in x for b in y]
    return enclosure(min(products), max(products))


def divide(x, y):
    assert y[0] > 0
    return times(x, (1 / y[1], 1 / y[0]))


def point(x):
    return F(x), F(x)


def atan_unit(v):
    # Exact rational sum and the alternating-series first-omitted-term bound.
    total = sum((F((-1) ** j, (2 * j + 1) * v ** (2 * j + 1))
                 for j in range(PI_TERMS)), F(0))
    omitted = F((-1) ** PI_TERMS,
                (2 * PI_TERMS + 1) * v ** (2 * PI_TERMS + 1))
    return min(total, total + omitted), max(total, total + omitted)


def make_pi():
    # atan(1/2)+atan(1/3)=pi/4 by the tangent addition formula and range.
    a, b = atan_unit(2), atan_unit(3)
    return enclosure(4 * (a[0] + b[0]), 4 * (a[1] + b[1]))


def sine(rational_turns, pi):
    # Fold a Fraction modulo two rather than using production numerator logic.
    r = rational_turns % 2
    sign = 1
    if r > 1:
        sign, r = -1, 2 - r
    if r > F(1, 2):
        r = 1 - r
    if r == 0:
        return point(0)
    if r == F(1, 2):
        return point(sign)
    x = times(pi, point(r))
    assert 0 <= x[0] <= x[1] <= 2
    square = times(x, x)
    # Horner evaluation of x * sum (-1)^j*x^(2j)/(2j+1)! on the entire
    # angle interval. No point midpoint, forward-term recurrence or Lipschitz
    # angle widening from the production implementation is used.
    poly = point(F((-1) ** (SIN_TERMS - 1), factorial(2 * SIN_TERMS - 1)))
    for j in reversed(range(SIN_TERMS - 1)):
        poly = add(times(poly, square), point(F((-1) ** j, factorial(2 * j + 1))))
    val = times(x, poly)
    tail = F(2 ** (2 * SIN_TERMS + 1), factorial(2 * SIN_TERMS + 1))
    assert tail < F(1, UNIT)
    val = enclosure(val[0] - tail, val[1] + tail)
    return val if sign > 0 else neg(val)


def independent_root(n, m):
    z = isqrt((m * UNIT * UNIT) // n)
    assert z * z * n <= m * UNIT * UNIT < (z + 1) * (z + 1) * n
    return F(z, UNIT), F(z + 1, UNIT)


def integer_power(x, exponent):
    values = [v ** exponent for v in x]
    if exponent % 2 == 0 and x[0] <= 0 <= x[1]:
        values.append(F(0))
    return enclosure(min(values), max(values))


def coefficient(ell, k, pi, root):
    m = M.bit_length() - 1
    s = D * m
    L, q = M // 4, M // (8 * s)
    u = (F(ell, N) - F(k, M)) % 1
    if u == 0:
        den = None
        first, ratio = point(F(2 * L + 1, M)), point(1)
    else:
        den = sine(u, pi)
        assert den[0] > 0
        first = divide(sine((2 * L + 1) * u, pi), times(point(M), den))
        ratio = divide(sine((2 * q + 1) * u, pi), times(point(2 * q + 1), den))
    powered = integer_power(ratio, s)
    amplitude = times(times(first, powered), root)
    a0 = (N - 1) // 2
    theta = F(2 * a0 * ell, N)
    real = times(amplitude, sine(F(1, 2) - theta, pi))
    imag = times(amplitude, sine(-theta, pi))
    return dict(real=real, imag=imag, F=first, R=ratio,
                powered_R=powered, denominator=den, u=u)


def encode_interval(x):
    if x is None:
        return None
    return dict(lo=down(x[0] * UNIT), hi=up(x[1] * UNIT), bits=B)


def as_fraction(x):
    return F(x.lo, 1 << x.bits), F(x.hi, 1 << x.bits)


def check_contained(oracle, produced):
    outer = as_fraction(produced)
    assert outer[0] <= oracle[0] <= oracle[1] <= outer[1]


def rational_json(x):
    return {'numerator': x.numerator, 'denominator': x.denominator}


def source_structure(source):
    tree = ast.parse(source)
    loops = []
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.For, ast.While, ast.comprehension)):
            loops.append({'line': getattr(node, 'lineno', None),
                          'kind': type(node).__name__,
                          'control': ast.unparse(node.iter if isinstance(node, (ast.For, ast.comprehension)) else node.test)})
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(ast.unparse(node))
    return {'imports': imports, 'loops': loops}


def budget_checks():
    m, s = 57, 285
    J, K, p, A = 587, 623, 459, 456
    eps, delta, eta = F(1, 1 << J), F(1, 1 << K), F(1, 1 << A)
    Q = N * M
    w0 = 4 * Q * eps + 2 * delta
    wC = 3 * (s + 1) * w0 + 3 * eps + 17 * delta
    coarse = 4 * (s + 1) * M * M * eps
    assert 64 * (K + 9) * delta <= eps < F(1, Q)
    assert F(2, Q) - eps > 0
    assert wC <= coarse <= eta / 64
    coordinate_radius = wC / 2 + F(1, 1 << (p + 1))
    assert 2 * coordinate_radius ** 2 < eta ** 2
    # Symbolic general proof is in REVIEW.md; this grid is supplementary.
    sample_count = 0
    for mm in range(2, 257):
        for dd in (5, 6, 7, 8, 16, 31, 64):
            ss = dd * mm
            jj = (dd + 5) * mm + ss.bit_length() + 8
            kk = jj + 2 * (jj + 1).bit_length() + 16
            aa = (dd + 3) * mm
            assert 64 * (kk + 9) <= 1 << (kk - jj)
            assert 256 * (ss + 1) <= 1 << (jj - aa - 2 * mm)
            sample_count += 1
    return {'J': J, 'K': K, 'p': p, 'A': A,
            'sine_width_over_epsilon': rational_json(64 * (K + 9) * delta / eps),
            'cartesian_width_over_eta': rational_json(wC / eta),
            'worst_radius_squared_over_eta_squared': rational_json(2 * coordinate_radius ** 2 / eta ** 2),
            'supplementary_parameter_cases': sample_count}


def main():
    source = Path('production_scalar.py').read_bytes()
    assert hashlib.sha256(source).hexdigest() == EXPECTED_SOURCE
    # Import only the byte-pinned fresh source after source review.
    from production_scalar import (CoefficientEngine, Paid, Interval, signed_power,
                                   nearest_even, rounded_certificate, CertificateError, DenseRequired)
    pi = make_pi()
    root = independent_root(N, M)
    oracle_records = [coefficient(ell, k, pi, root) for ell, k in PAIR_LIST]
    paid = Paid()
    engine = CoefficientEngine(N, M, D, paid)
    assert (engine.m, engine.s, engine.J, engine.K, engine.p) == (57, 285, 587, 623, 459)
    assert not engine.prepared and not paid.operations.get('pi_setup', 0)
    produced = [engine.coefficient(ell, k) for ell, k in PAIR_LIST]
    fresh_production_records = [asdict(record) for record in produced]
    author_dir = Path(__file__).resolve().parent / '../candidate'
    wrapper_dir = Path(__file__).resolve().parent / '../../q16_wrapper/candidate'
    wrapper_manifest = wrapper_dir / 'MANIFEST.json'
    wrapper_hash = hashlib.sha256(wrapper_manifest.read_bytes()).hexdigest()
    assert wrapper_hash == '234149beef4953463b73724c526e10c0b5bb9701e3bf9abbb13c334def2e6b34'
    wrapper_members = json.loads(wrapper_manifest.read_text())['files']
    for member, info in wrapper_members.items():
        data = (wrapper_dir / member).read_bytes()
        assert len(data) == info['bytes'] and hashlib.sha256(data).hexdigest() == info['sha256']
    author_records = json.loads((author_dir / 'RESULTS.json').read_text())['selected_results']
    wrapper_records = json.loads((wrapper_dir / 'RESULTS.json').read_text())['selected_coefficients']
    assert fresh_production_records == author_records == wrapper_records
    output_records = []
    for pair, oracle, prod in zip(PAIR_LIST, oracle_records, produced):
        for name, prod_name in [('real', 'real_enclosure'), ('imag', 'imag_enclosure'),
                                ('F', 'F'), ('R', 'R'), ('powered_R', 'powered_R')]:
            check_contained(oracle[name], getattr(prod, prod_name))
        if oracle['denominator'] is not None:
            check_contained(oracle['denominator'], prod.denominator)
        zr, zi = F(prod.real_integer, 1 << prod.p), F(prod.imag_integer, 1 << prod.p)
        distances = [max(abs(z - q[0]), abs(z - q[1]))
                     for z, q in ((zr, oracle['real']), (zi, oracle['imag']))]
        distance_squared = sum((r * r for r in distances), F(0))
        eta2 = F(1, 1 << (2 * engine.A))
        assert distance_squared <= eta2
        # Reconstruct the production rectangle certificate without production
        # arithmetic or rounding helpers, and independently minimize midpoint distance.
        radii = []
        for znum, rectangle in ((prod.real_integer, prod.real_enclosure),
                                (prod.imag_integer, prod.imag_enclosure)):
            left, right = as_fraction(rectangle)
            midgrid = (left + right) * F(1 << prod.p, 2)
            base = down(midgrid)
            chosen = min((base, base + 1), key=lambda v: (abs(v - midgrid), v % 2))
            assert chosen == znum
            lifted = znum * (1 << (prod.K - prod.p))
            radii.append(max(abs(lifted - rectangle.lo), abs(lifted - rectangle.hi)))
        lhs = sum(v * v for v in radii)
        rhs = 1 << (2 * (prod.K - engine.A))
        assert (tuple(radii), lhs, rhs) == ((prod.radius_real, prod.radius_imag), prod.radius_squared, prod.eta_squared_grid)
        assert lhs <= rhs
        output_records.append({'ell': pair[0], 'k': pair[1],
            'oracle_enclosures': {name: encode_interval(oracle[name]) for name in
                                   ('real', 'imag', 'F', 'R', 'powered_R', 'denominator')},
            'production_real_integer': prod.real_integer,
            'production_imag_integer': prod.imag_integer,
            'p': prod.p, 'production_K': prod.K,
            'oracle_contained_in_production': True,
            'oracle_error_squared_over_eta_squared': rational_json(distance_squared / eta2),
            'recomputed_radius_real': radii[0], 'recomputed_radius_imag': radii[1],
            'recomputed_radius_squared': lhs, 'eta_squared_grid': rhs})
    assert produced[0].residue == 0 and produced[0].denominator is None
    assert produced[1].residue == 1 and produced[1].denominator.lo > 0
    assert oracle_records[2]['R'][1] < 0 and oracle_records[2]['F'][1] < 0
    assert oracle_records[2]['powered_R'][1] < 0
    assert oracle_records[2]['real'][0] > 0
    assert produced[2].real_integer == produced[2].imag_integer == 0
    check_contained(pi, engine.scalar.pi)
    check_contained(root, engine.root)
    check_paid = Paid()
    U = 1 << 623
    sentinel = signed_power(Interval(-U // 2, -U // 4, 623), 285, check_paid)
    assert (sentinel.lo, sentinel.hi) == (-(1 << 338), -(1 << 53))
    sentinel_expected = integer_power((F(-1, 2), F(-1, 4)), 285)
    assert sentinel_expected == (F(-1, 1 << 285), F(-1, 1 << 570))
    power_cases = 0
    for bits in (3, 11, 19):
        unit = 1 << bits
        endpoints = (-unit, -unit + 1, -unit // 2, -1, 0, 1, unit // 3, unit - 1, unit)
        for i, lo in enumerate(endpoints):
            for hi in endpoints[i:]:
                for exponent in (1, 2, 3, 5, 8, 17, 32):
                    ans = signed_power(Interval(lo, hi, bits), exponent, check_paid)
                    possible = [F(lo, unit) ** exponent, F(hi, unit) ** exponent]
                    if exponent % 2 == 0 and lo <= 0 <= hi: possible.append(F(0))
                    assert ans.lo == down(min(possible) * unit)
                    assert ans.hi == up(max(possible) * unit)
                    power_cases += 1
    rounding_cases, tie_cases = 0, 0
    for denominator in (1, 2, 3, 4, 7, 16, 37):
        for numerator in range(-250, 251):
            exact = F(numerator, denominator)
            base = down(exact)
            expected = min((base, base + 1), key=lambda v: (abs(v - exact), v % 2))
            assert nearest_even(numerator, denominator, check_paid) == expected
            rounding_cases += 1
            tie_cases += 2 * (exact - base) == 1
    boundary = rounded_certificate(Interval(-16, 16, 8), Interval(0, 0, 8), 4, 4, check_paid)
    assert boundary[-2] == boundary[-1] == 256
    try:
        rounded_certificate(Interval(-17, 17, 8), Interval(0, 0, 8), 4, 4, check_paid)
    except CertificateError:
        pass
    else:
        raise AssertionError('strictly excessive radius passed')
    previous = paid.report()
    engine.prepare()
    after = paid.report()
    assert after['total_bit_work_upper'] > previous['total_bit_work_upper']
    assert paid.operations['pi_setup'] == paid.operations['sqrt_setup'] == 1
    assert paid.operations['atan_term'] == 1262 and paid.operations['sqrt_bisection'] == 625
    assert paid.operations['sine_taylor_term'] == 5040
    assert paid.operations['factorial_step'] == 10096
    assert engine.scalar.sine_calls == 12
    empty_paid = Paid()
    empty = CoefficientEngine(N, M, D, empty_paid)
    assert not empty.prepared
    assert empty_paid.report()['total_bit_work_upper'] > 0
    assert not empty_paid.operations.get('pi_setup', 0) and not empty_paid.operations.get('sqrt_setup', 0)
    dense_paid = Paid()
    dense = CoefficientEngine(1, 4, 5, dense_paid)
    try:
        dense.coefficient(0, 0)
    except DenseRequired:
        pass
    else:
        raise AssertionError('dense branch did not reject')
    assert not dense_paid.operations.get('pi_setup', 0) and not dense_paid.operations.get('sqrt_setup', 0)
    result = {
        'status': 'PASS_INDEPENDENT_NUMERIC_AND_SOURCE_REVIEW',
        'source_sha256': EXPECTED_SOURCE,
        'oracle': {'bits': B, 'pi_identity': '4*atan(1/2)+4*atan(1/3)',
                   'atan_terms_each': PI_TERMS, 'sine_horner_terms': SIN_TERMS,
                   'root_method': 'math.isqrt, verified by rational square inequalities',
                   'pi': encode_interval(pi), 'root': encode_interval(root)},
        'selected_coefficients': output_records,
        'fresh_production_records': fresh_production_records,
        'wrapper_numeric_equality': {
            'manifest_sha256': wrapper_hash,
            'results_sha256': hashlib.sha256((wrapper_dir / 'RESULTS.json').read_bytes()).hexdigest(),
            'verified_manifest_members': len(wrapper_members),
            'all_three_full_records_equal_fresh_scalar_run': True,
            'scope': 'Exact result and scalar-source equality only; independent producer provenance review remains separate.'},
        'sentinel': {'lo': sentinel.lo, 'hi': sentinel.hi, 'bits': 623, 'exponent': 285},
        'checks': {'selected_coefficients': 3, 'signed_power_fraction_cases': power_cases,
                   'nearest_even_cases': rounding_cases, 'exact_tie_cases': tie_cases,
                   'minimum_residue_one_positive': True, 'zero_residue_exact_branch': True,
                   'tiny_odd_witness_proved_positive_but_rounds_zero': True,
                   'boundary_certificate_equality_passes': True, 'excess_radius_rejected': True,
                   'pi_and_root_contained': True, 'empty_setup_lazy_and_header_paid': True,
                   'dense_setup_not_performed': True, 'prepare_reuse_paid_without_recompute': True,
                   'historical_source_executed': False},
        'error_budget': budget_checks(),
        'source_structure': source_structure(source),
        'production_ledger': after,
        'scope': 'Independent scalar/coefficient audit for three selected incidences plus generic primitive controls and source/proof review. Not full outer stream, recovery, scatter, all-length executable, or FFT speed evidence.'}
    Path('RESULTS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': result['status'], 'checks': result['checks']}, sort_keys=True))


if __name__ == '__main__':
    main()
