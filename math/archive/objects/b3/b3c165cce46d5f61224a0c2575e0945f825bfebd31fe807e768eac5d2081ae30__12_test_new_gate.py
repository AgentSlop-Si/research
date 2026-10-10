"""Independent regression checks for the October 9 spectral determinant gate."""
import unittest
import random
import numpy as np
from column_minor import validate,build_polynomial
from exact_minor import make_exact
from upper_minor import verify as verify_upper
from exact_upper import build as build_upper
from independence import witness
from five_parameter_gate import split,compute_h
from adjacent_tail import equations
from two_defect_tail import verify as verify_two_defect
from dual_support import primitive_root
from inverse_quartic import poly_eval


def rank_rect(A,p):
    A=[[int(v)%p for v in row] for row in A]
    m=len(A);n=len(A[0]);r=0
    for j in range(n):
        pivot=next((i for i in range(r,m) if A[i][j]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        inv=pow(A[r][j],-1,p)
        A[r]=[inv*x%p for x in A[r]]
        for i in range(r+1,m):
            mul=A[i][j]
            if mul:A[i]=[(A[i][k]-mul*A[r][k])%p for k in range(n)]
        r+=1
        if r==m:break
    return r

class SpectralGateTests(unittest.TestCase):
    def test_exact_quartic_45terms(self):
        Q,A,B,C=make_exact()
        self.assertEqual((len(Q),len(A),len(B),len(C)),(45,12,21,12))
        self.assertEqual(max(map(len,Q)),4)
        self.assertFalse(any(0 in mon and 5 in mon for mon in Q))

    def test_modular_quartic_independently(self):
        for p in (12289,65537):
            z=primitive_root(p,8)
            for w in (z,pow(z,3,p)):
                d=validate(p,w,6)
                self.assertEqual(d['term_count'],45)
                self.assertEqual(d['degree'],4)
                self.assertGreaterEqual(d['verified'],5)

    def test_exact_upper_resultants(self):
        D,R=build_upper()
        self.assertEqual([len(R[k]) for k in (1,2,5)],[192,300,330])
        self.assertTrue(all(max(map(len,R[k]))==7 for k in R))
        self.assertTrue(all(not(6 in m and 7 in m) for row in R.values() for m in row))

    def test_modular_upper_residuals(self):
        for p in (12289,65537):
            z=primitive_root(p,8)
            v=verify_upper(p,z,5)
            self.assertTrue(all(row['nonzero'] for row in v['elimination']))

    def test_jacobian_independence_witness(self):
        v=witness()
        self.assertEqual(v['nonzero_minor'],10570)
        self.assertEqual(v['selected_columns'],[0,1,2,3])

    def test_five_parameter_nonzero_polynomial(self):
        A,B,C,co=split()
        p=12289;z=primitive_root(p,8)
        x=[10931,3273,7557,2279,5478]
        H,bb,m,_=compute_h(x,p,z,(A,B,C,co))
        self.assertEqual((bb,m,H),(12110,11930,4730))
        self.assertNotEqual(H,0)
        self.assertTrue(all(len(row)==3 and all(len(e)==3 for e in row) for row in co))

    def test_cubic_31terms(self):
        eq,W,*_=equations()
        self.assertEqual(len(W),31)
        self.assertEqual(max(map(len,W)),3)
        self.assertEqual([len(eq[0]),len(eq[1])],[7,7])
        p=12289;z=primitive_root(p,8)
        self.assertEqual(poly_eval(W,[0,2,3,5,7,0],p,z),9966)

    def test_tail_rank_vandermonde_equivalence(self):
        rng=random.Random(10350)
        for p in (12289,65537):
            z=primitive_root(p,8)
            s1=(z+pow(z,2,p)+pow(z,3,p))%p
            s2=(pow(z,3,p)+pow(z,4,p)+pow(z,5,p))%p
            s3=pow(z,6,p)
            def matrix(tail):
                return [[pow(z,i*k,p) for k in range(3)]+[sum(pow(z,i*k,p)*tail[k-3] for k in range(3,8))%p] for i in range(5)]
            for _ in range(12):
                abc=[rng.randrange(1,p) for _ in range(3)]
                tail=[sum(abc[j]*pow(z,-(j+5)*k,p) for j in range(3))%p for k in range(3,8)]
                self.assertEqual(rank_rect(matrix(tail),p),3)
                self.assertEqual((tail[3]-s1*tail[2]+s2*tail[1]-s3*tail[0])%p,0)
                self.assertEqual((tail[4]-s1*tail[3]+s2*tail[2]-s3*tail[1])%p,0)
            for _ in range(12):
                tail=[rng.randrange(p) for _ in range(5)]
                e1=(tail[3]-s1*tail[2]+s2*tail[1]-s3*tail[0])%p
                e2=(tail[4]-s1*tail[3]+s2*tail[2]-s3*tail[1])%p
                self.assertEqual(rank_rect(matrix(tail),p)<=3,e1==0 and e2==0)

    def test_all_size_two_defect_tail(self):
        rows=verify_two_defect()
        self.assertEqual(len(rows),8)
        self.assertGreater(sum(row['checked_rows'] for row in rows),2000)

if __name__=='__main__':unittest.main(verbosity=2)
