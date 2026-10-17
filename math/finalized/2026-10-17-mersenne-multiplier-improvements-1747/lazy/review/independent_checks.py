"""Independent bounded tests of inspected fresh kernels, never historical code."""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import hashlib
import itertools
import json
from collections import Counter
from random import Random
from statistics import median
from time import perf_counter_ns

SOURCE = Path(__file__).resolve().parent.parent / 'source'
EXPECTED = {
    'coefficient_lift.py': '09877b7a81aff33431b436f6a94437555f0f8f2bb34992f9b18120557746366f',
    'lazy_fermat.py': 'b302f45c38705c83242db20d0a6ed57ef94888d0dec5a9810704a329355076e8',
    'lift_results.json': '84c98b0c3fc8a5ed90a6f9b6594195209ea0a2a69e93548f109afdc36b42b550',
    'results.json': '8501291fc6f09836487af1604e0ef26e0d689e6cedb6bb823695dc0fdc36bef7',
    'SHA256SUMS_pre_review.txt': 'c6927a3b0c5b0cdbc590b66172ee58f1525a4ec34a731261b982b40f3ccf6c5b',
    'REPORT.md': '14f674e37f9901e62d33f2fb939813a77ac0df60d60e4b272873257e171a1a84',
}

# Publication portability: gate the published bytes, preserving original seals separately.
publication_root = Path(__file__).resolve().parents[2]
publication_manifest = json.loads((publication_root / 'PUBLICATION_MANIFEST.json').read_text())
EXPECTED = {entry['path'].split('/')[-1]: entry['sha256']
            for entry in publication_manifest['files']
            if entry['path'].startswith('lazy/source/')}

def fingerprints():
    return {name: hashlib.sha256((SOURCE / name).read_bytes()).hexdigest()
            for name in EXPECTED}
assert fingerprints() == EXPECTED
sys.path.insert(0, str(SOURCE))
import lazy_fermat as lf
import coefficient_lift as cl

counts = Counter()
rng = Random(0x17411017)

