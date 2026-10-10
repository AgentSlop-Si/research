#!/usr/bin/env python3
"""Independent exact witness, barrier, and operation-count audit for Phase 10."""
import hashlib
import json
import math
import random
import time
from phase10_rational import P,Count,ntt,root_table,make_spectral_recurrent_example,phase10_transform
from test_phase10 import rank_mod


def matrix_audit(n=128,m=8,d=2,seed=204):
    k=n//m
    x,q,f=make_spectral_recurrent_example(k,m,d,seed,force_roots=True)
    y,cert,ctr=phase10_transform(x,m,d,rng=random.Random(101),return_certificate=True)
    assert cert['accepted']
    # Independent O(N^2) evaluation instead of same NTT implementation.
    tab=root_table(n)
    independent=[sum(x[t]*tab[(-j*t)%n] for t in range(n))%P for j in range(n)]
    assert y==independent
    C=[[x[b*m+t] for t in range(m)] for b in range(k)]
    full_rank=rank_mod(C)
    hankel_size=n//2
    hankel_rank=rank_mod([[x[i+j] for j in range(hankel_size)]
                            for i in range(hankel_size)])
    nonzero_x=sum(z!=0 for z in x)
    # Verify the stronger Phase 9-negative-control property. Fit a separate
    # stationary dense circulant C1 from first transition and then inspect
    # each residual e_(t)=v_(t+1)-C1*v_t.
    assert all(f[0][ell] for ell in range(k))
    lam=[f[1][ell]*pow(f[0][ell],P-2,P)%P for ell in range(k)]
    residual_spectra=[]
    per_transition_support=[]
    for t in range(1,m-1):
        E=[(f[t+1][ell]-lam[ell]*f[t][ell])%P for ell in range(k)]
        e=ntt(E,False)
        per_transition_support.append({'t':t,
            'spectral':sum(z!=0 for z in E),
            'spatial':sum(z!=0 for z in e)})
        residual_spectra.append(E)
    innovation_column_rank=rank_mod([
        [residual_spectra[t][ell] for t in range(m-2)]
        for ell in range(k)])
    # Check every local Green phase active after Phase 7 dechirp.
    amodes=[]
    for b in range(k):
        row=[]
        for t in range(m):
            phase=(t*(t-1)//2 +m*b*t)%n
            row.append(x[b*m+t]*tab[phase]%P)
        amodes.append(ntt(row,True))
    occupied=sum(any(amodes[b][i] for b in range(k)) for i in range(m))
    return {'n':n,'k':k,'m':m,'d':d,'seed':seed,'field':P,
        'input_sha256':hashlib.sha256(','.join(map(str,x)).encode()).hexdigest(),
        'output_sha256':hashlib.sha256(','.join(map(str,y)).encode()).hexdigest(),
        'input_nonzeros':nonzero_x,'polyphase_rank':full_rank,
        'maximum_polyphase_rank':m,
        'hankel_rank':hankel_rank,'maximum_hankel_rank':hankel_size,
        'occupied_green_phase_modes':occupied,
        'phase9_one_step_innovation_rank':innovation_column_rank,
        'maximum_phase9_innovation_rank':m-2,
        'phase9_one_step_innovation_support':per_transition_support,
        'exact_full_dft_mismatches':sum(a!=b for a,b in zip(y,independent)),
        'singular_denominators_handled':cert['singular_outputs'],
        'counted_field_ops_per_input':ctr.total()/n}


def asymptotic_scaling():
    records=[]
    for n in (256,512,1024,2048,4096,8192,16384,32768,65536,131072):
        m=1<<(int(math.log2(n)).bit_length()-1) # overwritten below: floor power2 of log2(n)
        lg=n.bit_length()-1
        m=1<<(lg.bit_length()-1)
        k=n//m
        d=2
        assert m>=2*d
        x,_,_=make_spectral_recurrent_example(k,m,d,919+n)
        c=Count()
        ts=time.perf_counter()
        y,cert,c=phase10_transform(x,m,d,rounds=3,
                        rng=random.Random(505+n),counter=c,return_certificate=True)
        elapsed=time.perf_counter()-ts
        assert cert['accepted']
        baseline_counter=Count()
        reference=ntt(x,True,baseline_counter)
        assert y==reference
        records.append({'n':n,'k':k,'m':m,'d':d,'ops':c.total(),
            'counted_field_ops_per_input':round(c.total()/n,4),
            'baseline_ntt_ops_per_input':round(baseline_counter.total()/n,4),
            'ops_ratio_vs_ntt':round(c.total()/baseline_counter.total(),4),
            'learned_max_order':cert['max_order'],
            'singular_outputs':cert['singular_outputs'],
            'prototype_seconds':round(elapsed,4)})
    return records


def probabilistic_model():
    # q^-K(M-2d) holds CONDITIONALLY on any prefix for which a deterministic
    # learned recurrence specifies the rest; this is an exact counting result.
    m=8;d=2;k=16
    exponent=k*(m-2*d)
    return {'n':m*k,'k':k,'m':m,'d':d,
        'remaining_unrestricted_field_coordinates':exponent,
        'accept_probability_conditional_on_prefix':f'{P}^(-{exponent})',
        'log10_probability':round(-exponent*math.log10(P),3),
        'note':'For any fixed first 2d columns, a chosen deterministic continuation specifies exactly one suffix. If no order-d model fits the prefix, probability is zero.'}


def main():
    witness=matrix_audit()
    assert witness['input_nonzeros']==witness['n']
    assert witness['polyphase_rank']==witness['m']
    assert witness['hankel_rank']==witness['maximum_hankel_rank']
    assert witness['occupied_green_phase_modes']==witness['m']
    assert witness['phase9_one_step_innovation_rank']==witness['m']-2
    assert all(e['spectral']==witness['k'] and e['spatial']==witness['k']
               for e in witness['phase9_one_step_innovation_support'])
    assert witness['exact_full_dft_mismatches']==0
    scaling=asymptotic_scaling()
    out={'status':'conditional exact algorithm; no general worst-case speedup',
         'witness':witness,'scaling':scaling,
         'prefix_rarity_obstruction':probabilistic_model(),
         'finite_field_warning':'Fixed GF(2013265921) only supports power-of-two lengths <=2^27; unbounded asymptotics require an appropriate exact arithmetic field/root model.',
         'membership_warning':'Randomized one-sided error certification, not deterministic for arbitrary inputs. Rejected inputs need conventional FFT fallback.'}
    with open('AUDIT_RESULTS.json','w') as f:json.dump(out,f,indent=2)
    print('HERO #0 PHASE 10: EXACT ALGEBRA AUDIT PASSED')
    print('N128 witness:',json.dumps({k:v for k,v in witness.items() if k in
          ('input_nonzeros','polyphase_rank','hankel_rank','occupied_green_phase_modes',
          'phase9_one_step_innovation_rank','exact_full_dft_mismatches',
          'singular_denominators_handled')},sort_keys=True))
    print('Random-input accepted-family probability exponent:',
          probabilistic_model()['log10_probability'])
    for v in scaling:
        print('N=%-6d M=%-2d d=%d counted_ops/N=%7.2f baseline=%7.2f ratio=%4.2f wall=%.3fs' %
              (v['n'],v['m'],v['d'],v['counted_field_ops_per_input'],
               v['baseline_ntt_ops_per_input'],v['ops_ratio_vs_ntt'],v['prototype_seconds']))


if __name__=='__main__':main()
