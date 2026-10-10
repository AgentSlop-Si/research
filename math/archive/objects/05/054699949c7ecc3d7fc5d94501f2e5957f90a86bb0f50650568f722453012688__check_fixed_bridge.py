"""Independent integer fixed-point Green bridge and a-posteriori certificates.
No uploaded code is imported. mpmath is used ONLY for external DFT/test oracles.
"""
from fractions import Fraction as F
import math,json,random
import mpmath as mp
mp.mp.dps=100

def rnd(a,b):
    assert b>0
    return (a+b//2)//b if a>=0 else -((-a+b//2)//b)
def add(a,b):return (a[0]+b[0],a[1]+b[1])
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def conj(a):return (a[0],-a[1])
def rawmul(a,b):return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def mul(a,b,Q):
    x,y=rawmul(a,b);return (rnd(x,Q),rnd(y,Q))
def scale(a,s,Q):return (rnd(a[0]*s,Q),rnd(a[1]*s,Q))
def div(a,s,Q):return (rnd(a[0]*Q,s),rnd(a[1]*Q,s))
def mass(a):return sum(abs(z[0])+abs(z[1]) for z in a)
def boxmax(a):return max((abs(z[0])+abs(z[1]) for z in a),default=0)
def roots(N,p):
    Q=1<<p; L=p+10; guard=(p+1).bit_length()+20;G=Q<<guard
    def atan(d):
        total=0; power=d;k=0
        while power*(2*k+1)<=G:
            v=G//(power*(2*k+1));total+=v if k%2==0 else -v
            power*=d*d;k+=1
        return total
    pi=16*atan(5)-4*atan(239);x=rnd(2*pi,N)
    ct=G;st=x;c=ct;s=st
    for k in range(L):
        ct=-rnd(ct*x*x,G*G*(2*k+1)*(2*k+2))
        st=-rnd(st*x*x,G*G*(2*k+2)*(2*k+3))
        c+=ct;s+=st
    root=(rnd(c,G//Q),rnd(s,G//Q))
    out=[(Q,0)]
    for _ in range(1,N):out.append(mul(out[-1],root,Q))
    return out,F(8*N,Q)
def solve_source(x,a,Q):
    coeff=[];prev=0
    for i in range(len(x)):
        prev=rnd(Q*Q,a*Q-prev);coeff.append(prev)
    beta=[];prev=(0,0)
    for v,c in zip(x,coeff):prev=scale(add(v,prev),c,Q);beta.append(prev)
    z=beta[:]
    for i in range(len(x)-2,-1,-1):z[i]=add(beta[i],scale(z[i+1],coeff[i],Q))
    return z

def tridiag(z,a):
    out=[]
    for i,v in enumerate(z):
        r=(a*v[0],a*v[1])
        if i:r=sub(r,z[i-1])
        if i+1<len(z):r=sub(r,z[i+1])
        out.append(r)
    return out

def source(x,Q):
    z3=solve_source(x,3,Q);z4=solve_source(x,4,Q)
    r3=[sub(a,b) for a,b in zip(x,tridiag(z3,3))]
    r4=[sub(a,b) for a,b in zip(x,tridiag(z4,4))]
    return [add(a,b) for a,b in zip(z3,z4)],F(2*mass(r3)+mass(r4),2*Q)

def select(a,k):
    if len(a)<=5:return sorted(a)[k]
    med=[select(a[i:i+5],len(a[i:i+5])//2) for i in range(0,len(a),5)]
    pivot=select(med,len(med)//2)
    lo=[x for x in a if x<pivot];eq=[x for x in a if x==pivot]
    if k<len(lo):return select(lo,k)
    if k<len(lo)+len(eq):return pivot
    hi=[x for x in a if x>pivot]
    return select(hi,k-len(lo)-len(eq))

def median_head(u):
    N=len(u);q=math.gcd(N,4);h=[None]*N
    for j in range(q):
        idx=list(range(j,N,q));m=len(idx)//2
        v=(select([u[k][0] for k in idx],m),select([u[k][1] for k in idx],m))
        for k in idx:h[k]=v
    return h,[sub(a,b) for a,b in zip(u,h)]

def head_transform(h):
    N=len(h);q=math.gcd(N,4);out=[(0,0)]*N
    rotations=[(1,0),(0,1),(-1,0),(0,-1)]
    for t in range(q):
        z=(0,0)
        for j in range(q):z=add(z,rawmul(h[j],rotations[(4*t*j//q)%4]))
        out[t*N//q]=(z[0]*(N//q),z[1]*(N//q))
    return out

def h_apply_exact(v,qs,Q):
    N=len(v);s=(sum(z[0] for z in v),sum(z[1] for z in v))
    t=(0,0)
    for a,b in zip(qs,v):t=add(t,rawmul(a,b))
    out=[];den=N*Q*Q
    for q,z in zip(qs,v):
        a=rawmul((3*Q-2*q[0],0),z);b=rawmul(conj(q),s)
        out.append((F(N*a[0]+t[0]+b[0],den),F(N*a[1]+t[1]+b[1],den)))
    return out

def solve_target(v,qs,Q):
    N=len(v);gs=[rnd(2*Q*Q,7*Q-4*q[0]) for q in qs]
    t=rnd(sum(gs),N)
    rp=rnd(2*Q+11*t,4);rm=rnd(2*Q+3*t,4)
    b0=(0,0);b1=(0,0)
    for q,g,z in zip(qs,gs,v):
        w=scale(z,g,Q);b1=add(b1,w);b0=add(b0,mul(q,w,Q))
    b0=(rnd(b0[0],N),rnd(b0[1],N));b1=(rnd(b1[0],N),rnd(b1[1],N))
    plus=div(add(b0,b1),2*rp,Q);minus=div(sub(b0,b1),2*rm,Q)
    a=add(plus,minus);b=sub(plus,minus)
    return [scale(sub(sub(z,a),mul(conj(q),b,Q)),g,Q) for z,q,g in zip(v,qs,gs)]

def target(v,qs,rho,Q):
    z=solve_target(v,qs,Q)
    hv=h_apply_exact(v,qs,Q);hz=h_apply_exact(z,qs,Q)
    residual=[];out=[]
    for vv,zz,hvv,hzz in zip(v,z,hv,hz):
        residual.append((F(vv[0],Q)-hzz[0]-F(zz[0],2*Q),F(vv[1],Q)-hzz[1]-F(zz[1],2*Q)))
        out.append((hvv[0]/2+F(vv[0],4*Q)-F(zz[0],8*Q),hvv[1]/2+F(vv[1],4*Q)-F(zz[1],8*Q)))
    rbox=boxmax(residual)
    tau=2*rho*F(boxmax(v),Q)+F(11,36)*(rbox+4*rho*F(boxmax(z),Q))
    return out,tau,rbox

def mpz(z):return mp.mpc(mp.mpf(z[0].numerator)/z[0].denominator,mp.mpf(z[1].numerator)/z[1].denominator)
def dft(x):
    N=len(x);w=mp.e**(2j*mp.pi/N)
    return [sum(x[j]*w**(j*k) for j in range(N)) for k in range(N)]
def qsolve(v,a):
    p=[];b=[]
    for i,x in enumerate(v):
        pp=F(a)-(1/p[-1] if i else 0);p.append(pp)
        b.append((F(x)+(b[-1] if i else 0))/pp)
    z=b[:]
    for i in range(len(v)-2,-1,-1):z[i]+=z[i+1]/p[i]
    return z

def run_case(x,p,eta=F(1,16),inject=True):
    N=len(x);Q=1<<p;qs,rho=roots(N,p);assert rho<=F(1,8)
    qerr=max(abs(mp.mpc(*q)/Q-mp.e**(2j*mp.pi*k/N)) for k,q in enumerate(qs));assert qerr<=float(rho)
    xg=[(int(a)*Q,int(b)*Q) for a,b in x]
    u,E=source(xg,Q);h,r=median_head(u);Mr=F(mass(r),Q)
    # ORACLE ONLY: instantiate an admissible decoder output with a known error.
    # The O(N) claim uses the previously proved packed-decoder interface instead.
    fr=dft([mp.mpc(*z)/Q for z in r]);bound=eta*Mr
    vh=head_transform(h);v=[]
    for k,(a,b) in enumerate(vh):
        bump=mp.mpf(bound.numerator)/bound.denominator/2 if inject else 0
        value=fr[k]+mp.mpc(a,b)/Q+((-1)**k)*bump
        v.append((int(mp.nint(value.real*Q)),int(mp.nint(value.imag*Q))))
    out,tau,rbox=target(v,qs,rho,Q)
    ev=F(2,Q) # certified decoder-to-fixed-point rounding; conservatively two components
    certificate=F(73,18)*(eta*Mr+E+ev)+tau
    truth=dft([mp.mpc(a,b) for a,b in x]);err=max(abs(mpz(y)-t) for y,t in zip(out,truth))
    assert err<=mp.mpf(certificate.numerator)/certificate.denominator
    # Check source residual certificate against an independent exact rational solve.
    for c in range(2):
        exact=[a+b for a,b in zip(qsolve([z[c] for z in x],3),qsolve([z[c] for z in x],4))]
        # Combined component bound checked below.
        if c==0:actual_E=sum(abs(F(u[i][c],Q)-exact[i]) for i in range(N))
        else:actual_E+=sum(abs(F(u[i][c],Q)-exact[i]) for i in range(N))
    assert actual_E<=E
    _,r0=median_head(xg);M0=F(mass(r0),Q)
    return dict(N=N,p=p,residual_mass=float(Mr),original_periodic_residual_mass=float(M0),source_certificate=float(E),source_actual_error=float(actual_E),target_certificate=float(tau),target_residual=float(rbox),root_error=float(qerr),root_bound=float(rho),total_certificate=float(certificate),observed_error=float(err),original_median_certificate=float(eta*M0),certificate_ratio=float(certificate/(eta*M0)) if M0 else None)

def target_only(N,p):
    Q=1<<p;qs,rho=roots(N,p)
    vv=[(j*j-7*j+3,4*j-2) for j in range(N)]
    v=[(a*Q,b*Q) for a,b in vv];out,tau,_=target(v,qs,rho,Q)
    # Independent conjugacy oracle, never used by the executor.
    inv=[z/N for z in dft([mp.mpc(*vv[(-j)%N]) for j in range(N)])]
    alpha=[];beta=[]
    for i,x in enumerate(inv):
        a=1/(mp.mpf('3.5')-(alpha[-1] if i else 0));alpha.append(a)
        beta.append(a*(x+(beta[-1] if i else 0)))
    z=beta[:]
    for j in range(N-2,-1,-1):z[j]+=alpha[j]*z[j+1]
    ss=[]
    for j,x in enumerate(inv):
        t=3*x-(inv[j-1] if j else 0)-(inv[j+1] if j+1<N else 0)
        ss.append(t/2+x/4-z[j]/8)
    truth=dft(ss);err=max(abs(mpz(a)-b) for a,b in zip(out,truth))
    assert err<=mp.mpf(tau.numerator)/tau.denominator,(N,p,err,tau)
    return dict(N=N,p=p,target_error=float(err),target_certificate=float(tau))

def main():
    rng=random.Random(1252);rows=[]
    for N in (4,8,16,32,64):
        for p in (32,48,64):
            rows.append(run_case([(rng.randint(-20,20),rng.randint(-20,20)) for _ in range(N)],p))
    # Integer, dense, near-Green-periodic family, fresh at each length.
    structured=[]
    for N in (8,16,32,64,128):
        A=1<<20;v=[F(1)]*N;tv=tridiag([(1,0)]*N,3)
        resolvent=qsolve(v,F(7,2))
        xx=[F(tv[i][0],2)+F(1,4)-resolvent[i]/8 for i in range(N)]
        x=[(rnd((A*z).numerator,(A*z).denominator),0) for z in xx]
        structured.append(run_case(x,64))
    zero=run_case([(0,0)]*16,48,inject=False)
    isolated=[target_only(N,p) for N in (4,8,16,32) for p in (32,48,64)]
    report={'scope':'Integer fixed-point source/target executors and exact a-posteriori certificates; direct DFT is a test-only decoder oracle, not the claimed runtime.','random_cases':rows,'near_green_periodic':structured,'zero_control':zero,'isolated_target_checks':isolated,'passed':len(rows)+len(structured)+len(isolated)+1}
    print(json.dumps(report,indent=2));open(__file__.replace('check_fixed_bridge.py','results.json'),'w').write(json.dumps(report,indent=2)+'\n')
if __name__=='__main__':main()
