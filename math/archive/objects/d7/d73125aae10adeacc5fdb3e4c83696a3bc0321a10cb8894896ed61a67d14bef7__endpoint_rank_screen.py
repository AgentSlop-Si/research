"""Exact necessary rank tests for two raw bidirectional scan stages.
Own code. Modular ranks certify LOWER bounds on the complex cyclotomic rank.
No finite-field coefficient specialization of the hypothetical factors is assumed.
"""
from pathlib import Path
from itertools import permutations
import json
import numpy as np

PRIME=257
GENERATOR=3

def fourier(n):
    w=pow(GENERATOR,(PRIME-1)//n,PRIME)
    assert pow(w,n,PRIME)==1 and pow(w,n//2,PRIME)!=1
    return np.array([[pow(w,i*j,PRIME) for j in range(n)] for i in range(n)],dtype=np.int64)

def all_prefix_ranks(a):
    n=a.shape[0]
    out=np.zeros((n+1,n+1),dtype=np.int64)
    for k in range(1,n+1):
        basis={}
        for j in range(n):
            v=a[:k,j].copy()
            for h in sorted(basis):
                if v[h]: v=(v-int(v[h])*basis[h])%PRIME
            piv=np.flatnonzero(v)
            if len(piv):
                h=int(piv[0]); basis[h]=v*pow(int(v[h]),-1,PRIME)%PRIME
            out[k,j+1]=len(basis)
    return out

def rank_tables(a):
    return [all_prefix_ranks(b) for b in (a,a[:,::-1],a[::-1,:],a[::-1,::-1])]

def pcount(p):
    n=len(p); a=np.zeros((n+1,n+1),dtype=np.int64)
    for j,i in enumerate(p): a[i+1,j+1]=1
    return a.cumsum(0).cumsum(1)

def reject(p,tables):
    n=len(p); q=pcount(p)
    for k in range(1,n):
        for l in range(1,n):
            counts=[int(q[k,l]), k-int(q[k,l]), l-int(q[k,l]),n-k-l+int(q[k,l])]
            dims=[(k,l),(k,n-l),(n-k,l),(n-k,n-l)]
            for name,t,c,(a,b) in zip(['TL','TR','BL','BR'],tables,counts,dims):
                r=int(t[a,b])
                if r>c+2:
                    return dict(k=k,l=l,quadrant=name,modular_rank=r,permutation_ones=c,stage_rank_upper_bound=c+2)
    return None

def bitperm(n,sigma):
    return [sum(((j>>s)&1)<<t for t,s in enumerate(sigma)) for j in range(n)]

def endpoint_orders(n):
    m=n.bit_length()-1
    natural=list(range(n)); reverse=bitperm(n,tuple(reversed(range(m))))
    # Output scatter order of the final radix-4 leaf layer in the verified control.
    radix4=[j+r*(n//4) for j in range(n//4) for r in [0,2,1,3]]
    return {'natural':natural,'bit_reversed':reverse,'radix4_final_scatter':radix4}

def endpoint_obstruction(tables):
    """A witness here excludes ALL internal permutations for fixed endpoints."""
    n=tables[0].shape[0]-1
    for k in range(1,n):
        for l in range(1,n):
            tl=int(tables[0][k,l]);tr=int(tables[1][k,n-l])
            bl=int(tables[2][n-k,l]);br=int(tables[3][n-k,n-l])
            for name,left,right,dimension in [('top',tl,tr,k),('bottom',bl,br,n-k),('left',tl,bl,l),('right',tr,br,n-l)]:
                if left+right>dimension+4:
                    return dict(k=k,l=l,side=name,first_modular_rank=left,second_modular_rank=right,sum_upper_bound=dimension+4)
    return None

def run():
    records=[]
    for n in [16,32,64]:
        m=n.bit_length()-1; rev=bitperm(n,tuple(reversed(range(m))))
        candidates=[('bit_reversal_xor_'+str(a),[x^a for x in rev]) for a in range(n)]
        candidates += [('bit_permutation_'+str(s),bitperm(n,s)) for s in permutations(range(m))]
        orders=endpoint_orders(n)
        for rn,cn in [('natural','natural'),('bit_reversed','bit_reversed'),('radix4_final_scatter','radix4_final_scatter')]:
            a=fourier(n)[np.ix_(orders[rn],orders[cn])]
            tables=rank_tables(a)
            tested=[]
            for name,p in candidates:
                w=reject(p,tables)
                tested.append(dict(name=name,rejected=w is not None,witness=w))
            rec=dict(n=n,row_order_name=rn,column_order_name=cn,row_order=orders[rn],column_order=orders[cn],all_internal_permutations_excluded=endpoint_obstruction(tables),total=len(tested),rejected=sum(x['rejected'] for x in tested),survivors=[x['name'] for x in tested if not x['rejected']],tests=tested)
            records.append(rec)
            print(n,rn,cn,'rejected',rec['rejected'],'/',len(tested),'survivors',rec['survivors'],flush=True)
    Path(__file__).with_name('endpoint_rank_results.json').write_text(json.dumps(records,indent=2)+'\n')

if __name__=='__main__':run()
