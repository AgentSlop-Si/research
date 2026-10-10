import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import numpy as np
from adapter import HybridAdaptiveFFT

class TestAdapter(unittest.TestCase):
    def test_sparse_delta_with_existing_engine(self):
        rng=np.random.default_rng(992)
        engine=HybridAdaptiveFFT(mode='plain')
        for n in [8,64,1024]:
            base=rng.standard_normal(n)
            f=engine.fft(base)
            updates=[(1,0.2),(n-1,0.4)]
            out,_=engine.fft_from_delta(f,updates)
            altered=base.copy();altered[1]+=0.2;altered[-1]+=0.4
            self.assertTrue(np.allclose(out,np.fft.fft(altered),atol=3e-10))
            self.assertEqual(engine.last_strategy,'metadata_sparse_factorized')
            compact=engine.rfft(base)
            out2,_=engine.rfft_from_delta(compact,n,updates)
            self.assertTrue(np.allclose(out2,np.fft.rfft(altered),atol=3e-10))

if __name__=='__main__':unittest.main()
