"""Phase21: certified reciprocal sparse-rational Fourier recovery.

Given R_k=(F_N r)_k and a model R=H/Q with <=2 taps H and <=4 taps Q,
reciprocation gives 1/R=Q/H: one binomial denominator and <=4 sparse
numerator terms. A 5x5 Hankel rank gate discovers the binomial *without*
knowing either original graph factor. Every candidate is validated by a
complete cyclic convolution identity, with an exact full-FFT fallback.

This is an exact arithmetic algorithm on promised structured inputs, NOT a
worst-case sub-NlogN algorithm for arbitrary inputs.
"""
from dataclasses import dataclass
from annihilator_engine import (Work, direct_one_frequency, batch_inverse_nonzero,
    bm_prefix_candidate, sparse_direct_fourier)
from blind_sparse_rational import poly_gcd
from blind_inverse import _linear_solve, InverseStats
from resultant_gate import det_mod, interp_newton
from rational_forcing import bluestein_transform


@dataclass
class ReciprocalStats:
    probes:int=0
    nonzero_probes:bool=False
    shift_trials:int=0
    nonconstant_gcd:int=0
    linear_gcd:int=0
    prony_calls:int=0
    independent_spectral_checks:int=0
    full_certificates:int=0
    full_certificate_entries:int=0
    denominator_zeros:int=0
    short_rank:int=0
    found:bool=False
    reason:str='no-certificate'
    skip_multidegree:int=0


def det_pencil_samples(T,w,base,p,co,max_terms=4):
    """Degree<=5 determinant in unknown a: det([T_(u+i+j)*(1-a*w^(u+i+j))]).

    Interpolate the degree-five polynomial at alpha=0,1,...,5.
    2x 5x5 determinants at six scalar sample values cost O(1) for K=4.
    """
    sz=max_terms+1
    wk=[1]
    for k in range(1,base+2*max_terms+1):
        wk.append(wk[-1]*w%p);co.multiplies+=1
    vals=[]
    for alpha in range(sz+1):
        Y=[]
        for j in range(base,base+2*max_terms+1):
            Y.append(T[j]*(1-alpha*wk[j])%p)
            co.multiplies+=2;co.additions+=1
        mat=[[Y[i+j] for j in range(sz)] for i in range(sz)]
        vals.append(det_mod(mat,p,co))
    return interp_newton(vals,p,co)


def recover_four_terms(Y,powers,p,co,max_terms=4):
    """Prony root search on provided Nth roots; exact, <=4 taps.

    Returns coefficients A_j s.t. Y_k=sum A_j omega^(jk) or None. Exponent
    0 is allowed, missing/merged terms are handled by minimal recurrence.
    """
    recurrence=bm_prefix_candidate(Y[:2*max_terms],max_terms,p,co)
    if recurrence is None:return None
    d=len(recurrence)-1
    if d<=0 or d>max_terms:return None
    exps=[]
    for e,z in enumerate(powers):
        s=recurrence[0]
        for v in recurrence[1:]:
            s=(s*z+v)%p
            co.multiplies+=1;co.additions+=1
        if s==0:exps.append(e)
        # Fail quickly if root count cannot match actual recurrence degree.
        if len(exps)>d:return None
    if len(exps)!=d:return None
    nodes=[powers[e] for e in exps]
    vmat=[]
    vpower=[1]*d
    for k in range(d):
        vmat.append(vpower[:]);vpower=[vpower[j]*nodes[j]%p for j in range(d)]
        co.multiplies+=d
    coeffs=_linear_solve(vmat,Y[:d],p,co,InverseStats())
    if coeffs is None:return None
    C={e:c%p for e,c in zip(exps,coeffs) if c%p}
    if not C or len(C)>max_terms:return None
    # Match every independent probe in the supplied prefix exactly.
    term_powers={e:1 for e in C}
    for k,y in enumerate(Y):
        z=0
        for e,c in C.items():
            z=(z+c*term_powers[e])%p
            term_powers[e]=term_powers[e]*powers[e]%p
            co.multiplies+=2;co.additions+=1
        if z!=y:return None
    return C


