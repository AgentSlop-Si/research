#!/usr/bin/env python3
"""Fresh controls for the proved packed microkernels. No supplied programs imported.

Exact Python integers model bounded-word arithmetic only when the proved width
assertion is checked. mpmath references are numerical falsification, not certificates.
"""
from fractions import Fraction as F
from itertools import product
import json
import math
import random
import mpmath as mp
from pathlib import Path

RNG = random.Random(10102026)
COUNTS = {}
MAX_BITS = {"dense": 0, "chirp": 0}
MAX_RATIO = {"dense_local_over_u": 0.0, "chirp_local_over_u": 0.0,
             "dense_stage_over_budget": 0.0, "chirp_stage_over_budget": 0.0}

def ceil_log2(n):
    return (n - 1).bit_length()

def bump(name):
    COUNTS[name] = COUNTS.get(name, 0) + 1

def pack(vals, D):
    return sum(v << (D*j) for j, v in enumerate(vals))

def dense_real(C, x, Q):
    r = len(x)
    P = Q.bit_length()-1
    D = 2*P+ceil_log2(r)+3
    B = 1 << D
    assert 4*r*Q*Q < B
    assert all(abs(v) <= Q for row in C for v in row)
    assert all(abs(v) <= Q for v in x)
    cp = pack([v+Q for row in C for v in row], D)
    xp = pack([v+Q for v in x[::-1]], D)
    z = cp*xp
    assert z.bit_length() <= (r*r+r-1)*D
    MAX_BITS["dense"] = max(MAX_BITS["dense"], z.bit_length())
    # Check every convolution digit, including overlapping unselected bands.
    aa = [v+Q for row in C for v in row]
    xx = [v+Q for v in x[::-1]]
    for k in range(r*r+r-1):
        expected = sum(aa[j]*xx[k-j] for j in range(max(0,k-r+1), min(k,r*r-1)+1))
        assert expected < B
        assert ((z >> (D*k)) & (B-1)) == expected
    S = sum(x)
    y = [((z >> (D*((i+1)*r-1))) & (B-1)) - Q*sum(C[i]) - Q*S - r*Q*Q
         for i in range(r)]
    assert y == [sum(a*b for a,b in zip(row,x)) for row in C]
    return y

def dense_complex(C, x, Q):
    CR = [[v[0] for v in row] for row in C]
    CI = [[v[1] for v in row] for row in C]
    xr = [v[0] for v in x]
    xi = [v[1] for v in x]
    a,b,c,d = dense_real(CR,xr,Q),dense_real(CI,xi,Q),dense_real(CR,xi,Q),dense_real(CI,xr,Q)
    return [(a[i]-b[i],c[i]+d[i]) for i in range(len(x))]

def cmul(x,y):
    return x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0]

def cadd(x,y):
    return x[0]+y[0],x[1]+y[1]

def direct_complex(C,x):
    out=[]
    for row in C:
        z=(0,0)
        for a,b in zip(row,x): z=cadd(z,cmul(a,b))
        out.append(z)
    return out

def chirp_real(k, a, Q):
    r=len(a)
    assert len(k)==2*r-1
    V=2*Q*Q
    P=Q.bit_length()-1
    D=3*P+ceil_log2(r)+4
    B=1<<D
    assert 8*r*Q**3 < B
    assert all(abs(x)<=V for x in a)
    assert all(abs(x)<=Q for x in k)
    ap=pack([x+V for x in a],D)
    kp=pack([x+Q for x in k],D)
    z=ap*kp
    assert z.bit_length()<=(3*r-2)*D
    MAX_BITS["chirp"]=max(MAX_BITS["chirp"],z.bit_length())
    for t in range(3*r-2):
        expected=sum((a[j]+V)*(k[t-j]+Q) for j in range(r) if 0<=t-j<len(k))
        assert expected<B
        assert ((z>>(D*t))&(B-1))==expected
    S=sum(a)
    out=[]
    for i in range(r):
        T=sum(k[i-j+r-1] for j in range(r))
        out.append(((z>>(D*(i+r-1)))&(B-1))-Q*S-V*T-r*V*Q)
    assert out==[sum(a[j]*k[i-j+r-1] for j in range(r)) for i in range(r)]
    return out

def chirp_complex(k,a,Q):
    kr,ki=[v[0] for v in k],[v[1] for v in k]
    ar,ai=[v[0] for v in a],[v[1] for v in a]
    p,q,s,t=chirp_real(kr,ar,Q),chirp_real(ki,ai,Q),chirp_real(kr,ai,Q),chirp_real(ki,ar,Q)
    return [(p[j]-q[j],s[j]+t[j]) for j in range(len(a))]

def pow2(e):
    return F(1<<e) if e>=0 else F(1,1<<(-e))

def floor_log2(x):
    assert x>0
    e=x.numerator.bit_length()-x.denominator.bit_length()
    return e-1 if x<pow2(e) else e

