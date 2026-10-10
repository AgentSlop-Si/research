#!/usr/bin/env python3
"""Independent exact checks. No uploaded code is imported or executed."""
from fractions import Fraction as F
from itertools import permutations
import json
import random
from pathlib import Path
import sympy as sp
from apply_allpass import AllPassCycle

BASE=Path(__file__).resolve().parent
rng=random.Random(1232)

def signed_cycle(n):
    m=sp.zeros(n)
    m[0,n-1]=-1
    for j in range(1,n): m[j,j-1]=1
    return m

def zero(a):
    return all(sp.expand(x)==0 for x in a)

def monomial(n):
    perm=list(range(n)); rng.shuffle(perm)
    q=sp.zeros(n)
    phases=[sp.Integer(1),sp.Integer(-1),sp.I,-sp.I]
    for j,p in enumerate(perm): q[p,j]=rng.choice(phases)
    return q

def norm1(a):
    return max(sum(sp.Abs(a[i,j]) for i in range(a.rows)) for j in range(a.cols))

def solver(x, reverse=False):
    n=len(x)
    a=F(1)
    for _ in range(n-1): a*=F(1,2)
    h=1/(2+a)
    order=list(range(n-1,-1,-1)) if reverse else list(range(n))
    xx=[x[j] for j in order]
    b=F(0)
    for j in range(1,n): b=(xx[j]+b)/2
    zz=[(xx[0]-b)*h]
    for j in range(1,n): zz.append((xx[j]+zz[-1])/2)
    yy=[2*xx[j]-3*zz[j] for j in range(n)]
    out=[None]*n
    for j,k in enumerate(order): out[k]=yy[j]
    return out

exact=[]
for n in [3,4,5,6,7,8,10,12]:
    eye=sp.eye(n); s=signed_cycle(n)
    d=monomial(n); m=d*s*d.H
    k=eye+(eye-m).inv()
    u=(eye-2*m)*(2*eye-m).inv()
    v=u.H
    den=2**n+1
    up=(2**(n-1)+2)*eye
    vp=(2**(n-1)+2)*eye
    power=eye
    for j in range(1,n):
        power=power*m
        up-=3*2**(n-1-j)*power
        vp+=3*2**(j-1)*power
    up/=den; vp/=den
    assert zero(m**n+eye)
    assert zero(k.H*k-(2*eye+(2*eye-m-m.H).inv()))
    assert sp.expand(k.det()-sp.Rational(2**n+1,2))==0
    assert zero(u.H*u-eye) and zero(v*u-eye)
    assert zero(u-up) and zero(v-vp)
    assert zero(v-k*(eye+(eye-m.H).inv()).inv())
    c=sp.Rational(2**(n+1)-1,den)
    assert norm1(u)==c and norm1(v)==c
    assert len(set(sp.Abs(u[i,0]) for i in range(n)))>=2
    q=monomial(n)
    for eps in [1,-1]:
        for reverse in [False,True]:
            m2=q.H*(m.H if reverse else m)*q
            k2=eye+(eye-m2).inv()
            pair=(k if eps==1 else k.inv())*q*(k2.inv() if eps==1 else k2)
            expected=((v if eps==1 else u) if reverse else eye)*q
            assert zero(pair-expected) and zero(pair.H*pair-eye)
    us=(eye-2*s)*(2*eye-s).inv()
    vs=us.H
    for trial in range(3):
        x=[F(rng.randint(-9,9),rng.randint(1,9)) for _ in range(n)]
        ux=solver(x); vx=solver(x,True)
        assert zero(sp.Matrix(ux)-us*sp.Matrix(x))
        assert zero(sp.Matrix(vx)-vs*sp.Matrix(x))
        assert solver(ux,True)==x and solver(vx)==x
    exact.append({'N':n,'all_exact_checks':True,'c_N':str(c),'forward_inverse_round_trips':6})