def check_cyclic_certificate(r,A,delay,alpha,p,co):
    """Certified relation A(S)r=(I-alpha S^delay)e0, on all N positions."""
    n=len(r)
    for j in range(n):
        acc=0
        for e,c in A.items():
            acc=(acc+c*r[(j-e)%n])%p
            co.multiplies+=1;co.additions+=1;co.reads+=1
        rhs=(1 if j==0 else 0)- (alpha if j==delay else 0)
        if acc!=rhs%p:return False,j+1
    return True,n


def discover_reciprocal_union(r,engine,co=None,probes=None,max_terms=4,max_degree_candidates=None,candidate_shifts=None):
    """Linear-time field arithmetic for nondegenerate fixed-s 2/s family.

    Requires first 4s Fourier probes nonzero, gcd of two corrected
    (s+1)x(s+1) Hankel determinants linear at a correct nonzero shift,
    <=(s+1)^2(2s+1) nonconstant gcd trial shifts, and an invertible
    recovered <=s-tap cyclic operator.
    Certification is exact for all inputs; failing hypotheses cause fallback.
    """
    if co is None:co=Work()
    meta=ReciprocalStats()
    n,p=engine.n,engine.p
    needed=4*max_terms
    if max_terms<1 or n<needed or p<=max_terms+1:return None,meta
    # Two (s+1)x(s+1) Hankel determinants: resultant degree <=
    # (s+1)^2(2s+1). If identically zero, reject once too many shift
    # candidates have appeared rather than performing unbounded N scans.
    if max_degree_candidates is None:
        max_degree_candidates=(max_terms+1)**2*(2*max_terms+1)
    if probes is None:
        R=[direct_one_frequency(r,engine.powers[k],p,co) for k in range(needed)]
    else:
        if len(probes)<needed:raise ValueError('need more Fourier probes')
        R=probes[:needed]
    meta.probes=needed
    if any(x==0 for x in R):
        meta.reason='one-of-16-Fourier-probes-vanishes';return None,meta
    meta.nonzero_probes=True
    T=batch_inverse_nonzero(R,p,co)

    for delta in (candidate_shifts if candidate_shifts is not None else range(1,n)):
        if not 1<=delta<n:continue
        w=engine.powers[delta]
        P0=det_pencil_samples(T,w,0,p,co,max_terms)
        P1=det_pencil_samples(T,w,1,p,co,max_terms)
        gcd_alpha=poly_gcd(P0,P1,p,co)
        meta.shift_trials+=1
        if len(gcd_alpha)<2:continue
        meta.nonconstant_gcd+=1
        if meta.nonconstant_gcd>max_degree_candidates:
            meta.reason='too-many-rank-candidates';return None,meta
        if len(gcd_alpha)!=2:
            meta.skip_multidegree+=1
            continue
        alpha=(-gcd_alpha[0])%p
        meta.linear_gcd+=1
        if alpha==0:continue
        Y=[];wk=1
        for f in T:
            Y.append(f*(1-alpha*wk)%p)
            wk=wk*w%p
            co.multiplies+=3;co.additions+=1
        meta.prony_calls+=1
        A=recover_four_terms(Y,engine.powers,p,co,max_terms)
        if A is None:continue
        meta.independent_spectral_checks+=needed
        # Check that A is invertible on the whole cyclic Fourier subgroup;
        # without this, the relation cannot determine all spectral entries.
        Ahat=sparse_direct_fourier(A,n,engine.powers,p,co)
        meta.denominator_zeros=sum(t==0 for t in Ahat)
        if meta.denominator_zeros:continue
        meta.full_certificates+=1
        passed,checked=check_cyclic_certificate(r,A,delta,alpha,p,co)
        meta.full_certificate_entries+=checked
        if passed:
            meta.found=True;meta.short_rank=len(A)
            meta.reason='full-cyclic-certificate'
            return (A,delta,alpha,Ahat),meta
        # Uniqueness: two ratios with (2,s) sparsity matching the first
        # 4s Fourier samples and no subgroup zeros must represent the same
        # transform on ALL N roots (4s-term Vandermonde cross-product).
        # Therefore no later admissible model can pass this certificate.
        meta.reason='first-16-probes-adversary-full-certificate-failed'
        return None,meta
    meta.reason='no-certified-model'
    return None,meta


