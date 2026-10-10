import unittest,random
from phase18 import (primitive_nth_root, MagneticTwirlPlan,WeightedSectorPlan,Count,
                     independent_twirl, independent_cyclic_green_solve, cyclic_window,
                     StridedGreenPlan, prime_factors, direct_dft)


def rank(A,p):
    if not A:return 0
    B=[[z%p for z in row] for row in A];h=len(B);w=len(B[0]);r=0
    for j in range(w):
        pivot=next((i for i in range(r,h) if B[i][j]),None)
        if pivot is None:continue
        B[r],B[pivot]=B[pivot],B[r]
        inv=pow(B[r][j],-1,p)
        for k in range(j,w):B[r][k]=B[r][k]*inv%p
        for i in range(r+1,h):
            v=B[i][j]
            if v:
                for k in range(j,w):B[i][k]=(B[i][k]-v*B[r][k])%p
        r+=1
        if r==h:break
    return r


def matrix_by_application(plan,n):
    cols=[]
    for j in range(n):
        e=[0]*n;e[j]=1;cols.append(plan.apply(e))
    return [[cols[j][i] for j in range(n)] for i in range(n)]


def independent_gaussian(A,b,p):
    n=len(b);C=[[u%p for u in row]+[b[i]%p] for i,row in enumerate(A)]
    for j in range(n):
        pivot=next((i for i in range(j,n) if C[i][j]),None)
        if pivot is None:raise ValueError('singular')
        C[j],C[pivot]=C[pivot],C[j]
        inv=pow(C[j][j],-1,p)
        for z in range(j,n+1):C[j][z]=C[j][z]*inv%p
        for i in range(n):
            if i==j:continue
            v=C[i][j]
            if v:
                for z in range(j,n+1):C[i][z]=(C[i][z]-v*C[j][z])%p
    return [C[i][-1] for i in range(n)]


