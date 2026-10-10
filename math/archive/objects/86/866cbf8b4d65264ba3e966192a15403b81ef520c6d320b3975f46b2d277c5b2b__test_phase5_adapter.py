import unittest
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy import fft
from cost_aware_fft import RelationFFT
from persistent_chain import ChainEngine

class AdapterTest(unittest.TestCase):
    def test_single_base_reuse_no_fft(self):
        n=64
        upstream=RelationFFT()
        base=upstream.register(np.arange(n,dtype=float))
        branch=base.shift(4).edit(7,1.25)
        engine=ChainEngine()
        chain=engine.from_phase5([base, branch])
        self.assertEqual(engine.stats['imported_phase5_bases'],1)
        self.assertEqual(engine.stats['seed_ffts'],0)
        expected=fft.irfft(fft.rfft(base.signal())*fft.rfft(branch.signal()),n=n)
        np.testing.assert_allclose(chain.dense(),expected,atol=1e-7)
        np.testing.assert_allclose(chain.frequencies([0,3,17]),fft.fft(expected)[[0,3,17]],atol=1e-7)

    def test_multiple_basis_fallback(self):
        n=32
        upstream=RelationFFT()
        a=upstream.register(np.sin(np.arange(n)))
        b=upstream.register(np.cos(np.arange(n)))
        # Phase 5 add linear representations via operator if present;
        # here construct combined state from internal documented terms.
        composite=a.fork()
        composite.terms.update(b.terms)
        engine=ChainEngine()
        v=engine.from_phase5([composite,a])
        self.assertEqual(engine.stats['materialized_phase5_states'],1)
        expected=fft.irfft(fft.rfft(composite.signal())*fft.rfft(a.signal()),n=n)
        np.testing.assert_allclose(v.dense(),expected,atol=1e-8)

if __name__=='__main__':unittest.main()
