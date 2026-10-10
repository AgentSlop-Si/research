"""Independent all-z transform for a supplied permuted geometric input.

Returns all unnormalized DFT bins, with F[k,j] = omega**(k*j).
Prerequisites: p is a known odd prime, N is dyadic, omega is supplied as a
primitive Nth root. The root is verified; choosing p and constructing omega
are separate, explicitly charged prerequisites. No dense Fourier matrix,
permutation sort, linear solve, or N-by-N transform is used here.

Cost after field/root selection: O(N(s+1)) additions/multiplications, one
field inversion, O(N) stored field/index words, where s counts successor
mismatches versus the ordinary cyclic shift. This is a restricted-input
algorithm, not an arbitrary-input faster FFT. Constant-size field operations
are not constant-time bit operations when p grows.
"""


def permuted_geometric_dft(order, z, p, omega):
    n = len(order)
    if n < 2 or n & (n-1):
        raise ValueError('dyadic length N >= 2 required')
    if p <= 2 or (p-1) % n:
        raise ValueError('known odd prime with N dividing p-1 required')
    z, omega = z % p, omega % p
    if pow(omega, n, p) != 1 or pow(omega, n//2, p) == 1:
        raise ValueError('omega must have exact order N')
    seen = [False]*n
    for j in order:
        if not isinstance(j, int) or j < 0 or j >= n or seen[j]:
            raise ValueError('order must permute 0,...,N-1')
        seen[j] = True
    successor = [0]*n
    for t in range(n):
        successor[order[t]] = order[(t+1) % n]
    x, power = [0]*n, 1
    for j in order:
        x[j] = power
        power = power*z % p
    # At this point power == z**N. No separate exponentiation is needed.
    d = [0]*n
    d[order[0]] = (1-power) % p
    for j, wj in enumerate(successor):
        zj = (j+1) % n
        if wj != zj:
            contribution = z*x[j] % p
            d[wj] = (d[wj]+contribution) % p
            d[zj] = (d[zj]-contribution) % p
    roots, power = [], 1
    for _ in range(n):
        roots.append(power)
        power = power*omega % p
    numerator = [0]*n
    for j, value in enumerate(d):
        if not value:
            continue
        step, power = roots[j], 1
        for k in range(n):
            numerator[k] = (numerator[k]+value*power) % p
            power = power*step % p
    denominators = [(1-z*r) % p for r in roots]
    regular = [k for k, value in enumerate(denominators) if value]
    exceptional = [k for k, value in enumerate(denominators) if not value]
    if len(exceptional) > 1:
        raise ArithmeticError('root or field prerequisites violated')
    prefix = [1]
    for k in regular:
        prefix.append(prefix[-1]*denominators[k] % p)
    back = pow(prefix[-1], -1, p)
    output = [0]*n
    for t in range(len(regular)-1, -1, -1):
        k = regular[t]
        output[k] = numerator[k]*back*prefix[t] % p
        back = back*denominators[k] % p
    for k in exceptional:
        step, power, value = roots[k], 1, 0
        for a in x:
            value = (value+a*power) % p
            power = power*step % p
        output[k] = value
    return output
