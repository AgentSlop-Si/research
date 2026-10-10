import unittest
from jet_linearize import ArithmeticDAG,linearize

class DomainBoundaryTests(unittest.TestCase):
    def test_boolean_only_identity_does_not_linearize(self):
        # Over any prime field of odd characteristic x*x equals x on {0,1},
        # but not as a polynomial.  Its derivative at zero is zero.
        dag=ArithmeticDAG(p=101)
        x=dag.var();square=dag.mul(x,x)
        for binary in (0,1):
            self.assertEqual(dag.evaluate([binary],[square]),[binary])
        lin,out=linearize(dag,[square],[0])
        self.assertEqual(lin.evaluate([1],out),[0])
        self.assertNotEqual(lin.evaluate([1],out),[1])

    def test_field_function_frobenius_has_zero_derivative(self):
        # Over F_5, x**5 = x at every field element, yet d(x**5)/dx=0.
        dag=ArithmeticDAG(p=5)
        x=dag.var();xx=dag.mul(x,x);xxxx=dag.mul(xx,xx);p5=dag.mul(xxxx,x)
        for i in range(5):
            self.assertEqual(dag.evaluate([i],[p5]),[i])
        lin,out=linearize(dag,[p5],[0])
        self.assertEqual(lin.evaluate([1],out),[0])

    def test_rational_identity_only_on_defined_domain(self):
        dag=ArithmeticDAG(p=101)
        x=dag.var()
        q=dag.sub(x,dag.const(4))
        y=dag.div(dag.mul(q,x),q)
        with self.assertRaises(ZeroDivisionError):
            dag.evaluate([4],[y])
        for v in (0,1,5,6,99):
            self.assertEqual(dag.evaluate([v],[y]),[v])
            lin,out=linearize(dag,[y],[v])
            self.assertEqual(lin.evaluate([8],out),[8])

if __name__=='__main__': unittest.main()
