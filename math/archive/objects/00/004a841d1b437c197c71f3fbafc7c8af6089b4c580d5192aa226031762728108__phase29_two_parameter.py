"""Phase 29: exact two-coupling Green-sum Fourier feasibility certificates.

We construct three independently ordered, complex-gauged Hamiltonian Green
resolvents G0,G1,G2 and the affine middle mixer B(lam,mu)=G0+lam*G1+mu*G2.
For fixed outer Green sums A,C and Fourier F, the target is T=A^-1 F C^-1.

Each phase/permutation-equivalent B must satisfy two independent moments
Q_s(B)=Q_s(T), s=1,2. Clearing entrywise denominators yields polynomials
P_s(lam,mu) in F_p[lam,mu] with total degree <= s*N^2. A single transverse
lambda slice with coprime P_1 and P_2, plus nonzero constant leading
mu coefficients, certifies there is no common polynomial component.
The explicit modular Bézout identity and preserved leading degrees lift the
no-common-component conclusion to the matching cyclotomic-rational matrices
in characteristic zero. They do NOT say the two polynomials have no points.

Cost: the dense synthesis check is not part of any fast FFT executor.
"""
from __future__ import annotations
import json
from pathlib import Path
from random import Random
from phase28_synthesis import (P, PRIMITIVE, inverse, random_cycle, green_matrix,
                               green_sum, green_components, matmul, invert, fft_matrix)
from phase28_polynomial import (poly_trim,poly_scale,poly_mul,eval_poly,
                                trace_power_from_matrix,trace_moment_poly,
                                gcd_modp,evaluate_B)

SEEDS = {4:2804, 8:2808, 16:2816}
SLICES = {4:1,8:0,16:1}

