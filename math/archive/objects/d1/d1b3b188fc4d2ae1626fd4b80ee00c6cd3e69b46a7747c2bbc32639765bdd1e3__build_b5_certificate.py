from sympy import QQ,sqrt,I
from sympy.polys.fields import field
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
K=QQ.algebraic_field(sqrt(2)*(1+I)/2);z=K.unit
F,w=field('w',K);sig=(2,7,5,0,6,1,3,4)
def matrix(d):
 t=[F(0),-(1+w*F(z**6))/(1+w*F(z**5)),(1+w*F(z**4))/(1+w*F(z**3)),d]
 return [[F(z**((2*(j//2)*r)%8))+(-1)**j*t[j//2]*F(z**(((2*(j//2)+1)*r)%8)) for j in range(8)] for r in range(8)]
def bs(M):return [M[0][j]+w*M[7][j] for j in range(8)]
def bc(M,r,j):
 B=bs(M);return B[sig[j]]*M[r][j]-B[j]*M[r][sig[j]],B[sig[j]]*M[r-1][j]-B[j]*M[r-1][sig[j]]
def res(M,r,j,k):
 b,c=bc(M,r,j);bb,cc=bc(M,r,k);return b*cc-bb*c
def edge(M,r,j):
 b,c=bc(M,r,j);return b*M[r-1][5]-c*M[r][5]
def encode(p):return [[list(m),[str(x) for x in reversed(c.to_list())]] for m,c in sorted(p.items())]
def rational(f):return {'numer':encode(f.numer),'denom':encode(f.denom)}
def bez(a,b):
 S,T,G=a.gcdex(b);assert S*a+T*b==G
 return {'left':encode(a),'right':encode(b),'s':encode(S),'t':encode(T),'gcd':encode(G)}
def f(d):
 M=matrix(d);return res(M,1,4,6)/(w*bs(M)[6])
D=f(F(0));A=f(F(1))-D;d=-D/A;M=matrix(d)
f2=res(M,2,4,6)/bs(M)[6];Q=f2.numer.monic()
for r,j in [(2,4),(2,6),(3,4),(4,6),(7,4)]:
 hf=edge(M,r,j);H=hf.numer.monic();c=bez(Q,H)
 print('edge',r,j,'Qdegree',Q.degree(),'Hdegree',H.degree(),'gcd',c['gcd'],flush=True)
 if c['gcd']==[[[0],['1']]]:
  cert={'field':'Q[z]/(z^4+1)','variable':'w=u0','edge_minor':[r,j],'A':rational(A),'D':rational(D),'A_D_bezout':bez(A.numer,D.numer),'t3':rational(d),'q_fraction':rational(f2),'Q':encode(Q),'h_fraction':rational(hf),'H':encode(H),'Q_H_bezout':c};(OUT/'B5_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n');break
