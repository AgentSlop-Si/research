#!/usr/bin/env python3
"""Exact one-stage Schur and compressed two-run jet controls; authored independently."""
import json
from pathlib import Path
P=65537

def solve(A,b):
 a=[r[:]+[v]for r,v in zip(A,b)];n=len(b)
 for j in range(n):
  k=next(i for i in range(j,n)if a[i][j]);a[j],a[k]=a[k],a[j];iv=pow(a[j][j],-1,P);a[j]=[v*iv%P for v in a[j]]
  for i in range(n):
   if i!=j:
    t=a[i][j];a[i]=[(v-t*w)%P for v,w in zip(a[i],a[j])]
 return [r[-1]for r in a]
def rank(A):
 a=[r[:]for r in A];i=0
 for j in range(len(a[0])):
  k=next((k for k in range(i,len(a))if a[k][j]),None)
  if k is None:continue
  a[i],a[k]=a[k],a[i];iv=pow(a[i][j],-1,P);a[i]=[v*iv%P for v in a[i]]
  for k in range(len(a)):
   if k!=i:
    t=a[k][j];a[k]=[(v-t*w)%P for v,w in zip(a[k],a[i])]
  i+=1
  if i==len(a):break
 return i
def mv(A,x):return [sum(a*b for a,b in zip(r,x))%P for r in A]
def mm(A,B):return [[sum(a*b for a,b in zip(r,c))%P for c in zip(*B)]for r in A]
def K(x,z):
 N=len(x);y=x[:];y[0]=0;h=1
 while h<N:
  for odd in range(1,N//h,2):
   s=h*odd;t=2*s%N
   if t:y[t]=(y[t]+z*y[s])%P
  h*=2
 y[0]=-sum(y[1:])%P;return y
def C(x,w):
 m=len(x)//2;return [pow(w,i,P)*(x[i]-x[i+m])%P for i in range(m)]
def ev(poly,z):return [sum(v*pow(z,d,P)for d,v in row.items())%P for row in poly]
def twotree(x,w):
 N=len(x);n=N.bit_length()-1;lam=pow(w,-1,P);out=[{}for _ in x];trunc=[{}for _ in x];v=dict(enumerate(x));visits=0
 def add(i,d,v):out[i][d]=(out[i].get(d,0)+v)%P
 for a in range(n+1):
  mass=sum(v.values())%P;y=v.copy()
  for b in range(n):
   assert len(y)==max(N//2**(a+b),1);visits+=len(y)
   if a+b<=n:
    for i,value in y.items():trunc[i][a+b]=(trunc[i].get(a+b,0)+value)%P
    trunc[0][a+b]=(trunc[0].get(a+b,0)-mass)%P
   for i,value in y.items():
    add(i,a+b,value)
    if a<n:add(i,a+b+1,-lam*value)
   add(0,a+b,-mass)
   if a<n:add(0,a+b+1,lam*mass)
   yy={}
   for i,value in y.items():
    t=2*i%N;yy[t]=(yy.get(t,0)+value)%P
   y=yy
  vv={}
  for i,value in v.items():
   t=(2*i+1)%N;vv[t]=(vv.get(t,0)+pow(w,i,P)*value)%P
  v=vv
 assert visits==sum(max(N//2**(a+b),1)for a in range(n+1)for b in range(n))
 assert visits<=4*N+n*n
 assert sum(len(r)for r in out)<=6*N
 for i in range(N):
  for d in range(n+1):assert out[i].get(d,0)==(trunc[i].get(d,0)-lam*trunc[i].get(d-1,0))%P
 return out,visits,sum(len(r)for r in trunc)

def one(N,z):
 n=N.bit_length()-1;m=N//2;l=N//4;w=pow(3,(P-1)//N,P);lam=pow(w,-1,P);q=(1-lam*z)%P;assert q
 Hcols=[]
 for j in range(m):
  x=[0]*N;x[2*j+1]=1;Hcols.append(C(K(x,z),w))
 H=list(map(list,zip(*Hcols)))
 E=list(range(0,m,2));O=list(range(1,m,2))
 EE=[[H[i][j]for j in E]for i in E];EO=[[H[i][j]for j in O]for i in E];OE=[[H[i][j]for j in E]for i in O];OO=[[H[i][j]for j in O]for i in O]
 expectedOO=[[0]*l for _ in range(l)];expectedOE=[[0]*l for _ in range(l)]
 for j in range(l):
  expectedOO[(2*j+1)%l][j]=pow(w,4*j+3,P)
  expectedOE[2*j%l][j]=pow(w,4*j+1,P)
 assert OO==expectedOO and OE==expectedOE
 D=[[(int(i==j)-z*OO[i][j])%P for j in range(l)]for i in range(l)]
 Dinv=list(map(list,zip(*(solve(D,[int(i==j)for i in range(l)])for j in range(l)))))
 fb=mm(mm(EO,Dinv),OE)
 S=[[(int(i==j)-z*EE[i][j]-z*z*fb[i][j])%P for j in range(l)]for i in range(l)]
 reduced=[S[i]+[(-int(i==0))%P]for i in range(l)]
 onesD=[sum(Dinv[i][j]for i in range(l))%P for j in range(l)]
 tail=[(-z-z*z*sum(onesD[k]*OE[k][j]for k in range(l)))%P for j in range(l)]
 reduced.append(tail+[(1-z)%P])
 x=[(i*i+7*i+3)%P for i in range(N)];f=C(K(x,z),w);sigma=sum(x)%P;fo=[f[i]for i in O];fe=[f[i]for i in E]
 go=mv(Dinv,fo);rhs=[(v+z*t)%P for v,t in zip(fe,mv(EO,go))]+[(sigma+z*sum(go))%P]
 sol=solve(reduced,rhs);ee,tt=sol[:-1],sol[-1];oo=mv(Dinv,[(a+z*b)%P for a,b in zip(fo,mv(OE,ee))])
 uu=[0]*m
 for i,v in zip(E,ee):uu[i]=v
 for i,v in zip(O,oo):uu[i]=v
 M=[[(int(i==j)-z*H[i][j])%P for j in range(m)]+[(-int(i==0))%P]for i in range(m)]
 M.append([(-z)%P]*m+[(1-z)%P]);assert mv(M,uu+[tt])==f+[sigma]
 # Constant Schur-action input; compact polynomial numerator via lifted two-tree path.
 v=[(j*j+13*j+1)%P for j in range(l)];rv=mv(OE,v);lift=[0]*N
 for j,a in enumerate(rv):lift[4*j+3]=a
 poly,visits,truncslots=twotree(lift,w);cc=C(ev(poly,z),w);compact=[cc[i]for i in E]
 assert compact==[(q*a)%P for a in mv(fb,v)]
 # Independent full-space resolvent oracle for the claimed two-tree identity.
 A1=[[0]*N for _ in range(N)]
 for j in range(N):A1[(2*j+1)%N][j]=pow(w,j,P)
 Ig=[[(int(i==j)-z*A1[i][j])%P for j in range(N)]for i in range(N)]
 direct=K(solve(Ig,lift),z);assert ev(poly,z)==[(q*a)%P for a in direct]
 h=[(5*i+9)%P for i in range(N)];scalar={}
 for i,row in enumerate(poly):
  for d,a in row.items():scalar[d]=(scalar.get(d,0)+h[i]*a)%P
 assert sum(a*pow(z,d,P)for d,a in scalar.items())%P==q*sum(a*b for a,b in zip(h,direct))%P
 odd2=list(range(1,l,2));nextblock=[[S[i][j]for j in odd2]for i in odd2]
 maxoff=max((sum(nextblock[i][j]!=0 for i in range(len(odd2))if i!=j)for j in range(len(odd2))),default=0)
 kk=l//2;T=[[0]*kk for _ in range(kk)]
 for j in range(kk):T[(4*j+2)%kk][j]=pow(w,16*j+10,P)
 ref=[[(int(i==j)-z*z*T[i][j])%P for j in range(kk)]for i in range(kk)]
 corr=[[(nextblock[i][j]-ref[i][j])%P for j in range(kk)]for i in range(kk)]
 U=[[0]*l for _ in range(kk)];V=[[0]*kk for _ in range(l)]
 for j in range(l):U[(2*j+1)%kk][j]=pow(w,8*j+6,P)
 for j in range(kk):V[(4*j+2)%l][j]=pow(w,8*j+5,P)
 transfer=mm(mm(U,Dinv),V)
 assert corr==[[(-z**3*v)%P for v in row]for row in transfer]
 uv=mm(U,V);r0=max(kk//8,1);assert rank(uv)==r0
 leading=[[0]*kk for _ in range(kk)]
 for j in range(kk):leading[(8*j+5)%kk][j]=pow(w,40*j+27,P)
 assert leading==uv
 reach=sorted({(2**(a+3)*j+3*2**(a+1)-1)%kk for a in range(kk.bit_length()+1)for j in range(kk)})
 assert len(reach)==(kk//4+1 if kk>=4 else 1)
 assert all(not any(transfer[i])for i in range(kk)if i not in reach)
 root=(-2*pow(3,-1,kk))%kk;treeguard=(1-z*z*pow(w,16*root+10,P))%P
 # Direct formal prefix of I-z^3 E^T U G V A^-1 E on a constant input.
 pos={v:i for i,v in enumerate(reach)};rr=len(reach);v0=[(3*i+5)%P for i in range(rr)]
 jet=[{0:v}for v in v0];state={j:v for j,v in zip(reach,v0)};jetwork=0
 for a in range(max(0,(n-3)//2+1)):
  mid={}
  for j,value in state.items():
   dst=(4*j+2)%l;mid[dst]=(mid.get(dst,0)+pow(w,8*j+5,P)*value)%P
  for b in range(n-3-2*a+1):
   jetwork+=len(mid);yy={}
   for j,value in mid.items():
    dst=(2*j+1)%kk;yy[dst]=(yy.get(dst,0)+pow(w,8*j+6,P)*value)%P
   for dst,value in yy.items():
    if dst in pos:
     row=jet[pos[dst]];d=3+2*a+b;row[d]=(row.get(d,0)-value)%P
   old=[mid.get(j,0)for j in range(l)];nxt={}
   for j,value in mid.items():
    dst=(2*j+1)%l;nxt[dst]=(nxt.get(dst,0)+pow(w,4*j+3,P)*value)%P
   assert [nxt.get(j,0)for j in range(l)]==mv(OO,old);mid=nxt
  old=[state.get(j,0)for j in range(kk)];nxt={}
  for j,value in state.items():
   dst=(4*j+2)%kk;nxt[dst]=(nxt.get(dst,0)+pow(w,16*j+10,P)*value)%P
  assert [nxt.get(j,0)for j in range(kk)]==mv(T,old);state=nxt
 assert jetwork<=4*kk//3+n*n+1
 woodbury=False;marked=False
 if treeguard and rank(nextblock)==kk:
  Ai=list(map(list,zip(*(solve(ref,[int(i==j)for i in range(kk)])for j in range(kk)))))
  AiE=[[Ai[i][j]for j in reach]for i in range(kk)]
  W=[transfer[i]for i in reach];red=mm(W,AiE);rr=len(reach)
  red=[[(int(i==j)-z**3*red[i][j])%P for j in range(rr)]for i in range(rr)]
  bvec=[(i*i+3*i+7)%P for i in range(kk)];hvec=[(11*i+2)%P for i in range(kk)]
  first=mv(Ai,bvec);eta=solve(red,mv(W,first));yy=[(a+z**3*b)%P for a,b in zip(first,mv(AiE,eta))]
  assert mv(nextblock,yy)==bvec
  left=[sum(hvec[i]*AiE[i][j]for i in range(kk))%P for j in range(rr)]
  assert sum(a*b for a,b in zip(hvec,yy))%P==(sum(a*b for a,b in zip(hvec,first))+z**3*sum(a*b for a,b in zip(left,eta)))%P
  woodbury=marked=True
 return {'support_operator_jet_state_visits':jetwork,'support_operator_jet_slots':sum(len(r)for r in jet),'support_reduced_dimension':len(reach),'woodbury_recovery_checked':woodbury,'marked_recovery_checked':marked,'leading_transfer_rank':r0,'reachable_row_rank_bound':len(reach),'reachable_rows':reach,'reference_tree_root':root,'reference_tree_guard':treeguard,'symbolic_transfer_identity_verified':True,'reference_tree_correction_rank':rank(corr),'next_literal_parity_pivot_matrix_N32_z1':nextblock if N==32 and z==1 else None,'next_literal_parity_pivot_max_offdiagonal_column_degree':maxoff,'N':N,'z':z,'original_border_dimension':m+1,'reduced_border_dimension':l+1,'pivot_guard':q,'two_run_state_visits':visits,'actual_series_slots_through_logN':truncslots,'allocated_polynomial_slots':sum(len(r)for r in poly),'maximum_degree':max(max(r,default=0)for r in poly),'exact_Schur_recovery':True,'exact_two_tree_numerator':True,'marked_contraction':True}

cases=[one(N,z)for N in (16,32,64,128,256)for z in (1,2,3)]
out={'field':P,'cases':cases,'all_exact_assertions_passed':True,'one_stage_plus_next_pivot_classification_only':True,'dense_schur_matrices_and_inverse_calls_are_verification_oracles':True,'uploaded_code_executed':False}
Path(__file__).with_name('NEXT_PIVOT_RANK_DIAGNOSTIC.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'case_count':len(cases),'maximum_N':256,'maximum_slot_ratio':max(c['allocated_polynomial_slots']/c['N']for c in cases),'all_exact_assertions_passed':True},indent=2))
