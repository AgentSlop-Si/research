"""Exact finite-field, all-basis audit for noncommuting two-slope Gram union.

Checks (a) local projector idempotence, (b) noncommuting q=1 projectors,
(c) the unit-step Fourier Green recurrence WITHOUT invoking an FFT backend,
(d) exact projected-input Fourier outputs over all input basis vectors,
(e) a two-slope dense structured positive control and a dropped-slope
mutation. Finite-instance audit, not a formal general proof.
"""
from __future__ import annotations
import json
from pathlib import Path
from dataclasses import dataclass
from math import gcd


def prime_factors(v):
    ans=[];d=2
    while d*d<=v:
        if v%d==0:
            ans.append(d)
            while v%d==0:v//=d
        d+=1
    if v>1:ans.append(v)
    return ans


def primitive_root(n,p):
    assert (p-1)%n==0
    pf=prime_factors(p-1)
    gen=next(x for x in range(2,p) if all(pow(x,(p-1)//q,p)!=1 for q in pf))
    z=pow(gen,(p-1)//n,p)
    assert pow(z,n,p)==1 and all(pow(z,n//q,p)!=1 for q in prime_factors(n))
    return z


def tri(u):return u*(u-1)//2


def exponent(g,M,a,beta,r,u):
    return (a*tri(u) + (a*M*r+beta)*u)%g


def phases(g,M,p,zg,state,r):
    a,beta=state
    return [pow(zg,exponent(g,M,a,beta,r,u),p) for u in range(M)]


def inv(x,p):
    assert x%p !=0
    return pow(x,-1,p)


def rank_one_apply(phase,vector,p):
    M=len(vector)
    dot=sum(phase[u]*vector[u] for u in range(M))%p
    z=dot*inv(M,p)%p
    return [z*inv(phase[u],p)%p for u in range(M)]


def gram2_coefficients(x,ps,pt,p):
    M=len(x)
    h=sum(ps[u]*inv(pt[u],p) for u in range(M))%p
    hb=sum(pt[u]*inv(ps[u],p) for u in range(M))%p
    det=(M*M-h*hb)%p
    if det==0:raise ValueError('Zero Gram determinant in chosen finite field')
    b0=sum(ps[u]*x[u] for u in range(M))%p
    b1=sum(pt[u]*x[u] for u in range(M))%p
    i=inv(det,p)
    c0=(M*b0-h*b1)*i%p
    c1=(M*b1-hb*b0)*i%p
    return c0,c1


def project2(x,ps,pt,p):
    c0,c1=gram2_coefficients(x,ps,pt,p)
    return [(c0*inv(ps[u],p)+c1*inv(pt[u],p))%p for u in range(len(x))]


def decode_chirp_unscaled_mod(d,g,M,state,zg,p):
    """Exact arithmetic analog of core.decode_balanced_scan, no FFT oracle.

    Returns the UNnormalized G-transform of the chirp-local vector
    sum_r conj(S_state[r,:]) * d[r]. Derives its output by the cyclic
    first-order recurrence, using a single K-point direct DFT of d.
    """
    a,beta=state;K=g//M
    zK=pow(zg,M,p)
    dhat=[sum(d[r]*pow(zK,(-j*r)%K,p) for r in range(K))%p
          for j in range(K)]
    terms=[];gauges=[];idxs=[]
    for j in range(g):
        idx=a*j%g
        ga=pow(zg,(a*tri(j)+beta*j)%g,p)
        bound=pow(zg,(-M*(idx+beta)-a*tri(M))%g,p)
        force=(dhat[idx%K]-bound*dhat[(idx+a*M)%K])%p
        terms.append(force*inv(ga,p)%p)
        gauges.append(ga);idxs.append(idx)
    seed=(sum(terms)*inv(2,p))%p
    out=[0]*g;prefix=0
    for j in range(g):
        out[idxs[j]]=gauges[j]*(seed-prefix)%p
        prefix=(prefix+terms[j])%p
    return out


def verify_case(n,p,M):
    g=n&-n;m=n//g;K=g//M
    assert g>=16 and g>=M*M and g>1
    z=primitive_root(n,p)
    zg=pow(z,m,p)
    zm=pow(z,g,p)
    states=[((1,(3*s)%g),(1+g//4,(3*s+1)%g)) for s in range(m)]
    assert all(gcd(a,g)==1 for group in states for a,b in group)
    phases_all=[[[phases(g,M,p,zg,state,r) for state in states[s]]
                 for r in range(K)] for s in range(m)]
    local_checks=0
    for s in range(m):
        for r in range(K):
            ps,pt=phases_all[s][r]
            for u in range(M):
                x=[int(v==u) for v in range(M)]
                proj=project2(x,ps,pt,p)
                assert project2(proj,ps,pt,p)==proj
                local_checks+=M
    # Show the two individual rank-one projections do NOT commute.
    ps,pt=phases_all[0][0]
    u=[1]+[0]*(M-1)
    forward=rank_one_apply(ps,rank_one_apply(pt,u,p),p)
    reverse=rank_one_apply(pt,rank_one_apply(ps,u,p),p)
    assert forward!=reverse, 'Two slope projectors accidentally commute'
    # Independent check of the modulo-p unit-step recurrence.
    decoder_entries=0
    for s in range(m):
        for i,state in enumerate(states[s]):
            for r in range(K):
                d=[int(t==r) for t in range(K)]
                got=decode_chirp_unscaled_mod(d,g,M,state,zg,p)
                pp=phases_all[s][r][i]
                for k in range(g):
                    expected=sum(inv(pp[u],p)*pow(zg,(-k*(r*M+u))%g,p)
                                 for u in range(M))%p
                    assert got[k]==expected,(n,p,s,i,r,k)
                    decoder_entries+=1
    # Each input e_n projects to q=2 local chirp span. Decode fast Green
    # recurrence -> CT -> compare to direct Fourier of the projected vector.
    checks=0
    for source in range(n):
        s=source%m;rg=(source//m)//M;u=(source//m)%M
        ps,pt=phases_all[s][rg]
        x=[int(v==u) for v in range(M)]
        c0,c1=gram2_coefficients(x,ps,pt,p)
        proj=[(c0*inv(ps[v],p)+c1*inv(pt[v],p))%p for v in range(M)]
        d0=[0]*K;d1=[0]*K
        d0[rg]=c0;d1[rg]=c1
        stage0=decode_chirp_unscaled_mod(d0,g,M,states[s][0],zg,p)
        stage1=decode_chirp_unscaled_mod(d1,g,M,states[s][1],zg,p)
        stage=[(stage0[k]+stage1[k])%p for k in range(g)]
        for k2 in range(m):
            for k1 in range(g):
                k=k1+g*k2
                # Only column s nonzero on this single-basis input.
                obtained=stage[k1]*pow(z,(-k1*s)%n,p)*pow(zm,(-k2*s)%m,p)%p
                direct=sum(proj[v]*pow(z,(-k*((rg*M+v)*m+s))%n,p)
                           for v in range(M))%p
                assert obtained==direct,(n,source,k,obtained,direct)
                checks+=1
    # Dense structured signal using nonzero contribution from *both* slopes.
    # Dropping second slope must fail exact recovery for this signal.
    mutation_fail=0
    for s in range(m):
        for r in range(K):
            ps,pt=phases_all[s][r]
            x=[(inv(ps[u],p)+2*inv(pt[u],p))%p for u in range(M)]
            assert project2(x,ps,pt,p)==x
            if rank_one_apply(ps,x,p)!=x:
                mutation_fail+=1
    assert mutation_fail>0
    return {'N':n,'prime':p,'M':M,'G':g,'odd_part':m,
            'all_basis_fourier_entries':checks,
            'local_idempotence_entries':local_checks,
            'independent_chirp_decoder_entries':decoder_entries,
            'noncommuting_projectors':True,
            'dropped_slope_mutations_rejected':mutation_fail}


def main():
    cases=[(48,97,4),(80,641,4),(96,97,4),(160,641,4)]
    res=[verify_case(*c) for c in cases]
    record={'scope':'Exact finite-field ALL-BASIS two-slope projection+Green recurrence+CT check, not a universal FFT theorem',
            'cases':res,
            'total_basis_entries':sum(r['all_basis_fourier_entries'] for r in res),
            'total_decoder_entries':sum(r['independent_chirp_decoder_entries'] for r in res)}
    target=Path(__file__).parent/'FINITE_FIELD_RESULTS.json'
    target.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2))

if __name__=='__main__':main()
