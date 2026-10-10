"""Phase22: exact trace-quotient sieve for Phase21 self-reciprocal resultants.

If U(w)=w**b V(w+w**(-1)), and a nontrivial Nth root of unity
annihilates U, then gcd(V_*(t), D_N(t)-2) != 1, where V_* has all
factors t-2 removed and D_N(t)=w**N+w**(-N) at t=w+w**(-1).

The converse at the level of roots in the algebraic closure holds, but
for recovery we require roots to lie in the supplied subgroup in F_p.
The present module supplies a *deterministic, no-false-rejection* filter,
not a new generic FFT algorithm.
"""
from dataclasses import dataclass
from annihilator_engine import Work


def trim(a,p):
    a=[x%p for x in a]
    while a and a[-1]==0:
        a.pop()
    return a


def add_constant(a,c,p,co):
    b=list(a) if a else [0]
    b[0]=(b[0]+c)%p
    co.additions+=1
    return trim(b,p)


def add_scaled(a,b,scale,p,co):
    z=[0]*max(len(a),len(b))
    for i in range(len(z)):
        v=a[i] if i<len(a) else 0
        if i<len(b):
            v=(v+scale*b[i])%p
            co.multiplies+=1;co.additions+=1
        z[i]=v
    return trim(z,p)


def divmod_poly(a,b,p,co):
    """Exact ordinary long division of low-degree field polynomials."""
    a=trim(a,p);b=trim(b,p)
    if not b:raise ZeroDivisionError('zero polynomial')
    if len(a)<len(b):return [],a
    inv=pow(b[-1],-1,p);co.inversions+=1
    q=[0]*(len(a)-len(b)+1)
    while len(a)>=len(b):
        i=len(a)-len(b)
        v=a[-1]*inv%p;co.multiplies+=1
        q[i]=v
        for j in range(len(b)):
            a[i+j]=(a[i+j]-v*b[j])%p
            co.multiplies+=1;co.additions+=1
        while a and a[-1]==0:a.pop()
    return trim(q,p),a


def gcd_poly(a,b,p,co):
    a=trim(a,p);b=trim(b,p)
    while b:
        _,r=divmod_poly(a,b,p,co)
        a,b=b,r
    if not a:return []
    inv=pow(a[-1],-1,p);co.inversions+=1
    co.multiplies+=len(a)
    return trim([v*inv%p for v in a],p)


def remove_t_two(a,p,co):
    """Remove all (t-2) factors, since w+w^-1=2 iff w=1."""
    a=trim(a,p)
    removed=0
    while len(a)>1:
        # Synthetic division by (t-2): q[k-1] = a[k], q[j-1]=a[j]+2*q[j]
        d=len(a)-1
        q=[0]*d
        q[-1]=a[-1]
        for j in range(d-1,0,-1):
            q[j-1]=(a[j]+2*q[j])%p
            co.multiplies+=1;co.additions+=1
        rem=(a[0]+2*q[0])%p
        co.multiplies+=1;co.additions+=1
        if rem:break
        a=trim(q,p);removed+=1
    return a,removed


def modmul(a,b,mod,p,co):
    """Dense schoolbook product followed by reduction by monic mod."""
    deg=len(mod)-1
    if deg<=0:return []
    if not a or not b:return []
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        if not x:continue
        for j,y in enumerate(b):
            out[i+j]=(out[i+j]+x*y)%p
            co.multiplies+=1;co.additions+=1
    for k in range(len(out)-1,deg-1,-1):
        c=out[k]
        if not c:continue
        h=k-deg
        for j in range(deg):
            out[h+j]=(out[h+j]-c*mod[j])%p
            co.multiplies+=1;co.additions+=1
        out[k]=0
    return trim(out[:deg],p)


def monic(a,p,co):
    a=trim(a,p)
    if not a:return []
    if a[-1]==1:return a
    inv=pow(a[-1],-1,p);co.inversions+=1
    co.multiplies+=len(a)
    return [x*inv%p for x in a]


def dickson_n_mod(n,mod,p,co):
    """Compute D_n(t) mod `mod`, D_n(z+z^-1)=z^n+z^-n.

    Binary pair recurrence takes <=3 modular polynomial products per bit.
    """
    if n<0:raise ValueError('negative N')
    mod=monic(mod,p,co)
    if len(mod)<=1:return []
    # D_0=2, D_1=t; reduce t in exceptional degree-1 quotient.
    two=trim([2],p)
    t=divmod_poly([0,1],mod,p,co)[1]
    if n == 0:
        return two
    # Dyadic lengths need only one modular square per doubling. In particular,
    # this saves two polynomial products per bit on the 2^k FFT family.
    if n & (n-1) == 0:
        a=t
        for _ in range(n.bit_length()-1):
            a=add_constant(modmul(a,a,mod,p,co),-2,p,co)
        return a
    a,b=two,t
    for bit in bin(n)[2:]:
        a2=add_constant(modmul(a,a,mod,p,co),-2,p,co)
        ab=add_scaled(modmul(a,b,mod,p,co),t,-1,p,co)
        b2=add_constant(modmul(b,b,mod,p,co),-2,p,co)
        if bit=='0':a,b=a2,ab
        else:a,b=ab,b2
    return a


@dataclass
class TraceSieveReport:
    possible:bool
    gcd_degree:int
    trace_degree:int
    removed_identity_factors:int
    gcd_coefficients:tuple
    incremental_ops:int


