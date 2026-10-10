"""Independent finite-field full-basis audit of the Phase15 joint evaluator.

Works over F_p where p=1 mod N. Uses only explicit modular additions,
multiplications, inverse, and short DFTs computed by direct sums. No
NumPy, Green output caching, or a hidden full-N FFT is used.

Checks both the full-rank stationary Wc expansion and the Wc-direct collapse
on every source basis vector against an independent N-point Fourier entry.
The slower W-inverse mode is diagnostic only; q-M streams would not save work.
"""
from __future__ import annotations
import json
from pathlib import Path
import sys
from field_stationary_audit import invert_matrix
from field_gram_audit import primitive_root,tri


def prepare(N,p,M):
    G=N&-N;odd=N//G;K=G//M
    assert G>=M*M and M>=2 and (M&(M-1))==0 and K>=M
    assert (p-1)%N==0
    z=primitive_root(N,p);zg=pow(z,odd,p)
    zK=pow(zg,M,p);zM=pow(zg,K,p);zm=pow(z,G,p)
    E=[(K*(u*(u+1)//2)+u)%G for u in range(M)]
    assert len({(u*(u+1)//2)%M for u in range(M)})==M
    W=[[pow(zg,(-i*E[u])%G,p) for i in range(M)] for u in range(M)]
    Winv=invert_matrix(W,p)
    assert all(sum(W[u][i]*Winv[i][v] for i in range(M))%p==int(u==v)
               for u in range(M) for v in range(M))
    return {
      'N':N,'G':G,'m':odd,'K':K,'M':M,'p':p,
      'z':z,'zg':zg,'zK':zK,'zM':zM,'zm':zm,
      'W':W,'Winv':Winv,
      'shortK':[[pow(zK,(-t*r)%K,p) for r in range(K)] for t in range(K)],
      'shortM':[[pow(zM,(-e*u)%M,p) for u in range(M)] for e in range(M)],
      'twid':[[pow(z,(-k*s)%N,p) for s in range(odd)] for k in range(G)],
      'oddDFT':[[pow(zm,(-a*s)%odd,p) for s in range(odd)] for a in range(odd)],
      'diag':[[[pow(zg,(tri(u)+(M*r+3*s)*u)%G,p) for u in range(M)]
               for r in range(K)] for s in range(odd)],
      'pref':[[[pow(zg,(-v*u-tri(u)-3*s*u)%G,p) for u in range(M)]
               for v in range(K)] for s in range(odd)]
    }


def apply_short(vec,cfg,frame=False,wrong_shift=False):
    N=cfg['N'];G=cfg['G'];K=cfg['K'];M=cfg['M'];m=cfg['m'];p=cfg['p']
    assert len(vec)==N
    stage=[[0]*m for _ in range(G)]
    active=range(m)
    for s in active:
        data=[[vec[(r*M+u)*m+s] for u in range(M)] for r in range(K)]
        if not any(z for row in data for z in row): continue
        prep=cfg['diag'][s]
        y=[[data[r][u]*prep[r][u]%p for u in range(M)] for r in range(K)]
        if frame:
            W=cfg['W'];Wi=cfg['Winv']
            # Full noncommuting frame c=W^-1 D^-1 x
            c=[[sum(Wi[i][u]*y[r][u] for u in range(M))%p for i in range(M)]
               for r in range(K)]
            assert all(sum(W[u][i]*c[r][i] for i in range(M))%p==y[r][u]
                       for r in range(K) for u in range(M))
            hat=[[sum(cfg['shortK'][t][r]*c[r][i] for r in range(K))%p
                  for t in range(K)] for i in range(M)]
        else:
            # Collapse Wc=y BEFORE doing M independent short K-FFTs.
            hat=[[sum(cfg['shortK'][t][r]*y[r][u] for r in range(K))%p
                  for t in range(K)] for u in range(M)]
        for v in range(K):
            vals=[]
            for u in range(M):
                t=v if wrong_shift else (v+u)%K
                if frame:
                    accum=sum(cfg['W'][u][i]*hat[i][t] for i in range(M))%p
                else:
                    accum=hat[u][t]
                vals.append(accum*cfg['pref'][s][v][u]%p)
            for ell in range(M):
                stage[v+K*ell][s]=sum(vals[u]*cfg['shortM'][ell][u]
                                          for u in range(M))%p
    # Final odd-factor short m-DFT (no full-size oracle used).
    return [sum(stage[k1][s]*cfg['twid'][k1][s]*cfg['oddDFT'][k2][s]
                for s in range(m))%p
            for k2 in range(m) for k1 in range(G)]


def verify_case(N,p,M):
    cfg=prepare(N,p,M)
    z=cfg['z']
    checks=0;frame_checks=0
    for n in range(N):
        vec=[0]*N;vec[n]=1
        a=apply_short(vec,cfg,frame=False)
        b=apply_short(vec,cfg,frame=True)
        for k in range(N):
            expected=pow(z,(-n*k)%N,p)
            assert a[k]==b[k]==expected,(N,n,k,a[k],b[k],expected)
            checks+=1
            frame_checks+=1
    # A deterministic non-basis input ensures linear superposition with
    # multiple active odd-column frames, not merely impulse lookups.
    vec=[(31*i*i+17*i+19)%p for i in range(N)]
    fused=apply_short(vec,cfg)
    framed=apply_short(vec,cfg,frame=True)
    assert fused==framed
    # independently evaluate Fourier at every output for the dense vector
    assert all(fused[k]==sum(vec[n]*pow(z,(-k*n)%N,p) for n in range(N))%p
               for k in range(N))
    # Mutation must be rejected; forgetting +(u) in the frequency index
    # is a plausible algebraic error when trying to fuse long scans.
    wrong=apply_short(vec,cfg,wrong_shift=True)
    failures=sum(a!=b for a,b in zip(wrong,fused))
    assert failures>0
    return {'N':N,'p':p,'M':M,'G':cfg['G'],'K':cfg['K'],'odd_m':cfg['m'],
            'all_basis_entries':checks,'frame_joint_entries':frame_checks,
            'mutated_wrong_shift_rejected':failures,
            'dense_signal_checked':True,
            'short_K_DFTs_per_fresh_input':cfg['m']*cfg['M'],
            'short_M_DFTs_per_fresh_input':cfg['m']*cfg['K'],
            'full_N_DFT_calls':0,'long_G_scans':0}


def main():
    cases=[(48,97,4),(80,641,4),(96,97,4),(192,193,8),(384,769,8)]
    rows=[verify_case(*args) for args in cases]
    output={'scope':'all-basis Fp equivalence of the stationary noncommuting bank and gauged 2-factor FFT; standard O(NlogN) work',
            'cases':rows,'exact_basis_entries':sum(row['all_basis_entries'] for row in rows),
            'exact_frame_joint_entries':sum(row['frame_joint_entries'] for row in rows),
            'not_a_sub_nlogn_fft':True}
    (Path(__file__).parent/'FIELD_JOINT_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'cases':[c['N'] for c in rows],
                      'basis_entries':output['exact_basis_entries'],
                      'wrong_shift_mutations':[c['mutated_wrong_shift_rejected'] for c in rows]},indent=2))

if __name__=='__main__':main()
