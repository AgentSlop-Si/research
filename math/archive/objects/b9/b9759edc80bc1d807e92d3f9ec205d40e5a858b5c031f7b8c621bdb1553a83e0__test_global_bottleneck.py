import cmath
import itertools
import math
import random
import sys
import unittest
from fractions import Fraction
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from global_bottleneck import (
    P, packed_dft, chirp_phases, direct_dft, ntt_reference,
    block_digits, block_encode_exact, grid_count, packing_possible
)


class PackedExactDFT(unittest.TestCase):
    def test_full_basis(self):
        for n in [2,4,8,16,32,64]:
            for j in range(n):
                x=[0]*n;x[j]=1
                got,_=packed_dft(x)
                self.assertEqual(got,direct_dft(x))

    def test_random_signed_mod_field(self):
        r=random.Random(20261009)
        for n in [2,4,8,16,32,64,128,256,512,1024,2048]:
            for _ in range(4):
                x=[r.randrange(-2*P,2*P) for j in range(n)]
                got,cost=packed_dft(x)
                self.assertEqual(got,ntt_reference(x),f'length {n}')
                self.assertEqual(cost.operand_bits,n*cost.cell_bits)
                self.assertGreater(cost.operand_bits,n*math.ceil(math.log2(P)))

    def test_direct_random(self):
        r=random.Random(13)
        for n in [2,4,8,16,32,64]:
            for _ in range(3):
                x=[r.randrange(P) for j in range(n)]
                self.assertEqual(packed_dft(x)[0],direct_dft(x))

    def test_chirp_inverse_and_periodicity(self):
        for n in [2,4,8,16,32,64]:
            d,h,zeta=chirp_phases(n)
            self.assertEqual(pow(zeta,n,P),P-1)
            for j in range(n):
                self.assertEqual(d[j]*h[j]%P,1)
                self.assertEqual(d[j],pow(zeta,j*j,P))
                self.assertEqual(h[j],pow(zeta,(-j*j)%(2*n),P))

    def test_invalid(self):
        for values in ([],[1,2,3]):
            with self.assertRaises(ValueError): packed_dft(values)

    def test_other_valid_prime_fields(self):
        rng=random.Random(212)
        for p in (167772161,469762049,1224736769):
            for n in (4,16,64):
                values=[rng.randrange(p) for _ in range(n)]
                got,_=packed_dft(values,p=p)
                self.assertEqual(got,direct_dft(values,p=p))

    def test_zero_and_constant(self):
        for n in [2,8,64,256]:
            for x in [[0]*n,[1]*n,[P-1]*n]:
                self.assertEqual(packed_dft(x)[0],ntt_reference(x))


class PackingBottleneck(unittest.TestCase):
    def test_grid_exact_small(self):
        self.assertEqual(grid_count(1,1),5)
        self.assertEqual(grid_count(1,2),9)
        self.assertEqual(grid_count(1,1,Fraction(1,4)),9)

    def test_capacity_examples(self):
        self.assertFalse(packing_possible(n=128,w=2,M=1,L=10))
        self.assertTrue(packing_possible(n=128,w=128,M=1,L=10))
        self.assertFalse(packing_possible(n=64,w=4,M=1,L=10,complex_coordinates=False))

    def test_monotonicity(self):
        for n in (8,32,128,512):
            for w in (1,2,4):
                vals=[packing_possible(n,w,1,L) for L in (1,2,4,16,256,65536)]
                self.assertEqual(vals,sorted(vals))

    def test_all_short_block_encodings_unique(self):
        for n,b in ((4,2),(6,3),(8,2),(8,4),(12,3)):
            codes={}
            for v in range(1<<n):
                bits=[(v>>(n-j-1)) & 1 for j in range(n)]
                code=block_digits(bits,b)
                self.assertNotIn(code,codes)
                codes[code]=v
            self.assertEqual(len(codes),1<<n)

    def test_block_boundary_lipschitz_witness(self):
        for n,b in [(4,2),(8,4),(16,8),(32,16)]:
            a=[0]*n
            c=a.copy();c[b-1]=1
            encoder_diff=max(abs(u-v) for u,v in zip(block_encode_exact(a,b),block_encode_exact(c,b)))
            self.assertEqual(encoder_diff,Fraction(1,2**b))
            # For delta of one standard basis vector, all N Fourier values have modulus one.
            omega=cmath.exp(2j*math.pi/n)
            for k in range(n):
                self.assertAlmostEqual(abs(omega**(k*(b-1))),1.0,places=12)
            self.assertEqual(Fraction(1,1)/encoder_diff,2**b)

    def test_information_output_digits(self):
        # A channel of w registers, each with <= 2**b states, cannot be
        # injective on all 2**N Boolean inputs unless w*b >= N.
        for n in [16,64,256]:
            for b in [1,2,4,8]:
                w=(n+b-1)//b
                self.assertGreaterEqual(w*b,n)
                if w>=2:
                    self.assertLess((w-1)*b,n+b)

if __name__=='__main__': unittest.main()
