import math
import unittest
import numpy as np

from phase36_two_mask import (
    CyclicMarkovGreen, make_green_triplet, sinkhorn_green, audit,
    projective_phase_floor, sandwich_phase_floor, fourier_matrix,
    cycle_from_seed,
)
from phase36_phase_rigidity import (
    phase_matrix, phase_rank_bound, outer_phase_rank_bound,
    exact_four_point_certificate, root_phase_cyclic_green,
    necessary_middle_phase_rank, complex_single_cycle_phase_certificate,
    general_cyclic_phase_rank,
)


class GreenRecurrences(unittest.TestCase):
    def test_green_dense_application(self):
        for n in (4,8,16,32):
            g=CyclicMarkovGreen(cycle_from_seed(n,320+n),1-1/n)
            x=np.arange(1,n+1)/n
            np.testing.assert_allclose(g.apply(x),g.dense()@x,atol=1e-12)

    def test_transposed_green_application(self):
        for n in (4,8,16,32):
            g=CyclicMarkovGreen(cycle_from_seed(n,321+n),1-1/n)
            x=np.sin(np.arange(n))
            np.testing.assert_allclose(g.transpose_apply(x),g.dense().T@x,atol=1e-12)

    def test_mass_preservation(self):
        for n in (4,8,16,64):
            g=CyclicMarkovGreen(cycle_from_seed(n,321+n),1-1/n)
            np.testing.assert_allclose(g.apply(np.ones(n)),np.ones(n),atol=1e-12)
            np.testing.assert_allclose(g.transpose_apply(np.ones(n)),np.ones(n),atol=1e-12)

    def test_exact_algebraic_outer_inverse(self):
        for n in (4,8,16,32,64):
            A,_,C=make_green_triplet(n)
            x=np.cos(np.arange(n)*0.42)
            for stage in (A,C):
                np.testing.assert_allclose(stage.inverse_apply(stage.apply(x)),x,atol=1e-11)
                np.testing.assert_allclose(stage.apply(stage.inverse_apply(x)),x,atol=1e-11)

    def test_bridge_kernel_uniform_ratio(self):
        for n in (4,8,16,64,1024):
            _,B,_=make_green_triplet(n)
            self.assertLess(B.ratio_bound(),math.e)


class PositiveScaling(unittest.TestCase):
    def test_boundary_calibration_all_sizes(self):
        for n in (4,8,16,32,64,128,256,512):
            A,B,C=make_green_triplet(n)
            circuit,fit=sinkhorn_green(A,B,C)
            e0=np.zeros(n);e0[0]=1
            np.testing.assert_allclose(circuit.apply(e0),np.ones(n),atol=2e-11)
            np.testing.assert_allclose(circuit.transpose_apply(e0),np.ones(n),atol=2e-11)
            self.assertLess(fit['iterations'],25)
            self.assertLess(fit['relative_marginal_error'],1e-11)

    def test_masks_have_bounded_spread(self):
        for n in (8,64,512):
            A,B,C=make_green_triplet(n)
            _,fit=sinkhorn_green(A,B,C)
            self.assertLessEqual(fit['x_spread'],fit['kernel_spread']+1e-10)
            self.assertLessEqual(fit['y_spread'],fit['kernel_spread']+1e-10)

    def test_dense_and_matrix_free(self):
        for n in (4,8,16,32):
            A,B,C=make_green_triplet(n)
            circuit,_=sinkhorn_green(A,B,C)
            M=circuit.dense()
            x=np.cos(np.arange(n)*0.13)
            np.testing.assert_allclose(M@x,circuit.apply(x),atol=1e-10)
            np.testing.assert_allclose(M.T@x,circuit.transpose_apply(x),atol=1e-10)

    def test_both_boundary_conditions_not_next_column(self):
        for n in (8,16,32,128):
            A,B,C=make_green_triplet(n)
            circuit,_=sinkhorn_green(A,B,C)
            e1=np.zeros(n);e1[1]=1
            omega=np.exp(-2j*np.pi*np.arange(n)/n)
            self.assertGreater(np.max(np.abs(circuit.apply(e1)-omega)),1)


