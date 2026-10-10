"""New standalone exact controls. Uploaded programs remain inert."""
from pathlib import Path
from math import gcd,log2
from itertools import product
import json
OUT=Path(__file__).resolve().parent
P=257
def root(n):
    w=pow(3,(P-1)//n,P)
    assert pow(w,n,P)==1 and (n==1 or pow(w,n//2,P)!=1)
    return w
def dft(a,w):return [sum(x*pow(w,j*k,P) for j,x in enumerate(a))%P for k in range(len(a))]
def rank(a):
    a=[[x%P for x in r] for r in a];r=0
    if not a:return 0
    for j in range(len(a[0])):
        pivot=next((i for i in range(r,len(a)) if a[i][j]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];v=pow(a[r][j],-1,P)
        a[r]=[x*v%P for x in a[r]]
        for i in range(r+1,len(a)):
            v=a[i][j]
            if v:a[i]=[(x-v*y)%P for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r
def rev(x,l):return sum(((x>>j)&1)<<(l-1-j) for j in range(l))
results={}

n=8;m=3;weights={}
for mask in range(1<<n):
    S=[i for i in range(n) if mask>>i&1]
    W=sum((n>>d)*len({i%(1<<d) for i in S}) for d in range(m))
    active={rev(i,m) for i in S};total=0
    for level in range(1,m+1):
        width=1<<level;out=set()
        for block in range(0,n,width):
            for j in range(width//2):
                a=block+j;b=a+width//2
                if a in active or b in active:out.update((a,b))
        total+=len(out);active=out
    assert total==W
    weights[mask]=W
for a in weights:
    for b in weights:
        assert weights[a]+weights[b]>=weights[a|b]+weights[a&b]
results['support_coverage']={'network_identities':256,'submodular_pairs':65536}

def conv(a,b):return [sum(a[i]*b[(j-i)%len(a)] for i in range(len(a))) for j in range(len(a))]
def add(a,b):return [x+y for x,y in zip(a,b)]
def shift(a,s,g=1):return [g*a[(i-s)%len(a)] for i in range(len(a))]
pair_cases=0
for n in range(1,11):
    for seed in range(18):
        a=[(i+seed)%7-3 for i in range(n)]
        b=[(i*3+seed*2)%5-2 for i in range(n)]
        R=[(i*i+seed)%3-1 for i in range(n)]
        if seed==0:R=[int(i==0) for i in range(n)]
        U,V,Y=conv(b,R),conv(a,R),conv(conv(a,b),R)
        da=[0]*n;db=[0]*n
        da[seed%n]+=seed%5-2;db[(seed*3)%n]+=2-seed%7
        ga,gb=(seed%3)-1,((seed//3)%3)-1
        sa,sb=seed%n,(2*seed+1)%n
        y1=add(shift(Y,sa,ga),conv(da,U))
        v1=add(shift(V,sa,ga),conv(da,R))
        y2=add(shift(y1,sb,gb),conv(db,v1))
        u2=add(shift(U,sb,gb),conv(db,R))
        aa=add(shift(a,sa,ga),da);bb=add(shift(b,sb,gb),db)
        assert y2==conv(conv(aa,bb),R) and v1==conv(aa,R) and u2==conv(bb,R)
        pair_cases+=1
results['fixed_pair_shift_gain_kernels']={'cases':pair_cases,'arithmetic':'exact Python integers'}

ap_cases=periodic_cases=0
for n in (2,4,8,16,32):
    w=root(n)
    for a in (1,2,min(n,5)):
        for b in (1,2,min(n,7)):
            for s in (1,2,3):
                for t in (1,2,4):
                    A=[[pow(w,((1+s*i)%n)*((2+t*j)%n),P) for j in range(b)] for i in range(a)]
                    assert rank(A)==min(a,b,n//gcd(n,s*t));ap_cases+=1
    for r in (1<<k for k in range(n.bit_length()-1)):
        q=n//r;t=q.bit_length()-1
        for c in (0,1):
            err=0
            for i in range(n):
                for j in range(n):
                    pred=pow(w,(c*i+(j-c)*(i%r))%n,P)
                    err+=pred!=pow(w,i*j,P)
            assert err==n*n-n*r*(2+t)//2
            periodic_cases+=1
results['fourier_rank_and_periodic_sparsity']={'arithmetic_progression_cases':ap_cases,'attained_periodic_bound_cases':periodic_cases}

sparse_cases=sparse_coordinates=0
for n in (2,4,8,16,32,64):
    w=root(n)
    for k in range(n+1):
        a=[0]*n
        for j in range(k):a[(5*j)%n]=(7*j+3)%P
        b=1 if k==0 else 1<<(k-1).bit_length();m=n//b
        V=[[0]*b for _ in range(m)]
        for t,x in enumerate(a):
            if x:
                for q in range(m):V[q][t%b]=(V[q][t%b]+x*pow(w,q*t,P))%P
        out=[0]*n
        for q in range(m):
            v=dft(V[q],pow(w,m,P))
            for j in range(b):out[q+m*j]=v[j]
        assert out==dft(a,w)
        sparse_cases+=1;sparse_coordinates+=n
results['grouped_sparse_decomposition']={'cases':sparse_cases,'output_coordinates':sparse_coordinates,'backend':'independent direct modular DFT, not #130'}

# Formal dual-number operations are independent of any submitted circuit engine.
def plus(a,b):return ((a[0]+b[0])%P,(a[1]+b[1])%P)
def mul(a,b):return (a[0]*b[0]%P,(a[0]*b[1]+a[1]*b[0])%P)
def times(a,c):return (a[0]*c%P,a[1]*c%P)
linear_cases=0
for n in (2,4,8,16):
    w=root(n)
    for seed in range(5):
        x=[(i*3+seed+1)%P for i in range(n)]
        for coordinate in range(n):
            a=[(v,int(i==coordinate)) for i,v in enumerate(x)]
            k=plus(mul(a[0],a[1]),a[0]);r=a[:];r[0]=plus(r[0],times(k,-1))
            for out in range(n):
                value=(0,0)
                for j in range(n):value=plus(value,times(r[j],pow(w,j*out,P)))
                value=plus(value,k)
                assert value[1]==pow(w,coordinate*out,P)
            linear_cases+=1
results['nonlinear_k_directional_identity']={'basis_direction_cases':linear_cases,'scope':'polynomial identity controls; finite function equality alone is insufficient'}

phase=[]
for L in range(2,7):
    n=1<<L;w=root(n)
    for s in range(1,L):
        q=L-s;mat=[];corr=[]
        for a in range(1<<s):
            for e in range(1<<s):
                row=[];rr=[]
                for d in range(1<<q):
                    for f in range(1<<q):
                        j=a+(1<<s)*d;b=e+(1<<s)*f
                        v=pow(w,j*rev(b,L),P)
                        split=pow(w,((1<<q)*a*rev(e,s)+(1<<s)*d*rev(f,q)+a*rev(f,q))%n,P)
                        assert v==split
                        H=-1 if (j&b).bit_count()%2 else 1
                        row.append(v);rr.append((v-H)%P)
                mat.append(row);corr.append(rr)
        expected=1<<min(s,q);r=rank(mat);r2=rank(corr)
        assert r==expected and expected-1<=r2<=expected+1
        if s>=2 and q>=2:assert r2==expected+1
        phase.append({'N':n,'cut':s,'fourier_rank':r,'walsh_correction_rank':r2})
results['paired_bit_phase_states']={'cuts':len(phase),'records':phase}

results['floating_counterexamples']={
    'sub_ulp_metadata_noop':1e16+1==1e16,
    'coalesced_snapshot_replay':1e16+(1.0-1e16),
    'explicit_current_metadata':1.0,
    'symbolic_float_coefficient_fold':(float(2**53)+1)-float(2**53)
}
assert results['floating_counterexamples']['coalesced_snapshot_replay']==0
assert results['floating_counterexamples']['symbolic_float_coefficient_fold']==0
results['scope']={'status':'PASS','uploaded_source_run':False,'historical_benchmarks_rerun':False,
                  'source_code_certification':False,'novelty_claim':False}
(OUT/'INDEPENDENT_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps({k:({kk:vv for kk,vv in v.items() if kk!='records'}) for k,v in results.items()},indent=2))
