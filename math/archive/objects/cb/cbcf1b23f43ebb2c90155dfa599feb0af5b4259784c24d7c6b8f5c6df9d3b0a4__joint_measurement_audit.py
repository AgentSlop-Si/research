"""Measured joint-orbit geometries on an exhaustively listed finite family.

This uses numerical KD-trees to produce explicit high-precision verified
pairs, NOT to certify a universally optimal minimal gap.
"""
import json
from pathlib import Path
import numpy as np
from scipy.spatial import cKDTree
import mpmath as mp
from orbit_stability import complementary_signal, folded_odd_coefficients


def measured_pair(n:int,r:int)->dict:
    m=n//2
    features=np.zeros((1,r),dtype=np.complex128)
    odd_k=tuple(range(1,2*r,2))
    for j in range(m):
        p=np.exp(2j*np.pi*np.asarray(odd_k)*j/n)
        features=np.concatenate((features-p,features+p),axis=0)
    xy=np.concatenate((features.real,features.imag),axis=1)
    tree=cKDTree(xy)
    distances,indices=tree.query(xy,k=2,workers=1)
    idx=int(np.argmin(distances[:,1]))
    other=int(indices[idx,1])
    coeff=tuple(a-b for a,b in zip(folded_odd_coefficients(idx,n),folded_odd_coefficients(other,n)))
    mp.mp.dps=80
    selected_diffs=[]
    for k in odd_k:
        delta=sum(mp.mpc(c)*mp.exp(2*mp.pi*mp.j*(k*j)/n) for j,c in enumerate(coeff))
        selected_diffs.append(mp.fabs(delta))
    gap=max(selected_diffs)
    x=np.asarray(complementary_signal(idx,n))
    y=np.asarray(complementary_signal(other,n))
    full_delta=np.fft.fft(x-y)
    return {"N":n,"r":r,"odd_bins":odd_k,"masks":[idx,other],"selected_max_abs_high_precision":mp.nstr(gap,35),"full_max_abs":float(abs(full_delta).max()),"ratio":mp.nstr(float(abs(full_delta).max())/gap,25),"nonzero_difference_coeffs":sum(c!=0 for c in coeff)}


def run():
    return [measured_pair(n,r) for n,r in [(16,1),(16,2),(16,4),(32,1),(32,2)]]

if __name__=='__main__':
    result=run()
    (Path(__file__).resolve().parent/'joint_measurement_results.json').write_text(json.dumps(result,indent=2)+'\n')
    for row in result:
        print('N',row['N'],'r',row['r'],'max_selected',row['selected_max_abs_high_precision'],'ratio',row['ratio'])
