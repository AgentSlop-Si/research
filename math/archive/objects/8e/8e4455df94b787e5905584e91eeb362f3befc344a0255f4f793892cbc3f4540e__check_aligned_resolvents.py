#!/usr/bin/env python3
"""Fresh finite controls for the aligned-resolvent corollary; no source imports."""
import json, random
from pathlib import Path

P = 12289
def eye(n): return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col))%P for col in zip(*b)] for row in a]
def add(a,b): return [[(x+y)%P for x,y in zip(r,s)] for r,s in zip(a,b)]
def rank(a):
    a=[r[:] for r in a]; row=0
    if not a: return 0
    for col in range(len(a[0])):
        pivot=next((i for i in range(row,len(a)) if a[i][col]%P),None)
        if pivot is None: continue
        a[row],a[pivot]=a[pivot],a[row]
        f=pow(a[row][col],-1,P);a[row]=[x*f%P for x in a[row]]
        for i in range(len(a)):
            if i!=row:
                f=a[i][col];a[i]=[(x-f*y)%P for x,y in zip(a[i],a[row])]
        row+=1
        if row==len(a):break
    return row
def inverse(a):
    n=len(a); b=[r[:]+e for r,e in zip(a,eye(n))]
    for col in range(n):
        pivot=next((i for i in range(col,n) if b[i][col]%P),None)
        if pivot is None: raise ValueError('singular')
        b[col],b[pivot]=b[pivot],b[col];f=pow(b[col][col],-1,P)
        b[col]=[x*f%P for x in b[col]]
        for i in range(n):
            if i!=col:
                f=b[i][col];b[i]=[(x-f*y)%P for x,y in zip(b[i],b[col])]
    ans=[r[n:] for r in b];assert mm(a,ans)==eye(n);return ans
def cuts(a,k): return ([r[:k] for r in a[k:]],[r[k:] for r in a[:k]])
def mask(a,rng):
    l=[rng.randrange(1,P) for _ in a];r=[rng.randrange(1,P) for _ in a]
    return [[l[i]*a[i][j]*r[j]%P for j in range(len(a))] for i in range(len(a))]

def run():
    rng=random.Random(1520);checks=[]
    # Singular principal blocks cannot be silently excluded.
    swap=[[0,1],[1,0]]; assert inverse(swap)==swap
    assert rank(cuts(swap,1)[0])==1
    for n in [4,8,16,32]:
        ts=[];xs=[]
        for case in range(4):
            while True:
                t=[[0]*n for _ in range(n)]
                for i in range(n):
                    t[i][i]=rng.randrange(P)
                    if i+1<n:
                        t[i][i+1]=rng.randrange(P);t[i+1][i]=rng.randrange(P)
                try:x=inverse(t);break
                except ValueError:pass
            ts.append(t);xs.append(mask(x,rng))
            for k in range(1,n):
                for tx,xx in zip(cuts(t,k),cuts(x,k)):
                    assert rank(tx)==rank(xx)<=1
        assert mm(ts[0],ts[1])!=mm(ts[1],ts[0])
        s=[[0]*n for _ in range(n)];prod=eye(n)
        for count,x in enumerate(xs,1):
            s=add(s,x);prod=mm(prod,x)
            for k in range(1,n):
                assert all(rank(a)<=count for a in cuts(s,k)+cuts(prod,k))
        omega=next(pow(g,(P-1)//n,P) for g in range(2,P)
                   if pow(pow(g,(P-1)//n,P),n//2,P)!=1)
        assert pow(omega,n,P)==1
        f=[[pow(omega,i*j,P) for j in range(n)] for i in range(n)]
        franks=[]
        for k in range(1,n):
            r=rank(cuts(f,k)[0]);assert r==min(k,n-k);franks.append(r)
        checks.append({'n':n,'tridiagonal_cases':4,'noncommuting':True,
                       'inverse_rank_identity_all_cuts':True,'sum_product_budgets_all_cuts':True,
                       'fourier_lower_cut_ranks':franks})
    result={'field':P,'singular_principal_control_passed':True,'cases':checks,
            'all_passed':True,'scope':'Exact finite-field controls. Complex all-N assertions follow from supplied proof, not extrapolation.'}
    out=Path(__file__).with_name('aligned_resolvent_results.json');out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
