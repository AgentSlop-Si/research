#!/usr/bin/env python3
"""Symbolic (log2 N)-parameter cost ledger: never allocates N entries."""
from math import ceil, floor, log2, log, pi, sqrt
import json

def plan(K,eps=.8,a=1.,gamma=.25):
    B=K
    P0=ceil(32*pi/eps);P1=ceil(32*pi*B/eps)
    p=ceil(log2(4*P0*P1))
    g=max(1,floor(gamma*K/p))
    kmin=ceil(16/(eps*eps)*(log(4)+(a+1)*K*log(2)))
    G=ceil(kmin/g);k=g*G
    h1=eps/(64*sqrt(2));coord_count=ceil(2/h1)+3
    s1=ceil(log2(coord_count**2))
    L=floor(gamma*K/(G*s1))
    if L<=0: return {'log2N':K,'regime_ready':False,'group_count':G,'symbol_bits':s1,'reason':'One transpose lane does not yet fit the N^gamma address bound'}
    chunks=ceil(B/L)
    return {'log2N':K,'regime_ready':True,'B':B,'descriptor_bits':p,'group_size':g,'groups':G,'sample_count':k,
            'transpose_chunk_lanes':L,'transpose_chunks':chunks,'T1_log2_entries_upper':g*p,
            'Ttr_log2_entries_upper':G*s1*L,'T2_log2_entries_upper':G*s1,
            'online_ops_per_block_upper_schematic':k+G+chunks*G+B+chunks,
            'schematic_online_ops_over_B':round((k+G+chunks*G+B+chunks)/B,3)}

if __name__=='__main__':
    print(json.dumps([plan(k) for k in (1000,1000000,100000000,10000000000)],indent=2))
