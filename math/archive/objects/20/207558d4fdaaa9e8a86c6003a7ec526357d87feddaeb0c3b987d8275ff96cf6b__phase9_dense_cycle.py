#!/usr/bin/env python3
"""Hero #0 Phase 9: learned *dense* circulant evolution plus sparse innovations.

Contract
--------
For N=K*M (radix two), x[b*M+t] = v_t[b].  Learn a K-by-K
circulant C from clean first transition v1=C v0.  Subsequent transitions:
    v_{t+1}=C v_t+e_t, t=1,..,M-2,
where every innovation e_t has at most s nonzero coordinates.

Learn C's full K-coordinate eigenvalue vector with two K-NTTs, O(K log K),
recover each e_t from 2s Fourier syndromes (Prony/Berlekamp--Massey),
then evaluate all N outputs using M-point FFTs in O(N(log M+s)).
If total errors E is bounded, direct geometric corrections avoid the M FFTs:
O(N(s+E)+K log K).

Membership is checked with R independent *random* Freivalds vectors at
O(R(N+K log K)); false acceptance probability <= p^-R under uniform random
vectors independent of input (unless an independent deterministic full check
is selected).  The transform is mathematically exact on the promised class.
Generic inputs may be rejected and fall back to NTT => worst-case N log N.

Finite field prime p=2013265921 for executable certificates only. It admits
powers of two <=2^27. Asymptotic theorem assumes a compatible sequence of
fields or ideal exact complex arithmetic, not constant-size field for all N.
"""
from __future__ import annotations
import random
import secrets
from typing import Optional
from phase8_weyl_cycle import (P, G, Costs, exact_ntt, roots,
                               batch_inverse_nonzero, add, mul, inv)
from phase6_exact import root_of_unity


def ntt_inverse(values, root, c: Optional[Costs]=None):
    n=len(values)
    reverse_root=pow(root,P-2,P)
    z=exact_ntt(list(values), reverse_root,c)
    inverse_n=inv(n,c)
    return [mul(e,inverse_n,c) for e in z]


def learn_eigenvalues(cols, n:int, c: Costs):
    """Assume first transition has no innovation: F(v1)=lambda*F(v0)."""
    k=len(cols[0]);m=len(cols)
    table=roots(n,c)
    wk=table[m]
    wk_inv=table[-m]
    f0=exact_ntt(cols[0],wk_inv,c)
    f1=exact_ntt(cols[1],wk_inv,c)
    lam=[0]*k
    positions=[];denominators=[]
    for ell,(a,b) in enumerate(zip(f0,f1)):
        c.zero_tests+=1
        if not a:
            if b:return None,None,table
            lam[ell]=0  # convention for unobservable zero seed mode
        else:
            positions.append(ell);denominators.append(a)
    reciprocals=batch_inverse_nonzero(denominators,c)
    for ell,reciprocal in zip(positions,reciprocals):
        lam[ell]=mul(f1[ell],reciprocal,c)
    return f0,lam,table


def berlekamp_massey(seq: list[int], c:Optional[Costs]=None)->list[int]:
    """C=[1,C1,...,CL], satisfying seq[n]+sum(Ci seq[n-i])=0."""
    cur=[1];old=[1]
    length=0;gap=1;previous=1
    for n in range(len(seq)):
        discrepancy=seq[n]
        for i in range(1,length+1):
            discrepancy=add(discrepancy,mul(cur[i],seq[n-i],c),c)
        if not discrepancy:
            gap+=1
            continue
        scale=mul(discrepancy,inv(previous,c),c)
        before=cur[:]
        if len(cur)<len(old)+gap:
            cur.extend([0]*(len(old)+gap-len(cur)))
        for j,x in enumerate(old):
            cur[j+gap]=add(cur[j+gap],-mul(scale,x,c),c)
        if 2*length<=n:
            length=n+1-length
            old=before;previous=discrepancy;gap=1
        else:
            gap+=1
    return cur[:length+1]


