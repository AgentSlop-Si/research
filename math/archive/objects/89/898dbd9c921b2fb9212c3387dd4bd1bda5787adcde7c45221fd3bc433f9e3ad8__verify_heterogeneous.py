import json,random,sys
from math import isqrt
sys.path.insert(0,'fft_dyadic_green_20261010')
from heterogeneous_fibers import *


def order_root(p,N):
    # all selected p prime and N power-of-2 or divides p-1
    from verify import primitive_root
    return pow(primitive_root(p),(p-1)//N,p)

rng=random.Random(20261010)
result={'heterogeneous_cases':0,'heterogeneous_heavy_cases':0,'random_rejections':0,'independent_exact_DFT_bins':0}
for N,p,Q in ((32,97,4),(64,257,8),(128,257,8),(144,577,12),(256,65537,16),(512,7681,16),(1024,65537,32)):
    assert (p-1)%N==0
    omega=order_root(p,N)
    M=N//Q
    for trial in range(11):
        budget=Q
        rows=[]
        # Important heavy case: first fiber uses all M modes, if M<=budget.
        if trial==0 and M<=budget:
            s=rng.sample(range(M),M)
            rows.append(tuple((h,rng.randrange(1,p)) for h in s))
            budget-=M
            result['heterogeneous_heavy_cases']+=1
        else:rows.append(())
        for t in range(1,Q):
            size=min(budget, rng.randrange(4) if trial%3 else rng.randrange(6))
            s=rng.sample(range(M),size)
            rows.append(tuple((h,rng.randrange(1,p)) for h in s))
            budget-=size
        raw=build_input(rows,p,omega,N)
        found=recognize_total_budget(raw,p,omega,Q,Q)
        assert found is not None,(N,trial,'rejected valid signal')
        z=transform_modes(found,p,omega,N)
        # independent direct DFT, not FFT
        direct=direct_dft(raw,p,omega)
        assert z==direct,(N,trial)
        result['heterogeneous_cases']+=1
        result['independent_exact_DFT_bins']+=N
    for trial in range(7):
        x=[rng.randrange(p) for _ in range(N)]
        found=recognize_total_budget(x,p,omega,Q,Q)
        assert found is None,(N,trial,'accepted random dense vector')
        result['random_rejections']+=1
print(json.dumps(result,indent=2))
with open('fft_dyadic_green_20261010/HETEROGENEOUS_RESULTS.json','w') as f:json.dump(result,f,indent=2)
# Positive extension not covered by the old uniform per-fiber r=O(1) theorem:
# one full-M-mode fiber, Q-1 one-mode fibers, total <=2Q.
from verify import rank_mod
for N,p,Q in ((64,257,8),(256,65537,16),(1024,65537,32)):
    M=N//Q
    assert M==Q
    omega=order_root(p,N)
    rows=[tuple((h,rng.randrange(1,p)) for h in range(M))]
    rows += [((t-1,rng.randrange(1,p)),) for t in range(1,Q)]
    x=build_input(rows,p,omega,N)
    found=recognize_total_budget(x,p,omega,Q,2*Q)
    assert found is not None and sum(map(len,found))==2*Q-1
    assert transform_modes(found,p,omega,N)==direct_dft(x,p,omega)
    matrix=[[x[t+Q*u] for u in range(M)] for t in range(Q)]
    assert rank_mod(matrix,p)==Q
    result.setdefault('heavy_and_max_rank_cases',0)
    result['heavy_and_max_rank_cases']+=1
    result['heterogeneous_cases']+=1
    result['independent_exact_DFT_bins']+=N
print('EXTENDED',json.dumps(result,indent=2))
with open('fft_dyadic_green_20261010/HETEROGENEOUS_RESULTS.json','w') as f:json.dump(result,f,indent=2)
