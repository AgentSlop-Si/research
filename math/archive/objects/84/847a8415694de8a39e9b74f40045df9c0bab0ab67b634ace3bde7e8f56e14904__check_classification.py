#!/usr/bin/env python3
"""Fresh exact checks. No project, predecessor, or uploaded code is imported.
Only Python's standard library is used. Coefficients are ascending throughout.
"""
from fractions import Fraction
from pathlib import Path
import hashlib, json, math, time

OUT=Path(__file__).resolve().parent

def trim(a):
    a=list(a)
    while len(a)>1 and not a[-1]: a.pop()
    return a

def add(a,b):
    z=a[0]*0 if a else b[0]*0
    return trim([(a[j] if j<len(a) else z)+(b[j] if j<len(b) else z) for j in range(max(len(a),len(b)))])

def neg(a): return [-x for x in a]
def sub(a,b): return add(a,neg(b))
def scale(a,c): return trim([x*c for x in a])
def mul(a,b):
    c=[a[0]*0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): c[i+j]+=x*y
    return trim(c)

def divmodp(a,b):
    a=trim(a); b=trim(b); zero=a[0]*0
    assert b!=[zero]
    q=[zero]*max(1,len(a)-len(b)+1)
    while len(a)>=len(b) and a!=[zero]:
        j=len(a)-len(b); c=a[-1]/b[-1]; q[j]=c
        for k,x in enumerate(b): a[k+j]-=c*x
        a=trim(a)
    return trim(q),a

def rem(a,b): return divmodp(a,b)[1]
def xgcd(a,b):
    one=a[-1]*0+1; zero=one*0
    u0,u1,v0,v1=[one],[zero],[zero],[one]
    while b!=[zero]:
        q,r=divmodp(a,b); a,b=b,r
        u0,u1=u1,sub(u0,mul(q,u1)); v0,v1=v1,sub(v0,mul(q,v1))
    c=one/a[-1]
    return scale(a,c),scale(u0,c),scale(v0,c)

def deriv(a): return trim([a[j]*j for j in range(1,len(a))])
def peval(a,x):
    r=x*0
    for c in reversed(a):r=r*x+c
    return r

class Fp:
    p=0
    def __init__(self,x): self.x=x.x if isinstance(x,Fp) else int(x)%self.p
    def __bool__(self):return bool(self.x)
    def __eq__(self,y):return self.x==Fp(y).x
    def __add__(self,y):return Fp(self.x+Fp(y).x)
    __radd__=__add__
    def __neg__(self):return Fp(-self.x)
    def __sub__(self,y):return self+-Fp(y)
    def __rsub__(self,y):return Fp(y)+-self
    def __mul__(self,y):return Fp(self.x*Fp(y).x)
    __rmul__=__mul__
    def __truediv__(self,y):return Fp(self.x*pow(Fp(y).x,-1,self.p))
    def __rtruediv__(self,y):return Fp(y)/self
    def __pow__(self,n):return Fp(pow(self.x,n,self.p))
    def __repr__(self):return str(self.x)

