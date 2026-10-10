from sympy import QQ,sqrt,I
from sympy.polys.fields import field
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
K=QQ.algebraic_field(sqrt(2)*(1+I)/2);z=K.unit
F,w=field('w',K);sig=(2,7,5,0,6,1,3,4)
def matrix(d):
 t=[d,(1+w*F(z**6))/(1+w*F(z**5)),-(1+w*F(z**4))/(1+w*F(z**3)),-(1+w*F(z**2))/(1+w*F(z))]
 return [[F(z**((2*(j//2)*r)%8))+(-1)**j*t[j//2]*F(z**(((2*(j//2)+1)*r)%8)) for j in range(8)] for r in range(8)]
def bs(M):return [M[0][j]+w*M[7][j] for j in range(8)]
def res(M,r,j,k):
 B=bs(M);b=lambda j:B[sig[j]]*M[r][j]-B[j]*M[r][sig[j]];c=lambda j:B[sig[j]]*M[r-1][j]-B[j]*M[r-1][sig[j]]
 return b(j)*c(k)-b(k)*c(j)
def encode(p):return [[list(m),[str(x) for x in reversed(c.to_list())]] for m,c in sorted(p.items())]
def rational(f):return {'numer':encode(f.numer),'denom':encode(f.denom)}
def bez(a,b):
 S,T,G=a.gcdex(b);assert S*a+T*b==G
 return {'left':encode(a),'right':encode(b),'s':encode(S),'t':encode(T),'gcd':encode(G)}
def text(p):return str(p.as_expr())
# B6=B3=B4=0. Legal guards imply B1 and B5 are nonzero.
def f(d):
 M=matrix(d);return res(M,3,1,5)/bs(M)[1]
D=f(F(0));A=f(F(1))-D
c0=bez(A.numer,D.numer);print('gcdAD',c0['gcd'],flush=True)
d=-D/A;M=matrix(d)
f2=res(M,4,2,5)/bs(M)[5];f3=res(M,7,2,5)/bs(M)[5]
Q=f2.numer.monic();H=f3.numer.monic();c1=bez(Q,H)
print('Qdegree',Q.degree(),'Hdegree',H.degree(),'gcd',c1['gcd'],flush=True)
cert={'field':'Q[z]/(z^4+1)','variable':'w=u0','A':rational(A),'D':rational(D),'A_D_bezout':c0,'t0':rational(d),'q_fraction':rational(f2),'Q':encode(Q),'h_fraction':rational(f3),'H':encode(H),'Q_H_bezout':c1}
(OUT/'B6_B3_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
