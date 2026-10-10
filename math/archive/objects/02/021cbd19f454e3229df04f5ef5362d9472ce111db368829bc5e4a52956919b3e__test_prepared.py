import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import unittest
import numpy as np
from prepared_update import PreparedPointEdit

class TestPrepared(unittest.TestCase):
    def test_streaming_point_updates(self):
        rng=np.random.default_rng(37)
        for n in [16,64,1024,4096]:
            x=rng.standard_normal(n)
            loc=n//3
            cache=np.fft.rfft(x)
            updater=PreparedPointEdit(n,loc)
            for d in rng.standard_normal(30):
                x[loc]+=d
                cache=updater.update(cache,d)
                self.assertTrue(np.allclose(cache,np.fft.rfft(x),atol=5e-10))

if __name__=='__main__':unittest.main()
