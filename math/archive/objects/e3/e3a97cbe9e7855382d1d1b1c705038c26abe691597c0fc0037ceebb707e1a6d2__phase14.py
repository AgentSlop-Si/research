"""HERO #17 Phase 14: mixed Weyl (magnetic) Green operators.

Exact modular algorithms, NOT a faster full DFT.
Field: prime p, primitive n-th root omega supplied (n | p-1).
S e_j=e_(j+1); T e_j=omega**j e_j.

H(eps,delta)=(I-alpha*S**eps-beta*T**delta)**-1, eps,delta in {+1,-1}.

Online all-vector execution uses a cyclic *first-order* recurrence, including
instances with a zero diagonal pivot. Operation counters are for prime-field
additions, multiplications and inversions, with the latter counted separately.
The Python pow used for an inverse is not a bit-level operation counter.
"""
from dataclasses import dataclass
from math import isqrt


def isprime(n):
    return n >= 2 and all(n % d for d in range(2,isqrt(n)+1))


def prime_factors(n):
    f=[];d=2
    while d*d<=n:
        if n % d==0:
            f.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:f.append(n)
    return f


def primitive_root(n,p):
    if not isprime(p) or (p-1)%n:raise ValueError('n must divide p-1, p prime')
    for g in range(2,p):
        w=pow(g,(p-1)//n,p)
        if w !=1 and all(pow(w,n//q,p)!=1 for q in prime_factors(n)):
            return w
    raise ValueError('no primitive root found')


def pow_count(a,e,p,c):
    """Nonnegative exponent using charged square-and-multiply."""
    if e<0:raise ValueError('pow_count exponent must be >=0')
    acc=1
    while e:
        if e&1:
            acc=(acc*a)%p;c.mul+=1
        e>>=1
        if e:
            a=(a*a)%p;c.mul+=1
    return acc


@dataclass
class Counts:
    add:int=0
    mul:int=0
    inv:int=0
    read:int=0
    write:int=0
    @property
    def field_ops(self):return self.add+self.mul+self.inv
    def as_dict(self):return {'adds':self.add,'multiplies':self.mul,'inversions':self.inv,
                              'field_ops':self.field_ops,'array_reads':self.read,'writes':self.write}


def inv_field(z,p,c):
    """One field inverse; bit-level modular inversion is not unit cost."""
    if z%p==0:raise ValueError('division by zero')
    c.inv+=1
    return pow(z,-1,p)


class MagneticGreen:
    """Charged O(n) preparation, O(n) online, O(n) storage.

    eps=shift exponent; delta=modulation exponent. Inputs and outputs are in
    their physical coordinate order, and the index permutation is charged via
    read and write counters. No FFT, matrix products, or N² intermediate.
    """
    def __init__(self,n,p,w,alpha,beta,eps=1,delta=1):
        if n<2 or eps not in (-1,1) or delta not in (-1,1):raise ValueError('invalid size or signs')
        self.n,self.p,self.w,self.alpha,self.beta=n,p,w,alpha%p,beta%p
        self.eps,self.delta=eps,delta
        self.prep=Counts();c=self.prep
        a=self.alpha;b=self.beta
        q=w if eps*delta==1 else inv_field(w,p,c)
        # Check exact nonsingularity independently of the recurrence.
        an=pow_count(a,n,p,c);bn=pow_count(b,n,p,c)
        self.discriminant=(1-an-bn)%p;c.add+=2
        if not self.discriminant:raise ValueError('singular magnetic Green')
        if not a:
            ds=[];prefix=[1]
            power=1
            for _ in range(n):
                d=(1-b*power)%p;c.mul+=1;c.add+=1
                if not d:raise ValueError('singular diagonal')
                ds.append(d)
                prefix.append(prefix[-1]*d%p);c.mul+=1
                power=power*q%p;c.mul+=1
            running=inv_field(prefix[-1],p,c)
            self.inverse_diag=[0]*n
            for j in range(n-1,-1,-1):
                self.inverse_diag[j]=running*prefix[j]%p
                running=running*ds[j]%p;c.mul+=2
            self.r=None
        else:
            ainv=inv_field(a,p,c)
            self.ainv=ainv;self.d=[];self.r=[]
            power=1
            for _ in range(n):
                d=(1-b*power)%p;c.mul+=1;c.add+=1
                self.d.append(d)
                self.r.append(d*ainv%p);c.mul+=1
                power=power*q%p;c.mul+=1
            at=1
            for j in range(n-1,0,-1):
                at=at*self.r[j]%p;c.mul+=1
            den=(self.d[0]*at-a)%p;c.mul+=1;c.add+=1
            self.denin=inv_field(den,p,c)
            # Det identity: (d0*at-a)*alpha^(n-1)=Delta
            assert den*pow_count(a,n-1,p,c)%p == self.discriminant

    def apply(self,x,counts=None):
        if len(x)!=self.n:raise ValueError('length mismatch')
        c=counts if counts is not None else Counts()
        n=self.n;p=self.p;eps=self.eps
        if self.r is None:
            y=[0]*n
            for j,iv in enumerate(self.inverse_diag):
                i=(eps*j)%n
                y[i]=x[i]*iv%p;c.mul+=1;c.read+=1;c.write+=1
            return y
        # Online: two passes over N; no dense matrix, no calls to FFT.
        bacc=0
        for j in range(n-1,0,-1):
            i=(eps*j)%n;c.read+=1
            bacc=(self.r[j]*bacc-self.ainv*x[i])%p
            c.mul+=2;c.add+=1
        c.read+=1
        yn=(x[0]-self.d[0]*bacc)*self.denin%p;c.add+=1;c.mul+=2
        y=[0]*n
        old_i=(eps*(n-1))%n;y[old_i]=yn;c.write+=1
        for j in range(n-1,0,-1):
            new_i=(eps*(j-1))%n
            y[new_i]=(self.r[j]*y[old_i]-self.ainv*x[old_i])%p
            c.mul+=2;c.add+=1;c.read+=2;c.write+=1
            old_i=new_i
        return y


def direct_matrix(n,p,w,a,b,eps=1,delta=1):
    """Build sparse inverse-target matrix for small independent oracle tests."""
    A=[[0]*n for _ in range(n)]
    for i in range(n):
        A[i][i]=(1-b*pow(w,delta*i%n,p))%p
        A[i][(i-eps)%n]=(A[i][(i-eps)%n]-a)%p
    return A


def inverse_dense(A,p):
    n=len(A)
    a=[[v%p for v in row]+[int(i==j)for j in range(n)]for i,row in enumerate(A)]
    for k in range(n):
        r=next((i for i in range(k,n) if a[i][k]),None)
        if r is None:raise ValueError('singular matrix')
        a[k],a[r]=a[r],a[k]
        inv=pow(a[k][k],-1,p)
        a[k]=[v*inv%p for v in a[k]]
        for i in range(n):
            if i!=k and a[i][k]:
                z=a[i][k];a[i]=[(v-z*t)%p for v,t in zip(a[i],a[k])]
    return [row[n:] for row in a]


def reference_row(i,x,alpha,beta,eps,delta,w,p):
    """O(n) independent Green-kernel row evaluation via polynomial products.

    Unlike MagneticGreen.apply this does not solve a recurrence for outputs;
    it sums exact nonzero kernel entries with prefix products. Used for audits.
    """
    n=len(x);q=w if eps*delta==1 else pow(w,-1,p)
    # All physical diagonal d_(eps*j) for j=0..n-1.
    d=[];power=1
    for j in range(n):
        d.append((1-beta*power)%p)
        power=power*q%p
    # Convert physical row i into ordered-cycle row t.
    t=(eps*i)%n
    # Prefix products along the forward cycle starting immediately AFTER row t.
    pre=[1]
    for r in range(1,n):
        pre.append(pre[-1]*d[(t+r)%n]%p)
    Delta=(1-pow(alpha,n,p)-pow(beta,n,p))%p
    if Delta==0:raise ValueError('singular')
    invDelta=pow(Delta,-1,p)
    ans=0;apow=1
    for ell in range(n):
        j=(t-ell)%n
        ans=(ans+apow*pre[n-1-ell]*x[(eps*j)%n])%p
        apow=apow*alpha%p
    return ans*invDelta%p


def matrix_power(A,k,p):
    n=len(A);out=[[int(i==j) for j in range(n)]for i in range(n)]
    while k:
        if k&1:out=matmul(out,A,p)
        k//=2
        if k:A=matmul(A,A,p)
    return out


def matmul(A,B,p):
    n=len(A);m=len(B[0]);z=len(B)
    return [[sum(A[i][k]*B[k][j] for k in range(z))%p for j in range(m)]for i in range(n)]


def q_polynomial_operator(n,p,w,a,b,eps=1,delta=1):
    """O(n^4) independent small-n matrix polynomial reference (not executor)."""
    D=direct_matrix(n,p,w,a,b,eps,delta)
    W=[[(int(i==j)-D[i][j])%p for j in range(n)]for i in range(n)]
    powW=[[int(i==j)for j in range(n)]for i in range(n)]
    summed=[[0]*n for _ in range(n)]
    for _ in range(n):
        for i in range(n):
            for j in range(n):summed[i][j]=(summed[i][j]+powW[i][j])%p
        powW=matmul(powW,W,p)
    Delta=(1-pow(a,n,p)-pow(b,n,p))%p
    return [[v*pow(Delta,-1,p)%p for v in row]for row in summed],powW


def weyl_coeff(A,w,p):
    n=len(A);nin=pow(n,-1,p)
    return [[nin*sum(pow(w,(-b*j)%n,p)*A[(j+a)%n][j] for j in range(n))%p
             for b in range(n)]for a in range(n)]


def triangular_support(n,eps,delta):
    return {((eps*a)%n,(delta*b)%n)for a in range(n)for b in range(n)if a+b<n}


def rank_mod(A,p):
    if not A:return 0
    a=[list(row)for row in A];nr=len(a);nc=len(a[0]);r=0
    for c in range(nc):
        i=next((z for z in range(r,nr)if a[z][c]),None)
        if i is None:continue
        a[r],a[i]=a[i],a[r]
        v=pow(a[r][c],-1,p)
        a[r]=[z*v%p for z in a[r]]
        for k in range(r+1,nr):
            if a[k][c]:
                t=a[k][c];a[k]=[(z-t*h)%p for z,h in zip(a[k],a[r])]
        r+=1
        if r==nr:break
    return r


def fourier(n,w,p):
    return [[pow(w,i*j%n,p)for j in range(n)]for i in range(n)]


def centered_block_rank(A,p):
    n=len(A);m=n//2
    rows=range(n-m,n);cols=range(m)
    return rank_mod([[A[i][j]for j in cols]for i in rows],p)


def twirl_matrix(H,n,w,p,operator='T'):
    """Deliberately dense O(n^4) reference; NOT online executor."""
    out=[[0]*n for _ in range(n)]
    nin=pow(n,-1,p)
    for i in range(n):
        for j in range(n):
            total=0
            for k in range(n):
                if operator=='T':
                    total+=pow(w,k*(i-j)%n,p)*H[i][j]
                elif operator=='S':
                    total+=H[(i-k)%n][(j-k)%n]
                else:raise ValueError('operator must be S or T')
            out[i][j]=total*nin%p
    return out


def twirl_closed_matrix(n,a,b,w,p,operator='T'):
    """Polynomial (no inverses of potentially singular one-direction Greens)."""
    den=pow((1-pow(a,n,p)-pow(b,n,p))%p,-1,p)
    out=[[0]*n for _ in range(n)]
    if operator=='T':
        for i in range(n):
            out[i][i]=sum(pow(b,k,p)*pow(w,i*k%n,p) for k in range(n))*den%p
    else:
        for i in range(n):
            for j in range(n):out[i][j]=pow(a,(i-j)%n,p)*den%p
    return out


def fused_weyl_twirl(x,p,w,alpha,beta,axis='T'):
    """Apply average over all n Weyl conjugates of magnetic Green H++.

      axis='T': (1/n) sum T**k H T**(-k)
      axis='S': (1/n) sum S**k H S**(-k)

    Exactly O(n) charged prime-field arithmetic, also when the individual
    one-direction Green would be singular. Returns (y, charged_counts).
    No explicit n-way branching and no FFT.
    """
    n=len(x);a=alpha%p;b=beta%p
    if n<2 or axis not in ('S','T'):raise ValueError('unsupported twirl')
    c=Counts()
    an=pow_count(a,n,p,c);bn=pow_count(b,n,p,c)
    delta=(1-an-bn)%p;c.add+=2
    if not delta:raise ValueError('singular mixed operator')
    din=inv_field(delta,p,c)
    y=[0]*n
    if axis=='T':
        if bn!=1:
            op=MagneticGreen(n,p,w,0,b)
            z=op.apply(x,c)
            factor=(1-bn)*din%p;c.add+=1;c.mul+=1
            for j in range(n):
                y[j]=z[j]*factor%p;c.mul+=1;c.write+=1
            c.add+=op.prep.add;c.mul+=op.prep.mul;c.inv+=op.prep.inv
        else:
            # A single diagonal selector; find beta*w**j == 1 by scanning.
            power=1
            for j in range(n):
                if b*power%p==1:
                    y[j]=n*x[j]*din%p;c.mul+=2;c.read+=1
                c.mul+=2;power=power*w%p;c.write+=1
    else:
        if an!=1:
            op=MagneticGreen(n,p,w,a,0)
            z=op.apply(x,c)
            factor=(1-an)*din%p;c.add+=1;c.mul+=1
            for j in range(n):
                y[j]=z[j]*factor%p;c.mul+=1;c.write+=1
            c.add+=op.prep.add;c.mul+=op.prep.mul;c.inv+=op.prep.inv
        else:
            # Rank-one root-of-unity weighted cyclic sum.
            ainv=inv_field(a,p,c)
            pw=1;total=0
            for j in range(n):
                total=(total+pw*x[j])%p;c.mul+=1;c.add+=1;c.read+=1
                pw=pw*ainv%p;c.mul+=1
            pw=1
            for j in range(n):
                y[j]=pw*total*din%p;c.mul+=2;c.write+=1
                pw=pw*a%p;c.mul+=1
    return y,c


def both_cut_ranks(A,p):
    """Two contiguous cross-block ranks at split floor(n/2)."""
    n=len(A);m=n//2
    left=range(m);right=range(m,n)
    return (rank_mod([[A[i][j]for j in left]for i in right],p),
            rank_mod([[A[i][j]for j in right]for i in left],p))


class StridedMagneticGreen:
    """Exact O(n) application of (I-alpha*S**stride-beta*T**delta)**-1.

    This is a NEW restricted class: arbitrary stride may create many cycles,
    each solved by a first-order recurrence. Not an FFT; root-of-unity
    binomial law is not asserted for non-coprime shifts.
    """
    def __init__(self,n,p,w,alpha,beta,stride,delta=1):
        if n<2 or delta not in (-1,1):raise ValueError('bad length or modulation sign')
        self.n=n;self.p=p;self.w=w
        self.alpha=alpha%p;self.beta=beta%p
        self.stride=stride%n;self.delta=delta
        c=Counts();self.prep=c
        # Full physical diagonal: no FFT and all phase generation charged.
        q=w if delta==1 else inv_field(w,p,c)
        power=1;diagonal=[]
        for _ in range(n):
            diagonal.append((1-self.beta*power)%p);c.mul+=1;c.add+=1
            power=power*q%p;c.mul+=1
        if not self.alpha:
            if any(d==0 for d in diagonal):raise ValueError('singular diagonal')
            prefixes=[1]
            for d in diagonal:prefixes.append(prefixes[-1]*d%p);c.mul+=1
            carry=inv_field(prefixes[-1],p,c)
            self.invdiag=[0]*n
            for j in range(n-1,-1,-1):
                self.invdiag[j]=carry*prefixes[j]%p
                carry=carry*diagonal[j]%p;c.mul+=2
            self.cycles=[]
            return
        self.invdiag=None
        ainv=inv_field(self.alpha,p,c);self.ainv=ainv
        seen=[False]*n
        info=[];denoms=[]
        for start in range(n):
            if seen[start]:continue
            idx=[];k=start
            while not seen[k]:
                seen[k]=True;idx.append(k)
                k=(k+self.stride)%n
            assert k==start
            rr=[diagonal[t]*ainv%p for t in idx];c.mul+=len(idx)
            ap=1
            for j in range(len(idx)-1,0,-1):
                ap=ap*rr[j]%p;c.mul+=1
            den=(diagonal[idx[0]]*ap-self.alpha)%p;c.mul+=1;c.add+=1
            if not den:raise ValueError('one cyclic component is singular')
            info.append((idx,rr,diagonal[idx[0]]));denoms.append(den)
        # Batch all cyclic closure inverses with just one field inversion.
        pref=[1]
        for d in denoms:pref.append(pref[-1]*d%p);c.mul+=1
        run=inv_field(pref[-1],p,c)
        invden=[0]*len(denoms)
        for j in range(len(denoms)-1,-1,-1):
            invden[j]=run*pref[j]%p
            run=run*denoms[j]%p;c.mul+=2
        self.cycles=[(idx,rr,d0,invden[j])for j,(idx,rr,d0)in enumerate(info)]

    def apply(self,x,c=None):
        if len(x)!=self.n:raise ValueError('length mismatch')
        c=c if c is not None else Counts()
        n=self.n;p=self.p
        y=[0]*n
        if self.invdiag is not None:
            for i in range(n):
                y[i]=x[i]*self.invdiag[i]%p;c.mul+=1;c.read+=1;c.write+=1
            return y
        for ids,r,d0,deninv in self.cycles:
            z=0
            for j in range(len(ids)-1,0,-1):
                z=(r[j]*z-self.ainv*x[ids[j]])%p
                c.mul+=2;c.add+=1;c.read+=1
            val=(x[ids[0]]-d0*z)*deninv%p
            c.mul+=2;c.add+=1;c.read+=1
            y[ids[-1]]=val;c.write+=1
            for j in range(len(ids)-1,0,-1):
                y[ids[j-1]]=(r[j]*y[ids[j]]-self.ainv*x[ids[j]])%p
                c.mul+=2;c.add+=1;c.read+=2;c.write+=1
        return y
