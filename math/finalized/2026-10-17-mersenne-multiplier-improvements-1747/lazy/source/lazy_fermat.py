"""Fresh exact lazy-reduction Fermat FFT experiment, 2026-10-17.

No historical source is imported or executed. Standard library only.
This is a finite-cost experiment, not a sub-N-log-N multiplier.
"""
from dataclasses import dataclass, field
from collections import Counter
from random import Random
from statistics import median
from time import perf_counter_ns
import json


@dataclass(frozen=True)
class Plan:
    k: int
    r: int
    q: int = field(init=False)
    mask: int = field(init=False)

    def __post_init__(self):
        assert self.k >= 2 and self.k & (self.k - 1) == 0
        assert self.r > 0 and 2 * self.r % self.k == 0
        object.__setattr__(self, 'q', (1 << self.r) + 1)
        object.__setattr__(self, 'mask', (1 << self.r) - 1)


def canonical(x, p, ledger):
    """One fold and at most one correction, for |x| <= K*2**r."""
    if ledger is not None:
        ledger['canonicalizations'] += 1
    z = (x & p.mask) - (x >> p.r)
    if z < 0:
        z += p.q
        if ledger is not None:
            ledger['canonical_corrections'] += 1
    elif z >= p.q:
        z -= p.q
        if ledger is not None:
            ledger['canonical_corrections'] += 1
    assert 0 <= z < p.q
    return z


def correct_only(x, p, ledger):
    """Canonical baseline: no redundant fold after ordinary addition."""
    if ledger is not None:
        ledger['canonicalizations'] += 1
    if x < 0:
        x += p.q
        if ledger is not None:
            ledger['canonical_corrections'] += 1
    elif x >= p.q:
        x -= p.q
        if ledger is not None:
            ledger['canonical_corrections'] += 1
    return x


def signed_shift(x, exponent, p, ledger):
    """A root action on a signed, noncanonical representative."""
    exponent %= 2 * p.r
    negative = exponent >= p.r
    s = exponent - p.r if negative else exponent
    if s:
        if ledger is not None:
            ledger['split_folds'] += 1
        x = ((x << s) & p.mask) - (x >> (p.r - s))
    if negative:
        x = -x
    return x


def transform(values, inverse, p, lazy, ledger=None, check_bounds=False):
    """Forward DIF and inverse DIT, with compatible scrambled spectrum."""
    assert len(values) == p.k
    a = list(values)
    assert all(0 <= x < p.q for x in a)
    length = 2 if inverse else p.k
    stage = 0
    while (length <= p.k if inverse else length >= 2):
        half = length // 2
        step = 2 * p.r // length
        for start in range(0, p.k, length):
            for j in range(half):
                u, v = a[start + j], a[start + half + j]
                if inverse and j:
                    v = signed_shift(v, -j * step, p, ledger)
                    if not lazy:
                        v = correct_only(v, p, ledger)
                x, y = u + v, u - v
                if ledger is not None:
                    ledger['butterfly_additions'] += 2
                if not lazy:
                    x = correct_only(x, p, ledger)
                    y = correct_only(y, p, ledger)
                if not inverse and j:
                    y = signed_shift(y, j * step, p, ledger)
                    if not lazy:
                        y = correct_only(y, p, ledger)
                a[start + j], a[start + half + j] = x, y
        stage += 1
        if check_bounds:
            assert max(map(abs, a)) <= (1 << (p.r + stage))
        if ledger is not None:
            ledger['peak_absolute_bits'] = max(ledger['peak_absolute_bits'],
                                              max(abs(x).bit_length() for x in a))
        length = length * 2 if inverse else length // 2
    if inverse:
        a = [signed_shift(x, -(p.k.bit_length() - 1), p, ledger) for x in a]
    if lazy:
        a = [canonical(x, p, ledger) for x in a]
    elif inverse:
        a = [correct_only(x, p, ledger) for x in a]
    return a


def convolution(a, b, p, lazy, ledger=None, check_bounds=False):
    assert len(a) + len(b) - 1 <= p.k
    aa = list(a) + [0] * (p.k - len(a))
    bb = list(b) + [0] * (p.k - len(b))
    fa = transform(aa, False, p, lazy, ledger, check_bounds)
    fb = transform(bb, False, p, lazy, ledger, check_bounds)
    products = []
    for x, y in zip(fa, fb):
        z = x * y
        if ledger is not None:
            ledger['native_pointwise_multiplications'] += 1
        z = (z & p.mask) - (z >> p.r)
        if z < 0:
            z += p.q
        products.append(z)
    return transform(products, True, p, lazy, ledger, check_bounds)


