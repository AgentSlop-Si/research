"""Exact full DFT of a freshly verified binary-index rank-one tensor.

The implementation uses modular scalar arithmetic.  It accepts an odd modulus,
a supplied principal dyadic root, and a unit pivot.  In particular, every
nonzero input over an odd prime field has an eligible first nonzero pivot.
No Fourier backend is called by the candidate.
"""

from collections import Counter
from dataclasses import dataclass


def _mul(a, b, modulus, counts, stage):
    counts[stage + "_multiplications"] += 1
    counts["field_multiplications"] += 1
    return a * b % modulus


@dataclass(frozen=True)
class TensorCertificate:
    n: int
    modulus: int
    pivot: int
    scale: int
    factors: tuple


def certify(values, modulus, counts=None):
    """Return an exact tensor certificate, or None for an unstructured input.

    A nonunit first nonzero pivot raises ValueError, rather than incorrectly
    declining or claiming a certificate.  Prime moduli avoid this case.
    """
    if counts is None:
        counts = Counter()
    if not isinstance(modulus, int) or isinstance(modulus, bool) or modulus < 3 or not modulus & 1:
        raise ValueError("modulus must be an odd integer at least three")
    n = len(values)
    if n < 1 or n & (n - 1):
        raise ValueError("length must be a positive power of two")
    pivot = None
    for j, value in enumerate(values):
        counts["validation_input_reads"] += 1
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value < modulus:
            raise ValueError("inputs must be canonical integer residues")
        if pivot is None and value:
            pivot = j
    d = n.bit_length() - 1
    if pivot is None:
        counts["accepted_zero_inputs"] += 1
        return TensorCertificate(n, modulus, 0, 0, ((1, 1),) * d)
    scale = values[pivot]
    counts["pivot_reads"] += 1
    factors = []
    ratios = []
    if d:
        try:
            inverse = pow(scale, -1, modulus)
        except ValueError as exc:
            raise ValueError("the first nonzero pivot must be a unit") from exc
        counts["field_inversions"] += 1
    for bit in range(d):
        counts["neighbor_input_reads"] += 1
        ratio = _mul(values[pivot ^ (1 << bit)], inverse, modulus, counts, "factor")
        ratios.append(ratio)
        factors.append((ratio, 1) if pivot & (1 << bit) else (1, ratio))
    generated = [scale]
    counts["certificate_values_written"] += 1
    for ratio in ratios:
        size = len(generated)
        for j in range(size):
            counts["certificate_values_read"] += 1
            generated.append(_mul(generated[j], ratio, modulus, counts, "certificate"))
            counts["certificate_values_written"] += 1
    for mask, value in enumerate(generated):
        counts["verification_input_reads"] += 1
        counts["exact_equality_checks"] += 1
        counts["verification_index_xors"] += 1
        if values[pivot ^ mask] != value:
            counts["declined_inputs"] += 1
            return None
    counts["accepted_nonzero_inputs"] += 1
    return TensorCertificate(n, modulus, pivot, scale, tuple(factors))


def root_powers(n, modulus, omega, counts):
    """Validate a supplied dyadic root and build its charged N-entry table.

    For N>1, omega**(N/2) == -1 suffices for a principal N-th root over
    every odd residue ring.  This check does not assume primality.
    """
    if not isinstance(omega, int) or isinstance(omega, bool) or not 0 <= omega < modulus:
        raise ValueError("root must be a canonical integer residue")
    d = n.bit_length() - 1
    if n == 1:
        if omega != 1:
            raise ValueError("the length-one root must equal one")
    else:
        half_power = omega
        for _ in range(d - 1):
            half_power = _mul(half_power, half_power, modulus, counts, "root_validation")
        if half_power != modulus - 1:
            raise ValueError("the supplied root is not a principal dyadic root")
    powers = [1]
    for _ in range(1, n):
        powers.append(_mul(powers[-1], omega, modulus, counts, "root_preparation"))
    counts["root_table_values_written"] += n
    return powers


def evaluate(certificate, omega, counts=None):
    """Evaluate every DFT coordinate of a trusted internally issued certificate.

    Certificate objects are not authenticated against manual field edits.
    The safe fresh-input entry point below constructs its own certificate.
    """
    if counts is None:
        counts = Counter()
    n, modulus = certificate.n, certificate.modulus
    powers = root_powers(n, modulus, omega, counts)
    if not certificate.scale:
        counts["final_output_values_written"] += n
        return [0] * n
    suffix = [certificate.scale]
    for bit in range(len(certificate.factors) - 1, -1, -1):
        a0, a1 = certificate.factors[bit]
        size = 1 << (len(certificate.factors) - bit)
        half = size >> 1
        values = []
        for k in range(size):
            counts["root_table_reads"] += 1
            counts["twiddle_index_shifts"] += 1
            factor = (_mul(a1, powers[k << bit], modulus, counts, "evaluation") + a0) % modulus
            counts["field_additions"] += 1
            counts["suffix_values_read"] += 1
            counts["suffix_index_masks"] += 1
            value = _mul(factor, suffix[k & (half - 1)], modulus, counts, "evaluation")
            values.append(value)
            counts["stage_values_written"] += 1
        suffix = values
    counts["final_output_values_returned"] += n
    return suffix


def transform(values, modulus, omega, counts=None):
    """Verify the fresh original input and return its full exact DFT, or None."""
    if counts is None:
        counts = Counter()
    certificate = certify(values, modulus, counts)
    if certificate is None:
        return None
    return evaluate(certificate, omega, counts)
