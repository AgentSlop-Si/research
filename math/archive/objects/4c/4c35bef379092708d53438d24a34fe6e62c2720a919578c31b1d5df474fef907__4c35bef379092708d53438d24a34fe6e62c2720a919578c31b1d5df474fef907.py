#!/usr/bin/env python3
"""Independent exact Phase20 review. No uploaded code imports or execution.
The independent gate scans constant-degree gcds at each subgroup node, using a
nonzero resultant witness. Separate Lagrange interpolation controls check the
source's compressed degree-45 elimination strategy.
"""
import collections,itertools,json,math,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parent
rng=random.Random(202610092344)
PERMS=list(itertools.permutations(range(3)))
SIGNS=[(-1)**sum(v[i]>v[j] for i in range(3) for j in range(i+1,3)) for v in PERMS]
def trim(q):
    q=list(q)
    while q and q[-1]==0:q.pop()
    return q

def pmul(a,b,p):
    c=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):c[i+j]=(c[i+j]+x*y)%p
    return trim(c)
def padd(a,b,p):
    c=[0]*max(len(a),len(b))
    for i,v in enumerate(a):c[i]=v
    for i,v in enumerate(b):c[i]=(c[i]+v)%p
    return trim(c)
def peval(q,x,p):
    v=0
    for c in reversed(q):v=(v*x+c)%p
    return v

def premainder(a,b,p):
    a=trim(a);b=trim(b);iv=pow(b[-1],-1,p)
    while len(a)>=len(b):
        q=a[-1]*iv%p;shift=len(a)-len(b)
        for i,c in enumerate(b):a[shift+i]=(a[shift+i]-q*c)%p
        a=trim(a)
    return a

def pgcd(a,b,p):
    a,b=trim(a),trim(b)
    while b:a,b=b,premainder(a,b,p)
    return [v*pow(a[-1],-1,p)%p for v in a] if a else []

def hankel_polynomial(R,w,base,p):
    result=[]
    for perm,sign in zip(PERMS,SIGNS):
        term=[sign%p]
        for i in range(3):
            k=base+i+perm[i]
            term=pmul(term,[R[k],-R[k]*pow(w,k,p)%p],p)
        result=padd(result,term,p)
    return result

def determinant(M,p):
    A=[row[:] for row in M];value=1
    for k in range(len(A)):
        j=next((j for j in range(k,len(A)) if A[j][k]%p),None)
        if j is None:return 0
        if j!=k:A[k],A[j]=A[j],A[k];value=-value
        pivot=A[k][k];value=value*pivot%p;iv=pow(pivot,-1,p)
        for i in range(k+1,len(A)):
            q=A[i][k]*iv%p
            for j in range(k,len(A)):A[i][j]=(A[i][j]-q*A[k][j])%p
    return value%p

def resultant(R,w,p):
    P=hankel_polynomial(R,w,0,p);Q=hankel_polynomial(R,w,1,p)
    P=([*P]+[0]*(4-len(P)))[::-1];Q=([*Q]+[0]*(4-len(Q)))[::-1]
    M=[]
    for poly in (P,Q):
        for j in range(3):M.append([0]*j+poly+[0]*(2-j))
    return determinant(M,p)

def numeric_hankel(seq,b,p):return determinant([[seq[b+i+j] for j in range(3)] for i in range(3)],p)
def dft(r,w,p,count=None):
    n=len(r)
    return [sum(v*pow(w,j*k%n,p) for j,v in enumerate(r))%p for k in range(n if count is None else count)]
def idft(R,w,p):return [v*pow(len(R),-1,p)%p for v in dft(R,pow(w,-1,p),p)]
def structured(n,p,w,d,a,h):
    denom=[(1-a*pow(w,d*k,p))%p for k in range(n)]
    if not all(denom):return None
    H=dft(h,w,p);return idft([v*pow(q,-1,p)%p for v,q in zip(H,denom)],w,p)
def decode(r,d,a,w,p):
    n=len(r);h=[(r[j]-a*r[(j-d)%n])%p for j in range(n)];H=dft(h,w,p)
    return [H[k]*pow(q,-1,p)%p if q else sum(r[j]*pow(w,k*j,p) for j in range(n))%p for k in range(n) for q in [(1-a*pow(w,k*d,p))%p]]

