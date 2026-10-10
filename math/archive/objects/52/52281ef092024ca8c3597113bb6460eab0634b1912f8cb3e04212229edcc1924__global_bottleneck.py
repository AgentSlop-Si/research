"""Exact direct global finite-field DFT and Boolean compression bottleneck audit.

All mathematical statements about complex-valued Lipschitz encoding/decoding
are in RESEARCH.md. The exact packed algorithm is NOT a linear-time FFT:
one arbitrary-width integer multiplication costs M(N*s) bit operations.
No cached inputs, no multi-threaded control, no uncharged table.
"""
from __future__ import annotations

from dataclasses import dataclass, asdict
from fractions import Fraction
from math import ceil, log2
from typing import Sequence

P = 998244353
ROOT = 3


def next_power_of_two(n: int) -> int:
    if n <= 0:
        raise ValueError("n must be positive")
    return 1 << (n - 1).bit_length()


def check_fft_size(n: int, p: int = P) -> None:
    if n < 1 or (n & (n - 1)):
        raise ValueError("N must be a positive power of two")
    if (p - 1) % (2*n):
        raise ValueError("a primitive 2N-th root must exist in the chosen field")


def chirp_phases(n: int, p: int = P, primitive_root: int = ROOT):
    """O(N) exact field products to prepare plus/minus quadratic chirps."""
    check_fft_size(n, p)
    zeta = pow(primitive_root, (p-1)//(2*n), p)
    if pow(zeta, n, p) != p-1 or pow(zeta, 2*n, p) != 1:
        raise ValueError("primitive_root does not produce a primitive 2N-th root")
    zinv = pow(zeta, p-2, p)
    zeta2 = zeta*zeta % p
    zinv2 = zinv*zinv % p
    d = [1]*n
    h = [1]*n
    mult_d, mult_h = zeta, zinv
    for j in range(1, n):
        d[j] = d[j-1]*mult_d % p
        h[j] = h[j-1]*mult_h % p
        mult_d = mult_d*zeta2 % p
        mult_h = mult_h*zinv2 % p
    return d, h, zeta


@dataclass(frozen=True)
class PackedCost:
    length: int
    field_prime: int
    cell_bits: int
    operand_bits: int
    packed_operand_actual_bits_A: int
    packed_operand_actual_bits_H: int
    product_actual_bits: int
    one_arbitrary_width_multiplication: int
    coefficient_reads: int
    # Cross-layer bit arithmetic cost is NOT counted as a unit operation.
    hidden_bit_model: str = "M(operand_bits) plus O(N*cell_bits) packing/unpacking plus field arithmetic"


def packed_dft(values: Sequence[int], p: int = P,
               primitive_root: int = ROOT) -> tuple[list[int], PackedCost]:
    """Fresh exact full NTT via ONE big-integer multiply (charged in bit model).

    Known composition of Bluestein's quadratic chirp with Kronecker
    substitution; one bigint multiply is emphatically NOT a unit-cost gate.
    """
    n = len(values)
    check_fft_size(n, p)
    d, h, _ = chirp_phases(n, p, primitive_root)
    a = [d[j]*(int(values[j]) % p) % p for j in range(n)]

    # For linear product of two length-N vectors with each entry <=p-1,
    # every nonnegative coefficient is <= N*(p-1)^2, so no base carries.
    bound = n * (p-1) * (p-1)
    cell_bytes = max(1, (bound.bit_length()+7)//8)
    cell_bits = 8*cell_bytes
    assert (1 << cell_bits) > bound
    buf_a = b''.join(t.to_bytes(cell_bytes, 'little') for t in a)
    buf_h = b''.join(t.to_bytes(cell_bytes, 'little') for t in h)
    aa = int.from_bytes(buf_a, 'little')
    hh = int.from_bytes(buf_h, 'little')
    product = aa * hh  # One enormous multiplication: must count its bit work!
    full = product.to_bytes(2*n*cell_bytes, 'little')
    coefficients = [int.from_bytes(full[i*cell_bytes:(i+1)*cell_bytes], 'little')
                    for i in range(2*n-1)]
    assert max(coefficients, default=0) <= bound

    out = []
    for j in range(n):
        value = coefficients[j]
        if j+n < len(coefficients):
            value += coefficients[j+n]
        out.append(d[j]*(value % p) % p)
    model = PackedCost(
        length=n, field_prime=p, cell_bits=cell_bits,
        operand_bits=n*cell_bits,
        packed_operand_actual_bits_A=aa.bit_length(),
        packed_operand_actual_bits_H=hh.bit_length(),
        product_actual_bits=product.bit_length(),
        one_arbitrary_width_multiplication=1,
        coefficient_reads=2*n-1)
    return out, model


def direct_dft(values: Sequence[int], p: int = P, primitive_root: int = ROOT) -> list[int]:
    """Independent quadratic reference: fresh exact DFT in F_p."""
    n = len(values)
    check_fft_size(n, p)
    omega = pow(primitive_root, (p-1)//n, p)
    out = []
    for k in range(n):
        step = pow(omega, k, p)
        phase = 1
        acc = 0
        for x in values:
            acc = (acc + (int(x) % p)*phase) % p
            phase = phase*step % p
        out.append(acc)
    return out


def ntt_reference(values: Sequence[int], p: int = P, primitive_root: int = ROOT) -> list[int]:
    """Independent iterative radix-2 NTT reference with full bit reversal."""
    n = len(values)
    check_fft_size(n, p)
    arr = [int(v) % p for v in values]
    j = 0
    for i in range(1,n):
        bit = n >> 1
        while j & bit:
            j ^= bit
            bit >>= 1
        j ^= bit
        if i < j:
            arr[i], arr[j] = arr[j], arr[i]
    length = 2
    while length <= n:
        base = pow(primitive_root, (p-1)//length, p)
        for start in range(0,n,length):
            phase = 1
            half = length >> 1
            for r in range(half):
                a = arr[start+r]
                b = phase*arr[start+half+r] % p
                arr[start+r] = (a+b) % p
                arr[start+half+r] = (a-b) % p
                phase = phase*base % p
        length *= 2
    return arr


def block_digits(bits: Sequence[int], block_bits: int) -> tuple[int,...]:
    """Exact fixed-point encoder. Encoded coordinate is digit / 2**block_bits."""
    if block_bits < 1 or len(bits) % block_bits:
        raise ValueError("block_bits must divide the nonzero signal length")
    if any(int(x) not in (0,1) for x in bits):
        raise ValueError("Boolean inputs required")
    out = []
    for i in range(0,len(bits),block_bits):
        digit = 0
        for j in range(block_bits):
            digit = (digit << 1) + int(bits[i+j])
        out.append(digit)
    return tuple(out)


def block_encode_exact(bits: Sequence[int], block_bits: int) -> tuple[Fraction,...]:
    return tuple(Fraction(d,1<<block_bits) for d in block_digits(bits,block_bits))


def grid_count(M: int, L: int, epsilon: Fraction = Fraction(0)) -> int:
    """Each real coordinate has at most Q grid cells, a theorem sufficient bound.

    Encoder coordinates are complex bounded in magnitude by integer M;
    decoder is L-Lipschitz on encoded values and has max error epsilon <1/2.
    """
    if M <= 0 or L <= 0 or not 0 <= epsilon < Fraction(1,2):
        raise ValueError("require M>0, L>0 and 0<=epsilon<1/2")
    ratio = Fraction(4*M*L,1)/(1-2*epsilon)
    return (ratio.numerator + ratio.denominator-1)//ratio.denominator + 1


def packing_possible(n: int, w: int, M: int, L: int,
                     epsilon: Fraction = Fraction(0), complex_coordinates: bool = True) -> bool:
    """Necessary capacity condition for an exact/near-exact complex FFT decoder."""
    if n < 1 or w < 1:
        raise ValueError("positive dimensions required")
    Q = grid_count(M,L,epsilon)
    return Q**(2*w if complex_coordinates else w) >= 2**n

if __name__ == "__main__":
    from random import Random
    r=Random(20261009)
    for n in (4,8,16,32,64,256,1024):
        vals=[r.randrange(P) for _ in range(n)]
        got,cost=packed_dft(vals)
        assert got==ntt_reference(vals)
        print(f'N={n:<5} radix_cell_bits={cost.cell_bits:<4} bigint_operand_bits={cost.operand_bits:<10} exact=True')
