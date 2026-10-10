"""Reproducible exact modular tests for the new annihilator and window gates."""
import unittest, random
from annihilator_gate import (nth_root, rank_mod,det_mod,nullspace_basis,mat_vec,mat_mul,
    transpose,Stage,left_annihilators,right_annihilators,casoratian_coefficients,
    projected_fourier_three,eval_poly,two_stage_witness,
    permutation_apply,ordering_defect,three_stage_gate,three_stage_projected_ranks,
    bit_reversal, fourier_block)

P=(12289,65537)

class TestFFTLocalGate(unittest.TestCase):
    def test_roots_and_ranks(self):
        for p in P:
            for n in (8,16,32,64,128):
                w=nth_root(n,p)
                self.assertEqual(pow(w,n,p),1)
                self.assertNotEqual(pow(w,n//2,p),1)
                self.assertEqual(rank_mod(fourier_block(n,w,range(n),range(n),p),p),n)

    def test_nullspace_and_degenerate_generators(self):
        for p in P:
            for seed in range(20):
                rng=random.Random(seed)
                for m in (3,5,8):
                    rows=[[rng.randrange(p) if seed%3 else 0 for _ in range(m)] for _ in range(2)]
                    basis=nullspace_basis(rows,p)
                    self.assertGreaterEqual(len(basis),m-2)
                    self.assertEqual(rank_mod(basis,p),len(basis))
                    self.assertTrue(all(not any(mat_vec(rows,x,p)) for x in basis))

    def test_casoratian_exact_identity_and_six_root_bound(self):
        for p in P:
            for n in (8,16,32,64,128):
                w=nth_root(n,p)
                for seed in range(10):
                    rng=random.Random((p+n)*200+seed)
                    Y=[[rng.randrange(p) if seed%2 else rng.randrange(3) for _ in range(5)] for _ in range(3)]
                    if rank_mod(Y,p)<3:continue
                    poly=casoratian_coefficients(Y,w,p)
                    self.assertEqual(len(poly),7)
                    self.assertTrue(any(poly))
                    roots=0
                    for j in range(n):
                        observed=det_mod(projected_fourier_three(Y,n,w,j,p),p)
                        expected=pow(w,3*j,p)*eval_poly(poly,pow(w,j,p),p)%p
                        self.assertEqual(observed,expected)
                        roots+=(observed==0)
                    self.assertLessEqual(roots,6)

    def test_stage_linear_work_exactness(self):
        for p in P:
            for n in (8,24,32,64):
                stage=Stage.random(n,p,p+n,zero_probability=0.4)
                dense=stage.matrix(p)
                r=random.Random(n+p)
                for _ in range(5):
                    x=[r.randrange(p) for _ in range(n)]
                    self.assertEqual(stage.apply(x,p),mat_vec(dense,x,p))

    def test_two_sided_annihilator_locality(self):
        for p in P:
            for n in (8,32,64):
                for seed in range(10):
                    s=Stage.random(n,p,seed+n,zero_probability=0.5)
                    M=s.matrix(p)
                    for start,width in ((0,3),(1,5),(n-6,6)):
                        for y in left_annihilators(s,start,width,p):
                            row=[sum(y[t]*M[start+t][j] for t in range(width))%p for j in range(n)]
                            self.assertFalse(any(row[:start]+row[start+width:]))
                        for x in right_annihilators(s,start,width,p):
                            col=[sum(M[i][start+t]*x[t] for t in range(width))%p for i in range(n)]
                            self.assertFalse(any(col[:start]+col[start+width:]))

    def test_two_stage_witness_all_generators_including_zero(self):
        for p in P:
            for n in (32,64,128):
                w=nth_root(n,p)
                for seed in range(8):
                    rng=random.Random(p+n+seed)
                    perm=list(range(n));rng.shuffle(perm)
                    s1=Stage.random(n,p,n*1021+seed,0.3 if seed%2 else 0.0)
                    s2=Stage.random(n,p,n*2027+seed,0.3 if seed%3 else 0.9)
                    c=two_stage_witness(n,s1,s2,perm,w,p)
                    self.assertGreater(c['determinant'],0)
                    self.assertEqual(c['projected_product'],[0]*3)
                    self.assertTrue(any(c['projected_fft']))
                    self.assertLessEqual(c['bad_determinant_windows'],6)
                    self.assertLessEqual(c['intersecting_windows'],15)
        # The N=24 boundary is not necessarily a power of two.
        p=12289;n=24
        w=nth_root(n,p)
        s=Stage.random(n,p,74,0.5)
        c=two_stage_witness(n,s,s,list(range(n-1,-1,-1)),w,p)
        self.assertTrue(any(c['projected_fft']))

    def test_three_stage_cut_bound_on_random_valid_stage_products(self):
        for p in P:
            n=32;w=nth_root(n,p)
            for name,perm1,perm2 in (
                ('identity',list(range(n)),list(range(n))),
                ('bitrev',bit_reversal(n),bit_reversal(n)),
                ('mixed',bit_reversal(n),list(range(n))),
            ):
                for W in (6,8,10):
                    c=three_stage_gate(n,perm1,perm2,W)
                    s=[Stage.random(n,p,p+3*i+n,zero_probability=0.3) for i in range(3)]
                    data=three_stage_projected_ranks(n,s,(perm1,perm2),c,w,p)
                    self.assertLessEqual(data['stage_compression_rank'],data['stage_rank_bound'])
                    self.assertGreaterEqual(data['fourier_compression_rank'],W-4)
                    if c['excludes_factorization']:
                        self.assertGreater(data['fourier_compression_rank'],data['stage_compression_rank'])

    def test_exact_combinatorial_permutation_counts(self):
        for n in (16,32,64):
            ids=list(range(n));br=bit_reversal(n)
            rr=three_stage_gate(n,br,br,6)
            self.assertFalse(rr['excludes_factorization'])
            rr=three_stage_gate(n,ids,ids,6)
            self.assertTrue(rr['excludes_factorization'])
        n=64; rng=random.Random(n+17); ids=list(range(n));p1=rng.sample(ids,n);p2=rng.sample(ids,n)
        rr=three_stage_gate(n,p1,p2,6)
        self.assertTrue(rr['excludes_factorization'])
        self.assertEqual(rr['violating_window_pairs'],2)

    def test_endpoint_nonaffine_rank_correction(self):
        # Bit reversal on both Fourier endpoints destroys the 'consecutive
        # Vandermonde' shortcut, reproducing the earlier false-proof trap.
        for p in P:
            for n in (16,32):
                w=nth_root(n,p); b=bit_reversal(n)
                h=rank_mod(fourier_block(n,w,b[:6],b[:6],p),p)
                self.assertLess(h,6)
                self.assertGreater(h,0)

    def test_combinatorial_random_permutation_expectation(self):
        # Exhaustively count *subsets* at modest n instead of all permutations.
        from itertools import combinations
        from math import comb
        n=10; W=3
        subsets=list(combinations(range(n),W))
        strict=0
        for R in subsets:
            for C in subsets:
                strict += (max(R)<min(C) or max(C)<min(R))
        self.assertEqual(strict,2*comb(n,2*W))
        self.assertEqual(len(subsets)**2,comb(n,W)**2)

    def test_window_rank_generalization_rank_two_middle(self):
        # An arbitrary rank-two offdiagonal submatrix remains bounded by 2+k;
        # this holds even if the stage is a sum of two QS stages.
        p=12289;n=32
        rng=random.Random(9)
        A=Stage.random(n,p,11,0).matrix(p);B=Stage.random(n,p,29,0).matrix(p)
        S=[[(A[i][j]+B[i][j])%p for j in range(n)] for i in range(n)]
        for seed in range(10):
            R=rng.sample(range(n),8);C=rng.sample(range(n),8)
            defect,_,_=ordering_defect(R,C,n)
            actual=rank_mod([[S[i][j] for j in C] for i in R],p)
            self.assertLessEqual(actual,defect+2)

if __name__=='__main__':
    unittest.main(verbosity=2)
