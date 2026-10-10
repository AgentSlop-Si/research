#!/usr/bin/env python3
"""Additional boundary, input-application, and operation-count controls.
Imports only this audit's independently authored implementation.
"""
import json, hashlib, zipfile
import numpy as np
import fresh_block_jet_audit as audit

def scan(g,x,p):
    counts={'multiplications':0,'additions':0}
    def mul(a,b): counts['multiplications']+=1; return int(a)*int(b)%p
    def add(a,b): counts['additions']+=1; return (int(a)+int(b))%p
    n=len(x); left=[0]*n;right=[0]*n
    if n>1:
        left[1]=mul(g[2,0],x[0])
        for i in range(2,n): left[i]=add(left[i-1],mul(g[2,i-1],x[i-1]))
        right[n-2]=mul(g[4,n-1],x[n-1])
        for i in range(n-3,-1,-1): right[i]=add(right[i+1],mul(g[4,i+1],x[i+1]))
    y=[mul(g[0,i],x[i]) for i in range(n)]
    for i in range(1,n): y[i]=add(y[i],mul(g[1,i],left[i]))
    for i in range(n-1): y[i]=add(y[i],mul(g[3,i],right[i]))
    return np.array(y,dtype=np.int64),counts

def main():
    P=[audit.perm(c)[0] for c in audit.read('AFFINE_LAYOUT.json')['affine_shuffle_columns']]
    g=np.array([[r[n] for n in audit.NAMES] for r in audit.read('GENERATOR_POINT_1.json')],dtype=np.int64)
    p=12289; J=audit.differential(g,P,p,list(range(32)),list(range(32)))
    ranks={}
    for m in [16,20,24,28,29]:
        rows=[i*32+j for i in range(m) for j in range(m)]
        ranks[str(m)]=audit.rank(J[rows],p)['rank']
    assert ranks=={'16':256,'20':400,'24':576,'28':784,'29':831}
    costs=[]
    for n in [2,3,8,256]:
        coeff=g[0,:,:n]; x=np.array([(i*i+3*i+9)%p for i in range(n)],dtype=np.int64)
        y,count=scan(coeff,x,p)
        assert np.array_equal(y,audit.mm(audit.stage(coeff,p),x[:,None],p).ravel())
        assert count=={'multiplications':5*n-4,'additions':4*n-6}
        costs.append({'N':n,**count,'dense_comparison_exact':True})
    x=np.array([(i**3+17*i+31)%p for i in range(256)],dtype=np.int64); original=x.copy()
    total={'multiplications':0,'additions':0}
    perm_indices=[np.argmax(a,axis=1) for a in P]
    for k in range(4):
        x,count=scan(g[k],x,p)
        for op in total: total[op]+=count[op]
        if k<3: x=x[perm_indices[k]]
    assert np.array_equal(x,audit.mm(audit.compose(audit.factors(g,P,p),p),original[:,None],p).ravel())
    assert total=={'multiplications':5104,'additions':4072}
    out={'status':'ALL_BOUNDARY_AND_COST_CONTROLS_PASSED','leading_block_pointwise_ranks_mod12289':ranks,'stage_application_controls':costs,'four_stage_N256_arithmetic':total,'four_stage_scalar_arithmetic_total':sum(total.values()),'permutation_gathered_entries':768,'warning':'This checks application of the supplied generic operator, not a Fourier realization or coefficient synthesis.'}
    (audit.ROOT/'BOUNDARY_AND_COST_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out,indent=2))

if __name__=='__main__': main()