class Rigidity(unittest.TestCase):
    def test_phase_rank_floor(self):
        for n in (4,8,16,32):
            self.assertGreater(phase_rank_bound(n,1),0)
            self.assertEqual(phase_rank_bound(n,n),0)
            self.assertGreaterEqual(projective_phase_floor(n),phase_rank_bound(n,1))

    def test_phase_rank_near_full_necessity(self):
        for n in (16,32,64,128,256,1024):
            r=necessary_middle_phase_rank(n,.02,.02)
            self.assertGreaterEqual(r, int(.99*n))
            if n<=128:self.assertEqual(r,n)
        self.assertEqual(necessary_middle_phase_rank(16,0,0),16)

    def test_random_complex_masks_against_rank_floor(self):
        rng=np.random.default_rng(31)
        for n in (4,8,16,32):
            _,B,_=make_green_triplet(n)
            mat=B.dense()
            F=fourier_matrix(n)
            for _ in range(4):
                x=np.exp(1j*rng.uniform(0,2*np.pi,n))*rng.uniform(.5,2,n)
                y=np.exp(1j*rng.uniform(0,2*np.pi,n))*rng.uniform(.5,2,n)
                M=x[:,None]*mat*y[None,:]
                self.assertGreaterEqual(np.linalg.norm(M-F,2)+1e-9,projective_phase_floor(n))

    def test_phase_sandwich_norm_bound(self):
        for n in (4,8,16,32,64):
            A,B,C=make_green_triplet(n)
            circuit,_=sinkhorn_green(A,B,C)
            F=fourier_matrix(n)
            measured=np.linalg.norm(circuit.dense()/math.sqrt(n)-F,2)
            bound=sandwich_phase_floor(n,.02,.02)
            self.assertGreater(bound,0)
            self.assertGreaterEqual(measured+1e-9,bound)

    def test_middle_phase_gauge_rank_one(self):
        for n in (4,8,16,32,64):
            conj,direct,G0,phases=root_phase_cyclic_green(n,3 if n>4 else 1)
            np.testing.assert_allclose(conj,direct,atol=5e-12)
            np.testing.assert_allclose(conj,phases[:,None]*G0*np.conjugate(phases)[None,:],atol=5e-12)
            s=np.linalg.svd(phase_matrix(direct),compute_uv=False)
            self.assertLess(s[1],1e-9*s[0])

    def test_full_phase_rank_not_fourier_coherence(self):
        for n in (4,8,16,32):
            cert=complex_single_cycle_phase_certificate(n)
            self.assertEqual(cert['phase_rank'],n)
            self.assertGreater(cert['normalized_min_singular'],1e-8)
            self.assertLessEqual(len(cert['crossratio_value_set']),2)
            self.assertGreater(cert['Fourier_crossratio_value_count'],len(cert['crossratio_value_set']))

    def test_phase_rank_dichotomy(self):
        for n in (4,8,16,32,64):
            self.assertEqual(general_cyclic_phase_rank(n,2*np.pi/n),1)
            self.assertEqual(general_cyclic_phase_rank(n,np.pi/n),n)
            self.assertEqual(general_cyclic_phase_rank(n,0.0713),n)

    def test_exact_fourier_cross_ratio(self):
        cert=exact_four_point_certificate()
        self.assertTrue(cert['exact_nonreal'])
        self.assertEqual(cert['imaginary_sign'],'negative')

    def test_valid_control_outside_near_identity(self):
        n=8
        F=fourier_matrix(n)
        _,B,_=make_green_triplet(n)
        mat=B.dense()
        A=F@np.linalg.inv(mat)
        np.testing.assert_allclose(A@mat,F,atol=1e-12)
        self.assertGreater(np.linalg.norm(A-np.eye(n),2),1)

    def test_double_frequency_operator_norm(self):
        for n in (4,8,16,32):
            inds=np.arange(n)
            w=np.exp(-2j*np.pi/n)
            F2=w**(2*inds[:,None]*inds[None,:])
            expected=math.sqrt(n*math.gcd(2,n))
            self.assertAlmostEqual(np.linalg.norm(F2,2),expected,places=9)


if __name__=='__main__':
    unittest.main()
