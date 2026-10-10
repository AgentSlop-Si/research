"""Hero #1 Phase18: certified cyclic-annihilator DFT with sparse defects.

Uses the *unchanged* Phase17 field arithmetic kernel and noncommuting Green
operator. Never assumes compression on arbitrary data: exact candidate check,
exact singular-frequency repair and full Bluestein fallback are mandatory.
"""
from dataclasses import dataclass, field
from math import log2
from green_sparse import P0,G0
from rational_forcing import AllLengthGreen, PolyStats, forcing_from_sparse, bluestein_transform


@dataclass
class Work:
    multiplies: int = 0
    additions: int = 0
    inversions: int = 0
    reads: int = 0
    writes: int = 0
    comparisons: int = 0
    bm_operations: int = 0
    candidates: int = 0
    repaired: int = 0
    sparse: PolyStats = field(default_factory=PolyStats)

    def arithmetic(self):
        return self.multiplies+self.additions+self.inversions+self.sparse.total_field_ops()


def shift_polynomial_apply(v, q, p, co=None):
    """Compute h = q(S)v, S v[j] = v[(j-1)%N], exactly."""
    n=len(v)
    assert n>0 and 0<len(q)<=n and q[0]%p
    d=len(q)-1
    out=[0]*n
    for j in range(n):
        accum=0
        for s,c in enumerate(q):
            accum=(accum+c*v[(j-s)%n])%p
        out[j]=accum
    if co is not None:
        co.multiplies+=n*(d+1)
        co.additions+=n*(d+1)
        co.reads+=n*(d+1)
        co.writes+=n
    return out


def candidate_majority_ratio(r,p,co=None):
    """Find projective ratio shared by >N/2 predecessor edges if it exists.

    Candidate (a:b) represents r[j]/r[j-1] with no field inversions.
    Correctness is certified *separately* by a full defect scan.
    """
    n=len(r)
    if n<2 or any(v%p==0 for v in r):
        return None
    pair=None
    balance=0
    for j in range(n):
        a,b=r[j]%p,r[(j-1)%n]%p
        if balance==0:
            pair=(a,b)
            balance=1
        else:
            if a*pair[1]%p == pair[0]*b%p:
                balance+=1
            else:
                balance-=1
            if co is not None:
                co.multiplies+=2
                co.comparisons+=1
        if co is not None:co.reads+=2
    assert pair is not None and pair[1] != 0
    return [pair[1],(-pair[0])%p]


def bm_prefix_candidate(r, max_degree, p, co=None):
    """BM on O(max_degree) *prefix* samples; never assumes it fits globally.

    Degree bound rejected early; the complete N-vector is then audited.
    Cost O(max_degree**2) field operations, not an unchecked free oracle.
    """
    if max_degree<1:return None
    sequence=r[:min(len(r),2*max_degree+2)]
    C=[1];B=[1]; L=0; delay=1; b=1
    for n,v in enumerate(sequence):
        discrepancy=v%p
        for i in range(1,L+1):
            discrepancy=(discrepancy+C[i]*sequence[n-i])%p
            if co is not None:
                co.multiplies+=1;co.additions+=1;co.reads+=2
        if not discrepancy:
            delay+=1
            continue
        factor=discrepancy*pow(b,-1,p)%p
        if co is not None:co.multiplies+=1;co.inversions+=1
        previous=C[:]
        extent=delay+len(B)
        if len(C)<extent:C.extend([0]*(extent-len(C)))
        for j,coef in enumerate(B):
            C[delay+j]=(C[delay+j]-factor*coef)%p
            if co is not None:co.multiplies+=1;co.additions+=1
        if 2*L<=n:
            L=n+1-L
            B=previous
            b=discrepancy
            delay=1
        else:delay+=1
        if L>max_degree:return None
    if L==0:return [1]
    C=C[:L+1]
    while len(C)>1 and C[-1]==0:C.pop()
    return C


