"""Independent exact-field and high-precision numerical Phase 13 checks."""
import unittest, random, math
from cut_capacity import (GreenGraph,cycles,random_green, graph_from_shift, reverse_cut_profile,
   exact_green, mat_add,mat_mul,rank_mod, fourier_mod, cut_profile,
   circuit_cut_budget,exact_cut_certificate, modular_cut_audit,
   approx_barrier_even_n)
from subset_gate import (subset_capacity,subset_certificate,
   structural_rank_lower_bound,error_barrier,hidden_bottleneck_graphs)

Q=65537


def block_rank(A,R,C):
    return rank_mod([[A[i][j] for j in C] for i in R],Q)

class Phase13(unittest.TestCase):
    def test_weighted_resolvent_inverse(self):
        rng=random.Random(1301)
        for n in (4,8,16,32,64):
            for _ in range(5):
                g=random_green(n,rng,zero_prob=.15)
                G=exact_green(g,Q)
                for i in range(n):
                    for j in range(n):
                        self.assertEqual((G[i][j]-g.weights[i]*G[g.pi[i]][j])%Q, int(i==j))

    def test_zero_weights_and_multicycles(self):
        n=16
        pi=[1,0,3,2,5,6,4,7,9,10,8,11,13,14,15,12]
        w=[3,0,3,7,2,2,2,0,3,0,0,17,1,2,3,4]
        g=GreenGraph(pi,w)
        G=exact_green(g,Q)
        for i in range(n):
            for j in range(n):
                self.assertEqual((G[i][j]-w[i]*G[pi[i]][j])%Q,int(i==j))
        for R in ({0,2,4},{1,3,5,7},{0,4,7,9,13},set(range(8))):
            C=set(range(n))-R
            fw,bw=subset_capacity(g,R)
            self.assertLessEqual(block_rank(G,sorted(R),sorted(C)),fw)
            self.assertLessEqual(block_rank(G,sorted(C),sorted(R)),bw)

    def test_cut_profile_bruteforce(self):
        rng=random.Random(1311)
        for n in (8,16,32,64,128):
            for _ in range(12):
                g=random_green(n,rng,zero_prob=.35)
                profile=cut_profile(g)
                rev=reverse_cut_profile(g)
                self.assertEqual(profile[0],0)
                self.assertEqual(profile[n],0)
                for m in range(1,n):
                    brute=sum(g.weights[i]!=0 and g.pi[i]>=m for i in range(m))
                    self.assertEqual(profile[m],brute)
                    fw,_=subset_capacity(g,set(range(m)))
                    self.assertEqual(profile[m],fw)
                    br=sum(g.weights[i]!=0 and g.pi[i]<m for i in range(m,n))
                    self.assertEqual(rev[m],br)

    def test_two_layer_arbitrary_weights_exact(self):
        rng=random.Random(1312)
        for n in (8,16,32,64):
            for rep in range(4):
                layers=[[random_green(n,rng,zero_prob=.15) for _ in range(2)]
                        for _ in range(2)]
                cuts=sorted({1,2,3,n//4,n//2,3*n//4,n-2,n-1})
                report=modular_cut_audit(layers,cuts,Q)
                self.assertTrue(all(row['actual_rank']<=row['capacity'] for row in report))

    def test_more_than_two_layers(self):
        rng=random.Random(1313)
        n=32
        layers=[[random_green(n,rng) for _ in range(3)] for _ in range(3)]
        c=modular_cut_audit(layers,[1,4,8,16,28],Q)
        self.assertEqual(len(c),5)

    def test_fourier_all_prefix_ranks_modular(self):
        for n in (4,8,16,32,64):
            F=fourier_mod(n,Q)
            for m in range(1,n):
                self.assertEqual(block_rank(F,range(m),range(m,n)),min(m,n-m))
                self.assertEqual(block_rank(F,range(m,n),range(m)),min(m,n-m))

    def test_exact_middle_cut_gap(self):
        n=64
        layers=[[graph_from_shift(n,s,Q,3) for s in (1,2)],
                [graph_from_shift(n,s,Q,3) for s in (3,4)]]
        proof=exact_cut_certificate(layers)
        self.assertTrue(proof['rejects'])
        self.assertEqual(proof['middle_capacity'],10)
        self.assertEqual(proof['middle_fourier_rank'],32)
        Tcheck=modular_cut_audit(layers,[16,24,32,40],Q)
        self.assertLessEqual(Tcheck[2]['actual_rank'],10)
        self.assertEqual(block_rank(fourier_mod(n,Q),range(32),range(32,n)),32)

    def test_hidden_crossing_not_visible_in_prefix(self):
        n=128;R={3,19,35,51,67,83,99,115}
        layers=hidden_bottleneck_graphs(n,sorted(R),seed=1307)
        prefix=exact_cut_certificate(layers)
        self.assertFalse(prefix['rejects'])
        hidden=subset_certificate(layers,R)
        self.assertEqual(hidden['cut_capacity_R_to_C'],4)
        self.assertEqual(hidden['cut_capacity_C_to_R'],4)
        self.assertEqual(hidden['Fourier_rank_lower_bound'],8)
        self.assertTrue(hidden['rejects_all_weight_assignments_for_these_graph_supports'])
        # Direct independently constructed finite-field matrices + full NTT.
        F=fourier_mod(n,Q)
        C=sorted(set(range(n))-R)
        self.assertEqual(block_rank(F,sorted(R),C),8)
        reports=modular_cut_audit(layers,[4,16,32,64],Q)
        self.assertTrue(reports)
        Gs=[exact_green(g,Q) for layer in layers for g in layer]
        T=mat_mul(mat_add(Gs[0],Gs[1],Q), mat_add(Gs[2],Gs[3],Q),Q)
        self.assertLessEqual(block_rank(T,sorted(R),C),4)
        self.assertLessEqual(block_rank(T,C,sorted(R)),4)

    def test_subset_rank_lower_universal(self):
        for n in range(2,130):
            for m in range(1,n):
                l=structural_rank_lower_bound(n,m)
                self.assertTrue(1<=l<=min(m,n-m))
                self.assertEqual(l,(m*(n-m)+n-1)//n)

    def test_precision_barriers_numeric(self):
        import numpy as np
        for n,m,c in [(32,16,5),(64,32,10),(128,64,10),(128,8,4)]:
            a=np.arange(n)
            U=np.exp(-2j*np.pi*np.outer(a,a)/n)/np.sqrt(n)
            B=U[:m,m:]
            s=np.linalg.svd(B,compute_uv=False)
            cert=error_barrier(n,m,c)
            self.assertLessEqual(cert['operator_error_at_least'],s[c]+1e-11)
            self.assertLessEqual(cert['relative_frobenius_error_at_least'],
                                 np.linalg.norm(s[c:])/np.sqrt(n)+1e-11)
            self.assertLessEqual(max(s),1.0000000001)
            self.assertAlmostEqual(sum(s*s),m*(n-m)/n,places=9)

    def test_general_subset_barrier_numeric(self):
        import numpy as np
        n=128; R=[3,19,35,51,67,83,99,115]
        C=sorted(set(range(n))-set(R))
        ids=np.arange(n)
        U=np.exp(-2j*np.pi*np.outer(ids,ids)/n)/np.sqrt(n)
        B=U[np.ix_(R,C)]
        s=np.linalg.svd(B,compute_uv=False)
        lower=error_barrier(n,len(R),4)
        self.assertLessEqual(lower['operator_error_at_least'],s[4]+1e-12)
        self.assertLessEqual(lower['relative_frobenius_error_at_least'],
                             np.linalg.norm(s[4:])/np.sqrt(n)+1e-12)

    def test_exact_cut_all_subsets_small(self):
        n=16
        gs=[graph_from_shift(n,s) for s in (1,2,4,8)]
        # Positive control: passes this necessary rank/cut gate, but is NOT
        # claimed to be an FFT factorization.
        req=[structural_rank_lower_bound(n,m) for m in range(n+1)]
        for mask in range(1, (1<<n)-1):
            R={i for i in range(n) if (mask>>i)&1}
            forward=sum(subset_capacity(g,R)[0] for g in gs)
            self.assertGreaterEqual(forward,req[len(R)])

if __name__=='__main__':unittest.main(verbosity=2)

class ExplicitExpander(unittest.TestCase):
    def test_expander_weighted_green_apply_exact(self):
        from explicit_expander import construction,apply_green_in_linear_work
        rng=random.Random(1903)
        for side in [4,8]:
            layers=construction(side)
            for g in [p for layer in layers for p in layer]:
                n=len(g.pi)
                x=[rng.randrange(Q) for _ in range(n)]
                dense=exact_green(g,Q)
                direct=[sum(a*v for a,v in zip(row,x))%Q for row in dense]
                quick,ops=apply_green_in_linear_work(g,x,Q)
                self.assertEqual(quick,direct)
                self.assertLessEqual(ops['mul'],4*n)
                self.assertLessEqual(ops['add_sub'],2*n+len(cycles(g.pi)))

    def test_expander_explicit_positive_topology(self):
        from explicit_expander import construction,uniform_gap_lower_bound
        from subset_gate import subset_capacity
        for side in (4,8,16,32):
            layers=construction(side)
            n=side*side
            self.assertGreater(uniform_gap_lower_bound(),1)
            self.assertEqual(sum(len(layer) for layer in layers),12)
            self.assertFalse(exact_cut_certificate(layers)['rejects'])
        side=4;n=side*side
        graphs=[g for layer in construction(side) for g in layer]
        for mask in range(1,2**n-1):
            subset={i for i in range(n) if mask>>i&1}
            cap=sum(subset_capacity(g,subset)[0] for g in graphs)
            self.assertGreaterEqual(cap,structural_rank_lower_bound(n,len(subset)))

    def test_expander_weight_arbitrary_not_fourier_factorization(self):
        from explicit_expander import construction
        n=16
        layers=construction(4)
        H=[]
        for layer in layers:
            term=None
            for g in layer:
                G=exact_green(g,Q)
                term=G if term is None else mat_add(term,G,Q)
            H.append(term)
        candidate=mat_mul(H[0],H[1],Q)
        F=fourier_mod(n,Q)
        errors=sum(v!=z for row1,row2 in zip(candidate,F)
                   for v,z in zip(row1,row2))
        self.assertGreater(errors,0)

    def test_numeric_expander_spectrum(self):
        from spectral_gate import gap
        from explicit_expander import construction,uniform_gap_lower_bound
        for side in [4,8,16]:
            layers=construction(side)
            g=[t for row in layers for t in row]
            numeric=gap(g)
            self.assertGreater(numeric['lambda_2'],1)
            self.assertGreaterEqual(numeric['lambda_2']+1e-8,uniform_gap_lower_bound())

class UniformExpanderEscape(unittest.TestCase):
    def test_twenty_term_uniform_architecture(self):
        """Five repeat copies have all-subsets capacity >= min(|R|,|C|).

        Analytical proof uses external Gabber-Galil 5 sqrt(2) spectral bound.
        These tests are finite verification of graphs, not proof of the bound.
        """
        from explicit_expander import construction,uniform_gap_lower_bound
        self.assertGreater(uniform_gap_lower_bound(5),2.0)
        for side in (4,8,16,32,64):
            layers=construction(side,copies=5)
            self.assertEqual(sum(map(len,layers)),20)
            a=exact_cut_certificate(layers)
            self.assertFalse(a['rejects'])
        side=4;n=16
        graphs=[g for layer in construction(side,copies=5) for g in layer]
        for mask in range(1,(1<<n)-1):
            subset={i for i in range(n) if (mask>>i)&1}
            forward=sum(subset_capacity(g,subset)[0] for g in graphs)
            backward=sum(subset_capacity(g,subset)[1] for g in graphs)
            self.assertGreaterEqual(min(forward,backward),min(len(subset),n-len(subset)))

    def test_spectrum_at_five_copies(self):
        from explicit_expander import construction,uniform_gap_lower_bound
        from spectral_gate import gap
        for side in (4,8,16):
            layers=construction(side,copies=5)
            vals=gap([g for layer in layers for g in layer])
            self.assertGreater(vals['lambda_2'],2)
            self.assertGreaterEqual(vals['lambda_2']+1e-9,uniform_gap_lower_bound(5))

