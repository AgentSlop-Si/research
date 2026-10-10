#!/usr/bin/env python3
"""Dual Phase9 innovation decoder: unknown dense C, spectrally sparse innovations.

If v_{t+1}=C v_t+e_t, first transition clean, C arbitrary circulant,
and each innovation F_K(e_t) has <=s nonzero frequencies, then recover C,
unknown innovation spectral support/values and ALL N Fourier outputs in
O(N(s+1)+K log K+s M^2) exact field operations; for constant s, M=Theta(logN),
this is O(N). Each innovation can be dense in time/position domain.

A Freivalds check rejects invalid inputs except probability <=p^(-R); verified
accepted promised inputs are evaluated with exact finite-field formulas.
This is not a universal all-input FFT speedup, nor a bounded-bit algorithm.
"""
from __future__ import annotations
import random
import secrets
from typing import Optional
from phase8_weyl_cycle import P,Costs,exact_ntt,roots,batch_inverse_nonzero,add,mul,inv
from phase9_dense_cycle import (learn_eigenvalues,decode_sparse_syndromes,
                                ntt_inverse)
from phase6_exact import root_of_unity


def recover_spectral_innovations(cols,lam,tab,max_modes:int,c:Costs):
    m=len(cols);k=len(cols[0]);n=k*m
    if max_modes==0:return [[] for _ in range(m-1)]
    if 2*max_modes>k:raise ValueError('2s<=K required')
    wk=tab[m]
    # lambda_ell = sum_d c_d omega_K^(ell*d), so c = DFT_minus(lambda)/K.
    kernel=ntt_inverse(lam,wk,c)
    innovations=[[] for _ in range(m-1)]
    for t in range(1,m-1):
        probe=[]
        for b in range(2*max_modes):
            cv=0
            for d in range(k):
                cv=add(cv,mul(kernel[d],cols[t][(b+d)%k],c),c)
            probe.append(add(cols[t+1][b],-cv,c))
        # e_t[b] = sum_ell (E_t[ell]/K)*omega_K^(ell*b).
        # Prony recovers ell and amplitude E/K from 2s consecutive b.
        recovered=decode_sparse_syndromes(probe,k,wk,max_modes,c)
        if recovered is None:return None
        innovations[t]=[(ell,mul(amp,k%P,c)) for ell,amp in recovered]
    return innovations


def verify_spectral_innovations(cols,lam,innovations,tab,m,c:Costs,rounds=3,rng=None):
    """Randomized all-transition Freivalds check with spectral errors."""
    if rng is None:rng=secrets.SystemRandom()
    k=len(cols[0]);wk=tab[m];wk_inv=tab[-m]
    invk=inv(k,c)
    for _ in range(rounds):
        w=[rng.randrange(P) for _ in range(k)]
        fw=exact_ntt(w,wk_inv,c)
        fphi=[mul(fw[ell],lam[-ell%k],c) for ell in range(k)]
        phi=ntt_inverse(fphi,wk_inv,c)
        for t in range(m-1):
            lhs=rhs=0
            for b in range(k):
                lhs=add(lhs,mul(w[b],cols[t+1][b],c),c)
                rhs=add(rhs,mul(phi[b],cols[t][b],c),c)
            # w^T e = (1/K) sum_ell E[ell]*F_minus(w)[-ell]
            for ell,ev in innovations[t]:
                rhs=add(rhs,mul(invk,mul(ev,fw[-ell%k],c),c),c)
            if lhs!=rhs:return False
    return True


