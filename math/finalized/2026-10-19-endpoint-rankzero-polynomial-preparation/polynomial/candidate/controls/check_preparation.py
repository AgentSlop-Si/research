#!/usr/bin/env python3
"""Fresh controls for the NF03 polynomial preparation continuation.
No historical implementation is imported or executed. MSW/Pan is not implemented.
"""
from fractions import Fraction as F
from math import factorial
from pathlib import Path
import hashlib, json, time
import mpmath as mp

HERE=Path(__file__).resolve().parents[1]
RESULT={"scope":"Original scalar/oracle/certificate/ledger controls; no MSW/Pan implementation or general timing claim", "tests":{}}

def ceil_log2(n):
    assert n>0
    return (n-1).bit_length()

def round_div(n,d):
    assert d>0
    s=-1 if n<0 else 1
    return s*((abs(n)+d//2)//d)

def unit_root(N,Q):
    M=Q+40; f=M+ceil_log2(M+1)+20; scale=1<<f
    def atan_sum(a):
        term=round_div(scale,a); total=0
        for j in range(M):
            total+=term
            if j+1<M:
                term=round_div(-term*(2*j+1),a*a*(2*j+3))
        return total
    pi_hat=16*atan_sum(5)-4*atan_sum(239)
    x=round_div(2*pi_hat,N)
    assert 0<=x<=2*scale
    term=scale; re=scale; im=0
    for j in range(1,M+1):
        term=round_div(term*x,scale*j)
        if j%4==0: re+=term
        if j%4==1: im+=term
        if j%4==2: re-=term
        if j%4==3: im-=term
    err=F(55*(M+1),scale)+F(20,1<<(4*M))+F(1,1<<(M-5))
    assert err<F(1,1<<Q)
    return (re,im,f,err)

def gadd(a,b): return (a[0]+b[0],a[1]+b[1])
def gsub(a,b): return (a[0]-b[0],a[1]-b[1])
def gmul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def gscale(a,s): return (a[0]*s,a[1]*s)
def gpow(a,n):
    r=(F(1),F(0))
    for _ in range(n): r=gmul(r,a)
    return r

def U(a): return abs(a[0])+abs(a[1])
def low(a): return max(abs(a[0]),abs(a[1]))

def P_symbolic(n):
    # z coefficient maps X exponents to integer coefficients.
    coeff=[{0:1}]
    for k in range(n):
        new=[{} for _ in range(len(coeff)+1)]
        for j,poly in enumerate(coeff):
            for e,c in poly.items():
                new[j][e+k]=new[j].get(e+k,0)-c
                new[j+1][e]=new[j+1].get(e,0)+c
        coeff=[{e:c for e,c in poly.items() if c} for poly in new]
    out=[]
    for j,poly in enumerate(coeff):
        phase=n*(n-1)//2-j*(j-1)//2
        assert phase>=0
        out.append({e+phase:c for e,c in poly.items()})
    assert max(e for poly in out for e in poly)<=n*(n-1)
    assert sum(abs(c) for poly in out for c in poly.values())<=1<<n
    return out

def B_symbolic(N):
    h=N//2; L=10*N**3+2; t=1<<L
    ph=P_symbolic(h); pg=P_symbolic(h-1)
    B=[{}]+[dict(x) for x in ph]
    for j,poly in enumerate(pg):
        for e,c in poly.items(): B[j][e]=B[j].get(e,0)+t*c
    B=[{e:c for e,c in poly.items() if c} for poly in B]
    assert B[-1]=={0:1}
    assert max(e for poly in B for e in poly)<=N*N
    assert sum(abs(c) for poly in B for c in poly.values())<=1<<(L+N)
    return B

def coefficient_oracle(N,A):
    m=N//2+1; L=10*N**3+2; rlog=L+N+1
    Q=A+rlog+ceil_log2(64*N*N)+2
    fB=A+ceil_log2(128*m*N*N)+4
    qr,qi,fq,qe=unit_root(N,Q)
    B=B_symbolic(N); out=[]
    for poly in B:
        ar=ai=0
        for e in range(max(poly),-1,-1):
            ar,ai=round_div(ar*qr-ai*qi,1<<fq),round_div(ar*qi+ai*qr,1<<fq)
            ar+=poly.get(e,0)<<fB
        out.append((F(ar,1<<fB),F(ai,1<<fB)))
    # Cruder proof budget with requested Q, independent of observed errors.
    budget=F(4*N*N,1<<(Q-rlog))+F(6*m*N*N,1<<fB)
    assert budget<F(1,1<<(A+1))
    return out,B,{"Q":Q,"fraction_bits":fB,"q_fraction_bits":fq,"budget":budget}

def mp_poly_eval(poly,q):
    value=mp.mpc(0)
    for e in range(max(poly),-1,-1): value=value*q+poly.get(e,0)
    return value

def taylor_coeff(coeff,w):
    # Horner shift, exact Gaussian rationals, low-degree coefficient list.
    shifted=[coeff[-1]]
    for c in reversed(coeff[:-1]):
        nxt=[(F(0),F(0)) for _ in range(len(shifted)+1)]
        for k,a in enumerate(shifted):
            nxt[k]=gadd(nxt[k],gmul(a,w))
            nxt[k+1]=gadd(nxt[k+1],a)
        nxt[0]=gadd(nxt[0],c)
        shifted=nxt
    return shifted

def certify(coeff,w,r,E=F(0)):
    a=taylor_coeff(coeff,w)
    left=U(a[0])+2*E
    rp=r*r
    for k in range(2,len(a)):
        left+=(U(a[k])+2*E)*rp; rp*=r
    right=(low(a[1])-E)*r
    return right>0 and left<right, right-left

def polynomial_from_roots(roots):
    p=[(F(1),F(0))]
    for a in roots:
        nxt=[(F(0),F(0)) for _ in range(len(p)+1)]
        for j,c in enumerate(p):
            nxt[j]=gsub(nxt[j],gmul(c,a)); nxt[j+1]=gadd(nxt[j+1],c)
        p=nxt
    return p

def independent_tests():
    scalar=[]
    for N in [4,6,8,10,14,32,66,130,256]:
        for Q in [1,8,32,128,192]:
            re,im,f,bound=unit_root(N,Q)
            with mp.workprec(Q+f+100):
                exact=mp.e**(2*mp.pi*mp.j/N)
                err=abs(mp.mpc(mp.mpf(re)/(1<<f),mp.mpf(im)/(1<<f))-exact)
                assert err<mp.mpf(1)/(1<<Q)
            if N==4:
                assert F(abs(re)+abs(im-(1<<f)),1<<f)<F(1,1<<Q)
            scalar.append({"N":N,"Q":Q,"fraction_bits":f})
    RESULT["tests"]["unit_root"]={"count":len(scalar),"cases":scalar,"rigor":"Exact rational error-budget checks for all; exact q=i L1 check for N=4; high-precision numerical corroboration elsewhere"}
    oracle=[]
    for N in [4,6,8,10]:
        for A in [16,64,128]:
            approx,B,meta=coefficient_oracle(N,A)
            with mp.workprec(meta['Q']+10*N**3+300):
                q=mp.e**(2*mp.pi*mp.j/N)
                total=mp.mpf(0)
                for a,poly in zip(approx,B):
                    ah=mp.mpc(mp.mpf(a[0].numerator)/a[0].denominator,mp.mpf(a[1].numerator)/a[1].denominator)
                    total+=abs(ah-mp_poly_eval(poly,q))
                assert total<mp.mpf(1)/(1<<A)
            if N==4:
                exact=[]
                for poly in B:
                    s=(F(0),F(0))
                    for e,c in poly.items():
                        s=gadd(s,gscale(gpow((F(0),F(1)),e),c))
                    exact.append(s)
                assert sum(U(gsub(a,b)) for a,b in zip(approx,exact))<F(1,1<<A)
            oracle.append({"N":N,"A":A,"q_bits":meta['Q'],"fraction_bits":meta['fraction_bits']})
    RESULT["tests"]["coefficient_oracle"]={"count":len(oracle),"cases":oracle,"rigor":"Exact symbolic height/degree/monicity and rational budgets; N=4 exact coefficients; other coefficient comparisons are numerical corroboration"}
    symbolic=[]
    for N in range(4,42,2):
        B=B_symbolic(N)
        symbolic.append({"N":N,"degree_z":len(B)-1,"degree_X":max(e for c in B for e in c)})
    RESULT["tests"]["symbolic_profiles"]={"count":len(symbolic),"cases":symbolic}
    roots=[(F(-2),F(1)),(F(1),F(0)),(F(3),F(-2))]
    coeff=polynomial_from_roots(roots); r=F(1,256); E=F(1,1<<30)
    centers=[gadd(a,(F(1,1<<18),F(-1,1<<19))) for a in roots]
    certs=[certify(coeff,w,r,E)[0] for w in centers]
    assert all(certs)
    assert not certify(coeff,(F(10),F(10)),r,E)[0]
    repeated=polynomial_from_roots([roots[0],roots[0],roots[2]])
    assert not certify(repeated,roots[0],r,E)[0]
    assert not certify(coeff,roots[1],F(64),E)[0]
    # Include full signed coefficient uncertainty, not only a zero error budget.
    theta=E/(128*(1+max(U(w) for w in centers))**3)
    pert=[gadd(c,(theta,-theta)) for c in coeff]
    for w in centers:
        at=taylor_coeff(coeff,w); ah=taylor_coeff(pert,w)
        assert max(U(gsub(a,b)) for a,b in zip(at,ah))<=E
        assert certify(pert,w,r,E)[0]
    RESULT["tests"]["rational_rouche"]={"positive_count":6,"negative_count":3,"all_passed":True}
    # Exact label matching, including equal exact real parts.
    label_roots=[(F(0),F(-2)),(F(0),F(3)),(F(5),F(1))]
    old=[gadd(a,(F(1,1024),F(-1,1024))) for a in label_roots]
    new=[gadd(label_roots[i],(F(-1,2048),F(1,2048))) for i in [2,0,1]]
    matched=[]
    for w in new:
        found=[j for j,a in enumerate(old) if sum(x*x for x in gsub(w,a))<F(1)]
        assert len(found)==1; matched.append(found[0])
    assert matched==[2,0,1]
    RESULT["tests"]["label_matching"]={"permutation":matched,"equal_real_part_case":True}
    # Same-family N=4: q=i gives exact integer Gaussian cubic.
    N=4; L=10*N**3+2; t=1<<L
    exact=[(F(-t),F(0)),(F(t-1),F(0)),(F(1),F(-1)),(F(1),F(0))]
    centers=[]
    with mp.workprec(1800):
        cm=[mp.mpc(a,b) for a,b in [(-t,0),(t-1,0),(1,-1),(1,0)]]
        seeds=[mp.mpc(1),mp.j*mp.sqrt(t),-mp.j*mp.sqrt(t)]
        for z in seeds:
            for _ in range(24):
                v=cm[3]; d=mp.mpc(0)
                for c in reversed(cm[:3]): d=d*z+v; v=v*z+c
                step=v/d; z-=step
                if abs(step)<mp.mpf(2)**-140: break
            scale=1<<100
            centers.append((F(int(mp.nint(z.real*scale)),scale),F(int(mp.nint(z.imag*scale)),scale)))
    r=F(1,1<<60)
    margins=[]
    for w in centers:
        ok,margin=certify(exact,w,r)
        assert ok; margins.append({"numerator_bits":margin.numerator.bit_length(),"denominator_bits":margin.denominator.bit_length()})
    for i in range(3):
        for j in range(i): assert sum(x*x for x in gsub(centers[i],centers[j]))>(2*r)**2
    RESULT["tests"]["actual_N4_disks"]={"m":3,"t_exponent":L,"radius_exponent":-60,"center_fraction_bits":100,"complete_by_degree_and_disjoint_certified_disks":True,"margin_bit_sizes":margins,"candidate_method":"Fresh multiprecision Newton only for this diagnostic; certificates exact Gaussian rational"}
    # Save exact replayable N4 certificates as numerator/denominator pairs.
    cert_json={"N":4,"t_exponent":L,"radius":[r.numerator,r.denominator],"centers":[[[x.numerator,x.denominator] for x in a] for a in centers]}
    (HERE/'evidence/N4_CERTIFICATES.json').write_text(json.dumps(cert_json,indent=2)+'\n')
    ledgers=[]
    for N in list(range(4,260,2))+[512,1024,10000]:
        m=N//2+1; ml=ceil_log2(m); nl=ceil_log2(N); L=10*N**3+2; R=L+N+1
        D=N*m*(m-1)*(1+R); eta=N*m*(1+N*R); rho=eta+(N-1)*(1+R)
        kv=ml+(m-1)*(1+R+D); wb=ml+kv; gb=1+wb+N*R
        hv=2*ml+(m-1)*(1+R); d0=(m-1)*D; a0=m*(R+2)
        for p in [1,53,1000,10**6]:
            vg=p+rho+5+ml; vb=vg+4+N*(1+R)
            rex=max(1,p+2,(m-1)*R+2,D+4,rho+2,eta+3+nl+(N-1)*(1+R),3+kv+hv,vb+4+kv+hv+wb,vg+3+wb+nl+(N-1)*(1+R),p+2*rho+5+ml+gb,d0+6+ml+a0)
            kappa=d0+rex+8+ml+a0+4
            J=m*m*D; engine=m**3+m*m*(L+N)+m*J+m*kappa
            precision=m*R+J+m*kappa
            assert kappa<=1000*(p+N**7)
            assert engine<=1000*(N**9+N*p)
            assert precision<=1000*(N**8+N*p)
            K=p+N**7; A=N*K
            assert A**3>=N**7*K*K
            ledgers.append({"N":N,"p":p,"kappa":kappa,"J_upper":J,"engine_proxy":engine,"coefficient_precision_proxy":precision})
    RESULT["tests"]["precision_ledgers"]={"count":len(ledgers),"max_N":10000,"max_p":10**6,"tested_envelopes":"kappa<=1000(p+N^7), engine proxy<=1000(N^9+Np), precision proxy<=1000(N^8+Np); finite checks only"}
    (HERE/'evidence/LEDGER_CASES.json').write_text(json.dumps(ledgers,indent=2)+'\n')

if __name__=='__main__':
    start=time.time(); independent_tests(); RESULT['all_passed']=True
    RESULT['elapsed_seconds']=round(time.time()-start,3)
    RESULT['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (HERE/'evidence/CHECK_RESULTS.json').write_text(json.dumps(RESULT,indent=2)+'\n')
    print(json.dumps({"all_passed":True,"test_groups":list(RESULT['tests']),"elapsed_seconds":RESULT['elapsed_seconds'],"script_sha256":RESULT['script_sha256']},indent=2))
