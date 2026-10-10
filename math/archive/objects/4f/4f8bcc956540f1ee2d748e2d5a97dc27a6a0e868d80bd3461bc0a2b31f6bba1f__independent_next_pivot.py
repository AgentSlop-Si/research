"""Fresh independent next-pivot checks. Executes no supplied source/constructor code."""
from independent_linear import *
from pathlib import Path
import json

def operators(N,W,p):
 l=N//4;k=N//8
 B=[[0]*l for _ in range(l)];T=[[0]*k for _ in range(k)];U=[[0]*l for _ in range(k)];V=[[0]*k for _ in range(l)]
 for j in range(l):B[(2*j+1)%l][j]=W[(4*j+3)%N];U[(2*j+1)%k][j]=W[(8*j+6)%N]
 for j in range(k):T[(4*j+2)%k][j]=W[(16*j+10)%N];V[(4*j+2)%l][j]=W[(8*j+5)%N]
 return B,T,U,V

def rawH(N,W,z,p):
 # Direct finite polynomial sum C sum(z^t(A0^t-e0*1^T)) J.
 n=N.bit_length()-1;m=N//2;H=[[0]*m for _ in range(m)]
 for j in range(m):
  pos=2*j+1;phase=1
  for t in range(n):
   if pos<m:H[pos][j]=(H[pos][j]+W[pos]*phase)%p
   else:H[pos-m][j]=(H[pos-m][j]-W[pos-m]*phase)%p
   H[0][j]=(H[0][j]-phase)%p
   pos=2*pos%N;phase=phase*z%p
 return H

