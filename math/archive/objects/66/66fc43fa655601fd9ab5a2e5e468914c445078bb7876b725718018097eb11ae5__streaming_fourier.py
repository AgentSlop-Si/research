#!/usr/bin/env python3
"""Independent exact finite-field blocked rational-series Fourier baseline."""
from collections import Counter
import json, math, random, time
from pathlib import Path

MOD = 998244353
GEN = 3

def mul(a, b, c, key):
    c[key] += 1
    return a * b % MOD

def mpow(a, e, c, key='power_modular_multiplications'):
    r = 1
    while e:
        if e & 1: r = mul(r, a, c, key)
        a = mul(a, a, c, key)
        e >>= 1
    return r

def ntt(a, inverse=False, counts=None):
    """Own in-place radix-two kernel; positive sign for forward transform."""
    c = counts if counts is not None else Counter()
    n = len(a)
    assert n and n & (n - 1) == 0 and (MOD - 1) % n == 0
    c['ntt_calls'] += 1
    c['ntt_elements_processed'] += n
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j: a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        exponent = (MOD - 1) // length
        wlen = mpow(GEN, (MOD - 1 - exponent) if inverse else exponent, c)
        for base in range(0, n, length):
            w = 1
            for j in range(base, base + length // 2):
                u = a[j]
                v = mul(a[j + length // 2], w, c, 'butterfly_multiplications')
                a[j] = (u + v) % MOD
                a[j + length // 2] = (u - v) % MOD
                c['butterflies'] += 1
                c['butterfly_additions_subtractions'] += 2
                w = mul(w, wlen, c, 'twiddle_update_multiplications')
        length <<= 1
    if inverse:
        inv = mpow(n, MOD - 2, c)
        for i in range(n): a[i] = mul(a[i], inv, c, 'inverse_scale_multiplications')
    return a

def normalize(n, raw, c):
    assert n >= 1 and n & (n - 1) == 0 and (MOD - 1) % n == 0
    merged = {}
    for j, a in raw:
        j %= n
        c['input_coefficients_read'] += 1
        c['input_merge_additions'] += 1
        merged[j] = (merged.get(j, 0) + a) % MOD
    c['distinct_input_positions'] = len(merged)
    return [(j, a) for j, a in merged.items() if a]

def prepare(n, raw):
    c = Counter()
    support = normalize(n, raw, c)
    k = len(support)
    if not k: return {'k': 0, 'n': n, 'prep_counts': c}
    zeta = mpow(GEN, (MOD - 1) // n, c)
    za = [(mpow(zeta, j, c), a) for j, a in support]
    q = [1]
    for z, a in za:
        nxt = q + [0]
        for i, v in enumerate(q):
            nxt[i + 1] = (nxt[i + 1] - mul(z, v, c, 'prep_multiplications')) % MOD
            c['prep_additions_subtractions'] += 1
        q = nxt
    p = [0] * k
    for z, a in za:
        h = 1
        for d in range(k):
            if d:
                h = (q[d] + mul(z, h, c, 'prep_multiplications')) % MOD
                c['prep_additions_subtractions'] += 1
            p[d] = (p[d] + mul(a, h, c, 'prep_multiplications')) % MOD
            c['prep_additions_subtractions'] += 1
    r = [1] + [0] * (k - 1)
    for d in range(1, k):
        for i in range(1, d + 1):
            r[d] = (r[d] - mul(q[i], r[d - i], c, 'prep_multiplications')) % MOD
            c['prep_additions_subtractions'] += 1
    f = 1 << (2 * k - 1).bit_length()
    qhat = ntt(q + [0] * (f - len(q)), counts=c)
    rhat = ntt(r + [0] * (f - len(r)), counts=c)
    return dict(k=k, n=n, f=f, p=p, qhat=qhat, rhat=rhat, prep_counts=c)

def stream(prepared, counts=None):
    """Yield output blocks; retained workspace O(k), excluding consumer output."""
    c = counts if counts is not None else Counter()
    k, n = prepared['k'], prepared['n']
    if not k:
        for _ in range(n):
            c['output_coefficients'] += 1
            yield [0]
        return
    f = prepared['f']
    p = prepared['p'][:]
    for offset in range(0, n, k):
        c['blocks'] += 1
        ahat = ntt(p + [0] * (f - k), counts=c)
        for i in range(f): ahat[i] = mul(ahat[i], prepared['rhat'][i], c, 'pointwise_multiplications')
        ntt(ahat, inverse=True, counts=c)
        a = ahat[:k]
        # Full transition is intentionally executed even for the final block.
        bhat = ntt(a + [0] * (f - k), counts=c)
        for i in range(f): bhat[i] = mul(bhat[i], prepared['qhat'][i], c, 'pointwise_multiplications')
        ntt(bhat, inverse=True, counts=c)
        assert bhat[:k] == p, 'Divisibility invariant failed'
        p = [(-bhat[i]) % MOD for i in range(k, 2 * k)]
        c['transition_negations'] += k
        out = a[:min(k, n - offset)]
        c['output_coefficients'] += len(out)
        yield out

def baseline(n, raw):
    c = Counter()
    support = normalize(n, raw, c)
    c['dense_input_zero_initializations'] = n
    x = [0] * n
    for j, a in support:
        x[j] = a
        c['dense_input_assignments'] += 1
    ntt(x, counts=c)
    return x, c

def direct(n, raw):
    c = Counter()
    supp = normalize(n, raw, c)
    zeta = mpow(GEN, (MOD - 1) // n, c)
    return [sum(a * mpow(zeta, j * m, c) for j, a in supp) % MOD for m in range(n)]

def run_case(label, n, raw, use_direct=False):
    start = time.perf_counter()
    prep = prepare(n, raw)
    pc = prep['prep_counts']
    gc = Counter()
    actual = [v for block in stream(prep, gc) for v in block]
    stream_seconds = time.perf_counter() - start
    start = time.perf_counter()
    expected, bc = baseline(n, raw)
    baseline_seconds = time.perf_counter() - start
    assert actual == expected, (label, n, prep['k'])
    if use_direct: assert actual == direct(n, raw)
    k = prep['k']
    if k:
        f = prep['f']; blocks = (n + k - 1) // k
        assert gc['ntt_calls'] == 4 * blocks
        assert pc['ntt_calls'] == 2
        assert gc['butterflies'] == 2 * blocks * f * (f.bit_length() - 1)
        assert gc['pointwise_multiplications'] == 2 * blocks * f
        assert pc['prep_multiplications'] == 3 * k * k - k
    assert bc['butterflies'] == n * (n.bit_length() - 1) // 2
    return dict(label=label, n=n, raw_entries=len(raw), active_k=k, convolution_length=prep.get('f'),
                direct_checked=use_direct, verified=True, preparation_counts=dict(pc),
                generation_counts=dict(gc), total_stream_counts=dict(pc + gc), full_ntt_counts=dict(bc),
                illustrative_seconds=dict(stream_including_preparation=stream_seconds, full_ntt=baseline_seconds))

def main():
    rng = random.Random(20261009)
    results = []
    def add(label, n, raw, d=False): results.append(run_case(label, n, raw, d))
    add('empty', 1, [], True)
    add('empty', 64, [], True)
    add('all_zero_after_merging', 32, [(3, 7), (35, -7), (4, 0)], True)
    add('duplicates_merged', 32, [(1, 5), (33, 9), (3, 2), (3, -1)], True)
    for n in [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096]:
        for k in sorted(set(x for x in [1, 2, 3, 4, 5, 7, 8, 16, 31, 32, 63, 64] if x <= n)):
            indices = rng.sample(range(n), k)
            raw = [(j, rng.randrange(1, MOD)) for j in indices]
            add('random_support', n, raw, n <= 64)
        if n <= 64: add('full_support', n, [(j, rng.randrange(1, MOD)) for j in range(n)], True)
        for k in [2, 4, 8, 16, 32, 64]:
            if k <= n:
                add('coset_support', n, [((1 + j * (n // k)) % n, rng.randrange(1, MOD)) for j in range(k)], n <= 64)
    report = dict(modulus=MOD, primitive_root=GEN, seed=20261009, number_of_cases=len(results),
                  all_verified=all(x['verified'] for x in results),
                  direct_verified_cases=sum(x['direct_checked'] for x in results), cases=results)
    path = Path(__file__).with_name('results.json')
    path.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'cases'}, indent=2))
    for n, k in [(4096, 1), (4096, 4), (4096, 16), (4096, 31), (4096, 64), (64, 64)]:
        r = next(x for x in results if x['label'] == 'random_support' and x['n'] == n and x['active_k'] == k)
        print(n, k, 'stream butterflies', r['total_stream_counts']['butterflies'], 'pointwise', r['generation_counts']['pointwise_multiplications'], 'prep scalar', r['preparation_counts']['prep_multiplications'], 'full butterflies', r['full_ntt_counts']['butterflies'])

if __name__ == '__main__': main()
