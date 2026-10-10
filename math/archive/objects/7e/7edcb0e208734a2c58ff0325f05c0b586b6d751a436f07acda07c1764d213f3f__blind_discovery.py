"""Hero #1 Phase19: deterministic linear-work *unknown* cyclic-shift discovery.

Two-valued adjacent projective-ratio certificate: when a nowhere-zero signal
has one sparse defect h=(I-alpha*S**delta)r (gcd(delta,N)=1), its ratios
r[j]/r[j-1] have two values, with counts delta^{-1} and N-delta^{-1}.
This permits full exact Fourier recovery with no supplied graph delay.
Every accepted candidate is independently verified across all N entries.
"""
from dataclasses import dataclass
from math import gcd
from annihilator_engine import (
    RecurrenceGreen, Work, decode_binomial, decode_factor_union,
    shift_binomial_apply, sparse_direct_fourier,
)
from rational_forcing import bluestein_transform

@dataclass
class DiscoveryStats:
    projective_comparisons: int = 0
    field_products: int = 0
    vector_reads: int = 0
    candidate_edge_tests: int = 0
    candidate_full_scans: int = 0
    rejected: int = 0
    gcd_calls: int = 0
    integer_inversions: int = 0
    nonlinear_divisions: int = 0

    def proxy(self):
        return self.field_products + self.projective_comparisons


def _equal_projective(a,b,c,d,p,stats):
    """Compare a/b and c/d without field inversions; denominators nonzero."""
    stats.projective_comparisons += 1
    stats.field_products += 2
    return (a*d-c*b)%p == 0


def _fingerprint_candidates(r,p,stats):
    """Return <=2 coprime shift guesses from exactly 1 or 2 adjacent ratios.

    No FFT, hashing, field division, or search over N delays is performed.
    Its guarantee covers every nowhere-zero 1-defect shift with coprime delta.
    """
    n=len(r)
    if n < 2 or any(v%p==0 for v in r):
        stats.vector_reads += n
        return []
    first=(r[0]%p,r[-1]%p)
    second=None
    counts=[0,0]
    for j in range(n):
        v=(r[j]%p,r[(j-1)%n]%p)
        stats.vector_reads += 2
        if _equal_projective(*v,*first,p,stats):
            counts[0]+=1
        elif second is None or _equal_projective(*v,*second,p,stats):
            if second is None:second=v
            counts[1]+=1
        else:
            return []
    if second is None:
        # A nowhere-zero cyclic geometric progression has zero defect at d=1.
        return [1]
    count=counts[0]
    proposed=[]
    for u in (count,n-count):
        stats.gcd_calls+=1
        if 0<u<n and gcd(u,n)==1:
            d=pow(u,-1,n)
            stats.integer_inversions+=1
            if d not in proposed:proposed.append(d)
    return proposed


def _majority_three(r,delay,p,stats):
    """Exact deterministic 3-edge majority, correct for <=1 defective edge."""
    n=len(r)
    if n<3 or any(r[j]%p==0 or r[(j-delay)%n]%p==0 for j in range(3)):
        return None
    sample=[(r[j]%p,r[(j-delay)%n]%p) for j in range(3)]
    stats.vector_reads+=6
    a,b=sample[0];c,d=sample[1];e,f=sample[2]
    if _equal_projective(a,b,c,d,p,stats):return (a,b)
    if _equal_projective(a,b,e,f,p,stats):return (a,b)
    if _equal_projective(c,d,e,f,p,stats):return (c,d)
    return None


def blind_one_defect(r,p,stats=None):
    """Find (delta,a,b,K) with h=(bI-aS**delta)r having K<=1 nonzeros.

    Each accepted candidate is verified via every coordinate. For r with
    a 1-defect coprime shift, success is unconditional, not probabilistic.
    On failure return None so caller can run its correct ordinary DFT.
    """
    if stats is None:stats=DiscoveryStats()
    n=len(r)
    if n<3:return None,stats
    for d in _fingerprint_candidates(r,p,stats):
        pair=_majority_three(r,d,p,stats)
        if pair is None:continue
        a,b=pair
        errors=0
        # Count every tested pair and stop on second distinct defect.
        for j in range(n):
            stats.candidate_edge_tests+=1
            stats.vector_reads+=2
            stats.field_products+=2
            if (b*r[j]-a*r[(j-d)%n])%p:
                errors+=1
                if errors>1:break
        stats.candidate_full_scans+=1
        if errors<=1:
            return (d,a,b,errors),stats
        stats.rejected+=1
    return None,stats


def transform_blind_one(engine,x):
    """Unconditionally exact FFT with full-basis certified 1-defect fast path.

    Phase17 FFT fallback is always invoked if the optional blind discovery
    fails. Both Green maps, discovery, verification and forcing are charged.
    """
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('wrong input length')
    work=Work()
    r=engine.P.apply(x)
    work.multiplies+=2*n;work.additions+=n;work.reads+=2*n;work.writes+=n
    candidate,ds=blind_one_defect(r,p)
    work.multiplies+=ds.field_products
    work.comparisons+=ds.projective_comparisons
    work.reads+=ds.vector_reads
    if candidate is None:
        forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,work.sparse)
        meta={'selected':'fallback','delay':None,'K':n,'resonant':0}
    else:
        delay,a,b,K=candidate
        forcing,meta=decode_binomial(r,delay,a,b,engine,work,'direct')
        assert meta['K']==K
        meta['selected']='blind-one-defect'
    y=engine.L.solve(forcing)
    work.multiplies+=3*n+1;work.additions+=2*n;work.reads+=3*n;work.writes+=2*n
    meta['work']=work
    meta['discovery']=ds
    return y,meta


