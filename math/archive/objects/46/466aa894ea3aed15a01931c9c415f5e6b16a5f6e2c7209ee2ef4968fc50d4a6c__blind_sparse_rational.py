"""Phase 20: certified unknown binomial denominator / <=2 unknown impulses.

For R_k = F_N(r)_k, if h=(I-alpha*S^delta)r has <=2 impulses,
Y_k=(1-alpha*(omega**delta)**k)*R_k is a sum of <=2 exponentials in k,
so its contiguous 3x3 Hankel determinants vanish. Their resultant can
identify candidates for unknown delta/alpha in O(N) field arithmetic in
the nondegenerate constant-resultant-degree case.

For EVERY input, a complete O(N) defect certificate is mandatory before the
O(N) sparse Fourier forcing is used. Fallback is ordinary exact FFT.
"""
from dataclasses import dataclass
from annihilator_engine import Work, direct_one_frequency, decode_binomial
from rational_forcing import bluestein_transform


def trim(a):
    while len(a)>1 and a[-1]==0:a.pop()
    return a


def mul(a,b,p,work):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            c[i+j]=(c[i+j]+x*y)%p
            work.multiplies+=1;work.additions+=1
    return trim(c)


def add_scaled(a,b,p,sign,work):
    c=[0]*max(len(a),len(b))
    for i,v in enumerate(a):c[i]=v
    for i,v in enumerate(b):c[i]=(c[i]+sign*v)%p;work.additions+=1
    return trim(c)


def three_hankel(y,base,p,work):
    """det([y_b,y_b+1,y_b+2; y_b+1,y_b+2,y_b+3; ...])."""
    a,b,c,d,e=y[base:base+5]
    t1=mul(mul(a,c,p,work),e,p,work)
    t2=mul(mul(b,c,p,work),d,p,work)
    t3=mul(mul(a,d,p,work),d,p,work)
    t4=mul(mul(b,b,p,work),e,p,work)
    t5=mul(mul(c,c,p,work),c,p,work)
    out=add_scaled(t1,t2,p,2,work)
    out=add_scaled(out,t3,p,-1,work)
    out=add_scaled(out,t4,p,-1,work)
    out=add_scaled(out,t5,p,-1,work)
    return out


def poly_gcd(a,b,p,work):
    """Monic polynomial gcd in alpha (degree <=3), counting division arithmetic."""
    a=trim(a[:]); b=trim(b[:])
    if not any(a) and not any(b):return [0]
    def degree(q):return len(q)-1 if any(q) else -1
    while degree(b)>=0:
        lead_inv=pow(b[-1],-1,p);work.inversions+=1
        while degree(a)>=degree(b):
            gap=degree(a)-degree(b)
            q=a[-1]*lead_inv%p;work.multiplies+=1
            for i,t in enumerate(b):
                a[gap+i]=(a[gap+i]-q*t)%p
                work.multiplies+=1;work.additions+=1
            trim(a)
        a,b=b,a
    lead_inv=pow(a[-1],-1,p);work.inversions+=1
    return [v*lead_inv%p for v in a]


@dataclass
class DiscoveryStats:
    samples: int=0
    shift_trials: int=0
    gcd_nonconstant: int=0
    linear_roots: int=0
    full_checks: int=0
    checked_entries: int=0
    branch: str='fallback'
    reason: str='no-certified-candidate'
    true_matches: int=0
    limit: int=45


def discover_two_defect_binomial(r,engine,work=None,max_candidates=45,probes=8):
    """Exactly sound, generically complete O(N) field-arithmetic discovery.

    Return (delta,alpha,h,support) or None. Condition for completeness:
    the true delta gives a degree-one gcd of the first two 3x3 Hankel
    determinants; their resultant in w is nonzero and degree <=45.
    This guarantees at most 45 candidate shifts require full scanning.
    On inputs outside this condition, decline and let exact FFT run.
    """
    if work is None:work=Work()
    meta=DiscoveryStats(limit=max_candidates)
    n,p=engine.n,engine.p
    if n<8 or len(r)!=n or probes<6:
        meta.reason='invalid-size';return None,meta
    R=[]
    for k in range(8):
        R.append(direct_one_frequency(r,engine.powers[k],p,work))
        meta.samples+=1
    # The root powers were already materialized for the Green engine; their
    # O(N) construction is accounted for by caller setup.
    for delta in range(1,n):
        w=engine.powers[delta]
        wk=1
        y=[]
        for k in range(6):
            y.append([R[k],(-R[k]*wk)%p]);wk=wk*w%p
            work.multiplies+=2
        P0=three_hankel(y,0,p,work)
        P1=three_hankel(y,1,p,work)
        g=poly_gcd(P0,P1,p,work)
        meta.shift_trials+=1
        if len(g)<=1:continue
        meta.gcd_nonconstant+=1
        if meta.gcd_nonconstant>max_candidates:
            meta.reason='too-many-resultant-roots'
            return None,meta
        if len(g)!=2:continue  # degree>1 may need expensive finite field factoring
        alpha=(-g[0])%p # monic
        meta.linear_roots+=1
        if alpha==0 or pow(alpha,n,p)==1:
            # One or more denominator zeros, requires separate frequency repair.
            # This phase deliberately targets the nonsingular subfamily.
            continue
        meta.full_checks+=1
        h=[];nonzero={}
        for j,v in enumerate(r):
            hv=(v-alpha*r[(j-delta)%n])%p
            work.multiplies+=1;work.additions+=1;work.reads+=2;work.writes+=1
            meta.checked_entries+=1
            h.append(hv)
            if hv:nonzero[j]=hv
            if len(nonzero)>2:break
        if 1<=len(nonzero)<=2:
            meta.branch='unknown-two-defect';meta.reason='full-defect-certified'
            meta.true_matches+=1
            return (delta,alpha,nonzero),meta
    return None,meta


def transform_phase20(engine,x,max_candidates=45):
    """Always exact: certified rational forcing or all-length Bluestein."""
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('wrong input size')
    work=Work()
    r=engine.P.apply(x)
    work.multiplies+=2*n;work.additions+=n;work.reads+=2*n;work.writes+=n
    choice,meta=discover_two_defect_binomial(r,engine,work,max_candidates)
    if choice is None:
        f,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,work.sparse)
        selection='fallback'
    else:
        d,a,entries=choice
        # Directly reconstruct F r from the certified two-sparse forcing.
        # Reusing decode_binomial's full scan is a deliberate, charged
        # independent validation and certified spectral division.
        f,dec=decode_binomial(r,d,a,1,engine,work,forcing_method='direct')
        selection='blind-two-defect'
    y=engine.L.solve(f)
    work.multiplies+=3*n+1;work.additions+=2*n;work.reads+=3*n;work.writes+=2*n
    return y, {'selected':selection,'discovery':meta,'work':work,
               'parameters':None if choice is None else (choice[0],choice[1])}