def gate(r,w,p,source_resonance_guard=True):
    n=len(r);R=dft(r,w,p,8);meta={'nonzero_witness':None,'linear_candidates':0,'full_checks':0,'skipped_non_coprime_guard':0}
    for z in range(46):
        if resultant(R,z,p):meta['nonzero_witness']=z;break
    if meta['nonzero_witness'] is None:return None,{**meta,'reason':'zero-resultant'}
    for d in range(1,n):
        z=pow(w,d,p);g=pgcd(hankel_polynomial(R,z,0,p),hankel_polynomial(R,z,1,p),p)
        if len(g)!=2:continue
        a=(-g[0])%p;meta['linear_candidates']+=1
        if not a:continue
        Y=[R[k]*(1-a*pow(z,k,p))%p for k in range(8)]
        if any(numeric_hankel(Y,b,p) for b in (2,3)):continue
        resonances=sum((1-a*pow(w,d*k,p))%p==0 for k in range(n))
        if (pow(a,n,p)==1 and math.gcd(d,n)!=1) if source_resonance_guard else (resonances>1):
            meta['skipped_non_coprime_guard']+=1;continue
        meta['full_checks']+=1
        h=[(r[j]-a*r[(j-d)%n])%p for j in range(n)]
        if 1<=sum(map(bool,h))<=2:return (d,a,h),{**meta,'reason':'accepted','resonances':resonances}
    return None,{**meta,'reason':'no-certificate'}

# Independent Lagrange interpolation at 46 points, not source Newton code.
def interpolate(values,p):
    H=[1]
    for x in range(len(values)):H=pmul(H,[-x%p,1],p)
    result=[0]*len(values)
    for x,value in enumerate(values):
        Q=[0]*len(values);Q[-1]=H[-1]
        for j in range(len(Q)-2,-1,-1):Q[j]=(H[j+1]+x*Q[j+1])%p
        assert (H[0]+x*Q[0])%p==0
        denominator=math.prod(x-j for j in range(len(values)) if j!=x)%p
        scale=value*pow(denominator,-1,p)%p
        for j,c in enumerate(Q):result[j]=(result[j]+scale*c)%p
    return trim(result)
def strip(q,p):
    q=list(q);z=o=0
    while q and q[0]==0:q=q[1:];z+=1
    while len(q)>1 and peval(q,1,p)==0:
        Q=[0]*(len(q)-1);Q[-1]=q[-1]
        for j in range(len(Q)-2,-1,-1):Q[j]=(q[j+1]+Q[j+1])%p
        assert (q[0]+Q[0])%p==0
        q=Q;o+=1
    return q,z,o

# Reproduce the declared finite support/parameter grid, not all GF(97)^8.
p,n,w=97,8,pow(5,12,97);fast=slow=0;reasons=collections.Counter();examples=[]
for d in (1,3,5,7):
    for a in (2,3,5,7,11):
        for j,k in itertools.combinations(range(n),2):
            for u,v in ((2,3),(5,7),(11,13),(17,19)):
                h=[0]*n;h[j]=u;h[k]=v;r=structured(n,p,w,d,a,h);assert r is not None
                got,meta=gate(r,w,p)
                if got:
                    fast+=1;dd,aa,hh=got;assert decode(r,dd,aa,w,p)==dft(r,w,p)
                else:
                    slow+=1;reasons[meta['reason']]+=1
                    if len(examples)<3:examples.append({'delta':d,'alpha':a,'support':[j,k],'amplitudes':[u,v],'reason':meta['reason']})
assert (fast,slow)==(2184,56),(fast,slow)
grid={'p':p,'N':n,'cases':fast+slow,'accepted':fast,'declined':slow,'decline_reasons':dict(reasons),'examples':examples,'exact_output_entries_for_accepted_inputs':8*fast,'scope':'28 supports x 4 delays x 5 alphas x 4 amplitude pairs; not all field vectors'}

