#!/usr/bin/env python3
"""Cold arithmetic control. Reads inert census data, not the discovery program."""
import json,hashlib
from pathlib import Path
from collections import Counter
R=Path(__file__).resolve().parent
p=53

def gauss(e,d,a,b):
    r=e*a%13;l=d*b%13
    if r+l>=13:return 0
    w=pow(16,e*d%13,p)
    row=[1]
    for n in range(1,r+l+1):
        row=[1]+[(row[k] if k<len(row) else 0)+pow(w,n-k,p)*row[k-1] for k in range(1,n+1)]
        row=[x%p for x in row]
    return row[l]

G={(e,d,a,b):gauss(e,d,a,b) for e in [1,-1] for d in [1,-1] for a in range(13) for b in range(13)}
def target(a,b):return pow(16,10*(a+b)**2%13,p)
def moment(y,a,b):
    cross=pow(y,13-a-b,p)*G[-1,1,a,b]*pow(G[-1,1,13-b,b],-1,p)%p
    return (target(a,b)-cross)*pow(G[1,1,a,b],-1,p)%p

def affine(y):
    A=[]
    for b,a in [(1,1),(1,2),(1,3),(1,4),(2,2),(2,3)]:
        v=[moment(y,a+j,b) for j in range(8)];A.append(v[:7]+[-v[7]%p])
    row=0;piv=[]
    for col in range(7):
        k=next((k for k in range(row,6) if A[k][col]),None)
        if k is None:continue
        A[row],A[k]=A[k],A[row]
        q=pow(A[row][col],-1,p);A[row]=[q*x%p for x in A[row]]
        for k in range(6):
            if k!=row:
                q=A[k][col];A[k]=[(x-q*y)%p for x,y in zip(A[k],A[row])]
        piv.append(col);row+=1
        if row==6:break
    assert piv==list(range(6))
    return [A[i][7] for i in range(6)]+[0,1],[-A[i][6]%p for i in range(6)]+[1,0]

def direct(h,y,z):
    E=[];F=[]
    for a in [1,2]:
        E.append(sum(h[j]*moment(y,a+j,3) for j in range(8))%p)
        F.append(sum(h[j]*pow(z,a+j,p)*G[1,-1,a+j,3]*pow(G[1,1,a+j,3],-1,p) for j in range(8))%p)
    return (E[0]*F[1]-E[1]*F[0])%p

def main():
    census=json.loads((R/'CROSS_GATE_CENSUS.json').read_text());rows=census['gates'];count=Counter();checks=0
    assert len(rows)==2704 and len({(r['y'],r['z']) for r in rows})==2704
    lines={y:affine(y) for y in range(1,p)}
    for y,(c,n) in lines.items():assert census['lines'][str(y)]=={'c':c,'n':n}
    exceptional=[]
    for r in rows:
        y,z=r['y'],r['z'];c,n=lines[y]
        evals=[direct([(a+lam*b)%p for a,b in zip(c,n)],y,z) for lam in [0,1,2]]
        a2=(evals[2]-2*evals[1]+evals[0])*pow(2,-1,p)%p
        a1=(evals[1]-evals[0]-a2)%p;a0=evals[0];poly=[a0,a1,a2]
        assert poly==r['quadratic']
        deg=max((i for i,v in enumerate(poly) if v),default=-1)
        assert deg==r['degree'] and deg>=0
        count[deg]+=1
        if deg==0:exceptional.append(r)
        for lam in range(p):
            h=[(a+lam*b)%p for a,b in zip(c,n)]
            assert direct(h,y,z)==sum(v*pow(lam,j,p) for j,v in enumerate(poly))%p
            checks+=1
    # The geometry that removes the opposite same-sign support is verified
    # independently for every row actually used in b=3 compatibility.
    for a in range(1,10):
        assert G[-1,-1,a,3]==0 and G[1,1,a,3]!=0
        assert (G[1,-1,a,3]!=0)==(a in [1,2])
    assert all(G[e,d,10,3]==0 for e,d in [(1,1),(1,-1),(-1,-1)])
    assert G[-1,1,10,3]!=0 and target(10,3)==1
    # Every reflected instance has the same target and Gaussian factor.
    for e in [1,-1]:
        for d in [1,-1]:
            for a in range(13):
                for b in range(13):
                    assert G[e,d,a,b]==G[-e,-d,-a%13,-b%13]
                    assert target(a,b)==target(-a%13,-b%13)
    result={'verdict':'PASS','cross_pairs':2704,'degree_counts':dict(count),'zero_polynomials':0,'scalar_gate_checks':checks,'constant_obstructions':exceptional,'frozen_census_sha256':hashlib.sha256((R/'CROSS_GATE_CENSUS.json').read_bytes()).hexdigest(),'method':'Gaussian Pascal recurrence; full six-by-seven RREF; three-point degree-two interpolation plus all 53 scalar controls; no discovery import','scope':'arithmetic verification, not independent human theorem acceptance'}
    (R/'INDEPENDENT_CROSS_ARITHMETIC.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
