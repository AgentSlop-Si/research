#!/usr/bin/env python3
"""Fresh exact reconstruction of the b=3 cross gate. No source program imported."""
import json
from collections import Counter
from pathlib import Path
P,Q,N=53,16,13
ROOT=Path(__file__).resolve().parent

def g(e,d,a,b):
    r=e*a%N;l=d*b%N
    if r+l>=N:return 0
    w=pow(Q,(e*d)%N,P)
    z=1
    for i in range(1,l+1):
        z=z*(1-pow(w,r+i,P))*pow((1-pow(w,i,P))%P,-1,P)%P
    return z
G={(e,d,a,b):g(e,d,a,b) for e in [-1,1] for d in [-1,1] for a in range(N) for b in range(N)}

def f(a,b):return pow(Q,10*(a+b)**2%N,P)
def u(y,a,b):
    return ((f(a,b)-pow(y,N-a-b,P)*G[-1,1,a,b]*pow(G[-1,1,N-b,b],-1,P))*pow(G[1,1,a,b],-1,P))%P

def solve(M,B):
    nr,nc=len(M),len(M[0]);A=[[v%P for v in r]+[b%P] for r,b in zip(M,B)];row=0;piv=[]
    for j in range(nc):
        k=next((k for k in range(row,nr) if A[k][j]),None)
        if k is None:continue
        A[row],A[k]=A[k],A[row]
        s=pow(A[row][j],-1,P);A[row]=[v*s%P for v in A[row]]
        for k in range(nr):
            if k!=row:
                s=A[k][j];A[k]=[(v-s*w)%P for v,w in zip(A[k],A[row])]
        piv.append(j);row+=1
        if row==nr:break
    assert not any(not any(r[:nc]) and r[-1] for r in A)
    out=[0]*nc
    for i,j in enumerate(piv):out[j]=A[i][-1]
    assert all(sum(x*y for x,y in zip(r,out))%P==b%P for r,b in zip(M,B))
    return out,piv

def line(y):
    E=[[u(y,a+j,b) for j in range(8)] for b,a in [(1,1),(1,2),(1,3),(1,4),(2,2),(2,3)]]
    M=[r[:6] for r in E]
    c,pc=solve(M,[-r[7] for r in E]);n,pn=solve(M,[-r[6] for r in E])
    assert pc==pn==list(range(6))
    c += [0,1];n += [1,0]
    for r in E:
        assert sum(x*y for x,y in zip(r,c))%P==0
        assert sum(x*y for x,y in zip(r,n))%P==0
    return c,n

def cross_gate(y,z,c,n):
    U=[u(y,a,3) for a in range(1,10)]
    V=[pow(z,a,P)*G[1,-1,a,3]*pow(G[1,1,a,3],-1,P)%P for a in range(1,10)]
    assert all(x==0 for x in V[2:]) and V[1]!=0
    E=[[sum(h[j]*U[s+j] for j in range(8))%P for h in [c,n]] for s in [0,1]]
    F=[[sum(h[j]*V[s+j] for j in range(8))%P for h in [c,n]] for s in [0,1]]
    def times(a,b):return [a[0]*b[0]%P,(a[0]*b[1]+a[1]*b[0])%P,a[1]*b[1]%P]
    a,b=times(E[0],F[1]),times(E[1],F[0])
    return [(x-y)%P for x,y in zip(a,b)]

def main():
    lines={y:line(y) for y in range(1,P)};rows=[];zero=[];degrees=Counter()
    for y in range(1,P):
        for z in range(1,P):
            c,n=lines[y];poly=cross_gate(y,z,c,n)
            deg=max((j for j,v in enumerate(poly) if v),default=-1)
            degrees[deg]+=1
            if deg<0:zero.append([y,z])
            rows.append({'y':y,'z':z,'quadratic':poly,'degree':deg})
    result={'scope':'all y,z in F53*, lambda arbitrary over F_(53^11)','counts':dict(degrees),'zero_polynomial_pairs':zero,'lines':{y:{'c':c,'n':n} for y,(c,n) in lines.items()},'gates':rows}
    (ROOT/'CROSS_GATE_CENSUS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'counts':dict(degrees),'zero_polynomial_pairs':zero}))
if __name__=='__main__':main()
