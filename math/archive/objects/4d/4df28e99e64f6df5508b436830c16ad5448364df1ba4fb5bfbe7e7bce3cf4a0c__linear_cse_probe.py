"""Symbolic pre/post linear forms for Phase29 WFTA120. Generate global CSE graph.

Arithmetic counted: each distinct addition/subtraction of two register-valued
linear forms counts 1. No multiplications are introduced in the pre/post weaves.
All equalities hold over Z before reduction to any field, rather than relying
on finite-field accidents.
"""
from dataclasses import dataclass
from collections import Counter
from typing import Tuple
from wfta8 import before8, after8
from wfta15 import before3, before5, after3, after5
from crt15 import Cost

class Lin:
    __slots__=('c','vec','id')
    def __init__(self,c,vec,id):self.c,self.vec,self.id=c,vec,id
    def __add__(self,o):return self.c.combine(self,o,+1)
    def __sub__(self,o):return self.c.combine(self,o,-1)
    def __mod__(self,mod):return self
    def __repr__(self):return f'L{self.id}'

class Compiler:
    def __init__(self,n):
        self.n=n
        self.nodes=[]
        self.byvector={}
        self.reused=0
        for j in range(n):
            z=tuple(1 if k==j else 0 for k in range(n))
            self._new(z,('input',j))
    def _new(self,vec,inst):
        a=Lin(self,vec,len(self.nodes))
        self.nodes.append(inst)
        self.byvector[vec]=a
        return a
    @property
    def inp(self):return [self.byvector[tuple(1 if k==j else 0 for k in range(self.n))] for j in range(self.n)]
    def combine(self,a,b,sgn):
        if type(b)==int and b==0:return a
        if not isinstance(a,Lin) or not isinstance(b,Lin):raise TypeError((type(a),type(b)))
        v=tuple(x+sgn*y for x,y in zip(a.vec,b.vec))
        cached=self.byvector.get(v)
        if cached is not None:
            self.reused+=1
            return cached
        return self._new(v,('add' if sgn==1 else 'sub',a.id,b.id))
    def run(self,inputs,mod):
        regs=[None]*len(self.nodes)
        for idx,inst in enumerate(self.nodes):
            if inst[0]=='input':regs[idx]=inputs[inst[1]]
            else:
                op,i,j=inst
                regs[idx]=(regs[i]+regs[j])%mod if op=='add' else (regs[i]-regs[j])%mod
        return regs

def build_before():
    c=Compiler(120); a=c.inp; dummy=Cost();p=2013265921
    b8=[list(before8(tuple(a[8*v+j] for j in range(8)),p,dummy)) for v in range(15)]
    b3=[[[0]*8 for _ in range(3)] for _ in range(5)]
    for v5 in range(5):
        for t8 in range(8):
            xs=tuple(b8[(10*u3+6*v5)%15][t8] for u3 in range(3))
            vv=before3(xs,p,dummy)
            for u3 in range(3):b3[v5][u3][t8]=vv[u3]
    b5=[[[0]*8 for _ in range(3)] for _ in range(6)]
    for u3 in range(3):
        for t8 in range(8):
            xs=tuple(b3[v5][u3][t8] for v5 in range(5))
            vv=before5(xs,p,dummy)
            for v5 in range(6):b5[v5][u3][t8]=vv[v5]
    outputs=[b5[v5][u3][t8].id for v5 in range(6) for u3 in range(3) for t8 in range(8)]
    print('BEFORE counted legacy',dummy.adds,'compiled adds',len(c.nodes)-120,'reused',c.reused,'unique out',len(set(outputs)))
    return c,outputs

def build_after():
    c=Compiler(144);s=c.inp;dummy=Cost();p=2013265921
    scaled=[[[s[(v5*3+u3)*8+t8] for t8 in range(8)] for u3 in range(3)] for v5 in range(6)]
    p5=[[[0]*8 for _ in range(3)] for _ in range(5)]
    for u3 in range(3):
        for t8 in range(8):
            vv=after5(tuple(scaled[v5][u3][t8] for v5 in range(6)),p,dummy)
            for v5 in range(5):p5[v5][u3][t8]=vv[v5]
    p3=[[0]*8 for _ in range(15)]
    for v5 in range(5):
        for t8 in range(8):
            vv=after3(tuple(p5[v5][u3][t8] for u3 in range(3)),p,dummy)
            for u3 in range(3):p3[(5*u3+3*v5)%15][t8]=vv[u3]
    out=[]
    for v in range(15):out.extend(after8(tuple(p3[v]),p,dummy))
    outputs=[x.id for x in out]
    print('AFTER counted legacy',dummy.adds,'compiled adds',len(c.nodes)-144,'reused',c.reused,'unique out',len(set(outputs)))
    return c,outputs

if __name__=='__main__':
    a,b=build_before();c,d=build_after()
    print('Total',len(a.nodes)-120+len(c.nodes)-144,'old',1038)
