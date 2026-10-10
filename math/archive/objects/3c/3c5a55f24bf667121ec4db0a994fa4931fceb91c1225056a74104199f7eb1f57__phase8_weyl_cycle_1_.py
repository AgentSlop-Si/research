#!/usr/bin/env python3
"""Hero #0 Phase 8: exact certified dynamical FFT families.

Length N = K*M, both powers of two and K>=M. All field operations
are mod 2013265921 for reproducible NTT tests, with a source-input
certificate required before any specialized execution.

THEOREM A: A fixed-width UNKNOWN circulant time-evolution operator
  v_{t+1} = sum_d c_d S^{shift_d} v_t,  (Sv)[b]=v[b+1]
can be *detected* in O(s^2 N) and *executed* by a single length K NTT
plus N rational/geometric outputs and ONE batched inversion.
For s constant and M=Theta(log N), time O(N). All inputs of this
certified family are exact, not generic-input FFT.

THEOREM B: arbitrary unknown time-varying coefficients for s fixed
noncommuting Weyl generators W_pq v[b] = wk^(q*b) v[b+p]
can be detected in O(s^2 N), propagated in Fourier space O(sN), then
completed with K length-M NTTs: O(N(s^2+log M)+K log K).

Both algorithms verify the *entire raw input*. If the certificate fails,
they return None (callers may choose an ordinary full NTT fallback).
The scalar arithmetic model counts data-dependent field inversions,
zero tests and branching, and is not a restricted linear circuit model.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Sequence
import random
from phase6_exact import P, G, root_of_unity

@dataclass
class Costs:
    adds:int=0
    mults:int=0
    zero_tests:int=0
    inversions:int=0
    inversion_mult_bound:int=0
    ntt_butterflies:int=0
    input_reads:int=0
    def total(self)->int:
        return self.adds+self.mults+self.inversion_mult_bound+self.zero_tests
    def as_dict(self):return vars(self).copy()


def add(x:int,y:int,c:Optional[Costs])->int:
    if c:c.adds+=1
    return (x+y)%P

def mul(x:int,y:int,c:Optional[Costs])->int:
    if c:c.mults+=1
    return x*y%P

def inv(x:int,c:Optional[Costs])->int:
    if x%P==0:raise ZeroDivisionError("attempt to invert zero")
    if c:
        c.inversions+=1
        c.inversion_mult_bound+=2*P.bit_length()
    return pow(x,P-2,P)

def roots(n:int,c:Optional[Costs]):
    w=root_of_unity(n)
    table=[1]*n
    for j in range(1,n):table[j]=mul(table[j-1],w,c)
    return table

def exact_ntt(a:list[int], root:int, c:Optional[Costs]=None)->list[int]:
    n=len(a)
    if not n or n&(n-1):raise ValueError("power-of-two transform length needed")
    data=a[:]
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:j^=bit;bit>>=1
        j^=bit
        if i<j:data[i],data[j]=data[j],data[i]
    length=2
    while length<=n:
        step=pow(root,n//length,P)
        # Bound generation by binary exponentiation (root independent of data).
        if c:c.mults+=2*P.bit_length()
        for offset in range(0,n,length):
            phase=1
            for j in range(length//2):
                u=data[offset+j]
                v=mul(data[offset+j+length//2],phase,c)
                data[offset+j]=add(u,v,c)
                data[offset+j+length//2]=add(u,-v,c)
                phase=mul(phase,step,c)
                if c:c.ntt_butterflies+=1
        length*=2
    return data

def to_columns(x:Sequence[int],m:int,c:Optional[Costs]=None)->list[list[int]]:
    n=len(x)
    if n%m:raise ValueError("N must be divisible by M")
    k=n//m
    if k<m or k&(k-1) or m&(m-1):
        raise ValueError("K and M must be radix two, K>=M")
    if (P-1)%n:raise ValueError("NTT field lacks Nth root")
    if c:c.input_reads+=n
    return [[x[b*m+t]%P for b in range(k)] for t in range(m)]

def solve_coeffs(equations, s:int, c:Optional[Costs]=None)->Optional[list[int]]:
    """Streaming fraction-field echelon solver; *all* equations charged.

    Equations yield (features with s entries, target). No solution -> None.
    Underdetermined -> zero for free variables, valid verified solution.
    """
    basis={}
    for feat,target in equations:
        row=[z%P for z in feat]+[target%P]
        for p,h in sorted(basis.items()):
            z=row[p]
            if c:c.zero_tests+=1
            if z:
                for j in range(p,s+1):row[j]=add(row[j],-mul(z,h[j],c),c)
        pivot=None
        for j in range(s):
            if c:c.zero_tests+=1
            if row[j]:pivot=j;break
        if pivot is None:
            if c:c.zero_tests+=1
            if row[s]!=0:return None
            continue
        back=inv(row[pivot],c)
        basis[pivot]=[mul(z,back,c) for z in row]
    result=[0]*s
    for p in sorted(basis.keys(),reverse=True):
        h=basis[p]
        v=h[s]
        for j in range(p+1,s):v=add(v,-mul(h[j],result[j],c),c)
        result[p]=v
    return result

def batch_inverse_nonzero(denoms:Sequence[int],c:Optional[Costs])->list[int]:
    """One field inversion, O(len(denoms)) multiplications."""
    n=len(denoms)
    if n==0:return []
    prefix=[1]*(n+1)
    for i,d in enumerate(denoms):
        if c:c.zero_tests+=1
        if not d:raise ZeroDivisionError
        prefix[i+1]=mul(prefix[i],d,c)
    backward=inv(prefix[n],c)
    result=[0]*n
    for i in range(n-1,-1,-1):
        result[i]=mul(prefix[i],backward,c)
        backward=mul(backward,denoms[i],c)
    return result

def cyclic_linear_synthesize(seed:Sequence[int],m:int,taps:Sequence[int],shifts:Sequence[int])->list[int]:
    """Generate *new* fresh input belonging to a particular certified family."""
    k=len(seed)
    if len(taps)!=len(shifts):raise ValueError
    cols=[[v%P for v in seed]]
    for t in range(1,m):
        prev=cols[-1]
        cols.append([sum(tap*prev[(b+j)%k] for tap,j in zip(taps,shifts))%P for b in range(k)])
    return [cols[t][b] for b in range(k) for t in range(m)]

def exact_circulant_cycle(x:Sequence[int],m:int,shifts:Sequence[int]=(0,1),
                           c:Optional[Costs]=None,return_certificate:bool=False):
    """Unknown constant circulant dynamics -> full exact Fourier outputs in O(N).

    When certification fails, output None without running the special decoder.
    The fallback FFT may be requested by the caller but is not hidden here.
    """
    c=c if c is not None else Costs()
    cols=to_columns(x,m,c)
    k=len(cols[0]);n=k*m
    s=len(shifts)
    if s<1:raise ValueError
    shifts=[j%k for j in shifts]
    def eqs():
        for t in range(m-1):
            row=cols[t];nextrow=cols[t+1]
            for b in range(k):
                yield [row[(b+d)%k] for d in shifts],nextrow[b]
    taps=solve_coeffs(eqs(),s,c)
    if taps is None:
        if return_certificate:return None,{"accepted":False,"reason":"not a shared circulant recurrence"},c
        return None
    # Full second pass with independent reconstruction to defend against
    # mistakes in the elimination certificate.
    for t in range(m-1):
        for b in range(k):
            expected=0
            for j,tap in zip(shifts,taps):
                expected=add(expected,mul(tap,cols[t][(b+j)%k],c),c)
            if c:c.zero_tests+=1
            if expected!=cols[t+1][b]:
                raise AssertionError("solver admitted an incorrect coefficient vector")
    tab=roots(n,c); w_k=tab[m]
    F0=exact_ntt(cols[0],pow(w_k,P-2,P),c)
    # For S^d v[b]=v[b+d], Fourier eigenvalue = omega_K^(ell*d).
    eigen=[]
    for ell in range(k):
        lam=0
        for tap,d in zip(taps,shifts):
            lam=add(lam,mul(tap,tab[(m*ell*d)%n],c),c)
        eigen.append(lam)
    # All numerator values reused for the M output bins in each class.
    numerator=[]
    for ell in range(k):
        lam_m=1
        for _ in range(m):lam_m=mul(lam_m,eigen[ell],c)
        num=add(1,-mul(lam_m,tab[(-m*ell)%n],c),c)
        numerator.append(mul(F0[ell],num,c))
    # For zero denominators, the rational geometric formula is replaced by M.
    nonsingular=[];rlist=[];answer=[0]*n
    for ell in range(k):
        for j in range(m):
            index=ell+j*k
            r=mul(eigen[ell],tab[(-index)%n],c)
            den=add(1,-r,c)
            if c:c.zero_tests+=1
            if den==0:
                answer[index]=mul(m%P,F0[ell],c)
            else:
                nonsingular.append(den)
                rlist.append((index,ell))
    for reciprocal,(index,ell) in zip(batch_inverse_nonzero(nonsingular,c),rlist):
        answer[index]=mul(numerator[ell],reciprocal,c)
    cert={"accepted":True,"taps":taps,"shifts":shifts,"k":k,"m":m,
          "phase_slots":n,"field":P,"inversions":c.inversions}
    return (answer,cert,c) if return_certificate else answer

def exact_unknown_shift_cycle(x:Sequence[int],m:int,c:Optional[Costs]=None,
                              return_certificate:bool=False):
    """Infer both unknown taps and unknown shift d in O(N), then certify.

    For generic identifiable seeds: F_0[0:3] all nonzero, c1!=0,
    1<=d<K. Then lambda_ell=F_1[ell]/F_0[ell]=c0+c1*wk^(ell*d),
    so (lambda_2-lambda_1)/(lambda_1-lambda_0) = wk^d.
    Identify d by K linear successive root multiplies. The whole raw
    input then undergoes independent exact recurrence certification.

    Degenerate/underspecified seeds return None (or the scalar dynamics
    branch); no claim that every valid two-tap family is identifiable.
    """
    c=c if c is not None else Costs()
    cols=to_columns(x,m,c)
    k=len(cols[0]);n=k*m
    if m<2:
        got,cert,c=exact_circulant_cycle(x,m,(0,),c,True)
        if return_certificate:return got,cert,c
        return got
    tab=roots(n,c);wk=tab[m]
    # Three direct Fourier dots cost O(K), not a second K-FFT.
    f0=[];f1=[]
    for ell in range(3):
        a0=a1=0
        for b in range(k):
            phase=tab[(-m*ell*b)%n]
            a0=add(a0,mul(cols[0][b],phase,c),c)
            a1=add(a1,mul(cols[1][b],phase,c),c)
        f0.append(a0);f1.append(a1)
    if all(f0):
        lam=[mul(f1[j],inv(f0[j],c),c) for j in range(3)]
        dif0=add(lam[1],-lam[0],c)
        dif1=add(lam[2],-lam[1],c)
        if dif0:
            ratio=mul(dif1,inv(dif0,c),c)
            current=1;d=None
            for j in range(k):
                if c:c.zero_tests+=1
                if current==ratio:
                    d=j;break
                current=mul(current,wk,c)
            if d is not None and d>0:
                got,cert,c=exact_circulant_cycle(x,m,(0,d),c,True)
                cert['inferred_shift']=d
                cert['spectral_ratio_identity']=True
                if return_certificate:return got,cert,c
                return got
        # Only branch needing scalar dynamics: two taps at d=0 or c1=0.
        if lam[0]==lam[1]==lam[2]:
            got,cert,c=exact_circulant_cycle(x,m,(0,),c,True)
            cert['inferred_shift']=0
            if return_certificate:return got,cert,c
            return got
    cert={"accepted":False,"reason":"not identifiable from first three frequencies"}
    if return_certificate:return None,cert,c
    return None

def synthesize_circulant_order(initial:Sequence[Sequence[int]], m:int,
                                taps_by_lag:Sequence[Sequence[int]],
                                shifts:Sequence[int])->list[int]:
    """Order-r recurrence: v_t = sum_{j=1}^r sum_d c_{j,d} S^d v_{t-j}."""
    r=len(taps_by_lag)
    if r<1 or len(initial)!=r or m<r:raise ValueError
    k=len(initial[0]);s=len(shifts)
    if not all(len(col)==k for col in initial):raise ValueError
    if not all(len(co)==s for co in taps_by_lag):raise ValueError
    cols=[[z%P for z in v] for v in initial]
    for t in range(r,m):
        nxt=[]
        for b in range(k):
            nxt.append(sum(taps_by_lag[j-1][i]*cols[t-j][(b+d)%k]
                           for j in range(1,r+1) for i,d in enumerate(shifts))%P)
        cols.append(nxt)
    return [cols[t][b] for b in range(k) for t in range(m)]


def exact_circulant_rational_cycle(x:Sequence[int],m:int,r:int,
                                    shifts:Sequence[int]=(0,1),
                                    c:Optional[Costs]=None,return_certificate:bool=False):
    """Certify order-r circulant time recurrence; evaluate full exact NTT.

    All coefficients unknown, finite fixed r,s and M=Theta(log N): O(N).
    The local M-FFT is eliminated by rational generating-function eval.
    There are at most r exceptional denominator roots per each ell,
    so direct O(M) summation of exceptional outputs also costs O(r*N).
    """
    c=c if c is not None else Costs()
    cols=to_columns(x,m,c)
    k=len(cols[0]);n=k*m
    s=len(shifts)
    if r<1 or r>m or s<1:raise ValueError
    shifts=[d%k for d in shifts]
    unknowns=r*s
    def eqs():
        for t in range(r,m):
            for b in range(k):
                yield [cols[t-j][(b+d)%k]
                       for j in range(1,r+1) for d in shifts],cols[t][b]
    controls=solve_coeffs(eqs(),unknowns,c)
    if controls is None:
        if return_certificate:return None,{"accepted":False,"reason":"not a fixed circulant recurrence"},c
        return None
    for t in range(r,m):
        for b in range(k):
            expected=0
            for j in range(1,r+1):
                for i,d in enumerate(shifts):
                    expected=add(expected,mul(controls[(j-1)*s+i],cols[t-j][(b+d)%k],c),c)
            if c:c.zero_tests+=1
            if expected!=cols[t][b]:raise AssertionError('invalid rational recurrence certificate')
    tab=roots(n,c);wk=tab[m]
    init_spectra=[exact_ntt(cols[j],pow(wk,P-2,P),c) for j in range(r)]
    result=[0]*n
    # All regular denominators are inverted in a single shared batch.
    denominators=[];target_index=[];numerators=[]
    singular_count=0
    for ell in range(k):
        b_lags=[]
        for j in range(r):
            v=0
            for i,d in enumerate(shifts):
                v=add(v,mul(controls[j*s+i],tab[(m*ell*d)%n],c),c)
            b_lags.append(v)
        # After the r initial Fourier values, generate just the scalar
        # recurrence sequence for this ell, in O(r*M) operations.
        seq=[init_spectra[j][ell] for j in range(r)]
        for t in range(r,m):
            v=0
            for j in range(1,r+1):
                v=add(v,mul(b_lags[j-1],seq[t-j],c),c)
            seq.append(v)
        front=[];back=[]
        for h in range(r):
            front_h=seq[h]
            for j in range(1,h+1):
                front_h=add(front_h,-mul(b_lags[j-1],seq[h-j],c),c)
            front.append(front_h)
            back_h=0
            for j in range(h+1,r+1):
                back_h=add(back_h,-mul(b_lags[j-1],seq[m+h-j],c),c)
            back.append(back_h)
        zpower_m=tab[(-m*ell)%n]
        for j in range(m):
            ind=ell+j*k
            z=tab[(-ind)%n]
            zpower=1
            numer=0;denom=1
            for h in range(r):
                term=add(front[h],mul(zpower_m,back[h],c),c)
                numer=add(numer,mul(term,zpower,c),c)
                zpower=mul(zpower,z,c)
                denom=add(denom,-mul(b_lags[h],zpower,c),c)
            if c:c.zero_tests+=1
            if denom==0:
                singular_count+=1
                # Direct polynomial value at an isolated pole, never 0/0.
                v=0;powz=1
                for term in seq:
                    v=add(v,mul(term,powz,c),c)
                    powz=mul(powz,z,c)
                result[ind]=v
            else:
                denominators.append(denom)
                numerators.append(numer)
                target_index.append(ind)
    for out,top,bot in zip(target_index,numerators,batch_inverse_nonzero(denominators,c)):
        result[out]=mul(top,bot,c)
    cert={"accepted":True,"order":r,"shifts":shifts,
          "coefficients_by_lag":[controls[j*s:(j+1)*s] for j in range(r)],
          "singular_outputs":singular_count,"k":k,"m":m,"field":P}
    return (result,cert,c) if return_certificate else result

def synthesize_time_weyl(seed:Sequence[int],m:int,dictionary:Sequence[tuple[int,int]],
                          controls:Sequence[Sequence[int]],omega_k:int)->list[int]:
    k=len(seed)
    if len(controls)!=m-1:raise ValueError
    cols=[[v%P for v in seed]]
    phase=[[pow(omega_k,(q*b)%k,P) for b in range(k)] for _,q in dictionary]
    for co in controls:
        if len(co)!=len(dictionary):raise ValueError
        prev=cols[-1]
        nxt=[]
        for b in range(k):
            nxt.append(sum(ci*phase[i][b]*prev[(b+pq[0])%k]
                           for i,(ci,pq) in enumerate(zip(co,dictionary)))%P)
        cols.append(nxt)
    return [cols[t][b] for b in range(k) for t in range(m)]

def exact_weyl_dynamic(x:Sequence[int],m:int,
                       dictionary:Sequence[tuple[int,int]]=((1,0),(0,1)),
                       c:Optional[Costs]=None,return_certificate:bool=False):
    """Certified time-dependent noncommuting Weyl dynamics.

    Uses one K transform + (M-1) frequency-domain Weyl updates + K M-NTTs;
    complexity O(N(s^2+log M)+K log K) for s=number of dictionary ops.
    """
    c=c if c is not None else Costs()
    cols=to_columns(x,m,c)
    k=len(cols[0]);n=k*m
    dic=[(p%k,q%k) for p,q in dictionary]
    s=len(dic)
    if not s:raise ValueError
    tab=roots(n,c)
    phases=[[tab[(m*q*b)%n] for b in range(k)] for p,q in dic]
    coefficients=[]
    for t in range(m-1):
        def eqs():
            for b in range(k):
                yield [mul(phases[i][b],cols[t][(b+p)%k],c)
                       for i,(p,q) in enumerate(dic)],cols[t+1][b]
        sol=solve_coeffs(eqs(),s,c)
        if sol is None:
            if return_certificate:return None,{"accepted":False,"reason":"no Weyl control"},c
            return None
        coefficients.append(sol)
        for b in range(k):
            v=0
            for i,(p,q) in enumerate(dic):
                ph=phases[i][b]
                v=add(v,mul(sol[i],mul(ph,cols[t][(b+p)%k],c),c),c)
            if c:c.zero_tests+=1
            if v!=cols[t+1][b]:raise AssertionError("wrong Weyl coefficients")
    wk=tab[m];wm=tab[k]
    F=exact_ntt(cols[0],pow(wk,P-2,P),c)
    # Need one K-sized spectrum per t to form each M-frequency combination.
    spectrum=[F]
    for sol in coefficients:
        nxt=[0]*k
        for ell in range(k):
            v=0
            for (p,q),co in zip(dic,sol):
                # W_{p,q}v[b]=omega_K^(q b)v[b+p]
                # F(W_{p,q}v)[ell]=omega_K^((ell-q)*p) F(v)[ell-q].
                src=(ell-q)%k
                v=add(v,mul(co,mul(tab[(m*src*p)%n],F[src],c),c),c)
            nxt[ell]=v
        spectrum.append(nxt)
        F=nxt  # Critical: evolve the whole spectral state, not initial seed.
    answer=[0]*n
    for ell in range(k):
        h=[mul(spectrum[t][ell],tab[(-ell*t)%n],c) for t in range(m)]
        local=exact_ntt(h,pow(wm,P-2,P),c)
        for j in range(m):answer[ell+j*k]=local[j]
    cert={"accepted":True,"dictionary":dic,"controls":coefficients,
          "k":k,"m":m,"field":P}
    return (answer,cert,c) if return_certificate else answer

def full_ntt_oracle(x:Sequence[int],c:Optional[Costs]=None)->list[int]:
    return exact_ntt(list(x),pow(root_of_unity(len(x)),P-2,P),c)

def direct_dft_oracle(x:Sequence[int])->list[int]:
    n=len(x);tab=roots(n,None)
    return [sum(x[b]*tab[(-k*b)%n] for b in range(n))%P for k in range(n)]

if __name__=='__main__':
    import unittest
    unittest.main(module='test_phase8')
