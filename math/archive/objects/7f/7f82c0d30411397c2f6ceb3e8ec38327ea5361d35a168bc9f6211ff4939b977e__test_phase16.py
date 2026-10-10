"""Exact finite-field and floating-point regression tests for Hero #0 Phase 16."""
import math
import unittest
import numpy as np
from phase16_gauge import (
    PRIME, find_root, fourier_mod, half_y, margulis_maps, monomial_centralizer_cases,
    monomial_commutator_mod, gauge_alpha, make_gauge_weights, recover_common_gauge,
    green_apply, apply_network, apply_network_stages, commutator_rank_for_gauge, rank_mod,
    phase_gauge_commutator_lower_bound, phase_gauge_e0_commutator,
    sparse_fourier_row_zeros, one_green_rook_no_go, numerical_one_green_check,
    one_green_approx_lower_bound, spanning_gauge_residuals,
)


class Phase16(unittest.TestCase):
    def test_exact_F4_two_mixed_green_layers_positive_control(self):
        from positive_small_factor import exact_F4_green_product
        import sympy as sp
        r=exact_F4_green_product()
        self.assertEqual(sp.simplify(r["Y"]*r["X"]-r["F"]),sp.zeros(4))
        self.assertEqual(sp.simplify(sum(r["stage_x"]["resolvents"],sp.zeros(4))-r["X"]),sp.zeros(4))
        self.assertEqual(sp.simplify(sum(r["stage_y"]["resolvents"],sp.zeros(4))-r["Y"]),sp.zeros(4))


    def test_monomial_classification_sufficiency_exact_field(self):
        for n in (4, 8, 16, 32, 64):
            root=find_root(n,PRIME)
            F=fourier_mod(n)
            for a,b in monomial_centralizer_cases(n):
                tau=[(a*j+b)%n for j in range(n)]
                weights=[pow(root,a*b*j%n,PRIME) for j in range(n)]
                C=monomial_commutator_mod(F,tau,weights)
                self.assertEqual(np.count_nonzero(C),0,(n,a,b))

    def test_monomial_classification_has_invalid_negative_controls(self):
        for n in (4,8,16,32):
            F=fourier_mod(n)
            tau=[(j+1)%n for j in range(n)]
            C=monomial_commutator_mod(F,tau,[1]*n)
            self.assertTrue(np.count_nonzero(C)>0)

    def test_half_y_is_nonaffine(self):
        for s in (4,6,8,16,32):
            tau=half_y(s); n=s*s; h=s//2
            self.assertEqual((tau[1]-tau[0])%n,1)
            self.assertNotEqual(tau[h],(h+tau[0])%n)

    def test_s2_half_y_affine_exception_still_excluded(self):
        tau=half_y(2)
        self.assertEqual(tau,[(1-j)%4 for j in range(4)])
        self.assertNotEqual((2*1)%4,0)  # b=1 fails the commuting condition
        F=fourier_mod(4)
        rng=np.random.default_rng(16222)
        for _ in range(10):
            d=[int(v) for v in rng.integers(1,PRIME,size=4)]
            C=monomial_commutator_mod(F,tau,gauge_alpha(tau,d))
            self.assertGreater(np.count_nonzero(C),0)

    def test_margulis_generators_commute_with_half_y(self):
        for s in (2,4,6,8,10,16):
            tau=half_y(s)
            for perm in margulis_maps(s):
                self.assertTrue(all(perm[tau[i]]==tau[perm[i]] for i in range(s*s)))

    def test_pure_gauge_recognition_and_rejection(self):
        rng=np.random.default_rng(16001)
        for s in (4,8,16):
            n=s*s;perms=margulis_maps(s);constants=[2,3,5,7]
            d=[int(x) for x in rng.integers(1,PRIME,size=n)]
            w=make_gauge_weights(perms,constants,d)
            recovered=recover_common_gauge(perms,w,constants)
            self.assertIsNotNone(recovered)
            self.assertEqual(make_gauge_weights(perms,constants,recovered),w)
            bad=[row[:] for row in w]
            bad[0][0]=(bad[0][0]+1)%PRIME or 1
            self.assertIsNone(recover_common_gauge(perms,bad,constants))

    def test_spanning_gauge_curvature_certificate(self):
        rng=np.random.default_rng(16200)
        s=8;n=s*s;perms=margulis_maps(s);c=[2,3,5,7]
        d=[int(x) for x in rng.integers(1,PRIME,size=n)]
        w=make_gauge_weights(perms,c,d)
        first=spanning_gauge_residuals(perms,w,c)
        self.assertEqual(first['components'],1)
        self.assertEqual(first['generator_edge_occurrences'],4*n)
        self.assertEqual(first['defects'],[])
        # Find a chord edge (a non-tree edge in this canonical gauge).
        # Editing a self-loop is especially convenient: its transport is a
        # gauge-invariant holonomy regardless of the spanning tree.
        loop=next((j,i) for j,perm in enumerate(perms) for i in range(n)
                  if perm[i]==i)
        t,i=loop
        edited=[row[:] for row in w]
        edited[t][i]=(edited[t][i]*2)%PRIME
        self.assertIsNone(recover_common_gauge(perms,edited,c))
        r=spanning_gauge_residuals(perms,edited,c)
        self.assertEqual(r['components'],1)
        self.assertGreaterEqual(len(r['defects']),1)
        self.assertEqual(len(r['defects']),1)
        self.assertEqual(r['defects'][0]['vertex'],i)

    def test_exact_green_diagonal_conjugation(self):
        rng=np.random.default_rng(16002)
        for s in (4,8):
            n=s*s;perms=margulis_maps(s);constants=[2,3,5,7]
            d=[int(x) for x in rng.integers(1,PRIME,size=n)]
            weights=make_gauge_weights(perms,constants,d)
            constant_weights=[[c]*n for c in constants]
            tau=half_y(s)
            a=gauge_alpha(tau,d)
            for trial in range(5):
                x=[int(v) for v in rng.integers(0,PRIME,size=n)]
                left=apply_network(perms,weights,x)
                xdi=[x[i]*pow(d[i],-1,PRIME)%PRIME for i in range(n)]
                z=apply_network(perms,constant_weights,xdi)
                right=[d[i]*z[i]%PRIME for i in range(n)]
                self.assertEqual(left,right)
                qx=[0]*n
                for j in range(n):qx[tau[j]]=a[j]*x[j]%PRIME
                lhs=apply_network(perms,weights,qx)
                qtx=[0]*n
                for j in range(n):qtx[tau[j]]=a[j]*left[j]%PRIME
                self.assertEqual(lhs,qtx)

    def test_gauged_commutator_nonzero_modular(self):
        rng=np.random.default_rng(16003)
        for s in (4,8,16):
            n=s*s;F=fourier_mod(n);tau=half_y(s)
            d=[int(x) for x in rng.integers(1,PRIME,size=n)]
            C=monomial_commutator_mod(F,tau,gauge_alpha(tau,d))
            self.assertTrue(np.count_nonzero(C)>0)

    def test_zariski_generic_commutator_rank(self):
        rng=np.random.default_rng(16004)
        for s in (4,8,16):
            n=s*s
            self.assertEqual(commutator_rank_for_gauge(s,[1]*n),n)
            for trial in range(3):
                d=[int(x) for x in rng.integers(1,PRIME,size=n)]
                self.assertEqual(commutator_rank_for_gauge(s,d),n)

    def test_rank_k_defect_relative_to_gauged_baseline(self):
        rng=np.random.default_rng(16005)
        s=4;n=s*s;perms=margulis_maps(s);c=[2,3,5,7]
        d=[int(x) for x in rng.integers(1,PRIME,size=n)]
        w=make_gauge_weights(perms,c,d)
        modified=[row[:] for row in w]
        k=3
        for j,i in [(0,0),(1,5),(2,9)]:
            modified[j][i]=modified[j][i]*3%PRIME
        baseline=np.asarray([apply_network_stages(perms,[w,w],[int(i==col) for i in range(n)])
                             for col in range(n)],dtype=np.int64).T
        newer=np.asarray([apply_network_stages(perms,[modified,w],[int(i==col) for i in range(n)])
                          for col in range(n)],dtype=np.int64).T
        defect=(newer-baseline)%PRIME
        self.assertLessEqual(rank_mod(defect),k)
        tau=half_y(s);a=gauge_alpha(tau,d)
        qmat=np.zeros((n,n),dtype=np.int64)
        for j in range(n):qmat[tau[j],j]=a[j]
        comm=(newer@qmat-qmat@newer)%PRIME
        self.assertLessEqual(rank_mod(comm),2*k)
        F=fourier_mod(n)
        self.assertGreater(rank_mod((F@qmat-qmat@F)%PRIME),2*k)

    def test_phase_only_bound_strictly_positive(self):
        last=0
        for s in (4,6,8,16,32,64):
            val=phase_gauge_commutator_lower_bound(s)
            self.assertGreater(val,0)
            self.assertGreaterEqual(val+1.e-12,last)
            last=val
        self.assertAlmostEqual(phase_gauge_commutator_lower_bound(4),math.sin(math.pi/16),places=10)

    def test_phase_only_bound_all_gauges(self):
        rng=np.random.default_rng(16006)
        for s in (4,6,8,10,16,32):
            n=s*s;bound=2*phase_gauge_commutator_lower_bound(s)
            for _ in range(12):
                d=np.exp(2j*np.pi*rng.random(n))
                actual=phase_gauge_e0_commutator(s,d)
                self.assertGreaterEqual(actual+1.e-10,bound)

    def test_fourier_rows_versus_weighted_permutation_support(self):
        rng=np.random.default_rng(16007)
        cases=((9,73),(16,65537),(25,101),(36,73),(64,65537))
        for n,p in cases:
            for _ in range(90):
                i,j=map(int,rng.integers(0,n,size=2))
                w=int(rng.integers(1,p))
                z,g=sparse_fourier_row_zeros(n,i,j,w,p)
                self.assertLessEqual(z,g)
                if j!=i:
                    self.assertIn(z,(0,g))

    def test_row_support_lower_bound_is_sharp(self):
        n=16;p=65537
        zeros,g=sparse_fourier_row_zeros(n,0,n//2,1,p)
        self.assertEqual(zeros,g)
        self.assertEqual(g,n//2)

    def test_rook_no_go_all_s_at_least_three(self):
        for s in range(3,100):
            r=one_green_rook_no_go(s)
            self.assertGreater(r['minimum_row_support'],r['rook_row_degree'])

    def test_approximation_bound(self):
        for s in (4,5,6,8):
            r=numerical_one_green_check(s,.30)
            self.assertGreaterEqual(r['observed_rel_fro_error']+1.e-10,r['proved_lower_bound'])

    def test_approximation_bound_allows_any_complex_weights(self):
        for n in (16,36,64,100):
            d=2*int(math.sqrt(n))-1
            a=d/n
            if a>=.5:continue
            for rho in (.1,.5,2):
                b=one_green_approx_lower_bound(n,d,rho)
                self.assertGreater(b,0)

if __name__=='__main__':
    unittest.main()
