"""Fully charged exact GT15/CT15 finite-field Fourier prototypes.

The models are separated:
 - data arith: additions/subtractions and nontrivial constant multiplies;
 - cold setup: input-independent field arith for root, powers and Winograd constants;
 - integer/root-order validations and routing index calculations recorded separately.

The exact scalar coefficient kernels are reused, never recomputed per row.
"""
from dataclasses import dataclass
from crt15 import P,GENERATOR,Cost,factors

@dataclass
class Kernel3:
    v:int
    h:int

@dataclass
class Kernel5:
    ca:int
    cd:int
    h1:int
    h2_minus_h1:int
    h1_plus_h2:int

@dataclass
class Plan:
    n:int
    g:int
    p:int
    w:int
    roots_g:list
    roots_n:list|None
    roots15:list|None
    k3:Kernel3
    k5:Kernel5
    setup:Cost
    omega3:int
    omega5:int


def mul(a,b,p,c):
    c.muls+=1;return a*b%p

def add(a,b,p,c):
    c.adds+=1;return (a+b)%p

def sub(a,b,p,c):
    c.adds+=1;return (a-b)%p

def power(a,e,p,c):
    """Binary powering, with charged modular multiplication and squaring."""
    if e<0:raise ValueError('negative exponent')
    if e==0:return 1
    r=1
    while e:
        if e&1:r=mul(r,a,p,c)
        e//=2
        if e:a=mul(a,a,p,c)
    return r


