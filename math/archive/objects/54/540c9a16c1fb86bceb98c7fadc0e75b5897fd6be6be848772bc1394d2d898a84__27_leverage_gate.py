"""A sharp fixed-frame rank/leverage obstruction for noncommuting chirp recovery.

For any M-by-q full-column-rank V, Pi=V(V*V)^(-1)V* is a rank-q
orthogonal projector. The M leverage values ell[u]=Pi[u,u] satisfy
  0<=ell[u]<=1, sum_u ell[u]=q, min_u ell[u]<=q/M.
Consequently, for any fixed collection of such projectors with q<=r,
there is a nonzero impulse-per-block input x such that
  ||F x - F Pi x||_2^2 >= (1-r/M)||x||_2^2.
This is a restricted, fixed-family minimax obstruction, NOT a universal
FFT lower bound nor applicable to arbitrary state selection after seeing x.
"""
from __future__ import annotations
import math
import json
from pathlib import Path
import numpy as np
import unit_step_core as core
import gram_union as gu


def leverage(g:int,M:int,states:tuple[core.ChirpState,...]):
    K=g//M;q=len(states)
    if q==0:return np.zeros((K,M),dtype=float)
    v=np.stack([np.conj(core.local_phase_matrix(g,M,st)) for st in states],axis=2)
    gam=np.einsum('kui,kuj->kij',v.conj(),v,optimize=True)
    coeff=np.linalg.solve(gam,v.swapaxes(1,2).conj()) # shape K,q,M
    lev=np.real(np.einsum('kui,kiu->ku',v,coeff,optimize=True))
    return lev


def construct_worst_fixed_union(g,m,M,families):
    x=np.zeros((g,m),dtype=np.complex128)
    summary=[]
    for s,fam in enumerate(families):
        lev=leverage(g,M,tuple(fam))
        idx=np.argmin(lev,axis=1)
        for r,u in enumerate(idx):
            x[r*M+u,s]=1.
        summary.append({'s':s,'q':len(fam),'minimum_leverage':float(lev.min()),
                        'max_leverage':float(lev.max()),
                        'max_trace_defect':float(np.max(abs(np.sum(lev,axis=1)-len(fam))))})
    return x.reshape(-1),summary


def experiment():
    records=[]
    for g,m,M in [(32,3,4),(64,3,8),(128,3,8),(256,3,8)]:
        families=gu.example_noncommuting_states(g,m,M)
        x,summary=construct_worst_fixed_union(g,m,M,families)
        result=gu.union_projection(x,families,M)
        relsq=result.residual_squared/result.energy
        q=len(families[0])
        assert relsq>=1-q/M-1e-10
        assert all(d['max_trace_defect']<1e-10 for d in summary)
        records.append({'N':g*m,'G':g,'M':M,'q':q,
                        'minimax_bound_rel_squared':1-q/M,
                        'actual_witness_rel_squared':relsq,
                        'max_gram_condition':result.maximum_gram_condition,
                        'columns':summary})
    target=Path(__file__).parent/'LEVERAGE_RESULTS.json'
    target.write_text(json.dumps(records,indent=2)+'\n')
    print(json.dumps([{'N':r['N'],'M':r['M'],'q':r['q'],
                       'minimax_lower':r['minimax_bound_rel_squared'],
                       'observed_rel_sq':r['actual_witness_rel_squared']} for r in records],indent=2))

if __name__=='__main__':experiment()
