"""Build certificates with independent modular determinant, boundary and mincut calculations.
The modular determinant is an algebraic nonvanishing certificate over C, because
w is a specialized primitive cyclotomic root in F_p with p=1 mod N.
"""
from pathlib import Path
import hashlib, json
import numpy as np
from moving_partition import *
from mixing_survivor import make

HERE=Path(__file__).resolve().parent

def independent_det_mod(M,p):
    a=np.array(M,dtype=np.int64,copy=True)
    nr,nc=a.shape
    assert nr==nc
    det=1
    for c in range(nc):
        cand=np.flatnonzero(a[c:,c])
        if cand.size==0:return 0
        v=c+int(cand[0])
        if v!=c:a[[v,c]]=a[[c,v]];det=(-det)%p
        elt=int(a[c,c]);det=det*elt%p
        inv=pow(elt,-1,p)
        if c+1<nc:
            coefs=a[c+1:,c]*inv%p
            a[c+1:,c+1:]=(a[c+1:,c+1:]-coefs[:,None]*a[c,c+1:])%p
            a[c+1:,c]=0
    return det%p

def modular_certificate(n, input_coords,output_coords,prime):
    root=primitive_root_of_unity(n,prime)
    pw=np.array([pow(root,k,prime) for k in range(n)],dtype=np.int64)
    a=np.array(input_coords,dtype=np.int64)
    b=np.array(output_coords,dtype=np.int64)
    assert len(a)==len(b)
    det=independent_det_mod(pw[(b[:,None]*a[None,:])%n],prime)
    assert det!=0,(n,prime)
    return {'prime':prime,'primitive_root':root,'determinant':det}

def cert(k,name,perms,ranks=[1,1,1,1]):
    n=1<<k
    found,checked=search_parity(k,perms,ranks,12289)
    assert found
    best=found[0]
    A=parity_set(n,best['mask'])
    B=parity_set(n,best['path'][-1],1)
    cost,sets,costs=moving_partition_budget(n,A,perms,ranks)
    assert cost==best['budget']
    modular=[modular_certificate(n,A,B,p) for p in (12289,65537)]
    return {'n':n,'name':name,'permutations':perms, 'orders':ranks,
      'initial_parity_mask':best['mask'], 'mask_path':best['path'],
      'boundary_costs':costs,'bound':cost,'fourier_rank':n//2,
      'gap':n//2-cost,'modular':modular}

def build():
    cases=[]
    for k in (6,7,8):
        t=transformations(k)
        progs={'rotations':[t['rotl']]*3,
               'twisted_bitrev':[t['bitrev_then_rotl']]*3,
               'middle_xor':[t['bitrev'],t['bitrev_then_xor'],t['bitrev']],
               'middle_rotate':[t['bitrev'],t['bitrev_then_rotl'],t['bitrev']],
               'mixed_twists':[t['bitrev_then_rotl'],t['bitrev_then_xor'],t['bitrev_then_rotl']]}
        for name,p in progs.items():
            found,num=search_parity(k,p,[1]*4)
            if found:
                c=cert(k,name,p)
                cases.append(c)
                print('N',c['n'],name,'mask',c['initial_parity_mask'],'rank',c['fourier_rank'],'cap',c['bound'],
                   'modular determinants',[(x['prime'],x['determinant']) for x in c['modular']],flush=True)
    out={'statement':'Selected exact characteristic-zero no-go certificates for 4-stage order-one QS networks',
         'proof_principle':'Each nonzero modular determinant certifies nonzero complex determinant; capacity bounds follow from moving-partition QS rank inequality.',
         'cases':cases}
    (HERE/'EXACT_CERTIFICATES.json').write_text(json.dumps(out,indent=2)+'\n')
    return out

if __name__=='__main__':build()
