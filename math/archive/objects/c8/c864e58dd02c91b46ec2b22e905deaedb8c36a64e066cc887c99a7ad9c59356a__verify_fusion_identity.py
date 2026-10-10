"""Independent exact modular checks of both periodic fusion identities.

This checks algebra and residual fitting; it does not exercise the approximate
sampler. Gaussian integers are embedded consistently in F_97, whose roots
support every tested length. No general FFT is called.
"""
import hashlib
import json
import math
import random
from pathlib import Path


def rotate(pair, quarter_turns):
    a, b = pair
    return ((a, b), (-b, a), (-a, -b), (b, -a))[quarter_turns % 4]


def mass(xs):
    return sum(abs(a) + abs(b) for a, b in xs)


def nearest(a, b):
    return (a + b // 2) // b if a >= 0 else -((-a + b // 2) // b)


def fit(xs, scaled):
    N = len(xs)
    q = math.gcd(N, 4)
    n = N // q
    coefficients = [[0, 0] for _ in range(q)]
    factor = n if scaled else 1
    for s in range(q):
        for c in range(2):
            values = [xs[j][c] for j in range(s, N, q)]
            total = sum(values)
            proposal = total if scaled else nearest(total, n)
            loss = sum(abs(factor * v - proposal) for v in values)
            if loss <= factor * sum(abs(v) for v in values):
                coefficients[s][c] = proposal
    residual = [tuple(factor * xs[j][c] - coefficients[j % q][c] for c in range(2))
                for j in range(N)]
    spectral = [(0, 0)] * N
    # Scaled means have a cancellation of n in their short Fourier spectrum.
    amplitude = 1 if scaled else n
    for t in range(q):
        pairs = [rotate(coefficients[s], -4 * s * t // q) for s in range(q)]
        spectral[t * n] = tuple(amplitude * sum(v[c] for v in pairs) for c in range(2))
    return residual, spectral, factor


def dft_mod(xs):
    p, generator, N = 97, 5, len(xs)
    assert 96 % N == 0
    root = pow(generator, 96 // N, p)
    imaginary_unit = pow(generator, 24, p)
    encoded = [(a + imaginary_unit * b) % p for a, b in xs]
    return [sum(x * pow(root, (-j * m) % N, p) for j, x in enumerate(encoded)) % p
            for m in range(N)]


def main():
    rng = random.Random(87344)
    cases = 0
    coordinates = 0
    by_mode = {"rounded_mean": 0, "scaled_exact_mean": 0}
    for N in (1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 96):
        q = math.gcd(N, 4)
        for trial in range(10):
            pattern = [(rng.randrange(-30, 31), rng.randrange(-30, 31)) for _ in range(q)]
            noise = [(0, 0) if trial == 0 else (rng.randrange(-9, 10), rng.randrange(-9, 10)) for _ in range(N)]
            xs = [tuple(pattern[j % q][c] + noise[j][c] for c in range(2)) for j in range(N)]
            expected = dft_mod(xs)
            for scaled in (False, True):
                residual, spectral, factor = fit(xs, scaled)
                assert mass(residual) <= factor * mass(xs)
                comparison_factor = 2 if scaled else 3
                assert mass(residual) <= comparison_factor * factor * mass(noise)
                if trial == 0:
                    assert mass(residual) == 0
                correction = dft_mod(residual)
                inv = pow(factor, -1, 97)
                imaginary_unit = pow(5, 24, 97)
                got = [(a + imaginary_unit * b + inv * y) % 97
                       for (a, b), y in zip(spectral, correction)]
                assert got == expected
                cases += 1
                coordinates += N
                by_mode["scaled_exact_mean" if scaled else "rounded_mean"] += 1
    report = {"status": "PASS", "exact_identity_cases": cases,
              "exact_output_coordinates": coordinates, "cases_by_mode": by_mode,
              "field": 97, "lengths": [1, 2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 96],
              "checks": ["negative-sign Fourier identity", "Gaussian-integer quarter-turn support",
                         "residual mass no worse than original", "near-periodic factor-three and factor-two bounds",
                         "exact periodic residual vanishes"],
              "scope": "Independent fitting/algebra checks; approximate integration is tested separately.",
              "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    Path("identity_results.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: report[k] for k in ("status", "exact_identity_cases", "exact_output_coordinates")}))


if __name__ == "__main__":
    main()