def solve_amplitudes(nodes:list[int], syndromes:list[int],c:Optional[Costs]=None):
    """Small Vandermonde solve: sum_j amp[j] node[j]^ell = syndrome[ell]."""
    s=len(nodes)
    if s==0:return []
    matrix=[]
    powers=[1]*s
    for ell in range(s):
        matrix.append(powers[:]+[syndromes[ell]])
        powers=[mul(v,x,c) for v,x in zip(powers,nodes)]
    for i in range(s):
        pivot=next((j for j in range(i,s) if matrix[j][i]),None)
        if pivot is None:return None
        matrix[i],matrix[pivot]=matrix[pivot],matrix[i]
        factor=inv(matrix[i][i],c)
        for j in range(i,s+1):matrix[i][j]=mul(matrix[i][j],factor,c)
        for row in range(s):
            if row==i:continue
            factor=matrix[row][i]
            if factor:
                for j in range(i,s+1):
                    matrix[row][j]=add(matrix[row][j],-mul(factor,matrix[i][j],c),c)
    return [r[s] for r in matrix]


def decode_sparse_syndromes(syndromes:list[int],k:int,root_neg:int,
                            max_errors:int,c:Optional[Costs]=None):
    """Exact recovery when residual has <=s spikes, using 2s syndromes.

    If the residual is denser, candidate may alias; Freivalds subsequently
    certifies all transitions with random vectors.  Never use a syndrome
    match alone to assert exact membership on arbitrary inputs.
    """
    if max_errors==0:return [] if all(v==0 for v in syndromes) else None
    polynomial=berlekamp_massey(syndromes,c)
    s=len(polynomial)-1
    if s>max_errors:return None
    if not s:
        return [] if all(v==0 for v in syndromes) else None
    nodes=[];positions=[]
    node=1
    for b in range(k):
        # z^s+C1 z^(s-1)+...+Cs = 0 for each exponential node
        h=1
        for coeff in polynomial[1:]:h=add(mul(h,node,c),coeff,c)
        if h==0:
            nodes.append(node);positions.append(b)
            if len(nodes)>s:return None
        node=mul(node,root_neg,c)
    if len(nodes)!=s:return None
    amps=solve_amplitudes(nodes,syndromes,c)
    if amps is None:return None
    for ell,val in enumerate(syndromes):
        prediction=0
        for node,amp in zip(nodes,amps):
            # s only polylog; repeated pow here has log s exponent not log K
            prediction=add(prediction,mul(amp,pow(node,ell,P),c),c)
            if c:c.mults+=2*max(1,ell.bit_length())
        if prediction!=val:return None
    return [(b,a) for b,a in zip(positions,amps) if a]


def find_innovations(cols,lam,table,max_errors:int,c:Costs):
    m=len(cols);k=len(cols[0]);n=k*m
    if max_errors==0:
        return [[] for _ in range(m-1)]
    if 2*max_errors>k:raise ValueError('require 2s<=K')
    # Sample Fourier coefficients 0,...,2s-1 of every column, O(s*N).
    probes=2*max_errors
    samples=[[0]*probes for _ in range(m)]
    for t in range(m):
        for ell in range(probes):
            acc=0
            for b in range(k):
                acc=add(acc,mul(cols[t][b],table[(-m*ell*b)%n],c),c)
            samples[t][ell]=acc
    innovations=[[] for _ in range(m-1)]
    for t in range(1,m-1):
        syndrome=[add(samples[t+1][ell],-mul(lam[ell],samples[t][ell],c),c)
                  for ell in range(probes)]
        result=decode_sparse_syndromes(syndrome,k,table[-m],max_errors,c)
        if result is None:return None
        innovations[t]=result
    return innovations


def apply_transpose_circulant_to_row(w,lam,tab,m,c:Costs):
    """phi=C^T w via 2 K-NTTs; C v has eigenvalues lam[ell]."""
    k=len(w);wk=tab[m];wk_inv=tab[-m]
    fw=exact_ntt(w,wk_inv,c)
    fphi=[mul(fw[ell],lam[-ell%k],c) for ell in range(k)]
    return ntt_inverse(fphi,wk_inv,c)


