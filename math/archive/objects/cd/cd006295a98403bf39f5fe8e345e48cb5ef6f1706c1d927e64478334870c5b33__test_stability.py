from __future__ import annotations
import math
import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

from orbit_stability import (
    is_power_of_two,canonical_representatives,complementary_signal,
    folded_odd_coefficients,theoretical_lipschitz_bound,
    identical_even_spectrum,necessary_odd_representatives,
)
from modular_audit import run_exact_audit

class GeometryTests(unittest.TestCase):
    def test_power_of_two(self):
        self.assertTrue(is_power_of_two(1024))
        self.assertFalse(is_power_of_two(0))
        self.assertFalse(is_power_of_two(12))

    def test_representatives(self):
        self.assertEqual(canonical_representatives(8),(0,1,2,4))
        self.assertEqual(canonical_representatives(64),(0,1,2,4,8,16,32))
        with self.assertRaises(ValueError):canonical_representatives(9)

    def test_family(self):
        for n in (8,16,32):
            m=n//2
            mask=(1<<m)-1
            self.assertEqual(complementary_signal(0,n),(0,)*m+(1,)*m)
            self.assertEqual(complementary_signal(mask,n),(1,)*m+(0,)*m)
            self.assertEqual(folded_odd_coefficients(0,n),(-1,)*m)
            self.assertEqual(folded_odd_coefficients(mask,n),(1,)*m)
        with self.assertRaises(ValueError):complementary_signal(256,8)

    def test_parsed_counts(self):
        self.assertEqual(identical_even_spectrum(16),(8,0,0,0,0,0,0,0))
        self.assertEqual(theoretical_lipschitz_bound(32,1)['M'],255)
        self.assertEqual(theoretical_lipschitz_bound(64,2)['M'],255)

    def test_growth(self):
        ns=(16,32,64,128,256,512,1024)
        exponents=[theoretical_lipschitz_bound(n,1)['exponent_floor'] for n in ns]
        self.assertEqual(exponents,[4,8,16,32,64,128,256])
        self.assertTrue(all(exponents[i+1]>exponents[i] for i in range(len(exponents)-1)))

    def test_monotone_with_more_representatives(self):
        for n in (16,32,64,128):
            b=[theoretical_lipschitz_bound(n,r)['M'] for r in range(1,n//2+1)]
            self.assertEqual(b,sorted(b,reverse=True))

    def test_lipschitz_required_odd_count(self):
        for n in (32,64,128,256,1024):
            for power in (0,1,2):
                L=n**power
                r=necessary_odd_representatives(n,L)
                self.assertLessEqual(theoretical_lipschitz_bound(n,r)['M'],n*L)
                if r>1:self.assertGreater(theoretical_lipschitz_bound(n,r-1)['M'],n*L)

    def test_dimension_count(self):
        for n in (8,16,32,64):
            for r in (1,2):
                if r>n//2:continue
                p=theoretical_lipschitz_bound(n,r)
                if p['M']:
                    self.assertLess(p['M']**(2*r),2**(n//2))

    def test_parseval_witness(self):
        import numpy as np
        rng=random.Random(1)
        for n in (8,16,32,64):
            for _ in range(10):
                u=rng.randrange(1<<(n//2))
                v=rng.randrange(1<<(n//2))
                if u==v:continue
                a=np.array(complementary_signal(u,n))
                b=np.array(complementary_signal(v,n))
                X=np.fft.fft(a-b)
                self.assertLess(np.abs(X[::2]).max(),1e-10)
                self.assertGreaterEqual(np.abs(X).max()+1e-10,math.sqrt(2))

    def test_exact_modular_orbits(self):
        counts=run_exact_audit()
        self.assertEqual(counts['vectors'],112)
        self.assertEqual(counts['odd_orbit_checks'],1680)

    def test_nearest_example_high_precision(self):
        from experiment import closest_pair
        for n in (8,16,32):
            info=closest_pair(n)
            self.assertGreater(info['full_spectrum_gap_max'],1)
            self.assertLess(info['even_spectral_difference_max'],1e-9)
            self.assertNotEqual(info['mask_u'],info['mask_v'])
            self.assertTrue(any(info['cyclotomic_integer_difference_coeffs']))
            self.assertLess(float(info['one_rep_gap_high_precision']),1)

if __name__=='__main__':unittest.main()

class JointOrbitControls(unittest.TestCase):
    def test_conjugate_positive_control(self):
        import numpy as np
        for n in (8,16,32,64):
            m=n//2
            # Compute one of each conjugate pair of odd frequencies.
            measured=tuple(range(1,m,2))
            self.assertEqual(len(measured),n//4)
            for mask in (0,1,(1<<m)-1,(1<<m)//3):
                x=np.array(complementary_signal(mask,n))
                X=np.fft.fft(x)
                reconstructed=np.zeros(n,dtype=complex)
                reconstructed[0]=m
                for k in measured:
                    reconstructed[k]=X[k]
                    reconstructed[n-k]=np.conj(X[k])
                self.assertLess(abs(reconstructed-X).max(),1e-10)

    def test_finite_joint_measurement_controls(self):
        from joint_measurement_audit import run
        data=run()
        self.assertEqual(len(data),5)
        self.assertGreater(float(data[3]['ratio']),float(data[4]['ratio']))
        self.assertAlmostEqual(float(data[2]['ratio']),1.0,places=10)
