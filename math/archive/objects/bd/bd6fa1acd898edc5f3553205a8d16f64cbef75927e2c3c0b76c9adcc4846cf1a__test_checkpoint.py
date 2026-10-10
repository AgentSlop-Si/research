import json
import math
import unittest
from pathlib import Path

import numpy as np

import prototype


ROOT = Path(__file__).resolve().parent


class CheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = json.loads((ROOT / "results.json").read_text(encoding="utf-8"))

    def test_packed_decoder_bounds(self):
        rows = self.results["packed_correctness"]
        self.assertEqual(len(rows), 20)
        for row in rows:
            self.assertLessEqual(
                row["decoder_error_normalized"],
                row["decoder_bound_normalized"] + 1e-12,
            )

    def test_sampling_scaling_is_inverse_sqrt_k(self):
        for case in ["flat", "random_phase", "gaussian", "spike_noise"]:
            rows = [r for r in self.results["sampling_scaling"] if r["case"] == case]
            xs = np.log([r["k"] for r in rows])
            ys = np.log([r["median_normalized_sampling_error"] for r in rows])
            slope = float(np.polyfit(xs, ys, 1)[0])
            self.assertGreater(slope, -0.60)
            self.assertLess(slope, -0.40)

    def test_linear_symbolic_cost_stays_constant_order(self):
        rows = self.results["cost_model_linear"][-4:]
        for row in rows:
            self.assertLess(row["modeled_total_non_io_over_N"], 12.0)
            self.assertLess(row["table_exponent_logN"], 0.73)
        etas = [r["predicted_sampling_scale"] for r in rows]
        self.assertTrue(all(b < a for a, b in zip(etas, etas[1:])))

    def test_subfft_symbolic_cost_matches_L_over_logL(self):
        rows = self.results["cost_model_subfft"][-4:]
        ratios = []
        for row in rows:
            L = float(row["log2N"])
            ell = float(row["log2log2N"])
            ratios.append(row["modeled_total_non_io_over_N"] / (L / ell))
            self.assertLess(row["table_exponent_logN"], 0.73)
        self.assertLess(max(ratios), 3.5)
        self.assertGreater(min(ratios), 2.5)

    def test_energy_mixture_is_not_asymptotically_stronger(self):
        rows = self.results["rejected_energy_mixture"]
        # Cauchy gives L_box/sqrt(N) <= sqrt(2)||x||_2.
        for row in rows:
            self.assertLessEqual(
                row["ratio_Lbox_over_sqrtN_to_l2"], math.sqrt(2.0) + 1e-12
            )
        # On a single spike the old scale is smaller by exactly sqrt(N).
        for row in rows:
            if row["case"] == "single_spike":
                self.assertAlmostEqual(
                    row["ratio_Lbox_over_sqrtN_to_l2"],
                    1.0 / math.sqrt(row["N"]),
                    places=12,
                )

    def test_hoeffding_sample_count_decreases_with_larger_tolerance(self):
        N = 1 << 20
        delta = N ** -1
        k1 = prototype.concentration_k(N, 0.1, delta)
        k2 = prototype.concentration_k(N, 0.2, delta)
        self.assertGreater(k1, k2)
        self.assertGreaterEqual(k1, 4 * k2 - 8)


if __name__ == "__main__":
    unittest.main(verbosity=2)
