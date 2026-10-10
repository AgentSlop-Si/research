"""Phase 25: affine-run exact Fourier inputs and zigzag Green-sum controls.

No sub-NlogN FFT for arbitrary input is claimed. All field-operation
complexities assume F_998244353 and N | 998244352.

The key positive result: if the input is geometric when traversed in a
permutation order made from r arithmetic runs, the Fourier transform is
computed with O(rN) field operations; it need not be close to ANY cyclic
stride under rank(W-Z^a).

The key falsification: two strongly noncommuting Green resolvents can have a
well-conditioned O(N)-apply, O(N)-inverse sum and still cannot approximate
an arbitrary-input DFT in spectral norm because of a constant cut rank.
"""
from __future__ import annotations
from dataclasses import dataclass
from phase23_resolvent import P, root, sqrt_mod, batch_invert_nonzero
from phase24_ordering import successor_of_order, cycle_rank_difference


def zigzag_order(n: int)->list[int]:
    if n<8 or n&(n-1):
        raise ValueError('power of two n >= 8 required')
    return list(range(0,n,2))+list(range(n-1,0,-2))


def affine_runs_zigzag(n: int)->list[tuple[int,int,int,int]]:
    """List (input-time start, run length, first spatial index, stride)."""
    m=n//2
    return [(0,m,0,2),(m,m,n-1,-2)]


def order_from_affine_runs(n:int,runs:list[tuple[int,int,int,int]])->list[int]:
    L=[-1]*n
    for t, length, first, stride in runs:
        if t<0 or length<0 or t+length>n:raise ValueError('invalid run')
        for u in range(length):
            if L[t+u]!=-1:raise ValueError('runs overlap in time')
            L[t+u]=(first+stride*u)%n
    seen=[False]*n
    for j in L:
        if j<0 or seen[j]:
            raise ValueError('runs must cover time indices and permute coordinates')
        seen[j]=True
    return L


def permuted_geometric_input(order:list[int],z:int)->list[int]:
    n=len(order)
    out=[0]*n; v=1
    for j in order:
        out[j]=v
        v=v*(z%P)%P
    return out


def _one_affine_run_contribution(n:int,omega:int,z:int,
                                 t0:int,length:int,first:int,stride:int)->list[int]:
    """One run's contributions to all Fourier frequencies, O(N) field work.

    Every denominator in the run is batch-inverted in linear field work.
    Root-of-unity 0/0 cases have exact value length, no division required.
    """
    za=pow(z,t0,P); zm=pow(z,length,P)
    step=pow(omega,stride%n,P)
    front=pow(omega,first%n,P)
    numerator_step=pow(omega,(stride*length)%n,P)
    cur=cur_first=cur_num=1
    vals=[0]*n; ds=[]; positions=[]
    for k in range(n):
        rat=z*cur%P
        if rat==1:
            vals[k]=za*cur_first%P*(length%P)%P
        else:
            numerator=(1-zm*cur_num)%P
            vals[k]=za*cur_first%P*numerator%P
            ds.append((1-rat)%P)
            positions.append(k)
        cur=cur*step%P
        cur_first=cur_first*front%P
        cur_num=cur_num*numerator_step%P
    if ds:
        inv=batch_invert_nonzero(ds)
        for k,v in zip(positions,inv):
            vals[k]=vals[k]*v%P
    return vals


def fourier_affine_geometric(n:int,z:int,
                runs:list[tuple[int,int,int,int]])->list[int]:
    """Normalized N-point DFT of x[order[t]]=z^t in O(rN) field work.

    r = number of affine runs. Memory O(N) beyond supplied runs and output.
    Precomputation O(r log N) binary exponentiation field operations.
    This is a structured-input executor, not an arbitrary-vector FFT.
    """
    order_from_affine_runs(n,runs)  # optional O(N) input validation
    w=root(n)
    inv_sqrt=pow(sqrt_mod(n),-1,P)
    out=[0]*n
    z%=P
    for t0,length,first,stride in runs:
        run=_one_affine_run_contribution(n,w,z,t0,length,first,stride)
        for k in range(n):out[k]=(out[k]+run[k])%P
    return [a*inv_sqrt%P for a in out]


