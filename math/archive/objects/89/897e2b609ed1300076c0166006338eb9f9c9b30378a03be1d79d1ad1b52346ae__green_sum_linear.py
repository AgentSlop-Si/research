"""An *O(N)-applicable* sum-of-two-Green escape layer, with exact audit code.

Important: a cheap operator with dense inverse and high operator-Schmidt rank
is NOT a factorization of the DFT.
"""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from phase11_gate import P, eye, matmul, mod_inverse, mod_rank, matrix_realignment

@dataclass
class PermutationGreen:
    pi: np.ndarray
    a: int

    def __post_init__(self):
        self.pi=np.asarray(self.pi,dtype=np.int64)
        n=len(self.pi)
        assert np.array_equal(np.sort(self.pi),np.arange(n))
        seen=np.zeros(n,dtype=bool)
        self.cycles=[]
        for i in range(n):
            if seen[i]: continue
            cycle=[]; j=i
            while not seen[j]:
                seen[j]=True; cycle.append(j); j=int(self.pi[j])
            assert j==i
            den=(1-pow(self.a,len(cycle),P))%P
            if not den: raise ValueError('singular Green cycle')
            self.cycles.append((cycle,pow(den,-1,P)))
        self.preparation_ops=sum(len(c) for c,_ in self.cycles)

    def apply(self,x):
        x=np.asarray(x,dtype=np.int64)%P
        y=np.zeros_like(x)
        for c,invden in self.cycles:
            acc=0; coeff=1
            for j in c:
                acc=(acc+coeff*int(x[j]))%P
                coeff=coeff*self.a%P
            y[c[0]]=acc*invden%P
            for ix in range(len(c)-1,0,-1):
                j=c[ix]; jp=c[(ix+1)%len(c)]
                y[j]=(int(x[j])+self.a*int(y[jp]))%P
        return y

    def explicit_inverse_sparse(self):
        n=len(self.pi)
        s=eye(n)
        s[np.arange(n),self.pi]=(s[np.arange(n),self.pi]-self.a)%P
        return s

    def explicit_dense(self):
        """For audits only! O(N^2) calls, not used to apply the operator."""
        n=len(self.pi)
        return np.column_stack([self.apply(eye(n)[:,i]) for i in range(n)])

class TwoGreenSum:
    def __init__(self,g1,g2): self.g1,self.g2=g1,g2
    def apply(self,x): return (self.g1.apply(x)+self.g2.apply(x))%P
    def explicit_dense(self):
        n=len(self.g1.pi)
        return np.column_stack([self.apply(eye(n)[:,i]) for i in range(n)])


def find_escape_layer(n,seed=2026,trials=60):
    rng=np.random.default_rng(seed)
    a=int(np.sqrt(n))
    for rep in range(trials):
        pi1=rng.permutation(n); pi2=rng.permutation(n)
        try:
            g1=PermutationGreen(pi1,3)
            g2=PermutationGreen(pi2,5)
        except ValueError: continue
        layer=TwoGreenSum(g1,g2)
        explicit=layer.explicit_dense()
        try: inverse=mod_inverse(explicit)
        except ValueError: continue
        inv_support=np.count_nonzero(inverse,axis=1)
        if min(inv_support)!=n: continue
        schmidt=mod_rank(matrix_realignment(explicit,a,a)) if a*a==n else None
        if schmidt==n:
            for _ in range(6):
                x=rng.integers(0,P,size=n,dtype=np.int64)
                assert np.array_equal(layer.apply(x),matmul(explicit,x))
            assert np.array_equal(matmul(inverse,explicit),eye(n))
            return {'n':n,'seed':seed,'trial':rep+1,
                    'a1':3,'a2':5,'permutation_1':list(map(int,pi1)),
                    'permutation_2':list(map(int,pi2)),
                    'row_support_min':int(min(inv_support)),
                    'row_support_max':int(max(inv_support)),
                    'schmidt_rank':schmidt,'number_green_solvers_per_input':2,
                    'green_cycle_count':len(g1.cycles)+len(g2.cycles)}
    return {'n':n,'not_found':True}

