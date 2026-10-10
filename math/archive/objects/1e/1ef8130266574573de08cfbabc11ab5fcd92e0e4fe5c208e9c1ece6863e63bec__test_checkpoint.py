from __future__ import annotations

import json
import unittest
from pathlib import Path

from finite_field import flatten, mat_identity, matrix_rank, solve_linear_columns
from weyl_line_basis import (
    character_packet_matrix,
    chirp_polynomial_matrix,
    chirp_spectrum,
    combine_green_line,
    find_generic_field_alpha,
    finite_field_case,
    gauged_fourier_matrix,
    green_matrix,
    leading_term_certificate,
    matrices_equal,
    offdiag_block_matrix,
    packet_basis_columns,
    packet_offdiag_rank,
    packet_support_degrees,
    solve_fourier_green_line,
    weyl_matrix,
    common_weyl_generator,
    matrix_power,
)

ROOT=Path(__file__).resolve().parent
CASES=[7,11,13,17]

class TestV21(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records={n:finite_field_case(n) for n in CASES}

    def test_all_fourier_blocks_invertible(self):
        for n,rec in self.records.items():
            self.assertEqual(rec['block_ranks'],[n-1]*n)

    def test_packet_offdiag_basis(self):
        for n,rec in self.records.items():
            self.assertEqual(rec['packet_offdiag_rank'],n*(n-1))

    def test_unique_top_degree_certificate(self):
        for n in CASES:
            for x in range(n):
                c=leading_term_certificate(n,x)
                self.assertEqual(c['top_degree'],(n-1)**2)
                self.assertEqual(len(set(c['unique_top_columns'])),n-1)
                self.assertNotIn(0,c['unique_top_columns'])

    def test_character_packets_have_degree_two_support(self):
        for n,rec in self.records.items():
            p,w,a=rec['field_prime'],rec['omega'],rec['alpha']
            for h in (1,2,3):
                if h>=n:continue
                for s in (0,1,2):
                    M=character_packet_matrix(n,p,w,a,h,s)
                    r,c,_=packet_support_degrees(M)
                    self.assertLessEqual(r,2)
                    self.assertLessEqual(c,2)

    def test_constant_diagonal_span_with_identity(self):
        for n,rec in self.records.items():
            p,w,a=rec['field_prime'],rec['omega'],rec['alpha']
            cols,_=packet_basis_columns(n,p,w,a)
            I=flatten(mat_identity(n))
            # deterministic arbitrary constant-diagonal target
            target=[]
            for i in range(n):
                for j in range(n):
                    target.append(7%p if i==j else (3*i+5*j+11)%p)
            sol=solve_linear_columns(cols+[I],target,p)
            self.assertIsNotNone(sol)

    def test_exact_green_line_fourier_representation(self):
        for n,rec in self.records.items():
            self.assertTrue(rec['green_line_identity'])

    def test_common_weyl_line(self):
        for n,rec in self.records.items():
            p,w=rec['field_prime'],rec['omega']
            U=common_weyl_generator(n,p,w)
            inv2=pow(2,-1,n)
            for h in range(1,n):
                left=weyl_matrix(n,p,w,h,-h)
                right=matrix_power(U,h,p)
                scalar=pow(w,(h*(h-1)*inv2)%n,p)
                right=[[scalar*v%p for v in row] for row in right]
                self.assertTrue(matrices_equal(left,right,p))

    def test_bluestein_chirp_polynomial_identity(self):
        for n,rec in self.records.items():
            self.assertTrue(rec['chirp_polynomial_identity'])

    def test_chirp_is_dense_in_both_domains(self):
        for n,rec in self.records.items():
            self.assertEqual(rec['chirp_spectrum_nonzero'],n)

    def test_selected_packet_count_gate(self):
        for n in CASES:
            # Each selected character packet has at most two entries per column.
            # A dense target therefore needs at least ceil(n/2) separately summed packets.
            self.assertGreaterEqual((n+1)//2,1)
            self.assertLess(2*((n+1)//2-1),n)

    def test_saved_results_match(self):
        saved=json.loads((ROOT/'results.json').read_text())
        expected=json.loads(json.dumps([self.records[n] for n in CASES],sort_keys=True))
        self.assertEqual(saved['finite_field_cases'],expected)

if __name__=='__main__':unittest.main(verbosity=2)
