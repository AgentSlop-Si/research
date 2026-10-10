"""Fresh independent ring/multiplication-determinant controls.
No predecessor source is imported or executed. Coefficients: low degree first.
"""
import json, math, itertools, time, pathlib
import sympy as sp
HERE=pathlib.Path(__file__).resolve().parent
q=sp.Symbol('q')

class Ring:
 def __init__(self,d):
  self.d=d; self.f=sp.Poly(sp.cyclotomic_poly(d,q),q); self.m=self.f.degree()
  self.fc=[int(self.f.nth(i)) for i in range(self.m)]
  self.zero=(0,)*self.m; self.one=(1,)+(0,)*(self.m-1); self.ops={'add':0,'multiply':0}
 def elt(self,x):
  if isinstance(x,int): return (x,)+(0,)*(self.m-1)
  z=list(x)+[0]*max(0,self.m-len(x))
  for k in range(len(z)-1,self.m-1,-1):
   t=z[k]
   for j,a in enumerate(self.fc): z[k-self.m+j]-=t*a
  return tuple(z[:self.m])
 def add(self,a,b):
  self.ops['add']+=1; return tuple(x+y for x,y in zip(a,b))
 def neg(self,a): return tuple(-x for x in a)
 def sub(self,a,b): return self.add(a,self.neg(b))
 def mul(self,a,b):
  self.ops['multiply']+=1; z=[0]*(2*self.m-1)
  for i,x in enumerate(a):
   if x:
    for j,y in enumerate(b):
     if y:z[i+j]+=x*y
  return self.elt(z)
 def pow(self,a,n):
  out=self.one
  while n:
   if n&1:out=self.mul(out,a)
   a=self.mul(a,a);n//=2
  return out
 def scale(self,a,k):return tuple(k*x for x in a)
 def subst(self,a,k):
  out=self.zero
  for i,x in enumerate(a):
   if x:out=self.add(out,self.scale(self.pow(self.elt([0,1]),i*k),x))
  return out

def padd(A,B,R):
 return [R.add(A[i] if i<len(A) else R.zero,B[i] if i<len(B) else R.zero) for i in range(max(len(A),len(B)))]
def pmul(A,B,R):
 out=[R.zero]*(len(A)+len(B)-1)
 for i,a in enumerate(A):
  for j,b in enumerate(B):out[i+j]=R.add(out[i+j],R.mul(a,b))
 return out
def prem(A,P,R):
 A=A[:]
 while len(A)>=len(P):
  c=A[-1];k=len(A)-len(P)
  for j in range(len(P)):A[j+k]=R.sub(A[j+k],R.mul(c,P[j]))
  assert A[-1]==R.zero
  A.pop()
 return A+[R.zero]*(len(P)-1-len(A))
def peval(A,x,R):
 out=R.zero
 for a in A[::-1]:out=R.add(R.mul(out,x),a)
 return out
def determinant(A,R):
 # Small division-free Leibniz determinant, deliberately not asymptotically fast.
 n=len(A);out=R.zero
 for perm in itertools.permutations(range(n)):
  v=R.one
  for j,k in enumerate(perm):v=R.mul(v,A[j][k])
  inversions=sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))
  out=R.add(out,R.scale(v,(-1)**inversions))
 return out
def resultant_monic(P,T,R):
 n=len(P)-1;columns=[]
 for j in range(n):columns.append(prem([R.zero]*j+T,P,R))
 return determinant([[columns[j][i] for j in range(n)] for i in range(n)],R)
def gaussian(n,R):
 Q=R.elt([0,1]);row=[R.one]
 for m in range(1,n+1):
  row=[R.add(row[k] if k<m else R.zero,R.mul(R.pow(Q,m-k),row[k-1]) if k else R.zero) for k in range(m+1)]
 return row
def alternate_H(n,R):
 Q=R.elt([0,1]);a=[R.one];b=[R.one,R.one]
 if n==0:return a
 for j in range(2,n+1):
  b,a=padd(pmul([R.one,R.one],b,R),[R.zero]+[R.mul(R.sub(R.pow(Q,j-1),R.one),x) for x in a],R),b
 return b
def contract(H,R):
 r=(len(H)-1)//2;S=[[R.elt(2)],[R.zero,R.one]]
 for j in range(2,r+1):S.append(padd([R.zero]+S[j-1],[R.neg(x) for x in S[j-2]],R))
 P=[H[r]]
 for j in range(1,r+1):P=padd(P,[R.mul(H[r+j],x) for x in S[j]],R)
 return P
def modular_poly(a,p):return sp.Poly(sum((x%p)*q**i for i,x in enumerate(a)),q,modulus=p)

