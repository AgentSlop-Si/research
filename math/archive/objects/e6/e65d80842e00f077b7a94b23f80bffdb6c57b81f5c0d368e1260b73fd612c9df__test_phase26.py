import math,random,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from phase26_cuts import *

class TestSimultaneousPhaseCut(unittest.TestCase):
    def test_partition_exact_balance(self):
        for n in (8,16,32,64,128):
            for k in range(1,n):
                left,right=phase_partition(n,k)
                self.assertEqual((len(left),len(right)),(n//2,n//2))
    def test_modular_pigeonhole(self):
        rng=random.Random(2601)
        for n in (16,64,128,256,1024):
            for s in (1,2,3):
                for trial in range(3):
                    steps=rng.sample(range(1,n),s)
                    k,r,hs=simultaneous_cut(n,steps)
                    self.assertTrue(all(abs(h)<n/r+1e-9 for h in hs))
                    self.assertEqual(len(phase_partition(n,k)[0]),n//2)
    def test_exact_crossing_translation(self):
        for n in (8,16,32,64):
            for k in range(1,n):
                for a in range(1,n):
                    self.assertEqual(translation_crossing(n,k,a),abs(signed_residue(k*a,n)))
    def test_affine_exception_certificate(self):
        for n in (16,32,64,128):
            for a in (2,n//2+2):
                order=two_run_zigzag(n,a)
                self.assertEqual(affine_edge_defects(order,[a,-a]),2)
                k,_=optimal_phase_cut(n,[a,1])
                left,right=phase_partition(n,k)
                self.assertLessEqual(crossing_edges(order,left,right),
                                     denominator_edge_bound(n,k,[a],2))
    def test_green_inverse_rank_same_as_edges(self):
        # Exact modular rank identity for a Green inverse across every cut.
        for n in (8,16,32,64):
            order=two_run_zigzag(n,n//2+2 if n>=16 else 2)
            for k in (1,2,3):
                left,right=phase_partition(n,k)
                matrix=cut_minor([Layer([Term(order,2)])],left,right)
                self.assertEqual(mod_rank(matrix),crossing_edges(order,left,right))
    def test_product_of_two_green_sums_internal_phases(self):
        rng=random.Random(2603)
        for n in (16,32,64,128):
            oa=two_run_zigzag(n,2)
            ob=two_run_zigzag(n,n//2+2)
            oc=list(range(n))
            layers=[]
            for t in range(3):
                terms=[]
                for j,order in enumerate([oa,ob,oc]):
                    d1=[rng.randrange(1,P) for _ in range(n)]
                    d2=[rng.randrange(1,P) for _ in range(n)]
                    terms.append(Term(order,2+j+t,left=d1,right=d2))
                diag=[rng.randrange(1,P) for _ in range(n)]
                layers.append(Layer(terms,diag))
            k,_=optimal_phase_cut(n,[2,n//2+2,1])
            left,right=phase_partition(n,k)
            rank=mod_rank(cut_minor(layers,left,right))
            bound=cut_rank_upper(layers,left,right)
            self.assertLessEqual(rank,bound)
    def test_random_order_not_affine_small_cut(self):
        n=128
        affine=two_run_zigzag(n,n//2+2)
        generic=generic_cycle(n,27182)
        k,_=optimal_phase_cut(n,[2,n//2+2,1])
        left,right=phase_partition(n,k)
        self.assertLess(crossing_edges(affine,left,right),crossing_edges(generic,left,right))

if __name__=='__main__':unittest.main()

class TestFourierAlternatingQuarterMinor(unittest.TestCase):
    def test_alternating_quarter_exact_fourier_minor_full_rank(self):
        # For n=4q, q even, the rows/cols are each two alternating quarters.
        # A parity-separated Vandermonde argument proves full rank at all sizes;
        # exact modular checks catch any orientation/indexing mistakes.
        for n in (8,16,32,64,128,256):
            left,right=phase_partition(n,2)
            w=pow(3,(P-1)//n,P)
            fourier=[[pow(w,(i*j)%n,P) for j in right] for i in left]
            self.assertEqual(mod_rank(fourier),n//2)

class TestAffineInternalPermutation(unittest.TestCase):
    def test_conjugation_and_rank_on_original_circuit(self):
        rng=random.Random(2677)
        for n in (32,64,128):
            p=affine_permutation(n,5,17)
            inverse=[0]*n
            for j,new in enumerate(p):inverse[new]=j
            lo=two_run_zigzag(n,2)
            hi=two_run_zigzag(n,n//2+2)
            L0=Layer([Term(lo,2,
                           left=[rng.randrange(1,P) for _ in range(n)],
                           right=[rng.randrange(1,P) for _ in range(n)]),
                      Term(list(range(n)),3)],
                     diag=[rng.randrange(1,P) for _ in range(n)])
            L1=Layer([Term(hi,4),Term(list(range(n)),5)],
                     diag=[rng.randrange(1,P) for _ in range(n)])
            moved=conjugate_affine_layer(L0,p)
            for _ in range(3):
                x=[rng.randrange(P) for _ in range(n)]
                original=L1.apply(permute_apply(p,L0.apply(x)))
                normal=L1.apply(moved.apply(permute_apply(p,x)))
                self.assertEqual(original,normal)
            u=5
            # The conjugated lower-stage zigzag uses +-2u, not +-2.
            k,_=optimal_phase_cut(n,[u*2, u, n//2+2, 1])
            left,right=phase_partition(n,k)
            columns=[inverse[j] for j in right]
            mat=[[0]*len(columns) for _ in left]
            for col,j in enumerate(columns):
                e=[0]*n;e[j]=1
                y=L1.apply(permute_apply(p,L0.apply(e)))
                for row,i in enumerate(left):mat[row][col]=y[i]
            ranks=mod_rank(mat)
            bound=cut_rank_upper([moved,L1],left,right)
            self.assertLessEqual(ranks,bound)
    def test_asymptotic_log_over_loglog_witnesses(self):
        for exponent in (32,64,128,256):
            n=1<<exponent
            # Small budgets are excluded even when every term brings a new
            # affine stride and up to two exceptions per Green cycle.
            small=next(q for q in range(1,exponent+1)
                       if not forbidden_by_coarse_cut(n,q))
            self.assertGreater(small,exponent//12)
            self.assertLess(small,exponent)

class TestSpectralLowerBounds(unittest.TestCase):
    def test_uniform_balanced_submatrix_floor_is_sharp(self):
        # R = even indices; C = the first N/2 consecutive columns.
        # Its normalized Fourier minor is precisely F_(N/2)/sqrt(2).
        import numpy as np
        for n in (16,32,64,128):
            row=np.arange(0,n,2)[:,None]
            col=np.arange(0,n//2)[None,:]
            b=np.exp(-2j*np.pi*(row*col)/n)/np.sqrt(n)
            singular=np.linalg.svd(b,compute_uv=False)
            self.assertLess(np.max(np.abs(singular - 1/np.sqrt(2))),3e-13)
    def test_multistage_constant_cut_budget(self):
        for n in (128,256,512,1024):
            orders=[two_run_zigzag(n,a) for a in (2,n//2+2,n//2+6)]+[list(range(n))]
            k,_=optimal_phase_cut(n,[2,n//2+2,n//2+6,1])
            left,right=phase_partition(n,k)
            edges=[crossing_edges(o,left,right) for o in orders]
            self.assertEqual(k,2)
            self.assertEqual(edges,[3,3,11,2])
            # Two stages, one Green term per ordering per stage.
            r=2*sum(edges)
            self.assertEqual(r,38)
            if n>=256:
                self.assertLess(r,n//4)
                self.assertGreater(error_floor(n,r),0)

class TestVariableGreenWeights(unittest.TestCase):
    def test_weighted_cycle_against_dense_equation(self):
        rng=random.Random(2690)
        for n in (8,16,32,64):
            order=two_run_zigzag(n,n//2+2 if n>=16 else 2)
            succ=successor(order)
            x=[rng.randrange(P) for _ in range(n)]
            gamma=[rng.randrange(1,P) for _ in range(n)]
            y=weighted_green_apply(order,gamma,x)
            by=[(y[succ[j]]-gamma[succ[j]]*y[j])%P for j in range(n)]
            self.assertEqual(by,[x[succ[j]] for j in range(n)])
    def test_weighted_green_inverse_cut_rank(self):
        rng=random.Random(2689)
        for n in (16,32,64):
            order=two_run_zigzag(n,n//2+2)
            gamma=[rng.randrange(1,P) for _ in range(n)]
            left,right=phase_partition(n,2)
            m=cut_minor([Layer([WeightedTerm(order,gamma)])],left,right)
            self.assertEqual(mod_rank(m),crossing_edges(order,left,right))
    def test_weighted_conjugation_and_two_stage_rank(self):
        rng=random.Random(264422)
        for n in (32,64,128,256):
            orders=[two_run_zigzag(n,a) for a in (2,n//2+2,n//2+6)]+[list(range(n))]
            def layer():
                terms=[]
                for order in orders:
                    weights=[rng.randrange(1,P) for _ in range(n)]
                    left=[rng.randrange(1,P) for _ in range(n)]
                    right=[rng.randrange(1,P) for _ in range(n)]
                    terms.append(WeightedTerm(order,weights,left,right))
                return Layer(terms,[rng.randrange(1,P) for _ in range(n)])
            low=layer();top=layer()
            k=2
            left,right=phase_partition(n,k)
            actual=mod_rank(cut_minor([low,top],left,right))
            self.assertLessEqual(actual,38)
            if n==256:self.assertEqual(actual,38)
            p=affine_permutation(n,5,7)
            moved=conjugate_affine_layer(low,p)
            x=[rng.randrange(P) for _ in range(n)]
            self.assertEqual(top.apply(permute_apply(p,low.apply(x))),
                             top.apply(moved.apply(permute_apply(p,x))))
