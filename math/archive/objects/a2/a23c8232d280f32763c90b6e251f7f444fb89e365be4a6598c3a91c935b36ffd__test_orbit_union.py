#!/usr/bin/env python3
"""Verification of exact graph-union grouping, including sparse support."""
import unittest,random
from phase6_exact import P,independent_full_dft,root_of_unity
from phase7_rank_fusion import root_table,dechirp,Counter
from phase7_orbit_union import orbit_union_transform,sample_orbit_union
from phase7_hidden_shift_detector import unknown_shift_rank1_transform

class OrbitUnionTests(unittest.TestCase):
    def test_exact_finite_field_orbits(self):
        tested=0
        for q,m in [(64,4),(128,8),(256,8),(512,8),(1024,16),(2048,16),(4096,16)]:
            k=q//m
            for r in [1,2,3,min(m,5)]:
                for zeros in [False,True]:
                    for repeat in range(3):
                        a=[1,3,5][repeat];beta=9+repeat
                        x,*_=sample_orbit_union(k,m,r,seed=q+repeat+10*r,
                                                  a=a,beta=beta,zeros=zeros)
                        got,certificate,c=orbit_union_transform(x,m,r,a,beta,return_certificate=True)
                        self.assertEqual(got,independent_full_dft(x))
                        U,H,g,groups=certificate
                        self.assertLessEqual(len(H),r)
                        self.assertEqual(c.inversions,1)
                        tab=root_table(q,root_of_unity(q),None)
                        V=list(dechirp(x,m,a,beta,tab,None))
                        for b in range(k):
                            for t in range(m):
                                want=sum(H[i][t]*U[(b+g[t])%k][i] for i in range(len(H)))%P
                                self.assertEqual(V[b][t],want)
                        tested+=1
        print('PASS exact hidden union cases',tested)

    def test_certified_failure_and_fallback_gate(self):
        k,m=32,8
        x,*_=sample_orbit_union(k,m,3,seed=999)
        self.assertIsNone(orbit_union_transform(x,m,1)[0])
        self.assertIsNone(orbit_union_transform(x,m,2)[0])
        self.assertEqual(orbit_union_transform(x,m,3)[0],independent_full_dft(x))
        rng=random.Random(4)
        for k,m in [(16,4),(32,8),(64,8)]:
            x=[rng.randrange(1,P) for _ in range(k*m)]
            self.assertIsNone(orbit_union_transform(x,m,3)[0])
        q=256
        x,*_=sample_orbit_union(32,8,1,seed=201)
        bad=x.copy();bad[-1]=(bad[-1]+1)%P
        self.assertIsNone(orbit_union_transform(bad,8,1)[0])

    def test_deduplicate_projective_orbits(self):
        # All columns from shift-scaled one reference, with most inputs zero.
        k,m=32,8;q=k*m
        rng=random.Random(71)
        f=[rng.randrange(1,P) if i%5 in (0,3) else 0 for i in range(k)]
        g=[(2*t*t+3*t)%k for t in range(m)]
        h=[rng.randrange(1,P) for _ in range(m)]
        tab=root_table(q,root_of_unity(q),None)
        x=[]
        for b in range(k):
            for t in range(m):
                val=h[t]*f[(b+g[t])%k]%P
                power=(t*(t-1)//2+m*b*t)%q
                x.append(val*tab[(-power)%q]%P)
        got,cert,c=orbit_union_transform(x,m,m,return_certificate=True)
        self.assertEqual(len(cert[1]),1)
        self.assertEqual(c.inversions,1)
        self.assertEqual(got,independent_full_dft(x))
        self.assertEqual(got,unknown_shift_rank1_transform(x,m)[0])

    def test_zero_columns_and_zero_everywhere(self):
        k,m=32,8;q=k*m
        x,*_=sample_orbit_union(k,m,2,seed=14)
        for b in range(k):
            x[b*m+3]=0
            x[b*m+7]=0
        got,cert,c=orbit_union_transform(x,m,2,return_certificate=True)
        self.assertEqual(got,independent_full_dft(x))
        self.assertEqual(cert[3][3],-1)
        self.assertEqual(cert[3][7],-1)
        got,cert,c=orbit_union_transform([0]*q,m,0,return_certificate=True)
        self.assertEqual(got,[0]*q)
        self.assertEqual(c.inversions,0)

if __name__=='__main__':unittest.main(verbosity=2)
