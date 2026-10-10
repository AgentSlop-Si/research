"""Full-size exact modular verification of a *different* O(N) Green network.
The network is NOT a Fourier transform. It is used as a negative control
against using full commutator rank as an FFT complexity measure.
"""
import json
import random
import time
from phase12 import (
    shift_green_apply,modulation_green_apply,primitive_root_of_order,
    batch_inverse,green_orbit_union_apply,stride_green_apply
)


def main():
    t0=time.time()
    n=65536;q=786433;a=2;b=2
    omega=primitive_root_of_order(n,q)
    assert pow(a,n,q)!=1 and pow(b,n,q)!=1
    rng=random.Random(20261010)
    x=[rng.randrange(q) for _ in range(n)]
    z=modulation_green_apply(x,b,q)
    y=shift_green_apply(z,a,q)
    bad_mod=0; bad_shift=0
    phase=1
    for j in range(n):
        if (1-b*phase)*z[j]%q!=x[j]:bad_mod+=1
        if (y[j]-a*y[(j-1)%n])%q!=z[j]:bad_shift+=1
        phase=phase*omega%q
    assert not bad_mod and not bad_shift
    # Independent dense cyclic-Green kernel evaluation for selected outputs.
    a_power=[1]*n
    for j in range(1,n):a_power[j]=a_power[j-1]*a%q
    scale=pow((1-pow(a,n,q))%q,-1,q)
    indices=[0,1,2,3,4,7,15,32,64,127,255,511,1023,4095,8191,16383,32767,65535]
    direct_matches=0
    for i in indices:
        val=0
        for j in range(n):
            val+=a_power[(i-j)%n]*z[j]
        val=val*scale%q
        assert val==y[i],(i,val,y[i])
        direct_matches+=1
    # Demonstrate that it is not the DFT by checking several actual bins.
    sampled_dft_disagreements=0
    for k in [0,1,2,17]:
        wk=pow(omega,k,q)
        w=1;dft=0
        for u in x:
            dft=(dft+w*u)%q
            w=w*wk%q
        if dft!=y[k]:sampled_dft_disagreements+=1
    assert sampled_dft_disagreements>=3
    K=16
    fused=stride_green_apply(x,pow(a,K,q),K,q)
    explicit=green_orbit_union_apply(x,a,K,q)
    assert fused==explicit
    beta=pow(a,K,q)
    assert all((fused[i]-beta*fused[(i-K)%n])%q==x[i] for i in range(n))
    result={
        'status':'passed','transform_length':n,'field_prime':q,
        'full_green_modulation_residual_failures':bad_mod,
        'full_green_shift_residual_failures':bad_shift,
        'independent_dense_kernel_rows_checked':direct_matches,
        'selected_bins_different_from_real_dft':sampled_dft_disagreements,
        'green_pair_commutator_rank_analytic':n,
        'weyl_twirled_paths':K,
        'full_outputs_exact_green_orbit_fusion_checked':n,
        'orbit_fusion_target':'(I-alpha^16 S^16)^-1, NOT Fourier',
        'time_seconds':round(time.time()-t0,3),
        'warning':'Neither the noncommuting Green pair nor the fused Weyl orbit is the DFT. These are controls for different operators.'
    }
    with open('LARGE_AUDIT_RESULTS.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
