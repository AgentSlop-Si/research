"""Exact, fresh-input Boolean FFT polynomial-degree research gates.

No caches, threads, approximate roots or uncharged oracle operations.
This is a falsification audit, not an improved all-input FFT.

The key result: every total-degree<=2 polynomial P agreeing with a linear map
A x on {0,1}^n has Jac(P) at (1/2,...,1/2) equal A. In particular,
    A h = (P(1/2+h)-P(1/2-h))/2.

Over a field of odd characteristic, the identity is exact. Evaluating P twice
costs two calls to ANY circuit for P, plus O(n+outputs) linear work. This is a
uniform reduction without extracting input-dependent circuit coefficients.

Degree 3: homogeneous cubic polynomials agreeing with A x on {0,1}^n have
only diagonal cubes plus antisymmetric pair gauges
    x_i^2*x_j - x_i*x_j^2.
A universal fixed-weight gradient-average recovery must use >=n evaluation
points because its second-moment matrix is (I+J)/6, of full rank.
"""
from __future__ import annotations
from dataclasses import dataclass
from itertools import product
from random import Random
from typing import Callable, Iterable, Sequence

P = 998244353
G = 3
INV2 = (P+1)//2
INV3 = pow(3, -1, P)
INV4 = pow(4, -1, P)
INV6 = pow(6, -1, P)

@dataclass
class Counter:
    additions: int = 0
    multiplications: int = 0
    def a(self,x:int,y:int)->int:
        self.additions+=1
        return (x+y)%P
    def s(self,x:int,y:int)->int:
        self.additions+=1
        return (x-y)%P
    def m(self,x:int,y:int)->int:
        self.multiplications+=1
        return (x*y)%P
    @property
    def work(self)->int:
        return self.additions+self.multiplications


