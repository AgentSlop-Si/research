"""Reproducible exact Phase 39 tests; python -m unittest -v tests_phase39."""
import json
import random
import subprocess
import unittest
from pathlib import Path
import numpy as np
from phase39_bivariate import (PRIMES,build,macaulay,rank_mod,anchored_spurious,
    witness,plant_positive_control,online_apply,dense_circuit,minor_quad,MON2,weyl_defects_mod)
from create_certificates import determinant
import phase37_curvature as g

ROOT=Path(__file__).resolve().parent

class Phase39(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixtures={(n,p):build(n,p,primitive) for n in (4,8,16)
                      for p,primitive in PRIMES}

    def test_split_primes(self):
        for n in (4,8,16):
            for p,primitive in PRIMES:
                w=pow(primitive,(p-1)//n,p)
                self.assertEqual(pow(w,n,p),1)
                self.assertEqual(pow(w,n//2,p),p-1)

    def test_distinct_cycle_order_at_n8(self):
        for p,primitive in PRIMES:
            inst=self.fixtures[(8,p)]
            self.assertEqual(len({tuple(x) for x in inst['cycles']+[inst['extra_cycle']]}),7)

    def test_n4_cycle_count_limitation(self):
        for p,_ in PRIMES:
            a=self.fixtures[(4,p)]
            self.assertEqual(len({tuple(x) for x in a['cycles']}),6)
            self.assertIn(tuple(a['extra_cycle']),{tuple(x) for x in a['cycles']})

    def test_anchored_spurious_root(self):
        for n in (4,8,16):
            for p,_ in PRIMES:
                z=anchored_spurious(self.fixtures[(n,p)])
                self.assertNotEqual(z,(0,0,0))

    def test_repaired_cubic_certificate_both_primes(self):
        for n in (4,8,16):
            for p,_ in PRIMES:
                a=self.fixtures[(n,p)]
                self.assertEqual(rank_mod(macaulay(a,kind='cubic'),p),10)

    def test_repaired_quartic_certificate_both_primes(self):
        for n in (4,8,16):
            for p,_ in PRIMES:
                a=self.fixtures[(n,p)]
                self.assertEqual(rank_mod(macaulay(a,kind='quartic'),p),15)

    def test_planted_valid_rank_deficient_cubic(self):
        for n in (4,8,16):
            for p,_ in PRIMES:
                self.assertLess(plant_positive_control(self.fixtures[(n,p)])['rank3'],10)

    def test_planted_valid_rank_deficient_quartic(self):
        for n in (4,8,16):
            for p,_ in PRIMES:
                self.assertLess(plant_positive_control(self.fixtures[(n,p)])['rank4'],15)

    def test_two_coupling_polynomial_degree(self):
        for n in (4,8):
            for p,_ in PRIMES:
                a=self.fixtures[(n,p)]
                for i,j in ((0,1),(0,2),(0,3),(1,2),(1,3)):
                    self.assertEqual(len(minor_quad(a,(0,1),(0,1,2,3),i,j)),6)

    def test_apply_equals_dense_reference_identity_permutations(self):
        for n in (4,8,16):
            for p,_ in PRIMES:
                a=self.fixtures[(n,p)]
                v=[(j*j*13+7*j+3)%p for j in range(n)]
                A=dense_circuit(a)
                expected=[sum(int(A[i,j])*v[j] for j in range(n))%p for i in range(n)]
                self.assertEqual(online_apply(a,v),expected)

    def test_apply_equals_dense_reference_random_masks_and_orders(self):
        for n in (8,16):
            for p,_ in PRIMES:
                rng=random.Random(390039+n+p)
                a=self.fixtures[(n,p)]
                rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
                m1=[rng.randrange(1,p) for _ in range(n)]
                m2=[rng.randrange(1,p) for _ in range(n)]
                v=[rng.randrange(p) for _ in range(n)]
                M=dense_circuit(a,9,17,m1,m2,rp,cp)
                expected=[sum(int(M[i,j])*v[j] for j in range(n))%p for i in range(n)]
                self.assertEqual(online_apply(a,v,9,17,m1,m2,rp,cp),expected)

    def test_online_linearity(self):
        a=self.fixtures[(16,998244353)];p=a['p'];rng=random.Random(39)
        u=[rng.randrange(p) for _ in range(16)]
        v=[rng.randrange(p) for _ in range(16)]
        lam,mu=17,23
        f=online_apply(a,[(x+y)%p for x,y in zip(u,v)],lam,mu)
        fu=online_apply(a,u,lam,mu);fv=online_apply(a,v,lam,mu)
        self.assertEqual(f,[(x+y)%p for x,y in zip(fu,fv)])

    def test_negative_actual_fourier(self):
        a=self.fixtures[(8,998244353)]
        M=dense_circuit(a)
        self.assertFalse(np.array_equal(M,a['F']))

    def test_exact_fourier_weyl_controls(self):
        for n in (8,16):
            for p,primitive in PRIMES:
                a=self.fixtures[(n,p)]
                self.assertEqual(weyl_defects_mod(a['F'],p,primitive),(0,0))
                d=weyl_defects_mod(dense_circuit(a),p,primitive)
                self.assertGreater(d[0],0)
                self.assertGreater(d[1],0)

    def test_compact_minor_certificates(self):
        cert=json.loads((ROOT/'certificates.json').read_text())
        for entry in cert['results']:
            n=entry['N'];p=entry['prime']
            if n>16:continue
            a=self.fixtures[(n,p)]
            for kind,name in [('cubic','cubic'),('quartic','quartic')]:
                mat=macaulay(a,kind=kind)
                selection=entry[name]['pivot_rows']
                d=determinant([mat[i] for i in selection],p)
                self.assertEqual(d,entry[name]['determinant_mod_prime'])
                self.assertNotEqual(d,0)

    def test_native_exhaustive_small_cases(self):
        exe=ROOT/'phase39_exact_audit'
        if not exe.exists():self.skipTest('native verifier not compiled; see RUN.md')
        for n in (4,8):
            for p,_ in PRIMES:
                for mode,rank in (('cubic',10),('quartic',15)):
                    result=subprocess.run([str(exe),str(ROOT/'instances'/f'phase39_N{n}_p{p}.txt'),'0',mode],
                                          capture_output=True,text=True,check=True)
                    data=json.loads(result.stdout)
                    self.assertEqual(data['minimum_rank'],rank)
                    self.assertEqual(data['deficient'],0)
                    expected=n*(n-1)*n*(n-1)*(n-2)*(n-3)
                    self.assertEqual(data['checked'],expected)

    def test_native_planted_factorization_is_not_excluded(self):
        # An intentionally valid projective middle decomposition must destroy
        # the Macaulay full-rank certificate. Test the C++ implementation,
        # not just the Python polynomial checker.
        import tempfile
        from phase39_bivariate import export_instance
        a=self.fixtures[(8,998244353)].copy()
        p=a['p'];n=a['n']
        B=(a['B0']+7*a['B1']+11*a['B2'])%p
        left=np.array([3+j for j in range(n)],dtype=np.int64)
        right=np.array([5+3*j for j in range(n)],dtype=np.int64)
        a['T']=((left[:,None]*B)%p*right[None,:])%p
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'planted.txt';export_instance(a,path)
            for kind in ('cubic','quartic'):
                result=subprocess.run([str(ROOT/'phase39_exact_audit'),str(path),'0',kind],
                                      capture_output=True,text=True)
                self.assertEqual(result.returncode,1)
                data=json.loads(result.stdout)
                self.assertGreater(data['deficient'],0)

    def test_native_sampled_n16(self):
        exe=ROOT/'phase39_exact_audit'
        if not exe.exists():self.skipTest('native verifier not compiled; see RUN.md')
        for p,_ in PRIMES:
            out=subprocess.run([str(exe),str(ROOT/'instances'/f'phase39_N16_p{p}.txt'),'0','quartic','1000'],
                               capture_output=True,text=True,check=True)
            rec=json.loads(out.stdout)
            self.assertEqual(rec['checked'],1000)
            self.assertEqual(rec['minimum_rank'],15)

if __name__=='__main__':unittest.main()
