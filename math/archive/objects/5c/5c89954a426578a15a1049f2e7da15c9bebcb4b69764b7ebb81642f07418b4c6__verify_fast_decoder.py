"""Independent verification of DECODER.md; no import of other experiment code."""
from pathlib import Path
import json, math
import numpy as np
rng=np.random.default_rng(824938)
OUT=Path(__file__).resolve().parent

def dense_sig(M,K,a,b,d):
 r=np.arange(K)[:,None]; t=np.arange(M)[None,:]
 return np.exp(2j*np.pi*((a*t*t+(b+d*r)*t)%M)/M)

def table(M,K,a,b,p):
 N=M*K; t=np.arange(M)
 H=np.zeros(M,complex); step=(2*a)%M; g=math.gcd(step,M)
 twist=np.exp(-2j*np.pi*p/K)-1
 for seed in range(g):
  H[seed]=np.sum(np.exp(-2j*np.pi*((a*t*t+b*t)%M)/M-2j*np.pi*(p+K*seed)*t/N))
  q=seed
  for _ in range(M//g-1):
   qn=(q+step)%M
   H[qn]=np.exp(2j*np.pi*p/N+2j*np.pi*((a+b+q)%M)/M)*(H[q]+twist)
   q=qn
 return H

def short_cyclic_conv(alpha,v):
 K=len(alpha); M=len(v); P=1<<(2*K-2).bit_length()
 fa=np.fft.fft(alpha,P); out=np.zeros(M,complex)
 for start in range(0,M,K):
  block=v[start:start+K]
  conv=np.fft.ifft(np.fft.fft(block,P)*fa)[:len(block)+K-1]
  np.add.at(out,(start+np.arange(len(conv)))%M,conv)
 return out

def fast(c,M,K,a,b,d):
 out=np.empty(M*K,complex); gd=math.gcd(d,M); L=M//gd; js=np.arange(L)
 for p in range(K):
  H=table(M,K,a,b,p)
  alpha=c*np.exp(-2j*np.pi*p*np.arange(K)/K)
  if K>L:
   beta=np.zeros(L,complex)
   np.add.at(beta,np.arange(K)%L,alpha)
  for orbit in range(gd):
   indices=(orbit+d*js)%M
   h=H[indices]; v=h[(-js)%L]
   if K<=L: w=short_cyclic_conv(alpha,v)
   else: w=np.fft.ifft(np.fft.fft(beta)*np.fft.fft(v))
   out[p+K*indices]=w[(-js)%L]/np.sqrt(M*K)
 return out

results=[]
for M,K in [(8,2),(8,4),(16,4),(16,8),(32,4),(31,4),(31,8)]:
 for a,b,d in ([(a,b,d) for a,b in [(1,0),(3,5)] for d in range(M)] if M<=16 else [(1,0,0),(1,0,2),(3,5,4),(3,5,8),(M-1,M-2,M-3),(1,0,1),(3,5,7)]):
  if a%M==0: continue
  N=M*K; sig=dense_sig(M,K,a,b,d); t=np.arange(M)
  table_err=0
  for p in range(K):
   reference=np.array([np.sum(np.exp(-2j*np.pi*((a*t*t+b*t)%M)/M-2j*np.pi*(p+K*q)*t/N)) for q in range(M)])
   table_err=max(table_err,float(np.max(abs(table(M,K,a,b,p)-reference))))
  basis_err=0
  for pos in range(N):
   x=np.zeros(N,complex); x[pos]=1
   c=np.sum(sig*x.reshape(K,M),axis=1)
   ref=np.fft.fft((sig.conj()*c[:,None]).ravel(),norm='ortho')
   basis_err=max(basis_err,float(np.max(abs(fast(c,M,K,a,b,d)-ref))))
  random_err=0
  for _ in range(4):
   x=rng.normal(size=(K,M))+1j*rng.normal(size=(K,M))
   c=np.sum(sig*x,axis=1)
   ref=np.fft.fft((sig.conj()*c[:,None]).ravel(),norm='ortho')
   random_err=max(random_err,float(np.max(abs(fast(c,M,K,a,b,d)-ref))))
  results.append({'M':M,'K':K,'a':a,'b':b,'d':d,'basis_vectors_tested':N,'random_vectors_tested':4,'table_max_absolute_error':table_err,'all_basis_decoder_max_absolute_error':basis_err,'four_random_decoder_max_absolute_error':random_err})
assert max(r['all_basis_decoder_max_absolute_error'] for r in results)<1e-10
assert max(r['four_random_decoder_max_absolute_error'] for r in results)<1e-9
(OUT/'fast_decoder_verification.json').write_text(json.dumps({'seed':824938,'results':results},indent=2))
print('cases',len(results),'basis_count',sum(r['basis_vectors_tested'] for r in results),'random_count',sum(r['random_vectors_tested'] for r in results),'basis max',max(r['all_basis_decoder_max_absolute_error'] for r in results),'random max',max(r['four_random_decoder_max_absolute_error'] for r in results),'table max',max(r['table_max_absolute_error'] for r in results))
