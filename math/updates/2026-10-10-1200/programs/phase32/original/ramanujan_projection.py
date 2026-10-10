"""Fast exact DFT of the rational Galois-orbit component of ANY input.

Given x of length n over characteristic-zero field or F_p (p>n), let P
average coordinates within each gcd(k,n) class. Return F_n P x.
No Fourier root is required by this evaluator. Field arithmetic is
O(n + tau(n)^2)=O(n), and integer word processing is O(n) in a word-RAM
using a linear sieve and tau(n)=n^o(1). Memory O(n).

The mathematical identity is the classical Ramanujan-Fourier transform
of even functions mod n. We claim integration/audit, not its invention.
"""
from __future__ import annotations
from dataclasses import dataclass
from math import gcd

@dataclass
class Counter:
    additions:int=0
    multiplications:int=0
    inversions:int=0
    stored_field_elements:int=0
    def field_ops(self):return self.additions+self.multiplications


def arithmetic_sieve(n):
    if n<1:raise ValueError('positive length required')
    spf=[0]*(n+1);phi=[0]*(n+1);mu=[0]*(n+1);primes=[]
    phi[1]=mu[1]=1
    for i in range(2,n+1):
        if spf[i]==0:
            spf[i]=i;primes.append(i);phi[i]=i-1;mu[i]=-1
        for p in primes:
            if p>spf[i] or p*i>n:break
            spf[i*p]=p
            if i%p==0:
                phi[i*p]=phi[i]*p;mu[i*p]=0;break
            phi[i*p]=phi[i]*(p-1);mu[i*p]=-mu[i]
    return spf,phi,mu

def gcd_table(n,spf):
    vals=[0]*n
    vals[0]=n
    if n>1:vals[1]=1
    for j in range(2,n):
        p=spf[j];base=vals[j//p]
        vals[j]=base*p if (n//base)%p==0 else base
        assert n%vals[j]==0
    return vals

def divisors_by_scan(n):
    return [d for d in range(1,n+1) if n%d==0]

def rational_projection(x,p=None):
    """Return exact F_n P_Q x and cost, with field char 0 or F_p.

    For p is None, use fractions.Fraction for exact characteristic-zero
    scaling (input x may contain rational entries); for p positive prime,
    use modular inverses; require p>n so all gcd-orbit sizes are invertible.
    """
    from fractions import Fraction
    n=len(x)
    if not n:raise ValueError('empty input')
    if p is not None and p<=n:raise ValueError('prime field characteristic must exceed n')
    c=Counter()
    spf,phi,mu=arithmetic_sieve(n)
    gcds=gcd_table(n,spf)
    ds=divisors_by_scan(n)
    sums={d:0 for d in ds};nonempty=set()
    for k,value in enumerate(x):
        d=gcds[k]
        value = value if p is None else value%p
        if d in nonempty:
            sums[d]=sums[d]+value if p is None else (sums[d]+value)%p
            c.additions+=1
        else:
            sums[d]=value;nonempty.add(d)
    means={}
    for d in ds:
        size=phi[n//d]
        if size==1:
            means[d]=sums[d]
        elif p is None:
            means[d]=sums[d]*Fraction(1,size);c.multiplications+=1
        else:
            means[d]=sums[d]*pow(size,-1,p)%p
            c.multiplications+=1;c.inversions+=1
    values={}
    for jg in ds:
        value=0;started=False
        for kg in ds:
            m=n//kg
            z=m//gcd(m,jg)
            sign=mu[z]
            if not sign:continue
            coef=sign*(phi[m]//phi[z])
            term=means[kg]
            if coef!=1:
                if coef==-1:term=-term
                else:
                    term=term*coef if p is None else term*coef%p
                    c.multiplications+=1
            if started:
                value=value+term if p is None else (value+term)%p
                c.additions+=1
            else:
                value=term;started=True
        values[jg]=value if p is None else value%p
    result=[values[g] for g in gcds]
    c.stored_field_elements=2*n+3*len(ds) # sums, means, orbit outputs + input/output reference
    return result,c

def projector_by_gcd(x,p=None):
    """Explicit rational orbit projector P_H for E=Q; test/reference."""
    n=len(x);spf,phi,mu=arithmetic_sieve(n);gt=gcd_table(n,spf)
    bucket={};counts={}
    for i,a in enumerate(x):
        d=gt[i];bucket[d]=bucket.get(d,0)+a;counts[d]=counts.get(d,0)+1
    if p is None:
        from fractions import Fraction
        mean={d:Fraction(bucket[d],counts[d]) for d in bucket}
    else:
        mean={d:bucket[d]*pow(counts[d],-1,p)%p for d in bucket}
    return [mean[gt[i]] for i in range(n)]

def direct_dft(x,p,root):
    n=len(x)
    powers=[1]*n
    for i in range(1,n): powers[i]=powers[i-1]*root%p
    return [sum(x[k]*powers[(j*k)%n] for k in range(n))%p for j in range(n)]

if __name__=='__main__':
    from relative_cyclotomic import FIELDS,order_root
    import random
    for n in [1,2,4,8,15,16,30,60,120,240,480,960]:
        for p,gen in FIELDS:
            if (p-1)%n:continue
            rng=random.Random(n+p)
            inp=[rng.randrange(p) for _ in range(n)]
            pred,c=rational_projection(inp,p)
            target=direct_dft(projector_by_gcd(inp,p),p,order_root(n,p,gen))
            assert pred==target,(n,p)
            print(n,p,'arithmetic',c.field_ops(),'tau memory',c.stored_field_elements)