def third_green(n:int,seed:int):
    rng=Random(seed)
    omega=pow(PRIMITIVE,-(P-1)//n,P)
    roots=[pow(omega,j,P) for j in range(n)]
    g=green_matrix(random_cycle(n,rng),inverse(7))
    left=[roots[rng.randrange(n)] for _ in range(n)]
    right=[roots[rng.randrange(n)] for _ in range(n)]
    return [[left[i]*g[i][j]*right[j]%P for j in range(n)] for i in range(n)]

def build_family(n:int,seed:int):
    a=green_sum(n,seed*3+1)
    g0,g1=green_components(n,seed*3+2)
    g2=third_green(n,seed*3+4)
    c=green_sum(n,seed*3+3)
    target=matmul(matmul(invert(a),fft_matrix(n)),invert(c))
    if any(x==0 for row in target for x in row):
        raise AssertionError('zero target entry: use support-aware analysis')
    return target,g0,g1,g2

def slice_family(g0,g1,lmbda):
    n=len(g0)
    return [[(g0[i][j]+lmbda*g1[i][j])%P for j in range(n)] for i in range(n)]

def poly_rem(a,b):
    a=poly_trim(a);b=poly_trim(b)
    if b==[0]: raise ZeroDivisionError
    invb=inverse(b[-1])
    while len(a)>=len(b) and a!=[0]:
        shift=len(a)-len(b);co=a[-1]*invb%P
        for k,v in enumerate(b): a[shift+k]=(a[shift+k]-co*v)%P
        a=poly_trim(a)
    return a

def poly_divmod(a,b):
    a=poly_trim(a);b=poly_trim(b)
    if b==[0]:raise ZeroDivisionError
    q=[0]*max(1,len(a)-len(b)+1)
    ib=inverse(b[-1])
    while len(a)>=len(b) and a!=[0]:
        k=len(a)-len(b);t=a[-1]*ib%P
        q[k]=t
        for j,x in enumerate(b):a[k+j]=(a[k+j]-t*x)%P
        a=poly_trim(a)
    return poly_trim(q),a

def poly_add(a,b,sign=1):
    c=[0]*max(len(a),len(b))
    for i,v in enumerate(a):c[i]=(c[i]+v)%P
    for i,v in enumerate(b):c[i]=(c[i]+sign*v)%P
    return poly_trim(c)

def bezout(a,b):
    """Get U,V with U*a+V*b=1 mod p when a,b coprime."""
    r0,r1=poly_trim(a),poly_trim(b)
    u0,u1=[1],[0];v0,v1=[0],[1]
    while r1!=[0]:
        q,r=poly_divmod(r0,r1)
        r0,r1=r1,r
        u0,u1=u1,poly_add(u0,poly_mul(q,u1),-1)
        v0,v1=v1,poly_add(v0,poly_mul(q,v1),-1)
    if len(r0)!=1 or r0[0]==0:raise AssertionError('non-coprime slice')
    invlead=inverse(r0[0]);u0=poly_scale(u0,invlead);v0=poly_scale(v0,invlead)
    if poly_add(poly_mul(u0,a),poly_mul(v0,b)) !=[1]:
        raise AssertionError('Bezout identity invalid')
    return u0,v0

def nonzero_entries(m):
    return all(v%P for row in m for v in row)

def certificate(n:int,seed:int|None=None,lmbda:int|None=None,with_polys:bool=True):
    seed=SEEDS[n] if seed is None else seed
    lmbda=SLICES[n] if lmbda is None else lmbda
    target,g0,g1,g2=build_family(n,seed)
    base=slice_family(g0,g1,lmbda)
    q1,q2=tuple(trace_power_from_matrix(target,s) for s in (1,2))
    p1=trace_moment_poly(q1,base,g2,1)
    p2=trace_moment_poly(q2,base,g2,2)
    if (len(p1)-1,len(p2)-1)!=(n*n,2*n*n):
        raise AssertionError('specialized degree drop')
    expected=[]
    d=1
    for row in g2:
        for val in row:d=d*val%P
    for s,q in ((1,q1),(2,q2)):
        expected.append(pow(d,s,P)*(trace_power_from_matrix(g2,s)-q)%P)
    if [p1[-1],p2[-1]]!=expected or not all(expected):
        raise AssertionError('parameter-independent leading coefficient failure')
    u,v=bezout(p1,p2)
    result={
      'claim':'zero-dimensional exceptional projective-moment locus; not empty-set theorem',
      'field_prime':P,'n':n,'seed':seed,'fixed_lambda_slice':lmbda,
      'degree_bound_total_p1':n*n,'degree_bound_total_p2':2*n*n,
      'degree_in_mu_p1':len(p1)-1,'degree_in_mu_p2':len(p2)-1,
      'leading_mu_coefficients':[p1[-1],p2[-1]],
      'expected_leading_coefficients':expected,
      'slice_gcd':[1],
      'bezout_identity':'U(mu)*P1(lambda0,mu)+V(mu)*P2(lambda0,mu)=1 mod prime',
      'bezout_U':u,'bezout_V':v,
      'upper_bound_joint_complex_solutions_with_multiplicity':2*n**4,
      'positive_control':False,
    }
    if with_polys: result['slice_P1']=p1;result['slice_P2']=p2
    return result

def validate(cert:dict):
    n=cert['n'];base=cert['slice_P1'];second=cert['slice_P2']
    assert len(base)==n*n+1 and len(second)==2*n*n+1
    assert [base[-1],second[-1]]==cert['leading_mu_coefficients']
    assert poly_add(poly_mul(cert['bezout_U'],base),poly_mul(cert['bezout_V'],second))==[1]
    return True

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser()
    ap.add_argument('--n',type=int,choices=[4,8,16],required=True)
    ap.add_argument('--output',type=str)
    args=ap.parse_args()
    result=certificate(args.n)
    assert validate(result)
    if args.output:
        Path(args.output).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items()
                      if k not in ('slice_P1','slice_P2','bezout_U','bezout_V')},indent=2))
