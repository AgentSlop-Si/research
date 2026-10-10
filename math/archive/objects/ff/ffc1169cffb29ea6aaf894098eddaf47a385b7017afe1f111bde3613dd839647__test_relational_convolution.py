import unittest
import numpy as np
from cost_aware_fft import RelationFFT
from relational_convolution import RelationalConvolver, DynamicBitProduct

class ConvolutionTests(unittest.TestCase):
    def setUp(self):
        self.rng=np.random.default_rng(20261009)
        self.fft=RelationFFT()
        self.conv=RelationalConvolver(max_core_bytes=1<<20)

    def check(self,sa,sb,rtol=1e-9,atol=1e-7):
        view=self.conv.product(sa,sb)
        a=sa.signal(); b=sb.signal(); n=len(a)
        expected=np.fft.ifft(np.fft.fft(a)*np.fft.fft(b)).real
        for method in ('native','reuse','auto'):
            y=view.full(method)
            np.testing.assert_allclose(y,expected,rtol=rtol,atol=atol)
        inds=self.rng.choice(n,size=min(n,12),replace=False)
        for i in inds:
            self.assertAlmostEqual(float(expected[i]), view.at(i), delta=atol+rtol*abs(expected[i]))
        qs=self.rng.choice(n//2+1,size=min(n//2+1,11),replace=False)
        np.testing.assert_allclose(view.frequency_bins(qs),np.fft.rfft(expected)[qs],rtol=rtol,atol=atol)
        return view

    def test_fresh_bases(self):
        for n in (1,2,4,8,17,128,512):
            a=self.fft.register(self.rng.standard_normal(n))
            b=self.fft.register(self.rng.standard_normal(n))
            self.check(a,b)

    def test_shifted_and_sparse(self):
        for n in (16,128,1024):
            a=self.fft.register(self.rng.standard_normal(n))
            b=self.fft.register(self.rng.standard_normal(n))
            x=a.shift(5).edit(2,.5).edit(4,-2).edit(2,.25)
            y=b.shift(-3).edit(5,2).edit(27%n,-.25)
            self.check(x,y)

    def test_multi_bases_and_sparse_pairs(self):
        for n in (16,256):
            ss=[self.fft.register(self.rng.standard_normal(n)) for _ in range(4)]
            a=self.fft.combine([ss[0].shift(2),ss[1]], [1.2,-.4])
            b=self.fft.combine([ss[2].shift(6),ss[3].shift(-1)], [.3,-2.])
            for i in (3,11,13): a.edit(i,.2+i/10)
            for i in (1,13,15): b.edit(i,-.9+i/10)
            self.check(a,b)

    def test_snapshot_is_immutable(self):
        a=self.fft.register(self.rng.standard_normal(64))
        b=self.fft.register(self.rng.standard_normal(64))
        v=self.conv.product(a,b)
        prior=v.full(method='reuse')
        a.edit(0,17.5)
        np.testing.assert_allclose(v.full(method='reuse'), prior)
        self.assertNotAlmostEqual(v.at(0),self.conv.product(a,b).at(0))

    def test_cache_reuse_and_eviction(self):
        a=self.fft.register(self.rng.standard_normal(256))
        b=self.fft.register(self.rng.standard_normal(256))
        self.conv=RelationalConvolver(max_core_bytes=256*8)
        v=self.conv.product(a,b)
        v.at(2); self.assertEqual(self.conv.stats['core_misses'],1)
        v.at(6); self.assertEqual(self.conv.stats['core_hits'],1)
        self.assertEqual(self.conv.memory_report()['cached_core_pairs'],1)
        c=self.fft.register(self.rng.standard_normal(256))
        self.conv.product(a,c).at(1)
        self.assertEqual(self.conv.memory_report()['cached_core_pairs'],1)
        self.assertGreater(self.conv.stats['core_evictions'],0)

    def test_sparse_only(self):
        n=31
        zero=self.fft.combine([self.fft.register(np.zeros(n))],[0.])
        a=zero.fork().edit(2,4.).edit(12,-3.)
        b=zero.fork().edit(3,7.).edit(21,-2.)
        v=self.check(a,b)
        self.assertEqual(v.at(5),28.)

    def test_empty_bins_and_boundaries(self):
        a=self.fft.register(np.array([1.,2.,3.]))
        v=self.conv.product(a,a)
        self.assertEqual(v.frequency_bins([]).size,0)
        with self.assertRaises(IndexError): v.at(3)
        with self.assertRaises(IndexError): v.frequency_bins([2])

    def test_wrong_length(self):
        a=self.fft.register(np.ones(8))
        b=self.fft.register(np.ones(7))
        with self.assertRaises(ValueError): self.conv.product(a,b)

class DynamicIntTests(unittest.TestCase):
    def test_random_flips_and_forks(self):
        rng=np.random.default_rng(901)
        for bits in (1,8,23,128,1033,8192):
            a=int.from_bytes(rng.bytes((bits+7)//8), 'little') % (1<<bits)
            b=int.from_bytes(rng.bytes((bits+7)//8), 'little') % (1<<bits)
            p=DynamicBitProduct(a,b,bits)
            q=p.fork()
            for _ in range(80):
                which='a' if rng.integers(2) == 0 else 'b'
                t=int(rng.integers(bits))
                p.flip(which,t)
                self.assertTrue(p.verify())
            self.assertTrue(q.verify())
            self.assertEqual(q.product,a*b)

    def test_reject_invalid(self):
        with self.assertRaises(ValueError): DynamicBitProduct(-3,1)
        with self.assertRaises(ValueError): DynamicBitProduct(16,1,4)
        p=DynamicBitProduct(1,2,10)
        with self.assertRaises(IndexError): p.flip('a',10)
        with self.assertRaises(ValueError): p.flip('x',0)

if __name__=='__main__': unittest.main()

class SubscriptionTests(unittest.TestCase):
    def test_both_operand_events(self):
        from relational_convolution import subscribe_convolution
        rng=np.random.default_rng(782)
        for n in (16,127,4096):
            fft=RelationFFT()
            a=fft.register(rng.standard_normal(n))
            b=fft.register(rng.standard_normal(n))
            v=RelationalConvolver().product(a,b)
            indices=[0,n//3,n//2,n-1]
            sub=subscribe_convolution(v,indices)
            aa=a.signal().copy();bb=b.signal().copy()
            for turn in range(120):
                side='left' if rng.integers(2) == 0 else 'right'
                index=int(rng.integers(n))
                delta=float(rng.standard_normal())
                sub.edit(side,index,delta)
                if side=='left': aa[index]+=delta
                else: bb[index]+=delta
                if turn%25==0:
                    gold=np.fft.ifft(np.fft.fft(aa)*np.fft.fft(bb)).real
                    np.testing.assert_allclose(sub.values(),gold[indices],rtol=1e-9,atol=1e-7)
            exact=sub.snapshot_view().full('reuse')
            np.testing.assert_allclose(exact,np.fft.ifft(np.fft.fft(aa)*np.fft.fft(bb)).real,atol=1e-7)

    def test_invalid_and_empty_subscription(self):
        from relational_convolution import subscribe_convolution
        fft=RelationFFT()
        a=fft.register(np.ones(8))
        c=RelationalConvolver().product(a,a)
        s=subscribe_convolution(c,[])
        self.assertEqual(s.values().size,0)
        with self.assertRaises(IndexError): subscribe_convolution(c,[-1])
        with self.assertRaises(ValueError): s.edit('nope',0,1)

class AutotuneTests(unittest.TestCase):
    def test_prepared_and_trained_dispatch(self):
        rng=np.random.default_rng(91)
        re=RelationFFT()
        n=4096
        a=re.register(rng.standard_normal(n))
        b=re.register(rng.standard_normal(n))
        con=RelationalConvolver(max_core_bytes=n*8)
        receipt=con.calibrate_sparse(a,b,k_values=(1,2,4),repeats=2)
        self.assertIn(receipt['cutoff'],(0,1,2,4))
        view=con.product(a.fork().edit(12,.3),b)
        np.testing.assert_allclose(view.full('auto'),view.full('prepared'),atol=1e-7)
        self.assertIn(view.last_method,('prepared','reuse'))

    def test_prepared_rejects_two_mutable_operands(self):
        re=RelationFFT()
        a=re.register(np.arange(16.))
        b=re.register(np.arange(16.)+1)
        view=RelationalConvolver().product(a.fork().edit(1,1.),b.fork().edit(2,1.))
        with self.assertRaises(ValueError):view.full('prepared')
