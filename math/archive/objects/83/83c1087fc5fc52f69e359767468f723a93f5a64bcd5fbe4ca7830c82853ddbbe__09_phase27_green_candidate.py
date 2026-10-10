"""Phase 27 non-affine Green-sum products, exact finite-field forward/transpose.

Each term is L*(I-alpha*W)^-1*R for a random Hamiltonian cycle W.
Each application and transpose application takes O(N) field arithmetic.
This is a candidate generator only, not a Fourier transform algorithm.
"""
from __future__ import annotations
from dataclasses import dataclass
import random
from phase27_fourier_recovery import P,root
from phase27_affine_gap import random_hamiltonian


def inverse_green_cycle(order:list[int],alpha:int,x:list[int],deninv:int)->list[int]:
    n=len(order)
    a=alpha%P
    tmp=0
    for j in order:
        tmp=(a*tmp+x[j])%P
    prev=tmp*deninv%P
    out=[0]*n
    for j in order:
        prev=(a*prev+x[j])%P
        out[j]=prev
    return out


@dataclass
class GreenTerm:
    order:list[int]
    alpha:int
    left:list[int]
    right:list[int]

    def __post_init__(self):
        n=len(self.order)
        if any(len(v)!=n for v in (self.left,self.right)):
            raise ValueError('size')
        den=(1-pow(self.alpha,n,P))%P
        if not den:raise ZeroDivisionError('singular Green denominator')
        self.deninv=pow(den,-1,P)
        self.reverse_order=self.order[::-1]

    def apply(self,x:list[int])->list[int]:
        v=[x[i]*self.right[i]%P for i in range(len(x))]
        y=inverse_green_cycle(self.order,self.alpha,v,self.deninv)
        return [self.left[i]*y[i]%P for i in range(len(x))]

    def transpose(self,x:list[int])->list[int]:
        v=[x[i]*self.left[i]%P for i in range(len(x))]
        y=inverse_green_cycle(self.reverse_order,self.alpha,v,self.deninv)
        return [self.right[i]*y[i]%P for i in range(len(x))]


@dataclass
class GreenSum:
    terms:list[GreenTerm]
    def apply(self,x:list[int])->list[int]:
        out=[0]*len(x)
        for term in self.terms:
            v=term.apply(x)
            for i in range(len(x)):
                out[i]=(out[i]+v[i])%P
        return out
    def transpose(self,x:list[int])->list[int]:
        out=[0]*len(x)
        for term in self.terms:
            v=term.transpose(x)
            for i in range(len(x)):
                out[i]=(out[i]+v[i])%P
        return out


class GreenCircuit:
    def __init__(self,layers:list[GreenSum]):
        if not layers:raise ValueError('empty circuit')
        self.layers=layers
    def apply(self,x:list[int])->list[int]:
        for layer in self.layers:
            x=layer.apply(x)
        return x
    def transpose(self,x:list[int])->list[int]:
        for layer in self.layers[::-1]:
            x=layer.transpose(x)
        return x


def seeded_nonaffine_circuit(n:int,seed:int=27,layers:int=2,terms:int=2)->GreenCircuit:
    rng=random.Random(seed)
    w=root(n)
    phase=[1]*n
    for i in range(1,n):phase[i]=phase[i-1]*w%P
    out=[]
    alpha_candidates=[2,3,5,7,11,13]
    for layer in range(layers):
        members=[]
        for t in range(terms):
            s=rng.randrange(1,2**31)
            # Generate an ordered N-cycle for the Green recurrence
            nodes=list(range(n));rng.shuffle(nodes)
            a=alpha_candidates[(layer*terms+t)%len(alpha_candidates)]
            left=[phase[rng.randrange(n)] for _ in range(n)]
            right=[phase[rng.randrange(n)] for _ in range(n)]
            members.append(GreenTerm(nodes,a,left,right))
        out.append(GreenSum(members))
    return GreenCircuit(out)


def dot(a:list[int],b:list[int])->int:
    return sum(x*y for x,y in zip(a,b))%P

if __name__=='__main__':
    from phase27_fourier_recovery import recover
    for n in (16,64,256,1024):
        g=seeded_nonaffine_circuit(n,2700+n)
        report=recover(g.apply,g.transpose,n,max_other_columns=8,trials=2)
        print(n,report.status,report.reason,report.oracle_calls_forward,report.oracle_calls_transpose)
