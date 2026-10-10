"""Independent recheck of saved structural-FFT research notes.

Claims are scoped to their computation models. Nothing here establishes
sub-N-log-N complexity for arbitrary complex FFTs or integer multiplication.
"""
import random
from math import ceil, log2
from phase3_barrier import choose_ntt_prime, ntt_root, radix2_ntt, inverse_ntt, rank_one_sign_sparse
from structural_fft import fwht_mod, SharedLookupTable, tabulated_fwht_mod, asymptotic_block_length


def check():
    rng = random.Random(20261009)
    for p in (3, 5):
        cache = SharedLookupTable(p, max_entries=100000)
        for n in (8, 16, 64, 256, 1024):
            b = 8 if p == 3 else 4
            for _ in range(5):
                a = [rng.randrange(p) for _ in range(n)]
                out, stats = tabulated_fwht_mod(a, p=p, block=b, cache=cache)
                assert out == fwht_mod(a, p=p)
                assert stats['online_field_reads'] == n * stats['passes']
        assert cache.stats()['total_stored_field_elements'] < 1000000
    for n in (8, 16, 32, 64, 128):
        q = choose_ntt_prime(n)
        root = ntt_root(n, q)
        assert q >= n+1
        for _ in range(2):
            a = [rng.randrange(q) for _ in range(n)]
            assert inverse_ntt(radix2_ntt(a, q, root), q, root) == a
    print('PASS: random WHT lookup/butterfly agreement and exact NTT round-trips')
    print('WHT asymptotic lookup-family resource counts (theoretical, not materialized):')
    print('N=2^L  block b  table fields (p=3)  table fields/N')
    for L in (16, 32, 64, 128, 256):
        n = 1 << L
        b = asymptotic_block_length(n, p=3, fraction=0.25)
        stored = b * 3**b
        assert stored < n
        print(f'{L:<6} {b:<8} {stored:<19} {stored/n:.3e}')
    print('NTT root-of-unity/output-width barrier:')
    print('N  smallest q  q^2 pair-table entries  N*ceil(log2 q) explicit output bits')
    for n in (8, 16, 32, 64, 128, 256, 512, 1024):
        q = choose_ntt_prime(n)
        print(f'{n:<5} {q:<11} {q*q:<21} {n*ceil(log2(q))}')
    print('Sign-restricted rank-one + sparse WHT (optimistic direct correction counts):')
    print('N  residual nonzeros  rank1+(sparse) estimated adds  FWHT adds')
    for n in (2, 4, 8, 16):
        c = rank_one_sign_sparse(n)
        s = c['nonzero']
        est = n-1+s
        base = n*int(log2(n))
        print(f'{n:<3} {s:<18} {est:<30} {base}')
        for _ in range(3):
            x = [rng.randrange(3) for _ in range(n)]
            from phase3_barrier import apply_rank_one_sparse
            assert apply_rank_one_sparse(c, x) == fwht_mod(x, 3)
    print('PASS: WHT decompositions match reference on random inputs')


if __name__ == '__main__':
    check()
