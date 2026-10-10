from fresh_probe import *
K,q,G,f,H,s=setup(7);N=7;t=sp.symbols('t');one=K.one
A=[s[:3],s[1:4],[one,q,q*q]];bb=[-s[3],-s[4],-q**3]
sol=solve(A,bb,K);assert sol and len(sol[1])==3;c=sol[0]+[one];assert not ev(c,q,K)
# All structural requirements in exact K, including the three prescribed row minors.
def determinant(M):
 M=[r[:] for r in M];d=one
 for k in range(len(M)):
  h=next((i for i in range(k,len(M)) if M[i][k]),None)
  if h is None:return K.zero
  if h!=k:M[h],M[k]=M[k],M[h];d=-d
  p=M[k][k];d*=p
  for i in range(k+1,len(M)):
   a=M[i][k]/p
   for j in range(k,len(M)):M[i][j]-=a*M[k][j]
 return d
rem=[[K(int(k==r)) for k in range(3)] for r in range(3)]
for r in range(3,7):rem.append([-sum((c[k]*rem[r-3+k][j] for k in range(3)),K.zero) for j in range(3)])
minors={}
for b,inds in {0:(0,1,2,3,5,6,7),2:(0,1,2,3,4,5,6),3:(0,1,2,3,4,6,7)}.items():
 M=[]
 for a in range(7):
  row=[G(a,b,1,1)*v for v in rem[a]]+[G(a,b,-1,1),G(a,b,1,-1)]+[G(a,b,-1,-1)*v for v in rem[-a%7]]
  M.append([row[i] for i in inds])
 minors[str(b)]=determinant(M);assert minors[str(b)]
# divide g by t-q
h=[K.zero]*3;h[2]=one;h[1]=c[2]+q;h[0]=c[1]+q*h[1];assert c[0]+q*h[0]==K.zero
disc=h[1]*h[1]-4*h[0]; assert disc and c[0] and ev(h,q,K)
out={'cubic_ascending':[enc(a,7) for a in c],'quadratic_ascending':[enc(a,7) for a in h],'quadratic_discriminant':enc(disc,7),'forced_root':'q','selected_minor_determinants':{k:enc(v,7) for k,v in minors.items()},'node_guards_nonzero':True,'squarefree_cubic':True,'splitting_field_degree_upper_bound':2}
(OUT/'N7_QUADRATIC_SPECIALIZATION.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
