"""Fresh independent controls; never imports candidate or historical code.
All claimed certificate inequalities are integer/Fraction exact. mpmath only
proposes N=4 centers; exact rational certificates decide their validity.
"""
from fractions import Fraction as F
from math import comb
from pathlib import Path
import json, hashlib, time

OUT=Path(__file__).resolve().parents[1]/'evidence'
T0=time.time()

def ceildiv(a,b): return -((-a)//b)
def near(a,b): return (2*a+b)//(2*b)
def clog(n): return (n-1).bit_length()
def q_fixed(N,Q):
    M=Q+40; f=M+clog(M+1)+20; s=1<<f
    def atan(a):
        v=near(s,a); total=v
        for j in range(M-1):
            v=near(-v*(2*j+1),a*a*(2*j+3)); total+=v
        return total
    ph=16*atan(5)-4*atan(239); x=near(2*ph,N)
    v=s; cs=s; sn=0
    for j in range(1,M+1):
        v=near(v*x,s*j)
        if j%2==0: cs+=(-1 if j%4==2 else 1)*v
        else: sn+=(-1 if j%4==3 else 1)*v
    return (cs,sn),f

# Separate enclosure: direct arctangent terms, followed by outward interval
# Taylor terms. It does not use the candidate's recurrence error formulas.
def q_enclosure(N,P):
    s=1<<P; terms=(P+12)//4+2
    def atan(a):
        lo=hi=0; ap=a
        for j in range(terms):
            den=(2*j+1)*ap; l=s//den; u=ceildiv(s,den)
            if j%2: lo-=u; hi-=l
            else: lo+=l; hi+=u
            ap*=a*a
        tail=ceildiv(s,(2*terms+1)*ap)
        return lo-tail,hi+tail
    al,au=atan(5); bl,bu=atan(239)
    pl=16*al-4*bu; pu=16*au-4*bl
    xl=(2*pl)//N; xu=ceildiv(2*pu,N)
    assert 0<=xl<=xu<=2*s
    lo=hi=s; cslo=cshi=s; snlo=snhi=0
    M=P+16
    for j in range(1,M+1):
        lo=(lo*xl)//(s*j); hi=ceildiv(hi*xu,s*j)
        if j%2==0:
            if j%4==2: cslo-=hi; cshi-=lo
            else: cslo+=lo; cshi+=hi
        else:
            if j%4==3: snlo-=hi; snhi-=lo
            else: snlo+=lo; snhi+=hi
    # Integral remainder for exp(ix), |x|<=2. M>=17 ensures <=2^(5-M).
    tail=1 if P+5-M<0 else 1<<(P+5-M)
    return ((cslo-tail,cshi+tail),(snlo-tail,snhi+tail)),P

def imul(a,b,s):
    vals=[x*y for x in a for y in b]
    return min(vals)//s,ceildiv(max(vals),s)
def iadd(a,b):return a[0]+b[0],a[1]+b[1]
def isub(a,b):return a[0]-b[1],a[1]-b[0]
def cmul_i(a,b,s):
    return isub(imul(a[0],b[0],s),imul(a[1],b[1],s)),iadd(imul(a[0],b[1],s),imul(a[1],b[0],s))

def symbolic_B(N):
    h=N//2; m=h+1; L=10*N**3+2
    def P(n):
        rows=[{0:1}]
        for k in range(n):
            nxt=[{} for _ in range(len(rows)+1)]
            for j,row in enumerate(rows):
                for e,v in row.items():
                    nxt[j+1][e]=nxt[j+1].get(e,0)+v
                    nxt[j][e+k]=nxt[j].get(e+k,0)-v
            rows=nxt
        return [{e+n*(n-1)//2-j*(j-1)//2:v for e,v in row.items() if v} for j,row in enumerate(rows)]
    rows=[{} for _ in range(m+1)]
    for j,row in enumerate(P(h)):
        for e,v in row.items():rows[j+1][e]=rows[j+1].get(e,0)+v
    for j,row in enumerate(P(h-1)):
        for e,v in row.items():rows[j][e]=rows[j].get(e,0)+(v<<L)
    return [{e:v for e,v in row.items() if v} for row in rows]

def oracle(N,A):
    h=N//2;m=h+1;L=10*N**3+2;Rexp=L+N+1
    Q=A+clog(64*N*N)+Rexp+2
    fb=A+clog(128*m*N*N)+4
    (qr,qi),fq=q_fixed(N,Q); s=1<<fq
    out=[]; rows=symbolic_B(N)
    for row in rows:
        ar=ai=0
        for e in range(max(row),-1,-1):
            ar,ai=near(ar*qr-ai*qi,s),near(ar*qi+ai*qr,s)
            ar+=row.get(e,0)<<fb
        out.append((ar,ai))
    assert out[-1]==(1<<fb,0)
    return out,fb,rows,Q

def certify_oracle(N,A):
    vals,fb,rows,Q=oracle(N,A); P=Q+64+clog(Q+1)
    qi,_=q_enclosure(N,P);s=1<<P
    err=0
    for val,row in zip(vals,rows):
        z=((0,0),(0,0))
        for e in range(max(row),-1,-1):
            z=cmul_i(z,qi,s);v=row.get(e,0)*s
            z=((z[0][0]+v,z[0][1]+v),z[1])
        for v,iv in zip(val,z):
            lifted=v<<(P-fb)
            err+=max(abs(lifted-iv[0]),abs(lifted-iv[1]))
    assert err < 1<<(P-A-1),(N,A,err.bit_length(),P-A-1)
    return {'N':N,'A':A,'q_bits':Q,'proven_l1_error_below_bits':P-err.bit_length(),'X_degree':max(max(r) for r in rows),'coefficient_count':len(rows),'exact_leading_one':True}

# Gaussian rationals, independently written for local proof checks.
def g(a,b=0):return F(a),F(b)
def add(a,b):return a[0]+b[0],a[1]+b[1]
def neg(a):return -a[0],-a[1]
def sub(a,b):return add(a,neg(b))
def mul(a,b):return a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]
def scale(a,x):return a[0]*x,a[1]*x
def gp(a,k):
    v=g(1)
    for _ in range(k):v=mul(v,a)
    return v
def U(a):return abs(a[0])+abs(a[1])
def low(a):return max(abs(a[0]),abs(a[1]))
def normsq(a):return a[0]**2+a[1]**2

def poly_roots(roots):
    co=[g(1)]
    for r in roots:
        new=[g(0)]*(len(co)+1)
        for k,c in enumerate(co):
            new[k]=sub(new[k],mul(c,r));new[k+1]=add(new[k+1],c)
        co=new
    return co

def shift(co,w):
    # Derivative-sum formula, distinct from a triangular Taylor-shift routine.
    return [sum_g(scale(mul(co[j],gp(w,j-k)),comb(j,k)) for j in range(k,len(co))) for k in range(len(co))]
def sum_g(items):
    s=g(0)
    for a in items:s=add(s,a)
    return s

def rc(co,w,r,E):
    a=shift(co,w)
    lhs=U(a[0])+2*E+sum((U(a[k])+2*E)*r**k for k in range(2,len(a)))
    rhs=(low(a[1])-E)*r
    return lhs<rhs,lhs,rhs

def local_tests():
    roots=[g(1,F(1,2)),g(F(-3,2),2),g(2,-3)]
    co=poly_roots(roots); m=3;R=4;delta=F(1,4);d0=delta**2;A0=(4*R)**m
    r=F(1,1<<30);ec=d0*r/(256*m*A0);theta=d0*r/(4096*m*A0);E=theta*A0
    pert=co.copy();pert[0]=add(pert[0],g(theta/4,theta/4))
    ws=[add(a,g(ec/4,-ec/4)) for a in roots]
    positive=[rc(pert,w,r,E)[0] for w in ws]
    assert all(positive)
    assert all(normsq(sub(ws[i],ws[j]))>(2*r)**2 for i in range(m) for j in range(i))
    bad=[]
    for c,w,rr in [(co,g(0),r),(poly_roots([g(0),g(0),g(2)]),g(0),r),(co,roots[0],F(8))]:
        ok,*_=rc(c,w,rr,F(0));bad.append(not ok);assert not ok
    # Root labels preserved under deliberate order permutation and equal real parts.
    old=[g(1,0),g(1,2),g(-2,1)];new=[add(old[j],g(F(1,1<<20),F(-1,1<<20))) for j in [2,0,1]]
    matches=[[j for j,x in enumerate(old) if normsq(sub(w,x))<F(1,4)] for w in new]
    assert matches==[[2],[0],[1]]
    return {'positive_disks':len(positive),'negative_cases':len(bad),'label_permutation':[x[0] for x in matches]}

def floorlog(x):
    assert x>0
    k=x.numerator.bit_length()-x.denominator.bit_length()
    if k>=0:
        if x < (1<<k): k-=1
    elif x < F(1,1<<(-k)):k-=1
    return k

def actual_n4():
    import mpmath as mp
    N=4;m=3;p=3;L=642;t=1<<L;R=1<<(L+N+1)
    delta=F(1,(2*R)**(N*m*(m-1)));eta=F(1,(2*R**N)**(N*m));rho=eta/F((2*R)**(N-1))
    KV=m*(2*R/delta)**(m-1);W=m*KV;G=2*W*R**N;HV=m*m*(2*R)**(m-1)
    amin=F(1,R**(m-1));d0=delta**(m-1);A0=(4*R)**m;eps=F(1,1<<p)
    vg=eps*rho/(32*m);vb=vg/(16*(2*R)**N)
    bounds=[F(1,2),F(1,1<<(p+2)),amin/4,delta/16,rho/4,eta/(8*N*(2*R)**(N-1)),1/(8*KV*HV),vb/(16*KV*HV*W),vg/(8*W*N*(2*R)**(N-1)),eps*rho**2/(32*m*G),d0/(64*m*A0)]
    rexp=-floorlog(min(bounds));r=F(1,1<<rexp);ec=d0*r/(256*m*A0)
    kappa=-floorlog(ec)+4;P=kappa+32
    co=[g(-t),g(t-1),g(1,-1),g(1)]
    with mp.workprec(P+1024):
        def fun(z):return ((z+1-1j)*z+(t-1))*z-t
        def der(z):return (3*z+2-2j)*z+(t-1)
        ws=[];iters=[]
        for initial in [mp.mpc(1),mp.mpc(0,1<<321),mp.mpc(0,-(1<<321))]:
            z=initial
            for j in range(32):
                step=fun(z)/der(z);z-=step
                if abs(step)<mp.ldexp(1,-P):break
            else: raise AssertionError('Newton proposal failed')
            iters.append(j+1)
            ws.append((F(int(mp.nint(mp.re(z)*mp.ldexp(1,P))),1<<P),F(int(mp.nint(mp.im(z)*mp.ldexp(1,P))),1<<P)))
    theta=d0*r/(4096*m*A0);E=theta*A0
    results=[]
    for w in ws:
        ok,lhs,rhs=rc(co,w,r,E);assert ok
        assert normsq(w)>(amin/2)**2
        # Certified resolvent denominator directly; L is a lower modulus bound.
        denominator=add(g(1),gp(w,N));assert low(denominator)>=3*eta/4
        results.append({'strict_RC':ok,'denominator_lower_bound_verified':True,'margin_positive':rhs-lhs>0})
    assert all(normsq(sub(ws[i],ws[j]))>(2*r)**2 for i in range(m) for j in range(i))
    cert={'polynomial':'z^3+(1-i)z^2+(2^642-1)z-2^642','N':N,'p':p,'radius_exponent':rexp,'E_numerator_hex':hex(E.numerator),'E_denominator_hex':hex(E.denominator),'centers':[{'real_numerator_hex':hex(w[0].numerator),'real_denominator_exponent':w[0].denominator.bit_length()-1,'imag_numerator_hex':hex(w[1].numerator),'imag_denominator_exponent':w[1].denominator.bit_length()-1} for w in ws]}
    (OUT/'FULL_TOLERANCE_N4_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
    # Opposite-sign root is deliberately mislabeled: threshold rejects it.
    assert normsq(sub(ws[1],ws[2]))>(delta/2)**2
    return {'N':N,'p':p,'r_exponent':rexp,'kappa':kappa,'proposal_precision_bits':P,'newton_iterations':iters,'three_exact_RC_certificates':results,'pairwise_disjoint':True,'full_formal_downstream_tolerances_used':True}

def ledger():
    rows=[]
    for N in list(range(4,260,2))+[512,1000,10000]:
        m=N//2+1;ell=10*N**3+N+3;D=N*m*(m-1)*(ell+1);D0=(m-1)*D;J=m*m*D
        assert D<=20*N**6 and D0<=20*N**7 and J<=20*N**8
        for p in [1,97,10**7]:
            K=p+N**7;A=N*K
            assert N**7*K*K<=A**3
            assert N**3*A*A<=A**3
            assert N**9*K*K<=A**3
        rows.append({'N':N,'D':D,'D0':D0,'J_upper':J})
    return {'lengths':len(rows),'precision_values_per_length':3,'last':rows[-1],'all_domination_checks':True}

if __name__=='__main__':
    qcases=[]
    for N in [4,6,10,32,128,10000]:
        for Q in [1,8,33,128,257]:
            val,f=q_fixed(N,Q);P=f+64;box,_=q_enclosure(N,P);error=0
            for v,(lo,hi) in zip(val,box):
                v<<=P-f;error+=max(abs(v-lo),abs(v-hi))
            assert error<1<<(P-Q)
            qcases.append({'N':N,'Q':Q,'proved_error_below_bits':P-error.bit_length()})
    print('Unit-root exact interval checks:',len(qcases),flush=True)
    ocases=[]
    for N in [4,6,8,10]:
        for A in [12,128]:
            ocases.append(certify_oracle(N,A));print('Oracle certified',N,A,flush=True)
    local=local_tests(); print('Generic certificate checks passed',flush=True)
    actual=actual_n4();print('Full-tolerance N=4 disks certified',flush=True)
    results={'status':'PASS','unit_root_enclosures':qcases,'coefficient_oracle_enclosures':ocases,'local_certificates':local,'actual_N4':actual,'precision_ledger':ledger(),'historical_or_candidate_code_executed':False,'MSW_engine_implemented':False,'seconds':time.time()-T0}
    OUT.mkdir(exist_ok=True);(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({k:v for k,v in results.items() if k not in ['unit_root_enclosures','coefficient_oracle_enclosures']},indent=2))
