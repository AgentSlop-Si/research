"""Exact, independent tests for nested 15 and nested 60 transforms."""
import unittest,random
from dataclasses import replace
from crt15 import P,GENERATOR,ALT_P,ALT_GENERATOR,n_root
from crt15_engine import make_plan, transform as gt_transform, predicted as gt_predicted
from wfta15 import make_wfta_plan,fft15_wfta,transform_wfta,predicted as wfta_predicted
from fused60 import make_fused60_plan, kernel60, transform_fused,predicted_fused
from weave_optimizer import cost_pre,cost_post,optimal,FACTORS
from crt15 import Cost
from itertools import permutations

FIELDS=((P,GENERATOR),(ALT_P,ALT_GENERATOR))

class TestPhase28(unittest.TestCase):
    def test_wfta15_kernel_single_basis(self):
        for p,gen in FIELDS:
            plan=make_wfta_plan(15,p=p,gen=gen)
            root=n_root(15,p,gen)
            self.assertEqual(plan.preparation.total(),12)
            for j in range(15):
                x=[0]*15;x[j]=1
                c=Cost();got=fft15_wfta(x,plan,c)
                self.assertEqual(got,[pow(root,(j*k)%15,p) for k in range(15)])
                self.assertEqual((c.adds,c.muls),(81,17))

    def test_fused60_kernel_complete_basis(self):
        for p,gen in FIELDS:
            plan=make_fused60_plan(60,p=p,gen=gen)
            root=n_root(60,p,gen)
            # a[i15*4+j4]; out[k15*4+k4]. F15 and F4 roots.
            for idx in range(60):
                x=[0]*60;x[idx]=1
                c=Cost();y=kernel60(x,plan,c)
                j15,j4=divmod(idx,4)
                expected=[pow(root,(4*j15*k15+15*j4*k4)%60,p) for k15 in range(15) for k4 in range(4)]
                self.assertEqual(y,expected)
                self.assertEqual((c.adds,c.muls),(444,69))

    def test_all_input_random_large_and_counts(self):
        for p,gen in FIELDS:
            for h in (1,2,4,8,16,32,64):
                n=60*h;plan=make_fused60_plan(n,p=p,gen=gen)
                rng=random.Random(28*n+p)
                x=[rng.randrange(p) for _ in range(n)]
                a,ca=transform_fused(x,plan)
                b,cb=transform_wfta(x,plan.wfta)
                self.assertEqual(a,b)
                self.assertEqual((ca.adds,ca.muls,ca.total()),predicted_fused(h))
                self.assertEqual((cb.adds,cb.muls,cb.total()),wfta_predicted(4*h))
                self.assertEqual(cb.total()-ca.total(),14*h)
                self.assertEqual(gt_predicted(4*h)[-1]-ca.total(),46*h)

    def test_independent_direct_dft_small(self):
        for p,gen in FIELDS:
            for h in (1,2,4):
                n=60*h;plan=make_fused60_plan(n,p=p,gen=gen)
                rng=random.Random(8*n+p)
                x=[rng.randrange(p) for _ in range(n)]
                got,_=transform_fused(x,plan)
                root=n_root(n,p,gen)
                expected=[sum(x[j]*pow(root,(j*k)%n,p) for j in range(n))%p for k in range(n)]
                self.assertEqual(got,expected)

    def test_prepared_coefficient_diagonal(self):
        for p,gen in FIELDS:
            for h in (1,2,4,8,16):
                plan=make_fused60_plan(60*h,p=p,gen=gen)
                self.assertEqual(plan.wfta.preparation.total(),12)
                self.assertEqual(plan.extra_setup.total(),17)
                self.assertEqual(sum(z!=1 for a in plan.wfta.d15 for z in a),17)
                self.assertEqual(sum(z!=1 for a in plan.d60 for b in a for z in b),69)
                self.assertEqual(len(plan.wfta.base.roots_g),4*h)

    def test_corruption_does_not_pass(self):
        p,gen=FIELDS[0];plan=make_fused60_plan(240,p=p,gen=gen)
        rng=random.Random(447)
        x=[rng.randrange(p) for _ in range(240)]
        good,_=transform_fused(x,plan)
        z=[list(map(list,row)) for row in plan.d60]
        z[1][1][3]=(z[1][1][3]+1)%p
        bad_plan=replace(plan,d60=tuple(tuple(tuple(v) for v in row) for row in z))
        bad,_=transform_fused(x,bad_plan)
        self.assertNotEqual(good,bad)

    def test_invalid_modulus_or_root_rejected(self):
        for x in (30,90,180,360):
            self.assertRaises(ValueError,make_fused60_plan,x)
        self.assertRaises(ValueError,make_fused60_plan,60,p=P,gen=GENERATOR,root=1)

    def test_noncoprime_twiddle_gauge_obstruction(self):
        from math import gcd,lcm
        for p,gen in FIELDS:
            for h in (2,4,8,16):
                g=4*h
                omega=n_root(g,p,gen)
                self.assertGreater(g,lcm(4,h))
                self.assertNotEqual(pow(omega,lcm(4,h),p),1)
                # F_g contains primitive g-th cross ratio, F4⊗Fh cannot.

    def test_tensor_weave_optimality_enumerate(self):
        B,A,cost=optimal()
        pre=[cost_pre(perm) for perm in permutations(FACTORS)]
        post=[cost_post(perm) for perm in permutations(FACTORS)]
        self.assertEqual((min(pre),min(post),cost),(216,228,444))
        self.assertEqual(B[-1].name,'F5')
        self.assertEqual(A[0].name,'F5')
        self.assertEqual(sorted(pre),[216,216,228,228,240,240])
        self.assertEqual(sorted(post),[228,228,240,240,252,252])

    def test_actual_setup_and_charged_cold_difference(self):
        for h in (1,2,4,8,16):
            p=make_fused60_plan(60*h)
            baseline=make_plan(60*h,mode='gt')
            self.assertEqual(p.wfta.base.setup.total(),baseline.setup.total())
            saving=(gt_predicted(4*h)[-1]+baseline.setup.total())-(predicted_fused(h)[-1]+baseline.setup.total()+12+17)
            self.assertEqual(saving,46*h-29)
            self.assertGreater(saving,0)

if __name__=='__main__': unittest.main(verbosity=2)
