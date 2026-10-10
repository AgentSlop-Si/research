"""Independent O(N)-setup/O(N)-apply finite-field rotation reference.

This is an audit remediation example, not a Fourier evaluator. It imports no
uploaded code. The caller supplies a primitive Nth root for N divisible by 4.
Field setup/root generation and Python integer bit costs are separate.
"""


def prepare_rotation(n, modulus, omega):
    if n < 4 or n % 4:
        raise ValueError('N must be a positive multiple of 4, at least 4')
    if pow(omega, n, modulus) != 1:
        raise ValueError('supplied root does not satisfy omega^N=1')
    negative_i = pow(omega, n//4, modulus)
    if negative_i*negative_i % modulus != modulus-1:
        raise ValueError('supplied root does not have the required fourth power phase')
    inverse_omega = pow(omega, -1, modulus)
    positive_i = pow(negative_i, -1, modulus)
    half = pow(2, -1, modulus)
    half_over_i = pow(2*positive_i, -1, modulus)
    forward = backward = 1
    coefficients = []
    for _ in range(1, n//2):
        forward = forward*omega % modulus
        backward = backward*inverse_omega % modulus
        coefficients.append(((forward+backward)*half % modulus,
                             (backward-forward)*half_over_i % modulus))
    return n, modulus, tuple(coefficients)


def apply_rotation(prepared, vector):
    n, modulus, coefficients = prepared
    if len(vector) != n:
        raise ValueError('incorrect vector length')
    out = [0]*n
    out[0], out[1] = vector[0] % modulus, -vector[1] % modulus
    for j, (co, si) in enumerate(coefficients, start=1):
        a, b = j+1, n//2+j
        out[a] = (co*vector[a]-si*vector[b]) % modulus
        out[b] = (si*vector[a]+co*vector[b]) % modulus
    return out
