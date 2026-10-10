"""Independent exact exploratory reductions; not a uniform theorem."""
import json, time
from pathlib import Path
import sympy as sp
q=sp.Symbol('q')

def bmod(a,b):
    while a and a.bit_length()>=b.bit_length(): a ^= b<<(a.bit_length()-b.bit_length())
    return a

def bmul(a,b):
    c=0
    while b:
        if b&1:c^=a
        a<<=1; b>>=1
    return c

def inv(a,f):
    r,s=f,a; u,v=0,1
    while s:
        t=0; rr=r
        while rr and rr.bit_length()>=s.bit_length():
            j=rr.bit_length()-s.bit_length();t^=1<<j;rr^=s<<j
        r,s=s,rr;u,v=v,u^bmul(t,v)
    assert r==1
    return bmod(u,f)

def mul(a,b,f):return bmod(bmul(a,b),f)
def trim(a):
    while a and not a[-1]:a.pop()
    return a

def rem(a,b,f):
    a=a[:];bi=inv(b[-1],f)
    while len(a)>=len(b):
        v=mul(a[-1],bi,f); d=len(a)-len(b)
        for j,c in enumerate(b):a[j+d]^=mul(v,c,f)
        trim(a)
    return a

def gcd(a,b,f):
    while b:a,b=b,rem(a,b,f)
    v=inv(a[-1],f)
    return [mul(c,v,f) for c in a]

def rs(n,f):
    h=[1]; qp=1
    # q-Pascal: [n,k]=[n-1,k]+q^(n-k)[n-1,k-1].
    for j in range(1,n+1):
        nh=[0]*(j+1); powers=[1]
        for k in range(j):powers.append(mul(powers[-1],2,f))
        for k in range(j+1):
            if k<j:nh[k]^=h[k]
            if k:nh[k]^=mul(powers[j-k],h[k-1],f)
        h=nh
    return h

def factors(n):
    pp=sp.Poly(sp.cyclotomic_poly(n,q),q,modulus=2)
    out=[]
    for a,e in sp.factor_list(pp)[1]:
        assert e==1
        f=sum((int(c)%2)<<i for i,c in enumerate(reversed(a.all_coeffs())))
        out.append(f)
    return sorted(out,key=lambda f:(f.bit_length(),f))

def power(a,k,f):
    r=1
    while k:
        if k&1:r=mul(r,a,f)
        a=mul(a,a,f);k>>=1
    return r

if __name__=='__main__':
    t=time.time();rows=[]
    for N in range(5,402,4):
        if sp.isprime(N):continue
        ff=factors(N); trials=[]
        for f in ff:
            assert power(2,N,f)==1
            assert all(power(2,N//p,f)!=1 for p in sp.factorint(N))
            h=rs((N-1)//2,f)
            d=trim([h[j] if j%2 else 0 for j in range(1,len(h))])
            g=gcd(h,d,f)
            trials.append({'modulus_bits':hex(f),'extension_degree':f.bit_length()-1,'gcd_degree':len(g)-1})
            if len(g)==1:break
        rows.append({'N':N,'trials':trials,'squarefree_at_some_prime_above_two':len(g)==1})
        print(N,trials,flush=True)
        Path(__file__).with_name('CHARACTERISTIC_TWO_RESULTS.json').write_text(json.dumps({'cases':rows,'elapsed_seconds':time.time()-t,'uniform_claim':False},indent=2)+'\n')
