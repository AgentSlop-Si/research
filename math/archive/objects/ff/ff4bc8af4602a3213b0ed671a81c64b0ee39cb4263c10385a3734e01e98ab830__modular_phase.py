"""Fourier phase rows with exact integer exponent reduction before float conversion."""
import numpy as np

_SAFE_N = 3037000499  # floor(sqrt(int64 max)); products of residues fit below this.


def phase_row(n, multiplier, indices):
    """Return exp(-2 pi i * multiplier * indices / n), reducing modulo n first.

    The object-integer path prevents overflow for very large logical periods.
    It is slower, but selected-frequency callers need not allocate length-n data.
    """
    n = int(n)
    if n < 1:
        raise ValueError('n must be positive')
    a = np.asarray(indices)
    if a.ndim != 1:
        raise ValueError('indices must be one-dimensional')
    multiplier = int(multiplier) % n
    if n <= _SAFE_N:
        residues = (np.asarray(a, dtype=np.int64) % n * multiplier) % n
    else:
        residues = np.fromiter(((int(k) % n * multiplier) % n for k in a),
                               dtype=np.float64, count=len(a))
    return np.exp((-2j * np.pi / n) * residues.astype(np.float64))
