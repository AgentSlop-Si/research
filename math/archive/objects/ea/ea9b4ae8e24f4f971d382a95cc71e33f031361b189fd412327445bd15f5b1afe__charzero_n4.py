"""Independent exact characteristic-zero proof for the N=4 Phase-38 witness.

This is an independent SymPy calculation over Q(i), not a finite-field lift.
"""
import json, sympy as s
from phase37_curvature import seeded_cycles

def green(n,order,alpha):
    pos={x:i for i,x in enumerate(order)}
    return s.Matrix(n,n,lambda i,j:alpha**((pos[i]-pos[j])%n)/(1-alpha**n))

def verify(n=4):
    assert n==4
    I=s.I
    alpha=[(1+I)/4,(2+I)/7,(1+2*I)/8,(1-I)/5,(2+I)/9,(1+I)/6]
    cyc=seeded_cycles(n)
    G=[green(n,c,a) for c,a in zip(cyc,alpha)]
    A=G[0]+(1+I)/3*G[1]
    C=G[4]+(1-I)/4*G[5]
    F=s.Matrix(n,n,lambda i,j:I**(i*j))
    T=A.inv()*F*C.inv()
    z=s.Symbol('z')
    B=G[2]+z*G[3]
    fs=[]
    for j in (1,2):
        f=s.cancel(T[1,j]*T[0,0]*B[1,0]*B[0,j]
                   -T[1,0]*T[0,j]*B[1,j]*B[0,0])
        fs.append(s.Poly(f,z,extension=I))
    d=s.gcd(fs[0],fs[1])
    R=s.resultant(fs[0].as_expr(),fs[1].as_expr(),z)
    assert d.degree()==0 and R!=0
    return {'N':4,'field':'Q(i)','degrees':[int(f.degree()) for f in fs],
            'gcd_degree':int(d.degree()), 'resultant_nonzero':bool(R!=0),
            'six_cycle_orders':cyc,'outer_invertible':A.det()!=0 and C.det()!=0}

if __name__=='__main__':
    print(json.dumps(verify(),indent=2))
