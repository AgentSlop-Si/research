"""Exact complex ranks of parity-block Fourier submatrices for N=2**k.

Mathematical input: universal sampling-set theorem for prime-power DFTs.
The stage-capacity calculations use the previous project's moving-partition lemma.
"""
from __future__ import annotations


def parity_block_rank(k: int, input_mask: int, output_mask: int) -> int:
    """Complex rank of F_N[R_b,C_a], N=2**k.

    C_a={x | parity(x & a)=0}; R_b={y | parity(y & b)=1}.
    Valid for nonzero masks, regardless of choice of parity signs.
    """
    n = 1 << k
    if not 0 < input_mask < n or not 0 < output_mask < n:
        raise ValueError('Both masks must be nonzero k-bit integers')
    u = input_mask.bit_length() - 1
    v = output_mask.bit_length() - 1
    return n // 4 if u + v <= k - 2 else n // 2


def deficient_pair_count(k: int) -> int:
    if k < 2:
        raise ValueError('k >= 2 required')
    return (k - 2) * (1 << (k - 1)) + 1


def boundary(mask: int, k: int) -> int:
    if not 0 < mask < 1 << k:
        raise ValueError('Invalid mask')
    total, prefix = 0, 0
    for i in range(k):
        prefix ^= (mask >> i) & 1
        if prefix:
            total += 1 << (k - i - 1)
    return total


def pullback_mask(mask: int, columns: list[int]) -> int:
    """Given GF(2) map P(x) with P(2**i)=columns[i], return mask for
    parity(P(x)&mask).  No modular roots or N-by-N Fourier matrix needed.
    """
    return sum(((v & mask).bit_count() % 2) << i for i, v in enumerate(columns))


def trace_witness(k: int, columns_per_shuffle: list[list[int]], a: int):
    masks = [a]
    for cols in columns_per_shuffle:
        masks.append(pullback_mask(masks[-1], cols))
    budgets = [boundary(m, k) for m in masks]
    rank = parity_block_rank(k, a, masks[-1])
    return {'N': 1 << k, 'input_mask': a, 'output_mask': masks[-1],
            'masks': masks, 'stage_capacities': budgets,
            'capacity': sum(budgets), 'complex_fourier_rank': rank,
            'gap': rank - sum(budgets)}


def best_witness(k: int, columns_per_shuffle: list[list[int]]):
    return max((trace_witness(k, columns_per_shuffle, a)
               for a in range(1, 1 << k)), key=lambda r: (r['gap'], -r['capacity']))


if __name__ == '__main__':
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parent/'prior_helpers'))
    from mixing_survivor import make
    for k in range(6, 13):
        _, cols = make(k, 20261016)
        print(best_witness(k, cols))
