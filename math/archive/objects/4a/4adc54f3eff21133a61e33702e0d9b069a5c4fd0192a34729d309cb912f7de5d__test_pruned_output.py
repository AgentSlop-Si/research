import unittest
import numpy as np
from pruned_output import first_k_dft, stream_basis_first_k, BandDFTPlan

class TestPrunedOutput(unittest.TestCase):
    def test_first_k_matches_fft(self):
        rng=np.random.default_rng(87)
        for n in (8,32,128,1024):
            x=rng.standard_normal(n)+1j*rng.standard_normal(n)
            for k in (1,2,4,8):
                if k<=n and n%k==0:
                    self.assertTrue(np.allclose(first_k_dft(x,k),np.fft.fft(x)[:k],rtol=2e-11,atol=2e-9))
    def test_band_matches_fft(self):
        rng=np.random.default_rng(44); n=256; x=rng.standard_normal(n)+1j*rng.standard_normal(n)
        for start,k in [(3,8),(64,16),(219,32)]:
            # Last case stays within the non-wrapping band.
            got=BandDFTPlan(n,k,start).execute(x)
            self.assertTrue(np.allclose(got,np.fft.fft(x)[start:start+k],rtol=2e-11,atol=2e-9))

    def test_stream_projection(self):
        rng=np.random.default_rng(4); b=rng.standard_normal((5,128))
        got=stream_basis_first_k((row for row in b),8)
        self.assertTrue(np.allclose(got,np.fft.fft(b,axis=1)[:,:8]))
if __name__=='__main__':unittest.main()
