import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from random import Random
from phase28_synthesis import *

class TestPhase28(unittest.TestCase):
    def test_01_fourier_type_II(self):
        for n in (4,8,16,32):
            with self.subTest(n=n):
                f=fft_matrix(n)
                self.assertEqual(ratio_correlation(f),
                                 [[n if i==j else 0 for j in range(n)] for i in range(n)])

    def test_02_mononomial_type_II(self):
        for n in (8,16,32):
            with self.subTest(n=n):
                rng=Random(111+n)
                r=list(range(n));c=list(range(n));rng.shuffle(r);rng.shuffle(c)
                d1=[rng.randrange(1,P) for _ in range(n)]
                d2=[rng.randrange(1,P) for _ in range(n)]
                f=permuted_scaled(fft_matrix(n),r,c,d1,d2)
                self.assertEqual(ratio_trace_invariants(f)['type_II'],1)

    def test_03_ratio_similarity_formula(self):
        for n in (8,16,32):
            with self.subTest(n=n):
                rng=Random(28+n)
                b=green_sum(n,7000+n)
                r=list(range(n));c=list(range(n));rng.shuffle(r);rng.shuffle(c)
                d1=[rng.randrange(1,P) for _ in range(n)]
                d2=[rng.randrange(1,P) for _ in range(n)]
                t=permuted_scaled(b,r,c,d1,d2)
                original=ratio_correlation(b)
                transformed=ratio_correlation(t)
                for i in range(n):
                    for j in range(n):
                        exp=d1[i]*original[r[i]][r[j]]*inverse(d1[j])%P
                        self.assertEqual(transformed[i][j],exp)
                self.assertEqual(ratio_trace_invariants(t),ratio_trace_invariants(b))

    def test_04_row_moment_trace_identity(self):
        for n in (8,16,32):
            m=green_sum(n,2890+n)
            self.assertEqual(ratio_trace_invariants(m)['trace2'],trace2_from_row_moments(m))

    def test_05_recover_gauges_permutations(self):
        for n in (8,16,32,64):
            for trial in range(2):
                with self.subTest(n=n,trial=trial):
                    rng=Random(890+n+100*trial)
                    b=green_sum(n,12345+trial*n)
                    r=list(range(n));c=list(range(n));rng.shuffle(r);rng.shuffle(c)
                    d1=[rng.randrange(1,P) for _ in range(n)]
                    d2=[rng.randrange(1,P) for _ in range(n)]
                    t=permuted_scaled(b,r,c,d1,d2)
                    res=equivalence_test(t,b)
                    self.assertEqual(res.status,'recovered',res.reason)
                    self.assertEqual(res.row_perm,r)
                    self.assertEqual(res.col_perm,c)
                    self.assertEqual(permuted_scaled(b,res.row_perm,res.col_perm,res.left,res.right),t)

    def test_06_positive_actual_F_triple(self):
        # Exact Fourier = A D1 P1 B P2 D2 C with A and B genuinely Green sums.
        # C deliberately dense, not an inexpensive Green mixer.
        for n in (8,16):
            with self.subTest(n=n):
                rng=Random(286+n)
                a=green_sum(n,600+n)
                b=green_sum(n,800+n)
                r=list(range(n));c=list(range(n));rng.shuffle(r);rng.shuffle(c)
                dl=[rng.randrange(1,P) for _ in range(n)]
                dr=[rng.randrange(1,P) for _ in range(n)]
                middle=permuted_scaled(b,r,c,dl,dr)
                # C=(A middle)^-1 F ensures valid Fourier control.
                c_outer=matmul(invert(matmul(a,middle)),fft_matrix(n))
                target=matmul(matmul(invert(a),fft_matrix(n)),invert(c_outer))
                res=equivalence_test(target,b)
                self.assertEqual(res.status,'recovered',res.reason)
                self.assertEqual(matmul(matmul(a,permuted_scaled(b,res.row_perm,res.col_perm,res.left,res.right)),c_outer),fft_matrix(n))

    def test_07_fixed_green_triples_excluded(self):
        for n in (8,16,32,64):
            for seed in (2800+n,3000+n):
                with self.subTest(n=n,seed=seed):
                    report=green_triple_fourier_test(n,seed)
                    self.assertEqual(report.status,'excluded',report.reason)
                    trace=green_triple_trace_certificate(n,seed)
                    self.assertNotEqual(trace['nonzero_difference'],0)

    def test_08_zero_pattern(self):
        b=[[2,1],[3,4]]
        t=[[2,0],[3,4]]
        self.assertEqual(equivalence_test(t,b).status,'excluded')
        self.assertEqual(equivalence_test(t,t).status,'inconclusive')

    def test_09_repeated_signature_inconclusive(self):
        # Fourier is highly symmetric; equality is not spuriously claimed by
        # a unique-fingerprint matcher with repeated fingerprints.
        for n in (8,16):
            self.assertEqual(equivalence_test(fft_matrix(n),fft_matrix(n)).status,'inconclusive')

    def test_10_corruption_negative(self):
        for n in (8,16,32):
            rng=Random(981+n)
            b=green_sum(n,333+n)
            rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
            t=permuted_scaled(b,rp,cp,[rng.randrange(1,P) for _ in range(n)],
                              [rng.randrange(1,P) for _ in range(n)])
            self.assertEqual(equivalence_test(t,b).status,'recovered')
            t[0][0]=(t[0][0]+1)%P
            self.assertEqual(equivalence_test(t,b).status,'excluded')

