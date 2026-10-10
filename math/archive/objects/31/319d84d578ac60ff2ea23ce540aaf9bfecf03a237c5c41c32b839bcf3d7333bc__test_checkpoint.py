from __future__ import annotations
import hashlib, json, os, unittest, zipfile

from cyclotomic_packet import run_packet_checks, run_apply_checks
from rational_scan_gate import random_gate_cases
from separator_inverse_gate import separator_checks, treewidth_lower_bound

ROOT=os.path.dirname(__file__)


class V19Tests(unittest.TestCase):
    def test_matrix_packet_identities(self):
        rows=run_packet_checks()
        self.assertEqual(len(rows),12)
        self.assertTrue(all(r['character_cases']==r['b'] for r in rows))

    def test_linear_time_packet_actions(self):
        rows=run_apply_checks()
        self.assertEqual(len(rows),48)
        self.assertTrue(all(r['match'] for r in rows))

    def test_rational_scan_rank_gate(self):
        rows=random_gate_cases()
        scan=[r for r in rows if 'denominator_degree' in r]
        self.assertGreaterEqual(len(scan),20)
        self.assertTrue(all(r['rectangle_rank']<=r['denominator_degree'] for r in scan))

    def test_fourier_selected_blocks_full_rank(self):
        rows=random_gate_cases()
        fourier=[r for r in rows if 'fourier_n' in r]
        self.assertEqual(len(fourier),4)
        self.assertTrue(all(r['fourier_rank']==r['rectangle_size'] for r in fourier))

    def test_separator_inverse_rank(self):
        rows=separator_checks()
        ordinary=[r for r in rows if 'inverse_cross_rank' in r]
        self.assertTrue(all(r['inverse_cross_rank']<=r['separator'] for r in ordinary))

    def test_fourier_separator_contradiction(self):
        rows=separator_checks()
        fr=[r for r in rows if 'fourier_cross_rank' in r][0]
        self.assertGreater(fr['fourier_cross_rank'],fr['separator_candidate'])

    def test_treewidth_bound(self):
        self.assertEqual(treewidth_lower_bound(17),4)
        self.assertEqual(treewidth_lower_bound(101),25)
        self.assertEqual(treewidth_lower_bound(1009),252)

    def test_prior_v18_integrity(self):
        path=os.path.join(ROOT,'PRIOR_v18_COMPLETE.zip')
        h=hashlib.sha256(open(path,'rb').read()).hexdigest()
        self.assertEqual(h,'b0b768e093e816f782fc2e4878a858e6abd7c37fbbf85c3e0c2286b5350b612e')
        with zipfile.ZipFile(path) as z:
            self.assertEqual(z.testzip(),None)


if __name__=='__main__':
    unittest.main(verbosity=2)
