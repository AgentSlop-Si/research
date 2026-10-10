"""Independent tests for Phase 17 claims, including exact GF(65537) checks."""
from __future__ import annotations
import itertools
import math
import unittest
import numpy as np
from phase17_gauge import (
    P,GEN,half_grid_permutation,unitary_fourier,ratio_matrix,
    ratio_singular_values,ratio_c,normalized_error_gap,rank_k_error_gap,minimum_rank_budget,
    gauged_permutation_weights,two_sided_defect,optimal_intertwiner_for_gauges,modrank,mod_matmul,
    modular_fourier,monomial_normalizer,modular_gauged_symmetry_defect,
    margulis_permutations,green_of_weighted_perm,primitive_root,
    make_gauge_from_monomial
)

class Phase17Tests(unittest.TestCase):
    def test_four_by_four_gram_characteristic_polynomial(self):
        import sympy as sp
        rho=sp.symbols("rho",real=True)
        A=sp.eye(4);B=sp.eye(4)
        A[0,1]=A[1,0]=rho;A[2,3]=A[3,2]=-rho
        B[0,2]=B[2,0]=rho;B[1,3]=B[3,1]=-rho
        l=sp.symbols("l")
        got=sp.factor((l*sp.eye(4)-A*B).det())
        expected=(l-(1+rho)**2)*(l-(1-rho)**2)*(l-(1-rho**2))**2
        self.assertEqual(sp.simplify(got-expected),0)

    def test_four_singular_values_exact_formula(self):
        for s in [2,4,6,8,10,12]:
            vals=np.linalg.svd(ratio_matrix(s),compute_uv=False)
            expect=ratio_singular_values(s)
            np.testing.assert_allclose(vals[:4],expect,atol=2e-11,rtol=2e-12)
            self.assertLess(max(vals[4:],default=0),3e-11)

    def test_rank_bound_analytic_constant(self):
        for s in [4,6,8,10,12,16,32,64,128]:
            rho=2*ratio_c(s)
            self.assertTrue(0<rho<1)
            self.assertTrue(normalized_error_gap(s)>0.26)
            self.assertAlmostEqual(ratio_singular_values(s)[0]/(s*s),(1+rho)/2,places=12)

    def test_monomial_affine_intertwining_exact_modular(self):
        n=16; F=modular_fourier(n)
        for u in [1,3,5,7,9,11,13,15]:
            for a,b in [(0,0),(2,7),(11,5)]:
                Q,R=monomial_normalizer(n,u,a,b,c=123)
                self.assertTrue(np.array_equal(mod_matmul(F,Q),mod_matmul(R,F)))
                self.assertTrue(np.all(np.count_nonzero(Q,axis=0)==1))
                self.assertTrue(np.all(np.count_nonzero(R,axis=0)==1))

    def test_negative_nonlinear_half_shift_exact_modular(self):
        for s in [4,8]:
            n=s*s; pi=half_grid_permutation(s)
            F=modular_fourier(n)
            F_inv=modular_fourier(n,inverse=True)*pow(n,-1,P)%P
            Q=np.zeros((n,n),dtype=np.int64)
            Q[pi,np.arange(n)]=1
            conjugated=mod_matmul(mod_matmul(F,Q),F_inv)
            self.assertTrue(np.any(np.count_nonzero(conjugated,axis=0)>1))

    def test_rank_k_tradeoff_and_best_low_rank_corrections(self):
        rng=np.random.default_rng(17300)
        s=8;n=s*s
        di=np.exp(2j*np.pi*rng.random(n));do=np.exp(2j*np.pi*rng.random(n))
        U=unitary_fourier(n)
        Tg=optimal_intertwiner_for_gauges(s,di,do)
        resid=U-Tg
        u,svals,vh=np.linalg.svd(resid,full_matrices=False)
        for k in [0,1,2,3]:
            correction=(u[:,:k]*svals[None,:k])@vh[:k,:]
            T=Tg+correction
            fro=np.linalg.norm(U-T,'fro')/np.sqrt(n)
            spectral=np.linalg.norm(U-T,2)
            bound=rank_k_error_gap(s,k)
            self.assertGreaterEqual(fro+1e-10,bound)
            self.assertGreaterEqual(spectral+1e-10,bound)
        for side in [4,8,16,32,64,128]:
            nside=side*side
            need=minimum_rank_budget(side)
            self.assertGreater(need,0)
            self.assertGreater(rank_k_error_gap(side,need-1),0)
            self.assertEqual(rank_k_error_gap(side,need),0)

    def test_asymmetric_diagonal_bridge_rank_budget(self):
        rng=np.random.default_rng(17301)
        s=8;n=s*s;pi=half_grid_permutation(s)
        g1,g2=margulis_permutations(s)[:2]
        matrices=[]
        for g,coeff in [(g1,0.11),(g2,0.19)]:
            P0=np.zeros((n,n),dtype=complex)
            P0[np.arange(n),g]=coeff
            matrices.append(np.linalg.inv(np.eye(n)-P0))
        di=np.exp(2j*np.pi*rng.random(n))
        do=np.exp(2j*np.pi*rng.random(n))
        bridge=np.ones(n,dtype=complex)
        baseline=bridge.copy()
        # Two genuinely pair-asymmetric bridge edits, one per pair.
        for j in [0,1]:
            bridge[j]=np.exp(2j*np.pi*rng.random())
        self.assertEqual(sum(bridge[j]!=bridge[pi[j]] for j in range(n))//2,2)
        Tg=do[:,None]*(matrices[1]@np.diag(baseline)@matrices[0])/di[None,:]
        T=do[:,None]*(matrices[1]@np.diag(bridge)@matrices[0])/di[None,:]
        self.assertLessEqual(np.linalg.matrix_rank(T-Tg,tol=1e-9),2)
        self.assertGreater(rank_k_error_gap(s,2),0)
        self.assertGreaterEqual(np.linalg.norm(unitary_fourier(n)-T,'fro')/np.sqrt(n)+1e-10,
                                rank_k_error_gap(s,2))

    def test_phase_gauge_intertwining_gap_all_entries(self):
        rng=np.random.default_rng(17001)
        for s in [4,6,8,10]:
            n=s*s
            floor=2*normalized_error_gap(s)
            for _ in range(5):
                din=np.exp(2j*np.pi*rng.random(n))
                dout=np.exp(2j*np.pi*rng.random(n))
                defect=two_sided_defect(s,din,dout)
                normalized=np.linalg.norm(defect,'fro')/np.sqrt(n)
                self.assertGreaterEqual(normalized+1e-11,floor)

    def test_exact_frobenius_projection_into_intertwiner_space(self):
        rng=np.random.default_rng(17171)
        for s in [4,6,8]:
            n=s*s; tau=half_grid_permutation(s)
            di=np.exp(2j*np.pi*rng.random(n))
            do=np.exp(2j*np.pi*rng.random(n))
            U=unitary_fourier(n)
            q=gauged_permutation_weights(s,di)
            r=gauged_permutation_weights(s,do)
            Q=np.zeros((n,n),complex);R=np.zeros((n,n),complex)
            Q[tau,np.arange(n)]=q
            R[tau,np.arange(n)]=r
            best=optimal_intertwiner_for_gauges(s,di,do)
            self.assertLess(np.linalg.norm(best@Q-R@best),3e-13)
            defect=two_sided_defect(s,di,do)
            self.assertAlmostEqual(np.linalg.norm(U-best,'fro'),
                                   0.5*np.linalg.norm(defect,'fro'),places=11)
            self.assertGreaterEqual(np.linalg.norm(U-best,'fro')/np.sqrt(n)+1e-10,
                                    normalized_error_gap(s))
            # In the original half-grid basis the optimal T0 commutes with Pi.
            T0=best*di[None,:]/do[:,None]
            self.assertLess(np.linalg.norm(T0[:,tau]-T0[tau,:]),3e-13)

    def test_gauge_symmetry_of_margulis_reference(self):
        for s in [4,6,8]:
            pi=half_grid_permutation(s)
            for g in margulis_permutations(s):
                self.assertTrue(np.array_equal(g[pi],pi[g]))

    def test_independently_gauged_margulis_network(self):
        rng=np.random.default_rng(17017)
        for s in [4,8]:
            n=s*s
            g=margulis_permutations(s)[1]
            P0=np.zeros((n,n))
            P0[np.arange(n),g]=.12
            G=np.linalg.inv(np.eye(n)-P0)
            self.assertLess(np.linalg.norm(G[:,half_grid_permutation(s)]-G[half_grid_permutation(s),:]),1e-11)
            din=np.exp(2j*np.pi*rng.random(n))
            dout=np.exp(2j*np.pi*rng.random(n))
            T=dout[:,None]*G/din[None,:]
            U=unitary_fourier(n)
            self.assertGreaterEqual(np.linalg.norm(T-U,2)+1e-11,normalized_error_gap(s))
            Q=np.zeros((n,n),complex);R=np.zeros((n,n),complex)
            tau=half_grid_permutation(s)
            Q[tau,np.arange(n)]=gauged_permutation_weights(s,din)
            R[tau,np.arange(n)]=gauged_permutation_weights(s,dout)
            self.assertLess(np.linalg.norm(T@Q-R@T),1e-10)

    def test_distinct_internal_gauges_with_commuting_diagonal_bridge(self):
        rng=np.random.default_rng(17201)
        s=4;n=s*s;pi=half_grid_permutation(s)
        maps=margulis_permutations(s)
        G=[]
        for perm,coeff in [(maps[1],0.12),(maps[3],0.20)]:
            P0=np.zeros((n,n),dtype=complex)
            P0[np.arange(n),perm]=coeff
            G.append(np.linalg.inv(np.eye(n)-P0))
        d1=np.exp(2j*np.pi*rng.random(n))
        b=np.ones(n,dtype=complex)
        for j in range(n):
            if j<pi[j]:
                b[j]=b[pi[j]]=np.exp(2j*np.pi*rng.random())
        d2=d1/b
        L1=(d1[:,None]*G[0])/d1[None,:]
        L2=(d2[:,None]*G[1])/d2[None,:]
        T=L2@L1
        T0=(T*d1[None,:])/d2[:,None]
        self.assertLess(np.linalg.norm(T0[:,pi]-T0[pi,:]),1e-12)
        self.assertGreaterEqual(np.linalg.norm(T-unitary_fourier(n),2)+1e-10,
                                normalized_error_gap(s))

    def test_small_s2_exception_exists_exactly(self):
        n=4; s=2; z=primitive_root(n)
        # input tau(j)=1-j, u=-1,b=1, a=1; sqrt(z^-1) from 8th root.
        c=pow(pow(GEN,(P-1)//8,P),-1,P)
        Q,R=monomial_normalizer(n,u=3,a=1,b=1,c=c)
        F=modular_fourier(n)
        self.assertTrue(np.array_equal(mod_matmul(F,Q),mod_matmul(R,F)))
        pi=half_grid_permutation(s)
        self.assertEqual([int(np.nonzero(Q[:,j])[0][0]) for j in range(n)],list(pi))
        self.assertEqual([int(np.nonzero(R[:,j])[0][0]) for j in range(n)],list(pi))
        q=np.asarray([Q[pi[j],j] for j in range(n)])
        r=np.asarray([R[pi[j],j] for j in range(n)])
        di=make_gauge_from_monomial(pi,q)
        do=make_gauge_from_monomial(pi,r)
        E=modular_gauged_symmetry_defect(s,di,do)
        self.assertEqual(int(np.count_nonzero(E)),0)

    def test_generic_independent_gauge_full_rank_modular(self):
        rng=np.random.default_rng(17018)
        for s,repeats in [(4,7),(8,3)]:
            n=s*s
            # The determinant is not identically zero: D_in=D_out=I is full rank.
            one=np.ones(n,dtype=np.int64)
            self.assertEqual(modrank(modular_gauged_symmetry_defect(s,one,one)),n)
            for _ in range(repeats):
                di=rng.integers(1,P,size=n,dtype=np.int64)
                do=rng.integers(1,P,size=n,dtype=np.int64)
                self.assertEqual(modrank(modular_gauged_symmetry_defect(s,di,do)),n)

    def test_one_edge_perturbation_rank(self):
        s=4;n=s*s;g=margulis_permutations(s)[0]
        w=np.full(n,7,dtype=np.int64)
        G=green_of_weighted_perm(g,w)
        w2=w.copy();w2[6]=71
        G2=green_of_weighted_perm(g,w2)
        self.assertEqual(modrank((G2-G)%P),1)
        rng=np.random.default_rng(17019)
        di=rng.integers(1,P,size=n,dtype=np.int64)
        do=rng.integers(1,P,size=n,dtype=np.int64)
        D=np.asarray(do[:,None]*np.asarray([pow(int(z),-1,P) for z in di])[None,:]%P)
        T0=D*G%P;T=D*G2%P
        self.assertEqual(modrank((T-T0)%P),1)
        tau=half_grid_permutation(s)
        # T0 may NOT intertwine independent gauges if G doesn't commute? G does.
        # Defect of perturbation relative to T0 has rank at most two.
        defect=modular_gauged_symmetry_defect(s,di,do)
        qi=np.asarray([int(di[tau[j]])*pow(int(di[j]),-1,P)%P for j in range(n)],dtype=np.int64)
        ro=np.asarray([int(do[tau[j]])*pow(int(do[j]),-1,P)%P for j in range(n)],dtype=np.int64)
        delta=(T-T0)%P
        change=(delta[:,tau]*qi[None,:]-ro[tau,None]*delta[tau,:])%P
        self.assertLessEqual(modrank(change),2)

if __name__=='__main__':
    unittest.main()
