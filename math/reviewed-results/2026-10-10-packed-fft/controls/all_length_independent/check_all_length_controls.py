"""Fresh independent mathematical falsification controls, 10 October 2026.
Uses only Python stdlib and no supplied research program. No implementation
benchmark or coefficient-certification claim. Integer FFT arithmetic is exact;
Decimal trigonometry supplies independently computed high-precision controls.
"""
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib, json, math, random, cmath
from pathlib import Path

BASE=Path(__file__).resolve().parent
D=Decimal

def arctan_inv(n):
    x=D(1)/n; x2=x*x; term=x; total=x; j=1
    while abs(term)>D('1e-90'):
        term=-term*x2; total+=term/(2*j+1); j+=1
    return total

def trig_turn(num,den):
    num%=den
    theta=2*PI*D(num)/D(den)
    if theta>PI: theta-=2*PI
    t2=theta*theta; ct=D(1); st=theta; c=ct; s=st; j=1
    while abs(ct)+abs(st)>D('1e-85'):
        ct=-ct*t2/D((2*j-1)*(2*j)); st=-st*t2/D((2*j)*(2*j+1))
        c+=ct; s+=st; j+=1
    return c,-s

def trunc(x,d):
    return x//d if x>=0 else -((-x)//d)

def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def add(a,b):return a[0]+b[0],a[1]+b[1]
def sub(a,b):return a[0]-b[0],a[1]-b[1]
def rnd(a,d):return trunc(a[0],d),trunc(a[1],d)
def dec(a,den):return D(a[0])/den,D(a[1])/den
def norm(a):return sum(x*x+y*y for x,y in a).sqrt()
def dmul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]

def circle(L,q):
    K=q+(L-1).bit_length()+10; C=1<<K
    root=trig_turn(1,L); seedden=16*C; seed=tuple(int(x*seedden) for x in root)
    assert norm([sub(dec(seed,seedden),root)])<D(1)/C
    seq=[(C,0)]
    for _ in range(1,L):seq.append(rnd(mul(seq[-1],seed),seedden))
    worst=max(norm([sub(dec(x,C),trig_turn(j,L))]) for j,x in enumerate(seq))
    assert worst<D(2)**(-q)/128
    return seq,C,worst

