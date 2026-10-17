"""Fresh independent exact checks. Written for this audit; no archived code imported.
Use q=w(1+t), arithmetic in Q(w)[t]/(t^N), and the Bezout determinant
for the ordinary discriminant of the reciprocal reduction of H_n.
"""
import sympy as s, math, time, json, sys
from pathlib import Path
OUT=Path(__file__).parent
class Calc:
 def __init__(self,d,N):
  q,w=s.symbols('q w'); self.wsymbol=w
  self.K=s.QQ.algebraic_field((s.Poly(s.cyclotomic_poly(d,q),q),w)); self.w=self.K.unit
  self.zero=self.K.zero; self.one=self.K.one; self.N=N; self.d=d
 def trim(self,a):
  while a and a[-1]==self.zero:a.pop()
  return a
 def add(self,a,b):
  return self.trim([(a[i] if i<len(a) else self.zero)+(b[i] if i<len(b) else self.zero) for i in range(max(len(a),len(b)))])
 def neg(self,a):return [-x for x in a]
 def sub(self,a,b):return self.add(a,self.neg(b))
 def scale(self,a,k):return self.trim([x*k for x in a]) if k else []
 def mul(self,a,b):
  if not a or not b:return []
  c=[self.zero]*min(self.N,len(a)+len(b)-1)
  for i,x in enumerate(a):
   if x:
    for j,y in enumerate(b[:self.N-i]):
     if y:c[i+j]+=x*y
  return self.trim(c)
 def val(self,a):
  return next((i for i,x in enumerate(a) if x),self.N)
 def inv_unit(self,a,prec):
  ai=self.one/a[0]; r=[ai]
  for k in range(1,prec):
   v=self.zero
   for j in range(1,min(len(a),k+1)):v+=a[j]*r[k-j]
   r.append(-v*ai)
  return self.trim(r)
 def zadd(self,a,b):
  return [self.add(a[i] if i<len(a) else [],b[i] if i<len(b) else []) for i in range(max(len(a),len(b)))]
 def H(self,n):
  one=[self.one]; h0=[one]; h1=[one,one]
  if n==0:return h0
  for k in range(1,n):
   qk=[self.w**k*math.comb(k,j) for j in range(min(k+1,self.N))]
   term=[[]]+[self.mul(x,self.sub(one,qk)) for x in h0]
   nxt=self.zadd(h1,[[]]+h1)
   h0,h1=h1,[self.sub(nxt[i],term[i] if i<len(term) else []) for i in range(len(nxt))]
  return h1
 def reciprocal(self,h):
  n=len(h)-1
  if n%2:
   # Exact polynomial division by z+1, constant coefficient first.
   t=[h[0]]
   for i in range(1,n):t.append(self.sub(h[i],t[-1]))
   assert t[-1]==h[-1]
  else:t=h
  m=(len(t)-1)//2
  assert t==t[::-1]
  S0=[2]; S1=[0,1]; pols=[S0,S1]
  for j in range(2,m+1):
   p=[0]+pols[-1]; prev=pols[-2]
   for i,v in enumerate(prev):p[i]-=v
   pols.append(p)
  r=[[] for _ in range(m+1)];r[0]=t[m]
  for j in range(1,m+1):
   for i,v in enumerate(pols[j]):r[i]=self.add(r[i],self.scale(t[m+j],v))
  return r
 def eval(self,f,x):
  ans=[]
  for a in f[::-1]:ans=self.add(self.scale(ans,x),a)
  return ans
 def bezout(self,f):
  m=len(f)-1;b=[self.scale(f[j+1],j+1) for j in range(m)]+[[]]
  B=[[[] for _ in range(m)]for _ in range(m)]
  for i in range(1,m+1):
   for j in range(i):
    a=self.sub(self.mul(f[i],b[j]),self.mul(f[j],b[i]))
    for k in range(i-j):B[i-1-k][j+k]=self.add(B[i-1-k][j+k],a)
  return B
 def det(self,A):
  n=len(A);ans=[self.one];pivots=[]
  for k in range(n):
   v,i,j=min((self.val(A[i][j]),i,j) for i in range(k,n) for j in range(k,n))
   if v==self.N:return [],pivots
   if i!=k:A[i],A[k]=A[k],A[i];ans=self.neg(ans)
   if j!=k:
    for row in A:row[j],row[k]=row[k],row[j]
    ans=self.neg(ans)
   p=A[k][k];pivots.append(v);ans=self.mul(ans,p)
   inv=self.inv_unit(p[v:],self.N-v)
   for i in range(k+1,n):
    if not A[i][k]:continue
    assert self.val(A[i][k])>=v
    ratio=self.mul(A[i][k][v:],inv)[:self.N-v]
    for j in range(k+1,n):A[i][j]=self.sub(A[i][j],self.mul(ratio,A[k][j]))
   print(' pivot',k,'valuation',v,'elapsed',round(time.time()-START,2),flush=True)
  return ans,pivots
 def constpoly(self,f,z):
  return s.Poly.from_list([a[0] if a else self.zero for a in f[::-1]],z,domain=self.K)
 def expected(self,A,b):
  z,x=s.symbols('z x'); G=self.constpoly(self.H(b),z);F=s.Poly(1+z**self.d,z,domain=self.K)
  PA=math.prod(j**j for j in range(1,A+1));sgn=(-1)**(A*(self.d-1)//2)
  if not b%2:
   C=sgn*self.d**(self.d*A*(A+1)//2)*PA**self.d*(G.rep.discriminant() if G.degree()>1 else self.one)*F.rep.resultant(G.rep)**(2*A)
   return C,{'g':None,'tau':None,'DiscJ':None}
  U=G.exquo(s.Poly(z+1,z,domain=self.K));g=U.rep.eval(self.K.convert(-1))
  W=self.one
  for j in range(1,b+1):W*=self.one-self.w**j
  for j in range(1,(self.d+b)//2+1):W/=self.one-self.w**(2*j)
  tau=self.d*W/g
  he=s.hermite_prob(A,x);hp=s.hermite_prob(A-1,x)
  j1=s.Poly(x*he,x);j2=s.Poly(hp,x);J=s.Poly.from_list([self.K.convert(j1.nth(i))-A*tau*self.K.convert(j2.nth(i)) for i in range(A+1,-1,-1)],x,domain=self.K)
  discJ=J.rep.discriminant();du=U.rep.discriminant() if U.degree()>1 else self.one;res=F.rep.resultant(U.rep)
  C=sgn*self.d**(self.d*A*(A+1)//2+A)*PA**(self.d-1)*discJ*du*res**(2*A)*g**2
  return C,{'g':str(self.K.to_sympy(g)),'tau':str(self.K.to_sympy(tau)),'DiscJ':str(self.K.to_sympy(discJ))}
 def expr(self,a):return str(self.K.to_sympy(a))

def run(d,A,b):
 global START
 START=time.time();n=d*A+b;M=d*A*(A-1)//2+A*(b%2);c=Calc(d,M+1)
 print('CASE',d,A,b,'n',n,'M',M,flush=True)
 h=c.H(n);r=c.reciprocal(h)
 print('constructed H and reciprocal R',len(r)-1,'elapsed',round(time.time()-START,2),flush=True)
 rp=c.eval(r,2);rm=c.eval(r,-2);vp=c.val(rp);vm=c.val(rm);em=3 if n%2 else 1
 assert vp<c.N and vm<c.N,'Boundary factor vanishes beyond available precision'
 target_disc_order=(M-vp-em*vm)//2
 assert target_disc_order>=0 and 2*target_disc_order+vp+em*vm==M
 # Only the needed leading term of Disc(R) is required. This avoids
 # computing many irrelevant higher Taylor coefficients in its square.
 c.N=target_disc_order+1
 r=[c.trim(a[:c.N]) for a in r]
 dr,piv=c.det(c.bezout(r));vd=c.val(dr)
 ordv=vp+em*vm+2*vd
 assert vd<c.N and ordv==M,(ordv,M)
 coeff=rp[vp]*rm[vm]**em*dr[vd]**2
 C,details=c.expected(A,b)
 assert coeff==C*d**M,'Coefficient mismatch'
 # Since q=w(1+t), Phi_d(q) has leading coefficient w Phi_d\'(w).
 q=s.symbols('q');phi=s.Poly(s.cyclotomic_poly(d,q),q)
 deriv=sum(c.K.convert(j*a)*c.w**j for (j,),a in phi.terms())
 p=min(k for k in range(2,d+1) if d%k==0)
 phi_quot=coeff/deriv**M;claimed_phi=C*(c.w**(d//p)-c.one)**M
 assert phi_quot==claimed_phi,'Phi conversion mismatch'
 result={'d':d,'A':A,'b':b,'n':n,'M':M,'ordinary_discriminant_order':ordv,'coefficient_t':c.expr(coeff),'C_qd_minus_one':c.expr(C),'coefficient_after_Phi_division':c.expr(phi_quot),'reciprocal_degree':len(r)-1,'bezout_pivot_valuations':piv,'boundary_orders_R2_Rminus2':[vp,vm],'order_DiscR':vd,'determinant_series_precision':c.N,'checks':'all exact assertions pass','elapsed_seconds':time.time()-START,**details}
 path=OUT/f'case_d{d}_A{A}_b{b}.json';path.write_text(json.dumps(result,indent=2)+'\n');print('PASS',path,'elapsed',round(time.time()-START,2),flush=True)
 return result
if __name__=='__main__':
 d,A,b=map(int,sys.argv[1:]);run(d,A,b)
