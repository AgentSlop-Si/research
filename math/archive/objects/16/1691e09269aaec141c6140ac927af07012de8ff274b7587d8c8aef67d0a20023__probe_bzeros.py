from sympy import QQ,sqrt,I
from sympy.polys.fields import field
from sympy.polys.rings import ring
import json
K=QQ.algebraic_field(sqrt(2)*(1+I)/2);z=K.unit
F,w=field('w',K);sig=(2,7,5,0,6,1,3,4);J=(1,2,4,5,6)
def matrix(t):return [[F(z**((2*(j//2)*r)%8))+(-1)**j*t[j//2]*F(z**(((2*(j//2)+1)*r)%8)) for j in range(8)] for r in range(8)]
def B(M):return [M[0][j]+w*M[7][j] for j in range(8)]
def resultant(M,r,j,k):
 bb=B(M);b=lambda j:bb[sig[j]]*M[r][j]-bb[j]*M[r][sig[j]];c=lambda j:bb[sig[j]]*M[r-1][j]-bb[j]*M[r-1][sig[j]]
 return b(j)*c(k)-b(k)*c(j)
def text(p):
 out=[]
 for m,c in sorted(p.items()):
  cc=' + '.join(str(q)+('*z^'+str(i) if i else '') for i,q in enumerate(reversed(c.to_list())) if q)
  out.append('('+cc+')*w^'+str(m[0]))
 return ' + '.join(out)
t=[(1+w)/(1+w*F(z**7)),-(1+w*F(z**6))/(1+w*F(z**5)),(1+w*F(z**4))/(1+w*F(z**3)),(1+w*F(z**2))/(1+w*F(z))]
M=matrix(t);print('B',[(j,str(x)) for j,x in enumerate(B(M)) if x==0],flush=True)
g=None
for r in range(1,8):
 E=[j for j in J if r not in {j,(j+1)%8,sig[j]}]
 for ix,j in enumerate(E):
  for k in E[ix+1:]:
   f=resultant(M,r,j,k)
   if not f:continue
   g=f.numer if g is None else g.gcd(f.numer)
   print('R',r,j,k,'degree',f.numer.degree(),'gcd',text(g.monic()),flush=True)
