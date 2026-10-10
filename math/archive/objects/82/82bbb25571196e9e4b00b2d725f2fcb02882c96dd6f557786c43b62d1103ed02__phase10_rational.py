#!/usr/bin/env python3
"""Hero #0 Phase 10: exact FFT for certified order-d *spectral* recurrence families.

For N=K*M, columns v_t[b]=x[b*M+t], frequency streams
F_t[ell]=DFT_K(v_t)[ell] have an UNKNOWN frequency-dependent recurrence
  F_t[ell] + sum_{i=1}^d q_i[ell]*F_{t-i}[ell] = 0.
Each of d arbitrary circulant controllers may be fully dense, and first d
columns are arbitrary. Learn from 2d columns; check every raw column using
independent random-vector fingerprints; synthesize all N exact outputs using
truncated generating-function numerator/denominator polynomials.

With M=Theta(log N), compatible exact scalar field and fixed rounds:
 O(d*N + d*d*K + N) operations, O(N) memory.  d=O(1) -> O(N),
 d=O(log log N) -> O(N log log N). CONDITIONED ON CERTIFICATE.
False accepts on nonpromised inputs <=p^-rounds. No universal faster FFT.
Fixed test prime P=2013265921 supports lengths up to 2^27 only.
"""
from __future__ import annotations
import dataclasses
import random
import secrets
from typing import Optional

P=2013265921
G=31

@dataclasses.dataclass
class Count:
    adds:int=0
    muls:int=0
    comparisons:int=0
    inversions:int=0
    input_reads:int=0
    output_writes:int=0
    butterflies:int=0
    def total(self):return self.adds+self.muls+self.comparisons+2*P.bit_length()*self.inversions
    def record(self):return dataclasses.asdict(self)|{'total':self.total()}


def add(a,b,c:Optional[Count]=None):
    if c:c.adds+=1
    return (a+b)%P

def mul(a,b,c:Optional[Count]=None):
    if c:c.muls+=1
    return (a*b)%P

def nonzero(a,c:Optional[Count]=None):
    if c:c.comparisons+=1
    return a%P != 0

def inv(a,c:Optional[Count]=None):
    if a%P==0:raise ZeroDivisionError
    if c:c.inversions+=1
    return pow(a,P-2,P)

