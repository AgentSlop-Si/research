"""Exact finite-field and combinatorial audit of Fourier operator compression.

This program supplies examples and independent arithmetic checks, not an
unrestricted FFT lower bound or a new Fourier algorithm.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from math import log2
from typing import Sequence

PRIME = 998244353
ROOT = 3


def check_length(n: int, prime: int = PRIME) -> None:
    if n < 2 or n & (n - 1) or (prime - 1) % n:
        raise ValueError('n must be a power of two, >=2, dividing prime-1')


def nth_root(n: int, prime: int = PRIME, root: int = ROOT) -> int:
    check_length(n, prime)
    w = pow(root, (prime - 1) // n, prime)
    if pow(w, n, prime) != 1 or pow(w, n // 2, prime) == 1:
        raise ValueError('root is not primitive at this length')
    return w


def fourier_matrix(n: int, p: int = PRIME) -> list[list[int]]:
    w = nth_root(n, p)
    # Precompute roots. Entry F[j,k] = omega ** (j*k).
    power = [pow(w, t, p) for t in range(n)]
    return [[power[(j*k) % n] for k in range(n)] for j in range(n)]


def mod_rank(rows: Sequence[Sequence[int]], p: int = PRIME) -> int:
    if not rows:
        return 0
    nc = len(rows[0])
    if any(len(row) != nc for row in rows):
        raise ValueError('ragged matrix')
    mat = [[x % p for x in row] for row in rows]
    r = 0
    for c in range(nc):
        pivot = next((t for t in range(r, len(mat)) if mat[t][c]), None)
        if pivot is None:
            continue
        mat[r], mat[pivot] = mat[pivot], mat[r]
        inv = pow(mat[r][c], -1, p)
        # Work on rows below only; rank unaffected by pivot scaling.
        for i in range(r + 1, len(mat)):
            factor = mat[i][c] * inv % p
            if factor:
                for j in range(c + 1, nc):
                    mat[i][j] = (mat[i][j] - factor * mat[r][j]) % p
                mat[i][c] = 0
        r += 1
        if r == len(mat):
            break
    return r


def displacement_residual(n: int, p: int = PRIME) -> tuple[list[list[int]], list[list[int]]]:
    """Z F - F D^(-1) = - e0 [omega^(-k)]_k; Z is the noncyclic downshift."""
    F = fourier_matrix(n, p)
    w = nth_root(n, p)
    v = [pow(w, (-k) % n, p) for k in range(n)]
    residual = []
    for i in range(n):
        residual.append([
            ((F[i-1][j] if i else 0) - F[i][j] * v[j]) % p
            for j in range(n)
        ])
    target = [[(-v[j] if i == 0 else 0) % p for j in range(n)] for i in range(n)]
    return residual, target


def verify_displacement(n: int, p: int = PRIME) -> bool:
    actual, expected = displacement_residual(n, p)
    return actual == expected and mod_rank(actual, p) == 1


def full_rank_rectangles(n: int, p: int = PRIME) -> list[dict]:
    """Check dyadic contiguous-row Fourier rectangles; theorem covers all column sets."""
    F = fourier_matrix(n, p)
    samples = []
    for r in (2, 4, 8, 16, 32, 64):
        if r > n // 2:
            break
        column_sets = [
            list(range(r)),
            list(range(n-r, n)),
            list(range(0, n, max(1, n//r)))[:r],
        ]
        for i, col in enumerate(column_sets):
            if len(set(col)) != len(col):
                continue
            for row_start in (0, n//2, n-r):
                if row_start + r > n:
                    continue
                block = [[F[u][v] for v in col] for u in range(row_start, row_start+r)]
                rank = mod_rank(block, p)
                samples.append({'n':n,'rows':r,'row_start':row_start,
                                'columns':i,'rank':rank,'expected':r})
                if rank != r:
                    raise AssertionError(('contiguous minor rank', n, r, row_start, i, rank))
    return samples


def reverse_bits(i: int, logn: int) -> int:
    j=0
    for _ in range(logn):
        j=(j<<1)|(i&1)
        i >>= 1
    return j


def fft_mod(values: Sequence[int], p: int = PRIME) -> tuple[list[int], int]:
    n=len(values)
    w=nth_root(n,p)
    bits=n.bit_length()-1
    out=[int(values[reverse_bits(j,bits)]) % p for j in range(n)]
    gates=0
    width=2
    while width <= n:
        half=width//2
        rot=pow(w,n//width,p)
        for start in range(0,n,width):
            factor=1
            for j in range(half):
                a=out[start+j]
                b=out[start+j+half]*factor%p
                out[start+j]=(a+b)%p
                out[start+j+half]=(a-b)%p
                factor=factor*rot%p
                gates+=1
        width*=2
    return out,gates


def verify_fft(n: int, p: int = PRIME) -> tuple[int,int]:
    # Verify on all basis vectors, i.e. matrix equality, not random samples.
    F=fourier_matrix(n,p)
    final_count=0
    for k in range(n):
        input=[0]*n
        input[k]=1
        out, count=fft_mod(input,p)
        if out != [F[j][k] for j in range(n)]:
            raise AssertionError(('FFT basis mismatch',n,k))
        final_count=count
    return n,final_count


@dataclass(frozen=True)
class EntropyRow:
    n: int
    stage: int
    support_per_row: int
    entropy_total_bits: int
    cumulative_gates: int


def entropy_audit(n: int) -> list[EntropyRow]:
    """Bitset proof certificate for normalized DIT, without numeric rounding.

    After t normalized FFT levels, every row is a sum of 2**t disjoint
    original inputs of magnitude 2**(-t/2), hence the row has Shannon
    entropy t bits. Disjointness, coverage, and support are checked exactly.
    """
    check_length(n)
    bits=n.bit_length()-1
    support=[1<<reverse_bits(j,bits) for j in range(n)]
    observations=[EntropyRow(n,0,1,0,0)]
    gate_count=0
    for t in range(1,bits+1):
        width=1<<t
        half=width//2
        for start in range(0,n,width):
            for j in range(half):
                a=start+j
                b=a+half
                if support[a]&support[b]:
                    raise AssertionError('unexpected support overlap')
                new=support[a]|support[b]
                support[a]=support[b]=new
                gate_count+=1
        expected=1<<t
        if any(v.bit_count()!=expected for v in support):
            raise AssertionError(('incorrect support',n,t))
        observations.append(EntropyRow(n,t,expected,n*t,gate_count))
    if gate_count != n*bits//2:
        raise AssertionError('butterfly count mismatch')
    if any(v.bit_count()!=n for v in support):
        raise AssertionError('final transform not dense')
    return observations


def grouped_macro_audit(n: int) -> list[dict]:
    """No counting a dense macro DFT as one ordinary bounded-volume gate."""
    check_length(n)
    L=n.bit_length()-1
    data=[]
    for h in range(1,L+1):
        if L%h:
            continue
        block=1<<h
        macro_calls=(L//h)*(n//block)
        primitive_min_per_macro=(block*h)//2
        primitive_total=macro_calls*primitive_min_per_macro
        if primitive_total!=n*L//2:
            raise AssertionError('missing grouped gate work')
        data.append(dict(n=n,levels_per_group=h,block_width=block,
                         macro_calls=macro_calls,
                         min_primitives_per_macro=primitive_min_per_macro,
                         total_primitives=primitive_total))
    return data



def evaluate_pole_representation(values: Sequence[int], p: int = PRIME) -> tuple[list[int], dict]:
    """Recover every Fourier coefficient from the N-pole rational signature.

    G(z) = sum_k x[k]/(1 - omega**k*z).  Its coefficient [z**j] is
    exactly F(x)[j].  Description O(N); this direct realization O(N**2).
    It is intentionally a naive extraction, NOT a universal lower bound.
    """
    n=len(values)
    w=nth_root(n,p)
    factors=[pow(w,k,p) for k in range(n)]
    state=[int(x)%p for x in values]
    out=[]
    for j in range(n):
        out.append(sum(state)%p)
        if j<n-1:
            state=[state[k]*factors[k]%p for k in range(n)]
    return out,{'description_field_elements':2*n,
                'coefficient_additions':n*(n-1),
                'state_multiplies':n*(n-1),
                'fft_butterflies':n*(n.bit_length()-1)//2}

def run_audit(ns=(4,8,16,32,64,128)) -> dict:
    records=[]
    for n in ns:
        n_verified, gates=verify_fft(n)
        if not verify_displacement(n):
            raise AssertionError(('displacement',n))
        ranks=full_rank_rectangles(n)
        entropy=entropy_audit(n)
        macros=grouped_macro_audit(n)
        sample=[((i+3)*(i+17)+i*i) % PRIME for i in range(n)]
        recovered, pole_cost=evaluate_pole_representation(sample)
        fast,_=fft_mod(sample)
        if recovered!=fast:
            raise AssertionError(('pole coefficient expansion',n))
        records.append(dict(n=n_verified,basis_tests=n,displacement_rank=1,
                            block_rank_checks=len(ranks),
                            gates=gates,pole_cost=pole_cost,
                            log2_abs_det=n*(n.bit_length()-1)//2,
                            entropy_first=asdict(entropy[0]),entropy_last=asdict(entropy[-1]),
                            grouped_macros=macros))
    return {'model': 'finite_field_exact_for_identity;complex_unitary_for_potentials',
            'prime':PRIME,'results':records}

if __name__=='__main__':
    import json
    result=run_audit()
    print(json.dumps(result,indent=2))