def ntt(x:Sequence[int],meter:Counter|None=None)->list[int]:
    """A conventional radix-two NTT for finite checks, with charged gates.

    Root/twiddle preparation is separated and called out in research costs.
    """
    n=len(x)
    if not n or n & (n-1) or (P-1)%n:
        raise ValueError('NTT needs supported nonzero power-of-two length')
    c=meter if meter is not None else Counter()
    out=[int(t)%P for t in x]
    j=0
    for i in range(1,n):
        bit=n>>1
        while j & bit:
            j^=bit
            bit>>=1
        j^=bit
        if i<j:out[i],out[j]=out[j],out[i]
    stage=2
    while stage<=n:
        wlen=pow(G,(P-1)//stage,P)
        for a in range(0,n,stage):
            w=1
            for b in range(a,a+stage//2):
                u=out[b]
                v=c.m(out[b+stage//2],w)
                out[b]=c.a(u,v)
                out[b+stage//2]=c.s(u,v)
                w=c.m(w,wlen)
        stage*=2
    return out


def direct_dft(x:Sequence[int])->list[int]:
    n=len(x)
    if not n or (P-1)%n:
        raise ValueError('missing n-th root')
    omega=pow(G,(P-1)//n,P)
    return [sum(int(x[j])*pow(omega,k*j,P) for j in range(n))%P
            for k in range(n)]


def quadratic_preprocess(x:Sequence[int], weights:Sequence[int],
                         variant:str='plain', c:Counter|None=None)->list[int]:
    """Degree-two polynomial lift, agreeing with x on Boolean inputs.

    variant='pair_overlap' builds squares from THREE overlapping products
    (x_i+x_j)^2,(x_i-x_j)^2,(x_i+x_j)(x_i-x_j), and cancels the x_i*x_j terms.
    No upstream FFT or input relation metadata is supplied.
    """
    if len(x)!=len(weights): raise ValueError('length mismatch')
    if variant not in ('plain','square','affine_square','pair_overlap'):
        raise ValueError('invalid variant')
    c=c or Counter(); n=len(x)
    if variant=='plain':return [v%P for v in x]
    squares=[]
    if variant=='pair_overlap':
        for i in range(0,n,2):
            if i+1==n:
                squares.append(c.m(x[i],x[i]))
                continue
            u=c.a(x[i],x[i+1]);v=c.s(x[i],x[i+1])
            a=c.m(u,u);b=c.m(v,v);d=c.m(u,v)
            t=c.a(a,b);two_d=c.m(2,d)
            squares.extend((c.m(INV4,c.a(t,two_d)), c.m(INV4,c.s(t,two_d))))
    else:
        squares=[c.m(v,v) for v in x]
    if variant in ('square','pair_overlap'):return squares
    return [c.a(c.m((1-w)%P,x0),c.m(w,z)) for x0,z,w in zip(x,squares,weights)]


def quadratic_fft(x:Sequence[int],weights:Sequence[int],
                  variant:str='affine_square', c:Counter|None=None)->list[int]:
    c=c if c is not None else Counter()
    z=quadratic_preprocess([a%P for a in x],weights,variant,c)
    return ntt(z,c)


def midpoint_recover(program:Callable[[Sequence[int]],Sequence[int]],
                     h:Sequence[int])->list[int]:
    """Full arbitrary-input transform using two Boolean-correct quadratic calls."""
    plus=[(INV2+x)%P for x in h]
    minus=[(INV2-x)%P for x in h]
    a=program(plus)
    b=program(minus)
    return [((u-v)*INV2)%P for u,v in zip(a,b)]


def cubic_fft(x:Sequence[int], gauge:Sequence[Sequence[int]],
             c:Counter|None=None)->list[int]:
    """Homogeneous cubic gauge lift, correct for all Boolean x.

    gauge[k][pair-index] multiplies x_i^2*x_j - x_i*x_j^2.
    Coefficients are fixed input-independent constants.
    """
    n=len(x)
    if len(gauge)!=n or any(len(g)!=n*(n-1)//2 for g in gauge):
        raise ValueError('invalid gauge matrix')
    c = c if c is not None else Counter()
    cube=[c.m(c.m(v,v),v) for v in x]
    out=ntt(cube,c)
    sq=[c.m(v,v) for v in x]
    pairs=[]
    for i in range(n):
        for j in range(i+1,n):
            pairs.append(c.s(c.m(sq[i],x[j]),c.m(x[i],sq[j])))
    for k in range(n):
        for a,coef in zip(pairs,gauge[k]):
            if coef:out[k]=c.a(out[k],c.m(coef,a))
    return out


def wedge_gauge(x:Sequence[int], a:Sequence[int], b:Sequence[int],
                c:Counter|None=None)->int:
    """A genuinely global cubic Boolean-null polynomial with dense overlap.

    G=(a.x^2)(b.x) - (a.x)(b.x^2).
    For binary x, G=0. Off the Boolean cube it is usually nonzero. It has
    choose(n,2) *potential* antisymmetric pair coefficients, but evaluates in
    O(n) ordinary scalar operations without explicitly expanding them.
    The identity does NOT calculate Fourier outputs or accelerate a full FFT.
    """
    if len(x)!=len(a) or len(x)!=len(b):raise ValueError('length mismatch')
    c=c if c is not None else Counter()
    ax=bx=ax2=bx2=0
    for xi,ai,bi in zip(x,a,b):
        sq=c.m(xi,xi)
        ax=c.a(ax,c.m(ai,xi))
        bx=c.a(bx,c.m(bi,xi))
        ax2=c.a(ax2,c.m(ai,sq))
        bx2=c.a(bx2,c.m(bi,sq))
    return c.s(c.m(ax2,bx),c.m(ax,bx2))


def wedge_coefficients(a:Sequence[int],b:Sequence[int])->list[int]:
    """Coefficients of x_i^2*x_j - x_i*x_j^2 for i<j."""
    if len(a)!=len(b):raise ValueError('length mismatch')
    return [(a[i]*b[j]-a[j]*b[i])%P
            for i in range(len(a)) for j in range(i+1,len(a))]


def cubic_global_wedge_fft(x:Sequence[int],a:Sequence[int],b:Sequence[int],
                           output_weights:Sequence[int],c:Counter|None=None)->list[int]:
    """An inexpensive dense-overlap perturbation of the full FFT.

    P_k(x)=FFT(x^3)[k]+weights[k]*G(x). On Boolean inputs equals FFT(x).
    The expensive full FFT still remains in the expression.
    """
    if len(x)!=len(output_weights):raise ValueError('length mismatch')
    c=c if c is not None else Counter()
    base=ntt([c.m(c.m(t,t),t) for t in x],c)
    delta=wedge_gauge(x,a,b,c)
    return [c.a(z,c.m(w,delta)) for z,w in zip(base,output_weights)]


def cubic_jacobian_vector(a:Sequence[int],h:Sequence[int],gauge:Sequence[Sequence[int]])->list[int]:
    """Exact differential of cubic_fft, not numerical finite differences."""
    n=len(a)
    diag=[3*a[i]*a[i]*h[i]%P for i in range(n)]
    out=ntt(diag)
    terms=[]
    for i in range(n):
        for j in range(i+1,n):
            # d(x_i^2*x_j-x_i*x_j^2)
            v=(2*a[i]*h[i]*a[j]+a[i]*a[i]*h[j]
               -h[i]*a[j]*a[j]-2*a[i]*a[j]*h[j])%P
            terms.append(v)
    for k in range(n):
        out[k]=(out[k]+sum(v*g for v,g in zip(terms,gauge[k])))%P
    return out


def cubic_recovery_nplus1(h:Sequence[int],gauge:Sequence[Sequence[int]])->list[int]:
    """A universal N+1-gradient recovery, charged O(N) evaluations.

    Fh = [Jac_P(1)h + sum_i Jac_P(e_i)h]/6 for any homogeneous cubic
    polynomial P matching F on the Boolean cube.
    """
    n=len(h)
    x=cubic_jacobian_vector([1]*n,h,gauge)
    for i in range(n):
        e=[0]*n;e[i]=1
        v=cubic_jacobian_vector(e,h,gauge)
        x=[(u+w)%P for u,w in zip(x,v)]
    return [v*INV6%P for v in x]


def second_moment_target(n:int)->list[list[int]]:
    """Necessary matrix for universal fixed-basepoint cubic-gradient extraction."""
    return [[(2 if i==j else 1)*INV6%P for j in range(n)] for i in range(n)]


def matrix_rank_mod(matrix:Sequence[Sequence[int]],p:int=P)->int:
    a=[[int(v)%p for v in row] for row in matrix]
    if not a:return 0
    n=len(a);m=len(a[0]);k=0
    for j in range(m):
        ix=next((i for i in range(k,n) if a[i][j]),None)
        if ix is None:continue
        a[k],a[ix]=a[ix],a[k]
        t=pow(a[k][j],-1,p)
        for col in range(j,m):a[k][col]=a[k][col]*t%p
        for i in range(n):
            if i==k or not a[i][j]:continue
            coef=a[i][j]
            for col in range(j,m):a[i][col]=(a[i][col]-coef*a[k][col])%p
        k+=1
        if k==n:break
    return k


def randomized_gauge(n:int,seed:int,nonzero=True)->list[list[int]]:
    rng=Random(seed)
    return [[rng.randrange(1,P) if nonzero else rng.randrange(P)
             for _ in range(n*(n-1)//2)] for __ in range(n)]


def run_audit()->dict:
    import time
    rng=Random(20261009)
    results=[];basis_total=0;cube_cases=0;cubic_cases=0;wedge_cases=0
    for n in (2,4,8,16,32,64):
        weights=[rng.randrange(P) for _ in range(n)]
        variants=[]
        for variant in ('square','affine_square','pair_overlap'):
            meter=Counter()
            data=[rng.randrange(P) for _ in range(n)]
            y=quadratic_fft(data,weights,variant,meter)
            if variant=='affine_square':
                pass
            # all Boolean checks of original circuit, plus arbitrary-input recovery
            for j in range(n):
                e=[int(t==j) for t in range(n)]
                assert quadratic_fft(e,weights,variant)==direct_dft(e)
                basis_total+=1
            for _ in range(6):
                z=[rng.randrange(P) for _ in range(n)]
                assert midpoint_recover(lambda v:quadratic_fft(v,weights,variant),z)==direct_dft(z)
            variants.append({'variant':variant,'work_one_evaluation':meter.work,
                             'twiddle_generation_not_in_work':True})
        g=randomized_gauge(n,seed=20261009+n)
        for j in range(n):
            e=[int(t==j) for t in range(n)]
            assert cubic_fft(e,g)==direct_dft(e)
            cubic_cases+=1
        for _ in range(5):
            bx=[rng.randrange(2) for _ in range(n)]
            assert cubic_fft(bx,g)==direct_dft(bx)
            h=[rng.randrange(P) for _ in range(n)]
            assert cubic_recovery_nplus1(h,g)==direct_dft(h)
            cubic_cases+=1
        assert matrix_rank_mod(second_moment_target(n))==n
        a=[rng.randrange(1,P) for _ in range(n)]
        b=[rng.randrange(1,P) for _ in range(n)]
        coeff=wedge_coefficients(a,b)
        for _ in range(4):
            xx=[rng.randrange(P) for _ in range(n)]
            terms=[]
            for i in range(n):
                for j in range(i+1,n):
                    terms.append((xx[i]*xx[i]*xx[j]-xx[i]*xx[j]*xx[j])%P)
            assert wedge_gauge(xx,a,b)==sum(c*t for c,t in zip(coeff,terms))%P
            yy=[rng.randrange(2) for _ in range(n)]
            assert wedge_gauge(yy,a,b)==0
            weights_k=[rng.randrange(P) for __ in range(n)]
            assert cubic_global_wedge_fft(yy,a,b,weights_k)==direct_dft(yy)
            wedge_cases+=1
        results.append({'n':n,'quadratic_variants':variants,
                        'cubic_gradient_min_calls':n,'explicit_recovery_calls':n+1,
                        'second_moment_rank':n,'wedge_pair_coefficients':len(coeff)})
    return {'modulus':P,'lengths':results,'quadratic_basis_columns_tested':basis_total,
            'cubic_boolean_and_recovery_cases':cubic_cases,
            'wedge_dense_overlap_tests':wedge_cases,
            'general_full_fft_O_N':'NOT_ESTABLISHED',
            'quadratic_uniform_reduction':'two_calls+O(N) arithmetic',
            'cubic_correction_lower_bound_scope':'fixed-weight linear combinations of Jacobian evaluations'}

if __name__=='__main__':
    import json
    from pathlib import Path
    data=run_audit()
    fn=Path(__file__).with_name('audit_results.json')
    fn.write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps(data,indent=2))
