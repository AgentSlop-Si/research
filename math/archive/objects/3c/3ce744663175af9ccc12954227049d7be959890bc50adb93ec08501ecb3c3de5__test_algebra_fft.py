import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import numpy as np
from scipy import fft
from algebra_fft import AlgebraFFT, DegreeExceeded


class AlgebraTests(unittest.TestCase):
    def setUp(self):
        self.n=64
        self.rng=np.random.default_rng(20261009)
        self.eng=AlgebraFFT(self.n)
        self.xdata=self.rng.normal(scale=.2,size=self.n)
        self.ydata=self.rng.normal(scale=.2,size=self.n)
        self.zdata=self.rng.normal(scale=.2,size=self.n)
        self.x=self.eng.signal(self.xdata,'X')
        self.y=self.eng.signal(self.ydata,'Y')
        self.z=self.eng.signal(self.zdata,'Z')

    def close(self,a,b):
        np.testing.assert_allclose(a,b,rtol=2e-9,atol=2e-9)

    def direct(self,ax,ay,az,which):
        X=fft.rfft(ax);Y=fft.rfft(ay);Z=fft.rfft(az)
        if which==1:
            return fft.irfft(X*Y+Z**2,n=self.n)
        if which==2:
            return fft.irfft(X*X+Y*Z,n=self.n)
        if which==3:
            return fft.irfft(X**3+2*X*Y+Z,n=self.n)

    def test_canonical_associative_commutative(self):
        e=self.eng
        self.assertEqual(e.add(e.add(self.x,self.y),self.z),e.add(self.z,self.x,self.y))
        self.assertEqual(e.mul(e.mul(self.x,self.y),self.z),e.mul(self.z,self.x,self.y))
        self.assertEqual(e.add(self.x,self.x),e.scale(self.x,2))
        self.assertEqual(e.add(self.x,e.scale(self.x,-1)),e.zero)
        self.assertEqual(e.mul(self.y,e.one),self.y)
        self.assertEqual(e.mul(self.y,e.zero),e.zero)
        self.assertEqual(e.scale(e.scale(self.x,3),2),e.scale(self.x,6))

    def test_dag_sharing_and_replacement(self):
        e=self.eng
        mid=e.mul(self.x,self.y)
        root=e.add(mid,e.mul(mid,self.z))
        v=e.edit_version(root,self.x,{3:.4})
        np.testing.assert_allclose(e.evaluate_time(v),fft.irfft(fft.rfft(self.xdata+np.eye(1,self.n,k=3)[0]*.4)*fft.rfft(self.ydata)*(1+fft.rfft(self.zdata)),n=self.n),atol=1e-9)
        self.assertLessEqual(e.reachable_count(v)-e.reachable_count(root),5)
        self.assertEqual(v,e.edit_version(root,self.x,{3:.4}))

    def test_frequency_and_full_spectrum(self):
        e=self.eng
        root=e.add(e.mul(self.x,self.y),e.mul(self.z,self.z))
        vals=e.evaluate_spectrum(root)
        self.close(fft.irfft(vals,n=self.n),self.direct(self.xdata,self.ydata,self.zdata,1))
        for k in [0,1,2,19,31,32,50,63]:
            self.assertAlmostEqual(e.frequency(root,k).real,fft.fft(self.direct(self.xdata,self.ydata,self.zdata,1))[k].real,places=8)
            self.assertAlmostEqual(e.frequency(root,k).imag,fft.fft(self.direct(self.xdata,self.ydata,self.zdata,1))[k].imag,places=8)

    def test_linear_single_all_and_bins(self):
        e=self.eng
        root=e.add(e.mul(self.x,self.y),e.mul(self.z,self.z))
        prep=e.prepare(root,self.x)
        self.assertEqual(prep.degree,1)
        for t,delta in [(0,.2),(3,-.15),(49,.5),(63,-.1)]:
            ax=self.xdata.copy();ax[t]+=delta
            wanted=self.direct(ax,self.ydata,self.zdata,1)
            self.close(prep.single(t,delta),wanted)
            self.close(prep.single(t,delta,[0,5,10,63]),wanted[[0,5,10,63]])
            f=fft.fft(wanted)
            for k in [0,1,3,41,63]:
                self.assertAlmostEqual(prep.single_frequency(t,delta,k).real,f[k].real,places=8)
                self.assertAlmostEqual(prep.single_frequency(t,delta,k).imag,f[k].imag,places=8)

    def test_quadratic_single_and_many(self):
        e=self.eng
        root=e.add(e.mul(self.x,self.x),e.mul(self.y,self.z))
        prep=e.prepare(root,self.x)
        self.assertEqual(prep.degree,2)
        self.assertEqual(prep.sparse_coefficients[2],{0:1.0})
        self.assertIsNone(prep.kernels[2])
        for edits in [{5:.2},{0:-.1,31:.25},{4:.15,17:-.3,33:.1},{}]:
            ax=self.xdata.copy()
            for t,d in edits.items():ax[t]+=d
            wanted=self.direct(ax,self.ydata,self.zdata,2)
            if len(edits)==1:
                t,d=next(iter(edits.items()))
                self.close(prep.single(t,d),wanted)
            self.close(prep.many(edits),wanted)
            self.close(prep.many(edits,method='spectral'),wanted)
            self.close(prep.many(edits,indices=[0,8,19,60]),wanted[[0,8,19,60]])

    def test_cubic_single_and_many(self):
        e=self.eng
        root=e.add(e.mul(self.x,self.x,self.x),e.scale(e.mul(self.x,self.y),2),self.z)
        prep=e.prepare(root,self.x)
        self.assertEqual(prep.degree,3)
        self.assertEqual(prep.sparse_coefficients[3],{0:1.0})
        self.assertIsNone(prep.kernels[3])
        self.assertRaises(DegreeExceeded,e.prepare,root,self.x,max_degree=2)
        for t,d in [(3,.01),(19,-.02)]:
            ax=self.xdata.copy();ax[t]+=d
            self.close(prep.single(t,d),self.direct(ax,self.ydata,self.zdata,3))
        edits={5:.01,15:-.04,28:.02}
        ax=self.xdata.copy()
        for t,d in edits.items():ax[t]+=d
        wanted=self.direct(ax,self.ydata,self.zdata,3)
        self.close(prep.many(edits,max_shift_terms=2),wanted)
        self.close(prep.many(edits,method='shifts'),wanted)
        self.close(prep.many(edits,indices=[0,4,55]),wanted[[0,4,55]])

    def test_exact_fallback_replacement(self):
        e=self.eng
        root=e.mul(self.x,self.x,self.x,self.x,self.y)
        self.assertRaises(DegreeExceeded,e.prepare,root,self.x,max_degree=3)
        edited=e.edit_version(root,self.x,{4:.03,20:-.01})
        ax=self.xdata.copy();ax[4]+=.03;ax[20]-=.01
        wanted=fft.irfft(fft.rfft(ax)**4*fft.rfft(self.ydata),n=self.n)
        self.close(e.evaluate_time(edited),wanted)

    def test_no_leaf_occurrence(self):
        e=self.eng
        root=e.mul(self.y,self.z)
        p=e.prepare(root,self.x)
        self.assertEqual(p.degree,0)
        self.close(p.single(2,20),e.evaluate_time(root))

    def test_symbolic_taylor_coefficients(self):
        e=self.eng
        root=e.add(e.mul(self.x,self.x,self.x),e.scale(e.mul(self.x,self.y),2),self.z)
        symbols=e.symbolic_jets(root,self.x)
        self.assertEqual(len(symbols),4)
        prepared=e.prepare(root,self.x)
        for h,uid in enumerate(symbols):
            expected=e.evaluate_time(uid)
            if prepared.kernels[h] is not None:
                self.close(expected,prepared.kernels[h])
            else:
                sparse=prepared.sparse_coefficients[h]
                got=np.zeros(self.n)
                for pos,amp in sparse.items():got[pos]=amp
                self.close(expected,got)

    def test_common_factor_search(self):
        e=self.eng
        root=e.add(e.mul(self.x,self.y),e.mul(self.x,self.z),
                   e.scale(e.mul(self.x,self.y,self.z),-2.))
        optimized=e.factor_common(root)
        self.assertNotEqual(root,optimized)
        self.close(e.evaluate_time(root),e.evaluate_time(optimized))
        a=e.spectral_operation_estimate(root)
        b=e.spectral_operation_estimate(optimized)
        self.assertLess(b['multiplications'],a['multiplications'])
        # Cost reductions do not rely on repeated numerical input values.
        self.assertEqual(optimized,e.factor_common(optimized))

    def test_shift_phase(self):
        e=self.eng
        root=e.mul(self.x,e.impulse(5,2))
        self.close(e.evaluate_time(root),2*np.roll(self.xdata,5))
        self.close(e.evaluate_spectrum(root),fft.rfft(2*np.roll(self.xdata,5)))

    def test_bounded_spectrum_cache(self):
        e=AlgebraFFT(64,max_spectrum_cache_bytes=64)
        a=e.signal(self.xdata)
        b=e.signal(self.ydata)
        for j in range(12):
            e.evaluate_spectrum(e.add(e.mul(a,b),e.impulse(j,0.2)))
        self.assertLessEqual(e._spectrum_cache_bytes,64)

    def test_dispatcher_expected_reuse_and_memory(self):
        e=self.eng
        root=e.add(e.mul(self.x,self.x),e.mul(self.y,self.z))
        cheap=e.plan_updates(root,self.x,expected_versions=1)
        self.assertEqual(cheap.mode,'fallback')
        hot=e.plan_updates(root,self.x,expected_versions=64)
        self.assertEqual(hot.mode,'jets')
        constrained=e.plan_updates(root,self.x,expected_versions=64,max_prepared_bytes=64)
        self.assertEqual(constrained.mode,'fallback')
        for p in [cheap,hot,constrained]:
            a=self.xdata.copy();a[12]+=.04
            self.close(p.single(12,.04),self.direct(a,self.ydata,self.zdata,2))

    def test_array_immutability(self):
        e=AlgebraFFT(64)
        a=self.xdata.copy()
        uid=e.signal(a)
        before=e.evaluate_time(uid)
        a[:]=0
        self.close(e.evaluate_time(uid),before)
        self.assertRaises(ValueError,e.signal,np.ones(12))
        self.assertRaises(ValueError,e.signal,np.full(64,float('inf')))

if __name__=='__main__':unittest.main()

class Phase7ImportTests(unittest.TestCase):
    def test_import_shared_seeds_shift_edits(self):
        from legacy_phase7.persistent_chain import ChainEngine
        rng=np.random.default_rng(11)
        n=64
        old=ChainEngine()
        a,b,c=[old.seed(rng.normal(scale=.15,size=n)) for _ in range(3)]
        chain=old.chain([a,b,c])
        chain2=chain.edit(0,4,.12).shift(1,3).scale(2,2.)
        eng=AlgebraFFT(n)
        root=eng.import_phase7(chain)
        root2=eng.import_phase7(chain2)
        self.assertEqual(eng.stats['imported_spectra'],3)
        self.assertEqual(len(eng._seeds),3)
        np.testing.assert_allclose(eng.evaluate_time(root),chain.dense(),rtol=2e-8,atol=2e-8)
        np.testing.assert_allclose(eng.evaluate_time(root2),chain2.dense(),rtol=2e-8,atol=2e-8)
