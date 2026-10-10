"""Phase 25 extension: full *natural-cut* rank with linear Green-sum inverse.

Twisted zigzag W has jump a=N/2+2 within even/odd classes, joined by
2 bridge edges. In natural order it has O(N) edges crossing the middle,
but the four-track order below turns 2I-alpha W-beta Z into a width-6
banded matrix plus four explicit matrix-entry updates.

Exact O(N) forward and inverse field-work controls. No faster general FFT.
"""
from __future__ import annotations
from dataclasses import dataclass
from phase23_resolvent import P
from phase24_ordering import successor_of_order,cycle_rank_difference
from phase25_affine import (
    apply_sparse_A, cyclic_green_apply, cyclic_shift_successor,
    permutation_difference_rank, order_from_affine_runs
)


def twisted_order(n:int)->list[int]:
    if n<16 or n&(n-1):raise ValueError('power of two n>=16')
    m=n//2;a=m+2
    L=[a*t%n for t in range(m)] + [(n-1-a*t)%n for t in range(m)]
    if len(set(L))!=n:raise AssertionError('twisted ordering not Hamiltonian')
    return L


def twisted_runs(n:int)->list[tuple[int,int,int,int]]:
    m=n//2;a=m+2
    return [(0,m,0,a),(m,m,n-1,-a)]


def four_track_order(n:int)->list[int]:
    """N physical coordinates, reordered by 4-track adjacent cells."""
    if n<16 or n&(n-1):raise ValueError('power of two n>=16')
    m=n//2;h=m//2
    p=[]
    for t in range(h):
        for q in (t,t+h):p.extend((2*q,2*q+1))
    return p


def crosscut_edge_count(n:int,order:list[int])->int:
    m=n//2
    w=successor_of_order(order)
    return sum(w[j]<m for j in range(m,n))


@dataclass
class FixedBandLU:
    data:list[list[int]]
    width:int
    invpiv:list[int]

    @property
    def n(self):return len(self.data)

    def get(self,i,j):
        if i<0 or i>=self.n or j<0 or j>=self.n or abs(i-j)>self.width:return 0
        return self.data[i][j-i+self.width]

    def set(self,i,j,v):
        if abs(i-j)>self.width:raise ValueError('outside band')
        self.data[i][j-i+self.width]=v%P

    @classmethod
    def factor(cls,rows,width):
        n=len(rows)
        factor=cls([row.copy() for row in rows],width,[0]*n)
        for i in range(n):
            pivot=factor.get(i,i)
            if not pivot:raise ArithmeticError('zero band pivot')
            inv=pow(pivot,-1,P)
            factor.invpiv[i]=inv
            for j in range(i+1,min(n,i+width+1)):
                a=factor.get(j,i)
                if not a:continue
                coef=a*inv%P
                factor.set(j,i,coef)
                for k in range(i+1,min(n,i+width+1)):
                    factor.set(j,k,factor.get(j,k)-coef*factor.get(i,k))
        return factor

    def solve(self,x):
        n=self.n;w=self.width
        if len(x)!=n:raise ValueError('RHS length')
        y=[0]*n
        for i in range(n):
            v=x[i]
            for j in range(max(0,i-w),i):v-=self.get(i,j)*y[j]
            y[i]=v%P
        out=[0]*n
        for i in range(n-1,-1,-1):
            v=y[i]
            for j in range(i+1,min(n,i+w+1)):v-=self.get(i,j)*out[j]
            out[i]=v*self.invpiv[i]%P
        return out


def _dense_solve(A,b):
    n=len(A)
    if not n:return []
    v=[[x%P for x in row]+[b[i]%P] for i,row in enumerate(A)]
    for j in range(n):
        p=next((i for i in range(j,n) if v[i][j]),None)
        if p is None:raise ArithmeticError('Woodbury small system singular')
        v[j],v[p]=v[p],v[j]
        inv=pow(v[j][j],-1,P)
        for k in range(j,n+1):v[j][k]=v[j][k]*inv%P
        for i in range(n):
            if i==j:continue
            f=v[i][j]
            for k in range(j,n+1):v[i][k]=(v[i][k]-f*v[j][k])%P
    return [v[i][-1] for i in range(n)]


