import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest,random
from phase25_affine import (
    P, root, zigzag_order, affine_runs_zigzag, order_from_affine_runs,
    permuted_geometric_input, fourier_affine_geometric,
    zigzag_geometric_fft, direct_dft, cyclic_shift_successor,
    all_stride_ranks, zigzag_commutator_rank, cyclic_green_apply,
    apply_sparse_A, green_sum_apply, ZigzagGreenSumInverse,
    permutation_difference_rank
)
from phase24_ordering import successor_of_order


def rank_mod(A):
    if not A:return 0
    M=[row.copy() for row in A]
    n=len(M);m=len(M[0]);r=0
    for j in range(m):
        p=next((i for i in range(r,n) if M[i][j]),None)
        if p is None:continue
        M[r],M[p]=M[p],M[r]
        inv=pow(M[r][j],-1,P)
        for i in range(r+1,n):
            a=M[i][j]*inv%P
            if not a:continue
            for k in range(j+1,m):M[i][k]=(M[i][k]-a*M[r][k])%P
            M[i][j]=0
        r+=1
        if r==n:break
    return r


def green_matrix(order,alpha):
    n=len(order)
    ret=[]
    for j in range(n):
        ej=[0]*n;ej[j]=1
        ret.append(cyclic_green_apply(order,alpha,ej))
    return [[ret[j][i] for j in range(n)] for i in range(n)]


class Phase25Tests(unittest.TestCase):
    def test_01_zigzag_runs_reconstruct_order(self):
        for n in (8,16,32,64,128):
            self.assertEqual(order_from_affine_runs(n,affine_runs_zigzag(n)),zigzag_order(n))

    def test_02_exact_all_stride_rank(self):
        for n in (8,16,32,64,128,256):
            ranks=all_stride_ranks(n)
            self.assertEqual(min(ranks),n//2-1)
            self.assertEqual(ranks[1],n//2-1)
            self.assertEqual(ranks[n-3],n//2-1) # a=n-2
            self.assertTrue(all(r>=n//2-1 for r in ranks))

    def test_03_commutator_rank_near_maximal(self):
        for n in (8,16,32,64,128,256,512):
            self.assertEqual(zigzag_commutator_rank(n),n-2)

    def test_04_geometric_all_degenerate_types(self):
        for n in (8,16,32,64):
            w=root(n)
            for z in (0,1,P-1,2,23042,pow(w,n//4,P),w,pow(w,3,P)):
                expected=direct_dft(permuted_geometric_input(zigzag_order(n),z))
                self.assertEqual(zigzag_geometric_fft(n,z),expected,(n,z))

    def test_05_four_affine_runs(self):
        for n in (16,32,64):
            m=n//4
            runs=[(0,m,0,4),(m,m,4*(m-1)+1,-4),
                  (2*m,m,2,4),(3*m,m,4*(m-1)+3,-4)]
            order=order_from_affine_runs(n,runs)
            self.assertEqual(sorted(order),list(range(n)))
            for z in (0,1,2,24577,root(n)):
                self.assertEqual(fourier_affine_geometric(n,z,runs),
                    direct_dft(permuted_geometric_input(order,z)))

    def test_06_cyclic_green_equations(self):
        for n in (8,16,32,64,128,256):
            rng=random.Random(111+n)
            v=[rng.randrange(P) for _ in range(n)]
            for L in (zigzag_order(n),list(range(n))):
                for a in (0,2,7,54):
                    y=cyclic_green_apply(L,a,v)
                    self.assertEqual(apply_sparse_A(L,a,y),v)
                    self.assertEqual(cyclic_green_apply(L,a,apply_sparse_A(L,a,v)),v)

    def test_07_green_sum_exact_inverse(self):
        for n in (8,16,32,64,128,256,512):
            rng=random.Random(123+n)
            for alpha,beta in ((2,3),(17,29),(5,2)):
                v=[rng.randrange(P) for _ in range(n)]
                solve=ZigzagGreenSumInverse.create(n,alpha,beta)
                self.assertEqual(solve.apply(green_sum_apply(n,alpha,beta,v)),v)
                self.assertEqual(green_sum_apply(n,alpha,beta,solve.apply(v)),v)

    def test_08_exact_crosscut_rank_two(self):
        for n in (8,16,32,64):
            G1=green_matrix(zigzag_order(n),2)
            G2=green_matrix(list(range(n)),3)
            m=n//2
            for G in (G1,G2):
                self.assertEqual(rank_mod([row[m:] for row in G[:m]]),1)
            S=[[(G1[i][j]+G2[i][j])%P for j in range(n)] for i in range(n)]
            self.assertEqual(rank_mod([row[m:] for row in S[:m]]),2)
            w=root(n);inv=pow(n,-1,P)
            Fblock=[[pow(w,i*(j+m),P) for j in range(m)] for i in range(m)]
            self.assertEqual(rank_mod(Fblock),m)

    def test_09_resolvent_commutator_rank_exact(self):
        for n in (8,16,32):
            W=successor_of_order(zigzag_order(n))
            Z=cyclic_shift_successor(n)
            Gw=green_matrix(zigzag_order(n),2)
            Gz=green_matrix(list(range(n)),3)
            # W*Z and Z*W are permutation compositions on columns.
            self.assertEqual(permutation_difference_rank(
                    [W[Z[i]] for i in range(n)],
                    [Z[W[i]] for i in range(n)]),n-2)
            # Check [Gw,Gz] via dense products, independent of rank formula.
            A=[[0]*n for _ in range(n)]
            for i in range(n):
                for k in range(n):
                    a=Gw[i][k];b=Gz[i][k]
                    for j in range(n):
                        A[i][j]+=(a*Gz[k][j]-b*Gw[k][j])
                A[i]=[v%P for v in A[i]]
            self.assertEqual(rank_mod(A),n-2)

    def test_10_invalid_orders_rejected(self):
        n=16
        for runs in [[(0,16,0,2)],[(0,8,0,2)],[(0,8,0,2),(8,8,0,2)]]:
            with self.assertRaises(ValueError):order_from_affine_runs(n,runs)
        with self.assertRaises(ValueError):zigzag_order(6)


if __name__=='__main__':unittest.main()
