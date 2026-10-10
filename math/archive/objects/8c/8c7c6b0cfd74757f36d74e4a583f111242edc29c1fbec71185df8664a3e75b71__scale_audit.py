#!/usr/bin/env python3
"""Fresh-input operation counts and full-size NTT baseline on equal output scope."""
import json, math, time
from pathlib import Path
from phase6_exact import OpCounter,ntt,root_of_unity,P
from phase7_rank_fusion import sample_dechirped_rank,Counter,exact_green_rank_fused
from phase7_hidden_shift_detector import unknown_shift_rank1_transform

def main():
    report=[]
    for logq in range(8,17):
        q=1<<logq
        m=1<<(int(math.log2(logq))) # within factor 2 of log2 q
        k=q//m
        g=[(7*t*t+5*t)%k for t in range(m)]
        x,_,_=sample_dechirped_rank(k,m,1,seed=q+29,a=3,beta=5,shifts=g)
        c=Counter()
        t0=time.perf_counter()
        got,c=unknown_shift_rank1_transform(x,m,3,5,counter=c)
        t1=time.perf_counter()
        assert got is not None
        ffc=OpCounter()
        w=root_of_unity(q)
        baseline=ntt(x,pow(w,P-2,P),ffc)
        t2=time.perf_counter()
        assert got==baseline
        row={'n':q,'k':k,'m':m,'tested_rank':1,'phase_modes_nonzero':m,
             'new_ops':c.basic_field_ops(),'ops_per_n':c.basic_field_ops()/q,
             'baseline_ntt_ops':ffc.add+ffc.mult,
             'baseline_ops_per_n':(ffc.add+ffc.mult)/q,
             'new_to_baseline_op_ratio':c.basic_field_ops()/(ffc.add+ffc.mult),
             'new_seconds':t1-t0,'ntt_seconds':t2-t1,'inversions':c.inversions,
             'certified_equal_to_ntt':True}
        report.append(row)
        print('N',q,'M',m,'new_op/N',round(row['ops_per_n'],2),
              'full_NTT_op/N',round(row['baseline_ops_per_n'],2),
              'ratio',round(row['new_to_baseline_op_ratio'],2))
    Path(__file__).with_name('scale_audit.json').write_text(json.dumps({'rows':report},indent=2))
if __name__=='__main__':main()
