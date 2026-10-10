"""Fresh read-only-source audit controls. No source package imports or execution."""
from pathlib import Path
from itertools import product, combinations
from math import comb
from fractions import Fraction
import hashlib, json, zipfile

ROOT = Path(__file__).resolve().parent

def sha(b): return hashlib.sha256(b).hexdigest()

def rem(coeff, divisor):
    a = list(coeff)
    while len(a) >= len(divisor):
        if a[-1]:
            t = a[-1] / divisor[-1] if isinstance(a[-1], Fraction) else a[-1]
            off = len(a)-len(divisor)
            for k,x in enumerate(divisor): a[off+k] -= t*x
        a.pop()
    return a + [0]*(len(divisor)-1-len(a))

def prime(n):
    return n>=2 and all(n%d for d in range(2,int(n**0.5)+1))

def root_of_order(n,q):
    factors=[d for d in range(2,n+1) if n%d==0 and prime(d)]
    for g in range(2,q):
        w=pow(g,(q-1)//n,q)
        if all(pow(w,n//d,q)!=1 for d in factors): return w
    raise AssertionError('No root')

results={}
count=0
for p in (2,3,5,7):
    for c in product(range(3),repeat=p):
        for target in range(p):
            d=list(c);d[target]-=1
            equal=not any(rem(d,[1]*p))
            t=c[(target+1)%p]
            criterion=all(c[r]==t+(r==target) for r in range(p))
            assert equal==criterion
            if equal: assert sum(c)==1+p*t
            count+=1
results['prime_count_vectors_and_targets']=count

for p in (3,5,7):
    target=p-1
    c=[Fraction(0)]*p;c[target]=Fraction(1,2)+Fraction(1,2)
    d=c[:];d[target]-=1
    assert not any(rem(d,[1]*p))
assert rem([0,1,0,0,0,1],[1,-1,1])==[1,0]
results['rational_two_half_paths_and_composite_sixth_roots']='pass'

# A positive irrational amplitude breaks mandatory target-phase coverage.
# Choose z=exp(2pi*i/5) or its conjugate: q=z+z^4=2cos(2pi/5)>0.
# Algebraically q(q+1)=1 modulo Phi_5.
qpoly=[0,1,0,0,1]; lam=[1,1,0,0,1]
prod=[0]*9
for i,a in enumerate(qpoly):
    for j,b in enumerate(lam):prod[i+j]+=a*b
assert rem(prod,[1]*5)==[1,0,0,0]
results['positive_irrational_amplitude_counterexample']='(1+z+z^4)(z+z^4)=1 in Q[z]/Phi_5; neither path has target phase 1'

# Full F_5, depth one, positive-real amplitudes, only phases 0,2,3.
# lam(1+z^2)=z and lam(1+z^3)=z^4, while lam=(1+sqrt(5))/2>0.
palette={0,2,3}; full_edges=[]
for i in range(5):
    for j in range(5):
        k=i*j%5
        terms=[(1, k)] if k in palette else [(lam,0),(lam,2 if k==1 else 3)]
        c=[0]*9
        for amp,r in terms:
            aa=[amp] if isinstance(amp,int) else amp
            for h,value in enumerate(aa):c[h+r]+=value
            full_edges.append((j,i,r,'1' if isinstance(amp,int) else 'phi'))
        c[k]-=1
        assert not any(rem(c,[1]*5))
assert len(full_edges)==33 and {e[2] for e in full_edges}==palette
assert comb(1+len(palette),len(palette))<5
results['full_F5_positive_real_alphabet_counterexample']={'n':5,'depth':1,'phase_exponents':sorted(palette),'amplitudes':['1','phi=(1+sqrt(5))/2'],'edges':len(full_edges),'entries_verified':25,'at_most_depth_bound':comb(4,3),'exact_depth_bound':comb(3,2)}

def graph_counts(n,edges):
    out=[]
    for source in range(n):
        c=[0]*(2*n+2);c[source]=1
        for u in range(2*n+2):
            for a,b in edges:
                if a==u:c[b]+=c[a]
        out.append(c[n+2:])
    return out

zero_controls=[]
for p in (2,3,5,7,11):
    edges=[(j,p) for j in range(p)]+[(p,p+1)]*p+[(p+1,o) for o in range(p+2,2*p+2)]
    assert len(edges)==3*p
    assert all(x==p for row in graph_counts(p,edges) for x in row)
    assert rem([1]*p,[1]*p)==[0]*(p-1)
    plus=edges+[(j,p+2+i) for i in range(p) for j in range(p)]
    assert all(x==p+1 for row in graph_counts(p,plus) for x in row)
    zero_controls.append({'p':p,'zero_edges':3*p,'zero_paths_per_pair':p,'fourier_plus_zero_edges':p*p+3*p})
results['zero_controls']=zero_controls

alphabet_trials=0
for p in (5,7,11):
    for s in range(1,4):
        for labels in combinations(range(p),s):
            exact={0};all_sums={0}
            for d in range(1,5):
                exact={(x+y)%p for x in exact for y in labels}
                all_sums|=exact
                assert len(exact)<=comb(d+s-1,s-1)
                assert len(all_sums)<=comb(d+s,s)
                alphabet_trials+=1
results['alphabet_checks']=alphabet_trials
results['p101_d3_thresholds']={'at_most':next(s for s in range(1,102) if comb(3+s,s)>=101),'exact':next(s for s in range(1,102) if comb(3+s-1,s-1)>=101)}

# Exhaust all normalized DAG supports on two inputs, two internal vertices,
# two outputs, and retain all-pair-unique supports with no mixed vertex.
allowed=[(u,v) for u in range(4) for v in range(max(u+1,2),6)]
accepted=0; minimum=99
for bits in range(1<<len(allowed)):
    edges=[e for k,e in enumerate(allowed) if bits>>k&1]
    counts=graph_counts(2,edges)
    if counts!=[[1,1],[1,1]]:continue
    anc=[set() for _ in range(6)];des=[set() for _ in range(6)]
    anc[0]={0};anc[1]={1};des[4]={0};des[5]={1}
    for u in range(6):
        for a,b in edges:
            if a==u:anc[b]|=anc[a]
    for v in reversed(range(6)):
        for a,b in edges:
            if b==v:des[a]|=des[b]
    if any(len(a)>1 and len(b)>1 for a,b in zip(anc,des)):continue
    assert len(edges)>=4
    accepted+=1;minimum=min(minimum,len(edges))
results['unique_path_two_terminal_exhaustion']={'supports':1<<len(allowed),'valid_no_mixed_vertex_supports':accepted,'minimum_edges':minimum}

gauss=[]; amplitude=None
for n in (3,5,7,9,15,17):
    qs=[]; k=1
    while len(qs)<2:
        q=n*k+1;k+=1
        if prime(q) and q%2:qs.append(q)
    for q in qs:
        w=root_of_order(n,q);half=pow(2,-1,n)
        G=sum(pow(w,(-half*t*t)%n,q) for t in range(n))%q
        assert G
        for i in range(n):
            for j in range(n):
                S=sum(pow(w,(-half*t*t+(i+j)*t)%n,q) for t in range(n))%q
                assert S==G*pow(w,(half*(i+j)**2)%n,q)%q
                recovered=S*pow(G,-1,q)*pow(w,(-half*(i*i+j*j))%n,q)%q
                assert recovered==pow(w,i*j,q)
        gauss.append({'n':n,'field':q,'root':w,'G':G,'entries':n*n})
        if n==3 and amplitude is None:
            weighted=(G+1)%q
            assert weighted!=G
            amplitude={'n':n,'field':q,'root':w,'expected_i0_j0':G,'t0_amplitude2_i0_j0':weighted,'same_path_phases':True}
results['gauss_exact_field_controls']=gauss
results['phase_only_fiber_counterexample']=amplitude

# Source archive/provenance verification was performed in the original private
# review environment. Its verified receipt is supplied separately; this portable
# program reruns the mathematical controls without needing private source files.
results['uploaded_programs_run_or_imported']=False
(ROOT/'FRESH_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
