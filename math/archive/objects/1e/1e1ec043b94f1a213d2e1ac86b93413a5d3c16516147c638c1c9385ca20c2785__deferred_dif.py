"""Phase24: exact deferred, fully completable radix-two DIF butterfly graph.

For a fixed queried set of output frequencies, only execute the branches
needed to produce them. Preserve the originals of an unused sibling in an
O(N)-word backup bank. If all outputs are later needed, generate only the
missing branch operations: the total (field additions + multiplications)
across preview and fallback is IDENTICAL to a full radix-two FFT.

All requested frequency indices are evaluated as part of one per-input graph;
no input-independent result cache or prior-call reuse is assumed.
"""
from dataclasses import dataclass

@dataclass
class DeferredStats:
    butterflies_completed:int=0
    additions:int=0
    multiplications:int=0
    reads:int=0
    writes:int=0
    backup_writes:int=0
    backup_reads:int=0
    backup_peak:int=0
    operations_marked:int=0
    def arithmetic(self):return self.additions+self.multiplications

class DeferredDIF:
    """In-place selective DIF with deferred sibling computation.

    Leaves are in bit-reversed order, output[k] = data[bitreverse(k)].
    Preview is batch-defined; completing the full graph reuses every
    previously executed addition and multiplication, with no recomputation.
    """
    def __init__(self, values, powers, p):
        n=len(values)
        if n<2 or n&(n-1):raise ValueError('power-of-two N required')
        if len(powers)!=n:raise ValueError('root table size mismatch')
        self.n,self.p=n,p
        self.a=[v%p for v in values]
        self.powers=powers
        self.states={}
        self.backups={}
        self._backup_words=0
        self.done_preview=False
        self.stats=DeferredStats()
    def _mark(self, key, mode):
        self.states[key]=mode
        self.stats.operations_marked+=1
    def _both(self,start,size):
        h=size//2;a=self.a;p=self.p;powrs=self.powers;step=self.n//size
        for j in range(h):
            u=a[start+j];v=a[start+h+j]
            a[start+j]=(u+v)%p
            a[start+h+j]=((u-v)*powrs[j*step])%p
        st=self.stats;st.additions+=2*h;st.multiplications+=h
        st.reads+=2*h;st.writes+=2*h
        st.butterflies_completed+=h
    def _one(self,start,size,odd):
        h=size//2;a=self.a;p=self.p;powrs=self.powers;step=self.n//size
        key=(start,size)
        if odd:
            # Keep u in left half; preserve original v in backup; write B.
            old=[a[start+h+j] for j in range(h)]
            for j,v in enumerate(old):
                u=a[start+j]
                a[start+h+j]=((u-v)*powrs[j*step])%p
            self.stats.additions+=h;self.stats.multiplications+=h
            self.stats.reads+=2*h;self.stats.writes+=h
            self._mark(key,'odd')
        else:
            # Keep v in right half; preserve original u in backup; write A.
            old=[a[start+j] for j in range(h)]
            for j,u in enumerate(old):
                v=a[start+h+j]
                a[start+j]=(u+v)%p
            self.stats.additions+=h
            self.stats.reads+=2*h;self.stats.writes+=h
            self._mark(key,'even')
        self.backups[key]=old
        self._backup_words+=h
        self.stats.backup_writes+=h
        self.stats.backup_peak=max(self._backup_words,self.stats.backup_peak)
    def _prepare(self,start,size,targets):
        if not targets:return
        if size==1:return
        h=size//2
        even={k//2 for k in targets if not(k&1)}
        odd={k//2 for k in targets if k&1}
        if even and odd:
            self._both(start,size)
            self._mark((start,size),'full')
            self._prepare(start,h,even)
            self._prepare(start+h,h,odd)
        elif even:
            self._one(start,size,False)
            self._prepare(start,h,even)
        else:
            self._one(start,size,True)
            self._prepare(start+h,h,odd)
    def _leaf(self,k):
        pos=0;length=self.n
        while length>1:
            h=length//2
            if k&1:pos+=h
            k>>=1;length=h
        return self.a[pos]
    def preview(self,frequencies):
        if self.done_preview:raise ValueError('preview can only be called once')
        keys=sorted(set(frequencies))
        if not keys:raise ValueError('preview must request at least one frequency')
        if any(k<0 or k>=self.n for k in keys):raise ValueError('output index invalid')
        self._prepare(0,self.n,set(keys))
        self.done_preview=True
        return {k:self._leaf(k) for k in keys}
    def _finish(self,start,size):
        if size==1:return
        h=size//2;key=(start,size)
        mode=self.states.get(key)
        if mode is None:
            self._both(start,size)
            self._mark(key,'full')
        elif mode in ('even','odd'):
            old=self.backups.pop(key)
            self._backup_words-=h
            self.stats.backup_reads+=h
            if mode=='even':
                # u preserved; v still in right child. Finish B only.
                for j,u in enumerate(old):
                    v=self.a[start+h+j]
                    self.a[start+h+j]=((u-v)*self.powers[j*(self.n//size)])%self.p
                self.stats.multiplications+=h;self.stats.additions+=h
                self.stats.reads+=2*h;self.stats.writes+=h
            else:
                # u still in left child, v backed up. Finish A only.
                for j,v in enumerate(old):
                    u=self.a[start+j]
                    self.a[start+j]=(u+v)%self.p
                self.stats.additions+=h
                self.stats.reads+=2*h;self.stats.writes+=h
            self._mark(key,'full')
            self.stats.butterflies_completed+=h
        self._finish(start,h)
        self._finish(start+h,h)
    def full(self):
        self._finish(0,self.n)
        return [self._leaf(k) for k in range(self.n)]
    def snapshot(self):
        s=self.stats
        return {'multiplies':s.multiplications,'additions':s.additions,
            'arithmetic':s.arithmetic(),'reads':s.reads,'writes':s.writes,
            'backup_reads':s.backup_reads,'backup_writes':s.backup_writes,
            'backup_peak':s.backup_peak,'backup_current':self._backup_words,
            'expanded_nodes':len(self.states)}
    def storage_bound(self):
        return dict(data_words=self.n,root_words=self.n,
            current_backup_words=self._backup_words,
            peak_backup_words=self.stats.backup_peak,
            state_words=len(self.states))


def transform_deferred_conjugate(engine,x,s=4):
    """Phase23 certified detector with x-side Green probes and deferred DIF."""
    from annihilator_engine import Work,batch_inverse_nonzero
    from short_probe_fusion import discover_short_probe
    from reciprocal_union import factor_sparse_hypercube
    n,p=engine.n,engine.p
    m=2*s+2
    if n<2 or n&(n-1) or m>=n:raise ValueError('dyadic N>2s+2 required')
    if len(x)!=n:raise ValueError('wrong input size')
    co=Work()
    session=DeferredDIF(x,engine.powers,p)
    wanted=list(range(m))+[n-1]
    previews=session.preview(wanted)
    preview=session.snapshot()
    co.multiplies+=preview['multiplies'];co.additions+=preview['additions']
    co.reads+=preview['reads']+preview['backup_reads'];co.writes+=preview['writes']+preview['backup_writes']
    # FP=LF, so take R_k from x-side Y_k and Y_{k-1}.
    R=[(engine.L.diag[k]*previews[k]+engine.L.shift*previews[k-1 if k else n-1])%p
       for k in range(m)]
    co.multiplies+=2*m;co.additions+=m;co.reads+=3*m;co.writes+=m
    residual=[None]
    def materialize_residual():
        if residual[0] is None:
            residual[0]=engine.P.apply(x)
            co.multiplies+=2*n;co.additions+=n;co.reads+=2*n;co.writes+=n
        return residual[0]
    choice,meta=discover_short_probe(None,engine,co,s=s,prefix_R=R,
                                    residual_loader=materialize_residual)
    factors=None
    if choice is None:
        y=session.full()
        end=session.snapshot()
        co.multiplies+=end['multiplies']-preview['multiplies']
        co.additions+=end['additions']-preview['additions']
        co.reads+=end['reads']+end['backup_reads']-preview['reads']-preview['backup_reads']
        co.writes+=end['writes']+end['backup_writes']-preview['writes']-preview['backup_writes']
        selection='deferred-conjugate-fallback'
    else:
        A,delay,alpha,Ahat=choice
        if len(A) in (2,4,8,16):
            factors=factor_sparse_hypercube(A,delay,alpha,n,p,
                len(A).bit_length()-1,co)
        wk=1;w=engine.powers[delay];numerator=[]
        for k in range(n):
            numerator.append((1-alpha*wk)%p)
            wk=wk*w%p
            co.multiplies+=2;co.additions+=1
        inverse=batch_inverse_nonzero(Ahat,p,co)
        forcing=[numerator[k]*inverse[k]%p for k in range(n)]
        co.multiplies+=n;co.writes+=n
        y=engine.L.solve(forcing)
        co.multiplies+=3*n+1;co.additions+=2*n;co.reads+=3*n;co.writes+=2*n
        end=session.snapshot()
        selection='deferred-conjugate-certified'
    return y,{'selected':selection,'work':co,'meta':meta,'preview':preview,
              'final_fft':end,'residual_computed':residual[0] is not None,
              'storage':session.storage_bound(),'graph_factors':factors}
