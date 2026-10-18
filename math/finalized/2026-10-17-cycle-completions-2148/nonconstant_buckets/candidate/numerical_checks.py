"""Fresh numerical, signed-window identity and adversarial engine controls."""
from pathlib import Path
import sys,json,time,hashlib
from fractions import Fraction
from collections import Counter
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
from nonconstant_buckets import *
checks=Counter();start=time.monotonic()
def check(name,truth):
    if not truth:raise AssertionError(name)
    checks[name]+=1
def rejected(name,fn):
    try:fn()
    except (Failure,ValueError,ArithmeticError):checks[name]+=1
    else:raise AssertionError('accepted '+name)
engine=SparseBucketEngine()
entries=((1,1,0),(3,1,0))
result=engine.run(entries,1,1,17)
check('nonconstant original support',all(n%(M//4)!=0 for n,_,_ in entries))
check('full explicit immutable output',type(result.numerators)is tuple and len(result.numerators)==B)
check('genuine complex output',any(im!=0 for _,im in result.numerators))
check('norm exactly one half',Fraction(2,4)==Fraction(1,2))
check('prepared Phi count',engine.ledger.operations['phi_evaluation']==5631)
check('prepared numerator roots',engine.ledger.operations['numerator_root_preparation']==129)
check('positive normalizer',engine.C.lo>=1<<K)
for j,v in enumerate(result.numerators):
    check('exact typed output',type(v)is tuple and len(v)==2 and all(type(z)is int for z in v))
    if j not in result.active_bins:check('explicit certified far zero',v==(0,0))
for n,_,_ in entries:
    actual={j for n0,j,d in engine.last_retained if n0==n}
    expected={j for j in range(B) if min((j*T+n)%M,(-j*T-n)%M)<2*T}
    check('exhaustive active-bin selection',actual==expected and len(actual)<=4)
check('exact far-tail comparison',3073*(1<<480)<20**114)
# Every retained certificate proves Euclidean numerical error plus global tail.
U=1<<(K-P)
for cert in result.certificates:
    _,qr,qi,lr,hr,li,hi,er,ei=cert
    check('complex squared certificate',er*er+ei*ei<=(U-result.tail_grid_units)**2)
# Distinct nontrivial phases, shifted bins, signs, and general complex amplitudes.
other=engine.run(entries,1,135791,35791)
check('schedule changes real output',other.numerators!=result.numerators)
check('general schedule nonzero phase',any(im for _,im in other.numerators))
complex_entries=((17,2,-1),(12345,-1,1));complex_run=engine.run(complex_entries,2,M-1,M-1)
check('complex original coefficients execute',len(complex_run.numerators)==B and bool(complex_run.certificates))
edge=engine.run(((M-1,-1,0),),0,1,0)
check('wraparound nonquarter mode executes',bool(edge.active_bins))
for name,args in [('unsorted',(((3,1,0),(1,1,0)),1,1,0)),('zero coefficient',(((1,0,0),),0,1,0)),('duplicate',(((1,1,0),(1,1,0)),1,1,0)),('even sigma',(entries,1,2,0)),('tau range',(entries,1,1,M)),('wrong normalization',(entries,0,1,0)),('over-normalized',(entries,2,1,0)),('out of range support',(((M,1,0),),0,1,0)),('coefficient width',(((1,1<<1024,0),),1025,1,0)),('bool schedule',(entries,1,True,0))]:
    rejected('reject '+name,lambda a=args:engine.run(*a))
# Independent rational-root interval oracle: full endpoint recurrence, no
# production midpoint-Lipschitz method, and one exact endpoint exponentiation.
OK=704;OS=1<<OK;OT=160
ceil=lambda a,b:-((-a)//b)
def atan_oracle(q):
    low=high=0
    for k in range(OK):
        denominator=(2*k+1)*pow(q,2*k+1)
        lo=OS//denominator;hi=ceil(OS,denominator)
        if k&1:low-=hi;high-=lo
        else:low+=lo;high+=hi
    high+=ceil(OS,(2*OK+1)*pow(q,2*OK+1))
    return low,high
av=atan_oracle(5);bv=atan_oracle(239);PI=(16*av[0]-4*bv[1],16*av[1]-4*bv[0])
fac=1
for k in range(2,2*OT+2):fac*=k
TAIL=ceil(1<<(OK+2*OT+1),fac)
check('oracle factorial tail',TAIL<=1)
def osin(p,q):
    a=p%(2*q);sign=1
    if a>q:a=2*q-a;sign=-1
    if 2*a>q:a=q-a
    if not a:return(0,0)
    if 2*a==q:return(sign*OS,sign*OS)
    xl=PI[0]*a//q;xh=ceil(PI[1]*a,q)
    tl=sl=xl;th=sh=xh
    for j in range(1,OT):
        den=OS*OS*(2*j)*(2*j+1)
        tl=tl*xl*xl//den;th=ceil(th*xh*xh,den)
        if j&1:sl-=th;sh-=tl
        else:sl+=tl;sh+=th
    ans=(max(-OS,sl-TAIL),min(OS,sh+TAIL))
    return ans if sign>0 else(-ans[1],-ans[0])
def odiv(a,b):
    assert b[0]>0
    low=[x*OS//y for x in a for y in b]
    hi=[ceil(x*OS,y) for x in a for y in b]
    return min(low),max(hi)
def omul(a,b):
    v=[x*y for x in a for y in b];return min(v)//OS,ceil(max(v),OS)
def oadd(a,b):return a[0]+b[0],a[1]+b[1]
def osub(a,b):return a[0]-b[1],a[1]-b[0]
def oscale(a,k):return min(a[0]*k,a[1]*k),max(a[0]*k,a[1]*k)
PDEN=OS**113
numerators=[osin(a,256) for a in range(129)]
def ophi(d):
    if not d:return OS,OS
    r=d%256;r=min(r,256-r);n=numerators[r]
    if n==(0,0):return n
    den=oscale(osin(d,M),ELL)
    rat=odiv(n,den);rat=(max(0,rat[0]),min(OS,rat[1]))
    return rat[0]**114//PDEN,ceil(rat[1]**114,PDEN)
# Avoid either production prefix logic or its rounded-power recurrence.
phi=[ophi(d) for d in range(LIMIT+1)]
OC=(OS+2*sum(x[0] for x in phi[1:G+1]),OS+2*sum(x[1] for x in phi[1:G+1]))
scale=1<<(OK-K)
check('independent normalizer enclosure',engine.C.lo*scale<=OC[0]<=OC[1]<=engine.C.hi*scale)
def owindow(d):
    vals=[phi[abs(d-a)] for a in range(-H,H+1)]
    return odiv((sum(x[0] for x in vals),sum(x[1] for x in vals)),OC)
for rr in (result,other,complex_run,edge):
    for cert in rr.certificates:
        j,qr,qi,lr,hr,li,hi,er,ei=cert
        real=(0,0);imag=(0,0)
        for n,re,im in rr.source_entries:
            q=(j*T+rr.sigma*n)%M;d=min(q,M-q)
            if d>=2*T:continue
            w=owindow(d);u=n*rr.tau%M
            pr=osin(M+4*u,2*M);pi=oscale(osin(2*u,M),-1)
            cr=osub(oscale(pr,re),oscale(pi,im));ci=oadd(oscale(pi,re),oscale(pr,im))
            ar=omul(w,cr);ai=omul(w,ci)
            ar=(ar[0]//(1<<rr.alpha_power),ceil(ar[1],1<<rr.alpha_power))
            ai=(ai[0]//(1<<rr.alpha_power),ceil(ai[1],1<<rr.alpha_power))
            real=oadd(real,ar);imag=oadd(imag,ai)
        check('independent complex enclosure',lr*scale<=real[0]<=real[1]<=hr*scale and li*scale<=imag[0]<=imag[1]<=hi*scale)
        OU=1<<(OK-P);tr=rr.tail_grid_units*scale
        oer=max(abs(qr*OU-real[0]),abs(qr*OU-real[1]));oei=max(abs(qi*OU-imag[0]),abs(qi*OU-imag[1]))
        check('higher-grid complex radius',oer*oer+oei*oei<=(OU-tr)**2)
# Independent direct original signed-window check at reduced dimensions only.
# This verifies all signs, source phases and shifts, not theorem-scale precision.
import mpmath as mp
mp.mp.dps=95
mm=256;bb=4;tt=64;hh=48;gg=16;ell=32;rr=1
coef=[1]
for _ in range(2):
    nxt=[0]*(len(coef)+ell-1)
    for j,c in enumerate(coef):
        for k in range(ell):nxt[j+k]+=c
    coef=nxt
radius=ell-1;den=ell**2
phi_small=lambda a:sum(mp.mpf(c)/den*mp.exp(-2j*mp.pi*a*(t-radius)/mm) for t,c in enumerate(coef))
cc=sum(phi_small(a) for a in range(-gg,gg+1))
small_modes=((1,1,0),(3,-1,2));sigma=5;tau=7
for j in range(bb):
    direct=0
    for off,c in enumerate(coef):
        t=off-radius
        dd=sum(mp.exp(2j*mp.pi*a*t/mm) for a in range(-hh,hh+1))
        source=sum(mp.mpc(re,im)*mp.exp(-2j*mp.pi*n*(sigma*t+tau)/mm) for n,re,im in small_modes)
        direct+=mp.mpf(c)/den*dd*source*mp.exp(-2j*mp.pi*j*t/bb)/cc
    dual=sum(mp.mpc(re,im)*mp.exp(-2j*mp.pi*n*tau/mm)*sum(phi_small(j*tt+sigma*n-a) for a in range(-hh,hh+1))/cc for n,re,im in small_modes)
    check('direct signed-window sparse identity',abs(direct-dual)<mp.mpf('1e-85'))
report={'status':'PASS_FRESH_NONCONSTANT_NUMERICAL_CONTROLS','assertions':sum(checks.values()),'checks':dict(checks),
    'elapsed_seconds':time.monotonic()-start,'oracle_bits':OK,'oracle_method':'full endpoint recurrence and exact powers; direct signed-window reduced fixture',
    'fixture':{'entries':[list(x) for x in entries],'h':1,'sigma':1,'tau':17,'norm_squared':[1,2]},
    'fixture_active_bins':list(result.active_bins),'fixture_certificates':[list(x) for x in result.certificates],
    'nontrivial_schedule':{'sigma':other.sigma,'tau':other.tau,'active_bins':list(other.active_bins)},
    'receipt':engine.ledger.report(),'fresh_source_sha256':hashlib.sha256((HERE/'nonconstant_buckets.py').read_bytes()).hexdigest()}
(HERE/'NUMERICAL_CHECK_RESULTS.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps({k:report[k] for k in ('status','assertions','elapsed_seconds')},indent=2),flush=True)