def exact_spectral_innovation_cycle(x:list[int],m:int,max_modes_per_step:int,
                                     rounds:int=3,c:Optional[Costs]=None,rng=None,
                                     return_certificate:bool=False):
    c=c or Costs()
    n=len(x)
    if m<2 or (m&(m-1)) or n&(n-1) or n%m:raise ValueError
    k=n//m
    if k<m or k&(k-1) or (P-1)%n or max_modes_per_step<0 or 2*max_modes_per_step>k:
        raise ValueError
    if rounds<1:raise ValueError('at least one Freivalds round required')
    c.input_reads+=n
    cols=[[x[b*m+t]%P for b in range(k)] for t in range(m)]
    f0,lam,tab=learn_eigenvalues(cols,n,c)
    if f0 is None:
        return (None,{"accepted":False,"reason":"clean first transition impossible"},c) if return_certificate else None
    innovations=recover_spectral_innovations(cols,lam,tab,max_modes_per_step,c)
    if innovations is None:
        return (None,{"accepted":False,"reason":"spectral sparse decoder failed"},c) if return_certificate else None
    if not verify_spectral_innovations(cols,lam,innovations,tab,m,c,rounds,rng):
        return (None,{"accepted":False,"reason":"independent recurrence fingerprint failed"},c) if return_certificate else None
    events_by_ell=[[] for _ in range(k)]
    for t,changes in enumerate(innovations):
        for ell,E in changes:
            length=m-1-t
            # rho(ell,j) = lambda_ell*z(ell,0)*omega_M^(-j).
            # For a fixed event, generate all M rho^length values by one
            # initial exponentiation and a geometric walk: O(M) per event.
            rho0=mul(lam[ell],tab[(-ell)%n],c)
            power=pow(rho0,length,P)
            c.mults+=2*max(1,length.bit_length())
            ratio=tab[(-k*length)%n]
            powers=[]
            for j in range(m):
                powers.append(power)
                power=mul(power,ratio,c)
            events_by_ell[ell].append((t,E,powers))
    # One output sweep + O(#events * M) exact correction work.
    answer=[0]*n
    nonsingular=[];indices=[];singular=[]
    for ell in range(k):
        eigenpower=1
        for _ in range(m):eigenpower=mul(eigenpower,lam[ell],c)
        # rho^M = lambda^M * omega_K^(-ell), independent of j.
        base_num=mul(f0[ell],add(1,-mul(eigenpower,tab[(-ell*m)%n],c),c),c)
        for j in range(m):
            index=ell+j*k
            z=tab[(-index)%n]
            rho=mul(lam[ell],z,c)
            den=add(1,-rho,c)
            if den:
                # stage all N reciprocal denominators for one batch inversion
                numer=base_num
                for t,E,powers in events_by_ell[ell]:
                    z_t=tab[(-index*(t+1))%n]
                    numer=add(numer,mul(mul(E,z_t,c),add(1,-powers[j],c),c),c)
                indices.append((index,numer));nonsingular.append(den)
            else:
                y=mul(m%P,f0[ell],c)
                for t,E,_ in events_by_ell[ell]:
                    y=add(y,mul(mul(E,tab[(-index*(t+1))%n],c),(m-1-t)%P,c),c)
                singular.append((index,y))
    for inverse,(index,num) in zip(batch_inverse_nonzero(nonsingular,c),indices):
        answer[index]=mul(num,inverse,c)
    for index,y in singular:answer[index]=y
    cert={"accepted":True,"n":n,"k":k,"m":m,"mode":"dual-spectral-innovation",
          "max_modes_per_step":max_modes_per_step,
          "total_innovation_modes":sum(map(len,innovations)),
          "error_vectors_dense_in_position_domain":True,
          "freivalds_rounds":rounds,"false_acceptance_upper_bound":f"{P}^-{rounds}",
          "counted_ops":c.total(),"counts":c.as_dict(),
          "detected_innovations":innovations}
    return (answer,cert,c) if return_certificate else answer


def make_spectral_cycle(k:int,m:int,innovations:dict[int,list[tuple[int,int]]],seed=0,
                        lam_override=None):
    rng=random.Random(seed);n=k*m
    if n&(n-1) or k<m or (P-1)%n:raise ValueError
    wn=root_of_unity(n);wk=pow(wn,m,P);wk_inv=pow(wk,P-2,P)
    v0=[rng.randrange(1,P) for _ in range(k)]
    f0=exact_ntt(v0,wk_inv)
    if any(a==0 for a in f0):raise AssertionError
    lam=[rng.randrange(1,P) for _ in range(k)] if lam_override is None else list(lam_override)
    spectrum=f0[:];cols=[v0]
    for t in range(m-1):
        spectrum=[lam[ell]*spectrum[ell]%P for ell in range(k)]
        for ell,E in innovations.get(t,[]):
            spectrum[ell]=(spectrum[ell]+E)%P
        cols.append(ntt_inverse(spectrum,wk_inv))
    x=[cols[t][b] for b in range(k) for t in range(m)]
    kernel=ntt_inverse(lam,wk)
    return x,{"lambda":lam,"kernel":kernel,"innovations":innovations}