# Separate raw-integer modular implementation for large guard certificates.
def mgcd(a,b,p,bezout=False):
    a=a[:]; b=b[:]; u0,u1,v0,v1=[1],[0],[0],[1]
    def mm(a,b):
        c=[0]*(len(a)+len(b)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
        return trim(c)
    def ms(a,b):return trim([((a[i] if i<len(a) else 0)-(b[i] if i<len(b) else 0))%p for i in range(max(len(a),len(b)))])
    while b!=[0]:
        r=a[:]; iq=pow(b[-1],-1,p); quot=[0]*max(1,len(a)-len(b)+1)
        while len(r)>=len(b) and r!=[0]:
            j=len(r)-len(b); c=r[-1]*iq%p; quot[j]=c
            for k,x in enumerate(b):r[k+j]=(r[k+j]-c*x)%p
            r=trim(r)
        a,b=b,r
        if bezout:u0,u1=u1,ms(u0,mm(quot,u1)); v0,v1=v1,ms(v0,mm(quot,v1))
    v=pow(a[-1],-1,p)
    return ([x*v%p for x in a],[x*v%p for x in u0],[x*v%p for x in v0])

def isprime(n):
    if n<2:return False
    if n%2==0:return n==2
    return all(n%d for d in range(3,math.isqrt(n)+1,2))

def factors(n):
    out=[]; d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out

def node(N,p):
    for q in range(2,p):
        if pow(q,N,p)==1 and all(pow(q,N//l,p)!=1 for l in factors(N)):return q
    raise AssertionError('No primitive node')

def mcoeff(m,q,p):
    a=[1]; powers=[pow(q,j,p) for j in range(m+1)]
    for n in range(1,m+1):
        a=[((a[j-1] if j else 0)-(powers[j]*a[j] if j<n else 0))%p for j in range(n+1)]
    return a

def modular_certificates(limit):
    certs=[]
    for N in range(5,limit+1,4):
        p=1; trials=[]; m=(N-1)//2
        while True:
            p+=N
            if not isprime(p):continue
            q=node(N,p); t=mcoeff(m,q,p); dt=[j*t[j]%p for j in range(1,m+1)]
            gs,u,v=mgcd(t,dt,p,True); gn,_,_=mgcd(t,[p-1]+[0]*(N-1)+[1],p)
            trials.append({'p':p,'q':q,'squarefree_gcd_degree':len(gs)-1,'resonance_gcd_degree':len(gn)-1})
            if gs==[1] and gn==[1]:break
        # Explicit Bezout certificate for the only outstanding uniform guard.
        check=[0]*(max(len(u)+len(t),len(v)+len(dt))-1)
        for a,b in [(u,t),(v,dt)]:
            for i,x in enumerate(a):
                for j,y in enumerate(b):check[i+j]=(check[i+j]+x*y)%p
        assert trim(check)==[1]
        certs.append({'N':N,'minimum':m,'prime_p':p,'primitive_q':q,'T':t,'squarefree_bezout_u':u,'squarefree_bezout_v':v,'trials':trials})
    return certs

# Rational cyclotomic fields: no external algebra package.
def cyclotomic(n):
    cache={}
    for d in range(1,n+1):
        if n%d:continue
        a=[Fraction(-1)]+[Fraction(0)]*(d-1)+[Fraction(1)]
        for e in sorted(cache):
            if d%e==0:
                a,r=divmodp(a,cache[e]); assert r==[0]
        cache[d]=a
    return cache[n]

class Cyc:
    modulus=[]
    def __init__(self,x):
        if isinstance(x,Cyc):self.a=x.a;return
        a=x if isinstance(x,(list,tuple)) else [x]
        self.a=tuple(rem([Fraction(v) for v in a],self.modulus))
    def __bool__(self):return any(self.a)
    def __eq__(self,y):return self.a==Cyc(y).a
    def __add__(self,y):return Cyc(add(self.a,Cyc(y).a))
    __radd__=__add__
    def __neg__(self):return Cyc(neg(self.a))
    def __sub__(self,y):return self+-Cyc(y)
    def __rsub__(self,y):return Cyc(y)+-self
    def __mul__(self,y):return Cyc(mul(self.a,Cyc(y).a))
    __rmul__=__mul__
    def inv(self):
        g,u,v=xgcd(list(self.a),self.modulus);assert g==[1];return Cyc(u)
    def __truediv__(self,y):return self*Cyc(y).inv()
    def __rtruediv__(self,y):return Cyc(y)/self
    def __pow__(self,n):
        if n<0:return self.inv()**(-n)
        a=Cyc(1);b=self
        while n:
            if n&1:a=a*b
            b=b*b;n//=2
        return a
    def __repr__(self):return str(self.a)

def coeff(m,q):
    a=[q*0+1]; zero=q*0
    for n in range(1,m+1):a=[(a[j-1] if j else zero)-(q**j*a[j] if j<n else zero) for j in range(n+1)]
    return a

def serialize(x):
    if isinstance(x,Fp):return x.x
    if isinstance(x,Cyc):return [str(v) for v in x.a]
    if isinstance(x,list):return [serialize(v) for v in x]
    return x

def bank_control(N,q,all_basis=True):
    zero=q*0; one=zero+1; m=(N-1)//2; h=(N+1)//2
    f=[q**((h*k*k)%N) for k in range(2*N+1)]
    t=coeff(m,q)
    assert t[0]==(-1)**m
    assert all(t[j]==(-1)**m*t[m-j] for j in range(m+1))
    assert all(sum((t[j]*f[k+j+1] for j in range(m+1)),zero)==zero for k in range(m))
    gs,_,_=xgcd(t,deriv(t));gn,_,_=xgcd(t,[ -one]+[zero]*(N-1)+[one])
    if m%2:
        # Additional resonance can occur in finite characteristic, so this assertion
        # is reserved for characteristic-zero controls or independently good primes.
        if isinstance(q,Cyc): assert gn==[-one,one]
        return {'N':N,'squarefree_gcd_degree':len(gs)-1,'resonance_gcd':serialize(gn),'orthogonality':True}
    assert gs==[one] and gn==[one]
    R=[sum((t[j+1+l]*f[l+1] for l in range(m-j)),zero) for j in range(m)]
    s0=-R[0]/t[0];delta=one-s0
    delta_product=(-1)**m*q**(-m*(m+1)//2)
    for j in range(1,m+1):delta_product*=one-q**j
    assert delta==delta_product and delta!=zero
    s=[s0]+f[1:N]
    assert all(sum((t[j]*s[k+j] for j in range(m+1)),zero)==zero for k in range(m+1))
    # Quotient-algebra trace uses literal multiplication matrices, not Newton sums.
    def qm(a,b):return rem(mul(a,b),t)
    def qi(a):
        g,u,v=xgcd(a,t);assert g==[one];return rem(u,t)
    z=[zero,one]
    powers=[[one]]
    for k in range(1,2*m-1): powers.append(qm(powers[-1],z))
    trace_basis=[sum(((powers[k+j]+[zero]*m)[j] for j in range(m)),zero) for k in range(m)]
    def trace(a):
        return sum((a[j]*trace_basis[j] for j in range(len(a))),zero)
    b=qm(qm(R,qi(z)),qi(deriv(t)))
    zn=[one]
    for _ in range(N):zn=qm(zn,z)
    closure=sub([one],zn); a=qm(closure,b); closure_inverse=qi(closure)
    xpow=[one];moments=[]
    for k in range(N):
        moments.append(trace(qm(b,xpow)));xpow=qm(xpow,z)
    assert moments==s
    ell=[trace(qm(a,[zero]*j+[one])) for j in range(m)]
    def functional(y):return sum((ell[j]*y[j] for j in range(len(y))),zero)
    def scan(x):
        y=[zero]
        for v in reversed(x):y=add(qm(z,y),[v])
        y0=qm(y,closure_inverse);out=[zero]*N;out[0]=functional(y0)+delta*x[0];y=y0
        for i in range(N-1,0,-1):
            y=add([x[i]],qm(z,y));out[i]=functional(y)+delta*x[i]
        return out
    inputs=[[one if i==j else zero for i in range(N)] for j in range(N)] if all_basis else [[zero+(i*i+3*i+7) for i in range(N)],[zero+(1 if i%3==0 else -2) for i in range(N)]]
    for x in inputs:
        actual=scan(x);expected=[sum((f[(j-i)%N]*x[j] for j in range(N)),zero) for i in range(N)]
        assert actual==expected
    return {'N':N,'minimum':m,'delta':serialize(delta),'T':serialize(t),'shifted_numerator':serialize(R),'all_moments_checked':N,'all_basis_vectors':all_basis,'scan_inputs':len(inputs),'scan_entry_comparisons':len(inputs)*N,'squarefree_gcd_degree':0,'resonance_gcd_degree':0}

def hermite_discriminant_controls():
    # Independent direct integer polynomial resultant using exact rational elimination.
    rows=[]
    for n in range(1,13):
        a=[Fraction(1)];b=[Fraction(0),Fraction(1)]
        for k in range(2,n+1):a,b=b,sub([Fraction(0)]+b,scale(a,Fraction(k-1)))
        H=a if n==0 else b
        D=deriv(H);size=(len(H)-1)+(len(D)-1)
        mat=[]
        for shift in range(len(D)-1):mat.append([Fraction(0)]*shift+list(reversed(H))+[Fraction(0)]*(size-shift-len(H)))
        for shift in range(len(H)-1):mat.append([Fraction(0)]*shift+list(reversed(D))+[Fraction(0)]*(size-shift-len(D)))
        det=Fraction(1)
        for i in range(size):
            pivot=next(j for j in range(i,size) if mat[j][i])
            if pivot!=i:mat[i],mat[pivot]=mat[pivot],mat[i];det=-det
            c=mat[i][i];det*=c
            for j in range(i+1,size):
                v=mat[j][i]/c
                for k in range(i+1,size):mat[j][k]-=v*mat[i][k]
        disc=(-1)**(n*(n-1)//2)*det;want=math.prod(j**j for j in range(1,n+1))
        assert disc==want
        rows.append({'degree':n,'discriminant':str(disc)})
    return rows

def main():
    start=time.time();certs=modular_certificates(1001)
    (OUT/'MODULAR_CERTIFICATES.json').write_text(json.dumps(certs,indent=2)+'\n')
    print('Certified all',len(certs),'sizes N=1 mod 4 in [5,1001]',flush=True)
    banks=[]
    for N in [5,9,13,17,21,25,45,65,245]:
        c=next(c for c in certs if c['N']==N);Fp.p=c['prime_p']
        for sign in [1,-1]:
            row=bank_control(N,Fp(c['primitive_q'])**sign,all_basis=N<=25);row.update(field='F'+str(Fp.p),sign=sign);banks.append(row)
        print('Finite bank',N,'passed',flush=True)
    for N in [3,5,7,9]:
        Cyc.modulus=cyclotomic(N)
        for sign in [1,-1]:
            row=bank_control(N,Cyc([0,1])**sign);row.update(field='Q(zeta_'+str(N)+')',sign=sign);banks.append(row)
        print('Characteristic-zero',N,'passed',flush=True)
    results={'modular_certificates':len(certs),'largest_N':1001,'failed_final_guards':0,'extra_prime_trials':sum(len(c['trials'])-1 for c in certs),'bad_reductions':[{'N':c['N'],'trial':t} for c in certs for t in c['trials'][:-1]],'bank_controls':banks,'hermite_discriminants':hermite_discriminant_controls(),'elapsed_seconds':time.time()-start}
    (OUT/'CHECK_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print('All exact controls passed in',round(time.time()-start,2),'seconds',flush=True)

if __name__=='__main__':main()
