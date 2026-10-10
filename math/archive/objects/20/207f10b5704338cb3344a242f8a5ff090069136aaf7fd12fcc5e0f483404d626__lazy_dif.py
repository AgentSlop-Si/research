"""Hero #1 Phase 24: lazily evaluated, in-place exact radix-two DIF Fourier DAG.

The input-independent butterfly DAG is exactly the standard radix-two DIF FFT.
Visiting requested Fourier outputs (in any order) expands their prerequisite
butterfly nodes once. If the client later requests the whole transform, the
additional work completes exactly the same arithmetic graph; already computed
butterflies are not repeated. Storage O(N), not O(N log N).

Use N | p-1, omega primitive Nth root; all operations in F_p.
The comparison to Phase 23 streaming probes is a structured/generic cost
improvement, NOT an exact sub-N log N algorithm for arbitrary input.
"""
from dataclasses import dataclass
from annihilator_engine import Work, batch_inverse_nonzero, sparse_direct_fourier
from rational_forcing import nextpow2
from short_probe_fusion import discover_short_probe
from reciprocal_union import factor_sparse_hypercube

@dataclass
class LazyStats:
    expanded_nodes:int=0
    butterflies:int=0
    multiplications:int=0
    additions:int=0
    reads:int=0
    writes:int=0
    requested_outputs:int=0
    max_arrays:int=1
    def arithmetic(self):
        return self.multiplications+self.additions

class LazyDIF:
    """Exact DFT in place with an input-independent precomputed roots table.

    A node is identified by segment start and length. Its DIF butterflies
    produce both child input arrays, even if only one child output is initially
    requested. Thus on fallback no node is expanded again. N powers, data and
    expanded-node flags use O(N) working memory.
    """
    def __init__(self, data, powers, p):
        n=len(data)
        if n<2 or n&(n-1):raise ValueError('length must be power of two >=2')
        if len(powers)!=n:raise ValueError('root table size mismatch')
        self.n,self.p=n,p
        self.powers=powers
        self.a=[v%p for v in data]
        self.expanded=set()
        self.stats=LazyStats()
        self._got=set()
    def _expand(self, start, size):
        if size==1 or (start,size) in self.expanded:
            return
        h=size//2; step=self.n//size; p=self.p;a=self.a;powrs=self.powers
        for j in range(h):
            u=a[start+j];v=a[start+h+j]
            a[start+j]=(u+v)%p
            a[start+h+j]=((u-v)*powrs[j*step])%p
        self.expanded.add((start,size))
        s=self.stats
        s.expanded_nodes+=1
        s.butterflies+=h
        s.multiplications+=h
        s.additions+=2*h
        s.reads+=2*h
        s.writes+=2*h
    def get(self, k):
        if not (0<=k<self.n):raise IndexError('frequency index outside transform')
        self.stats.requested_outputs+=1
        start=0;size=self.n
        while size>1:
            self._expand(start,size)
            h=size//2
            bit=k&1
            start+=bit*h
            size=h;k>>=1
        return self.a[start]
    def prefix(self,m):
        if not (0<=m<=self.n):raise ValueError('invalid prefix length')
        return [self.get(k) for k in range(m)]
    def full(self):
        # This can be done in any order; output depends on input only, not order.
        return [self.get(k) for k in range(self.n)]
    def snapshot(self):
        s=self.stats
        return dict(butterflies=s.butterflies,multiplications=s.multiplications,
                    additions=s.additions,expanded_nodes=s.expanded_nodes,
                    reads=s.reads,writes=s.writes,requested_outputs=s.requested_outputs)
    def storage_bound(self):
        # Count data slots, expanded-node flags and the shared power table.
        return self.n, len(self.expanded), len(self.powers)


