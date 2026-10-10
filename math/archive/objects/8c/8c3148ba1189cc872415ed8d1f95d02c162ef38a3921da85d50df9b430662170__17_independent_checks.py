#!/usr/bin/env python3
"""Independent Phase23 checks and a root-free recurrence executor.

Python 3.10+ standard library only. No uploaded source is imported, executed,
or read. All residues use P=998244353. This program deliberately chooses its
own consistent square-root signs; exact identities do not depend on those signs.
The direct DFT and recursive radix-two reference are separate from the Green
evaluators. Run from any directory; results are written beside this script.
"""
import hashlib
import itertools
import json
import math
from pathlib import Path
import platform
import random
import sys
import time

P = 998244353
G = 3
INV2 = (P + 1) // 2


def inverse(a):
    return pow(a % P, -1, P)


def batch_inverse(values):
    """Exactly one field inversion, 3m field multiplications, O(m) storage."""
    prefixes = [1]
    for a in values:
        assert a % P
        prefixes.append(prefixes[-1] * a % P)
    running = inverse(prefixes[-1])
    result = [0] * len(values)
    for k in reversed(range(len(values))):
        result[k] = running * prefixes[k] % P
        running = running * values[k] % P
    return result


class FieldTransform:
    def __init__(self, n):
        assert n >= 4 and n & (n - 1) == 0 and (P - 1) % n == 0
        self.n = n
        self.w = pow(G, (P - 1) - (P - 1) // n, P)
        self.winv = inverse(self.w)
        eta = pow(G, (P - 1) // 8, P)
        self.sqrt2 = (eta + inverse(eta)) % P
        self.sqrt_n = pow(self.sqrt2, n.bit_length() - 1, P)
        self.scale = inverse(self.sqrt_n)
        self.isqrt2 = inverse(self.sqrt2)
        self.i = inverse(pow(self.w, n // 4, P))
        self.roots = [1]
        for _ in range(1, n):
            self.roots.append(self.roots[-1] * self.w % P)
        self.cs = []
        inv2i = inverse(2 * self.i)
        for k in range(1, n // 2):
            c = (self.roots[k] + self.roots[-k]) * INV2 % P
            s = (self.roots[-k] - self.roots[k]) * inv2i % P
            self.cs.append((c, s))
        assert self.sqrt2 ** 2 % P == 2 and self.sqrt_n ** 2 % P == n
        assert self.roots[-1] * self.w % P == 1
        assert self.roots[n // 2] == P - 1

    def spectrum_to_c(self, f):
        n = self.n
        y = [0] * n
        y[0], y[1] = f[0], f[n // 2]
        for k in range(1, n // 2):
            y[k + 1] = (f[k] + f[-k]) * self.isqrt2 % P
            y[n // 2 + k] = (f[k] - f[-k]) * self.i * self.isqrt2 % P
        return y

    def direct(self, x):
        f = []
        for t in self.roots:
            total = 0
            for a in reversed(x):
                total = (total * t + a) % P
            f.append(total * self.scale % P)
        return self.spectrum_to_c(f)

    def recursive_fft(self, x):
        def recur(a, w):
            if len(a) == 1:
                return a
            e = recur(a[::2], w * w % P)
            o = recur(a[1::2], w * w % P)
            half = len(e)
            out = [0] * len(a)
            z = 1
            for j in range(half):
                b = z * o[j] % P
                out[j] = (e[j] + b) % P
                out[j + half] = (e[j] - b) % P
                z = z * w % P
            return out
        return self.spectrum_to_c([a * self.scale % P for a in recur(x, self.w)])

    def geometric_resolvent(self, z):
        n, h = self.n, self.n // 2
        z %= P
        zn = pow(z, n, P)
        if zn == 1:
            # Find the character's frequency without a discrete logarithm.
            target = inverse(z)
            f = self.roots.index(target)
            spectrum = [0] * n
            spectrum[f] = self.sqrt_n
            return self.spectrum_to_c(spectrum)
        denominators = [(1 - z) % P, (1 + z) % P]
        denominators += [(1 - 2 * z * c + z * z) % P for c, s in self.cs]
        invs = batch_inverse(denominators)
        factor = (1 - zn) * self.scale % P
        y = [factor * invs[0] % P, factor * invs[1] % P] + [0] * (n - 2)
        for j, ((c, s), d) in enumerate(zip(self.cs, invs[2:]), 1):
            factor2 = factor * self.sqrt2 * d % P
            y[j + 1] = factor2 * (1 - z * c) % P
            y[h + j] = factor2 * z * s % P
        return y

    def sparse_difference(self, x, order):
        d = difference(x, order)
        support = [(j, a) for j, a in enumerate(d) if a]
        accum = [0] * self.n
        for j, a in support:
            t = 1
            for k in range(self.n):
                accum[k] = (accum[k] + a * t) % P
                t = t * self.roots[j] % P
        invs = batch_inverse([(1 - t) % P for t in self.roots[1:]])
        spectrum = [sum(x) * self.scale % P]
        spectrum += [accum[k] * self.scale * pow(invs[k - 1], order, P) % P
                     for k in range(1, self.n)]
        return self.spectrum_to_c(spectrum), len(support)

    def recurrence2(self, x, u, v):
        """New complete order-two recurrence executor, including singular roots.

        Verifies all input equations, uses one batch inversion, and evaluates
        at most two exceptional Fourier frequencies by direct Horner summation.
        No discriminant, polynomial roots, or data-dependent square roots.
        Returns all C*x outputs and exact exception locations.
        """
        x = [a % P for a in x]
        u, v = u % P, v % P
        assert len(x) == self.n
        assert all(x[k + 2] == (u * x[k + 1] + v * x[k]) % P
                   for k in range(self.n - 2))
        xn = (u * x[-1] + v * x[-2]) % P
        p0 = (x[0] - xn) % P
        p1 = (x[1] - u * x[0] - v * x[-1]) % P
        qvals = [(1 - u * t - v * t * t) % P for t in self.roots]
        regular = [k for k, q in enumerate(qvals) if q]
        exceptional = [k for k, q in enumerate(qvals) if not q]
        assert len(exceptional) <= 2
        invs = batch_inverse([qvals[k] for k in regular])
        spectrum = [0] * self.n
        for k, iq in zip(regular, invs):
            spectrum[k] = (p0 + p1 * self.roots[k]) * iq * self.scale % P
        for k in exceptional:
            value = 0
            for a in reversed(x):
                value = (value * self.roots[k] + a) % P
            spectrum[k] = value * self.scale % P
        return self.spectrum_to_c(spectrum), exceptional


def synthesize(n, nodes, weights):
    x = [0] * n
    for z, a in zip(nodes, weights):
        value = a
        for k in range(n):
            x[k] = (x[k] + value) % P
            value = value * z % P
    return x


def infer_recurrence2(x):
    """Complete raw-input recognition of fixed-coefficient order <=2."""
    x = [a % P for a in x]
    if not any(x):
        return (0, 0)
    if x[0]:
        z = x[1] * inverse(x[0]) % P
        if all(x[k + 1] == z * x[k] % P for k in range(len(x) - 1)):
            return (z, 0)
    determinant = (x[1] * x[1] - x[0] * x[2]) % P
    if determinant == 0:
        return None
    u = (x[1] * x[2] - x[0] * x[3]) * inverse(determinant) % P
    v = (x[1] * x[3] - x[2] * x[2]) * inverse(determinant) % P
    if all(x[k + 2] == (u * x[k + 1] + v * x[k]) % P
           for k in range(len(x) - 2)):
        return u, v
    return None


def source_detector_accepts(x):
    """Independent mathematical reconstruction of source acceptance predicate.

    A split distinct quadratic is tested by Euler's criterion; recovering its
    roots is unnecessary to verify the predicate and avoids copying source code.
    """
    x = [a % P for a in x]
    if not any(x):
        return True
    if x[0]:
        z = x[1] * inverse(x[0]) % P
        if all(x[k + 1] == z * x[k] % P for k in range(len(x) - 1)):
            return True
    recurrence = infer_recurrence2(x)
    if recurrence is None:
        return False
    u, v = recurrence
    disc = (u * u + 4 * v) % P
    return disc != 0 and pow(disc, (P - 1) // 2, P) == 1


def root_free_adaptive(x, engine=None):
    """Full raw-input algorithm: complete order<=2 path, otherwise exact FFT."""
    model = FieldTransform(len(x)) if engine is None else engine
    if len(x) != model.n:
        raise ValueError("input and engine lengths differ")
    residues = [a % P for a in x]
    coefficients = infer_recurrence2(residues)
    if coefficients is None:
        return model.recursive_fft(residues), "recursive_fft_fallback"
    y, _ = model.recurrence2(residues, *coefficients)
    return y, "root_free_recurrence_at_most_two"


def difference(x, order):
    y = list(x)
    for _ in range(order):
        y = [(y[k] - y[k - 1]) % P for k in range(len(y))]
    return y


def gf2_hankel_rank(word, m):
    mask = (1 << m) - 1
    rows = [(word >> k) & mask for k in range(m)]
    basis = {}
    for row in rows:
        while row:
            pivot = row.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = row
                break
            row ^= basis[pivot]
    return len(basis)


def integer_hankel_determinant(word, m):
    """Fraction-free Bareiss, used only to verify the mod-2 lifting claim."""
    a = [[(word >> (i + j)) & 1 for j in range(m)] for i in range(m)]
    sign, divisor = 1, 1
    for k in range(m - 1):
        pivot = next((i for i in range(k, m) if a[i][k]), None)
        if pivot is None:
            return 0
        if pivot != k:
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        for i in range(k + 1, m):
            for j in range(k + 1, m):
                numerator = a[i][j] * a[k][k] - a[i][k] * a[k][j]
                assert numerator % divisor == 0
                a[i][j] = numerator // divisor
            a[i][k] = 0
        divisor = a[k][k]
    return sign * a[-1][-1]


def run():
    start = time.perf_counter()
    rng = random.Random(2300910)
    results = {"dependencies": "Python >=3.10 standard library only", "modulus": P,
               "uploaded_code_executed_or_imported": False, "checks": {}}
    checks = results["checks"]
    assert all(pow(G, (P - 1) // q, P) != 1 for q in (2, 7, 17))
    geometric_count, root_count, support_count, direct_fft_count = 0, 0, 0, 0
    for n in (4, 8, 16, 32, 64, 128):
        engine = FieldTransform(n)
        for _ in range(3):
            x = [rng.randrange(P) for _ in range(n)]
            assert engine.direct(x) == engine.recursive_fft(x)
            direct_fft_count += 1
        for z in [0, 2, 3, 7, rng.randrange(P)] + engine.roots:
            x = synthesize(n, [z], [1])
            assert engine.geometric_resolvent(z) == engine.direct(x)
            if pow(z, n, P) == 1:
                root_count += 1
            else:
                geometric_count += 1
        for k in range(n):
            e = [0] * n
            e[k] = 1
            count = sum(a != 0 for a in engine.direct(e))
            v2 = (k & -k).bit_length() - 1 if k else None
            expected = n // 2 + 1 if k in (0, n // 2) else n - 2 ** (v2 + 1) + 1
            assert count == expected
            support_count += 1
    checks["small_direct_references"] = {"fft_comparisons": direct_fft_count,
        "nonroot_geometric_cases": geometric_count, "all_root_cases": root_count,
        "inverse_support_rows": support_count, "sizes": [4, 8, 16, 32, 64, 128]}

    recurrence_records = []
    difference_records = []
    adaptive_cases = 0
    for n in (8, 32, 128, 512, 2048, 8192):
        engine = FieldTransform(n)
        cases = []
        for name, u, v, initial in [
                ("repeated_nonroot", 34, -289, [5, 238]),
                ("irreducible_discriminant", 0, 3, [1, 4]),
                ("double_zero_root", 0, 0, [0, 1]),
                ("repeated_root_one", 2, -1, [4, 11]),
                ("two_root_frequencies", 0, 1, [9, 2]),
                ("generic", 7, 11, [3, 19])]:
            x = list(initial)
            for _ in range(n - 2):
                x.append((u * x[-1] + v * x[-2]) % P)
            inferred = infer_recurrence2(x)
            assert inferred is not None
            y, exceptional = engine.recurrence2(x, *inferred)
            assert y == engine.recursive_fft(x)
            ya, method = root_free_adaptive(x, engine)
            assert ya == y and method == "root_free_recurrence_at_most_two"
            adaptive_cases += 1
            cases.append({"case": name, "exceptions": exceptional,
                          "source_exponential_detector_accepts": source_detector_accepts(x)})
        recurrence_records.append({"N": n, "cases": cases})
        raw = [rng.randrange(P) for _ in range(n)]
        ya, method = root_free_adaptive(raw, engine)
        assert ya == engine.recursive_fft(raw) and method == "recursive_fft_fallback"
        adaptive_cases += 1
        for order, x in [(1, [7] * (n // 3) + [12] * (n - n // 3)),
                         (2, [(3 + 7 * k) % P for k in range(n)]),
                         (3, [(k * k + 2 * k + 5) % P for k in range(n)])]:
            y, support = engine.sparse_difference(x, order)
            assert support <= order + 1
            assert y == engine.recursive_fft(x)
            difference_records.append({"N": n, "order": order, "support": support})
        for _ in range(5):
            nodes = [rng.randrange(P), rng.randrange(P)]
            weights = [rng.randrange(1, P), rng.randrange(1, P)]
            x = synthesize(n, nodes, weights)
            assert source_detector_accepts(x)
            actual = [sum(t) % P for t in zip(*[
                [a * b % P for b in engine.geometric_resolvent(z)]
                for z, a in zip(nodes, weights)])]
            assert actual == engine.recursive_fft(x)
    checks["root_free_recurrence_extension"] = recurrence_records
    checks["sparse_difference_cases"] = difference_records
    checks["two_exponential_large_cases"] = 30
    checks["raw_input_adaptive_cases"] = adaptive_cases

    rank_counts = {}
    for m in range(1, 10):
        counts = [0] * (m + 1)
        for word in range(1 << (2 * m - 1)):
            r = gf2_hankel_rank(word, m)
            counts[r] += 1
            if m <= 5:
                det = integer_hankel_determinant(word, m)
                assert (det % 2 != 0) == (r == m)
        expected = [1] + [3 * 4 ** (r - 1) for r in range(1, m)] + [4 ** (m - 1)]
        assert counts == expected
        rank_counts[str(m)] = counts
    checks["exhaustive_binary_hankel_rank_distribution"] = rank_counts

    binary_counts = []
    for n in (4, 8, 12, 16):
        transition_counts = [0] * (n + 1)
        geometric_words = []
        combined = 0
        for word in range(1 << n):
            x = [(word >> k) & 1 for k in range(n)]
            s1 = sum(a != 0 for a in difference(x, 1))
            s2 = sum(a != 0 for a in difference(x, 2))
            transition_counts[s1] += 1
            assert s2 >= s1
            accepted = source_detector_accepts(x)
            if accepted:
                geometric_words.append(''.join(map(str, x)))
            combined += bool(accepted or s1 <= 2 or s2 <= 2)
        assert transition_counts == [2 * math.comb(n, s) if s % 2 == 0 else 0
                                     for s in range(n + 1)]
        assert combined == n * (n - 1) + 4
        if n >= 8:
            assert len(geometric_words) == 6
        binary_counts.append({"N": n, "transitions": transition_counts,
            "geometric_accepted_words": geometric_words,
            "combined_fast_path_count": combined,
            "source_union_upper_count": n * (n - 1) + 34})
    checks["exhaustive_binary_fast_path_counts"] = binary_counts

    # The leading Hankel rank is necessary, not sufficient for a global recurrence.
    x = [0] * 16
    x[-1] = 1
    assert gf2_hankel_rank(0, 8) == 0
    assert infer_recurrence2(x) is None
    checks["low_leading_hankel_rank_not_sufficient"] = {"N": 16, "input": x,
        "leading_hankel_rank": 0, "order_at_most_two_recurrence": False}

    # Verify simultaneous permutation/difference equivariance, order 1..3.
    for n in (8, 32, 128):
        x = [rng.randrange(P) for _ in range(n)]
        perm = list(range(n))
        rng.shuffle(perm)
        y = [0] * n
        for k in range(n):
            y[perm[k]] = x[k]
        for order in (1, 2, 3):
            yd = list(y)
            for _ in range(order):
                following = [0] * n
                for k in range(n):
                    following[perm[k]] = (yd[perm[k]] - yd[perm[k - 1]]) % P
                yd = following
            xd = difference(x, order)
            assert all(yd[perm[k]] == xd[k] for k in range(n))
    checks["permutation_equivariance_cases"] = 9
    results["status"] = "PASS"
    results["elapsed_seconds"] = round(time.perf_counter() - start, 3)
    results["environment"] = {"python": sys.version, "platform": platform.platform()}
    path = Path(__file__).resolve().parent / "CHECK_RESULTS.json"
    path.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({"status": results["status"], "elapsed_seconds": results["elapsed_seconds"],
                      "results": str(path)}, indent=2))


if __name__ == "__main__":
    run()
