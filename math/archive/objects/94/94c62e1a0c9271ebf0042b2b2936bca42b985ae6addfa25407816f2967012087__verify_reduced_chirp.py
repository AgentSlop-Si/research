"""Independent all-a reduced-period construction test, using previously verified recurrence."""
from pathlib import Path
import math,json
import numpy as np
OUT=Path(__file__).resolve().parent
# Standalone recurrence, rather than import a script that runs its experiment.
def reduced_table(M,K,a,b):
 N=M*K; h=math.gcd(a,M); L=M//h; J=K*h; aa=a//h
 Q=np.empty(N,complex); t=np.arange(L)
 if L==1: Q[:]=1
 else:
  g=math.gcd(2*aa,L)
  for p in range(J):
   H=np.zeros(L,complex)
   for seed in range(g):
    H[seed]=np.sum(np.exp(-2j*np.pi*((aa*t*t)%L)/L-2j*np.pi*(p+J*seed)*t/N))
    q=seed
    for _ in range(L//g-1):
     qn=(q+2*aa)%L
     H[qn]=np.exp(2j*np.pi*p/N+2j*np.pi*((aa+q)%L)/L)*(H[q]+np.exp(-2j*np.pi*p/J)-1)
     q=qn
   Q[p+J*np.arange(L)]=H
 n=(np.arange(N)+b*K)%N
 D=np.empty(N,complex); special=n%J==0
 D[special]=h
 D[~special]=(1-np.exp(-2j*np.pi*(n[~special]%K)/K))/(1-np.exp(-2j*np.pi*(n[~special]%J)/J))
 return Q[n]*D
results=[]
for M,K in [(8,2),(16,4),(32,8),(31,4)]:
 for a in range(M):
  for b in [0,3,M-1]:
   t=np.arange(M); N=M*K
   direct=np.array([np.sum(np.exp(-2j*np.pi*((a*t*t+b*t)%M)/M-2j*np.pi*m*t/N)) for m in range(N)])
   err=float(np.max(abs(reduced_table(M,K,a,b)-direct)))
   results.append({'M':M,'K':K,'a':a,'b':b,'max_absolute_error':err})
assert max(r['max_absolute_error'] for r in results)<1e-9
(OUT/'reduced_chirp_verification.json').write_text(json.dumps({'results':results},indent=2))
print('all-a chirp cases',len(results),'max error',max(r['max_absolute_error'] for r in results))
