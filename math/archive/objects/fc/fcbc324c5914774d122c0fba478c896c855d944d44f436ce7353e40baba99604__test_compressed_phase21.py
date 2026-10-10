"""Exact theorem/certificate tests for the proved reciprocal-resultant reduction."""
import random, unittest
from math import comb
from annihilator_engine import (RecurrenceGreen,dense_from_shift_defects,
    direct_one_frequency, batch_inverse_nonzero,Work)
from rational_forcing import direct_dft_any
from reciprocal_resultant import transform_resultant_reciprocal
from compressed_resultant import (transform_compressed_reciprocal,compressed_U_from_inverse_probes,
                                   charged_pow,eval_horner)
from resultant_pattern import find_resultant_coeff,res_at

P=2013265921

def evaluate(coeff,w,p):
    v=0
    for c in reversed(coeff):v=(v*w+c)%p
    return v

class CompressedTheorem(unittest.TestCase):
    def test_universal_reciprocity_all_orders_1_to_6(self):
        rng=random.Random(21067)
        for s in range(1,7):
            T=[rng.randrange(1,P) for _ in range(4*s)]
            m=s+1;D=m*m*(2*m-1)
            v=s*(s+1)*(4*s+5)//6
            q=m*m; b=s*(s+1)*(2*s+1)//6
            data,poly,red=find_resultant_coeff(T,P,s)
            self.assertEqual(data['degree'],D-v)
            self.assertEqual(data['zero_factor'],v)
            self.assertEqual(data['one_factor'],q)
            self.assertEqual(data['reduced_degree'],2*b)
            self.assertTrue(data['palindromic'])
            sign=-1 if (m*m)%2 else 1
            for j in range(D+1):
                lo=poly[j] if j<len(poly) else 0
                hi=poly[D-j] if D-j<len(poly) else 0
                self.assertEqual(lo,sign*hi%P,(s,j))
            # Construct U via just (b+1) samples and check actual full polynomial.
            U,meta=compressed_U_from_inverse_probes(T,P,s,Work())
            self.assertEqual(len(U),2*b+1)
            self.assertEqual(U,red)
            for w in (2,11,77,123,977):
                lhs=res_at(T,w,P,Work(),s)
                rhs=pow(w,v,P)*pow(w-1,q,P)*evaluate(U,w,P)%P
                self.assertEqual(lhs,rhs,(s,w))

    def test_compressed_matches_full_resultant_for_hidden_filters(self):
        rng=random.Random(212121)
        for n in (30,64,128,384):
            eng=RecurrenceGreen(n,P,31)
            for _ in range(5):
                d,e=rng.sample(range(1,n),2)
                u,v=rng.sample(range(n),2)
                h=[0]*n;h[u]=7;h[v]=11
                r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,P),e,29,P)
                x=eng.P.solve(r)
                y,m=transform_compressed_reciprocal(eng,x,s=4)
                z,m2=transform_resultant_reciprocal(eng,x,max_terms=4)
                direct=direct_dft_any(x,eng.omega,P)
                self.assertEqual(y,direct)
                self.assertEqual(z,direct)
                if m['selected']!='fallback':
                    self.assertEqual(m['meta'].full_certificate_entries,n)

    def test_compressed_three_unknown_filters(self):
        n=64;eng=RecurrenceGreen(n,P,31)
        h=[0]*n;h[4]=7;h[35]=11
        r=h[:]
        for d,a in [(5,17),(11,29),(19,41)]:
            r=dense_from_shift_defects(r,d,a,P)
        x=eng.P.solve(r)
        y,m=transform_compressed_reciprocal(eng,x,s=8)
        self.assertEqual(y,direct_dft_any(x,eng.omega,P))
        self.assertEqual(m['selected'],'compressed-reciprocal-certified')
        self.assertIsNotNone(m['graph_factors'])
        self.assertEqual(len(m['graph_factors']['shifts']),3)
        self.assertEqual(len(m['graph_factors']['defects']),2)

    def test_compressed_handles_generic_and_probe_attack(self):
        eng=RecurrenceGreen(64,P,31)
        rng=random.Random(1881)
        for _ in range(4):
            x=[rng.randrange(P) for _ in range(64)]
            y,m=transform_compressed_reciprocal(eng,x)
            self.assertEqual(y,direct_dft_any(x,eng.omega,P))
            self.assertEqual(m['selected'],'fallback')
        h=[0]*64;h[3]=7;h[33]=11
        r=dense_from_shift_defects(dense_from_shift_defects(h,13,17,P),29,29,P)
        poly=[1]
        for k in range(16):
            w=eng.powers[k];tmp=[0]*(len(poly)+1)
            for j,c in enumerate(poly):
                tmp[j]=(tmp[j]-w*c)%P
                tmp[j+1]=(tmp[j+1]+c)%P
            poly=tmp
        for j,c in enumerate(poly):r[j]=(r[j]+c)%P
        x=eng.P.solve(r)
        y,m=transform_compressed_reciprocal(eng,x)
        self.assertEqual(y,direct_dft_any(x,eng.omega,P))
        self.assertEqual(m['selected'],'fallback')
        self.assertGreater(m['meta'].full_certificates,0)

if __name__=='__main__':unittest.main()
