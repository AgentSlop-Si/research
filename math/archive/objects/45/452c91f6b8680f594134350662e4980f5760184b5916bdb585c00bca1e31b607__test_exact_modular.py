"""Exact finite-field identity checks for the factorization ONLY.

OpenAI #130 is NOT an NTT over this field; we are testing the universal
algebraic grouping identity using integer arithmetic with no rounding.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import random
from hybrid_sparse import normalize_changes

P = 998244353
G = 3

def direct_ntt(vec, w):
    n = len(vec)
    return [sum(vec[j]*pow(w,j*q,P) for j in range(n)) % P for q in range(n)]

def grouped_sparse_ntt(n, edits):
    assert (P-1)%n == 0
    w = pow(G,(P-1)//n,P)
    edits = {i:int(round(z.real))%P for i,z in normalize_changes(n,edits).items()}
    k = len(edits)
    b = 1 << (max(1,k)-1).bit_length()
    m = n//b
    wm=pow(w,b,P)
    wb=pow(w,m,P)
    tmp=[[0]*b for _ in range(m)]
    for j,val in edits.items():
        r,t=divmod(j,b)[1], j//b
        for q in range(m):
            tmp[q][r]=(tmp[q][r]+val*pow(wm,t*q,P))%P
    for q in range(m):
        for r in range(b):
            tmp[q][r]=(tmp[q][r]*pow(w,r*q,P))%P
    out=[0]*n
    for q in range(m):
        row = direct_ntt(tmp[q],wb)
        for l in range(b):
            out[q+m*l]=row[l]
    return out

class TestExactAlgebra(unittest.TestCase):
    def test_exact_grouped_agrees_with_direct(self):
        rng=random.Random(32)
        for n in [1,2,4,8,16,32,64,128]:
            w=pow(G,(P-1)//n,P)
            for k in sorted(set([0,1,2,3,4,7,n//2,n])):
                if k>n:continue
                locations=rng.sample(range(n),k)
                vals=[rng.randrange(-30,31) for _ in locations]
                vec=[0]*n
                edits=[]
                for j,v in zip(locations,vals):
                    vec[j] = v%P
                    edits.append((j,v))
                actual=grouped_sparse_ntt(n,edits)
                want=direct_ntt(vec,w)
                self.assertEqual(actual,want,f'failed {n=} {k=}')

if __name__=='__main__':unittest.main()
