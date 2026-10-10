"""Fresh independent numerical controls, not a proof or source-code replay."""
import numpy as np,math,json
from pathlib import Path
rng=np.random.default_rng(951003); rows=[]
for s in [2,4,6,8,10,12,16]:
 N=s*s; h=s//2; t=np.arange(N); tau=s*(t//s)+(t%s+h)%s
 U=np.exp(-2j*np.pi*np.outer(t,t)/N)/np.sqrt(N)
 H=np.exp(-2j*np.pi*(np.outer(t,tau)-np.outer(tau,t))/N)
 rho=2/(s*np.sin(np.pi/s)); expected=np.array([N/2*(1+rho),N/2*np.sqrt(max(0,1-rho*rho)),N/2*np.sqrt(max(0,1-rho*rho)),N/2*(1-rho)])
 spec=np.linalg.svd(H,compute_uv=False); E0=U[:,tau]-U[tau,:]; sing=np.linalg.svd(E0,compute_uv=False)
 sample=[]
 for k in [0,1,N//8]:
  di=np.exp(2j*np.pi*rng.random(N)); do=np.exp(2j*np.pi*rng.random(N))
  Q=np.zeros((N,N),complex); R=np.zeros((N,N),complex)
  Q[tau,t]=di[tau]/di; R[tau,t]=do[tau]/do
  E=U@Q-R@U; T=(U+R@U@Q)/2
  A=rng.normal(size=(N,k))+1j*rng.normal(size=(N,k)); B=rng.normal(size=(k,N))+1j*rng.normal(size=(k,N))
  if k: T=T+A@B/(10*N)
  gap=.5*np.sqrt(max(0,1-rho-8*k/N)); err=np.linalg.norm(U-T,'fro')/np.sqrt(N)
  sample.append(dict(k=k,actual_frobenius=err,bound=gap,passed=bool(err+1e-10>=gap),defect_squared=float(np.linalg.norm(E,'fro')**2),defect_lower=N*(1-rho)))
 rows.append(dict(s=s,N=N,rank4_max_error=float(np.max(np.abs(spec[:4]-expected))),remaining_singular_max=float(max(spec[4:],default=0)),identity_defect_min_singular=float(sing[-1]),samples=sample))
Path(__file__).with_name('fresh_two_sided_gauge_results.json').write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps([dict(s=x['s'],rank4_error=x['rank4_max_error'],identity_defect_min_singular=x['identity_defect_min_singular'],all_passed=all(y['passed'] for y in x['samples'])) for x in rows],indent=2))
