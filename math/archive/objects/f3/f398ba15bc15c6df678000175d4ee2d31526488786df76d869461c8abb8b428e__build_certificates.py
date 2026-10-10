from __future__ import annotations
import json,random
from pathlib import Path
from nonlinear_fourier_oracle import moving_partition_certificate
from permutation_edits import affine_from_columns,mcnot_permutation,rank_permutation_difference,robust_rank_limit
from exact_field_controls import fourier_rank_mod

BASE=Path(__file__).resolve().parent
# Reproduce the earlier GF(2) layout from its published deterministic seed.
def _random_invertible_columns(k,rng):
    columns=[1<<i for i in range(k)]
    for _ in range(2*k*k):
        i,j=rng.sample(range(k),2)
        if rng.randrange(4)==0:
            mask=(1<<i)|(1<<j)
            columns=[c ^ ((((c>>i)&1)^((c>>j)&1))*mask) for c in columns]
        else:
            columns=[c ^ (((c>>j)&1)<<i) for c in columns]
    return columns

def legacy_columns(k,seed=20261016):
    rng=random.Random(seed+17*k)
    return [_random_invertible_columns(k,rng) for _ in range(3)]

def pullback_mask(mask,cols):
    return sum(((v&mask).bit_count()%2)<<i for i,v in enumerate(cols))

def produce():
    obj={'date':'2026-10-10','status':'Exact rank obstructions, NOT an improved FFT',
         'previous_archive':'prior_checkpoint_full.zip',
         'nonaffine_256':{},'edit_robust':{}}
    k=8;n=1<<k;cols=legacy_columns(k)
    perms=[affine_from_columns(c) for c in cols]
    baseline=moving_partition_certificate(k,perms,[1]*4,112)
    gates=[{'controls':list(cs),'target':tar} for cs,tar in [((2,7),6),((3,6),2),((2,4),3),((3,4),2),((2,3),4)]]
    changed=[p.copy() for p in perms]
    for step in gates:
        changed[2]=changed[2][mcnot_permutation(k,step['controls'],step['target'])]
    result=moving_partition_certificate(k,changed,[1]*4,112)
    C=[x for x in range(n) if ((x&112).bit_count()&1)==0]
    assert result['rank_gap']==4 and result['capacity_bound']==124
    obj['nonaffine_256']={
         'k':k,'stages':4,'stage_rank_bound':1,
         'affine_shuffle_columns':cols,
         'toffoli_gate_sequence_in_shuffle_2':gates,
         'baseline_affine_witness':{x:y for x,y in baseline.items() if x!='output_rows'},
         'witness':result,
         'modular_fourier_ranks':{str(p):fourier_rank_mod(n,result['output_rows'],C,p) for p in (12289,65537)},
         'directed_scan_network_mincut':124,
         'full_shuffle_nonaffine_mismatches_to_its_linearized_map':160
    }
    for k in (11,12):
        n=1<<k; cols=legacy_columns(k)
        affine=[affine_from_columns(c) for c in cols]
        input_mask={11:1648,12:3584}[k]
        baseline=moving_partition_certificate(k,affine,[1]*4,input_mask)
        bmask=input_mask
        for col in cols:bmask=pullback_mask(bmask,col)
        rec={'input_mask':input_mask,'output_mask':bmask,
             'stage_capacities':baseline['stage_channel_budget'],
             'capacity':baseline['capacity_bound'],
             'complex_fourier_rank':baseline['exact_complex_fourier_rank']}
        changed=[p.copy() for p in affine]
        edits=[{'shuffle_index':0,'controls':[0,2],'target':k-1},
               {'shuffle_index':1,'controls':[1,3],'target':k-1}]
        ds=[]
        for gate in edits:
            j=gate['shuffle_index']
            changed[j]=changed[j][mcnot_permutation(k,gate['controls'],gate['target'])]
            ds.append(rank_permutation_difference(changed[j],affine[j]))
        assert ds==[n//8,n//8]
        assert rec['complex_fourier_rank']>robust_rank_limit(rec['capacity'],ds)
        obj['edit_robust'][str(n)]={
          'k':k,'affine_shuffle_columns':cols,
          'base_input_mask':rec['input_mask'],
          'base_output_mask':rec['output_mask'],
          'base_stage_boundaries':rec['stage_capacities'],
          'base_capacity':rec['capacity'],
          'exact_complex_fourier_rank':rec['complex_fourier_rank'],
          'nonlinear_edits':edits,
          'edit_ranks':ds,
          'perturbed_network_rank_bound_on_original_endpoint_sets':robust_rank_limit(rec['capacity'],ds),
          'strict_gap':rec['complex_fourier_rank']-robust_rank_limit(rec['capacity'],ds)
        }
    (BASE/'EXACT_CERTIFICATES.json').write_text(json.dumps(obj,indent=2))
    for key,v in obj['edit_robust'].items():
        print('ROBUST',key,'Fourier rank',v['exact_complex_fourier_rank'],'network max',v['perturbed_network_rank_bound_on_original_endpoint_sets'],'gap',v['strict_gap'])
    w=obj['nonaffine_256']['witness'];print('NONAFFINE',w['N'],'Fourier',w['exact_complex_fourier_rank'],'network',w['capacity_bound'],'gap',w['rank_gap'])
if __name__=='__main__':produce()