# Exact counterexample to the source's overly conservative noncoprime guard.
noncoprime_counterexample=None
for n in (8,16,24,32):
    p=97;w=pow(5,(p-1)//n,p)
    for d in range(1,n):
        g=math.gcd(d,n)
        if g!=2:continue
        for power in range(1,n):
            a=pow(w,power,p)
            if pow(a,n//g,p)==1:continue
            for j,k in itertools.combinations(range(min(n,8)),2):
                h=[0]*n;h[j]=2;h[k]=3;r=structured(n,p,w,d,a,h)
                assert r is not None
                R=dft(r,w,p,8);gg=pgcd(hankel_polynomial(R,pow(w,d,p),0,p),hankel_polynomial(R,pow(w,d,p),1,p),p)
                if len(gg)!=2:continue
                source,sm=gate(r,w,p);fixed,fm=gate(r,w,p,False)
                if source is None and fixed is not None:
                    noncoprime_counterexample={'N':n,'p':p,'omega':w,'delta':d,'alpha':a,'h':h,'r':r,'actual_resonances':0,'alpha_to_N':pow(a,n,p),'alpha_to_cycle_length':pow(a,n//g,p),'true_gcd':gg,'nonzero_resultant_witness':sm['nonzero_witness'],'nonzero_resultant_value':resultant(R,sm['nonzero_witness'],p),'source_guard_rejects_all_candidates':True,'correct_resonance_gate_accepts':True}
                    assert decode(r,fixed[0],fixed[1],w,p)==dft(r,w,p)
                    break
            if noncoprime_counterexample:break
        if noncoprime_counterexample:break
    if noncoprime_counterexample:break
assert noncoprime_counterexample is not None

# Interpolation, degree and root-group folding checks across independent fields.
interpolation=[];interpolation_inputs=[]
for p,n,g in ((97,8,5),(257,16,3),(2013265921,128,31)):
    w=pow(g,(p-1)//n,p)
    for mode in ('generic','two_defect','zero','sparse','character'):
        if mode=='generic':r=[rng.randrange(p) for _ in range(n)]
        elif mode=='two_defect':
            h=[0]*n;h[1]=7;h[n//2]=11;d=n//2-1;a=2
            while pow(a,n,p)==1:a+=1
            r=structured(n,p,w,d,a,h);assert r is not None
        elif mode=='zero':r=[0]*n
        elif mode=='sparse':r=[0]*n;r[0]=2;r[3]=5
        else:r=[pow(w,3*j,p) for j in range(n)]
        R=dft(r,w,p,8);T=interpolate([resultant(R,z,p) for z in range(46)],p)
        assert len(T)<=46
        for z in range(46,min(p,70)):assert peval(T,z,p)==resultant(R,z,p)
        reduced,z,o=strip(T,p)
        for q in range(2,min(p,20)):assert peval(T,q,p)==peval(reduced,q,p)*pow(q,z,p)*pow(q-1,o,p)%p
        folded=[0]*n
        for j,v in enumerate(reduced):folded[j%n]=(folded[j%n]+v)%p
        assert dft(folded,w,p)==[peval(reduced,pow(w,j,p),p) for j in range(n)]
        row={'p':p,'N':n,'mode':mode,'degree':len(T)-1,'zero_factor':z,'one_factor':o,'reduced_degree':len(reduced)-1,'palindromic':reduced==reduced[::-1]}
        interpolation.append(row)
        if mode in ('generic','two_defect'):interpolation_inputs.append(r)

# The formerly rejected Phase19 wrap-collision is genuinely accepted.
p=2013265921;n=128;w=pow(31,(p-1)//n,p);d=63;a=pow(w,9,p)
r=[0]*n
for t in range(n):r[t*d%n]=pow(a,t,p)*(3 if t<17 else 5)%p
choice,meta=gate(r,w,p);assert choice is not None and meta['resonances']==1
assert decode(r,choice[0],choice[1],w,p)==dft(r,w,p)
resonant={'N':n,'p':p,'accepted_delay':choice[0],'accepted_alpha':choice[1],'resonances_repaired':1,'exact_full_DFT_equal':True}

# Eight-probe adversary: same proposals, changed unprobed Fourier coordinate.
h=[0]*n;h[11]=5;h[93]=9;r=structured(n,p,w,37,17,h);assert r is not None
base,meta=gate(r,w,p);assert base
mutant=[(r[j]+pow(n,-1,p)*pow(w,-8*j,p))%p for j in range(n)]
assert dft(mutant,w,p,8)==dft(r,w,p,8)
assert dft(mutant,w,p)[8]!=dft(r,w,p)[8]
choice,meta=gate(mutant,w,p);assert choice is None and meta['full_checks']>0
mutation={'N':n,'unchanged_prefix':8,'changed_bin':8,'full_certificate_rejects':True,'full_checks':meta['full_checks']}

# New family controls across both dyadic and nondyadic lengths.
family_controls=[]
for p,n,g in ((998244353,17,3),(2013265921,30,31),(2013265921,60,31),(2013265921,128,31),(2013265921,384,31)):
    w=pow(g,(p-1)//n,p);d=next(d for d in range(n//3+1,n) if math.gcd(d,n)==1)
    accepted=0
    for trial in range(3):
        h=[0]*n;j,k=rng.sample(range(n),2);h[j]=7;h[k]=11
        r=structured(n,p,w,d,2,h);assert r is not None
        choice,meta=gate(r,w,p)
        if choice:
            accepted+=1;assert decode(r,choice[0],choice[1],w,p)==dft(r,w,p)
    family_controls.append({'N':n,'p':p,'cases':3,'accepted':accepted})

# Soundness on unrelated random vectors, and small-degree interpolation controls.
random_rows=[]
for p,n,g in ((97,8,5),(257,16,3),(2013265921,128,31)):
    w=pow(g,(p-1)//n,p);accepted=0
    for _ in range(20):
        r=[rng.randrange(p) for _ in range(n)];choice,meta=gate(r,w,p)
        if choice:
            accepted+=1;assert sum(map(bool,choice[2]))<=2
            assert decode(r,choice[0],choice[1],w,p)==dft(r,w,p)
    random_rows.append({'N':n,'p':p,'inputs':20,'accepted_certificates':accepted,'false_acceptances':0})
for degree in (0,1,10,32,45):
    p=97;q=[rng.randrange(p) for _ in range(degree+1)];q[-1]=1
    assert interpolate([peval(q,z,p) for z in range(46)],p)==q

# Corrected guard versus actual resonance counts; source remains untouched.
resonance_guard_cases=0;conservative_false_rejections=0
for n in (8,12,16,24,32):
    p=97;w=pow(5,(p-1)//n,p)
    for d in range(1,n):
        g=math.gcd(d,n)
        for a in range(1,p):
            zeros=sum((1-a*pow(w,d*k,p))%p==0 for k in range(n))
            expected=g if pow(a,n//g,p)==1 else 0
            assert zeros==expected
            corrected_reject=g>1 and pow(a,n//g,p)==1
            assert corrected_reject==(zeros>1)
            old_reject=g>1 and pow(a,n,p)==1
            conservative_false_rejections+=bool(old_reject and not corrected_reject)
            resonance_guard_cases+=1
p=97;n=8;w=pow(5,12,p);d=2;a=1;r=[3,7,3,7,5,7,5,7]
h=[(r[j]-a*r[(j-d)%n])%p for j in range(n)]
zeros=[k for k in range(n) if (1-a*pow(w,d*k,p))%p==0]
assert h==[95,0,0,0,2,0,0,0] and zeros==[0,4]
assert math.gcd(d,n)>1 and pow(a,n//math.gcd(d,n),p)==1
assert decode(r,d,a,w,p)==dft(r,w,p)
resonance_guard={'exhaustive_pairs':resonance_guard_cases,'old_guard_nonresonant_false_rejections':conservative_false_rejections,'corrected_predicate_matches_more_than_one_actual_zero':True,'genuine_non_coprime_example':{'N':n,'p':p,'delta':d,'alpha':a,'r':r,'h':h,'zero_denominator_bins':zeros,'corrected_guard_rejects':True,'optional_two_direct_repairs_match_DFT':True,'two_repairs_cost_O_2N_not_free':True}}

out={'corrected_resonance_guard_controls':resonance_guard,'dyadic_and_nondyadic_family_controls':family_controls,'finite_parameter_grid':grid,'noncoprime_nonresonant_counterexample':noncoprime_counterexample,'resultant_interpolation_controls':interpolation,'Phase19_resonant_counterexample_now_recovered':resonant,'unchanged_eight_probe_adversary':mutation,'generic_soundness_controls':random_rows,'uploaded_code_executed':False,'uploaded_modules_imported':False,'source_selector_execution_claim':False,'independent_gate':'degree<=45 nonzero polynomial witness, direct constant-degree gcd subgroup scan, full exact support certificate'}
text=json.dumps(out,indent=2,sort_keys=True)+'\n';(ROOT/'INDEPENDENT_RESULTS.json').write_text(text);print(text,end='')