def batch_inverse_nonzero(elements,p,co=None):
    """One field inverse for any number of nonzero elements."""
    if not elements:return []
    prefix=[1]*(len(elements)+1)
    for i,d in enumerate(elements):
        assert d%p
        prefix[i+1]=prefix[i]*d%p
    inv=pow(prefix[-1],-1,p)
    result=[0]*len(elements)
    for i in range(len(elements)-1,-1,-1):
        result[i]=prefix[i]*inv%p
        inv=inv*elements[i]%p
    if co is not None:
        co.multiplies+=3*len(elements)
        co.inversions+=1
        co.reads+=4*len(elements)
        co.writes+=2*len(elements)+1
    return result


def sparse_direct_fourier(entries,n,powers,p,co=None):
    """Evaluate K geometric streams without an N-size FFT."""
    ans=[0]*n
    for j,v in entries.items():
        node=powers[j]
        cur=v%p
        for k in range(n):
            ans[k]=(ans[k]+cur)%p
            cur=cur*node%p
        if co is not None:
            co.multiplies+=n
            co.additions+=n
            co.reads+=n
            co.writes+=n
    return ans


def direct_one_frequency(r,node,p,co=None):
    cur=1;acc=0
    for v in r:
        acc=(acc+v*cur)%p
        cur=cur*node%p
    if co is not None:
        co.multiplies+=2*len(r)
        co.additions+=len(r)
        co.reads+=len(r)
        co.repaired+=1
    return acc


