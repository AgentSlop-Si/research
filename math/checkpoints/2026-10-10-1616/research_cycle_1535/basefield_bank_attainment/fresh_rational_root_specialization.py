from fresh_probe import *
K,q,G,f,H,s=setup(11);N=11;t=sp.symbols('t')
T=K.one/G(9,2,-1,1);u=[(f(a,2)-T*G(a,2,-1,1))/G(a,2,1,1) for a in range(2,9)]
A=[[s[r+k] for k in range(4)] for r in range(3)]+[u[:4]]
b=solve(A,[-s[6],-s[7],-s[8],-u[6]],K)[0]+[K.zero,K.zero,K.one]
l=solve(A,[-s[4],-s[5],-s[6],-u[4]],K)[0]+[K.one,K.zero,K.zero]
v=solve(A,[-s[5],-s[6],-s[7],-u[5]],K)[0]+[K.zero,K.one,K.zero]
def mod(a,p,z):
 out=0
 for x in a.to_list():out=(out*z+int(x.numerator)*pow(int(x.denominator),-1,p))%p
 return out

def detmod(M,p):
 M=[r[:] for r in M];det=1
 for k in range(len(M)):
  h=next((i for i in range(k,len(M)) if M[i][k]%p),None)
  if h is None:return 0
  if h!=k:M[h],M[k]=M[k],M[h];det=-det
  z=M[k][k]%p;det=det*z%p
  for i in range(k+1,len(M)):
   a=M[i][k]*pow(z,-1,p)%p
   for j in range(k,len(M)):M[i][j]=(M[i][j]-a*M[k][j])%p
 return det%p

def guards(c,p,z):
 cc=[mod(a,p,z) for a in c];gg=sp.Poly.from_list(cc[::-1],t,modulus=p);res=int(sp.resultant(gg,gg.diff()))%p
 rem=[[int(k==r) for k in range(6)] for r in range(6)]
 for r in range(6,11):rem.append([(-sum(cc[k]*rem[r-6+k][j] for k in range(6)))%p for j in range(6)])
 def gm(a,b,e,d):return mod(G(a,b,e,d),p,z)
 minors={}
 cols={0:(0,1,2,3,4,5,6,8,9,10,11),3:(0,1,2,3,4,5,6,7,8,9,10),4:(0,1,2,3,4,5,6,7,9,10,11),5:(0,1,2,3,4,5,6,9,10,11,12)}
 for r,inds in cols.items():
  M=[]
  for a in range(11):
   row=[gm(a,r,1,1)*k%p for k in rem[a]]+[gm(a,r,-1,1),gm(a,r,1,-1)]+[gm(a,r,-1,-1)*k%p for k in rem[-a%11]]
   M.append([row[k] for k in inds])
  minors[str(r)]=detmod(M,p)
 return {'prime':p,'q_residue':z,'sextic_coefficients_ascending':cc,'constant_term':cc[0],'resultant':res,'selected_minors':minors,'guard_product':cc[0]*res*sp.prod(minors.values())%p,'factorization':str(sp.factor_list(gg.as_expr(),modulus=p))}

for names,x,y in [('7,8',K(7),K(8))]:
 sol=solve([[ev(l,x,K),ev(v,x,K)],[ev(l,y,K),ev(v,y,K)]],[-ev(b,x,K),-ev(b,y,K)],K)
 if not sol or len(sol[1])!=2:continue
 lam,mu=sol[0];c=[a+lam*ll+mu*vv for a,ll,vv in zip(b,l,v)];assert not ev(c,x,K) and not ev(c,y,K)
 good=None
 for p,z in [(23,2),(67,9),(89,2)]:
  if pow(z,11,p)!=1 or z==1:continue
  try:r=guards(c,p,z)
  except ValueError:continue
  print(names,r,flush=True)
  if r['guard_product']:good=r;break
 if good:
  # Synthetic division twice, coefficients in ascending order.
  h=c
  for a in [x,y]:
   temp=[K.zero]*(len(h)-1);temp[-1]=h[-1]
   for k in range(len(h)-2,0,-1):temp[k-1]=h[k]+a*temp[k]
   assert h[0]+a*temp[0]==K.zero;h=temp
  out={'forced_root_names':names,'forced_roots':[enc(x,11),enc(y,11)],'lambda':enc(lam,11),'mu':enc(mu,11),'sextic':[enc(a,11) for a in c],'residual_quartic':[enc(a,11) for a in h],'good_reduction':good,'splitting_field_degree_upper_bound':24}
  (OUT/'N11_RATIONAL_ROOT_SPECIALIZATION.json').write_text(json.dumps(out,indent=2,default=int)+'\n');break
