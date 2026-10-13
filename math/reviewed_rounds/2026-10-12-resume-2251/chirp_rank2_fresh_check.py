"""Fresh gate-design checks; imports no repository/author programs.
This is a mathematical reference check, NOT a metered production executor.
"""
from itertools import product, combinations, permutations
from math import gcd
import json, hashlib, pathlib, random
OUT=pathlib.Path(__file__).with_name('chirp_rank2_fresh_results.json')

def synthesis(N,p,w,a,terms):
    return tuple(sum(c*pow(w,(a*j*j+b*j)%N,p) for b,c in terms)%p for j in range(N))

def direct_dft(x,p,w):
    N=len(x)
    return tuple(sum(x[j]*pow(w,j*k,p) for j in range(N))%p for k in range(N))

def family(N,p,w):
    # Complete explicit-family enumeration, no eliminant or recurrence oracle.
    out={tuple([0]*N): {0: ()}}
    for a in range(N//gcd(2,N)):
        for s in (1,2):
            for bs in combinations(range(N),s):
                for cs in product(range(1,p),repeat=s):
                    terms=tuple(zip(bs,cs))
                    x=synthesis(N,p,w,a,terms)
                    out.setdefault(x,{})[a]=terms
    return out

def coeff(x,p,c):
    n=len(x); z=x[c]; l=x[(c-1)%n]; ll=x[(c-2)%n]; r=x[(c+1)%n]; rr=x[(c+2)%n]
    return (z**3%p,(-2*z*l*r)%p,0,(l*l*rr+ll*r*r)%p,(-z*ll*rr)%p)

def det_poly_check(x,p,c,t):
    N=len(x); total=0
    for perm in permutations(range(3)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(3) for j in range(i+1,3))
        v=sign
        for i,j in enumerate(perm):
            d=i-j;v=v*x[(c+d)%N]*pow(t,d*(d-1)//2,p)%p
        total=(total+v)%p
    return total

def acquire(x,p,w):
    N=len(x); L=N//gcd(2,N)
    if not any(x): return [(0,())], [],[]
    c=next(j for j,v in enumerate(x) if v); e=coeff(x,p,c)
    accepted=[]; roots=[]; failures=[]
    for a in range(L):
        t=pow(w,(-2*a)%N,p)
        if sum(e[k]*pow(t,k,p) for k in range(5))%p: continue
        roots.append(a)
        y=tuple(x[j]*pow(w,(-a*j*j)%N,p)%p for j in range(N))
        y0,y1,y2,y3=(y[j%N] for j in range(4)); delta=(y0*y2-y1*y1)%p
        if delta==0:
            if not y0: failures.append((a,'singular zero-prefix'));continue
            z=y1*pow(y0,-1,p)%p
            bs=[b for b in range(N) if pow(w,b,p)==z]
            if len(bs)!=1: failures.append((a,'rank-one grid'));continue
            terms=((bs[0],y0),)
        else:
            S=(y0*y3-y1*y2)*pow(delta,-1,p)%p
            P=(y1*y3-y2*y2)*pow(delta,-1,p)%p
            bs=[b for b in range(N) if (pow(w,b,p)**2-S*pow(w,b,p)+P)%p==0]
            if len(bs)!=2: failures.append((a,'rank-two grid'));continue
            z0,z1=(pow(w,b,p) for b in bs)
            c0=(y1-y0*z1)*pow((z0-z1)%p,-1,p)%p;c1=(y0-c0)%p
            if not c0 or not c1: failures.append((a,'zero coefficient'));continue
            terms=tuple(zip(bs,(c0,c1)))
        if synthesis(N,p,w,a,terms)!=x: failures.append((a,'full raw verification'));continue
        accepted.append((a,terms))
    return accepted,roots,failures

def gauss_output(N,p,w,a,terms):
    # Accepted all-phase rank-one orbit construction, applied to two shifts.
    d=gcd(2*a,N); K=N//d; c0=(-a*K)%d
    row=[0]*N
    row[c0]=sum(pow(w,(a*j*j+c0*j)%N,p) for j in range(N))%p
    c=c0
    for _ in range(K-1):
        nxt=(c+2*a)%N
        row[nxt]=pow(w,(-a-c)%N,p)*row[c]%p
        c=nxt
    return tuple(sum(gamma*row[(k+b)%N] for b,gamma in terms)%p for k in range(N))

results={'status':'PASS','role':'Unmetered fresh self-authored design checks, not production acceptance','exhaustive':[]}
first_false=None;first_late=None;degree_checks=0;output_coordinates=0
for N,p,w in [(3,7,2),(4,5,2),(5,11,3),(6,7,3)]:
    known=family(N,p,w); checked=0;members=0;false_roots=0;maxroots=0
    for x in product(range(p),repeat=N):
        accepted,roots,failures=acquire(x,p,w);checked+=1
        assert bool(accepted)==(x in known),(N,p,w,x,accepted)
        if any(x): assert {a for a,_ in accepted}==set(known.get(x,{})),(N,p,x,accepted,known.get(x))
        maxroots=max(maxroots,len(roots));false_roots+=len(failures)
        if failures and first_false is None: first_false={'N':N,'p':p,'omega':w,'x':x,'roots':roots,'accepted':accepted,'failures':failures}
        if any(reason=='full raw verification' for a,reason in failures) and first_late is None: first_late={'N':N,'p':p,'omega':w,'x':x,'roots':roots,'accepted':accepted,'failures':failures}
        if accepted:
            members+=1;a,terms=accepted[0]
            assert gauss_output(N,p,w,a,terms)==direct_dft(x,p,w)
            output_coordinates+=N
    results['exhaustive'].append({'N':N,'p':p,'omega':w,'raw_vectors':checked,'members':members,'false_phase_roots':false_roots,'max_filter_roots':maxroots})
# Independent direct determinant evaluation against expanded quartic, including wrap.
rng=random.Random(2251)
for N,p,w in [(3,7,2),(4,5,2),(5,11,3),(6,7,3),(8,17,2),(12,13,2),(16,17,3)]:
    for _ in range(80):
        x=tuple(rng.randrange(p) for _ in range(N))
        for c in range(N):
            if not x[c]:continue
            e=coeff(x,p,c)
            for t in range(p):
                assert sum(e[k]*pow(t,k,p) for k in range(5))%p==det_poly_check(x,p,c,t)
                degree_checks+=1
# Sharp four-phase ambiguity, genuinely rank two because there are zeros.
N,p,w=8,17,2;x=(2,0,2,0,2,0,2,0)
accepted,roots,failures=acquire(x,p,w)
assert [a for a,_ in accepted]==[0,1,2,3]
assert all(len(terms)==2 for a,terms in accepted)
for a,terms in accepted: assert gauss_output(N,p,w,a,terms)==direct_dft(x,p,w)
results['four_phase_ambiguity']={'N':N,'p':p,'omega':w,'x':x,'quartic_coefficients':coeff(x,p,0),'witnesses':accepted,'DFT':direct_dft(x,p,w),'roots':roots}
results['first_false_root']=first_false;results['first_full_raw_rejection']=first_late
results['determinant_point_checks']=degree_checks;results['accepted_output_coordinates']=output_coordinates
# Boundary structured mixtures: all canonical phases, nonunit phases and zero entries.
boundaries=[]
for N,p,w in [(8,17,2),(12,13,2),(16,17,3),(32,97,19),(512,65537,15028)]:
    assert pow(w,N,p)==1 and all(pow(w,d,p)!=1 for d in range(1,N))
    ct=0
    for a in range(N//gcd(2,N)):
        for terms in [((0,1),(1,1)),((1,1),(N-1,p-1)),((0,1),(N//2,1))]:
            x=synthesis(N,p,w,a,terms);valid,_,_=acquire(x,p,w)
            assert valid and any(b==a for b,ts in valid)
            for b,ts in valid: assert gauss_output(N,p,w,b,ts)==direct_dft(x,p,w)
            ct+=1
    boundaries.append({'N':N,'p':p,'omega':w,'structured_cases':ct})
results['structured_boundaries']=boundaries
results['script_sha256']=hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest()
OUT.write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results,indent=2))
