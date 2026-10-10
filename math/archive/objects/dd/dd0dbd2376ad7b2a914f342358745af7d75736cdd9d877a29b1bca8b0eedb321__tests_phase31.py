"""Tests including independently recomputed nonzero cubic determinants."""
from __future__ import annotations
import hashlib
import struct
import unittest
from itertools import permutations,combinations
from pathlib import Path
from random import Random
from phase31_rectangular import (ROOT,P,SEEDS,family,FAST_PAIRS,
                                 rectangular_quadrics,certificate,exhaustive_n4)
from phase31_executor import FiveGreenExecutor,dense_reference
from phase30_dimension_gate import lifted_general
from phase30_macaulay import rank_pivots,determinant_modp

SEVEN_PAIRS=((0,1,0,1),(0,1,0,2),(0,1,0,3),
             (0,2,1,2),(0,2,2,3),(1,2,0,1),(1,2,0,3))
CERT=ROOT/'certificates'


class TestPhase31(unittest.TestCase):
    def test_minimal_cubic_equation_count(self):
        from math import comb,ceil
        self.assertEqual(comb(7,3),35)
        self.assertEqual(ceil(comb(7,3)/5),7)
        self.assertEqual(len(SEVEN_PAIRS),7)

    def test_five_green_executor(self):
        for n in (4,8,16,32,64,128):
            with self.subTest(n=n):
                seed=SEEDS.get(n,2800+n)
                _,gs=family(n,seed)
                x=[Random(31*n+j).randrange(P) for j in range(n)]
                coeffs=(1,2,3,4,5)
                self.assertEqual(FiveGreenExecutor(n,seed).apply(x,coeffs),
                                 dense_reference(x,coeffs,gs))

    def test_n4_seven_equations_exhaustive(self):
        t,gs=family(4)
        hist={}
        for r in permutations(range(4),3):
            for c in permutations(range(4),4):
                rank,det,_=certificate(t,gs,r,c,pairs=SEVEN_PAIRS)
                hist[rank]=hist.get(rank,0)+1
                self.assertEqual(rank,35)
                self.assertTrue(det)
        self.assertEqual(hist,{35:576})

    def test_n8_stored_all_rank_certificate(self):
        raw=(CERT/'rank7_N8_all.bin').read_bytes()
        self.assertEqual(len(raw),564480)
        self.assertEqual(set(raw),{35})
        self.assertEqual(hashlib.sha256(raw).hexdigest(),
           '81b6cca8a880659e2ca3583bd0f145914fdb8ba9af5973024df010c5f7cb4dc3')

    def test_n16_stored_sampled_certificate(self):
        idx=(CERT/'indices_N16_100000.bin').read_bytes()
        raw=(CERT/'ranks7_N16_100000.bin').read_bytes()
        self.assertEqual(len(raw),100000)
        self.assertEqual(len(idx),800000)
        self.assertEqual(set(raw),{35})
        self.assertEqual(len(set(struct.unpack('<'+'Q'*100000,idx))),100000)

    def test_independent_n8_determinants(self):
        n=8;t,g=family(n)
        rows=list(permutations(range(n),3))
        cols=list(permutations(range(n),4))
        rng=Random(310031)
        samples={0,1,1679,1680,len(rows)*len(cols)-1}
        samples.update(rng.randrange(len(rows)*len(cols)) for _ in range(80))
        for m in sorted(samples):
            rs=rows[m//len(cols)];cs=cols[m%len(cols)]
            qs=rectangular_quadrics(t,g,rs,cs,pairs=SEVEN_PAIRS)
            matrix=lifted_general(qs,5,3)
            self.assertEqual(len(matrix),35)
            rk,_=rank_pivots(matrix)
            self.assertEqual(rk,35)
            self.assertNotEqual(determinant_modp(matrix),0)

    def test_independent_n16_determinants(self):
        n=16;t,g=family(n)
        rows=list(permutations(range(n),3))
        cols=list(permutations(range(n),4))
        rng=Random(310032)
        for _ in range(100):
            rs=rows[rng.randrange(len(rows))]
            cs=cols[rng.randrange(len(cols))]
            mat=lifted_general(rectangular_quadrics(t,g,rs,cs,pairs=SEVEN_PAIRS),5,3)
            self.assertEqual(len(mat),35)
            self.assertNotEqual(determinant_modp(mat),0)

    def test_planted_valid_positive_control(self):
        n=8
        data=(CERT/'input_planted_N8.bin').read_bytes()
        values=struct.unpack('<'+'I'*((len(data)-8)//4),data[8:])
        t=[[values[i*n+j] for j in range(n)] for i in range(n)]
        g=[[[values[(k+1)*n*n+i*n+j] for j in range(n)]for i in range(n)]for k in range(5)]
        rng=Random(310031+n)
        r=list(range(n));c=list(range(n));rng.shuffle(r);rng.shuffle(c)
        mat=lifted_general(rectangular_quadrics(t,g,r[:3],c[:4],pairs=SEVEN_PAIRS),5,3)
        rank,_=rank_pivots(mat)
        self.assertLess(rank,35)
        # All seven quadratic equations vanish at the planted coefficient vector.
        pvars=[1,2,3,4,5]
        from phase30_dimension_gate import monomials
        qs=rectangular_quadrics(t,g,r[:3],c[:4],pairs=SEVEN_PAIRS)
        for coeffs in qs:
            self.assertEqual(sum(co*__import__('math').prod(pow(v,e,P)
                for v,e in zip(pvars,m)) for co,m in zip(coeffs,monomials(2,5)))%P,0)

    def test_six_term_rectangular_controls(self):
        from phase31_six_control import run
        self.assertEqual(run(4)['histogram'],{56:576})
        self.assertEqual(run(8,6)['histogram'],{56:6})
        self.assertEqual(run(16,6)['histogram'],{56:6})

    def test_seven_term_exploratory_controls(self):
        from phase31_seven_control import run
        self.assertEqual(run(8,3)['rank_histogram'],{84:3})
        self.assertEqual(run(16,3)['rank_histogram'],{84:3})

    def test_larger_input_N16_native_sample_is_not_exhaustive(self):
        count_all=(16*15*14)*(16*15*14*13)
        self.assertEqual(count_all,146764800)
        self.assertLess(100000,count_all)

if __name__=='__main__':unittest.main(verbosity=2)
