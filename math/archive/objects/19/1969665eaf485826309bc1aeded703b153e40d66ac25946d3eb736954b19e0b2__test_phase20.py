"""Exact Phase20 regression and adversarial checks."""
import random,unittest
from resultant_gate import (
    D,ResStats,interp_newton,resultant_at,strip_trivial_factors,
    sparse_group_eval,discover_resultant,transform_resultant)
from blind_sparse_rational import discover_two_defect_binomial
from annihilator_engine import RecurrenceGreen,Work,dense_from_shift_defects,direct_one_frequency
from rational_forcing import direct_dft_any
from blind_discovery import blind_bounded_defects


class Phase20(unittest.TestCase):
    def test_polynomial_interpolation(self):
        p=2013265921;g=random.Random(70)
        for deg in (0,1,3,10,32,45):
            ref=[g.randrange(p) for _ in range(deg+1)]
            y=[]
            for w in range(D+1):
                out=0
                for c in ref[::-1]:out=(out*w+c)%p
                y.append(out)
            c=interp_newton(y,p,Work())
            self.assertEqual(c,ref)

    def test_structured_two_defects_all_lengths(self):
        rng=random.Random(200120)
        for p,g,n in [(998244353,3,17),(2013265921,31,30),
                      (2013265921,31,60),(2013265921,31,128),
                      (2013265921,31,384)]:
            engine=RecurrenceGreen(n,p,g)
            for t in range(5):
                d=rng.randrange(1,n)
                alpha=rng.randrange(2,p)
                if pow(alpha,n,p)==1:alpha=2
                pos=rng.sample(range(n),2)
                h=[0]*n
                for j in pos:h[j]=rng.randrange(1,p)
                r=dense_from_shift_defects(h,d,alpha,p)
                x=engine.P.solve(r)
                y,m=transform_resultant(engine,x)
                self.assertEqual(y,direct_dft_any(x,engine.omega,p))
                if all(r) and n>20:
                    self.assertEqual(m['selected'],'blind-resultant-2defects')

    def test_resonant_wrap_collision_recovers(self):
        p,n=2013265921,128
        engine=RecurrenceGreen(n,p,31)
        delta=63;alpha=pow(engine.omega,9,p)
        r=[0]*n
        for t in range(n):
            r[(t*delta)%n]=pow(alpha,t,p)*(3 if t<17 else 5)%p
        self.assertEqual(sum(bool((r[j]-alpha*r[(j-delta)%n])%p) for j in range(n)),2)
        self.assertIsNone(blind_bounded_defects(r,p,2)[0])
        x=engine.P.solve(r)
        y,m=transform_resultant(engine,x)
        self.assertEqual(m['selected'],'blind-resultant-2defects')
        self.assertEqual(y,direct_dft_any(x,engine.omega,p))
        self.assertEqual(m['work'].repaired,9)  # 8 probes + 1 resonance repair

    def test_nonresonant_fourier_certificate(self):
        p,n=2013265921,128;engine=RecurrenceGreen(n,p,31)
        h=[0]*n;h[11]=5;h[93]=9
        r=dense_from_shift_defects(h,37,17,p)
        f,meta=discover_resultant(r,engine)
        self.assertIsNotNone(f)
        d,a,entries=f
        self.assertEqual(len(entries),2)
        self.assertEqual(meta.entries_verified,n)
        self.assertGreater(meta.interp_degree,0)
        self.assertLessEqual(meta.interp_degree,D)
        self.assertLessEqual(meta.root_candidates,D)

    def test_generic_input_fallback(self):
        p,n=2013265921,128;engine=RecurrenceGreen(n,p,31)
        rng=random.Random(5522)
        r=[rng.randrange(1,p) for _ in range(n)]
        x=engine.P.solve(r)
        y,m=transform_resultant(engine,x)
        self.assertEqual(m['selected'],'fallback')
        self.assertEqual(y,direct_dft_any(x,engine.omega,p))

    def test_unmodified_eight_probes_adversary(self):
        p,n=2013265921,128;engine=RecurrenceGreen(n,p,31)
        h=[0]*n;h[11]=5;h[93]=9
        r=dense_from_shift_defects(h,37,17,p)
        # Nonzero polynomial Delta(z)=prod_{k=0}^7(z-omega^k) has
        # zero Fourier values at the first 8 frequencies.
        poly=[1]
        for k in range(8):
            z=engine.powers[k]
            nxt=[0]*(len(poly)+1)
            for j,c in enumerate(poly):
                nxt[j]=(nxt[j]-c*z)%p
                nxt[j+1]=(nxt[j+1]+c)%p
            poly=nxt
        pert=r[:]
        for j,c in enumerate(poly):pert[j]=(pert[j]+c)%p
        self.assertNotEqual(pert,r)
        for k in range(8):
            self.assertEqual(direct_one_frequency(r,engine.powers[k],p),
                             direct_one_frequency(pert,engine.powers[k],p))
        x=engine.P.solve(pert)
        y,m=transform_resultant(engine,x)
        self.assertEqual(m['selected'],'fallback')
        self.assertEqual(y,direct_dft_any(x,engine.omega,p))

    def test_preconditioner_zero_and_simple(self):
        p,n=2013265921,64;engine=RecurrenceGreen(n,p,31)
        for r in ([0]*n,[1]+[0]*(n-1),[i*i+10 for i in range(n)]):
            x=engine.P.solve(r)
            y,m=transform_resultant(engine,x)
            self.assertEqual(y,direct_dft_any(x,engine.omega,p))

    def test_root_eval_vs_direct_horner(self):
        p,n=2013265921,384;engine=RecurrenceGreen(n,p,31)
        rng=random.Random(512)
        for degree in (1,10,30,45):
            c=[rng.randrange(p) for _ in range(degree+1)]
            f,_=sparse_group_eval(c,engine,Work())
            for k,w in enumerate(engine.powers):
                val=0
                for cc in c[::-1]:val=(val*w+cc)%p
                self.assertEqual(f[k],val)

    def test_resultant_root_degree_witness(self):
        p,n=2013265921,64;engine=RecurrenceGreen(n,p,31)
        r=[random.Random(k).randrange(p) for k in range(n)]
        R=[direct_one_frequency(r,engine.powers[k],p) for k in range(8)]
        coeff=interp_newton([resultant_at(R,w,p,Work()) for w in range(D+1)],p,Work())
        self.assertLessEqual(len(coeff)-1,D)
        for w in range(D+1,D+8):
            val=0
            for c in coeff[::-1]:val=(val*w+c)%p
            self.assertEqual(val,resultant_at(R,w,p,Work()))
        red,z,o=strip_trivial_factors(coeff,p,Work())
        for w in (2,23,89):
            av=0;rv=0
            for c in coeff[::-1]:av=(av*w+c)%p
            for c in red[::-1]:rv=(rv*w+c)%p
            self.assertEqual(av,rv*pow(w,z,p)*pow(w-1,o,p)%p)

if __name__=='__main__':unittest.main()
