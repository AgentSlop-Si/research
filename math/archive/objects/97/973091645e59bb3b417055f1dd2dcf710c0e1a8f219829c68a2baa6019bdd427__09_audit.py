"""Reproduce summary data. Dense exact inspections are research audits only."""
from __future__ import annotations
import json,random
from phase22_gram import *


def main():
    details=[]; control=[]
    for n in (8,16,32,64):
        for seed in (11,17,23,29,43,2026):
            A=dense_from_apply(seeded_green_sum(n,seed,2),n)
            B=dense_from_apply(seeded_green_sum(n,seed+701,2),n)
            K,C=quadratic_form_data(A,B)
            st,_=permutation_fingerprint_gate(K,C)
            zk=sum(K[i][i]==0 for i in range(n))
            zc=sum(C[i][i]==0 for i in range(n))
            details.append(dict(n=n,seed=seed,result=st,zero_diags_K=zk,zero_diags_C=zc))
        for seed in (17,29,2026):
            rng=random.Random(seed)
            A=dense_from_apply(seeded_green_sum(n,seed,2),n)
            perm=list(range(n));rng.shuffle(perm)
            q=[rng.randrange(1,MOD) for _ in range(n)]
            F=fft_matrix(n)
            B=make_positive_control(A,perm,q,F)
            K,C=quadratic_form_data(A,B)
            status,p=permutation_fingerprint_gate(K,C)
            qr=recover_mask(K,C,p) if p else None
            ok=(status=='candidate' and p==perm and (qr==q or qr==[(-x)%MOD for x in q]))
            control.append(dict(n=n,seed=seed,result='recovered' if ok else 'failed'))
    report={
        'test_family':'independently permuted, two-term weighted cyclic Green sums over F_998244353',
        'negative_fixed_pairs':details,
        'positive_controls':control,
        'negative_excluded':sum(d['result']=='excluded' for d in details),
        'positive_recovered':sum(d['result']=='recovered' for d in control),
        'complexity_note':'O(qN) application of each Green sum; diagnostic dense matrices cost O(N^2) oracle operations and cubic matrix inversion. Not a fast FFT.',
        'status_note':'Negative samples do not imply a theorem for all tunable Green stages.'
    }
    with open('audit.json','w') as f:json.dump(report,f,indent=2)
    print('EXACT SAMPLE VETO',report['negative_excluded'],'/',len(details))
    print('EXACT POSITIVE RECOVERY',report['positive_recovered'],'/',len(control))
    print('SIZES',sorted(set(d['n'] for d in details)))
    print('DIAGONAL-ZERO OBSTRUCTIONS',sum(d['zero_diags_K']!=d['zero_diags_C'] for d in details))

if __name__=='__main__':main()
