#!/usr/bin/env python3
"""Fresh exact small-field checks for projective graph consistency."""
from pathlib import Path
import itertools as it,json,random,sys

def det(A,p):return (A[0][0]*A[1][1]-A[0][1]*A[1][0])%p
def mm(A,B,p):return [[sum(A[i][k]*B[k][j] for k in range(2))%p for j in range(2)] for i in range(2)]
def mv(A,v,p):return tuple(sum(x*y for x,y in zip(row,v))%p for row in A)
def tr(A):return [list(x) for x in zip(*A)]
def inv(A,p):
 d=pow(det(A,p),-1,p);return [[A[1][1]*d%p,-A[0][1]*d%p],[-A[1][0]*d%p,A[0][0]*d%p]]
def norm(v,p):
 assert any(v)
 if v[0]%p:return (1,v[1]*pow(v[0],-1,p)%p)
 return (0,1)
def points(p):return [(1,x) for x in range(p)]+[(0,1)]
def val(C,u,v,p):return sum(u[i]*C[i][j]*v[j] for i in range(2) for j in range(2))%p
def H(C,p):return [[C[0][1],C[1][1]],[-C[0][0]%p,-C[1][0]%p]]
def qe(q,v,p):return (q[0]*v[0]*v[0]+q[1]*v[0]*v[1]+q[2]*v[1]*v[1])%p

