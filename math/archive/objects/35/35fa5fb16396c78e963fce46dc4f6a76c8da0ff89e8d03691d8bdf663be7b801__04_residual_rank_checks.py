"""Independent exact modular controls for the near-grid residual rank theorem."""
import json
from pathlib import Path

def factors(n):
    out=[];p=2
    while p*p<=n:
        if n%p==0:
            out.append(p)
            while n%p==0:n//=p
        p+=1
    if n>1:out.append(n)
    return out

def prime(n):
    if n<2:return False
    p=2
    while p*p<=n:
        if n%p==0:return False
        p+=1
    return True

def rank(A,p):
    A=[row[:]for row in A];m=len(A);n=len(A[0]);r=0
    for j in range(n):
        pivot=next((k for k in range(r,m)if A[k][j]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r];inv=pow(A[r][j],-1,p)
        A[r]=[x*inv%p for x in A[r]]
        for i in range(r+1,m):
            q=A[i][j]
            if q:A[i]=[(x-q*y)%p for x,y in zip(A[i],A[r])]
        r+=1
        if r==m:break
    return r

out=[]
for n in [3,5,6,7,9,10,12,15,16,17,24,31,45]:
    Q=1<<(n-1).bit_length();order=n*Q;p=order+1
    while not prime(p):p+=order
    fs=factors(p-1)
    generator=next(g for g in range(2,p)if all(pow(g,(p-1)//q,p)!=1 for q in fs))
    z=pow(generator,(p-1)//order,p)
    nums=[k*Q-n*((2*k*Q+n)//(2*n))for k in range(n)]
    H=[[pow(z,u*j%order,p)for j in range(n)]for u in nums]
    from math import gcd
    expected=n//gcd(n,Q);actual=rank(H,p)
    assert len(set(nums))==expected and actual==expected
    out.append({'N':n,'Q':Q,'prime':p,'root_order':order,'distinct_residues':len(set(nums)),'rank':actual,'expected':expected})
Path(__file__).with_name('RESIDUAL_RANK_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
print('All',len(out),'exact residual-rank controls passed.')
