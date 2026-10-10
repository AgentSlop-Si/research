#!/usr/bin/env python3
"""New independent exact checks: inverse Gray crossing and full inverse system."""
import fractions,json,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parent
P=1009; rng=random.Random(106092255)
def mm(a,b,p=P):
 bt=list(zip(*b));return [[sum(x*y for x,y in zip(row,col))%p for col in bt] for row in a]
def ident(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def inv(a,p=P):
 n=len(a);a=[row[:]+e for row,e in zip(a,ident(n))]
 for j in range(n):
  k=next((k for k in range(j,n) if a[k][j]%p),None)
  if k is None:return None
  a[j],a[k]=a[k],a[j];z=pow(a[j][j],-1,p);a[j]=[z*x%p for x in a[j]]
  for k in range(n):
   if k!=j:
    z=a[k][j];a[k]=[(x-z*y)%p for x,y in zip(a[k],a[j])]
 return [row[n:] for row in a]
def perm(q):return [[int(i==q[j]) for j in range(len(q))] for i in range(len(q))]
def transpose(a):return list(map(list,zip(*a)))
def rev(i,m):return int(format(i,f'0{m}b')[::-1],2)
def qs1(n):
 while True:
  a=[[0]*n for _ in range(n)]
  for i in range(n):a[i][i]=rng.randrange(P)
  l,r,u,v=[[rng.randrange(P) for _ in range(n)] for _ in range(4)]
  t,s=[[rng.randrange(P) if rng.randrange(3) else 0 for _ in range(n)] for _ in range(2)]
  for j in range(n):
   state=r[j]
   for i in range(j+1,n):a[i][j]=l[i]*state%P;state=state*t[i]%P
   state=v[j]
   for i in range(j-1,-1,-1):a[i][j]=u[i]*state%P;state=state*s[i]%P
  ai=inv(a)
  if ai is not None:return a,ai
def separated_minors(a):
 n=len(a);count=0
 for i in range(n):
  for j in range(i+1,n):
   for k in range(j+1,n):
    for l in range(k+1,n):
     assert (a[i][k]*a[j][l]-a[i][l]*a[j][k])%P==0
     assert (a[k][i]*a[l][j]-a[k][j]*a[l][i])%P==0
     count+=2
 return count

inverse_gray=[]
for m in range(1,19):
 n=1<<m;q=[i^(i>>1) for i in range(n)];b=[0]*n
 for i,j in enumerate(q):b[j]=i
 d=[0]*(n+1)
 for x,y in zip(b,b[1:]):
  x,y=sorted((x,y));d[x+1]+=1;d[y+1]-=1
 v=0;vlist=[]
 for t in range(1,n):v+=d[t];vlist.append(v)
 assert max(vlist)==m
 t=(2*n+(-1)**m)//3;assert vlist[t-1]==m
 if m>1:
  h=n//2;prev=b[:h];assert b==prev+[2*h-1-x for x in prev]
  for u in range(1,h):
   old=sum((x<h-u)!=(y<h-u) for x,y in zip(prev,prev[1:])) if m<=10 else None
   if old is not None:assert vlist[h+u-1]==old+1
 inverse_gray.append({'m':m,'N':n,'inverse_gray_crossing_maximum':m,'maximizing_threshold':t})

systems=[];minor_count=0
for m in [2,3,4]:
 n=1<<m;r=perm([rev(i,m) for i in range(n)]);g=perm([i^(i>>1) for i in range(n)])
 for case in range(12):
  pairs=[qs1(n) for _ in range(4)];s=[x[0] for x in pairs];si=[x[1] for x in pairs]
  if case==0:s[1]=ident(n);si[1]=ident(n)
  f=mm(mm(mm(mm(mm(mm(s[3],r),s[2]),g),s[1]),r),s[0])
  u,v,w=si[3],si[0],si[2]
  z=mm(mm(mm(mm(mm(mm(transpose(g),w),r),u),f),v),r)
  assert z==s[1]
  recovered=mm(mm(mm(mm(mm(mm(inv(u),r),inv(w)),g),z),r),inv(v))
  assert recovered==f
  for a in [u,v,w,z]:minor_count+=separated_minors(a)
  systems.append({'N':n,'case':case,'exact_recovery':True,'diagonal_middle_control':case==0})

# Actual F4 over Gaussian integers. Gaussian pairs avoid numerical complex values.
def ga(a,b):return(a[0]+b[0],a[1]+b[1])
def gm(a,b):return(a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def gmat(a,b):
 bt=list(zip(*b));out=[]
 for row in a:
  outrow=[]
  for col in bt:
   z=(0,0)
   for x,y in zip(row,col):z=ga(z,gm(x,y))
   outrow.append(z)
  out.append(outrow)
 return out
def lift(a):return [[(x,0) for x in row] for row in a]
r=lift(perm([0,2,1,3]));g=lift(perm([0,1,3,2]));b=lift([[1,1,0,0],[1,-1,0,0],[0,0,1,1],[0,0,1,-1]])
d=lift(ident(4));d[3][3]=(0,1)
s1=lift(ident(4));s2=gmat(g,b);s3=d;s4=gmat(r,b)
product=s4
for factor in [r,s3,g,s2,r,s1]:product=gmat(product,factor)
roots=[(1,0),(0,1),(-1,0),(0,-1)]
assert product==[[roots[(i*j)%4] for j in range(4)] for i in range(4)]
for a in [s1,s2,s3,s4]:
 assert gm(a[0][2],a[1][3])==gm(a[0][3],a[1][2])
 assert gm(a[2][0],a[3][1])==gm(a[2][1],a[3][0])
assert s4[0][1]!=(0,0) and s4[1][2]!=(0,0) and s4[0][2]==(0,0)

out={'inverse_gray_checks':inverse_gray,'exact_modular_system_checks':systems,'separated_minor_equalities_checked':minor_count,
 'gaussian_integer_F4_R_G_R_identity':True,'F4_last_stage_outside_transition_free_separated_chart':True,
 'zero_transitions_and_diagonal_middle_included':True,'uploaded_code_executed':False}
(ROOT/'EXACT_RESULTS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
