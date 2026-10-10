import unittest
from random import Random
from cut_budget import (PRIMES,rank,fourier,stage,qsrank,matmul,middle_shuffle,
                        two_stage_bound,endpoint_certificate,endpoint_patterns,permute)

class TestTwoStageMinorObstruction(unittest.TestCase):
    def test_vandermonde_half_rank(self):
        for p,g in PRIMES:
            for n in (4,8,16,32,64):
                f=fourier(n,p,g); m=n//2
                self.assertEqual(rank([row[:m] for row in f[:m]],p),m)
                self.assertEqual(rank([row[m:] for row in f[:m]],p),m)

    def test_either_endpoint_can_be_permuted(self):
        rng=Random(77)
        for p,g in PRIMES:
            for n in (8,16,32):
                f=fourier(n,p,g);m=n//2
                order=list(range(n));rng.shuffle(order)
                self.assertEqual(rank([f[k][:m] for k in order[:m]],p),m)
                self.assertEqual(rank([f[k][m:] for k in order[:m]],p),m)
                self.assertEqual(rank([[row[k] for k in order[:m]] for row in f[:m]],p),m)
                self.assertEqual(rank([[row[k] for k in order[m:]] for row in f[:m]],p),m)

    def test_arbitrary_internal_shuffles(self):
        rng=Random(903)
        for p,_ in PRIMES:
            for n in (8,16,32):
                for ra,rb in ((1,1),(2,3),(3,1)):
                    A=stage(n,ra,p,rng);B=stage(n,rb,p,rng)
                    self.assertLessEqual(qsrank(A,p),ra)
                    self.assertLessEqual(qsrank(B,p),rb)
                    order=list(range(n));rng.shuffle(order)
                    M=matmul(B,middle_shuffle(A,order),p)
                    cert=two_stage_bound(M,A,B,order,p)
                    self.assertLessEqual(cert['left_rank']+cert['right_rank'],
                         n//2+2*(ra+rb))

    def test_double_endpoint_weakening(self):
        p,g=PRIMES[0];n=16;f=fourier(n,p,g);o=endpoint_patterns(n)
        original=endpoint_certificate(f,p)
        both=endpoint_certificate(permute(f,o['bit_reversal'],o['bit_reversal']),p)
        self.assertEqual(original['necessary_rank_sum'],4)
        self.assertEqual(both['necessary_rank_sum'],1)

    def test_n32_two_stage_r3_unsupported(self):
        # Exact all-parameter certificate, NOT just a finite random search.
        n=32;r=3
        self.assertLess(2*r,n//4)

    def test_fft_full_matrix_invertible(self):
        for p,g in PRIMES:
            for n in (4,8,16):
                self.assertEqual(rank(fourier(n,p,g),p),n)

if __name__=='__main__':unittest.main()
