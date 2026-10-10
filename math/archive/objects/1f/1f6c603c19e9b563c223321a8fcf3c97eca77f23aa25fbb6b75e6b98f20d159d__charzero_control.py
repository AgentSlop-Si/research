"""Independent exact Q(i) control for small Phase-37 two-mask circuits.
No finite-field lifting assumptions required for this test.
"""
from __future__ import annotations
import sys, argparse
import sympy as s
from phase37_curvature import seeded_cycles

def verify(n=4):
    assert n in (4,8)
    I=s.I
    cycles=seeded_cycles(n,37037)
    alpha=[(1+I)/4,(2+I)/7,(1+2*I)/8,(1-I)/5,(2+I)/9,(1+I)/6]
    def green(cyc,a):
        pos={value:k for k,value in enumerate(cyc)}
        t=1-a**n
        return s.Matrix(n,n,lambda i,j:a**((pos[i]-pos[j])%n)/t)
    G=[green(c,a) for c,a in zip(cycles,alpha)]
    A=G[0]+(1+I)/3*G[1]
    C=G[4]+(1-I)/4*G[5]
    D1=s.diag(*[I**((3*j+1)%4) for j in range(n)])
    D2=s.diag(*[I**((j*j+j+1)%4) for j in range(n)])
    # Evaluate only columns 0,1,2 and only rows 0,1, reducing intermediate work.
    V=(D2*C)[:,:3]
    b0=(D1*G[2]*V)
    b1=(D1*G[3]*V)
    m0=(A*b0)[:2,:]
    m1=(A*b1)[:2,:]
    X=s.Symbol('lambda')
    def pol(j,k):
        vals=lambda row,col:s.cancel(m0[row,col]+X*m1[row,col])
        numerator=s.expand(vals(0,j)*vals(1,k))
        denominator=s.expand(vals(0,k)*vals(1,j))
        return s.Poly(s.expand(numerator**n-denominator**n),X,extension=I)
    f=pol(0,1);g=pol(0,2)
    gcd=s.gcd(f,g)
    return {'N':n,'degrees':[f.degree(),g.degree()],
            'charzero_gcd_degree':gcd.degree(),
            'charzero_gcd_one':gcd.degree()==0}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--n',type=int,default=4);arg=a.parse_args()
    print(verify(arg.n))
