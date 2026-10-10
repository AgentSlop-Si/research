import json
import math
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

from generate_bitrev_certificates import bitrev, single
from independent_verifier import verify_one
from gauge_audit import run as gauge_check
from cost_audit import audit
from multistage_jacobian import materialize,rank_minor
from generate_bitrev_certificates import run_rank

ROOT=Path(__file__).resolve().parent

class TestNewMultistageGate(unittest.TestCase):
    def test_dimension_bound(self):
        for n in (8,16,32,64,128):
            t=n//4
            self.assertLess(n+t*(4*n-6),n*n)
            self.assertGreaterEqual(n+(t+1)*(4*n-6),n*n)

    def test_bitrev_n8_all_depths(self):
        for t,expected in ((1,34),(2,60),(3,64)):
            result,_=single(8,t,12289)
            self.assertEqual(result['rank'],expected)

    def test_bitrev_n16_two_primes(self):
        for p in (12289,65537):
            for t,r in ((3,190),(4,248),(5,256)):
                result,_=single(16,t,p)
                self.assertEqual(result['rank'],r)

    def test_bitrev_n32_near_threshold(self):
        for t,r in ((8,1008),(9,1024)):
            result,_=single(32,t,12289)
            self.assertEqual(result['rank'],r)

    def test_gauge_kernel(self):
        for n,t in ((8,2),(16,4),(32,8)):
            result=gauge_check(n,t,12289)
            self.assertTrue(result['gauge_complete'])

    def test_full_dimensional_determinants_independent(self):
        for n in (8,16,32):
            self.assertTrue(verify_one(n,verbose=False))

    def test_fresh_arithmetic(self):
        for n in (8,16,32):
            self.assertEqual(audit(n,12289)['exact_results'],'passed')

    def test_identity_shuffles_do_not_dominate(self):
        for n in (8,16,32):
            t=n//4+1
            self.assertLess(t,n//2)
            _,jac,_,_=materialize(n,t,[list(range(n))]*(t-1),99017,12289)
            rank,_,_=run_rank(jac,12289)
            self.assertLess(rank,n*n)

    def test_saved_json_is_consistent(self):
        data=json.loads((ROOT/'BITREV_RESULTS.json').read_text())
        self.assertEqual(len(data),34)
        for result in data:
            n,t=result['n'],result['t']
            self.assertEqual(result['rank'],min(n*n,n+t*(4*n-6)))
            self.assertIn(result['prime'],(12289,65537))
        saved=json.loads((ROOT/'GAUGE_RESULTS.json').read_text())
        self.assertEqual(len(saved),12)
        self.assertTrue(all(r['all_gauges_killed_by_jacobian'] for r in saved))

if __name__=='__main__':unittest.main()
