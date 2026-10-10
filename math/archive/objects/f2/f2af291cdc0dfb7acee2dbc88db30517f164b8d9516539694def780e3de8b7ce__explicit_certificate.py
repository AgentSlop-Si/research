#!/usr/bin/env python3
"""Deterministic full-Hankel, full-block-rank, all-mode-active witness.

N=128, K=16, M=8, p=2013265921, a=1, beta=0, hidden shifts g_t=t,
f=(2,1,...,1), h_t=t+1. Every x entry is nonzero. No random numbers.
"""
import json
from pathlib import Path
from phase6_exact import P,root_of_unity,hankel_rank,independent_full_dft
from phase7_rank_fusion import root_table,count_phase_modes
from phase7_hidden_shift_detector import unknown_shift_rank1_transform
from test_phase7 import reconstruct_v,field_rank

def main():
    n=128;k=16;m=8
    f=[2]+[1]*(k-1);g=list(range(m));h=list(range(1,m+1))
    tab=root_table(n,root_of_unity(n),None)
    x=[]
    for b in range(k):
        for t in range(m):
            power=(t*(t-1)//2 +m*b*t)%n
            x.append(f[(b+g[t])%k]*h[t]*tab[(-power)%n]%P)
    value,c=unknown_shift_rank1_transform(x,m)
    report={
        'n':n,'k':k,'m':m,'prime':P,'chirp_slope_a':1,'shift_beta':0,
        'reference_f':f,'column_weights_h':h,'hidden_column_shifts_g':g,
        'number_nonzero_x':sum(bool(z) for z in x),
        'ordinary_dechirped_block_rank':field_rank(reconstruct_v(x,m,1,0)),
        'global_green_modes_active':count_phase_modes(x,m),
        'global_hankel_rank':hankel_rank(x),'max_possible_hankel_rank':n//2,
        'exact_equal_to_independent_NTT':value==independent_full_dft(x),
        'total_field_inversions_detector':c.inversions,
        'charged_ops':c.basic_field_ops(),
    }
    assert report['number_nonzero_x']==n
    assert report['ordinary_dechirped_block_rank']==m
    assert report['global_green_modes_active']==m
    assert report['global_hankel_rank']==n//2
    assert report['exact_equal_to_independent_NTT']
    assert report['total_field_inversions_detector']==1
    Path(__file__).with_name('EXPLICIT_CERTIFICATE.json').write_text(json.dumps(report,indent=2))
    print('EXACT CERTIFIED WITNESS',json.dumps(report,indent=2))

if __name__=='__main__':main()
