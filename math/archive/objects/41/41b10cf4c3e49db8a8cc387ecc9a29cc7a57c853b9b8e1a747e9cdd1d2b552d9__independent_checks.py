#!/usr/bin/env python3
"""Independent mathematical checks. Never import or execute uploaded modules.
This intentionally uses Hankel solves rather than the source's BM implementation.
Its check-time complexity is not the optimized theorem's complexity.
"""
import collections, itertools, json, math, pathlib, random
ROOT=pathlib.Path(__file__).resolve().parent
rng=random.Random(202610092330)

def prime(p): return p>=2 and all(p%d for d in range(2,math.isqrt(p)+1))
def field(n):
    k=4
    while not prime(k*n+1): k+=1
    p=k*n+1
    factors=[q for q in range(2,n+1) if n%q==0 and prime(q)]
    for g in range(2,p):
        w=pow(g,k,p)
        if pow(w,n,p)==1 and all(pow(w,n//q,p)!=1 for q in factors): return p,w
    raise AssertionError('root')
def dft(r,w,p,count=None):
    n=len(r)
    return [sum(v*pow(w,j*k%n,p) for j,v in enumerate(r))%p for k in range(n if count is None else count)]
def idft(R,w,p): return [v*pow(len(R),-1,p)%p for v in dft(R,pow(w,-1,p),p)]
def conv(C,r,p): return [sum(c*r[(j-e)%len(r)] for e,c in C.items())%p for j in range(len(r))]
def spectrum(C,n,w,p): return [sum(c*pow(w,e*k%n,p) for e,c in C.items())%p for k in range(n)]
def residual_from_inverse(C,n,w,p):
    values=spectrum(C,n,w,p)
    if not all(values): return None
    r=idft([pow(v,-1,p) for v in values],w,p)
    assert conv(C,r,p)==[1]+[0]*(n-1)
    return r

def solve(A,b,p):
    m=len(b); M=[list(row)+[value] for row,value in zip(A,b)]
    for col in range(m):
        pivot=next((i for i in range(col,m) if M[i][col]%p),None)
        if pivot is None: return None
        M[col],M[pivot]=M[pivot],M[col]
        inv=pow(M[col][col],-1,p)
        M[col]=[v*inv%p for v in M[col]]
        for i in range(m):
            if i!=col:
                factor=M[i][col]
                M[i]=[(a-factor*b)%p for a,b in zip(M[i],M[col])]
    return [row[-1] for row in M]

def inverse_proposal(r,s,w,p):
    R=dft(r,w,p,2*s)
    if not all(R): return None,'zero-probe'
    b=[pow(v,-1,p) for v in R]
    recurrence=None
    for degree in range(1,s+1):
        H=[[b[i+j] for j in range(degree)] for i in range(degree)]
        a=solve(H,[-b[i+degree]%p for i in range(degree)],p)
        if a is not None and all((b[i+degree]+sum(a[j]*b[i+j] for j in range(degree)))%p==0 for i in range(len(b)-degree)):
            recurrence=a+[1];break
    if recurrence is None:return None,'no-recurrence'
    nodes=[(e,pow(w,e,p)) for e in range(len(r)) if sum(c*pow(w,e*j,p) for j,c in enumerate(recurrence))%p==0]
    if len(nodes)!=degree:return None,'not-subgroup-roots'
    a=solve([[pow(z,k,p) for _,z in nodes] for k in range(degree)],b[:degree],p)
    if a is None or not all(a):return None,'degenerate'
    return {e:c for (e,z),c in zip(nodes,a)},'proposal'
def recover(r,s,w,p):
    C,reason=inverse_proposal(r,s,w,p)
    if C is None:return None,reason
    if conv(C,r,p)!=[1]+[0]*(len(r)-1):return None,'certificate-failed'
    return C,'accepted'

def graph_detect(r,p,K):
    n=len(r)
    if n<2*K+1 or not all(r):return None
    ratios=collections.Counter(r[j]*pow(r[j-1],-1,p)%p for j in range(n))
    if len(ratios)>2*K*K:return None
    possible={0}
    for count in ratios.values():possible|={x+count for x in tuple(possible)}
    candidates=[1] if len(ratios)==1 else [pow(u,-1,n) for u in sorted(possible) if 0<u<n and math.gcd(u,n)==1]
    for delta in candidates:
        sample=collections.Counter(r[j]*pow(r[(j-delta)%n],-1,p)%p for j in range(2*K+1))
        alpha=max(sample,key=sample.get)
        h=[(r[j]-alpha*r[(j-delta)%n])%p for j in range(n)]
        if sum(bool(v) for v in h)<=K:return delta,alpha,h
    return None

def binomial_signal(n,d,a,j,c,p):
    assert math.gcd(n,d)==1 and pow(a,n,p)!=1
    r=[0]*n
    scale=c*pow((1-pow(a,n,p))%p,-1,p)%p
    for t in range(n):r[(j+t*d)%n]=scale*pow(a,t,p)%p
    return r

def graph_decode(r,candidate,w,p):
    d,a,h=candidate;n=len(r);H=dft(h,w,p);R=[]
    for k in range(n):
        den=(1-a*pow(w,k*d%n,p))%p
        R.append(H[k]*pow(den,-1,p)%p if den else sum(r[j]*pow(w,k*j%n,p) for j in range(n))%p)
    return R

# Exhaustive independent classifications at GF(17)^4.
p,n,w=17,4,4
all_count=nonzero=graph_yes=invertible=inverse_yes=0
for r in itertools.product(range(p),repeat=n):
    all_count+=1
    if all(r):
        nonzero+=1
        oracle=any(sum((r[j]-a*r[(j-d)%n])%p!=0 for j in range(n))<=1 for d in (1,3) for a in range(1,p))
        found=graph_detect(r,p,1)
        assert bool(found)==oracle
        if found:
            graph_yes+=1
            assert graph_decode(r,found,w,p)==dft(r,w,p)
    R=dft(r,w,p)
    if all(R):
        invertible+=1
        C0=idft([pow(v,-1,p) for v in R],w,p)
        support={j:c for j,c in enumerate(C0) if c}
        eligible=len(support)<=2
    else:eligible=False;support={}
    C,reason=recover(r,2,w,p)
    assert (C is not None)==eligible
    if C is not None:
        inverse_yes+=1
        assert C==support
assert (all_count,nonzero,graph_yes,invertible,inverse_yes)==(83521,65536,832,65536,1280)
exhaustive={'field':17,'N':4,'vectors':all_count,'nowhere_zero_vectors':nonzero,'graph_eligible':graph_yes,'invertible_vectors':invertible,'inverse_sparse_eligible':inverse_yes,'misses':0,'false_acceptances':0}

# Unknown shifts, including both orientation gauges and full Fourier decoding.
graph_rows=[];orientation=None
for n in (3,4,5,7,8,12,16,30,64,128):
    p,w=field(n);a=next(a for a in range(2,p) if pow(a,n,p)!=1)
    count=0
    for d in range(1,n):
        if math.gcd(d,n)!=1:continue
        for j in sorted({0,n//3,n-1}):
            r=binomial_signal(n,d,a,j,3,p)
            found=graph_detect(r,p,1);assert found is not None
            assert graph_decode(r,found,w,p)==dft(r,w,p)
            forward=[(r[q]-a*r[(q-d)%n])%p for q in range(n)]
            reverse=[(r[q]-pow(a,-1,p)*r[(q+d)%n])%p for q in range(n)]
            assert sum(map(bool,forward))==sum(map(bool,reverse))==1
            u=pow(d,-1,n);counts=sorted(collections.Counter(r[q]*pow(r[q-1],-1,p)%p for q in range(n)).values())
            assert counts==sorted([u,n-u])
            if n==7 and d==3 and j==0:orientation={'N':n,'p':p,'signal':r,'delay':d,'alpha':a,'reverse_delay':n-d,'reverse_alpha':pow(a,-1,p),'forward_defect':forward,'reverse_defect':reverse}
            count+=1
    # Zero-defect character needs exactly one direct-frequency repair.
    r=[pow(w,2*j,p) for j in range(n)]
    found=graph_detect(r,p,1);assert found and not any(found[2])
    assert graph_decode(r,found,w,p)==dft(r,w,p)
    graph_rows.append({'N':n,'p':p,'one_defect_inputs':count,'character_check':True})

# Independent sparse inverse families, with actual support below/equal cap.
inverse_rows=[];matrix_entries=0
for n in (7,8,12,16,30,64,128,384):
    p,w=field(n);cap=min(8,n//2);count=0
    for t in range(1,min(6,cap)+1):
        for trial in range(4):
            for attempt in range(1000):
                C={e:rng.randrange(1,p) for e in rng.sample(range(n),t)}
                r=residual_from_inverse(C,n,w,p)
                if r is not None:break
            assert r is not None
            recovered,reason=recover(r,cap,w,p)
            assert recovered==C
            got=[pow(v,-1,p) for v in spectrum(recovered,n,w,p)]
            assert got==dft(r,w,p)
            count+=1;matrix_entries+=n
    inverse_rows.append({'N':n,'p':p,'cap':cap,'inputs':count})

# Complete hidden-factor families, unknown impulse location/scale and gauge.
union_rows=[]
for n in (17,30,64,128):
    p,w=field(n)
    ds=[next(d for d in range(n//2,n) if math.gcd(d,n)==1),n-1,1]
    alphas=[a for a in range(2,p) if all(pow(a,n//math.gcd(n,d),p)!=1 for d in ds)][:3]
    for m in (1,2,3):
        Q={0:1}
        for d,a in zip(ds[:m],alphas[:m]):
            new=collections.defaultdict(int)
            for e,c in Q.items():new[e]=(new[e]+c)%p;new[(e+d)%n]=(new[(e+d)%n]-a*c)%p
            Q={e:c for e,c in new.items() if c}
        for j in (0,n//3,n-1):
            c=3;C={(e-j)%n:a*pow(c,-1,p)%p for e,a in Q.items()}
            r=residual_from_inverse(C,n,w,p);assert r is not None
            recovered,reason=recover(r,2**m,w,p)
            assert recovered==C
            assert conv(Q,r,p)==[c if k==j else 0 for k in range(n)]
            assert dft(r,w,p)==[pow(z,-1,p) for z in spectrum(C,n,w,p)]
            matrix_entries+=n
        union_rows.append({'N':n,'p':p,'factors':m,'actual_inverse_taps':len(C),'positions':3})

# Positive separated-wrap K=2,3 controls with explicitly verified hypotheses.
bounded_rows=[]
for n in (12,16,30,64,128):
    p,w=field(n);d=next(d for d in range(n//3+1,n) if math.gcd(d,n)==1);u=pow(d,-1,n)
    for K in (2,3):
        done=0
        for attempt in range(500):
            a=rng.randrange(2,p)
            if pow(a,n,p)==1:continue
            sites=[0]+rng.sample(range(1,n),K-1)
            h=[0]*n
            for t in sites:h[t*d%n]=rng.randrange(1,p)
            denom=[(1-a*pow(w,k*d,p))%p for k in range(n)]
            R=[v*pow(z,-1,p)%p for v,z in zip(dft(h,w,p),denom)]
            r=idft(R,w,p)
            if not all(r):continue
            wraps=collections.defaultdict(set)
            for j in range(n):
                ratio=r[j]*pow(r[j-1],-1,p)%p
                wraps[ratio].add(int((u*((j-1)%n))%n>=n-u))
            if any(len(types)>1 for types in wraps.values()):continue
            assert len(wraps)<=2*K*K
            found=graph_detect(r,p,K);assert found is not None
            assert graph_decode(r,found,w,p)==R
            done+=1
            if done==3:break
        assert done==3,(n,K,done)
        bounded_rows.append({'N':n,'p':p,'K':K,'separated_inputs':done})

# Noncoprime filter unions are covered by inverse sparsity, not ratio completeness.
noncoprime_unions=[]
for n in (16,30,64):
    p,w=field(n);Q={0:1}
    for d in (n//2,2):
        a=next(a for a in range(2,p) if pow(a,n//math.gcd(n,d),p)!=1)
        new=collections.defaultdict(int)
        for e,c in Q.items():new[e]=(new[e]+c)%p;new[(e+d)%n]=(new[(e+d)%n]-a*c)%p
        Q={e:c for e,c in new.items() if c}
    r=residual_from_inverse(Q,n,w,p);assert r is not None
    assert recover(r,4,w,p)[0]==Q
    noncoprime_unions.append({'N':n,'p':p,'tap_count':len(Q)})

# End-to-end Green identity with independent dense pivoted solves.
green_rows=[]
for n in (7,8,12,16,30):
    p,w=field(n)
    L=[[(7+pow(w,j,p) if j==k else 0)+(2 if k==(j-1)%n else 0) for k in range(n)] for j in range(n)]
    P=[[(7+2*pow(w,-j,p) if j==k else 0)+(1 if k==(j-1)%n else 0) for k in range(n)] for j in range(n)]
    checked=0
    for trial in range(4):
        while True:
            C={e:rng.randrange(1,p) for e in rng.sample(range(n),min(3,n//2))}
            r=residual_from_inverse(C,n,w,p)
            if r is not None:break
        x=solve(P,r,p)
        if x is None:continue
        C2,reason=recover(r,min(3,n//2),w,p);assert C2==C
        recovered_R=[pow(z,-1,p) for z in spectrum(C2,n,w,p)]
        y=solve(L,recovered_R,p);assert y==dft(x,w,p)
        checked+=1
    green_rows.append({'N':n,'p':p,'checks':checked,'solver':'independent dense pivoted Gaussian elimination'})

# Adversarial short-probe alias: proposal unchanged, full certificate fails.
n=128;p,w=field(n);C={2:2,7:3,64:5,127:7}
while residual_from_inverse(C,n,w,p) is None:C[2]=(C[2]+1)%p or 1
r=residual_from_inverse(C,n,w,p);s=4;k0=8
mutation=[(r[j]+pow(n,-1,p)*pow(w,-k0*j,p))%p for j in range(n)]
assert dft(r,w,p,8)==dft(mutation,w,p,8)
assert dft(r,w,p)[8]!=dft(mutation,w,p)[8]
assert inverse_proposal(mutation,s,w,p)[0]==C
assert recover(mutation,s,w,p)==(None,'certificate-failed')
mutation_record={'N':n,'p':p,'unchanged_probes':8,'changed_bin':8,'proposal_unchanged':True,'full_certificate_rejects':True}

# Cross-wrap collision source control, independently built and rejected.
p=2013265921;n=128;w=pow(31,(p-1)//n,p);d=63;a=pow(w,9,p)
r=[0]*n
for t in range(n):r[t*d%n]=pow(a,t,p)*(3 if t<17 else 5)%p
assert sum((r[j]-a*r[(j-d)%n])%p!=0 for j in range(n))==2
assert graph_detect(r,p,2) is None
collision={'N':n,'p':p,'delta':d,'defects':2,'detector_rejects':True}
assert graph_detect([1,1,16,16],17,1) is None
assert conv({0:1,2:1},[1,1,16,16],17)==[0]*4

# Scope and accounting controls based on exact arithmetic, not source execution.
p=17;n=16;w=3
ld=[(7+pow(w,j,p))%p for j in range(n)]
pd=[(7+2*pow(w,-j,p))%p for j in range(n)]
def det_cyclic(diag,b,p):return (math.prod(diag)-(-b)**len(diag))%p
assert ld[3]==0 and pd[11]==0 and det_cyclic(ld,2,p)==det_cyclic(pd,1,p)==16
precision=[]
for n in (128,384,1024,4096):
    gram_off=2*math.cos(math.pi/n)
    cond=math.sqrt((2+gram_off)/(2-gram_off))
    formula=1/math.tan(math.pi/(2*n))
    assert abs(cond/formula-1)<1e-9
    precision.append({'N':n,'condition_number':formula})
output={'exhaustive_GF17_N4':exhaustive,'unknown_graph_cases':graph_rows,'orientation_nonidentifiability':orientation,
        'bounded_separated_wrap_cases':bounded_rows,'noncoprime_inverse_unions':noncoprime_unions,'end_to_end_Green_cases':green_rows,'sparse_inverse_cases':inverse_rows,'unknown_union_cases':union_rows,'inverse_and_union_fourier_entries':matrix_entries,
        'unchanged_probe_mutation':mutation_record,'resonant_cross_wrap_counterexample':collision,
        'noncoprime_character_counterexample':True,'inherited_zero_diagonal_nonsingular_counterexample':True,'complex_two_node_conditioning':precision,
        'uploaded_code_executed':False,'source_modules_imported':False,'independent_recurrence_method':'Hankel-system enumeration, not uploaded BM',
        'scope':'Exact mathematical controls; not execution or timing certification of uploaded implementation.'}
text=json.dumps(output,indent=2,sort_keys=True)+'\n'
(ROOT/'INDEPENDENT_RESULTS.json').write_text(text)
print(text,end='')
