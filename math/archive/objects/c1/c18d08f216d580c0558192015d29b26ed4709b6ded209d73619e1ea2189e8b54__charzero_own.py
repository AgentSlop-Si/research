from fractions import Fraction as Q
from pathlib import Path
import json
import independent_phase38 as m
class C:
 def __init__(self,a=0,b=0):self.a,self.b=(a.a,a.b) if isinstance(a,C) else (Q(a),Q(b))
 def __bool__(self):return bool(self.a or self.b)
 def __eq__(self,o):o=C(o);return self.a==o.a and self.b==o.b
 def __add__(self,o):o=C(o);return C(self.a+o.a,self.b+o.b)
 __radd__=__add__
 def __neg__(self):return C(-self.a,-self.b)
 def __sub__(self,o):return self+-C(o)
 def __rsub__(self,o):return C(o)+-self
 def __mul__(self,o):o=C(o);return C(self.a*o.a-self.b*o.b,self.a*o.b+self.b*o.a)
 __rmul__=__mul__
 def inv(self):n=self.a*self.a+self.b*self.b;assert n;return C(self.a/n,-self.b/n)
 def __truediv__(self,o):return self*C(o).inv()
 def __rtruediv__(self,o):return C(o)*self.inv()
 def __pow__(self,n):
  if n<0:return self.inv()**(-n)
  a=self;b=C(1)
  while n:
   if n&1:b=b*a
   a=a*a;n//=2
  return b
 def data(self):return [str(self.a),str(self.b)]
def mm(A,B):return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def inv(A):
 n=len(A);X=[r[:]+[C(i==j) for j in range(n)] for i,r in enumerate(A)]
 for j in range(n):
  k=next(k for k in range(j,n) if X[k][j]);X[k],X[j]=X[j],X[k];s=X[j][j];X[j]=[x/s for x in X[j]]
  for k in range(n):
   if k!=j:s=X[k][j];X[k]=[x-s*y for x,y in zip(X[k],X[j])]
 return [r[n:] for r in X]
n=4;I=C(0,1);F=[[I**(i*j) for j in range(n)] for i in range(n)]
alphas=[C(a,b)/d for a,b,d in [(1,1,4),(2,1,7),(1,2,8),(1,-1,5),(2,1,9),(1,1,6)]];G=[]
for order,a in zip(m.orders(n),alphas):
 pos={j:i for i,j in enumerate(order)};G.append([[a**((pos[i]-pos[j])%n)/(1-a**n) for j in range(n)] for i in range(n)])
A=[[G[0][i][j]+(1+I)/3*G[1][i][j] for j in range(n)] for i in range(n)];D=[[G[4][i][j]+(1-I)/4*G[5][i][j] for j in range(n)] for i in range(n)]
T=mm(mm(inv(A),F),inv(D));polys=[]
def prod(a,b):return [a[0]*b[0],a[0]*b[1]+a[1]*b[0],a[1]*b[1]]
for j in [1,2]:
 aa=prod([G[2][1][0],G[3][1][0]],[G[2][0][j],G[3][0][j]])
 bb=prod([G[2][1][j],G[3][1][j]],[G[2][0][0],G[3][0][0]])
 polys.append([T[1][j]*T[0][0]*x-T[1][0]*T[0][j]*y for x,y in zip(aa,bb)])
a,b=polys;res=(a[2]*b[0]-a[0]*b[2])**2-(a[2]*b[1]-a[1]*b[2])*(a[1]*b[0]-a[0]*b[1]);assert res and a[2] and b[2]
# Both modular images of the exact rational coefficients agree with independent finite source data.
checks=[]
for p,gen in [(998244353,3),(2013265921,31)]:
 ii=pow(gen,(p-1)//4,p)
 def reduce(x):return (x.a.numerator*pow(x.a.denominator,-1,p)+x.b.numerator*pow(x.b.denominator,-1,p)*ii)%p
 aa,cc,ff,gg,hh=m.kernels(4,p);target=m.mm(m.mm(m.inv(aa,p),ff,p),m.inv(cc,p),p);want=m.gate(target,gg,hh,[0,1,0,1,2],p);assert [[reduce(x) for x in f] for f in polys]==want;checks.append({'prime':p,'resultant':reduce(res)})
Path('CHARZERO_RESULTS.json').write_text(json.dumps({'status':'PASS','field':'Q(i)','degrees':[2,2],'gcd_degree':0,'polynomials':[[x.data() for x in f] for f in polys],'nonzero_resultant':res.data(),'modular_consistency':checks},indent=2)+'\n');print('Q(i) exact nonzero resultant and both modular reductions PASS')
