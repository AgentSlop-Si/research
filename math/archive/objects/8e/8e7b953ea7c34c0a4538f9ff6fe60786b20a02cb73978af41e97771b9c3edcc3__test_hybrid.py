import unittest,random
from hybrid_engine import RecurrenceGreen
from annihilator_engine import dense_from_shift_defects,far_coprime_shift
from rational_forcing import direct_dft_any

class HybridTests(unittest.TestCase):
    def test_hybrid_three_families_and_generic(self):
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        d1,d2=far_coprime_shift(n),n-1
        one=[0]*n;one[13]=7
        two=[0]*n;two[13]=7;two[53]=11
        for name,r,branch in [
            ('one',dense_from_shift_defects(one,d1,2,p),'blind-graph'),
            ('two',dense_from_shift_defects(two,d1,2,p),'blind-graph'),
            ('twofactor',dense_from_shift_defects(dense_from_shift_defects(one,d1,2,p),d2,3,p),'blind-sparse-inverse'),
            ('generic',[random.Random(100+j).randrange(1,p) for j in range(n)],'fallback')]:
            with self.subTest(name=name):
                x=e.P.solve(r)
                y,m=e.transform_phase19_hybrid(x)
                self.assertEqual(y,direct_dft_any(x,e.omega,p))
                self.assertEqual(m['selected'],branch)
    def test_hybrid_mutation_adversarial(self):
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        d=far_coprime_shift(n)
        h=[0]*n;h[15]=11
        r=dense_from_shift_defects(dense_from_shift_defects(h,d,2,p),n-1,3,p)
        omega=e.omega;invn=pow(n,-1,p)
        r2=[(r[j]+invn*pow(omega,-9*j%n,p))%p for j in range(n)]
        y,m=e.transform_phase19_hybrid(e.P.solve(r2))
        self.assertEqual(y,direct_dft_any(e.P.solve(r2),omega,p))
        self.assertEqual(m['selected'],'fallback')

if __name__=='__main__':unittest.main(verbosity=2)
