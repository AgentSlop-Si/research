import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))

import numpy as np
from scipy import fft
from cost_aware_fft import RelationFFT, sparse_from_known_changes
from phase import phases_tiled

class TestRelationFFT(unittest.TestCase):
    def setUp(self):
        self.e = RelationFFT(max_cache_bytes=2*1024**2,
                             max_phase_bytes=2*1024**2,
                             max_temp_bytes=16*1024**2)
        self.rng = np.random.default_rng(20261009)

    def assertSpectrum(self, state, method):
        expected=fft.rfft(state.signal())
        actual=self.e.materialize(state, method=method)
        np.testing.assert_allclose(actual, expected, rtol=3e-9, atol=2e-7)

    def test_phase_tiled_non_power_of_two_and_special(self):
        for n in [1,2,5,7,16,512,1024,8192]:
            for p in sorted(set([0,1 % n,(n-1),n//3])):
                got=phases_tiled(n,p,count=n//2+1)
                q=np.arange(n//2+1)
                want=np.exp(-2j*np.pi*((q*p)%n)/n)
                np.testing.assert_allclose(got,want,rtol=1e-10,atol=1e-10)

    def test_input_immutable_and_root_reuse(self):
        for n in [1,2,5,7,8,128]:
            x=self.rng.standard_normal(n)
            root=self.e.register(x)
            original=x.copy(); x[0]+=100
            np.testing.assert_allclose(root.signal(), original)
            self.assertSpectrum(root, 'reuse')
            self.assertSpectrum(root, 'native')
            self.assertEqual(self.e.recommend(root),'reuse')

    def test_one_and_multi_edits_all_k(self):
        for n in [8,16,31,128,1024]:
            for k in [1,2,3,4,7,16,30]:
                if k > n: continue
                root=self.e.register(self.rng.standard_normal(n))
                branch=root.fork()
                ps=self.rng.choice(n,size=k,replace=False)
                for p in ps:
                    branch.edit(int(p),float(self.rng.normal()))
                self.assertSpectrum(branch,'direct')
                self.assertSpectrum(branch,'native')
                if n & (n-1)==0:
                    self.assertSpectrum(branch,'pruned')
                for q in [0,n//4,n//2]:
                    np.testing.assert_allclose(branch.bin(q),fft.rfft(branch.signal())[q],atol=2e-7)
                qs=[0,n//4,n//2]
                np.testing.assert_allclose(branch.bins(qs),fft.rfft(branch.signal())[qs],atol=2e-7)

    def test_same_index_merging_and_cancel(self):
        root=self.e.register([1.,2.,3.,4.,5.,6.,7.,8.])
        a=root.fork().edit(2,5).edit(2,-3).edit(2,-2)
        self.assertEqual(a.distinct_edits,0)
        np.testing.assert_allclose(a.spectrum(),root.spectrum())
        self.assertEqual(root.distinct_edits,0)
        b=root.fork().edit(2,5).edit(2,-2)
        self.assertEqual(b.distinct_edits,1)
        self.assertSpectrum(b,'direct')

    def test_shift_after_edit_and_edit_after_shift(self):
        for n in [7,8,37,64]:
            root=self.e.register(self.rng.normal(size=n))
            a=root.fork().edit(1,3.5).edit(n-1,-2.1).shift(n+3)
            self.assertSpectrum(a,'direct')
            self.assertSpectrum(a,'native')
            self.assertSpectrum(a.shift(-3),'direct')
            b=root.shift(-4).edit(2,5.5)
            self.assertSpectrum(b,'direct')
            c=root.shift(0)
            self.assertSpectrum(c,'linear')

    def test_lowrank_known_family(self):
        n=64
        bases=self.rng.normal(size=(3,n))
        C=self.rng.normal(size=(13,3))
        states=self.e.states_from_bases(bases,C)
        self.assertEqual(len(states),13)
        for j,state in enumerate(states):
            np.testing.assert_allclose(state.signal(), C[j]@bases,atol=1e-12)
            self.assertSpectrum(state,'linear')
            q=[0,1,20,32]
            np.testing.assert_allclose(state.bins(q),fft.rfft(C[j]@bases)[q],atol=1e-10)

    def test_lowrank_plus_sparse_and_cancelled_terms(self):
        n=128
        a=self.e.register(self.rng.normal(size=n))
        b=self.e.register(self.rng.normal(size=n))
        c=self.e.combine([a,b],[2,-0.5]).shift(7).edit(20,4).edit(6,-3)
        for mode in ('direct','pruned','native'):
            self.assertSpectrum(c,mode)
        z=self.e.combine([a,a],[1,-1])
        self.assertEqual(z.term_count,0)
        self.assertEqual(self.e.recommend(z),'zero')
        np.testing.assert_equal(z.spectrum(),np.zeros(n//2+1))

    def test_lazy_bins_no_full_materialization(self):
        n=4096
        root=self.e.register(self.rng.normal(size=n))
        s=root.fork().edit(11,3).edit(250,-7).edit(11,-0.5).shift(25)
        self.assertIsNone(s._cached_output)
        want=fft.rfft(s.signal())
        self.assertAlmostEqual(abs(s.bin(123)-want[123]),0,delta=1e-8)
        np.testing.assert_allclose(s.bins([5,11,17,31]),want[[5,11,17,31]],atol=1e-8)
        self.assertIsNone(s._cached_output)

    def test_exact_cache_and_byte_budget(self):
        n=256
        x=self.rng.standard_normal(n)
        a=self.e.fft(x,cache=True)
        a[:]=0
        b=self.e.fft(x,cache=True)
        np.testing.assert_allclose(b,fft.rfft(x))
        self.assertEqual(self.e.stats['exact_hits'],1)
        e=RelationFFT(max_cache_bytes=128,max_phase_bytes=0)
        e.fft(x)
        self.assertEqual(e.memory_report()['internal_exact_cache_bytes'],0)

    def test_fail_safe_inputs(self):
        for bad in ([],[np.nan,0],[np.inf,2],[[1,2],[3,4]],[1+2j]):
            with self.assertRaises(ValueError): self.e.register(bad)
        with self.assertRaises(ValueError):
            self.e.register([1,2,3]).edit(10,1)
        with self.assertRaises(ValueError):
            self.e.register([1,2,3]).edit(1,float('nan'))
        a=self.e.register([1,2,3]); b=self.e.register([1,2])
        with self.assertRaises(ValueError): self.e.combine([a,b],[1,1])
        with self.assertRaises(ValueError): self.e.materialize(a,method='pruned') if a.edits else self.e.materialize(a,method='nonexistent')

    def test_cached_output_invalidation(self):
        root=self.e.register(self.rng.normal(size=256))
        branch=root.fork()
        a=branch.spectrum(cache_output=True,copy=False)
        self.assertFalse(a.flags.writeable)
        self.assertIsNotNone(branch._cached_output)
        branch.edit(4,0.5)
        self.assertIsNone(branch._cached_output)
        self.assertSpectrum(branch,'direct')

    def test_calibration_verifies_methods(self):
        root=self.e.register(self.rng.normal(size=2048))
        state=root.fork().edit(7,3).edit(21,-1)
        profile=self.e.calibrate(state,repeats=2)
        self.assertEqual(profile.best_method,self.e.recommend(state))
        self.assertSpectrum(state,'auto')
        self.assertGreaterEqual(len(profile.median_seconds),2)

    def test_functional_update(self):
        n=32
        x=self.rng.normal(size=n)
        F=fft.rfft(x)
        changes=[(2,3),(4,-0.5),(2,1.25)]
        y=x.copy()
        for p,d in changes:y[p]+=d
        for method in ('direct','pruned'):
            result=sparse_from_known_changes(F,n,changes,method=method)
            np.testing.assert_allclose(result,fft.rfft(y),rtol=1e-10,atol=1e-9)

    def test_no_mutation_of_internal_arrays(self):
        root=self.e.register([1,2,3,4,5,6])
        view=root.spectrum(copy=False)
        self.assertFalse(view.flags.writeable)
        with self.assertRaises(ValueError): view[0] = 999
        self.assertSpectrum(root,'reuse')

if __name__=='__main__':
    unittest.main()

class TestTrackedBins(unittest.TestCase):
    def test_live_bins_updates_and_fork(self):
        from cost_aware_fft import TrackedBins
        rng=np.random.default_rng(111)
        for n in (7,16,101,1024):
            x=rng.normal(size=n)
            eng=RelationFFT()
            root=eng.register(x)
            qs=[0,1,n//4,n//2]
            tracker=TrackedBins(root,qs,max_phase_entries=2)
            y=x.copy()
            for p,d in [(1,1.25),(n-1,-0.45),(1,-0.5),(0,1.2)]:
                tracker.edit(p,d)
                y[p]+=d
                np.testing.assert_allclose(tracker.values(),fft.rfft(y)[qs],rtol=1e-12,atol=1e-9)
            self.assertEqual(root.distinct_edits,0)
            np.testing.assert_allclose(tracker.current_state().signal(),y)

    def test_multi_edits_coalescing(self):
        from cost_aware_fft import subscribe
        eng=RelationFFT()
        initial=np.arange(32,dtype=np.float64)
        tracked=subscribe(eng.register(initial),[0,2,7,16])
        tracked.edit_many([(2,1),(2,-1),(11,8),(7,2)])
        expected=initial.copy(); expected[11]+=8; expected[7]+=2
        self.assertEqual(tracked.state.distinct_edits,2)
        np.testing.assert_allclose(tracked.values(),fft.rfft(expected)[[0,2,7,16]],atol=1e-9)
        tracked.state.edit(5,1)
        with self.assertRaises(RuntimeError): tracked.values()

    def test_exact_modular_identity(self):
        # Independently check Fourier delta identity in an exact finite field;
        # the real-valued engine itself still operates in floating point.
        p=998244353;n=16
        root=pow(3,(p-1)//n,p)
        a=[(7*i+13)%p for i in range(n)]
        changes=[(2,50),(7,-12),(2,-18)]
        def transform(x):
            return [sum(x[t]*pow(root,q*t,p) for t in range(n))%p for q in range(n)]
        before=transform(a)
        for t,d in changes: a[t]=(a[t]+d)%p
        after=transform(a)
        predicted=[(before[q]+sum(d*pow(root,q*t,p) for t,d in changes))%p for q in range(n)]
        self.assertEqual(after,predicted)

class TestAutoFallback(unittest.TestCase):
    def test_bypass_on_unrelated_inputs_and_hit_when_repeated(self):
        e=RelationFFT(max_cache_bytes=8*1024**2)
        rng=np.random.default_rng(101)
        for i in range(22):
            x=rng.normal(size=512)
            np.testing.assert_allclose(e.fft(x),fft.rfft(x),atol=1e-9)
        self.assertGreater(e.stats['hash_bypasses'],0)
        # Explicit cache mode always checks and verifies repetitions.
        x=rng.normal(size=2048)
        e.fft(x,cache=True)
        got=e.fft(x,cache=True)
        np.testing.assert_allclose(got,fft.rfft(x))
        self.assertGreaterEqual(e.stats['exact_hits'],1)

    def test_auto_mode_validates_argument(self):
        e=RelationFFT()
        with self.assertRaises(ValueError): e.fft([1,2,3],cache='always')
