"""Exact fixed-graph Fourier research primitives, over a supplied prime field.

The actual Fourier executor below is O(N log N), NOT a faster FFT.
The O(N) auxiliary algorithms compute closed traces or tree Green operators,
not the arbitrary-input Fourier vector. See THEORY.md for the missing step.

Only Python's standard library is required. The finite fields are verification
models: no claim that a fixed field supports unbounded transform lengths.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence


@dataclass
class Counts:
    additions: int = 0  # Includes subtractions, not indexing.
    multiplications: int = 0


@dataclass(frozen=True)
class Field:
    p: int
    generator: int

    def inverse(self, value: int) -> int:
        value %= self.p
        if value == 0:
            raise ZeroDivisionError("Zero has no multiplicative inverse.")
        return pow(value, -1, self.p)

    def root(self, length: int) -> int:
        if length < 1 or (self.p - 1) % length:
            raise ValueError("The supplied field must contain the required root.")
        root = pow(self.generator, (self.p - 1) // length, self.p)
        if pow(root, length, self.p) != 1:
            raise ValueError("Invalid supplied generator/root.")
        if length > 1 and length & (length - 1) == 0:
            if pow(root, length // 2, self.p) == 1:
                raise ValueError("The supplied dyadic root is not primitive.")
        return root


def binary_reversals(bits: int) -> list[int]:
    if bits < 0:
        raise ValueError("bits must be nonnegative")
    result = [0] * (1 << bits)
    if bits:
        for j in range(1, len(result)):
            result[j] = (result[j >> 1] >> 1) | ((j & 1) << (bits - 1))
    return result


class FixedGraph:
    """Plan for Q_N; full root, phase and address preparation is O(N)."""

    def __init__(self, length: int, field: Field):
        if length < 1 or length & (length - 1):
            raise ValueError("length must be a positive power of two")
        self.N = length
        self.n = length.bit_length() - 1
        self.field = field
        self.w = field.root(length)
        self.roots = [1] * length
        # Count exact field multiplications for root-table preparation separately.
        self.root_table_multiplications = max(0, length - 2)
        if length > 1:
            self.roots[1] = self.w
        for j in range(2, length):
            self.roots[j] = self.roots[j - 1] * self.w % field.p
        self.phi = [0] * length
        for j in range(1, length):
            self.phi[j] = self.phi[j >> 1] + (j & 1) * (j >> 1)
        self.reversal = binary_reversals(self.n)

    def _check(self, x: Sequence[int]) -> None:
        if len(x) != self.N:
            raise ValueError(f"Expected {self.N} coordinates, got {len(x)}")

    def apply(self, x: Sequence[int], counts: Counts | None = None) -> list[int]:
        """One Q application: N additions and N/2-1 multiplies (N >= 2)."""
        self._check(x)
        if self.N == 1:
            return [x[0] % self.field.p]
        p = self.field.p
        m = self.N // 2
        out = [0] * self.N
        for r in range(m):
            out[2 * r] = (x[r] + x[r + m]) % p
            difference = (x[r] - x[r + m]) % p
            out[2 * r + 1] = difference if r == 0 else self.roots[r] * difference % p
        if counts is not None:
            counts.additions += self.N
            counts.multiplications += m - 1
        return out

    def power(self, x: Sequence[int], exponent: int, counts: Counts | None = None) -> list[int]:
        if exponent < 0:
            raise ValueError("This evaluator accepts nonnegative powers.")
        self._check(x)
        result = [v % self.field.p for v in x]
        for _ in range(exponent):
            result = self.apply(result, counts)
        return result

    def fourier(self, x: Sequence[int], counts: Counts | None = None) -> list[int]:
        """Actual full Fourier executor. Its work is still Theta(N log N)."""
        v = self.power(x, self.n, counts)
        p = self.field.p
        out = [0] * self.N
        for k, r in enumerate(self.reversal):
            if self.phi[r] == 0:
                out[k] = v[r]
            else:
                out[k] = self.roots[(-self.phi[r]) % self.N] * v[r] % p
                if counts is not None:
                    counts.multiplications += 1
        return out

    def trace_prefix(self, extra: int = 0) -> tuple[list[int], int]:
        """tr(Q^k), k=1..n+extra, by 2^(n+extra+1)-2 periodic states.

        Any FIXED extra preserves O(N) work. With extra=0 the count is 2N-2.
        Exponent/address integers are polynomially bounded for fixed extra.
        """
        if extra < 0:
            raise ValueError("extra must be nonnegative")
        phase_table = [0] * (1 << (self.n + extra))
        for j in range(1, len(phase_table)):
            phase_table[j] = phase_table[j >> 1] + (j & 1) * (j >> 1)
        traces = []
        states = 0
        for k in range(1, self.n + extra + 1):
            copies, remainder = divmod(self.n, k)
            repeat = ((1 << (copies * k)) - 1) // ((1 << k) - 1)
            reversals = binary_reversals(k)
            total = 0
            mask = (1 << k) - 1
            for a in range(1 << k):
                s = (a * repeat) << remainder
                if remainder:
                    s += a >> (k - remainder)
                # Next k emitted bits: rotate the period word to position n.
                v = (((a << remainder) & mask) | (a >> (k - remainder))) if remainder else a
                exponent = (s * reversals[v] + phase_table[v]) & (self.N - 1)
                total = (total + self.roots[exponent]) % self.field.p
            states += 1 << k
            traces.append(total)
        return traces, states

    def determinant_jet(self, extra: int = 0) -> list[int]:
        """det(I-zQ) mod z^(n+extra+1), not an arbitrary-input vector solve."""
        degree = self.n + extra
        if self.field.p <= degree:
            raise ValueError("Need characteristic greater than the truncation degree.")
        traces, _ = self.trace_prefix(extra)
        d = [1]
        for j in range(1, degree + 1):
            value = sum(d[j - k] * traces[k - 1] for k in range(1, j + 1))
            d.append(-value * self.field.inverse(j) % self.field.p)
        return d

    def branch_apply(self, x: Sequence[int], bit: int) -> list[int]:
        self._check(x)
        if self.N < 2 or bit not in (0, 1):
            raise ValueError("Branches require N >= 2 and bit in {0,1}.")
        p = self.field.p
        out = [0] * self.N
        for s, value in enumerate(x):
            target = (2 * s + bit) & (self.N - 1)
            out[target] = (out[target] + self.roots[bit * s] * value) % p
        return out

    def branch_solve(self, x: Sequence[int], bit: int, z: int) -> list[int]:
        """Solve (I-z A_bit)y=x by one tree accumulation and one root division.

        Topological preparation is included on every call in this implementation.
        It could instead be cached, but that is not needed for the O(N) bound.
        """
        self._check(x)
        if self.N < 2 or bit not in (0, 1):
            raise ValueError("Branches require N >= 2 and bit in {0,1}.")
        p = self.field.p
        root = 0 if bit == 0 else self.N - 1
        successor = [(2 * s + bit) & (self.N - 1) for s in range(self.N)]
        indegree = [0] * self.N
        for s in range(self.N):
            if s != root:
                indegree[successor[s]] += 1
        stack = [s for s in range(self.N) if indegree[s] == 0]
        out = [v % p for v in x]
        processed = 0
        while stack:
            s = stack.pop()
            if s == root:
                continue
            t = successor[s]
            out[t] = (out[t] + z * self.roots[bit * s] * out[s]) % p
            processed += 1
            indegree[t] -= 1
            if indegree[t] == 0:
                stack.append(t)
        if processed != self.N - 1:
            raise AssertionError("The binary branch should be a rooted tree plus self-loop.")
        out[root] = out[root] * self.field.inverse(1 - z * self.roots[bit * root]) % p
        return out

    def haar_apply(self, x: Sequence[int], z: int) -> list[int]:
        """Apply H_N(z)=C(I-z A_0)^-1 J with an O(N)-work recursive Haar tree."""
        if self.N < 2 or len(x) != self.N // 2:
            raise ValueError("H input length must be N/2, with N >= 2.")
        p = self.field.p
        beta = (2 * z - 1) * self.field.inverse(1 - z) % p

        def rec(v: Sequence[int], scale: int) -> list[int]:
            m = len(v)
            if m == 1:
                return [beta * v[0] % p]
            h = m // 2
            u = [(v[a] + v[a + h]) % p for a in range(h)]
            d = [(v[a] - v[a + h]) % p for a in range(h)]
            small = rec(u, scale * 2)
            out = [0] * m
            for a in range(h):
                out[2 * a] = z * small[a] % p
                out[2 * a + 1] = self.roots[scale * (2 * a + 1)] * d[a] % p
            return out

        return rec(x, 1)

    def haar_inverse(self, y: Sequence[int], z: int) -> list[int]:
        """Invert H itself in O(N); this does NOT invert I-zH."""
        if self.N < 2 or len(y) != self.N // 2:
            raise ValueError("H output length must be N/2, with N >= 2.")
        p = self.field.p
        iz, i2 = self.field.inverse(z), self.field.inverse(2)
        ibeta = (1 - z) * self.field.inverse(2 * z - 1) % p

        def rec(v: Sequence[int], scale: int) -> list[int]:
            m = len(v)
            if m == 1:
                return [ibeta * v[0] % p]
            h = m // 2
            u = rec([v[2 * a] * iz % p for a in range(h)], scale * 2)
            d = [v[2 * a + 1] * self.roots[(-scale * (2 * a + 1)) % self.N] % p
                 for a in range(h)]
            return ([(u[a] + d[a]) * i2 % p for a in range(h)]
                    + [(u[a] - d[a]) * i2 % p for a in range(h)])

        return rec(y, 1)
