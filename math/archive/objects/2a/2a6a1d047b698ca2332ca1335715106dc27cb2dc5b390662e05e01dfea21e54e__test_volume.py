import math
import unittest
from volume_gate import (entropy,block_fourier_layer,block_volume_toll,
    gt3_gate_tolls,volume_lower_bound_fixed_arity, Fourier_target_volume,
    Fourier_target_entropy, shear_identity_residue, required_max_entry_for_gate_budget)

class VolumeGate(unittest.TestCase):
    def test_exact_lifting(self):
        self.assertEqual(shear_identity_residue()[1][1],2013265920)
    def test_entropy_one_layer_saturation(self):
        for n in (8,12,24):
            for b in (2,3,4,6):
                if n%b:continue
                A=block_fourier_layer(n,b)
                self.assertAlmostEqual(entropy(A),n*math.log2(b),places=9)
                self.assertAlmostEqual((n//b)*b*math.log2(b),n*math.log2(b),places=9)
    def test_gt3_volume_entropic_saturation(self):
        for G in (2,4,8,16,32,64,512,4096):
            summary=gt3_gate_tolls(G)
            self.assertAlmostEqual(summary['volume_gate_capacity'],summary['volume_dft_required'],places=8)
            self.assertAlmostEqual(summary['entropy_gate_capacity'],summary['entropy_dft_required'],places=8)
    def test_constant_bounded_gate_lower_bound(self):
        for n in (8,16,32,64,256):
            # b=2,C=1: saturation by radix2 is a model-specific theorem.
            self.assertAlmostEqual(volume_lower_bound_fixed_arity(n,2,1),n*math.log2(n)/2,places=9)
            for B in (3,4,8):
                self.assertTrue(volume_lower_bound_fixed_arity(n,B,1)>0)
    def test_coefficient_growth_for_linear_gate_budget(self):
        for n in (16,256,4096,65536):
            c=required_max_entry_for_gate_budget(n,n,2)
            self.assertAlmostEqual(c,max(1,n**0.25/(2**0.5)))
            c2=required_max_entry_for_gate_budget(n,2*n,2)
            self.assertGreaterEqual(c,c2)
    def test_bound_ceiling_monotonic(self):
        for n in (16,64,256):
            last=1e100
            for B in (2,4,8,16):
                gate_lb=volume_lower_bound_fixed_arity(n,B,1)
                self.assertLess(gate_lb,last)
                last=gate_lb

if __name__=='__main__': unittest.main()
