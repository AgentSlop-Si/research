"""Phase 40 regression suite: exact modular rank, positive controls, and graph gauges."""
import itertools, json, random, subprocess, unittest
from pathlib import Path
import numpy as np
import phase40_four_green as fg
import phase40_holonomy as gh
import phase40_weyl_control as wc
import phase40_local_synthesis as ls

ROOT=Path(__file__).resolve().parent

class Phase40(unittest.TestCase):
    def test_monomial_dimensions(self):
        self.assertEqual((len(fg.MON1),len(fg.MON2),len(fg.MON3),len(fg.MON4)),(4,10,20,35))

    def test_new_fourth_ordering(self):
        for p,g in fg.PRIMES:
            for n in (8,16):
                a=fg.build(n,p,g)
                orders=[tuple(c) for c in a['cycles']]+[tuple(a['extra_cycle']),tuple(a['fourth_cycle'])]
                self.assertEqual(len(orders),len(set(orders)))

    def test_natural_mapping_certificate(self):
        for p,g in fg.PRIMES:
            for n in (8,16,32):
                a=fg.build(n,p,g)
                w=fg.witness(a)
                self.assertEqual(w['cycle_cubic_rank'],20)
                self.assertEqual(w['all_cubic_rank'],20)

    def test_planted_projective_positive(self):
        for p,g in fg.PRIMES:
            for n in (8,16):
                inst=fg.build(n,p,g)
                w=fg.plant(inst)
                self.assertLess(w['cycle_cubic_rank'],20)
                self.assertLess(w['all_cubic_rank'],20)

    def test_adaptive_cycle_rescues_actual_N16(self):
        bads=[((2,8),(8,10,3,2,5)),((2,5),(2,6,8,5,3))]
        alternate=((0,1),(1,2),(2,4),(3,4),(0,3))
        for p,g in fg.PRIMES:
            inst=fg.build(16,p,g)
            for rows,cols in bads:
                oldrank=fg.old.rank_mod(fg.macaulay(inst,rows,cols),p)
                rank2=fg.old.rank_mod(fg.macaulay(inst,rows,cols,pairs=alternate),p)
                self.assertEqual(oldrank,19)
                self.assertEqual(rank2,20)
                self.assertEqual(fg.witness(inst,rows,cols)['all_cubic_rank'],20)

    def test_online_eight_green_matches_dense(self):
        for p,g in fg.PRIMES:
            for n in (8,16,32):
                inst=fg.build(n,p,g);rng=random.Random(n+p)
                x=[rng.randrange(0,p) for _ in range(n)]
                rp=list(range(n));cp=list(range(n));rng.shuffle(rp);rng.shuffle(cp)
                m1=[rng.randrange(1,p) for _ in range(n)]
                m2=[rng.randrange(1,p) for _ in range(n)]
                a=fg.online_apply(inst,x,mask1=m1,mask2=m2,rowperm=rp,colperm=cp)
                b=fg.dense_apply(inst,x,mask1=m1,mask2=m2,rowperm=rp,colperm=cp)
                self.assertEqual(a,b)

    def test_normalize_one_cycle_and_two_cycles(self):
        for p in (998244353,2013265921):
            for n in (8,16,64):
                cycles,weights=gh.random_problem(n,p)
                first=gh.normalize_gauge(n,cycles[:1],weights[:1],p)
                joint=gh.normalize_gauge(n,cycles,weights,p)
                self.assertEqual(len(first['holonomies']),1)
                self.assertEqual(len(joint['holonomies']),n+1)
                self.assertEqual(sum(first['edge_weights'][k]!=1 for k in first['tree']),0)

    def test_holonomy_gauge_invariance(self):
        for p in (998244353,2013265921):
            for n in (8,16,64,256):
                v=gh.verify_problem(n,p)
                self.assertTrue(v['simultaneous_conjugacy_exact'])
                self.assertEqual(v['independent_phase_invariants'],n+1)

    def test_weighted_green_defining_equation(self):
        for p in (998244353,2013265921):
            n=20
            cycles,weights=gh.random_problem(n,p)
            x=[(7*j*j+11*j+13)%p for j in range(n)]
            for cy,w in zip(cycles,weights):
                y=gh.weighted_green_apply(cy,w,x,p)
                for j,v in enumerate(cy):
                    u=cy[j-1]
                    self.assertEqual((y[v]-w[j]*y[u])%p,x[v])

    def test_singular_weighted_green_rejected(self):
        with self.assertRaises(ValueError):
            gh.weighted_green_apply([0,1,2],[1,1,1],[3,4,5],998244353)

    def test_weyl_positive_and_negative_controls(self):
        for p,g in fg.PRIMES:
            for n in (8,16,32,64):
                self.assertEqual(wc.defect_counts(lambda x:wc.fft_positive(x,p,g),n,p,g),(0,0))
                bad=wc.defect_counts(wc.green_product(n,p,g),n,p,g)
                self.assertNotEqual(bad,(0,0))

    def test_native_exact_known_mapping(self):
        binary=ROOT/'phase40_exact_audit'
        if not binary.exists():self.skipTest('Compile with g++ first')
        for p,g in fg.PRIMES:
            path=ROOT/f'N8_p{p}.txt'
            if not path.exists():fg.export_instance(fg.build(8,p,g),path)
            r=subprocess.run([str(binary),str(path),'1000'],capture_output=True,text=True)
            self.assertEqual(r.returncode,0,r.stdout+r.stderr)
            obj=json.loads(r.stdout)
            self.assertEqual(obj['minrank'],20)
            self.assertEqual(obj['checked'],1000)

    def test_native_known_bad_rescued(self):
        binary=ROOT/'phase40_exact_audit'
        if not binary.exists():self.skipTest('Compile with g++ first')
        inst=fg.build(16,*fg.PRIMES[0]);path=ROOT/f'N16_p{inst["p"]}.txt'
        if not path.exists():fg.export_instance(inst,path)
        r=subprocess.run([str(binary),str(path),'0','100000','rescue'],capture_output=True,text=True)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        self.assertEqual(json.loads(r.stdout)['deficient'],0)

    def test_jacobian_phase_local_dominance(self):
        for p in (998244353,2013265921):
            for n in (8,16,32):
                self.assertEqual(ls.jacobian(n,p)['jacobian_rank'],4)

    def test_joint_nonzero_jacobian_minor(self):
        saved=json.loads((ROOT/'phase40_jacobian_certificates.json').read_text())
        for result in saved['cases']:
            exact=ls.common_minor(result['N'])
            self.assertEqual(exact,result)
            self.assertTrue(all(k!=0 for k in result['modular_determinants'].values()))

    def test_native_planted_factorization_not_excluded(self):
        binary=ROOT/'phase40_exact_audit'
        if not binary.exists():self.skipTest('Compile first')
        p,g=fg.PRIMES[0];n=8;inst=fg.build(n,p,g)
        B=sum(int(t)*inst[f'B{i}'] for i,t in enumerate((1,7,11,17)))%p
        left=np.array([i+3 for i in range(n)],dtype=np.int64)
        right=np.array([i+11 for i in range(n)],dtype=np.int64)
        target=(B*left[:,None])%p
        target=(target*right[None,:])%p
        path=ROOT/'planted_N8.txt';fg.export_instance(inst,path,target)
        result=subprocess.run([str(binary),str(path),'1'],capture_output=True,text=True)
        self.assertEqual(result.returncode,1)
        record=json.loads(result.stdout)
        self.assertEqual(record['checked'],1)
        self.assertLess(record['minrank'],20)

if __name__=='__main__':unittest.main()
