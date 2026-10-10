"""Hero #1 Phase25: exact no-recomputation Good-Thomas FFT for N=3*2**t.

Standard prime-factor (Good-Thomas) factorization with a project-specific
cached three-output Winograd codelet and optimized deferred radix-2 children.
All field additions/subtractions and non-identity field multiplications counted.
Index arithmetic, data copies, integer modular reductions and root setup are
tracked separately or excluded from field arithmetic; see THEOREM.md.
"""
from dataclasses import dataclass
from math import log2
from pathlib import Path
import sys

# Import prior checkpoint's separately reviewed radix-two scheduler unchanged,
# then override its butterfly primitive solely to skip multiplication by 1.
sys.path.insert(0,str(Path(__file__).resolve().parent/'phase24_source'))
from deferred_dif import DeferredDIF

@dataclass
class Count:
    additions:int=0
    multiplications:int=0
    data_reads:int=0
    data_writes:int=0
    permutations:int=0
    def arithmetic(self): return self.additions+self.multiplications

class TightDIF(DeferredDIF):
    """Same deferred graph and memory as Phase24; skips the j=0 identity multiply."""
    def _both(self,start,size):
        h=size//2;a=self.a;p=self.p;roots=self.powers;step=self.n//size
        for j in range(h):
            u=a[start+j];v=a[start+h+j]
            a[start+j]=(u+v)%p
            sub=(u-v)%p
            a[start+h+j]=sub if j==0 else sub*roots[j*step]%p
        st=self.stats;st.additions+=2*h;st.multiplications+=h-1
        st.reads+=2*h;st.writes+=2*h;st.butterflies_completed+=h
    def _one(self,start,size,odd):
        h=size//2;a=self.a;p=self.p;roots=self.powers;step=self.n//size
        key=(start,size)
        if odd:
            old=[a[start+h+j] for j in range(h)]
            for j,v in enumerate(old):
                u=a[start+j];sub=(u-v)%p
                a[start+h+j]=sub if j==0 else sub*roots[j*step]%p
            self.stats.additions+=h;self.stats.multiplications+=h-1
            self.stats.reads+=2*h;self.stats.writes+=h
            self._mark(key,'odd')
        else:
            old=[a[start+j] for j in range(h)]
            for j,u in enumerate(old):a[start+j]=(u+a[start+h+j])%p
            self.stats.additions+=h
            self.stats.reads+=2*h;self.stats.writes+=h
            self._mark(key,'even')
        self.backups[key]=old
        self._backup_words+=h;self.stats.backup_writes+=h
        self.stats.backup_peak=max(self._backup_words,self.stats.backup_peak)
    def _finish(self,start,size):
        if size==1:return
        h=size//2;key=(start,size)
        mode=self.states.get(key)
        if mode is None:
            self._both(start,size);self._mark(key,'full')
        elif mode in ('even','odd'):
            old=self.backups.pop(key)
            self._backup_words-=h;self.stats.backup_reads+=h
            if mode=='even':
                for j,u in enumerate(old):
                    sub=(u-self.a[start+h+j])%self.p
                    self.a[start+h+j]=sub if j==0 else sub*self.powers[j*(self.n//size)]%self.p
                self.stats.multiplications+=h-1;self.stats.additions+=h
                self.stats.reads+=2*h;self.stats.writes+=h
            else:
                for j,v in enumerate(old):
                    u=self.a[start+j];self.a[start+j]=(u+v)%self.p
                self.stats.additions+=h
                self.stats.reads+=2*h;self.stats.writes+=h
            self._mark(key,'full');self.stats.butterflies_completed+=h
        self._finish(start,h);self._finish(start+h,h)

def winograd_constants(eta,p):
    """Precompute the two fixed length-3 coefficients once per FFT call.

    When accounting includes setup, this is two field multiplications and one
    subtraction (plus ring-constant /2 from p odd), shared across all triples.
    """
    inv2=(p+1)//2
    eta2=eta*eta%p
    return ((-inv2)%p, (eta-eta2)*inv2%p)

class TripleCodelet:
    """Partial 3-point Fourier codelet with exact 6-add/2-mul full completion."""
    def __init__(self,a,b,c,p,eta,coefficients=None):
        self.a,self.b,self.c=a,b,c
        self.p=p;self.eta=eta
        if coefficients is None:
            coefficients=winograd_constants(eta,p)
        self.v,self.w=coefficients
        self.t=self.d=self.mid=self.z=None
        self.outputs={};self.cnt=Count()
    def get(self,k):
        if not 0<=k<3:raise IndexError(k)
        if k in self.outputs:return self.outputs[k]
        p=self.p;c=self.cnt
        if self.t is None:
            self.t=(self.b+self.c)%p;c.additions+=1
        if k==0:
            o=(self.a+self.t)%p;c.additions+=1
        else:
            if self.d is None:
                self.d=(self.b-self.c)%p;c.additions+=1
            if self.mid is None:
                self.mid=(self.a+self.v*self.t)%p
                c.additions+=1;c.multiplications+=1
            if self.z is None:
                self.z=self.w*self.d%p;c.multiplications+=1
            o=(self.mid+self.z)%p if k==1 else (self.mid-self.z)%p
            c.additions+=1
        self.outputs[k]=o;return o
    def full(self): return [self.get(k) for k in range(3)]


def primitive_roots(n,p,g):
    if (p-1)%n:raise ValueError('no primitive length-N root from supplied generator')
    w=pow(g,(p-1)//n,p)
    if pow(w,n,p)!=1 or any(pow(w,n//q,p)==1 for q in prime_factors(n)):
        raise ValueError('supplied generator fails primitive-order check')
    return w

def prime_factors(n):
    f=[];d=2
    while d*d<=n:
        if n%d==0:
            f.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:f.append(n)
    return f

def base_radix2_full(x,p,omega):
    """Unnormalized radix-2 DIF, skip identity twiddles, return (values, count)."""
    n=len(x)
    if n<2 or (n&(n-1)):raise ValueError('requires dyadic length >=2')
    a=[v%p for v in x];roots=[pow(omega,k,p) for k in range(n)]
    cnt=Count()
    step=1;h=n//2
    while h:
        for start in range(0,n,2*h):
            for j in range(h):
                u=a[start+j];v=a[start+h+j]
                a[start+j]=(u+v)%p
                sub=(u-v)%p
                a[start+h+j]=sub if j==0 else sub*roots[j*step]%p
            cnt.additions+=2*h;cnt.multiplications+=h-1
            cnt.data_reads+=2*h;cnt.data_writes+=2*h
        step*=2;h//=2
    log=n.bit_length()-1
    out=[a[int(f'{k:0{log}b}'[::-1],2)] for k in range(n)]
    cnt.permutations+=n
    return out,cnt

class DeferredGT3:
    """N=3G, G dyadic >=2; predeclared preview batch and no-repeat completion."""
    def __init__(self,x,p=2013265921,g=31):
        n=len(x)
        if n%3:raise ValueError('N must be 3*2**t')
        G=n//3
        if G<2 or G&(G-1):raise ValueError('N must be 3*2**t with t>=1')
        w=primitive_roots(n,p,g);wG=pow(w,3,p);eta=pow(w,G,p)
        self.n=n;self.G=G;self.p=p;self.g=g;self.omega=w;self.eta=eta
        self.invg=pow(G,-1,3);self.inv3=pow(3,-1,G)
        self.eG=3*self.inv3;self.e3=G*self.invg
        # Prime-field root setup is explicit: G-1 field multiplications;
        # if precomputed roots are supplied/reused, this is a common cost.
        self.roots=[1]*G
        for j in range(1,G):self.roots[j]=self.roots[j-1]*wG%p
        self.root_setup_ops=G-1
        # Three temporary input rows are recycled after the row-DIF copies.
        row_inputs=[[x[(jG*self.eG+j3*self.e3)%n]%p for jG in range(G)] for j3 in range(3)]
        self.rows=[TightDIF(values,self.roots,p) for values in row_inputs]
        del row_inputs
        self.coefficients=winograd_constants(eta,p)
        self.cnt=Count(permutations=n)
        self.triples={}
        self.preview_done=False
        self.cache={}
        self.preview_j=set()
        self._row_stats_preview=None
    def k_to_grid(self,k):
        if not 0<=k<self.n:raise ValueError('frequency out of range')
        return (k%self.G)*self.inv3%self.G, (k%3)*self.invg%3
    def grid_to_k(self,j,k3):
        return (3*j+self.G*k3)%self.n
    def _make_triple(self,j,row_samples):
        if j not in self.triples:
            self.triples[j]=TripleCodelet(*(row_samples[row][j] for row in range(3)), self.p,self.eta,self.coefficients)
        return self.triples[j]
    def preview(self,frequencies):
        if self.preview_done:raise ValueError('one preview batch supported')
        qs=sorted(set(frequencies))
        if not qs:raise ValueError('need nonempty frequencies')
        grid=[(k,*self.k_to_grid(k)) for k in qs]
        keys={a for _,a,_ in grid};self.preview_j=keys
        rs=[row.preview(keys) for row in self.rows]
        out={}
        for k,j,k3 in grid:
            out[k]=self._make_triple(j,rs).get(k3)
        self.cache.update(out);self.preview_done=True
        return out
    def full(self):
        rs=[]
        for row in self.rows:rs.append(row.full())
        for j in range(self.G):
            self._make_triple(j,rs).full()
        out=[None]*self.n
        for j,triple in self.triples.items():
            for k3,v in enumerate(triple.full()):out[self.grid_to_k(j,k3)]=v
        assert all(v is not None for v in out)
        return out
    def stats(self):
        adds=sum(row.stats.additions for row in self.rows)
        muls=sum(row.stats.multiplications for row in self.rows)
        adds+=sum(tr.cnt.additions for tr in self.triples.values())
        muls+=sum(tr.cnt.multiplications for tr in self.triples.values())
        backups=sum(row.stats.backup_peak for row in self.rows)
        return dict(field_additions=adds,field_multiplications=muls,arithmetic=adds+muls,
            peak_backup_words=backups,backup_current=sum(row.storage_bound()['current_backup_words'] for row in self.rows),
            triple_states=len(self.triples),index_permutation_moves=self.cnt.permutations,
            working_words=self.n,root_table_words=self.G,
            root_setup_multiplications=self.root_setup_ops,
            winograd_setup_field_ops=3,
            input_permutation_writes=self.n,
            row_copy_writes=self.n)
    def predicted_full_arithmetic(self):
        G=self.G;L=G.bit_length()-1
        return 3*(G*L+(G//2*L-G+1))+8*G


def ct3_baseline(x,p=2013265921,g=31):
    """Fair Cooley-Tukey N=3G reference: same FFTG and Winograd triple codelets,
    but with the two required nonidentity twiddles per kG>0.
    """
    N=len(x)
    if N%3:raise ValueError('N divisible by 3 required')
    G=N//3
    if G<2 or G&(G-1):raise ValueError('G power of two >=2 required')
    omega=primitive_roots(N,p,g);wG=pow(omega,3,p);eta=pow(omega,G,p)
    cnt=Count(permutations=N)
    coeffs=winograd_constants(eta,p)
    table=[1]*(2*G)
    for j in range(1,len(table)):table[j]=table[j-1]*omega%p
    # Root table generation is setup, deliberately excluded from per-input graph.
    row_inputs=[[x[j3+3*jG] for jG in range(G)] for j3 in range(3)]
    row_outputs=[]
    for inputs in row_inputs:
        out,stats=base_radix2_full(inputs,p,wG)
        row_outputs.append(out)
        cnt.additions+=stats.additions;cnt.multiplications+=stats.multiplications
    Y=[None]*N
    for kG in range(G):
        a=row_outputs[0][kG]
        b=row_outputs[1][kG]
        c=row_outputs[2][kG]
        if kG>0:
            b=b*table[kG]%p
            c=c*table[2*kG]%p
            cnt.multiplications+=2
        tr=TripleCodelet(a,b,c,p,eta,coeffs)
        vals=tr.full()
        cnt.additions+=tr.cnt.additions;cnt.multiplications+=tr.cnt.multiplications
        for k3,v in enumerate(vals):Y[kG+G*k3]=v
    return Y,cnt


def direct_dft(x,omega,p):
    n=len(x);out=[]
    for k in range(n):
        wk=pow(omega,k,p);z=1;acc=0
        for v in x:
            acc=(acc+v*z)%p;z=z*wk%p
        out.append(acc)
    return out
