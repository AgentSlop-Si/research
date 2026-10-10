#!/usr/bin/env python3
"""Independent bounded search replay; reads original search as specification only.
No original module is imported or executed. Exact inverses are derived analytically.
Uses basis 1, (z+z^-1), ..., (z^4+z^-4) rather than cosine basis.
"""
from pathlib import Path
from itertools import product
from collections import Counter
import hashlib,json,time
import numpy as np

HERE=Path(__file__).resolve().parent
n=6

def main():
    start=time.perf_counter(); I=np.eye(n,dtype=np.int64)
    # E0 extracts x0 and the five independent even-paired sums.
    E0=np.zeros((6,11),dtype=np.int64); E0[0,0]=1
    for j in range(1,6): E0[j,j]=E0[j,11-j]=1
    # Numerator of 2 times the even compressed Fourier matrix in an exact
    # real-cyclotomic basis. 1+S1+...+S5=0, S_j=z^j+z^-j.
    tensor=np.zeros((5,6,6),dtype=np.int64)
    for row,col in product(range(6),repeat=2):
        e=(row*col)%11; k=min(e,11-e)
        if not k: tensor[0,row,col]=2
        elif k<5: tensor[k,row,col]=1
        else: tensor[:,row,col]=-1
    # Verify basis embedding against 2*cos(2*pi*row*col/11), exactly.
    basis=np.zeros((5,11),dtype=np.int64); basis[0,0]=1
    for j in range(1,5): basis[j,j]=basis[j,11-j]=1
    for row,col in product(range(6),repeat=2):
        poly=tensor[:,row,col]@basis
        poly[(row*col)%11]-=1; poly[(-row*col)%11]-=1
        assert np.all(poly==poly[-1])  # multiple of Phi_11
    # R=(I-v e_anchor^T)(2I+a u e0^T), with u0=v0=v_anchor=0.
    # Hence 4R^-1=(2I-a u e0^T)(I+v e_anchor^T), without floating point.
    candidates={}
    for alpha in (0,2,-2,4,-4,1,-1):
        for flags in product((0,1),repeat=5):
            u=np.array((0,*flags),dtype=np.int64)
            star=2*I.copy(); star[:,0]+=alpha*u
            inverse_star=2*I.copy(); inverse_star[:,0]-=alpha*u
            for anchor in range(6):
                mask_options=[(0,0,0,0,0)] if anchor==0 else product((0,1),repeat=5)
                for mask in mask_options:
                    v=np.array((0,*mask),dtype=np.int64); v[anchor]=0
                    D=I.copy(); D[:,anchor]-=v
                    Di=I.copy(); Di[:,anchor]+=v
                    R=D@star; Q=inverse_star@Di
                    assert np.array_equal(R@Q,4*I) and np.array_equal(Q@R,4*I)
                    key=tuple(map(int,R.flat))
                    if key in candidates: assert np.array_equal(candidates[key][1],Q)
                    candidates[key]=(R,Q)
    keys=sorted(candidates)
    R=np.stack([candidates[k][0] for k in keys]); Q=np.stack([candidates[k][1] for k in keys])
    cost=np.count_nonzero(R@E0,axis=(1,2))
    # Left outer layer is transpose of the same six-by-eleven product.
    assert np.array_equal(cost,np.count_nonzero(np.transpose(R@E0,(0,2,1)),axis=(1,2)))
    maxq=int(abs(Q).max()); maxt=int(abs(tensor).max())
    intermediate_bound=6*maxt*maxq; final_bound=6*6*maxt*maxq**2
    assert final_bound < 2**63
    right=tensor[None,:,:,:]@Q[:,None,:,:]
    one_side=cost+11+np.count_nonzero(np.any(right!=0,axis=1),axis=(1,2))
    selected=np.flatnonzero(one_side<=61)
    histogram={str(int(k)):int(v) for k,v in sorted(Counter(one_side).items())}
    best=10**9; minimizers=0; selected_pairs=0; witness=None; max_seen=0
    for i in selected:
        # Genuine exact integer coefficient matrices, for every selected right.
        both=Q[i].T[None,None,:,:]@right[selected]
        max_seen=max(max_seen,int(abs(both).max()))
        scores=cost[i]+cost[selected]+np.count_nonzero(np.any(both!=0,axis=1),axis=(1,2))
        local=int(scores.min()); selected_pairs+=len(selected)
        if local<best:
            best=local; minimizers=int(np.count_nonzero(scores==best))
            j=int(selected[np.argmin(scores)]); witness={'left_scaled_basis':R[i].tolist(),'right_scaled_basis':R[j].tolist()}
        elif local==best: minimizers+=int(np.count_nonzero(scores==best))
    claimed=json.loads((HERE/'input_snapshot/F11_BOUNDED_RATIONAL_SEARCH.json').read_text())
    assert len(R)==claimed['raw_candidate_count']==14212
    assert len(selected)==claimed['selected_candidate_count']==982
    assert best==claimed['best_even_sector_edges']==58
    assert maxq==claimed['max_scaled_inverse_integer']==4
    assert final_bound==claimed['arithmetic_absolute_bound']==1152
    result={'verdict':'PASS_BOUNDED_NEGATIVE_ONLY','author_program_executed_or_imported':False,
        'raw_unique_candidates':len(R),'exact_inverse_checks':2*len(R),'selected_candidates':len(selected),
        'ordered_pairs_checked':selected_pairs,'best_one_sided_even_score':int(one_side.min()),
        'one_sided_histogram':histogram,'best_two_sided_even_score':best,'minimum_pair_count':minimizers,
        'odd_sector_edges_unchanged':45,'best_total_edges':best+45,'witness':witness,
        'integer_tensor_coefficient_bound':final_bound,'largest_integer_seen':max_seen,'max_inverse_coefficient':maxq,
        'basis':'1,S1,S2,S3,S4 with Sj=zeta_11^j+zeta_11^-j; S5=-1-S1-S2-S3-S4',
        'inverses':'Analytic nilpotent-factor inverses, checked exactly on both sides; no floating-point inversion.',
        'scope':'The 14212 specified unique rational star-and-difference bases, with ordered two-sided pairs restricted to the 982 bases scoring at most 61 individually. No conclusion about discarded two-sided combinations, arbitrary rational/complex bases, or general topologies.',
        'runtime_seconds':round(time.perf_counter()-start,3),
        'reviewer_source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE/'INDEPENDENT_BOUNDED_SEARCH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
