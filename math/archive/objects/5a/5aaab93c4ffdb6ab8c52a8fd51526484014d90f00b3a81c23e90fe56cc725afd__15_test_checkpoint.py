#!/usr/bin/env python3
from __future__ import annotations

import math
import unittest
from fractions import Fraction

import numpy as np

import prototype as p
import composite_cycle_core as core


class DivisorSpectrumV13Tests(unittest.TestCase):
    def setUp(self) -> None:
        self.rng = np.random.default_rng(20261010)

    def test_factorization_and_divisors(self) -> None:
        for n, expected in [
            (1, {}), (2, {2: 1}), (60, {2: 2, 3: 1, 5: 1}),
            (1001, {7: 1, 11: 1, 13: 1}),
        ]:
            self.assertEqual(p.factor_trial(n), expected)
        self.assertEqual(p.all_divisors(60), [1,2,3,4,5,6,10,12,15,20,30,60])

    def test_totient(self) -> None:
        values = {1:1, 2:1, 3:2, 4:2, 6:2, 12:4, 35:24, 49:42, 77:60}
        for n, expected in values.items():
            self.assertEqual(p.euler_phi(n), expected)

    def test_divisor_sum_never_exceeds_coarse_bound(self) -> None:
        for n in range(4, 250):
            for m in range(2, math.isqrt(n) + 1):
                if n % m == 0:
                    self.assertLessEqual(
                        p.direct_divisor_variance_factor(n,m),
                        p.coarse_composite_variance_factor(n,m),
                    )

    def test_least_prime_factor_closed_form(self) -> None:
        for n in [15,21,35,49,77,121,143,221,437,899,10403]:
            lp = p.least_prime_factor(n)
            self.assertLess(lp, n)
            self.assertEqual(
                p.direct_divisor_variance_factor(n,lp),
                p.least_factor_variance_factor(n),
            )

    def test_executor_matches_materialized_projected_fft(self) -> None:
        for n,m in [(12,3),(30,5),(35,5),(77,7),(143,11),(840,10)]:
            for _ in range(3):
                x=self.rng.normal(size=n)+1j*self.rng.normal(size=n)
                state=core.draw_state(n,self.rng)
                got=p.direct_composite_row(x,m,state)
                ref=core.direct_row_estimate(x,m,state)
                self.assertLess(np.max(np.abs(got-ref)),2e-10)

    def test_analytic_covariance_matches_exhaustive(self) -> None:
        for n,m in [(12,3),(18,3),(30,5),(35,5),(49,7)]:
            actual=p.exhaustive_covariance_matrix(n,m)
            formula=p.analytic_covariance_matrix(n,m)
            err=min(np.max(np.abs(actual-formula)),np.max(np.abs(actual-formula.conj())))
            self.assertLess(err,2e-11)

    def test_sharp_bound_controls_covariance_norm(self) -> None:
        for n,m in [(12,3),(18,3),(30,5),(35,5),(49,7),(77,7)]:
            q=p.analytic_covariance_matrix(n,m)
            norm=float(np.linalg.eigvalsh((q+q.conj().T)/2)[-1])
            bound=float(p.direct_divisor_variance_factor(n,m))
            self.assertLessEqual(norm,bound*(1+1e-10))

    def test_unbiasedness_by_full_state_enumeration(self) -> None:
        for n,m in [(12,3),(18,3),(35,5)]:
            x=self.rng.normal(size=n)+1j*self.rng.normal(size=n)
            rows=[]
            for a in range(1,n):
                if math.gcd(a,n)!=1:
                    continue
                for beta in range(n):
                    rows.append(p.direct_composite_row(x,m,core.ChirpState(a,beta)))
            mean=np.mean(np.asarray(rows),axis=0)
            self.assertLess(np.max(np.abs(mean-p.normalized_dft(x))),3e-11)

    def test_semiprime_work_is_linear_for_polynomial_factors(self) -> None:
        # p and q grow together; W/N remains bounded while W/(N log N) falls.
        pairs=[(17,19),(29,31),(101,103),(211,223),(401,409)]
        normalized=[]
        ratios=[]
        for a,b in pairs:
            n=a*b
            w=p.direct_composite_work_proxy(n,a)
            normalized.append(w/n)
            ratios.append(w/(n*math.log2(n)))
        self.assertLess(max(normalized),12.0)
        self.assertLess(ratios[-1],ratios[0])

    def test_balanced_semiprime_variance_scale(self) -> None:
        for a,b in [(17,19),(29,31),(101,103),(211,223)]:
            n=a*b
            v=float(p.least_factor_variance_factor(n))
            self.assertAlmostEqual(v,2.0/(b-1),places=14)
            self.assertLess(v,3.0/math.sqrt(n))

    def test_median_failure_bound_monotone_in_rows(self) -> None:
        n=101*103
        v=float(p.least_factor_variance_factor(n))
        tol=n**(-0.1)
        bounds=[p.median_union_failure_bound(n,r,v,tol) for r in [3,5,9,17,25]]
        for a,b in zip(bounds,bounds[1:]):
            self.assertLessEqual(b,a)

    def test_planner_selects_direct_for_balanced_semiprime(self) -> None:
        chosen,_=p.choose_adaptive_plan(101*103,rows=9,tolerance=(101*103)**(-0.2))
        self.assertEqual(chosen.method,'direct_composite')
        self.assertEqual(chosen.m,101)

    def test_planner_retains_bessel_for_prime_rough_length(self) -> None:
        # 2^20-3 is prime; no nontrivial direct divisor exists and offset
        # classes are huge, so the all-length Bessel fallback survives.
        n=(1<<20)-3
        chosen,_=p.choose_adaptive_plan(n,rows=9,tolerance=n**(-0.2))
        self.assertEqual(chosen.method,'bessel_rank')

    def test_direct_robust_reproducible(self) -> None:
        n,m=143,11
        x=np.exp(2j*np.pi*self.rng.random(n))
        got1=p.direct_composite_robust(x,m,9,12345)
        got2=p.direct_composite_robust(x,m,9,12345)
        self.assertTrue(np.array_equal(got1,got2))
        radius=4*math.sqrt(float(p.direct_divisor_variance_factor(n,m)))*np.linalg.norm(x)
        self.assertLess(np.max(np.abs(got1-p.normalized_dft(x))),radius)

    def test_candidate_execution_direct(self) -> None:
        n=35
        chosen,_=p.choose_adaptive_plan(n,rows=5,tolerance=0.8)
        # For this loose finite-size target, direct should be available.
        direct=min(p.direct_candidates(n,5,0.8),key=lambda c:c.work_proxy)
        x=self.rng.normal(size=n)+1j*self.rng.normal(size=n)
        got=p.execute_candidate(x,direct,seed=7)
        self.assertEqual(got.shape,(n,))
        self.assertTrue(np.all(np.isfinite(got)))


if __name__=='__main__':
    unittest.main(verbosity=2)
