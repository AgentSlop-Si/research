import sys
from pathlib import Path
import unittest
from random import Random
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

from exact_audit import (verify_hidden_order,verify_inverse,verify_grid,
                         exhaustive_grid4,tridiagonal_green,rank_mod)
from expander_stage import random_order,apply_two_path,union_bound_failure,path_union_edges
from linear_inverse import (MOD,ParityGreenInverse,PentadiagonalLDLT,
                            tridiagonal_multiply,interleave_order)
from grid_stage import transpose_order,grid_balanced_check,two_path_edges
from spectral_certificate import run as exact_gap_certificate


class Tests(unittest.TestCase):
    def test_hidden_order_all_cuts_and_fourier_minors(self):
        for n in (8,16,32,64):
            with self.subTest(n=n):
                r=verify_hidden_order(n)
                self.assertLessEqual(r['hidden_max_cut_rank'],4)
                self.assertEqual(r['fourier_hidden_LL_rank'],n//2)
                self.assertEqual(r['fourier_hidden_LR_rank'],n//2)

    def test_parity_stage_inverse_bidirectional(self):
        rng=Random(214)
        for n in (4,8,16,32,64,128,256):
            with self.subTest(n=n): verify_inverse(n,rng)

    def test_pentadiagonal_border_exact_identity(self):
        for n in (4,8,16):
            with self.subTest(n=n):
                eps=pow(20,-1,MOD)
                sigma=list(range(0,n,2))+list(range(1,n,2))
                tau=interleave_order(n)
                T=[[((3 if i==j else -1 if abs(i-j)==1 else 0)%MOD)
                    for j in range(n)] for i in range(n)]
                A=[[T[sigma[i]][sigma[j]] for j in range(n)] for i in range(n)]
                K=[[ (T[i][j]+eps*A[i][j])%MOD
                      for j in range(n)] for i in range(n)]
                Kprime=[[K[i][j] for j in tau] for i in tau]
                Kmodel=[[ (3*(1+eps) if i==j else -eps if abs(i-j)==1
                             else -1 if abs(i-j)==2 else 0) %MOD
                         for j in range(n)] for i in range(n)]
                Kmodel[1][n-2]=(Kmodel[1][n-2]-1)%MOD
                Kmodel[n-2][1]=(Kmodel[n-2][1]-1)%MOD
                self.assertEqual(Kprime,Kmodel)
                prep=ParityGreenInverse(n)
                rng=Random(n)
                for _ in range(3):
                    x=[rng.randrange(MOD) for i in range(n)]
                    self.assertEqual(prep.solve_k([sum(Kmodel[i][j]*x[j] for j in range(n))%MOD for i in range(n)]),x)

    def test_grid_mixer_exact_executor(self):
        rng=Random(301)
        for L in (4,6,8):
            with self.subTest(L=L):
                r=verify_grid(L,rng)
                self.assertEqual(r['dense_executor_full_vector_tests'],5)

    def test_grid_all_balanced_four_by_four(self):
        r=exhaustive_grid4()
        self.assertEqual(r['balanced_subsets'],12870)
        self.assertEqual(r['min_grid_boundary'],4)

    def test_random_path_mixer_exact_executor(self):
        from exact_audit import permuted_sum,dense_apply
        rng=Random(582)
        for n in (32,64):
            with self.subTest(n=n):
                order=random_order(n,seed=n+23)
                G=tridiagonal_green(n)
                eps=pow(100,-1,MOD)
                M=permuted_sum(G,order,eps)
                for _ in range(4):
                    x=[rng.randrange(MOD) for i in range(n)]
                    self.assertEqual(dense_apply(M,x),apply_two_path(x,order))

    def test_probability_formula(self):
        self.assertLess(union_bound_failure(32),0.097)
        self.assertLess(union_bound_failure(64),.00015)
        self.assertLess(union_bound_failure(128),2e-10)
        self.assertLess(union_bound_failure(256),1e-21)

    def test_exact_integer_spectral_gap_certificates(self):
        for n in (32,64,128):
            with self.subTest(n=n):
                c=exact_gap_certificate(n)
                self.assertEqual(c['positive_leading_principal_minors'],n)
                self.assertTrue(c['spectral_gap_strict_gt_one_quarter'])

    def test_numerical_path_cut_robust_singular_bound(self):
        try:
            import numpy as np
            from scipy.linalg import solve_banded
        except ImportError:
            self.skipTest("Optional NumPy and SciPy not installed")
        from grid_stage import grid_edges,crossing_count
        for L in (4,8,16):
            n=L*L
            ab=np.zeros((3,n))
            ab[0,1:]=-1;ab[1,:]=3;ab[2,:-1]=-1
            G=solve_banded((1,1),ab,np.eye(n))
            perm=transpose_order(L)
            M=G+.01*G[np.ix_(perm,perm)]
            self.assertLessEqual(np.linalg.cond(M),5.00000001)
            rng=Random(n)
            for S in (set(range(n//2)),{r*L+c for r in range(L) for c in range(L//2)},
                      set(rng.sample(range(n),n//2))):
                path1,path2=two_path_edges(L)
                e=sum((a in S)!=(b in S) for a,b in path1+path2)
                I=np.array(sorted(S));J=np.array(sorted(set(range(n))-S))
                vals=np.linalg.svd(M[np.ix_(I,J)],compute_uv=False)
                self.assertGreaterEqual(int(np.count_nonzero(vals>=1/2500 - 1e-12)),e//15)


class HaarControls(unittest.TestCase):
    def test_haar_modular_orthogonality_and_composite(self):
        from haar_control import haar,root_half_mod,apply_haar_green
        self.assertEqual(root_half_mod()*root_half_mod()%MOD,pow(2,-1,MOD))
        for n in (8,16,32):
            with self.subTest(n=n):
                cols=[haar([int(i==j) for i in range(n)],p=MOD) for j in range(n)]
                W=[[cols[j][i] for j in range(n)] for i in range(n)]
                for i in range(n):
                    for j in range(n):
                        self.assertEqual(sum(W[i][k]*W[j][k] for k in range(n))%MOD,int(i==j))
                r=rank_mod([[(W[i][j] - (i==j))%MOD for j in range(n)] for i in range(n)])
                self.assertGreater(r,n//2)
                perm=random_order(n,seed=n+68)
                rng=Random(n)
                x=[rng.randrange(MOD) for _ in range(n)]
                self.assertEqual(haar(apply_two_path(x,perm),p=MOD),
                                 apply_haar_green(x,perm))

if __name__=='__main__': unittest.main()
