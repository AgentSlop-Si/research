from sympy import QQ,sqrt,I
from sympy.polys.fields import field
from pathlib import Path
import json
OUT=Path(__file__).resolve().parent
K=QQ.algebraic_field(sqrt(2)*(1+I)/2);z=K.unit
F,w=field('w',K);sig=(2,7,5,0,6,1,3,4)
def matrix(a,b):
 t=[a,b,-(1+w*F(z**4))/(1+w*F(z**3)),-(1+w*F(z**2))/(1+w*F(z))]
 return [[F(z**((2*(j//2)*r)%8))+(-1)**j*t[j//2]*F(z**(((2*(j//2)+1)*r)%8)) for j in range(8)] for r in range(8)]
def bs(M):return [M[0][j]+w*M[7][j] for j in range(8)]
def bc(M,r,j):
 B=bs(M);return B[sig[j]]*M[r][j]-B[j]*M[r][sig[j]],B[sig[j]]*M[r-1][j]-B[j]*M[r-1][sig[j]]
def res(M,r,j,k):
 b,c=bc(M,r,j);bb,cc=bc(M,r,k);return b*cc-bb*c
def edge(M,r,j):
 b,c=bc(M,r,j);return b*M[r-1][6]-c*M[r][6]
def encode(p):return [[list(m),[str(x) for x in reversed(c.to_list())]] for m,c in sorted(p.items())]
def rational(f):return {'numer':encode(f.numer),'denom':encode(f.denom)}
def bez(a,b):
 S,T,G=a.gcdex(b);assert S*a+T*b==G
 return {'left':encode(a),'right':encode(b),'s':encode(S),'t':encode(T),'gcd':encode(G)}
D1=edge(matrix(F(0),F(0)),1,2);A1=edge(matrix(F(0),F(1)),1,2)-D1
c1=bez(A1.numer,D1.numer);print('gcd t1 pivot',c1['gcd'],flush=True)
b=-D1/A1
D0=edge(matrix(F(0),b),2,5);A0=edge(matrix(F(1),b),2,5)-D0
c0=bez(A0.numer,D0.numer);print('gcd t0 pivot',c0['gcd'],flush=True)
a=-D0/A0;M=matrix(a,b)
g=None;acc=[]
for tag,f in [('E41',edge(M,4,1)),('E42',edge(M,4,2)),('E45',edge(M,4,5)),('E51',edge(M,5,1)),('R315',res(M,3,1,5)),('R725',res(M,7,2,5))]:
 if not f:print(tag,'zero',flush=True);continue
 p=f.numer.monic();g=p if g is None else g.gcd(p)
 acc.append((tag,f));print(tag,'degree',p.degree(),'gcd',encode(g),flush=True)
 if g==g.ring.one:break
cert={'field':'Q[z]/(z^4+1)','variable':'w=u0','A1':rational(A1),'D1':rational(D1),'A1_D1_bezout':c1,'t1':rational(b),'A0':rational(A0),'D0':rational(D0),'A0_D0_bezout':c0,'t0':rational(a),'equations':[{'name':tag,'fraction':rational(f)} for tag,f in acc]}
if len(acc)==2:cert['final_bezout']=bez(acc[0][1].numer,acc[1][1].numer)
(OUT/'B6_ZEROEDGE_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
