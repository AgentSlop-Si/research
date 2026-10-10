"""Independent Phase 18 tests with exact finite-field and complex checks."""
import math
import unittest
import numpy as np
from phase17_gauge import (P, modrank, modular_fourier, mod_matmul,
                           margulis_permutations, half_grid_permutation,
                           unitary_fourier, normalized_error_gap)
from phase18_curvature import (
    weighted_permutation,green_inverse,flat_weights,paired_difference_energy,
    direct_fourier_commutator,modular_phase_sum,GreenTerm,network_matrix,
    curvature_gate,forest_gauge_holonomies,modular_network,
)

class Phase18Tests(unittest.TestCase):
    def test_exact_frobenius_commutator_all_s(self):
        for s in (2,4,6,8,10,12,16):
            d=direct_fourier_commutator(s)
            self.assertAlmostEqual(np.linalg.norm(d,'fro')**2/(s*s),2.,places=11)

    def test_modular_exact_fourier_trace_identity(self):
        for s in (2,4,8,16):
            self.assertEqual(modular_phase_sum(s),0)

    def test_term_commutator_energy_identity(self):
        rng=np.random.default_rng(18001)
        for s in (4,6):
            n=s*s; tau=half_grid_permutation(s)
            Pi=np.eye(n)[tau]
            for perm in margulis_permutations(s):
                w=0.3*np.exp(2j*np.pi*rng.random(n))
                X=weighted_permutation(perm,w)
                D=X@Pi-Pi@X
                energy=paired_difference_energy(perm,w,tau)
                self.assertAlmostEqual(np.linalg.norm(D,'fro')**2,energy,places=10)
                G=green_inverse(perm,w)
                self.assertLess(np.linalg.norm(G@Pi-Pi@G-G@D@G,'fro'),1e-11)

    def _network(self,s,seed,mode):
        rng=np.random.default_rng(seed)
        n=s*s; maps=margulis_permutations(s)
        phase=np.ones(n,dtype=complex) if mode=='raw' else np.exp(2j*np.pi*rng.random(n))
        layers=[]
        for l in range(2):
            layer=[]
            for j in range(2):
                idx=l*2+j
                c=[0.13,0.17,0.21,0.25][idx]
                ref=flat_weights(maps[idx],c,phase)
                w=ref.copy()
                if mode=='raw':
                    # Small but nonzero symmetry-breaking energy.
                    touched=rng.choice(n,size=max(1,n//16),replace=False)
                    w[touched]*=np.exp(0.06j)
                elif mode=='flat':
                    touched=rng.choice(n,size=max(1,n//12),replace=False)
                    w[touched]*=np.exp(0.04j)
                else:
                    w*=np.exp(0.9j*rng.standard_normal(n))
                layer.append(GreenTerm(maps[idx],w,0.25,ref))
            layers.append(layer)
        return layers,phase

    def test_theorem_raw_paired_energy_nonvacuous(self):
        for s in (4,6,8):
            layers,d=self._network(s,1800+s,'raw')
            res=curvature_gate(s,layers,phase_gauge=d)
            self.assertGreater(res['raw_symmetry_error_floor'],0.4)
            self.assertLessEqual(res['raw_symmetry_error_floor'],res['actual_relative_fro_error']+1e-10)
            self.assertLessEqual(res['flat_gauge_error_floor'],res['actual_relative_fro_error']+1e-10)

    def test_phase_holonomy_energy_nonvacuous(self):
        for s in (4,6,8):
            layers,d=self._network(s,2800+s,'flat')
            res=curvature_gate(s,layers,phase_gauge=d)
            self.assertGreater(res['flat_gauge_error_floor'],0.10)
            self.assertLessEqual(res['flat_gauge_error_floor'],res['actual_relative_fro_error']+1e-10)

    def test_strong_curvature_does_not_invalidate_bounds(self):
        for s in (4,8):
            layers,d=self._network(s,3900+s,'strong')
            res=curvature_gate(s,layers,phase_gauge=d)
            self.assertGreaterEqual(res['actual_relative_fro_error']+1e-10,
                                    max(res['raw_symmetry_error_floor'],res['flat_gauge_error_floor']))

    def test_false_flat_reference_rejected(self):
        layers,d=self._network(4,1818,'flat')
        fake=np.exp(2j*np.pi*np.random.default_rng(41).random(16))
        with self.assertRaises(ValueError):
            curvature_gate(4,layers,phase_gauge=fake)
        with self.assertRaises(ValueError):
            curvature_gate(4,layers)

    def test_exact_forest_holonomy_recovery(self):
        rng=np.random.default_rng(28013)
        for s in (4,8):
            n=s*s; perms=margulis_permutations(s)
            scalars=[2,3,4,5]
            d=[int(x) for x in rng.integers(1,P,size=n)]
            weights=[[int(c)*d[i]*pow(d[int(perm[i])],-1,P)%P for i in range(n)]
                     for perm,c in zip(perms,scalars)]
            initial=forest_gauge_holonomies(perms,weights,scalars,P)
            self.assertEqual(initial['holonomy_count'],0)
            # First locate nontree edges in the canonical forest. Keep injected errors off it.
            # A loop or a genuine fundamental cycle always carries independent holonomy.
            tree_ids=set()
            from collections import deque
            adj=[[] for _ in range(n)]
            for t,perm in enumerate(perms):
                for i,j in enumerate(perm):
                    eid=t*n+i
                    adj[i].append((int(j),eid));adj[int(j)].append((i,eid))
            seen=set()
            for root in range(n):
                if root in seen:continue
                seen.add(root);q=deque([root])
                while q:
                    u=q.popleft()
                    for v,eid in adj[u]:
                        if v not in seen:
                            seen.add(v);tree_ids.add(eid);q.append(v)
            nontree=[eid for eid in range(len(perms)*n) if eid not in tree_ids]
            chosen=nontree[:min(4,len(nontree))]
            for eid in chosen:
                weights[eid//n][eid%n]=weights[eid//n][eid%n]*7%P
            found=forest_gauge_holonomies(perms,weights,scalars,P)
            self.assertEqual(found['holonomy_count'],len(chosen))
            self.assertEqual(found['edges'],4*n)
            self.assertEqual(found['tree_edges'],n-1)
            self.assertEqual(found['components'],1)
            self.assertTrue(all(x['holonomy_ratio']==7 for x in found['nontrivial_fundamental_holonomies']))

    def test_exact_modular_rank_perturbation_and_fourier_defect(self):
        rng=np.random.default_rng(188181)
        s=4;n=16;perms=margulis_permutations(s);scalars=[2,3,4,5]
        d=[int(x) for x in rng.integers(1,P,size=n)]
        ws=[np.asarray([c*d[i]*pow(d[int(perm[i])],-1,P)%P for i in range(n)],dtype=np.int64)
            for perm,c in zip(perms,scalars)]
        flat=[[GreenTerm(perms[l*2+j],ws[l*2+j].copy(),1) for j in range(2)] for l in range(2)]
        disturbed=[list(layer) for layer in flat]
        disturbed=[[GreenTerm(t.perm,t.weights.copy(),1) for t in layer] for layer in flat]
        k=3
        for index in [0,13,31]:
            t=index//n;i=index%n
            disturbed[t//2][t%2].weights[i]=(int(disturbed[t//2][t%2].weights[i])*3)%P
        base=modular_network(flat,P)
        changed=modular_network(disturbed,P)
        self.assertLessEqual(modrank((changed-base)%P),k)
        tau=half_grid_permutation(s)
        Q=np.zeros((n,n),dtype=np.int64)
        for j in range(n):Q[int(tau[j]),j]=d[int(tau[j])]*pow(d[j],-1,P)%P
        F=modular_fourier(n)
        defect=(mod_matmul(F,Q)-mod_matmul(Q,F))%P
        self.assertEqual(modrank(defect),n)
        self.assertLessEqual(modrank((changed-base)%P),k)
        self.assertGreater(n,2*k) # exact Fourier impossible in this rank-k neighborhood

    def test_rank_budget_matches_prior_phase17_theorem(self):
        from phase17_gauge import minimum_rank_budget
        for s in (4,8,16,32,64):
            self.assertGreater(minimum_rank_budget(s),0)
            self.assertAlmostEqual(normalized_error_gap(s)**2,
                                   (1-2/(s*math.sin(math.pi/s)))/4,places=12)

if __name__=='__main__': unittest.main()

class Phase18PolyphaseTests(unittest.TestCase):
    def test_exact_polyphase_conjugation_and_order_eight(self):
        from phase18_curvature import modular_polyphase_certificate
        for s in (2,4,8,16):
            r=modular_polyphase_certificate(s)
            self.assertEqual(r['fft_factorization_failures'],0,r)
            self.assertEqual(r['polyphase_conjugation_failures'],0,r)
            self.assertEqual(r['order_eight_failures'],0,r)

    def test_commutator_complete_singular_spectrum(self):
        from phase18_curvature import exact_commutator_singular_values
        for s in (2,4,6,8,10,12):
            observed=np.linalg.svd(direct_fourier_commutator(s),compute_uv=False)
            expected=exact_commutator_singular_values(s)
            np.testing.assert_allclose(observed,expected,rtol=2e-12,atol=2e-12)

    def test_rank_defect_spectral_formula_and_old_bound(self):
        from phase18_curvature import symmetry_rank_correction_floor
        s=8;n=s*s
        d=np.linalg.svd(direct_fourier_commutator(s),compute_uv=False)
        for k in (0,1,3,8,12,16,17,24,31,32):
            expected=.5*math.sqrt(np.sum(d[min(2*k,n):]**2)/n)
            self.assertAlmostEqual(symmetry_rank_correction_floor(n,k),expected,places=12)
            if k<n//2:self.assertGreater(symmetry_rank_correction_floor(n,k),0)
            else:self.assertEqual(symmetry_rank_correction_floor(n,k),0)

    def test_constructed_low_rank_perturbations_obey_floor(self):
        from phase18_curvature import symmetry_rank_correction_floor
        s=4;n=s*s;U=unitary_fourier(n)
        maps=margulis_permutations(s)
        P0=weighted_permutation(maps[0],.15*np.ones(n))
        T0=np.linalg.inv(np.eye(n)-P0)
        rng=np.random.default_rng(18122)
        for k in (0,1,2,4,7):
            D=rng.normal(size=(n,k))+1j*rng.normal(size=(n,k))
            E=rng.normal(size=(k,n))+1j*rng.normal(size=(k,n))
            T=T0+D@E
            actual=np.linalg.norm(U-T,'fro')/math.sqrt(n)
            self.assertGreaterEqual(actual+1e-10,symmetry_rank_correction_floor(n,k))

class Phase18LinearCostTests(unittest.TestCase):
    def test_linear_certificate_nonvacuous_and_dominates_dense_norm_bound(self):
        from phase18_curvature import linear_time_curvature_certificate
        v=Phase18Tests()
        for s in (4,8):
            for mode in ('raw','flat','strong'):
                layers,d=v._network(s,18100+s,mode)
                fast=linear_time_curvature_certificate(s,layers,phase_gauge=d)
                slow=curvature_gate(s,layers,phase_gauge=d)
                self.assertEqual(fast['read_weight_entries'],4*s*s)
                self.assertLessEqual(fast['relative_fro_error_floor_raw'],
                                     slow['actual_relative_fro_error']+1e-11)
                self.assertLessEqual(fast['relative_fro_error_floor_flat'],
                                     slow['actual_relative_fro_error']+1e-11)
                self.assertGreaterEqual(fast['bound_green_norm_g']+1e-9,
                                        slow['max_green_norm_g'])
    def test_linear_certificate_rejects_unstable_or_fake_references(self):
        from phase18_curvature import linear_time_curvature_certificate
        v=Phase18Tests();layers,d=v._network(4,18119,'flat')
        with self.assertRaises(ValueError):
            linear_time_curvature_certificate(4,layers,phase_gauge=np.ones(16))
        layers[0][0].weights[0]=1.1
        with self.assertRaises(ValueError):
            linear_time_curvature_certificate(4,layers,phase_gauge=d)

class Phase18ExactWeylGateTests(unittest.TestCase):
    def test_genuinely_curved_candidate_still_fails_fourier_weyl_gate(self):
        from phase18_curvature import modular_fourier_weyl_gate
        n=16;s=4
        self.assertTrue(modular_fourier_weyl_gate(modular_fourier(n))['passes'])
        rng=np.random.default_rng(182022)
        perms=margulis_permutations(s)
        layers=[]
        for l in range(2):
            layer=[]
            for j in range(2):
                perm=perms[l*2+j]
                weights=rng.integers(2,500,size=n,dtype=np.int64)
                layer.append(GreenTerm(perm,weights,1))
            layers.append(layer)
        T=modular_network(layers,P)
        result=modular_fourier_weyl_gate(T)
        self.assertFalse(result['passes'])
        self.assertGreater(result['weyl_defect_nonzeros'],0)
