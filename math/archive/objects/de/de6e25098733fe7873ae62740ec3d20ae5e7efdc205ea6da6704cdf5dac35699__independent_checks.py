#!/usr/bin/env python3
from pathlib import Path
from itertools import product
import random,json
import numpy as np
HERE=Path(__file__).resolve().parent;p=65537;root=3;rng=random.Random(230915)
def wroot(n):
    w=pow(root,(p-1)//n,p);assert pow(w,n,p)==1 and (n==1 or pow(w,n//2,p)!=1);return w

def dft(x,w,sgn=-1):return [sum(v*pow(w,sgn*i*j,p) for j,v in enumerate(x))%p for i in range(len(x))]
def solve_linear(A,b,n):
    if n==0:return [] if all(v%p==0 for v in b) else None
    T=[[v%p for v in row]+[v%p] for row,v in zip(A,b)];r=0;piv=[]
    for c in range(n):
        i=next((i for i in range(r,len(T)) if T[i][c]),None)
        if i is None:continue
        T[i],T[r]=T[r],T[i];iv=pow(T[r][c],-1,p);T[r]=[v*iv%p for v in T[r]]
        for i in range(len(T)):
            if i!=r and T[i][c]:
                v=T[i][c];T[i]=[(a-v*b)%p for a,b in zip(T[i],T[r])]
        piv.append(c);r+=1
        if r==len(T):break
    if any(not any(row[:n]) and row[-1] for row in T):return None
    x=[0]*n
    for i,c in enumerate(piv):x[c]=T[i][-1]
    return x

def fit(prefix,d):
    for r in range(d+1):
        A=[[prefix[t-i] for i in range(1,r+1)] for t in range(r,len(prefix))]
        b=[-prefix[t]%p for t in range(r,len(prefix))]
        q=solve_linear(A,b,r)
        if q is not None:return q
    return None

def generate(seed,q,M):
    r=len(q)
    if not r:return [0]*M
    f=seed[:]
    while len(f)<M:f.append(-sum(q[i-1]*f[-i] for i in range(1,r+1))%p)
    return f

def eval_poly(co,z):
    y=0
    for c in co[::-1]:y=(y*z+c)%p
    return y

cases=[];output_entries=0;exceptional=0
for K,M,d in [(4,8,1),(8,8,2),(16,8,2),(16,16,3),(8,8,4)]:
    n=K*M;w=wroot(n);wk=pow(w,M,p)
    for trial in range(3):
        streams=[];fitted=[];types=[]
        for ell in range(K):
            if ell==0:
                q=[-1%p];seed=[rng.randrange(1,p)];kind='forced_simple_pole'
            elif ell==1 and d>=2:
                a=pow(w,ell,p);q=[-2*a%p,a*a%p];seed=[1,2*a%p];kind='forced_repeated_pole'
            elif ell==2 and d>=2:
                a=rng.randrange(1,p);q=[-a%p,0];seed=[rng.randrange(p),rng.randrange(p)];kind='zero_characteristic_root'
            else:
                r=rng.randrange(d+1);q=[rng.randrange(p) for _ in range(r)];seed=[rng.randrange(p) for _ in range(r)];kind='general_or_zero'
            f=generate(seed,q,M);learned=fit(f[:2*d],d);assert learned is not None
            reconstructed=generate(f[:len(learned)],learned,M);assert reconstructed==f
            streams.append(f);fitted.append(learned);types.append(kind)
        columns=[]
        for t in range(M):
            spectrum=[streams[ell][t] for ell in range(K)]
            columns.append([v*pow(K,-1,p)%p for v in dft(spectrum,wk,1)])
        x=[columns[t][b] for b in range(K) for t in range(M)]
        direct=dft(x,w);got=[0]*n;ex=0
        for ell,f in enumerate(streams):
            q=fitted[ell];r=len(q);Q=[1]+q
            P=[sum(Q[i]*f[j-i] for i in range(j+1))%p for j in range(r)]
            B=[sum(Q[i]*f[M+j-i] for i in range(j+1,r+1))%p for j in range(r)]
            # Independently check every coefficient in Q*S=P+z^M B.
            convolution=[0]*(M+r)
            for i,v in enumerate(Q):
                for t,a in enumerate(f):convolution[i+t]=(convolution[i+t]+v*a)%p
            expected=P+[0]*(M-r)+B
            assert convolution==expected
            for j in range(M):
                index=ell+j*K;z=pow(w,-index,p);den=eval_poly(Q,z)
                assert pow(z,M,p)==pow(wk,-ell,p)
                if den:val=(eval_poly(P,z)+pow(wk,-ell,p)*eval_poly(B,z))*pow(den,-1,p)%p
                else:val=eval_poly(f,z);ex+=1
                assert val==direct[index];got[index]=val;output_entries+=1
        assert got==direct;exceptional+=ex
        cases.append({'K':K,'M':M,'d':d,'full_outputs':n,'singular_outputs':ex,
                      'learned_orders':[len(q) for q in fitted],'forced_modes':types[:3]})
# Prefix-only false model: a late impulse is not a low-order recurrence.
delayed=[0]*7+[1];assert fit(delayed,4) is None
assert fit(delayed[:4],2)==[] and generate([],[],8)!=delayed
# Capacity count on a small field independently exhausts parameterized sequences.
def small_sequences(qfield,M,d):
    out=set()
    for co in product(range(qfield),repeat=d):
        for initial in product(range(qfield),repeat=d):
            f=list(initial)
            while len(f)<M:f.append(-sum(co[i-1]*f[-i] for i in range(1,d+1))%qfield)
            out.add(tuple(f))
    return out
capacity=[]
for dd in [1,2]:
    st=small_sequences(3,6,dd);assert len(st)<=3**(2*dd)
    capacity.append({'q':3,'M':6,'d':dd,'distinct_sequences':len(st),'parameter_bound':3**(2*dd),'all_sequences':3**6})

# Same-register Fourier realignment, exact field rank and Gram identity.
def rank(A):
    a=[r[:] for r in A];r=0
    for c in range(len(a[0])):
        i=next((i for i in range(r,len(a)) if a[i][c]),None)
        if i is None:continue
        a[r],a[i]=a[i],a[r];iv=pow(a[r][c],-1,p);a[r]=[v*iv%p for v in a[r]]
        for i in range(r+1,len(a)):
            v=a[i][c]
            if v:a[i]=[(x-v*y)%p for x,y in zip(a[i],a[r])]
        r+=1
        if r==len(a):break
    return r
schmidt=[]
for A,B in [(2,2),(2,4),(2,8),(4,4),(4,8),(4,16),(8,8),(8,16),(16,16)]:
    n=A*B;w=wroot(n);wa=pow(w,B,p)
    R=[];Rdual=[]
    for a,c in product(range(A),repeat=2):
        row=[];dual=[]
        for b,d in product(range(B),repeat=2):
            val=pow(w,-(c*B+d)*(a*B+b),p)
            assert val==pow(wa,-a*d-c*b,p)*pow(w,-b*d,p)%p
            row.append(val);dual.append(pow(val,-1,p))
        R.append(row);Rdual.append(dual)
    assert rank(R)==A*A
    # Bilinear root-inverted Gram controls; not a finite-field complex conjugation claim.
    for i,row in enumerate(R):
        for j,col in enumerate(Rdual):assert sum(x*y for x,y in zip(row,col))%p==(B*B%p if i==j else 0)
    z=np.exp(-2j*np.pi/n)
    C=np.array([[z**((c*B+d)*(a*B+b))/np.sqrt(n) for b,d in product(range(B),repeat=2)] for a,c in product(range(A),repeat=2)])
    error=float(np.max(np.abs(C@C.conj().T-(B/A)*np.eye(A*A))))
    assert error<1e-10
    # The controlled-phase diagonal has coefficient rank A and applies pointwise.
    phase=[[pow(wa,a*b,p) for b in range(B)] for a in range(A)]
    assert rank(phase)==A
    schmidt.append({'A':A,'B':B,'N':n,'exact_rank':A*A,'complex_Gram_error':error,
                    'controlled_phase_rank':A,'flat_singular_value':float(np.sqrt(B/A))})
result={'field':p,'learned_rational_cases':cases,'full_output_entries':output_entries,
        'singular_outputs':exceptional,'late_impulse_negative_control':True,'capacity_controls':capacity,
        'operator_schmidt_cases':schmidt,
        'scope':'Independent exact promised-family output/rational controls and fixed-register matrix gate; no uploaded code executed, no universal fast Fourier claim.'}
(HERE/'INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'rational_cases':len(cases),'outputs':output_entries,'singular_outputs':exceptional,'realignment_cases':len(schmidt)},indent=2))