def direct_branches(x,a,b,k,p,w,ell=0):
    n=len(x);q=pow(w,n//k,p);s=[0]*n;phase=1
    for j in range(k):
        Q=[[int(i==v) for v in range(n)] for i in range(n)]
        for t in range(n):
            Q[(t+1)%n][t]=(Q[(t+1)%n][t]-a)%p
            Q[t][t]=(Q[t][t]-b*phase*pow(q,t,p))%p
        z=independent_gaussian(Q,x,p)
        coeff=pow(phase,(-ell)%k,p)
        for i in range(n):s[i]=(s[i]+coeff*z[i])%p
        phase=phase*q%p
    return [v*pow(k,-1,p)%p for v in s]


def F(n,p,w):return [[pow(w,-i*j%n,p) for j in range(n)] for i in range(n)]


def commutator(A,B,p):
    n=len(A)
    X=[[sum(A[i][k]*B[k][j] for k in range(n))%p for j in range(n)] for i in range(n)]
    Y=[[sum(B[i][k]*A[k][j] for k in range(n))%p for j in range(n)] for i in range(n)]
    return [[(X[i][j]-Y[i][j])%p for j in range(n)] for i in range(n)]


class Phase18Tests(unittest.TestCase):
    def test_roots(self):
        for n,p in [(8,97),(12,97),(15,241),(24,97),(64,193)]:
            w=primitive_nth_root(n,p)
            self.assertEqual(pow(w,n,p),1)
            for q in prime_factors(n):self.assertNotEqual(pow(w,n//q,p),1)

    def test_window_against_direct(self):
        rng=random.Random(199)
        for n in [8,9,12,15,24,64]:
            p=193 if n==64 else (241 if n==15 else 97)
            for k in [1,2,n//2,n]:
                if k>n or n%k:continue
                for a in [0,1,2,5]:
                    x=[rng.randrange(p) for _ in range(n)];c=Count()
                    got=cyclic_window(x,a,k,p,c)
                    expected=[sum(pow(a,r,p)*x[(i-r)%n] for r in range(k))%p for i in range(n)]
                    self.assertEqual(got,expected)
                    self.assertLess(c.report()['total_field_ops'],10*n+20)

    def test_strided_solver_residual(self):
        p=193;n=64
        rng=random.Random(235)
        for k in [1,2,4,8,16,32,64]:
            d=3; ck=5
            try:plan=StridedGreenPlan(n,k,p,d,ck)
            except ZeroDivisionError:continue
            x=[rng.randrange(p) for _ in range(n)]; y=plan.apply(x)
            self.assertTrue(all((d*y[i]-ck*y[(i-k)%n]-x[i])%p==0 for i in range(n)))
        plan=StridedGreenPlan(n,16,p,0,2)
        x=[rng.randrange(p) for _ in range(n)];y=plan.apply(x)
        self.assertTrue(all((-2*y[(i-16)%n]-x[i])%p==0 for i in range(n)))

    def test_unweighted_dense_independent(self):
        rng=random.Random(17)
        for n,k,p in [(12,3,97),(12,4,97),(16,4,97),(24,6,97),(32,8,97),(64,8,193),(72,9,433)]:
            w=primitive_nth_root(n,p);q=pow(w,n//k,p)
            tests=0
            for a,b in [(2,3),(5,7),(7,11),(1,2),(3,5)]:
                try:
                    plan=MagneticTwirlPlan(n,k,p,a,b,w)
                    x=[rng.randrange(p) for _ in range(n)]
                    expected=independent_twirl(x,a,b,k,p,q)
                except (ZeroDivisionError,ValueError):continue
                self.assertEqual(plan.apply(x),expected)
                tests+=1
            self.assertGreater(tests,0)

    def test_gaussian_reference_small(self):
        rng=random.Random(71)
        for n,k,p in [(8,4,97),(12,3,97),(12,6,97),(15,5,241)]:
            w=primitive_nth_root(n,p)
            for a,b in [(2,3),(1,2),(2,1),(0,2)]:
                try:plan=MagneticTwirlPlan(n,k,p,a,b,w)
                except (ZeroDivisionError,ValueError):continue
                x=[rng.randrange(p) for _ in range(n)]
                self.assertEqual(plan.apply(x),direct_branches(x,a,b,k,p,w))

    def test_zero_diagonal_cases(self):
        for n,k,p in [(12,3,97),(12,4,97),(16,4,97)]:
            w=primitive_nth_root(n,p);x=[(i*7+3)%p for i in range(n)]
            plan=MagneticTwirlPlan(n,k,p,2,1,w)
            self.assertEqual(plan.apply(x),direct_branches(x,2,1,k,p,w))

    def test_noncommutation(self):
        n=8;p=97;w=primitive_nth_root(n,p);k=4;q=pow(w,n//k,p)
        S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
        U=[[int(i==j)*pow(q,j,p) for j in range(n)] for i in range(n)]
        Qs=[]
        for j in [0,1]:
            Q=[[((int(i==h)-3*S[i][h]-5*pow(q,j,p)*U[i][h])%p) for h in range(n)] for i in range(n)]
            Qs.append(Q)
        self.assertGreater(rank(commutator(*Qs,p),p),0)

    def test_weighted_sector_independent(self):
        rng=random.Random(51)
        for n,k,p in [(12,3,97),(16,4,97),(24,6,97),(64,8,193),(72,9,433)]:
            w=primitive_nth_root(n,p);q=pow(w,n//k,p)
            for a,b in [(2,3),(5,7)]:
                try:plan=MagneticTwirlPlan(n,k,p,a,b,w)
                except (ZeroDivisionError,ValueError):continue
                x=[rng.randrange(p) for _ in range(n)]
                for ell in range(min(k,5)):
                    weighted=WeightedSectorPlan(plan,ell)
                    expected=independent_twirl(x,a,b,k,p,q,ell)
                    self.assertEqual(weighted.apply(x),expected,(n,k,a,b,ell))

    def test_weighted_sector_gaussian(self):
        n,k,p=12,4,97;w=primitive_nth_root(n,p)
        x=[(i*i+2*i+1)%p for i in range(n)]
        plan=MagneticTwirlPlan(n,k,p,2,1,w)
        for ell in range(k):
            self.assertEqual(WeightedSectorPlan(plan,ell).apply(x),direct_branches(x,2,1,k,p,w,ell))

    def test_sector_covariance(self):
        n,k,p=24,6,97;w=primitive_nth_root(n,p)
        plan=MagneticTwirlPlan(n,k,p,2,3,w);rng=random.Random(65)
        for ell in range(k):
            sp=WeightedSectorPlan(plan,ell);x=[rng.randrange(p) for _ in range(n)]
            sx=[x[(i-1)%n] for i in range(n)]
            a=sp.apply(sx);b=sp.apply(x)
            self.assertEqual(a,[pow(plan.q,ell,p)*b[(i-1)%n]%p for i in range(n)])

    def test_rank_classification(self):
        cases=[(8,4,97),(12,3,97),(12,4,97),(16,4,97),(24,6,97),(32,8,97)]
        for n,k,p in cases:
            w=primitive_nth_root(n,p)
            for alpha in [1,2,3,5,7]:
                beta=2
                try:plan=MagneticTwirlPlan(n,k,p,alpha,beta,w)
                except ZeroDivisionError:continue
                M=matrix_by_application(plan,n)
                actual=rank(M,p)
                expected=n-k+1 if pow(alpha,n,p)==1 else n
                self.assertEqual(actual,expected,(n,k,alpha,beta))

    def test_F_commutator_rank(self):
        for n,p in [(5,241),(8,97),(9,73),(12,97),(15,241),(16,97)]:
            w=primitive_nth_root(n,p);A=F(n,p,w)
            S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
            self.assertEqual(rank(commutator(A,S,p),p),n if n%2==0 else n-1)

    def test_DFT_is_not_twirl(self):
        n=16;p=97;w=primitive_nth_root(n,p)
        plan=MagneticTwirlPlan(n,4,p,2,3,w)
        A=matrix_by_application(plan,n)
        E=[[ (a-b)%p for a,b in zip(ra,rb)] for ra,rb in zip(F(n,p,w),A)]
        self.assertGreaterEqual(rank(E,p),n//2)
        self.assertNotEqual(A,F(n,p,w))

    def test_general_subgroup_commutator_rank(self):
        # Exact covariance defect rank for all cyclic subgroup strides K|N.
        for n,p in [(8,97),(12,97),(15,241),(16,97),(24,97),(32,97)]:
            w=primitive_nth_root(n,p)
            A=F(n,p,w)
            for k in (z for z in range(1,n+1) if n%z==0):
                SK=[[int(i==(j+k)%n) for j in range(n)] for i in range(n)]
                measured=rank(commutator(A,SK,p),p)
                predicted=n-k if (n-k)%2==0 else n
                self.assertEqual(measured,predicted,(n,k))

    def test_all_weighted_sectors_commute_stride(self):
        n,k,p=24,6,97;w=primitive_nth_root(n,p)
        plan=MagneticTwirlPlan(n,k,p,2,3,w)
        x=[(i*i+4*i+7)%p for i in range(n)]
        sk=[x[(i-k)%n] for i in range(n)]
        for ell in range(k):
            sector=WeightedSectorPlan(plan,ell)
            original=sector.apply(x)
            self.assertEqual(sector.apply(sk),
                             [original[(i-k)%n] for i in range(n)])

    def test_sector_sum_correction_rank_bound(self):
        rng=random.Random(437)
        for n,k,p in [(8,4,97),(12,3,97),(12,4,97),(16,4,97)]:
            w=primitive_nth_root(n,p)
            plan=MagneticTwirlPlan(n,k,p,2,3,w)
            sectors=[matrix_by_application(WeightedSectorPlan(plan,j),n) for j in range(k)]
            coeff=[rng.randrange(p) for _ in range(k)]
            A=[[sum(coeff[j]*sectors[j][i][h] for j in range(k))%p
                for h in range(n)] for i in range(n)]
            SK=[[int(i==(j+k)%n) for j in range(n)] for i in range(n)]
            self.assertEqual(rank(commutator(A,SK,p),p),0)
            full=F(n,p,w)
            diff=[[(full[i][h]-A[i][h])%p for h in range(n)] for i in range(n)]
            target=n-k if (n-k)%2==0 else n
            self.assertGreaterEqual(rank(diff,p),(target+1)//2)

    def test_full_resolvent_invertibility_criterion(self):
        # For every j the denominator is nonsingular exactly when
        # (1-beta^K)^(N/K) != alpha^N.
        for n,k,p in [(8,4,97),(12,3,97),(12,4,97)]:
            w=primitive_nth_root(n,p);q=pow(w,n//k,p)
            for alpha in range(7):
                for beta in range(7):
                    predicted=(pow((1-pow(beta,k,p))%p,n//k,p)!=pow(alpha,n,p))
                    try:
                        MagneticTwirlPlan(n,k,p,alpha,beta,w)
                        got=True
                    except (ZeroDivisionError,ValueError):got=False
                    self.assertEqual(got,predicted,(n,k,alpha,beta))

    def test_all_prime_weyl_coefficients(self):
        from weyl_line_gate import (fourier_matrix,weyl_support,
                  exact_fourier_gauss_coeff,trace_weyl_coefficient)
        for n,p in [(3,7),(5,241),(7,29),(11,23)]:
            w=primitive_nth_root(n,p);FM=fourier_matrix(n,p,w)
            self.assertEqual(len(weyl_support(FM,p,w)),n*n)
            for a in range(n):
                for b in range(n):
                    self.assertEqual(trace_weyl_coefficient(FM,a,b,p,w),
                       exact_fourier_gauss_coeff(a,b,n,p,w))

    def test_projective_and_affine_line_support(self):
        from weyl_line_gate import lines_through_origin,affine_lines
        for n in [3,5,7]:
            ls=lines_through_origin(n)
            self.assertEqual(len(ls),n+1)
            self.assertEqual(len(set().union(*ls)),n*n)
            for i in range(len(ls)):
                for j in range(i+1,len(ls)):
                    self.assertEqual(len(ls[i]&ls[j]),1)
            af=affine_lines(n)
            self.assertEqual(len(af),n*(n+1))
            self.assertTrue(all(len(z)==n for z in af))

    def test_weighted_sector_weyl_affine_line(self):
        from weyl_line_gate import weyl_support
        n,k,p=12,3,97
        w=primitive_nth_root(n,p)
        plan=MagneticTwirlPlan(n,k,p,2,3,w)
        for ell in range(k):
            sector=WeightedSectorPlan(plan,ell)
            supp=weyl_support(matrix_by_application(sector,n),p,w)
            self.assertTrue(supp)
            self.assertTrue(all(b==ell*(n//k) for a,b in supp))

    def test_rotated_one_direction_line(self):
        from weyl_line_gate import weyl_support
        n,p=5,241;w=primitive_nth_root(n,p)
        a,b=2,3
        W=[[int(i==(j+a)%n)*pow(w,b*j%n,p) for j in range(n)] for i in range(n)]
        def mul(A,B):
            return [[sum(A[i][z]*B[z][j] for z in range(n))%p
                    for j in range(n)] for i in range(n)]
        base=[[int(i==j) for j in range(n)] for i in range(n)];A=[[0]*n for _ in range(n)]
        for t in range(n):
            for i in range(n):
                for j in range(n):A[i][j]=(A[i][j]+(t+2)*base[i][j])%p
            base=mul(base,W)
        supp=weyl_support(A,p,w)
        self.assertTrue(supp)
        self.assertTrue(all((a*yb-b*xa)%n==0 for xa,yb in supp))
        # Two Weyl endpoint monomials shift the line into an affine coset.
        L=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)]
        R=[[int(i==j)*pow(w,4*j%n,p) for j in range(n)] for i in range(n)]
        gauged=mul(mul(L,A),R)
        supp2=weyl_support(gauged,p,w)
        self.assertEqual(len(supp),len(supp2))
        self.assertTrue(all((a*(yb-4)-b*(xa-1))%n==0 for xa,yb in supp2))

    def test_full_weyl_support_O_N_nonDFT_control(self):
        # Counterexample to extrapolating one-direction support bounds
        # to products: two linear-work Green stages can already have
        # all N^2 Weyl coefficients nonzero.
        from weyl_line_gate import weyl_support
        n,p=5,241;w=primitive_nth_root(n,p);a,b=2,3
        shift=StridedGreenPlan(n,1,p,1,a)
        diag=[pow((1-b*pow(w,i,p))%p,-1,p) for i in range(n)]
        class Prod:
            def apply(self,x):
                y=[diag[i]*x[i]%p for i in range(n)]
                return shift.apply(y)
        M=matrix_by_application(Prod(),n)
        self.assertEqual(len(weyl_support(M,p,w)),n*n)
        self.assertNotEqual(M,F(n,p,w))

    def test_preparation_linear_charged(self):
        for n,k,p in [(64,8,193),(256,16,257),(1024,32,12289),(4096,64,12289)]:
            w=primitive_nth_root(n,p)
            try:plan=MagneticTwirlPlan(n,k,p,2,3,w)
            except ZeroDivisionError:continue
            prep=plan.counter.report()['total_field_ops']
            x=[(i*77+13)%p for i in range(n)];c=Count()
            out=plan.apply(x,c)
            self.assertEqual(len(out),n)
            self.assertLessEqual(prep+c.report()['total_field_ops'],15*n+150)

    def test_reject_singular_D(self):
        p=97;n=12;k=3;w=primitive_nth_root(n,p)
        with self.assertRaises(ZeroDivisionError):
            MagneticTwirlPlan(n,k,p,1,0,w)

    def test_endpoints_K1_and_KN(self):
        n=12;p=97;w=primitive_nth_root(n,p)
        for k in (1,n):
            for a,b in [(2,3),(2,1)]:
                try:plan=MagneticTwirlPlan(n,k,p,a,b,w)
                except (ValueError,ZeroDivisionError):continue
                x=[(i+5)**2%p for i in range(n)]
                self.assertEqual(plan.apply(x),direct_branches(x,a,b,k,p,w))


if __name__=='__main__':unittest.main()
