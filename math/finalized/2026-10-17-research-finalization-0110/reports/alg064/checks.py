#!/usr/bin/env python3
"""New exact-rational transcription controls for the ALG-064 numerical contract.
No historical/source programs, network or non-standard packages are used.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import product
import json, math, random
from pathlib import Path

Z=(F(0),F(0)); O=(F(1),F(0))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def sub(a,b): return (a[0]-b[0],a[1]-b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def scale(a,b): return (a[0]*b,a[1]*b)
def nu(a): return abs(a[0])+abs(a[1])
def norm2(a): return a[0]*a[0]+a[1]*a[1]
def div(a,b):
    s=norm2(b); assert s
    return ((a[0]*b[0]+a[1]*b[1])/s,(a[1]*b[0]-a[0]*b[1])/s)
def real(a): return (F(a),F(0))
def rounded(a,p):
    q=1<<p
    def rr(x):
        t=x*q
        # Nearest, ties upward; each real component error <= 2^(-p-1).
        n=(2*t.numerator+t.denominator)//(2*t.denominator)
        return F(n,q)
    return (rr(a[0]),rr(a[1]))
def horner(a,z,p=None):
    y=Z
    for c in reversed(a):
        y=mul(y,z)
        if p is not None: y=rounded(y,p)
        y=add(y,c)
        if p is not None: y=rounded(y,p)
    return y

def pi_ball(bits):
    target=F(1,1<<(bits+8))
    def atan_inv(n):
        s=F(0); j=0
        while True:
            s += F((-1)**j,(2*j+1)*n**(2*j+1)); j+=1
            err=F(1,(2*j+1)*n**(2*j+1))
            if err<=target: return s,err
    a,ea=atan_inv(5); b,eb=atan_inv(239)
    v=16*a-4*b; e=16*ea+4*eb
    rv=rounded(real(v),bits+5)[0]
    return rv,e+abs(rv-v)

def trig_ball(a,bits,cosine):
    target=F(1,1<<(bits+6)); j=0; s=F(0)
    while True:
        k=2*j+(0 if cosine else 1)
        s += F((-1)**j)*a**k/F(math.factorial(k))
        nxt=k+2
        e=abs(a)**nxt/F(math.factorial(nxt))
        if e<=target: return s,e
        j+=1

@lru_cache(None)
def nodes(n,p):
    """Exact rational certificates to exp(2*pi*i*k/n), error <= 2^-p."""
    pi,pe=pi_ball(p+8); out=[]; rho=F(1,1<<p)
    for k in range(n):
        kk=k if 2*k<=n else k-n
        a=2*pi*kk/n; ae=2*abs(kk)*pe/n
        co,ce=trig_ball(a,p+8,True); si,se=trig_ball(a,p+8,False)
        z=rounded((co,si),p)
        er=abs(z[0]-co)+ce+ae; ei=abs(z[1]-si)+se+ae
        assert er*er+ei*ei<=rho*rho
        out.append(z)
    return tuple(out)

def boundary(x,c,L):
    n=len(x); P=[]; B=[]
    for j in range(L):
        a=Z; b=Z
        for i in range(j+1): a=add(a,mul(c[i],x[j-i]))
        for i in range(j+1,L+1): b=add(b,mul(c[i],x[n+j-i]))
        P.append(a); B.append(b)
    e=[]
    for j in range(L,n):
        a=Z
        for i in range(L+1): a=add(a,mul(c[i],x[j-i]))
        e.append(a)
    return P,B,e

def degree(c): return max(i for i,v in enumerate(c) if v!=Z)
def grid_bits(a):
    b=0
    for z in a:
        for v in z:
            d=v.denominator
            assert d&(d-1)==0
            b=max(b,d.bit_length()-1)
    return b

def precision(n,L,r,S,H,K,eps,b):
    tau=F(1,(2*n)**r); p=max(2*b,1)
    while True:
        rho=F(1,1<<p)
        eta_q=3*L*(H+2)*rho; eta_a=3*L*(K+2)*rho
        if (rho<=F(1,n) and eta_q<=min(tau/4,eps*tau/(8*(S+1)))
            and eta_a<=eps*tau/8 and 3*n*(S+2)*rho<=eps and rho<=eps/4):
            return p,tau,eta_q,eta_a
        p+=1

def evaluate(x,c,L,eps):
    n=len(x); P,B,e=boundary(x,c,L); A=[add(a,b) for a,b in zip(P,B)]
    S=sum(map(nu,x)); H=sum(map(nu,c)); K=sum(map(nu,A)); R=sum(map(nu,e))
    r=degree(c); b=grid_bits(x+c)
    p,tau,eq,ea=precision(n,L,r,S,H,K,eps,b)
    if R>eps*tau/8: return {'accepted':False,'R':R,'threshold':eps*tau/8}
    ns=nodes(n,p); y=[]; suspects=[]
    for k,z in enumerate(ns):
        qh=horner(c,z,p); ah=horner(A,z,p)
        if norm2(qh)<(3*tau/4)**2:
            suspects.append(k); y.append(horner(x,z,p))
        else:
            assert norm2(qh)>0
            y.append(rounded(div(ah,qh),p))
    assert len(suspects)<=r
    # Independent exact polynomial evaluation at a much sharper certified node.
    pref=p+20; nr=nodes(n,pref); rr=F(1,1<<pref)
    direct_rad=3*n*S*rr
    for z,out in zip(nr,y):
        direct=horner(x,z)
        assert direct_rad<eps
        assert norm2(sub(out,direct))<=(eps-direct_rad)**2
    # Check every denominator/evaluation radius against the sharper reference.
    qrad=3*max(r,1)*H*rr; arad=3*max(L,1)*K*rr
    for z,zr in zip(ns,nr):
        qh=horner(c,z,p); ah=horner(A,z,p)
        qref=horner(c,zr); aref=horner(A,zr)
        assert eq>qrad and ea>=arad
        assert norm2(sub(qh,qref))<=(eq-qrad)**2
        assert norm2(sub(ah,aref))<=(ea-arad)**2
    return {'accepted':True,'suspects':len(suspects),'p':p,'r':r,'outputs':n,'R_nonzero':R!=0}

def make_recurrence(n,c,initial,L):
    x=initial[:]
    for j in range(L,n):
        a=Z
        for i in range(1,L+1): a=add(a,mul(c[i],x[j-i]))
        x.append(scale(a,-1))
    return x

def identity_controls():
    count=0
    # Arbitrary data, not only recurrence data, with trailing-zero connections.
    rng=random.Random(64017)
    for n in range(2,15):
        for L in range(1,n):
            for _ in range(5):
                x=[(F(rng.randrange(-4,5),8),F(rng.randrange(-2,3),4)) for j in range(n)]
                c=[O]+[(F(rng.randrange(-3,4),4),F(rng.randrange(-1,2),2)) for i in range(L)]
                if count%3==0: c[-1]=Z
                P,B,e=boundary(x,c,L)
                lhs=[Z]*(n+L)
                for i,ci in enumerate(c):
                    for j,xj in enumerate(x): lhs[i+j]=add(lhs[i+j],mul(ci,xj))
                rhs=P+e+B
                assert lhs==rhs
                count+=1
    return count

def exact_threshold_controls():
    # N=2,4 roots are Gaussian rationals: no transcendental approximation here.
    count=0; sharp=0
    for n,ns in [(2,[O,real(-1)]),(4,[O,(F(0),F(1)),real(-1),(F(0),F(-1))])]:
        for r in range(0,4):
            for tail in product(range(-2,3),repeat=r):
                c=[O]+[real(v) for v in tail]
                rr=degree(c); tau=F(1,(2*n)**rr)
                small=sum(norm2(horner(c,z))<tau*tau for z in ns)
                assert small<=rr
                sharp+=small==rr and rr>0
                count+=1
    return count,sharp

def run():
    result={'verdict':'PASS','program_provenance':'fresh standalone checker; no historical/source code run',
            'exact_defect_polynomial_identities':identity_controls()}
    a,b=exact_threshold_controls(); result['exact_gaussian_grid_threshold_cases']=a; result['sharp_threshold_controls']=b
    accepted=0; rejected=0; outputs=0; suspects=0; nonzero=0; ps=[]; cases=[]
    for n in [4,8,16,32]:
        cases.extend([
            (n,[O,real(-1)],[real(1)],1,'constant resonant'),
            (n,[O,real(1)],[real(1)],1,'alternating resonant'),
            (n,[O,real(-2),O],[real(1),real(2)],2,'repeated root affine'),
            (n,[O,Z,O],[real(1),real(2)],2,'quadratic repeated-grid roots'),
            (n,[O,Z,Z],[real(1),real(2)],2,'untapped span'),
            (n,[O,real(F(-1,2))],[real(1)],1,'dyadic geometric'),
            (n,[O,(F(0),F(-1))],[real(1)],1,'complex resonant'),
            (n,[O,real(-2),real(2)],[real(1),real(1)],2,'nonunit complex characteristic roots')])
    for n in [8,16,32]:
        cases.extend([
            (n,[O,Z,Z,Z,real(-1)],[real(1),real(2),real(-1),real(3)],4,'four distinct resonances'),
            (n,[O,real(-3),real(3),real(-1)],[real(1),real(2),real(5)],3,'triple root'),
            (n,[O,real(-1),Z,Z,Z],[real(1),real(-2),real(3),real(4)],4,'nonconstant untapped span')])
    rng=random.Random(64173)
    for _ in range(12):
        n=8 if _<6 else 16; L=3 if _%2 else 4
        c=[O]+[(F(rng.randrange(-2,3)),F(rng.randrange(-1,2))) for i in range(L)]
        initial=[real(rng.randrange(-3,4)) for i in range(L)]
        cases.append((n,c,initial,L,'random exact integer recurrence'))
    for n,c,initial,L,label in cases:
        x=make_recurrence(n,c,initial,L)
        d=evaluate(x,c,L,F(1,1<<16))
        assert d['accepted']; accepted+=1; outputs+=d['outputs']; suspects+=d['suspects']; ps.append(d['p'])
    # Near-unit dyadic root, exact recurrence, avoids exact resonance.
    for n in [4,8,16]:
        c=[O,real(-1+F(1,1<<18))]; x=make_recurrence(n,c,[real(1)],1)
        d=evaluate(x,c,1,F(1,1<<12)); assert d['accepted'] and d['suspects']==1
        accepted+=1; outputs+=d['outputs']; suspects+=d['suspects']; ps.append(d['p'])
    # Defect below the threshold is admitted; a late impulse above it is rejected.
    for n in [4,8,16,32]:
        x=[real(1)]*n; c=[O,real(-1)]; eps=F(1,1<<12); tau=F(1,2*n)
        x[-1]=add(x[-1],real(eps*tau/32))
        d=evaluate(x,c,1,eps); assert d['accepted'] and d['R_nonzero']
        accepted+=1; nonzero+=1; outputs+=d['outputs']; suspects+=d['suspects']; ps.append(d['p'])
        x[-1]=add(x[-1],real(1))
        d=evaluate(x,c,1,eps); assert not d['accepted']; rejected+=1
    # Branch-radius lemma with deliberately adversarial dyadic q perturbations.
    radius_cases=0
    for n,ns in [(2,[O,real(-1)]),(4,[O,(F(0),F(1)),real(-1),(F(0),F(-1))])]:
        for c in [[O,real(-1)],[O,Z,O],[O,real(-2),O],[O,Z,Z]]:
            r=degree(c); tau=F(1,(2*n)**r)
            for shift in [real(-tau/4),real(tau/4),(F(0),tau/4),Z]:
                qs=[add(horner(c,z),shift) for z in ns]
                bad=[j for j,q in enumerate(qs) if norm2(q)<(3*tau/4)**2]
                assert len(bad)<=r
                assert all(norm2(horner(c,ns[j]))<tau*tau for j in bad)
                radius_cases+=1
    result.update({'accepted_vectors':accepted,'all_output_error_checks':outputs,
                   'direct_suspect_bins':suspects,'accepted_nonzero_residual_vectors':nonzero,
                   'late_defect_rejections':rejected,'adversarial_classifier_radius_controls':radius_cases,
                   'minimum_working_fraction_bits':min(ps),'maximum_working_fraction_bits':max(ps),
                   'fourier_lengths':[4,8,16,32],
                   'node_certification':'Exact rational Machin arctangent intervals and sine/cosine Taylor remainder bounds; component radii squared <= 2^(-2p)',
                   'limitations':'Finite controls support the written all-size proof. Test root generator is not a production complexity claim.'})
    Path(__file__).with_name('CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__': run()
