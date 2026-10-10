"""End-to-end Phase23/24 certificate with mixed-radix no-repeat fallback."""
import unittest,random
from gt3_green import transform_deferred_conjugate_gt3
from gt3_deferred import DeferredGT3,direct_dft
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects

class TestPhase25Green(unittest.TestCase):
    def test_mixed_radix_structured_and_fallback(self):
        rgen=random.Random(25311)
        for n in (24,48,96,192,384,768):
            eng=RecurrenceGreen(n,2013265921,31)
            h=[0]*n;h[4]=7;h[n-9]=11
            r=dense_from_shift_defects(dense_from_shift_defects(h,n//2-3,17,eng.p),n//2+7,29,eng.p)
            xs=[('structured',eng.P.solve(r))]+[('random',[rgen.randrange(eng.p) for _ in range(n)]) for _ in range(2)]
            for kind,x in xs:
                out,meta=transform_deferred_conjugate_gt3(eng,x)
                expected=direct_dft(x,eng.omega,eng.p)
                self.assertEqual(out,expected)
                if kind=='structured':
                    self.assertEqual(meta['selected'],'gt3-certified')
                    self.assertTrue(meta['residual_computed'])
                else:
                    self.assertEqual(meta['selected'],'gt3-fallback')
                    self.assertFalse(meta['residual_computed'])
                    self.assertEqual(meta['fft_graph']['arithmetic'],meta['native_gt3_reference_ops'])

    def test_adversarial_prefix_equal_then_reject(self):
        n=192;p=2013265921
        eng=RecurrenceGreen(n,p,31)
        h=[0]*n;h[4]=7;h[55]=11
        r=dense_from_shift_defects(dense_from_shift_defects(h,43,17,p),61,29,p)
        k0=19
        rbad=[(r[j]+pow(eng.powers[k0],-j,p))%p for j in range(n)]
        x=eng.P.solve(rbad)
        out,meta=transform_deferred_conjugate_gt3(eng,x)
        self.assertEqual(out,direct_dft(x,eng.omega,p))
        self.assertEqual(meta['selected'],'gt3-fallback')
        self.assertGreater(meta['meta'].failed_certificates,0)
        self.assertTrue(meta['residual_computed'])
        self.assertEqual(meta['fft_graph']['arithmetic'],meta['native_gt3_reference_ops'])

if __name__=='__main__':unittest.main()
