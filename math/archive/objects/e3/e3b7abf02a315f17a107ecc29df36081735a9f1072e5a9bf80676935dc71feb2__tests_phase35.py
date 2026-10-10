"""Independent functional checks for Phase 35's analytic and exact claims."""
import json
import unittest
from fractions import Fraction
from pathlib import Path
from phase33_two_sided import P1,P2,GEN1,GEN2,make_cycles,inverse,root_of_unity
from phase35_balance import (
    GreenStage, make_stage, transpose_cycle, signature_gate,
    balanced_residual, planted_control, independent_control,
    rowperm_transpose_stage, apply_calibrated, transpose_calibrated,
    hadamard4_positive_control, analytic_weak_coupling_bound,
    exact_individual_couplings_bound)
from phase35_polynomial_certificate import (
    P as BIGP, certificate, determinant_mod, integer_determinant,
    make_distance_arrays, eval_poly_matrix)
from phase34_products import permutation_successor,permutation_rank_difference


class Phase35Tests(unittest.TestCase):
    def test_transpose_cycle_correct(self):
        for n in (8,16,32):
            cyc=make_cycles(n,1,100)[0]
            succ=permutation_successor(cyc)
            rev=permutation_successor(transpose_cycle(cyc))
            for i in range(n):
                self.assertEqual(rev[succ[i]],i)

    def test_cyclic_green_constant_mass(self):
        for p in (P1,P2):
            for n in (8,16,32):
                A=make_stage(n,[inverse(4,p),inverse(5,p)],35100,p)
                self.assertEqual(A.apply([1]*n),[A.mass]*n)
                self.assertEqual(A.apply_transpose([1]*n),[A.mass]*n)

    def test_transpose_dense_action_independent(self):
        for n in (8,16,32):
            A=make_stage(n,[3,5],35100)
            rng=[(7+i*i+2*i)%P1 for i in range(n)]
            expected=[]
            for j in range(n):
                s=0
                for w,g in zip(A.weights,A.greens):
                    s+=sum(w*g.entry(i,j)*rng[i] for i in range(n))
                expected.append(s%P1)
            self.assertEqual(A.apply_transpose(rng),expected)

    def test_dense_forward_action_independent(self):
        for n in (8,16):
            A=make_stage(n,[3,5],35100)
            rng=[(5+11*i*i)%P1 for i in range(n)]
            exp=[sum(w*g.entry(i,j)*rng[j]
                     for j in range(n) for w,g in zip(A.weights,A.greens))%P1
                 for i in range(n)]
            self.assertEqual(A.apply(rng),exp)

    def test_hadamard_positive_fourier_factorization(self):
        for p,gen in ((P1,GEN1),(P2,GEN2)):
            a=hadamard4_positive_control(p,gen)
            self.assertTrue(a['exact_Fourier_factorization'])

    def test_sig_match_planted(self):
        for n in (8,16,32,64,128):
            A=make_stage(n,[inverse(4,P1),inverse(5,P1)],35100)
            pull=list(reversed(range(n)))
            B=rowperm_transpose_stage(A,pull)
            gate=signature_gate(A,B)
            self.assertTrue(gate['possible'])
            self.assertEqual(gate['perm'],pull)
            e0=[1]+[0]*(n-1)
            self.assertEqual(apply_calibrated(A,B,gate,e0),[1]*n)
            self.assertEqual(transpose_calibrated(A,B,gate,e0),[1]*n)

    def test_rank_distant_examples(self):
        for n in (8,16,32,64):
            A=make_stage(n,[3,5],35100)
            a,b=[permutation_successor(g.cycle) for g in A.greens]
            delta,_=permutation_rank_difference(a,b)
            self.assertGreater(delta,n//2)

    def test_balance_fails_planted_for_all_sizes(self):
        for n in (8,16,32,64,128,256,512,1024):
            out=planted_control(n)
            self.assertTrue(out['first_row_and_column_exact'])
            self.assertTrue(out['permutation_recovered_correctly'])
            self.assertEqual(out['balance_defect_coordinates'],n-1)
            self.assertEqual(out['second_column_mismatch_coordinates'],n-1)

    def test_independent_signatures_reject(self):
        for n in (8,16,32,64,128,256,512,1024):
            out=independent_control(n)
            self.assertFalse(out['B_signature_match'])
            self.assertFalse(out['moment2_equal'])
            self.assertFalse(out['A_balanced'])

    def test_second_prime_independent(self):
        for n in (8,32,128):
            out=independent_control(n,p=P2)
            self.assertFalse(out['B_signature_match'])
            self.assertFalse(out['moment2_equal'])

    def test_weak_coupling_analytic_bound(self):
        for rho in (Fraction(0),Fraction(1,8),Fraction(1,4),Fraction(3,10)):
            self.assertTrue(analytic_weak_coupling_bound(rho)['excludes_all_sizes_N_at_least_2'])
        data=exact_individual_couplings_bound()
        self.assertEqual(data['leverage_defect_upper'],'49/408')
        self.assertEqual(data['leverage_modulus_lower'],'359/408')

    def test_single_green_inverse_column_support(self):
        for n in (8,16,32):
            A=make_stage(n,[inverse(4,P1)],35100)
            # Left seed flat-leverage impossible because A^-1 e0 is two-sparse.
            self.assertGreater(balanced_residual(A)['nonzero_coordinates'],0)

    def test_characteristic_zero_polynomials(self):
        for n in (8,16):
            c=certificate(n)
            self.assertTrue(c['gcd_divides_det_in_Z'])
            self.assertTrue(c['all_complex_admissible_couplings_excluded'])
            self.assertGreater(c['rank_difference_between_cycles'],n//2)

    def test_saved_polynomial_certificate_contents(self):
        path=Path(__file__).with_name('polynomial_audit.json')
        certs=json.loads(path.read_text())['certificates']
        import sympy as s
        z=s.symbols('z')
        for c in certs:
            polys={name:s.Poly.from_list(coefs[::-1],gens=z,domain=s.ZZ)
                   for name,coefs in c['integer_coefficient_arrays_ascending'].items()}
            self.assertEqual(polys['H0'].gcd(polys['H1']),polys['gcd'])
            self.assertTrue(polys['det_C'].rem(polys['gcd']).is_zero)
            self.assertEqual(polys['H0'].degree(),c['char_zero_degrees']['H0'])

    def test_integer_polynomial_vs_second_modulus(self):
        # Explicitly cross-check reconstructed Z-polynomials over two other fields.
        import sympy as s
        z=s.symbols('z')
        certs=json.loads(Path(__file__).with_name('polynomial_audit.json').read_text())['certificates']
        for c in certs:
            n=c['N']; ds=make_distance_arrays(c['nonaffine_cycles'])
            cs=c['integer_coefficient_arrays_ascending']
            for p in (P1,P2):
                for v in (2,3,5):
                    M=eval_poly_matrix(*ds,v)
                    mm=[[u%p for u in row] for row in M]
                    det=determinant_mod(mm,p)
                    self.assertEqual(sum(x*pow(v,i,p) for i,x in enumerate(cs['det_C']))%p,det)
                    for j in (0,1):
                        minor=[[mm[i][k] for k in range(n) if k!=j] for i in range(1,n)]
                        cof=determinant_mod(minor,p)*(-1 if j%2 else 1)%p
                        h=(n*mm[0][j]*cof-det)%p
                        got=sum(x*pow(v,i,p) for i,x in enumerate(cs['H'+str(j)]))%p
                        self.assertEqual(got,h)


if __name__=='__main__':unittest.main()
