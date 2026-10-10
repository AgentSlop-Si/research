"""Exact arithmetic experiments: one-way scans, arbitrary internal shuffles,
low-rank broadcasts and the full, fresh discrete Fourier transform.

The scan+shuffle / rank-broadcast lower bounds are rigorously proved in
RESEARCH.md. This file is an independently runnable finite verification, not a
new FFT algorithm. All matrices are over a prime field; the proofs also work
in characteristic zero with a primitive Nth root.
"""
from __future__ import annotations
from dataclasses import dataclass
import random

P = 998244353
G = 3


def identity(n: int) -> list[list[int]]:
    return [[int(i == j) for j in range(n)] for i in range(n)]


def matrix_mul(a: list[list[int]], b: list[list[int]], p: int = P) -> list[list[int]]:
    n = len(a)
    out = [[0] * n for _ in range(n)]
    for i in range(n):
        for k, ak in enumerate(a[i]):
            if ak:
                for j, bkj in enumerate(b[k]):
                    out[i][j] = (out[i][j] + ak * bkj) % p
    return out


def matrix_sub(a: list[list[int]], b: list[list[int]], p: int = P) -> list[list[int]]:
    return [[(u - v) % p for u, v in zip(rowa, rowb)] for rowa, rowb in zip(a, b)]


def matvec(a: list[list[int]], x: list[int], p: int = P) -> list[int]:
    return [sum(u * v for u, v in zip(row, x)) % p for row in a]


def rank_mod(a: list[list[int]], p: int = P) -> int:
    if not a:
        return 0
    rows, cols = len(a), len(a[0])
    x = [[int(z) % p for z in row] for row in a]
    r = 0
    for c in range(cols):
        pivot = next((i for i in range(r, rows) if x[i][c]), None)
        if pivot is None:
            continue
        x[r], x[pivot] = x[pivot], x[r]
        scale = pow(x[r][c], -1, p)
        x[r] = [t * scale % p for t in x[r]]
        for j in range(r + 1, rows):
            v = x[j][c]
            if v:
                x[j] = [(z - v * w) % p for z, w in zip(x[j], x[r])]
        r += 1
        if r == rows:
            break
    return r


def invert_mod(a: list[list[int]], p: int = P) -> list[list[int]]:
    n = len(a)
    x = [[z % p for z in a[i]] + identity(n)[i] for i in range(n)]
    for k in range(n):
        r = next((j for j in range(k, n) if x[j][k]), None)
        if r is None:
            raise ValueError('singular matrix')
        x[k], x[r] = x[r], x[k]
        v = pow(x[k][k], -1, p)
        x[k] = [z * v % p for z in x[k]]
        for j in range(n):
            if j == k:
                continue
            s = x[j][k]
            if s:
                x[j] = [(u - s * v) % p for u, v in zip(x[j], x[k])]
    return [row[n:] for row in x]


