"""Fresh supplementary checks authored for the 2026-10-10 matrix finalization.
Does not read, import, execute, compile, or parse any supplied research program.
Analytic proofs establish the theorems; these controls test algebra and indexing.
"""
from fractions import Fraction
from itertools import combinations
import json, math, random
from pathlib import Path
out={"method":"fresh independent mathematical controls; not a replay of supplied programs"}
# Exhaust all cross-color splits satisfying the two side-size hypotheses.
n=0
for t in range(1,151):
 for a in range(t+1):
  for b in range(t+1):
   if 3*(a+b)>=2*t and 3*(2*t-a-b)>=2*t:
    assert max(min(a,t-b),min(t-a,b)) >= (t+2)//3
    n+=1
out['cross_color_count_cases']=n
# Exact recurrence, thresholds, and contradiction at and above claimed cutoffs.
n=0
for q in range(1,21):
 for r in range(1,9):
  a=3**r;c=Fraction(q*(a-1),2);b=q*r*a*a
  for diagonal in (False,True):
   threshold=(4*b+4*c+2) if diagonal else (b+2*c)
   for off in (1,2,3,4,5,11,100,10000):
    N=int(threshold)+off;m=N//2 if diagonal else N;m0=m
    for j in range(r):
     assert m>=4*q
     m=(m-q+2)//3
    assert m>=Fraction(m0,a)-Fraction(q,2)*(1-Fraction(1,a))
    assert m*m>N*q*r
    n+=1
out['separator_threshold_cases']=n
# All exact odd-set moment arithmetic, and asymptotic gap sanity.
gaps=[]
for exponent in range(3,25):
 N=2**exponent;L=N//4
 B=Fraction(L)+Fraction(3,4)+Fraction(1,4*L)+Fraction(1,16*L*L)
 assert B<L+1
 delta=math.sqrt(1-math.sqrt(float(B/(L+1))))
 gaps.append({'N':N,'delta':delta,'sqrt_2N_delta':math.sqrt(2*N)*delta})
out['dyadic_gap_examples']=gaps
# Floating-point SVD controls are explicitly numerical, never exact certificates.
try:
 import numpy as np
 rng=random.Random(20261010);tests=0;minratio=1e99
 for N in (8,16,32,64):
  L=N//4;k=2*L-1;h=2*L+1
  U=np.exp(2j*np.pi*np.arange(N)[:,None]*np.arange(N)[None,:]/N)/math.sqrt(N)
  B=L+.75+1/(4*L)+1/(16*L*L)
  delta=math.sqrt(1-math.sqrt(B/(L+1)))
  if N==8:
   pairs=((R,H) for R in combinations(range(N),k) for H in combinations(range(N),h))
  else:
   pairs=((rng.sample(range(N),k),rng.sample(range(N),h)) for _ in range(200))
  for R,H in pairs:
   V=U[np.ix_(R,H)]
   I=sorted(set(range(N))-set(R));X=U[np.ix_(I,H)];A=X.conj().T@X
   assert np.linalg.norm(V.conj().T@V+A-np.eye(h),2)<1e-11
   assert np.real(np.trace(A@A))<=B+1e-10
   sig=np.linalg.svd(V,compute_uv=False)[L]
   assert sig+1e-11>=delta
   minratio=min(minratio,sig/delta);tests+=1
 out['numerical_fourier_controls']={'cases':tests,'minimum_observed_sigma_to_lower_bound_ratio':minratio,'status':'passed; floating-point regression only'}
except ImportError:
 out['numerical_fourier_controls']={'status':'not run; numpy unavailable'}
Path(__file__).with_name('fresh_check_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
