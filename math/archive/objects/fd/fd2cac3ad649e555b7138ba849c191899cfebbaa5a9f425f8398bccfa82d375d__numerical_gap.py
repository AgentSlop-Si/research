#!/usr/bin/env python3
"""Floating diagnostics for the analytic, gauge-uniform commutator spectral gap."""
from pathlib import Path
import json, numpy as np
FOLDER=Path(__file__).parent
C=json.loads((FOLDER/'CERTIFICATES.json').read_text())
def branch(x):
    n=len(x['cycle']); T=np.eye(n)
    for i,j in enumerate(x['cycle']):T[i,j]-=x['weights'][i]
    G=np.linalg.inv(T)
    G=np.diag(x['left_diag'])@G@np.diag(x['right_diag'])
    return G[np.ix_(x['row_permutation'],x['col_permutation'])]

def check(w):
    n=w['N'];bs=[branch(v) for v in w['branch_parameters']]
    A=bs[0]+bs[1];B=bs[2]+bs[3]; X=(bs[4]+bs[5]) if not w['two_stage'] else np.eye(n)
    roots=np.exp(-2j*np.pi*np.arange(n)[:,None]*np.arange(n)[None,:]/n)
    H=roots@np.linalg.inv(X); Ai=np.linalg.inv(A)
    Ps=[np.diag(1/B[:,v])@Ai@np.diag(H[:,v]) for v in range(n)]
    P0=Ps[0]; ts=[np.linalg.solve(P0,Ps[v]) for v in range(n)]
    comm=ts[1]@ts[2]-ts[2]@ts[1]
    snorm=lambda M:np.linalg.norm(M,2)
    minsv=lambda M:np.linalg.svd(M,compute_uv=False)[-1]
    m=minsv(P0);a=snorm(ts[1]);b=snorm(ts[2]);s=minsv(comm); M1=snorm(Ps[1]); M2=snorm(Ps[2])
    delta=min(m/2, s*m/(4*np.sqrt(a*a+b*b)*np.sqrt((1+M1/m)**2+(1+M2/m)**2)))
    lb=delta*np.min(np.abs(B))/(np.sqrt(n)*snorm(np.linalg.inv(A))*snorm(np.linalg.inv(X)))
    rng=np.random.default_rng(777)
    diffs=[]
    for j in range(30):
        ell=np.exp(1j*rng.uniform(-3,3,n))*np.exp(rng.uniform(-.5,.5,n))
        dd=np.exp(1j*rng.uniform(-3,3,n))*np.exp(rng.uniform(-.5,.5,n))
        ee=np.exp(1j*rng.uniform(-3,3,n))*np.exp(rng.uniform(-.5,.5,n))
        candidate=np.diag(ell)@A@np.diag(dd)@B@np.diag(ee)@X
        diffs.append(snorm(candidate-roots))
    assert lb>0 and min(diffs)+1e-7>=lb
    return {'N':n,'two_stage':w['two_stage'],'min_singular_comm_diagnostic':s,'analytic_spectral_lower_bound_diagnostic':lb,'smallest_tested_spectral_error':min(diffs),'max_tested_spectral_error':max(diffs)}

def main():
    # Only first four-/six-Green n=4 samples; assertions guard numerical quantities, not a proof of their decimal values.
    results=[]
    for w in C:
        if w['N']==4:results.append(check(w))
    (FOLDER/'NUMERICAL_RESULTS.json').write_text(json.dumps(results,indent=2))
    print(json.dumps(results,indent=2))
if __name__=='__main__':main()
