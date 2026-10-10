import random
import unittest
from phase26_circuits import (P, Ledger, root_table, split_radix_dif, scalar_radix2,
    independent_dft, radix2_predicted, gt3_split)
from phase25_source.gt3_deferred import DeferredGT3

class Phase26(unittest.TestCase):
    def test_small_basis_exact(self):
        for n in (2,4,8,16,32,64):
            powers,_=root_table(n)
            for j in range(n):
                x=[int(i==j) for i in range(n)]
                s,sc=split_radix_dif(x,powers)
                r,rc=scalar_radix2(x,powers)
                expected=[powers[j*k%n] for k in range(n)]
                self.assertEqual(s,expected)
                self.assertEqual(r,expected)
                a,m=radix2_predicted(n)
                self.assertEqual((sc.adds,sc.muls),(a,m))
                self.assertEqual((rc.adds,rc.muls),(a,m))
    def test_random_long(self):
        rng=random.Random(2601)
        for n in (128,256,512,1024,2048,4096):
            powers,_=root_table(n)
            for _ in range(3):
                x=[rng.randrange(P) for j in range(n)]
                y,cs=split_radix_dif(x,powers)
                ref,cr=scalar_radix2(x,powers)
                self.assertEqual(y,ref)
                self.assertEqual((cs.adds,cs.muls),(cr.adds,cr.muls))
    def test_shear_butterfly_bases(self):
        for n in (2,4,8,16,32,64):
            powers,_=root_table(n)
            for j in range(n):
                x=[int(j==i) for i in range(n)]
                y,c=scalar_radix2(x,powers,shear=True)
                ref,d=scalar_radix2(x,powers)
                self.assertEqual(y,ref)
                self.assertEqual(c.adds,d.adds)
                self.assertEqual(c.muls-d.muls,n*(n.bit_length()-1)//2)
    def test_gt3_mixed_matrices(self):
        for G in (2,4,8,16,32,64,128):
            n=3*G
            powers,_=root_table(n)
            if G<=16:
                xs=[[int(i==j) for i in range(n)] for j in range(n)]
            else:
                r=random.Random(G)
                xs=[[r.randrange(P) for _ in range(n)] for _ in range(4)]
            for x in xs:
                v,c=gt3_split(x,method='split')
                ref,cr=gt3_split(x,method='radix2')
                self.assertEqual(v,ref)
                prior=DeferredGT3(x).full()
                self.assertEqual(v,prior)
                self.assertEqual((c.adds,c.muls),(cr.adds,cr.muls))
                if G<=8:self.assertEqual(v,independent_dft(x,powers))
    def test_cold_setup_ledger(self):
        for n in (8,16,64,1024):
            powers,prep=root_table(n)
            self.assertEqual(prep,n-1)
            self.assertEqual(powers[0],1)
            self.assertEqual(powers[-1]*powers[1]%P,1)
    def test_recurrence_exhaustive(self):
        cache={1:(0,0),2:(2,0)}
        for t in range(2,16):
            n=2**t
            a1,m1=cache[n//2]
            a2,m2=cache[n//4]
            cache[n]=(a1+2*a2+3*n//2, m1+2*m2+3*n//4-2)
            self.assertEqual(cache[n],radix2_predicted(n))

if __name__=='__main__':unittest.main()
