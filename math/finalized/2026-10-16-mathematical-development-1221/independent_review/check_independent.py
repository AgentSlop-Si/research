import numpy as np,json,itertools
results={'q2':[],'q29':[],'materialization':[]}
for m in [2,3,5,7,9]:
 n=m*m;q=np.exp(2j*np.pi/m);lam=2.**(-(4+m*(2*m-1).bit_length()));I=np.eye(n,dtype=complex);L=I.copy()
 for a in range(m):
  for c in range(m):
   L[a*m+c,((a-1)%m)*m+c]-=.25
   L[a*m+c,a*m+(c-1)%m]-=.25*q**a
 phi=[(-c%m)*m+(a+c)%m for a in range(m) for c in range(m)]
 M=L[np.ix_(phi,phi)];K=M+lam*L;S=np.linalg.inv(L)+lam*np.linalg.inv(M)
 assert np.linalg.norm(S@M@np.linalg.inv(K)@L-I)<1e-10
 U=np.roll(np.eye(m,dtype=complex),1,axis=0);Q=np.diag([q**(-c) for c in range(m)]);R=(U.T+Q+lam*np.eye(m))/4
 E=np.eye(m,dtype=complex)
 for a in range(m):E=np.linalg.solve((1+lam)*np.eye(m)-lam*q**a*U/4,R)@E
 assert np.linalg.norm(E,2)<=2**(-m)+1e-12
 assert np.linalg.cond(np.eye(m)-E)<=5/3+1e-12
 C=I-K/(1+lam);f=np.arange(n)+1j*np.arange(n)[::-1];h=L@f/(1+lam);y=np.zeros(n,complex)
 for k in range(1,18):
  y=h+C@y;x=M@y;exact=np.linalg.solve(S,f)
  err=np.linalg.norm(x-exact)/np.linalg.norm(exact)
  assert err<=20*2**(-k)+1e-12
 results['q2'].append({'m':m,'boundary_norm':float(np.linalg.norm(E,2)),'condition':float(np.linalg.cond(np.eye(m)-E)),'stationary17_relative_error':float(err)})
for N in [10,11,15,27,101]:
 t=np.pi/(2*N);s=np.sin(3*t)/(1-np.sin(t));l=np.cos(3*t)+s*np.cos(t);e=np.exp(1j*(-np.pi/2+5*t));la=e*l
 a=np.array([e*np.exp(-3j*t),s*e*np.exp(-1j*t),s*e*np.exp(1j*t),e*np.exp(3j*t)])
 assert abs(sum(a)-2*la)<1e-12
 assert abs(a[0]*a[2]+a[0]*a[3]+a[1]*a[3]-la**2)<1e-12
 assert abs((la-a[0]-a[1])**2+a[1]*a[2])<1e-12
 results['q29'].append({'N':N,'kernel_error':float(abs((la-a[0]-a[1])**2+a[1]*a[2]))})
groups=[{0,1},{0,2},{1,3}]
def saving(S):
 best=0
 for mask in range(1<<len(S)):
  T=[groups[S[i]] for i in range(len(S)) if mask>>i&1]
  best=max(best,2*len(set().union(*T))-3*len(T))
 return best
values=[saving(S) for S in [[0],[0,1],[0,2],[0,1,2]]]
assert values==[1,1,1,2];results['materialization']=values
results['scope']='Independent numerical transcription controls only; root separately checked algebraic proofs. No uniform theorem follows from these tests.'
print(json.dumps(results,indent=2))
