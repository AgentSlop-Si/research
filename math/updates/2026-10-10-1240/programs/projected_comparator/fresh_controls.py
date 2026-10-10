#!/usr/bin/env python3
"""Independent Phase33 projected-FFT comparator controls.

Standard library only. No submitted or comparator-author program is imported,
executed, or used as a test oracle. All roots are fixed test fixtures, checked
here. The candidate algorithm receives only its cutoff root.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import random


def check_root(root, c, p):
    if pow(root, 1 << c, p) != 1:
        raise ValueError("root has wrong order")
    if c and pow(root, 1 << (c - 1), p) == 1:
        raise ValueError("root is not primitive")


def short_fft(a, powers, p, ledger):
    """Fresh iterative radix-2 DFT; powers is the common cutoff root table."""
    n = len(a)
    assert n and not n & (n - 1)
    a = list(a)
    j = 0
    for i in range(1, n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            a[i], a[j] = a[j], a[i]
    length = 2
    while length <= n:
        stride = len(powers) // length
        for start in range(0, n, length):
            for k in range(length // 2):
                lo = a[start + k]
                hi = a[start + k + length // 2] * powers[k * stride] % p
                a[start + k] = (lo + hi) % p
                a[start + k + length // 2] = (lo - hi) % p
                ledger["fft_additions"] += 2
                ledger["fft_multiplications_including_identity"] += 1
        length <<= 1
    return a


def candidate(x, c, omega, p):
    n = len(x)
    assert n and not n & (n - 1)
    t = n.bit_length() - 1
    assert 0 <= c <= t
    ledger = {k: 0 for k in (
        "input_reads", "bucket_additions", "fft_additions",
        "fft_multiplications_including_identity", "low_merge_additions",
        "high_scatter_additions", "output_initial_writes",
        "prepared_root_multiplications", "peak_fft_length")}
    if not t:
        ledger["input_reads"] = ledger["output_initial_writes"] = 1
        return [x[0] % p], ledger
    c = max(1, c)
    if c == 1:
        assert omega % p == p - 1
    check_root(omega, c, p)
    powers = [1]
    for _ in range(1, 1 << c):
        powers.append(powers[-1] * omega % p)
        ledger["prepared_root_multiplications"] += 1
    low = [x[0] % p]
    ledger["input_reads"] += 1
    y = None
    for j in range(1, t + 1):
        m = min(c, j)
        size = 1 << m
        bucket = [0] * size
        for u in range(1, 1 << j, 2):
            bucket[u % size] = (bucket[u % size] + x[(n >> j) * u]) % p
            ledger["input_reads"] += 1
            ledger["bucket_additions"] += 1
        table = short_fft(bucket, powers, p, ledger)
        ledger["peak_fft_length"] = max(ledger["peak_fft_length"], size)
        if j <= c:
            old = low
            low = [(old[k % len(old)] + table[k]) % p for k in range(size)]
            ledger["low_merge_additions"] += size
            if j == c:
                y = [low[k % size] for k in range(n)]
                ledger["output_initial_writes"] = n
        else:
            stride = 1 << (j - c)
            for q in range(n // stride):
                k = stride * q
                y[k] = (y[k] + table[q % size]) % p
                ledger["high_scatter_additions"] += 1
    assert y is not None
    return y, ledger


def candidate_representatives(x, c, omega, p):
    """Fresh implementation of the frozen note's exact reconstruction formula."""
    n = len(x)
    t = n.bit_length() - 1
    if not t:
        return [x[0] % p]
    c = max(c, 1)
    check_root(omega, c, p)
    powers = [1]
    for _ in range((1 << c) - 1):
        powers.append(powers[-1] * omega % p)
    tables = {}
    fft_ledger = {"fft_additions": 0, "fft_multiplications_including_identity": 0}
    for j in range(1, t + 1):
        size = 1 << min(j, c)
        bucket = [0] * size
        for u in range(1, 1 << j, 2):
            bucket[u % size] = (bucket[u % size] + x[(n >> j) * u]) % p
        tables[j] = short_fft(bucket, powers, p, fft_ledger)
    prefix = [x[0] % p]
    for j in range(1, t + 1):
        prefix.append((prefix[-1] + tables[j][0]) % p)
    y = [None] * n
    y[0] = prefix[-1]
    for ell in range(1, t + 1):
        representative_modulus = 1 << min(ell, c)
        values = {}
        for v in range(1, representative_modulus, 2):
            value = prefix[t - ell]
            for s in range(1, min(ell, c) + 1):
                j = t - ell + s
                index = ((1 << (min(j, c) - s)) * v) % len(tables[j])
                value = (value + tables[j][index]) % p
            values[v] = value
        for u in range(1, 1 << ell, 2):
            y[(n >> ell) * u] = values[u % representative_modulus]
    assert None not in y
    return y