def probabilistic_verify(cols,lam,innovations,tab,m,c:Costs,rounds=3,rng=None):
    """Freivalds certificate. For false candidates Pr[accept] <= p^(-rounds).

    The theorem needs independent truly uniform finite-field w vectors chosen
    AFTER learned lambda and innovations have been fixed.  Default SystemRandom
    uses OS randomness; deterministic seeded RNG is only for reproducible tests.
    """
    if rng is None:rng=secrets.SystemRandom()
    k=len(cols[0])
    for trial in range(rounds):
        w=[rng.randrange(P) for _ in range(k)]
        phi=apply_transpose_circulant_to_row(w,lam,tab,m,c)
        for t in range(m-1):
            lhs=rhs=0
            for b in range(k):
                lhs=add(lhs,mul(w[b],cols[t+1][b],c),c)
                rhs=add(rhs,mul(phi[b],cols[t][b],c),c)
            for b,a in innovations[t]:
                rhs=add(rhs,mul(w[b],a,c),c)
            if lhs!=rhs:return False
    return True


def exact_dense_cycle_with_innovations(x:list[int],m:int,max_errors_per_step:int,
             global_fast_limit:Optional[int]=3,verification_rounds:int=3,
             counter:Optional[Costs]=None,rng=None,return_certificate:bool=False):
    """Recover full transform on certified sparse-innovation dense cycles.

    If total innovations E<=global_fast_limit, O((s+E)N+KlogK).
    Otherwise O(N(s+log M)+KlogK). Input-dependent division is counted.
    Returns None if membership test rejects. For generic inputs, probability
    of a false accept is at most P^-verification_rounds under true randomness.
    """
    c=counter or Costs();n=len(x)
    if m<2 or n%m or n&(n-1) or m&(m-1):raise ValueError('N,K,M radix two')
    k=n//m
    if k<m or k&(k-1):raise ValueError('K>=M radix two')
    if (P-1)%n:raise ValueError('field lacks root')
    if max_errors_per_step<0:raise ValueError
    if verification_rounds<1:raise ValueError('at least one Freivalds round is required')
    c.input_reads+=n
    cols=[[x[b*m+t]%P for b in range(k)] for t in range(m)]
    f0,lam,tab=learn_eigenvalues(cols,n,c)
    if f0 is None:
        return (None,{"accepted":False,"reason":"clean first transition impossible"},c) if return_certificate else None
    innovations=find_innovations(cols,lam,tab,max_errors_per_step,c)
    if innovations is None:
        return (None,{"accepted":False,"reason":"sparse syndrome decoding failed"},c) if return_certificate else None
    if not probabilistic_verify(cols,lam,innovations,tab,m,c,verification_rounds,rng):
        return (None,{"accepted":False,"reason":"independent recurrence fingerprint failed"},c) if return_certificate else None
    total=sum(map(len,innovations))
    choose_direct=(global_fast_limit is not None and total<=global_fast_limit)
    w_m_inv=tab[-k]
    # All lambda powers in O(N), shared by both evaluators.
    lam_powers=[]
    for ell in range(k):
        pw=[1]
        for t in range(m):pw.append(mul(pw[-1],lam[ell],c))
        lam_powers.append(pw)
    base_num=[]
    for ell in range(k):
        base_num.append(mul(f0[ell],add(1,-mul(lam_powers[ell][m],tab[(-ell*m)%n],c),c),c))
    # Sparse event mode: direct sum, no length-M FFT needed.
    events=[(t,b,a) for t,row in enumerate(innovations) for b,a in row]
    coeffs=None; boundary=None
    if not choose_direct:
        # Compute all E_t(ell) with O(s*N) direct sparse Fourier sums.
        E=[[0]*k for _ in range(m-1)]
        for t,row in enumerate(innovations):
            for ell in range(k):
                y=0
                for b,a in row:
                    y=add(y,mul(a,tab[(-m*ell*b)%n],c),c)
                E[t][ell]=y
        # B_ell = sum_t lambda_ell^(M-1-t)*E_t(ell)
        boundary=[0]*k
        for ell in range(k):
            y=0
            for t in range(m-1):
                y=add(y,mul(E[t][ell],lam_powers[ell][m-1-t],c),c)
            boundary[ell]=y
        # H_ell(z_j) = sum_t E_t(ell) z_j^t.
        # z_j=omega_N^(-ell) omega_M^(-j): length-M FFT per ell.
        coeffs=[]
        for ell in range(k):
            coef=[0]*m
            for t in range(m-1):coef[t]=mul(E[t][ell],tab[(-ell*t)%n],c)
            coeffs.append(exact_ntt(coef,w_m_inv,c))
    # Prepare all denominators, invert in a single batch.
    nonsingular=[];position=[];answer=[0]*n; singular=[]
    for ell in range(k):
        for j in range(m):
            index=ell+j*k
            z=tab[-index%n]
            rho=mul(lam[ell],z,c)
            den=add(1,-rho,c)
            if den:
                nonsingular.append(den);position.append((index,ell,j,z))
            else:singular.append((index,ell,j,z))
    inverses=batch_inverse_nonzero(nonsingular,c)
    def numerator_value(index,ell,j,z):
        if choose_direct:
            numer=base_num[ell]
            for t,b,a in events:
                ehat=mul(a,tab[(-m*ell*b)%n],c)
                exponent=t+1;L=m-exponent
                geometric=add(1,-mul(lam_powers[ell][L],tab[(-index*L)%n],c),c)
                zpow=tab[(-index*exponent)%n]
                numer=add(numer,mul(mul(ehat,zpow,c),geometric,c),c)
            return numer
        zh=mul(z,coeffs[ell][j],c)
        z_m=tab[(-index*m)%n]
        return add(add(base_num[ell],zh,c),-mul(z_m,boundary[ell],c),c)
    for reciprocal,(index,ell,j,z) in zip(inverses,position):
        answer[index]=mul(numerator_value(index,ell,j,z),reciprocal,c)
    for index,ell,j,z in singular:
        value=mul(m%P,f0[ell],c)
        # limit of (1-rho^L)/(1-rho) as rho -> 1 is L
        for t,row in enumerate(innovations):
            if not row:continue
            ehat=0
            for b,a in row:
                ehat=add(ehat,mul(a,tab[(-m*ell*b)%n],c),c)
            power=tab[(-index*(t+1))%n]
            value=add(value,mul(mul(ehat,power,c),(m-t-1)%P,c),c)
        answer[index]=value
    cert={"accepted":True,"n":n,"k":k,"m":m,"innovation_total":total,
          "innovation_max_per_step":max(map(len,innovations),default=0),
          "mode":"direct-geometric" if choose_direct else "batched-small-NTT",
          "verification_rounds":verification_rounds,"false_acceptance_bound":f"{P}^-{verification_rounds}",
          "lambda_nonzero":sum(v!=0 for v in lam),"counted_ops":c.total(),
          "counts":c.as_dict(),"detected_innovations":innovations}
    return (answer,cert,c) if return_certificate else answer


