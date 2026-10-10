"""Fresh Phase 21 audit controls. Never imports or executes submitted source.

Run from any directory with Python 3.10+. Only the standard library is used.
Selected arithmetic-count data are read for comparisons; archive provenance is separate.
Transforms here use a fresh decimation-in-frequency construction, including
small-radix direct butterflies, rather than the submission's DIT butterflies.
"""
from pathlib import Path
import itertools
import json
import math
import random

BASE = Path(__file__).resolve().parent


def factors(n):
    ans = []
    d = 2
    while d * d <= n:
        if n % d == 0:
            ans.append(d)
            while n % d == 0:
                n //= d
        d += 1
    if n > 1:
        ans.append(n)
    return ans


def prime(n):
    return n >= 2 and all(n % d for d in range(2, math.isqrt(n) + 1))


def exact_order(x, length, p):
    return pow(x, length, p) == 1 and all(
        pow(x, length // d, p) != 1 for d in factors(length))


def root(length, p):
    assert prime(p) and (p - 1) % length == 0
    for x in range(2, p):
        y = pow(x, (p - 1) // length, p)
        if exact_order(y, length, p):
            return y
    raise AssertionError("No root found")


def field(n):
    for m in itertools.count(1):
        p = 2 * n * m + 1
        if prime(p):
            return p, root(2 * n, p)


def powers(x, length, p):
    ans = [1]
    for _ in range(length - 1):
        ans.append(ans[-1] * x % p)
    return ans


def direct_values(a, eta, p, indices=None):
    if indices is None:
        indices = range(2 * len(a))
    # Independent monomial summation, not recurrence or Horner.
    return [sum(c * pow(eta, j * t, p) for t, c in enumerate(a)) % p
            for j in indices]


def coefficients(n, eta, p):
    q = pow(eta, 8, p)
    phi = [1]
    for t in range(1, n):
        phi.append(phi[-1] * (1 - pow(q, t, p)) % p)
    return [pow(q, (t * t * pow(4, -1, n)) % n, p) *
            pow(phi[t], -1, p) % p for t in range(n)]


def recurrence_values(a, eta, p, residual=True):
    """Fresh implementation from the polynomial identity with I/O counters."""
    n = len(a)
    assert n >= 3 and n % 2 and prime(p) and exact_order(eta, 2 * n, p)
    L = 2 * n
    ep = powers(eta, L, p)
    defects = []
    read_count = 0
    for t in range(1, n):
        d = ((1 - ep[8 * t % L]) * a[t] - ep[(4 * t - 2) % L] * a[t - 1]) % p
        read_count += 2
        if d:
            defects.append((t, d))
    forcing = [0] * L
    if residual:
        for t, d in defects:
            term = d
            for j in range(L):
                forcing[j] = (forcing[j] + term) % p
                term = term * ep[t] % p
    y = [None] * L
    writes = [0] * L
    for parity in range(2):
        orbit = [(parity + 4 * j) % L for j in range(n)]
        assert len(set(orbit)) == n
        for index in orbit[:2]:
            val = a[-1]
            read_count += 1
            for coefficient in a[-2::-1]:
                val = (val * ep[index] + coefficient) % p
                read_count += 1
            y[index] = val
            writes[index] += 1
        boundary = a[-1] * ep[-2] % p
        read_count += 1
        if parity:
            boundary = -boundary % p
        for j in range(n - 2):
            k, next_k, last_k = orbit[j:j + 3]
            y[last_k] = (y[k] - ep[(k + 2) % L] * y[next_k] + boundary - forcing[k]) % p
            writes[last_k] += 1
    assert set(writes) == {1}
    # Also check the closing equations, which were not used to propagate.
    for k in range(L):
        assert (y[(k + 8) % L] - y[k] + ep[(k + 2) % L] * y[(k + 4) % L]
                - ep[(n * k - 2) % L] * a[-1] + forcing[k]) % p == 0
    return y, defects, {"raw_coefficient_reads": read_count, "output_writes": sum(writes)}


def dif_transform(a, omega, p):
    """Direct-butterfly mixed-radix decimation in frequency, fresh code."""
    size = len(a)
    if size == 1:
        return [a[0] % p]
    radix = factors(size)[0]
    width = size // radix
    little_root = pow(omega, width, p)
    tw = powers(omega, size, p)
    small = [[pow(little_root, s * k, p) for s in range(radix)]
             for k in range(radix)]
    out = [0] * size
    for k in range(radix):
        block = [sum(a[j + width * s] * small[k][s]
                     for s in range(radix)) * tw[j * k % size] % p
                 for j in range(width)]
        transformed = dif_transform(block, pow(omega, radix, p), p)
        for j, v in enumerate(transformed):
            out[k + radix * j] = v
    return out


def radix2_dif(a, omega, p):
    """Independent in-place radix-2 DIF; final bit reversal restores order."""
    a = list(a)
    size = len(a)
    assert size & (size - 1) == 0
    roots = powers(omega, size, p)
    span = size
    while span >= 2:
        half = span // 2
        for start in range(0, size, span):
            for j in range(half):
                u, v = a[start + j], a[start + j + half]
                a[start + j] = (u + v) % p
                a[start + j + half] = (u - v) * roots[j * size // span] % p
        span = half
    bits = size.bit_length() - 1
    return [a[int(format(j, '0%db' % bits)[::-1], 2)] for j in range(size)]


def convolution(a, b, root_value, p, length, transform, spectrum=None):
    fa = transform(a + [0] * (length - len(a)), root_value, p) if spectrum is None else spectrum
    fb = transform(b + [0] * (length - len(b)), root_value, p)
    out = transform([u * v % p for u, v in zip(fa, fb)], pow(root_value, -1, p), p)
    return [v * pow(length, -1, p) % p for v in out]


def chart_data(n, q, p, alpha=2, beta=3):
    phi = [1]
    for t in range(1, n):
        phi.append(phi[-1] * (1 - pow(q, t, p)) % p)
    delta = (1 - pow(alpha, n, p) - pow(beta, n, p)) % p
    gamma = sum(pow(q, -t * t, p) for t in range(n)) * pow(n, -1, p) % p
    assert delta and gamma
    A = [delta * gamma * phi[t] * pow(alpha, -t, p) % p for t in range(n)]
    B = [phi[t] * pow(beta, -t, p) % p for t in range(n)]
    h = [pow(q, (t * t * pow(4, -1, n)) % n, p) * pow(phi[t], -1, p) % p for t in range(n)]
    return A, B, h


def power_count(k):
    return k.bit_length() - 1 + k.bit_count() if k else 0


def validation_count(order):
    return power_count(order) + sum(power_count(order // d) for d in factors(order))


def counts(n):
    m, z = 0, n
    while z % 3 == 0:
        m += 1
        z //= 3
    assert z == 1
    P = 1 << (2 * n - 2).bit_length()
    common = 13 * n + 7 + validation_count(2 * n) + 2 * power_count(n)
    kernel = 14 * n - 17
    fft = 3 * n + 20 * n * m // 3
    online = 2 * fft + 5 * n
    p_common = P + 12 * n + 3 + validation_count(n) + validation_count(P) + 2 * power_count(n)
    p_fft = 3 * P * (P.bit_length() - 1) // 2
    p_total = p_common + 3 * p_fft + P + 3 * n
    return dict(n=n, common_fast=common, spectrum_recurrence=kernel,
                spectrum_mixed_ntt=fft, online_fast=online,
                fast_total=common + kernel + online,
                three_mixed_ntt_total=common + fft + online,
                three_radix2_ntt_total=p_total,
                omitted_executable_negations=n - 1,
                fast_with_executable_negations=common + kernel + online + n - 1,
                mixed_with_executable_negations=common + fft + online + n - 1,
                fast_with_one_cached_negation=common + kernel + online + 1,
                fast_with_inverse_output_swap=common + kernel + online,
                power2_common=p_common, power2_fft=p_fft)


def main():
    report = {"source_programs_executed_or_imported": False, "failures": [],
              "kernel_cases": [], "sparse_cases": [], "chart_cases": [],
              "operation_table": [], "negative_controls": {}, "exhaustive": {}}
    submitted = json.loads((BASE / 'data/OPERATION_TABLE.json').read_text())
    for old in submitted['operation_table']:
        c = counts(old['n'])
        for key in ['common_fast', 'spectrum_recurrence', 'spectrum_mixed_ntt',
                    'online_fast', 'fast_total', 'three_mixed_ntt_total', 'three_radix2_ntt_total']:
            assert c[key] == old[key], (old['n'], key, c[key], old[key])
        report['operation_table'].append(c)

    bins = 0
    for n in [3, 5, 7, 9, 11, 13, 15, 17, 21, 25, 27, 33, 49, 81, 125, 243]:
        p, eta = field(n)
        tested = []
        for exponent in [1, -1]:
            e = pow(eta, exponent, p)
            h = coefficients(n, e, p)
            actual, ds, io = recurrence_values(h, e, p)
            assert not ds
            expected = direct_values(h, e, p)
            assert actual == expected
            assert actual == dif_transform(h + [0] * n, e, p)
            tested.append(exponent)
            bins += 2 * n
        report['kernel_cases'].append(dict(n=n, p=p, root_exponents=tested, bins=4*n, io=io))
    report['kernel_direct_bins'] = bins

    rng = random.Random(20261010)
    sparse_bins = 0
    for n in [3, 5, 9, 15, 27, 81, 243, 729, 6561]:
        p, eta = field(n)
        for wanted in range(min(3, n - 1) + 1):
            positions = rng.sample(range(1, n), wanted)
            defects = {t: rng.randrange(1, p) for t in positions}
            # Allow zero initial value, including the all-zero input.
            a = [0 if wanted % 2 == 0 else rng.randrange(1, p)]
            for t in range(1, n):
                a.append((pow(eta, 4*t-2, p)*a[-1] + defects.get(t, 0)) *
                         pow(1-pow(eta, 8*t, p), -1, p) % p)
            y, detected, io = recurrence_values(a, eta, p)
            assert dict(detected) == defects
            assert y == dif_transform(a + [0] * n, eta, p)
            if n <= 81:
                assert y == direct_values(a, eta, p)
            sparse_bins += 2 * n
            report['sparse_cases'].append(dict(n=n, p=p, defects=wanted, bins=2*n, io=io,
                submitted_online_field_count=20*n-25+6*wanted*n))
    report['sparse_full_bins'] = sparse_bins

    p, eta = 7, root(6, 7)
    for a in itertools.product(range(p), repeat=3):
        y, _, _ = recurrence_values(a, eta, p)
        assert y == direct_values(a, eta, p)
    report['exhaustive'] = dict(n=3, p=7, raw_inputs=343, full_bins=2058)

    # A residual-free recurrence applied to an arbitrary input must fail.
    n, p, eta = 9, 19, root(18, 19)
    a = [0, 1] + [0] * 7
    try:
        recurrence_values(a, eta, p, residual=False)
        raise AssertionError('Missing residual was not detected')
    except AssertionError:
        # Explicit reconstruction without closure assertions isolates mismatch.
        ep = powers(eta, 18, p)
        wrong = [None] * 18
        for parity in (0, 1):
            wrong[parity] = ep[parity]
            wrong[(parity + 4) % 18] = ep[(parity + 4) % 18]
            for j in range(n - 2):
                k = (parity + 4*j) % 18
                wrong[(k+8)%18] = (wrong[k]-ep[(k+2)%18]*wrong[(k+4)%18]) % p
        assert wrong != direct_values(a, eta, p)
        report['negative_controls']['omitting_residual_changes_bins'] = sum(x != y for x,y in zip(wrong, direct_values(a, eta, p)))

    for invalid_n, p, eta in [(2, 5, 2), (4, 17, 2), (9, 19, 1), (9, 19, 4)]:
        valid = invalid_n >= 3 and invalid_n % 2 and prime(p) and exact_order(eta, 2*invalid_n, p)
        assert not valid
    report['negative_controls']['invalid_length_or_root_rejections'] = 4
    # Swapping the two center +/- asym outputs removes the uncharged negation
    # without adding a field operation. Check both expressions directly.
    for p in (7, 19, 109):
        for _ in range(100):
            center, scalar, difference = [rng.randrange(p) for _ in range(3)]
            negative_asym = (-scalar % p) * difference % p
            positive_asym = scalar * difference % p
            assert ((center + negative_asym) % p, (center - negative_asym) % p) == (
                (center - positive_asym) % p, (center + positive_asym) % p)
    report['negative_controls']['inverse_output_swap_identity_cases'] = 300
    report['fallback_radix_examples'] = [dict(n=n, top_radix=2, remaining_radix=n,
        direct_remaining_butterfly_field_ops=4*n*n,
        whole_forward_field_ops=4*n*n+3*n) for n in (5, 25, 125)]
    composite_examples = []
    for eta in range(2, 91):
        if exact_order(eta, 6, 91) and math.gcd(1 - pow(eta, 8, 91), 91) > 1:
            composite_examples.append(dict(n=3, modulus=91, eta=eta,
                q=pow(eta, 8, 91), denominator_gcd=math.gcd(1-pow(eta,8,91),91)))
            break
    assert composite_examples
    report['negative_controls']['composite_modulus_passes_order_only_test'] = composite_examples[0]

    for old in submitted['operation_table']:
        n, p = old['n'], old['p']
        eta = root(2*n, p)
        q = pow(eta, 8, p)
        P = 1 << (2*n-2).bit_length()
        psi = root(P, p)
        alpha, beta = next((a,b) for a,b in [(2,3),(3,4),(5,7),(7,11)]
                          if (1-pow(a,n,p)-pow(b,n,p))%p)
        A, B, h = chart_data(n,q,p,alpha,beta)
        x = [rng.randrange(p) for _ in range(n)]
        v = [B[j] * x[j] % p for j in range(n)][::-1]
        hs, _, _ = recurrence_values(h,eta,p)
        c_rec = convolution(h,v,eta,p,2*n,dif_transform,hs)
        c_plain = convolution(h,v,eta,p,2*n,dif_transform)
        c_power = convolution(h,v,psi,p,P,radix2_dif)
        assert c_rec == c_plain
        assert c_rec[:2*n-1] == c_power[:2*n-1]
        if n <= 243:
            rows = list(range(n))
        else:
            chosen_rows = {0, 1, n - 2, n - 1}
            while len(chosen_rows) < 20:
                chosen_rows.add(rng.randrange(n))
            rows = sorted(chosen_rows)
        for j in rows:
            direct = A[j] * sum(h[j+t]*B[t]*x[t] for t in range(n-j)) % p
            assert direct == A[j]*c_rec[n-1+j]%p
        report['chart_cases'].append(dict(n=n,p=p,eta=eta,q=q,psi=psi,
            alpha=alpha,beta=beta,full_convolution_coefficients_checked=2*n-1,
            chart_output_coordinates_checked=n,direct_rows=len(rows)))
        if n == 6561:
            a = [rng.randrange(p) for _ in range(n)]
            y, ds, io = recurrence_values(a,eta,p)
            reference = dif_transform(a+[0]*n,eta,p)
            assert y == reference
            assert len(ds) > 3
            report['dense_case'] = dict(n=n,p=p,defects=len(ds),bins=len(y),
                forced_recurrence_matches=True,default_backend='ordinary mixed-radix NTT',
                detection_field_ops=4*(n-1),source_ntt_field_ops=old['spectrum_mixed_ntt'])
    out = BASE / 'INDEPENDENT_RESULTS.json'
    out.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ['kernel_direct_bins','sparse_full_bins','exhaustive','negative_controls','dense_case','operation_table']},indent=2))
    print('PASS: fresh independent controls; no submitted program executed or imported')


if __name__ == '__main__':
    main()