def decode_annihilator(r,q,engine,work=None,forcing_method='auto'):
    """From h=q(S)r, reconstruct every F(r)[k] (including q(omega^k)=0).

    Requires 0<len(q)<=N and nonzero constant coefficient q[0].
    No assumptions about residual support: full-transform fallback if dense.
    """
    if work is None:work=Work()
    n,p=engine.n,engine.p
    if len(r)!=n or not q or len(q)>n or not q[0]%p:
        raise ValueError('bad residual or annihilator')
    q=[c%p for c in q]
    h=shift_polynomial_apply(r,q,p,work)
    entries={j:v for j,v in enumerate(h) if v%p}
    K=len(entries); d=len(q)-1
    limit=max(3,n//max(6,(n.bit_length()-1)**2))
    if forcing_method=='auto':
        forcing_method=('direct' if K<=3 else ('rational' if K<=limit else 'bluestein'))
    if forcing_method=='direct':
        if K>3:raise ValueError('direct mode limited to <=3 defects; use rational')
        forcing=sparse_direct_fourier(entries,n,engine.powers,p,work)
    elif forcing_method=='rational':
        forcing,_=forcing_from_sparse(entries,n,engine.omega,p,engine.primitive_gen,work.sparse)
    elif forcing_method=='bluestein':
        forcing,_=bluestein_transform(h,n,engine.omega,p,engine.primitive_gen,work.sparse)
    else:raise ValueError('bad forcing method')
    zeros=[];nonzero=[];positions=[]
    for k,z in enumerate(engine.powers):
        # Horner q(z); exactly d multiplies and d additions.
        val=q[-1]
        for c in reversed(q[:-1]):val=(val*z+c)%p
        if val:positions.append(k);nonzero.append(val)
        else:zeros.append(k)
    work.multiplies+=n*d
    work.additions+=n*d
    work.reads+=n*(d+1)
    inverses=batch_inverse_nonzero(nonzero,p,work)
    out=[0]*n
    for k,inv in zip(positions,inverses):out[k]=forcing[k]*inv%p
    for k in zeros:out[k]=direct_one_frequency(r,engine.powers[k],p,work)
    work.multiplies+=len(positions)
    work.writes+=n
    return out, {'K':K,'degree':d,'resonant':len(zeros),'forcing_method':forcing_method,'work':work}


class RecurrenceGreen(AllLengthGreen):
    """Phase18 exact Green FFT with certified long-range recurrence selection."""
    pass


def majority_long_shift(r,delay,p,co=None):
    """Projective majority for graph edges j<-j-delay with no divisions."""
    n=len(r)
    if not (1 <= delay < n) or any(v%p==0 for v in r):return None
    pair=None;balance=0
    for j in range(n):
        a,b=r[j]%p,r[(j-delay)%n]%p
        if not balance:pair=(a,b);balance=1
        else:
            if a*pair[1]%p==pair[0]*b%p:balance+=1
            else:balance-=1
            if co is not None:co.multiplies+=2;co.comparisons+=1
        if co is not None:co.reads+=2
    return (pair[0],pair[1])


def shift_binomial_apply(r,delay,a,b,p,co=None):
    """h=(b I-a S**delay)r; degree delay, only two taps."""
    n=len(r)
    if not (1<=delay<n):raise ValueError('bad delay')
    ans=[(b*r[j]-a*r[(j-delay)%n])%p for j in range(n)]
    if co is not None:
        co.multiplies+=2*n;co.additions+=n
        co.reads+=2*n;co.writes+=n
    return ans


def count_resonant_binomial(n,delay,a,b,p):
    """Number of N-th roots satisfying b-a*z**delay=0, without N scans."""
    from math import gcd
    if b%p==0:raise ValueError('constant term must not vanish')
    if a%p==0:return 0
    g=gcd(n,delay);ell=n//g
    # (a/b)^ell = 1 precisely when each delay-cycle is singular.
    ratio=a*pow(b,-1,p)%p
    return g if pow(ratio,ell,p)==1 else 0


def decode_binomial(r,delay,a,b,engine,work=None,forcing_method='auto'):
    """Exact F(r) via sparse defects of an *arbitrarily long* cyclic shift.

    Runtime O(N + sparse-forcing-cost + N*resonances), independent of delay
    when no resonance occurs. Direct repairs ensure correctness when singular.
    """
    if work is None:work=Work()
    n,p=engine.n,engine.p
    a,b=a%p,b%p
    if b==0:raise ValueError('nonzero constant coefficient required')
    h=shift_binomial_apply(r,delay,a,b,p,work)
    entries={j:v for j,v in enumerate(h) if v}
    K=len(entries)
    limit=max(3,n//max(6,(n.bit_length()-1)**2))
    if forcing_method=='auto':
        forcing_method='direct' if K<=3 else ('rational' if K<=limit else 'bluestein')
    if forcing_method=='direct':
        if K>3:raise ValueError('direct mode limited to <=3 defects')
        forcing=sparse_direct_fourier(entries,n,engine.powers,p,work)
    elif forcing_method=='rational':
        forcing,_=forcing_from_sparse(entries,n,engine.omega,p,engine.primitive_gen,work.sparse)
    elif forcing_method=='bluestein':
        forcing,_=bluestein_transform(h,n,engine.omega,p,engine.primitive_gen,work.sparse)
    else:raise ValueError('unknown method')
    z=pow(engine.omega,delay,p)
    work.multiplies+=2*delay.bit_length() # upper bound on pow modular multiplications
    cur=1
    zero=[];nonzero=[];nonzero_pos=[]
    for k in range(n):
        val=(b-a*cur)%p
        if val:nonzero_pos.append(k);nonzero.append(val)
        else:zero.append(k)
        cur=cur*z%p
    work.multiplies+=2*n;work.additions+=n
    inverses=batch_inverse_nonzero(nonzero,p,work)
    out=[0]*n
    for k,inv in zip(nonzero_pos,inverses):out[k]=forcing[k]*inv%p
    for k in zero:out[k]=direct_one_frequency(r,engine.powers[k],p,work)
    work.multiplies+=len(nonzero_pos)
    work.writes+=n
    return out,{'K':K,'delay':delay,'resonant':len(zero),
                'forcing_method':forcing_method,'work':work}


def dense_from_shift_defects(h,delay,alpha,p):
    """Construct r=(I-alpha*S**delay)^-1 h by independent graph cycles.

    It is a test-signal generator, not an uncharged part of the FFT runtime.
    Uses two linear scans per permutation cycle and one inversion per cycle.
    """
    from math import gcd
    n=len(h)
    if not (1<=delay<n):raise ValueError('bad delay')
    g=gcd(n,delay);ell=n//g
    if pow(alpha,ell,p)==1:raise ValueError('singular shift graph')
    r=[0]*n
    for first in range(g):
        vertices=[];j=first
        for _ in range(ell):
            vertices.append(j)
            j=(j+delay)%n
        assert j==first
        z=0
        for j in vertices:z=(alpha*z+h[j])%p
        prev=z*pow((1-pow(alpha,ell,p))%p,-1,p)%p
        for j in vertices:
            prev=(alpha*prev+h[j])%p
            r[j]=prev
    assert shift_binomial_apply(r,delay,alpha,1,p)==[v%p for v in h]
    return r


def far_coprime_shift(n):
    from math import gcd
    for delta in range(max(2,n//2-1),n):
        if gcd(delta,n)==1:return delta
    return n-1


def graph_polynomial_apply(r,delay,q,p,co=None):
    """h_j = sum_i q_i r_(j-i*delay): O(N*len(q))."""
    n=len(r)
    if not (1<=delay<n and 1<=len(q)<=n and q[0]%p):
        raise ValueError('invalid graph polynomial')
    ans=[0]*n
    for j in range(n):
        v=0
        for i,c in enumerate(q):v=(v+c*r[(j-i*delay)%n])%p
        ans[j]=v
    if co is not None:
        co.multiplies+=n*len(q);co.additions+=n*len(q)
        co.reads+=n*len(q);co.writes+=n
    return ans


def graph_bm_candidate(r,delay,max_degree,p,co=None):
    """Find a short recurrence along one graph cycle, verify globally later.

    If gcd(N,delay)=1, the orbit visits all vertices; otherwise it sees
    one representative cycle and any candidate MUST still pass the full audit.
    """
    from math import gcd
    n=len(r)
    if max_degree<1 or not (1<=delay<n):return None
    orbitlen=n//gcd(n,delay)
    count=min(orbitlen,2*max_degree+2)
    seq=[r[(t*delay)%n] for t in range(count)]
    if co is not None:co.reads+=count
    return bm_prefix_candidate(seq,max_degree,p,co)


def decode_graph_polynomial(r,delay,q,engine,work=None,forcing_method='auto'):
    """DFT through a degree-d polynomial in the distant-shift S**delay.

    Cost O(N*d + sparse-forcing-cost + N*d*gcd(N,delay)) worst case for
    resonances; singular frequency count <= d*gcd(N,delay).
    """
    if work is None:work=Work()
    n,p=engine.n,engine.p
    q=[v%p for v in q]
    if not q or q[0]==0:raise ValueError('invalid recurrence')
    h=graph_polynomial_apply(r,delay,q,p,work)
    entries={j:z for j,z in enumerate(h) if z}
    K=len(entries)
    threshold=max(3,n//max(6,(n.bit_length()-1)**2))
    if forcing_method=='auto':
        forcing_method='direct' if K<=3 else ('rational' if K<=threshold else 'bluestein')
    if forcing_method=='direct':
        if K>3:raise ValueError('direct mode only for <=3 nonzeros')
        forcing=sparse_direct_fourier(entries,n,engine.powers,p,work)
    elif forcing_method=='rational':
        forcing,_=forcing_from_sparse(entries,n,engine.omega,p,engine.primitive_gen,work.sparse)
    elif forcing_method=='bluestein':
        forcing,_=bluestein_transform(h,n,engine.omega,p,engine.primitive_gen,work.sparse)
    else:raise ValueError('invalid method')
    step=pow(engine.omega,delay,p)
    work.multiplies+=2*delay.bit_length()
    zk=1
    zeros=[];nonzero=[];positions=[]
    for k in range(n):
        val=q[-1]
        for ci in reversed(q[:-1]):val=(val*zk+ci)%p
        if val:positions.append(k);nonzero.append(val)
        else:zeros.append(k)
        zk=zk*step%p
    d=len(q)-1
    work.multiplies+=n*(d+1);work.additions+=n*d
    work.reads+=n*(d+1)
    inverses=batch_inverse_nonzero(nonzero,p,work)
    out=[0]*n
    for k,inv in zip(positions,inverses):out[k]=forcing[k]*inv%p
    for k in zeros:out[k]=direct_one_frequency(r,engine.powers[k],p,work)
    work.multiplies+=len(positions);work.writes+=n
    return out,{'K':K,'degree_on_graph':d,'delay':delay,'resonant':len(zeros),
                'forcing_method':forcing_method,'work':work}


def _transform_graph_bm(self,x,max_degree=3,delays=None,method='auto'):
    """Fully charged constant-bank exact adaptive transform, Phase18 final.

    If no certified sparse-defect candidate passes, compute Phase17 Bluestein.
    All shift distances and recurrence coefficients are treated as proposals,
    never as unverified promises.
    """
    if len(x)!=self.n:raise ValueError('length mismatch')
    n,p=self.n,self.p
    work=Work()
    r=self.P.apply(x)
    work.multiplies+=2*n;work.additions+=n;work.reads+=2*n;work.writes+=n
    if delays is None:delays=(1,far_coprime_shift(n)) if n>3 else (1,)
    delays=tuple(dict.fromkeys(int(d) for d in delays if 1<=d<n))
    threshold=max(3,n//max(6,(n.bit_length()-1)**2))
    options=[]
    for delay in delays:
        if max_degree<1:break
        pair=majority_long_shift(r,delay,p,work)
        if pair is not None:
            a,b=pair
            h=shift_binomial_apply(r,delay,a,b,p,work)
            K=sum(bool(v) for v in h)
            work.comparisons+=n;work.candidates+=1
            if K<n/2 and K<=threshold:
                from math import gcd
                g=gcd(n,delay)
                # singularity check via exponent of a*b^-1; charge field inverse.
                resonant=count_resonant_binomial(n,delay,a,b,p)
                work.inversions+=1
                work.multiplies+=2*max(1,n.bit_length())
                if resonant<=min(4,max_degree*g):
                    options.append((K,1,'majority',delay,[b,(-a)%p]))
        if max_degree>=2:
            q=graph_bm_candidate(r,delay,max_degree,p,work)
            if q is not None:
                h=graph_polynomial_apply(r,delay,q,p,work)
                K=sum(bool(v) for v in h)
                work.comparisons+=n;work.candidates+=1
                if K<=threshold:
                    # gcd=1 implies at most degree(q) resonant nodes.
                    # Otherwise conservatively skip candidates that could
                    # require extensive direct repair; correctness unaffected.
                    from math import gcd
                    if gcd(n,delay)<=max(1,4//max(1,len(q)-1)):
                        options.append((K,len(q)-1,'graph-bm',delay,q))
    if method=='bluestein' or not options:
        forcing,_=bluestein_transform(r,n,self.omega,p,self.primitive_gen,work.sparse)
        meta={'K':n,'delay':None,'degree_on_graph':None,'resonant':0,
              'forcing_method':'bluestein','selected':'fallback'}
    else:
        K,d,origin,delay,q=min(options,key=lambda t:(t[0],t[1]))
        if origin=='majority':
            forcing,meta=decode_binomial(r,delay,(-q[1])%p,q[0],self,work)
            meta['degree_on_graph']=1
        else:
            forcing,meta=decode_graph_polynomial(r,delay,q,self,work)
        meta.update({'Q':q,'selected':origin})
    y=self.L.solve(forcing)
    work.multiplies+=3*n+1;work.additions+=2*n
    work.reads+=3*n;work.writes+=2*n
    meta['work']=work
    return y,meta

RecurrenceGreen.transform_recurrence=_transform_graph_bm


def decode_factor_union(r,factors,engine,work=None,forcing_method='auto'):
    """Exact Fourier from a *provided* ordered union of cyclic graph filters.

    Factors are pairs (delta,alpha) representing (I-alpha*S**delta).
    These factors commute algebraically (all are polynomials in S): the
    noncommuting part of the wider construction is Green L/P, not this bank.

    Runtime O(m*N + sparse-forcing(K) + N*number_of_resonances). No claim
    that discovering the factors from unknown data is free or automatic.
    """
    if work is None:work=Work()
    n,p=engine.n,engine.p
    if len(r)!=n or not factors:raise ValueError('missing signal/factors')
    factors=[(int(delta),int(alpha)%p) for delta,alpha in factors]
    if any(not (1<=delta<n) for delta,alpha in factors):
        raise ValueError('invalid graph shift')
    h=[z%p for z in r]
    for delta,alpha in factors:
        h=shift_binomial_apply(h,delta,alpha,1,p,work)
    entries={j:z for j,z in enumerate(h) if z}
    K=len(entries)
    limit=max(3,n//max(6,(n.bit_length()-1)**2))
    if forcing_method=='auto':
        forcing_method='direct' if K<=3 else ('rational' if K<=limit else 'bluestein')
    if forcing_method=='direct':
        if K>3:raise ValueError('direct requires <=3 defects')
        forcing=sparse_direct_fourier(entries,n,engine.powers,p,work)
    elif forcing_method=='rational':
        forcing,_=forcing_from_sparse(entries,n,engine.omega,p,engine.primitive_gen,work.sparse)
    elif forcing_method=='bluestein':
        forcing,_=bluestein_transform(h,n,engine.omega,p,engine.primitive_gen,work.sparse)
    else:raise ValueError('unknown forcing method')
    # Spectral denominator is product of factor eigenvalues at each node.
    # Stream each long-shift phase across all k; no expanded 2**m-tap q.
    denom=[1]*n
    for delta,alpha in factors:
        step=pow(engine.omega,delta,p)
        work.multiplies+=2*delta.bit_length()
        current=1
        for k in range(n):
            denom[k]=(denom[k]*(1-alpha*current))%p
            current=current*step%p
        work.multiplies+=3*n
        work.additions+=n
        work.reads+=n;work.writes+=n
    positions=[k for k,v in enumerate(denom) if v]
    zero=[k for k,v in enumerate(denom) if not v]
    inverses=batch_inverse_nonzero([denom[k] for k in positions],p,work)
    out=[0]*n
    for k,inv in zip(positions,inverses):out[k]=forcing[k]*inv%p
    for k in zero:out[k]=direct_one_frequency(r,engine.powers[k],p,work)
    work.multiplies+=len(positions);work.writes+=n
    return out,{'K':K,'factors':factors,'factor_count':len(factors),
                'resonant':len(zero),'forcing_method':forcing_method,'work':work}


def _transform_known_factors(self,x,factors,forcing_method='auto'):
    """A separate exact structured family. Inputs include the factor description.

    A dense defect triggers the fully charged Bluestein branch instead of
    a false compression; the supplied factor description is still charged
    for applying the factors before deciding to use it.
    """
    if len(x)!=self.n:raise ValueError('length mismatch')
    n,p=self.n,self.p
    work=Work()
    r=self.P.apply(x)
    work.multiplies+=2*n;work.additions+=n;work.reads+=2*n;work.writes+=n
    h=r[:]
    for delta,alpha in factors:
        h=shift_binomial_apply(h,delta,alpha,1,p,work)
    K=sum(bool(z) for z in h)
    threshold=max(3,n//max(6,(n.bit_length()-1)**2))
    if K>threshold:
        forcing,_=bluestein_transform(r,n,self.omega,p,self.primitive_gen,work.sparse)
        meta={'K':K,'selected':'full-fallback','resonant':0,'factor_count':len(factors)}
    else:
        # Previous h scan is counted as a certificate, not reused for free
        # by the independent decoder in this first implementation.
        forcing,meta=decode_factor_union(r,factors,self,work,forcing_method)
        meta['selected']='known-factor-union'
    y=self.L.solve(forcing)
    work.multiplies+=3*n+1;work.additions+=2*n
    work.reads+=3*n;work.writes+=2*n
    meta['work']=work
    return y,meta

RecurrenceGreen.transform_known_factors=_transform_known_factors
