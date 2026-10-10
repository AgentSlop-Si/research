import random
import unittest
from math import lcm,gcd
from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR,direct_dft,n_root
from crt15_engine import make_plan,transform,predicted,fft3,fft5,fft15_gt,fft15_ct,Cost,power

FIELDS=((P,GENERATOR),(ALT_P,ALT_GENERATOR))

class TestPhase27(unittest.TestCase):
    def test_small_codelets_direct(self):
        for p,g in FIELDS:
            for n in (15,30):
                w=n_root(n,p,g)
                plan=make_plan(n,p,g,mode='ct')
                rr=random.Random(371+n+p)
                for _ in range(6):
                    x=[rr.randrange(p) for _ in range(n)]
                    c=Cost(); a=fft15_gt(x[:15],plan,c)
                    self.assertEqual((c.adds,c.muls),(81,25))
                    c=Cost(); b=fft15_ct(x[:15],plan,c)
                    self.assertEqual((c.adds,c.muls),(81,33))
                    if n==15:
                        expected=direct_dft(x,p,g)
                        self.assertEqual(a,expected)
                        self.assertEqual(b,expected)
                    else:
                        # 15th root of length30 is w^2
                        from crt15 import dft15
                        self.assertEqual(a,dft15(x[:15],pow(w,2,p),p))
                        self.assertEqual(b,a)

    def test_all_input_bases(self):
        for p,g in FIELDS:
            for n in (15,30,60,120,240):
                root=n_root(n,p,g)
                plan_gt=make_plan(n,p,g,mode='gt')
                plan_ct=make_plan(n,p,g,mode='ct')
                G=n//15
                for j in range(n):
                    x=[0]*n;x[j]=1
                    a,ca=transform(x,plan_gt)
                    b,cb=transform(x,plan_ct)
                    d,cc=transform(x,plan_ct,inner='ct')
                    expect=[pow(root,(j*k)%n,p) for k in range(n)]
                    self.assertEqual(a,expect)
                    self.assertEqual(b,expect)
                    self.assertEqual(d,expect)
                    self.assertEqual((ca.adds,ca.muls,ca.total()),predicted(G))
                    self.assertEqual(cb.total()-ca.total(),14*(G-1))
                    self.assertEqual(cc.total()-ca.total(),22*G-14)

    def test_dense_input_and_fallback_independence(self):
        for p,g in FIELDS:
            for n in (30,120,480):
                rng=random.Random(p+n)
                plans=[make_plan(n,p,g,mode='gt'),make_plan(n,p,g,mode='ct')]
                for _ in range(5):
                    v=[rng.randrange(p) for _ in range(n)]
                    a,_=transform(v,plans[0])
                    b,_=transform(v,plans[1])
                    self.assertEqual(a,b)
                    if n<=120:self.assertEqual(a,direct_dft(v,p,g))

    def test_corrupted_root_and_codelet_rejected(self):
        p,g=FIELDS[0];n=120
        self.assertRaises(ValueError,make_plan,n,p,g,root=1)
        plan=make_plan(n,p,g,mode='gt');rng=random.Random(44)
        v=[rng.randrange(p) for _ in range(n)]
        y,_=transform(v,plan)
        plan.k5.h1=(plan.k5.h1+1)%p
        y_corrupt,_=transform(v,plan)
        self.assertNotEqual(y,y_corrupt)

    def test_predicted_matches_all_degrees(self):
        for G in (1,2,4,8,16,32,64,128,256):
            for mode in ('gt','ct'):
                plan=make_plan(15*G,mode=mode)
                rng=random.Random(17*G)
                x=[rng.randrange(P) for _ in range(15*G)]
                res,c=transform(x,plan)
                self.assertEqual((c.adds,c.muls,c.total()),predicted(G,outer=mode))

    def test_cold_setup_root_tables_and_memory(self):
        for G in (1,2,4,8,16,32,64,128):
            gt=make_plan(15*G,mode='gt');ct=make_plan(15*G,mode='ct')
            self.assertEqual(ct.setup.total()-gt.setup.total(),(15*G-1)+14)
            self.assertEqual(len(gt.roots_g),G)
            self.assertEqual(len(ct.roots_n),15*G)
            self.assertIsNone(gt.roots_n)
            self.assertIsNone(gt.roots15)

    def test_cross_ratio_no_go(self):
        p,g=FIELDS[0]
        for a,b in ((2,2),(4,4),(4,8),(3,3),(3,5),(3,8),(5,8),(3,10)):
            n=a*b
            if (p-1)%n:continue
            root=n_root(n,p,g)
            # F_n contains a 2x2 cross ratio equal to this primitive n-th root.
            self.assertEqual(pow(root,n,p),1)
            self.assertTrue(all(pow(root,n//d,p)!=1 for d in {2,3,5} if n%d==0))
            if gcd(a,b)>1:
                self.assertNotEqual(pow(root,lcm(a,b),p),1)
            else:
                self.assertEqual(pow(root,lcm(a,b),p),1)
                # Certified CRT permutation for ALL n^2 Fourier matrix entries.
                ea=b*pow(b,-1,a);eb=a*pow(a,-1,b)
                wa=pow(root,b,p);wb=pow(root,a,p)
                for u in range(a):
                    for v in range(b):
                        j=(ea*u+eb*v)%n
                        for r in range(a):
                            for s in range(b):
                                k=(b*r+a*s)%n
                                self.assertEqual(pow(root,(j*k)%n,p),pow(wa,u*r,p)*pow(wb,v*s,p)%p)

if __name__=='__main__':unittest.main(verbosity=2)
