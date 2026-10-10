"""Exact audit of a scoped bidirectional-scan extension; no float zero tests."""
from pathlib import Path
from random import Random
import hashlib
import json

from exact_fields import PrimeField, CyclotomicField, inverse, mm, mv, rank, fourier
from sandwich import (Counted, Sandwich, prepare, generator_matrix, dense_parts,
                      cut_ranks, permutation_matrix, crossing_counts, row_support)


def basis_matrix(field, plan):
    n = len(plan.diagonal)
    cols = [plan.apply(field, [field.one if i == j else field.zero for i in range(n)]) for j in range(n)]
    return [list(row) for row in zip(*cols)]


def random_plan(field, n, block_size, rng):
    nonzero = lambda: rng.randrange(1, field.p)
    alpha, beta = [0]+[nonzero() for _ in range(n-1)], [0]+[nonzero() for _ in range(n-1)]
    lower = [0]+[0 if i % block_size == 0 else nonzero() for i in range(1, n)]
    upper = [0 if (i+1) % block_size == 0 else nonzero() for i in range(n-1)]+[0]
    while True:
        plan = Sandwich(alpha, beta, lower, [nonzero() for _ in range(n)], upper)
        _, t, _ = dense_parts(field, plan)
        try:
            inverse(field, t)
            return plan
        except ValueError:
            pass


