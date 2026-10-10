"""Finite phasor-table decoder with bounded-word guarded lane addition.

This is a functional prototype, not a fast Python FFT. ``eager`` charges a cold,
complete first table. ``lazy`` is only a functional demonstrator and is never
evidence for the cold asymptotic theorem. Samples use phase 0,1,2,3 = 1,i,-1,-i.
Returned integer pairs divided by ``denominator`` are the algorithmic outputs;
Python complex values are a convenience conversion after the algorithm.
"""

from collections import Counter
from math import ceil, factorial, log2, pi, sqrt


def _power_two_at_least(n):
    return 1 << (max(1, ceil(n)) - 1).bit_length()


def _nearest(a, b):
    """Nearest integer to a/b; ties away from zero."""
    if b <= 0:
        raise ValueError("positive denominator required")
    return (a + b // 2) // b if a >= 0 else -((-a + b // 2) // b)


class WordAudit:
    """Check that each explicitly counted arithmetic operand/result is one word.

    Counters record arithmetic and table memory operations, not Python object
    allocations or interpreter instructions. Loop/index/control overhead is
    separately bounded in THEOREM.md and has the same asymptotic cost.
    """

    def __init__(self, width):
        self.width = width
        self.limit = 1 << width
        self.counts = Counter()
        self.max_bits = 0

    def check(self, value, signed=False):
        self.max_bits = max(self.max_bits, abs(value).bit_length())
        bound = self.limit // 2 if signed or value < 0 else self.limit
        if abs(value) >= bound:
            raise OverflowError(f"{abs(value).bit_length()} bits exceeds word {self.width}")
        return value

    def op(self, name, value, *operands):
        signed = value < 0 or any(operand < 0 for operand in operands)
        for operand in operands:
            self.check(operand, signed=signed)
        self.counts[name] += 1
        return self.check(value, signed=signed)

    def rounded(self, a, b):
        self.check(a, signed=a < 0)
        self.check(b, signed=a < 0)
        self.check(abs(a) + b // 2, signed=a < 0)
        self.counts["round_integer_division"] += 1
        return self.check(_nearest(a, b))


def _pi_fixed(P, W):
    """Machin's formula using only integer word operations.

    Internal guard precision bounds accumulated floor error. For P>=8 the
    returned value divided by 2**P differs from pi by less than 2**(-P).
    """
    guard = (128 * (P + 1) ** 2).bit_length()
    R = W.op("shift", 1 << (P + guard))

    def atan(q):
        qpow, total, sign, m = q, 0, 1, 0
        while True:
            denominator = W.op("multiply", qpow * (2 * m + 1), qpow, 2 * m + 1)
            term = W.op("integer_division", R // denominator, R, denominator)
            if term == 0:
                break
            total = W.op("add", total + sign * term, total, term)
            qpow = W.op("multiply", qpow * q * q, qpow, q * q)
            sign, m = -sign, m + 1
        return total

    a, b = atan(5), atan(239)
    value = W.op("add", 16 * a - 4 * b, 16 * a, 4 * b)
    W.counts["multiply"] += 2
    return W.rounded(value, 1 << guard)


def _trig_parameters(bits):
    if bits < 8:
        raise ValueError("trig_bits must be at least 8")
    d = 1
    while 4 ** (d + 1) * 2 ** (bits + 4) > factorial(d + 1):
        d += 1
    P = bits + (256 * (d + 1)).bit_length() + 4
    return d, P


def _phasors(Q, bits, W):
    """Certified fixed-point samples exp(2*pi*i*a/Q), a=0,...,Q-1.

    Complex absolute approximation error is at most 2**(-bits). The Taylor
    degree and working precision depend on requested accuracy only.
    """
    d, P = _trig_parameters(bits)
    S = W.op("shift", 1 << P)
    piS = _pi_fixed(P, W)
    output = []
    for a in range(Q):
        centered = a if 2 * a <= Q else a - Q
        product = W.op("multiply", 2 * piS * centered, 2 * piS, centered)
        theta = W.rounded(product, Q)
        term_re, term_im = S, 0
        total_re, total_im = S, 0
        for n in range(1, d + 1):
            den = W.op("multiply", S * n, S, n)
            new_re = W.rounded(W.op("multiply", -term_im * theta, term_im, theta), den)
            new_im = W.rounded(W.op("multiply", term_re * theta, term_re, theta), den)
            term_re, term_im = new_re, new_im
            total_re = W.op("add", total_re + term_re, total_re, term_re)
            total_im = W.op("add", total_im + term_im, total_im, term_im)
        output.append((total_re, total_im))
        W.counts["table_write"] += 2
    return output, S, {"degree": d, "precision_bits": P, "complex_error_bound": 2.0 ** -bits}


class GuardedDecoder:
    def __init__(self, N, sample_count, *, block_size=4, phase_grid=32,
                 slope_grid=None, group_size=1, lane_step_bits=5,
                 trig_bits=24, word_bits=None, table_mode="eager",
                 max_table_entries=1_000_000):
        B, Q0, g, K = block_size, phase_grid, group_size, sample_count
        Q1 = _power_two_at_least(B * Q0) if slope_grid is None else slope_grid
        if N < 1 or B < 1 or g < 1 or K < 1 or K % g:
            raise ValueError("positive parameters and sample_count divisible by group_size required")
        if Q0 < 4 or Q0 & (Q0 - 1) or Q1 < Q0 or Q1 & (Q1 - 1):
            raise ValueError("phase grids must be powers of two with slope_grid >= phase_grid >= 4")
        if lane_step_bits < 0 or table_mode not in ("eager", "lazy"):
            raise ValueError("invalid rounding precision or table mode")
        self.N, self.K, self.B, self.g, self.G = N, K, B, g, K // g
        self.Q0, self.Q1 = Q0, Q1
        self.H = 1 << lane_step_bits
        self.q0_bits = Q0.bit_length() - 1
        self.p = self.q0_bits + Q1.bit_length() - 1
        self.D = Q0 * Q1
        self.table_entries = self.D ** g
        _, P = _trig_parameters(trig_bits)
        self.r = (2 * self.H * self.G).bit_length()
        default_width = max(4 * max(1, N.bit_length()) + 4 * P + 64,
                            self.p * g + 1, self.r + 1)
        self.w = default_width if word_bits is None else word_bits
        if self.w < max(self.r, self.p * g + 1, 2 * P + 32):
            raise ValueError("word_bits too small for packed keys or certified fixed-point construction")
        self.L = self.w // self.r
        self.words_per_row = (B + self.L - 1) // self.L
        self.mask = (1 << self.r) - 1
        self.W = WordAudit(self.w)
        self.trig, self.S, self.trig_info = _phasors(Q1, trig_bits, self.W)
        self.table_mode = table_mode
        if table_mode == "eager":
            if self.table_entries > max_table_entries:
                raise ValueError("eager table exceeds explicit max_table_entries cap")
            self.table = [None] * self.table_entries
            for key in range(self.table_entries):
                self.table[key] = self._row(key)
        else:
            self.table = {}
        self.cold_counts = dict(self.W.counts)
        self.decoder_bound = pi / Q0 + pi * (B - 1) / Q1 + 2.0 ** -trig_bits + sqrt(2) / (2 * self.H)

    def _row(self, key):
        W = self.W
        descriptors = []
        remaining = key
        for _ in range(self.g):
            descriptor = W.op("bit_and", remaining & (self.D - 1), remaining, self.D - 1)
            remaining = W.op("shift", remaining >> self.p, remaining)
            a0 = W.op("bit_and", descriptor & (self.Q0 - 1), descriptor, self.Q0 - 1)
            a1 = W.op("shift", descriptor >> self.q0_bits, descriptor)
            descriptors.append((a0 * (self.Q1 // self.Q0), a1))
            W.counts["multiply"] += 1
        rows = [[0] * self.words_per_row, [0] * self.words_per_row]
        denominator = W.op("multiply", self.g * self.S, self.g, self.S)
        for t in range(self.B):
            sums = [0, 0]
            for a0, a1 in descriptors:
                exponent = W.op("bit_and", (a0 + t * a1) & (self.Q1 - 1), a0 + t * a1, self.Q1 - 1)
                W.counts["multiply"] += 1
                W.counts["add"] += 1
                pair = self.trig[exponent]
                W.counts["table_read"] += 2
                for c in range(2):
                    sums[c] = W.op("add", sums[c] + pair[c], sums[c], pair[c])
            index, lane = divmod(t, self.L)
            for c in range(2):
                quantized = W.rounded(W.op("multiply", sums[c] * self.H, sums[c], self.H), denominator)
                quantized = min(self.H, max(-self.H, quantized))
                W.counts["comparison"] += 2
                code = W.op("add", quantized + self.H, quantized, self.H)
                shifted = W.op("shift", code << (lane * self.r), code)
                rows[c][index] = W.op("bit_or", rows[c][index] | shifted, rows[c][index], shifted)
        W.counts["table_write"] += 2 * self.words_per_row
        return tuple(rows[0]), tuple(rows[1])

    def decode(self, samples):
        if len(samples) != self.K:
            raise ValueError("sample count differs from constructed decoder")
        if any(not (0 <= j < self.N and phase in (0, 1, 2, 3)) for j, phase in samples):
            raise ValueError("sample indices/phases out of range")
        W = self.W
        start_counts = Counter(W.counts)
        slopes = []
        for j, _ in samples:
            product = W.op("multiply", self.Q1 * j, self.Q1, j)
            slope = W.op("bit_and", -W.rounded(product, self.N) & (self.Q1 - 1), self.Q1 - 1)
            slopes.append(slope)
        outputs = []
        for m0 in range(0, self.N, self.B):
            keys = [0] * self.G
            for i, ((j, phase), slope) in enumerate(zip(samples, slopes)):
                product = W.op("multiply", j * m0, j, m0)
                residue = W.op("remainder", product % self.N, product, self.N)
                scaled = W.op("multiply", self.Q0 * residue, self.Q0, residue)
                start = W.op("bit_and", (phase * (self.Q0 // 4) - W.rounded(scaled, self.N)) & (self.Q0 - 1), self.Q0 - 1)
                W.counts["multiply"] += 1
                W.counts["add"] += 1
                shifted = W.op("shift", slope << self.q0_bits, slope)
                descriptor = W.op("bit_or", start | shifted, start, shifted)
                group, position = divmod(i, self.g)
                packed = W.op("shift", descriptor << (position * self.p), descriptor)
                keys[group] = W.op("bit_or", keys[group] | packed, keys[group], packed)
            sums = [[0] * self.words_per_row, [0] * self.words_per_row]
            for key in keys:
                if self.table_mode == "lazy" and key not in self.table:
                    self.table[key] = self._row(key)
                row = self.table[key]
                for c in range(2):
                    for z in range(self.words_per_row):
                        W.counts["table_read"] += 1
                        sums[c][z] = W.op("packed_word_add", sums[c][z] + row[c][z], sums[c][z], row[c][z])
            for t in range(min(self.B, self.N - m0)):
                z, lane = divmod(t, self.L)
                pair = []
                for c in range(2):
                    shifted = W.op("shift", sums[c][z] >> (lane * self.r), sums[c][z])
                    code = W.op("bit_and", shifted & self.mask, shifted, self.mask)
                    pair.append(W.op("add", code - self.G * self.H, code, self.G * self.H))
                    W.counts["output_write"] += 1
                outputs.append(tuple(pair))
        denominator = self.G * self.H
        online_counts = dict(Counter(W.counts) - start_counts)
        return {
            "values": [complex(a / denominator, b / denominator) for a, b in outputs],
            "integer_outputs": outputs,
            "denominator": denominator,
            "error_bound": self.decoder_bound,
            "counts": {"cold": self.cold_counts, "online": online_counts,
                       "total": dict(W.counts), "max_operand_bits": W.max_bits},
            "parameters": {"N": self.N, "sample_count": self.K, "block_size": self.B,
                           "group_size": self.g, "groups": self.G,
                           "phase_grid": self.Q0, "slope_grid": self.Q1,
                           "descriptor_bits": self.p, "key_bits": self.p * self.g,
                           "word_bits": self.w, "lane_bits": self.r,
                           "lanes_per_word": self.L, "words_per_row_per_component": self.words_per_row,
                           "table_mode": self.table_mode, "possible_table_rows": self.table_entries,
                           "materialized_table_rows": len(self.table), "trig": self.trig_info},
        }


def decode_samples(N, samples, **kwargs):
    return GuardedDecoder(N, len(samples), **kwargs).decode(samples)


def asymptotic_parameters(N, epsilon, gamma=0.5):
    """Explicit theoretical tuning; does not construct its often huge table.

    Returns ``None`` in the finite small-N base regime. Bounds assume epsilon
    and polynomial failure exponent fixed as N grows.
    """
    if N < 2 or not (0 < epsilon < 1 and 0 < gamma < 1):
        raise ValueError("N>=2 and epsilon,gamma in (0,1) required")
    B = max(1, N.bit_length() - 1)
    Q0 = _power_two_at_least(64 / epsilon)
    Q1 = _power_two_at_least(B * Q0)
    p = Q0.bit_length() + Q1.bit_length() - 2
    gamma_numerator, gamma_denominator = gamma.as_integer_ratio()
    g = (gamma_numerator * (N.bit_length() - 1)) // (gamma_denominator * p)
    if not g:
        return None
    hbits = ceil(log2(32 / epsilon))
    return {"block_size": B, "phase_grid": Q0, "slope_grid": Q1,
            "group_size": g, "lane_step_bits": hbits,
            "trig_bits": max(8, ceil(log2(32 / epsilon)))}
