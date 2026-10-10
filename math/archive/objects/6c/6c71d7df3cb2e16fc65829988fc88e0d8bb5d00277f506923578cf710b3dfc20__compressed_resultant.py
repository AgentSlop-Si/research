"""Proved reciprocal-resultant compression for blind 2/s sparse-rational FFTs.

For Hankel order m=s+1, the fixed-degree Sylvester resultant satisfies
  T(w)=w^v (w-1)^(m^2) U(w),
  v=s(s+1)(4s+5)/6,
  U(w)=w^b V(w+1/w), b=sum_{j=1}^s j^2.
The identity is universal, not a fitted degree/palindrome assumption.
It is proved in THEOREM.md by Cauchy-Binet, Newton polygons and reciprocity.

Only b+1 exact determinant evaluations recover V, versus the D+1
naive samples of the conservative degree bound D=m^2(2m-1).
Full cyclic convolution certification and an ordinary FFT fallback remain.
"""
from dataclasses import dataclass
from math import comb
from annihilator_engine import Work, direct_one_frequency, batch_inverse_nonzero
from resultant_pattern import res_at
from resultant_gate import sparse_group_eval
from reciprocal_union import discover_reciprocal_union, factor_sparse_hypercube
from rational_forcing import bluestein_transform

@dataclass
class CompressedMeta:
    dot_probes:int=0
    resultant_samples:int=0
    witness_samples:int=0
    compressed_degree:int=0
    compressed_terms:int=0
    zero_factor:int=0
    one_factor:int=0
    root_candidates:int=0
    selected:str='fallback'
    reason:str='not-certified'
    full_certificates:int=0
    full_certificate_entries:int=0
    interpolation_distinct:bool=False


def charged_pow(x,e,p,co):
    """Square-and-multiply with every modular product counted."""
    v=1;b=x%p
    while e:
        if e&1:
            v=v*b%p;co.multiplies+=1
        e>>=1
        if e:
            b=b*b%p;co.multiplies+=1
    return v


def interpolate_nodes(xs,ys,p,co):
    """Exact Newton interpolation at arbitrary distinct x nodes."""
    n=len(xs)
    if len(ys)!=n or len(set(xs))!=n:
        raise ValueError('non-distinct interpolation nodes')
    inverses=[];denoms=[]
    for j in range(1,n):
        for i in range(j,n):
            denoms.append((xs[i]-xs[i-j])%p);co.additions+=1
    inverses=batch_inverse_nonzero(denoms,p,co)
    dd=ys[:];q=0
    for j in range(1,n):
        for i in range(n-1,j-1,-1):
            dd[i]=(dd[i]-dd[i-1])*inverses[q+(i-j)]%p
            co.multiplies+=1;co.additions+=1
        q+=n-j
    # Above inverse-index ordering is j-specific ascending i, safe.
    out=[0]*n
    basis=[1]
    for j in range(n):
        for i,c in enumerate(basis):
            out[i]=(out[i]+c*dd[j])%p
            co.multiplies+=1;co.additions+=1
        if j==n-1:break
        nx=[0]*(len(basis)+1)
        for i,c in enumerate(basis):
            nx[i]=(nx[i]-xs[j]*c)%p
            nx[i+1]=(nx[i+1]+c)%p
            co.multiplies+=1;co.additions+=2
        basis=nx
    return out


def eval_horner(coeff,t,p,co):
    v=0
    for c in coeff[::-1]:
        v=(v*t+c)%p
        co.multiplies+=1;co.additions+=1
    return v


def to_palindromic_coeff(V,p,co):
    """w^b V(w+1/w), linear combination of short binomial expansions."""
    b=len(V)-1
    U=[0]*(2*b+1)
    for j,v in enumerate(V):
        for k in range(j+1):
            exponent=b+j-2*k
            U[exponent]=(U[exponent]+v*comb(j,k))%p
            co.multiplies+=1;co.additions+=1
    return U


def sample_distinct_reciprocals(count,p,co):
    """Pick w !=0,1 with distinct w+w^-1; bound 2*count+constant trials."""
    wlist=[];nodes=[];seen=set();w=2
    while len(wlist)<count and w<p:
        inv=pow(w,-1,p);co.inversions+=1
        node=(w+inv)%p;co.additions+=1
        if node not in seen:
            seen.add(node);wlist.append(w);nodes.append(node)
        w+=1
    if len(wlist)<count:return None,None
    return wlist,nodes


