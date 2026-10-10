from __future__ import annotations
import json
import math
import random
import unittest
from pathlib import Path

from green_bank_gate import (
    certify_bounded_cycle_case,
    certify_hamiltonian_case,
    common_cycle_cell,
    cycle_metadata,
    exhaustive_two_order_check,
    generate_results,
    random_n_cycle,
    random_permutation_with_cycles,
    simultaneous_separated_sets,
)


class GreenBankGateTests(unittest.TestCase):
    def test_simultaneous_separation_random(self):
        rng = random.Random(1)
        for n in (17, 64, 101, 257):
            for t in range(1, 7):
                orders = []
                for _ in range(t):
                    p = list(range(n)); rng.shuffle(p)
                    pos = [0] * n
                    for i, x in enumerate(p): pos[x] = i
                    orders.append(pos)
                A, B, orient = simultaneous_separated_sets(orders)
                self.assertGreaterEqual(len(A), n // (2 ** t))
                self.assertEqual(len(A), len(B))
                for o, s in zip(orders, orient):
                    if A:
                        if s == 1:
                            self.assertLess(max(o[x] for x in A), min(o[y] for y in B))
                        else:
                            self.assertGreater(min(o[x] for x in A), max(o[y] for y in B))

    def test_threshold_exact_certificates(self):
        cases = {2: 13, 3: 37, 4: 83, 5: 193, 6: 449, 7: 1031, 8: 2309}
        for t, n in cases.items():
            row = certify_hamiltonian_case(t, n)
            self.assertGreater(row.separated_size, t)
            self.assertLessEqual(row.sum_rank, t)
            self.assertEqual(row.fourier_rank, row.separated_size)
            self.assertNotEqual(row.fourier_det, 0)
            self.assertTrue(all(r <= 1 for r in row.term_ranks))

    def test_bounded_cycle_partition(self):
        rng = random.Random(2)
        for n, t, c in ((109, 2, 3), (257, 3, 2), (1297, 4, 2)):
            perms = [random_permutation_with_cycles(n, c, rng) for _ in range(t)]
            cell, orders, product = common_cycle_cell(perms)
            A, B, _ = simultaneous_separated_sets(orders, cell)
            self.assertGreaterEqual(len(cell), n // product)
            self.assertGreaterEqual(len(A), len(cell) // (2 ** t))
            self.assertEqual(len(A), len(B))

    def test_exhaustive_two_order_n8(self):
        out = exhaustive_two_order_check(8)
        self.assertEqual(out["permutations_checked"], math.factorial(8))
        self.assertGreaterEqual(out["minimum_separated_size"], 2)
        self.assertEqual(out["guaranteed_floor"], 2)

    def test_boundary_controls(self):
        rng = random.Random(3)
        for t, n in ((3, 31), (4, 79), (5, 191)):
            perms = [random_n_cycle(n, rng) for _ in range(t)]
            orders = [cycle_metadata(p)[1] for p in perms]
            A, _, _ = simultaneous_separated_sets(orders)
            # The universal threshold cannot force a (t+1)-square here.
            self.assertLessEqual(n, (2 ** t) * (t + 1) - 1)
            self.assertGreaterEqual(len(A), n // (2 ** t))

    def test_results_roundtrip(self):
        generated = generate_results()
        path = Path(__file__).with_name("results.json")
        if path.exists():
            saved = json.loads(path.read_text())
            self.assertEqual(saved, generated)


if __name__ == "__main__":
    unittest.main(verbosity=2)
