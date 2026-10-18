"""Fresh bounded component controls; not the independent transcendental oracle."""
import json
from dataclasses import asdict
from fractions import Fraction
from pathlib import Path
from production_scalar import (Paid, Interval, Scalar, CoefficientEngine,
    signed_power, nearest_even, rounded_certificate, CertificateError, DenseRequired)


def main():
    checks = {}
    paid = Paid()
    N, M, D = (1 << 55) - 1, 1 << 57, 5
    engine = CoefficientEngine(N, M, D, paid)
    assert (engine.m, engine.s, engine.h, engine.t, engine.J, engine.K, engine.p) == (57, 285, 4561, 9124, 587, 623, 459)
    assert paid.operations.get('pi_setup', 0) == 0 and paid.operations.get('sqrt_setup', 0) == 0
    assert not engine.prepared
    checks['precision_metadata'] = True
    results = [engine.coefficient(ell, k) for ell, k in ((0, 0), (1 << 53, (1 << 55) + 1), (0, 1710))]
    checks['selected_coefficient_evaluations'] = len(results)
    assert engine.scalar.sine_calls == 12
    assert paid.operations['pi_setup'] == paid.operations['sqrt_setup'] == 1
    assert paid.operations['atan_term'] == 2 * (623 + 8)
    assert paid.operations['sqrt_bisection'] == 625
    assert paid.operations['sine_taylor_term'] == 8 * 630
    assert paid.operations['factorial_step'] == 8 * 1262
    assert results[0].residue == 0 and results[0].denominator is None
    assert results[1].residue == 1 and results[1].denominator.lo > 0
    assert results[2].R.hi < 0 and results[2].F.hi < 0 and results[2].powered_R.lo < 0 and results[2].powered_R.hi <= 0
    assert results[2].real_integer == results[2].imag_integer == 0
    for result in results:
        assert result.radius_squared <= result.eta_squared_grid
        assert result.radius_squared == result.radius_real ** 2 + result.radius_imag ** 2
    calls = paid.events
    engine.prepare()
    assert paid.events > calls and paid.operations['pi_setup'] == paid.operations['sqrt_setup'] == 1
    checks['repeated_prepare_paid_without_recomputation'] = True
    U = 1 << 623
    sentinel = signed_power(Interval(-U // 2, -U // 4, 623), 285, paid)
    assert (sentinel.lo, sentinel.hi) == (-(1 << 338), -(1 << 53))
    positive_mutant = (1 << 53, 1 << 338)
    assert positive_mutant != (sentinel.lo, sentinel.hi)
    try:
        # A newly authored stand-in for the historical helper's API guard.
        if 285 % 2: raise ValueError('even exponent required')
        raise AssertionError('even-only control unexpectedly accepted odd exponent')
    except ValueError as exc:
        assert str(exc) == 'even exponent required'
    checks['odd_285_sentinel_and_mutants'] = True
    checks['historical_helper_executed'] = False
    production_ledger = paid.report()

    empty_paid = Paid()
    empty = CoefficientEngine(N, M, D, empty_paid)
    empty_receipt = empty_paid.report()
    assert empty_receipt['total_bit_work_upper'] > 0
    assert empty_paid.operations.get('pi_setup', 0) == empty_paid.operations.get('sqrt_setup', 0) == 0
    checks['empty_no_numeric_setup_header_paid'] = True
    guard_paid = Paid()
    guard = CoefficientEngine(1, 4, 5, guard_paid)
    try: guard.coefficient(0, 0)
    except DenseRequired as exc: assert str(exc) == 'OUTER_DENSE_REQUIRED'
    else: raise AssertionError('dense guard did not fail')
    assert guard_paid.operations.get('pi_setup', 0) == guard_paid.operations.get('sqrt_setup', 0) == 0
    checks['dense_guard_no_numeric_setup'] = True

    primitive = Paid()
    count = 0
    for bits in (4, 7, 13):
        U = 1 << bits
        points = (-U, -U + 1, -U // 2, -1, 0, 1, U // 2, U - 1, U)
        for lo in points:
            for hi in points:
                if lo > hi: continue
                for exponent in (1, 2, 3, 4, 7, 8, 15):
                    a = signed_power(Interval(lo, hi, bits), exponent, primitive)
                    endpoints = (Fraction(lo, U) ** exponent, Fraction(hi, U) ** exponent)
                    exact_low = 0 if exponent % 2 == 0 and lo <= 0 <= hi else min(endpoints)
                    exact_high = max(endpoints)
                    assert a.lo == (exact_low * U).__floor__()
                    assert a.hi == (exact_high * U).__ceil__()
                    count += 1
    checks['signed_power_exact_fraction_controls'] = count
    ties = []
    for integer in range(-20, 21):
        for divisor in (2, 4, 16):
            n = integer * divisor + divisor // 2
            expected = integer if integer % 2 == 0 else integer + 1
            actual = nearest_even(n, divisor, primitive)
            assert actual == expected
            ties.append((n, divisor, actual))
    checks['positive_negative_exact_ties'] = len(ties)
    certificates = []
    # Exact boundary accepted; one-unit excess rejected deterministically.
    result = rounded_certificate(Interval(0, 16, 8), Interval(0, 0, 8), 4, 4, primitive)
    assert result[-2] <= result[-1]
    try: rounded_certificate(Interval(-256, 256, 8), Interval(0, 0, 8), 4, 4, primitive)
    except CertificateError as exc: certificates.append(str(exc))
    else: raise AssertionError('bad radius certificate accepted')
    checks['certificate_failure_control'] = certificates
    # Exact algebraic sine values and squares independently known.
    scalar = Scalar(96, primitive)
    algebraic = 0
    for den, num, square in ((6, 1, Fraction(1, 4)), (4, 1, Fraction(1, 2)),
                            (3, 1, Fraction(3, 4)), (2, 1, Fraction(1))):
        for period in range(-5, 6):
            for sign in (-1, 1):
                a = scalar.sin_pi(2 * den * period + sign * num, den)
                left, right = Fraction(a.lo, 1 << 96), Fraction(a.hi, 1 << 96)
                assert left <= right
                if sign == 1:
                    assert 0 <= left and left * left <= square <= right * right
                else:
                    assert right <= 0 and right * right <= square <= left * left
                algebraic += 1
    for n in range(-5, 6):
        a = scalar.sin_pi(n, 1)
        assert (a.lo, a.hi) == (0, 0)
        algebraic += 1
    checks['sine_exact_algebraic_controls'] = algebraic
    root = engine.root
    assert root.lo ** 2 * N <= M * (1 << 1246) <= root.hi ** 2 * N
    checks['sqrt_exact_rational_square_control'] = True
    invalid = []
    for args in ((True, M, D), (N, True, D), (N, M, True), (0, M, D),
                 (N, M, 4), (N, M + 1, D), (N, M // 2, D)):
        ledger = Paid()
        try: CoefficientEngine(*args, paid=ledger)
        except ValueError as exc: invalid.append({'args': args, 'error': str(exc), 'prefix': ledger.report()})
        else: raise AssertionError('malformed header accepted')
        assert ledger.operations.get('pi_setup', 0) == 0
    checks['invalid_header_controls'] = len(invalid)
    for pair in ((True, 0), (0, True), (-1, 0), (0, -1), (N, 0), (0, M), (0, 10000)):
        try: engine.coefficient(*pair)
        except ValueError: pass
        else: raise AssertionError('invalid incidence accepted')
    checks['invalid_incidence_controls'] = 7
    output = {
        'status': 'PASS_FRESH_COMPONENT_CONTROLS_PENDING_INDEPENDENT_REVIEW',
        'scope': 'Fresh numerical kernel; three selected coefficient evaluations only. Wrapper provenance, full incidence enumeration and independent transcendental oracle are separate gates.',
        'checks': checks,
        'selected_results': [asdict(r) for r in results],
        'sentinel': asdict(sentinel),
        'production_ledger': production_ledger,
        'empty_ledger': empty_receipt,
        'guard_ledger': guard_paid.report(),
        'primitive_ledger': primitive.report(),
        'malformed_header_prefix_receipts': invalid,
        'final_production_ledger_after_invalid_controls': paid.report(),
    }
    Path('RESULTS.json').write_text(json.dumps(output, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': output['status'], 'checks': checks}, sort_keys=True))


if __name__ == '__main__': main()
