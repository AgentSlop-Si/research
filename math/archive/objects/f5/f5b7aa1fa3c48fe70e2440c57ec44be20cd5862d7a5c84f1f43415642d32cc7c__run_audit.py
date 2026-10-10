"""Focused exact correctness, rejection, and operation-count audit."""

from collections import Counter
import json
from pathlib import Path
import random

from tensor_sideinfo import certify, evaluate, transform


def direct_dft(values, modulus, omega):
    n = len(values)
    return [sum(value * pow(omega, j * k, modulus) for j, value in enumerate(values)) % modulus
            for k in range(n)]


def fft_reference(values, modulus, omega):
    """Independent recursive radix-two reference; never used by the candidate."""
    n = len(values)
    if n == 1:
        return list(values)
    even = fft_reference(values[::2], modulus, omega * omega % modulus)
    odd = fft_reference(values[1::2], modulus, omega * omega % modulus)
    out = [0] * n
    power = 1
    for k in range(n // 2):
        term = power * odd[k] % modulus
        out[k] = (even[k] + term) % modulus
        out[k + n // 2] = (even[k] - term) % modulus
        power = power * omega % modulus
    return out


def synthesize(factors, scale, modulus):
    values = [scale]
    for a0, a1 in factors:
        values = [a0 * value % modulus for value in values] + [a1 * value % modulus for value in values]
    return values


def main():
    randomizer = random.Random(20261009)
    exact_cases = 0
    declined_cases = 0
    invalid_cases = 0
    count_records = []
    for modulus, generator, max_log in [(17, 3, 4), (97, 5, 5), (65537, 3, 12)]:
        for d in range(max_log + 1):
            n = 1 << d
            omega = pow(generator, (modulus - 1) // n, modulus)
            examples = [[0] * n, [1] * n]
            if n <= 32:
                examples.extend([[int(j == k) for j in range(n)] for k in range(n)])
            for _ in range(3):
                factors = [(randomizer.randrange(modulus), randomizer.randrange(modulus)) for _ in range(d)]
                examples.append(synthesize(factors, randomizer.randrange(1, modulus), modulus))
            for values in examples:
                counts = Counter()
                observed = transform(values, modulus, omega, counts)
                assert observed is not None
                expected = direct_dft(values, modulus, omega) if n <= 32 else fft_reference(values, modulus, omega)
                assert observed == expected, (modulus, n, values)
                exact_cases += 1
                if any(values):
                    assert counts["field_multiplications"] == (0 if n == 1 else 6 * n - 7 + 2 * d)
                    assert counts["field_additions"] == 2 * n - 2
                    assert counts["certificate_multiplications"] == n - 1
                    assert counts["exact_equality_checks"] == n
                    assert counts["field_inversions"] == int(n > 1)
            if d >= 2:
                # A single altered non-pivot/non-neighbor coordinate destroys
                # the tensor identity, while retaining a dense fresh input.
                values = [1] * n
                values[-1] = 2
                counts = Counter()
                assert transform(values, modulus, omega, counts) is None
                assert not counts["root_preparation_multiplications"]
                assert not counts["evaluation_multiplications"]
                declined_cases += 1
            if modulus == 65537:
                values = synthesize([(1, randomizer.randrange(1, modulus)) for _ in range(d)], 7, modulus)
                counts = Counter()
                result = transform(values, modulus, omega, counts)
                assert result == fft_reference(values, modulus, omega)
                exact_cases += 1
                count_records.append({"n": n, "counts": dict(sorted(counts.items()))})

    # Composite-ring positive control: 2 has principal order eight mod 17,
    # and 4 has principal order eight mod 257; combine these by exact CRT.
    modulus = 17 * 257
    omega = next(x for x in range(modulus) if x % 17 == 2 and x % 257 == 4)
    values = synthesize([(1, 2), (3, 4), (5, 6)], 1, modulus)
    assert transform(values, modulus, omega) == direct_dft(values, modulus, omega)
    exact_cases += 1

    for callback in [
        lambda: transform([], 17, 1),
        lambda: transform([0, 0, 0], 17, 1),
        lambda: transform([True, 1], 17, 16),
        lambda: transform([17, 1], 17, 16),
        lambda: transform([1, 1], 16, 15),
        lambda: transform([1, 1], 17, 1),
        lambda: transform([1], 17, 2),
        lambda: certify([3, 3], 15),
    ]:
        try:
            callback()
        except ValueError:
            invalid_cases += 1
        else:
            raise AssertionError("invalid input accepted")

    result = {
        "status": "PASS", "exact_full_output_cases": exact_cases,
        "unstructured_declines": declined_cases, "invalid_input_cases": invalid_cases,
        "count_records": count_records,
        "scope": "fresh verified binary-index rank-one tensors; no arbitrary-input FFT claim",
    }
    destination = Path(__file__).with_name("results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({key: value for key, value in result.items() if key != "count_records"}, indent=2))


if __name__ == "__main__":
    main()
