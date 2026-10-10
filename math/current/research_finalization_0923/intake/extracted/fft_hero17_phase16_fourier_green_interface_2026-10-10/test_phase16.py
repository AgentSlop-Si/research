import random
import unittest
from phase16 import (nth_root, fourier, identity, mm, mv, rank_mod, solve,
                     nullspace, cyclic_distance, column_band_valid,
                     boundary_pair, intertwining_check, harper,
                     harper_algebra_audit, harper_rational_witness,
                     evaluated_poly, boundary_circulant_gauge, shift, modulation, chirp)

PRIMES={3:7,4:5,5:11,6:7,7:29,8:17,9:19,10:11,11:23,
        12:13,13:53,15:31,16:17,17:103,45:181}

class Phase16Tests(unittest.TestCase):
    def test_01_root_orders(self):
        for n,p in PRIMES.items():
            w=nth_root(n,p)
            self.assertEqual(pow(w,n,p),1)
            self.assertEqual(len({pow(w,j,p) for j in range(n)}),n)

    def test_02_fourier_covariance_sufficiency(self):
        for n in (3,4,5,8,9,13,16):
            p=PRIMES[n];w=nth_root(n,p);F=fourier(n,p,w)
            self.assertTrue(intertwining_check(F,p,w))
            M=[row.copy() for row in F]
            M[1][1]=(M[1][1]+1)%p
            self.assertFalse(intertwining_check(M,p,w))

    def test_03_fourier_pair_boundary_all(self):
        for n in (3,5,7,9,11,13,15,17):
            p=PRIMES[n]
            for a in sorted(set((0,(n-1)//4,(n-1)//2))):
                b=(n-1)//2-a
                P,Q=boundary_pair(n,a,p)
                self.assertTrue(column_band_valid(P,a),(n,a,p,'P'))
                self.assertTrue(column_band_valid(Q,b),(n,b,p,'Q'))
                self.assertEqual(rank_mod(Q,p),n,(n,a,b,p))
                self.assertEqual(mm(fourier(n,p),Q,p),P)

    def test_04_direct_basis_vectors(self):
        for n in (5,9,13,17):
            p=PRIMES[n]; a=(n-1)//4;P,Q=boundary_pair(n,a,p)
            for j in range(n):
                e=[int(i==j) for i in range(n)]
                y=mv(P,solve(Q,e,p),p)
                self.assertEqual(y,mv(fourier(n,p),e,p))

    def test_05_random_fresh_vectors(self):
        rng=random.Random(16010)
        for n in (5,7,9,11,13,17):
            p=PRIMES[n];a=(n-1)//4;P,Q=boundary_pair(n,a,p);F=fourier(n,p)
            for _ in range(4):
                v=[rng.randrange(p) for _ in range(n)]
                self.assertEqual(mv(P,solve(Q,v,p),p),mv(F,v,p))

    def test_06_quadratic_diagonal_gauges(self):
        rng=random.Random(16011)
        for n in (5,9,13,17):
            p=PRIMES[n];a=(n-1)//4;w=nth_root(n,p)
            P,Q=boundary_pair(n,a,p);F=fourier(n,p,w)
            L=[pow(w,(3*i*i+2*i)%n,p) for i in range(n)]
            R=[pow(w,(7*i*i+i)%n,p) for i in range(n)]
            for _ in range(3):
                v=[rng.randrange(p) for _ in range(n)]
                got=[L[i]*z%p for i,z in enumerate(mv(P,solve(Q,[R[i]*v[i]%p for i in range(n)],p),p))]
                ref=[L[i]*z%p for i,z in enumerate(mv(F,[R[i]*v[i]%p for i in range(n)],p))]
                self.assertEqual(got,ref)

    def test_07_boundary_root_zeros_exact(self):
        for n in (5,7,9,11,13,15,17):
            p=PRIMES[n];a=(n-1)//4;b=(n-1)//2-a
            P,Q=boundary_pair(n,a,p)
            self.assertEqual(sum(x!=0 for x in P[0]),2*a+1)
            for j in range(n):
                self.assertEqual(sum(P[k][j]==0 for k in range(n)),2*b)
                self.assertEqual(sum(Q[k][j]!=0 for k in range(n)),2*b+1)

    def test_08_boundary_nullity_one(self):
        for n in (5,9,13,17):
            p=PRIMES[n];w=nth_root(n,p);a=(n-1)//4;b=(n-1)//2-a
            for j in range(n):
                allowed={(j+t)%n for t in range(-a,a+1)}
                forbidden=[k for k in range(n) if k not in allowed]
                A=[[pow(w,-k*(j-b+r)%n,p) for r in range(2*b+1)] for k in forbidden]
                self.assertEqual(len(nullspace(A,p)),1)

    def test_09_circulant_chirp_gauge(self):
        for n in (5,7,9,11,13,15,17):
            p=PRIMES[n];a=(n-1)//4
            P,Q=boundary_pair(n,a,p)
            predicted,h,DL,DR=boundary_circulant_gauge(n,a,p,Q)
            self.assertEqual(predicted,Q)
            self.assertEqual(len(h),n)
            self.assertTrue(all(x!=0 for x in DL+DR))

    def test_10_field_sensitive_rank_exception(self):
        n=45;a=11
        P,Q=boundary_pair(n,a,181)
        self.assertEqual(rank_mod(Q,181),43)
        self.assertTrue(column_band_valid(P,a))
        self.assertTrue(column_band_valid(Q,11))
        P2,Q2=boundary_pair(n,a,271)
        self.assertEqual(rank_mod(Q2,271),n)

    def test_11_harper_commutes_fourier(self):
        for n in (3,4,5,6,7,8,9,10,11,12,13,15,16):
            p=PRIMES[n];F=fourier(n,p);H=harper(n,p)
            self.assertEqual(mm(F,H,p),mm(H,F,p))

    def test_12_harper_algebra_odd(self):
        for n in (3,5,7,9,11,13,15):
            dim,aug=harper_algebra_audit(n,PRIMES[n])
            self.assertEqual(dim,n)
            self.assertEqual(aug,n)

    def test_13_harper_nonpolynomial_multiple_four(self):
        for n in (4,8,12,16):
            dim,aug=harper_algebra_audit(n,PRIMES[n])
            self.assertEqual(dim,n-1)
            self.assertEqual(aug,n)

    def test_14_harper_two_mod_four(self):
        for n in (6,10):
            dim,aug=harper_algebra_audit(n,PRIMES[n])
            self.assertEqual(dim,n)
            self.assertEqual(aug,n)

    def test_15_harper_rational_witness_odd(self):
        for n in (3,5,7,9,11,13,15):
            p=PRIMES[n];d,a,b=harper_rational_witness(n,p,(n-1)//2)
            self.assertEqual(d,(n-1)//2)
            H=harper(n,p);P=evaluated_poly(a,H,p);Q=evaluated_poly(b,H,p)
            self.assertEqual(rank_mod(Q,p),n)
            self.assertEqual(mm(fourier(n,p),Q,p),P)

    def test_16_harper_no_shallower_relation_samples(self):
        for n in (5,7,9,11):
            self.assertIsNone(harper_rational_witness(n,PRIMES[n],(n-3)//2))

    def test_17_exact_kernels(self):
        for n in (3,5,9,13):
            p=PRIMES[n];a=(n-1)//4;P,Q=boundary_pair(n,a,p)
            self.assertEqual(rank_mod(P,p),n)
            self.assertEqual(rank_mod(Q,p),n)
            # Both banded factors are invertible; neither can be treated as a free change of basis.

    def test_18_clifford_chirp_conjugation(self):
        for n in (5,7,8,9,11,16):
            p=PRIMES[n];w=nth_root(n,p)
            for a,s in ((1,1),(2,3),(3,n//2)):
                D=chirp(n,a,p,w)
                Di=chirp(n,-a,p,w)
                actual=mm(mm(D,shift(n,s),p),Di,p)
                predicted=mm(shift(n,s),modulation(n,2*a*s,p,w),p)
                k=pow(w,a*s*s%n,p)
                self.assertEqual(actual,[[k*x%p for x in row] for row in predicted])

    def test_19_integer_lower_bound(self):
        for n in range(3,102):
            for a in range((n-1)//2+1):
                for b in range((n-1)//2+1):
                    if 2*(a+b)+1<n:
                        self.assertLess(2*(a+b)+1,n)

if __name__=='__main__':unittest.main()
