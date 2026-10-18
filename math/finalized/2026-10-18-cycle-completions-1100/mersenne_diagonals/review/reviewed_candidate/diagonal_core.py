"""Fresh width-adaptive Mersenne Taylor-shift arithmetic core.

No historical implementation is imported. Wide represented multiplication is
explicit difference-form Karatsuba. Python host timings are not the bit model.
"""

LEAF = 16


def kmul(x, y):
    if x < 0 or y < 0:
        value = kmul(abs(x), abs(y))
        return -value if (x < 0) != (y < 0) else value
    t = max(x.bit_length(), y.bit_length())
    if t <= LEAF:
        z = 0
        while y:
            if y & 1:
                z += x
            x <<= 1
            y >>= 1
        return z
    h = (t + 1) // 2
    mask = (1 << h) - 1
    x0, x1, y0, y1 = x & mask, x >> h, y & mask, y >> h
    z0, z2 = kmul(x0, y0), kmul(x1, y1)
    dx, dy = x1 - x0, y1 - y0
    zd = kmul(abs(dx), abs(dy))
    if (dx < 0) != (dy < 0):
        zd = -zd
    return z0 + ((z0 + z2 - zd) << h) + (z2 << (2 * h))


def inverse_odd(u, t):
    assert u > 0 and u & 1 and t >= 1
    v, p = 1, 1
    while p < t:
        p = min(2 * p, t)
        mask = (1 << p) - 1
        # Both calls use at most p-bit arguments.
        correction = (2 - (kmul(u & mask, v) & mask)) & mask
        v = kmul(v, correction) & mask
    return v


def _buffers(x, W, t):
    assert x >= 0 and x.bit_length() <= W and W >= 1 and t >= 8 and t % 8 == 0
    q = (W + t - 1) // t
    step = t // 8
    raw = x.to_bytes(q * step, "little")
    return raw, bytearray(q * step), q, step


def stream_mul(x, k, W, t, product=kmul):
    """Return x*k mod 2**W; k has at most t bits; scan bounded byte windows."""
    assert 0 <= k < 1 << t
    raw, out, q, step = _buffers(x, W, t)
    mask, carry = (1 << t) - 1, 0
    for j in range(q):
        a = int.from_bytes(raw[j * step:(j + 1) * step], "little")
        z = product(a, k) + carry
        out[j * step:(j + 1) * step] = (z & mask).to_bytes(step, "little")
        carry = z >> t
    return int.from_bytes(out, "little") & ((1 << W) - 1)


def stream_div_odd(x, u, W, t, v=None, product=kmul):
    """Return x/u mod 2**W, by low-to-high modular division, with 0<=carry<u."""
    assert 0 < u < 1 << t and u & 1
    if v is None:
        v = inverse_odd(u, t)
    raw, out, q, step = _buffers(x, W, t)
    mask, carry = (1 << t) - 1, 0
    for j in range(q):
        a = int.from_bytes(raw[j * step:(j + 1) * step], "little")
        b = product((a - carry) & mask, v) & mask
        z = product(u, b) + carry - a
        carry = z >> t
        out[j * step:(j + 1) * step] = b.to_bytes(step, "little")
    return int.from_bytes(out, "little") & ((1 << W) - 1)


def odd_part(i):
    assert i >= 1
    return i >> ((i & -i).bit_length() - 1)


def parameters(n, h):
    assert n >= 1 and h >= 0
    g = (n - 1).bit_length()
    H = h + n + 1
    W = H + g
    Bn = max(1, (n - 1) * g)
    B = min(W, Bn)
    t = 8 * ((B + 7) // 8)
    return H, g, W, Bn, B, t


def tables(n, W, t):
    """Small representatives U, their micro-inverses v, and W-bit inverses V."""
    mask_t, mask_W = (1 << t) - 1, (1 << W) - 1
    short_t = 8 * ((max(1, (n - 1).bit_length()) + 7) // 8)
    U = [1]
    for i in range(1, n):
        U.append(stream_mul(U[-1], odd_part(i), t, short_t))
    v = [0] * n
    v[-1] = inverse_odd(U[-1], t)
    for i in range(n - 1, 0, -1):
        v[i - 1] = stream_mul(v[i], odd_part(i), t, short_t)
    V = [0] * n
    if W <= t:
        for i in range(n):
            V[i] = v[i] & mask_W
    else:
        V[-1] = stream_div_odd(1, U[-1], W, t, v[-1])
        for i in range(n - 1, 0, -1):
            V[i - 1] = stream_mul(V[i], odd_part(i), W, short_t)
    return U, v, V


def packed_convolution(a, b, W, product=kmul):
    n = len(a)
    assert n == len(b) and n >= 1
    guard = (n - 1).bit_length()
    slot_bytes = (2 * W + guard + 7) // 8
    left = b"".join(x.to_bytes(slot_bytes, "little") for x in a)
    right = b"".join(x.to_bytes(slot_bytes, "little") for x in b)
    p = product(int.from_bytes(left, "little"), int.from_bytes(right, "little"))
    raw = p.to_bytes(2 * n * slot_bytes, "little")
    mask = (1 << W) - 1
    return [int.from_bytes(raw[i * slot_bytes:(i + 1) * slot_bytes], "little") & mask
            for i in range(2 * n - 1)]


def shift(a, sigma=1, h=None, convolution_product=kmul):
    assert sigma in (-1, 1)
    if not a:
        return []
    if h is None:
        h = max(abs(x).bit_length() for x in a)
    assert all(abs(x) < 1 << h for x in a)
    n = len(a)
    if n == 1:
        return list(a)
    H, g, W, Bn, B, t = parameters(n, h)
    U, v, V = tables(n, W, t)
    mask = (1 << W) - 1
    A, J = [], []
    for i, x in enumerate(a):
        scaled = stream_mul(x & mask, U[i], W, t)
        A.append((scaled << (g - i.bit_count())) & mask)
        z = (V[i] << i.bit_count()) & mask
        J.append((-z if sigma < 0 and i & 1 else z) & mask)
    D = packed_convolution(A[::-1], J, W, convolution_product)
    result = []
    for j in range(n):
        z = stream_div_odd(D[n - 1 - j], U[j], W, t, v[j])
        R = (z << j.bit_count()) & mask
        assert R & ((1 << g) - 1) == 0
        y = R >> g
        if y >= 1 << (H - 1):
            y -= 1 << H
        result.append(y)
    return result
