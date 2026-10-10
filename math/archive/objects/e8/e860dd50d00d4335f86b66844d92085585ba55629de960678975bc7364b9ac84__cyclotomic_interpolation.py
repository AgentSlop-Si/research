"""Stdlib exact Newton interpolation over Q[z]/(z^m+1).

The quotient is a field for m=2^t, since z^m+1 is cyclotomic.
Used only to independently check tiny interpolation degrees (N=4,8).
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from orbit_recovery import subset_sum_cyclotomic_coeffs,target_conjugate_coeffs,validate_n


@dataclass(frozen=True)
class Cyclo:
    c: tuple[Fraction, ...]

    @classmethod
    def of(cls, vals):
        return cls(tuple(Fraction(v) for v in vals))

    @classmethod
    def zero(cls,m):return cls.of([0]*m)
    @classmethod
    def one(cls,m):return cls.of([1]+[0]*(m-1))

    def __add__(self,other):
        return Cyclo(tuple(a+b for a,b in zip(self.c, other.c)))

    def __sub__(self,other):
        return Cyclo(tuple(a-b for a,b in zip(self.c,other.c)))

    def __neg__(self):return Cyclo(tuple(-a for a in self.c))

    def __mul__(self,other):
        m=len(self.c)
        c=[Fraction(0)]*m
        for i,a in enumerate(self.c):
            if not a: continue
            for j,b in enumerate(other.c):
                if not b: continue
                s=i+j
                c[s%m]+=a*b*(1 if s<m else -1)
        return Cyclo(tuple(c))

    def inv(self):
        if not any(self.c):raise ZeroDivisionError('zero cyclotomic value')
        m=len(self.c)
        one=Cyclo.one(m)
        A=[]
        for i in range(m):
            A.append([Fraction(0)]*(m+1))
        for j in range(m):
            unit=Cyclo.of([int(k==j) for k in range(m)])
            col=(self*unit).c
            for i in range(m):A[i][j]=col[i]
        for i in range(m):A[i][m]=one.c[i]
        for j in range(m):
            pivot=next((i for i in range(j,m) if A[i][j]),None)
            if pivot is None:raise ZeroDivisionError('non-invertible cyclotomic value')
            A[j],A[pivot]=A[pivot],A[j]
            scale=A[j][j]
            A[j]=[v/scale for v in A[j]]
            for i in range(m):
                if i==j:continue
                scale=A[i][j]
                if scale:
                    A[i]=[a-scale*b for a,b in zip(A[i],A[j])]
        ans=Cyclo(tuple(A[i][-1] for i in range(m)))
        assert self*ans==one
        return ans

    def __truediv__(self,other):return self*other.inv()


def newton_interpolant(n: int, u: int):
    """Return nodes, divided differences for the UNIQUE degree<2^m map."""
    validate_n(n)
    m=n//2
    if m>5:
        raise ValueError('exact interpolation intentionally limited to m<=5')
    xs=[Cyclo.of(subset_sum_cyclotomic_coeffs(n,mask)) for mask in range(1<<m)]
    ys=[Cyclo.of(target_conjugate_coeffs(n,u,mask)) for mask in range(1<<m)]
    coeff=[]
    for i,(x,y) in enumerate(zip(xs,ys)):
        if i==0: coeff.append(y);continue
        guess=coeff[-1]
        for j in range(i-2,-1,-1):
            guess=guess*(x-xs[j])+coeff[j]
        den=Cyclo.one(m)
        for j in range(i):den=den*(x-xs[j])
        coeff.append((y-guess)/den)
    return xs,ys,coeff


def evaluate_newton(x, xs, coefficients):
    y=coefficients[-1]
    for i in range(len(coefficients)-2,-1,-1):
        y=y*(x-xs[i])+coefficients[i]
    return y


def interpolation_audit(n: int, u: int=3):
    xs,ys,cs=newton_interpolant(n,u)
    assert len(set(xs))==len(xs)
    for x,y in zip(xs,ys):
        assert evaluate_newton(x,xs,cs)==y
    degree=max(i for i,c in enumerate(cs) if any(c.c))
    return {'N':n,'u':u,'boolean_samples':len(xs),'exact_min_polynomial_degree':degree,
            'newton_top_coefficient':tuple(str(v) for v in cs[degree].c),
            'all_samples_verified':True}


def rational_interpolation_rank(n: int, u: int, d: int) -> dict:
    """Exact rank of univariate rational interpolation constraints.

    P(alpha_mask) - beta_mask Q(alpha_mask) = 0, deg(P),deg(Q) <= d.
    Full column rank certifies NO rational map at that degree. Nonfull rank
    does not alone certify a valid denominator at every sample.
    """
    if n>8:
        raise ValueError('exact small-case rank check limited to N<=8')
    m=n//2
    xs=[Cyclo.of(subset_sum_cyclotomic_coeffs(n,t)) for t in range(1<<m)]
    ys=[Cyclo.of(target_conjugate_coeffs(n,u,t)) for t in range(1<<m)]
    zero=Cyclo.zero(m);one=Cyclo.one(m)
    A=[]
    for x,y in zip(xs,ys):
        powers=[one]
        for t in range(d):powers.append(powers[-1]*x)
        A.append(powers+[-y*v for v in powers])
    rows=len(A)
    cols=2*(d+1)
    rank=0
    for j in range(cols):
        pivot=next((i for i in range(rank,rows) if A[i][j]!=zero),None)
        if pivot is None:continue
        A[rank],A[pivot]=A[pivot],A[rank]
        inv=A[rank][j].inv()
        A[rank]=[v*inv for v in A[rank]]
        for i in range(rank+1,rows):
            scale=A[i][j]
            if scale!=zero:
                A[i]=[a-scale*b for a,b in zip(A[i],A[rank])]
        rank+=1
        if rank==rows:break
    return {'N':n,'u':u,'max_degree':d,'rows':rows,'columns':cols,
            'rank_over_cyclotomic_field':rank,'no_rational_solution_proved':rank==cols}


def rational_interpolant(n: int, u: int, d: int):
    """Construct a full-rank nullspace candidate with nonvanishing denominators.

    Intended for N=8, d=8 only. Raises ValueError if no candidate is found.
    """
    if n>8:raise ValueError('small exact example only')
    m=n//2
    xs=[Cyclo.of(subset_sum_cyclotomic_coeffs(n,t)) for t in range(1<<m)]
    ys=[Cyclo.of(target_conjugate_coeffs(n,u,t)) for t in range(1<<m)]
    zero=Cyclo.zero(m);one=Cyclo.one(m)
    A=[]
    for x,y in zip(xs,ys):
        powers=[one]
        for _ in range(d):powers.append(powers[-1]*x)
        A.append(powers+[-y*v for v in powers])
    rows=len(A);cols=2*(d+1); pivots=[];rank=0
    for j in range(cols):
        pivot=next((i for i in range(rank,rows) if A[i][j]!=zero),None)
        if pivot is None:continue
        A[rank],A[pivot]=A[pivot],A[rank]
        inv=A[rank][j].inv()
        A[rank]=[v*inv for v in A[rank]]
        for i in range(rows):
            if i!=rank and A[i][j]!=zero:
                factor=A[i][j]
                A[i]=[a-factor*b for a,b in zip(A[i],A[rank])]
        pivots.append(j);rank+=1
        if rank>=rows:break
    frees=[j for j in range(cols) if j not in pivots]
    basis=[]
    for free in frees:
        vec=[zero]*cols
        vec[free]=one
        for i,piv in enumerate(pivots):
            vec[piv]=-A[i][free]
        basis.append(vec)
    def ev(c,x):
        ans=zero
        for a in reversed(c):ans=ans*x+a
        return ans
    for t in range(1,40):
        weights=[Cyclo.of([t**j]+[0]*(m-1)) for j in range(len(basis))]
        v=[sum((base[j]*weight for base,weight in zip(basis,weights)),zero) for j in range(cols)]
        P,Q=v[:d+1],v[d+1:]
        if all(ev(Q,x)!=zero and ev(P,x)==y*ev(Q,x) for x,y in zip(xs,ys)):
            return {'N':n,'u':u,'degree':d,'num_coeffs':P,'den_coeffs':Q,
                    'denominator_nonzero_on_all':True,'all_values_verified':True,
                    'nullspace_dimension':len(frees)}
    raise ValueError('no nonvanishing rational interpolant found in finite candidate sweep')
