"""New full-rank stationary Toeplitz family numerical structural controls."""
import math
import unittest
import numpy as np
import stationary_toeplitz as st
import gram_union as gu
import unit_step_core as core
import one_root_chirp as orc


class StationaryToeplitzTests(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(1417)

    def test_distinct_node_remainder_and_toeplitz(self):
        for G,M in [(16,4),(32,4),(64,8),(128,8),(256,16),(512,16),(1024,32)]:
            K=G//M
            u=np.arange(M)
            E=(K*(u*(u-1)//2)+(K+1)*u)%G
            np.testing.assert_array_equal(E%K,u)
            for q in [1,2,M]:
                W,gram,defect=st.construction(G,M,q)
                self.assertEqual(np.linalg.matrix_rank(W),q)
                self.assertLess(defect,2e-10)
                np.testing.assert_allclose(gram,gram.conj().T,atol=2e-10)

    def test_fixed_stationary_factorization_at_multiple_blocks(self):
        G,M,m=128,8,3
        K=G//M
        fam=st.stationary_states(G,m,M,4)
        roots=orc.one_root_table(G)
        W,gram,_=st.construction(G,M,4,roots)
        tri=np.arange(M)*(np.arange(M)-1)//2
        for s in range(m):
            for r in (0,1,K//2,K-1):
                V=np.stack([np.conj(orc.local_phases(G,M,z,roots)[r,:]) for z in fam[s]],axis=1)
                D=roots[(-tri-(M*r+3*s)*np.arange(M))%G]
                np.testing.assert_allclose(V,D[:,None]*W,atol=1e-10)
                np.testing.assert_allclose(V.conj().T@V,gram,atol=2e-10)

    def test_q1_q2_matches_generic_gram_union(self):
        for G,m,M in [(32,3,4),(64,3,8),(128,3,8)]:
            x=self.rng.normal(size=G*m)+1j*self.rng.normal(size=G*m)
            for q in (1,2):
                new=st.stationary_eval(x,M,q)
                old=gu.union_projection(x,st.stationary_states(G,m,M,q),M)
                np.testing.assert_allclose(new.output,old.output,atol=1e-9)
                self.assertAlmostEqual(new.squared_residual_formula,old.residual_squared,delta=1e-8)

    def test_full_rank_arbitrary_dense_input_matches_numpy(self):
        for G,m,M in [(16,3,4),(32,5,4),(64,3,8),(128,3,8),(256,3,16)]:
            n=G*m
            x=self.rng.normal(size=n)+1j*self.rng.normal(size=n)
            res=st.stationary_eval(x,M,M)
            np.testing.assert_allclose(res.output,np.fft.fft(x)/math.sqrt(n),atol=4e-10)
            self.assertTrue(res.used_all_full_rank_channels)
            self.assertLess(res.squared_residual_formula,1e-7)
            self.assertLess(res.gram_toeplitz_defect,1e-9)
            self.assertEqual(res.operation_proxy['dyadic_green_scans'],n*M)

    def test_stationary_full_frame_is_noncommuting(self):
        for G,M in [(16,4),(64,8),(128,8),(256,16)]:
            W,Gamma,_=st.construction(G,M,M)
            # If all rank-one normalized column projectors commuted, full
            # rank would force mutual orthogonality, i.e. Gamma=M*I.
            # But E(u) mod K=u prevents Fourier rows from being orthogonal.
            self.assertGreater(np.max(abs(Gamma-M*np.eye(M))),1e-4)
            norms=np.linalg.norm(W,axis=0)
            self.assertAlmostEqual(float(norms[0]),math.sqrt(M),delta=1e-9)

    def test_rank_q_projection_still_cannot_be_exact_all_inputs(self):
        G,m,M=128,3,8
        n=G*m
        x=np.zeros(n,complex)
        x[1]=1.
        two=st.stationary_eval(x,M,2)
        self.assertGreater(two.squared_residual_formula,0.1)
        full=st.stationary_eval(x,M,M)
        self.assertLess(full.squared_residual_formula,1e-9)

    def test_same_clock_graph_union_collision_ceiling(self):
        import orbit_collision_gate as og
        for M in (2,4,8,16,32):
            for K in (M,2*M):
                G=K*M
                self.assertEqual(og.exact_unique_pairs(G,M),og.predicted_unique_pairs(G,M))
                self.assertLess(og.exact_unique_pairs(G,M),M*G)

if __name__=='__main__':unittest.main(verbosity=2)
