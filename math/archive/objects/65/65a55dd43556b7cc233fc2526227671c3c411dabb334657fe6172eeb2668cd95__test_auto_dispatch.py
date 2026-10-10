import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import numpy as np
from algebra_fft import AlgebraFFT
from auto_dispatch import plan_auto

class DispatchTests(unittest.TestCase):
    def test_small_batch_never_pays_new_jit(self):
        rng=np.random.default_rng(301)
        n=48; eng=AlgebraFFT(n)
        a=eng.signal(rng.standard_normal(n));b=eng.signal(rng.standard_normal(n))
        p=eng.prepare(eng.add(eng.mul(a,a),b),a)
        ans=plan_auto(p,expected_versions=1,min_unseen_jit_versions=1000000)
        self.assertEqual(ans.mode,'numpy')
        np.testing.assert_allclose(ans.single(5,.03),p.single(5,.03))
    def test_invalid_batch(self):
        rng=np.random.default_rng(22)
        n=32;e=AlgebraFFT(n)
        a=e.signal(rng.standard_normal(n));p=e.prepare(e.mul(a,a),a)
        with self.assertRaises(ValueError):plan_auto(p,expected_versions=0)
        low=plan_auto(p,expected_versions=10000,max_compiled_bytes=1)
        self.assertEqual(low.mode,'numpy')
    def test_calibration_validity_and_partial(self):
        rng=np.random.default_rng(99)
        n=128;e=AlgebraFFT(n)
        a,b,c=[e.signal(rng.normal(size=n)) for _ in range(3)]
        p=e.prepare(e.add(e.mul(a,a,a),e.mul(b,c)),a)
        for inds in (None,[1,4,16,127]):
            plan=plan_auto(p,expected_versions=10000,output_bins=inds,min_unseen_jit_versions=1,samples=2)
            for edit in [(2,.01),(53,-.02)]:
                np.testing.assert_allclose(plan.single(*edit,indices=inds),p.single(*edit,indices=inds),rtol=1e-9,atol=1e-9)
            self.assertIn(plan.mode,('native','numpy'))
if __name__=='__main__':unittest.main()
