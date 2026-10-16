"""Compressed resultant gate for Phase20's unknown one-binomial/two-defect route.

Two Hankel determinants are cubics in alpha and polynomials of degree
<=6 and <=9 respectively in w. Their Sylvester resultant is a degree
<=45 polynomial in w. Interpolate it at 46 fixed non-group nodes,
then find all its Nth-root zeroes via a *charged sparse Fourier evaluator*.
This is O(N) field arithmetic at fixed K=2, not a hidden full-N FFT.
"""
from dataclasses import dataclass
from math import gcd
from blind_sparse_rational import three_hankel,poly_gcd
from annihilator_engine import Work,direct_one_frequency,decode_binomial
from rational_forcing import bluestein_transform,forcing_from_sparse
from green_sparse import SparseInputDFT, Cost

D=45

@dataclass
class ResStats:
    probes:int=0
    interp_degree:int=-1
    interpolations:int=0
    witness_checks:int=0
    root_candidates:int=0
    gcd_linear:int=0
    full_defect_scans:int=0
    spectral_rejections:int=0
    entries_verified:int=0
    selected:str='fallback'
    factor_at_zero:int=0
    factor_at_one:int=0
    reciprocal_quotient:bool=False
    reduced_degree:int=-1
    reason:str='no-certified-candidate'
    root_eval_ops:int=0


def poly_alpha(R,w,p,b,work):
    powers=[1]
    for k in range(1,6):
        powers.append(powers[-1]*w%p)
        work.multiplies+=1
    y=[[R[k],(-R[k]*powers[k])%p] for k in range(6)]
    work.multiplies+=6
    return three_hankel(y,b,p,work)


def det_mod(a,p,work):
    a=[row[:] for row in a]
    n=len(a);det=1
    for i in range(n):
        piv=next((j for j in range(i,n) if a[j][i]),None)
        if piv is None:return 0
        if piv!=i:
            a[i],a[piv]=a[piv],a[i];det=-det
        pivot=a[i][i]
        det=det*pivot%p;work.multiplies+=1
        inv=pow(pivot,-1,p);work.inversions+=1
        for j in range(i+1,n):
            fact=a[j][i]*inv%p;work.multiplies+=1
            if fact:
                for k in range(i+1,n):
                    a[j][k]=(a[j][k]-fact*a[i][k])%p
                    work.multiplies+=1;work.additions+=1
    return det%p


def resultant_at(R,w,p,work):
    a=poly_alpha(R,w,p,0,work)
    b=poly_alpha(R,w,p,1,work)
    aa=list(reversed(a+[0]*(4-len(a))))
    bb=list(reversed(b+[0]*(4-len(b))))
    syl=[]
    for c in (aa,bb):
        for t in range(3):syl.append([0]*t+c+[0]*(2-t))
    return det_mod(syl,p,work)


def interp_newton(y,p,work):
    """Interpolate polynomial of degree at most len(y)-1 at nodes 0..d."""
    d=len(y)-1
    dd=y[:]
    inverses=[0]+[pow(j,-1,p) for j in range(1,d+1)]
    work.inversions+=d
    for j in range(1,d+1):
        inv=inverses[j]
        for i in range(d,j-1,-1):
            dd[i]=(dd[i]-dd[i-1])*inv%p
            work.additions+=1;work.multiplies+=1
    out=[0]*(d+1)
    basis=[1]
    for j in range(d+1):
        for i,z in enumerate(basis):
            out[i]=(out[i]+z*dd[j])%p
            work.multiplies+=1;work.additions+=1
        if j==d:break
        nxt=[0]*(len(basis)+1)
        for i,z in enumerate(basis):
            nxt[i]=(nxt[i]-j*z)%p
            nxt[i+1]=(nxt[i+1]+z)%p
            work.multiplies+=1;work.additions+=2
        basis=nxt
    while out and out[-1]==0:out.pop()
    return out


def strip_trivial_factors(coeff,p,work):
    """Remove only factors known nonzero on trial shifts:
       w=omega**delta !=0 and !=1 for 1<=delta<N.

    Fully reconstructing the resultant first means each division is an
    exact per-instance proof, not an assumed universal factorization.
    """
    coeff=coeff[:]
    zeros=0
    while coeff and coeff[0]==0:
        coeff.pop(0);zeros+=1
    ones=0
    while len(coeff)>1 and sum(coeff)%p==0:
        q=[0]*(len(coeff)-1)
        acc=coeff[-1]
        for i in range(len(coeff)-2,-1,-1):
            q[i]=acc
            acc=(acc+coeff[i])%p
            work.additions+=1
        assert acc==0
        coeff=q;ones+=1
    return coeff,zeros,ones


def eval_poly(x,coeff,p,work):
    r=0
    for c in reversed(coeff):
        r=(r*x+c)%p
        work.multiplies+=1;work.additions+=1
    return r