def root_of_unity(n: int, p: int = P, generator: int = G) -> int:
    if n <= 0 or (p-1) % n:
        raise ValueError('need N dividing p-1')
    omega = pow(generator, (p-1)//n, p)
    # Proper primitiveness check for power-of-two n only (test domain).
    if n & (n-1) or pow(omega, n, p) != 1 or (n > 1 and pow(omega, n//2, p) == 1):
        raise ValueError('require power-of-two N and primitive root')
    return omega


def dft_direct(x: list[int], p: int = P, generator: int = G) -> list[int]:
    n = len(x)
    w = root_of_unity(n, p, generator)
    return [sum(int(x[j]) * pow(w, (k*j) % n, p) for j in range(n)) % p for k in range(n)]


def scan_vector(x: list[int], direction: str, a: list[int], b: list[int], p: int = P) -> list[int]:
    n = len(x)
    if len(a) != n or len(b) != n or direction not in {'forward', 'backward'}:
        raise ValueError('invalid scan parameters')
    y = [0] * n
    if direction == 'forward':
        for i in range(n):
            y[i] = (b[i] * x[i] + (a[i] * y[i-1] if i else 0)) % p
    else:
        for i in range(n-1, -1, -1):
            y[i] = (b[i] * x[i] + (a[i] * y[i+1] if i+1 < n else 0)) % p
    return y


def inverse_scan_vector(y: list[int], direction: str, a: list[int], b: list[int], p: int = P) -> list[int]:
    n = len(y)
    if any(not z % p for z in b):
        raise ValueError('an invertible scan requires all nonzero b')
    if direction == 'forward':
        return [((y[i] - (a[i] * y[i-1] if i else 0)) * pow(b[i], -1, p)) % p for i in range(n)]
    if direction == 'backward':
        return [((y[i] - (a[i] * y[i+1] if i+1 < n else 0)) * pow(b[i], -1, p)) % p for i in range(n)]
    raise ValueError('invalid direction')


def matrix_from_action(n: int, action) -> list[list[int]]:
    cols = []
    for j in range(n):
        v = [0] * n
        v[j] = 1
        cols.append(action(v))
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def permutation_matrix(order: list[int]) -> list[list[int]]:
    n = len(order)
    if sorted(order) != list(range(n)):
        raise ValueError('not a permutation')
    return [[int(j == order[i]) for j in range(n)] for i in range(n)]


def broadcast_matrix(u: list[int], v: list[int], p: int = P) -> list[list[int]]:
    n = len(u)
    if len(v) != n:
        raise ValueError('different lengths')
    if (1 + sum(x*y for x,y in zip(u,v))) % p == 0:
        raise ValueError('broadcast I+uv^T is singular')
    return [[(int(i == j) + u[i]*v[j]) % p for j in range(n)] for i in range(n)]


def fft_via_two_scans(x: list[int], p: int = P, generator: int = G):
    """Ordinary radix-2 FFT re-expressed as TWO one-way scans per butterfly level.

    This demonstrates a matching O(log N)-stage control, NOT a faster FFT.
    All shuffles, diagonal twiddles, and O(N)-work scans remain explicit.
    """
    n = len(x)
    if n == 0 or n & (n-1):
        raise ValueError('power-of-two N required')
    w = root_of_unity(n, p, generator)
    levels = n.bit_length() - 1
    inv2 = pow(2, -1, p)
    data = [int(x[int(f'{i:0{levels}b}'[::-1], 2)] if levels else x[0]) % p for i in range(n)]
    operations = {'one_way_scans':0, 'pair_shuffles':0, 'scalar_multiplications':0,
                  'additions':0, 'moved_words':n, 'twiddle_table_entries':0,
                  'twiddle_prep_multiplications':0, 'stage_root_powers':0}
    for level in range(1, levels + 1):
        span = 1 << level
        half = span >> 1
        order = [j for start in range(0,n,span)
                 for k in range(half) for j in (start+k, start+k+half)]
        reordered = [data[i] for i in order]
        operations['pair_shuffles'] += 2
        operations['moved_words'] += 2*n
        stage_root = pow(w, n//span, p)
        twiddles = [1]
        for _ in range(1,half):
            twiddles.append(twiddles[-1]*stage_root % p)
        operations['twiddle_prep_multiplications'] += half-1
        operations['stage_root_powers'] += 1
        operations['twiddle_table_entries'] += half
        for pair in range(n//2):
            reordered[2*pair+1] = (-2*twiddles[pair % half]*reordered[2*pair+1]) % p
        operations['scalar_multiplications'] += n//2
        # First (backward) scan: even := even - odd/2; odds unchanged.
        a_back = [(-inv2 if j % 2 == 0 else 0) for j in range(n)]
        temp = scan_vector(reordered, 'backward', a_back, [1]*n, p)
        # Second (forward) scan: odd := odd + previous even.
        a_forward = [(1 if j % 2 else 0) for j in range(n)]
        transformed = scan_vector(temp, 'forward', a_forward, [1]*n, p)
        operations['one_way_scans'] += 2
        operations['scalar_multiplications'] += n//2  # backward -1/2 weight
        operations['additions'] += n                  # half each scan
        for j, original_index in enumerate(order):
            data[original_index] = transformed[j]
    return data, operations


def inverse_row_support_bound(scan_count: int, n: int) -> int:
    return min(n, 1 << scan_count)


def minimum_broadcast_rank_budget(n: int, scan_count: int) -> int:
    """If F_N = product of scans/shuffles/diagonals/(I+UV^T),
    total broadcast rank >= floor(N/(2**t+1)).
    """
    if n < 2 or scan_count < 0:
        raise ValueError('N>=2, t>=0 required')
    return n // (inverse_row_support_bound(scan_count, n) + 1)


@dataclass
class ExactFactor:
    kind: str
    matrix: list[list[int]]
    rank_budget: int = 0


def random_word(n: int, scans: int, broadcasts: int, seed: int, p: int = P) -> list[ExactFactor]:
    randomizer = random.Random(seed)
    if scans < 0 or broadcasts < 0:
        raise ValueError('negative number of stages')
    kinds = ['forward' if i%2==0 else 'backward' for i in range(scans)] + ['broadcast']*broadcasts
    kinds += ['perm', 'diag']
    randomizer.shuffle(kinds)
    word = []
    for kind in kinds:
        if kind in {'forward','backward'}:
            a = [randomizer.randrange(0,7) for _ in range(n)]
            b = [randomizer.randrange(1,7) for _ in range(n)]
            mat = matrix_from_action(n, lambda x, d=kind, aa=a, bb=b: scan_vector(x,d,aa,bb,p))
        elif kind == 'broadcast':
            u = [randomizer.randrange(0, 9) for _ in range(n)]
            v = [randomizer.randrange(0, 9) for _ in range(n)]
            mat = broadcast_matrix(u,v,p)
        elif kind == 'perm':
            order = list(range(n)); randomizer.shuffle(order)
            mat = permutation_matrix(order)
        else:
            diag = [randomizer.randrange(1,8) for _ in range(n)]
            mat = [[diag[i] if i==j else 0 for j in range(n)] for i in range(n)]
        word.append(ExactFactor(kind,mat,int(kind=='broadcast')))
    return word


def word_certificate(word: list[ExactFactor], p: int = P) -> dict:
    """Independently invert all factors, erase broadcast factors, then audit
    inverse Fourier rigidity invariant: A^-1 = row-sparse S + rank-B E.
    """
    n = len(word[0].matrix)
    total = identity(n)
    for factor in word:
        total = matrix_mul(factor.matrix, total, p)
    inverse = invert_mod(total,p)
    sparse = identity(n)
    for factor in word:
        mat = identity(n) if factor.kind=='broadcast' else invert_mod(factor.matrix,p)
        sparse = matrix_mul(sparse,mat,p)
    difference = matrix_sub(inverse,sparse,p)
    t = sum(f.kind in {'forward','backward'} for f in word)
    budget = sum(f.rank_budget for f in word)
    support = max(sum(v!=0 for v in row) for row in sparse)
    total_support = sum(sum(v != 0 for v in row) for row in sparse)
    mass_bound = n if t == 0 else min(n*n, (2*n-1)*(1 << (t-1)))
    if total_support > mass_bound:
        raise AssertionError('boundary-row support-mass bound failed')
    err_rank = rank_mod(difference,p)
    if support > min(n,2**t) or err_rank > budget:
        raise AssertionError('inverse sparsity or low-rank telescoping failed')
    if matrix_mul(total,inverse,p)!=identity(n):
        raise AssertionError('inverse is incorrect')
    return {'size':n,'scans':t,'broadcast_budget':budget,
            'max_sparse_row_support':support,'max_allowed_row_support':min(n,2**t),
            'sparse_total_nonzeros':total_support,'sparse_total_bound':mass_bound,
            'difference_rank':err_rank, 'certified_rank_upper_bound':budget,
            'forward_invertible':True}


def vander_certificate(n: int, s: int, b: int, rows_support: list[set[int]], p: int=P,
                       generator: int=G) -> dict:
    """Witness: if (b+1)(s+1)<=N, deleting row-sparse S from F cannot
    leave rank <=b: choose b+1 zero-S columns for consecutive b+1 rows.
    """
    if (b+1)*(s+1)>n or len(rows_support)<b+1:
        raise ValueError('invalid witness parameters')
    if any(len(row)>s or any(j<0 or j>=n for j in row) for row in rows_support):
        raise ValueError('invalid support')
    union = set().union(*rows_support[:b+1])
    cols = [j for j in range(n) if j not in union][:b+1]
    if len(cols)!=b+1:
        raise AssertionError('cardinality count failed')
    w = root_of_unity(n,p,generator)
    minor = [[pow(w,i*j,p) for j in cols] for i in range(b+1)]
    mrank = rank_mod(minor,p)
    if mrank!=b+1:
        raise AssertionError('Vandermonde determinant should be nonzero')
    return {'n':n,'s':s,'b':b,'rows':list(range(b+1)),
            'columns':cols,'minor_rank':mrank,'union_support_size':len(union),
            'exact_rank_contradiction':True}


def bidirectional_sum_escape(n: int, p: int = P) -> dict:
    """Counterexample to extending scan inverse sparsity to SUMS of scans.

    H = (weighted forward scan) + (weighted backward scan), evaluated in
    O(N) arithmetic; at tested sizes its inverse is completely dense and
    usually is not an I+rank-one update. This is NOT a Fourier evaluator.
    """
    if n < 2:
        raise ValueError('N>=2 required')
    fwd = matrix_from_action(n,lambda x: scan_vector(
        x,'forward',[0]+[j+2 for j in range(1,n)],[1]*n,p))
    bwd = matrix_from_action(n,lambda x: scan_vector(
        x,'backward',[j+3 for j in range(n-1)]+[0],[1]*n,p))
    mat = [[(fwd[i][j]+bwd[i][j])%p for j in range(n)] for i in range(n)]
    inv = invert_mod(mat,p)
    return {'N':n,'inverse_nnz':sum(bool(z) for row in inv for z in row),
            'inverse_all_entries_nonzero':all(z for row in inv for z in row),
            'inverse_minus_diagonal_rank':rank_mod(
                matrix_sub(inv,[[inv[i][i] if i==j else 0 for j in range(n)]for i in range(n)],p),p),
            'work':'two O(N) weighted scans plus N scalar additions',
            'computes_Fourier':False}
