#!/usr/bin/env python3
"""Fresh ALG-064 exact-discovery/dyadic-interface reference. Standard library only.
No historical project imports, network or external writes. See REPORT.md.
"""
from fractions import Fraction as F
from math import factorial

ZERO=(F(0),F(0)); ONE=(F(1),F(0))
def z(a=0,b=0): return (F(a),F(b))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def neg(a): return (-a[0],-a[1])
def sub(a,b): return add(a,neg(b))
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def div(a,b):
    d=b[0]*b[0]+b[1]*b[1]
    if not d: raise ZeroDivisionError
    return ((a[0]*b[0]+a[1]*b[1])/d,(a[1]*b[0]-a[0]*b[1])/d)
def nu(a): return abs(a[0])+abs(a[1])
def sq(a): return a[0]*a[0]+a[1]*a[1]
def rnd(a,p):
    def one(v):
        u=v*(1<<p); k=(2*u.numerator+u.denominator)//(2*u.denominator)
        return F(k,1<<p)
    return (one(a[0]),one(a[1]))
def height(v): return max(abs(v.numerator).bit_length(),v.denominator.bit_length())
def dyadic_precision(x):
    b=0
    for t in x:
        for v in t:
            q=v.denominator
            if q&(q-1): raise ValueError('raw input must be dyadic')
            b=max(b,q.bit_length()-1)
    return b

def discover(x,d):
    """Exact real-block rational RREF. Fixed declared span d; free vars zero.
    Consistency is equivalent to some declared recurrence span <=d.
    Returned boundary span is always d, even when polynomial degree is smaller.
    All tail rows are paid.
    """
    n=len(x)
    if not 0<=d<n: raise ValueError('cap requires 0 <= d < N')
    if not d: return ([ONE] if all(t==ZERO for t in x) else None),{'rows':2*n,'cols':0,'rank':0,'rational_operations':0,'max_fraction_bits':1}
    rows=[]
    for j in range(d,n):
        rr=[]; ii=[]
        for i in range(1,d+1):
            a,b=x[j-i]; rr.extend((a,-b)); ii.extend((b,a))
        rows.extend((rr+[-x[j][0]],ii+[-x[j][1]]))
    # Clear the shared dyadic denominator before elimination.
    scale=1<<dyadic_precision(x)
    rows=[[v*scale for v in row] for row in rows]
    k=0; piv=[]; ops=0; bits=max([1]+[height(v) for row in rows for v in row])
    for col in range(2*d):
        pivot=next((i for i in range(k,len(rows)) if rows[i][col]),None)
        if pivot is None: continue
        rows[k],rows[pivot]=rows[pivot],rows[k]
        a=rows[k][col]
        rows[k]=[v/a for v in rows[k]]; ops+=2*d+1
        for i in range(len(rows)):
            if i==k or not rows[i][col]: continue
            a=rows[i][col]
            rows[i]=[u-a*v for u,v in zip(rows[i],rows[k])]; ops+=2*(2*d+1)
        bits=max(bits,max(height(v) for row in rows for v in row))
        piv.append(col); k+=1
        if k==len(rows): break
    receipt={'rows':len(rows),'cols':2*d,'rank':k,'rational_operations':ops,'max_fraction_bits':bits}
    if any(all(not v for v in row[:-1]) and row[-1] for row in rows): return None,receipt
    sol=[F(0)]*(2*d)
    for i,col in enumerate(piv): sol[col]=rows[i][-1]
    c=[ONE]+[(sol[2*i],sol[2*i+1]) for i in range(d)]
    assert all(sum_complex([mul(c[i],x[j-i]) for i in range(d+1)])==ZERO for j in range(d,n))
    return c,receipt

def sum_complex(xs):
    r=ZERO
    for a in xs: r=add(r,a)
    return r

def boundary(x,c):
    n=len(x); d=len(c)-1
    e=[sum_complex([mul(c[i],x[j-i]) for i in range(d+1)]) for j in range(d,n)]
    a=[add(sum_complex([mul(c[i],x[j-i]) for i in range(j+1)]),sum_complex([mul(c[i],x[n+j-i]) for i in range(j+1,d+1)])) for j in range(d)]
    return a,sum(map(nu,e),F(0))

def coefficient_bridge(x,c,eps):
    n=len(x); d=len(c)-1; s=sum(map(nu,x),F(0)); tau=F(1,(2*n)**d)
    b=dyadic_precision(x)
    while F(1,1<<b)>eps*tau/(8*d*(s+1)): b+=1
    ch=[ONE]+[rnd(v,b) for v in c[1:]]
    a,r=boundary(x,ch)
    assert r<=d*F(1,1<<b)*s<=eps*tau/8
    return ch,a,r,b,tau

def atan_series(q,target):
    total=F(0); j=0
    while True:
        total+=F((-1)**j,(2*j+1)*q**(2*j+1)); j+=1
        err=F(1,(2*j+1)*q**(2*j+1))
        if err<=target: return total,err,j

