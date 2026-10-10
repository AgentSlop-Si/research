from __future__ import annotations
import json
import unittest
from pathlib import Path

from two_line_weyl import (
    all_nonzero_vectors, canonical_partner, certify_pair, compatibility_kappa,
    dephased_fourier_tensor, det2, exact_two_line_factorization,
    field_for_length, fourier_matrix, fourier_weyl_coefficient,
    fourier_weyl_coefficient_direct, line_operator, mat_eq, mat_mul,
    matrix_rank, predicted_line_operator, qnorm,
)


class TwoLineWeylTests(unittest.TestCase):
    def test_weyl_coefficient_formula(self):
        for n in (5,7,11,13):
            p,w=field_for_length(n)
            for a,b in all_nonzero_vectors(n):
                self.assertEqual(
                    fourier_weyl_coefficient(n,p,w,a,b),
                    fourier_weyl_coefficient_direct(n,p,w,a,b),
                )

    def test_rank_dichotomy_exhaustive_n5_n7(self):
        for n in (5,7):
            for u in all_nonzero_vectors(n):
                for v in all_nonzero_vectors(n):
                    if det2(u,v,n)==0:
                        continue
                    cert=certify_pair(n,u,v)
                    self.assertEqual(cert.tensor_rank,1 if cert.kappa==0 else n)

    def test_partner_parameterization(self):
        for n in (5,7,11,13,17):
            for u in all_nonzero_vectors(n):
                if qnorm(u,n)==0:
                    continue
                for t in (1,2,n-1):
                    v=canonical_partner(u,n,t)
                    self.assertNotEqual(det2(u,v,n),0)
                    self.assertEqual(compatibility_kappa(u,v,n),0)

    def test_exact_factorizations(self):
        cases={7:[(1,0),(1,2),(2,3)],11:[(1,0),(1,2),(3,4)],13:[(1,0),(0,1),(2,3)],17:[(1,0),(0,1),(3,5)]}
        for n,us in cases.items():
            p,w=field_for_length(n);F=fourier_matrix(n,p,w)
            for u in us:
                if qnorm(u,n)==0:continue
                for t in (1,2):
                    v,A,B=exact_two_line_factorization(n,p,w,u,t)
                    self.assertTrue(mat_eq(mat_mul(A,B,p),F,p),(n,u,v))

    def test_line_closed_forms(self):
        for n in (5,7,11,13,17):
            p,w=field_for_length(n)
            for u in all_nonzero_vectors(n):
                if qnorm(u,n)==0:continue
                self.assertTrue(mat_eq(line_operator(n,p,w,u),predicted_line_operator(n,p,w,u),p),(n,u))

    def test_nonvertical_factors_are_full_rank(self):
        for n in (5,7,11,13,17):
            p,w=field_for_length(n)
            for u in all_nonzero_vectors(n):
                A=line_operator(n,p,w,u)
                if qnorm(u,n)==0:
                    self.assertEqual(matrix_rank(A,p),1)
                else:
                    self.assertEqual(matrix_rank(A,p),n)

    def test_bad_pair_requires_full_tensor_rank(self):
        cases=[(7,(1,0),(0,1)),(11,(1,1),(1,3)),(13,(2,1),(4,3)),(17,(1,4),(3,2))]
        for n,u,v in cases:
            self.assertNotEqual(det2(u,v,n),0)
            self.assertNotEqual(compatibility_kappa(u,v,n),0)
            p,w=field_for_length(n)
            self.assertEqual(matrix_rank(dephased_fourier_tensor(n,p,w,u,v),p),n)

    def test_predecessor_present(self):
        self.assertTrue(Path(__file__).with_name('PRIOR_v21_COMPLETE.zip').is_file())


if __name__=='__main__':
    unittest.main(verbosity=2)
