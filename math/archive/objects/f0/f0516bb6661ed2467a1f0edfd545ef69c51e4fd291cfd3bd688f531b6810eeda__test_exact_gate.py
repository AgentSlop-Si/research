"""Independent finite-field auditing of the exact complex theorems.
The rigorous characteristic-zero proofs are in PROOF_CERTIFICATE.md.
"""
import random,unittest
from fractions import Fraction
from math import ceil
from itertools import combinations
import numpy as np
from bitrev_rank import exact_cut_rank,bitrev_perm,predicted_qs_rank
from coset_rank import (prim_root,rank_mod,fourier_submatrix,dyadic_union_columns,
                        rank_coset_formula,single_consecutive_coset_formula)

PRIMES=(12289,65537)


def formula_sum(n):
    m=n.bit_length()-1
    if m%2==0: return (4*n*n+3*n*m-4*n)//24
    return (4*n*n+3*n*m+n)//24


def reversal_rank_sums(n):
    return sum(exact_cut_rank(n,k) for k in range(1,n))

class ExactFourierBitrevTest(unittest.TestCase):
    def test_all_finite_field_cuts(self):
        for n in (4,8,16,32,64):
            b=bitrev_perm(n)
            for p in PRIMES:
                M=fourier_submatrix(n,b,b,p)
                for k in range(1,n):
                    r=rank_mod(M[:k,k:],p)
                    self.assertEqual(r,exact_cut_rank(n,k),(n,p,k))
                    # Symmetric Fourier matrix means lower left is transposed upper right.
                    self.assertEqual(r,rank_mod(M[k:,:k],p))

    def test_N128_selected_cuts(self):
        n=128;b=bitrev_perm(n)
        selected=(1,2,3,7,8,15,16,31,32,47,61,62,63,64,65,66,67,81,95,96,111,112,120,125,126,127)
        for p in PRIMES:
            M=fourier_submatrix(n,b,b,p)
            for k in selected:
                self.assertEqual(rank_mod(M[:k,k:],p),exact_cut_rank(n,k),(n,p,k))

    def test_n8_exhaustive_critical_minors(self):
        n=8; sub=list(combinations(range(n),3));cols=list(combinations(range(n),5))
        for p in PRIMES:
            M=fourier_submatrix(n,list(range(n)),list(range(n)),p)
            for rows in sub:
                for C in cols:
                    self.assertEqual(rank_mod(M[np.ix_(rows,C)],p),3,(p,rows,C))

    def test_random_independent_endpoint_orders(self):
        rng=random.Random(17081)
        for n in (16,32,64):
            L=n//4;cut=n//2-1
            for p in PRIMES:
                F=fourier_submatrix(n,list(range(n)),list(range(n)),p)
                for _ in range(24):
                    row=list(range(n));col=list(range(n))
                    rng.shuffle(row);rng.shuffle(col)
                    M=F[np.ix_(row,col)]
                    rank=rank_mod(M[:cut,cut:],p)
                    self.assertGreaterEqual(rank,L+1,(n,p,row,col,rank))

    def test_trace_square_exact_inequality(self):
        for n in (8,16,32,64,128,256,512):
            L=n//4
            val=Fraction(L,1)+Fraction(3,4)+Fraction(1,4*L)+Fraction(1,16*L*L)
            self.assertLess(val,L+1)
            self.assertEqual(ceil(val),L+1)

    def test_optimal_peak_and_sum_formulas(self):
        for m in range(1,13):
            n=1<<m
            self.assertEqual(predicted_qs_rank(n),1 if n==2 else (1 if n==4 else n//4+1))
            s=reversal_rank_sums(n)
            self.assertEqual(s,formula_sum(n),(n,s,formula_sum(n)))
            self.assertGreaterEqual(6*s,n*n-1)

    def test_coset_formula(self):
        rng=random.Random(260910)
        for n in (8,16,32,64):
            for p in PRIMES:
                for q in (2,4,8):
                    if q>n:continue
                    for _ in range(12):
                        rows=sorted(rng.sample(range(n),rng.randint(1,n)))
                        bases=sorted(rng.sample(range(q),rng.randint(1,q)))
                        cols=dyadic_union_columns(n,q,bases)
                        a=rank_mod(fourier_submatrix(n,rows,cols,p),p)
                        b=rank_coset_formula(n,q,bases,rows,p)
                        self.assertEqual(a,b,(n,p,q,rows,bases))

    def test_consecutive_single_coset_formula(self):
        rng=random.Random(20261009)
        for n in (8,16,32,64):
            for p in PRIMES:
                for q in (2,4,8):
                    if q>n:continue
                    for _ in range(10):
                        rows=sorted(rng.sample(range(n),rng.randint(1,n)))
                        b=rng.randrange(q);k=rng.randint(1,n//q)
                        cols=[b+q*j for j in range(k)]
                        rk=rank_mod(fourier_submatrix(n,rows,cols,p),p)
                        expect=single_consecutive_coset_formula(n,q,b,rows,k)
                        self.assertEqual(rk,expect,(n,p,q,b,k))

    def test_prior_endpoint_positive_control(self):
        n=16
        order=[0,8,4,12,1,9,5,13,2,10,6,14,3,11,7,15]
        for p in PRIMES:
            M=fourier_submatrix(n,order,order,p)
            self.assertEqual(rank_mod(M[3:, :9],p),8)
            # Applying a naive Vandermonde rule would incorrectly yield 9.
            self.assertEqual(min(13,9),9)

if __name__=='__main__':unittest.main(verbosity=2)
