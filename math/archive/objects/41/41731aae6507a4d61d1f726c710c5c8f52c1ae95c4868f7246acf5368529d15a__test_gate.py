import random,unittest
from jet_linearize import (P, ArithmeticDAG,build_fft,build_nonlinear_fft,
    direct_dft,linearize,eval_dual)

class GateTests(unittest.TestCase):
    def test_linearized_arithmetic_gadget(self):
        r=random.Random(9)
        for mode in ('square','rational','baseline'):
            for n in (2,4,8,16):
                with self.subTest(mode=mode,n=n):
                    d,x,y=build_nonlinear_fft(n,mode)
                    _,_,_,w=build_fft(n)
                    for rep in range(10):
                        z=[r.randrange(P) for _ in range(n)]
                        if mode=='rational' and z[0]==P-1: z[0]=12
                        self.assertEqual(d.evaluate(z,y),direct_dft(z,w))
                    for rep in range(5):
                        base=[r.randrange(P) for _ in range(n)] if rep else [0]*n
                        if mode=='rational' and base[0]==P-1: base[0]=9
                        L,outs=linearize(d,y,base)
                        self.assertLessEqual(L.cost(),3*d.cost())
                        for _ in range(5):
                            z=[r.randrange(P) for _ in range(n)]
                            f=direct_dft(z,w)
                            self.assertEqual(L.evaluate(z,outs),f)
                            self.assertEqual(eval_dual(d,base,z,y),f)

    def test_baseline_derivative_cost(self):
        for n in (2,4,8,16,32,64):
            d,x,y,w=build_fft(n)
            L,outs=linearize(d,y,[0]*n)
            self.assertLessEqual(L.cost(),d.cost())
            z=[(j*31+7)%P for j in range(n)]
            self.assertEqual(L.evaluate(z,outs),direct_dft(z,w))

    def test_nonlinearity_really_present(self):
        for mode in ('square','rational','baseline'):
            d,_,_=build_nonlinear_fft(8,mode)
            self.assertTrue(any(g.op in ('mul','div') and g.a>=0 and
                    d.gates[g.a].op != 'const' and d.gates[g.b].op!='const'
                    for g in d.gates))

    def test_singular_rational_basepoint(self):
        d,_,outs=build_nonlinear_fft(4,'rational')
        with self.assertRaises(ZeroDivisionError):
            linearize(d,outs,[P-1,0,0,0])

    def test_division_gadget_without_zero_extension(self):
        d=ArithmeticDAG()
        x=d.var(); two=d.const(2)
        # (x^2-4)/(x-2)=x+2 except at x=2.
        num=d.sub(d.mul(x,x),d.const(4))
        den=d.sub(x,two)
        out=d.div(num,den)
        for base in (0,1,3,7):
            L,idx=linearize(d,[out],[base])
            for delta in (0,1,2,7,31):
                self.assertEqual(L.evaluate([delta],idx),[delta])
                self.assertEqual(eval_dual(d,[base],[delta],[out]),[delta])
        with self.assertRaises(ZeroDivisionError):
            linearize(d,[out],[2])

    def test_linearity_zero_at_every_input(self):
        d=ArithmeticDAG()
        x=d.var(); y=d.var()
        t=d.mul(x,y)
        zero=d.sub(t,d.mul(y,x))
        f=d.add(d.add(x,y),zero)
        for base in ([0,0],[1,1],[171,321]):
            L,out=linearize(d,[f],base)
            for z in ([0,1],[2,5],[33,99]):
                self.assertEqual(L.evaluate(z,out),[(z[0]+z[1])%P])

if __name__=='__main__':unittest.main()