def transform_reciprocal_union(engine,x,max_terms=4):
    """Exact all-input unnormalized DFT through the project's Green identity."""
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('wrong input length')
    co=Work()
    r=engine.P.apply(x)
    co.multiplies+=2*n;co.additions+=n;co.reads+=2*n;co.writes+=n
    choice,meta=discover_reciprocal_union(r,engine,co,max_terms=max_terms)
    if choice is None:
        forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,co.sparse)
        branch='fallback'
    else:
        A,delta,alpha,Ahat=choice
        Bhat=[];wk=1;w=engine.powers[delta]
        for k in range(n):
            Bhat.append((1-alpha*wk)%p)
            wk=wk*w%p
            co.multiplies+=2;co.additions+=1
        invs=batch_inverse_nonzero(Ahat,p,co)
        forcing=[Bhat[k]*invs[k]%p for k in range(n)]
        co.multiplies+=n;co.writes+=n
        branch='reciprocal-blind-sparse-rational'
    factors=None
    if choice is not None and len(choice[0]) in (2,4,8,16):
        factors=factor_sparse_hypercube(choice[0],choice[1],choice[2],n,p,
                                      (len(choice[0]).bit_length()-1),co)
    y=engine.L.solve(forcing)
    co.multiplies+=3*n+1;co.additions+=2*n;co.reads+=3*n;co.writes+=2*n
    return y,{'selected':branch,'discovery':meta,'work':co,
              'recovered_A':None if choice is None else choice[0],
              'recovered_B':None if choice is None else (choice[1],choice[2]),
              'graph_factors':factors}


def factor_four_tap_rectangle(A,delay,alpha,n,p):
    """Recover valid two-binomial graph factorization, when one exists.

    From A(z)=c*z^b*(1-a*z^d)*(1-bb*z^e) and B=1-alpha*z^delay,
    derive Q and two impulse H. This performs <=24 assignments of four
    support taps. It never assumes uniqueness or graph factor discovery.
    A's full cyclic certificate is verified independently elsewhere.
    """
    from itertools import permutations
    if len(A)!=4:return None
    pairs=list(A)
    for base,first,second,last in permutations(pairs,4):
        if (first+second-base)%n !=last:continue
        c=A[base];d=(first-base)%n;e=(second-base)%n
        if d==0 or e==0:continue
        if c*A[last]%p != A[first]*A[second]%p:continue
        invc=pow(c,-1,p)
        a=(-A[first]*invc)%p;b=(-A[second]*invc)%p
        # Re-expand explicitly, rejecting coincident/merged terms.
        target={base:c%p,(base+d)%n:(-c*a)%p,
                (base+e)%n:(-c*b)%p,
                (base+d+e)%n:(c*a*b)%p}
        if target!=A:continue
        u=(-base)%n;h1=invc;v=(u+delay)%n;h2=(-alpha*invc)%p
        if v==u:continue
        return {'shifts':(d,e),'multipliers':(a,b),
                'defects':{u:h1,v:h2},'rectangle_base':base}
    return None


def factor_sparse_hypercube(A,delay,alpha,n,p,number_of_factors,co=None):
    """Find *a* graph-factor decomposition of the certified A, if it exists.

    If |supp A|=2**t and Q(z)=prod_i(1-a_i*z**d_i) has no support
    collisions, enumerate the cube origin and t incident edges. This
    is O_t(1) field work independent of N, but not a unique-factor theorem.
    """
    from itertools import permutations
    t=number_of_factors
    if not 1<=t<=6 or len(A)!=1<<t:return None
    support=list(A)
    for origin in support:
        rest=[j for j in support if j!=origin]
        for edges in permutations(rest,t):
            c=A[origin]
            cinv=pow(c,-1,p)
            if co:co.inversions+=1
            ds=[(edge-origin)%n for edge in edges]
            aa=[(-A[edge]*cinv)%p for edge in edges]
            if co:co.multiplies+=t
            terms={origin:c}
            for d,a in zip(ds,aa):
                newterms=dict(terms)
                for exp,val in terms.items():
                    nex=(exp+d)%n
                    newterms[nex]=(newterms.get(nex,0)-a*val)%p
                    if co:co.multiplies+=1;co.additions+=1
                terms=newterms
            terms={e:c0 for e,c0 in terms.items() if c0}
            if terms!=A:continue
            u=(-origin)%n;v=(u+delay)%n
            if u==v:continue
            return {'shifts':tuple(ds),'multipliers':tuple(aa),
                    'defects':{u:cinv,v:(-alpha*cinv)%p},
                    'cube_origin':origin}
    return None
