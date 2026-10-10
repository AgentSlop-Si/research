"""Transparent asymptotic and finite-size table cost accounting."""
from dataclasses import dataclass,asdict
from math import ceil,log2

@dataclass
class Accounting:
    log2_N:int
    epsilon:float
    cap_fraction:float
    quantization_R:int
    states_per_component:int
    states_per_complex:int
    grouped_block_K:int
    grouped_levels:int
    passes:int
    full_table_entries:int
    full_table_output_words:int
    normalized_error_bound:float
    log2_table_entries:float
    preprocessing_below_N:bool


def model(log2_N:int,epsilon:float=0.05,cap_fraction:float=0.5)->Accounting:
    if log2_N<1 or epsilon<=0 or not (0<cap_fraction<1):
        raise ValueError("invalid log N, error or table exponent fraction")
    # This conservative R depends on L rather than group count so is easier
    # to choose before K, and ensures rounded error O(epsilon).
    R=ceil(8*(log2_N+1)/epsilon)
    q=2*R+1
    max_key_bits=cap_fraction*log2_N
    K=1
    while (2*(2*K))*log2(q)+log2(2*K)<=max_key_bits:
        K*=2
    t=K.bit_length()-1
    groups=ceil(log2_N/t) if t>=1 else log2_N
    table_entries=q**(2*K) if t>=1 else 0
    words=K*table_entries
    bound=(4*groups+1)/R
    return Accounting(log2_N,epsilon,cap_fraction,R,q,q*q,K,t,groups,table_entries,words,bound,
                      (2*K*log2(q)) if t>=1 else 0.0,
                      (t>=1 and 2*K*log2(q)+log2(K)<log2_N))


def summary(rows):
    result=[]
    for l in rows:
        r=model(l)
        result.append({
          'log2_N':l,'grid_step':1/r.quantization_R,'bits_per_complex':2*log2(r.states_per_component),
          'grouped_K':r.grouped_block_K,'butterflies_per_lookup':r.grouped_levels,
          'passes':r.passes,'ordinary_stages':l,'ideal_stage_reduction_factor':r.grouped_levels,
          'table_entries_log2':r.log2_table_entries,'table_exponent_N':r.log2_table_entries/l,
          'normalization_error_bound':r.normalized_error_bound})
    return result

if __name__=='__main__':
    import json
    print(json.dumps(summary([8,12,20,64,128,256,1024,8192,65536]),indent=2))