def audit():
    rng = Random(2026100917)
    out = dict(status='PASS', reconstruction_cases=0, basis_vectors=0,
               fresh_vectors=0, inverse_cut_equalities=0,
               counted_setup_cases=0, counted_apply_cases=0,
               block_inverse_cases=0, shuffled_product_cases=0,
               permutation_crossing_cases=0, Fourier_rank_bound_cases=0,
               invalid_inputs=0, dense_inverse_examples=[], shuffled_rank_examples=[])
    for field in (PrimeField(97), PrimeField(257), CyclotomicField(4), CyclotomicField(8)):
        sizes = (2, 3, 4, 8, 12) if isinstance(field, PrimeField) else (2, 3, 4)
        for n in sizes:
            for _ in range(3):
                val = lambda: field.integer(rng.randrange(1, 30))
                p, q, u, v, d = [[val() for _ in range(n)] for _ in range(5)]
                counted = Counted(field)
                plan = prepare(counted, p, q, u, v, d)
                assert counted.total() == 17*n-19
                out['counted_setup_cases'] += 1
                a = generator_matrix(field, p, q, u, v, d)
                l, t, r = dense_parts(field, plan)
                assert mm(field, mm(field, l, a), r) == t
                out['reconstruction_cases'] += 1
                for j in range(n):
                    x = [field.one if i == j else field.zero for i in range(n)]
                    counted = Counted(field)
                    assert plan.apply(counted, x) == mv(field, a, x)
                    assert counted.total() == 9*n-8
                    out['basis_vectors'] += 1
                    out['counted_apply_cases'] += 1
                for _ in range(3):
                    x = [val() for _ in range(n)]
                    assert plan.apply(field, x) == mv(field, a, x)
                    out['fresh_vectors'] += 1
                try:
                    ainv = inverse(field, a)
                except ValueError:
                    continue
                acuts, icuts = cut_ranks(field, a, rank), cut_ranks(field, ainv, rank)
                assert acuts == icuts
                assert all(max(pair) <= 1 for pair in acuts)
                out['inverse_cut_equalities'] += 2*(n-1)

    # Inverse cut-rank equality also holds when leading principal blocks
    # are singular: reverse permutation makes all such assumptions unsafe.
    field = PrimeField(257)
    for n in (2, 4, 8, 16):
        a = permutation_matrix(field, list(reversed(range(n))))
        assert cut_ranks(field, a, rank) == cut_ranks(field, inverse(field, a), rank)
        out['inverse_cut_equalities'] += 2*(n-1)

    for n in (4, 8, 16, 32):
        for block_size in (1, 2, 3, 4):
            for _ in range(3):
                plan = random_plan(field, n, block_size, rng)
                a = basis_matrix(field, plan)
                ai = inverse(field, a)
                b = max(e-s for s, e in plan.blocks(field.zero))
                assert max(row_support(ai, field.zero)) <= min(n, 2*b+1)
                assert all(max(pair) <= 1 for pair in cut_ranks(field, a, rank))
                out['block_inverse_cases'] += 1
                word = a
                support_bound = 2*b+1
                for _ in range(2):
                    bp = random_plan(field, n, block_size, rng)
                    bmat = basis_matrix(field, bp)
                    perm = list(range(n)); rng.shuffle(perm)
                    pmat = permutation_matrix(field, perm)
                    word = mm(field, mm(field, bmat, pmat), word)
                    bb = max(e-s for s, e in bp.blocks(field.zero))
                    support_bound *= 2*bb+1
                    assert max(row_support(inverse(field, word), field.zero)) <= min(n, support_bound)
                    out['shuffled_product_cases'] += 1

        # The irreducible sandwich can have a fully dense inverse while
        # every off-diagonal cut of both matrix and inverse has rank one.
        dense_example = None
        for attempt in range(200):
            plan = random_plan(field, n, n, rng)
            a = basis_matrix(field, plan)
            ai = inverse(field, a)
            if min(row_support(ai, field.zero)) == n:
                dense_example = dict(N=n, inverse_nonzeros=n*n,
                                     max_inverse_cut_rank=max(max(v) for v in cut_ranks(field, ai, rank)),
                                     largest_tridiagonal_block=n)
                break
        assert dense_example is not None
        out['dense_inverse_examples'].append(dense_example)

        # Remove the permutation at the endpoint: genuine internal
        # conjugation of B destroys the shared-order rank bound.
        best = None
        for attempt in range(40):
            ap = random_plan(field, n, n, rng)
            bp = random_plan(field, n, n, rng)
            a, bmat = basis_matrix(field, ap), basis_matrix(field, bp)
            perm = list(range(n)); rng.shuffle(perm)
            pmat = permutation_matrix(field, perm)
            mixed = mm(field, mm(field, mm(field, a, pmat), bmat), inverse(field, pmat))
            cuts = cut_ranks(field, mixed, rank)
            middle = cuts[n//2-1]
            cand = dict(N=n, permutation=perm, balanced_cut_ranks=middle,
                        stage_max_cut_rank=1, endpoint_permutation_removed=True)
            if best is None or min(middle) > min(best['balanced_cut_ranks']):
                best = cand
            if min(middle) == n//2:
                break
        assert min(best['balanced_cut_ranks']) > 1 or n == 4
        out['shuffled_rank_examples'].append(best)

    for n in range(2, 33):
        for _ in range(5):
            perm = list(range(n)); rng.shuffle(perm)
            pmat = permutation_matrix(field, perm)
            crossings = crossing_counts(perm)
            assert cut_ranks(field, pmat, rank) == [(c,c) for c in crossings]
            assert 2*sum(crossings) == sum(abs(i-j) for i,j in enumerate(perm))
            out['permutation_crossing_cases'] += 1

    # Frobenius/operator-norm lower bound is stated over C, not arbitrary
    # finite fields. Exact cyclotomic tests verify small dyadic instances.
    for n in (2, 4, 8):
        field = CyclotomicField(n)
        f = fourier(field, n)
        for _ in range(8):
            rows, cols = list(range(n)), list(range(n))
            rng.shuffle(rows); rng.shuffle(cols)
            changed = [[f[i][j] for j in cols] for i in rows]
            cuts = cut_ranks(field, changed, rank)
            for s, (ru, rl) in enumerate(cuts, 1):
                assert n*ru >= s*(n-s) and n*rl >= s*(n-s)
                out['Fourier_rank_bound_cases'] += 2

    field = PrimeField(97)
    for args in (([1], [1], [1], [1], [1]),
                 ([0,1], [1,1], [1,1], [1,1], [1,1]),
                 ([1,1], [1,1], [1,1], [1,0], [1,1]),
                 ([1,1], [1], [1,1], [1,1], [1,1])):
        try:
            prepare(field, *args)
        except ValueError:
            out['invalid_inputs'] += 1
        else:
            raise AssertionError('expected coefficient rejection')
    out['source_sha256'] = {p.name:hashlib.sha256(p.read_bytes()).hexdigest()
                            for p in sorted(Path(__file__).parent.glob('*.py'))}
    return out


if __name__ == '__main__':
    result = audit()
    Path(__file__).with_name('results.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))
