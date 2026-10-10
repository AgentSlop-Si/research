"""Independent exact tests of Phase21 reciprocal rational graph recovery."""
import random
import unittest
from annihilator_engine import RecurrenceGreen,dense_from_shift_defects
from rational_forcing import direct_dft_any
from reciprocal_union import (discover_reciprocal_union, transform_reciprocal_union,
                              factor_four_tap_rectangle)

P=2013265921

def example(n,d,e,u,v,a=17,b=29,hu=7,hv=11,p=P):
    h=[0]*n;h[u]=hu;h[v]=hv
    r=dense_from_shift_defects(dense_from_shift_defects(h,d,a,p),e,b,p)
    return r,h

class ReciprocalPhase21(unittest.TestCase):
    def test_two_hidden_filters_two_hidden_defects(self):
        for n,d,e,u,v in [(30,7,13,3,16),(64,13,29,3,33),
                          (128,31,53,3,65),(384,191,121,3,193)]:
            eng=RecurrenceGreen(n,P,31)
            r,h=example(n,d,e,u,v)
            x=eng.P.solve(r)
            y,meta=transform_reciprocal_union(eng,x)
            self.assertEqual(y,direct_dft_any(x,eng.omega,P))
            self.assertEqual(meta['selected'],'reciprocal-blind-sparse-rational')
            self.assertEqual(meta['discovery'].full_certificate_entries,n)
            self.assertEqual(meta['discovery'].short_rank,4)
            factors=meta['graph_factors']
            self.assertIsNotNone(factors)
            self.assertEqual(len(factors['defects']),2)
            rd=r[:]
            for shift,alpha in zip(factors['shifts'],factors['multipliers']):
                rd=[(rd[j]-alpha*rd[(j-shift)%n])%P for j in range(n)]
            hz=[0]*n
            for j,vv in factors['defects'].items():hz[j]=vv
            self.assertEqual(rd,hz)

    def test_random_parameter_sweep(self):
        rng=random.Random(2101)
        for n in (30,64,128):
            eng=RecurrenceGreen(n,P,31)
            count=0
            for _ in range(14):
                d,e=rng.sample(range(1,n),2)
                u,v=rng.sample(range(n),2)
                a,b=rng.sample(range(3,200),2)
                r,h=example(n,d,e,u,v,a,b)
                x=eng.P.solve(r)
                y,meta=transform_reciprocal_union(eng,x)
                self.assertEqual(y,direct_dft_any(x,eng.omega,P))
                if meta['selected'].startswith('reciprocal'):
                    count+=1
            self.assertGreaterEqual(count,8,(n,count))

    def test_generic_random_fallback(self):
        rng=random.Random(210101)
        for n in (30,64,128):
            eng=RecurrenceGreen(n,P,31)
            for _ in range(3):
                x=[rng.randrange(P) for _ in range(n)]
                y,meta=transform_reciprocal_union(eng,x)
                self.assertEqual(y,direct_dft_any(x,eng.omega,P))
                self.assertEqual(meta['selected'],'fallback')

    def test_unchanged_sixteen_probes_attack(self):
        eng=RecurrenceGreen(64,P,31)
        r,_=example(64,13,29,3,33)
        # Add a nonzero polynomial Delta(z)=prod_{k=0}^15(z-omega^k),
        # so the first 16 Fourier coefficients are exactly unchanged.
        poly=[1]
        for k in range(16):
            nxt=[0]*(len(poly)+1)
            for j,c in enumerate(poly):
                nxt[j]=(nxt[j]-c*eng.powers[k])%P
                nxt[j+1]=(nxt[j+1]+c)%P
            poly=nxt
        corrupted=r[:]
        for j,c in enumerate(poly):corrupted[j]=(corrupted[j]+c)%P
        self.assertNotEqual(corrupted,r)
        for k in range(16):
            wk=eng.powers[k]
            def dot(z):return sum(v*pow(wk,j,P) for j,v in enumerate(z))%P
            self.assertEqual(dot(r),dot(corrupted))
        found,meta=discover_reciprocal_union(corrupted,eng)
        self.assertIsNone(found)
        self.assertGreaterEqual(meta.full_certificates,1)
        x=eng.P.solve(corrupted)
        y,m=transform_reciprocal_union(eng,x)
        self.assertEqual(m['selected'],'fallback')
        self.assertEqual(y,direct_dft_any(x,eng.omega,P))

    def test_zero_fourier_probe_safe_fallback(self):
        eng=RecurrenceGreen(64,P,31)
        r,_=example(64,13,29,0,1,hu=1,hv=P-1)
        x=eng.P.solve(r)
        y,meta=transform_reciprocal_union(eng,x)
        self.assertEqual(meta['selected'],'fallback')
        self.assertEqual(meta['discovery'].reason,'one-of-16-Fourier-probes-vanishes')
        self.assertEqual(y,direct_dft_any(x,eng.omega,P))

    def test_one_or_no_input(self):
        eng=RecurrenceGreen(64,P,31)
        for x in ([0]*64,[1]+[0]*63):
            y,meta=transform_reciprocal_union(eng,x)
            self.assertEqual(y,direct_dft_any(x,eng.omega,P))

    def test_nonunique_rectangle_is_reported_only_as_a_valid_factorization(self):
        eng=RecurrenceGreen(64,P,31)
        r,h=example(64,13,29,3,33)
        A,delta,alpha,_=discover_reciprocal_union(r,eng)[0]
        fact=factor_four_tap_rectangle(A,delta,alpha,64,P)
        self.assertIsNotNone(fact)
        self.assertEqual(len(fact['shifts']),2)

if __name__=='__main__':unittest.main()
