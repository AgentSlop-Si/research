"""Independent tests for Phase23 shorter Fourier prefix and full certificates."""
import random,unittest
from annihilator_engine import (RecurrenceGreen, Work, direct_one_frequency,
    dense_from_shift_defects)
from short_probe_fusion import (prefix_fourier_stream,discover_short_probe,
    transform_short_probe)
from compressed_resultant import transform_compressed_reciprocal
from rational_forcing import direct_dft_any

class ShortProbeTests(unittest.TestCase):
    def test_streaming_prefix_independent_naive(self):
        rng=random.Random(23001)
        for p,g,n in ((2013265921,31,30),(2013265921,31,128),
                        (998244353,3,64),(998244353,3,128)):
            eng=RecurrenceGreen(n,p,g)
            for m in (1,2,6,10,16):
                for _ in range(3):
                    r=[rng.randrange(p) for j in range(n)]
                    w=Work()
                    actual=prefix_fourier_stream(r,eng.powers,m,p,w)
                    expected=[direct_one_frequency(r,eng.powers[k],p) for k in range(m)]
                    self.assertEqual(actual,expected)
                    self.assertEqual(w.multiplies,n*(m-1))
                    self.assertEqual(w.additions,n*m)

    def test_joint_resultant_matches_independent_pencils(self):
        from resultant_pattern import res_at
        from joint_pencil import shared_res_at
        rng=random.Random(23007)
        p=2013265921
        for s in (2,3,4):
            for _ in range(25):
                t=[rng.randrange(p) for k in range(2*s+2)]
                w=rng.randrange(2,p)
                a=Work();b=Work()
                self.assertEqual(res_at(t,w,p,a,s),shared_res_at(t,w,p,b,s))
                self.assertLess(b.arithmetic(),a.arithmetic())

    def test_structured_two_hidden_factors_and_exact_DFT(self):
        rng=random.Random(23002)
        for p,g,n in ((2013265921,31,30),(2013265921,31,64),
                      (2013265921,31,128),(2013265921,31,384),
                      (998244353,3,64),(998244353,3,128)):
            e=RecurrenceGreen(n,p,g)
            successful=0
            for _ in range(6):
                d,z=rng.sample(range(1,n),2)
                positions=rng.sample(range(n),2)
                h=[0]*n
                for j,v in zip(positions,(7,11)):
                    h[j]=v
                r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,p),z,29,p)
                x=e.P.solve(r)
                y,meta=transform_short_probe(e,x)
                self.assertEqual(y,direct_dft_any(x,e.omega,p),
                                 (p,n,d,z,meta['meta']))
                successful+=(meta['selected']=='short-prefix-certified')
            self.assertGreater(successful,0,(p,n))

    def test_generic_random_exact_fallback(self):
        rng=random.Random(23003)
        for n in (30,64,128,384):
            e=RecurrenceGreen(n,2013265921,31)
            for _ in range(3):
                x=[rng.randrange(e.p) for j in range(n)]
                y,meta=transform_short_probe(e,x)
                self.assertEqual(y,direct_dft_any(x,e.omega,e.p))
                self.assertEqual(meta['selected'],'fallback')

    def test_adversarial_identical_ten_probes(self):
        p=2013265921;n=128
        e=RecurrenceGreen(n,p,31)
        h=[0]*n;h[4]=7;h[55]=11
        r=dense_from_shift_defects(dense_from_shift_defects(h,43,17,p),61,29,p)
        m=10
        k0=19
        rbad=[(r[j]+pow(e.powers[k0],-j,p))%p for j in range(n)]
        a=prefix_fourier_stream(r,e.powers,m,p)
        b=prefix_fourier_stream(rbad,e.powers,m,p)
        self.assertEqual(a,b)
        self.assertNotEqual(r,rbad)
        x=e.P.solve(rbad)
        out,info=transform_short_probe(e,x)
        self.assertEqual(out,direct_dft_any(x,e.omega,p))
        self.assertEqual(info['selected'],'fallback')
        self.assertGreater(info['meta'].cyclic_checks,0)
        self.assertGreater(info['meta'].failed_certificates,0)

    def test_inherited_phase22_comparison(self):
        p=2013265921;n=384
        e=RecurrenceGreen(n,p,31)
        h=[0]*n;h[15]=7;h[n-19]=11
        r=dense_from_shift_defects(dense_from_shift_defects(h,119,17,p),191,29,p)
        x=e.P.solve(r)
        old,stats_old=transform_compressed_reciprocal(e,x)
        new,stats_new=transform_short_probe(e,x)
        self.assertEqual(old,new)
        self.assertEqual(new,direct_dft_any(x,e.omega,p))
        self.assertEqual(stats_new['selected'],'short-prefix-certified')
        self.assertLess(stats_new['work'].arithmetic(),stats_old['work'].arithmetic())

    def test_zero_probe_fallback(self):
        p=2013265921;n=64;e=RecurrenceGreen(n,p,31)
        # r=all ones => all nonzero-frequency probes vanish.
        r=[1]*n;x=e.P.solve(r)
        y,meta=transform_short_probe(e,x)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(meta['selected'],'fallback')
        self.assertEqual(meta['meta'].reason,'zero-Fourier-probe')

if __name__=='__main__':unittest.main()
