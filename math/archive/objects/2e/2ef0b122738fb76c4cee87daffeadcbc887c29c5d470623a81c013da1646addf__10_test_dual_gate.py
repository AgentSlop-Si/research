"""Independent regression suite for exact Fourier dual-support / onion charts."""
import hashlib
import json
from pathlib import Path
import unittest
import numpy as np
from dual_support import test_mod,P8,primitive_root,constraints
from dual_sparse_polynomials import construct_dual,modular_validation
from general_onion import verify,build
from onion_peel import build_onion
from exception_s1 import witness
from inverse_quartic import rankmod,invert_mod

HERE=Path(__file__).resolve().parent
class GateTests(unittest.TestCase):
    def test_two_sided_n8_and_n16_mod(self):
        for n in (8,16):
            for p in (12289,65537):
                stats=test_mod(n,p,6,2026+p+n)
                self.assertEqual(stats['checked'],6)
                self.assertEqual(stats['variables'],2*n)

    def test_20_symbolic_equations_and_10_zero_polynomials(self):
        remain,Bhat,S,D,extra=construct_dual()
        self.assertEqual(len(remain),20)
        self.assertTrue(all(bool(poly) for _,poly in remain))
        saved=json.loads((HERE/'dual_twenty_equations.json').read_text())
        self.assertEqual(len(saved['equations']),20)
        self.assertEqual(saved['summary']['max_degree'],9)
        self.assertEqual(saved['summary']['total_terms'],8437)
        want={(name,tuple((tuple(mon),tuple(c)) for mon,c in terms)) for name,terms in
              ((name, sorted(e.items())) for name,e in remain)}
        got={(obj['name'],tuple((tuple(mon),tuple(co)) for mon,co in obj['terms'])) for obj in saved['equations']}
        self.assertEqual(want,got)

    def test_symbolic_polynomial_evaluation_matches_direct(self):
        remain,Bhat,S,D,extra=construct_dual()
        stats=modular_validation(remain,Bhat,S,D,3)
        self.assertEqual(sum(v['independent_samples'] for v in stats),12)

    def test_8_parameter_n8_n16_n32_n64(self):
        for n in (8,16,32,64):
            for p in (12289,65537):
                stats=verify(n,p,4,2048)
                self.assertEqual(stats['samples'],4)
                self.assertEqual(stats['full_rank_stages'],4)
                self.assertEqual(stats['both_B_anchors_nonzero'],4)
                self.assertEqual(stats['remaining_nonzero_test_cases'],4)
                self.assertEqual(stats['free_parameters'],8)
                self.assertEqual(stats['eliminated_rank_identities'],4*n-14)
                self.assertEqual(stats['remaining_rank_identities'],(n-4)*(n-5))

    def test_n8_two_independent_reconstruction_codes_agree(self):
        p=12289;w=primitive_root(p,8)
        rng=np.random.default_rng(999)
        for i in range(12):
            x=list(map(int,rng.integers(1,p,size=8)))
            C1,B1,d1=build_onion(p,w,x)
            C2,B2,d2=build(8,p,w,P8,x)
            self.assertTrue(np.array_equal(C1,C2))
            self.assertTrue(np.array_equal(B1,B2))
            self.assertEqual(d1['rho'],d2['rho'])

    def test_generic_inverse_stays_in_separated_chart(self):
        p=12289
        x=[101,203,307,401,509,601,701,809]
        for n in (8,16,32,64):
            w=primitive_root(p,n)
            perm=P8 if n==8 else [n-1,0,n-2]+list(range(1,n-2))
            C,B,data=build(n,p,w,perm,x)
            self.assertEqual(rankmod(C,p),n)
            A=invert_mod(C,p)
            self.assertTrue(int(A[n-1,0]) and int(A[0,n-1]))
            lower=[(int(A[i,j])*int(A[n-1,0])-int(A[i,0])*int(A[n-1,j]))%p
                for i in range(2,n-1) for j in range(1,i)]
            upper=[(int(A[i,j])*int(A[0,n-1])-int(A[i,n-1])*int(A[0,j]))%p
                for i in range(1,n-2) for j in range(i+1,n-1)]
            self.assertFalse(any(lower))
            self.assertFalse(any(upper))

    def test_exception_S1_zero_but_C_invertible(self):
        for p in (12289,65537):
            obj=witness(p)
            self.assertEqual(obj['s_1'],0)
            self.assertEqual(obj['rank_C'],8)
            self.assertTrue(obj['corner_B70'] and obj['corner_B07'])
            self.assertTrue(obj['inverse_corner_A70'] and obj['inverse_corner_A07'])
            self.assertEqual(obj['eliminated_constraints_verified'],10)
            self.assertEqual(obj['remaining_nonzero'],20)

    def test_prior_zip_is_preserved(self):
        path=HERE/'prior_checkpoint_full.zip'
        self.assertTrue(path.is_file())
        import zipfile
        with zipfile.ZipFile(path) as z:
            self.assertIsNone(z.testzip())
            self.assertIn('fft_inverse_quartic_gate_2026-10-09/RESEARCH.md',z.namelist())

if __name__=='__main__': unittest.main(verbosity=2)
