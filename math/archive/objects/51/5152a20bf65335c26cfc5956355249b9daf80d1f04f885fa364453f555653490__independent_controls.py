#!/usr/bin/env python3
"""Newly authored bounded exact controls. Never imports/executes submitted files.
These are finite identity checks, not asymptotic, novelty, or implementation certification.
"""
from fractions import Fraction as Q
from math import comb, factorial
import json
from pathlib import Path

P=97

def dft(x, root):
    n=len(x)
    return [sum(x[j]*pow(root,(j*k)%n,P) for j in range(n))%P for k in range(n)]

def solve_cycle(rhs, nxt, edges):
    n=len(rhs); order=[]; at=0
    for _ in range(n):
        assert at not in order
        order.append(at); at=nxt[at]
    assert at==0 and len(set(order))==n
    accum=0; prod=1
    for j in order:
        accum=(accum+prod*rhs[j])%P;prod=prod*edges[j]%P
    if prod==1:return None
    y=[0]*n;y[0]=accum*pow((1-prod)%P,-1,P)%P
    for t in range(n-1,0,-1):
        j=order[t];y[j]=(rhs[j]+edges[j]*y[nxt[j]])%P
    assert all((y[j]-edges[j]*y[nxt[j]]-rhs[j])%P==0 for j in range(n))
    return y

