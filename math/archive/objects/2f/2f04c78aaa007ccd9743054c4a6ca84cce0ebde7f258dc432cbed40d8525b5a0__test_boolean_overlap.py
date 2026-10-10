import unittest,random,sys,pathlib
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]))
from boolean_overlap import Circuit,P,direct_dft,fft_circuit,nonlinear_fft_case,experiment

class TestBooleanOverlap(unittest.TestCase):
    def test_product_onehot_correction(self):
        c=Circuit(4)
        x=c.inputs
        a=c.add(c.add(x[0],x[1]),c.const(3))
        b=c.sub(c.add(x[1],x[2]),c.const(5))
        y=c.mul(a,b)
        au=c.onehot_audit()
        self.assertEqual(au['base'][y],-15%P)
        self.assertEqual(au['delta'][y][1],(3-5+1)%P)
        self.assertEqual(au['overlap'],1)
        q,ids=c.project_linear([y])
        self.assertTrue(q.check_linear())
        for i in range(4):
            v=[0]*4;v[i]=1
            self.assertEqual(q.eval(v,ids),c.eval(v,[y]))
        for _ in range(20):
            v=[random.randrange(P) for _ in range(4)]
            expected=au['base'][y]+sum(au['delta'][y].get(i,0)*v[i] for i in range(4))
            self.assertEqual(q.eval(v,ids)[0],expected%P)
    def test_x_square_zero_tangent_not_zero_boolean(self):
        c=Circuit(1)
        y=c.mul(c.inputs[0],c.inputs[0])
        a=c.onehot_audit()
        self.assertEqual(a['delta'][y],{0:1})
        self.assertEqual(a['overlap'],1)
        q,out=c.project_linear([y]);self.assertTrue(q.check_linear())
        self.assertEqual(q.eval([3],out),[3])
        self.assertEqual(c.eval([3],[y]),[9])
    def test_syntactic_disjoint_support(self):
        c=Circuit(4)
        x=c.inputs
        f=c.mul(c.add(x[0],x[1]),c.add(x[2],x[3]))
        au=c.onehot_audit()
        self.assertEqual(au['overlap'],0)
        self.assertEqual(au['delta'][f],{})
        q,o=c.project_linear([f]);self.assertTrue(q.check_linear())
        for i in range(4):
            v=[j==i for j in range(4)]
            self.assertEqual(c.eval(v,[f]),[0])
            self.assertEqual(q.eval(v,o),[0])
        self.assertNotEqual(c.eval([1,0,1,0],[f]),q.eval([1,0,1,0],o))
    def test_dense_overlap_gate(self):
        n=32;c=Circuit(n)
        s=c.const(0)
        for t in c.inputs:s=c.add(s,t)
        y=c.mul(s,s)
        audit=c.onehot_audit();self.assertEqual(audit['overlap'],n)
        self.assertEqual(len(audit['delta'][y]),n)
        q,o=c.project_linear([y]);self.assertTrue(q.check_linear())
        for _ in range(15):
            v=[random.randrange(P) for _ in range(n)]
            self.assertEqual(q.eval(v,o)[0],sum(v)%P)
    def test_nonzero_constant_affine_output(self):
        c=Circuit(2)
        x0,x1=c.inputs
        t=c.mul(c.add(x0,c.const(2)),c.sub(x1,c.const(3)))
        audit=c.onehot_audit();q,out=c.project_linear([t]);self.assertTrue(q.check_linear())
        for x in ([0,0],[1,0],[0,1],[4,7]):
            expected=(audit['base'][t]+sum(audit['delta'][t].get(i,0)*x[i] for i in range(2)))%P
            self.assertEqual(q.eval(x,out),[expected])
    def test_full_fourier_matrix_all_variants(self):
        for n in (2,4,8,16,32,64):
            for variant in ('plain','squares','boolean_null','hybrid'):
                with self.subTest(n=n,variant=variant):
                    c,out=nonlinear_fft_case(n,variant)
                    q,z=c.project_linear(out)
                    self.assertTrue(q.check_linear())
                    for i in range(n):
                        vec=[int(i==j) for j in range(n)]
                        self.assertEqual(c.eval(vec,out),direct_dft(vec))
                        self.assertEqual(q.eval(vec,z),direct_dft(vec))
    def test_full_cube_n4(self):
        n=4
        for variant in ('plain','squares','boolean_null','hybrid'):
            c,out=nonlinear_fft_case(n,variant)
            for mask in range(1<<n):
                x=[mask>>i&1 for i in range(n)]
                self.assertEqual(c.eval(x,out),direct_dft(x))
    def test_random_dags_independent_onehot(self):
        rng=random.Random(223)
        for n in (3,6,10):
            c=Circuit(n)
            for _ in range(100):
                a,b=rng.randrange(len(c.nodes)),rng.randrange(len(c.nodes))
                op=rng.choice(('add','sub','mul'))
                getattr(c,op)(a,b)
            outs=list(range(len(c.nodes)))
            au=c.onehot_audit()
            q,ids=c.project_linear(outs,au)
            self.assertTrue(q.check_linear())
            v0=c.eval([0]*n,outs)
            for i in range(n):
                v=[int(j==i) for j in range(n)]
                vi=c.eval(v,outs)
                for j in outs:
                    self.assertEqual(au['delta'][j].get(i,0),(vi[j]-v0[j])%P)
                self.assertEqual(q.eval(v,ids),vi)
    def test_invalid_data(self):
        with self.assertRaises(ValueError):Circuit(0)
        c=Circuit(4)
        with self.assertRaises(ValueError):c.eval_all([1,2])
        with self.assertRaises(ValueError):fft_circuit(c,c.inputs[:3])
    def test_experiment(self):
        rows=experiment((4,8),seed=55)
        self.assertEqual(len(rows),8)
        self.assertTrue(all(x['verified_columns']==x['n'] for x in rows))

if __name__=='__main__':unittest.main()