def qreal(x,p,emin,emax):
    sign=-1 if x<0 else 1
    x=abs(x)
    if x<pow2(emin): return F(0),"zero"
    if x>=pow2(emax+1): return sign*(2-pow2(-p))*pow2(emax),"clip"
    e=floor_log2(x)
    step=pow2(e-p)
    return sign*int(x/step)*step,"normal"

def norm(z):
    return mp.sqrt(sum(mp.mpf(v.numerator)/v.denominator*mp.mpf(v.numerator)/v.denominator for pair in z for v in pair))

def to_mp(z):
    return mp.mpc(mp.mpf(z[0].numerator)/z[0].denominator,mp.mpf(z[1].numerator)/z[1].denominator)

def quantize_block(z,P):
    maxabs=max(abs(v) for pair in z for v in pair)
    if not maxabs: return F(1),[(0,0)]*len(z)
    R=pow2(floor_log2(maxabs)+1)
    Q=1<<P
    x=[(int(pair[0]*Q/R),int(pair[1]*Q/R)) for pair in z]
    assert F(1,2)<=maxabs/R<1
    assert all(abs(v)<Q for pair in x for v in pair)
    return R,x

def phase(angle,Q):
    # Not a certified coefficient generator: high-precision numerical test data.
    c=mp.exp(mp.j*angle)
    return tuple(max(-Q,min(Q,int(v*Q))) for v in [c.real,c.imag])

def fourier_ref(z):
    r=len(z)
    return [sum(to_mp(z[j])*mp.exp(-2*mp.pi*mp.j*i*j/r) for j in range(r))/mp.sqrt(r) for i in range(r)]

def local(z,p,backend):
    r=len(z)
    P=p+ceil_log2(r)+16
    Q=1<<P
    R,x=quantize_block(z,P)
    if backend=="dense":
        C=[]
        for i in range(r):
            row=[]
            for j in range(r):
                c=mp.exp(-2*mp.pi*mp.j*i*j/r)/mp.sqrt(r)
                row.append((int(c.real*Q),int(c.imag*Q)))
            C.append(row)
        num=dense_complex(C,x,Q)
        assert num==direct_complex(C,x)
        y=[(R*F(a,Q*Q),R*F(b,Q*Q)) for a,b in num]
    else:
        d=[phase(-mp.pi*j*j/r,Q) for j in range(r)]
        k=[phase(mp.pi*j*j/r,Q) for j in range(-(r-1),r)]
        alpha=int(Q/mp.sqrt(r))
        a=[cmul(d[j],x[j]) for j in range(r)]
        c=chirp_complex(k,a,Q)
        slow=[(0,0) for _ in range(r)]
        for i in range(r):
            for j in range(r): slow[i]=cadd(slow[i],cmul(a[j],k[i-j+r-1]))
        assert c==slow
        num=[cmul(d[i],c[i]) for i in range(r)]
        y=[(R*F(alpha*a,Q**5),R*F(alpha*b,Q**5)) for a,b in num]
    return y

# Exhaustive all signs and boundaries: Q=2, r=1 and r=2.
for r in [1,2]:
    for data in product(range(-2,3),repeat=r*r+r):
        C=[list(data[i*r:(i+1)*r]) for i in range(r)]
        x=list(data[r*r:])
        dense_real(C,x,2)
        bump("exhaustive_dense")

for r in [1,2,3,4,8,16]:
    for P in [1,2,5,13]:
        Q=1<<P
        for _ in range(12):
            C=[[(RNG.randint(-Q,Q),RNG.randint(-Q,Q)) for _ in range(r)] for _ in range(r)]
            x=[(RNG.randint(-Q,Q),RNG.randint(-Q,Q)) for _ in range(r)]
            assert dense_complex(C,x,Q)==direct_complex(C,x)
            bump("random_dense_complex")
        for edge in [-Q,Q]:
            dense_real([[edge]*r for _ in range(r)],[edge]*r,Q)
            bump("dense_extreme")

# Exhaustive convolution with arbitrary signs, larger input bound than kernel.
for r in [1,2]:
    for k in product(range(-1,2),repeat=2*r-1):
        for a in product(range(-2,3),repeat=r):
            chirp_real(k,a,1)
            bump("exhaustive_chirp_convolution")
for r in [1,2,3,4,8,16]:
    for P in [1,2,5,13]:
        Q=1<<P
        V=2*Q*Q
        for _ in range(12):
            k=[(RNG.randint(-Q,Q),RNG.randint(-Q,Q)) for _ in range(2*r-1)]
            a=[(RNG.randint(-V,V),RNG.randint(-V,V)) for _ in range(r)]
            got=chirp_complex(k,a,Q)
            slow=[]
            for i in range(r):
                z=(0,0)
                for j in range(r): z=cadd(z,cmul(a[j],k[i-j+r-1]))
                slow.append(z)
            assert got==slow
            bump("random_chirp_complex")
        for edge in [-1,1]:
            chirp_real([edge*Q]*(2*r-1),[edge*V]*r,Q)
            bump("chirp_extreme")

