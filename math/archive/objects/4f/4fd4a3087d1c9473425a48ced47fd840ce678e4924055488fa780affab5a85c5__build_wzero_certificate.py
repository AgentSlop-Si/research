from sympy import QQ,sqrt,I
from sympy.polys.fields import field
from sympy.polys.rings import ring
import json
from pathlib import Path
OUT=Path(__file__).resolve().parent
K=QQ.algebraic_field(sqrt(2)*(1+I)/2);z=K.unit
FF,d=field('d',K);RR=D=d.numer.ring;pp=d.numer
sig=(2,7,5,0,6,1,3,4)
def matrix(t):return [[FF(z**((2*(j//2)*r)%8))+(-1)**j*t[j//2]*FF(z**(((2*(j//2)+1)*r)%8)) for j in range(8)] for r in range(8)]
def minor(M,r,j):return M[0][sig[j]]*M[r][j]-M[0][j]*M[r][sig[j]]
def resultant(M,r,j,k):
 b=lambda j:minor(M,r,j)
 c=lambda j:minor(M,r-1,j)
 return b(j)*c(k)-b(k)*c(j)
def encode(p):
 return [[list(m),[str(x) for x in reversed(c.to_list())]] for m,c in sorted(p.items())]
def rational(f):return {'numer':encode(f.numer),'denom':encode(f.denom)}
def gcdcert(a,b):
 S,T,G=a.gcdex(b);assert G==a.ring.one and S*a+T*b==a.ring.one
 return {'left':encode(a),'right':encode(b),'s':encode(S),'t':encode(T)}
def txt(p):
 return str(p.as_expr()).replace('sqrt(2)','sqrt(2)')
# h_16 is linear in t1; h_14 is linear in t2.
base=[FF(0),FF(0),FF(0),d]
M=matrix(base)
D6=minor(M,1,6);D4=minor(M,1,4)
b1=base.copy();b1[1]=FF(1);A6=minor(matrix(b1),1,6)-D6
b2=base.copy();b2[2]=FF(1);A4=minor(matrix(b2),1,4)-D4
c6=gcdcert(A6.numer,D6.numer);c4=gcdcert(A4.numer,D4.numer)
b=-D6/A6;c=-D4/A4
base=[FF(0),b,c,d];qf=minor(matrix(base),1,2);Q=qf.numer.monic()
P0=resultant(matrix(base),2,4,5);base[0]=FF(1);P1=resultant(matrix(base),2,4,5)
A0=P1-P0
c0=gcdcert(Q,A0.numer)
a=-P0/A0
M=matrix([a,b,c,d]);hf=resultant(M,3,1,4);H=hf.numer.monic()
final=gcdcert(Q,H)
cert={'field':'Q[z]/(z^4+1)','variable':'d=t3','source_minors':[[1,2],[1,4],[1,6]],'source_resultants':[[2,4,5],[3,1,4]],'A6':rational(A6),'D6':rational(D6),'A4':rational(A4),'D4':rational(D4),'A6_D6_bezout':c6,'A4_D4_bezout':c4,'t1':rational(b),'t2':rational(c),'q_fraction':rational(qf),'Q':encode(Q),'P0':rational(P0),'A0':rational(A0),'Q_A0_bezout':c0,'t0':rational(a),'h_fraction':rational(hf),'H':encode(H),'Q_H_bezout':final}
(OUT/'WZERO_CERTIFICATE.json').write_text(json.dumps(cert,indent=2)+'\n')
for k,p in [('A6',A6.numer),('D6',D6.numer),('A4',A4.numer),('D4',D4.numer),('Q',Q),('A0 numerator',A0.numer),('H',H)]:print(k,txt(p),flush=True)
print('DEGREES',Q.degree(),H.degree(),'FINAL BEZOUT',final,flush=True)