def transform_semiblind_union(engine,x,known_factors):
    """Unknown last factor, previously *supplied* factors.

    Supplied factors cost O(mN) to apply. Their application may be dense.
    If Q_known(Px) has one defect after a hidden shift, recover last shift
    deterministically in O(N), then run exact union decoding from original Px.
    """
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('wrong input length')
    work=Work()
    r=engine.P.apply(x)
    work.multiplies+=2*n;work.additions+=n;work.reads+=2*n;work.writes+=n
    intermediate=r[:]
    for d,a in known_factors:
        if not (1<=d<n):raise ValueError('invalid known factor')
        intermediate=shift_binomial_apply(intermediate,d,a,1,p,work)
    candidate,ds=blind_one_defect(intermediate,p)
    work.multiplies+=ds.field_products;work.comparisons+=ds.projective_comparisons
    work.reads+=ds.vector_reads
    if candidate is None:
        forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,work.sparse)
        meta={'selected':'fallback','K':n,'resonant':0,'unknown_delay':None}
    else:
        delay,a,b,K=candidate
        work.inversions+=1
        alpha=a*pow(b,-1,p)%p
        work.multiplies+=1
        factors=list(known_factors)+[(delay,alpha)]
        forcing,meta=decode_factor_union(r,factors,engine,work,'direct')
        assert meta['K']==K
        meta.update({'selected':'semi-blind-union','unknown_delay':delay})
    y=engine.L.solve(forcing)
    work.multiplies+=3*n+1;work.additions+=2*n;work.reads+=3*n;work.writes+=2*n
    meta['work']=work;meta['discovery']=ds
    return y,meta


# Convenient opt-in entry points; original Phase18 implementation unchanged.
RecurrenceGreen.transform_blind_one=transform_blind_one
RecurrenceGreen.transform_semiblind_union=transform_semiblind_union


def blind_bounded_defects(r,p,max_defects=2,stats=None):
    """Blind shift / multiplier recovery using small adjacent-ratio alphabet.

    If a coprime-shift recurrence has K<=max_defects sparse edges, and its
    adjacent-ratio classes do not mix the two modular-wrap types, succeeds
    deterministically without knowing the shift. Every accepted candidate
    gets a full exact graph-defect certificate, so soundness is unconditional.

    Constant K => O(N * K * 2**(2*K*K)) arithmetic (coarse upper bound),
    including discovery and full verification. This is NOT an all-input FFT.
    """
    if stats is None:stats=DiscoveryStats()
    n=len(r); K=int(max_defects)
    if K<1 or 2*K+1>n or not all(v%p for v in r):
        stats.vector_reads+=n
        return None,stats
    B=2*K*K
    groups=[]  # Each (projective numerator,denominator,count)
    for j in range(n):
        a,b=r[j]%p,r[(j-1)%n]%p
        stats.vector_reads+=2
        for g in groups:
            if _equal_projective(a,b,g[0],g[1],p,stats):
                g[2]+=1
                break
        else:
            groups.append([a,b,1])
            if len(groups)>B:
                return None,stats
    # Any wrap class has its entire count included in u if no cross-wrap
    # equality collisions occurred. Enumerate ALL possible subset counts.
    possible={0}
    for a,b,count in groups:
        possible|={v+count for v in tuple(possible)}
    # Optionally finite alphabet has only one class: the uniform character
    # case is recovered by delay 1.
    candidate_delays=[]
    if len(groups)==1:candidate_delays=[1]
    else:
        for u in sorted(possible):
            if 0<u<n and gcd(u,n)==1:
                d=pow(u,-1,n)
                stats.gcd_calls+=1
                stats.integer_inversions+=1
                if d not in candidate_delays:candidate_delays.append(d)
    for d in candidate_delays:
        # 2K+1 distinct observations guarantee strict ratio majority on any
        # genuine K-defect delay, regardless of the adversarial defect sites.
        leader=None;votes=0
        for j in range(2*K+1):
            pair=(r[j]%p,r[(j-d)%n]%p)
            stats.vector_reads+=2
            if votes==0:
                leader=pair;votes=1
            elif _equal_projective(*pair,*leader,p,stats):
                votes+=1
            else:votes-=1
        if leader is None:continue
        # Critical: full-vector certificate, never trust the fingerprint.
        a,b=leader
        errors=0
        for j in range(n):
            stats.candidate_edge_tests+=1
            stats.vector_reads+=2
            stats.field_products+=2
            if (b*r[j]-a*r[(j-d)%n])%p:
                errors+=1
                if errors>K:break
        stats.candidate_full_scans+=1
        if errors<=K:
            return (d,a,b,errors),stats
        stats.rejected+=1
    return None,stats


def transform_blind_bounded(engine,x,max_defects=2):
    """Exact FFT with new bounded-defect blind model and all-input fallback."""
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('wrong input length')
    work=Work()
    r=engine.P.apply(x)
    work.multiplies+=2*n;work.additions+=n;work.reads+=2*n;work.writes+=n
    candidate,ds=blind_bounded_defects(r,p,max_defects)
    work.multiplies+=ds.field_products;work.comparisons+=ds.projective_comparisons
    work.reads+=ds.vector_reads
    if candidate is None:
        forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,work.sparse)
        meta={'selected':'fallback','delay':None,'K':n,'resonant':0}
    else:
        delay,a,b,K=candidate
        forcing,meta=decode_binomial(r,delay,a,b,engine,work)
        assert meta['K']==K
        meta['selected']='blind-bounded-defects'
    y=engine.L.solve(forcing)
    work.multiplies+=3*n+1;work.additions+=2*n;work.reads+=3*n;work.writes+=2*n
    meta['work']=work;meta['discovery']=ds
    return y,meta

RecurrenceGreen.transform_blind_bounded=transform_blind_bounded
