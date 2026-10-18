import sympy as s,numpy as np,json
from pathlib import Path
D,E=s.symbols('D E');a=6;b=4;p=17

def numerator(e):return s.Poly(s.cancel(e).as_numer_denom()[0],D,E,modulus=p)
def pack(poly):return [[list(m),int(c)%p] for m,c in poly.terms() if int(c)%p]
def monoms(n):return [(i,j) for k in range(n+1) for i in range(k,-1,-1) for j in [k-i]]
def certificate(fs,target):
 for cap in range(max(f.total_degree() for f in fs),22):
  mons=monoms(cap);ix={m:i for i,m in enumerate(mons)};rows=[];labels=[]
  for j,f in enumerate(fs):
   for m in monoms(cap-f.total_degree()):
    row=np.zeros(len(mons),dtype=np.int64)
    for ex,c in f.terms():row[ix[(ex[0]+m[0],ex[1]+m[1])]]=int(c)%p
    rows.append(row);labels.append((j,m))
  A=np.array(rows,dtype=np.int64).T;t=np.zeros(len(mons),dtype=np.int64)
  for m,c in target.terms():t[ix[m]]=int(c)%p
  M=np.c_[A,t];pivs=[];rr=0
  for col in range(A.shape[1]):
   nz=np.flatnonzero(M[rr:,col])
   if len(nz)==0:continue
   z=rr+int(nz[0]);M[[rr,z]]=M[[z,rr]];M[rr]=(M[rr]*pow(int(M[rr,col]),-1,p))%p
   rowsnz=np.flatnonzero(M[:,col]);rowsnz=rowsnz[rowsnz!=rr]
   M[rowsnz]=(M[rowsnz]-M[rowsnz,col,None]*M[rr])%p
   pivs.append(col);rr+=1
   if rr==M.shape[0]:break
  if any(not np.any(row[:-1]) and row[-1] for row in M):continue
  sol=np.zeros(A.shape[1],dtype=np.int64)
  for r,col in enumerate(pivs):sol[col]=M[r,-1]
  assert np.array_equal((A@sol)%p,t)
  hs=[s.Poly(0,D,E,modulus=p) for _ in fs]
  for c,(j,m) in zip(sol,labels):
   if c:hs[j]+=s.Poly(int(c)*D**m[0]*E**m[1],D,E,modulus=p)
  check=sum((h*f for h,f in zip(hs,fs)),s.Poly(0,D,E,modulus=p))
  assert check==target
  return dict(degree_cap=cap,inputs=[pack(f) for f in fs],target=pack(target),multipliers=[pack(h) for h in hs])
 raise RuntimeError('no certificate')

h=D/(D+a*E);A=a*h/E;B=-a*h/D;C=(b*h-E)/D;F=E*(s.Rational(b,a)+1/D)
f330=[numerator(A+C*E+F-a*h),numerator(C+D+B*F+a*h),numerator(A*D+C*F-h)]
R=1-E**2-D**2*E;A=D**3/R;C=-D-A*E;B=E-D**2-A*D*E
u=A*D;v=B;r=-B*D;t=-A*E
lin=[(v-b*u,u-b*v),(r+t,r-t),(r-a*u,-t-a*v)]
f312=[numerator(1+B*E-A*D)]+[numerator(lin[i][0]*lin[j][1]-lin[i][1]*lin[j][0]) for i,j in [(0,1),(0,2),(1,2)]]
certs={'modulus':17,'root_zeta':3,'a':6,'b':4,'330':certificate(f330,s.Poly(E**2,D,E,modulus=p)),'312':certificate(f312,s.Poly(D**6,D,E,modulus=p))}
path=Path(__file__).parent/'CERTIFICATES.json';path.write_text(json.dumps(certs,indent=2)+'\n')
print({name:(certs[name]['degree_cap'],[len(v) for v in certs[name]['multipliers']]) for name in ['330','312']})
# Exact one-variable Bezout certificates. Each gcd is 1 over F17[D].
BB=-2*D**2/(1+D**4);AA=2*D**3/(1+D**4);HH=D*(D**4-1)/(1+D**4)
ee=(b-BB)/(1-b*BB)
EE=b+a*D+a/D;hh=D/(D+a*EE)
univs={
 '510':[a*D**2-D+a,b*D**4+a*D**3+D**2+a*D+b],
 '420':[EE-D**2-hh*(a*D+b),a/EE-a*EE-D*EE/hh-a],
 '411':[AA+HH+(AA-HH)*ee,AA-HH*ee-a*(1+BB*ee)]}
for name,expressions in univs.items():
 fs=[s.Poly(s.cancel(e).as_numer_denom()[0],D,modulus=p) for e in expressions]
 u,v,g=s.gcdex(*fs);assert g==s.Poly(1,D,modulus=p)
 fs2=[s.Poly(f.as_expr(),D,E,modulus=p) for f in fs];hs=[s.Poly(f.as_expr(),D,E,modulus=p) for f in [u,v]]
 certs[name]={'inputs':[pack(f) for f in fs2],'target':pack(s.Poly(1,D,E,modulus=p)),'multipliers':[pack(h) for h in hs]}
path.write_text(json.dumps(certs,indent=2)+'\n')
