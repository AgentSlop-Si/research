"""Finite-field probes of the prime-length, both-endpoint permutation corollary.

Chebotarev's all-minors theorem is over characteristic zero. Modular tests can
corroborate selected minors but CANNOT prove the characteristic-zero theorem.
"""
from __future__ import annotations
import json
from itertools import combinations
from pathlib import Path
from random import Random
from cut_budget import fourier, rank, permute, endpoint_certificate


def is_prime(n):
    if n<2:return False
    if n%2==0:return n==2
    a=3
    while a*a<=n:
        if n%a==0:return False
        a+=2
    return True


def field(n,seed=1):
    # Small/medium suitable primes with p == 1 (mod n). Primality checked.
    k=(1000000+seed)//n
    while True:
        p=k*n+1
        if is_prime(p):
            for a in range(2,100):
                z=pow(a,k,p)
                if z!=1 and pow(z,n,p)==1:
                    # n is prime: nonunity nth root has order exactly n
                    return p,a
        k+=1


def run():
    rng=Random(20261009)
    out=[]
    for n in (5,7,11,13,17,31):
        m=n//2
        for seed in (1,41):
            p,g=field(n,seed)
            f=fourier(n,p,g)
            # Exhaustively test every m-by-m minor at small prime lengths.
            if n<=7:
                subsets=list(combinations(range(n),m))
                pairs=[(r,c) for r in subsets for c in subsets]
            else:
                pairs=[]
                for _ in range(60):
                    pairs.append((sorted(rng.sample(range(n),m)),sorted(rng.sample(range(n),m))))
            for rr,cc in pairs:
                r=rank([[f[i][j] for j in cc] for i in rr],p)
                assert r==m,(n,p,rr,cc,r)
            # Even if both endpoints are shuffled, prime Fourier half-blocks
            # have full row rank by Chebotarev (proven over C, sampled here).
            for _ in range(8):
                ro=list(range(n));co=list(range(n))
                rng.shuffle(ro);rng.shuffle(co)
                w=permute(f,ro,co)
                assert rank([row[:m] for row in w[:m]],p)==m
                assert rank([row[m:] for row in w[:m]],p)==m
            # The standard general-cut transfer lemma works for odd N as well.
            cert=endpoint_certificate(permute(f,ro,co),p) if n<=17 else None
            if cert is not None:assert cert['necessary_rank_sum']>= (m+1)//2
            out.append({'length':n,'modulus':p,'primitive_generator':g,'minor_size':m,
                        'checked_square_minors':len(pairs),'both_endpoint_orders':8,
                        'channel_rank_sum_lower_bound':(m+1)//2,
                        'per_stage_equal_rank_bound':(m+3)//4})
    Path(__file__).with_name('prime_endpoint_results.json').write_text(json.dumps(out,indent=2)+'\n')
    print('PASS: prime Fourier minor samples:',sum(e['checked_square_minors'] for e in out))
    print('PASS: both-endpoint permutations:',sum(e['both_endpoint_orders'] for e in out))
    for x in out:
        if x['modulus']==field(x['length'],1)[0]:
            print('prime N=',x['length'],'rank sum >=',x['channel_rank_sum_lower_bound'])
    return out

if __name__=='__main__':run()
