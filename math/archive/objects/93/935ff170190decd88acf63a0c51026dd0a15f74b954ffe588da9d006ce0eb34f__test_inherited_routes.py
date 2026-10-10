#!/usr/bin/env python3
from __future__ import annotations

import math
import unittest
import numpy as np

import prototype as p
import offset_class_core as oc
import unit_step_core as uc
import v11_fused_reference as bc


class InheritedRouteRegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.rng=np.random.default_rng(1302026)

    def test_offset_exact_modulation_identity(self) -> None:
        for n,prime in [(12,2),(18,3),(35,5)]:
            q=oc.next_prime_power(n,prime)
            x=self.rng.normal(size=n)+1j*self.rng.normal(size=n)
            target=p.normalized_dft(x)
            selected,_,_=oc.exact_nearest_grid_map(n,q)
            for num,targets in oc.offset_classes(n,q).items():
                padded=oc.phase_modulated_padded_input(x,q,num)
                lifted=math.sqrt(q/n)*oc.normalized_dft(padded)[selected[targets]]
                self.assertLess(np.max(np.abs(lifted-target[targets])),3e-12)

    def test_offset_row_unbiased_small(self) -> None:
        n,prime=12,2
        q=oc.next_prime_power(n,prime)
        block=oc.choose_prime_power_block(q,prime)
        x=self.rng.normal(size=n)+1j*self.rng.normal(size=n)
        values=[]
        for a in range(1,q):
            if math.gcd(a,q)!=1:continue
            for beta in range(q):
                values.append(oc.offset_class_row(x,prime,uc.ChirpState(a,beta),block))
        self.assertLess(np.max(np.abs(np.mean(values,axis=0)-p.normalized_dft(x))),4e-12)

    def test_bessel_streamed_matches_materialized_small(self) -> None:
        n=63
        x=self.rng.normal(size=n)+1j*self.rng.normal(size=n)
        q=bc.next_power_of_two(n)
        block=bc.choose_dyadic_block(q)
        state=uc.draw_state(q,self.rng)
        rank=8
        reference=bc.reference_bessel_chirp_row(x,rank,block,state)
        streamed=bc.streamed_bessel_chirp_row(x,rank,block,state)
        self.assertLess(np.max(np.abs(reference-streamed)),3e-11)

    def test_bessel_fused_error_below_certified_bound(self) -> None:
        n=63
        x=self.rng.normal(size=n)+1j*self.rng.normal(size=n)
        q=bc.next_power_of_two(n)
        block=bc.choose_dyadic_block(q)
        state=uc.draw_state(q,self.rng)
        rank=8
        got=bc.fused_addition_bessel_chirp_row(x,rank,block,state,halfwidth=0)
        center=bc.exact_lift_with_addition_fusion(x,rank,block,halfwidth=0)
        # Randomized row is not close to the center deterministically; just
        # verify finite execution and the deterministic fused center bound.
        self.assertTrue(np.all(np.isfinite(got)))
        target=p.normalized_dft(x)
        deterministic=np.max(np.abs(center-target))
        bound=bc.fused_deterministic_error_bound(x,rank,block,0)
        self.assertLessEqual(deterministic,bound*(1+1e-9))

    def test_scan_fusion_rank_gate_survives(self) -> None:
        for n,r in [(127,8),(255,10)]:
            cert=oc.scan_fusion_rank_certificate(n,r)
            self.assertEqual(cert['exact_chebyshev_rank'],r)


if __name__=='__main__':
    unittest.main(verbosity=2)