def make_plan(k, bound):
    multiple = k // 2
    r = max(multiple, ((bound.bit_length() + multiple - 1) // multiple) * multiple)
    return Plan(k, r)


def digits(x, base):
    """Simple reference conversion; deliberately not a fast-conversion claim."""
    out = []
    while x:
        x, d = divmod(x, base)
        out.append(d)
    return out or [0]


def multiply(x, y, m, mersenne, lazy, ledger=None):
    base = (1 << m) - int(mersenne)
    a, b = digits(x, base), digits(y, base)
    k = 1 << max(1, (len(a) + len(b) - 2).bit_length())
    p = make_plan(k, min(len(a), len(b)) * (base - 1)**2)
    cs = convolution(a, b, p, lazy, ledger)
    z = 0
    for c in reversed(cs[:len(a) + len(b) - 1]):
        z = z * base + c
    return z


def reference_dft(a, p, inverse=False):
    root = pow(2, 2 * p.r // p.k, p.q)
    if inverse:
        root = pow(root, -1, p.q)
    out = [sum(x * pow(root, j * k, p.q) for j, x in enumerate(a)) % p.q
           for k in range(p.k)]
    if inverse:
        out = [x * pow(p.k, -1, p.q) % p.q for x in out]
    return out


def reverse_bits(i, bits):
    return int(format(i, '0%db' % bits)[::-1], 2)


def validate():
    rng = Random(202610171728)
    checks = Counter()
    for k in (2, 4, 8, 16, 32):
        for multiple in (1, 2, 3):
            p = Plan(k, multiple * k // 2)
            R = 1 << p.r
            for e in range(-2 * p.r, 2 * p.r + 1):
                for x in (-k * R, -R - 1, -R, -1, 0, 1, R - 1, R, k * R):
                    out = signed_shift(x, e, p, Counter())
                    assert out % p.q == x * pow(2, e % (2 * p.r), p.q) % p.q
                    assert abs(out) <= max(R, abs(x) + R)
                    checks['signed_shift_cases'] += 1
            boundary = [0, 1, p.q - 1]
            vectors = [[boundary[j % 3] for j in range(k)], [p.q - 1] * k]
            vectors += [[rng.randrange(p.q) for _ in range(k)] for _ in range(12)]
            for a in vectors:
                ref = reference_dft(a, p)
                scrambled = [ref[reverse_bits(j, k.bit_length() - 1)] for j in range(k)]
                for lazy in (False, True):
                    f = transform(a, False, p, lazy, check_bounds=True)
                    assert f == scrambled
                    assert transform(f, True, p, lazy, check_bounds=True) == a
                    checks['dft_and_inverse_cases'] += 1
    for bits in (1, 2, 8, 19, 64, 129, 511, 1024, 4096):
        for m in (2, 5, 16, 63):
            for mersenne in (False, True):
                for _ in range(4):
                    x, y = rng.getrandbits(bits), rng.getrandbits(bits)
                    for lazy in (False, True):
                        assert multiply(x, y, m, mersenne, lazy) == x * y
                        checks['integer_product_cases'] += 1
    return dict(checks)


def benchmark():
    """Convolution-only same-plan control; no claim about historical timings."""
    rng = Random(202610171729)
    rows = []
    for k, m in ((64, 192), (128, 384), (256, 768), (512, 1536)):
        length = k // 2
        p = make_plan(k, length * ((1 << m) - 2)**2)
        pairs = [([rng.getrandbits(m) % ((1 << m) - 1) for _ in range(length)],
                  [rng.getrandbits(m) % ((1 << m) - 1) for _ in range(length)])
                 for _ in range(5)]
        samples = {False: [], True: []}
        for a, b in pairs:
            expected = [sum(a[i] * b[j - i] for i in range(length)
                            if 0 <= j - i < length) for j in range(k - 1)] + [0]
            order = [False, True] * 3
            rng.shuffle(order)
            for lazy in order:
                start = perf_counter_ns()
                result = convolution(a, b, p, lazy)
                elapsed = perf_counter_ns() - start
                assert result == expected
                samples[lazy].append(elapsed)
        ledgers = {}
        for lazy in (False, True):
            ledger = Counter()
            convolution(*pairs[0], p, lazy, ledger)
            ledgers[str(lazy)] = dict(ledger)
        medians = {str(k): median(v) for k, v in samples.items()}
        rows.append({'K': k, 'm': m, 'r': p.r, 'convolution_median_ns': medians,
                     'canonical_over_lazy_ratio': medians['False'] / medians['True'],
                     'ledgers': ledgers})
    return rows


if __name__ == '__main__':
    print(json.dumps({'validation': validate(), 'benchmarks': benchmark()}, indent=2))
