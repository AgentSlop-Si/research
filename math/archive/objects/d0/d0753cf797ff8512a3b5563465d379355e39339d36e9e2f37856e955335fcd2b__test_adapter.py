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

class TestLazyAdapter(unittest.TestCase):
    def test_lazy_adapter_surfaces(self):
        rng=np.random.default_rng(993);n=128
        x=rng.standard_normal(n)+1j*rng.standard_normal(n)
        engine=HybridAdaptiveFFT(mode='plain');base=np.fft.fft(x)
        s=engine.lazy_spectrum(base);s.add_edit(3,1.5);x[3]+=1.5
        self.assertTrue(np.allclose(s.bins([0,4,77]),np.fft.fft(x)[[0,4,77]]))
        b=engine.buffered_spectrum(base,flush_threshold=2);b.add_edit(1,1);b.add_edit(2,2)
        self.assertEqual(b.flush_count,1)
        v=engine.prepared_bin_view(base,[1,2],[0,5]);v.add_edit(1,1)
        xx=x.copy(); # x already differs at 3; view is from original base, so use independent truth
        original=np.fft.ifft(base); original[1]+=1
        self.assertTrue(np.allclose(v.values(),np.fft.fft(original)[[0,5]],atol=2e-10))
