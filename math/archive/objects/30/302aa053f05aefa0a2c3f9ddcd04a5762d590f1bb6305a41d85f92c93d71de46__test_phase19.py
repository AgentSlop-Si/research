"""Independent full-DFT, mutation, and all-length tests for Phase19."""
import unittest
import random
from math import gcd
from blind_discovery import blind_one_defect, DiscoveryStats, RecurrenceGreen
from annihilator_engine import dense_from_shift_defects,shift_binomial_apply,far_coprime_shift
from rational_forcing import direct_dft_any

CASES=[(2013265921,31,30),(2013265921,31,60),
       (2013265921,31,128),(2013265921,31,384),
       (998244353,3,7),(998244353,3,17),(998244353,3,119)]

class Phase19Tests(unittest.TestCase):
    def test_completely_unknown_one_defect_full(self):
        for p,g,n in CASES:
            e=RecurrenceGreen(n,p,g)
            deltas={1,n-1,far_coprime_shift(n)}
            for d in deltas:
                if gcd(d,n)!=1:continue
                for location in {0,n//3,n-1}:
                    h=[0]*n;h[location]=13
                    r=dense_from_shift_defects(h,d,2,p)
                    self.assertTrue(all(r))
                    candidate,stats=blind_one_defect(r,p)
                    self.assertIsNotNone(candidate,(n,d,location))
                    self.assertLessEqual(stats.candidate_full_scans,2)
                    dd,a,b,K=candidate
                    self.assertEqual(K,1)
                    self.assertEqual(sum(bool(v) for v in shift_binomial_apply(r,dd,a,b,p)),1)
                    x=e.P.solve(r)
                    got,meta=e.transform_blind_one(x)
                    self.assertEqual(got,direct_dft_any(x,e.omega,p))
                    self.assertEqual(meta['selected'],'blind-one-defect')
                    self.assertEqual(meta['K'],1)
                    self.assertEqual(meta['resonant'],0)
                    self.assertLessEqual(meta['discovery'].candidate_full_scans,2)

    def test_zero_defect_all_character(self):
        for p,g,n in CASES:
            e=RecurrenceGreen(n,p,g)
            r=[pow(e.omega,7*j,p) for j in range(n)]
            candidate,_=blind_one_defect(r,p)
            self.assertIsNotNone(candidate)
            self.assertEqual(candidate[-1],0)
            x=e.P.solve(r)
            got,meta=e.transform_blind_one(x)
            self.assertEqual(got,direct_dft_any(x,e.omega,p))
            self.assertEqual(meta['K'],0)
            self.assertEqual(meta['resonant'],1)

    def test_fallback_generic_and_zero_coordinates(self):
        rng=random.Random(311224)
        for p,g,n in CASES:
            e=RecurrenceGreen(n,p,g)
            for mode in ('random','zeros'):
                x=[rng.randrange(1,p) for _ in range(n)]
                if mode=='zeros':
                    r=e.P.apply(x);r[n//2]=0;x=e.P.solve(r)
                got,meta=e.transform_blind_one(x)
                self.assertEqual(got,direct_dft_any(x,e.omega,p))
                self.assertEqual(meta['selected'],'fallback')

    def test_semi_blind_second_shift_and_dense_singles(self):
        for p,g,n in CASES:
            e=RecurrenceGreen(n,p,g)
            d1,d2=far_coprime_shift(n),n-1
            h=[0]*n;h[n//3]=11
            v=dense_from_shift_defects(h,d2,3,p)
            r=dense_from_shift_defects(v,d1,2,p)
            self.assertTrue(all(r))
            self.assertEqual(sum(bool(q) for q in shift_binomial_apply(r,d1,2,1,p)),n)
            self.assertEqual(sum(bool(q) for q in shift_binomial_apply(r,d2,3,1,p)),n)
            x=e.P.solve(r)
            out,meta=e.transform_semiblind_union(x,[(d1,2)])
            self.assertEqual(out,direct_dft_any(x,e.omega,p))
            self.assertEqual(meta['selected'],'semi-blind-union')
            self.assertEqual(meta['K'],1)
            self.assertEqual(meta['resonant'],0)
            self.assertEqual(meta['unknown_delay'],d2)

    def test_semi_blind_wrong_factor_safe_fallback(self):
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        d1,d2=far_coprime_shift(n),n-1
        h=[0]*n;h[5]=7
        r=dense_from_shift_defects(dense_from_shift_defects(h,d2,3,p),d1,2,p)
        x=e.P.solve(r)
        got,meta=e.transform_semiblind_union(x,[(d1,5)])
        self.assertEqual(got,direct_dft_any(x,e.omega,p))
        self.assertEqual(meta['selected'],'fallback')

    def test_no_oracle_arbitrary_delays(self):
        rng=random.Random(837)
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        for d in range(1,n):
            if gcd(n,d)!=1:continue
            h=[0]*n;h[rng.randrange(n)]=rng.randrange(1,p)
            alpha=rng.randrange(2,p-1)
            if pow(alpha,n,p)==1:continue
            r=dense_from_shift_defects(h,d,alpha,p)
            candidate,ds=blind_one_defect(r,p)
            self.assertIsNotNone(candidate,(d,alpha))
            self.assertLessEqual(ds.candidate_full_scans,2)
            self.assertEqual(candidate[-1],1)

    def test_projective_ratios_cover_invertible_and_noninvertible_counts(self):
        p=2013265921
        for n in (12,30,128,384):
            for d in range(1,n):
                if gcd(d,n)!=1:continue
                h=[0]*n;h[n//2]=5
                r=dense_from_shift_defects(h,d,2,p)
                found,ds=blind_one_defect(r,p)
                self.assertEqual(found[-1],1)
                self.assertLessEqual(ds.candidate_full_scans,2)

    def test_adversarial_two_mode_false_signatures(self):
        rng=random.Random(20261010)
        p,g,n=2013265921,31,60
        e=RecurrenceGreen(n,p,g)
        # Alternating linear exponentials, plateaux and random perturbations.
        inputs=[]
        inputs.append([2 if j%2 else 1 for j in range(n)])
        inputs.append([pow(2,j,p) if j<n//2 else pow(3,j,p) for j in range(n)])
        for _ in range(15):inputs.append([rng.randrange(1,p) for _ in range(n)])
        for r in inputs:
            picked,ds=blind_one_defect(r,p)
            if picked is not None:
                d,a,b,K=picked
                self.assertLessEqual(K,1)
                self.assertLessEqual(sum(bool(z) for z in shift_binomial_apply(r,d,a,b,p)),1)
            self.assertLessEqual(ds.candidate_full_scans,2)
            x=e.P.solve(r)
            y,meta=e.transform_blind_one(x)
            self.assertEqual(y,direct_dft_any(x,e.omega,p))

if __name__=='__main__':unittest.main(verbosity=2)

class BoundedDefectTests(unittest.TestCase):
    def test_blind_two_defects_unknown_long_shift(self):
        from blind_discovery import blind_bounded_defects
        rng=random.Random(1919)
        for p,g,n in CASES:
            if n<7:continue
            e=RecurrenceGreen(n,p,g)
            d=far_coprime_shift(n)
            for trial in range(3):
                h=[0]*n
                for j in rng.sample(range(n),2):h[j]=rng.randrange(1,100)
                r=dense_from_shift_defects(h,d,2,p)
                self.assertTrue(all(r))
                found,ds=blind_bounded_defects(r,p,2)
                self.assertIsNotNone(found,(n,trial))
                self.assertEqual(found[-1],2)
                dd,a,b,K=found
                self.assertEqual(sum(bool(v) for v in shift_binomial_apply(r,dd,a,b,p)),2)
                x=e.P.solve(r)
                y,meta=e.transform_blind_bounded(x,2)
                self.assertEqual(y,direct_dft_any(x,e.omega,p))
                self.assertEqual(meta['selected'],'blind-bounded-defects')
                self.assertEqual(meta['K'],2)

    def test_resonant_cross_wrap_collision_safe_fallback(self):
        from blind_discovery import blind_bounded_defects
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        d=far_coprime_shift(n)
        alpha=pow(e.omega,9,p)
        self.assertEqual(pow(alpha,n,p),1)
        r=[0]*n
        for t in range(n):
            r[(t*d)%n]=pow(alpha,t,p)*(3 if t<17 else 5)%p
        self.assertTrue(all(r))
        self.assertEqual(sum(bool(v) for v in shift_binomial_apply(r,d,alpha,1,p)),2)
        found,ds=blind_bounded_defects(r,p,2)
        self.assertIsNone(found,'must preserve known wrap-collision counterexample')
        x=e.P.solve(r)
        y,meta=e.transform_blind_bounded(x,2)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(meta['selected'],'fallback')

    def test_generalized_input_generic_exact(self):
        rng=random.Random(20261011)
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        for _ in range(15):
            x=[rng.randrange(1,p) for j in range(n)]
            y,meta=e.transform_blind_bounded(x,2)
            self.assertEqual(y,direct_dft_any(x,e.omega,p))
            self.assertEqual(meta['selected'],'fallback')

    def test_reduced_two_defects_with_missing_zeros(self):
        p,g,n=2013265921,31,60
        e=RecurrenceGreen(n,p,g)
        r=[0]*n
        r[0]=3;r[3]=4;r[25]=7
        candidate,ds=__import__('blind_discovery').blind_bounded_defects(r,p,2)
        self.assertIsNone(candidate)
        x=e.P.solve(r)
        y,meta=e.transform_blind_bounded(x,2)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(meta['selected'],'fallback')
