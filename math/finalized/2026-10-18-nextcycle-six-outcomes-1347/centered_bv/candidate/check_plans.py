"""Allocation-free structural plans and exact affine-family algebra only."""
from pathlib import Path
from math import isqrt
import json

def ceil_sqrt_ratio(a,b):
    r=isqrt(a//b)
    return r+(r*r*b<a)

def main():
    plans=[]
    for m in (11,12,13,16,20,28,64,128,256,512,1024):
        M=1<<m;N=M//4
        for C in (1,2,3,8):
            K=C*(1<<((m+3)//4));S=2*K+1;P=16*m+16;q=N
            Q=P+2*m+q.bit_length()+20
            assert 160*m+4<M and K<M//2 and S<M
            assert (1<<Q)>M and Q>P+2*m+20
            plans.append({'m':m,'variation_factor':C,'cutoff':K,'candidate_count':S,
                          'largest_mathematical_q':q,'working_bits_at_that_q':Q,
                          'full_numerical_execution':False})
    affine=[]
    for m in range(3,15):
        N=1<<(m-2)
        # c_j=N+j, exact sum of squares; no N-entry allocation needed.
        E=N**3+N*N*(N-1)+N*(N-1)*(2*N-1)//6
        B=2*(2*N-1);C=ceil_sqrt_ratio(N*B*B,4*E)
        assert C==2
        affine.append({'m':m,'N':N,'energy':E,'variation_l1':B,'C':C,'q':N,
                       'kind':'exact affine algebra; no provider or outer execution'})
    result={'structural_plans':plans,'affine_family_checks':affine,
        'scope':'Allocation-free guard/formula checks, not large-length numerical execution or arbitrary-original coverage.'}
    Path('STRUCTURAL_PLANS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'structural_plans':len(plans),'exact_affine_checks':len(affine)}))
if __name__=='__main__':main()