def multiplication_orbits(n, c):
    """Reference definition, not the residue-bucket characterization."""
    h = [a for a in range(n) if a % 2 and (a - 1) % (1 << c) == 0]
    if n == 1:
        return [[0]]
    seen = set()
    result = []
    for k in range(n):
        if k not in seen:
            orbit = sorted({k * a % n for a in h})
            seen.update(orbit)
            result.append(orbit)
    assert len(seen) == n
    return result


def project(v, orbits, p):
    y = [None] * len(v)
    for orbit in orbits:
        avg = sum(v[k] for k in orbit) * pow(len(orbit), -1, p) % p
        for k in orbit:
            y[k] = avg
    return y


def direct_dft(x, root, p):
    n = len(x)
    return [sum(value * pow(root, j * k, p) for j, value in enumerate(x)) % p
            for k in range(n)]


def square_extension_controls():
    """Base fields without primitive Nth roots: F3(i), F5(sqrt(2))."""
    results = []
    for p, non_square, c, zeta in [(3, 2, 1, (1, 1)), (5, 2, 2, (0, 1))]:
        def add(a, b):
            return ((a[0] + b[0]) % p, (a[1] + b[1]) % p)

        def mul(a, b):
            return ((a[0] * b[0] + non_square * a[1] * b[1]) % p,
                    (a[0] * b[1] + a[1] * b[0]) % p)

        def power(a, k):
            result = (1, 0)
            while k:
                if k & 1:
                    result = mul(result, a)
                a = mul(a, a)
                k >>= 1
            return result

        assert all(k * k % p != non_square for k in range(p))
        assert power(zeta, 8) == (1, 0) and power(zeta, 4) != (1, 0)
        omega_pair = power(zeta, 8 // (1 << c))
        assert omega_pair[1] == 0
        orbits = multiplication_orbits(8, c)
        vectors = [[int(i == j) for i in range(8)] for j in range(8)]
        vectors += [[(i * i + 2 * i + 1) % p for i in range(8)]]
        for x in vectors:
            f = []
            for k in range(8):
                value = (0, 0)
                for j in range(8):
                    value = add(value, mul((x[j], 0), power(zeta, j * k)))
                f.append(value)
            projected = [None] * 8
            for orbit in orbits:
                total = (0, 0)
                for k in orbit:
                    total = add(total, f[k])
                avg = mul(total, (pow(len(orbit), -1, p), 0))
                for k in orbit:
                    projected[k] = avg
            y, _ = candidate(x, c, omega_pair[0], p)
            assert projected == [(v, 0) for v in y]
        assert (p - 1) % 8 != 0
        results.append({"base_prime": p, "extension_polynomial": f"X^2-{non_square}",
                        "N": 8, "cutoff": c, "base_cutoff_root": omega_pair[0],
                        "base_has_primitive_Nth_root": False,
                        "vectors_checked": len(vectors), "pass": True})
    return results


def characteristic_zero_coefficient_controls():
    """Exact full matrices in Z[z]/(z^(N/2)+1), with rational averages.

    Compare subgroup-averaged DFT coefficients with the independently derived
    zero-or-root coefficient formula. Integer cross multiplication verifies the
    average, without numerical approximation or a finite-field reduction.
    """
    cases = []
    for t in range(1, 7):
        n = 1 << t
        degree = n // 2
        for c in range(t + 1):
            h_group = [a for a in range(1, n, 2) if (a - 1) % (1 << c) == 0]
            m_cutoff = max(1, c)
            for original_index in range(n):
                if original_index:
                    valuation = (original_index & -original_index).bit_length() - 1
                    j = t - valuation
                    unit = original_index >> valuation
                    m = min(j, m_cutoff)
                    orbit_size = 1 << (j - m)
                    residue = unit % (1 << m)
                for k in range(n):
                    actual = [0] * degree
                    for a in h_group:
                        e = (a * original_index * k) % n
                        actual[e % degree] += 1 if e < degree else -1
                    expected = [0] * degree
                    if not original_index:
                        expected[0] = len(h_group)
                    elif k % orbit_size == 0:
                        e = ((n >> m) * (k // orbit_size) * residue) % n
                        expected[e % degree] = len(h_group) * (1 if e < degree else -1)
                    assert actual == expected, ("characteristic_zero", t, c, original_index, k)
            cases.append({"t": t, "C": c, "entries": n * n})
    return {"status": "PASS", "ring": "Z[z]/(z^(N/2)+1); exact cross-multiplied rational averages",
            "parameter_cases": len(cases), "matrix_entries": sum(v["entries"] for v in cases),
            "cases": cases}


def main():
    rng = random.Random(331033)
    basis_cases, random_cases, count_cases = [], [], []
    entries = 0
    # Every root is a supplied, deterministic test fixture, never searched for.
    for p, generator, max_t in [(17, 3, 4), (97, 5, 5), (257, 3, 7), (65537, 3, 6)]:
        for t in range(max_t + 1):
            n = 1 << t
            zeta = pow(generator, (p - 1) // n, p)
            check_root(zeta, t, p)
            columns = [[pow(zeta, j * k, p) for k in range(n)] for j in range(n)]
            for c in range(t + 1):
                effective_c = max(1, c) if t else 0
                omega = pow(zeta, n // (1 << effective_c), p)
                orbits = multiplication_orbits(n, c)
                rank = 1 if not t else ((t + 1) if c == 0 else
                       (1 << c) + (t - c) * (1 << (c - 1)))
                assert len(orbits) == rank
                for j in range(n):
                    x = [int(i == j) for i in range(n)]
                    y, ledger = candidate(x, c, omega, p)
                    assert y == project(columns[j], orbits, p), (p, t, c, j)
                    assert candidate_representatives(x, c, omega, p) == y, ("representatives", p, t, c, j)
                    entries += n
                basis_cases.append({"p": p, "t": t, "C": c, "rank": rank,
                                    "basis_vectors": n, "entries": n * n})
                if t:
                    m = effective_c
                    fft_work = sum(min(m, j) * (1 << min(m, j)) for j in range(1, t + 1))
                    assert ledger["input_reads"] == n
                    assert ledger["bucket_additions"] == n - 1
                    assert ledger["fft_additions"] == fft_work
                    assert ledger["fft_multiplications_including_identity"] == fft_work // 2
                    assert ledger["low_merge_additions"] == (1 << (m + 1)) - 2
                    assert ledger["high_scatter_additions"] == n - (1 << m)
                    assert ledger["output_initial_writes"] == n
                    count_cases.append({"p": p, "t": t, "C": c, **ledger})
                for _ in range(2):
                    x = [rng.randrange(p) for _ in range(n)]
                    y, _ = candidate(x, c, omega, p)
                    fx = direct_dft(x, zeta, p)
                    assert y == project(fx, orbits, p)
                    assert y == direct_dft(project(x, orbits, p), zeta, p)
                    assert candidate_representatives(x, c, omega, p) == y
                random_cases.append({"p": p, "t": t, "C": c, "vectors": 2})

    # Larger dense controls, direct DFT rather than a second FFT oracle.
    for t in [8, 9]:
        p, g = 65537, 3
        n = 1 << t
        zeta = pow(g, (p - 1) // n, p)
        x = [rng.randrange(p) for _ in range(n)]
        fx = direct_dft(x, zeta, p)
        for c in range(t + 1):
            omega = pow(zeta, n // (1 << max(1, c)), p)
            y, _ = candidate(x, c, omega, p)
            assert y == project(fx, multiplication_orbits(n, c), p)
            assert candidate_representatives(x, c, omega, p) == y
            random_cases.append({"p": p, "t": t, "C": c, "vectors": 1})

    # Negative controls: wrong orientation, omitted orbit-sum scale, and bad root.
    p, t, c = 257, 5, 3
    n = 1 << t
    zeta = pow(3, (p - 1) // n, p)
    omega = pow(zeta, n // (1 << c), p)
    x = [0] * n
    x[1] = 1
    truth = project(direct_dft(x, zeta, p), multiplication_orbits(n, c), p)
    wrong_sign, _ = candidate(x, c, pow(omega, -1, p), p)
    assert wrong_sign != truth
    # Multiplying all shell-t bucket sums by this scale reproduces averaging
    # without restoring the geometric-sum orbit size, for this one-shell input.
    correct, _ = candidate(x, c, omega, p)
    omitted_scale = [v * pow(1 << (t - c), -1, p) % p for v in correct]
    assert omitted_scale != truth
    rejected = False
    try:
        candidate(x, c, 1, p)
    except ValueError:
        rejected = True
    assert rejected

    result = {
        "status": "PASS",
        "independence": "Fresh standard-library controls; no author or submitted program executed/imported.",
        "basis_parameter_cases": len(basis_cases),
        "basis_vectors": sum(v["basis_vectors"] for v in basis_cases),
        "basis_output_entries": entries,
        "reconstruction_variants": ["frozen_note_representatives", "independent_nested_support_streaming"],
        "dense_parameter_cases": len(random_cases),
        "dense_vectors": sum(v["vectors"] for v in random_cases),
        "basis_cases": basis_cases, "dense_cases": random_cases,
        "operation_ledger_cases": count_cases,
        "characteristic_zero_coefficients": characteristic_zero_coefficient_controls(),
        "root_limited_extension_controls": square_extension_controls(),
        "negative_controls": {"wrong_Fourier_sign_detected": True,
                              "omitted_orbit_size_detected": True,
                              "nonprimitive_root_rejected": True},
        "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    out = Path(__file__).with_name("fresh_results.json")
    out.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in
                     {"basis_cases", "dense_cases", "operation_ledger_cases"}}, indent=2))


if __name__ == "__main__":
    main()