def prefix(N,p,W,B,T,U,V,S):
 n=N.bit_length()-1;k=N//8;l=N//4;v=[(j*j+17*j+2)%p for j in range(len(S))]
 base=[0]*k
 for s,c in zip(S,v):base[s]=c
 # Independent dense-vector power/convolution oracle.
 truth=[[0]*len(S) for _ in range(n+1)];truth[0]=v[:];ta=base[:]
 for a in range(max(0,(n-3)//2+1)):
  vb=mv(V,ta,p)
  for b in range(n-2-2*a):
   vals=mv(U,vb,p);degree=3+2*a+b
   for j,s in enumerate(S):truth[degree][j]=(truth[degree][j]-vals[s])%p
   vb=mv(B,vb,p)
  ta=mv(T,ta,p)
 # Compressed structural state propagation with scalar arrays and stamps.
 spaces={k:([0]*k,[-1]*k),l:([0]*l,[-1]*l)};tick=0
 def advance(state,mod,mul,shift,weight):
  nonlocal tick
  tick+=1;vals,seen=spaces[mod];active=[]
  for i,value in state:
   d=(mul*i+shift)%mod
   if seen[d]!=tick:seen[d]=tick;vals[d]=0;active.append(d)
   vals[d]=(vals[d]+weight(i)*value)%p
  return [(i,vals[i]) for i in active]
 # The compressed branch reuses stamped workspaces and emits contributions.
 state=list(zip(S,v));terms=[(s,c) for s,c in zip(S,v)];visits=0;previsits=0;exact=[]
 for a in range(max(0,(n-3)//2+1)):
  previsits+=len(state);mid=advance(state,l,4,2,lambda i:W[(8*i+5)%N])
  for b in range(n-2-2*a):
   bound=max(k//(2*4**a*2**b),1);assert len(mid)<=bound
   visits+=len(mid);exact.append({'a':a,'b':b,'states':len(mid),'cap':bound})
   out=advance(mid,k,2,1,lambda i:W[(8*i+6)%N])
   for s,c in out:
    assert s in S;terms.append(((3+2*a+b)*k+s,-c%p))
   mid=advance(mid,l,2,1,lambda i:W[(4*i+3)%N])
  state=advance(state,k,4,2,lambda i:W[(16*i+10)%N])
 # Stable radix-N sort uses two passes for keys < (n+1)*k <= N^2.
 assert all(key<N*N for key,value in terms)
 for radix in [1,N]:
  count=[0]*N
  for key,value in terms:count[(key//radix)%N]+=1
  where=[0]*N
  for i in range(1,N):where[i]=where[i-1]+count[i-1]
  sorted_terms=[None]*len(terms)
  for term in terms:
   digit=(term[0]//radix)%N;sorted_terms[where[digit]]=term;where[digit]+=1
  terms=sorted_terms
 merged=[]
 for key,value in terms:
  if merged and merged[-1][0]==key:merged[-1]=(key,(merged[-1][1]+value)%p)
  else:merged.append((key,value))
 # Dict below is verification lookup only; sorted merged is the produced jet.
 got={(key//k,key%k):value for key,value in merged}
 assert [[got.get((d,s),0) for s in S] for d in range(n+1)]==truth
 assert visits<=4*k/3+n*n
 marker=[(19*j+11)%p for j in range(len(S))]
 assert [sum(marker[j]*got.get((d,s),0) for j,s in enumerate(S))%p for d in range(n+1)]==[dot(marker,r,p) for r in truth]
 return {'N':N,'p':p,'active_mid_visits':visits,'T_input_visits':previsits,'stored_sparse_slots':len(got),'emitted_contributions':len(terms),'radix_passes':2,'workspace_array_slots':2*(k+l),'exact_frontiers':exact}

def case(N,p,z):
 n=N.bit_length()-1;m=N//2;l=N//4;k=N//8;w,W=root_table(N,p);B,T,U,V=operators(N,W,p)
 q=(1-z*pow(w,-1,p))%p;D=add(eye(l),B,p,-z);di=inverse(D,p);assert bool(q)==bool(di)
 S=sorted({(2**(a+3)*j+3*2**(a+1)-1)%k for a in range(n+2) for j in range(k)})
 assert len(S)==(1 if k==2 else k//4+1)
 uv=mm(U,V,p);expected=[[0]*k for _ in range(k)]
 for j in range(k):expected[(8*j+5)%k][j]=W[(40*j+27)%N]
 assert uv==expected and rank(uv,p)==max(k//8,1)
 power=eye(l)
 for a in range(n+2):
  actual=mm(mm(U,power,p),V,p);expr=[[0]*k for _ in range(k)]
  for s in range(k):expr[(2**(a+3)*s+3*2**(a+1)-1)%k][s]=W[((48*2**a-8)*s+36*2**a-9-a)%N]
  assert actual==expr;power=mm(B,power,p)
 root=(-2*pow(3,-1,k))%k;lam=W[(16*root+10)%N];delta=(1-z*z*lam)%p
 A=add(eye(k),T,p,-z*z);assert det(A,p)==delta
 result={'N':N,'p':p,'z':z,'q':q,'delta':delta,'support':S,'leading_rank':rank(uv,p),'support_size':len(S),'tree_root':root}
 if di is None:result['chart']='q_zero';return result
 H=rawH(N,W,z,p);even=list(range(0,m,2));odd=list(range(1,m,2))
 assert block(H,odd,odd)==B
 sch=add(add(eye(l),block(H,even,even),p,-z),mm(mm(block(H,even,odd),di,p),block(H,odd,even),p),p,-z*z)
 Z=block(sch,list(range(1,l,2)),list(range(1,l,2)))
 transfer=mm(mm(U,di,p),V,p);assert Z==add(A,transfer,p,-z**3)
 assert all(not any(transfer[i]) for i in range(k) if i not in S)
 result['transfer_rank']=rank(transfer,p);result['Z_determinant']=det(Z,p)
 if not delta:result['chart']='delta_zero';return result
 ai=inverse(A,p);aE=block(ai,list(range(k)),S);small=add(eye(len(S)),mm(block(transfer,S,list(range(k))),aE,p),p,-z**3)
 assert det(Z,p)==delta*det(small,p)%p
 si=inverse(small,p)
 if si is None:assert inverse(Z,p) is None;result['chart']='coupled_zero';return result
 Wsmall=block(transfer,S,list(range(k)));prediction=add(ai,mm(mm(mm(aE,si,p),Wsmall,p),ai,p),p,z**3)
 assert prediction==inverse(Z,p)
 x=[(i*i+3*i+9)%p for i in range(k)];h=[(11*i+5)%p for i in range(k)];first=mv(ai,x,p);eta=mv(si,mv(Wsmall,first,p),p);y=mv(prediction,x,p)
 assert mv(Z,y,p)==x
 left=[sum(h[i]*aE[i][j] for i in range(k))%p for j in range(len(S))]
 assert dot(h,y,p)==(dot(h,first,p)+z**3*dot(left,eta,p))%p
 result['chart']='guarded_solve';return result

if __name__=='__main__':
 cases=[case(N,p,z) for p in [257,65537] for N in [16,32,64,128] for z in [0,1,2,3]]
 for N in [16,32,64]:
  p=65537;w,W=root_table(N,p);cases.append(case(N,p,w))
 prefixes=[]
 for p in [257,65537]:
  for N in [16,32,64,128,256]:
   w,W=root_table(N,p);prefixes.append(prefix(N,p,W,*operators(N,W,p),sorted({(2**(a+3)*j+3*2**(a+1)-1)%(N//8) for a in range(N.bit_length()+1) for j in range(N//8)})))
 out={'status':'passed','constructor_code_executed':False,'cases':cases,'constant_input_prefixes':prefixes}
 Path('NEXT_PIVOT_INDEPENDENT_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'status':'passed','cases':len(cases),'guarded_solves':sum(c['chart']=='guarded_solve' for c in cases),'guard_failures':[c for c in cases if c['chart']!='guarded_solve'],'prefixes':len(prefixes)},sort_keys=True))
