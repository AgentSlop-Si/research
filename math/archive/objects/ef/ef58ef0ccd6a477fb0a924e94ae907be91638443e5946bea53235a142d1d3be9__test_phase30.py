"""Phase30 compact regression. Exhaustive native N16 recomputation is in RUN.md."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
from random import Random
from itertools import permutations
import sys,unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from phase30_four_parameter import build_four,FourGreenExecutor,combine,P,SEEDS
from phase30_macaulay import (
    fullminor_N4_audit,full_minor_quadrics,planted_fullminor,rank_pivots,
    lifted_rows,determinant_modp,fullminor_anchor_sample,
    planted_fullminor as positive_gate)
from phase30_dimension_gate import minimum_minor_block,five_term_control,fifth_green,general_minors,lifted_general

ROOT=Path(__file__).resolve().parents[1]
CERT=ROOT/'certificates'

class TestPhase30(unittest.TestCase):
    def test_four_green_linear_executor_exact(self):
        for n in (4,8,16,32,64,128):
            with self.subTest(n=n):
                seed=SEEDS.get(n,2800+n)
                _,g=build_four(n,seed)
                rng=Random(100+n)
                x=[rng.randrange(P) for _ in range(n)]
                c=(1,2,3,5)
                dense=combine(g,c)
                expected=[sum(dense[i][j]*x[j] for j in range(n))%P for i in range(n)]
                self.assertEqual(FourGreenExecutor(n,seed).apply(x,c),expected)

    def test_complete_n4(self):
        r=fullminor_N4_audit(degree=3)
        self.assertEqual(r['rank_histogram'],{20:576})
        self.assertFalse(r['failing_mappings'])
        self.assertEqual(r['pairs'],576)

    def test_planted_valid_projective_controls(self):
        for n in (4,8,16):
            r=positive_gate(n=n)
            self.assertTrue(r['all_quadrics_vanish'])
            self.assertEqual(r['rank'],19)
            self.assertEqual(r['max_rank'],20)

    def test_native_n8_complete_both_primes(self):
        for prime in (998244353,2013265921):
            raw=(CERT/f'cpp_witnesses_N8_p{prime}.bin').read_bytes()
            self.assertEqual(len(raw),112896*21)
            self.assertEqual(raw[::21],bytes([20])*112896)
            self.assertEqual(len(set(raw[k:k+21] for k in range(0,len(raw),21))),1)

    def test_native_n16_complete_one_prime(self):
        raw=(CERT/'ranks_N16_all_p998244353.bin').read_bytes()
        self.assertEqual(len(raw),11289600)
        self.assertEqual(set(raw),{20})
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
           'f57c8b81adb0976bd5a3f5bf51d6701dcc897a6f7196d528f0fb3e23fcbc5e44')

    def test_compiled_witnesses_checked_independently(self):
        n=8; t,g=build_four(n)
        tr=list(permutations(range(n),3))
        raw=(CERT/'cpp_witnesses_N8_p998244353.bin').read_bytes()
        rng=Random(3099)
        ids={0,1,335,336,112895}
        ids.update(rng.randrange(112896) for _ in range(200))
        for i in ids:
            rs=tr[i//336];cs=tr[i%336]
            rows=lifted_rows(full_minor_quadrics(t,g,rs,cs,(0,1,2),(0,1,2)),3)
            rank,_=rank_pivots(rows)
            self.assertEqual(rank,20)
            witnesses=list(raw[21*i+1:21*i+21])
            self.assertNotEqual(determinant_modp([rows[j] for j in witnesses]),0)

    def test_n16_python_sampled_determinants(self):
        n=16;t,g=build_four(n)
        tr=list(permutations(range(n),3));nt=len(tr)
        rng=Random(301016)
        ids={0,nt**2-1,nt**2//2}
        ids.update(rng.randrange(nt**2) for _ in range(250))
        for i in ids:
            rs=tr[i//nt];cs=tr[i%nt]
            rows=lifted_rows(full_minor_quadrics(t,g,rs,cs,(0,1,2),(0,1,2)),3)
            rank,pivots=rank_pivots(rows)
            self.assertEqual(rank,20)
            self.assertNotEqual(determinant_modp([rows[j] for j in pivots]),0)

    def test_native_valid_planted_control(self):
        meta=json.loads((CERT/'planted_mapping_N8.json').read_text())
        tr=list(permutations(range(8),3))
        offset=tr.index(tuple(meta['rp'][:3]))*336+tr.index(tuple(meta['cp'][:3]))
        raw=(CERT/'planted_witnesses_N8.bin').read_bytes()
        self.assertEqual(len(raw),112896*21)
        self.assertEqual(raw[21*offset],19)
        self.assertEqual(sum(raw[::21].count(k) for k in (19,20)),112896)
        self.assertEqual(raw[::21].count(19),1)

    def test_five_green_dimension_gate(self):
        self.assertEqual([(q,minimum_minor_block(q)) for q in (3,4,5,9,10,16)],
            [(3,3),(4,3),(5,4),(9,4),(10,5),(16,5)])
        r=five_term_control(8,trial=3)
        for check in r['checks']:
            self.assertEqual([check['degrees'][d]['deficiency'] for d in (3,4,5)], [6,6,6])

    def test_five_term_four_by_four_gate(self):
        # For five generators the 3x3 gate is mathematically incapable of
        # proving projective infeasibility, but 4x4 can do so. Here the n=4
        # audit is exhaustive; n=8,16 controls are explicitly sampled.
        for n in (4,8,16):
            seed=SEEDS[n];t,g=build_four(n,seed)
            gens=(*g,fifth_green(n,seed*3+11))
            rng=Random(4010+n)
            if n==4:
                trs=list(permutations(range(n),4))
                mappings=((rs,cs) for rs in trs for cs in trs)
                count=576
            else:
                mappings=((rng.sample(range(n),4),rng.sample(range(n),4)) for k in range(100))
                count=100
            observed=0
            for rs,cs in mappings:
                qs=general_minors(t,gens,rs,cs)
                rows=lifted_general(qs,5,3)
                rank,_=rank_pivots(rows)
                self.assertEqual(rank,35)
                observed+=1
            self.assertEqual(observed,count)

    def test_n8_fullminor_sampler(self):
        r=fullminor_anchor_sample(8,samples=100,degree=3)
        self.assertEqual(r['histogram'],{20:100})
        self.assertFalse(r['bad'])

if __name__=='__main__': unittest.main()