def zigzag_geometric_fft(n:int,z:int)->list[int]:
    return fourier_affine_geometric(n,z,affine_runs_zigzag(n))


def direct_dft(x:list[int])->list[int]:
    """Independent O(N^2) exact reference, used ONLY for small tests."""
    n=len(x);w=root(n)
    inv_sqrt=pow(sqrt_mod(n),-1,P)
    y=[0]*n
    for k in range(n):
        r=pow(w,k,P);t=1;s=0
        for a in x:
            s=(s+(a%P)*t)%P
            t=t*r%P
        y[k]=s*inv_sqrt%P
    return y


def cyclic_shift_successor(n:int)->list[int]:
    return [(j+1)%n for j in range(n)]


def _compose(A:list[int],B:list[int])->list[int]:
    return [A[B[j]] for j in range(len(A))]


def permutation_difference_rank(A:list[int],B:list[int])->int:
    """rank(P_A-P_B) by cycles, exact over every field, O(N)."""
    n=len(A)
    if sorted(A)!=list(range(n)) or sorted(B)!=list(range(n)):
        raise ValueError('permutations required')
    invB=[0]*n
    for j,b in enumerate(B):invB[b]=j
    return cycle_rank_difference([invB[A[j]] for j in range(n)],a=0)


def all_stride_ranks(n:int)->list[int]:
    W=successor_of_order(zigzag_order(n))
    return [cycle_rank_difference(W,a) for a in range(1,n)]


def zigzag_commutator_rank(n:int)->int:
    """Exact rank(WZ-ZW), valid over any field; equals N-2."""
    W=successor_of_order(zigzag_order(n))
    Z=cyclic_shift_successor(n)
    return permutation_difference_rank(_compose(W,Z),_compose(Z,W))


def cyclic_green_apply(order:list[int],alpha:int,x:list[int])->list[int]:
    """Solve (I-alpha W)y=x in O(N) field operations for W successor in order."""
    n=len(order)
    if len(x)!=n:raise ValueError('wrong RHS size')
    alpha%=P
    an=pow(alpha,n,P)
    if an==1:raise ZeroDivisionError('resonant cyclic Green denominator')
    seq=[x[j]%P for j in order]
    tail=0
    for t in range(1,n):
        tail=alpha*(tail+seq[t])%P
    y0=(seq[0]+tail)*pow((1-an)%P,-1,P)%P
    ans=[0]*n
    v=y0
    for t,j in enumerate(order):
        if t:
            v=(seq[t]+alpha*v)%P
        ans[j]=v
    return ans


def apply_sparse_A(order:list[int],alpha:int,x:list[int])->list[int]:
    """A x=(I-alpha W)x, O(N)."""
    n=len(order)
    if len(x)!=n:raise ValueError('wrong RHS size')
    alpha%=P
    y=x.copy()
    for t,j in enumerate(order):
        y[order[(t+1)%n]]=(y[order[(t+1)%n]]-alpha*x[j])%P
    return y


def green_sum_apply(n:int,alpha:int,beta:int,x:list[int])->list[int]:
    zig=zigzag_order(n)
    g1=cyclic_green_apply(zig,alpha,x)
    g2=cyclic_green_apply(list(range(n)),beta,x)
    return [(a+b)%P for a,b in zip(g1,g2)]


