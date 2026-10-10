"""Independent dense reconstruction check of the new 3-stage rank witness.

This module deliberately DOES NOT use the fast scan executor or three_stage_projected_ranks.
"""
from annihilator_gate import (Stage,rank_mod,mat_mul,transpose,nth_root,
  left_annihilators,right_annihilators,bit_reversal,three_stage_gate,fourier_block)
import json,random

def explicit_perm_matrix(perm):
    n=len(perm)
    return [[int(perm[j]==i) for j in range(n)] for i in range(n)]

def run():
    out=[]
    for n in (16,32,64):
        p=12289;w=nth_root(n,p)
        ids=list(range(n));br=bit_reversal(n)
        cases=[('identity',ids,ids),('mixed',br,ids),('bitrev',br,br)]
        for case,p1,p2 in cases:
            W=6
            gates=three_stage_gate(n,p1,p2,W)
            stages=[Stage.random(n,p,800+z+3*n,0.4) for z in range(3)]
            S1,S2,S3=[s.matrix(p) for s in stages]
            P1=explicit_perm_matrix(p1);P2=explicit_perm_matrix(p2)
            M=mat_mul(S3,mat_mul(P2,mat_mul(S2,mat_mul(P1,S1,p),p),p),p)
            i=gates['I_start'];j=gates['J_start'];I=list(range(i,i+W));J=list(range(j,j+W))
            Y=left_annihilators(stages[2],i,W,p)[:W-2]
            X=right_annihilators(stages[0],j,W,p)[:W-2]
            B=[[M[a][b] for b in J] for a in I]
            A=fourier_block(n,w,I,J,p)
            Fproj=mat_mul(mat_mul(Y,A,p),transpose(X),p)
            Mproj=mat_mul(mat_mul(Y,B,p),transpose(X),p)
            rF=rank_mod(Fproj,p);rM=rank_mod(Mproj,p)
            assert rF>=W-4
            assert rM<=gates['defect']+1
            if gates['excludes_factorization']:assert rF>rM
            out.append({'n':n,'case':case,'rF':rF,'rM':rM,'k':gates['defect']})
    return out

if __name__=='__main__':
    data=run()
    print(json.dumps(data,indent=2))
    print('Independent dense checks passed:',len(data))
