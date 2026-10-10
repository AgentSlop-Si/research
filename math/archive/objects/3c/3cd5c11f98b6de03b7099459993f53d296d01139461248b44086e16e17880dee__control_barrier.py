#!/usr/bin/env python3
"""Exact control-dimension / dense convolution barrier for a Weyl-cycle extension."""
import random,json,math
from phase8_weyl_cycle import P,root_of_unity,exact_ntt

def check_single(k,seed):
    rng=random.Random(seed);w=root_of_unity(k)
    u=[rng.randrange(1,P) for _ in range(k)]
    v=[rng.randrange(P) for _ in range(k)]
    g=[vb*pow(ub,P-2,P)%P for ub,vb in zip(u,v)]
    U=exact_ntt(u,pow(w,P-2,P))
    G=exact_ntt(g,pow(w,P-2,P))
    V=exact_ntt(v,pow(w,P-2,P))
    invK=pow(k,P-2,P)
    reconstructed=[sum(G[q]*U[(ell-q)%k] for q in range(k))*invK%P for ell in range(k)]
    assert reconstructed==V
    return len([q for q in G if q!=0])

def main():
    data=[]
    for k in (8,16,32,64,128,256):
        supports=[check_single(k,seed=61_234+k*400+t) for t in range(30)]
        data.append({'k':k,'trials':len(supports),'min_control_spectral_support':min(supports),
            'max_control_spectral_support':max(supports),'exact_convolution_identity':True,
            'union_bound_some_fourier_coefficient_zero':k/P})
    # For fixed seed column u with no zeros, the map g -> v=g*u
    # is bijective; its Fourier transform is bijective too. Thus for
    # g uniform, each Fourier entry is uniform and independently distributed.
    # A fixed predeclared s-dimensional subspace catches only q^(s-k)
    # fraction; adaptive support among K frequencies adds binom(K,s).
    log10_binom=lambda k,s:math.lgamma(k+1)/math.log(10)-math.lgamma(s+1)/math.log(10)-math.lgamma(k-s+1)/math.log(10)
    examples=[]
    for k,s in [(16,2),(32,3),(128,4),(256,8)]:
        examples.append({'k':k,'s':s,
          'log10_union_upper_bound_adaptive_s_sparse_modes':log10_binom(k,s)+(s-k)*math.log10(P)})
    result={'tests':data,'adaptive_dictionary_cardinality_bounds':examples,
            'identity':'DFT(g .* u)[ell] = K^{-1} sum_q DFT(g)[q] DFT(u)[ell-q]',
            'conclusion':'Generic controls have dense spectrum; allowing all per-site controls moves the difficult operation to dense cyclic convolution (not a universal lower bound).'}
    with open('CONTROL_BARRIER.json','w') as f:json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
