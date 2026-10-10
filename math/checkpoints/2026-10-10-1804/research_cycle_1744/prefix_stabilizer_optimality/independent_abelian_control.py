#!/usr/bin/env python3
"""Fresh standard-library-only controls: direct translations, exact DP and counts."""
import itertools, json, math, time
from functools import lru_cache
from pathlib import Path
OUT = Path(__file__).resolve().parent

def control(factors):
    start=time.monotonic()
    elems=list(itertools.product(*(range(q) for q in factors)))
    n=len(elems); idx={x:i for i,x in enumerate(elems)}
    add=[[idx[tuple((a+b)%q for a,b,q in zip(x,y,factors))] for y in elems] for x in elems]
    def translate(S,g):
        ans=0
        while S:
            b=S&-S; x=b.bit_length()-1; S^=b; ans|=1<<add[g][x]
        return ans
    def stabilizer(S):
        return sum(1<<g for g in range(n) if translate(S,g)==S)
    def closure(S):
        old=-1; S|=1
        while S!=old:
            old=S
            for g in range(n):
                if old>>g&1: S|=translate(old,g)
        return S
    # The independent group DP keeps the identity first, justified by translation.
    size=1<<(n-1); score=[0]*size; count=[0]*size; count[0]=1; last=[0]*size
    for mask in range(1,size):
        S=(mask<<1)|1
        weight=stabilizer(S).bit_count()-1
        best=-1; ways=0; bits=mask
        while bits:
            b=bits&-bits; bits^=b; prev=mask^b
            if score[prev]>best: best=score[prev]; ways=count[prev]; last[mask]=b.bit_length()
            elif score[prev]==best: ways+=count[prev]
        score[mask]=best+weight; count[mask]=ways
    order=[]; mask=size-1
    while mask:
        x=last[mask]; order.append(x); mask^=1<<(x-1)
    order.append(0); order.reverse()
    S=0; generated=1; total=0; stab_sizes=[]
    for j,x in enumerate(order,1):
        S|=1<<x; H=stabilizer(S); total+=H.bit_count()-1; stab_sizes.append(H.bit_count())
        generated=closure(generated|H)
        assert generated & ~S == 0, 'accumulated stabilizer lemma failed'
    assert total==score[-1]
    subgroups={1}; queue=[1]
    while queue:
        H=queue.pop()
        for g in range(n):
            if not(H>>g&1):
                K=closure(H|(1<<g))
                if K not in subgroups: subgroups.add(K); queue.append(K)
    def prime(p): return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
    @lru_cache(None)
    def predicted_count(H):
        h=H.bit_count()
        if h==1: return 1
        return sum(math.factorial(h//K.bit_count())*predicted_count(K)**(h//K.bit_count())
                   for K in subgroups if K!=H and K&~H==0 and h%K.bit_count()==0 and prime(h//K.bit_count()))
    target=0; rem=n
    for p in range(2,n+1):
        while rem%p==0: target+=n-n//p; rem//=p
    assert score[-1]==target
    assert n*count[-1]==predicted_count((1<<n)-1)
    return dict(factors=factors, order=n, maximum=score[-1], predicted_maximum=target,
                maximizing_permutations=n*count[-1], predicted_count=predicted_count((1<<n)-1),
                identity_first_states=size, subgroups=len(subgroups),
                witness=[elems[x] for x in order], stabilizer_sizes=stab_sizes,
                seconds=round(time.monotonic()-start,6))

if __name__=='__main__':
    groups=[(n,) for n in range(2,13)]+[(2,2),(4,2),(2,2,2),(3,3),(6,2),(4,4),(8,2),(4,2,2),(2,2,2,2),(6,3)]
    with (OUT/'independent_abelian_results.jsonl').open('w') as out:
        for factors in groups:
            line=json.dumps(control(factors)); out.write(line+'\n'); out.flush(); print(line,flush=True)
