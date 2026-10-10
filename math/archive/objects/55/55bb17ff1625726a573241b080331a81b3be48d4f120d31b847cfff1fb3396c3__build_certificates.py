"""Generate compact, self-contained exact obstruction certificates."""
import random
import json
from parity_oracle import best_witness
from gf2_depth_certificate import random_invertible_columns,construct_witness
from heterogeneous_certificate import derive


def legacy_columns(k,seed=20261016):
    rng=random.Random(seed+17*k)
    return [random_invertible_columns(k,rng) for _ in range(3)]


def produce():
    output={'kind':'Exact parity-block Fourier rank and GF2-affine scan depth certificates',
            'created':'2026-10-10','legacy_seed':20261016,
            'legacy_layout_witnesses':{}, 'universal_GF2_depth_witnesses':{},
            'heterogeneous_example':None}
    for k in (8,9,10,11,12):
        layout=legacy_columns(k)
        witness=best_witness(k,layout)
        witness['three_GF2_shuffle_columns']=layout
        output['legacy_layout_witnesses'][str(1<<k)]=witness
    for t in (2,3,4,5,6):
        q=(4*t-1).bit_length();k=t*q+1
        cols=[random_invertible_columns(k,random.Random(90000+t*100+j)) for j in range(t-1)]
        witness=construct_witness(k,cols,1)
        witness['GF2_shuffle_columns']=cols
        output['universal_GF2_depth_witnesses'][str(t)]=witness
    k=29;orders=[1,2,1,3]; quotas=[5,6,5,7]
    # 1/32 + 2/64 + 1/32 + 3/128 = 0.117..., sum quotas 23<k
    cols=[random_invertible_columns(k,random.Random(92000+j)) for j in range(3)]
    witness=derive(k,cols,orders,quotas)
    witness['GF2_shuffle_columns']=cols
    output['heterogeneous_example']=witness
    from pathlib import Path
    path=Path(__file__).resolve().parent/'EXACT_CERTIFICATES.json'
    with open(path,'w') as f:json.dump(output,f,indent=2)
    return output

if __name__=='__main__':
    obj=produce()
    for N,rec in obj['legacy_layout_witnesses'].items():
        print(f'N={N} gap={rec["gap"]} input={rec["input_mask"]} output={rec["output_mask"]} '
              f'capacity={rec["capacity"]} rank={rec["complex_fourier_rank"]}')
    for t,rec in obj['universal_GF2_depth_witnesses'].items():
        print(f'Universal rank-one t={t} k={rec["k"]} gap={rec["gap"]}',flush=True)