def sat_solve(n,clauses):
 graph=[[] for _ in range(2*n)];reverse=[[] for _ in range(2*n)]
 for a,b in clauses:
  for x,y in [(a^1,b),(b^1,a)]:graph[x].append(y);reverse[y].append(x)
 seen=set();order=[]
 def dfs(v):
  seen.add(v)
  for u in graph[v]:
   if u not in seen:dfs(u)
  order.append(v)
 for v in range(2*n):
  if v not in seen:dfs(v)
 comp={}
 def visit(v,k):
  comp[v]=k
  for u in reverse[v]:
   if u not in comp:visit(u,k)
 for v in reversed(order):
  if v not in comp:visit(v,len(comp))
 if any(comp[2*i]==comp[2*i+1] for i in range(n)):return None
 assignment=[comp[2*i+1]>comp[2*i] for i in range(n)]
 assert all(assignment[a//2]==bool(a%2) or assignment[b//2]==bool(b%2) for a,b in clauses)
 return assignment

def solve(n,edges,p,finite_atleast=False):
 graph=[[] for _ in range(n)]
 for i,j,C in edges:
  if det(C,p):T=H(C,p);graph[i].append((j,T));graph[j].append((i,inv(T,p)))
 component=[None]*n;maps=[None]*n;roots=[]
 for root in range(n):
  if component[root] is not None:continue
  k=len(roots);roots.append(root);component[root]=k;maps[root]=[[1,0],[0,1]];stack=[root]
  while stack:
   i=stack.pop()
   for j,T in graph[i]:
    if component[j] is None:component[j]=k;maps[j]=mm(T,maps[i],p);stack.append(j)
 count=len(roots);quadratics=[[] for _ in roots];relations=[]
 for i,j,C in edges:
  T=mm(mm(tr(maps[i]),C,p),maps[j],p);ci,cj=component[i],component[j]
  if ci==cj:quadratics[ci].append((T[0][0],(T[0][1]+T[1][0])%p,T[1][1]));continue
  assert det(T,p)==0
  if not any(x for row in T for x in row):continue
  col=next(j for j in range(2) if any(T[i][j] for i in range(2)));left=[T[i][col] for i in range(2)];row=next(i for i in range(2) if left[i]);right=[T[row][j]*pow(left[row],-1,p)%p for j in range(2)];alpha=norm((left[1],-left[0]%p),p);beta=norm((right[1],-right[0]%p),p);relations.append((ci,alpha,cj,beta))
 domains=[[v for v in points(p) if all(qe(q,v,p)==0 for q in qq)] for qq in quadratics]
 for ci,D in enumerate(domains):
  if not D:
   qq=quadratics[ci];k=next(k for k,q in enumerate(qq) if any(q));witness={k};candidates=[v for v in points(p) if qe(qq[k],v,p)==0];assert len(candidates)<=2
   for v in candidates:witness.add(next(j for j,q in enumerate(qq) if qe(q,v,p)))
   assert len(witness)<=3 and not any(all(qe(qq[j],v,p)==0 for j in witness) for v in points(p));return None,dict(reason='empty_domain',witness_quadratics=len(witness))
 flags={};bycomp=[[] for _ in roots]
 def flag(c,a):
  if a not in domains[c]:return None
  if (c,a) not in flags:flags[(c,a)]=len(flags);bycomp[c].append(a)
  return 2*flags[(c,a)]+1
 clauses=[]
 for ci,a,cj,b in relations:
  x,y=flag(ci,a),flag(cj,b)
  if x is None and y is None:return None,dict(reason='false_edge')
  if x is None:x=y
  if y is None:y=x
  clauses.append((x,y))
 if finite_atleast:
  for c,D in enumerate(domains):
   if len(D)<=2:
    vs=[flag(c,a) for a in D];clauses.append((vs[0],vs[-1]))
 for c,aa in enumerate(bycomp):
  for a,b in it.combinations(aa,2):clauses.append((flag(c,a)^1,flag(c,b)^1))
 assignment=sat_solve(len(flags),clauses)
 if assignment is None:return None,dict(reason='2sat_unsat')
 choice=[];repaired=0
 for c,D in enumerate(domains):
  selected=[a for a in bycomp[c] if assignment[flags[(c,a)]]];assert len(selected)<=1
  if selected:choice.append(selected[0])
  else:choice.append(D[0]);repaired+=int(D[0] in bycomp[c])
 solution=[norm(mv(maps[i],choice[component[i]],p),p) for i in range(n)]
 assert all(val(C,solution[i],solution[j],p)==0 for i,j,C in edges)
 return solution,dict(reason='sat',components=count,flags=len(flags),clauses=len(clauses),all_false_flag_repairs=repaired)

def brute(n,edges,p):
 for vv in it.product(points(p),repeat=n):
  if all(val(C,vv[i],vv[j],p)==0 for i,j,C in edges):return vv
 return None

def trim(a,p):
 a=[x%p for x in a]
 while a and a[-1]==0:a.pop()
 return a

def prem(a,b,p):
 a=trim(a,p);b=trim(b,p);assert b
 while len(a)>=len(b):
  c=a[-1]*pow(b[-1],-1,p)%p;k=len(a)-len(b)
  for j,x in enumerate(b):a[j+k]=(a[j+k]-c*x)%p
  a=trim(a,p)
 return a

def pgcd(a,b,p):
 a=trim(a,p);b=trim(b,p)
 while b:a,b=b,prem(a,b,p)
 return [x*pow(a[-1],-1,p)%p for x in a] if a else []

def domain_profile(qs,p):
 if not any(any(q) for q in qs):return dict(unrestricted=True,finite_points=p+1)
 g=[]
 for q in qs:
  if any(q):g=pgcd(g,q,p)
 infinity=all(q[2]%p==0 for q in qs);degree=len(g)-1
 if degree<=0:distinct=0
 elif degree==1:distinct=1
 else:
  derivative=trim([g[1],2*g[2]],p)
  distinct=1 if not derivative or len(pgcd(g,derivative,p))>1 else 2
 finite=[v for v in points(p) if all(qe(q,v,p)==0 for q in qs)]
 # The source exhaustion criterion: g divides the square product of named
 # allowed affine root factors; infinity is checked separately.
 product=[1]
 for x,y in finite:
  if x==0:continue
  root=y*pow(x,-1,p)%p
  for _ in range(2):
   new=[0]*(len(product)+1)
   for j,c in enumerate(product):new[j]=(new[j]-root*c)%p;new[j+1]=(new[j+1]+c)%p
   product=new
 exhausted=(not prem(product,g,p)) and (not infinity or (0,1) in finite)
 assert exhausted==(len(finite)==distinct+int(infinity))
 return dict(unrestricted=False,gcd=g,infinity=infinity,closure_points=distinct+int(infinity),finite_points=len(finite),all_closure_points_base_named=exhausted)

def gi(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def ginv(A,p):
 n=len(A);Z=[A[i][:]+gi(n)[i] for i in range(n)]
 for j in range(n):
  k=next(k for k in range(j,n) if Z[k][j]%p);Z[j],Z[k]=Z[k],Z[j];c=pow(Z[j][j],-1,p);Z[j]=[x*c%p for x in Z[j]]
  for k in range(n):
   if k!=j:
    c=Z[k][j];Z[k]=[(x-c*y)%p for x,y in zip(Z[k],Z[j])]
 return [r[n:] for r in Z]
def extract(B,pi,tau,p):
 edges=[];n=len(pi)
 for i,k in it.combinations(range(n),2):
  forbidden={i,k,pi[i],pi[k],tau[i],tau[k]}
  for j in range(n):
   if j in forbidden:continue
   v=tau.index(j);A,C=B[i][j],B[i][v];BB,D=B[pi[i]][j],B[pi[i]][v];EE,G=B[k][j],B[k][v];FF,HH=B[pi[k]][j],B[pi[k]][v];c=[(A*G-C*EE)%p,(BB*G-D*EE)%p,(A*HH-C*FF)%p,(BB*HH-D*FF)%p];matrix=[[c[0],c[2]],[c[1],c[3]]];assert det(matrix,p)==det([[A,C],[BB,D]],p)*det([[EE,G],[FF,HH]],p)%p;edges.append((i,k,matrix))
 return edges

def chirp(n,w,p):
 F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];X=ginv(F,p)
 for i in range(n):X[i][i]=(X[i][i]+pow(w,((n+1)//2)*i*i,p))%p
 return ginv(X,p)

def main():
 rng=random.Random(230610);cases=[]
 for p in [2,3,5]:
  for n in [2,3,4]:
   for trial in range(24):
    edges=[]
    for k in range(rng.randrange(0,2*n+4)):
     i,j=rng.sample(range(n),2);mode=rng.randrange(4)
     if mode==0:C=[[0,0],[0,0]]
     elif mode==1:
      u=[rng.randrange(p) for _ in range(2)];v=[rng.randrange(p) for _ in range(2)];C=[[a*b%p for b in v] for a in u]
     else:C=[[rng.randrange(p) for _ in range(2)] for _ in range(2)]
     edges.append((i,j,C))
    expected=brute(n,edges,p)
    for exact_flags in [False,True]:
     answer,stats=solve(n,edges,p,exact_flags);assert (answer is None)==(expected is None);cases.append(dict(p=p,n=n,trial=trial,finite_domain_atleast_one=exact_flags,feasible=answer is not None,**stats))
 # Exactly three quadratics are genuinely needed: q1=xy, q2=x(x-y),
 # q3=y(x-y). Every pair has a projective root; triple intersection empty.
 witness=[]
 for p in [2,3,5,7]:
  qs=[(0,1,0),(1,-1%p,0),(0,1,-1%p)];assert not any(all(qe(q,v,p)==0 for q in qs) for v in points(p));assert all(any(all(qe(qs[j],v,p)==0 for j in pair) for v in points(p)) for pair in it.combinations(range(3),2));witness.append(p)
 profiles=[]
 for p,qs in [(241,[(234,0,1)]),(3,[(1,0,1)]),(2,[(1,0,1)]),(5,[(1,0,0)]),(5,[(0,0,1)]),(5,[(0,0,0)]),(5,[(1,0,0),(0,0,1)])]:
  profiles.append(dict(p=p,quadratics=qs,**domain_profile(qs,p)))
 assert profiles[0]['closure_points']==2 and profiles[0]['finite_points']==0
 assert profiles[2]['closure_points']==profiles[2]['finite_points']==1
 integration=[]
 for n,w,pi,tau,expected in [(3,15,[1,2,0],[2,0,1],True),(5,91,[2,3,4,0,1],[3,2,4,1,0],False)]:
  edges=extract(chirp(n,w,241),pi,tau,241);answer,stats=solve(n,edges,241,True);assert (answer is not None)==expected;integration.append(dict(N=n,edges=len(edges),feasible=expected,**stats))
 boundary=[];p=241;n=5;pi=[2,3,4,0,1];tau=[3,2,4,1,0]
 for trial in range(8):
  B=[[0]*n for _ in range(n)]
  for k,perm in enumerate([pi,tau]):
   weights=[2+i+k for i in range(n)]
   if trial%2==0:weights[k]=0
   den=gi(n)
   for i in range(n):den[i][perm[i]]=(den[i][perm[i]]-weights[i])%p
   G=ginv(den,p);left=[i+2 for i in range(n)];right=[i+7 for i in range(n)]
   if trial%3==0:left[k]=0;right[k+2]=0
   for i in range(n):
    for j in range(n):B[i][j]=(B[i][j]+left[i]*G[i][j]*right[j])%p
  answer,stats=solve(n,extract(B,pi,tau,p),p,True);assert answer is not None;boundary.append(dict(trial=trial,singular_masks=trial%3==0,zero_edges=trial%2==0,**stats))
 bezout=[0]*4
 for q,h in [([113,40,220],[169,215]),([207,140,92],[108,146])]:
  for i,x in enumerate(q):
   for j,y in enumerate(h):bezout[i+j]=(bezout[i+j]+x*y)%241
 assert bezout==[1,0,0,0]
 out=dict(status='PASS',supplied_N5_Bezout_identity=bezout,target_integration=integration,genuine_boundary_controls=boundary,domain_profiles=profiles,cases=cases,graph_solver_bruteforce_comparisons=len(cases),tight_three_quadratic_witness_fields=witness,source_code_executed=False)
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
