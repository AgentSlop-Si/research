import unittest,random
from itertools import combinations
from phase14 import (MagneticGreen,Counts,primitive_root,prime_factors,
    direct_matrix,inverse_dense,q_polynomial_operator,weyl_coeff,triangular_support,
    rank_mod,centered_block_rank,fourier,twirl_matrix,twirl_closed_matrix,reference_row,fused_weyl_twirl,both_cut_ranks,matmul,StridedMagneticGreen)

CASES=[(3,307),(4,97),(5,521),(6,97),(7,701),(8,97),(9,919),(10,101),
       (11,1123),(12,97),(15,1531),(16,97)]
SIGNS=[(1,1),(1,-1),(-1,1),(-1,-1)]

class Phase14Tests(unittest.TestCase):
    def test_root_orders(self):
        for n,p in CASES:
            w=primitive_root(n,p)
            self.assertEqual(pow(w,n,p),1)
            self.assertTrue(all(pow(w,n//q,p)!=1 for q in prime_factors(n)))

    def test_qbinomial_matrix_power(self):
        for n,p in CASES[:8]:
            w=primitive_root(n,p)
            for ep,de in SIGNS:
                a,b=2,3
                if (1-pow(a,n,p)-pow(b,n,p))%p==0:continue
                H,Wn=q_polynomial_operator(n,p,w,a,b,ep,de)
                expected=(pow(a,n,p)+pow(b,n,p))%p
                self.assertEqual(Wn,[[expected if i==j else 0 for j in range(n)]for i in range(n)])
                self.assertEqual(H,inverse_dense(direct_matrix(n,p,w,a,b,ep,de),p))

    def test_recurrence_all_basis_vectors(self):
        for n,p in CASES:
            w=primitive_root(n,p)
            for ep,de in SIGNS:
                for a,b in ((2,3),(5,1),(2,0),(0,3)):
                    if (1-pow(a,n,p)-pow(b,n,p))%p==0:continue
                    op=MagneticGreen(n,p,w,a,b,ep,de)
                    oracle=inverse_dense(direct_matrix(n,p,w,a,b,ep,de),p)
                    for j in range(n):
                        x=[int(k==j)for k in range(n)]
                        self.assertEqual(op.apply(x),[row[j]for row in oracle])

    def test_random_fresh_vectors(self):
        rng=random.Random(1714)
        for n,p in CASES:
            w=primitive_root(n,p)
            for ep,de in SIGNS:
                for _ in range(5):
                    a=rng.randrange(1,p);b=rng.randrange(1,p)
                    if (1-pow(a,n,p)-pow(b,n,p))%p==0:continue
                    x=[rng.randrange(p)for _ in range(n)]
                    op=MagneticGreen(n,p,w,a,b,ep,de)
                    ans=op.apply(x)
                    A=direct_matrix(n,p,w,a,b,ep,de)
                    self.assertEqual([sum(A[i][j]*ans[j]for j in range(n))%p for i in range(n)],x)

    def test_zero_pivot(self):
        for n,p in CASES:
            w=primitive_root(n,p)
            for ep,de in SIGNS:
                op=MagneticGreen(n,p,w,2,1,ep,de)
                self.assertEqual(op.d[0],0)
                x=[(i*i+7*i+3)%p for i in range(n)]
                ans=op.apply(x)
                A=direct_matrix(n,p,w,2,1,ep,de)
                self.assertEqual([sum(A[i][j]*ans[j]for j in range(n))%p for i in range(n)],x)

    def test_discriminant_singularity(self):
        for n,p in CASES:
            w=primitive_root(n,p)
            with self.assertRaises(ValueError):
                MagneticGreen(n,p,w,0,1)
            with self.assertRaises(ValueError):
                MagneticGreen(n,p,w,1,0)

    def test_small_direct_rows(self):
        for n,p in CASES:
            w=primitive_root(n,p)
            x=[(i*17+3)%p for i in range(n)]
            for ep,de in SIGNS:
                G=MagneticGreen(n,p,w,2,1,ep,de)
                y=G.apply(x)
                self.assertEqual(y,[reference_row(i,x,2,1,ep,de,w,p) for i in range(n)])

    def test_quasiseparable_block_rank(self):
        for n,p in CASES:
            w=primitive_root(n,p)
            for ep,de in SIGNS:
                for a,b in ((2,3),(2,1),(0,3)):
                    if not (1-pow(a,n,p)-pow(b,n,p))%p:continue
                    H=inverse_dense(direct_matrix(n,p,w,a,b,ep,de),p)
                    self.assertLessEqual(centered_block_rank(H,p),1)

    def test_random_branch_sums(self):
        rng=random.Random(602)
        for n,p in CASES:
            w=primitive_root(n,p)
            m=n//2
            F=fourier(n,w,p)
            self.assertEqual(centered_block_rank(F,p),m)
            for B in range(1,m):
                A=[[0]*n for _ in range(n)]
                for z in range(B):
                    ep,de=SIGNS[rng.randrange(4)]
                    a=rng.randrange(1,p);b=rng.randrange(1,p)
                    if (1-pow(a,n,p)-pow(b,n,p))%p==0:continue
                    H=inverse_dense(direct_matrix(n,p,w,a,b,ep,de),p)
                    v=rng.randrange(1,p)
                    for i in range(n):
                        for j in range(n):A[i][j]=(A[i][j]+v*H[i][j])%p
                self.assertLessEqual(centered_block_rank(A,p),B)
                self.assertNotEqual(A,F)

    def test_triangular_support_exact(self):
        for n,p in CASES:
            w=primitive_root(n,p)
            for ep,de in SIGNS:
                a,b=2,3
                if (1-pow(a,n,p)-pow(b,n,p))%p==0:continue
                H=inverse_dense(direct_matrix(n,p,w,a,b,ep,de),p)
                C=weyl_coeff(H,w,p)
                support=triangular_support(n,ep,de)
                self.assertEqual({(i,j)for i in range(n)for j in range(n)if C[i][j]},support)

    def test_odd_four_orientation_cover(self):
        for n,p in CASES:
            if n%2==0:continue
            S=[triangular_support(n,*pair)for pair in SIGNS]
            self.assertEqual(len(set.union(*S)),n*n)
            misses=[(1,1),(1,n-1),(n-1,1),(n-1,n-1)]
            for k in range(4):
                U=set.union(*[s for i,s in enumerate(S)if i!=k])
                self.assertNotEqual(len(U),n*n)
                self.assertTrue(len(set((i,j)for i in range(n)for j in range(n)if (i,j)not in U))>=1)
            F=weyl_coeff(fourier(n,primitive_root(n,p),p),primitive_root(n,p),p)
            self.assertTrue(all(c!=0 for row in F for c in row))

    def test_even_defect_mode(self):
        for n,p in CASES:
            if n%4:continue
            w=primitive_root(n,p)
            S=set.union(*[triangular_support(n,*z)for z in SIGNS])
            self.assertEqual({(a,b)for a in range(n)for b in range(n)}-S,{(n//2,n//2)})
            F=weyl_coeff(fourier(n,w,p),w,p)
            self.assertNotEqual(F[n//2][n//2],0)

    def test_n_equal_two_mod_four_membership(self):
        for n,p in ((6,97),(10,101)):
            w=primitive_root(n,p)
            F=weyl_coeff(fourier(n,w,p),w,p)
            self.assertEqual(F[n//2][n//2],0)
            # All other Weyl slots are spanned by the four signed triangles.
            covered=set.union(*[triangular_support(n,*sgn) for sgn in SIGNS])
            self.assertEqual(set((i,j) for i in range(n)for j in range(n))-covered,
                             {(n//2,n//2)})

    def test_two_twirl_closures(self):
        for n,p in CASES[:8]:
            w=primitive_root(n,p)
            for a,b in ((2,3),(2,1),(0,3)):
                if (1-pow(a,n,p)-pow(b,n,p))%p==0:continue
                G=inverse_dense(direct_matrix(n,p,w,a,b),p)
                for orientation in ('T','S'):
                    self.assertEqual(twirl_matrix(G,n,w,p,orientation),twirl_closed_matrix(n,a,b,w,p,orientation))

    def test_long_range_shift_escapes_cut_gate(self):
        for n,p in ((4,97),(8,97),(12,97),(16,97)):
            w=primitive_root(n,p)
            stride=n//2
            op=StridedMagneticGreen(n,p,w,2,0,stride)
            x=[(j**2+3*j+17)%p for j in range(n)]
            c=Counts();ans=op.apply(x,c)
            self.assertEqual([ (ans[i]-2*ans[(i-stride)%n])%p for i in range(n)],x)
            self.assertLessEqual(c.field_ops,7*n)
            # Its full cross-cut rank is n/2 despite linear work.
            m=n//2
            A=[[0]*n for _ in range(n)]
            for i in range(n):
                A[i][i]=1;A[i][(i-stride)%n]=(A[i][(i-stride)%n]-2)%p
            H=inverse_dense(A,p)
            self.assertEqual(both_cut_ranks(H,p),(m,m))

    def test_general_stride_multicycle_independent(self):
        for n,p in ((6,97),(8,97),(9,919),(10,101),(12,97),(16,97)):
            w=primitive_root(n,p)
            for stride in (0,1,2,n//2,n-1):
                for delta in (-1,1):
                    alpha,beta=2,3
                    try:
                        op=StridedMagneticGreen(n,p,w,alpha,beta,stride,delta)
                    except ValueError:continue
                    A=[[0]*n for _ in range(n)]
                    for i in range(n):
                        A[i][i]=(1-beta*pow(w,delta*i%n,p))%p
                        A[i][(i-stride)%n]=(A[i][(i-stride)%n]-alpha)%p
                    H=inverse_dense(A,p)
                    rng=random.Random(n*100+stride*7+delta)
                    x=[rng.randrange(p)for _ in range(n)]
                    ref=[sum(H[i][j]*x[j] for j in range(n))%p for i in range(n)]
                    self.assertEqual(op.apply(x),ref)

    def test_four_sign_linear_span_dimension(self):
        for n,p in ((3,307),(4,97),(5,521),(6,97),(7,701),(8,97),(9,919),(10,101)):
            w=primitive_root(n,p);rows=[]
            for ep,de in SIGNS:
                for a in range(n+2):
                    for b in range(n+2):
                        if (1-pow(a,n,p)-pow(b,n,p))%p==0:continue
                        G=inverse_dense(direct_matrix(n,p,w,a,b,ep,de),p)
                        C=weyl_coeff(G,w,p)
                        rows.append([v for row in C for v in row])
            self.assertEqual(rank_mod(rows,p),n*n-int(n%2==0))

    def test_deep_branching_cut_rank_budget(self):
        rng=random.Random(44214)
        for n,p in ((5,521),(8,97),(9,919),(12,97),(16,97)):
            w=primitive_root(n,p)
            for total_branches in (1,2,3):
                sumA=[[0]*n for _ in range(n)]
                depth_total=0
                for branch in range(total_branches):
                    depth=rng.randrange(1,5)
                    depth_total+=depth
                    operator=[[int(i==j)for j in range(n)]for i in range(n)]
                    for _ in range(depth):
                        eps,de=SIGNS[rng.randrange(4)]
                        a=rng.randrange(1,p);b=rng.randrange(1,p)
                        if (1-pow(a,n,p)-pow(b,n,p))%p==0:b=0
                        G=inverse_dense(direct_matrix(n,p,w,a,b,eps,de),p)
                        operator=matmul(G,operator,p)
                        # An arbitrary diagonal gauge (cross-cut rank zero).
                        diag=[rng.randrange(1,p) for _ in range(n)]
                        operator=[[v*diag[i]%p for v in row]for i,row in enumerate(operator)]
                    factor=rng.randrange(1,p)
                    for i in range(n):
                        for j in range(n):sumA[i][j]=(sumA[i][j]+factor*operator[i][j])%p
                self.assertLessEqual(max(both_cut_ranks(sumA,p)),depth_total)

    def test_fused_weyl_twirl_both_axes(self):
        for n,p in CASES:
            w=primitive_root(n,p)
            x=[(j*j+17*j+9)%p for j in range(n)]
            for a,b in ((2,3),(2,1),(1,2),(0,3)):
                if (1-pow(a,n,p)-pow(b,n,p))%p==0:continue
                G=inverse_dense(direct_matrix(n,p,w,a,b),p)
                for axis in ('S','T'):
                    ref=twirl_matrix(G,n,w,p,axis)
                    expected=[sum(row[j]*x[j]for j in range(n))%p for row in ref]
                    ans,c=fused_weyl_twirl(x,p,w,a,b,axis)
                    self.assertEqual(ans,expected)
                    self.assertLess(c.field_ops,15*n+200)

    def test_dense_infinite_span_dimension(self):
        for n in (3,5,7,9):
            S=[triangular_support(n,*z)for z in SIGNS]
            self.assertEqual(len(S[0]),n*(n+1)//2)
            for missing in range(4):
                u=set.union(*[s for i,s in enumerate(S)if i!=missing])
                self.assertTrue(len(u)<n*n)

    def test_linear_accounting(self):
        for n,p in ((64,193),(1024,12289)):
            w=primitive_root(n,p)
            op=MagneticGreen(n,p,w,2,3)
            x=[(i**2+31*i+3)%p for i in range(n)]
            c=Counts();y=op.apply(x,c)
            self.assertEqual(len(y),n)
            self.assertLess(op.prep.field_ops,10*n+100)
            self.assertLess(c.field_ops,7*n+10)
            self.assertEqual(c.write,n)

    def test_not_fourier(self):
        for n,p in ((5,521),(16,97)):
            w=primitive_root(n,p);x=[i+1 for i in range(n)]
            G=MagneticGreen(n,p,w,2,3)
            y=G.apply(x)
            F=fourier(n,w,p)
            z=[sum(F[i][j]*x[j]for j in range(n))%p for i in range(n)]
            self.assertNotEqual(y,z)


if __name__=='__main__':unittest.main()