def make_plan(n,p=P,gen=GENERATOR,mode='gt',root=None):
    if n%15:raise ValueError('15 divides N')
    g=n//15
    if g&(g-1):raise ValueError('G=N/15 must be power of two')
    if (p-1)%n:raise ValueError('unsupported prime length')
    c=Cost()
    if root is None:
        root=power(gen,(p-1)//n,p,c)
    if power(root,n,p,Cost())!=1 or any(power(root,n//q,p,Cost())==1 for q in factors(n)):
        raise ValueError('invalid primitive root')
    omega_g=power(root,15,p,c)
    omega15=power(root,g,p,c)
    rg=[1]*g
    for j in range(1,g):rg[j]=mul(rg[j-1],omega_g,p,c)
    omega3=power(omega15,5,p,c)
    omega5=power(omega15,3,p,c)
    inv2=(p+1)//2
    # DFT3 coefficients: v=(w+w^2)/2, h=(w-w^2)/2.
    w3sq=mul(omega3,omega3,p,c)
    v3=mul(add(omega3,w3sq,p,c),inv2,p,c)
    h3=mul(sub(omega3,w3sq,p,c),inv2,p,c)
    # DFT5 independent prepared cosine/sine combinations.
    w2=mul(omega5,omega5,p,c);w3=mul(w2,omega5,p,c);w4=mul(w3,omega5,p,c)
    c1=mul(add(omega5,w4,p,c),inv2,p,c)
    c2=mul(add(w2,w3,p,c),inv2,p,c)
    h1=mul(sub(omega5,w4,p,c),inv2,p,c)
    h2=mul(sub(w2,w3,p,c),inv2,p,c)
    ca=mul(add(c1,c2,p,c),inv2,p,c)
    cd=mul(sub(c1,c2,p,c),inv2,p,c)
    hm=sub(h2,h1,p,c);hp=add(h1,h2,p,c)
    root15=[1]*15
    if mode in ('ct','ctfull'):
        for j in range(1,15):root15[j]=mul(root15[j-1],omega15,p,c)
    else:root15=None
    roots_n=None
    if mode in ('ct','ctfull'):
        roots_n=[1]*n
        for j in range(1,n):roots_n[j]=mul(roots_n[j-1],root,p,c)
    if mode not in ('gt','ct','ctfull'):raise ValueError('invalid mode')
    return Plan(n,g,p,root,rg,roots_n,root15,Kernel3(v3,h3),Kernel5(ca,cd,h1,hm,hp),c,omega3,omega5)


def fft2(a,plan,c):
    n=len(a);p=plan.p
    if n==1:return [a[0]%p]
    assert n==plan.g and len(plan.roots_g)==n
    b=[x%p for x in a]
    h=n//2
    while h:
        step=n//(2*h)
        for k in range(0,n,2*h):
            for j in range(h):
                u=b[k+j];v=b[k+h+j]
                s=add(u,v,p,c);d=sub(u,v,p,c)
                if j:d=mul(d,plan.roots_g[j*step],p,c)
                b[k+j]=s;b[k+h+j]=d
                c.reads+=2;c.writes+=2
        h//=2
    t=n.bit_length()-1
    return [b[int(f'{i:0{t}b}'[::-1],2)] for i in range(n)]


def fft3(a,plan,c):
    p=plan.p;u,v,w=a
    s=add(v,w,p,c);d=sub(v,w,p,c)
    y0=add(u,s,p,c)
    mid=add(u,mul(plan.k3.v,s,p,c),p,c)
    h=mul(plan.k3.h,d,p,c)
    c.reads+=3;c.writes+=3
    return [y0,add(mid,h,p,c),sub(mid,h,p,c)]


def fft5(a,plan,c):
    p=plan.p;k=plan.k5;x0,x1,x2,x3,x4=a
    s1=add(x1,x4,p,c);s2=add(x2,x3,p,c)
    d1=sub(x1,x4,p,c);d2=sub(x2,x3,p,c)
    s=add(s1,s2,p,c);t=sub(s1,s2,p,c)
    mid=add(x0,mul(k.ca,s,p,c),p,c)
    v=mul(k.cd,t,p,c)
    e1=add(mid,v,p,c);e2=sub(mid,v,p,c)
    pair=add(d1,d2,p,c)
    k1=mul(k.h1,pair,p,c);k2=mul(k.h2_minus_h1,d2,p,c);k3=mul(k.h1_plus_h2,d1,p,c)
    o1=add(k1,k2,p,c);o2=sub(k3,k1,p,c)
    y0=add(x0,s,p,c)
    y1=add(e1,o1,p,c);y4=sub(e1,o1,p,c)
    y2=add(e2,o2,p,c);y3=sub(e2,o2,p,c)
    c.reads+=5;c.writes+=5
    return [y0,y1,y2,y3,y4]


def fft15_gt(a,plan,c):
    p=plan.p
    # CRT input: (3,5) and output: k=5 r +3 s.
    lines=[[a[(10*u+6*v)%15] for u in range(3)] for v in range(5)]
    vals=[fft3(v,plan,c) for v in lines]
    out=[0]*15
    for r in range(3):
        xx=fft5([vals[v][r] for v in range(5)],plan,c)
        for s in range(5):out[(5*r+3*s)%15]=xx[s]
    return out


def fft15_ct(a,plan,c):
    p=plan.p
    assert plan.roots15 is not None
    vals=[fft5([a[u+3*v] for v in range(5)],plan,c) for u in range(3)]
    out=[0]*15
    for q in range(5):
        xx=[vals[u][q] for u in range(3)]
        for u in (1,2):
            if q:xx[u]=mul(xx[u],plan.roots15[u*q],p,c)
        z=fft3(xx,plan,c)
        for r in range(3):out[q+5*r]=z[r]
    return out


def transform(a,plan,inner='gt'):
    n=len(a);g=plan.g;p=plan.p
    if n!=plan.n:raise ValueError('input length does not match plan')
    c=Cost()
    if inner not in ('gt','ct'):raise ValueError('inner mode')
    if plan.roots_n is None and inner=='ct':raise ValueError('CT codelet needs setup roots')
    out=[0]*n
    if plan.roots_n is None:  # Good-Thomas outer CRT map
        eg=15*pow(15,-1,g) if g>1 else 0
        e15=g*pow(g,-1,15)
        rows=[]
        for v in range(15):
            rows.append(fft2([a[(eg*u+e15*v)%n] for u in range(g)],plan,c))
        for r in range(g):
            xx=fft15_gt([rows[v][r] for v in range(15)],plan,c)
            for s in range(15):out[(15*r+g*s)%n]=xx[s]
    else:  # Cooley-Tukey outer, pay every nonidentity cross twiddle
        rows=[]
        for u in range(15):rows.append(fft2([a[u+15*v] for v in range(g)],plan,c))
        for q in range(g):
            xx=[rows[u][q] for u in range(15)]
            for u in range(1,15):
                if q:xx[u]=mul(xx[u],plan.roots_n[u*q],p,c)
            transformed=fft15_gt(xx,plan,c) if inner=='gt' else fft15_ct(xx,plan,c)
            for r in range(15):out[q+g*r]=transformed[r]
    # CRT and natural-order permutations move N inputs, N outputs; count separately
    c.reads+=n;c.writes+=n
    return out,c


def predicted(g,inner='gt',outer='gt'):
    t=g.bit_length()-1
    if (1<<t)!=g:raise ValueError('g must be dyadic')
    # core cost per length G dyadic, then G length15 Fourier codelets
    a=15*g*t+81*g
    m=15*(g*t//2-g+1)+25*g if g>1 else 25
    if inner=='ct':m+=8*g
    if outer=='ct':m+=14*(g-1)
    return a,m,a+m

if __name__=='__main__':
    import random
    for g in (1,2,4,8,16,32,64,128):
        n=15*g
        plans={m:make_plan(n,mode=m) for m in ('gt','ct')}
        x=[random.Random(n*230+j).randrange(P) for j in range(n)]
        a,ca=transform(x,plans['gt'])
        b,cb=transform(x,plans['ct'])
        d,cd=transform(x,plans['ct'],inner='ct')
        assert a==b==d
        assert (ca.adds,ca.muls,ca.total())==predicted(g)
        assert (cb.adds,cb.muls,cb.total())==predicted(g,outer='ct')
        assert (cd.adds,cd.muls,cd.total())==predicted(g,inner='ct',outer='ct')
        print(n,ca.total(),cb.total(),cd.total(),plans['gt'].setup.total(),plans['ct'].setup.total())