def preview_butterflies(n,m):
    """Count DIF butterflies to compute outputs k=0,...,m-1."""
    if n<2 or n&(n-1) or not 0<=m<=n:raise ValueError('bad sizes')
    total=0;level=0;length=n
    while length>1:
        total+=min(1<<level,m)*(length//2)
        level+=1;length//=2
    return total


def transform_lazy_short_probe(engine,x,s=4,return_preview=False):
    """Phase23 certificate + lazily cached Fourier probes/fallback for N=2^t.

    Only difference versus transform_short_probe: all initial Fourier probes
    and the fallback are subgraphs of one same exact radix-2 DFT DAG.
    Full correctness rests on the unmodified full cyclic certificate and the
    exact fallback; fixed small probe prefixes cannot determine arbitrary DFT.
    """
    n,p=engine.n,engine.p
    if n<2 or n&(n-1):raise ValueError('power-of-two N required')
    if len(x)!=n:raise ValueError('input size mismatch')
    co=Work()
    r=engine.P.apply(x)
    co.multiplies+=2*n;co.additions+=n;co.reads+=2*n;co.writes+=n
    session=LazyDIF(r,engine.powers,p)
    m=2*s+2
    probes=session.prefix(m)
    preview=session.snapshot()
    co.multiplies+=session.stats.multiplications
    co.additions+=session.stats.additions
    co.reads+=session.stats.reads;co.writes+=session.stats.writes
    choice,meta=discover_short_probe(r,engine,co,s=s,prefix_R=probes)
    factors=None
    if choice is None:
        forcing=session.full()
        co.multiplies+=session.stats.multiplications-preview['multiplications']
        co.additions+=session.stats.additions-preview['additions']
        co.reads+=session.stats.reads-preview['reads'];co.writes+=session.stats.writes-preview['writes']
        selection='lazy-dif-fallback'
    else:
        A,delay,alpha,Ahat=choice
        if len(A) in (2,4,8,16):
            factors=factor_sparse_hypercube(A,delay,alpha,n,p,
                len(A).bit_length()-1,co)
        wk=1;w=engine.powers[delay]
        numerator=[]
        for k in range(n):
            numerator.append((1-alpha*wk)%p)
            wk=wk*w%p
            co.multiplies+=2;co.additions+=1
        inverse=batch_inverse_nonzero(Ahat,p,co)
        forcing=[numerator[k]*inverse[k]%p for k in range(n)]
        co.multiplies+=n;co.writes+=n
        selection='lazy-dif-certified'
    y=engine.L.solve(forcing)
    co.multiplies+=3*n+1;co.additions+=2*n;co.reads+=3*n;co.writes+=2*n
    full_b=(n//2)*(n.bit_length()-1)
    return y,{'selected':selection,'meta':meta,'work':co,'preview':preview,
              'final_fft':session.snapshot(),
              'full_radix_butterflies':full_b,
              'storage':session.storage_bound(),'graph_factors':factors}


def direct_full_fft(a,powers,p):
    sess=LazyDIF(a,powers,p)
    return sess.full(),sess.snapshot()


def transform_conjugate_lazy(engine,x,s=4):
    """Delay preconditioning and use native exact FFT fallback with zero repeats.

    F(Px)=L(Fx), so needed probes of F(Px) come from k and k-1 of the
    original DFT. This allows the partial radix-two graph to be built on x.
    On the common early-rejection branch, P and L are never applied at all.
    Fully certified structured candidates still use Green recovery. In both
    branches, previously computed input FFT butterflies are never repeated.
    """
    n,p=engine.n,engine.p
    if n<2 or n&(n-1):raise ValueError('power-of-two N required')
    if len(x)!=n:raise ValueError('input size mismatch')
    co=Work()
    session=LazyDIF(x,engine.powers,p)
    m=2*s+2
    if not 1<=m<n:raise ValueError('need nontrivial prefix shorter than N')
    Y=session.prefix(m)
    ylast=session.get(n-1)
    preview=session.snapshot()
    co.multiplies+=preview['multiplications'];co.additions+=preview['additions']
    co.reads+=preview['reads'];co.writes+=preview['writes']
    # LF=FP. L has diagonal and shift: (L Y)[k]=diag[k]Y[k]+shift Y[k-1].
    R=[((engine.L.diag[k]*Y[k]+engine.L.shift*(Y[k-1] if k else ylast))%p)
       for k in range(m)]
    co.multiplies+=2*m;co.additions+=m;co.reads+=3*m;co.writes+=m
    residual=[None]
    def get_residual():
        if residual[0] is None:
            residual[0]=engine.P.apply(x)
            co.multiplies+=2*n;co.additions+=n;co.reads+=2*n;co.writes+=n
        return residual[0]
    choice,meta=discover_short_probe(None,engine,co,s=s,prefix_R=R,
                                     residual_loader=get_residual)
    factors=None
    if choice is None:
        y=session.full()
        co.multiplies+=session.stats.multiplications-preview['multiplications']
        co.additions+=session.stats.additions-preview['additions']
        co.reads+=session.stats.reads-preview['reads'];co.writes+=session.stats.writes-preview['writes']
        selection='conjugate-lazy-fallback'
    else:
        A,delay,alpha,Ahat=choice
        if len(A) in (2,4,8,16):
            factors=factor_sparse_hypercube(A,delay,alpha,n,p,
                len(A).bit_length()-1,co)
        w=engine.powers[delay]
        wk=1
        numerator=[]
        for k in range(n):
            numerator.append((1-alpha*wk)%p)
            wk=wk*w%p
            co.multiplies+=2;co.additions+=1
        inverse=batch_inverse_nonzero(Ahat,p,co)
        forcing=[numerator[k]*inverse[k]%p for k in range(n)]
        co.multiplies+=n;co.writes+=n
        y=engine.L.solve(forcing)
        co.multiplies+=3*n+1;co.additions+=2*n;co.reads+=3*n;co.writes+=2*n
        selection='conjugate-lazy-certified'
    return y,{'selected':selection,'meta':meta,'work':co,
              'preview':preview,'final_fft':session.snapshot(),
              'residual_computed':residual[0] is not None,
              'storage':session.storage_bound(),
              'graph_factors':factors}
