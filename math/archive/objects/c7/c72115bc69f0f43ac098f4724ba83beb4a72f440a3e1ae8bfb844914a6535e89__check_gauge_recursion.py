"""Exact rational controls for the analytically proved gauge block identity.
Includes p=0 and operation-counted weighted-cycle application.
"""
from fractions import Fraction as F
from pathlib import Path
import json

HERE=Path(__file__).resolve().parent
def reversal_order(n):
    order=[0]
    while len(order)<n:order=[2*j for j in order]+[2*j+1 for j in order]
    assert len(order)==n
    return order
def green(n,p,rev=False):
    order=reversal_order(n) if rev else list(range(n))
    pos={j:k for k,j in enumerate(order)}
    den=1-p**n
    assert den
    weights=[p**k/den for k in range(n)]
    return [[weights[(pos[i]-pos[j])%n]for j in range(n)]for i in range(n)]
def natural(n,p,d):
    assert d
    G=green(n,p)
    return [[d**(i-j)*G[i][j]for j in range(n)]for i in range(n)]
def stage(n,p,q,t,d):
    A=natural(n,p,d);J=green(n,q,True)
    return [[A[i][j]+t*J[i][j]for j in range(n)]for i in range(n)]
def matvec(A,x):return [sum(a*b for a,b in zip(row,x))for row in A]

def counted_cycle(y,order,a,b,boundary_inverse):
    # Ordinary edges a, wrap edge b. The boundary reciprocal is supplied.
    n=len(y);mul=add=0
    h=y[order[1]]
    for k in range(2,n):h=y[order[k]]+a*h;mul+=1;add+=1
    x=[F(0)]*n
    x[order[0]]=(y[order[0]]+b*h)*boundary_inverse;mul+=2;add+=1
    for k in range(1,n):x[order[k]]=y[order[k]]+a*x[order[k-1]];mul+=1;add+=1
    assert (mul,add)==(2*n-1,2*n-2)
    return x,mul,add
def counted_stage(y,p,q,t,d):
    n=len(y)
    ordinary=p*d;wrap=p*d**(1-n)
    a,m1,a1=counted_cycle(y,list(range(n)),ordinary,wrap,1/(1-p**n))
    b,m2,a2=counted_cycle(y,reversal_order(n),q,q,1/(1-q**n))
    out=[a[k]+t*b[k]for k in range(n)]
    counts=(m1+m2+n,a1+a2+n)
    assert counts==(5*n-2,5*n-4)
    return out,counts

tests=[]
parameters=[(F(2,7),F(3,11),F(-5,13),F(7,5)),
            (F(-2,3),F(-1,5),F(4,9),F(-3,7)),
            (F(0),F(2,9),F(3,8),F(5,4)),
            (F(1,3),F(0),F(2,5),F(3,2)),
            (F(2,5),F(3,7),F(0),F(1))]
for n in [4,8,16,32]:
    m=n//2
    for p,q,t,d in parameters:
        A=stage(n,p,q,t,d)
        Aprime=stage(m,p*p,q*q,t,d/p if p else d)
        E=green(m,q*q,True)
        order=reversal_order(m);position={j:k for k,j in enumerate(order)}
        predecessor={order[k]:order[(k-1)%m]for k in range(m)}
        U=[[d**(i-j)*p**(m+i-j)/(1-p**n)for j in range(m)]for i in range(m)]
        for i in range(m):
            for j in range(m):
                assert A[i][j]==Aprime[i][j]
                assert A[m+i][m+j]==Aprime[i][j]
                assert A[i][m+j]==d**(-m)*U[i][j]+t*q*E[predecessor[i]][j]
                assert A[m+i][j]==d**m*U[i][j]+t*q*E[i][j]
        N=natural(n,p,d)
        for i in range(n):
            edge=p*d if i else p*d**(1-n)
            for j in range(n):assert N[i][j]-edge*N[(i-1)%n][j]==int(i==j)
        assert (p*d)**(n-1)*(p*d**(1-n))==p**n
        y=[F(k+1,2*k+3)for k in range(n)]
        got,counts=counted_stage(y,p,q,t,d)
        assert got==matvec(A,y)
        if p:
            assert U[0][0]
            assert all(U[i][j]*U[0][0]==U[i][0]*U[0][j]for i in range(m)for j in range(m))
            assert (p*p)**m==p**n and (q*q)**m==q**n
        else:assert all(v==0 for row in U for v in row)
        tests.append({'N':n,'parameters':[str(z)for z in (p,q,t,d)],'both_principal_halves':True,'both_crossblocks':True,'weighted_inverse_identity':True,'counted_apply_matches_dense':True,'multiplications':counts[0],'additions':counts[1]})
out={'passed':True,'arithmetic':'Exact rational arithmetic','controls':tests,'proof_scope':'Finite controls support the separate symbolic all-N derivation; these controls alone are not an all-N proof.','three_stage_supplied_coefficient_ledger':{'multiplications':'17N-6','additions':'15N-12'},'limits':'No masks/twiddles synthesis or full-product Fourier recurrence is claimed.'}
(HERE/'GAUGE_RECURSION_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print('Verified',len(tests),'exact controls, both diagonal/cross blocks, p=0, weighted inverse, and counted stage schedule.')
