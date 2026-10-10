"""Exact-subproblem sharing in a radix-2 FFT (educational research prototype).

Canonical signatures are constructed bottom-up for each even/odd FFT recursion
node. Identical coefficient sequences share a node ID, and each unique FFT is
computed once. This is not a sub-n-log-n algorithm for arbitrary FFT input.

Run: python fft_collision_research.py
Requires only Python's standard library. NumPy is optional for extra checks.
"""
import cmath
import math
import random
from collections import Counter


def canonical_fft(signal):
    """FFT using a hash-consed DAG of repeated *exact* recursive subproblems.

    Return (FFT values, stats). n must be a positive power of two.
    Expected O(n) canonicalization under RAM constant-time hash tables.
    Arithmetic butterfly count is sum over levels of size/2 per unique node.
    """
    n = len(signal)
    if n == 0 or n & (n - 1):
        raise ValueError("length must be a positive power of 2")

    intern = {}
    nodes = []  # each node: (size, left id, right id, leaf value)
    calls = 0
    def build(offset, stride, size):
        nonlocal calls
        calls += 1
        if size == 1:
            val = signal[offset]
            key = (1, val)
            spec = (1, -1, -1, val)
        else:
            left = build(offset, stride * 2, size // 2)
            right = build(offset + stride, stride * 2, size // 2)
            key = (size, left, right)
            spec = (size, left, right, None)
        ident = intern.get(key)
        if ident is None:
            ident = len(nodes)
            intern[key] = ident
            nodes.append(spec)
        return ident

    root = build(0, 1, n)
    results = {}
    twiddles = {}
    butterflies = 0
    def evaluate(ident):
        nonlocal butterflies
        if ident in results:
            return results[ident]
        size, left_id, right_id, value = nodes[ident]
        if size == 1:
            out = (complex(value),)
        else:
            left = evaluate(left_id)
            right = evaluate(right_id)
            half = size // 2
            factors = twiddles.get(size)
            if factors is None:
                factors = [cmath.exp(-2j * math.pi * k / size) for k in range(half)]
                twiddles[size] = factors
            out = [0j] * size
            for k in range(half):
                t = factors[k] * right[k]
                out[k] = left[k] + t
                out[k + half] = left[k] - t
                butterflies += 1
            out = tuple(out)
        results[ident] = out
        return out

    fft = evaluate(root)
    unique_by_size = Counter(size for size, _, _, _ in nodes)
    return fft, {
        'input_length': n,
        'radix2_butterflies': n * (n.bit_length()-1) // 2,
        'shared_butterflies': butterflies,
        'unique_fft_nodes': len(nodes),
        'tree_nodes_visited': calls,
        'unique_by_size': dict(sorted(unique_by_size.items())),
        'cached_complex_entries': sum(len(x) for x in results.values()),
    }


def reference_dft(a):
    n = len(a)
    return [sum(a[j] * cmath.exp(-2j * math.pi * j * k / n) for j in range(n)) for k in range(n)]


def tests():
    for n in (2, 4, 8, 16, 32, 64):
        for seed in range(4):
            r = random.Random(300 + 10*n + seed)
            seq = [r.randrange(2) for _ in range(n)]
            actual, stats = canonical_fft(seq)
            expected = reference_dft(seq)
            err = max(abs(x-y) for x,y in zip(actual,expected))
            assert err < 1e-8, (n,seed,err)
            assert stats['tree_nodes_visited'] == 2*n-1
    a = [4,3,2,1,0,0,0,0]
    b = [8,7,6,5,0,0,0,0]
    fa,_ = canonical_fft(a)
    fb,_ = canonical_fft(b)
    prod = [x*y for x,y in zip(fa,fb)]
    # reverse FFT by the conjugation identity
    rev,_ = canonical_fft([v.conjugate() for v in prod])
    coeffs = [round((v.conjugate()/8).real) for v in rev]
    assert coeffs == [32,52,61,60,34,16,5,0], coeffs
    print('TESTS PASSED: 24 direct-DFT comparisons; canonicalization node invariant; 1234*5678 =',
          sum(coeffs[j]*10**j for j in range(8)))


def experiment():
    print('N | distribution | standard_butterflies | shared_butterflies | fraction_saved | unique_nodes | cached_entries')
    for n in (256, 1024, 4096, 16384):
        rng = random.Random(1000+n)
        random_input = [rng.randrange(2) for _ in range(n)]
        rng256 = random.Random(2000+n)
        alphabet256_input = [rng256.randrange(256) for _ in range(n)]
        cases = {
            'uniform_ones': [1]*n,
            'period_8': ([1,0,1,1,0,0,1,0]*(n//8)),
            'random_binary': random_input,
            'random_0_255': alphabet256_input,
        }
        for label, values in cases.items():
            _,s = canonical_fft(values)
            frac = 1-s['shared_butterflies']/s['radix2_butterflies']
            print(f"{n} | {label} | {s['radix2_butterflies']} | {s['shared_butterflies']} | {frac:.3%} | {s['unique_fft_nodes']} | {s['cached_complex_entries']}")
        if n == 4096:
            _,s1 = canonical_fft(cases['random_binary'])
            _,s2 = canonical_fft(cases['period_8'])
            print('LEVELS random binary N=4096:',s1['unique_by_size'])
            print('LEVELS period 8 N=4096:',s2['unique_by_size'])


def standard_fft(signal):
    """Ordinary radix-2 FFT without memoization; separate independent reference."""
    n = len(signal)
    twiddles = {}
    def rec(offset, stride, length):
        if length == 1:
            return (complex(signal[offset]),)
        even = rec(offset, stride * 2, length // 2)
        odd = rec(offset + stride, stride * 2, length // 2)
        factors = twiddles.get(length)
        if factors is None:
            factors = [cmath.exp(-2j * math.pi * k / length) for k in range(length // 2)]
            twiddles[length] = factors
        out = [0j] * length
        for k in range(length // 2):
            t = factors[k] * odd[k]
            out[k] = even[k] + t
            out[k + length // 2] = even[k] - t
        return tuple(out)
    return rec(0, 1, n)


def expected_unique_binary(n, m):
    """Expected distinct independent uniform binary blocks of size m."""
    B = n // m
    if m > 50:
        return B  # the expected relative duplicate count is negligible here
    p = 2**(-m)
    return -math.expm1(B * math.log1p(-p)) / p


def expected_butterflies_binary(n):
    return sum((m / 2) * expected_unique_binary(n, m)
               for m in (1 << j for j in range(1, n.bit_length())))


def benchmarks():
    from time import perf_counter
    import statistics
    print('EXPECTED_RANDOM_BUTTERFLIES (independent uniform bits)')
    for n in (256, 1024, 4096, 16384, 65536):
        print(f'N={n}, expected={expected_butterflies_binary(n):.1f}, regular={n*(n.bit_length()-1)//2}')
    print('TIMINGS_SECONDS (pure Python, per-run median of 3; not a hardware-level performance claim)')
    for n in (4096,16384,65536):
        rng = random.Random(123456+n)
        for label,values in (
            ('period_8',[1,0,1,1,0,0,1,0]*(n//8)),
            ('random_binary',[rng.randrange(2) for _ in range(n)]),
        ):
            times = {}
            for fn in (standard_fft,canonical_fft):
                tt=[]
                for _ in range(3):
                    t0=perf_counter()
                    result=fn(values)
                    dt=perf_counter()-t0
                    tt.append(dt)
                times[fn.__name__]=statistics.median(tt)
            reference=standard_fft(values)
            actual,_=canonical_fft(values)
            assert max(abs(a-b) for a,b in zip(reference,actual)) < 1e-8
            print(f"N={n} {label} standard={times['standard_fft']:.5f}s shared={times['canonical_fft']:.5f}s ratio={times['standard_fft']/times['canonical_fft']:.2f}x")


if __name__ == '__main__':
    tests()
    experiment()
    benchmarks()