result={'scope':'Fresh independently authored exact finite checks; no uploaded executable imported or executed.', 'field_prime':P}
affine=0; singular=0
for n in [4,8,16]:
    q=pow(5,(P-1)//n,P)
    assert pow(q,n,P)==1 and pow(q,n//2,P)!=1
    for a in range(1,n,4):
      inva=pow(a,-1,n)
      for b in [1,3]:
       for c in [1,3]:
        nxt=[(a*j+c)%n for j in range(n)]
        target_nxt=[(inva*(k+b))%n for k in range(n)]
        x=[(13*j*j+9*j+2)%P for j in range(n)]
        mx=[pow(q,(b*j)%n,P)*x[nxt[j]]%P for j in range(n)]
        fx=dft(x,q)
        target=[pow(q,(-c*target_nxt[k])%n,P)*fx[target_nxt[k]]%P for k in range(n)]
        assert dft(mx,q)==target
        for lam in [0,1,2,3,5,pow(5,48//n,P)]:
            e=[lam*pow(q,(b*j)%n,P)%P for j in range(n)]
            eh=[lam*pow(q,(-c*target_nxt[k])%n,P)%P for k in range(n)]
            prod=1
            for z in eh:prod=prod*z%P
            assert prod==(-pow(lam,n,P))%P
            rhs=[0]*n;rhs[0]=3;rhs[n//2+1]=7
            source=solve_cycle(rhs,nxt,e)
            if source is None:
                assert (1+pow(lam,n,P))%P==0;singular+=1;continue
            fu=[sum(rhs[j]*pow(q,(j*k)%n,P) for j in [0,n//2+1])%P for k in range(n)]
            out=solve_cycle(fu,target_nxt,eh)
            assert out==dft(source,q)
            affine+=1
result['affine_cycle']={'n':[4,8,16],'end_to_end_exact_cases':affine,'singular_declines':singular,'intertwining_and_edge_product_checked':True,'cycle_executor':'Two linear traversals plus one inversion; independently implemented.'}

raw=corrected=resonant=0
for s in [4,8,16]:
  omega=pow(5,(P-1)//s,P)
  for lam in [2,3,4,5]:
    c=pow(lam,s,P)
    for w in range(1,P):
      if (1-c*pow(w,s,P))%P==0:continue
      amp=7
      grid=[lam*pow(omega,j,P)%P for j in range(s)]
      samples=[amp*pow((1-w*t)%P,-1,P)%P for t in grid]
      scale=pow(s,-1,P)
      for m in range(s):
        invfft=sum(samples[j]*pow(omega,(-j*m)%s,P) for j in range(s))*scale*pow(lam,-m,P)%P
        aliased=amp*pow(w,m,P)*pow((1-c*pow(w,s,P))%P,-1,P)%P
        assert invfft==aliased
        assert invfft*((1-c*pow(w,s,P))%P)%P==amp*pow(w,m,P)%P
      raw+=1;corrected+=1
  for phase in range(s):
    w=pow(omega,phase,P);amp=9
    samples=[sum(amp*pow(w*t,m,P) for m in range(s))%P for t in [pow(omega,j,P) for j in range(s)]]
    assert samples==[(s*amp)%P if (phase+j)%s==0 else 0 for j in range(s)]
    assert (amp*(1-pow(w,s,P)))%P==0
    resonant+=1
result['rational_sampling']={'polefree_alias_cases':raw,'corrected_coefficient_cases':corrected,'resonant_impulse_cases':resonant,'no_runtime_claim':True}

def eye(n):return [[Q(i==j) for j in range(n)] for i in range(n)]
def mul(a,b):return [[sum(a[i][k]*b[k][j] for k in range(len(b))) for j in range(len(b[0]))] for i in range(len(a))]
def add(a,b,ca=1,cb=1):return [[ca*x+cb*y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def inv(a):
    n=len(a);aug=[a[i][:]+eye(n)[i] for i in range(n)]
    for j in range(n):
        k=next(k for k in range(j,n) if aug[k][j]);aug[j],aug[k]=aug[k],aug[j]
        v=aug[j][j];aug[j]=[x/v for x in aug[j]]
        for k in range(n):
            if k!=j:
                v=aug[k][j];aug[k]=[x-v*y for x,y in zip(aug[k],aug[j])]
    return [r[n:] for r in aug]
def transpose(a):return list(map(list,zip(*a)))
def matpow(a,k):
    out=eye(len(a))
    for _ in range(k):out=mul(out,a)
    return out
allpass=[];half=[]
for n in range(3,9):
    i=eye(n);s=[[Q(0) for _ in range(n)] for _ in range(n)];s[0][-1]=Q(-1)
    for j in range(1,n):s[j][j-1]=Q(1)
    u=mul(add(i,s,1,-2),inv(add(i,s,2,-1)))
    assert mul(transpose(u),u)==i
    cn=Q(2**(n+1)-1,2**n+1)
    assert max(sum(abs(u[a][b]) for a in range(n)) for b in range(n))==cn
    assert all(all(v for v in row) for row in u)
    assert len(set(abs(v) for v in u[0]))>1
    allpass.append(n)
    if n%2==0:
        m=n//2;x=matpow(s,m)
        assert mul(x,x)==add(i,i,-1,0)
        rational=mul(add(i,x,2**m,-1),inv(add(i,x,1,-1)))
        closed=add(i,x,Q(2**m+1,2),Q(2**m-1,2))
        assert rational==closed
        assert mul(transpose(closed),closed)==add(i,i,Q(4**m+1,2),0)
        assert all(sum(v!=0 for v in row)==2 for row in closed)
        half.append(n)
result['allpass']={'exact_rational_unitary_norm_and_nonflat_lengths':allpass,'halfcycle_exact_fusion_lengths':half}

h=24;v=comb(h,3);rho=h;degree=sum(comb(3,t)*comb(h-3,3-t) for t in [0,2]);I=3*v*v
W=2*v**3+I*(v*degree+rho);m=h**3;delta=2*v*v*(v-3*h*rho);wp=2**45
s=W*m-delta;S=wp*m-delta
epsilon=Q(delta,m*wp);gamma=Q(13,25_000_000_000);x=Q(191,20)
assert sum(x**j/Q(factorial(j)) for j in range(41))>m
assert epsilon-gamma*x==Q(2328493845853,115964116992000000000000)>0
assert [v,degree,I,W,delta,s,S]==[2024,1393,12289728,34666930287616,2425172992,479235641870830592,486388757330840576]
result['h24_arithmetic_only']={'m':m,'v':v,'degree':degree,'W':W,'W_star':wp,'Delta':delta,'s':s,'S':S,'rational_exponent_slack':str(epsilon-gamma*x),'conditional_framework_transfer_checked':False}
# Literal negative-alpha assumption from row12 can admit an impossible upper bound.
alpha=Q(-10);Delta=1;delta=Q(1,2)
assert alpha*Delta*delta<1
wrong_bound=1+Q(2)/(1-abs(alpha)*Delta*delta)
assert wrong_bound==Q(1,2)<1
result['textual_counterexample']={'source_row':12,'alpha':-10,'degree':1,'p':'4/3','delta':'1/2','literal_assumption_holds':True,'displayed_bound':'1/2','reason':'A Cayley transform of a real symmetric one-edge adjacency is unitary, with eigenvalues modulus one, so any induced norm is at least spectral radius 1. Require absolute value in hypothesis.'}
result['status']='PASS: bounded controls and literal-hypothesis counterexample verified'
out=Path(__file__).with_name('INDEPENDENT_CONTROLS.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
