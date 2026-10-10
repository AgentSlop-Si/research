"""Independent exact Q(i) audit of the Phase 39 two-parameter certificate at N=4.
No finite-field modular inference is used in this test.
"""
import json
import sympy as S
import phase37_curvature as q
from phase39_bivariate import MON1, MON2, MON3, MON4, FOUR, PATH
N=4; I=S.I
cycles=q.seeded_cycles(N,37037)
alpha=[(1+I)/4,(2+I)/7,(1+2*I)/8,(1-I)/5,(2+I)/9,(1+I)/6]

def green(order,a):
    pos={v:j for j,v in enumerate(order)}
    return S.Matrix(N,N,lambda i,j:a**((pos[i]-pos[j])%N)/(1-a**N))

Gs=[green(c,a) for c,a in zip(cycles,alpha)]
B2=green(cycles[0],(1+3*I)/11)
A=Gs[0]+(1+I)/3*Gs[1]
C=Gs[4]+(1-I)/4*Gs[5]
F=S.Matrix(N,N,lambda j,k:I**((j*k)%4))
T=A.inv()*F*C.inv()
B=(Gs[2],Gs[3],B2)
x=S.symbols('x0 x1 x2')
Y=S.zeros(N,N)
for t,bt in enumerate(B):Y+=x[t]*bt

def minor(a,b):
    # Two rows 0,1, columns a,b.
    return S.expand(T[0,a]*T[1,b]*Y[1,a]*Y[0,b]-
                    T[0,b]*T[1,a]*Y[1,b]*Y[0,a])

def certificate(kind):
    if kind=='cubic': pairs=FOUR; factors=MON1; outmons=MON3
    else: pairs=PATH; factors=MON2; outmons=MON4
    mat=[]
    for a,b in pairs:
        poly=S.Poly(minor(a,b),*x,extension=I)
        f=[poly.coeff_monomial(x[0]**k[0]*x[1]**k[1]*x[2]**k[2]) for k in MON2]
        for mult in factors:
            row=[]
            for mon in outmons:
                source=tuple(m-n for m,n in zip(mon,mult))
                row.append(f[MON2.index(source)] if source in MON2 else 0)
            mat.append(row)
    return mat

if __name__=='__main__':
    assert A.det()!=0 and C.det()!=0
    from sympy.polys.matrices import DomainMatrix
    from sympy import QQ_I
    out={}
    for typ,full in [('cubic',10),('quartic',15)]:
        rows=certificate(typ)
        mat=DomainMatrix.from_Matrix(S.Matrix(rows)).convert_to(QQ_I)
        rank=mat.rank()
        assert rank==full,(typ,rank)
        out[typ]={'rank':rank,'columns':full,'rows':len(rows)}
        print(typ,rank,'/',full,flush=True)
    with open('charzero_n4.json','w') as f:json.dump({'field':'Q(i)','N':4,'certificates':out},f,indent=2)
