"""Exact regression tests for Phase 37: finite-field and characteristic-zero controls."""
import unittest
import random
import phase37_curvature as q

class Phase37Tests(unittest.TestCase):
    def setUp(self):q.set_field(998244353,3)

    def test_primitive_green_holonomy_n8(self):
        a=q.small_audit(8,anchor_checks=64)
        self.assertEqual(set(a['green_phase_curvature_ranks']),{7})
        self.assertEqual(set(a['Fourier_phase_curvature_ranks']),{1})

    def test_projective_curvature_n16(self):
        a=q.small_audit(16,anchor_checks=12)
        self.assertEqual(set(a['green_phase_curvature_ranks']),{15})
        self.assertEqual(set(a['Fourier_phase_curvature_ranks']),{1})

    def test_projective_curvature_n64(self):
        a=q.small_audit(64,anchor_checks=4)
        self.assertEqual(set(a['green_phase_curvature_ranks']),{63})

    def test_projective_curvature_independent_prime(self):
        q.set_field(2013265921,31)
        a=q.small_audit(32,anchor_checks=8)
        self.assertEqual(set(a['green_phase_curvature_ranks']),{31})
        self.assertEqual(set(a['Fourier_phase_curvature_ranks']),{1})

    def test_positive_fourier_plaquettes_are_roots(self):
        for n in (4,8,16):
            m=q.scaled_permuted(q.fourier(n))
            for i in range(1,n):
                self.assertTrue(q.is_nth_root(q.ratio(m,0,0,i,1),n))

    def test_Green_plaquettes_are_roots_but_wrong_rank(self):
        n=16
        a=pow(q.PRIMITIVE,(q.P-1)//(n*n),q.P)
        g=q.cycle_green(n,q.cycles(n)[1],a)
        self.assertTrue(all(q.is_nth_root(q.ratio(g,0,0,i,j),n)
                            for i in range(1,n) for j in range(1,n)))
        self.assertEqual(q.gf2_rank(q.parity_curvature(g,n)),n-1)

    def test_two_mask_complex_pencil_p1(self):
        for n in (4,8,16,32,64,128):
            v=q.two_mask_gate(n)
            self.assertTrue(v['excluded'])
            self.assertEqual(v['degrees'],[2*n,2*n])
            self.assertTrue(v['exact_application_control'])

    def test_two_mask_complex_pencil_p2(self):
        q.set_field(2013265921,31)
        for n in (4,8,16,32,64,128):
            v=q.two_mask_gate(n)
            self.assertTrue(v['excluded'])
            self.assertEqual(v['degrees'],[2*n,2*n])

    def test_explicit_bezout_p1_p2(self):
        for p,gen in [(998244353,3),(2013265921,31)]:
            q.set_field(p,gen)
            result=q.two_mask_gate(32,include_witness=True)
            f,g=result['polynomials_coefficients_mod_prime']
            s,t=result['bezout_coefficients_mod_prime']
            self.assertEqual(q.add(q.mul(s,f),q.mul(t,g)),[1])

    def test_plant_fourier_root_control(self):
        n=8;F=q.fourier(n)
        rand=random.Random(4)
        B=[[rand.randrange(1,q.P) for _ in range(n)] for __ in range(n)]
        lam=7
        A=[[(F[i][j]-lam*B[i][j])%q.P for j in range(n)] for i in range(n)]
        f=q.plaquette_polynomial(A,B,n,(0,1),(0,1))
        g=q.plaquette_polynomial(A,B,n,(0,1),(0,2))
        evalat=lambda f:sum(v*pow(lam,k,q.P) for k,v in enumerate(f))%q.P
        self.assertEqual(evalat(f),0)
        self.assertEqual(evalat(g),0)
        self.assertGreaterEqual(len(q.gcd_poly(f,g)),2)

    def test_two_mask_online_linearity(self):
        for n in (8,32,64):
            net=q.construct_two_mask_circuit(n)
            rand=random.Random(n)
            lam=123
            x=[rand.randrange(q.P) for _ in range(n)]
            y=[rand.randrange(q.P) for _ in range(n)]
            ax=net['apply'](x,lam);ay=net['apply'](y,lam)
            v=[(x[i]+y[i])%q.P for i in range(n)]
            self.assertEqual(net['apply'](v,lam),[(ax[i]+ay[i])%q.P for i in range(n)])

    def test_six_distinct_nonaffine_cycles_n8_plus(self):
        import math
        for n in (8,16,32,64,128):
            cyc=q.seeded_cycles(n)
            self.assertEqual(len({tuple(c) for c in cyc}),6)
            for c in cyc:
                succ=[0]*n
                for idx,j in enumerate(c):succ[j]=c[(idx+1)%n]
                self.assertFalse(any(all(succ[k]==(u*k+b)%n for k in range(n))
                    for u in range(1,n,2) for b in range(n)))

    def test_charzero_direct_n4(self):
        from charzero_control import verify
        report=verify(4)
        self.assertTrue(report['charzero_gcd_one'])
        self.assertEqual(report['degrees'],[8,8])

if __name__=='__main__':unittest.main()
