"""Independent exact finite-field tests for Hero #1 Phase18."""
import random
import unittest
from math import gcd
from annihilator_engine import (
    RecurrenceGreen,Work, shift_polynomial_apply,graph_polynomial_apply,
    decode_annihilator,decode_binomial,decode_graph_polynomial,
    dense_from_shift_defects, majority_long_shift,graph_bm_candidate,
    far_coprime_shift, batch_inverse_nonzero, count_resonant_binomial,
    shift_binomial_apply, decode_factor_union,
)
from rational_forcing import direct_dft_any, general_root

CASES=[(2013265921,31,30),(2013265921,31,60),(2013265921,31,128),
       (2013265921,31,384),(998244353,3,7),(998244353,3,17),
       (998244353,3,119)]


class Phase18Tests(unittest.TestCase):
    def check_fft(self,e,x,actual):
        self.assertEqual(actual,direct_dft_any(x,e.omega,e.p))

    def test_geometric_dense_degree_one(self):
        for p,g,n in CASES:
            with self.subTest(n=n,p=p):
                e=RecurrenceGreen(n,p,g)
                r=[pow(2,j,p) for j in range(n)]
                self.assertEqual(len([v for v in r if v]),n)
                x=e.P.solve(r)
                actual,meta=e.transform_recurrence(x)
                self.check_fft(e,x,actual)
                self.assertEqual(meta['K'],1)
                self.assertEqual(meta['selected'],'majority')
                self.assertEqual(meta['delay'],1)
                self.assertEqual(meta['resonant'],0)

    def test_two_exponentials_prefix_BM(self):
        for p,g,n in CASES:
            with self.subTest(n=n,p=p):
                e=RecurrenceGreen(n,p,g)
                r=[(pow(2,j,p)+pow(3,j,p))%p for j in range(n)]
                x=e.P.solve(r)
                y,meta=e.transform_recurrence(x)
                self.check_fft(e,x,y)
                self.assertEqual(meta['selected'],'graph-bm')
                self.assertEqual(meta['K'],2)
                self.assertEqual(meta['degree_on_graph'],2)
                self.assertEqual(meta['delay'],1)

    def test_long_cycle_degree_one_three_defects(self):
        for p,g,n in CASES:
            if n<15:continue
            with self.subTest(n=n,p=p):
                e=RecurrenceGreen(n,p,g)
                delay=far_coprime_shift(n)
                self.assertEqual(gcd(n,delay),1)
                h=[0]*n
                for j,v in ((0,1),(n//3,2),(2*n//3,3)):h[j]=v
                r=dense_from_shift_defects(h,delay,2,p)
                self.assertTrue(all(r))
                x=e.P.solve(r)
                self.assertTrue(all(x))
                y,meta=e.transform_recurrence(x)
                self.check_fft(e,x,y)
                self.assertEqual(meta['selected'],'majority')
                self.assertEqual(meta['K'],3)
                self.assertEqual(meta['delay'],delay)

    def test_long_cycle_degree_two(self):
        for p,g,n in CASES:
            if n<17:continue
            with self.subTest(n=n,p=p):
                e=RecurrenceGreen(n,p,g)
                delay=far_coprime_shift(n)
                r=[0]*n
                for t in range(n):
                    r[(t*delay)%n]=(pow(2,t,p)+pow(3,t,p))%p
                q=graph_bm_candidate(r,delay,3,p)
                self.assertEqual(q,[1,(-5)%p,6])
                self.assertEqual(sum(bool(z) for z in graph_polynomial_apply(r,delay,q,p)),2)
                x=e.P.solve(r)
                y,meta=e.transform_recurrence(x)
                self.check_fft(e,x,y)
                self.assertEqual(meta['selected'],'graph-bm')
                self.assertEqual(meta['degree_on_graph'],2)
                self.assertEqual(meta['K'],2)
                self.assertEqual(meta['delay'],delay)

    def test_long_cycle_degree_two_injected_defect(self):
        p,g,n=2013265921,31,384
        e=RecurrenceGreen(n,p,g)
        delay=far_coprime_shift(n)
        u=[2,5]+[0]*(n-2)
        for t in range(2,n):u[t]=(5*u[t-1]-6*u[t-2]+(29 if t==n//2 else 0))%p
        r=[0]*n
        for t,jval in enumerate(u):r[(t*delay)%n]=jval
        x=e.P.solve(r)
        y,meta=e.transform_recurrence(x)
        self.check_fft(e,x,y)
        self.assertEqual(meta['selected'],'graph-bm')
        self.assertEqual(meta['K'],3)
        self.assertEqual(meta['delay'],delay)

    def test_singular_degree_one_repair(self):
        for p,g,n in CASES:
            e=RecurrenceGreen(n,p,g)
            alpha=pow(e.omega,-min(n-1,3),p)
            r=[pow(alpha,j,p) for j in range(n)]
            self.assertEqual(count_resonant_binomial(n,1,alpha,1,p),1)
            x=e.P.solve(r)
            actual,meta=e.transform_recurrence(x)
            self.check_fft(e,x,actual)
            self.assertEqual(meta['K'],0)
            self.assertEqual(meta['resonant'],1)
            self.assertEqual(meta['work'].repaired,1)

    def test_singular_degree_two_repair(self):
        for p,g,n in CASES:
            e=RecurrenceGreen(n,p,g)
            alpha=pow(e.omega,-2,p)
            r=[(pow(alpha,j,p)+pow(2,j,p))%p for j in range(n)]
            x=e.P.solve(r)
            y,meta=e.transform_recurrence(x)
            self.check_fft(e,x,y)
            self.assertEqual(meta['K'],2)
            self.assertEqual(meta['resonant'],1)
            self.assertEqual(meta['work'].repaired,1)

    def test_non_coprime_cycles_and_singularity_count(self):
        p,g,n=2013265921,31,64
        e=RecurrenceGreen(n,p,g)
        delay=n//2
        self.assertEqual(count_resonant_binomial(n,delay,1,1,p),n//2)
        r=[1]*n
        z,meta=decode_graph_polynomial(r,delay,[1,-1],e)
        self.assertEqual(z,direct_dft_any(r,e.omega,p))
        self.assertEqual(meta['resonant'],n//2)
        self.assertEqual(meta['work'].repaired,n//2)
        self.assertEqual(count_resonant_binomial(n,delay,2,1,p),0)
        h=[0]*n
        for i in range(n//2):h[i]=i+1
        r2=dense_from_shift_defects(h,delay,2,p)
        self.assertEqual(graph_polynomial_apply(r2,delay,[1,-2],p),h)
        self.assertTrue(all(r2))
        self.assertEqual(sum(bool(v) for v in h),gcd(n,delay))

    def test_generic_adversarial_fallback(self):
        rand=random.Random(11447)
        for p,g,n in CASES:
            e=RecurrenceGreen(n,p,g)
            for _ in range(2):
                x=[rand.randrange(1,p) for _ in range(n)]
                y,meta=e.transform_recurrence(x)
                self.check_fft(e,x,y)
                self.assertEqual(meta['selected'],'fallback')

    def test_mutation_defect_certificate(self):
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        delta=far_coprime_shift(n)
        h=[0]*n;h[0]=1;h[n//3]=2
        r=dense_from_shift_defects(h,delta,2,p)
        correct=graph_polynomial_apply(r,delta,[1,-2],p)
        wrong=graph_polynomial_apply(r,delta,[1,-3],p)
        self.assertEqual(sum(bool(v) for v in correct),2)
        self.assertGreater(sum(bool(v) for v in wrong),n//2)
        y,_=decode_graph_polynomial(r,delta,[1,-2],e)
        self.assertEqual(y,direct_dft_any(r,e.omega,p))

    def test_exhaustive_small_random_field(self):
        randomgen=random.Random(158)
        for p,g,n in [(2013265921,31,5),(998244353,3,7),(998244353,3,17)]:
            e=RecurrenceGreen(n,p,g)
            for _ in range(20):
                r=[randomgen.randrange(p) for _ in range(n)]
                x=e.P.solve(r)
                y,meta=e.transform_recurrence(x,max_degree=2)
                self.check_fft(e,x,y)
                self.assertLessEqual(meta['K'],n)

    def test_union_two_long_graph_filters_sparse_only_jointly(self):
        for p,g,n in CASES:
            if n<17:continue
            with self.subTest(n=n,p=p):
                e=RecurrenceGreen(n,p,g)
                delta1,delta2=far_coprime_shift(n),n-1
                h=[0]*n
                for j,v in [(0,1),(n//3,2),(n//2,3)]:h[j]=v
                intermediate=dense_from_shift_defects(h,delta1,2,p)
                r=dense_from_shift_defects(intermediate,delta2,3,p)
                x=e.P.solve(r)
                self.assertTrue(all(r) and all(x))
                # Neither single operator produces ANY zero defect in cases.
                a=shift_binomial_apply(r,delta1,2,1,p)
                b=shift_binomial_apply(r,delta2,3,1,p)
                self.assertEqual(sum(bool(z) for z in a),n)
                self.assertEqual(sum(bool(z) for z in b),n)
                y,meta=e.transform_known_factors(x,[(delta1,2),(delta2,3)])
                self.check_fft(e,x,y)
                self.assertEqual(meta['selected'],'known-factor-union')
                self.assertEqual(meta['K'],3)
                self.assertEqual(meta['resonant'],0)
                self.assertEqual(meta['factor_count'],2)

    def test_union_generic_fallback_and_singular_repair(self):
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        rng=random.Random(4118)
        x=[rng.randrange(1,p) for _ in range(n)]
        y,meta=e.transform_known_factors(x,[(63,2),(127,3)])
        self.assertEqual(meta['selected'],'full-fallback')
        self.check_fft(e,x,y)
        # Direct union decoder must account for a resonant factor.
        root=pow(e.omega,-2,p)
        r=[pow(root,j,p) for j in range(n)]
        y2,detail=decode_factor_union(r,[(1,root)],e)
        self.assertEqual(y2,direct_dft_any(r,e.omega,p))
        self.assertEqual(detail['resonant'],1)
        self.assertEqual(detail['work'].repaired,1)

    def test_batch_inverse_single_operation(self):
        p=2013265921
        rand=random.Random(2026)
        xs=[rand.randrange(1,p) for _ in range(200)]
        co=Work()
        vals=batch_inverse_nonzero(xs,p,co)
        self.assertEqual(co.inversions,1)
        self.assertEqual([x*y%p for x,y in zip(xs,vals)],[1]*len(xs))

    def test_degree_zero_identity_and_input_checks(self):
        p=2013265921
        e=RecurrenceGreen(30,p,31)
        r=[(j*j+2)%p for j in range(e.n)]
        actual,meta=decode_graph_polynomial(r,1,[1],e,forcing_method='bluestein')
        self.assertEqual(actual,direct_dft_any(r,e.omega,p))
        self.assertEqual(meta['resonant'],0)
        with self.assertRaises(ValueError):decode_graph_polynomial(r,1,[0,1],e)
        with self.assertRaises(ValueError):dense_from_shift_defects([1]*8,4,1,p)

if __name__=='__main__':unittest.main()