@dataclass
class TwistedGreenSumInverse:
    n:int
    alpha:int
    beta:int
    p:list[int]
    zig:list[int]
    natural:list[int]
    band:FixedBandLU
    updates:list[tuple[int,int,int]]
    h:list[list[int]]
    small:list[list[int]]

    @classmethod
    def create(cls,n:int,alpha:int,beta:int):
        Worder=twisted_order(n);natural=list(range(n))
        alpha%=P;beta%=P
        if pow(alpha,n,P)==1 or pow(beta,n,P)==1:
            raise ArithmeticError('cyclic Green singular')
        W=successor_of_order(Worder)
        Z=cyclic_shift_successor(n)
        p=four_track_order(n)
        where=[0]*n
        for i,j in enumerate(p):where[j]=i
        width=6
        rows=[[0]*(2*width+1) for _ in range(n)]
        updates=[]
        for i in range(n):rows[i][width]=2
        for edge,coeff in ((W,-alpha),(Z,-beta)):
            for oldj,oldi in enumerate(edge):
                j=where[oldj];i=where[oldi]
                if abs(i-j)<=width:
                    rows[i][j-i+width]=(rows[i][j-i+width]+coeff)%P
                else:
                    updates.append((i,j,coeff%P))
        band=FixedBandLU.factor(rows,width)
        h=[]
        for i,j,v in updates:
            e=[0]*n;e[i]=v
            h.append(band.solve(e))
        small=[[(int(i==j)+h[j][updates[i][1]])%P
             for j in range(len(updates))] for i in range(len(updates))]
        # Verify nonsingularity when constructing, avoid false success.
        _dense_solve(small,[0]*len(updates))
        return cls(n,alpha,beta,p,Worder,natural,band,updates,h,small)

    def apply(self,x):
        if len(x)!=self.n:raise ValueError('wrong RHS length')
        ax=apply_sparse_A(self.zig,self.alpha,x)
        y=self.band.solve([ax[j] for j in self.p])
        rhs=[y[j] for i,j,v in self.updates]
        coeff=_dense_solve(self.small,rhs)
        correction=[(y[k]-sum(self.h[i][k]*coeff[i]
                     for i in range(len(self.updates))))%P for k in range(self.n)]
        natural=[0]*self.n
        for i,j in enumerate(self.p):natural[j]=correction[i]
        return apply_sparse_A(self.natural,self.beta,natural)


def twisted_green_sum_apply(n:int,alpha:int,beta:int,x:list[int])->list[int]:
    w=cyclic_green_apply(twisted_order(n),alpha,x)
    z=cyclic_green_apply(list(range(n)),beta,x)
    return [(a+b)%P for a,b in zip(w,z)]


def twisted_stride_ranks(n:int)->list[int]:
    W=successor_of_order(twisted_order(n))
    return [cycle_rank_difference(W,a) for a in range(1,n)]


def hidden_quarter_partition(n:int)->tuple[list[int],list[int]]:
    """Balanced low-cut partition: Q0 union Q2 versus Q1 union Q3.

    The 4-track order's first and second halves represent exactly these
    sets. For twisted a=N/2+2: 3 W edges and 2 Z edges cross J -> I.
    """
    if n<16 or n&(n-1):raise ValueError('power of two n>=16 required')
    q=n//4
    return (list(range(0,q))+list(range(2*q,3*q)),
            list(range(q,2*q))+list(range(3*q,4*q)))


def hidden_cut_edge_counts(n:int)->tuple[int,int]:
    left,right=hidden_quarter_partition(n)
    Lset=set(left)
    w=successor_of_order(twisted_order(n))
    z=cyclic_shift_successor(n)
    return (sum(w[j] in Lset for j in right),
            sum(z[j] in Lset for j in right))


def hidden_cut_spectral_error_floor(n:int)->float:
    """Rigorous lower bound for ||M-F||_2 for any M having this
    rank-5 balanced block, including outer monomial transformations.
    Bound positive for N>20; tends to 1/sqrt(2).
    """
    if n<16 or n&(n-1):raise ValueError('power of two n>=16 required')
    return (max(0.0,(n/4-5)/(n/2-5)))**0.5
