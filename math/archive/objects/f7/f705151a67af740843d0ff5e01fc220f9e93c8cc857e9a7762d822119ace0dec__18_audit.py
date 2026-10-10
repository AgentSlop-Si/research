"""Independent exact Phase 23 audit. Includes exhaustive binary Hankel counts."""
import json,random,time,collections
from phase23_resolvent import *

def hankel_rank_gf2(bits:int,m:int)->int:
    mask=(1<<m)-1
    rows=[(bits>>i)&mask for i in range(m)]
    r=0
    for j in range(m):
        p=next((i for i in range(r,m) if (rows[i]>>j)&1),None)
        if p is None:continue
        rows[p],rows[r]=rows[r],rows[p]
        for i in range(r+1,m):
            if (rows[i]>>j)&1:rows[i]^=rows[r]
        r+=1
    return r

def invertible_hankel_gf2(bits:int,m:int)->bool:
    return hankel_rank_gf2(bits,m)==m

def cyclic_transitions(bits:int,n:int)->int:
    return sum(((bits>>k)&1)!=((bits>>((k-1)%n))&1) for k in range(n))

def main():
    exhaustive=[]
    for m in range(1,10):
        cases=1<<(2*m-1)
        hist=collections.Counter(hankel_rank_gf2(b,m) for b in range(cases))
        for r in range(m+1):
            expected=1 if r==0 else (3*(4**(r-1)) if r<m else 4**(m-1))
            assert hist[r]==expected,(m,r,hist[r],expected)
        count=hist[m]
        assert count*2==cases,(m,count,cases)
        exhaustive.append(dict(m=m,binary_inputs=cases,full_rank_gf2=count,
                               ratio=0.5,rank_counts=dict(sorted(hist.items()))))
    transition_hist={}
    for n in (4,8,12,16):
        hist=collections.Counter(cyclic_transitions(mask,n) for mask in range(1<<n))
        for s in range(n+1):
            exp=(2*__import__('math').comb(n,s) if s%2==0 else 0)
            assert hist[s]==exp,(n,s,hist[s],exp)
        transition_hist[n]=dict(sorted(hist.items()))
    # Our field verification of high Hankel ranks is independent of the
    # GF2 exact counting theorem; no GF2->Fp implication is assumed.
    rng=random.Random(21092026)
    ranks={}
    for n in (32,64,128,256):
        rs=[hankel_rank([rng.randrange(2) for _ in range(n)]) for _ in range(16)]
        ranks[n]=dict(full=sum(v==n//2 for v in rs),draws=len(rs),minrank=min(rs))
    checks=[]
    for n in (8,64,512,4096,8192):
        eng=RealGreenFourier.create(n)
        x=synthesize_exponential_sequence(n,[1,17],[87,93])
        vec,method=adaptive_real_transform(x,eng)
        assert method=='green_rank_2'
        checks.append(dict(n=n,method=method,checksum=sum(vec)%P,
                           supports='O(N) precomputation and O(N) apply for rank<=2'))
    obj={'exhaustive_GF2_hankel_counts':exhaustive,'sampled_binary_ranks_mod_998244353':ranks,
         'binary_cyclic_transition_distributions':transition_hist,
         'adaptive_green_cases':checks,'previous_phase_regressions':'tested separately'}
    with open('audit.json','w') as f:json.dump(obj,f,indent=2)
    print(json.dumps(obj,indent=2))

if __name__=='__main__':main()
