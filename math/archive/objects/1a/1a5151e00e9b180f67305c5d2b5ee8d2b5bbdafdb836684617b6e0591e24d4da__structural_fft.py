"""Input-independent FFT arithmetic DAG and finite-field WHT tabulation research.

Complex-FFT part is a symbolic, reusable, static circuit implementing classic
radix-2 and split-radix DFTs.  It does NOT achieve sub-O(N log N).

Finite-field part is an independently correct tabulated Walsh-Hadamard transform
with reusable tables compiled using smaller precomputed tables, following the
algorithmic principle of Josh Alman's 2023 work. It is a DIFFERENT transform.

All accounting uses an explicitly stated RAM/arithmetic model. This is
research/proof education code, not a faster production FFT implementation.
"""
from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
import cmath
import math
import sys
import time
from typing import Sequence


def _is_power_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


@dataclass(frozen=True, slots=True)
class Instruction:
    op: str
    a: int
    b: int = -1
    constant: complex = 0j


class FFTGraph:
    """Static arithmetic DAG for any complex-valued input of length N=2^L.

    Nodes 0..N-1 are input reads; higher nodes are operations.  Equivalent
    expressions are interned by stable symbolic keys, not by input values.
    Twiddle factors are computed once at compile time and kept with nodes.
    Compilation and execution take O(N log N) time, independent of input data.
    """

    def __init__(self, n: int, method: str = "split_radix") -> None:
        if not _is_power_two(n):
            raise ValueError("FFT length must be a positive power of two")
        if method not in ("radix2", "split_radix"):
            raise ValueError("method must be 'radix2' or 'split_radix'")
        self.n = n
        self.method = method
        self.instructions: list[Instruction] = []
        self._interned: dict[tuple, int] = {}
        self._twiddle_cache: dict[tuple[int, int], complex] = {}
        self._attempted_nodes = 0
        self.compile_seconds = 0.0
        t0 = time.perf_counter()
        indices = tuple(range(n))
        if method == "radix2":
            self.outputs = tuple(self._build_radix2(indices))
        else:
            self.outputs = tuple(self._build_split_radix(indices))
        self.compile_seconds = time.perf_counter() - t0

    def _new(self, op: str, a: int, b: int = -1,
             constant: complex = 0j, key: tuple | None = None) -> int:
        if key is None:
            key = (op, a, b)
        self._attempted_nodes += 1
        result = self._interned.get(key)
        if result is not None:
            return result
        result = self.n + len(self.instructions)
        self.instructions.append(Instruction(op, a, b, constant))
        self._interned[key] = result
        return result

    def _add(self, a: int, b: int) -> int:
        # Exploit universal commutativity of complex addition.
        return self._new("add", a, b, key=("add", min(a, b), max(a, b)))

    def _sub(self, a: int, b: int) -> int:
        return self._new("sub", a, b)

    def _rotate(self, node: int, n: int, exponent: int) -> int:
        e = exponent % n
        if e == 0:
            return node
        # +/-1 and +/-i need only sign changes/exchanges, not a generic
        # complex multiply. Their work is still counted as an instruction.
        if 4 * e == n:
            return self._new("neg_i", node)
        if 2 * e == n:
            return self._new("neg", node)
        if 4 * e == 3 * n:
            return self._new("pos_i", node)
        factor = self._twiddle_cache.get((n, e))
        if factor is None:
            factor = cmath.exp(-2j * math.pi * e / n)
            self._twiddle_cache[(n, e)] = factor
        return self._new("mul", node, constant=factor, key=("mul", node, n, e))

    def _build_radix2(self, idx: tuple[int, ...]) -> list[int]:
        n = len(idx)
        if n == 1:
            return [idx[0]]
        even = self._build_radix2(idx[::2])
        odd = self._build_radix2(idx[1::2])
        result = [0] * n
        for k in range(n // 2):
            t = self._rotate(odd[k], n, k)
            result[k] = self._add(even[k], t)
            result[k + n // 2] = self._sub(even[k], t)
        return result

    def _build_split_radix(self, idx: tuple[int, ...]) -> list[int]:
        n = len(idx)
        if n == 1:
            return [idx[0]]
        if n == 2:
            return [self._add(idx[0], idx[1]),
                    self._sub(idx[0], idx[1])]
        even = self._build_split_radix(idx[::2])
        odd1 = self._build_split_radix(idx[1::4])
        odd3 = self._build_split_radix(idx[3::4])
        q = n // 4
        result = [0] * n
        for k in range(q):
            u = self._rotate(odd1[k], n, k)
            v = self._rotate(odd3[k], n, 3 * k)
            summed = self._add(u, v)
            difference = self._sub(u, v)
            # X[k+N/4] = E[k+N/4] - i*(u-v).
            minus_i_difference = self._new("neg_i", difference)
            result[k] = self._add(even[k], summed)
            result[k + 2 * q] = self._sub(even[k], summed)
            result[k + q] = self._add(even[k + q], minus_i_difference)
            result[k + 3 * q] = self._sub(even[k + q], minus_i_difference)
        return result

    def execute(self, a: Sequence[complex]) -> list[complex]:
        if len(a) != self.n:
            raise ValueError(f"expected {self.n} coefficients")
        values = [complex(v) for v in a]
        for ins in self.instructions:
            x = values[ins.a]
            if ins.op == "add":
                result = x + values[ins.b]
            elif ins.op == "sub":
                result = x - values[ins.b]
            elif ins.op == "mul":
                result = x * ins.constant
            elif ins.op == "neg_i":
                # x=(a+bi) -> b-ai, no general complex multiplication
                result = complex(x.imag, -x.real)
            elif ins.op == "pos_i":
                result = complex(-x.imag, x.real)
            elif ins.op == "neg":
                result = -x
            else:
                raise RuntimeError(f"unknown op {ins.op}")
            values.append(result)
        return [values[j] for j in self.outputs]

    def execute_two_real(self, a: Sequence[float], b: Sequence[float]
                         ) -> tuple[list[complex],list[complex]]:
        """Two arbitrary *real* transforms in one compiled complex FFT.

        The packing identity is classic, not a new algorithm. Each recovered
        length-N output is explicitly materialized in O(N) work.
        """
        if len(a) != self.n or len(b) != self.n:
            raise ValueError(f"both arrays must have length {self.n}")
        z = [complex(x, y) for x,y in zip(a,b)]
        Z = self.execute(z)
        A=[]
        B=[]
        for k in range(self.n):
            u = Z[k]
            v = Z[(-k) % self.n].conjugate()
            A.append((u+v)/2)
            B.append((u-v)/(2j))
        return A,B

    def stats(self) -> dict[str, int | float | str]:
        op_types: dict[str, int] = {}
        for ins in self.instructions:
            op_types[ins.op] = op_types.get(ins.op, 0) + 1
        fanout = [0] * (self.n + len(self.instructions))
        for ins in self.instructions:
            fanout[ins.a] += 1
            if ins.op in ("add", "sub"):
                fanout[ins.b] += 1
        for i in self.outputs:
            fanout[i] += 1
        # A rough Python-object footprint (not full RSS or all allocator overhead).
        footprint = (sys.getsizeof(self.instructions) +
                     sum(sys.getsizeof(x) for x in self.instructions) +
                     sys.getsizeof(self._interned) +
                     sys.getsizeof(self.outputs) +
                     sys.getsizeof(self._twiddle_cache))
        return {
            "n": self.n,
            "method": self.method,
            "nodes": len(self.instructions) + self.n,
            "internal_nodes": len(self.instructions),
            "duplicate_symbolic_operations_eliminated":self._attempted_nodes-len(self.instructions),
            "complex_add_sub": op_types.get("add", 0) + op_types.get("sub", 0),
            "nontrivial_complex_multiplies": op_types.get("mul", 0),
            "trivial_rotations": sum(op_types.get(op, 0) for op in ("neg_i", "pos_i", "neg")),
            "shared_nodes_fanout_gt1": sum(f > 1 for f in fanout),
            "twiddle_constants": len(self._twiddle_cache),
            "compile_seconds": self.compile_seconds,
            "approx_plan_bytes": footprint,
        }


class CompactSplitRadix:
    """Implicit, static split-radix computation graph with O(N) twiddle storage.

    The recursive *template* is constant size.  Twiddle tables for all sizes
    4,8,...,N together use O(N) stored complex constants; no O(N log N)-node
    expanded DAG is materialized.  Online execution is still O(N log N).
    """
    def __init__(self, n: int) -> None:
        if not _is_power_two(n):
            raise ValueError("n must be a positive power of two")
        self.n = n
        self.twiddles: dict[int, tuple[tuple[complex,complex],...]] = {}
        start = time.perf_counter()
        size = 4
        while size <= n:
            self.twiddles[size] = tuple((
                cmath.exp(-2j * math.pi * k / size),
                cmath.exp(-2j * math.pi * 3*k / size),
            ) for k in range(size//4))
            size *= 2
        self.compile_seconds = time.perf_counter()-start

    def execute(self, a: Sequence[complex]) -> list[complex]:
        if len(a) != self.n:
            raise ValueError(f"expected {self.n} values")
        def compute(sub: Sequence[complex]) -> list[complex]:
            m = len(sub)
            if m == 1:
                return [complex(sub[0])]
            if m == 2:
                u,v = complex(sub[0]),complex(sub[1])
                return [u+v,u-v]
            e = compute(sub[::2])
            o1 = compute(sub[1::4])
            o3 = compute(sub[3::4])
            q = m//4
            out = [0j]*m
            for k,(w1,w3) in enumerate(self.twiddles[m]):
                if k == 0:
                    u,v = o1[k],o3[k]
                else:
                    u,v = w1*o1[k],w3*o3[k]
                plus = u+v
                minus = u-v
                minus_i = complex(minus.imag,-minus.real)
                out[k] = e[k]+plus
                out[k+2*q] = e[k]-plus
                out[k+q] = e[k+q]+minus_i
                out[k+3*q] = e[k+q]-minus_i
            return out
        return compute(a)

    def stats(self) -> dict[str, float | int]:
        twiddle_pairs = sum(len(v) for v in self.twiddles.values())
        return {
            "n":self.n,
            "twiddle_pairs":twiddle_pairs,
            "twiddle_complex_values":2*twiddle_pairs,
            "compile_seconds":self.compile_seconds,
            "approx_python_twiddle_bytes":(
                sys.getsizeof(self.twiddles) +
                sum(sys.getsizeof(table) + sum(sys.getsizeof(pair) +
                    sys.getsizeof(pair[0])+sys.getsizeof(pair[1]) for pair in table)
                    for table in self.twiddles.values())
            ),
            "nontrivial_complex_multiplies":count_nontrivial_twiddles(self.n,"split_radix"),
            "complex_add_sub":self.n*(self.n.bit_length()-1),
        }


def count_nontrivial_twiddles(n: int, method: str = "split_radix") -> int:
    """Proven recurrence of the graph's generic complex multiplication count.

    A radix-2 stage has n/2-2 nontrivial multipliers (0 and n/4 are
    trivial) for n>=4. A split-radix stage has two per k except k=0.
    """
    if not _is_power_two(n):
        raise ValueError("n must be a power of two")
    if method not in ("radix2", "split_radix"):
        raise ValueError("unknown method")
    @lru_cache(None)
    def count(m: int) -> int:
        if m <= 2:
            return 0
        own = m // 2 - 2
        if method == "radix2":
            return 2 * count(m // 2) + own
        return count(m // 2) + 2 * count(m // 4) + own
    return count(n)


def fwht_mod(values: Sequence[int], p: int = 3) -> list[int]:
    """Standard in-place butterfly Walsh-Hadamard transform modulo odd p."""
    n = len(values)
    if not _is_power_two(n) or p < 3 or p % 2 == 0:
        raise ValueError("n must be power of two; p must be odd >=3")
    out = [int(v) % p for v in values]
    half = 1
    while half < n:
        width = half * 2
        for start in range(0, n, width):
            for j in range(half):
                a, b = out[start+j], out[start+j+half]
                out[start+j] = (a+b) % p
                out[start+j+half] = (a-b) % p
        half *= 2
    return out


class SharedLookupTable:
    """Uniform table across ALL possible block inputs; input-independent build.

    b=2^t, entries=p^b; using smaller tables reduces compilation work to
    Theta(b*p^b) modular additions at the largest size (versus naive
    Theta(b log b*p^b) computing each table entry independently).
    """
    def __init__(self, p: int = 3, max_entries: int = 250_000) -> None:
        if p < 3 or p % 2 == 0:
            raise ValueError("p must be odd >= 3")
        self.p = p
        self.max_entries = max_entries
        self.tables: dict[int, list[tuple[int,...]]] = {1: [(i,) for i in range(p)]}
        self.modular_add_sub_build = 0
        self.build_seconds = 0.0

    def ensure(self, b: int) -> list[tuple[int,...]]:
        if not _is_power_two(b):
            raise ValueError("block length must be a power of two")
        if b in self.tables:
            return self.tables[b]
        if self.p ** b > self.max_entries:
            raise ValueError(f"table too large: {self.p}^{b} entries; adjust max_entries deliberately")
        prev = self.ensure(b//2)
        p = self.p
        table: list[tuple[int,...]] = []
        t0 = time.perf_counter()
        for code in range(p**b):
            code_copy = code
            even_code = 0
            odd_code = 0
            place = 1
            # Convert base-p digits into child subproblem IDs.
            for _ in range(b//2):
                even_code += (code_copy % p) * place
                code_copy //= p
                odd_code += (code_copy % p) * place
                code_copy //= p
                place *= p
            even, odd = prev[even_code], prev[odd_code]
            output = [0] * b
            for k in range(b//2):
                output[2*k] = (even[k] + odd[k]) % p
                output[2*k+1] = (even[k] - odd[k]) % p
            table.append(tuple(output))
        self.tables[b] = table
        self.modular_add_sub_build += b*(p**b)
        self.build_seconds += time.perf_counter() - t0
        return table

    def stats(self) -> dict[str, int | float]:
        return {
            "p": self.p,
            "largest_block": max(self.tables),
            "total_table_entries": sum(len(t) for t in self.tables.values()),
            "total_stored_field_elements": sum(b*len(t) for b,t in self.tables.items()),
            "build_modular_add_sub": self.modular_add_sub_build,
            "build_seconds": self.build_seconds,
            "approx_python_table_bytes": sum(
                sys.getsizeof(tab) + sum(sys.getsizeof(row) for row in tab)
                for tab in self.tables.values()),
        }


def tabulated_fwht_mod(values: Sequence[int], p: int = 3,
                       block: int = 8,
                       cache: SharedLookupTable | None = None
                       ) -> tuple[list[int], dict[str, int]]:
    """Exact Walsh-Hadamard transform with grouped bit-axis lookup passes.

    No assumption about input repetition. Each compiled table represents all
    p^b possible block values. The online passes take O(N*ceil(log N/log b))
    word-RAM operations, assuming constant-time indexed accesses and
    constant-size field arithmetic. Table preprocessing is accounted separately.
    """
    n = len(values)
    if not _is_power_two(n) or p < 3 or p % 2 == 0 or not _is_power_two(block):
        raise ValueError("bad length, modulus or block length")
    if cache is None:
        cache = SharedLookupTable(p)
    if cache.p != p:
        raise ValueError("cache and modulus differ")
    out = [int(x) % p for x in values]
    nbits = n.bit_length()-1
    blockbits = block.bit_length()-1
    if blockbits == 0:
        raise ValueError("block must be >=2")
    processed = 0
    lookups = 0
    passes = 0
    while processed < nbits:
        bits = min(blockbits, nbits-processed)
        b = 1 << bits
        table = cache.ensure(b)
        stride = 1 << processed
        jump = stride * b
        for base in range(0, n, jump):
            for low in range(stride):
                # The b entries with all nonselected bit coordinates held fixed.
                code = 0
                power = 1
                for t in range(b):
                    code += out[base + low + t*stride]*power
                    power *= p
                result = table[code]
                for t in range(b):
                    out[base + low + t*stride] = result[t]
                lookups += 1
        processed += bits
        passes += 1
    return out, {
        "n": n,
        "p": p,
        "block": block,
        "passes": passes,
        "lookups": lookups,
        "online_field_reads": n*passes,
        "online_field_writes": n*passes,
        "baseline_modular_add_sub": n*nbits,
    }


def asymptotic_block_length(n: int, p: int = 3, fraction: float = .25) -> int:
    """A theoretical b(N)=Theta(log N) whose table remains sublinear in N.

    For realistic N, the returned block may be 2; this function illustrates
    an asymptotic family, not an effective practical heuristic.
    """
    if not _is_power_two(n) or p < 3 or not (0 < fraction < 1):
        raise ValueError("invalid arguments")
    cap = max(2, int(fraction * math.log(n) / math.log(p)))
    return 1 << (cap.bit_length()-1)
