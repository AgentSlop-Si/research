"""Independent audit built for this synthesis. Never imports/runs archive code.
Only the supplied JSON witness data are loaded; no source code is imported.
"""
from pathlib import Path
from itertools import combinations_with_replacement, product
from fractions import Fraction as F
import hashlib, json

ROOT = Path(__file__).resolve().parent
DATA = ROOT/'source_certificate_data.json'
PRIME = 998244353


def prime_trial(n):
    if n % 2 == 0:
        return n == 2
    return all(n % d for d in range(3, 1 + __import__('math').isqrt(n), 2))


def det_fraction_free_mod(rows, p):
    """Bareiss recurrence evaluated in the prime field, with row pivoting."""
    a = [r[:] for r in rows]
    assert a and all(len(r) == len(a) for r in a)
    n = len(a)
    previous, sign = 1, 1
    for k in range(n - 1):
        pivot_row = next((i for i in range(k, n) if a[i][k]), None)
        if pivot_row is None:
            return 0
        if pivot_row != k:
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign *= -1
        pivot = a[k][k]
        inv_previous = pow(previous, -1, p)
        for i in range(k + 1, n):
            left = a[i][k]
            for j in range(k + 1, n):
                a[i][j] = (pivot * a[i][j] - left * a[k][j]) * inv_previous % p
            a[i][k] = 0
        previous = pivot
    return sign * a[-1][-1] % p


