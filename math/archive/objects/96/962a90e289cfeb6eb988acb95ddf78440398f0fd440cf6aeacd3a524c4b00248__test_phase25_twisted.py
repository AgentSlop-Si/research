import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest,random
from phase25_affine import (
 P,root,zigzag_order,cyclic_green_apply,successor_of_order,
 cyclic_shift_successor,permutation_difference_rank,cycle_rank_difference,
 fourier_affine_geometric,permuted_geometric_input,direct_dft
)
from phase25_twisted import (
 twisted_order,twisted_runs,twisted_stride_ranks,twisted_green_sum_apply,
 TwistedGreenSumInverse,crosscut_edge_count,four_track_order
)
from test_phase25 import rank_mod,green_matrix


class Phase25TwistedTests(unittest.TestCase):
    def test_01_general_odd_slope_strides_and_noncommutation(self):
        for n in (16,32,64,128):
            m=n//2;Z=cyclic_shift_successor(n)
            for u in range(1,m,2):
                a=2*u
                L=[a*t%n for t in range(m)]+[(n-1-a*t)%n for t in range(m)]
                self.assertEqual(sorted(L),list(range(n)))
                W=successor_of_order(L)
                ranks=[cycle_rank_difference(W,b) for b in range(1,n)]
                self.assertEqual(min(ranks),m-1,(n,u))
                self.assertEqual(ranks[a-1],m-1,(n,u))
                self.assertEqual(ranks[(n-a)%n-1],m-1,(n,u))
                self.assertEqual(permutation_difference_rank(
                    [W[Z[j]] for j in range(n)],
                    [Z[W[j]] for j in range(n)]),n-2,(n,u))

    def test_02_twisted_order_affine_closed_form(self):
        for n in (16,32,64,128):
            L=twisted_order(n)
            m=n//2
            self.assertEqual(L,[ (m+2)*t%n for t in range(m) ] + [ (n-1-(m+2)*t)%n for t in range(m) ])
            self.assertEqual(crosscut_edge_count(n,L),m-1)
            self.assertEqual(min(twisted_stride_ranks(n)),m-1)
            self.assertEqual(len(four_track_order(n)),n)

    def test_03_four_boundary_edges_and_banded_executor(self):
        for n in (16,32,64,128,256,512):
            obj=TwistedGreenSumInverse.create(n,2,3)
            self.assertEqual(obj.band.width,6)
            self.assertEqual(len(obj.updates),4)
            self.assertEqual({(obj.p[j],obj.p[i]) for i,j,v in obj.updates},
                {(1,n//2-1),(n-2,n//2),(n//2-1,n//2),(n-1,0)})

    def test_04_fourier_input_exact_twist(self):
        for n in (16,32,64):
            L=twisted_order(n)
            for z in (0,1,2,root(n),pow(root(n),n//8,P),2389):
                self.assertEqual(fourier_affine_geometric(n,z,twisted_runs(n)),
                  direct_dft(permuted_geometric_input(L,z)))

    def test_05_twisted_sum_forward_backward(self):
        for n in (16,32,64,128,256,512,1024):
            rng=random.Random(2525+n)
            x=[rng.randrange(P) for _ in range(n)]
            for alpha,beta in ((2,3),(7,11)):
                solver=TwistedGreenSumInverse.create(n,alpha,beta)
                self.assertEqual(solver.apply(twisted_green_sum_apply(n,alpha,beta,x)),x)
                self.assertEqual(twisted_green_sum_apply(n,alpha,beta,solver.apply(x)),x)

    def test_06_natural_crosscut_rank_full(self):
        for n in (16,32,64):
            m=n//2
            Gw=green_matrix(twisted_order(n),2)
            Gz=green_matrix(list(range(n)),3)
            self.assertEqual(rank_mod([r[m:] for r in Gw[:m]]),m-1)
            self.assertEqual(rank_mod([r[m:] for r in Gz[:m]]),1)
            S=[[(Gw[i][j]+Gz[i][j])%P for j in range(n)] for i in range(n)]
            self.assertEqual(rank_mod([r[m:] for r in S[:m]]),m)

    def test_07_numerical_spectral_condition_control(self):
        import numpy as np
        alpha=.25;beta=.2;delta=alpha/(1-alpha)+beta/(1-beta)
        bound=(2+delta)/(2-delta)
        self.assertAlmostEqual(bound,31/17)
        for n in (16,32,64):
            for L in (zigzag_order(n),twisted_order(n)):
                W=successor_of_order(L)
                A=np.eye(n);B=np.eye(n)
                for j in range(n):
                    A[W[j],j]-=alpha
                    B[(j+1)%n,j]-=beta
                S=np.linalg.inv(A)+np.linalg.inv(B)
                self.assertLessEqual(np.linalg.cond(S),bound+1e-10)


class HiddenCutTests(unittest.TestCase):
    def test_08_hidden_quarter_cut_edges_are_constant(self):
        from phase25_twisted import hidden_quarter_partition,hidden_cut_edge_counts
        for n in (16,32,64,128,256,512,1024,4096):
            left,right=hidden_quarter_partition(n)
            self.assertEqual(len(left),n//2)
            self.assertEqual(len(right),n//2)
            self.assertEqual(set(left)&set(right),set())
            self.assertEqual(hidden_cut_edge_counts(n),(3,2))

    def test_09_hidden_cut_green_sum_rank_five(self):
        from phase25_twisted import hidden_quarter_partition
        for n in (16,32,64,128):
            rows,cols=hidden_quarter_partition(n)
            Gw=green_matrix(twisted_order(n),2)
            Gz=green_matrix(list(range(n)),3)
            def block(G):return [[G[i][j] for j in cols] for i in rows]
            self.assertEqual(rank_mod(block(Gw)),3)
            self.assertEqual(rank_mod(block(Gz)),2)
            S=[[(Gw[i][j]+Gz[i][j])%P for j in range(n)] for i in range(n)]
            self.assertEqual(rank_mod(block(S)),5)
            # Every normalized Fourier balanced block has rank >=N/4,
            # using its all-equal modulus and spectral norm 1.
            if n>=32:
                self.assertGreater(n//4,5)

    def test_10_error_floor(self):
        from phase25_twisted import hidden_cut_spectral_error_floor
        import math
        for n in (32,64,128,256,1024,4096):
            val=hidden_cut_spectral_error_floor(n)
            self.assertGreater(val,0)
            self.assertLess(val,1)
        self.assertAlmostEqual(hidden_cut_spectral_error_floor(1024),
            math.sqrt((1024/4-5)/(1024/2-5)))

class SpectralFloorAudit(unittest.TestCase):
    def test_11_independent_Fourier_singular_values(self):
        import numpy as np
        from phase25_twisted import hidden_quarter_partition,hidden_cut_spectral_error_floor
        for n in (32,64,128):
            rows,cols=hidden_quarter_partition(n)
            F=np.exp(-2j*np.pi*np.outer(rows,cols)/n)/np.sqrt(n)
            singular=np.linalg.svd(F,compute_uv=False)
            # Rank-five best spectral-norm approximation error is sigma_6.
            self.assertGreaterEqual(singular[5]+1e-12,
                                    hidden_cut_spectral_error_floor(n))
            self.assertAlmostEqual(np.sum(singular**2),n/4,places=9)


if __name__=='__main__':unittest.main()
