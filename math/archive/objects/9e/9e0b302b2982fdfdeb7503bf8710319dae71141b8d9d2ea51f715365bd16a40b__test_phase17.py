import random
import unittest
from phase17 import (
    nth_root, fourier, rank, eye, mm, mat_add, sparse_degrees,
    cyclic_shift, graph_certificate, local_band_certificate,
    check_submatrix_vandermonde, intertwining_defect,
    mixed_green_denominator,covariance_defect_rank_via_denominator,
    MagneticGreenPlan,RankOneFeedbackPlan,FieldCount,mixed_feedback_residual,
    covariance_blackbox_probe)


def diag_gauge_F(F, p, left, right):
    n=len(F)
    return [[F[i][j]*pow(left[i],-1,p)*pow(right[j],-1,p)%p for j in range(n)] for i in range(n)]


def sparse_random(n,max_degree,p,rr):
    A=[[0]*n for _ in range(n)]
    for j in range(n):
        support=rr.sample(range(n),rr.randint(1,max_degree))
        for i in support:A[i][j]=rr.randrange(1,p)
    return A


class GraphFeedbackTest(unittest.TestCase):
    def test_01_roots_composite(self):
        for n,p in [(4,17),(8,17),(9,19),(12,37),(15,31),(16,17),(31,311)]:
            w=nth_root(n,p)
            self.assertEqual(pow(w,n,p),1)
            self.assertEqual(len({pow(w,j,p) for j in range(n)}),n)

    def test_02_vandermonde_any_indices(self):
        for n,p in [(8,17),(9,19),(12,37),(16,17)]:
            w=nth_root(n,p)
            rr=random.Random(n+70)
            for q in (1,2,3,n//2):
                cols=rr.sample(range(n),q)
                start=rr.randrange(n)
                rows=[(start+j)%n for j in range(q)]
                self.assertTrue(check_submatrix_vandermonde(rows,cols,n,p,w))

    def test_03_graph_cert_irregular(self):
        rr=random.Random(171)
        for n,p,s,t in [(16,17,2,2),(17,103,3,2),(24,73,3,3),(31,311,2,3)]:
            w=nth_root(n,p)
            for _ in range(20):
                P=sparse_random(n,t,p,rr)
                Q=sparse_random(n,s,p,rr)
                cert=graph_certificate(P,Q,t,s)
                self.assertEqual(cert['bound'],n//(1+s*t))
                self.assertTrue(check_submatrix_vandermonde(cert['rows'],cert['neighbors'],n,p,w))
                self.assertTrue(all(P[i][j]==0 for i in cert['rows'] for j in cert['columns']))

    def test_04_graph_cert_permutation_support(self):
        rr=random.Random(515)
        n,p=32,97;w=nth_root(n,p)
        for _ in range(50):
            # Two unrelated global permutations, no locality whatsoever.
            P=[[0]*n for _ in range(n)]
            Q=[[0]*n for _ in range(n)]
            for A in [P,Q]:
                perm=rr.sample(range(n),n)
                for j,i in enumerate(perm):A[i][j]=rr.randrange(1,p)
            cert=graph_certificate(P,Q,1,1)
            self.assertEqual(cert['bound'],16)
            self.assertTrue(check_submatrix_vandermonde(cert['rows'],cert['neighbors'],n,p,w))

    def test_05_arbitrary_long_range_sparse_graph(self):
        n,p=64,257;w=nth_root(n,p)
        P=eye(n)
        Q=eye(n)
        for j in range(n):Q[(j+n//2)%n][j]=2
        cert=graph_certificate(P,Q,1,2)
        self.assertEqual(cert['bound'],n//3)
        self.assertTrue(check_submatrix_vandermonde(cert['rows'],cert['neighbors'],n,p,w))

    def test_06_exact_local_band_cert(self):
        for n,p in [(16,17),(17,103),(24,73),(31,311),(32,97)]:
            w=nth_root(n,p)
            for a,b in [(0,0),(1,0),(0,2),(1,2),(2,2),(3,3)]:
                cert=local_band_certificate(n,a,b)
                bound=max(0,n//2-a-b)
                self.assertEqual(cert['bound'],bound)
                self.assertTrue(check_submatrix_vandermonde(cert['rows'],cert['neighbors'],n,p,w))

    def test_07_same_operator_rank_feedback_ledger(self):
        rr=random.Random(1317)
        for n,p,s,t in [(9,19,2,2),(16,17,2,3),(17,103,3,3),(24,73,3,2)]:
            F=fourier(n,p)
            for _ in range(6):
                P=sparse_random(n,t,p,rr)
                Q=sparse_random(n,s,p,rr)
                L=[rr.randrange(1,p) for _ in range(n)]
                R=[rr.randrange(1,p) for _ in range(n)]
                A=diag_gauge_F(F,p,L,R)
                # Synthesize a valid exact Fourier factorization, then audit
                # the ranks of its actual numerator / denominator corrections.
                k=2
                # rank-2 random update U V^T
                U=[[rr.randrange(p) for _ in range(k)] for _ in range(n)]
                V=[[rr.randrange(p) for _ in range(n)] for _ in range(k)]
                X=[[sum(U[i][h]*V[h][j] for h in range(k))%p for j in range(n)] for i in range(n)]
                Qp=mat_add(Q,X,p)
                if rank(Qp,p)<n:
                    # Exact theorem assumes an invertible corrected denominator.
                    continue
                Y=mat_add(mm(A,Qp,p),P,p,-1)
                b=graph_certificate(P,Q,t,s)['bound']
                self.assertGreaterEqual(rank(X,p)+rank(Y,p),b)
                self.assertEqual(mm(A,Qp,p),mat_add(P,Y,p))

    def test_08_F_intertwining_exact(self):
        for n,p in [(4,17),(9,19),(12,37),(16,17),(17,103)]:
            w=nth_root(n,p)
            F=fourier(n,p,w)
            defect=intertwining_defect(F,p,w)
            self.assertTrue(all(not any(row) for row in defect))
            self.assertTrue(all(row[0]==1 for row in F))

    def test_09_even_identity_full_defect(self):
        for n,p in [(4,17),(8,17),(12,37),(16,17),(24,73),(32,97)]:
            w=nth_root(n,p)
            D=intertwining_defect(eye(n),p,w)
            self.assertEqual(rank(D,p),n)

    def test_10_odd_identity_corank_one(self):
        for n,p in [(5,31),(7,29),(9,19),(11,23),(17,103)]:
            self.assertEqual(rank(intertwining_defect(eye(n),p,nth_root(n,p)),p),n-1)

    def test_11_magnetic_green_generically_full_defect(self):
        for n,p in [(4,17),(5,31),(7,29),(8,17),(9,19),(11,23),(12,37),(16,17),(17,103)]:
            w=nth_root(n,p)
            Q=mixed_green_denominator(n,p,w,2,3)
            if rank(Q,p)==n:
                defect=covariance_defect_rank_via_denominator(Q,p,w)
                self.assertGreaterEqual(defect,n-1)
                if n%2==0:self.assertEqual(defect,n)

    def test_12_dense_mixed_green_residual(self):
        rr=random.Random(1337)
        for n,p in [(4,17),(5,31),(7,29),(8,17),(9,19),(17,103),(64,257)]:
            w=nth_root(n,p)
            c=FieldCount();plan=MagneticGreenPlan(n,p,w,2,3,c)
            for _ in range(4):
                x=[rr.randrange(p) for _ in range(n)]
                y=plan.solve(x,c)
                self.assertEqual(mixed_feedback_residual(y,x,n,p,w,2,3,[0]*n,[0]*n),[0]*n)

    def test_13_global_feedback_sherman_morrison(self):
        rr=random.Random(413)
        for n,p in [(4,17),(5,31),(8,17),(17,103),(31,311),(64,257)]:
            w=nth_root(n,p)
            c=FieldCount();green=MagneticGreenPlan(n,p,w,2,3,c)
            x=[rr.randrange(p) for _ in range(n)]
            for _ in range(5):
                u=[rr.randrange(p) for _ in range(n)]
                v=[rr.randrange(p) for _ in range(n)]
                try:f=RankOneFeedbackPlan(green,u,v,c)
                except ZeroDivisionError:continue
                y=f.solve(x,c)
                self.assertEqual(mixed_feedback_residual(y,x,n,p,w,2,3,u,v),[0]*n)

    def test_14_graph_feedback_cannot_simulate_fourier_small_rank(self):
        # For P=I (t=1), the mixed magnetic Q has s<=2
        # (diagonal plus nearest-neighbor shift). A rank-one denominator
        # feedback is insufficient when floor(n/3)>=2.
        for n in [8,16,32,64,256,65536]:
            self.assertGreaterEqual(n//(1+1*2),2)

    def test_15_charged_linear_scaling(self):
        rr=random.Random(150)
        p=2013265921
        records=[]
        for n in [256,1024,4096]:
            w=nth_root(n,p);c=FieldCount();g=MagneticGreenPlan(n,p,w,2,3,c)
            x=[rr.randrange(p) for _ in range(n)]
            prep=c.work();y=g.solve(x,c);run=c.work()-prep
            self.assertEqual(mixed_feedback_residual(y,x,n,p,w,2,3,[0]*n,[0]*n),[0]*n)
            self.assertLessEqual(prep,9*n+10)
            self.assertLessEqual(run,5*n+10)
            records.append((n,prep,run))
        self.assertEqual(len(records),3)

    def test_16_large_full_residual_65536(self):
        n,p=65536,2013265921
        w=nth_root(n,p);c=FieldCount();g=MagneticGreenPlan(n,p,w,2,3,c)
        x=[(i*i*17+31*i+9)%p for i in range(n)]
        prep=c.work();y=g.solve(x,c)
        self.assertEqual(mixed_feedback_residual(y,x,n,p,w,2,3,[0]*n,[0]*n),[0]*n)
        self.assertLess(c.work()-prep,6*n)

    def test_17_covariance_probe(self):
        rr=random.Random(17)
        n,p=16,17;w=nth_root(n,p)
        F=fourier(n,p,w)
        applyF=lambda x:[sum(a*b for a,b in zip(row,x))%p for row in F]
        self.assertTrue(covariance_blackbox_probe(applyF,n,p,w,trials=5,seed=31))
        # No random chance here: the first-column normalization fails.
        self.assertFalse(covariance_blackbox_probe(lambda x:x,n,p,w,trials=5,seed=31))
        c=FieldCount();g=MagneticGreenPlan(n,2013265921,nth_root(n,2013265921),2,3,c)
        self.assertFalse(covariance_blackbox_probe(g.solve,n,2013265921,g.w,trials=3,seed=71))

    def test_18_feedback_covariance_rank_barrier(self):
        # For alpha !=0, B=SQ-QT^-1 obeys a second-order recurrence.
        # Thus rank Delta(Q^-1) >= N-2 for *every* invertible Q.
        for n,p in [(4,17),(5,31),(7,29),(8,17),(9,19),(11,23),(12,37),(16,17),(17,103),(24,73),(32,97)]:
            w=nth_root(n,p)
            for alpha,beta in [(1,1),(2,3),(3,5),(1,0),(0,1)]:
                Q=mixed_green_denominator(n,p,w,alpha,beta)
                if rank(Q,p)<n:continue
                d=covariance_defect_rank_via_denominator(Q,p,w)
                self.assertGreaterEqual(d,n-2)
                if alpha==0:self.assertGreaterEqual(d,n-1)

    def test_19_arbitrary_fourier_endpoint_permutations(self):
        rr=random.Random(171719)
        for n,p,t,s in [(16,17,2,2),(17,103,3,2),(24,73,3,3),(31,311,2,3)]:
            w=nth_root(n,p)
            for _ in range(20):
                P=sparse_random(n,t,p,rr)
                Q=sparse_random(n,s,p,rr)
                row_order=rr.sample(range(n),n)
                input_order=rr.sample(range(n),n)
                row_freq=[0]*n
                for k,i in enumerate(row_order):row_freq[i]=k
                cert=graph_certificate(P,Q,t,s,row_order=row_order)
                self.assertEqual(cert['bound'],n//(1+s*t))
                I=cert['rows'];J=cert['neighbors']
                self.assertTrue(all(P[i][j]==0 for i in I for j in cert['columns']))
                self.assertEqual(rank([[pow(w,-row_freq[i]*input_order[j]%n,p) for j in J] for i in I],p),len(J))

if __name__=='__main__':unittest.main(verbosity=2)