def one_control(d):
 t=time.perf_counter();R=Ring(d);r=(d-1)//4;Q=R.elt([0,1]);H=gaussian(2*r,R)
 assert H==alternate_H(2*r,R)
 P=contract(H,R);assert P[-1]==R.one
 derivative=[R.scale(P[i],i) for i in range(1,len(P))]
 disc=R.scale(resultant_monic(P,derivative,R),(-1)**(r*(r-1)//2))
 H1=peval(H,R.one,R);Hm1=peval(H,R.elt(-1),R)
 D=R.mul(R.mul(H1,R.scale(Hm1,(-1)**r)),R.mul(disc,disc))
 Cstar=[R.one]
 for j in range(2,2*r):
  eta=R.neg(R.add(R.pow(Q,j),R.pow(Q,d-j)))
  Cstar=pmul(Cstar,[R.neg(eta),R.one],R)
 T=pmul(pmul([R.elt(-2),R.one],derivative,R),Cstar,R)
 M=resultant_monic(P,T,R)
 cluster=R.one
 for j in range(d):cluster=R.mul(cluster,peval(H,R.neg(R.pow(Q,j)),R))
 assertions={}
 # Compare complete arrays only after independent construction.
 src=json.loads(pathlib.Path(f'content_extension_independent_audit_0420/REBUILT_{d}.json').read_text())
 for key,arr in [('D',D),('R',cluster),('M',M),('P_discriminant',disc)]:
  assertions['full_'+key+'_array']=list(arr)==src[key];assert assertions['full_'+key+'_array']
 phi=modular_poly([int(R.f.nth(i)) for i in range(R.m+1)],2)
 mod={key:{'coefficients':[int(modular_poly(arr,2).nth(i)) for i in range(R.m)], 'gcd_with_phi':str(sp.gcd(phi,modular_poly(arr,2)).as_expr())} for key,arr in [('D',D),('R',cluster),('M',M),('DiscP',disc),('H1',H1)]}
 conjugate_gcd={}
 for a in range(1,d):
  if math.gcd(a,d)!=1:continue
  g=sp.gcd(sp.gcd(phi,modular_poly(M,2)),modular_poly(R.subst(M,a),2))
  conjugate_gcd[str(a)]=str(g.as_expr())
 normR=int(sp.resultant(R.f,sp.Poly(sum(x*q**i for i,x in enumerate(cluster)),q)))
 assert normR==2**16*17**68*101**4
 # Explicit trace-dual extraction: delta_j=d beta_j is integral.
 F=[int(R.f.nth(i)) for i in range(R.m+1)]
 quotient=sp.div(sp.Poly(q**d-1,q),R.f)[0]
 Qval=R.elt([int(quotient.nth(i)) for i in range(quotient.degree()+1)])
 inv_deriv_numerator=R.mul(Qval,Q) # zeta^(1-d)=zeta
 deltas=[]
 G=[a for a in range(1,d) if math.gcd(a,d)==1]
 for j in range(R.m):
  tail=R.elt(F[j+1:]);delta=R.mul(inv_deriv_numerator,tail);deltas.append(delta)
  v=R.mul(delta,M);trace=R.zero
  for a in G:trace=R.add(trace,R.subst(v,a))
  assert trace==R.elt(d*M[j])
 c=0;coeff=[]
 for x in M:
  aa,bb,g=sp.gcdex(c,x);aa=int(aa);bb=int(bb);g=int(g)
  coeff=[aa*y for y in coeff]+[bb];c=g
 assert sum(a*b for a,b in zip(coeff,M))==c
 W=R.zero
 for b,delta in zip(coeff,deltas):W=R.add(W,R.scale(delta,b))
 target=R.zero
 for a in G:target=R.add(target,R.mul(R.subst(W,a),R.subst(M,a)))
 assert target==R.elt(d*c) and c==17**2
 elapsed=time.perf_counter()-t
 return {'d':d,'H':[list(x) for x in H],'P':[list(x) for x in P],'D':list(D),'R':list(cluster),'M':list(M),'P_discriminant':list(disc),'H1':list(H1),'mod2':mod,'conjugate_pair_mod2_gcds':conjugate_gcd,'norm_R':str(normR),'norm_R_factorization':{'2':16,'17':68,'101':4},'trace_dual_certificate':{'delta_j':[list(x) for x in deltas],'integer_bezout_coefficients':coeff,'W':list(W),'content_M':c,'trace_WM':d*c,'identity':'sum_(a in (Z/17Z)^*) sigma_a(W) sigma_a(M)=17^3'},'assertions':assertions,'ring_operation_counts':R.ops,'elapsed_seconds':elapsed}

if __name__=='__main__':
 out=one_control(17);(HERE/'FRESH_17_CONTROL.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'d':17,'assertions':out['assertions'],'seconds':out['elapsed_seconds'],'ring_operations':out['ring_operation_counts']},indent=2))