# Exact total quantizer semantics, including strict threshold transitions.
p,emin,emax=4,-10,6
for sign in [-1,1]:
    for value,classification in [(F(0),"zero"),(pow2(emin)-pow2(emin-8),"zero"),
                                  (pow2(emin),"normal"),(pow2(emax+1)-pow2(emax-p),"normal"),
                                  (pow2(emax+1),"clip"),(pow2(emax+3),"clip")]:
        out,label=qreal(sign*value,p,emin,emax)
        assert label==classification
        if classification!="clip": assert abs(out-sign*value)<=pow2(-p)*value+pow2(emin)
        bump("quantizer_edges")

mp.mp.dps=120
for backend in ["dense","chirp"]:
    for r in [1,2,3,4,7,8,16]:
        for p in [4,9,20]:
            cases=[[(F(0),F(0))]*r,
                   [(F(1 if j%2 else -1),F((-1)**j)) for j in range(r)],
                   [(pow2(-50+j*3),-pow2(20-j*2)) for j in range(r)]]
            for _ in range(3):
                cases.append([(F(RNG.randint(-100,100))*pow2(RNG.randint(-30,20)),
                               F(RNG.randint(-100,100))*pow2(RNG.randint(-30,20))) for j in range(r)])
            for z in cases:
                y=local(z,p,backend)
                target=fourier_ref(z)
                err=mp.sqrt(sum(abs(to_mp(a)-b)**2 for a,b in zip(y,target)))
                nz=norm(z)
                if nz:
                    ratio=err/(pow2(-p).numerator/pow2(-p).denominator*nz)
                    MAX_RATIO[backend+"_local_over_u"]=max(MAX_RATIO[backend+"_local_over_u"],float(ratio))
                    assert ratio<mp.mpf("0.001")
                else: assert err==0
                # Rescale input to model reachable small global states before q.
                if nz:
                    scale=pow2(floor_log2(max(abs(v) for pair in z for v in pair))+1)
                    zsmall=[(a/scale,b/scale) for a,b in z]
                    ysmall=local(zsmall,p,backend)
                    v=10
                    tau=pow2(-v-p)
                    rounded=[]
                    for pair in ysmall:
                        parts=[]
                        for a in pair:
                            q,label=qreal(a,p,-v-p,v+4)
                            assert label!="clip"
                            parts.append(q)
                        rounded.append(tuple(parts))
                    targetsmall=fourier_ref(zsmall)
                    error=mp.sqrt(sum(abs(to_mp(a)-b)**2 for a,b in zip(rounded,targetsmall)))
                    budget=3*mp.mpf(2)**(-p)*norm(zsmall)+mp.sqrt(2*r)*mp.mpf(tau.numerator)/tau.denominator
                    assert error<=budget
                    MAX_RATIO[backend+"_stage_over_budget"]=max(MAX_RATIO[backend+"_stage_over_budget"],float(error/budget))
                bump(backend+"_numerical_local")

# Two deliberate invalid constructions must fail, rather than pass vacuously.
Q=2; r=2; C=[[Q,Q],[Q,Q]]; x=[Q,Q]
D=1 # intentionally too narrow
z=pack([v+Q for row in C for v in row],D)*pack([v+Q for v in x[::-1]],D)
B=1<<D
bad=((z>>(D*(r-1)))&(B-1))-Q*sum(C[0])-Q*sum(x)-r*Q*Q
assert bad!=sum(a*b for a,b in zip(C[0],x))
bump("negative_control_insufficient_base")
D=2*(Q.bit_length()-1)+ceil_log2(r)+3; B=1<<D
z=pack([v+Q for row in C for v in row],D)*pack([v+Q for v in x[::-1]],D)
digit=(z>>(D*(r-1)))&(B-1)
bad=digit-Q*sum(v+Q for v in C[0])-Q*sum(v+Q for v in x)-r*Q*Q
assert bad!=sum(a*b for a,b in zip(C[0],x))
bump("negative_control_biased_correction_sums")

result={"status":"all_controls_passed","counts":COUNTS,"maximum_observed_product_bits":MAX_BITS,
        "maximum_numerical_error_ratios":MAX_RATIO,
        "precision_decimal_digits":mp.mp.dps,
        "limitations":["Fresh toy controls, not supplied-program execution",
                       "Python exact integers only check asserted width; no machine-word runtime benchmark",
                       "High-precision Fourier comparisons are not certified transcendental enclosures",
                       "No full composed production FFT executor tested"]}
Path(__file__).with_name("fresh_packed_results.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
