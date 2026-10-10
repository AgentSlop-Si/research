"""Independent rational-number check for midpoint and cubic gauge theorems.

Does not import degree_boundary; uses exact fractions rather than modular code.
"""
from fractions import Fraction as F
from itertools import product
from random import Random


def qpoly(x,A,alpha):
    # Degree-two Boolean-correct polynomial, arbitrary target linear map A.
    return [sum(A[k][i]*x[i]+alpha[k][i]*(x[i]*x[i]-x[i])
                for i in range(len(x))) for k in range(len(A))]


def cpoly(x,A,gauge):
    n=len(x)
    def pairs():
        for i in range(n):
            for j in range(i+1,n):
                yield (i,j,x[i]*x[i]*x[j]-x[i]*x[j]*x[j])
    values=list(pairs())
    return [sum(A[k][i]*x[i]**3 for i in range(n))+
            sum(gauge[k][t]*v for t,(_,__,v) in enumerate(values))
            for k in range(len(A))]


def cjac(a,h,A,gauge):
    n=len(a)
    out=[sum(A[k][i]*3*a[i]*a[i]*h[i] for i in range(n))
         for k in range(len(A))]
    t=0
    for i in range(n):
        for j in range(i+1,n):
            d=2*a[i]*h[i]*a[j]+a[i]**2*h[j]-h[i]*a[j]**2-2*a[i]*a[j]*h[j]
            for k in range(len(A)):
                out[k]+=gauge[k][t]*d
            t+=1
    return out


def det_bareiss(M):
    A=[[F(v) for v in row] for row in M]
    n=len(A);p=F(1)
    for k in range(n-1):
        if A[k][k]==0:
            swap=next((i for i in range(k+1,n) if A[i][k]),None)
            if swap is None:return F(0)
            A[k],A[swap]=A[swap],A[k]
            p=-p
        for i in range(k+1,n):
            for j in range(k+1,n):
                A[i][j]=(A[k][k]*A[i][j]-A[i][k]*A[k][j])/p
        p=A[k][k]
        for i in range(k+1,n):A[i][k]=0
    return A[-1][-1]


def main():
    rng=Random(20261009)
    r={'quadratic_boolean_cases':0,'quadratic_general_midpoint_cases':0,
       'cubic_boolean_cases':0,'cubic_nplus1_cases':0,'moment_determinant_cases':0}
    for n in (2,3,4,5,6):
        A=[[F(rng.randrange(-4,5)) for i in range(n)] for k in range(n)]
        alpha=[[F(rng.randrange(-4,5)) for i in range(n)] for k in range(n)]
        gauge=[[F(rng.randrange(-4,5)) for t in range(n*(n-1)//2)] for k in range(n)]
        for bits in product((F(0),F(1)),repeat=n):
            ref=[sum(A[k][i]*bits[i] for i in range(n)) for k in range(n)]
            assert qpoly(bits,A,alpha)==ref
            assert cpoly(bits,A,gauge)==ref
            r['quadratic_boolean_cases']+=1;r['cubic_boolean_cases']+=1
        for __ in range(8):
            h=[F(rng.randrange(-10,11),rng.randrange(1,8)) for i in range(n)]
            midpoint=[F(1,2)]*n
            vp=qpoly([v+x for v,x in zip(midpoint,h)],A,alpha)
            vm=qpoly([v-x for v,x in zip(midpoint,h)],A,alpha)
            ref=[sum(A[k][i]*h[i] for i in range(n)) for k in range(n)]
            assert [(x-y)/2 for x,y in zip(vp,vm)]==ref
            r['quadratic_general_midpoint_cases']+=1
            y=cjac([F(1)]*n,h,A,gauge)
            for j in range(n):
                e=[F(int(i==j)) for i in range(n)]
                z=cjac(e,h,A,gauge)
                y=[t+u for t,u in zip(y,z)]
            assert [v/6 for v in y]==ref
            r['cubic_nplus1_cases']+=1
        # determinant of M=(I+11^T)/6 equals (n+1)/6^n
        M=[[F(2 if i==j else 1,6) for j in range(n)] for i in range(n)]
        assert det_bareiss(M)==F(n+1,6**n)
        r['moment_determinant_cases']+=1
    return r

if __name__=='__main__':
    import json
    print(json.dumps(main(),indent=2))
