"""Numerical full-state check for sequential fibers with one shared scratch.

The local primitive is synthetic: it has an ill-conditioned invertible prefix
on (two B-banks + scratch) and then exactly cancels it before a unitary bank
exchange.  The purpose is to validate the block-diagonal/shared-scratch
condition-reset argument, not to model the #130 circuit itself.
"""
import json
import math
from pathlib import Path
import numpy as np


def dft(n):
    j=np.arange(n)[:,None]; k=np.arange(n)[None,:]
    return np.exp(-2j*np.pi*j*k/n)/math.sqrt(n)


def swap_block(B):
    U=dft(B); Z=np.zeros((B,B),complex)
    return np.block([[Z,-U.conj().T],[U,Z]])


def local_prefixes(B, scratch, K):
    d=2*B+scratch
    scales=np.geomspace(1.0,K,d)
    D=np.diag(scales.astype(complex))
    Di=np.diag((1/scales).astype(complex))
    W=np.block([
        [swap_block(B), np.zeros((2*B,scratch),complex)],
        [np.zeros((scratch,2*B),complex), np.eye(scratch,dtype=complex)]
    ])
    # cumulative prefixes: D, then Di@D=I, then W
    return [D, Di@D, W], W


def embed_current(prefix, N, B, scratch, fiber):
    # Full coordinates: bank A N, bank B N, shared scratch s.
    total=2*N+scratch
    idx=list(range(fiber*B,(fiber+1)*B))
    idx += list(range(N+fiber*B,N+(fiber+1)*B))
    idx += list(range(2*N,2*N+scratch))
    M=np.eye(total,dtype=complex)
    M[np.ix_(idx,idx)] = prefix
    return M


def embed_completed(W, N, B, scratch, fiber):
    return embed_current(W,N,B,scratch,fiber)


def run(N=12,B=3,scratch=4,K=1e5):
    assert N%B==0
    prefixes,W=local_prefixes(B,scratch,K)
    Q=np.eye(2*N+scratch,dtype=complex)
    rows=[]; maxc=1.0
    for f in range(N//B):
        base=Q.copy()
        for t,P in enumerate(prefixes,1):
            M=embed_current(P,N,B,scratch,f)@base
            c=float(np.linalg.cond(M)); maxc=max(maxc,c)
            rows.append({'fiber':f,'prefix':t,'condition':c})
        Q=embed_completed(W,N,B,scratch,f)@base
        # scratch is restored at fiber boundary; completed block is unitary
        c=float(np.linalg.cond(Q)); maxc=max(maxc,c)
        rows.append({'fiber':f,'prefix':'completed','condition':c})
    return {'N':N,'B':B,'scratch':scratch,'K':K,
            'max_condition':maxc,'final_condition':float(np.linalg.cond(Q)),
            'rows':rows}


def main():
    out=[run(K=K) for K in (1e2,1e4,1e6)]
    p=Path(__file__).with_name('full_state_shared_scratch_results.json')
    p.write_text(json.dumps(out,indent=2))
    for x in out:
        print('K=',x['K'],'max=',x['max_condition'],'final=',x['final_condition'])
    print('wrote',p)

if __name__=='__main__': main()