def trace_subgroup_sieve(V,n,p,co=None):
    """Sound filter: rejects only if no non-identity Nth-root annihilates U.

    May admit candidates in an extension field instead of the base field;
    these false-positive sieves are harmless (the original root scan runs).
    """
    if co is None:co=Work()
    start=co.arithmetic()
    if n<1 or p<3 or p%2==0:raise ValueError('odd prime field required')
    V=trim(V,p)
    if not V:raise ValueError('V identically zero: fallback, do not use sieve')
    V,removed=remove_t_two(V,p,co)
    if len(V)<=1:
        return TraceSieveReport(False,0,0,removed,(1,),co.arithmetic()-start)
    V=monic(V,p,co)
    d=dickson_n_mod(n,V,p,co)
    h=add_constant(d,-2,p,co)
    g=gcd_poly(V,h,p,co)
    return TraceSieveReport(len(g)>1,len(g)-1,len(V)-1,
                            removed,tuple(g),co.arithmetic()-start)


def direct_dickson(n,t,p):
    if n==0:return 2%p
    if n==1:return t%p
    a=2;b=t%p
    for _ in range(2,n+1):a,b=b,(t*b-a)%p
    return b


def charged_power(a,n,p,co):
    if n<0:raise ValueError('negative exponent')
    b=a%p;z=1
    while n:
        if n&1:
            z=z*b%p;co.multiplies+=1
        n//=2
        if n:
            b=b*b%p;co.multiplies+=1
    return z


def modular_sqrt(a,p,co):
    """Tonelli-Shanks. Return a square root or None, with field cost counted."""
    a%=p
    if a==0:return 0
    if charged_power(a,(p-1)//2,p,co)!=1:return None
    if p%4==3:
        x=charged_power(a,(p+1)//4,p,co)
        co.multiplies+=1
        assert x*x%p==a
        return x
    q=p-1;s=0
    while q%2==0:q//=2;s+=1
    z=2
    while charged_power(z,(p-1)//2,p,co)!=p-1:
        z+=1
    c=charged_power(z,q,p,co)
    x=charged_power(a,(q+1)//2,p,co)
    t=charged_power(a,q,p,co)
    m=s
    while t!=1:
        j=0;u=t
        while u!=1 and j<m:
            u=u*u%p;co.multiplies+=1;j+=1
        if j==m:raise ArithmeticError('Tonelli-Shanks internal nonresidue')
        b=c
        for _ in range(m-j-1):
            b=b*b%p;co.multiplies+=1
        x=x*b%p;co.multiplies+=1
        b2=b*b%p;co.multiplies+=1
        t=t*b2%p;co.multiplies+=1
        c=b2;m=j
    co.multiplies+=1
    assert x*x%p==a
    return x


def discrete_logs_bsgs(targets,omega,n,p,co):
    """Charge construction and lookup of a size ~sqrt(N) baby-step table.

    Canonical small machine-word field elements permit expected O(1) integer
    dictionary lookups (Python uses deterministic integer hashing here).
    Worst-case deterministic replacement: sorting and binary search in
    O(sqrt(N) log N) word comparisons, which is still o(N) for fixed targets.
    """
    if not targets:return {}
    from math import isqrt
    m=isqrt(n)+1
    baby={};v=1
    for j in range(m):
        if v not in baby:baby[v]=j;co.writes+=1
        v=v*omega%p;co.multiplies+=1;co.reads+=1
    step=charged_power(omega,(n-m)%n,p,co)
    out={}
    for target in targets:
        g=target%p
        if g==0:continue
        for i in range((n+m-1)//m+1):
            co.comparisons+=1;co.reads+=1
            if g in baby:
                d=(i*m+baby[g])%n
                if charged_power(omega,d,p,co)==target%p:
                    out[target%p]=d
                    break
            g=g*step%p;co.multiplies+=1
    return out


def shifts_from_linear_trace_gcd(report,engine,co):
    """Returns complete list of admissible nonidentity shift exponents.

    Call ONLY when trace gcd degree is 1. This branch is exact and requires
    no N-point evaluation. Degree >1 needs polynomial factorization, so the
    caller instead uses the original certified all-N scan.
    """
    if report.gcd_degree!=1:raise ValueError('linear gcd required')
    n,p=engine.n,engine.p
    a0,a1=report.gcd_coefficients
    assert a1==1
    t=(-a0)%p
    disc=(t*t-4)%p;co.multiplies+=1;co.additions+=1
    root=modular_sqrt(disc,p,co)
    if root is None:return []  # no base-field candidate, so no subgroup candidate
    inv2=(p+1)//2  # 2^-1 for odd prime p; fixed field constant
    roots={((t+root)*inv2)%p,((t-root)*inv2)%p}
    co.multiplies+=2;co.additions+=2
    roots.discard(1) # the identity shift is forbidden
    # Roots in F_p outside <omega> also have no admissible shift exponent.
    roots={w for w in roots if charged_power(w,n,p,co)==1}
    m=discrete_logs_bsgs(roots,engine.omega,n,p,co)
    return sorted({d for d in m.values() if 1<=d<n})


def shifts_from_trace_gcd_scan(report,engine,co):
    """Complete deterministic shift enumeration for arbitrary trace-gcd degree.

    Uses inversion symmetry to inspect floor(N/2) trace points, rather than
    N resultant evaluations. The trace gcd has degree <= b_s.
    """
    if report.gcd_degree<1:return []
    n,p=engine.n,engine.p
    g=report.gcd_coefficients
    out=[]
    for delta in range(1,n//2+1):
        w=engine.powers[delta]
        invw=engine.powers[(n-delta)%n]
        t=(w+invw)%p
        co.additions+=1;co.reads+=2
        v=0
        for c in reversed(g):
            v=(v*t+c)%p
            co.multiplies+=1;co.additions+=1
        if v==0:
            out.append(delta)
            if delta!=n-delta:out.append(n-delta)
    return sorted(out)