def fft(z,q,circ,C,inv=False):
    H=len(z); v=(H-1).bit_length(); z=list(z)
    for i in range(H):
        j=int(format(i,f'0{v}b')[::-1],2)
        if i<j:z[i],z[j]=z[j],z[i]
    sh=int((D(1)/D(2).sqrt())*C)
    for ell in range(1,v+1):
        L=1<<ell; half=L//2
        for base in range(0,H,L):
            for j in range(half):
                c=circ[j*(H//L)]
                if inv:c=c[0],-c[1]
                aa=tuple(x*C for x in z[base+j]); bb=mul(z[base+j+half],c)
                z[base+j]=rnd(tuple(x*sh for x in add(aa,bb)),C*C)
                z[base+j+half]=rnd(tuple(x*sh for x in sub(aa,bb)),C*C)
    return z

def dft(z):
    N=len(z); circle=[trig_turn(j,N) for j in range(N)]; scale=D(N).sqrt()
    out=[]
    for k in range(N):
        v=(D(0),D(0))
        for j,a in enumerate(z):v=add(v,dmul(a,circle[k*j%N]))
        out.append(tuple(x/scale for x in v))
    return out

def fallback_case(N,t,case):
    H=1<<((2*N-2).bit_length()); k=H.bit_length(); q=t+(H.bit_length()-1)+(k-1).bit_length()+13; U=1<<q
    ch,C,e1=circle(H,q); cn,F,e2=circle(2*N,q)
    if case==0:a=[(D('.5'),D(0))]+[(D(0),D(0))]*(N-1)
    elif case==1:a=[(D('.5') if j%2 else D('-.5'),D(0)) for j in range(N)]
    else:
        rg=random.Random(100*N+t); a=[(D(rg.randrange(-7,8))/16,D(rg.randrange(-7,8))/16) for _ in range(N)]
        a[0]=(D('.5'),D(0))
    ai=[tuple(int(x*U) for x in z) for z in a]
    ds=[cn[j*j%(2*N)] for j in range(N)]
    vv=[rnd(mul(x,d),F) for x,d in zip(ai,ds)]+[(0,0)]*(H-N)
    bh=[(0,0)]*H
    for j in range(-(N-1),N):
        b=cn[j*j%(2*N)]; bh[j%H]=rnd((b[0]*U,-b[1]*U),F)
    zz=fft(vv,q,ch,C); cc=fft(bh,q,ch,C)
    al=int((D(H)/N).sqrt()*C)
    lam=[rnd((x*al,y*al),C) for x,y in cc]
    ww=[rnd(mul(x,y),U) for x,y in zip(lam,zz)]
    ff=fft(ww,q,ch,C,True)
    yy=[rnd(mul(d,f),F) for d,f in zip(ds,ff)]
    err=norm([sub(dec(y,U),z) for y,z in zip(yy,dft(a))]); A=norm(a)
    budget=D(2048*k*H)/U
    assert err<=budget and err<=D(2)**(-t)*A
    return {'N':N,'t':t,'case':case,'relative_error':str(err/A),'bound_ratio':str(err/budget),'phase_ratio':str(max(e1,e2)*U)}

def identity_control(N):
    H=1<<((2*N-2).bit_length()); a=[(D((j*7)%11-5)/8,D((j*3)%7-3)/8) for j in range(N)]
    da=[trig_turn(j*j,2*N) for j in range(N)]
    va=[dmul(x,d) for x,d in zip(a,da)]+[(D(0),D(0))]*(H-N)
    bb=[(D(0),D(0))]*H
    for j in range(-(N-1),N):
        d=trig_turn(j*j,2*N); bb[j%H]=(d[0],-d[1])
    zv=dft(va); cv=dft(bb); alpha=(D(H)/N).sqrt()
    w=[tuple(v*alpha for v in dmul(z,c)) for z,c in zip(zv,cv)]
    wc=[(x,-y) for x,y in w]; fi=[(x,-y) for x,y in dft(wc)]
    yy=[dmul(d,f) for d,f in zip(da,fi)]
    err=norm([sub(x,y) for x,y in zip(yy,dft(a))])
    assert err<D('1e-70')
    return {'N':N,'identity_error':str(err)}

def interpolation_control(N,s):
    M=1<<((4*N-1).bit_length()); h=16*s+1; L=M//4; qq=M//(8*s)
    assert M>=16*s and 2*h+2<M
    c=(N-1)//2; aa=[complex(((j*7)%13-6)/16,((j*3)%11-5)/16) for j in range(N)]
    z=[sum(x*cmath.exp(-2j*math.pi*(j-c)*k/M) for j,x in enumerate(aa))/math.sqrt(M) for k in range(M)]
    target=[sum(x*cmath.exp(-2j*math.pi*j*l/N) for j,x in enumerate(aa))/math.sqrt(N) for l in range(N)]
    rows=[]; col=[0.0]*M; out=[]
    for l in range(N):
        retained={(l*M//N+j)%M for j in range(-h,h+2)}
        val=0j; tail=0.0
        for k in range(M):
            numer=(l*M-k*N)%(N*M)
            if 2*numer>N*M:numer-=N*M
            if numer==0:ker=(2*L+1)/M
            else:
                ang=math.pi*numer/(N*M); den=math.sin(ang)
                ker=math.sin((2*L+1)*ang)/(M*den)*(math.sin((2*qq+1)*ang)/((2*qq+1)*den))**s
            weight=math.sqrt(M/N)*ker; val+=weight*z[k]
            if k not in retained:tail+=abs(weight); col[k]+=abs(weight)
        out.append(cmath.exp(-2j*math.pi*c*l/N)*val); rows.append(tail)
    err=math.sqrt(sum(abs(x-y)**2 for x,y in zip(out,target)))
    size=math.sqrt(sum(abs(x)**2 for x in aa)); schur=math.sqrt(max(rows)*max(col)); claimed=12*4**(-s)
    assert err<1e-10*size and schur<=claimed
    return {'N':N,'s':s,'M':M,'relative_identity_error':err/size,'tail_schur':schur,'tail_bound':claimed}

def symbolic_budgets():
    count=0; max_budget_ratio=Fraction(0)
    for v in range(2,301):
        H=1<<v; k=v+1
        for t in range(2,v+2):
            q=t+v+(k-1).bit_length()+13; u=Fraction(1,1<<q); eps=Fraction(1,1<<t)
            assert 500*k*u<=1
            assert 2048*k*H*u<=eps/4
            assert 3*100*k+160*k+2<=500*k
            assert 500*k+16*k*4<=600*k
            assert 1200*k+2<=2048*k
            max_budget_ratio=max(max_budget_ratio,2048*k*H*u/eps); count+=1
    return {'cases':count,'max_absolute_budget_over_epsilon':str(max_budget_ratio)}

with localcontext() as ctx:
    ctx.prec=100
    PI=16*arctan_inv(5)-4*arctan_inv(239)
    idres=[identity_control(n) for n in [2,3,5,7,9,16,17,31]]
    numres=[fallback_case(n,t,c) for n in [2,3,5,8,9,17,31,33,65] for t in sorted(set([2,n.bit_length()])) for c in range(3)]
    results={'status':'passed','controls_kind':'fresh independent stdlib Decimal and exact integer arithmetic; falsification only','source_programs_executed':False,'identity':idres,'fallback':numres,'symbolic_budgets':symbolic_budgets(),'interpolation':[interpolation_control(n,s) for n,s in [(17,2),(31,2),(33,3),(137,18)]]}
    results['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (BASE/'CONTROL_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'status':results['status'],'identity_cases':len(idres),'fallback_cases':len(numres),'symbolic_cases':results['symbolic_budgets']['cases'],'interpolation_cases':len(results['interpolation']),'script_sha256':results['script_sha256']},indent=2))