orientation=[]
for n in range(3,8):
    edges={frozenset((j,(j+1)%n)) for j in range(n)}
    valid=[]
    checked=0
    for tail in permutations(range(1,n)):
        order=(0,)+tail
        checked+=1
        ee={frozenset((order[j],order[(j+1)%n])) for j in range(n)}
        if ee==edges: valid.append(order)
    assert len(valid)==2
    assert (0,)+tuple(range(1,n)) in valid
    assert (0,)+tuple(range(n-1,0,-1)) in valid
    orientation.append({'N':n,'directed_cycles_checked':checked,'orientations_found':len(valid)})

class Count:
    operations=0
    def __init__(self,x): self.x=x.x if isinstance(x,Count) else F(x)
    def op(self,other,fn):
        Count.operations+=1
        return Count(fn(self.x,Count(other).x))
    def __add__(self,o): return self.op(o,lambda a,b:a+b)
    __radd__=__add__
    def __sub__(self,o): return self.op(o,lambda a,b:a-b)
    def __rsub__(self,o): return Count(o).__sub__(self)
    def __mul__(self,o): return self.op(o,lambda a,b:a*b)
    __rmul__=__mul__
    def __truediv__(self,o): return self.op(o,lambda a,b:a/b)
    def __rtruediv__(self,o): return Count(o).__truediv__(self)

def counted(n):
    half=Count(F(1,2)); a=Count(1)
    Count.operations=0
    for _ in range(n-1): a=a*half
    h=1/(2+a)
    prep=Count.operations
    x=[Count(F(j-2,j+1)) for j in range(n)]
    Count.operations=0
    b=Count(0)
    for j in range(1,n): b=(x[j]+b)*half
    z=[(x[0]-b)*h]
    for j in range(1,n): z.append((x[j]+z[-1])*half)
    y=[2*x[j]-3*z[j] for j in range(n)]
    run=Count.operations
    assert prep==n+1 and run==7*n-2
    assert [a.x for a in y]==solver([a.x for a in x])
    return {'N':n,'preparation_field_operations':prep,'application_field_operations':run}

counts=[counted(n) for n in [3,4,8,16,32,64,128,256]]

powers=[]
for n in [3,4,5,6,8,9,10,12]:
    eye=sp.eye(n); s=signed_cycle(n)
    u=(eye-2*s)*(2*eye-s).inv()
    for power in [-5,-3,-1,0,1,2,4,7]:
        v=u**(-power)
        assert zero(v.T*v-eye)
        assert all(x.is_Rational and sp.denom(x)%2==1 for x in v)
        assert any(x*x != sp.Rational(1,n) for x in v)
        powers.append({'N':n,'exponent':power,'exact_checks':True})

reusable=[]
for n in [3,4,5,8,12,16]:
    order=list(range(n)); rng.shuffle(order)
    weights=[sp.Integer(1)]*n
    for j in range(1,n): weights[j]=rng.choice([sp.Integer(1),sp.Integer(-1),sp.I,-sp.I])
    weights[0]=-1/sp.prod(weights[1:])
    m=sp.zeros(n)
    for j in range(n): m[order[j],order[j-1]]=weights[j]
    eye=sp.eye(n); u=(eye-2*m)*(2*eye-m).inv()
    evaluator=AllPassCycle(n,order,weights)
    x=[sp.Rational(rng.randint(-5,5),rng.randint(1,5))+sp.I*sp.Rational(rng.randint(-5,5),rng.randint(1,5)) for _ in range(n)]
    ux=evaluator.apply(x); vx=evaluator.apply(x,True)
    assert zero(sp.Matrix(ux)-u*sp.Matrix(x))
    assert zero(sp.Matrix(vx)-u.H*sp.Matrix(x))
    assert zero(sp.Matrix(evaluator.apply(ux,True))-sp.Matrix(x))
    reusable.append({'N':n,'exact_weighted_cycle_and_inverse':True})
results={'status':'PASS','exact_matrix_tests':exact,'orientation_enumeration':orientation,
         'operation_counts':counts,'fixed_cycle_power_checks':powers,'reusable_evaluator_checks':reusable,'scope':'Finite exact checks corroborate; PROOF.md provides all-N proof. No general Fourier speedup.'}
(BASE/'results.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
