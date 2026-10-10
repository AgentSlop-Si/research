#!/usr/bin/env python3
"""Independently certify structural richness of the exact Phase 8 cycles."""
import json,math,random
from phase8_weyl_cycle import (P,Costs,root_of_unity,roots,cyclic_linear_synthesize,
  synthesize_circulant_order,synthesize_time_weyl,exact_circulant_cycle,
  exact_unknown_shift_cycle,exact_circulant_rational_cycle,exact_weyl_dynamic,
  full_ntt_oracle,direct_dft_oracle,exact_ntt)
from phase6_exact import hankel_rank

def rank(matrix):
    if not matrix:return 0
    m=[list(row) for row in matrix]
    rows=len(m);cols=len(m[0]);r=0
    for col in range(cols):
        i=next((i for i in range(r,rows) if m[i][col]),None)
        if i is None:continue
        m[i],m[r]=m[r],m[i]
        den=pow(m[r][col],P-2,P)
        for j in range(col,cols):m[r][j]=m[r][j]*den%P
        for i in range(r+1,rows):
            d=m[i][col]
            if d:
                for j in range(col,cols):m[i][j]=(m[i][j]-d*m[r][j])%P
        r+=1
        if r==rows:break
    return r

def is_projective_shift(v,w):
    k=len(v)
    for d in range(k):
        ref=next((b for b in range(k) if v[(b+d)%k]),None)
        if ref is None:
            if not any(w):return True
            continue
        a=w[ref];den=v[(ref+d)%k]
        if all(w[b]*den%P==a*v[(b+d)%k]%P for b in range(k)):
            return True
    return False

def orbit_count(columns):
    representatives=[]
    for col in columns:
        if not any(is_projective_shift(col,ref) for ref in representatives):
            representatives.append(col)
    return len(representatives)

def properties(x,m):
    n=len(x);k=n//m
    tab=roots(n,None);wm=tab[k]
    ordinary=[[x[b*m+t] for t in range(m)] for b in range(k)]
    dechirped=[[x[b*m+t]*tab[((t*(t-1)//2)+(m*b)*t)%n]%P for t in range(m)] for b in range(k)]
    active=set()
    for row in dechirped:
        local=exact_ntt(row,wm)
        active.update(j for j,v in enumerate(local) if v)
    cols_dechirped=[[dechirped[b][t] for b in range(k)] for t in range(m)]
    return {'n':n,'k':k,'m':m,'nonzero_input_count':sum(bool(z) for z in x),
            'ordinary_polyphase_rank':rank(ordinary),
            'phase7_dechirped_rank':rank(dechirped),
            'active_green_modes':len(active),
            'phase7_projective_cyclic_shift_orbits':orbit_count(cols_dechirped),
            'hankel_rank':hankel_rank(x)}

def generate():
    k,m=16,8;n=k*m;rng=random.Random(8776)
    # A two-tap hidden-shift operator, not a shifted template.
    seed=[rng.randrange(1,P) for _ in range(k)]
    x=cyclic_linear_synthesize(seed,m,[3,11],(0,5))
    got,cert,c=exact_unknown_shift_cycle(x,m,return_certificate=True)
    res1=properties(x,m)
    res1.update({'family':'unknown circulant two tap order1',
       'inferred_shift':cert['inferred_shift'],'inferred_taps':cert['taps'],
       'output_mismatches':sum(a!=b for a,b in zip(got,full_ntt_oracle(x))),
       'independent_quadratic_dft_mismatches':sum(a!=b for a,b in zip(got,direct_dft_oracle(x))),
       'counted_ops':c.total(),'inversions':c.inversions,
       'input_sha256':__import__('hashlib').sha256(','.join(map(str,x)).encode()).hexdigest()})
    # A richer order-2 recurrence with independent full-rank initial columns.
    initial=[[rng.randrange(1,P) for _ in range(k)] for _ in range(2)]
    x2=synthesize_circulant_order(initial,m,[[13,11],[7,17]],(0,1))
    got2,cert2,c2=exact_circulant_rational_cycle(x2,m,2,return_certificate=True)
    res2=properties(x2,m)
    res2.update({'family':'learned order-2 rational cycle',
         'learned_coefficients':cert2['coefficients_by_lag'],
         'output_mismatches':sum(a!=b for a,b in zip(got2,full_ntt_oracle(x2))),
         'independent_quadratic_dft_mismatches':sum(a!=b for a,b in zip(got2,direct_dft_oracle(x2))),
         'counted_ops':c2.total(),'inversions':c2.inversions,
         'input_sha256':__import__('hashlib').sha256(','.join(map(str,x2)).encode()).hexdigest()})
    # Noncommuting S,D operators, with unknown time-varying controls.
    wk=root_of_unity(k)
    controls=[[rng.randrange(1,P),rng.randrange(1,P)] for _ in range(m-1)]
    x3=synthesize_time_weyl([rng.randrange(1,P) for _ in range(k)],m,[(1,0),(0,1)],controls,wk)
    got3,cert3,c3=exact_weyl_dynamic(x3,m,return_certificate=True)
    res3=properties(x3,m)
    res3.update({'family':'noncommuting time-varying Weyl dynamics',
         'output_mismatches':sum(a!=b for a,b in zip(got3,full_ntt_oracle(x3))),
         'independent_quadratic_dft_mismatches':sum(a!=b for a,b in zip(got3,direct_dft_oracle(x3))),
         'counted_ops':c3.total(),'inversions':c3.inversions,
         'input_sha256':__import__('hashlib').sha256(','.join(map(str,x3)).encode()).hexdigest()})
    all_results=[res1,res2,res3]
    for result in all_results:
        assert result['nonzero_input_count']==n,result
        assert result['ordinary_polyphase_rank']==m,result
        assert result['phase7_dechirped_rank']==m,result
        assert result['active_green_modes']==m,result
        assert result['hankel_rank']==n//2,result
        assert result['output_mismatches']==0,result
        assert result['independent_quadratic_dft_mismatches']==0,result
    with open('EXPLICIT_CERTIFICATES.json','w') as f:json.dump(all_results,f,indent=2)
    print(json.dumps(all_results,indent=2))
if __name__=='__main__':generate()