if __name__=='__main__':
    import json
    for n in (4,16,64):
        z=find_escape_layer(n)
        print(json.dumps(z)[:500])

@dataclass
class WeightedPermutationGreen:
    """G=(I-diag(weights)*P)^(-1); arbitrary permutation and per-row weights.

    After O(N) preparation with one field inversion per permutation cycle,
    each fresh-vector application uses O(N) field operations.
    """
    pi: np.ndarray
    weights: np.ndarray

    def __post_init__(self):
        self.pi=np.asarray(self.pi,dtype=np.int64)
        self.weights=np.asarray(self.weights,dtype=np.int64)%P
        n=len(self.pi)
        assert len(self.weights)==n and np.array_equal(np.sort(self.pi),np.arange(n))
        seen=np.zeros(n,dtype=bool)
        self.cycles=[]
        for i in range(n):
            if seen[i]: continue
            cy=[];j=i;product=1
            while not seen[j]:
                seen[j]=True;cy.append(j)
                product=product*int(self.weights[j])%P
                j=int(self.pi[j])
            assert j==i
            den=(1-product)%P
            if den==0: raise ValueError('singular weighted Green cycle')
            self.cycles.append((cy,pow(den,-1,P)))

    def apply(self,x):
        x=np.asarray(x,dtype=np.int64)%P
        out=np.zeros_like(x)
        for cy,invden in self.cycles:
            acc=0; prefix=1
            for j in cy:
                acc=(acc+prefix*int(x[j]))%P
                prefix=prefix*int(self.weights[j])%P
            out[cy[0]]=acc*invden%P
            for k in range(len(cy)-1,0,-1):
                j=cy[k]; jp=cy[(k+1)%len(cy)]
                out[j]=(int(x[j])+int(self.weights[j])*int(out[jp]))%P
        return out

    def explicit_inverse_sparse(self):
        n=len(self.pi);s=eye(n)
        s[np.arange(n),self.pi]=(s[np.arange(n),self.pi]-self.weights)%P
        return s

    def explicit_dense(self):
        n=len(self.pi)
        return np.column_stack([self.apply(eye(n)[:,i]) for i in range(n)])


def find_weighted_escape(n,seed=2027,trials=40):
    rng=np.random.default_rng(seed)
    a=int(np.sqrt(n));assert a*a==n
    for trial in range(1,trials+1):
        pi1=rng.permutation(n);pi2=rng.permutation(n)
        w1=rng.integers(2,P,size=n,dtype=np.int64)
        w2=rng.integers(2,P,size=n,dtype=np.int64)
        try:
            g1=WeightedPermutationGreen(pi1,w1)
            g2=WeightedPermutationGreen(pi2,w2)
        except ValueError: continue
        layer=TwoGreenSum(g1,g2)
        dense=layer.explicit_dense()
        try: inv=mod_inverse(dense)
        except ValueError: continue
        if np.count_nonzero(inv,axis=1).min()!=n: continue
        schmidt=mod_rank(matrix_realignment(dense,a,a))
        if schmidt!=n: continue
        ones=np.ones(n,dtype=np.int64)
        y=layer.apply(ones)
        if len(set(map(int,y)))==1: continue
        for _ in range(5):
            x=rng.integers(0,P,size=n,dtype=np.int64)
            assert np.array_equal(layer.apply(x),matmul(dense,x))
        assert np.array_equal(matmul(inv,dense),eye(n))
        return {'n':n,'seed':seed,'trial':trial,'schmidt_rank':schmidt,
                'inverse_row_support_min':int(np.count_nonzero(inv,axis=1).min()),
                'inverse_row_support_max':int(np.count_nonzero(inv,axis=1).max()),
                'one_vector_output_not_constant':len(set(map(int,y)))>1,
                'permutation1':list(map(int,pi1)),'permutation2':list(map(int,pi2)),
                'weights1':list(map(int,w1)),'weights2':list(map(int,w2))}
    return {'n':n,'not_found':True}
