#!/usr/bin/env python3
"""Fresh exact finite-field controls. No uploaded or constructor code imported."""
import json
from pathlib import Path
P=65537
def zero(n,m=None):return [[0]*(n if m is None else m) for _ in range(n)]
def eye(n):
 a=zero(n)
 for i in range(n):a[i][i]=1
 return a
def add(a,b,k=1):return [[(x+k*y)%P for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,k):return [[k*x%P for x in r] for r in a]
def mul(a,b):
 c=zero(len(a),len(b[0]))
 for i,row in enumerate(a):
  for k,v in enumerate(row):
   if v:
    for j,w in enumerate(b[k]):
     if w:c[i][j]=(c[i][j]+v*w)%P
 return c
def transpose(a):return [list(r) for r in zip(*a)]
def rank(a):
 a=[r[:] for r in a];r=0
 for c in range(len(a[0])):
  k=next((k for k in range(r,len(a)) if a[k][c]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=pow(a[r][c],-1,P);a[r]=[v*x%P for x in a[r]]
  for k in range(r+1,len(a)):
   if a[k][c]:
    v=a[k][c];a[k]=[(x-v*y)%P for x,y in zip(a[k],a[r])]
  r+=1
  if r==len(a):break
 return r
def inv(a):
 n=len(a);a=[r[:]+s for r,s in zip(a,eye(n))]
 for c in range(n):
  k=next((k for k in range(c,n) if a[k][c]),None)
  if k is None:return None
  a[c],a[k]=a[k],a[c];v=pow(a[c][c],-1,P);a[c]=[v*x%P for x in a[c]]
  for k in range(n):
   if k!=c and a[k][c]:
    v=a[k][c];a[k]=[(x-v*y)%P for x,y in zip(a[k],a[c])]
 return [r[n:] for r in a]
def sub(a,r,c):return [[a[i][j] for j in c] for i in r]
def op(n,fun,weights):
 a=zero(n)
 for j in range(n):a[fun(j)%n][j]=weights[j]%P
 return a
def disp(x,a,y=None):return add(mul(x,a),mul(a,x if y is None else y),-1)
def blockdiag(a,c):return [r+[0] for r in a]+[[0]*len(a)+[c]]
def hcoeff(N,w,t):
 m=N//2;h=zero(m)
 for j in range(m):
  r=(2**t*(2*j+1))%N
  h[r%m][j]=(h[r%m][j]+pow(w,r,P))%P
  h[0][j]=(h[0][j]-1)%P
 return h
def kval(N,w,z,x):
 # Independent direct defining finite sum; verification oracle only.
 n=N.bit_length()-1;y=[0]*N
 for t in range(n):
  a=pow(z,t,P)
  for j,v in enumerate(x):y[(2**t*j)%N]=(y[(2**t*j)%N]+a*v)%P
  y[0]=(y[0]-a*sum(x))%P
 return y
def cval(N,w,x):return [pow(w,r,P)*(x[r]-x[r+N//2])%P for r in range(N//2)]
def mv(a,x):return [sum(u*v for u,v in zip(row,x))%P for row in a]
def vecadd(a,b,k=1):return [(u+k*v)%P for u,v in zip(a,b)]
def dot(a,b):return sum(u*v for u,v in zip(a,b))%P
results=[];formal=[];marked=[];kernel=[]
for N in [8,16,32,64,128]:
 n=N.bit_length()-1;m=N//2;l=N//4;w=pow(3,(P-1)//N,P)
 assert pow(w,N,P)==1 and pow(w,N//2,P)==P-1
 ev=list(range(0,m,2));od=list(range(1,m,2));Hc=[hcoeff(N,w,t) for t in range(n)]
 F0=sub(Hc[0],ev,ev);G0=sub(Hc[0],ev,od);R=sub(Hc[0],od,ev);T=sub(Hc[0],od,od)
 er=zero(l);er[0]=[1]*l
 Vtree=op(l,lambda j:4*j+1,[pow(w,8*j+2,P) for j in range(l)])
 assert F0==scale(er,-1) and G0==scale(er,-1)
 assert sub(Hc[1],ev,ev)==add(Vtree,er,-1)
 S0=eye(l);S1=er;S2=add(scale(sub(Hc[1],ev,ev),-1),mul(G0,R),-1)
 assert S2==add(add(scale(Vtree,-1),er),mul(er,R))
 charts=[]
 for style in ['unit','varying']:
  c=[1 if style=='unit' else pow(w,3*j+1,P) for j in range(l)]
  for wrapL,wrapR in [(1,1),(0,1),(2,3)]:
   cl=c[:];cr=c[:];cl[-1]=wrapL;cr[-1]=wrapR
   xl=op(l,lambda j:j+1,cl);xr=op(l,lambda j:j+1,cr)
   if l>=4:
    rows=list(range(2,l,4));cols=list(range(l//4))
    assert sub(disp(xl,S0,xr),rows,cols)==zero(l//4)
    assert sub(disp(xl,S1,xr),rows,cols)==zero(l//4)
    lead=sub(disp(xl,S2,xr),rows,cols)
    assert rank(lead)==l//4
    for j in range(l//4):assert lead[j][j]==(-pow(w,8*j+2,P)*cl[4*j+1])%P
    formal.append({'N':N,'chart':'shift_'+style,'wraps':[wrapL,wrapR],'minor_size':l//4,'lowest_degree':2})
   charts.append(('shift_'+style+str((wrapL,wrapR)),xl,xr))
 for b in [0,1]:
  c=[pow(w,5*j+2,P) for j in range(l)];x=op(l,lambda j:2*j+b,c)
  if l>=8:
   rows=list(range(2+b,l,8));cols=list(range(l//8))
   assert sub(disp(x,S0),rows,cols)==zero(l//8)
   assert sub(disp(x,S1),rows,cols)==zero(l//8)
   assert rank(sub(disp(x,S2),rows,cols))==l//8
   formal.append({'N':N,'chart':'doubling_'+str(b),'minor_size':l//8,'lowest_degree':2})
  charts.append(('doubling_'+str(b),x,x))
  # Explicit invisible rank-one perturbation: XG=GX=0.
  u=[0]*l;u[0]=pow(c[0],-1,P);u[l//2]=-pow(c[l//2],-1,P)%P
  v=[0]*l;v[1-b]=1;g=[[a*d%P for d in v] for a in u]
  assert rank(g)==1 and mul(x,g)==zero(l) and mul(g,x)==zero(l)
  kernel.append({'N':N,'b':b,'tree_rank':rank(x),'certified_kernel_dimension_at_least':(l//2)**2})
 for z in [0,1,2,3]:
  q=(1-z*pow(w,-1,P))%P
  if not q:continue
  H=zero(m)
  for t,a in enumerate(Hc):H=add(H,scale(a,pow(z,t,P)))
  F=sub(H,ev,ev);G=sub(H,ev,od);V=inv(add(eye(l),T,-z));assert V is not None
  S=add(add(eye(l),F,-z),mul(mul(G,V),R),-z*z)
  ones=[[1]*l];beta=add(scale(ones,-z),mul(mul(ones,V),R),-z*z)[0]
  M=[row+[-int(i==0)%P] for i,row in enumerate(S)]+[beta+[(1-z)%P]]
  Si=inv(S);Mi=inv(M)
  for name,xl,xr in charts:
   Y=op(l,lambda j:j+1,[1]*l)  # Noncommuting intermediary tests the resolvent term.
   rhs=add(xl,xr,-1);rhs=add(rhs,disp(xl,F,xr),-z)
   inner=mul(mul(add(mul(xl,G),mul(G,Y),-1),V),R)
   inner=add(inner,mul(mul(G,V),add(mul(Y,R),mul(R,xr),-1)))
   inner=add(inner,mul(mul(mul(mul(G,V),disp(Y,T)),V),R),z)
   rhs=add(rhs,inner,-z*z);d=disp(xl,S,xr);assert rhs==d
   Xl=blockdiag(xl,7);Xr=blockdiag(xr,7);dm=disp(Xl,M,Xr)
   top=[(-xl[i][0]+7*int(i==0))%P for i in range(l)]
   bottom=vecadd([7*v%P for v in beta],mv(transpose(xr),beta),-1)
   assert dm==[row+[top[i]] for i,row in enumerate(d)]+[bottom+[0]]
   if Si is not None:
    assert disp(xr,Si,xl)==scale(mul(mul(Si,d),Si),-1)
    assert rank(disp(xr,Si,xl))==rank(d)
   if Mi is not None:assert disp(Xr,Mi,Xl)==scale(mul(mul(Mi,dm),Mi),-1)
   steinrank=None
   if name.startswith('doubling') and Si is not None:
    steinrank=rank(add(S,mul(mul(xl,S),transpose(xl)),-1));assert steinrank>=l//2
   results.append({'N':N,'z':z,'chart':name,'rank_displacement':rank(d),'inverse_checked':Si is not None,'border_inverse_checked':Mi is not None,'stein_rank':steinrank})
  # Independent full-space marked solve at bounded sizes.
  if N<=64 and Mi is not None:
   x=[(j*j+3*j+7)%P for j in range(N)];h=[(5*j*j+2*j+1)%P for j in range(N)]
   kx=kval(N,w,z,x);f=cval(N,w,kx);fE=f[::2];fO=f[1::2];vf=mv(V,fO)
   gx=vecadd(fE,mv(G,vf),z);sx=(sum(x)+z*sum(vf))%P
   et=mv(Mi,gx+[sx]);e=et[:-1];t=et[-1];o=mv(V,vecadd(fO,mv(R,e),z))
   u=[0]*m;u[::2]=e;u[1::2]=o;ju=[0]*N;ju[1::2]=u
   y=vecadd(kx,kval(N,w,z,ju),z);y[0]=(y[0]+t)%P
   Q=add(op(N,lambda j:2*j,[1]*N),op(N,lambda j:2*j+1,[pow(w,j,P) for j in range(N)]))
   full=inv(add(eye(N),Q,-z));assert full is not None and y==mv(full,x)
   a=[]
   for j in range(m):
    ej=[0]*N;ej[2*j+1]=1;a.append(z*dot(h,kval(N,w,z,ej))%P)
   aE=a[::2];aO=a[1::2];pv=mv(transpose(V),aO)
   pm=vecadd(aE,mv(transpose(R),pv),z)
   base=(dot(h,kx)+dot(aO,vf))%P
   assert (base+dot(pm,e)+h[0]*t)%P==dot(h,y)
   marked.append({'N':N,'z':z,'all_source_marker_boundary_terms_checked':True})
# A coefficient-only reconstruction checks the formal solve recurrence independently.
formal_recurrences=[]
for N in [8,16,32]:
 n=N.bit_length()-1;m=N//2;l=N//4;w=pow(3,(P-1)//N,P);Hc=[hcoeff(N,w,t) if t<n else zero(m) for t in range(n+1)]
 ev=list(range(0,m,2));od=list(range(1,m,2));T=sub(Hc[0],od,od);R=sub(Hc[0],od,ev)
 Vc=[eye(l)]
 for t in range(n):Vc.append(mul(T,Vc[-1]))
 Mc=[]
 for d in range(n+1):
  S=eye(l) if d==0 else scale(sub(Hc[d-1],ev,ev),-1)
  if d>=2:
   for a in range(d-1):S=add(S,mul(mul(sub(Hc[a],ev,od),Vc[d-2-a]),R),-1)
  beta=[0]*l
  if d==1:beta=[P-1]*l
  if d>=2:beta=scale(mul(mul([[1]*l],Vc[d-2]),R),-1)[0]
  Mc.append([r+[-int(d==0 and i==0)%P] for i,r in enumerate(S)]+[beta+[int(d==0)-int(d==1)]])
 M0i=inv(Mc[0]);assert M0i is not None
 # Arbitrary polynomial source verifies recurrence and all carried source coefficients.
 bc=[[(7*d+3*j*j+1)%P for j in range(l+1)] for d in range(n+1)];yc=[]
 for d in range(n+1):
  v=bc[d][:]
  for k in range(1,d+1):v=vecadd(v,mv(Mc[k],yc[d-k]),-1)
  yc.append(mv(M0i,v))
 for d in range(n+1):
  acc=[0]*(l+1)
  for k in range(d+1):acc=vecadd(acc,mv(Mc[k],yc[d-k]))
  assert acc==bc[d]
 formal_recurrences.append({'N':N,'degree':n,'arbitrary_polynomial_source':True,'unknown_coefficients':(n+1)*(l+1)})
output={'field':P,'uploaded_or_external_code_executed':False,'formal_leading_minor_controls':formal,'scalar_displacement_controls':results,'source_marker_recovery_controls':marked,'invisible_tree_kernel_controls':kernel,'formal_recurrence_controls':formal_recurrences,'scope':'Exact bounded test oracles; all-size rank and operation bounds require the accompanying proofs.'}
p=Path(__file__).with_name('SCHUR_DISPLACEMENT_CONTROLS.json');p.write_text(json.dumps(output,indent=2)+'\n')
print(json.dumps({'formal_minors':len(formal),'scalar_charts':len(results),'marked':len(marked),'kernel_controls':len(kernel),'formal_recurrences':len(formal_recurrences),'output':str(p)},indent=2))
