import unittest
from math import log2
from complex_check import run,normalized_fft_gate_stages,log2_determinant_magnitude,fourier

class IndependentComplexTests(unittest.TestCase):
    def test_matrix_gate_entropy(self):
        for n in (2,4,8,16,32):
            stages,err=normalized_fft_gate_stages(n)
            self.assertLess(err,1e-10)
            self.assertEqual(len(stages),n.bit_length())
            for stage,h in enumerate(stages):
                self.assertAlmostEqual(h,n*stage,places=8)

    def test_fourier_determinant(self):
        for n in (2,4,8,16,32):
            v=log2_determinant_magnitude(fourier(n))
            self.assertAlmostEqual(v,n*log2(n)/2,places=8)

    def test_complex_audit(self):
        self.assertEqual(len(run((2,4,8))),3)

if __name__=='__main__':unittest.main()
