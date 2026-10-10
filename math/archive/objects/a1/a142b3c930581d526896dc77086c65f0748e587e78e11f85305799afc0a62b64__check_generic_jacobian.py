#!/usr/bin/env python3
"""New exact modular Jacobian controls for the four-stage R-G-R image."""
import json,pathlib,random
ROOT=pathlib.Path(__file__).resolve().parent;P=1009;rng=random.Random(109092259)
def mm(a,b):
 bt=list(zip(*b));return [[sum(x*y for x,y in zip(row,col))%P for col in bt] for row in a]
def identity(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def pm(q):return [[int(i==q[j]) for j in range(len(q))] for i in range(len(q))]
def rank(a):
 a=[row[:] for row in a];rr=0
 for j in range(len(a[0])):
  k=next((i for i in range(rr,len(a)) if a[i][j]%P),None)
  if k is None:continue
  a[rr],a[k]=a[k],a[rr];iv=pow(a[rr][j],-1,P);a[rr]=[x*iv%P for x in a[rr]]
  for i in range(rr+1,len(a)):
   z=a[i][j]
   if z:a[i]=[(x-z*y)%P for x,y in zip(a[i],a[rr])]
  rr+=1
  if rr==len(a):break
 return rr
def minor_certificate(matrix):
 a=[row[:] for row in matrix];rows=list(range(len(a)));selected=[];cols=[];rr=0
 for j in range(len(a[0])):
  k=next((i for i in range(rr,len(a)) if a[i][j]%P),None)
  if k is None:continue
  a[rr],a[k]=a[k],a[rr];rows[rr],rows[k]=rows[k],rows[rr]
  selected.append(rows[rr]);cols.append(j)
  iv=pow(a[rr][j],-1,P);a[rr]=[x*iv%P for x in a[rr]]
  for i in range(rr+1,len(a)):
   z=a[i][j]
   if z:a[i]=[(x-z*y)%P for x,y in zip(a[i],a[rr])]
  rr+=1
  if rr==len(a):break
 b=[[matrix[i][j] for j in cols] for i in selected];det=1
 for j in range(rr):
  k=next(i for i in range(j,rr) if b[i][j]%P)
  if k!=j:b[j],b[k]=b[k],b[j];det=-det
  pivot=b[j][j];det=det*pivot%P;iv=pow(pivot,-1,P)
  for i in range(j+1,rr):
   z=b[i][j]*iv%P
   if z:b[i]=[(x-z*y)%P for x,y in zip(b[i],b[j])]
 assert det%P
 return {'rows_in_order':selected,'columns_in_order':cols,'determinant_mod_1009':det%P}
def stage(n):
 d,a,b,g,h=[[rng.randrange(1,P) for _ in range(n)] for _ in range(5)]
 s=[[d[i] if i==j else(a[i]*b[j]%P if i>j else g[i]*h[j]%P) for j in range(n)] for i in range(n)]
 deriv=[]
 for i in range(n):
  z=[[0]*n for _ in range(n)];z[i][i]=1;deriv.append(z)
 for i in range(1,n):
  z=[[0]*n for _ in range(n)]
  for j in range(i):z[i][j]=b[j]
  deriv.append(z)
 for j in range(n-1):
  z=[[0]*n for _ in range(n)]
  for i in range(j+1,n):z[i][j]=a[i]
  deriv.append(z)
 for i in range(n-1):
  z=[[0]*n for _ in range(n)]
  for j in range(i+1,n):z[i][j]=h[j]
  deriv.append(z)
 for j in range(1,n):
  z=[[0]*n for _ in range(n)]
  for i in range(j):z[i][j]=g[i]
  deriv.append(z)
 assert len(deriv)==5*n-4
 return s,deriv

out=[]
for m in [2,3,4]:
 n=1<<m;r=pm([int(format(i,f'0{m}b')[::-1],2) for i in range(n)]);g=pm([i^(i>>1) for i in range(n)]);perms=[r,g,r]
 for trial in range(2):
  while True:
   data=[stage(n) for _ in range(4)];s=[x[0] for x in data]
   if all(rank(x)==n for x in s):break
  left=[None]*4;right=[None]*4;left[3]=identity(n);right[0]=identity(n)
  for i in range(1,4):right[i]=mm(mm(perms[i-1],s[i-1]),right[i-1])
  for i in range(2,-1,-1):left[i]=mm(mm(left[i+1],s[i+1]),perms[i])
  cols=[]
  for i in range(4):
   for ds in data[i][1]:cols.append(sum(mm(mm(left[i],ds),right[i]),[]))
  jac=list(map(list,zip(*cols)));actual=rank(jac);bound=min(n*n,17*n-26)
  assert actual<=bound
  # Exact gauge tangent cancellation at all three interfaces.
  gauges=0
  for i in range(3):
   for j in range(n):
    d=[[0]*n for _ in range(n)];d[j][j]=1
    di=mm(d,s[i]);dj=mm(mm(mm(s[i+1],perms[i]),d),list(map(list,zip(*perms[i]))))
    a=mm(mm(left[i],di),right[i]);b=mm(mm(left[i+1],dj),right[i+1])
    assert a==b;gauges+=1
  cert=minor_certificate(jac) if n==16 else None
  if cert:assert len(cert['rows_in_order'])==246
  out.append({'N':n,'trial':trial,'raw_separated_chart_variables':len(cols),'target_entries':n*n,
   'exact_modular_jacobian_rank':actual,'dimension_bound_including_middle_GL2_gauge':bound,'gauge_tangent_cancellations':gauges,'nonzero_minor_certificate':cert})
res={'field':P,'reproducibility_seed':109092259,'integer_parameter_range':[1,1008],'cases':out,'uploaded_code_executed':False,'interpretation':'Generic parameter-image controls only; these random targets are not Fourier compatibility solutions.'}
(ROOT/'JACOBIAN_RESULTS.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
