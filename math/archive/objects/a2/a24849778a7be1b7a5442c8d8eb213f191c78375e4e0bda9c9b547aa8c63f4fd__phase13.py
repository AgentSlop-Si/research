"""Exact prime-field checks for Hero #17 Phase 13. This is NOT an O(N) DFT.
F[i,j] = omega**(i*j); S e_j=e_(j+1); T e_j=omega**j e_j.
"""
from math import gcd,isqrt
from dataclasses import dataclass

def primes_of(n):
    out=[]; d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0:n//=d
        d+=1
    if n>1:out.append(n)
    return out

def isprime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))

def omega_root(n,p):
    if (p-1)%n or not isprime(p):raise ValueError('Require p prime and n|(p-1)')
    for g in range(2,p):
        w=pow(g,(p-1)//n,p)
        if w!=1 and all(pow(w,n//d,p)!=1 for d in primes_of(n)):return w
    raise ValueError('No root')

def rank(A,p):
    m=[list(row) for row in A]
    if not m:return 0
    rows=len(m); cols=len(m[0]); r=0
    for j in range(cols):
        k=next((i for i in range(r,rows) if m[i][j]%p),None)
        if k is None:continue
        m[r],m[k]=m[k],m[r]
        z=pow(m[r][j],-1,p);m[r]=[t*z%p for t in m[r]]
        for i in range(r+1,rows):
            if m[i][j]:
                t=m[i][j];m[i]=[(a-t*b)%p for a,b in zip(m[i],m[r])]
        r+=1
        if r==rows:break
    return r

def inverse(A,p):
    n=len(A)
    x=[[z%p for z in row]+[int(i==j) for j in range(n)]for i,row in enumerate(A)]
    for j in range(n):
        k=next((i for i in range(j,n) if x[i][j]),None)
        if k is None:return None
        x[j],x[k]=x[k],x[j]
        z=pow(x[j][j],-1,p);x[j]=[t*z%p for t in x[j]]
        for i in range(n):
            if i!=j and x[i][j]:
                t=x[i][j];x[i]=[(a-t*b)%p for a,b in zip(x[i],x[j])]
    return [r[n:] for r in x]

def fourier(n,w,p):
    return [[pow(w,i*j%n,p) for j in range(n)]for i in range(n)]

def gamma(n,w,p):
    return sum(pow(w,j*j%n,p) for j in range(n))*pow(n,-1,p)%p

def coeff_F(n,w,p):
    iv4=pow(4,-1,n);g=gamma(n,w,p)
    return [[g*pow(w,-iv4*(a-b)**2%n,p)%p for b in range(n)] for a in range(n)]

def coeff_trace(A,w,p):
    n=len(A);ivn=pow(n,-1,p)
    return [[ivn*sum(pow(w,-b*k%n,p)*A[(k+a)%n][k] for k in range(n))%p
             for b in range(n)]for a in range(n)]

def synth(C,w,p):
    n=len(C)
    return [[sum(C[(i-j)%n][b]*pow(w,b*j%n,p) for b in range(n))%p
             for j in range(n)]for i in range(n)]

def delta(n,u,v,r,s):
    D=(u*s-v*r)%n; dot=(u*r+v*s)%n
    return D,(D-dot)*pow(2,-1,n)%n

def rotated(n,w,p,u,v,r,s):
    D,z=delta(n,u,v,r,s)
    if gcd(D,n)!=1:raise ValueError('non-generating basis')
    iv2=pow(2,-1,n);iv4=pow(4,-1,n);G=gamma(n,w,p)
    aa=(u*u+v*v)%n;bb=(r*r+s*s)%n
    return [[G*pow(w,(-iv4*aa*i*i+iv2*u*v*i-iv4*bb*j*j+iv2*r*s*j+z*i*j)%n,p)%p
             for j in range(n)]for i in range(n)]

def rotated_direct(n,w,p,u,v,r,s):
    C=coeff_F(n,w,p);o=[]
    for i in range(n):
        row=[]
        for j in range(n):
            a=(u*i+r*j)%n;b=(v*i+s*j)%n
            phase=(u*v*i*(i-1)//2+r*s*j*(j-1)//2+v*r*i*j)%n
            row.append(C[a][b]*pow(w,-phase%n,p)%p)
        o.append(row)
    return o

def rotated_rank(n,u,v,r,s):
    D,z=delta(n,u,v,r,s)
    if gcd(D,n)!=1:raise ValueError('non-generating basis')
    return n//gcd(n,z)

def hankel(n,w,p,u,v,r,s):
    C=rotated(n,w,p,u,v,r,s);h=(n+1)//2
    return [[C[i+j][0] for j in range(h)]for i in range(h)]

def gs_matrix(n,a,p):
    den=(1-pow(a,n,p))%p
    if not den:raise ValueError('singular shift Green')
    inv=pow(den,-1,p)
    return [[inv*pow(a,(i-j)%n,p)%p for j in range(n)]for i in range(n)]

def gt_diag(n,b,w,p):
    return [pow((1-b*pow(w,j,p))%p,-1,p) for j in range(n)]

def branch_matrix(n,a,b,w,p):
    gs=gs_matrix(n,a,p);gt=gt_diag(n,b,w,p)
    return [[gs[i][j]*gt[j]%p for j in range(n)] for i in range(n)]

def sum_matrix(n,a,b,w,p):
    gs=gs_matrix(n,a,p);gt=gt_diag(n,b,w,p)
    return [[(gs[i][j]+(gt[j] if i==j else 0))%p for j in range(n)]for i in range(n)]

def matvec(A,x,p):
    return [sum(a*b for a,b in zip(row,x))%p for row in A]

@dataclass
class Cost:
    add:int=0
    mul:int=0
    inv:int=0
    @property
    def total(self):return self.add+self.mul+self.inv
    def json(self):return {'addition_subtraction':self.add,'multiplication':self.mul,'inversion':self.inv,'total_field_ops':self.total}

def gs_apply(x,a,p,c=None):
    """Cyclic recurrence (I-a*S)y=x; 1 inverse + O(N) operations."""
    n=len(x);c=c if c is not None else Cost()
    if n==0:return []
    acc=x[0]%p;power=a%p
    for k in range(n-1,0,-1):
        acc=(acc+power*x[k])%p;power=power*a%p
        c.add+=1;c.mul+=2
    den=(1-power)%p;c.add+=1
    if not den:raise ValueError('singular')
    y=[0]*n;y[0]=acc*pow(den,-1,p)%p;c.inv+=1;c.mul+=1
    for k in range(1,n):
        y[k]=(x[k]+a*y[k-1])%p;c.add+=1;c.mul+=1
    return y

def prepare_gt(n,b,w,p,c=None):
    c=c if c is not None else Cost()
    out=[];power=1
    for j in range(n):
        den=(1-b*power)%p;c.mul+=1;c.add+=1
        if not den:raise ValueError('singular modulation Green')
        out.append(pow(den,-1,p));c.inv+=1
        power=power*w%p;c.mul+=1
    return out

def branch_apply(x,a,b,w,p,c=None,diag=None):
    c=c if c is not None else Cost()
    if diag is None:diag=prepare_gt(len(x),b,w,p,c)
    first=[xx*dd%p for xx,dd in zip(x,diag)];c.mul+=len(x)
    return gs_apply(first,a,p,c)

def sum_apply(x,a,b,w,p,c=None,diag=None):
    c=c if c is not None else Cost()
    if diag is None:diag=prepare_gt(len(x),b,w,p,c)
    first=gs_apply(x,a,p,c)
    out=[]
    for y,xx,dd in zip(first,x,diag):
        out.append((y+xx*dd)%p);c.mul+=1;c.add+=1
    return out

def find_dense_inverse_witness(n,w,p,limit=70):
    for a in range(2,min(limit,p)):
        if pow(a,n,p)==1:continue
        for b in range(2,min(limit,p)):
            if pow(b,n,p)==1:continue
            H=sum_matrix(n,a,b,w,p)
            HI=inverse(H,p)
            if HI is not None and all(z!=0 for row in HI for z in row):
                return (a,b)
    return None

def prepare_gt_batch(n,b,w,p,c=None):
    """One field inversion, O(N) multiplies for all modulation denominators."""
    c=c if c is not None else Cost()
    power=1; den=[]; prefix=[1]
    for j in range(n):
        d=(1-b*power)%p; c.mul+=1;c.add+=1
        if not d:raise ValueError('singular modulation Green')
        den.append(d);prefix.append(prefix[-1]*d%p);c.mul+=1
        power=power*w%p;c.mul+=1
    running=pow(prefix[-1],-1,p);c.inv+=1
    output=[0]*n
    for j in range(n-1,-1,-1):
        output[j]=running*prefix[j]%p
        running=running*den[j]%p;c.mul+=2
    return output

def reverse_matrix(n,a,b,w,p):
    gs=gs_matrix(n,a,p);gt=gt_diag(n,b,w,p)
    return [[gt[i]*gs[i][j]%p for j in range(n)]for i in range(n)]

def reverse_apply(x,a,b,w,p,c=None,diag=None):
    c=c if c is not None else Cost()
    if diag is None:diag=prepare_gt_batch(len(x),b,w,p,c)
    ys=gs_apply(x,a,p,c)
    out=[yy*dd%p for yy,dd in zip(ys,diag)];c.mul+=len(x)
    return out

def triple_matrix(n,a,b,g,w,p):
    """(I-a*S)^-1 (I-b*T)^-1 (I-g*S)^-1 -- O(N) executor."""
    left=gs_matrix(n,a,p);right=gs_matrix(n,g,p);center=gt_diag(n,b,w,p)
    return [[sum(left[i][k]*center[k]*right[k][j] for k in range(n))%p
             for j in range(n)]for i in range(n)]

def triple_apply(x,a,b,g,w,p,c=None,diag=None):
    c=c if c is not None else Cost()
    if diag is None:diag=prepare_gt_batch(len(x),b,w,p,c)
    y=gs_apply(x,g,p,c)
    y=[v*d%p for v,d in zip(y,diag)];c.mul+=len(x)
    return gs_apply(y,a,p,c)
