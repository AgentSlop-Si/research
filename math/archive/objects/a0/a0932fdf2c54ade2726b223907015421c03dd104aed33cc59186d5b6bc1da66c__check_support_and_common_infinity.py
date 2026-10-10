"""Fresh exact support charts and common-infinite-outer N4 check.
Rebuilds Green matrices from geometric sums and adjugates from cofactors.
"""
from pathlib import Path
from itertools import combinations
import json
import sympy as s
HERE=Path(__file__).resolve().parent
a,c,t=s.symbols('a c t');Q=s.QQ_I
Z,V=s.zeros(4),s.zeros(4);order=[0,2,1,3]
for j in range(4):Z[(j+1)%4,j]=1;V[order[(j+1)%4],order[j]]=1
def green(T,p):
    r=s.Rational(1,p)
    return sum((r**j*T**j for j in range(4)),s.zeros(4))/(1-r**4)
G,J=green(Z,4),green(V,5);H=G+t*J
A=s.Matrix(4,4,lambda i,j:s.expand((-1)**(i+j)*H.minor_submatrix(j,i).det()))
co=[A.applyfunc(lambda z:s.Poly(z,t).nth(j))for j in range(4)]
F=s.Matrix(4,4,lambda i,j:s.I**(i*j))
parts={(u,v):co[u]*F*co[v]for u in range(4)for v in range(4)}
K={(i,j):s.Poly.from_dict({uv:s.expand(M[i,j])for uv,M in parts.items()},(a,c),domain=Q)for i in range(4)for j in range(4)}
roots=sorted(set(-G[i,j]/J[i,j]for i in range(4)for j in range(4)))
assert len(roots)==9
records=[]
for b in roots:
    B=G+b*J
    zero=[(i,j)for i in range(4)for j in range(4)if B[i,j]==0]
    equations=[K[z]for z in zero];rectangles=0
    for i,k in combinations(range(4),2):
        for j,l in combinations(range(4),2):
            if all(B[u,v]!=0 for u,v in [(i,j),(i,l),(k,j),(k,l)]):
                equations.append(K[i,j]*K[k,l]*B[i,l]*B[k,j]-K[i,l]*K[k,j]*B[i,j]*B[k,l]);rectangles+=1
    basis=s.groebner(equations,c,a,domain=Q,order='grevlex')
    assert len(basis.polys)==1 and basis.polys[0].is_one
    records.append({'b':str(b),'zero_positions':zero,'supported_rectangles':rectangles,'basis':['1']})
    print('Excluded support branch',b,flush=True)
C=J.adjugate();Kinf=C*F*C
assert Kinf[0,0]!=0
rows=[]
for i in range(1,4):
    for j in range(1,4):
        aa=[G[i,0]*G[0,j],G[i,0]*J[0,j]+J[i,0]*G[0,j],J[i,0]*J[0,j]]
        bb=[G[i,j]*G[0,0],G[i,j]*J[0,0]+J[i,j]*G[0,0],J[i,j]*J[0,0]]
        rows.append([s.expand(Kinf[i,j]*Kinf[0,0]*aa[k]-Kinf[i,0]*Kinf[0,j]*bb[k])for k in range(3)])
det=s.expand(s.Matrix(rows[:3]).det())
assert det!=0
out={'field':'Q(i)','independent_geometric_sum_and_cofactor_construction':True,'zero_middle_branches':records,'both_outer_infinity':{'K00':str(Kinf[0,0]),'rank_minor':str(det),'nonzero':True},'scope':'All finite independently variable outer couplings on every zero-middle support branch; common-infinite outer chart for every projective middle coupling.'}
(HERE/'SUPPORT_AND_COMMON_INFINITY_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n')
print('All support branches and common-infinite-outer chart verified.',flush=True)