def root_of_unity(n):
    if n<1 or n&(n-1) or (P-1)%n:
        raise ValueError('requires power-of-two n dividing P-1')
    return pow(G,(P-1)//n,P)

def root_table(n,c:Optional[Count]=None):
    w=root_of_unity(n)
    z=[1]*n
    for i in range(1,n):z[i]=mul(z[i-1],w,c)
    return z

def ntt(seq,negative=True,c:Optional[Count]=None):
    """Standalone radix-two modular FFT; forward uses negative powers."""
    n=len(seq)
    w=root_of_unity(n)
    if negative:w=pow(w,P-2,P)
    a=[x%P for x in seq]
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:
            j^=bit;bit>>=1
        j^=bit
        if i<j:a[i],a[j]=a[j],a[i]
    stride=2
    while stride<=n:
        base=pow(w,n//stride,P)
        if c:c.muls+=2*max(1,(n//stride).bit_length()) # charge scalar root preparation
        for start in range(0,n,stride):
            z=1
            for t in range(stride//2):
                u=a[start+t]
                v=mul(a[start+t+stride//2],z,c)
                a[start+t]=add(u,v,c)
                a[start+t+stride//2]=add(u,-v,c)
                z=mul(z,base,c)
                if c:c.butterflies+=1
        stride*=2
    if not negative:
        ninv=inv(n,c)
        a=[mul(v,ninv,c) for v in a]
    return a


def berlekamp_massey(s,c:Optional[Count]=None):
    """Shortest monic connection q for finite sequence: s_t+sum_i q_i*s_(t-i)=0.

    Algorithm yields a recurrence fitting *all* given 2d observations,
    potentially overfitting arbitrary data; the later random check is vital.
    """
    connection=[1]; previous=[1]
    L=0; m=1; b=1
    for n in range(len(s)):
        delta=s[n]
        for i in range(1,L+1):
            delta=add(delta,mul(connection[i],s[n-i],c),c)
        if not nonzero(delta,c):
            m+=1;continue
        correction=mul(delta,inv(b,c),c)
        old=connection[:]
        if len(connection)<len(previous)+m:
            connection.extend([0]*(len(previous)+m-len(connection)))
        for j,z in enumerate(previous):
            connection[j+m]=add(connection[j+m],-mul(correction,z,c),c)
        if 2*L<=n:
            L=n+1-L;previous=old;b=delta;m=1
        else:m+=1
    return connection[:L+1]


def batch_inverse_nonzero(a,c:Optional[Count]=None):
    """Invert an array containing NO zeros, with one field inversion."""
    if not a:return []
    prefix=[1]
    for z in a:prefix.append(mul(prefix[-1],z,c))
    v=inv(prefix[-1],c)
    out=[0]*len(a)
    for i in range(len(a)-1,-1,-1):
        out[i]=mul(v,prefix[i],c)
        v=mul(v,a[i],c)
    return out


def poly_eval(coefficients,z,c:Optional[Count]=None):
    v=0
    for a in reversed(coefficients):v=add(mul(v,z,c),a,c)
    return v


def extract_columns(x,m,c:Optional[Count]=None):
    n=len(x)
    if n%m:raise ValueError('M must divide N')
    k=n//m
    if k<m or k&(k-1) or m&(m-1):
        raise ValueError('radix-two K,M required and K>=M')
    root_of_unity(n)
    if c:c.input_reads+=n
    return [[x[b*m+t]%P for b in range(k)] for t in range(m)]


def learn_spectral_recurrences(cols,max_order,c:Optional[Count]=None):
    m=len(cols);k=len(cols[0])
    if not 1<=max_order or 2*max_order>m:
        raise ValueError('require 1<=d and 2d<=M')
    train=[ntt(cols[t],True,c) for t in range(2*max_order)]
    q=[]
    for ell in range(k):
        samples=[train[t][ell] for t in range(2*max_order)]
        coeff=berlekamp_massey(samples,c)
        if len(coeff)-1>max_order:return None,None
        order=len(coeff)-1
        # Verify connection even on rank-deficient training prefixes.
        for t in range(order,2*max_order):
            val=samples[t]
            for i in range(1,order+1):
                val=add(val,mul(coeff[i],samples[t-i],c),c)
            if nonzero(val,c):return None,None
        q.append(coeff)
    return train,q


def transpose_circulant_action(w, eigenvalues,c:Optional[Count]=None):
    """Return C^T w where DFT(Cv)[ell]=eigenvalues[ell]*DFT(v)[ell]."""
    fw=ntt(w,True,c)
    k=len(w)
    z=[mul(fw[ell],eigenvalues[-ell%k],c) for ell in range(k)]
    return ntt(z,False,c)


def verify_raw_recurrence(cols,q,max_order,rounds=3,rng=None,c:Optional[Count]=None):
    """Freivalds-style one-sided certificate; false pass <=p^-rounds.

    Sample w only after q has been learned. For each t>=d, certify:
       w^T v_t + sum_i (C_i^T w)^T v_(t-i) = 0.
    Even if all K coefficients of each C_i are dense, this uses only
    d inverse/forward K transforms per random w plus dN dot products.
    """
    if rounds<1:raise ValueError('positive independent rounds required')
    if rng is None:rng=secrets.SystemRandom()
    m=len(cols);k=len(cols[0]);d=max_order
    for _ in range(rounds):
        w=[rng.randrange(P) for _ in range(k)]
        # Share the forward Fourier transform of w across all d operators.
        fw=ntt(w,True,c)
        projected=[None]*d
        for i in range(1,d+1):
            products=[mul(fw[ell],q[-ell%k][i] if i<len(q[-ell%k]) else 0,c)
                      for ell in range(k)]
            projected[i-1]=ntt(products,False,c)
        # t<2d may be checked too, even though they were used for training.
        for t in range(d,m):
            value=0
            for b in range(k):value=add(value,mul(w[b],cols[t][b],c),c)
            for i in range(1,d+1):
                phi=projected[i-1]
                for b in range(k):
                    value=add(value,mul(phi[b],cols[t-i][b],c),c)
            if nonzero(value,c):return False
    return True


def synthesize_from_recurrences(train,q,m,n,c:Optional[Count]=None):
    """Evaluate S_ell(z)=sum_(t=0)^(M-1) F_t[ell] z^t exactly at all
    z=omega_N^(-ell-j*K) with O(d*N) scalar operations.

    Use Q(z)*S(z)=P(z)+z^M B(z), deg(P),deg(B)<order.
    Since z^M=omega_K^(-ell), at all M outputs the numerator
    has degree<order. Numerator/denominator evaluations take O(order)
    per output. Q has at most order singular roots; each is evaluated
    by a direct length-M Horner evaluation, cost O(order*M) per ell.
    Nonzero denominators are inverted in one batch.
    """
    k=n//m
    table=root_table(n,c)
    numerators=[0]*n;denominators=[0]*n
    outputs=[0]*n
    nonzero_indices=[];nz_den=[]
    singular_count=0
    for ell in range(k):
        coeff=q[ell]
        r=len(coeff)-1
        if not r:
            # BM order zero on nonempty sample means all sample values zero;
            # certified later columns zero too.
            continue
        f=[train[t][ell] for t in range(min(len(train),m))]
        for t in range(len(f),m):
            val=0
            for i in range(1,r+1):
                val=add(val,-mul(coeff[i],f[t-i],c),c)
            f.append(val)
        if len(f)!=m:raise AssertionError('invalid recurrence prefix')
        head=[];tail=[]
        zm=table[(-ell*m)%n]
        for j in range(r):
            p=0;b=0
            for i in range(j+1):p=add(p,mul(coeff[i],f[j-i],c),c)
            for i in range(j+1,r+1):b=add(b,mul(coeff[i],f[m+j-i],c),c)
            head.append(p);tail.append(add(p,mul(zm,b,c),c))
        # tail[j] stores P[j]+zm*B[j].
        z=table[(-ell)%n]
        phase=table[(-k)%n]
        for j in range(m):
            pos=ell+j*k
            denom=poly_eval(coeff,z,c)
            if nonzero(denom,c):
                numerators[pos]=poly_eval(tail,z,c)
                nz_den.append(denom);nonzero_indices.append(pos)
            else:
                singular_count+=1
                # A root of Q is removable (S is a polynomial), but using
                # the truncated direct sum avoids any derivative assumptions.
                outputs[pos]=poly_eval(f,z,c)
            z=mul(z,phase,c)
    recip=batch_inverse_nonzero(nz_den,c)
    for pos,v in zip(nonzero_indices,recip):
        outputs[pos]=mul(numerators[pos],v,c)
    if c:c.output_writes+=n
    return outputs,singular_count


def phase10_transform(x:list[int],m:int,max_order:int,rounds=3,rng=None,
                      counter:Optional[Count]=None,return_certificate=False):
    """Certified exact fast-path transform, or None (rejected).

    A correct promised input ALWAYS passes and returns exact DFT.
    Non-promised input may false-accept with probability <=P^-rounds
    under independent uniform w vectors (input fixed before randomness).
    """
    c=counter or Count()
    cols=extract_columns(x,m,c)
    train,q=learn_spectral_recurrences(cols,max_order,c)
    if train is None:
        cert={'accepted':False,'reason':'no order-d recurrence fits initial 2d columns'}
        return (None,cert,c) if return_certificate else None
    if not verify_raw_recurrence(cols,q,max_order,rounds,rng,c):
        cert={'accepted':False,'reason':'independent random-vector recurrence check failed'}
        return (None,cert,c) if return_certificate else None
    out,singular=synthesize_from_recurrences(train,q,m,len(x),c)
    cert={'accepted':True,'max_order':max(len(x)-1 for x in q),
          'max_allowed_order':max_order,'singular_outputs':singular,
          'rounds':rounds,'false_accept_bound':f'{P}^(-{rounds})',
          'operator_support_model':'arbitrary circulants, one per recurrence lag'}
    return (out,cert,c) if return_certificate else out


def make_spectral_recurrent_example(k,m,d,seed=0,force_roots=None):
    """Generate fully dense spectral streams with unknown order-d controller.

    Uses independent frequency-specific coefficients and d initial spectral
    columns. For d=2 the residuals against every one-step controller
    are generically dense in BOTH spatial and Fourier representations.
    """
    rng=random.Random(seed)
    q=[];freqs=[[0]*k for _ in range(m)]
    for ell in range(k):
        coeff=[1]+[rng.randrange(1,P) for _ in range(d)]
        if force_roots is not None and ell==0:
            # Example Q(z)=(1-z)^d creates a pole at output k=0,
            # but it is always removable from the finite S(z).
            import math
            coeff=[(-1)**i*math.comb(d,i)%P for i in range(d+1)]
        q.append(coeff)
        for t in range(d):freqs[t][ell]=rng.randrange(P)
        for t in range(d,m):
            freq_val=0
            for i in range(1,d+1):freq_val=(freq_val-coeff[i]*freqs[t-i][ell])%P
            freqs[t][ell]=freq_val
    cols=[ntt(row,False) for row in freqs]
    x=[cols[t][b] for b in range(k) for t in range(m)]
    return x,q,freqs


def reference_full_ntt(x):
    return ntt(x,True)


def direct_full_dft(x):
    n=len(x);table=root_table(n)
    return [sum(x[t]*table[(-k*t)%n] for t in range(n))%P for k in range(n)]

if __name__=='__main__':
    n=2048;m=16;k=n//m
    x,q,_=make_spectral_recurrent_example(k,m,2,87,force_roots=True)
    y,cert,c=phase10_transform(x,m,2,rng=random.Random(42),return_certificate=True)
    assert y==reference_full_ntt(x)
    print('Phase 10 self-test:',n,cert,'ops/input:',round(c.total()/n,3))
