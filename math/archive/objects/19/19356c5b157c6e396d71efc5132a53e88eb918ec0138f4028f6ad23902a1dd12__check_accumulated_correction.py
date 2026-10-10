"""Independent exact controls for dyadic natural-term correction rank/cost."""
from pathlib import Path
from fractions import Fraction as F
import json
import sympy as s

HERE=Path(__file__).resolve().parent
def green(n,p):return [[p**((i-j)%n)/(1-p**n)for j in range(n)]for i in range(n)]
def rank(A):
    A=[row.copy()for row in A];row=0
    for col in range(len(A[0])):
        pivot=next((i for i in range(row,len(A))if A[i][col]),None)
        if pivot is None:continue
        A[row],A[pivot]=A[pivot],A[row]
        lead=A[row][col];A[row]=[v/lead for v in A[row]]
        for i in range(row+1,len(A)):
            lead=A[i][col]
            if lead:A[i]=[x-lead*y for x,y in zip(A[i],A[row])]
        row+=1
    return row
def cyclic(y,a,b,inv):
    n=len(y);mul=add=0;h=y[1]
    for i in range(2,n):h=y[i]+a*h;mul+=1;add+=1
    z=[(y[0]+b*h)*inv];mul+=2;add+=1
    for i in range(1,n):z.append(y[i]+a*z[-1]);mul+=1;add+=1
    return z,mul,add
records=[]
for n in [4,8,16,32]:
    for k in [2**j for j in range(1,n.bit_length())]:
        m=n//k;p=F(2,7);d=F(3,5);r=p**m;vscale=d**m;local=p*d
        G=green(n,p)
        Q=[[d**(i-j)*G[i][j] if i//m!=j//m else F(0) for j in range(n)]for i in range(n)]
        C=green(k,r)
        for i in range(k):C[i][i]-=1/(1-r**k)
        u=[local**i for i in range(m)];v=[local**(-j)for j in range(m)]
        for i in range(n):
            for j in range(n):
                alpha,ii=divmod(i,m);beta,jj=divmod(j,m)
                assert Q[i][j]==vscale**(alpha-beta)*C[alpha][beta]*u[ii]*v[jj]
        assert rank(C)==k and rank(Q)==k
        x=[F(i+1,3*i+2)for i in range(n)]
        h=[];mult=adds=0
        for b in range(k):
            h.append(sum(v[j]*x[b*m+j]for j in range(m)));mult+=m;adds+=m-1
        y,mm,aa=cyclic(h,r*vscale,r*vscale**(1-k),1/(1-r**k));mult+=mm;adds+=aa
        y=[y[i]-h[i]/(1-r**k)for i in range(k)];mult+=k;adds+=k
        out=[u[j]*y[b]for b in range(k)for j in range(m)];mult+=n
        assert out==[sum(Q[i][j]*x[j]for j in range(n))for i in range(n)]
        assert (mult,adds)==(2*n+3*k-1,n+2*k-2)
        records.append({'N':n,'k':k,'rank':k,'factorization_checked':True,'apply_matches_dense':True,'multiplications':mult,'additions':adds})
# Exact exceptional complex control: r is a primitive sixth root.
r=(1+s.sqrt(-3))/2;k=4
C=s.Matrix(k,k,lambda i,j:r**((i-j)%k)/(1-r**k) if i!=j else 0).applyfunc(s.simplify)
assert s.simplify(r**k-1)!=0
assert s.simplify((r**k)**(k-1)-1)==0
exceptional_rank=C.rank()
assert exceptional_rank==3
eigenvalues=[s.simplify(r*(zeta-r**(k-1))/((1-r*zeta)*(1-r**k)))for zeta in [1,s.I,-1,-s.I]]
assert sum(v==0 for v in eigenvalues)==1
out={'passed':True,'generic_rational_controls':records,'exceptional_complex_control':{'k':4,'r':'(1+sqrt(-3))/2','rank':exceptional_rank,'zero_eigenvalues':1},'proof_scope':'Controls accompany the symbolic all-size compression and eigenvalue proof; no full-product lower bound is claimed.','linear_apply_bound':{'multiplications':'2N+3k-1','additions':'N+2k-2'},'p_zero_boundary':'The natural term is I, so the off-block correction is identically zero.'}
(HERE/'ACCUMULATED_CORRECTION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print('Verified',len(records),'generic compression/rank/counted-application controls and one exact exceptional rank drop.')
