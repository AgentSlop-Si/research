"""Independent exact finite-field brute-force tests for rank-r recognition."""
import random
import unittest
from math import comb, gcd
from phase_union_general import (phase_table, phase_eliminant, evaluate_poly,
    bounded_bm, recognize, transform_if_recognized, direct_dft, make_signal)

CASES=[(7,29,16),(17,103,72),(31,311,260),(63,127,9),(119,239,49),
       (127,509,16),(255,1021,811),(511,3067,64),(1023,4093,16)]
EVEN_CASES=[(8,17,9),(12,13,2),(16,17,3),(24,73,52),(32,97,28),(36,37,2),
            (48,97,25),(60,61,2),(64,193,125),(80,241,102),(96,97,5),
            (100,101,2),(120,241,49),(128,257,9),(192,193,5),(256,257,3),
            (512,7681,7146),(1024,12289,10302)]

class TestPhaseUnionGeneral(unittest.TestCase):
    def test_exact_root_orders(self):
        for n,p,w in CASES+EVEN_CASES:self.assertEqual(len(phase_table(n,p,w)),n)
        with self.assertRaises(ValueError):phase_table(17,103,1)

    def test_const_term_and_polynomial_root(self):
        rng=random.Random(1010)
        for r in (1,2,3,4,5):
            n,p,w=next((n,p,w) for n,p,w in CASES if n>=3*r)
            roots=phase_table(n,p,w)
            for _ in range(12):
                a=rng.randrange(n)
                modes=[(b,rng.randrange(1,p)) for b in rng.sample(range(n),r)]
                x=make_signal(n,p,w,a,modes)
                center=next(j for j in range(r,n-r) if x[j])
                pol=phase_eliminant(x,center-r,r,p)
                self.assertEqual(len(pol),comb(r+2,3)+1)
                expected=(-1 if (r*(r+1)//2)%2 else 1)*pow(x[center],r+1,p)%p
                self.assertEqual(pol[0],expected)
                self.assertEqual(evaluate_poly(pol,roots[-2*a%n],p),0)

    def test_all_quadratic_coefficients_and_ranks(self):
        rng=random.Random(2026100917)
        for r in (1,2,3,4):
            for n,p,w in CASES[:7]:
                if n<3*r:continue
                a_candidates=[0,1,n//2,7,n-1]
                if n%3==0:a_candidates += [3,n//3]
                if n%7==0:a_candidates += [7,n//7]
                for a in sorted(set(q%n for q in a_candidates)):
                    for s in range(1,r+1):
                        modes=[(b, rng.randrange(1,p)) for b in rng.sample(range(n),s)]
                        x=make_signal(n,p,w,a,modes)
                        out,cert=transform_if_recognized(x,p,w,r)
                        self.assertIsNotNone(cert,(n,r,a,s,modes))
                        self.assertEqual(out,direct_dft(x,p,w),(n,r,a,s))
                        self.assertLessEqual(cert.candidates_found,gcd(2,n)*comb(r+2,3))
                        self.assertLessEqual(len(cert.modes),r)

    def test_r5_r6_large(self):
        rng=random.Random(1717)
        for r,n,p,w in [(5,63,127,9),(5,119,239,49),(6,63,127,9),(6,119,239,49)]:
            for a in (0,1,7,21):
                modes=[(b,rng.randrange(1,p)) for b in rng.sample(range(n),r)]
                x=make_signal(n,p,w,a,modes)
                out,cert=transform_if_recognized(x,p,w,r)
                self.assertIsNotNone(cert,(r,n,a))
                self.assertEqual(out,direct_dft(x,p,w),(r,n,a))

    def test_growth_and_many_roots(self):
        rng=random.Random(7733)
        for n,p,w in CASES[-4:]:
            for r in (2,3,4):
                modes=[(b,rng.randrange(1,p)) for b in rng.sample(range(n),r)]
                x=make_signal(n,p,w,n//3,modes)
                out,cert=transform_if_recognized(x,p,w,r)
                self.assertIsNotNone(cert,(r,n))
                roots=phase_table(n,p,w)
                for k in [0,1,n//2,n-1,13]:
                    self.assertEqual(out[k],sum(x[j]*roots[-k*j%n] for j in range(n))%p,(n,r,k))

    def test_random_noise_no_false_certificates(self):
        rng=random.Random(171717)
        for r in (1,2,3,4):
            for n,p,w in CASES[:6]:
                if n<3*r:continue
                for _ in range(12):
                    x=[rng.randrange(p) for _ in range(n)]
                    self.assertIsNone(recognize(x,p,w,r))

    def test_every_even_n_and_nonunit_phase(self):
        rng=random.Random(20261009)
        for n,p,w in EVEN_CASES:
            for r in (1,2,3,4,5):
                if n<3*r:continue
                a_candidates=[0,1,n-1,n//2]
                a_candidates += [q for q in (2,3,4,6,8,12,16,24,32,64) if q<n and gcd(q,n)>1]
                for a in sorted(set(a_candidates)):
                    s=rng.randrange(1,r+1)
                    modes=[(b,rng.randrange(1,p)) for b in rng.sample(range(n),s)]
                    x=make_signal(n,p,w,a,modes)
                    out,cert=transform_if_recognized(x,p,w,r)
                    self.assertIsNotNone(cert,(n,p,r,a,modes))
                    self.assertLessEqual(cert.candidates_found,gcd(2,n)*comb(r+2,3))
                    if n<=256:
                        self.assertEqual(out,direct_dft(x,p,w),(n,r,a))
                    else:
                        roots=phase_table(n,p,w)
                        for k in (0,1,2,n//2,n-1):
                            self.assertEqual(out[k],sum(x[j]*roots[-k*j%n] for j in range(n))%p,(n,r,a,k))

    def test_bm_limited_and_zero_edges(self):
        n,p,w=63,127,9
        roots=phase_table(n,p,w)
        for r in (1,2,3,4,5):
            x=[0]*n;x[0]=1
            self.assertIsNone(recognize(x,p,w,r))
            self.assertEqual(transform_if_recognized([0]*n,p,w,r)[0],[0]*n)
            x=make_signal(n,p,w,0,[(j+1,2+j) for j in range(r)])
            C=bounded_bm(x,p,r)
            self.assertIsNotNone(C)
            self.assertEqual(len(C),r+1)
        noise=[0]*n
        noise[n//2]=1
        self.assertIsNone(bounded_bm(noise,p,2))

if __name__=='__main__':unittest.main()
