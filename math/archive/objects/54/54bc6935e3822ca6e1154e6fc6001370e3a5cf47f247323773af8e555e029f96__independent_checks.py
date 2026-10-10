#!/usr/bin/env python3
"""Independent auditor controls. No source imports, files, or third-party modules."""
import itertools,json,math,random,sys
from pathlib import Path
RNG=random.Random(90107)
def poly(nodes,p):
 a=[1]
 for x in nodes:
  b=[0]*(len(a)+1)
  for i,c in enumerate(a): b[i]=(b[i]-x*c)%p;b[i+1]=(b[i+1]+c)%p
  a=b
 return a
def ev(a,x,p):
 s=0
 for c in reversed(a): s=(s*x+c)%p
 return s
def rem(a,b,p):
 a=a[:]
 while len(a)>=len(b):
  c=a[-1]*pow(b[-1],-1,p)%p;k=len(a)-len(b)
  for j,t in enumerate(b):a[k+j]=(a[k+j]-c*t)%p
  a.pop()
 return a+[0]*(len(b)-1-len(a))
def transpose(a):return [list(x) for x in zip(*a)] if a else []
def mm(a,b,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)] for row in a]
def mv(a,v,p):return [sum(x*y for x,y in zip(row,v))%p for row in a]
def add(a,b,p,sgn=1):return [[(x+sgn*y)%p for x,y in zip(r,s)]for r,s in zip(a,b)]
def eye(n):return [[int(i==j)for j in range(n)]for i in range(n)]
def rank(a,p):
 if not a:return 0
 a=[r[:]for r in a];r=0
 for j in range(len(a[0])):
  k=next((k for k in range(r,len(a))if a[k][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];q=pow(a[r][j],-1,p);a[r]=[v*q%p for v in a[r]]
  for k in range(r+1,len(a)):
   q=a[k][j];a[k]=[(x-q*y)%p for x,y in zip(a[k],a[r])]
  r+=1
  if r==len(a):break
 return r
def inv(a,p):
 n=len(a)
 if not n:return []
 a=[row[:]+e for row,e in zip(a,eye(n))]
 for j in range(n):
  k=next(k for k in range(j,n)if a[k][j]);a[j],a[k]=a[k],a[j]
  v=pow(a[j][j],-1,p);a[j]=[x*v%p for x in a[j]]
  for i in range(n):
   if i!=j:
    v=a[i][j];a[i]=[(x-v*y)%p for x,y in zip(a[i],a[j])]
 return [r[n:]for r in a]
def root(n,p):return next(w for w in range(1,p)if pow(w,n,p)==1 and len({pow(w,k,p)for k in range(n)})==n)
def card(nodes,x,p):
 a=poly([z for z in nodes if z!=x],p);q=pow(ev(a,x,p),-1,p)
 return [c*q%p for c in a]
def transfer(nodes,p):
 m=len(nodes);q=poly(nodes,p)
 return transpose([rem([0]*(m+j)+[1],q,p)for j in range(m)])
def make_case(n,p,A,full=False):
 m=n//2;w=root(n,p);roots=[pow(w,-j,p)for j in range(n)];B=[i for i in range(n)if i not in A]
 e=[roots[i]for i in range(0,n,2)if i not in A];o=[roots[i]for i in A if i%2];t=len(e)
 ar=[roots[i]for i in A];br=[roots[i]for i in B];ra=transfer(ar,p);rb=transfer(br,p);I=eye(m)
 assert mm(ra,ra,p)==I and mm(rb,rb,p)==I
 ca=add(ra,I,p,-1);cb=add(rb,I,p)
 assert rank(ca,p)==rank(cb,p)==t
 assert rank(ca+cb,p)==min(m,2*t)
 assert rank(add(ra,rb,p,-1),p)==m
 r=2*min(t,m-t)
 assert rank(add(ra,rb,p),p)==r
 assert rank(add(mm(ra,rb,p),I,p),p)==r
 assert rank(add(mm(ra,rb,p),mm(rb,ra,p),p,-1),p)==r
 if not full:return {'n':n,'p':p,'t':t,'rank':r}
 ua=[card(ar,x,p)for x in o];ub=[card(br,x,p)for x in e]
 C=[[ev(c,x,p)for c in ub]for x in o];D=[[ev(c,x,p)for c in ua]for x in e]
 assert rank(C,p)==rank(D,p)==t
 PA,PB=poly(ar,p),poly(br,p)
 for i,x in enumerate(o):
  for j,y in enumerate(e):
   assert C[i][j]==ev(PB,x,p)*pow((x-y)*ev(poly([z for z in br if z!=y],p),y,p),-1,p)%p
   assert D[j][i]==ev(PA,y,p)*pow((y-x)*ev(poly([z for z in ar if z!=x],p),x,p),-1,p)%p
 low=[RNG.randrange(p)for _ in range(m)];high=[RNG.randrange(p)for _ in range(m)]
 a=[(x+y)%p for x,y in zip(low,high)];b=[(x-y)%p for x,y in zip(low,high)]
 for x,c in zip(o,ua):a=[(v-2*ev(high,x,p)*z)%p for v,z in zip(a,c)]
 for x,c in zip(e,ub):b=[(v+2*ev(high,x,p)*z)%p for v,z in zip(b,c)]
 assert a==rem(low+high,PA,p) and b==rem(low+high,PB,p)
 y=[(x-z)*pow(2,-1,p)%p for x,z in zip(a,b)]
 zo=[-v%p for v in mv(inv(D,p),[ev(y,x,p)for x in e],p)]
 ze=[-v%p for v in mv(inv(C,p),[ev(y,x,p)for x in o],p)]
 hh=y[:]
 for v,c in list(zip(zo,ua))+list(zip(ze,ub)):hh=[(z+v*q)%p for z,q in zip(hh,c)]
 ll=[(x-z)%p for x,z in zip(a,hh)]
 for v,c in zip(zo,ua):ll=[(z+2*v*q)%p for z,q in zip(ll,c)]
 assert ll==low and hh==high
 for j in A:assert ev(a,roots[j],p)==ev(low+high,roots[j],p)
 for j in B:assert ev(b,roots[j],p)==ev(low+high,roots[j],p)
 # Different fixed common coefficient bases leave all three defect ranks unchanged.
 G=eye(m)
 for j in range(m):G[j][j]=RNG.randrange(1,p)
 for j in range(m-1):G[j][j+1]=RNG.randrange(p)
 Gi=inv(G,p);raa=mm(mm(G,ra,p),Gi,p);rbb=mm(mm(G,rb,p),Gi,p)
 assert rank(add(mm(raa,rbb,p),mm(rbb,raa,p),p,-1),p)==r
 # Actual full child evaluator: ordinary coset DFT values then direct newcomer replacement.
 out=[None]*n
 for j in range(0,n,2):out[j]=ev(a,roots[j],p)
 for j in range(1,n,2):out[j]=ev(b,roots[j],p)
 for j in A:
  if j%2:out[j]=ev(a,roots[j],p)
 for j in B:
  if not j%2:out[j]=ev(b,roots[j],p)
 assert out==[ev(low+high,x,p)for x in roots]
 wrong=False
 if t:
  bad=y[:]
  for v,c in list(zip(zo,ua))+list(zip(ze,ub)):bad=[(z-v*q)%p for z,q in zip(bad,c)]
  wrong=bad!=high
 if t==1:
  ge=[pow(e[0],m-1-i,p)for i in range(m)];go=[pow(o[0],m-1-i,p)for i in range(m)]
  assert a==[(x+y+(o[0]-e[0])*ev(high,o[0],p)*z)%p for x,y,z in zip(low,high,ge)]
  assert b==[(x-y+(e[0]-o[0])*ev(high,e[0],p)*z)%p for x,y,z in zip(low,high,go)]
 return {'n':n,'p':p,'t':t,'rank':r,'wrong_sign_detected':wrong,'dense_counts':[sum(v!=0 for row in M for v in row)for M in (ra,rb)]}
def main():
 exhaustive=[];total=0
 for n,p in [(2,101),(4,101),(6,103),(8,97),(10,101),(12,97)]:
  hist=[0]*(n//2+1)
  for A in itertools.combinations(range(n),n//2):
   c=make_case(n,p,A);hist[c['t']]+=1;total+=1
  assert hist==[math.comb(n//2,t)**2 for t in range(n//2+1)]
  exhaustive.append({'n':n,'p':p,'partitions':sum(hist),'histogram':hist})
 full=[]
 for n,p in [(2,101),(4,101),(6,103),(8,97),(10,101),(12,97),(16,17),(30,151),(32,193),(64,193)]:
  m=n//2
  for t in sorted({0,1,m//2,max(0,m-1),m}):
   for trial in range(2):
    es=RNG.sample(list(range(0,n,2)),t);os=RNG.sample(list(range(1,n,2)),t)
    A=sorted((set(range(0,n,2))-set(es))|set(os));full.append(make_case(n,p,A,True))
 # An explicit maximal-density one-exchange transfer over GF(17).
 dense=make_case(16,17,[1,2,4,6,8,10,12,14],True);assert dense['dense_counts']==[64,64]
 # Distinctness is essential to a Cauchy inverse; repeated row node invalidates it.
 repeated=[[pow(x-y,-1,101)for y in (3,4)]for x in (1,1)];assert rank(repeated,101)==1
 # A nonprimitive root gives repeated nodes and singular Fourier evaluation.
 badF=[[pow(100,i*j,101)for j in range(4)]for i in range(4)];assert rank(badF,101)==2
 counts=[]
 for n in [256,1024,4096,16384,65536]:
  counts.append({'n':n,'plan_scalar':13*n+13,'plan_inversions':8,'forward_scalar':5*n+3,'inverse_scalar':13*n//2+7,'plan_plus_forward':18*n+16})
 n=65536;fullcost=23*n+14+(3*n//2)*(n.bit_length()-2);ordinary=n-1+(3*n//2)*(n.bit_length()-1)
 assert fullcost==2981902 and ordinary==1638399
 result={'status':'PASS','uploaded_code_executed':False,'exhaustive_rank_partitions':total,'exhaustive':exhaustive,'full_cases':full,'full_case_count':len(full),'dense_control':dense,'all_n16_partition_histogram':[math.comb(8,t)**2 for t in range(9)],'wrong_sign_controls_detected':sum(c['wrong_sign_detected']for c in full),'invalid_root_rank':2,'repeated_cauchy_row_rank':1,'independently_derived_source_ledger_counts':counts,'full_n65536_counts':{'hybrid':fullcost,'classical':ordinary},'large_source_execution_repeated':False}
 path=Path(sys.argv[1] if len(sys.argv)>1 else 'INDEPENDENT_RESULTS.json');path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n');print('PASS',total,'exhaustive rank partitions;',len(full),'full forward/inverse/DFT cases')
if __name__=='__main__':main()