def compressed_U_from_inverse_probes(T,p,s,co,extra_witness=3):
    """Construct exact U coefficients from b+1 determinant values.

    The factor structure is mathematical, not a heuristic extrapolation.
    Extra independent evaluations defend against implementation bugs.
    """
    m=s+1;q=m*m
    v=s*(s+1)*(4*s+5)//6
    b=s*(s+1)*(2*s+1)//6
    wlist,ts=sample_distinct_reciprocals(b+1+extra_witness,p,co)
    if not wlist:return None,None
    denoms=[];resvals=[]
    for w in wlist:
        rw=res_at(T,w,p,co,s)
        den=charged_pow(w,v+b,p,co)*charged_pow((w-1)%p,q,p,co)%p
        co.multiplies+=1
        if den==0:raise AssertionError('nonzero interpolation denominator')
        denoms.append(den);resvals.append(rw)
    invs=batch_inverse_nonzero(denoms,p,co)
    vals=[(r*iv)%p for r,iv in zip(resvals,invs)]
    co.multiplies+=len(vals)
    V=interpolate_nodes(ts[:b+1],vals[:b+1],p,co)
    for j in range(b+1,len(wlist)):
        if eval_horner(V,ts[j],p,co)!=vals[j]:
            raise AssertionError('universal resultant factorization / implementation error')
    U=to_palindromic_coeff(V,p,co)
    if any(U[j]!=U[-1-j] for j in range(len(U)//2)):
        raise AssertionError('recovered residual polynomial not palindromic')
    return U,{'v':v,'q':q,'b':b,'samples':b+1,
              'witnesses':extra_witness,'symmetric_degree':2*b,
              'nonzero_coefficients':sum(x!=0 for x in U)}


def discover_compressed_reciprocal(r,engine,co=None,s=4):
    if co is None:co=Work()
    meta=CompressedMeta()
    n,p=engine.n,engine.p
    b=s*(s+1)*(2*s+1)//6
    if not 1<=s<=8 or n<4*s or p<=4*b+20:
        meta.reason='invalid-size-or-field';return None,meta
    R=[direct_one_frequency(r,engine.powers[k],p,co) for k in range(4*s)]
    meta.dot_probes=4*s
    if not all(R):
        meta.reason='zero-Fourier-probe';return None,meta
    T=batch_inverse_nonzero(R,p,co)
    U,detail=compressed_U_from_inverse_probes(T,p,s,co)
    if U is None or not any(U):
        meta.reason='identically-zero-resultant';return None,meta
    meta.resultant_samples=detail['samples']
    meta.witness_samples=detail['witnesses']
    meta.compressed_degree=detail['symmetric_degree']
    meta.compressed_terms=detail['nonzero_coefficients']
    meta.zero_factor=detail['v'];meta.one_factor=detail['q']
    meta.interpolation_distinct=True
    # Roots of U at the Nth roots correspond exactly to admissible w roots of
    # the full resultant, since w^v(w-1)^q is invertible for 1<=delta<N.
    values,_=sparse_group_eval(U,engine,co)
    candidates=[i for i in range(1,n) if values[i]==0]
    meta.root_candidates=len(candidates)
    # After removing universal factors, a nonzero U has degree <= 2*b.
    if len(candidates)>2*b:
        meta.reason='candidate-bound';return None,meta
    found,detail2=discover_reciprocal_union(r,engine,co,probes=R,
                          max_terms=s,candidate_shifts=candidates)
    meta.selected='certified' if found else 'fallback'
    meta.reason=detail2.reason
    meta.full_certificates=detail2.full_certificates
    meta.full_certificate_entries=detail2.full_certificate_entries
    return found,meta


def transform_compressed_reciprocal(engine,x,s=4):
    n,p=engine.n,engine.p
    if len(x)!=n:raise ValueError('wrong input')
    co=Work();r=engine.P.apply(x)
    co.multiplies+=2*n;co.additions+=n;co.reads+=2*n;co.writes+=n
    found,meta=discover_compressed_reciprocal(r,engine,co,s)
    if found is None:
        forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,co.sparse)
        selection='fallback';factors=None
    else:
        A,delta,alpha,Ahat=found
        factors=factor_sparse_hypercube(A,delta,alpha,n,p,
                (len(A).bit_length()-1),co) if len(A) in (2,4,8,16) else None
        b=[];wk=1;w=engine.powers[delta]
        for k in range(n):
            b.append((1-alpha*wk)%p)
            wk=wk*w%p
            co.multiplies+=2;co.additions+=1
        inv=batch_inverse_nonzero(Ahat,p,co)
        forcing=[b[k]*inv[k]%p for k in range(n)]
        co.multiplies+=n;co.writes+=n
        selection='compressed-reciprocal-certified'
    y=engine.L.solve(forcing)
    co.multiplies+=3*n+1;co.additions+=2*n;co.reads+=3*n;co.writes+=2*n
    return y,{'selected':selection,'meta':meta,'work':co,'graph_factors':factors}