# Exhaust every integer in the legal whole-transform envelope in small plans.
for r in range(1, 10):
    for k in (2, 4, 8, 16):
        if 2 * r % k:
            continue
        p = lf.Plan(k, r)
        R = 1 << r
        powers = [(e, pow(2, e % (2*r), p.q)) for e in range(-2*r-1, 2*r+2)]
        for x in range(-k*R, k*R+1):
            C = max(1, (abs(x) + R - 1) // R)
            z = lf.canonical(x, p, None)
            assert z == x % p.q
            counts['exhaustive_boundary_canonicalizations'] += 1
            for e, factor in powers:
                y = lf.signed_shift(x, e, p, None)
                assert y % p.q == (x * factor) % p.q
                assert abs(y) <= C * R
                counts['exhaustive_signed_shift_envelopes'] += 1
        for a in range(p.q):
            for b in range(p.q):
                if r > 5 and a not in (0, 1, R-1, R):
                    break
                assert lf.correct_only(a+b, p, None) == (a+b) % p.q
                assert lf.correct_only(a-b, p, None) == (a-b) % p.q
                z = a*b
                z = (z & p.mask) - (z >> r)
                if z < 0:
                    z += p.q
                assert z == (a*b) % p.q
                counts['canonical_add_sub_product_cases'] += 1

# This DFT control does not call either implementation's reference transform.
def bit_reverse(k):
    ell = k.bit_length()-1
    return [sum(((i >> bit) & 1) << (ell-1-bit) for bit in range(ell))
            for i in range(k)]

def direct(values, p, inverse):
    rev = bit_reverse(p.k)
    root = pow(2, 2*p.r//p.k, p.q)
    if inverse:
        root = pow(root, -1, p.q)
        values = [values[rev[i]] for i in range(p.k)]
    powers = [pow(root, i, p.q) for i in range(p.k)]
    result = [sum(v * powers[(j*h) % p.k] for j, v in enumerate(values)) % p.q
              for h in range(p.k)]
    if inverse:
        scale = pow(p.k, -1, p.q)
        return [(v*scale) % p.q for v in result]
    return [result[rev[i]] for i in range(p.k)]

for k in (2, 4, 8, 16, 32, 64):
    for w in (1, 2, 3, 5, 7, 8, 9, 15, 16, 31):
        p = lf.Plan(k, w*k//2)
        R = p.q-1
        samples = [[0]*k, [R]*k, [R]+[0]*(k-1),
                   [R if i % 2 else 0 for i in range(k)],
                   [i % p.q for i in range(k)]]
        samples += [[rng.randrange(p.q) for _ in range(k)] for _ in range(5)]
        for values in samples:
            for inverse in (False, True):
                want = direct(values, p, inverse)
                for lazy in (False, True):
                    got = lf.transform(values, inverse, p, lazy, check_bounds=True)
                    assert got == want
                    counts['independent_dft_residue_comparisons'] += 1
                assert cl.lifted_transform(values, inverse, p) == want
                counts['independent_dft_lift_comparisons'] += 1

# Exhaustive tiny coefficient vectors include both signed carry extremes.
for k, w in ((2, 1), (2, 2), (4, 1), (4, 2), (8, 1)):
    d = k//2
    bound = k*((1 << w)-1)
    q = (1 << (w*d))+1
    for coeff in itertools.product(range(-bound, bound+1), repeat=d):
        want = sum(c * pow(1 << w, j) for j,c in enumerate(coeff)) % q
        assert cl.stream_evaluate(coeff, w, k) == want
        counts['exhaustive_signed_carry_vectors'] += 1

# Compare entry conversion with an independent division-based oracle.
for d in (1, 2, 3, 4, 7, 16, 32, 128):
    for w in (1, 2, 3, 5, 7, 8, 9, 15, 16, 31, 63, 64, 65):
        R = 1 << (d*w)
        for x in [0, 1, R-1, R//2] + [rng.randrange(R) for _ in range(8)]:
            y = x
            wanted = []
            for _ in range(d):
                y, digit = divmod(y, 1 << w)
                wanted.append(digit)
            assert cl.lift(x, w, d) == wanted
            counts['entry_lift_division_oracle_cases'] += 1

# No redundant rerun of the author's suites or timing experiment. These fresh
# inputs check coefficient convolution and the symbolic ledgers independently.
convolution_plans = []
for k, m in ((64, 192), (128, 384), (256, 768), (512, 1536)):
    n = k//2
    base = (1 << m)-1
    p = lf.make_plan(k, n*(base-1)**2)
    a = [rng.randrange(base) for _ in range(n)]
    b = [rng.randrange(base) for _ in range(n)]
    want = [0]*k
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            want[i+j] += x*y
    ell = k.bit_length()-1
    F = k*ell//2-k+1
    ledgers = {}
    for mode in (False, True):
        ledger = Counter()
        assert lf.convolution(a, b, p, mode, ledger, True) == want
        assert ledger['butterfly_additions'] == 3*k*ell
        assert ledger['split_folds'] == 3*F+k
        assert ledger['native_pointwise_multiplications'] == k
        assert ledger['canonicalizations'] == (3*k if mode else 3*k*ell+3*F+k)
        counts['fresh_convolution_and_ledger_checks'] += 1
        ledgers[str(mode)] = dict(ledger)
    convolution_plans.append({'K': k, 'm': m, 'r': p.r, 'ledgers': ledgers})

for bits in (2, 19, 129, 1024, 4096):
    for m in (2, 5, 16, 63):
        for mersenne in (False, True):
            x, y = rng.getrandbits(bits), rng.getrandbits(bits)
            for mode in (False, True):
                assert lf.multiply(x, y, m, mersenne, mode) == x*y
                counts['fresh_end_to_end_integer_products'] += 1

assert fingerprints() == EXPECTED
print(json.dumps({'status':'PASS', 'source_fingerprints':EXPECTED,
                  'independent_checks':dict(counts),
                  'fresh_convolution_ledgers':convolution_plans,
                  'scope':'Fresh independent correctness and operation counts only; no historical source executed, no fresh timing claim.'}, indent=2))
