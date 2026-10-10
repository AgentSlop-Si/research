from __future__ import annotations
import unittest,sys,json,random,cmath
from pathlib import Path
import numpy as np
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
sys.path.insert(0,str(BASE.parent/'fft_green_phase40_four_middle'))
from phase41_phase_geometry import dense_cycle_green,distinct_quotients,signatures,blaschke_template
from phase41_exact_jacobian import exact_case,log_jac,PRIMES,sqrt_minus_one,chord_spec,dense_green
from phase40_holonomy import random_problem,normalize_gauge
from phase41_unit_holonomy import model,ratios_and_jac,fit,four_target
from phase41_three_exact import certify as three_exact_certify
from phase41_arbitrary_amplitude import full_jac as arbitrary_gain_full_jac
from phase41_full_audit import compare as compare_syntheses

class Phase41Tests(unittest.TestCase):
    def test_single_cycle_flat_and_two_ratios(self):
        for n in (8,16,32):
            rng=random.Random(41+n)
            c1=list(range(n));c2=list(range(n));rng.shuffle(c2)
            for c in (c1,c2):
                ws=[cmath.exp(1j*.3+1j*2*rng.random()) for _ in range(n)]
                G=dense_cycle_green(c,ws)
                assert abs(sum(0 for _ in ws)) == 0
                mags=[abs(G[i][j]) for i in range(n) for j in range(n)]
                self.assertLess(max(mags)-min(mags),1e-10)
                for a,b in ((0,1),(n//2,n//2+1),(1,n-1)):
                    _,q=distinct_quotients(G,a,b)
                    self.assertLessEqual(len(q),2)
    def test_two_cycle_signature_bound(self):
        for n in (8,16,32):
            rng=random.Random(21+n)
            c1=list(range(n));c2=list(range(n));rng.shuffle(c2)
            gs=[]
            for c in (c1,c2):
                w=[cmath.exp(1j*(rng.uniform(-2,2))) for _ in range(n)]
                gs.append(dense_cycle_green(c,w))
            for a,b in ((0,1),(1,n-1)):
                groups=signatures(gs[0],gs[1],a,b)
                self.assertLessEqual(len(groups),4)
    def test_gaussian_rational_phase_jacobian(self):
        for n in (8,16,32,64):
            c=exact_case(n,k=4)
            self.assertEqual(list(c['real_jacobian_ranks'].values()),[6,6])
            self.assertTrue(all(c['modular_determinants'].values()))
    def test_lower_windows_jacobian(self):
        for n in (8,16):
            for k in (2,3):
                c=exact_case(n,k=k)
                self.assertEqual(list(c['real_jacobian_ranks'].values()),[k+2,k+2])
    def test_numerical_derivative_independent_fd(self):
        for n in (8,16):
            cycles,edges,chords=model(n)
            theta=np.random.default_rng(n+191).uniform(-2,2,len(chords))
            R,J=ratios_and_jac(n,theta,edges,chords)
            for d in (0,min(3,len(chords)-1)):
                eps=1e-6;dt=np.zeros(len(chords));dt[d]=eps
                FD=(ratios_and_jac(n,theta+dt,edges,chords)[0]-ratios_and_jac(n,theta-dt,edges,chords)[0])/(2*eps)
                self.assertLess(max(abs(FD-J[:,d])),1e-7)
            self.assertEqual(np.linalg.matrix_rank(np.r_[J.real,J.imag],tol=1e-8),6)
    def test_fourier_has_more_than_eight_distinct_row_ratios(self):
        for n in (16,32,64):
            om=pow(3,(998244353-1)//n,998244353)
            self.assertEqual(len({pow(om,j,998244353) for j in range(n)}),n)
    def test_local_nonunit_escape(self):
        for n in (16,32,64,256):
            d=blaschke_template(n)
            self.assertLess(d['max_target_error'],2e-12)
            self.assertLess(d['max_modulus_error'],2e-12)
    def test_three_unitary_cycle_full_local_jacobian(self):
        for n in (8,16,32,64):
            case=three_exact_certify(n)
            self.assertEqual(list(case['exact_real_jacobian_rank'].values()),[2*n-2,2*n-2])
            self.assertTrue(all(case['nonzero_minor_mod_two_primes'].values()))
    def test_two_arbitrary_gain_cycles_all_two_row_jacobian(self):
        for n in (8,16,32,64):
            for p in (998244353,2013265921):
                data=arbitrary_gain_full_jac(n,p)
                self.assertEqual(data['jacobian_rank'],n-1)
    def test_numerical_full_two_row_controls_still_fail_third_row(self):
        for n in (8,16,32):
            for kind in ('two_arbitrary_gain_cycles','three_unit_cycles'):
                data=compare_syntheses(n,kind)
                self.assertLess(data['two_row_max_entry_error'],1e-9)
                self.assertGreater(data['third_row_max_entry_error'],.1)
    def test_two_phase_targets_numerical_control(self):
        for n in (8,16):
            record=json.loads((BASE/f'phase41_two_target_fit_N{n}.json').read_text())
            cycles,edges,chords=model(n)
            z,J=ratios_and_jac(n,np.asarray(record['theta']),edges,chords,2)
            self.assertLess(float(np.max(np.abs(z-four_target(n)[:2]))),5e-10)

if __name__=='__main__':unittest.main()
