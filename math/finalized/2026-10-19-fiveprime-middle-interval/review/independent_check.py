#!/usr/bin/env python3
"""Independent, exact original-index controls for the 5q middle interval.
Not a square-mask census. No floating-point arithmetic or external dependencies.
"""
from itertools import combinations
from hashlib import sha256
from pathlib import Path
import json

OUT=Path(__file__).resolve().parent

def divide_monic(numerator,denominator):
    r=list(numerator); m=len(denominator)-1
    out=[0]*max(1,len(r)-m)
    for k in range(len(r)-1,m-1,-1):
        if r[k]:
            t=r[k]; out[k-m]=t
            for j,c in enumerate(denominator): r[k-m+j]-=t*c
    assert not any(r)
    while len(out)>1 and out[-1]==0: out.pop()
    return out

def phi_pq(q):
    # (x^(5q)-1)(x-1)/[(x^5-1)(x^q-1)]
    N=5*q
    num=[0]*(N+2)
    num[0]=1; num[1]=-1; num[N]=-1; num[N+1]=1
    den=[0]*(q+6)
    den[0]=1; den[5]=-1; den[q]=-1; den[q+5]=1
    p=divide_monic(num,den)
    assert len(p)==4*(q-1)+1 and p[-1]==1
    return p

def reduce_poly(c,p):
    c=list(c); deg=len(p)-1
    for i in range(len(c)-1,deg-1,-1):
        t=c[i]
        if t:
            for j,a in enumerate(p):
                c[i-deg+j]-=t*a
    return tuple(c[:deg])

def coordinates(q):
    N=5*q; e5=q*pow(q,-1,5); eq=5*pow(5,-1,q)
    indices={(a,b):(a*e5+b*eq)%N for a in range(5) for b in range(q)}
    return N,e5,eq,indices

def zero_sum(S,h,q,p):
    N=5*q; c=[0]*N
    for x in S: c[(h*x)%N]+=1
    return not any(reduce_poly(c,p))

def run(q,full_local):
    N,e5,eq,idx=coordinates(q); p=phi_pq(q)
    crt=0
    for (a,b),r in idx.items():
        for (u,v),c in idx.items():
            assert (r*c-e5*a*u-eq*b*v)%N==0; crt+=1
    pairs=list(combinations(range(5),2))
    support={(A,f):{idx[u,v] for u in range(5) for v in range(q) if u in A or v==f} for A in pairs for f in range(q)}
    hs=[idx[a,b] for a in range(1,5) for b in range(1,q)] if full_local else [idx[1,1]]
    local=0; zeros=0
    for A in pairs:
      for B in pairs:
       for f in range(q):
        for g in range(q):
         S=support[A,f]&support[B,g]
         predicted=(A==B and f!=g) or (not set(A)&set(B) and f==g)
         for h in hs:
            actual=zero_sum(S,h,q,p)
            assert actual==predicted,(q,A,B,f,g,h,actual,predicted)
            local+=1; zeros+=actual
    # Row/column-regular candidate with genuinely group-dependent fiber permutations.
    # It satisfies all same-a row-Gram conditions but must fail a primitive pair.
    rowkeys=sorted(idx,key=idx.get)
    mask=[]
    for a,b in rowkeys:
        A=tuple(sorted((a,(a+1)%5)))
        f=((a+1)*b+a)%q
        mask.append(support[A,f])
    assert all(len(S)==2*q+3 for S in mask)
    assert all(sum(c in S for S in mask)==2*q+3 for c in range(N))
    row_zero=row_bad=col_zero=col_bad=samegroup=0
    primitive_failure=None
    colS=[{r for r in range(N) if c in mask[r]} for c in range(N)]
    for r in range(N):
      for s in range(N):
        if r==s: continue
        z=zero_sum(mask[r]&mask[s],r-s,q,p)
        row_zero+=z; row_bad+=not z
        if rowkeys[r][0]==rowkeys[s][0]:
            assert z; samegroup+=1
        if not z and (r-s)%5 and (r-s)%q and primitive_failure is None:
            primitive_failure={"rows":[r,s],"crt_rows":[list(rowkeys[r]),list(rowkeys[s])],"intersection":sorted(mask[r]&mask[s])}
        zc=zero_sum(colS[r]&colS[s],s-r,q,p)
        col_zero+=zc; col_bad+=not zc
    assert row_bad and col_bad and primitive_failure
    # Standard divisor-line positive control, exact both full Gram orders.
    pos=[{idx[u,v] for u in range(5) for v in range(q) if u==a} for a,b in rowkeys]
    poscols=[{r for r in range(N) if c in pos[r]} for c in range(N)]
    positive=0
    for r in range(N):
      for s in range(N):
        if r==s:
            assert len(pos[r])==q and len(poscols[r])==q
        else:
            assert zero_sum(pos[r]&pos[s],r-s,q,p)
            assert zero_sum(poscols[r]&poscols[s],s-r,q,p)
        positive+=2
    return {"q":q,"phi":p,"crt_product_checks":crt,"primitive_local_checks":local,"primitive_local_zeros":zeros,"negative_degree":2*q+3,"negative_row_zero_offdiagonals":row_zero,"negative_row_nonzero_offdiagonals":row_bad,"negative_col_zero_offdiagonals":col_zero,"negative_col_nonzero_offdiagonals":col_bad,"same_group_zero_checks":samegroup,"primitive_failure":primitive_failure,"positive_full_gram_entries":positive}

if __name__=='__main__':
    results={"scope":"Independent exact controls, not an exhaustive square-mask census","results":[run(7,True),run(11,True),run(13,False)]}
    (OUT/'RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({"verdict":"PASS","checks":[{k:r[k] for k in ['q','crt_product_checks','primitive_local_checks','same_group_zero_checks','positive_full_gram_entries']} for r in results['results']]},indent=2))
