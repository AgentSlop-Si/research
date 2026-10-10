#!/usr/bin/env python3
"""Independent exact-rational tests of a proposed reduced-center DFT network.

Scope: finite scalar network and constants only. Does not execute tensor recursion
or prove the entire published theorem. Uses rational arithmetic throughout.
"""
from fractions import Fraction as F
from itertools import combinations
from math import comb
from decimal import Decimal, localcontext
import random

class ReducedNetwork:
    def __init__(self,h):
        self.h=h
        self.triples=list(combinations(range(h),3))
        self.v=len(self.triples)
        self.tsets=[set(t) for t in self.triples]
        self.neighbors=[[(k, F(1-len(S & T),2)) for k,T in enumerate(self.tsets) if len(S & T)%2==0] for S in self.tsets]
        self.occurrences=[[t for t,T in enumerate(self.triples) if j in T] for j in range(h)]

    def new_scratch(self, rng):
        a=[[F(rng.randint(-9,9)) for _ in ns] for ns in self.neighbors]
        c=[F(rng.randint(-9,9)) for _ in range(self.h)]
        return (a,c)

    def J(self,a):
        return [sum((coeff * a[s][r] for r, (_,coeff) in enumerate(self.neighbors[s])),F(0)) for s in range(self.v)]

    def R(self,c):
        cs=sum(c,F(0))
        return [sum((c[j] for j in T),F(0))/2-cs/6 for T in self.triples]

    def G(self,x):
        return [sum((x[t] for t in ts),F(0)) for ts in self.occurrences]

    def step(self,x,y, scratch, direction=1):
        """Run eight reversible gates in forward or exact inverse order."""
        a,c=scratch
        x=list(map(F,x))
        y=list(map(F,y))
        gx=self.G(x)
        def gate(k, sign):
            if k in (0,5):
                ja=self.J(a)
                sig = -1 if k==0 else 1
                for s in range(self.v): y[s] += sign*sig*ja[s]
            elif k in (1,4):
                rc=self.R(c)
                sig = -1 if k==1 else 1
                for s in range(self.v): y[s] += sign*sig*rc[s]
            elif k in (2,7):
                sig = 1 if k==2 else -1
                for s,ns in enumerate(self.neighbors):
                    for pos,(t,_) in enumerate(ns): a[s][pos] += sign*sig*x[t]
            elif k in (3,6):
                sig = 1 if k==3 else -1
                for j in range(self.h): c[j] += sign*sig*gx[j]
            else: raise AssertionError(k)
        if direction==1:
            for k in range(8): gate(k,1)
        else:
            for k in range(7,-1,-1): gate(k,-1)
        return y

def run():
    rng=random.Random(0xDFF)
    print('Independent exact-rational network validation')
    for h in (6,7,8):
        net=ReducedNetwork(h)
        for trial in range(3):
            x=[F(rng.randint(-6,6)) for _ in range(net.v)]
            y=[F(rng.randint(-6,6)) for _ in range(net.v)]
            scratch=net.new_scratch(rng)
            saved=([r.copy() for r in scratch[0]],scratch[1].copy())
            after=net.step(x,y,scratch,1)
            assert after == [q+p for q,p in zip(y,x)],(h,trial)
            assert scratch == saved,(h,trial,'forward scratch')
            inv=net.step(x,y,scratch,-1)
            assert inv == [q-p for q,p in zip(y,x)],(h,trial,'inverse')
            assert scratch == saved,(h,trial,'inverse scratch')
        print(f'PASS forward + inverse + arbitrary scratch restoration: h={h}, v={net.v}, trials=3')

    # Perform all 3 stages of the published 3-coordinate exchange.
    h=6
    net=ReducedNetwork(h)
    v=net.v
    # Flat coordinates to avoid large tensor dependencies.
    indices=[(i,j,k) for i in range(v) for j in range(v) for k in range(v)]
    X={d:F(rng.randint(-4,4)) for d in indices}
    Y={d:F(rng.randint(-4,4)) for d in indices}
    x0=X.copy();y0=Y.copy()
    for stage in range(3):
        other=[k for k in range(3) if k!=stage]
        for frozen in ((i,j) for i in range(v) for j in range(v)):
            keys=[]
            for t in range(v):
                key=[0,0,0]
                key[stage]=t
                for axis,value in zip(other,frozen): key[axis]=value
                keys.append(tuple(key))
            scratch=net.new_scratch(rng)
            saved=([r.copy() for r in scratch[0]],scratch[1].copy())
            if stage!=1:
                # Stage 1/3: X -> Y
                out=net.step([X[d] for d in keys],[Y[d] for d in keys],scratch,1)
                for d,value in zip(keys,out): Y[d]=value
            else:
                # Stage 2: inverse Y -> X
                out=net.step([Y[d] for d in keys],[X[d] for d in keys],scratch,-1)
                for d,value in zip(keys,out): X[d]=value
            assert scratch==saved
    assert all(X[d] == -y0[d] and Y[d]==x0[d] for d in indices)
    print(f'PASS three-stage bank exchange: h={h}, entries per bank={len(indices)}, invocations=1200, scratch restored')

    # Recompute all numeric claims from exact integer formulas with Decimal logs.
    def parameters(h,center):
        v=comb(h,3)
        d=comb(h-3,3)+3*(h-3)
        i0=3*v*v
        n0=v**3
        W=2*n0+i0*(v*d+center)
        Wstar=1<<(W-1).bit_length()
        m=h**3
        delta=2*n0-2*i0*center*h
        assert Wstar>=W and delta>0
        return (h,v,d,W,Wstar,m,delta)
    with localcontext() as ctx:
        ctx.prec=75
        for h,center in [(100,101),(24,25),(24,24)]:
            _,v,d,W,Wstar,m,delta=parameters(h,center)
            ratio=Decimal(delta)/Decimal(m*Wstar)
            gap=-(Decimal(1)-ratio).ln()/Decimal(m).ln()
            print(f'h={h}, centers={center}, Wstar=2^{Wstar.bit_length()-1}, delta={delta}, exponent_gap={gap:.25E}')
            if h==24 and center==24:
                assert gap > Decimal('5e-10')
            if h==100:
                assert W == 1873807244643542670000
                assert delta==6871402692000000
    print('PASS all reduced/original dimensions and exponent-gap calculations')

if __name__ == '__main__':run()
