"""Independent small falsification controls. No supplied program imported or run."""
import json, math, random
import numpy as np
from pathlib import Path
R=random.Random(95106); p=65537

def fft(a,q):
 n=len(a)
 if n==1:return a[:]
 if not any(a):return [0]*n
 e=fft(a[::2],q*q%p);o=fft(a[1::2],q*q%p)
 out=[0]*n;w=1
 for j in range(n//2):
  v=w*o[j]%p;out[j]=(e[j]+v)%p;out[j+n//2]=(e[j]-v)%p;w=w*q%p
 return out

def bm(s):
 C=[1];B=[1];L=0;shift=1;b=1
 for n in range(len(s)):
  d=sum(C[j]*s[n-j] for j in range(min(L,n)+1))%p
  if not d:shift+=1;continue
  T=C[:];coef=d*pow(b,-1,p)%p
  C += [0]*max(0,len(B)+shift-len(C))
  for j in range(len(B)): C[j+shift]=(C[j+shift]-coef*B[j])%p
  if 2*L<=n:L=n+1-L;B=T;b=d;shift=1
  else:shift+=1
 return L,(C+[0]*(L+1-len(C)))[:L+1]

def evalpoly(c,z):
 ans=0
 for v in c[::-1]:ans=(ans*z+v)%p
 return ans

def recover(c,q,t):
 n=len(c);r,C=bm(c[:2*t])
 if r>t:return None
 if r==0:return [] if not any(c) else None
 if C[-1]==0:return None
 vals=fft(C+[0]*(n-len(C)),q);roots=[v for v,z in enumerate(vals) if z==0]
 if len(roots)!=r:return None
 A=[sum(C[i]*c[j-i] for i in range(j+1))%p for j in range(r)]
 deriv=[(i*C[i])%p for i in range(1,r+1)];freq=[0]*n;ans=[]
 for v in roots:
  z=pow(q,v,p);lam=pow(z,-1,p);den=evalpoly(deriv,z)
  if not den:return None
  g=-lam*evalpoly(A,z)*pow(den,-1,p)%p
  if not g:return None
  u=(-v)%n;freq[u]=g;ans.append((u,g))
 return ans if fft(freq,q)==c else None

exact=0;corrupt=0
for n in [8,16,32,64]:
 q=pow(3,(p-1)//n,p);assert pow(q,n,p)==1 and pow(q,n//2,p)!=1
 for t in range(1,min(5,n//2)+1):
  for r in range(t+1):
   for trial in range(3):
    supp=R.sample(range(n),r);f=[0]*n
    for u in supp:f[u]=R.randrange(1,p)
    c=fft(f,q);a=recover(c,q,t);assert a is not None and dict(a)=={u:f[u] for u in supp};exact+=1
    cc=c[:];cc[-1]=(cc[-1]+1)%p
    actual=fft(cc,pow(q,-1,p));want=sum(v!=0 for v in actual)<=t
    assert (recover(cc,q,t) is not None)==want;corrupt+=1

profiles=[]
for sizes in [[3,2,1],[4,1],[2,2,2],[1,1,1]]:
 exponents=sorted(k for m in sizes for k in range(m));n=sum(sizes);ratios=[]
 for eps in [0.02,0.01,0.005]:
  nodes=[complex(2*a,0.3*a)+eps*(j+1)+eps*eps*(j+1)**2*0.2j for a,m in enumerate(sizes) for j in range(m)]
  V=np.array([[z**k for z in nodes] for k in range(n)],complex)
  sv=np.linalg.svd(V,compute_uv=False);ratios.append((sv/np.power(eps,exponents)).tolist())
 assert min(min(x) for x in ratios)>1e-9
 # ratio change is bounded on these three scales; only a falsification check.
 assert max(max(x) for x in ratios)/min(min(x) for x in ratios)<1e10
 profiles.append({'sizes':sizes,'exponents':exponents,'scaled_singular_values':ratios})

interpolation=[]
for n,s in [(17,2),(31,2),(65,3),(129,3)]:
 M=1<<(4*n-1).bit_length();L=M//4;q=M//(8*s);h=16*s+1
 assert 2*h+2<M and M>=16*s
 ell=np.arange(n);ks=np.arange(M);a=(n-1)//2
 t=ell[:,None]/n-ks[None,:]/M;t=(t+0.5)%1-0.5
 K=((2*L+1)/M)*np.sinc((2*L+1)*t)/np.sinc(t)*(np.sinc((2*q+1)*t)/np.sinc(t))**s
 B=np.sqrt(M/n)*K;D=np.exp(-2j*np.pi*a*ell/n)
 x=np.array([R.random()+1j*R.random() for _ in range(n)]);v=np.zeros(M,complex);v[(np.arange(n)-a)%M]=x
 z=np.fft.fft(v)/np.sqrt(M);target=np.fft.fft(x)/np.sqrt(n)
 identity=np.max(np.abs(D*(B@z)-target));assert identity<1e-10
 rr=ell*M//n;offset=(ks[None,:]-rr[:,None])%M;mask=(offset<=h+1)|(offset>=M-h);Bh=B*mask
 sparse=np.zeros(M,complex)
 for k in R.sample(range(M),5):sparse[k]=R.random()+1j*R.random()
 out=np.zeros(n,complex);inc=0
 for k in np.flatnonzero(sparse):
  seen=set()
  for wrap in [-1,0,1]:
   lo=max(0,math.ceil((k+wrap*M-h-2)*n/M));hi=min(n-1,math.floor((k+wrap*M+h+2)*n/M))
   for l in range(lo,hi+1):
    if l in seen:continue
    seen.add(l);d=(k-(l*M//n))%M
    if d<=h+1 or d>=M-h:out[l]+=B[l,k]*sparse[k];inc+=1
 scatter=np.max(np.abs(out-Bh@sparse));assert scatter<1e-11
 E=B-Bh;schur=math.sqrt(np.max(np.sum(abs(E),axis=0))*np.max(np.sum(abs(E),axis=1)))
 assert schur<=12*4**(-s)+1e-12
 interpolation.append({'N':n,'M':M,'s':s,'identity_error':float(identity),'sparse_scatter_error':float(scatter),'incidences':inc,'schur_tail_bound':schur,'theoretical_tail_bound':12*4**(-s)})

res={'status':'PASS','scope':'Small independent falsification checks only; not a benchmark, HIKP execution, or numerical implementation theorem.','supplied_programs_executed':False,'exact_modal_accept_cases':exact,'corrupted_suffix_classification_cases':corrupt,'singular_profiles':profiles,'sparse_interpolation_cases':interpolation}
Path(__file__).with_name('fresh_controls_results.json').write_text(json.dumps(res,indent=2)+'\n')
print(json.dumps({k:v for k,v in res.items() if k not in ['singular_profiles','sparse_interpolation_cases']},indent=2))
