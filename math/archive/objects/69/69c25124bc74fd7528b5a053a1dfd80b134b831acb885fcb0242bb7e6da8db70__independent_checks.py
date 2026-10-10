#!/usr/bin/env python3
"""Independent mathematical controls, standard library; no submitted imports."""
from pathlib import Path
import itertools as it, json, random,sys,math,cmath

def I(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def add(a,b,p):return [[(x+y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def mul(a,b,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*b)] for r in a]
def inv(a,p):
 n=len(a);z=[[x%p for x in a[i]]+I(n)[i] for i in range(n)]
 for j in range(n):
  k=next(k for k in range(j,n) if z[k][j]);z[j],z[k]=z[k],z[j];v=pow(z[j][j],-1,p);z[j]=[x*v%p for x in z[j]]
  for k in range(n):
   if k!=j:
    v=z[k][j];z[k]=[(x-v*y)%p for x,y in zip(z[k],z[j])]
 return [r[n:] for r in z]
def rank(a,p):
 z=[row[:] for row in a];r=0
 for j in range(len(z[0])):
  ks=[i for i in range(r,len(z)) if z[i][j]%p]
  if not ks:continue
  k=ks[0];z[r],z[k]=z[k],z[r];v=pow(z[r][j],-1,p);z[r]=[x*v%p for x in z[r]]
  for k in range(len(z)):
   if k!=r:
    v=z[k][j];z[k]=[(x-v*y)%p for x,y in zip(z[k],z[r])]
  r+=1
  if r==len(z):break
 return r
def sub(a,rows,cols):return [[a[i][j] for j in cols] for i in rows]
def cycles(pi):
 rem=set(range(len(pi)));out=[]
 while rem:
  start=min(rem);v=start;c=[]
  while v in rem:c.append(v);rem.remove(v);v=pi[v]
  assert v==start;out.append(c)
 return out
def green(pi,w,p):
 n=len(pi);H=I(n)
 for i,j in enumerate(pi):H[i][j]=(H[i][j]-w[i])%p
 return H,inv(H,p)
def valid(pi,w,p):return all(math.prod(w[i] for i in c)%p!=1 for c in cycles(pi))
def diag(v):return [[x if i==j else 0 for j in range(len(v))] for i,x in enumerate(v)]
def perm(pi):return [[int(j==pi[i]) for j in range(len(pi))] for i in range(len(pi))]
def pmapping(P):return [row.index(1) for row in P]
def negate(A,p):return [[-x%p for x in row] for row in A]
def affsolve(nv,equations,p):
 # Equations are lists of (variable,nonzero coefficient), and RHS.
 graph=[[] for _ in range(nv)]
 for terms,k in equations:
  if len(terms)==2:
   (i,a),(j,b)=terms;graph[i].append((j,-a*pow(b,-1,p)%p,k*pow(b,-1,p)%p));graph[j].append((i,-b*pow(a,-1,p)%p,k*pow(a,-1,p)%p))
 comp=[None]*nv;alpha=[None]*nv;beta=[None]*nv;members=[]
 for i in range(nv):
  if comp[i] is not None:continue
  c=len(members);members.append([]);comp[i]=c;alpha[i]=1;beta[i]=0;stack=[i]
  while stack:
   u=stack.pop();members[c].append(u)
   for v,a,b in graph[u]:
    if comp[v] is None:comp[v]=c;alpha[v]=a*alpha[u]%p;beta[v]=(a*beta[u]+b)%p;stack.append(v)
 fixed={}
 for terms,k in equations:
  if not terms:
   if k%p:return None,'zero_equation'
   continue
  c=comp[terms[0][0]];assert all(comp[v]==c for v,a in terms);a=sum(a*alpha[v] for v,a in terms)%p;b=(k-sum(a*beta[v] for v,a in terms))%p
  if not a:
   if b:return None,'inconsistent_cycle'
  else:
   value=b*pow(a,-1,p)%p
   if c in fixed and fixed[c]!=value:return None,'conflicting_pins'
   fixed[c]=value
 chosen=[]
 for c,vs in enumerate(members):
  forbidden={-beta[v]*pow(alpha[v],-1,p)%p for v in vs}
  if c in fixed:
   if fixed[c] in forbidden:return None,'forced_zero'
   chosen.append(fixed[c])
  else:
   options=[t for t in range(min(p,len(forbidden)+1)) if t not in forbidden]
   if not options:return None,'finite_field_exhaustion'
   chosen.append(options[0])
 solution=[(alpha[v]*chosen[comp[v]]+beta[v])%p for v in range(nv)];assert all(solution)
 assert all(sum(a*solution[v] for v,a in terms)%p==k%p for terms,k in equations)
 return solution,'solved'
def scale_system(U,V,B,p):
 n=len(U);K=mul(mul(U,B,p),V,p);equations=[];off=0
 for i in range(n):
  for j in range(n):
   terms=[]
   if V[i][j]:terms.append((i,V[i][j]))
   if U[i][j]:terms.append((n+j,U[i][j]))
   if terms:equations.append((terms,K[i][j]))
   else:
    off+=1
    if K[i][j]:return None,'offsupport_failure',off
 ans,reason=affsolve(2*n,equations,p);return ans,reason,off

def scan(pi,weights,v,p):
 out=[0]*len(pi)
 for cyc in cycles(pi):
  num=0;product=1
  for i in cyc:num=(num+product*v[i])%p;product=product*weights[i]%p
  assert product!=1;out[cyc[0]]=num*pow(1-product,-1,p)%p
  for k in range(len(cyc)-1,0,-1):i=cyc[k];out[i]=(v[i]+weights[i]*out[pi[i]])%p
 return out

def main():
 rng=random.Random(41410);p=241;positive=[]
 for n in [5,8,9]:
  for trial in range(4):
   orders=[];pis=[]
   while len(pis)<2:
    order=list(range(n));rng.shuffle(order);pi=[0]*n
    for i,x in enumerate(order):pi[x]=order[(i+1)%n]
    if pis and [pi[pis[0][i]] for i in range(n)]==[pis[0][pi[i]] for i in range(n)]:continue
    orders.append(order);pis.append(pi)
   branches=[];Qs=[];supports=[];endpoint_perms=[]
   for j,pi in enumerate(pis):
    while True:
     weights=[rng.randrange(2,p) for _ in range(n)]
     if trial%2==0:weights[j]=0
     if valid(pi,weights,p):break
    G=green(pi,weights,p)[1];left=list(range(n));right=list(range(n))
    if trial>=2:rng.shuffle(left);rng.shuffle(right)
    PL,PR=perm(left),perm(right);dl=[rng.randrange(1,p) for _ in range(n)];dr=[rng.randrange(1,p) for _ in range(n)];T=mul(mul(mul(mul(diag(dl),PL,p),G,p),PR,p),diag(dr),p);Q=inv(T,p);branches.append(T);Qs.append(Q);endpoint_perms.append((PL,PR));base=mul(inv(PR,p),inv(PL,p),p);edge=mul(mul(inv(PR,p),perm(pi),p),inv(PL,p),p);supports.append((pmapping(base),pmapping(edge)))
   B=add(*branches,p);knownx=[rng.randrange(1,p) for _ in range(n)];knowny=[rng.randrange(1,p) for _ in range(n)];U=mul(diag(knownx),Qs[0],p);V=mul(Qs[1],diag(knowny),p);ans,reason,off=scale_system(U,V,B,p);assert ans is not None;x,y=ans[:n],ans[n:];r0,r1=supports[0];s0,s1=supports[1];a=[U[i][r0[i]] for i in range(n)];b=[U[i][r1[i]] for i in range(n)];d=[V[s0.index(j)][j] for j in range(n)];e=[V[s1.index(j)][j] for j in range(n)];assert all(a) and all(d)
   rel0=mul(perm(r1),inv(perm(r0),p),p);rel1=mul(inv(perm(s0),p),perm(s1),p);pi0,pi1=pmapping(rel0),pmapping(rel1);assert len(cycles(pi0))==len(cycles(pi1))==1
   W0=mul(diag([-b[i]*pow(a[i],-1,p)%p for i in range(n)]),rel0,p);W1=mul(negate(rel1,p),diag([e[j]*pow(d[j],-1,p)%p for j in range(n)]),p);ww0=[W0[i][pi0[i]] for i in range(n)];ww1=[W1[i][pi1[i]] for i in range(n)];assert valid(pi0,ww0,p) and valid(pi1,ww1,p);G0=inv(add(I(n),negate(W0,p),p),p);G1=inv(add(I(n),negate(W1,p),p),p);T0=mul(mul(inv(perm(r0),p),G0,p),diag([x[i]*pow(a[i],-1,p)%p for i in range(n)]),p);T1=mul(mul(diag([y[j]*pow(d[j],-1,p)%p for j in range(n)]),G1,p),inv(perm(s0),p),p);assert add(T0,T1,p)==B
   # Recover the SAME prescribed endpoint permutations and original cycles.
   recoveredQ=[mul(diag([pow(v,-1,p) for v in x]),U,p),mul(V,diag([pow(v,-1,p) for v in y]),p)]
   for k,Q in enumerate(recoveredQ):
    PL,PR=endpoint_perms[k];Qprime=mul(mul(PR,Q,p),PL,p);g=[Qprime[i][i] for i in range(n)];assert all(g);wprime=[-Qprime[i][pis[k][i]]*pow(g[i],-1,p)%p for i in range(n)];assert valid(pis[k],wprime,p);G=green(pis[k],wprime,p)[1];recon=mul(mul(mul(PL,G,p),diag([pow(v,-1,p) for v in g]),p),PR,p);assert recon==[T0,T1][k]
   ir0=[r0.index(i) for i in range(n)];is0=[s0.index(i) for i in range(n)]
   for j in range(n):
    z=[int(i==j) for i in range(n)];v=scan(pi0,ww0,[x[i]*pow(a[i],-1,p)*z[i]%p for i in range(n)],p);v=[v[ir0[i]] for i in range(n)];w=scan(pi1,ww1,[z[is0[i]] for i in range(n)],p);w=[y[i]*pow(d[i],-1,p)*w[i]%p for i in range(n)];assert [(v[i]+w[i])%p for i in range(n)]==[B[i][j] for i in range(n)]
   # Projective rescaling: the correspondingly rescaled solution remains valid.
   lam=[rng.randrange(1,p) for _ in range(n)];mu=[rng.randrange(1,p) for _ in range(n)];Up=mul(diag(lam),U,p);Vp=mul(V,diag(mu),p);xp=[lam[i]*x[i]%p for i in range(n)];yp=[mu[i]*y[i]%p for i in range(n)];assert mul(mul(Up,B,p),Vp,p)==add(mul(Up,diag(yp),p),mul(diag(xp),Vp,p),p)
   positive.append(dict(N=n,trial=trial,monomial_endpoints=trial>=2,zero_edges=trial%2==0,offsupport_entries_checked=off,full_entries_checked=n*n,scan_basis_vectors=n))
 # Nonvacuous fixed directions, full offsupport pass, incompatible scales.
 n=5;pi=[1,2,3,4,0];tau=[2,0,3,4,1];U=green(pi,[2]*n,p)[0];V=green(tau,[3]*n,p)[0];K=add(U,V,p);K[0][0]=(K[0][0]+1)%p;B=mul(mul(inv(U,p),K,p),inv(V,p),p);ans,reason,off=scale_system(U,V,B,p);assert ans is None and reason in ['conflicting_pins','inconsistent_cycle'];assert (U[0][2],V[0][2],K[0][2])==(0,p-3,p-3);assert (U[4][0],V[4][0],K[4][0])==(p-2,0,p-2);assert (U[0][0],V[0][0],K[0][0])==(1,1,3)
 # Column nullspaces and all row-pair eliminations really pass.
 UB=mul(U,B,p);column_ranks=[]
 for j in range(n):
  rs=[i for i in range(n) if j not in {i,pi[i],tau[i]}];A=[[UB[i][j],UB[i][tau.index(j)]] for i in rs];column_ranks.append(rank(A,p));assert rank(A,p)==1
 # All cleared row constraints are also retained.
 relations=0
 for i,k in it.combinations(range(n),2):
  for j in range(n):
   if j in {i,k,pi[i],pi[k],tau[i],tau[k]}:continue
   v=tau.index(j);aa,cc=B[i][j],B[i][v];bb,dd=B[pi[i]][j],B[pi[i]][v];ee,gg=B[k][j],B[k][v];ff,hh=B[pi[k]][j],B[pi[k]][v];coeff=[aa*gg-cc*ee,bb*gg-dd*ee,aa*hh-cc*ff,bb*hh-dd*ff];assert sum(x*y for x,y in zip(coeff,[1,-2,-2,4]))%p==0;relations+=1
 assert relations==9
 Bbad=[row[:] for row in B];Bbad[0][0]=(Bbad[0][0]+1)%p;_,badreason,_=scale_system(U,V,Bbad,p);assert badreason=='offsupport_failure'
 # Invertibility alone does not guarantee the required base coordinates.
 zero_base=perm(pi);assert rank(zero_base,p)==n and all(zero_base[i][i]==0 for i in range(n))
 singular_direction=green(pi,[0]*n,p)[0]
 for i in range(n):singular_direction[i][pi[i]]=-1%p
 assert rank(singular_direction,p)==n-1 and not valid(pi,[1]*n,p)
 # Exact determinant data over Z by six-term/Leibniz small control.
 def integer_det(A):
  total=0
  for order in it.permutations(range(len(A))):total+=(-1)**sum(order[i]>order[j] for i in range(n) for j in range(i+1,n))*math.prod(A[i][order[i]] for i in range(n))
  return total
 Ui=[[int(i==j)-2*int(j==pi[i]) for j in range(n)] for i in range(n)];Vi=[[int(i==j)-3*int(j==tau[i]) for j in range(n)] for i in range(n)];Ki=[[Ui[i][j]+Vi[i][j]+int(i==j==0) for j in range(n)] for i in range(n)];detdata=[integer_det(A) for A in [Ui,Vi,Ki]];assert detdata==[-31,-242,-1625]
 # Free-parameter exhaustion is distinct from ordinary linear inconsistency.
 ans,why=affsolve(2,[([(0,1),(1,1)],1)],2);assert ans is None and why=='finite_field_exhaustion'
 ans3,why3=affsolve(2,[([(0,1),(1,1)],1)],3);assert ans3==[2,2]
 assert (2^3)==1 # F4 in basis 1,t with t^2=t+1: t+(t+1)=1.
 brute_cases=0
 for field in [2,3,5]:
  for nv in [2,4,6]:
   for trial in range(16):
    equations=[]
    for _ in range(rng.randrange(1,nv+3)):
     ids=rng.sample(range(nv),rng.randrange(0,3));terms=[(i,rng.randrange(1,field)) for i in ids];equations.append((terms,rng.randrange(field)))
    expected=next((v for v in it.product(range(1,field),repeat=nv) if all(sum(a*v[i] for i,a in terms)%field==k for terms,k in equations)),None);answer,_=affsolve(nv,equations,field);assert (answer is None)==(expected is None);brute_cases+=1
 out=dict(status='PASS',positive_recoveries=positive,total_entries=sum(v['full_entries_checked'] for v in positive),total_scan_basis_vectors=sum(v['scan_basis_vectors'] for v in positive),N5_cleared_row_relations=relations,offsupport_negative_control=True,invertible_zero_base_rejected=True,singular_direction_guard=True,N5_scale_failure=reason,N5_column_nullspace_ranks=column_ranks,N5_integer_determinants=detdata,F2_nonzero_exhaustion=True,F3_nonzero_solution=ans3,F4_nonzero_solution=[2,3],affine_graph_exhaustive_comparisons=brute_cases,source_code_executed=False)
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
