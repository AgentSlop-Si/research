"""Hero #17 Phase 10: exact Fourier projector union over finite prime fields.

Computes P_K x = F^{-1} diag(1_K) F x for arbitrary fresh x, when
K is a union of residue classes modulo d, modified at q exceptions.

This is a different task from computing the complete DFT: no universal
O(N) FFT is claimed. Every field addition/multiplication used by the
executor, inverse preparation and root validation is charged.

The primitive Nth root w in F_p and p prime are supplied. Finite-field
prime selection/certification is outside this model, just as it is for
most explicitly parameterized NTT executors. For p polynomial in N,
indexing and field arithmetic occupy O(log N) bits per field element.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from math import isqrt


@dataclass
class Ledger:
    plan_adds:int=0
    plan_muls:int=0
    online_adds:int=0
    online_muls:int=0
    plan_int_ops:int=0
    online_int_ops:int=0
    plan_field_inverse_calls:int=0
    input_reads:int=0
    output_writes:int=0
    plan_table_writes:int=0
    root_validations:int=0

    def add(self,a,b,p,plan=False):
        if plan:self.plan_adds+=1
        else:self.online_adds+=1
        return (a+b)%p
    def sub(self,a,b,p,plan=False):
        if plan:self.plan_adds+=1
        else:self.online_adds+=1
        return (a-b)%p
    def mul(self,a,b,p,plan=False):
        if plan:self.plan_muls+=1
        else:self.online_muls+=1
        return (a*b)%p
    def ipow(self,a,e,p,plan=True):
        """Binary exponentiation; every field multiplication charged."""
        if e<0:raise ValueError('negative exponent')
        b=a%p;r=1
        while e:
            if plan:self.plan_int_ops+=1
            else:self.online_int_ops+=1
            if e&1:r=self.mul(r,b,p,plan)
            e>>=1
            if e:b=self.mul(b,b,p,plan)
        return r
    def inv(self,a,p):
        """Fermat inverse for supplied prime field: fully charged O(log p)."""
        if a%p==0:raise ZeroDivisionError('not invertible')
        self.plan_field_inverse_calls+=1
        return self.ipow(a,p-2,p,True)
    def total_field(self):
        return self.plan_adds+self.plan_muls+self.online_adds+self.online_muls
    def snapshot(self):return asdict(self)


def distinct_prime_factors(n,ledger=None):
    out=[];d=2
    while d*d<=n:
        if ledger:ledger.plan_int_ops+=1
        if n%d==0:
            out.append(d)
            while n%d==0:
                n//=d
                if ledger:ledger.plan_int_ops+=1
        d+=1
    if n>1:out.append(n)
    return out


def primitive_check(n,p,w,L):
    """Charge validation of supplied w, NOT a primality proof for supplied p."""
    if L.ipow(w,n,p)!=1:raise ValueError('root does not have order dividing N')
    L.root_validations+=1
    for q in distinct_prime_factors(n,L):
        if L.ipow(w,n//q,p)==1:raise ValueError('root is not primitive')
        L.root_validations+=1


class SpectralUnion:
    """Exact cyclic spectral projection with a sparse exception graph.

    K = {k: k mod d in residues} union add, excluding remove.
    Add frequencies must not be in the base and remove frequencies
    must be in the base; duplicates and conflicts are forbidden.

    Complexity fully charged (word-RAM/field model):
      preparation O(N + |residues|*d + q + log p + sqrt(N))
      application O(N*(d+q)); storage O(N+d+q).
    With d+q=O(1), both preparation and application take O(N).
    """
    def __init__(self,n,p,w,d,residues,add=(),remove=(),validate_root=True):
        if n<2 or d<1 or n%d!=0:raise ValueError('d must divide N')
        if p<=2 or (p-1)%n!=0:raise ValueError('supplied prime field must have Nth roots')
        L=Ledger()
        if validate_root:primitive_check(n,p,w,L)
        S=frozenset(residues)
        if any(a<0 or a>=d for a in S):raise ValueError('invalid residue')
        add=tuple(add);remove=tuple(remove)
        if len(set(add))!=len(add) or len(set(remove))!=len(remove):
            raise ValueError('duplicate exceptional frequency')
        if any(k<0 or k>=n or k%d in S for k in add):
            raise ValueError('added frequency already belongs to base or outside N')
        if any(k<0 or k>=n or k%d not in S for k in remove):
            raise ValueError('removed frequency absent from base or outside N')
        self.n=n;self.p=p;self.w=w;self.d=d;self.residues=S
        self.added=add;self.removed=remove
        self._added_set=frozenset(add);self._removed_set=frozenset(remove)
        self.m=n//d
        self.events=tuple((k,1) for k in add)+tuple((k,-1) for k in remove)
        self.L=L
        W=[1]*n
        for j in range(1,n):
            W[j]=L.mul(W[j-1],w,p,plan=True)
            L.plan_table_writes+=1
        self.W=W
        inv_d=L.inv(d%p,p)
        self.inv_n=L.inv(n%p,p)
        weights=[]
        for ell in range(d):
            v=0
            for a in S:
                L.plan_int_ops+=1
                v=L.add(v,W[(-a*ell*self.m)%n],p,plan=True)
            weights.append(L.mul(v,inv_d,p,plan=True))
            L.plan_table_writes+=1
        self.weights=tuple(weights)
        self.nonzero_weights=tuple((ell,v) for ell,v in enumerate(weights) if v)
        self.plan_ledger=L.snapshot()
        self.L=Ledger()

    def contains(self,k):
        return (k in self._added_set) or ((k %self.d in self.residues) and k not in self._removed_set)

    def apply(self,x):
        n=self.n;p=self.p;L=self.L
        if len(x)!=n:raise ValueError('incorrect input length')
        # Base spectral projector as a cyclic (at most d-tap) comb.
        out=[0]*n
        for ell,weight in self.nonzero_weights:
            jump=ell*self.m
            for j in range(n):
                L.online_int_ops+=1
                pos=j+jump
                if pos>=n:pos-=n
                v=x[pos]%p;L.input_reads+=1
                out[j]=L.add(out[j],L.mul(weight,v,p),p)
        # A frequency projector is rank one, with all phases generated
        # via charged field multiplications and no FFTs or dense tables.
        for k,sign in self.events:
            step_neg=self.W[(-k)%n];step_pos=self.W[k]
            acc=0;power=1
            for j in range(n):
                L.input_reads+=1
                acc=L.add(acc,L.mul(x[j]%p,power,p),p)
                power=L.mul(power,step_neg,p)
            alpha=L.mul(acc,self.inv_n,p)
            if sign==-1:alpha=L.sub(0,alpha,p)
            power=1
            for j in range(n):
                out[j]=L.add(out[j],L.mul(alpha,power,p),p)
                power=L.mul(power,step_pos,p)
        L.output_writes+=n
        return out

    def cost(self):
        return {'plan':self.plan_ledger,'online':self.L.snapshot(),
                'total_field_operations':sum(self.plan_ledger[k] for k in
                    ('plan_adds','plan_muls','online_adds','online_muls'))+self.L.total_field(),
                'q':len(self.events),'d':self.d,'n':self.n}


def classical_fft(x,p,w,validate_root=True):
    """Radix-2 exact DFT, independently constructed for same-task control."""
    n=len(x)
    if n<2 or n&(n-1):raise ValueError('N must be a power of 2')
    L=Ledger()
    if validate_root:primitive_check(n,p,w,L)
    W=[1]*n
    for j in range(1,n):
        W[j]=L.mul(W[j-1],w,p,plan=True)
        L.plan_table_writes+=1
    result=[0]*n
    def rec(coeff,indices):
        length=len(indices)
        if length==1:
            result[indices[0]]=coeff[0];L.output_writes+=1
            return
        half=length//2
        factor=W[(-indices[0]*half)%n]
        lo=[];hi=[]
        for a,b in zip(coeff[:half],coeff[half:]):
            tw=L.mul(factor,b,p)
            lo.append(L.add(a,tw,p))
            hi.append(L.sub(a,tw,p))
        rec(lo,indices[::2]);rec(hi,indices[1::2])
    L.input_reads+=n
    rec([v%p for v in x],list(range(n)))
    return result,L


def classical_fft_project(x,plan:SpectralUnion):
    """Fully charged same-output control: FFT, frequency mask, inverse FFT."""
    n=plan.n;p=plan.p;w=plan.w
    forward,L1=classical_fft(x,p,w)
    w_inv=L1.ipow(w,n-1,p,plan=False)
    for k in range(n):
        L1.online_int_ops+=1
        if not plan.contains(k):forward[k]=0
    back,L2=classical_fft(forward,p,w_inv)
    inv=L2.inv(n,p)
    y=[L2.mul(inv,v,p) for v in back]
    L2.output_writes+=n
    return y,{'forward':L1.snapshot(),'inverse':L2.snapshot(),
               'total_field_operations':L1.total_field()+L2.total_field()}


class BatchSpectralUnion:
    """Shared spectral-projector graph for several full-length output vectors.

    All masks use the same N, finite field and residue modulus d. Each
    mask description is (residues, add, remove), same conventions as
    SpectralUnion. Distinct base residue sets, exceptional frequencies
    and signed exception patterns are computed at most once per batch.

    Let s=#distinct residue sets, q=#distinct exceptional frequencies,
    and H=sum(|exception pattern|) over distinct signed patterns.
    With B output masks:
      charged work O(N(1 + s*d + q + H + B) + B*d^2),
      memory O(N(s + q + B + #distinct_patterns) + B*d).
    These are fully explicit N-coordinate projected outputs, not DFT bins.
    """
    def __init__(self,n,p,w,d,masks,validate_root=True):
        if n<2 or d<1 or n%d:raise ValueError('d must divide N')
        if p<=2 or (p-1)%n:raise ValueError('field incompatible with N')
        L=Ledger()
        if validate_root:primitive_check(n,p,w,L)
        self.n=n;self.p=p;self.w=w;self.d=d;self.m=n//d
        self.mask_keys=[];self.base_keys=set();self.event_keys=set()
        self.exception_freqs=set()
        for entries in masks:
            S,added,removed=entries
            S=frozenset(S);added=tuple(added);removed=tuple(removed)
            if any(a<0 or a>=d for a in S):raise ValueError('invalid residue')
            if len(set(added))!=len(added) or len(set(removed))!=len(removed):
                raise ValueError('repeated exception')
            if any(k<0 or k>=n or k%d in S for k in added):
                raise ValueError('invalid add exception')
            if any(k<0 or k>=n or k%d not in S for k in removed):
                raise ValueError('invalid remove exception')
            events=tuple(sorted([(k,1) for k in added]+[(k,-1) for k in removed]))
            self.mask_keys.append((S,events))
            self.base_keys.add(S);self.event_keys.add(events)
            self.exception_freqs.update(k for k,_ in events)
            L.plan_int_ops+=len(S)+len(events)
        W=[1]*n
        for j in range(1,n):
            W[j]=L.mul(W[j-1],w,p,plan=True)
            L.plan_table_writes+=1
        self.W=W
        invd=L.inv(d%p,p);self.invn=L.inv(n%p,p)
        self.weights={}
        for S in self.base_keys:
            arr=[]
            for ell in range(d):
                acc=0
                for a in S:
                    acc=L.add(acc,W[(-a*ell*self.m)%n],p,True)
                    L.plan_int_ops+=1
                arr.append(L.mul(acc,invd,p,True))
                L.plan_table_writes+=1
            self.weights[S]=tuple((ell,v) for ell,v in enumerate(arr) if v)
        self.plan_ledger=L.snapshot()
        self.L=Ledger()

    def apply(self,x):
        if len(x)!=self.n:raise ValueError('incorrect input length')
        n=self.n;p=self.p;L=self.L
        base_cache={}
        for S,taps in self.weights.items():
            z=[0]*n
            for ell,wgt in taps:
                shift=ell*self.m
                for j in range(n):
                    loc=j+shift
                    if loc>=n:loc-=n
                    L.online_int_ops+=1
                    z[j]=L.add(z[j],L.mul(wgt,x[loc]%p,p),p)
                    L.input_reads+=1
            base_cache[S]=z
            L.output_writes+=n  # cached intermediate vector
        atom_cache={}
        for k in self.exception_freqs:
            ratio_neg=self.W[(-k)%n];ratio_pos=self.W[k]
            coef=0;z=1
            for j in range(n):
                coef=L.add(coef,L.mul(x[j]%p,z,p),p)
                z=L.mul(z,ratio_neg,p)
                L.input_reads+=1
            coef=L.mul(coef,self.invn,p)
            z=1;atom=[]
            for j in range(n):
                atom.append(L.mul(coef,z,p))
                z=L.mul(z,ratio_pos,p)
            atom_cache[k]=atom
            L.output_writes+=n
        correction_cache={}
        for event_key in self.event_keys:
            correction=[0]*n
            for k,sgn in event_key:
                atom=atom_cache[k]
                for j in range(n):
                    if sgn==1:correction[j]=L.add(correction[j],atom[j],p)
                    else:correction[j]=L.sub(correction[j],atom[j],p)
            correction_cache[event_key]=correction
            L.output_writes+=n
        outputs=[]
        for S,event_key in self.mask_keys:
            base=base_cache[S];corr=correction_cache[event_key]
            if not event_key:
                out=base.copy()
            elif not S:
                out=corr.copy()
            else:
                out=[L.add(a,b,p) for a,b in zip(base,corr)]
            outputs.append(out)
            L.output_writes+=n
        return outputs

    def cost(self):
        return {'plan':self.plan_ledger,'online':self.L.snapshot(),
            'total_field_operations':sum(self.plan_ledger[k] for k in
                ('plan_adds','plan_muls','online_adds','online_muls'))+self.L.total_field(),
            'n':self.n,'d':self.d,'masks':len(self.mask_keys),
            'distinct_bases':len(self.base_keys),
            'distinct_exception_frequencies':len(self.exception_freqs),
            'distinct_exception_patterns':len(self.event_keys)}
