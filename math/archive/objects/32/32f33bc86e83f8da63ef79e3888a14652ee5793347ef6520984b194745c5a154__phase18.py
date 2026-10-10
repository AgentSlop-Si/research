"""Hero #17 Phase 18: exact root-of-unity magnetic Green orbit fusion.

Algebra over a supplied prime field, N-th root and factor K|N.
S e_i=e_{i+1}; U e_i=q**i e_i, q=omega**(N/K).
G_j=(I-a*S-b*q**j*U)^(-1), j=0,...,K-1.

R_l = (1/K) sum_j q**(-j*l) G_j.
The l=0 R_0 has a fully charged O(N) executor, even for growing K.
Each fixed l sector has O((l+1)N+poly(l)+K) arithmetic cost.

This computes resolvent averages, NOT the DFT; all claims are model-specific.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd


def prime_factors(n):
    ans=[];f=2
    while f*f<=n:
        if n%f==0:
            ans.append(f)
            while n%f==0:n//=f
        f+=1
    if n>1:ans.append(n)
    return ans


def primitive_nth_root(n,p):
    if n<2 or (p-1)%n:raise ValueError('N must divide p-1')
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in prime_factors(p-1)):
            w=pow(g,(p-1)//n,p)
            assert pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in prime_factors(n))
            return w
    raise ValueError('no primitive generator found')


@dataclass
class Count:
    add_sub:int=0
    mult:int=0
    inv:int=0
    def add(self,a,b,p):self.add_sub+=1;return (a+b)%p
    def sub(self,a,b,p):self.add_sub+=1;return (a-b)%p
    def mul(self,a,b,p):self.mult+=1;return (a*b)%p
    def inverse(self,a,p):
        if a%p==0:raise ZeroDivisionError('noninvertible scalar')
        self.inv+=1;return pow(a,-1,p)
    def report(self):return dict(add_sub=self.add_sub,mult=self.mult,inv=self.inv,total_field_ops=self.add_sub+self.mult+self.inv)


def power_count(a,exp,p,c):
    """Binary power with each field multiply counted (including squaring)."""
    value=1;base=a%p
    while exp:
        if exp&1:value=c.mul(value,base,p)
        exp>>=1
        if exp:base=c.mul(base,base,p)
    return value


def cyclic_window(x,base,length,p,c):
    """Apply sum_{r=0}^{length-1} base**r S**r in O(N+length) field ops.
    Every index lookup is constant-time; no FFT, precomputation or free table.
    """
    n=len(x)
    if not 1<=length<=n:raise ValueError('bad window length')
    if length==1:return list(x)
    bp=power_count(base,length,p,c)
    seed=0;val=1
    for r in range(length):
        seed=c.add(seed,c.mul(val,x[(-r)%n],p),p)
        val=c.mul(val,base,p)
    output=[0]*n;output[0]=seed
    for i in range(1,n):
        output[i]=c.sub(c.add(c.mul(base,output[i-1],p),x[i],p),
                        c.mul(bp,x[(i-length)%n],p),p)
    return output


class StridedGreenPlan:
    """Prepared inverse of D=d I - a^K S^K; K disjoint length-M cycles."""
    def __init__(self,n,k,p,c_d, a_k, counter=None):
        if n%k:raise ValueError('k must divide n')
        self.n,self.k,self.m,self.p=n,k,n//k,p
        self.d,self.ck=c_d%p,a_k%p
        c=counter or Count();self.preparation_counter=c
        if self.d==0:
            if self.ck==0:raise ValueError('D is singular')
            self.zero_case=True
            self.scale=c.inverse((-self.ck)%p,p)
        else:
            self.zero_case=False
            self.inv_d=c.inverse(self.d,p)
            self.r=c.mul(self.ck,self.inv_d,p)
            self.r_m=power_count(self.r,self.m,p,c)
            self.inv_closure=c.inverse(c.sub(1,self.r_m,p),p)
    def apply(self,x,c=None):
        c=c or Count();n,k,m,p=self.n,self.k,self.m,self.p
        if len(x)!=n:raise ValueError('bad RHS length')
        if self.zero_case:
            return [c.mul(self.scale,x[(i+k)%n],p) for i in range(n)]
        output=[0]*n
        for residue in range(k):
            B=0
            for t in range(m):
                i=residue+k*t
                B=c.add(c.mul(self.r,B,p),c.mul(self.inv_d,x[i],p),p)
            z=c.mul(B,self.inv_closure,p)
            for t in range(m):
                i=residue+k*t
                z=c.add(c.mul(self.r,z,p),c.mul(self.inv_d,x[i],p),p)
                output[i]=z
        return output


class MagneticTwirlPlan:
    """O(N) averaged inverse for K noncommuting magnetic Green branches."""
    def __init__(self,n,k,p,alpha,beta,omega,c=None):
        if n%k:raise ValueError('K must divide N')
        self.n,self.k,self.p=n,k,p
        self.alpha,self.beta=alpha%p,beta%p
        self.omega=omega
        self.counter=c or Count()
        c=self.counter
        # This checks a supplied root; root search itself is not charged here.
        # Integer trial division costs O(sqrt(N)) RAM operations and is part
        # of the asymptotic preparation bound but not scalar-field ledger.
        if power_count(omega,n,p,c)!=1 or any(
            power_count(omega,n//z,p,c)==1 for z in prime_factors(n)
        ):
            raise ValueError('omega must have exact order N')
        self.q=power_count(omega,n//k,p,c)
        self.ak=power_count(self.alpha,k,p,c)
        self.bk=power_count(self.beta,k,p,c)
        d=c.sub(1,self.bk,p)
        self.strided=StridedGreenPlan(n,k,p,d,self.ak,c)
    def apply(self,x,c=None):
        c=c or Count()
        t=cyclic_window(x,self.alpha,self.k,self.p,c)
        return self.strided.apply(t,c)


class WeightedSectorPlan:
    """O((ell+1)N + K + ell^2) exact executor for R_ell, ell<K.
    Uses polynomial expansion of Gaussian binomial coefficient (q-Pochhammer).
    """
    def __init__(self,twirl:MagneticTwirlPlan,ell:int,c=None):
        self.twirl=twirl
        n,k,p,q=twirl.n,twirl.k,twirl.p,twirl.q
        if not 0<=ell<k:raise ValueError('sector must be in [0,K)')
        self.ell=ell;self.window=k-ell;self.p=p
        c=c or Count();self.counter=c
        poly=[1];den=1;qh=q
        # ∏_{i=1}^ell(1-q^i z)
        for i in range(1,ell+1):
            nxt=[0]*(len(poly)+1)
            for j,val in enumerate(poly):
                nxt[j]=c.add(nxt[j],val,p)
                nxt[j+1]=c.sub(nxt[j+1],c.mul(val,qh,p),p)
            poly=nxt
            den=c.mul(den,c.sub(1,qh,p),p)
            qh=c.mul(qh,q,p)
        invden=c.inverse(den,p)
        betapow=power_count(twirl.beta,ell,p,c)
        common=c.mul(betapow,invden,p)
        self.coeffs=[c.mul(common,a,p) for a in poly]
        self.bases=[]
        base=twirl.alpha
        for j in range(ell+1):
            self.bases.append(base)
            base=c.mul(base,q,p)
        self.diag=[]; v=1; qell=power_count(q,ell,p,c)
        for j in range(n):
            self.diag.append(v)
            v=c.mul(v,qell,p)
    def apply(self,x,c=None):
        c=c or Count();n,p=self.twirl.n,self.p
        source=[c.mul(d,z,p) for d,z in zip(self.diag,x)]
        rhs=[0]*n
        for coeff,base in zip(self.coeffs,self.bases):
            window=cyclic_window(source,base,self.window,p,c)
            for i in range(n):rhs[i]=c.add(rhs[i],c.mul(coeff,window[i],p),p)
        return self.twirl.strided.apply(rhs,c)


def independent_cyclic_green_solve(x,alpha,beta_phase,q,p):
    """Independent O(N) per-branch reference solving
    (1-beta_phase*q**i) y_i - alpha*y_(i-1) = x_i.
    Not the fused identity, uses cyclic scalar recurrence and individual inverses.
    """
    n=len(x);ph=1;coeff=[];v=0;A=1
    for i in range(n):
        di=(1-beta_phase*ph)%p
        if di==0:raise ValueError('reference needs nonzero diagonal')
        inv=pow(di,-1,p)
        r=alpha*inv%p;b=x[i]*inv%p
        coeff.append((r,b))
        v=(r*v+b)%p
        A=A*r%p
        ph=ph*q%p
    if A==1:raise ValueError('singular cyclic reference')
    z=v*pow((1-A)%p,-1,p)%p
    ans=[]
    for r,b in coeff:
        z=(r*z+b)%p
        ans.append(z)
    return ans


def independent_twirl(x,alpha,beta,k,p,q,ell=0):
    """Independent sum of K distinct resolvent solves, O(KN)."""
    n=len(x);acc=[0]*n;phase=1
    ik=pow(k,-1,p)
    for j in range(k):
        result=independent_cyclic_green_solve(x,alpha,beta*phase%p,q,p)
        weight=pow(phase,(-ell)%k,p)
        for i in range(n):acc[i]=(acc[i]+weight*result[i])%p
        phase=phase*q%p
    return [(ik*value)%p for value in acc]


def direct_dft(x,p,omega):
    n=len(x)
    return [sum(z*pow(omega,-i*j%n,p) for j,z in enumerate(x))%p for i in range(n)]
