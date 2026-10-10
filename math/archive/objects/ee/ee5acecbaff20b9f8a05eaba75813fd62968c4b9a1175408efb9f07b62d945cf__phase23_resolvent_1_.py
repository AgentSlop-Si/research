"""Phase 23: exact O(N)-field-work real Fourier residual on exponential inputs.

The length-N real orthogonal Fourier residual C (as defined in Phase 22)
obeys C Z = R C with real 2x2 rotation blocks R and known seed v=C e0.
For g(z)=(1,z,...,z^(N-1)),
 C g(z)=(1-z**N)*(I-z*R)^(-1)*v when z**N != 1.
We solve all 1x1 and 2x2 blocks by batch inversion in O(N) field operations.
For Nth-root inputs, a Fourier-character shortcut gives the exact answer.
No general o(N log N) Fourier algorithm is claimed.
"""
from __future__ import annotations
from dataclasses import dataclass

P=998244353
PRIMITIVE=3

def root(n:int)->int:
    if n < 4 or n&(n-1) or (P-1)%n:
        raise ValueError('N must be a supported power of two >= 4')
    return pow(PRIMITIVE,-(P-1)//n,P)

def sqrt_mod(a:int)->int:
    a%=P
    if not a:return 0
    if pow(a,(P-1)//2,P)!=1:raise ValueError('not a square')
    q=P-1;s=0
    while q%2==0:q//=2;s+=1
    z=2
    while pow(z,(P-1)//2,P)!=P-1:z+=1
    c=pow(z,q,P);r=pow(a,(q+1)//2,P);t=pow(a,q,P);m=s
    while t!=1:
        xx=t*t%P;j=1
        while xx!=1:xx=xx*xx%P;j+=1
        b=pow(c,1<<(m-j-1),P)
        r=r*b%P;t=t*b*b%P;c=b*b%P;m=j
    return r

def batch_invert_nonzero(ds:list[int])->list[int]:
    """O(len(ds)) field multiplication, one field inversion (one exponentiation)."""
    n=len(ds);pref=[1]*(n+1)
    for i,d in enumerate(ds):
        if d%P==0:raise ZeroDivisionError('singular resolvent')
        pref[i+1]=pref[i]*d%P
    back=pow(pref[-1],P-2,P)
    result=[0]*n
    for i in range(n-1,-1,-1):
        result[i]=back*pref[i]%P
        back=back*ds[i]%P
    return result

@dataclass
class RealGreenFourier:
    n:int
    omega:int
    sqrt_n:int
    inv_sqrt_n:int
    sqrt2:int
    inv_sqrt2:int
    i:int
    angles:list[tuple[int,int]]

    @classmethod
    def create(cls,n:int)->'RealGreenFourier':
        w=root(n)
        sqn=sqrt_mod(n);sq2=sqrt_mod(2)
        sn=pow(sqn,-1,P);is2=pow(sq2,-1,P)
        im=pow(w,n//4,P)     # -i, because omega=exp(-2pi i/n)
        ip=pow(im,-1,P)      # +i
        i2=pow(2,-1,P);i2i=pow(2*ip%P,-1,P)
        wp=1;wm=1;winv=pow(w,-1,P)
        angles=[]
        for j in range(1,n//2):
            wp=wp*w%P;wm=wm*winv%P
            c=(wp+wm)*i2%P
            s=(wm-wp)*i2i%P
            angles.append((c,s))
        return cls(n,w,sqn,sn,sq2,is2,ip,angles)

    def geometric(self,z:int)->list[int]:
        """C*[1,z,...,z^(N-1)] in O(N) field operations and memory.

        A field square-root and transform root are precomputed in create().
        Excludes the cost of producing the explicit N-vector input, which
        is not necessary when the geometric progression is given by z.
        """
        n=self.n;h=n//2;z%=P
        zn=pow(z,n,P)
        out=[0]*n
        if zn==1:
            # The geometric input is exactly a character. Find its frequency
            # with a single O(N) orbit scan; no discrete-log oracle is used.
            target=z
            current=1;winv=pow(self.omega,-1,P)
            f=None
            for j in range(n):
                if current==target:
                    f=j;break
                current=current*winv%P
            if f is None:
                raise ArithmeticError('z^N=1 but root not in chosen orbit')
            if f==0:out[0]=self.sqrt_n
            elif f==h:out[1]=self.sqrt_n
            else:
                k=f if f<h else n-f
                v=self.sqrt_n*self.inv_sqrt2%P
                out[k+1]=v
                out[h+k]=v*self.i*(1 if f<h else -1)%P
            return out

        twoz=(2*z)%P;z2=z*z%P
        ds=[(1-z)%P,(1+z)%P]
        for c,_s in self.angles:
            ds.append((1-twoz*c+z2)%P)
        inv=batch_invert_nonzero(ds)
        factor=(1-zn)%P
        dc=self.inv_sqrt_n*factor%P
        out[0]=dc*inv[0]%P
        out[1]=dc*inv[1]%P
        amp=dc*self.sqrt2%P
        for j,(c,s) in enumerate(self.angles,1):
            iz=inv[j+1]
            out[j+1]=amp*(1-z*c)%P*iz%P
            out[h+j]=amp*z%P*s%P*iz%P
        return out

    def exponential_sum(self,nodes:list[int],weights:list[int])->list[int]:
        if len(nodes)!=len(weights):raise ValueError('nodes/weights size mismatch')
        out=[0]*self.n
        for z,a in zip(nodes,weights):
            if a%P==0:continue
            vec=self.geometric(z)
            for j,b in enumerate(vec):out[j]=(out[j]+a*b)%P
        return out


def synthesize_exponential_sequence(n:int,nodes:list[int],weights:list[int])->list[int]:
    if len(nodes)!=len(weights):raise ValueError('nodes/weights size mismatch')
    x=[0]*n
    for z,a in zip(nodes,weights):
        power=1
        for j in range(n):
            x[j]=(x[j]+a*power)%P
            power=power*z%P
    return x


def hankel_rank(x:list[int])->int:
    """EXPERIMENTAL O(N^3) diagnostic: rank of m-by-m leading Hankel, m=N/2."""
    n=len(x)
    if n&1 or n<4:raise ValueError('even length >=4 needed')
    m=n//2
    A=[[x[i+j]%P for j in range(m)] for i in range(m)]
    r=0
    for j in range(m):
        pivot=next((i for i in range(r,m) if A[i][j]),None)
        if pivot is None:continue
        A[r],A[pivot]=A[pivot],A[r]
        inverse=pow(A[r][j],-1,P)
        for i in range(r+1,m):
            if not A[i][j]:continue
            z=A[i][j]*inverse%P
            for k in range(j+1,m):A[i][k]=(A[i][k]-z*A[r][k])%P
            A[i][j]=0
        r+=1
        if r==m:break
    return r


def c_inverse_row_nonzeros(n:int,k:int)->int:
    """Exact number of nonzero entries in row k of C^T, N a power of 2.
    Odd k has N-1 entries. k=0,N/2 has N/2+1 entries.
    """
    root(n)
    if not 0<=k<n:raise ValueError('column index outside range')
    if k in (0,n//2):return n//2+1
    v=(k&-k).bit_length()-1
    return n-(1<<(v+1))+1


def discover_geometric_rank_at_most_two(x:list[int]):
    """Detect rank-0, rank-1 or distinct-node rank-2 exponential input in O(N).

    Returns (nodes,weights) with exact identity at every input index, or None.
    This is a restricted detector, NOT a general Prony factorization. Handles
    nodes that are Nth roots; the Green executor switches to its root branch.
    """
    n=len(x)
    if n<4:return None
    x=[v%P for v in x]
    if not any(x):return [],[]
    if x[0]:
        z=x[1]*pow(x[0],-1,P)%P
        a=x[0];p=1
        valid=True
        for observed in x:
            if a*p%P!=observed:
                valid=False;break
            p=p*z%P
        if valid:return [z],[a]
    if n<4:return None
    det=(x[1]*x[1]-x[0]*x[2])%P
    if not det:return None
    invdet=pow(det,-1,P)
    u=(x[1]*x[2]-x[0]*x[3])*invdet%P
    v=(x[1]*x[3]-x[2]*x[2])*invdet%P
    # Reject immediately if the inferred order-two recurrence fails anywhere.
    for k in range(n-2):
        if x[k+2]!=(u*x[k+1]+v*x[k])%P:return None
    discriminant=(u*u+4*v)%P
    try:sq=sqrt_mod(discriminant)
    except ValueError:return None
    if not sq:return None  # two equal roots require k*z^k terms, not this family
    inv2=pow(2,-1,P)
    z1=(u+sq)*inv2%P;z2=(u-sq)*inv2%P
    if z1==z2:return None
    a=(x[1]-x[0]*z2)*pow((z1-z2)%P,-1,P)%P
    b=(x[0]-a)%P
    return [z1,z2],[a,b]


def adaptive_real_transform(x:list[int],engine:RealGreenFourier|None=None):
    """Working adaptive executor. Green path iff <=2 geometric components.

    For arbitrary data we use an ordinary radix-two modular FFT, included
    explicitly for a complete correct algorithm (worst case O(N log N)).
    Returns (real-transform, method). Green detector and executor are O(N).
    """
    n=len(x)
    eng=engine if engine is not None else RealGreenFourier.create(n)
    if eng.n!=n:raise ValueError('engine has wrong transform size')
    structure=discover_geometric_rank_at_most_two(x)
    if structure is not None:
        nodes,weights=structure
        return eng.exponential_sum(nodes,weights),'green_rank_'+str(len(nodes))
    # Standard exact reference radix-two DFT and Phase22 parity post-transform.
    w=eng.omega
    a=[v%P for v in x]
    j=0
    for i in range(1,n):
        bit=n>>1
        while j&bit:j^=bit;bit>>=1
        j^=bit
        if i<j:a[i],a[j]=a[j],a[i]
    block=2
    while block<=n:
        base=pow(w,n//block,P)
        for lo in range(0,n,block):
            tw=1
            for j in range(block//2):
                even=a[lo+j];odd=a[lo+j+block//2]*tw%P
                a[lo+j]=(even+odd)%P
                a[lo+j+block//2]=(even-odd)%P
                tw=tw*base%P
        block<<=1
    out=[0]*n;h=n//2
    out[0]=a[0]*eng.inv_sqrt_n%P
    out[1]=a[h]*eng.inv_sqrt_n%P
    coeff=eng.inv_sqrt_n*eng.inv_sqrt2%P
    for j in range(1,h):
        out[j+1]=(a[j]+a[n-j])*coeff%P
        out[h+j]=(a[j]-a[n-j])*coeff%P*eng.i%P
    return out,'reference_fft_fallback'


def cyclic_difference(x:list[int],order:int=1)->list[int]:
    """(I-Z)^order x, with Z the cyclic right-shift; O(order*N) work."""
    if order<0:raise ValueError('negative difference order')
    out=[v%P for v in x]
    for _ in range(order):
        out=[(out[k]-out[k-1])%P for k in range(len(out))]
    return out


def _normalized_fourier_to_real_residual(f:list[int],eng:RealGreenFourier)->list[int]:
    """C=Q^-1 H^T F; the supplied spectrum already includes 1/sqrt(N)."""
    n=eng.n;h=n//2
    out=[0]*n;out[0]=f[0];out[1]=f[h]
    t=eng.inv_sqrt2
    for j in range(1,h):
        out[j+1]=(f[j]+f[n-j])*t%P
        out[h+j]=(f[j]-f[n-j])*t%P*eng.i%P
    return out


def real_transform_sparse_differences(x:list[int],eng:RealGreenFourier,
                                      order:int=1,max_nonzeros:int=2):
    """Exact sparse-cyclic-difference Green executor, O(N*(order+s)).

    Uses F(I-Z)^order = (I-D)^order F. Singular zero-frequency
    component is calibrated by direct summation. Returns None if not
    sparse enough. No arbitrary FFT complexity saving is claimed.
    """
    n=len(x)
    if n!=eng.n:raise ValueError('transform size mismatch')
    if order<1:raise ValueError('order must be positive')
    diff=cyclic_difference(x,order)
    support=[(j,v) for j,v in enumerate(diff) if v]
    if len(support)>max_nonzeros:return None
    # Evaluate F(diff) in O(N*s) without a full FFT: one geometric
    # frequency progression per active time-coordinate of diff.
    accum=[0]*n
    for j,a in support:
        frequency_step=pow(eng.omega,j,P)
        power=1
        for k in range(n):
            accum[k]=(accum[k]+a*power)%P
            power=power*frequency_step%P
    # Diagonal Green inverse of (I-D)^order on the nonzero-frequency
    # subspace: batch-invert all (1-omega^k) factors in linear field work.
    omega_power=1
    denoms=[]
    for k in range(1,n):
        omega_power=omega_power*eng.omega%P
        denoms.append((1-omega_power)%P)
    inverses=batch_invert_nonzero(denoms)
    f=[0]*n
    f[0]=sum(x)*eng.inv_sqrt_n%P
    for k in range(1,n):
        f[k]=accum[k]*eng.inv_sqrt_n%P*pow(inverses[k-1],order,P)%P
    return _normalized_fourier_to_real_residual(f,eng)


def adaptive_real_transform_structured(x:list[int],eng:RealGreenFourier|None=None,
                                       max_difference_order:int=2,
                                       max_changes:int=2):
    """Adaptive exact transform: rank<=2 exponentials, sparse differences,
    else unchanged standard radix-two NTT. O(N log N) worst case.
    """
    n=len(x)
    model=eng if eng is not None else RealGreenFourier.create(n)
    if model.n!=n:raise ValueError('engine size mismatch')
    structure=discover_geometric_rank_at_most_two(x)
    if structure is not None:
        nodes,weights=structure
        return model.exponential_sum(nodes,weights),'green_rank_'+str(len(nodes))
    for order in range(1,max_difference_order+1):
        result=real_transform_sparse_differences(x,model,order,max_changes)
        if result is not None:return result,f'green_difference_r{order}'
    return adaptive_real_transform(x,model)
