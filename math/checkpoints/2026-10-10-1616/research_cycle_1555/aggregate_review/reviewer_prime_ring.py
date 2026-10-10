"""Fresh standard-library integer/cyclotomic verification of four-chain family."""
from pathlib import Path
import json

class PrimeRing:
    def __init__(self,p):
        self.p=p; self.d=p-1;self.zero=(0,)*self.d;self.one=(1,)+(0,)*(self.d-1)
        self.powers=[tuple(int(i==k) for i in range(self.d)) for k in range(self.d)]+[(-1,)*self.d]
    def z(self,k):return self.powers[k%self.p]
    def add(self,a,b):return tuple(x+y for x,y in zip(a,b))
    def neg(self,a):return tuple(-x for x in a)
    def sub(self,a,b):return self.add(a,self.neg(b))
    def scalar(self,a,k):return tuple(x*k for x in a)
    def mul(self,a,b):
        c=[0]*(2*self.d-1)
        for i,x in enumerate(a):
            if x:
                for j,y in enumerate(b):
                    if y:c[i+j]+=x*y
        for k in range(len(c)-1,self.d-1,-1):
            for j in range(self.d):c[k-self.d+j]-=c[k]
        return tuple(c[:self.d])
    def sum(self,xs):
        s=self.zero
        for x in xs:s=self.add(s,x)
        return s
    def conj(self,a):return self.sum(self.scalar(self.z(-k),v) for k,v in enumerate(a))