def certificate_check(data):
    results = []
    for key, source in data['conjugate_pair_cubic_certificates'].items():
        n = int(key)
        root = pow(3, (PRIME - 1) // n, PRIME)
        assert pow(root, n, PRIME) == 1 and pow(root, n // 2, PRIME) != 1
        known = [i for i in range(n) if i not in (1, n - 1)]
        monomials = [m for d in (1, 2, 3)
                     for m in combinations_with_replacement(known, d) if sum(m) % n == 1]
        supports = source['supports']
        assert len({tuple(s) for s in supports}) == len(supports)
        assert all(0 <= len(s) <= 3 and s == sorted(set(s)) and all(0 <= j < n for j in s)
                   for s in supports)
        assert len(supports) == len(monomials) + 1
        rows = []
        for support in supports:
            bins = [sum(pow(root, k*j, PRIME) for j in support) % PRIME for k in range(n)]
            row = []
            for monomial in monomials:
                value = 1
                for k in monomial:
                    value = value * bins[k] % PRIME
                row.append(value)
            rows.append(row + [bins[1]])
        determinant = det_fraction_free_mod(rows, PRIME)
        assert determinant != 0 and determinant == source['determinant_mod_998244353']
        results.append({'N': n, 'monomials': len(monomials), 'witness_rows': len(rows),
                        'primitive_root': root, 'determinant_mod_p': determinant,
                        'matches_supplied_determinant': True})
    return results


# Exact cyclotomic arithmetic for dyadic N: Z[z]/(z^(N/2)+1).
def zpower(k, half):
    k %= 2 * half
    return tuple((1 if k < half else -1) if i == k % half else 0 for i in range(half))


def add(a, b):
    return tuple(x + y for x, y in zip(a, b))


def scale(c, a):
    return tuple(c * x for x in a)


def mul(a, b):
    half = len(a)
    out = [0] * half
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            k = i + j
            out[k % half] += x * y * (1 if k < half else -1)
    return tuple(out)


def spectrum(x):
    n = len(x)
    out = []
    for k in range(n):
        s = (0,) * (n // 2)
        for j, bit in enumerate(x):
            if bit:
                s = add(s, zpower(k*j, n//2))
        out.append(s)
    return out


def cubic_control():
    count = 0
    for bits in product((0, 1), repeat=8):
        x = spectrum(bits)
        q = add(add(mul(x[1], x[6]), mul(x[2], x[5])), mul(x[3], x[4]))
        r = add(add(mul(mul(x[1], x[1]), x[5]), mul(x[1], mul(x[3], x[3]))),
                mul(mul(x[2], x[2]), x[3]))
        rhs = add(scale(-1, mul(add(x[0], (-4, 0, 0, 0)), q)), scale(-1, r))
        rhs = add(rhs, scale(-2, mul(mul(x[1], x[2]), x[4])))
        assert scale(4, x[7]) == rhs
        count += 1
    return {'N': 8, 'all_binary_inputs_verified': count, 'ring': 'Z[z]/(z^4+1)'}


def ambiguity_controls():
    out = []
    for n in (8, 16):
        half = n//2
        even_spectra, odd_spectra = set(), set()
        for u in product((0, 1), repeat=half):
            bits = u + tuple(1-b for b in u)
            x = spectrum(bits)
            even_spectra.add(tuple(x[::2]))
            odd_spectra.add(tuple(x[1::2]))
            expected = ((half,) + (0,) * (half-1),) + ((0,) * half,) * (half-1)
            assert tuple(x[::2]) == expected
        assert len(even_spectra) == 1 and len(odd_spectra) == 2**half
        out.append({'N': n, 'inputs': 2**half, 'distinct_even_spectra': 1,
                    'distinct_odd_spectra': len(odd_spectra)})
    return out


def lagrange_coeffs(omit, coordinate):
    coefs = [F(0)] * 3
    for t in range(4):
        if t == omit:
            continue
        value = F((t % 2) if coordinate == 0 else (t // 2))
        others = [u for u in range(4) if u not in (omit, t)]
        a, b = others
        denom = (t-a)*(t-b)
        for degree, c in enumerate((a*b, -a-b, 1)):
            coefs[degree] += value*c/denom
    return coefs


def sharp_quadratic_gate():
    results = []
    successes = [0] * 4
    for omitted in range(4):
        polys = [lagrange_coeffs(omitted, j) for j in (0, 1)]
        mask = []
        for t in range(4):
            pair = tuple(sum(c * t**k for k, c in enumerate(poly)) for poly in polys)
            correct = pair == (t % 2, t // 2)
            assert correct == (t != omitted)
            successes[t] += correct
            mask.append(correct)
        results.append({'omitted_t': omitted, 'pair_polynomials_ascending':
                        [[str(c) for c in poly] for poly in polys], 'correct': mask})
    assert successes == [3] * 4
    return {'measurement': 't=x1+2*x2', 'interpolants': results,
            'pointwise_success_probability': '3/4', 'exact_rational_verification': True}


def cubic_full_control():
    first = [F(0), F(10,3), F(-3), F(2,3)]
    second = [F(0), F(-7,6), F(3,2), F(-1,3)]
    for t in range(4):
        recovered = tuple(sum(c*t**k for k,c in enumerate(poly)) for poly in (first,second))
        assert recovered == (t%2, t//2)
    return {'measurement': 't=x1+2*x2',
            'first_bit_polynomial_ascending': [str(c) for c in first],
            'second_bit_polynomial_ascending': [str(c) for c in second],
            'all_four_inputs_verified': True}


def midpoint_controls():
    tests = 0
    for n in range(2, 9):
        # Dense fixed linear target and arbitrary independent quadratic Boolean gauges.
        b = [[F((i+2)*(j+1)-3) for j in range(n)] for i in range(n)]
        gauge = [[F((-1)**(i+j)*(i+j+1), i+1) for j in range(n)] for i in range(n)]
        def q(x):
            return [sum(b[i][j]*x[j]+gauge[i][j]*(x[j]*x[j]-x[j]) for j in range(n))
                    for i in range(n)]
        for d in range(1, 8):
            h = [F(j-d, d) for j in range(n)]
            plus = q([F(1,2)+x for x in h])
            minus = q([F(1,2)-x for x in h])
            recovered = [(x-y)/2 for x,y in zip(plus,minus)]
            target = [sum(b[i][j]*h[j] for j in range(n)) for i in range(n)]
            assert recovered == target
            tests += 1
    return {'general_rational_midpoint_cases': tests, 'N_range': [2, 8]}


def main():
    assert prime_trial(PRIME)
    data = json.loads(DATA.read_text())
    provenance = json.loads((ROOT/'source_provenance.json').read_text())
    assert hashlib.sha256(DATA.read_bytes()).hexdigest() == provenance['source_member_sha256']
    out = {'method': 'independently authored checker; uploaded/archive code never executed or imported',
           'source_archive_sha256_recorded': provenance['source_archive_sha256'],
           'source_json_sha256_verified': hashlib.sha256(DATA.read_bytes()).hexdigest(),
           'prime': PRIME, 'prime_verified_by_trial_division': True,
           'cubic_impossibility_certificates': certificate_check(data),
           'cubic_positive_control': cubic_control(),
           'even_spectrum_ambiguity': ambiguity_controls(),
           'sharp_3_over_4_gate_control': sharp_quadratic_gate(),
           'midpoint_controls': midpoint_controls(),
           'cubic_full_reconstruction_control': cubic_full_control()}
    path = ROOT/'independent_boolean_results.json'
    path.write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps(out, indent=2))

if __name__ == '__main__':
    main()
