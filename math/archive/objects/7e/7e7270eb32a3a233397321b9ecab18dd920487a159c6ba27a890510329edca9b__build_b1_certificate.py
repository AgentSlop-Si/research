from sympy import QQ,sqrt,I
from sympy.polys.fields import field
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
K=QQ.algebraic_field(sqrt(2)*(1+I)/2);z=K.unit
F,w=field('w',K);sig=(2,7,5,0,6,1,3,4)
def matrix(d):
 t=[(1+w)/(1+w*F(z**7)),-(1+w*F(z**6))/(1+w*F(z**5)),(1+w*F(z**4))/(1+w*F(z**3)),d]
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
# R146/(w B6) is legal since u0 !=0 and B4=2(1-w)!=0 implies B6!=0.
def f(d):
 M=matrix(d);return res(M,1,4,6)/(w*bs(M)[6])
D=f(F(0));A=f(F(1))-D
print('A,D',text(A.numer),text(D.numer),flush=True)
c0=bez(A.numer,D.numer);print('gcdAD',c0['gcd'],flush=True)
d=-D/A;M=matrix(d)
f2=res(M,2,4,6)/bs(M)[6];f3=res(M,3,1,4)
Q=f2.numer.monic();H=f3.numer.monic();c1=bez(Q,H)
print('Qdegree',Q.degree(),'Hdegree',H.degree(),'gcd',c1['gcd'],flush=True)
print('t3',rational(d),flush=True)
cert={'field':'Q[z]/(z^4+1)','variable':'w=u0','A':rational(A),'D':rational(D),'A_D_bezout':c0,'t3':rational(d),'q_fraction':rational(f2),'Q':encode(Q),'h_fraction':rational(f3),'H':encode(H),'Q_H_bezout':c1}
(OUT/'B1_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