if __name__=='__main__':unittest.main()

class TestExceptionalPolynomials(unittest.TestCase):
    def test_11_n_squared_degree_and_positive_control(self):
        from phase28_polynomial import example
        for n in (4,8):
            with self.subTest(n=n):
                e=example(n)
                self.assertTrue(e['nonzero_polynomial'])
                self.assertEqual(e['root_check'],0)
                self.assertLessEqual(e['polynomial_degree'],n*n)
                self.assertNotEqual(e['other_coupling_witness'],0)

    def test_12_trace_gap_positive_typeII(self):
        # A strictly positive Green sum over complex arithmetic has trace
        # at least n^4; check independently using real alpha and ordinary float
        # only for positive-control illustration, not as finite-field positivity.
        import math
        for n in (4,8,16):
            alpha=.1
            order=list(range(n))
            m=[[0.0]*n for _ in range(n)]
            for col in range(n):
                j=col
                for k in range(n):
                    m[j][col]+=alpha**k/(1-alpha**n)
                    j=(j+1)%n
            R=[[sum(m[i][k]/m[j][k] for k in range(n)) for j in range(n)] for i in range(n)]
            t=sum(R[i][j]*R[j][i] for i in range(n) for j in range(n))
            self.assertGreaterEqual(t+1e-6,n**4)
            self.assertGreater(t,n**3)

class TestPhase28PolynomialCoupling(unittest.TestCase):
    def test_13_components_equal_existing_green_sum(self):
        from phase28_polynomial import evaluate_B
        for n in (4,8,16,32):
            x,y=green_components(n,128+n)
            self.assertEqual(evaluate_B(x,y,3*inverse(2)%P),green_sum(n,128+n))

    def test_14_actual_fourier_negative_one_parameter(self):
        from phase28_polynomial import trace_poly, eval_poly,product_affines
        for n in (4,8):
            seed=2800+n
            a=green_sum(n,seed*3+1)
            b0,b1=green_components(n,seed*3+2)
            c=green_sum(n,seed*3+3)
            t=matmul(matmul(invert(a),fft_matrix(n)),invert(c))
            pt=trace2_from_row_moments(t)
            poly=trace_poly(pt,b0,b1)
            z=3*inverse(2)%P
            self.assertNotEqual(eval_poly(poly,z),0)
            self.assertLessEqual(len(poly)-1,n*n)

class TestPhase28FinalProofCertificates(unittest.TestCase):
    def test_15_coupling_bezout_n4_n8_n16(self):
        from phase28_polynomial import exceptional_coupling_certificate
        for n in (4,8,16):
            with self.subTest(n=n):
                cert=exceptional_coupling_certificate(n,2800+n)
                self.assertTrue(cert['verification_passes'])
                self.assertTrue(cert['nonzero_reduced_leading_coeffs'])
                self.assertEqual(cert['gcd'],[1])
                if n==16:
                    self.assertEqual((cert['removed_from_p1'],cert['removed_from_p2']),(1,2))
                    self.assertEqual((cert['reduced_degree_p1'],cert['reduced_degree_p2']),(255,510))

    def test_16_o_n_executor_exact_dense(self):
        from phase28_executor import seeded_executor
        for n in (8,16,32,64,128):
            with self.subTest(n=n):
                seed=2800+n
                exe=seeded_executor(n,seed)
                mat=green_sum(n,seed)
                rng=Random(n)
                for _ in range(3):
                    v=[rng.randrange(P) for _ in range(n)]
                    expected=[sum(mat[i][j]*v[j] for j in range(n))%P for i in range(n)]
                    self.assertEqual(exe.apply(v),expected)

    def test_17_interpolation_matches_symbolic(self):
        from phase28_polynomial import (trace_moment_poly,trace_moment_poly_interpolated,
                                       trace_power_from_matrix)
        for n in (4,8):
            seed=2800+n
            a=green_sum(n,seed*3+1)
            b0,b1=green_components(n,seed*3+2)
            c=green_sum(n,seed*3+3)
            t=matmul(matmul(invert(a),fft_matrix(n)),invert(c))
            for s in (1,2):
                scalar=trace_power_from_matrix(t,s)
                direct=trace_moment_poly(scalar,b0,b1,s)
                interpol=trace_moment_poly_interpolated(scalar,b0,b1,s)
                self.assertEqual(direct,interpol)
