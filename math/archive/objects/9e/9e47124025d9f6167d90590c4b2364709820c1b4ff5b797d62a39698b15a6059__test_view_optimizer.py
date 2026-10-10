import unittest
import numpy as np

from multi_view import SharedProjectedFourierStore, union_frequency_sets
from view_optimizer import AdaptiveSpectralOrganizer


class TestViewOptimizer(unittest.TestCase):
    def make(self, *, n=512, r=6):
        rng=np.random.default_rng(551)
        vb={
            'a':[1,2,3,4,5,6,7,8],
            'b':[1,2,3,4,9,10,11,12],
            'c':[101,102,103,104,105,106,107,108],
        }
        union,_,_=union_frequency_sets(vb,n)
        basis=rng.standard_normal((r,n))+1j*rng.standard_normal((r,n))
        proj=np.fft.fft(basis,axis=1)[:,union]
        c=rng.standard_normal(r)+1j*rng.standard_normal(r)
        st=SharedProjectedFourierStore(n,union,proj,vb,c,prepared_positions=[17,211],event_capacity=128,promote_after=None)
        return rng,vb,basis,c,st

    def test_merge_and_exact_group_cache(self):
        rng,vb,basis,c,st=self.make()
        opt=AdaptiveSpectralOrganizer(st,history_queries=12,min_history=3,replan_every=6,merge_threshold=1.05,min_sync=.5)
        x=c@basis
        # a and b query at the same producer versions; c is phase shifted.
        for t in range(18):
            d=.01*(1+1j); i=t%len(c); opt.add_coefficient(i,d); x+=d*basis[i]
            if t%2==0:
                ga=opt.query('a'); gb=opt.query('b')
                fx=np.fft.fft(x)
                self.assertTrue(np.allclose(ga,fx[vb['a']],rtol=3e-11,atol=3e-9))
                self.assertTrue(np.allclose(gb,fx[vb['b']],rtol=3e-11,atol=3e-9))
            if t%4==1: opt.query('c')
        opt.replan()
        groups=[set(g) for g in opt.partition]
        self.assertIn({'a','b'},groups)
        self.assertTrue(any(len(g)>1 for g in groups))
        # Sequential same-version calls should make the second consumer a group cache hit.
        opt.add_point(17,.25-.1j); x[17]+=.25-.1j
        before=opt.stats.group_cache_hits
        a=opt.query('a'); b=opt.query('b'); fx=np.fft.fft(x)
        self.assertTrue(np.allclose(a,fx[vb['a']],rtol=3e-11,atol=3e-9))
        self.assertTrue(np.allclose(b,fx[vb['b']],rtol=3e-11,atol=3e-9))
        self.assertGreaterEqual(opt.stats.group_cache_hits,before+1)

    def test_split_after_rate_divergence(self):
        _rng,vb,basis,c,st=self.make()
        opt=AdaptiveSpectralOrganizer(st,history_queries=10,min_history=3,replan_every=1000,merge_threshold=1.04,min_sync=.45)
        # synchronized phase
        for t in range(8):
            opt.add_coefficient(t%len(c),.01)
            opt.query('a'); opt.query('b')
        opt.replan()
        self.assertTrue(any(set(g)=={'a','b'} for g in opt.partition))
        # a becomes much hotter; bounded history forgets the old synchronization.
        for t in range(30):
            opt.add_coefficient(t%len(c),.005)
            opt.query('a')
            if t in (0,29): opt.query('b')
        opt.replan()
        self.assertFalse(any(set(g)=={'a','b'} for g in opt.partition))

    def test_no_merge_without_frequency_reuse(self):
        _rng,vb,basis,c,st=self.make()
        opt=AdaptiveSpectralOrganizer(st,history_queries=8,min_history=3,replan_every=1000,merge_threshold=1.05,min_sync=.4)
        for t in range(8):
            opt.add_coefficient(t%len(c),.01)
            opt.query('a');opt.query('c')
        opt.replan()
        self.assertFalse(any(set(g)=={'a','c'} for g in opt.partition))

    def test_dormant_probe_rediscovers_new_sync(self):
        _rng,vb,basis,c,st=self.make()
        opt=AdaptiveSpectralOrganizer(st,history_queries=10,min_history=3,replan_every=6,
            merge_threshold=1.04,min_sync=.45,probe_period_updates=12,probe_window_updates=6)
        # First observation window: deliberately asynchronous -> singleton partition.
        for t in range(8):
            opt.add_coefficient(t%len(c),.01)
            opt.query('a')
            if t in (1,6): opt.query('b')
        opt.replan()
        self.assertFalse(any(set(g)=={'a','b'} for g in opt.partition))
        # Advance beyond the dormant period, then make a and b query together
        # throughout the new probe window.
        for t in range(20):
            opt.add_coefficient(t%len(c),.005)
            if t>=12:
                opt.query('a');opt.query('b')
        # One more producer update closes the probe epoch and triggers replan.
        opt.add_coefficient(0,.001)
        self.assertTrue(any(set(g)=={'a','b'} for g in opt.partition))


if __name__=='__main__': unittest.main()
