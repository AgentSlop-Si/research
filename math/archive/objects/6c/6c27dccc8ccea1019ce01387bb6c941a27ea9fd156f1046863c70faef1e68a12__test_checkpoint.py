from __future__ import annotations

import collections
import hashlib
import math
import random
import unittest
from pathlib import Path

from local_ring_weil import (
    SL2,
    cell_valuation,
    coefficient_field,
    core_size_from_valuation,
    cross_ratio,
    enumerate_sl2,
    factor_nonunit_cell,
    in_congruence_parabolic,
    multiplicative_order,
    predicted_upper_shear,
    radix_p_dense_terms,
    support_counts,
    upper_shear_gauss_matrix,
    upper_shear_matrix,
    valuation_class_counts_formula,
)

ROOT = Path(__file__).resolve().parent
PREDECESSOR_SHA = "3d6bfe84b09b565e7e06ea6c93384d7a3352698cd90475947a01515b94910ce2"


class LocalRingWeilTests(unittest.TestCase):
    def test_gauss_kernel_and_closed_form_agree(self):
        for p, k in ((3, 2), (3, 3), (5, 2), (7, 2)):
            q = p**k
            ell, zeta = coefficient_field(q)
            for v in range(k + 1):
                b = 0 if v == k else p**v
                by_fft = upper_shear_matrix(q, b, ell, zeta)
                by_gauss = upper_shear_gauss_matrix(q, b, ell, zeta)
                predicted = predicted_upper_shear(q, p, k, b, ell, zeta)
                self.assertEqual(by_fft, by_gauss)
                self.assertEqual(by_fft, predicted)

    def test_exact_support_hierarchy(self):
        for p, k in ((3, 3), (5, 2), (7, 2)):
            q = p**k
            ell, zeta = coefficient_field(q)
            for v in range(k + 1):
                b = 0 if v == k else p**v
                op = upper_shear_matrix(q, b, ell, zeta)
                rows, cols = support_counts(op)
                expected = p ** (k - v)
                self.assertEqual(set(rows), {expected})
                self.assertEqual(set(cols), {expected})

    def test_cross_ratio_has_exact_residual_root_order(self):
        for p, k in ((3, 3), (5, 2), (7, 2)):
            q = p**k
            ell, zeta = coefficient_field(q)
            for v in range(k):
                g = p**v
                op = upper_shear_matrix(q, g, ell, zeta)
                ratio = cross_ratio(op, 0, g, 0, g, ell)
                self.assertEqual(multiplicative_order(ratio, ell), q // g)

    def test_sl2_valuation_counts(self):
        for p, k in ((3, 2), (5, 2)):
            q = p**k
            group = enumerate_sl2(q)
            measured = collections.Counter(cell_valuation(s, p, k) for s in group)
            self.assertEqual(dict(measured), valuation_class_counts_formula(p, k))
            self.assertEqual(len(group), p ** (3 * k - 2) * (p * p - 1))

    def test_nonunit_cell_factorization(self):
        group = enumerate_sl2(9)
        for s in group:
            if s.b % 3 == 0:
                left, upper = factor_nonunit_cell(s, 3)
                self.assertEqual(left @ upper, s.normalized())

    def test_congruence_parabolics_are_subgroups(self):
        group = enumerate_sl2(9)
        for t in (1, 2):
            h = [s for s in group if in_congruence_parabolic(s, 3, t)]
            hset = set(h)
            for s in h:
                self.assertIn(s.inverse(), hset)
            for a in h:
                for b in h:
                    self.assertIn((a @ b).normalized(), hset)

    def test_full_fourier_weyl_element_is_outside_easy_subgroup(self):
        q = 27
        w = SL2(0, -1, 1, 0, q).normalized()
        self.assertFalse(in_congruence_parabolic(w, 3, 1))
        rng = random.Random(2501)
        easy = []
        # Random determinant-one elements with b divisible by p.
        for _ in range(80):
            a = rng.randrange(q)
            while math.gcd(a, q) != 1:
                a = rng.randrange(q)
            b = 3 * rng.randrange(q // 3)
            c = rng.randrange(q)
            d = (1 + b * c) * pow(a, -1, q) % q
            easy.append(SL2(a, b, c, d, q))
        product = SL2(1, 0, 0, 1, q)
        for s in easy:
            product = product @ s
            self.assertTrue(in_congruence_parabolic(product, 3, 1))
        self.assertNotEqual(product, w)

    def test_double_cosets_can_refine_valuation_but_not_core_size(self):
        # B_- double cosets over Z/9 are slightly finer than valuation alone.
        # This guards against overstating the group-theoretic classification.
        q = 9
        p = 3
        group = enumerate_sl2(q)
        borel = [
            SL2(a, 0, c, pow(a, -1, q), q)
            for a in range(q)
            if math.gcd(a, q) == 1
            for c in range(q)
        ]
        unseen = set(group)
        orbit_valuations = []
        while unseen:
            s = next(iter(unseen))
            orbit = {(l @ s @ r).normalized() for l in borel for r in borel}
            unseen -= orbit
            orbit_valuations.append((cell_valuation(s, p, 2), len(orbit)))
        self.assertEqual(len(orbit_valuations), 4)
        self.assertEqual(sum(v == 1 for v, _ in orbit_valuations), 2)
        self.assertEqual(core_size_from_valuation(3, 2, 1), (3, 3))

    def test_operation_ledger(self):
        for p, k in ((3, 6), (5, 4)):
            q = p**k
            values = []
            for v in range(k + 1):
                blocks, length = core_size_from_valuation(p, k, v)
                self.assertEqual(blocks * length, q)
                terms = radix_p_dense_terms(p, k, v)
                self.assertEqual(terms, (k - v) * p * q)
                values.append(terms)
            self.assertEqual(values, sorted(values, reverse=True))

    def test_predecessor_archive_present_and_hashed(self):
        path = ROOT / "PRIOR_v24_COMPLETE.zip"
        self.assertTrue(path.is_file())
        self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), PREDECESSOR_SHA)


if __name__ == "__main__":
    unittest.main(verbosity=2)