def nodes(n,p):
    """Certified positive DFT nodes. Independent Machin + Taylor per node.
    Radius is a proven l1 bound, hence also an absolute complex bound.
    """
    rho=F(1,1<<p)
    aa,ea,ma=atan_series(5,rho/1280)
    ab,eb,mb=atan_series(239,rho/1280)
    pi=16*aa-4*ab; q=p+4
    piq=rnd((pi,F(0)),p+8)[0]
    pie=16*ea+4*eb+abs(piq-pi)
    degree=0
    while F(4**(degree+1),factorial(degree+1))>rho/64: degree+=1
    rem=F(4**(degree+1),factorial(degree+1))
    out=[]; radii=[]
    for k in range(n):
        kk=k if 2*k<=n else k-n
        a=F(2*kk,n)*piq
        assert abs(a)<4
        cs=F(0); sn=F(0); term=F(1)
        for j in range(degree+1):
            if j%4==0: cs+=term
            elif j%4==1: sn+=term
            elif j%4==2: cs-=term
            else: sn-=term
            term=term*a/(j+1)
        value=rnd((cs,sn),q)
        rad=2*pie+2*rem+nu(sub(value,(cs,sn)))
        assert rad<=rho
        out.append(value); radii.append(rad)
    # Compress the potentially enormous exact radius to an outward dyadic bound.
    scaled=max(radii)*(1<<(p+8))
    radius_up=F((scaled.numerator+scaled.denominator-1)//scaled.denominator,1<<(p+8))
    assert radius_up<=rho
    return out,{'pi_terms':ma+mb,'taylor_degree':degree,'node_count':n,'rho':rho,'max_node_radius':radius_up,'grid_fraction_bits':q}

def horner(poly,t,p=None):
    v=ZERO
    for a in reversed(poly):
        v=mul(v,t)
        if p is not None: v=rnd(v,p)
        v=add(v,a)
        if p is not None: v=rnd(v,p)
    return v

def precision(x,c,a,b,tau,eps):
    n=len(x); d=len(c)-1
    s=sum(map(nu,x),F(0)); h=sum(map(nu,c),F(0)); k=sum(map(nu,a),F(0))
    p=max(2*b,1)
    while True:
        rho=F(1,1<<p)
        if (rho<=F(1,n) and 3*d*(h+2)*rho<=min(tau/4,eps*tau/(8*(s+1))) and 3*d*(k+2)*rho<=eps*tau/8 and 3*n*(s+2)*rho<=eps and rho<=eps/4): return p,s,h,k
        p+=1

def direct_fallback(x,eps,b,reason,discovery):
    n=len(x); s=sum(map(nu,x),F(0)); p=max(1,b)
    while F(1,1<<p)>min(F(1,n),eps/(3*n*(s+2))): p+=1
    tt,root=nodes(n,p)
    yy=[horner(x,t,p) for t in tt]
    return yy,{'branch':'certified_direct_fallback','reason':reason,'N':n,'cap':discovery.get('cap'),'p':p,'discovery':discovery,'roots':root,'certified_error':3*n*(s+2)*F(1,1<<p),'direct_bins':n,'direct_horner_pairs':n*n,'output_count':n}

def pipeline(x,d,eps=F(1,1<<12),supplied_coefficients=None):
    x=[z(*v) for v in x]; eps=F(eps); n=len(x)
    if not n: raise ValueError('empty vector')
    if not 0<eps<=1: raise ValueError('epsilon must be in (0,1]')
    if not isinstance(d,int) or not 0<=d<n: raise ValueError('cap requires 0 <= d < N')
    b=dyadic_precision(x)
    if n==1: return x,{'branch':'copy','N':1,'certified_error':F(0),'output_count':1}
    if supplied_coefficients is None:
        c,disc=discover(x,d)
    else:
        # Adversarial adapter test only, not the raw-input API's discovery path.
        c=[z(*v) for v in supplied_coefficients]
        if len(c)!=d+1 or c[0]!=ONE: raise ValueError('invalid coefficient shape/normalization')
        disc={'injected_for_control':True}
        _,r=boundary(x,c)
        if r: return direct_fallback(x,eps,b,'supplied exact coefficient verification failed',disc)
    disc['cap']=d
    if c is None: return direct_fallback(x,eps,b,'cap inconsistent',disc)
    if not d: return [ZERO]*n,{'branch':'zero','N':n,'cap':0,'discovery':disc,'certified_error':F(0),'output_count':n}
    ch,a,r,bc,tau=coefficient_bridge(x,c,eps)
    if r>eps*tau/8: return direct_fallback(x,eps,b,'rounded defect certificate failed',disc)
    p,s,h,k=precision(x,ch,a,bc,tau,eps); rho=F(1,1<<p)
    tt,root=nodes(n,p); out=[]; suspects=[]; bounds=[]
    eq=3*d*(h+2)*rho; ea=3*d*(k+2)*rho
    for idx,t in enumerate(tt):
        q=horner(ch,t,p); av=horner(a,t,p)
        if sq(q)<(3*tau/4)**2:
            out.append(horner(x,t,p)); suspects.append(idx); bounds.append(3*n*(s+2)*rho)
        else:
            out.append(rnd(div(av,q),p)); bounds.append((eq*s+ea+r)/(3*tau/4)+rho)
    rdegree=max(i for i,v in enumerate(ch) if v!=ZERO)
    assert len(suspects)<=rdegree<=d and max(bounds)<=eps
    return out,{'branch':'recurrence','N':n,'cap':d,'degree':rdegree,'p':p,'coefficient_fraction_bits':bc,'non_dyadic_exact_coefficients':sum(v.denominator&(v.denominator-1)!=0 for a in c for v in a),'rounded_defect':r,'tau':tau,'discovery':disc,'roots':root,'suspect_bins':suspects,'certified_error':max(bounds),'output_count':n,'direct_horner_pairs':n*len(suspects)}
