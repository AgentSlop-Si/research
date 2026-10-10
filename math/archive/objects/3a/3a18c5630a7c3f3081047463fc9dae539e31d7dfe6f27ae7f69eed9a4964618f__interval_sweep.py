"""Exhaustively test consecutive-input moving-partition obstructions.
No finite field required: consecutive Fourier columns form a Vandermonde family.
"""
import numpy as np
from moving_partition import transformations
from bisection_probe import input_line_permutations

def sweep_intervals(k,perms,ranks=None):
    n=1<<k
    if ranks is None:ranks=[1]*(len(perms)+1)
    seq=[np.asarray(x,dtype=np.int32) for x in input_line_permutations(n,perms)]
    best=[];checked=0;possible=[]
    for a in range(n):
        for b in range(a+1,n+1):
            m=b-a
            rk=min(m,n-m)
            if not rk:continue
            ds=[int(np.count_nonzero(((s[:-1]>=a)&(s[:-1]<b)) != ((s[1:]>=a)&(s[1:]<b)))) for s in seq]
            cap=sum(c*r for c,r in zip(ds,ranks))
            checked+=1
            if rk>cap:
                best.append((rk-cap,rk,cap,a,b,ds))
    best.sort(reverse=True)
    return best,checked

if __name__=='__main__':
 for k in (6,7,8):
    tr=transformations(k)
    progs={
        'all_bitrev':[tr['bitrev']]*3,
        'all_rotl':[tr['rotl']]*3,
        'bitrev_middle_rotate':[tr['bitrev'],tr['bitrev_then_rotl'],tr['bitrev']],
        'bitrev_middle_xor':[tr['bitrev'],tr['bitrev_then_xor'],tr['bitrev']],
        'mix_both':[tr['bitrev_then_rotl'],tr['bitrev_then_xor'],tr['bitrev_then_rotl']],
    }
    for name,ps in progs.items():
        witness,num=sweep_intervals(k,ps)
        print('n',1<<k,name,'intervals',num,'witnesses',len(witness),'strongest',witness[:1],flush=True)
