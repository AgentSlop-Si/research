"""Phase 38 self-contained exact tests. Historical tests remain in nested Phase 37 ZIP."""
import unittest, random, shutil, subprocess, tempfile, json
from pathlib import Path
import numpy as np
import phase38_joint_masks as p38
import phase37_curvature as p37

BASE=Path(__file__).resolve().parent

class Phase38Tests(unittest.TestCase):
    def setUp(self):p37.set_field(998244353,3)

    def test_exact_modular_inverse_p1(self):
        x=p38.build(16)
        I=np.eye(16,dtype=np.int64)
        self.assertTrue(np.array_equal(p38.field_mm(x['A'],p38.field_inv(x['A'],x['p']),x['p']),I))
        self.assertTrue(np.array_equal(p38.field_mm(x['C'],p38.field_inv(x['C'],x['p']),x['p']),I))

    def test_exact_modular_inverse_p2(self):
        x=p38.build(16,2013265921,31)
        I=np.eye(16,dtype=np.int64)
        self.assertTrue(np.array_equal(p38.field_mm(x['A'],p38.field_inv(x['A'],x['p']),x['p']),I))
        self.assertTrue(np.array_equal(p38.field_mm(x['C'],p38.field_inv(x['C'],x['p']),x['p']),I))

    def test_greens_are_actual_cyclic_inverses(self):
        for n in (8,16,32):
            c=p37.construct_two_mask_circuit(n)
            rng=random.Random(3800+n)
            for cyc,a in zip(c['cycles'],c['alphas']):
                x=[rng.randrange(p37.P) for _ in range(n)]
                y=p37.cycle_green_apply(cyc,a,x)
                mat=p37.cycle_green(n,cyc,a)
                self.assertEqual(y,[sum(mat[i][j]*x[j] for j in range(n))%p37.P for i in range(n)])

    def test_quadratic_resultant_matches_sympy(self):
        import sympy as s
        z=s.symbols('z');rand=random.Random(38)
        for prime,gen in p38.PRIMES:
            for _ in range(36):
                f=[rand.randrange(prime) for k in range(3)]
                g=[rand.randrange(prime) for k in range(3)]
                self.assertEqual(p38.resultant2(f,g,prime),
                                 int(s.resultant(sum(int(f[k])*z**k for k in range(3)),
                                                 sum(int(g[k])*z**k for k in range(3)),z))%prime)

    def test_two_mask_quadratics_p1(self):
        for n in (4,8,16,32,64,128,256):
            x=p38.build(n)
            w=p38.witness(x)
            self.assertEqual(w['polynomial_degrees'],[2,2])
            self.assertNotEqual(w['quadratic_resultant'],0)
            self.assertEqual(p37.add(p37.mul(w['bezout_u'],w['first_eq']),
                                      p37.mul(w['bezout_v'],w['second_eq'])),[1])

    def test_two_mask_quadratics_p2(self):
        for n in (4,8,16,32,64,128,256):
            x=p38.build(n,2013265921,31)
            w=p38.witness(x)
            self.assertEqual(w['polynomial_degrees'],[2,2])
            self.assertNotEqual(w['quadratic_resultant'],0)
            self.assertEqual(p37.add(p37.mul(w['bezout_u'],w['first_eq']),
                                      p37.mul(w['bezout_v'],w['second_eq'])),[1])

    def test_exact_all_small_permutations_python(self):
        for n in (4,8):
            x=p38.build(n)
            for r0 in range(n):
                for r1 in range(n):
                    if r0==r1:continue
                    for c0 in range(n):
                        for c1 in range(n):
                            if c0==c1:continue
                            f=p38.poly_eq(x,(r0,r1),(c0,c1,0),1)
                            for c2 in range(n):
                                if c2==c0 or c2==c1:continue
                                g=p38.poly_eq(x,(r0,r1),(c0,c1,c2),2)
                                self.assertNotEqual(p38.resultant2(f,g,x['p']),0)

    def test_sequential_mod_scaling_no_overflow(self):
        x=p38.build(8)
        rng=random.Random(111)
        n=8;pp=x['p']
        B=(x['B0']+7*x['B1'])%pp
        u=np.array([rng.randrange(1,pp) for _ in range(n)],dtype=np.int64)
        v=np.array([rng.randrange(1,pp) for _ in range(n)],dtype=np.int64)
        T=((u[:,None]*B)%pp*v[None,:])%pp
        got=p38.recover_masks(T,B,pp)
        self.assertIsNotNone(got)
        self.assertTrue(np.array_equal(((got[0][:,None]*B)%pp*got[1][None,:])%pp,T))

    def test_calibration_matches_exact_first_row_col(self):
        for n in (4,8,16,32,64):
            x=p38.build(n)
            report=p38.anchored_fit(x,7)
            self.assertEqual(report['calibrated_entries'],2*n-1)
            self.assertEqual(report['mismatches_in_interior'],(n-1)**2)

    def test_positive_planted_masks_and_permutations(self):
        for n in (4,8,16):
            report=p38.plant_valid_control(n)
            self.assertTrue(report['phase_masks_recovered'])
            self.assertTrue(report['full_Fourier_reconstruction'])
            self.assertEqual(report['quadratic_resultant'],0)
            self.assertFalse(report['cheap_Green_outer'])

    def test_modular_collision_in_second_prime_is_not_complex_solution(self):
        # The only modular accidental root in N=64 second-prime exhaustive audit.
        rows=(53,55); cols=(19,26,5)
        x=p38.build(64,998244353,3)
        f=p38.poly_eq(x,rows,cols,1);g=p38.poly_eq(x,rows,cols,2)
        self.assertEqual(p38.resultant2(f,g,x['p']),470304279)
        x=p38.build(64,2013265921,31)
        f=p38.poly_eq(x,rows,cols,1);g=p38.poly_eq(x,rows,cols,2)
        self.assertEqual(p38.resultant2(f,g,x['p']),0)

    def test_charzero_n4(self):
        import charzero_n4
        report=charzero_n4.verify()
        self.assertEqual(report['gcd_degree'],0)
        self.assertTrue(report['resultant_nonzero'])

    def test_native_full_small_exactness(self):
        if shutil.which('g++') is None:self.skipTest('g++ unavailable')
        with tempfile.TemporaryDirectory() as t:
            binpath=Path(t)/'checker'
            subprocess.run(['g++','-std=c++17','-O3',str(BASE/'exhaustive_permutations.cpp'),'-o',str(binpath)],check=True)
            for n in (4,8,16):
                inst=p38.build(n)
                path=Path(t)/f'N{n}.txt'
                p38.export_instance(inst,path)
                got=subprocess.run([str(binpath),str(path)],capture_output=True,text=True,check=True)
                out=json.loads(got.stdout)
                self.assertEqual(out['checked'],n*(n-1)*n*(n-1)*(n-2))
                self.assertEqual(out['zero_resultants'],0)

    def test_native_positive_limit_and_sample(self):
        if shutil.which('g++') is None:self.skipTest('g++ unavailable')
        with tempfile.TemporaryDirectory() as t:
            binpath=Path(t)/'checker'
            subprocess.run(['g++','-std=c++17','-O3',str(BASE/'exhaustive_permutations.cpp'),'-o',str(binpath)],check=True)
            inst=p38.build(128)
            p38.export_instance(inst,Path(t)/'instance.txt')
            got=subprocess.run([str(binpath),str(Path(t)/'instance.txt'),'0','30000'],capture_output=True,text=True,check=True)
            out=json.loads(got.stdout)
            self.assertEqual(out['checked'],30000)
            self.assertEqual(out['zero_resultants'],0)

if __name__=='__main__':unittest.main()
