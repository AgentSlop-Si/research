import random,unittest
from math import gcd
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from hybrid_phase20 import transform_hybrid_phase20
from rational_forcing import direct_dft_any

class Phase20HybridTests(unittest.TestCase):
    def test_shared_eight_spectral_probes_resonance(self):
        p,n=2013265921,128;e=RecurrenceGreen(n,p,31)
        d=63;a=pow(e.omega,9,p)
        r=[0]*n
        for t in range(n):r[(t*d)%n]=pow(a,t,p)*(3 if t<17 else 5)%p
        x=e.P.solve(r)
        y,m=transform_hybrid_phase20(e,x)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(m['selected'],'phase20-blind-two-defect')
        self.assertEqual(m['phase19_inverse'].sample_count,8)
        self.assertEqual(m['phase20_resultant'].probes,8)
        self.assertEqual(m['work'].repaired,9)  # 8 shared + one singular repair

    def test_old_inverse_branch_unchanged(self):
        p,n=2013265921,128;e=RecurrenceGreen(n,p,31)
        h=[0]*n;h[11]=7
        r=dense_from_shift_defects(dense_from_shift_defects(h,43,2,p),n-1,3,p)
        x=e.P.solve(r)
        y,m=transform_hybrid_phase20(e,x)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(m['selected'],'phase19-blind-inverse')
        self.assertIsNone(m['phase20_resultant'])

    def test_old_ratio_branch_unchanged(self):
        p,n=2013265921,128;e=RecurrenceGreen(n,p,31)
        h=[0]*n;h[11]=7;h[37]=9
        r=dense_from_shift_defects(h,31,2,p)
        x=e.P.solve(r)
        y,m=transform_hybrid_phase20(e,x)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(m['selected'],'phase19-blind-ratio')

    def test_generic_fallback(self):
        p,n=2013265921,128;e=RecurrenceGreen(n,p,31)
        rr=random.Random(2002)
        x=[rr.randrange(1,p) for _ in range(n)]
        y,m=transform_hybrid_phase20(e,x)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(m['selected'],'fallback')

if __name__=='__main__':unittest.main()
