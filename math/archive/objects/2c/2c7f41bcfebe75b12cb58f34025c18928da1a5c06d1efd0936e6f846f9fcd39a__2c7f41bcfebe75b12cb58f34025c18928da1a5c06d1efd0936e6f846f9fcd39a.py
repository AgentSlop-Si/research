#!/usr/bin/env python3
"""Independent Phase9 cost/rank/success audits. Reproducible fixed seeds."""
from __future__ import annotations
from math import comb,log10,log2,floor
import hashlib,json,random,time
from phase9_dense_cycle import (P,Costs,make_dense_cycle,exact_dense_cycle_with_innovations,
                                exact_reference_dft,root_of_unity)
from test_phase9 import matrix_rank_mod


def log10_probability_sparse(k,m,s):
    # Exact probability, conditional on DFT(v0) all nonzero, for uniform input:
    # after v0/v1 determine C, each next v[t+1] is uniform; residual uniform.
    logs=[log10(comb(k,i))+i*log10(P-1)-k*log10(P) for i in range(min(s,k)+1)]
    highest=max(logs)
    return (m-2)*(highest+log10(sum(10**(u-highest) for u in logs)))


def witness():
    k,m=16,8;n=k*m
    rng=random.Random(7427)
    innovations={t:[((3*t+2)%k,rng.randrange(1,P))] for t in range(1,m-1)}
    x,meta=make_dense_cycle(k,m,innovations,seed=721)
    answer,cert,c=exact_dense_cycle_with_innovations(
        x,m,1,3,3,Costs(),random.Random(727),True)
    assert answer==exact_reference_dft(x)
    poly=[[x[b*m+t] for t in range(m)] for b in range(k)]
    w=root_of_unity(n)
    tab=[pow(w,i,P) for i in range(n)]
    dechirped=[[x[b*m+t]*tab[(t*(t-1)//2+m*b*t)%n]%P
                 for t in range(m)] for b in range(k)]
    mode_occupied=[]
    for r in range(m):
        exists=False
        for b in range(k):
            value=sum(dechirped[b][t]*tab[(k*r*t)%n] for t in range(m))%P
            if value:exists=True;break
        mode_occupied.append(exists)
    # H_64 = [x[i+j]], indices 0..126
    half=n//2
    hankel=[[x[i+j] for j in range(half)] for i in range(half)]
    evidence={
        'n':n,'k':k,'m':m,'field_prime':P,'seed':721,
        'innovation_seed':7427,'all_input_nonzero':all(x),
        'kernel_support':sum(v!=0 for v in meta['kernel_c']),
        'distinct_eigenvalues':len(set(meta['lambda'])),
        'polyphase_column_rank':matrix_rank_mod(poly),
        'dechirped_column_rank':matrix_rank_mod(dechirped),
        'hankel_rank':matrix_rank_mod(hankel),
        'green_phase_modes_present':sum(mode_occupied),
        'exact_output_mismatches':sum(a!=b for a,b in zip(answer,exact_reference_dft(x))),
        'detected_innovations':cert['detected_innovations'],
        'operations':c.total(),
        'input_sha256':hashlib.sha256(','.join(map(str,x)).encode()).hexdigest(),
        'output_sha256':hashlib.sha256(','.join(map(str,answer)).encode()).hexdigest()
    }
    assert evidence['polyphase_column_rank']==m
    assert evidence['dechirped_column_rank']==m
    assert evidence['hankel_rank']==half
    assert evidence['green_phase_modes_present']==m
    assert evidence['kernel_support']==k
    assert evidence['all_input_nonzero']
    return evidence


def scaling():
    records=[]
    for exponent in (8,9,10,11,12,13,14,15,16):
        n=1<<exponent
        m=1<<int(floor(log2(exponent)))
        k=n//m
        if k<m:continue
        for per_step in (0,1,3):
            rng=random.Random(57+n+per_step)
            events={t:[(b,rng.randrange(1,P)) for b in rng.sample(range(k),per_step)]
                    for t in range(1,m-1)} if per_step else {}
            x,_=make_dense_cycle(k,m,events,seed=72+per_step)
            start=time.perf_counter()
            y,cert,c=exact_dense_cycle_with_innovations(
                x,m,per_step,3,3,Costs(),random.Random(27+per_step),True)
            elapsed=time.perf_counter()-start
            assert y is not None,(n,m,cert)
            assert y==exact_reference_dft(x)
            records.append({'n':n,'k':k,'m':m,'errors_per_transition':per_step,
                            'total_errors':cert['innovation_total'],
                            'mode':cert['mode'],'counted_ops':c.total(),
                            'ops_per_n':round(c.total()/n,3),
                            'seconds_python':round(elapsed,4),
                            'inversions':c.inversions,'ntt_butterflies':c.ntt_butterflies})
    return records


def main():
    report={
        'model':'GF(2013265921), exact field ops, root supplied; Python time for reproducibility only',
        'witness':witness(),
        'scaling':scaling(),
        'generic_input_log10_probability':[
            {'n':k*m,'k':k,'m':m,'max_spikes_per_transition':s,
             'log10_probability_conditional_on_f0_nonzero':log10_probability_sparse(k,m,s)}
            for k,m,s in [(16,8,0),(16,8,1),(16,8,2),(32,8,2),
                          (128,16,2),(512,16,3)]],
        'one_sided_error':'false accept <= q^(-R*rank(residual matrix)) if R independent uniform vectors',
        'important':'This is an exact *promised family* and randomized membership test, not an all-input FFT upper bound.'
    }
    open('AUDIT_RESULTS.json','w').write(json.dumps(report,indent=2))
    print('WITNESS',json.dumps(report['witness'],indent=2))
    print('SCALING')
    for row in report['scaling']:
        print('N=',row['n'],'M=',row['m'],'s=',row['errors_per_transition'],
              'ops/N=',row['ops_per_n'],'mode=',row['mode'])
    print('BARRIER',json.dumps(report['generic_input_log10_probability'],indent=2))
    print('PASS: all generated exact output vectors match independent length-N NTT')


if __name__=='__main__':main()
