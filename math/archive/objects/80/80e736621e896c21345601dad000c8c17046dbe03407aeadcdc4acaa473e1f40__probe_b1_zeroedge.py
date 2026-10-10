from sympy import QQ,sqrt,I,Poly,groebner
from sympy.polys.fields import field
K=QQ.algebraic_field(sqrt(2)*(1+I)/2);z=K.unit
F,d,w=field('d,w',K);sig=(2,7,5,0,6,1,3,4)
def matrix(t):return [[F(z**((2*(j//2)*r)%8))+(-1)**j*t[j//2]*F(z**(((2*(j//2)+1)*r)%8)) for j in range(8)] for r in range(8)]
t=[(1+w)/(1+w*F(z**7)),-(1+w*F(z**6))/(1+w*F(z**5)),(1+w*F(z**4))/(1+w*F(z**3)),d];M=matrix(t);B=[M[0][j]+w*M[7][j] for j in range(8)]
b=lambda r,j:B[sig[j]]*M[r][j]-B[j]*M[r][sig[j]]
c=lambda r,j:B[sig[j]]*M[r-1][j]-B[j]*M[r-1][sig[j]]
R=lambda r,j,k:b(r,j)*c(r,k)-b(r,k)*c(r,j)
E=lambda r,j:b(r,j)*M[r-1][1]-c(r,j)*M[r][1]
# All these factors are nonzero from t0,t1,t2!=0 and B4+v4 B6=0.
guard=[w.numer,(1+w).numer,(1+w*F(z**7)).numer,(1+w*F(z**6)).numer,(1+w*F(z**5)).numer,(1+w*F(z**4)).numer,(1+w*F(z**3)).numer,B[6].numer]
P=[]
for tag,f in [('R146',R(1,4,6)),('R246',R(2,4,6)),('E34',E(3,4)),('E46',E(4,6)),('E56',E(5,6))]:
 p=f.numer
 for g in guard:
  while p and max(map(sum,(h:=p.gcd(g)).keys()))>0:p=p.exquo(h)
 pp=Poly.from_dict(p.to_dict(),p.ring.symbols,domain=K);P.append(pp)
 print(tag,'terms',len(p),'degree',max(map(sum,p.keys())),str(pp.as_expr()),flush=True)
 G=groebner(P,*p.ring.symbols,domain=K)
 print('basis',G,flush=True)
 if list(G)==[1]:break
