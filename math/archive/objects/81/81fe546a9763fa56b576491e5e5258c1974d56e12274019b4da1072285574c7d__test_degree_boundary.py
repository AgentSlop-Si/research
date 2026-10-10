import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
from itertools import product,combinations_with_replacement
from random import Random
from degree_boundary import (
    P, INV2, Counter, ntt, direct_dft, quadratic_fft, midpoint_recover,
    cubic_fft, cubic_jacobian_vector, cubic_recovery_nplus1, randomized_gauge,
    wedge_gauge, wedge_coefficients, cubic_global_wedge_fft, second_moment_target,
    matrix_rank_mod, run_audit,
)
from feature_rank_audit import verify as verify_feature_rank

class DegreeBoundaryTests(unittest.TestCase):
    def test_standard_ntt_vs_independent_direct(self):
        rng=Random(101)
        for n in (1,2,4,8,16,32,64,128):
            for _ in range(3):
                x=[rng.randrange(P) for j in range(n)]
                self.assertEqual(ntt(x),direct_dft(x))

    def test_quadratic_midpoint_exhaustive_boolean(self):
        rng=Random(102)
        for n in (2,4,8):
            weights=[rng.randrange(P) for _ in range(n)]
            for variant in ('plain','square','affine_square','pair_overlap'):
                for tup in product((0,1),repeat=n):
                    self.assertEqual(quadratic_fft(tup,weights,variant),direct_dft(tup))

    def test_quadratic_midpoint_full_matrix(self):
        rng=Random(103)
        for n in (2,4,8,16,32,64):
            weights=[rng.randrange(P) for _ in range(n)]
            for variant in ('square','affine_square','pair_overlap'):
                fn=lambda x: quadratic_fft(x,weights,variant)
                for i in range(n):
                    basis=[int(j==i) for j in range(n)]
                    self.assertEqual(midpoint_recover(fn,basis),direct_dft(basis))
                for _ in range(3):
                    x=[rng.randrange(P) for _ in range(n)]
                    self.assertEqual(midpoint_recover(fn,x),direct_dft(x))

    def test_midpoint_not_simple_boolean_evaluation(self):
        n=4; weights=[7,22,56,3]
        a=[INV2]*n
        self.assertNotEqual(quadratic_fft(a,weights,'affine_square'),direct_dft(a))
        self.assertEqual(midpoint_recover(lambda x:quadratic_fft(x,weights,'affine_square'),[31,10,87,6]),
                         direct_dft([31,10,87,6]))

    def test_wedge_exact_pair_expansion(self):
        rng=Random(104)
        for n in (2,3,4,8,16):
            a=[rng.randrange(1,P) for _ in range(n)]
            b=[rng.randrange(1,P) for _ in range(n)]
            coeff=wedge_coefficients(a,b)
            for _ in range(5):
                x=[rng.randrange(P) for _ in range(n)]
                pairs=[]
                for i in range(n):
                    for j in range(i+1,n):
                        pairs.append((x[i]*x[i]*x[j]-x[i]*x[j]*x[j])%P)
                self.assertEqual(wedge_gauge(x,a,b),sum(t*v for t,v in zip(coeff,pairs))%P)
                bits=[rng.randrange(2) for _ in range(n)]
                self.assertEqual(wedge_gauge(bits,a,b),0)

    def test_wedge_global_cubic_correct_on_cube(self):
        rng=Random(105)
        for n in (2,4,8,16):
            a=[rng.randrange(P) for _ in range(n)]
            b=[rng.randrange(P) for _ in range(n)]
            output_weights=[rng.randrange(P) for _ in range(n)]
            for _ in range(10):
                bits=[rng.randrange(2) for _ in range(n)]
                self.assertEqual(cubic_global_wedge_fft(bits,a,b,output_weights),direct_dft(bits))

    def test_cubic_dense_gauge_exact_boolean(self):
        rng=Random(106)
        for n in (2,4,8):
            gauge=randomized_gauge(n,n+1)
            for bits in product((0,1),repeat=n):
                self.assertEqual(cubic_fft(bits,gauge),direct_dft(bits))

    def test_cubic_midpoint_shortcut_fails(self):
        n=4
        gauge=randomized_gauge(n,107)
        h=[13,24,12,19]
        j=cubic_jacobian_vector([INV2]*n,h,gauge)
        # Correcting for the 3/4 derivative of the x_i^3 term does not
        # remove the antisymmetric pair gauge at the midpoint.
        estimate=[v*4*pow(3,-1,P)%P for v in j]
        self.assertNotEqual(estimate,direct_dft(h))

    def test_cubic_universal_nplus1_recovery(self):
        rng=Random(108)
        for n in (2,4,8,16):
            gauge=randomized_gauge(n,100+n)
            for k in range(n):
                x=[int(j==k) for j in range(n)]
                self.assertEqual(cubic_recovery_nplus1(x,gauge),direct_dft(x))
            for _ in range(4):
                x=[rng.randrange(P) for j in range(n)]
                self.assertEqual(cubic_recovery_nplus1(x,gauge),direct_dft(x))

    def test_cubic_second_moment_matrix_full_rank(self):
        for n in (1,2,3,4,5,8,16,32,64,128):
            M=second_moment_target(n)
            self.assertEqual(matrix_rank_mod(M),n)
            inv6=pow(6,-1,P)
            for i in range(n):
                self.assertEqual(3*M[i][i]%P,1)
                for j in range(i):
                    self.assertEqual(M[i][j],inv6)

    def test_exact_boolean_nullspace_dimensions(self):
        """Independently check that cubic pair gauges span the FULL kernel."""
        for n in (2,3,4,5,6,7,8):
            masks=list(product((0,1),repeat=n))
            mono3=list(combinations_with_replacement(range(n),3))
            B=[[int(all(bits[i] for i in mono)) for mono in mono3] for bits in masks]
            rank=matrix_rank_mod(B)
            self.assertEqual(rank,n+n*(n-1)//2+n*(n-1)*(n-2)//6)
            self.assertEqual(len(mono3)-rank,n*(n-1)//2)
        for n in (2,3,4,5,6,7):
            mono=[()]+[(i,) for i in range(n)]+list(combinations_with_replacement(range(n),2))
            B=[[int(all(bits[i] for i in m)) for m in mono]
                for bits in product((0,1),repeat=n)]
            self.assertEqual(len(mono)-matrix_rank_mod(B),n)

    def test_counter_charged_baseline(self):
        n=16
        weights=[5]*n
        costs={}
        for variant in ('plain','square','affine_square','pair_overlap'):
            c=Counter();quadratic_fft([3]*n,weights,variant,c)
            costs[variant]=c.work
        self.assertLess(costs['plain'],costs['square'])
        self.assertLess(costs['square'],costs['pair_overlap'])
        self.assertLess(costs['square'],costs['affine_square'])

    def test_validation(self):
        with self.assertRaises(ValueError):ntt([1,2,3])
        with self.assertRaises(ValueError):quadratic_fft([1,2,3],[1,2],'affine_square')
        with self.assertRaises(ValueError):quadratic_fft([1,2],[1,2],'unknown')
        with self.assertRaises(ValueError):cubic_fft([1,2],[[]])
        with self.assertRaises(ValueError):wedge_gauge([1,2],[1,2],[1])

    def test_audit_end_to_end(self):
        result=run_audit()
        self.assertEqual(result['quadratic_basis_columns_tested'],378)
        self.assertEqual(result['wedge_dense_overlap_tests'],24)
        self.assertEqual(result['general_full_fft_O_N'],'NOT_ESTABLISHED')

    def test_high_overlap_feature_bank_requires_extra_slot(self):
        for n in (2,4,8):
            z=verify_feature_rank(n)
            self.assertEqual(z['rank_N_nonlinear_features'],n)
            self.assertEqual(z['rank_after_adding_all_FFT_outputs'],n+1)
            self.assertEqual(z['rank_after_adding_square_and_FFT_outputs'],n+1)

if __name__=='__main__':unittest.main()