def sparse_group_eval(coeff,engine,work):
    n,p=engine.n,engine.p
    entries={j%n:v%p for j,v in enumerate(coeff) if v%p}
    if n and len(entries)<len([v for v in coeff if v%p]):
        # Wrap-coeff collision
        entries={}
        for j,v in enumerate(coeff):
            jj=j%n;entries[jj]=(entries.get(jj,0)+v)%p
        entries={j:v for j,v in entries.items() if v}
    if n&(n-1)==0:
        f,cc=SparseInputDFT(n,engine.omega,p).from_entries(entries)
        # root powers already made by engine and charged as setup, but pruned
        # evaluator charges its own root table in Cost: do not double charge.
        work.multiplies+=cc.ntt_mults
        work.additions+=cc.ntt_adds
        work.reads+=cc.split_entries+cc.node_size_sum
        work.writes+=cc.output_writes
        return f,cc.arithmetic()
    f,stats=forcing_from_sparse(entries,n,engine.omega,p,engine.primitive_gen,work.sparse)
    return f,stats.total_field_ops()


def hankel_numeric(seq,base,p,work):
    """Numerical 3x3 Hankel determinant, including all field operations."""
    a,b,c,d,e=seq[base:base+5]
    result=(a*c*e+2*b*c*d-a*d*d-b*b*e-c*c*c)%p
    work.multiplies+=12;work.additions+=4
    return result


def discover_resultant(r,engine,work=None,frequency_prefix=None):
    if work is None:work=Work()
    meta=ResStats()
    n,p=engine.n,engine.p
    if n<8 or p<=D+10:
        meta.reason='unsupported-size-or-field';return None,meta
    if frequency_prefix is None:
        R=[direct_one_frequency(r,engine.powers[k],p,work) for k in range(8)]
    else:
        if len(frequency_prefix)<8:raise ValueError('need eight supplied probes')
        R=frequency_prefix[:8]
    meta.probes=len(R)
    vals=[resultant_at(R,w,p,work) for w in range(D+1)]
    coeff=interp_newton(vals,p,work)
    meta.interpolations=D+1
    meta.interp_degree=len(coeff)-1
    if not coeff:
        meta.reason='identically-zero-resultant';return None,meta
    # Independent evaluation at noninterpolation points guards algorithmic code.
    for w in (D+1,D+2,D+3):
        if eval_poly(w,coeff,p,work)!=resultant_at(R,w,p,work):
            raise AssertionError('invalid resultant degree/interpolation')
        meta.witness_checks+=1
    # Omit zero/one shift-root factors, never cancelling any admissible
    # graph delay (w is a nontrivial Nth root of unity).
    coeff,z,o=strip_trivial_factors(coeff,p,work)
    meta.factor_at_zero=z;meta.factor_at_one=o
    meta.reduced_degree=len(coeff)-1
    meta.reciprocal_quotient=(coeff==coeff[::-1])
    vals,subcost=sparse_group_eval(coeff,engine,work)
    meta.root_eval_ops=subcost
    positions=[d for d in range(1,n) if vals[d]==0]
    meta.root_candidates=len(positions)
    if len(positions)>D:
        meta.reason='resultant-root-bound-violated';return None,meta
    for d in positions:
        w=engine.powers[d]
        a=poly_alpha(R,w,p,0,work)
        b=poly_alpha(R,w,p,1,work)
        g=poly_gcd(a,b,p,work)
        if len(g)!=2:continue
        meta.gcd_linear+=1
        alpha=(-g[0])%p
        if alpha==0:continue
        # Two unused Fourier probes protect against spurious solutions of
        # only the first two Hankel determinant equations. This is NOT
        # sufficient alone: full time-domain support verification follows.
        wpower=1;adjusted=[]
        for f in R:
            adjusted.append(f*(1-alpha*wpower)%p)
            wpower=wpower*w%p
            work.multiplies+=3;work.additions+=1
        if any(hankel_numeric(adjusted,k,p,work) for k in (2,3)):
            meta.spectral_rejections+=1
            continue
        # There are g singular frequencies iff alpha**(n//g) == 1,
        # where g=gcd(d,n); otherwise there are none. Keep the existing
        # charged direct Fourier repair when g=1 and reject only multipoles.
        resonance_gcd=gcd(d,n)
        if resonance_gcd>1 and pow(alpha,n//resonance_gcd,p)==1:continue
        meta.full_defect_scans+=1
        h={}
        for j in range(n):
            value=(r[j]-alpha*r[(j-d)%n])%p
            work.multiplies+=1;work.additions+=1;work.reads+=2;work.writes+=1
            meta.entries_verified+=1
            if value:h[j]=value
            if len(h)>2:break
        if 1<=len(h)<=2:
            meta.selected='blind-2defects';meta.reason='full-defect-certified'
            return (d,alpha,h),meta
    return None,meta


def transform_resultant(engine,x):
    n,p=engine.n,engine.p
    work=Work()
    r=engine.P.apply(x)
    work.multiplies+=2*n;work.additions+=n;work.reads+=2*n;work.writes+=n
    found,meta=discover_resultant(r,engine,work)
    if found:
        d,alpha,entries=found
        forcing,dm=decode_binomial(r,d,alpha,1,engine,work,forcing_method='direct')
        branch='blind-resultant-2defects'
    else:
        forcing,_=bluestein_transform(r,n,engine.omega,p,engine.primitive_gen,work.sparse)
        branch='fallback'
    out=engine.L.solve(forcing)
    work.multiplies+=3*n+1;work.additions+=2*n;work.reads+=3*n;work.writes+=2*n
    return out,{'selected':branch,'certificate':meta,'work':work,
                'params':None if found is None else (found[0],found[1])}
