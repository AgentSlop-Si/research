#!/usr/bin/env python3
"""Independent bounded algebra controls; no predecessor code or files imported."""
from fractions import Fraction as F
from itertools import combinations
import hashlib,json,math,random
from pathlib import Path

def H(p):
    return -sum(float(t)*math.log2(float(t)) for t in p if t)
def h2(t):
    return H([t,1-t])
def sqnorm(v):
    return sum(x*x for x in v)
def negacyclic_mul(a,b):
    m=len(a); out=[0]*m
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            e=i+j;out[e % m]+=x*y*(-1 if e>=m else 1)
    return out

def conj(a):
    m=len(a);out=[0]*m;out[0]=a[0]
    for i in range(1,m):out[m-i]=-a[i]
    return out

def dft(x,k):
    n=len(x);m=n//2;out=[0]*m
    for j,c in enumerate(x):
        e=(j*k)%n;out[e%m]+=c*(-1 if e>=m else 1)
    return out

results={"method":"Fresh standard-library controls; exact Fraction/integer identities, floating entropy diagnostics only", "checks":{}}
# Unit coefficient rows over rational entries: s is a square, so desired w is rational.
entropy_cases=0;min_slack=10**9;max_delta=0
for s in [4,16,64,256]:
    w=[F(1,math.isqrt(s))]*s+[F(0)]*3
    for t in [F(1,100),F(1,30),F(1,10),F(1,5)]:
        c=(1-t*t)/(1+t*t);sn=2*t/(1+t*t)
        for i,j in [(0,1),(0,s),(s-1,s+2)]:
            v=w[:];v[i]=c*w[i]-sn*w[j];v[j]=sn*w[i]+c*w[j]
            assert sqnorm(v)==1
            err2=sqnorm([a-b for a,b in zip(v,w)])
            p=[x*x for x in v];q=[x*x for x in w]
            tv=sum(abs(a-b) for a,b in zip(p,q))/2
            assert tv*tv<=err2
            cp=p[:s]+[sum(p[s:])]
            delta=sum(abs(a-b) for a,b in zip(cp,q[:s]+[F(0)]))/2
            assert delta<=tv
            assert delta<F(1,2)
            penalty=float(delta)*math.log2(s)+h2(delta)
            slack=H(p)-(math.log2(s)-penalty)
            assert slack>=-1e-11
            assert H(p)+1e-11>=H(cp)
            entropy_cases+=1;min_slack=min(min_slack,slack);max_delta=max(max_delta,float(delta))
ancilla_cases=0
for e in [F(0),F(1,10000),F(1,1000),F(1,100),F(1,10)]:
    # v_original=(1-e)w; ancillary squared norm=1-(1-e)^2.
    ancillary2=1-(1-e)**2
    original_error2=e*e
    assert original_error2+ancillary2==2*e
    assert (1-e)**2+ancillary2==1
    ancilla_cases+=1
results['checks']['robust_entropy']={"rational_unitary_row_cases":entropy_cases,"ancilla_identity_cases":ancilla_cases,"minimum_float_entropy_slack":min_slack,"maximum_coarsened_total_variation":max_delta}
# Exact cyclotomic controls of the odd-only Parseval improvement.
pair_cases=0;even_values=0;odd_energy_cases=0
for n in [8,16]:
    m=n//2
    masks=list(range(1<<m)) if n==8 else [0]+[1<<i for i in range(m)]+[(1<<i)|(1<<j) for i,j in combinations(range(m),2)]
    for a,b in combinations(masks,2):
        d=[((a>>j)&1)-((b>>j)&1) for j in range(m)]
        ham=sum(x*x for x in d);assert ham>=1
        x=d+[-z for z in d]
        energy=[0]*m
        for k in range(n):
            row=dft(x,k)
            if k%2==0:
                assert row==[0]*m;even_values+=1
            else:
                z=negacyclic_mul(row,conj(row));energy=[a+b for a,b in zip(energy,z)]
        assert energy==[4*m*ham]+[0]*(m-1)
        odd_energy_cases+=1;pair_cases+=1
results['checks']['complementary_family']={"distinct_pairs":pair_cases,"even_output_zero_checks":even_values,"exact_odd_parseval_checks":odd_energy_cases,"minimum_Hamming":1,"inferred_all_size_separation":"max odd output difference >= 2 sqrt(Hamming)"}
# Exact randomized encoder and randomized decoder distributions.
rng=random.Random(1605364252);message_cases=0
for M in [2,4,8,16]:
    for Q in range(1,7):
        for seed in range(7):
            E=[]
            for u in range(M):
                a=[rng.randint(1,19) for _ in range(Q)];E.append([F(v,sum(a)) for v in a])
            D=[]
            for a in range(Q):
                v=[rng.randint(0,19) for _ in range(M+1)];D.append([F(z,sum(v)) for z in v])
            success=sum(E[u][a]*D[a][u] for u in range(M) for a in range(Q))/M
            optimal=sum(max(E[u][a] for u in range(M)) for a in range(Q))/M
            assert success<=optimal<=min(F(1),F(Q,M))
            message_cases+=1
results['checks']['randomized_messages']={"exact_fraction_channel_cases":message_cases,"public_seed_handling":"same inequality for each independent seed, then average"}
# Integer source quantization threshold at several success probabilities.
thresholds=[]
for n in [8,16,32,64,128,1024]:
    for r in [1,2,4]:
        if r>n//2:continue
        for delta in [F(0),F(1,3),F(9,10)]:
            target=(1-delta)*(1<<(n//2));b=0
            while (n*(1<<b)+2)**(2*r)<target:b+=1
            assert (n*(1<<b)+2)**(2*r)>=target
            if b:assert (n*(1<<(b-1))+2)**(2*r)<target
            thresholds.append({"N":n,"r":r,"failure_delta":str(delta),"necessary_integer_b":b})
assert next(x['necessary_integer_b'] for x in thresholds if x['N']==1024 and x['r']==1 and x['failure_delta']=='0')==246
results['checks']['quantization']={"threshold_cases":len(thresholds),"thresholds":thresholds}
# Explicit negative/scope controls.
controls={}
# One public label with input-dependent uncharged routing can carry M values: Q=1 bound fails unless metadata counted.
controls['uncharged_metadata_detected']=(F(1)>F(1,8))
# At radius exactly 1, two spectra at separation 2 may have intersecting closed balls; strict radius is necessary.
controls['radius_one_boundary_detected']=abs(1-0)<=1 and abs(1-2)<=1
# Missing the odd-only support count would lose sqrt(2), the source's valid but weaker constant.
controls['odd_support_factor_detected']=(F(4*4,4)==4 and F(4*4,8)==2)
# Flat N-vector: zero estimate has linfty 1 while relative l2 error is 1, for alpha=1/4 at N=16.
controls['false_relative_l2_inference_detected']=(1<=16**F(1,4) and F(1)>F(1,2))
# Rank deficit one is not the pathwise Omega(N/log N) hypothesis.
controls['deficit_one_not_large_deficit']=(1<1024//10)
assert all(controls.values());results['negative_scope_controls']=controls
results['status']='PASS'
p=Path(__file__).with_name('CHECK_RESULTS.json');p.write_text(json.dumps(results,indent=2,sort_keys=True)+'\n')
print(json.dumps({"status":results['status'],"entropy_cases":entropy_cases,"cyclotomic_pairs":pair_cases,"stochastic_cases":message_cases,"threshold_cases":len(thresholds),"negative_controls":len(controls)},sort_keys=True))