def make_dense_cycle(k:int,m:int,innovations:dict[int,list[tuple[int,int]]],seed:int=0,lam_override=None):
    """Independent test-only generator; DFT/IDFT each column is *not* online work."""
    rng=random.Random(seed)
    n=k*m
    if k<m or n&(n-1) or (P-1)%n:raise ValueError
    wn=root_of_unity(n)
    wk=pow(wn,m,P);wk_inv=pow(wk,P-2,P)
    v0=[rng.randrange(1,P) for _ in range(k)]
    f0=exact_ntt(v0,wk_inv)
    if any(v==0 for v in f0):raise AssertionError('rare seed with zero Fourier entry')
    lam=[rng.randrange(1,P) for _ in range(k)] if lam_override is None else list(lam_override)
    assert len(lam)==k
    # Arbitrary dense circulant kernel obtained from inverse transform of lambda.
    cinv=pow(k,P-2,P)
    c=[a*cinv%P for a in exact_ntt(lam,wk_inv)]
    spectra=[f0]
    cols=[v0]
    for t in range(m-1):
        fnext=[lam[ell]*spectra[-1][ell]%P for ell in range(k)]
        for b,amplitude in innovations.get(t,[]):
            for ell in range(k):
                fnext[ell]=(fnext[ell]+amplitude*pow(wk,(-ell*b)%k,P))%P
        spectra.append(fnext)
        cols.append([z*cinv%P for z in exact_ntt(fnext,wk)])
    x=[cols[t][b] for b in range(k) for t in range(m)]
    return x,{"v0":v0,"lambda":lam,"kernel_c":c,"innovations":innovations}


def exact_reference_dft(x:list[int]):
    wn=root_of_unity(len(x))
    return exact_ntt(x,pow(wn,P-2,P))