@dataclass
class BandLU:
    """Exact field LU for 5-diagonal matrix with nonzero leading pivots.

    Store lower multipliers in offset -1,-2 slots and upper U on +1,+2.
    Each solve is O(N) field operations, memory O(N). No pivoting.
    """
    rows:list[list[int]]
    n:int
    inv_pivots:list[int]

    def _get(self,i:int,j:int)->int:
        if not (0<=i<self.n and 0<=j<self.n) or abs(j-i)>2:return 0
        return self.rows[i][j-i+2]

    def _set(self,i:int,j:int,v:int)->None:
        if abs(j-i)>2:raise ValueError('out of band')
        self.rows[i][j-i+2]=v%P

    @classmethod
    def factor(cls, rows:list[list[int]])->'BandLU':
        obj=cls([r.copy() for r in rows],len(rows),[0]*len(rows))
        n=obj.n
        for i in range(n):
            pivot=obj._get(i,i)
            if pivot==0:raise ArithmeticError('zero pivot; choose nonsingular parameters')
            invpivot=pow(pivot,-1,P)
            obj.inv_pivots[i]=invpivot
            for j in range(i+1,min(n,i+3)):
                a=obj._get(j,i)
                if not a:continue
                factor=a*invpivot%P
                obj._set(j,i,factor)
                for k in range(i+1,min(n,i+3)):
                    obj._set(j,k,obj._get(j,k)-factor*obj._get(i,k))
        return obj

    def solve(self,b:list[int])->list[int]:
        n=self.n
        if len(b)!=n:raise ValueError('bad RHS length')
        y=[0]*n
        for i in range(n):
            v=b[i]
            if i>=1:v-=self._get(i,i-1)*y[i-1]
            if i>=2:v-=self._get(i,i-2)*y[i-2]
            y[i]=v%P
        x=[0]*n
        for i in range(n-1,-1,-1):
            v=y[i]
            if i+1<n:v-=self._get(i,i+1)*x[i+1]
            if i+2<n:v-=self._get(i,i+2)*x[i+2]
            x[i]=v*self.inv_pivots[i]%P
        return x


@dataclass
class ZigzagGreenSumInverse:
    """O(N) exact inverse application for S=G_W+G_Z, two unrelated cycles.

    Use S^-1=B(A+B)^-1 A, A=I-alpha W, B=I-beta Z.
    A+B is pentadiagonal + one rank-1 wrap correction.
    """
    n:int
    alpha:int
    beta:int
    band:BandLU
    h:list[int]
    correction_inverse:int
    zig:list[int]
    nat:list[int]

    @classmethod
    def create(cls,n:int,alpha:int,beta:int)->'ZigzagGreenSumInverse':
        zig=zigzag_order(n);nat=list(range(n))
        alpha%=P;beta%=P
        if pow(alpha,n,P)==1 or pow(beta,n,P)==1:
            raise ArithmeticError('a cyclic Green denominator is singular')
        # T=2I-alpha W-beta Z_open, where Z_open has no n-1->0 edge.
        rows=[[0]*5 for _ in range(n)]
        for j in range(n):rows[j][2]=2
        for t,j in enumerate(zig):
            i=zig[(t+1)%n]
            if abs(i-j)>2:raise AssertionError('zigzag ceased to be banded')
            rows[i][j-i+2]=(rows[i][j-i+2]-alpha)%P
        for j in range(n-1):
            i=j+1
            rows[i][j-i+2]=(rows[i][j-i+2]-beta)%P
        band=BandLU.factor(rows)
        # A+B=T+u v^T, u=-beta e_0, v=e_{n-1}.
        u=[0]*n;u[0]=-beta%P
        h=band.solve(u)
        denom=(1+h[-1])%P
        if not denom:raise ArithmeticError('rank-one correction singular')
        return cls(n,alpha,beta,band,h,pow(denom,-1,P),zig,nat)

    def apply(self,x:list[int])->list[int]:
        if len(x)!=self.n:raise ValueError('wrong RHS length')
        ax=apply_sparse_A(self.zig,self.alpha,x)
        y=self.band.solve(ax)
        coefficient=y[-1]*self.correction_inverse%P
        corrected=[(a-coefficient*h)%P for a,h in zip(y,self.h)]
        return apply_sparse_A(self.nat,self.beta,corrected)


def green_sum_inverse_via_solve(n:int,alpha:int,beta:int,x:list[int])->list[int]:
    return ZigzagGreenSumInverse.create(n,alpha,beta).apply(x)
