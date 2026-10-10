"""Independent correctness, storage and charged-arithmetic tests for Phase24."""
import random,unittest
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from rational_forcing import direct_dft_any
from lazy_dif import LazyDIF,preview_butterflies,transform_conjugate_lazy
from deferred_dif import DeferredDIF,transform_deferred_conjugate
from short_probe_fusion import transform_short_probe,prefix_fourier_stream


class DeferredFourierTests(unittest.TestCase):
    def test_every_query_subset_and_full_completion(self):
        for n in (16,32,64,128,256):
            for p,g in ((2013265921,31),(998244353,3)):
                eng=RecurrenceGreen(n,p,g)
                rng=random.Random(24001+n+p)
                data=[rng.randrange(p) for _ in range(n)]
                oracle=direct_dft_any(data,eng.omega,p)
                for _ in range(16):
                    count=rng.randrange(1,n+1)
                    keys=rng.sample(range(n),count)
                    sess=DeferredDIF(data,eng.powers,p)
                    vals=sess.preview(keys)
                    self.assertEqual(len(vals),count)
                    for k,y in vals.items():self.assertEqual(y,oracle[k])
                    self.assertEqual(sess.stats.backup_peak,n-count)
                    self.assertEqual(sess.storage_bound()['current_backup_words'],n-count)
                    self.assertLessEqual(sess.stats.arithmetic(),(3*n//2)*(n.bit_length()-1))
                    self.assertEqual(sess.full(),oracle)
                    self.assertEqual(sess.stats.arithmetic(),(3*n//2)*(n.bit_length()-1))
                    self.assertEqual(sess.storage_bound()['current_backup_words'],0)

    def test_single_frequency_and_all_frequencies(self):
        n=128;e=RecurrenceGreen(n)
        rng=random.Random(24002)
        x=[rng.randrange(e.p) for _ in range(n)]
        reference=direct_dft_any(x,e.omega,e.p)
        for k in (0,1,7,63,127):
            sess=DeferredDIF(x,e.powers,e.p)
            self.assertEqual(sess.preview([k])[k],reference[k])
            self.assertEqual(sess.stats.backup_peak,n-1)
            self.assertEqual(sess.full(),reference)
        sess=DeferredDIF(x,e.powers,e.p)
        self.assertEqual(sess.preview(range(n)),dict(enumerate(reference)))
        self.assertEqual(sess.stats.backup_peak,0)
        self.assertEqual(sess.full(),reference)

    def test_preview_closed_form_m10_plus_neighbor(self):
        for n in (32,64,128,256,1024,4096):
            e=RecurrenceGreen(n)
            keys=list(range(10))+[n-1]
            s=DeferredDIF([1]*n,e.powers,e.p)
            out=s.preview(keys)
            self.assertEqual(out[0],n)
            self.assertEqual(s.stats.arithmetic(),49*n//8-12)
            self.assertEqual(s.stats.backup_peak,n-11)
            eager=LazyDIF([1]*n,e.powers,e.p)
            _=[eager.get(k) for k in keys]
            self.assertEqual(eager.stats.arithmetic(),3*(43*n//16-11))
            self.assertEqual(eager.stats.arithmetic()-s.stats.arithmetic(),31*n//16-21)
            self.assertEqual(s.full(),eager.full())

    def test_green_conjugate_probes_independently(self):
        rng=random.Random(24003)
        for n in (32,64,128,512):
            e=RecurrenceGreen(n)
            for _ in range(4):
                x=[rng.randrange(e.p) for _ in range(n)]
                sess=DeferredDIF(x,e.powers,e.p)
                d=sess.preview(list(range(10))+[n-1])
                r=e.P.apply(x)
                R=prefix_fourier_stream(r,e.powers,10,e.p)
                for k in range(10):
                    y=(e.L.diag[k]*d[k]+e.L.shift*d[k-1 if k else n-1])%e.p
                    self.assertEqual(y,R[k])

    def test_all_input_correct_structured_and_generic(self):
        rng=random.Random(24004)
        for p,g,n in ((2013265921,31,64),(2013265921,31,128),
                      (2013265921,31,256),(2013265921,31,512),
                      (998244353,3,64),(998244353,3,128)):
            e=RecurrenceGreen(n,p,g)
            h=[0]*n;h[4]=7;h[n-9]=11
            r=dense_from_shift_defects(dense_from_shift_defects(h,n//2-3,17,p),n//2+7,29,p)
            samples=[('structured',e.P.solve(r))]
            samples.extend(('generic',[rng.randrange(p) for _ in range(n)]) for _ in range(3))
            for label,x in samples:
                y,meta=transform_deferred_conjugate(e,x)
                self.assertEqual(y,direct_dft_any(x,e.omega,e.p))
                self.assertEqual(meta['residual_computed'],label=='structured')
                if label=='generic':
                    self.assertEqual(meta['selected'],'deferred-conjugate-fallback')
                    self.assertEqual(meta['final_fft']['arithmetic'],3*(n//2)*(n.bit_length()-1))
                else:
                    self.assertEqual(meta['selected'],'deferred-conjugate-certified')

    def test_phase23_structured_exact_saving(self):
        for n in (64,128,256,1024):
            e=RecurrenceGreen(n)
            h=[0]*n;h[4]=7;h[n-9]=11
            r=dense_from_shift_defects(dense_from_shift_defects(h,n//2-3,17,e.p),n//2+7,29,e.p)
            x=e.P.solve(r)
            a,ma=transform_short_probe(e,x)
            b,mb=transform_deferred_conjugate(e,x)
            self.assertEqual(a,b)
            self.assertEqual(ma['selected'],'short-prefix-certified')
            self.assertEqual(mb['selected'],'deferred-conjugate-certified')
            self.assertEqual(ma['work'].arithmetic()-mb['work'].arithmetic(),103*n//8-18)

    def test_adversarial_identical_short_prefix_safe_fallback(self):
        p=2013265921;n=128;e=RecurrenceGreen(n,p,31)
        h=[0]*n;h[4]=7;h[55]=11
        r=dense_from_shift_defects(dense_from_shift_defects(h,43,17,p),61,29,p)
        m=10;k0=19
        rbad=[(r[j]+pow(e.powers[k0],-j,p))%p for j in range(n)]
        self.assertEqual(prefix_fourier_stream(r,e.powers,m,p),
                         prefix_fourier_stream(rbad,e.powers,m,p))
        x=e.P.solve(rbad)
        y,meta=transform_deferred_conjugate(e,x)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(meta['selected'],'deferred-conjugate-fallback')
        self.assertGreater(meta['meta'].failed_certificates,0)
        self.assertTrue(meta['residual_computed'])
        self.assertEqual(meta['final_fft']['arithmetic'],3*n//2*(n.bit_length()-1))

    def test_wrong_length_and_double_preview_rejected(self):
        e=RecurrenceGreen(32)
        s=DeferredDIF([0]*32,e.powers,e.p)
        with self.assertRaises(ValueError):s.preview([33])
        with self.assertRaises(ValueError):s.preview([])
        with self.assertRaises(ValueError):DeferredDIF([0]*31,e.powers,e.p)
        with self.assertRaises(ValueError):transform_deferred_conjugate(e,[0]*31)

if __name__=='__main__':unittest.main()
