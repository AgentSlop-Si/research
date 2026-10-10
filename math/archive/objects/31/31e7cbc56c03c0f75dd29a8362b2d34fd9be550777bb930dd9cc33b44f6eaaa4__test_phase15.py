"""Phase 15 unit checks: whole DFT, full noncommuting bank equivalence,
condition certificates, and short-FFT Neumann chart approximation."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import unittest
import numpy as np
import math
from joint_decoder import joint_collapsed,explicit_frame_joint_check
from conditioning import triangular_permutation,certified_constant, exp_rational_upper
from fast_frame import W_series,fast_inverse
import stationary_toeplitz as st
from fractions import Fraction


class Phase15(unittest.TestCase):
    def setUp(self):self.rng=np.random.default_rng(15091)

    def test_triangular_permutations(self):
        for h in range(1,14):self.assertTrue(triangular_permutation(1<<h))

    def test_rational_certificate(self):
        cert=certified_constant()
        self.assertEqual(cert['cond_gram_strict_upper'],str(Fraction(741**2,259**2)))
        self.assertTrue(exp_rational_upper(Fraction(11,28))<Fraction(741,500))

    def test_joint_output_all_lengths(self):
        for G,m,M in [(16,3,4),(32,5,4),(64,3,8),(128,3,8),
                      (256,3,16),(512,1,16),(1024,1,16),(1024,7,16)]:
            x=self.rng.normal(size=G*m)+1j*self.rng.normal(size=G*m)
            v=joint_collapsed(x,M)
            np.testing.assert_allclose(v.output,np.fft.fft(x)/np.sqrt(G*m),atol=2e-10,rtol=5e-10)
            self.assertEqual(v.long_green_scans,0)
            self.assertEqual(v.short_K_ffts,m*M)
            self.assertEqual(v.short_M_ffts,m*G//M)

    def test_explicit_frame_equivalence(self):
        for G,m,M in [(16,3,4),(32,5,4),(64,3,8),(128,3,8)]:
            x=self.rng.normal(size=G*m)+1j*self.rng.normal(size=G*m)
            a,b,cre=explicit_frame_joint_check(x,M)
            np.testing.assert_allclose(a,b,atol=1e-10)
            self.assertLess(cre,1e-10)

    def test_bound_and_observed_condition(self):
        for M in (2,4,8,16,32):
            for ratio in (4,8,16):
                K=ratio*M; G=M*K
                W,gram,_=st.construction(G,M,M)
                self.assertLess(float(np.linalg.cond(gram)),8.2)

    def test_series_W_product_bound(self):
        for M,K in [(4,16),(8,32),(16,64),(32,128),(32,256)]:
            G=M*K
            W,_,_=st.construction(G,M,M)
            c=self.rng.normal(size=M)+1j*self.rng.normal(size=M)
            for P in (2,4,8):
                approx=W_series(c,M,K,P)
                lam=math.pi*(M-1)**2/(2*K*M)
                tau=lam**(P+1)/math.factorial(P+1)/(1-lam/(P+2))
                tol=math.sqrt(M)*tau*np.linalg.norm(c)+1e-10
                self.assertLessEqual(np.linalg.norm(W@c-approx),tol)

    def test_fast_solve_with_analytic_error(self):
        for M,K in [(4,16),(8,32),(16,64),(32,128),(64,512)]:
            W,_,_=st.construction(M*K,M,M)
            y=self.rng.normal(size=M)+1j*self.rng.normal(size=M)
            truth=np.linalg.solve(W,y)
            c,bound,work=fast_inverse(y,M,K,8,26)
            err=np.linalg.norm(c-truth)
            self.assertLessEqual(err,bound+1e-10)
            self.assertLess(err,1e-7)
            self.assertEqual(work['local_M_ffts_charged'],26*10)

    def test_negative_malformed_cases(self):
        x=np.ones(48,complex)
        with self.assertRaises(ValueError):joint_collapsed(x,8)
        with self.assertRaises(ValueError):fast_inverse(np.ones(4),4,8,4,5)


if __name__=='__main__':unittest.main(verbosity=2)
