"""Fresh exact controls for P_{3p}. No repository programs are imported.

Uses integer polynomial arithmetic only. A q-polynomial is a low-first list;
a bivariate polynomial maps X exponent to such a list. All cyclotomic field
valuations are exact, using degree<phi representatives in the t=q-1 basis.
"""
from fractions import Fraction
from math import comb, gcd
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent
checks=[]
def check(label,condition,details=None):
    assert condition,label
    checks.append({'check':label,'passed':True,'details':details})

def trim(a):
    while a and a[-1]==0:a.pop()
    return a
def plus(a,b,sgn=1):
    c=a+[0]*max(0,len(b)-len(a))
    for j,v in enumerate(b):c[j]+=sgn*v
    return trim(c)
def mul(a,b):
    if not a or not b:return []
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]+=x*y
    return trim(c)
def bpadd(a,b,sgn=1):
    c={i:x[:] for i,x in a.items()}
    for i,y in b.items():c[i]=plus(c.get(i,[]),y,sgn)
    return {i:x for i,x in c.items() if x}
def bpmul(a,b):
    c={}
    for i,x in a.items():
        for j,y in b.items():c[i+j]=plus(c.get(i+j,[]),mul(x,y))
    return {i:x for i,x in c.items() if x}
def edge(j):return [1]+[0]*(j-1)+[-1]
def scalar(a,j):return {i:mul(x,edge(j)) for i,x in a.items()}
def block(first,last):
    n=last-first+1
    if n==0:return {0:[1]}
    a,b={0:[1]},{1:[1]}
    for edge_index in range(first,last):
        a,b=b,bpadd({i+1:x for i,x in b.items()},scalar(a,edge_index),-1)
    return b
def vp(a,p):
    assert a
    k=0
    while a%p==0:a//=p;k+=1
    return k,a%p
def specialize(a,p,s):
    # Phi_{p^s}=1+q^m+...+q^{(p-1)m}; monic long division.
    m=p**(s-1);e=(p-1)*m;r=a[:]
    for n in range(len(r)-1,e-1,-1):
        v=r[n]
        if v:
            for k in range(p):r[n-e+k*m]-=v
    r=r[:e];t=[0]*e
    for n,v in enumerate(r):
        if v:
            for j in range(n+1):t[j]+=v*comb(n,j)
    terms=[]
    for j,v in enumerate(t):
        if v:
            k,u=vp(v,p);terms.append((e*k+j,u*((-1)**k)%p))
    if not terms:return None
    w,res=min(terms)
    assert sum(1 for z in terms if z[0]==w)==1
    return w,res
def scaled(poly,p,s,alpha,L,derivative=False):
    result={};valuation_data={}
    for j,a in poly.items():
        if derivative:
            if j==0:continue
            a=[j*z for z in a];j-=1
        z=specialize(a,p,s)
        if z is None:continue
        v,r=z;valuation_data[str(j)]={'valuation':v,'residue':r}
        w=v+j*alpha-L
        assert w>=0,(p,j,alpha,L,w)
        if w==0:result[j]=r
    return result,valuation_data
def lower_hull(data):
    hull=[]
    for a in sorted((int(j),z['valuation']) for j,z in data.items()):
        while len(hull)>1 and Fraction(a[1]-hull[-1][1],a[0]-hull[-1][0])<=Fraction(hull[-1][1]-hull[-2][1],hull[-1][0]-hull[-2][0]):hull.pop()
        hull.append(a)
    return hull

records=[]
for p in [5,7,11,13]:
    s=2;h=(p-1)//2;alpha=Fraction(2*p-1,2*p);c=(-1)**((p+1)//2)%p
    P=block(1,3*p)
    A=[block(k*p+1,(k+1)*p) for k in range(3)]
    L=[block(k*p+1,(k+1)*p-1) for k in range(3)]
    R=[block(k*p+2,(k+1)*p) for k in range(3)]
    M=block(p+2,2*p-1)
    rhs=bpmul(bpmul(A[0],A[1]),A[2])
    rhs=bpadd(rhs,scalar(bpmul(bpmul(L[0],R[1]),A[2]),p),-1)
    rhs=bpadd(rhs,scalar(bpmul(bpmul(A[0],L[1]),R[2]),2*p),-1)
    rhs=bpadd(rhs,scalar(scalar(bpmul(bpmul(L[0],M),R[2]),p),2*p))
    check(f'p={p}: exact triple-block identity',P==rhs)
    for k in [1,2]:
        dif=bpadd(A[k],A[0],-1)
        val=[specialize(a,p,s)[0] for a in dif.values()]
        check(f'p={p}: shifted block {k} coefficient bound',min(val)>=p,{'minimum':min(val)})
    for k in range(3):
        r,_=scaled(A[k],p,s,Fraction(1),Fraction(p))
        check(f'p={p}: block {k} additive residual',r=={p:1,1:c},r)
    r,data=scaled(P,p,s,alpha,3*p*alpha)
    check(f'p={p}: alpha residual',r=={3*p:1,p:(-3)%p},r)
    hull=lower_hull(data)
    check(f'p={p}: exact Newton vertices',hull==[(1,3*p-2),(p,2*p-1),(3*p,0)],hull)
    r,_=scaled(P,p,s,Fraction(1),Fraction(3*p-1))
    check(f'p={p}: t-scale residual',r=={p:(-3)%p,1:(-3*c)%p},r)
    r,_=scaled(P,p,s,alpha,Fraction(3*p-2),True)
    check(f'p={p}: derivative alpha residual',r=={2*p:(3*c)%p,0:(-3*c)%p},r)
    r,_=scaled(P,p,s,Fraction(1),Fraction(3*p-2),True)
    check(f'p={p}: derivative t residual',r=={0:(-3*c)%p},r)
    check(f'p={p}: primitive side denominator',gcd(2*p-1,2*p)==1)
    check(f'p={p}: derivative residual on alpha roots',(6*c)%p!=0)
    check(f'p={p}: derivative residual on t roots',(-3*c)%p!=0)
    check(f'p={p}: exact root-order condition',3*p<p**s)
    records.append({'p':p,'s':s,'degree':3*p,'coefficient_valuations':data,'newton_vertices':hull,'claimed_discriminant_valuation':3*p*(3*p-2)})

p=3;s=3;P=block(1,9)
r,data=scaled(P,p,s,Fraction(5,6),Fraction(15,2))
check('p=3 negative control: generic alpha residual loses its lower term',r=={9:1},r)
check('p=3 exceptional Newton polygon',lower_hull(data)==[(1,12),(3,6),(9,0)],lower_hull(data))
check('p=3 target requires s>=3',not 9<3**2 and 9<3**3)

report={'status':'PASS','checks_passed':len(checks),'checks':checks,'prime_controls':records,'scope':'Exact finite controls; the uniform p>=5 proof and fixed-degree p=3 certificate are in REPORT.md. No equality-mask or root-order census.'}
(OUT/'BOUNDARY_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'status':'PASS','checks_passed':len(checks),'primes':[5,7,11,13],'negative_control_p':3},indent=2))
