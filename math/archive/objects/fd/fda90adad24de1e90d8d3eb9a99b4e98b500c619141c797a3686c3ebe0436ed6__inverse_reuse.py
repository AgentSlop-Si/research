"""Hero #1 Phase20 shared-probe adaptation of Phase19: fully blind sparse *circular inverse* Fourier transform.

If C(S)r=e_0 and C has <=s nonzero coefficients, discover C from only 2s
ordinary Fourier samples of r, via Prony/Berlekamp-Massey and subgroup
root enumeration, certify C(S)r=e_0 on all N coordinates, and evaluate
Fr[k]=1/C(omega**k) in O(sN+s**3) field arithmetic.

This includes unknown products of constant many long graph binomials with
ONE impulsive forcing defect, even if neither factor alone compresses r.
For arbitrary input, certificate failure causes a full exact FFT fallback.
"""
from dataclasses import dataclass
from annihilator_engine import (
    RecurrenceGreen,Work,batch_inverse_nonzero,
    bm_prefix_candidate,direct_one_frequency,sparse_direct_fourier,
)
from rational_forcing import bluestein_transform


@dataclass
class InverseStats:
    sample_count: int = 0
    inverse_support: int = 0
    root_candidates: int = 0
    root_scan_multiplies: int = 0
    root_scan_additions: int = 0
    support_checks: int = 0
    certificate_entries_checked: int = 0
    certificate_failed_at: int | None = None
    fallback_reason: str | None = None
    interpolation_pivots: int = 0
    bad_initial_fourier_samples: int = 0


def _linear_solve(mat,vec,p,co,meta):
    """Exact modular Gaussian elimination; pivoting and every op charged."""
    d=len(vec)
    a=[[(v%p) for v in mat[i]]+[vec[i]%p] for i in range(d)]
    for i in range(d):
        pivot=next((j for j in range(i,d) if a[j][i]),None)
        if pivot is None:return None
        if pivot!=i:a[i],a[pivot]=a[pivot],a[i]
        meta.interpolation_pivots+=1
        inv=pow(a[i][i],-1,p)
        co.inversions+=1
        for k in range(i,d+1):
            a[i][k]=a[i][k]*inv%p
            co.multiplies+=1
        for j in range(i+1,d):
            mult=a[j][i]
            if not mult:continue
            for k in range(i,d+1):
                a[j][k]=(a[j][k]-mult*a[i][k])%p
                co.multiplies+=1;co.additions+=1
    res=[0]*d
    for i in range(d-1,-1,-1):
        v=a[i][d]
        for j in range(i+1,d):
            v=(v-a[i][j]*res[j])%p
            co.multiplies+=1;co.additions+=1
        res[i]=v
    return res


def discover_sparse_circular_inverse_reuse(r,engine,max_taps,work=None,meta=None,frequency_prefix=None):
    """Find and *certify* sparse C with sum_e C[e]r[j-e]=[j==0].

    Returns dictionary exponent -> coefficient or None. Soundness is exact
    because every output coordinate is independently checked. The promised
    s-sparse invertible case is complete when 2s<=N and field roots exist.
    """
    if work is None:work=Work()
    if meta is None:meta=InverseStats()
    n,p=engine.n,engine.p
    s=int(max_taps)
    if len(r)!=n or s<1 or 2*s>n:
        meta.fallback_reason='invalid-size-or-tap-limit'
        return None,meta
    # Exactly 2s direct Fourier probes. No hidden length-N FFT here.
    frequencies=[]
    if frequency_prefix is not None and len(frequency_prefix)<2*s:
        raise ValueError('short precomputed frequency prefix')
    for k in range(2*s):
        value=(frequency_prefix[k] if frequency_prefix is not None
               else direct_one_frequency(r,engine.powers[k],p,work))
        meta.sample_count+=1
        if not value:
            meta.bad_initial_fourier_samples+=1
            meta.fallback_reason='zero-Fourier-probe'
            return None,meta
        frequencies.append(value)
    inverse_samples=batch_inverse_nonzero(frequencies,p,work)
    # Prony: inverse_samples[k] = sum_e C[e]*(omega**e)**k.
    recurrence=bm_prefix_candidate(inverse_samples,s,p,work)
    if recurrence is None or not 1<len(recurrence)<=s+1:
        meta.fallback_reason='invalid-short-recurrence'
        return None,meta
    degree=len(recurrence)-1
    if recurrence[0]!=1 or recurrence[-1]%p==0:
        meta.fallback_reason='nonminimal-short-recurrence'
        return None,meta
    # Recurrence coefficients [1,c1,..,cd] define root polynomial
    # lambda**d+c1*lambda**(d-1)+...+cd. Search all N known roots.
    exponents=[]
    for e,z in enumerate(engine.powers):
        val=recurrence[0]
        for ci in recurrence[1:]:
            val=(val*z+ci)%p
            work.multiplies+=1;work.additions+=1
            meta.root_scan_multiplies+=1;meta.root_scan_additions+=1
        if not val:exponents.append(e)
        meta.root_candidates+=1
    if len(exponents)!=degree:
        meta.fallback_reason='roots-not-all-Nth-roots'
        return None,meta
    lambdas=[engine.powers[e] for e in exponents]
    # Unique distinct nodes imply invertible Vandermonde.
    vandermonde=[]
    powers=[1]*degree
    for k in range(degree):
        vandermonde.append(powers[:])
        powers=[powers[j]*lambdas[j]%p for j in range(degree)]
        work.multiplies+=degree
    coefficients=_linear_solve(vandermonde,inverse_samples[:degree],p,work,meta)
    if coefficients is None or any(c%p==0 for c in coefficients):
        meta.fallback_reason='singular-or-degenerate-interpolation'
        return None,meta
    C={e:c%p for e,c in zip(exponents,coefficients)}
    meta.inverse_support=len(C)
    # All-input safety gate. A wrong inferred inverse can NEVER be accepted:
    # check the entire vector, including every wrap and every input entry.
    for j in range(n):
        value=0
        for e,c in C.items():
            value=(value+c*r[(j-e)%n])%p
            work.multiplies+=1;work.additions+=1;work.reads+=1
            meta.support_checks+=1
        meta.certificate_entries_checked+=1
        if value != (1 if j==0 else 0):
            meta.certificate_failed_at=j
            meta.fallback_reason='full-convolution-certificate-failed'
            return None,meta
    return C,meta


def sparse_inverse_forcing(C,engine,work=None):
    """Fr[k] = 1/C(omega**k), with all denominators certified nonzero."""
    if work is None:work=Work()
    n,p=engine.n,engine.p
    values=sparse_direct_fourier(C,n,engine.powers,p,work)
    if any(v==0 for v in values):
        # Algebraically impossible after successful C(S)r=e0 certificate.
        raise ArithmeticError('certified circular inverse has zero spectrum')
    result=batch_inverse_nonzero(values,p,work)
    return result


