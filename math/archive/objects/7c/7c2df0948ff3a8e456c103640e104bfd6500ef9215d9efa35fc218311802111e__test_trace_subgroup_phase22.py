"""Exact field tests for Phase22 Dickson trace subgroup sieve.

The oracle is independent: brute evaluate V(w+w^-1) on all Nth roots.
No prior resultant implementation is used for this oracle.
"""
import random,unittest
from annihilator_engine import RecurrenceGreen,Work,dense_from_shift_defects
from trace_subgroup import (direct_dickson,dickson_n_mod,trace_subgroup_sieve,
    shifts_from_linear_trace_gcd, modular_sqrt,discrete_logs_bsgs, shifts_from_trace_gcd_scan)
from compressed_resultant import transform_compressed_reciprocal
from rational_forcing import direct_dft_any

class TraceSubgroupTests(unittest.TestCase):
    def test_exact_Dickson_mod_polynomials(self):
        rng=random.Random(2201)
        p=2013265921
        for n in (1,2,3,4,5,7,8,13,16,30,32,45,64,128):
            for _ in range(4):
                roots=[rng.randrange(1,p) for j in range(3)]
                v=[1]
                for z in roots:
                    q=[0]*(len(v)+1)
                    for i,c in enumerate(v):
                        q[i]=(q[i]-z*c)%p;q[i+1]=(q[i+1]+c)%p
                    v=q
                res=dickson_n_mod(n,v,p,Work())
                for root in roots:
                    val=0
                    for c in reversed(res):val=(val*root+c)%p
                    self.assertEqual(val,direct_dickson(n,root,p),(n,root,v))

    def test_sieve_no_false_reject_against_brute(self):
        rng=random.Random(2202)
        for p,g,n in ((2013265921,31,16),(2013265921,31,30),
                       (2013265921,31,64),(998244353,3,32),
                       (998244353,3,128)):
            eng=RecurrenceGreen(n,p,g)
            for q in range(60):
                degree=rng.randrange(1,9)
                v=[rng.randrange(p) for _ in range(degree+1)]
                if q%3==0:
                    w=eng.powers[rng.randrange(1,n)]
                    z=(w+pow(w,-1,p))%p
                    f=[0]*(len(v)+1)
                    for j,c in enumerate(v):
                        f[j]=(f[j]-c*z)%p
                        f[j+1]=(f[j+1]+c)%p
                    v=f
                if q%13==0:
                    # Insert a spurious root w=1; the sieve removes it.
                    f=[0]*(len(v)+1)
                    for j,c in enumerate(v):
                        f[j]=(f[j]-2*c)%p
                        f[j+1]=(f[j+1]+c)%p
                    v=f
                rep=trace_subgroup_sieve(v,n,p,Work())
                brute=[]
                for i in range(1,n):
                    w=eng.powers[i]; t=(w+pow(w,-1,p))%p
                    value=0
                    for c in reversed(v):value=(value*t+c)%p
                    if value==0:brute.append(i)
                self.assertEqual(rep.possible,bool(brute),(p,n,v,rep,brute))
                if rep.gcd_degree==1:
                    actual=shifts_from_linear_trace_gcd(rep,eng,Work())
                    self.assertEqual(actual,brute,(n,v,rep))
                if rep.possible:
                    self.assertEqual(shifts_from_trace_gcd_scan(rep,eng,Work()),brute)

    def test_identity_and_negative_quadratic_cases(self):
        p=2013265921;n=128;eng=RecurrenceGreen(n,p,31)
        only_identity=trace_subgroup_sieve([-2,1],n,p,Work())
        self.assertFalse(only_identity.possible)
        both=trace_subgroup_sieve([-4,0,1],n,p,Work())
        self.assertTrue(both.possible)
        self.assertEqual(shifts_from_linear_trace_gcd(both,eng,Work()),[n//2])
        for d in (1,5,63):
            w=eng.powers[d]
            self.assertEqual(discrete_logs_bsgs({w},eng.omega,n,p,Work())[w],d)

    def test_exhaustive_gf17_quadratic_trace_polynomials(self):
        p=17;n=4;eng=RecurrenceGreen(n,p,3)
        # The 4th roots in F_17 are {1,4,-1,-4}, and nonidentity traces
        # are exactly {0,-2}. This test enumerates every nonzero quadratic.
        count=0
        for a in range(p):
            for b in range(p):
                for c in range(p):
                    if a==b==c==0:continue
                    coeff=[a,b,c]
                    report=trace_subgroup_sieve(coeff,n,p,Work())
                    oracle=(a==0 or (a-2*b+4*c)%p==0)
                    self.assertEqual(report.possible,oracle,coeff)
                    if report.possible:
                        self.assertEqual(shifts_from_trace_gcd_scan(report,eng,Work()),
                                         [k for k in (1,2,3) if (a+b*((eng.powers[k]+eng.powers[n-k])%p)+c*((eng.powers[k]+eng.powers[n-k])%p)**2)%p==0])
                    count+=1
        self.assertEqual(count,4912)

    def test_structured_and_adversarial_exact_DFTs(self):
        p=2013265921;rng=random.Random(2221)
        linear=0; rejected=0
        for n in (30,64,128,384):
            eng=RecurrenceGreen(n,p,31)
            for _ in range(8):
                d,e=rng.sample(range(1,n),2)
                u,v=rng.sample(range(n),2)
                h=[0]*n;h[u]=7;h[v]=11
                r=dense_from_shift_defects(dense_from_shift_defects(h,d,17,p),e,29,p)
                x=eng.P.solve(r)
                z,meta=transform_compressed_reciprocal(eng,x)
                self.assertEqual(z,direct_dft_any(x,eng.omega,p))
                linear+=meta['meta'].trace_linear_extracted
                if meta['meta'].trace_rejected:rejected+=1
            for _ in range(8):
                x=[rng.randrange(p) for j in range(n)]
                z,meta=transform_compressed_reciprocal(eng,x)
                self.assertEqual(z,direct_dft_any(x,eng.omega,p))
                self.assertEqual(meta['selected'],'fallback')
        self.assertGreater(linear,15)
        self.assertEqual(rejected,0)

if __name__=='__main__':unittest.main()
