import unittest,random
from crt15 import Cost,P,GENERATOR,ALT_P,ALT_GENERATOR,n_root
from fused60 import make_fused60_plan,transform_fused,predicted_fused
from fused120 import make_fused120_plan,transform_fused120,kernel120,predicted_fused120
from wfta8 import before8,after8,prepare_diag8,fft8_wfta

FIELDS=((P,GENERATOR),(ALT_P,ALT_GENERATOR))

def direct_dft(x,p,root):
    n=len(x);out=[]
    for k in range(n):
        step=pow(root,k,p);power=1;v=0
        for xj in x:
            v+=power*xj
            power=power*step%p
        out.append(v%p)
    return out

class TestPhase29(unittest.TestCase):
    def test_wfta8_codelet_all_basis_both_fields(self):
        for p,gen in FIELDS:
            root=n_root(8,p,gen)
            diag=prepare_diag8(root,p)
            self.assertEqual(sum(v!=1 for v in diag),4)
            for j in range(8):
                x=[0]*8;x[j]=1
                c=Cost();result=fft8_wfta(x,root,p,c)
                self.assertEqual(result,[pow(root,j*k,p) for k in range(8)])
                self.assertEqual((c.adds,c.muls),(26,4))

    def test_full_kernel120_crt_tensor_basis(self):
        for p,gen in FIELDS:
            plan=make_fused120_plan(120,p=p,gen=gen)
            root=n_root(120,p,gen)
            # tensor inputs are v15*8+j8; 15th root omega15=w^8 and omega8=w^15.
            for v in range(15):
                for j8 in range(8):
                    x=[0]*120;x[8*v+j8]=1
                    c=Cost();z=kernel120(x,plan,c)
                    self.assertEqual((c.adds,c.muls),(1038,140))
                    expected=[pow(root,(8*v*k15+15*j8*k8)%120,p)
                              for k15 in range(15) for k8 in range(8)]
                    self.assertEqual(z,expected)

    def test_full_DFT_small_exact_direct(self):
        for p,gen in FIELDS:
            for h in (1,2,4):
                n=120*h;plan=make_fused120_plan(n,p=p,gen=gen)
                root=n_root(n,p,gen)
                rng=random.Random(2003*p+113*h)
                x=[rng.randrange(p) for _ in range(n)]
                a,c=transform_fused120(x,plan)
                self.assertEqual(a,direct_dft(x,p,root))
                self.assertEqual((c.adds,c.muls,c.total()),predicted_fused120(h))

    def test_phase28_crosscheck_large(self):
        for p,gen in FIELDS:
            for h in (1,2,4,8,16,32,64):
                n=120*h
                plan=make_fused120_plan(n,p=p,gen=gen)
                old=make_fused60_plan(n,p=p,gen=gen)
                rng=random.Random(3155+n+p)
                x=[rng.randrange(p) for _ in range(n)]
                a,c=transform_fused120(x,plan)
                b,d=transform_fused(x,old)
                self.assertEqual(a,b)
                self.assertEqual(d.total()-c.total(),13*h)
                self.assertEqual(c.total(),predicted_fused120(h)[-1])

    def test_root_supply_rejects_invalid(self):
        p,gen=FIELDS[0]
        for n in (15,60,121,240):
            with self.subTest(n=n):
                if n%120:witherr=ValueError
                else:continue
                with self.assertRaises(witherr):make_fused120_plan(n,p=p,gen=gen)

    def test_bad_diagonal_detected(self):
        p,gen=FIELDS[0]
        plan=make_fused120_plan(120,p=p,gen=gen)
        d=[[list(cell) for cell in row] for row in plan.d120]
        d[0][0][3]=(d[0][0][3]+1)%p
        from dataclasses import replace
        mutated=replace(plan,d120=tuple(tuple(tuple(x) for x in row) for row in d))
        found=False
        for j in range(120):
            x=[0]*120;x[j]=1
            reference=kernel120(x,plan,Cost())
            changed=kernel120(x,mutated,Cost())
            if reference!=changed:found=True;break
        self.assertTrue(found)

    def test_cold_setup_break_even(self):
        for p,gen in FIELDS:
            for h in (1,2,4,8,16):
                n=120*h
                old=make_fused60_plan(n,p=p,gen=gen)
                new=make_fused120_plan(n,p=p,gen=gen)
                self.assertEqual(old.wfta.base.setup.total(),new.wfta.base.setup.total())
                self.assertEqual(old.wfta.preparation.total(),new.wfta.preparation.total())
                self.assertEqual(old.extra_setup.total(),17)
                self.assertEqual(new.extra_setup.total(),74)
                self.assertEqual((old.extra_setup.total()-new.extra_setup.total()),-57)
                self.assertEqual((old.extra_setup.total()-new.extra_setup.total())+13*h,13*h-57)

    def test_weighted_four_rank_six_symbolic(self):
        from weighted4_rank_gate import run
        result=run()
        self.assertEqual(result['necessary_diagonal_width_in_fixed_Q_pre_post_model'],6)
        self.assertTrue(result['explicit_width_six_witness'])

    def test_weighted_four_gate_increases_cost(self):
        from weighted4_gate import tensor_weighted4,reference_weighted4
        from wfta15 import make_wfta_plan
        for p,gen in FIELDS:
            plan=make_wfta_plan(120,p=p,gen=gen)
            root=n_root(8,p,gen)
            i=pow(root,2,p)
            x=[random.Random(j*17+p).randrange(p) for j in range(60)]
            for q in (0,1):
                y,c,paid=tensor_weighted4(x,plan,pow(root,q,p),i)
                z,baseline=reference_weighted4(x,plan,pow(root,q,p),i)
                self.assertEqual(y,z)
                self.assertEqual(c.adds,468)
                self.assertEqual((c.total(),paid),(572,104) if q==0 else (575,107))
                self.assertGreater(c.total(),baseline.total())

    def test_exact_cyclotomic_proof(self):
        from symbolic_phase29 import run
        result=run()
        self.assertTrue(result['all_exact'])
        self.assertEqual(result['tensor120']['identity_coefficients'],4)
        self.assertEqual(result['wfta8']['exact_dft_entries'],64)

    def test_gauge_formula(self):
        from gauge_obstruction import run,bound
        x=run()
        self.assertEqual(x['stage8_upper_bound_extra_savings'],21)
        self.assertEqual(x['stage4_upper_bound_extra_savings'],3)
        self.assertEqual(bound(8,16),8*16-(16+28))

if __name__=='__main__':unittest.main()
