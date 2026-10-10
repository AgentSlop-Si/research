"""Independent exact tests of fully blind sparse circular inversion."""
import unittest,random
from math import gcd
from types import SimpleNamespace
from blind_inverse import RecurrenceGreen,discover_sparse_circular_inverse
from annihilator_engine import dense_from_shift_defects,far_coprime_shift
from rational_forcing import direct_dft_any

CASES=[(998244353,3,7),(998244353,3,17),
       (2013265921,31,30),(2013265921,31,60),
       (2013265921,31,128),(2013265921,31,384)]

def inverse_dft(y,e):
    n,p=e.n,e.p
    invn=pow(n,-1,p)
    return [sum(y[k]*pow(e.omega,(-k*j)%n,p) for k in range(n))%p*invn%p
            for j in range(n)]

def make_r_from_sparse_inverse(C,e):
    n,p=e.n,e.p
    values=[]
    for z in e.powers:
        val=sum(c*pow(z,j,p) for j,c in C.items())%p
        if val==0:raise ValueError('chosen polynomial singular')
        values.append(pow(val,-1,p))
    r=inverse_dft(values,e)
    # Independent circular certificate, not using recovery routine.
    for j in range(n):
        assert sum(c*r[(j-t)%n] for t,c in C.items())%p==(1 if j==0 else 0)
    return r

class BlindInverseTests(unittest.TestCase):
    def test_single_unknown_factor_and_location(self):
        for p,g,n in CASES:
            e=RecurrenceGreen(n,p,g)
            d=far_coprime_shift(n)
            for j in (0,n//3,n-1):
                h=[0]*n;h[j]=9
                r=dense_from_shift_defects(h,d,2,p)
                x=e.P.solve(r)
                y,m=e.transform_blind_inverse(x,min(4,n//2))
                self.assertEqual(y,direct_dft_any(x,e.omega,p))
                self.assertEqual(m['selected'],'blind-sparse-circular-inverse')
                self.assertEqual(m['inverse_support'],2)
                self.assertEqual(m['inverse_certificate'].certificate_entries_checked,n)

    def test_two_totally_unknown_factors_and_location(self):
        for p,g,n in CASES:
            if n<8:continue
            e=RecurrenceGreen(n,p,g)
            d1,d2=far_coprime_shift(n),n-1
            h=[0]*n;h[n//3]=11
            intermediate=dense_from_shift_defects(h,d2,3,p)
            r=dense_from_shift_defects(intermediate,d1,2,p)
            self.assertTrue(all(r) and all(intermediate))
            self.assertTrue(all((r[j]-2*r[(j-d1)%n])%p for j in range(n)))
            self.assertTrue(all((r[j]-3*r[(j-d2)%n])%p for j in range(n)))
            x=e.P.solve(r)
            y,m=e.transform_blind_inverse(x,4)
            self.assertEqual(y,direct_dft_any(x,e.omega,p))
            self.assertEqual(m['selected'],'blind-sparse-circular-inverse')
            self.assertEqual(m['inverse_support'],4)
            self.assertEqual(m['inverse_certificate'].certificate_entries_checked,n)

    def test_three_unknown_factors(self):
        for p,g,n in [(2013265921,31,60),(2013265921,31,128),
                      (2013265921,31,384)]:
            e=RecurrenceGreen(n,p,g)
            delays=[far_coprime_shift(n),n-1,1]
            alphas=[2,3,5]
            h=[0]*n;h[n//3]=11
            r=h
            for d,a in zip(delays,alphas):
                r=dense_from_shift_defects(r,d,a,p)
            x=e.P.solve(r)
            y,m=e.transform_blind_inverse(x,8)
            self.assertEqual(y,direct_dft_any(x,e.omega,p))
            self.assertEqual(m['selected'],'blind-sparse-circular-inverse')
            self.assertLessEqual(m['inverse_support'],8)

    def test_sparse_inverse_not_factored_as_binomials(self):
        for p,g,n in [(2013265921,31,30),(2013265921,31,128)]:
            e=RecurrenceGreen(n,p,g)
            taps={2:2,7:3,n//2:5,n-1:7}
            r=make_r_from_sparse_inverse(taps,e)
            x=e.P.solve(r)
            y,m=e.transform_blind_inverse(x,5)
            self.assertEqual(y,direct_dft_any(x,e.omega,p))
            self.assertEqual(m['selected'],'blind-sparse-circular-inverse')
            self.assertEqual(m['inverse_taps'],taps)

    def test_adversarial_same_first_probes_full_certificate_rejects(self):
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        h=[0]*n;h[7]=13
        r=dense_from_shift_defects(h,far_coprime_shift(n),2,p)
        r=dense_from_shift_defects(r,n-1,3,p)
        # This adversarial change alters *none* of the first eight Fourier
        # samples used for the 4-tap candidate, but changes another bin.
        k0=8
        invn=pow(n,-1,p)
        mutant=[(r[j]+invn*pow(e.omega,(-k0*j)%n,p))%p for j in range(n)]
        for k in range(8):
            self.assertEqual(direct_dft_any(r,e.omega,p)[k],
                             direct_dft_any(mutant,e.omega,p)[k])
        x=e.P.solve(mutant)
        y,m=e.transform_blind_inverse(x,4)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(m['selected'],'fallback')
        self.assertEqual(m['inverse_certificate'].fallback_reason,
                         'full-convolution-certificate-failed')
        self.assertIsNotNone(m['inverse_certificate'].certificate_failed_at)

    def test_zero_fourier_probe_and_generic_fallback(self):
        rng=random.Random(5010)
        for p,g,n in CASES:
            e=RecurrenceGreen(n,p,g)
            r=[0]*n;r[0]=1;r[1]=p-1
            x=e.P.solve(r)
            y,m=e.transform_blind_inverse(x,min(4,n//2))
            self.assertEqual(y,direct_dft_any(x,e.omega,p))
            self.assertEqual(m['selected'],'fallback')
            self.assertEqual(m['inverse_certificate'].fallback_reason,'zero-Fourier-probe')
            x=[rng.randrange(1,p) for _ in range(n)]
            y,m=e.transform_blind_inverse(x,4)
            self.assertEqual(y,direct_dft_any(x,e.omega,p))
            self.assertEqual(m['selected'],'fallback')

    def test_single_impulse_and_zero_coordinates(self):
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        r=[0]*n;r[17]=23
        x=e.P.solve(r)
        y,m=e.transform_blind_inverse(x,4)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(m['selected'],'blind-sparse-circular-inverse')
        self.assertEqual(m['inverse_support'],1)

    def test_repeated_spectral_nodes_no_false_certificate(self):
        p,g,n=2013265921,31,128
        e=RecurrenceGreen(n,p,g)
        # Near-collinear false fit or no root-group membership must fall back.
        r=[(j*j*j+31*j+19)%p for j in range(n)]
        x=e.P.solve(r)
        y,m=e.transform_blind_inverse(x,4)
        self.assertEqual(y,direct_dft_any(x,e.omega,p))
        self.assertEqual(m['selected'],'fallback')

if __name__=='__main__':unittest.main(verbosity=2)
