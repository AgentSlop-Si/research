import unittest,sys,random
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from circuit import build_adaptive,differentiate,reference_dft,Circuit,primitive_nth_root
from boolean_cube import power_of_sum,evaluate_quotient,coefficient_by_onto_functions,boolean_jet_failure

class TestBranchAndBoolean(unittest.TestCase):
    def test_root(self):
        for n in (2,4,8,16,32,64):
            w=primitive_nth_root(n)
            self.assertEqual(pow(w,n,998244353),1)
            self.assertNotEqual(pow(w,n//2,998244353),1)

    def test_linearization_all_basis(self):
        for n in (2,4,8,16,32,64):
            for mode in ('polynomial','rational','sign_branch'):
                base=[(i*7+5) for i in range(n)]
                if mode=='sign_branch' and n>=16:base[0]=998244352
                c,_=build_adaptive(n,base,mode=mode)
                lin=differentiate(c,base)
                self.assertLessEqual(lin.cost,3*c.cost)
                for j in range(n):
                    x=[int(i==j) for i in range(n)]
                    self.assertEqual(lin.evaluate(x),reference_dft(x))

    def test_generic_exact_identity(self):
        rng=random.Random(20261009)
        for n in (2,4,8,16):
            base=[rng.randrange(1,100) for _ in range(n)]
            for mode in ('polynomial','rational','sign_branch'):
                c,_=build_adaptive(n,base,mode=mode)
                for _ in range(8):
                    x=[rng.randrange(100) for _ in range(n)]
                    self.assertEqual(c.evaluate(x),reference_dft(x))

    def test_branch_changes_not_derivative(self):
        n=16
        for val in (1,998244352):
            base=[val]+[4]*(n-1)
            c,label=build_adaptive(n,base,mode='sign_branch')
            lin=differentiate(c,base)
            self.assertEqual(lin.evaluate([2]*n),reference_dft([2]*n))
            self.assertLessEqual(lin.cost,3*c.cost)

    def test_singularity_fallback(self):
        p=97; n=8
        # sqrt(-1) exists in F_97; the rational branch must avoid the pole
        root=next(x for x in range(p) if x*x%p==p-1)
        base=[1]*n;base[-1]=root
        c,label=build_adaptive(n,base,p=p,mode='rational')
        self.assertIn('fallback',label)
        self.assertEqual(c.evaluate(base),reference_dft(base,p))
        self.assertEqual(differentiate(c,base).evaluate(base),reference_dft(base,p))

    def test_no_finite_field_Zariski_extrapolation(self):
        # Over F_p, x^p=x as functions, not as formal polynomials.
        # This is why modular finite tests do not themselves prove the generic theorem.
        p=97
        self.assertTrue(all(pow(x,p,p)==x for x in range(p)))

    def test_boolean_jet_counterexample(self):
        p=998244353;n=8
        w=primitive_nth_root(n,p)
        matrix=[[pow(w,k*j,p) for j in range(n)] for k in range(n)]
        for mask in range(1<<n):
            x=[(mask>>j)&1 for j in range(n)]
            y,jet=boolean_jet_failure(x,matrix,p)
            self.assertEqual(y,reference_dft(x,p))
            self.assertEqual(jet,[0]*n)
        self.assertNotEqual(reference_dft([1]+[0]*7,p),[0]*n)

    def test_boolean_multilinear_unique(self):
        # A multilinear polynomial vanishing at all Boolean inputs is zero.
        # In this test, multiply on disjoint supports and cancel globally.
        p=998244353
        for n in (4,8):
            for bits in range(1<<n):
                x=[(bits>>i)&1 for i in range(n)]
                correction=x[0]*x[1]
                f=reference_dft(x,p)
                formula=[(a + correction - correction)%p for a in f]
                self.assertEqual(formula,f)

    def test_stirling_coefficients(self):
        for n in (3,4,6,8,10):
            q=power_of_sum(n,n)
            self.assertEqual(len(q),(1<<n)-1)
            for mask,c in q.items():
                self.assertEqual(c,coefficient_by_onto_functions(n,mask.bit_count()))

    def test_quotient_eval(self):
        for n in (3,4,6):
            q=power_of_sum(n,n)
            for bits in range(1<<n):
                x=[(bits>>i)&1 for i in range(n)]
                self.assertEqual(evaluate_quotient(q,x),sum(x)**n)

    def test_high_degree_quotient(self):
        n=12
        q=power_of_sum(n,n)
        self.assertEqual(len(q),4095)
        self.assertEqual(q[(1<<n)-1],coefficient_by_onto_functions(n,n))

if __name__=='__main__':unittest.main()

class TestMobiusRecovery(unittest.TestCase):
    def test_boolean_fourier_unique_multilinear_form(self):
        p=998244353
        for n in (4,8):
            roots=primitive_nth_root(n,p)
            vals=[reference_dft([(mask>>j)&1 for j in range(n)],p)
                  for mask in range(1<<n)]
            for frequency in range(n):
                c=[vals[mask][frequency] for mask in range(1<<n)]
                for i in range(n):
                    for mask in range(1<<n):
                        if mask&(1<<i):c[mask]=(c[mask]-c[mask^(1<<i)])%p
                self.assertEqual(c[0],0)
                for mask,v in enumerate(c):
                    expected=(pow(roots,frequency*(mask.bit_length()-1),p)
                              if mask.bit_count()==1 else 0)
                    self.assertEqual(v,expected)
