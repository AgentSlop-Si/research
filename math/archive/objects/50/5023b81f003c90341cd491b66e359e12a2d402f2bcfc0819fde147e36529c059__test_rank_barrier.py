"""Independent finite-field matrix-rank stress tests for the Jacobian bottleneck."""
from __future__ import annotations
import random
import unittest

P=998244353
ROOT=3


def rank_mod(rows, p=P):
    if not rows: return 0
    a=[[v%p for v in row] for row in rows]
    height,width=len(a),len(a[0]); r=0
    for col in range(width):
        sel=next((i for i in range(r,height) if a[i][col]),None)
        if sel is None:continue
        a[r],a[sel]=a[sel],a[r]
        inv=pow(a[r][col],p-2,p)
        for j in range(col,width):a[r][j]=a[r][j]*inv%p
        for i in range(height):
            if i==r:continue
            f=a[i][col]
            if f:
                for j in range(col,width):a[i][j]=(a[i][j]-f*a[r][j])%p
        r+=1
        if r==height:break
    return r


def matmul(A,B,p=P):
    if len(A[0])!=len(B):raise ValueError('wrong dimensions')
    return [[sum(A[i][k]*B[k][j] for k in range(len(B)))%p
             for j in range(len(B[0]))] for i in range(len(A))]


def fourier_matrix(n,p=P):
    if (p-1)%n:raise ValueError('bad root')
    root=pow(ROOT,(p-1)//n,p)
    return [[pow(root,k*j,p) for j in range(n)] for k in range(n)]


class BottleneckRank(unittest.TestCase):
    def test_exact_fft_rank_is_full(self):
        for n in (1,2,4,8,16,32):
            self.assertEqual(rank_mod(fourier_matrix(n)),n)

    def test_any_nonlinear_jacobian_factors_through_width(self):
        # For differentiable E:C^n -> C^w and D:C^w -> C^n,
        # J_(D o E) = J_D J_E at a point, with rank <= w.
        # Testing arbitrary Jacobians is a finite-field model of the identity.
        r=random.Random(20261009)
        for n in (2,4,8,16):
            F=fourier_matrix(n)
            for w in (1,max(1,n//2),n-1):
                J_encoder=[[r.randrange(P) for _ in range(n)] for _ in range(w)]
                J_decoder=[[r.randrange(P) for _ in range(w)] for _ in range(n)]
                composition=matmul(J_decoder,J_encoder)
                self.assertLessEqual(rank_mod(composition),w)
                self.assertNotEqual(composition,F)

    def test_construction_at_full_width(self):
        n=8
        J_encoder=[[int(i==j) for j in range(n)] for i in range(n)]
        J_decoder=fourier_matrix(n)
        self.assertEqual(matmul(J_decoder,J_encoder),fourier_matrix(n))

if __name__=='__main__': unittest.main()
