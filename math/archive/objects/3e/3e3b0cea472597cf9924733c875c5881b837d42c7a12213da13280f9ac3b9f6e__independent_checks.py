#!/usr/bin/env python3
"""Own exact symmetry, commutator, and perturbation checks."""
from pathlib import Path
import json,sys,random
P=65537;R=random.Random(151010)
def eye(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(r,c))%P for c in zip(*b)] for r in a]
def add(a,b,scale=1):return [[(x+scale*y)%P for x,y in zip(r,s)] for r,s in zip(a,b)]
def inv(a):
 n=len(a);a=[r[:]+eye(n)[i] for i,r in enumerate(a)]
 for j in range(n):
  k=next(k for k in range(j,n) if a[k][j]);a[k],a[j]=a[j],a[k];c=pow(a[j][j],-1,P);a[j]=[x*c%P for x in a[j]]
  for k in range(n):
   if k!=j:
    c=a[k][j]
    if c:a[k]=[(x-c*y)%P for x,y in zip(a[k],a[j])]
 return [r[n:] for r in a]
def rank(a):
 a=[r[:] for r in a];k=0
 for j in range(len(a[0])):
  q=next((q for q in range(k,len(a)) if a[q][j]),None)
  if q is None:continue
  a[k],a[q]=a[q],a[k];c=pow(a[k][j],-1,P);a[k]=[x*c%P for x in a[k]]
  for q in range(k+1,len(a)):
   c=a[q][j]
   if c:a[q]=[(x-c*y)%P for x,y in zip(a[q],a[k])]
  k+=1
  if k==len(a):break
 return k

def maps(s):
 return [[((x+2*y)%s)*s+y for x in range(s) for y in range(s)],[((x+2*y+1)%s)*s+y for x in range(s) for y in range(s)],[x*s+(y+2*x)%s for x in range(s) for y in range(s)],[x*s+(y+2*x+1)%s for x in range(s) for y in range(s)]]
def shifts(s):
 h=s//2;return [[((x+h)%s)*s+y for x in range(s) for y in range(s)],[x*s+(y+h)%s for x in range(s) for y in range(s)],[((x+h)%s)*s+(y+h)%s for x in range(s) for y in range(s)]]
def comm(A,pi):return [[(A[i][pi[j]]-A[pi[i]][j])%P for j in range(len(A))] for i in range(len(A))]
def green(pi,w):
 K=eye(len(pi))
 for i,j in enumerate(pi):K[i][j]=(K[i][j]-w[i])%P
 return inv(K)
def main():
 out={'status':'PASS','uploaded_or_constructor_code_executed':False};central=0;weyl_orbits=0
 for s in range(2,22,2):
  n=s*s;h=s//2
  for pi in maps(s):
   for q in shifts(s):
    for i in range(n):assert pi[q[i]]==q[pi[i]];central+=1
  for a in range(s):
   for b in range(s):
    aa=(a+h)%s;bb=(b+h)%s;e=(a-aa)*b;ep=(aa-a)*bb;assert (2*(e+ep))%n==n//2
    # Pi_xy contributes parity signs that cancel over its two-step orbit.
    assert (a+aa+b+bb)%2==0;weyl_orbits+=1
 out['centralizer_vertex_checks']=central;out['exact_W_fourth_power_orbits']=weyl_orbits
 spectra=[];orthogonal=0
 for s in [2,4,8]:
  n=s*s;w=pow(3,(P-1)//n,P);norm=pow(s,-1,P);F=[[pow(w,i*j,P)*norm%P for j in range(n)] for i in range(n)];Fc=[[pow(w,(-i*j)%n,P)*norm%P for j in range(n)] for i in range(n)];pis=shifts(s)
  for index,pi in enumerate(pis):
   C=comm(F,pi);Cc=comm(Fc,pi);H=mm(list(map(list,zip(*Cc))),C);H2=mm(H,H);Id=eye(n)
   residual=add(H2,H,-4)
   if index:residual=add(residual,Id,2)
   assert not any(v for row in residual for v in row);assert sum(H[i][i] for i in range(n))%P==2*n%P;assert rank(C)==(n//2 if index==0 else n)
   spectra.append({'s':s,'shift':index,'commutator_rank':rank(C),'trace_Gram':2*n,'Gram_polynomial':'x(x-4)' if index==0 else 'x^2-4x+2'})
  group=[list(range(n))]+pis;conjs=[[[F[q[i]][q[j]] for j in range(n)] for i in range(n)] for q in group];conjbars=[[[Fc[q[i]][q[j]] for j in range(n)] for i in range(n)] for q in group]
  for a in range(4):
   for b in range(4):assert sum(conjbars[a][i][j]*conjs[b][i][j] for i in range(n) for j in range(n))%P==(n if a==b else 0);orthogonal+=1
  proj=[[sum(A[i][j] for A in conjs)*pow(4,-1,P)%P for j in range(n)] for i in range(n)]
  assert all(not any(v for row in comm(proj,pi) for v in row) for pi in pis)
 out['exact_spectra']=spectra;out['group_projection_inner_products']=orthogonal
 # Genuine mixed-axis two-stage products; changes count per solver occurrence.
 perturb=[];resolvent_identity=0
 for s in [2,4]:
  n=s*s;plans=maps(s);base=[green(pi,[2]*n) for pi in plans];T0=mm(add(base[0],base[1],3),add(base[2],base[3],5));pis=shifts(s);assert all(rank(comm(T0,pi))==0 for pi in pis)
  for k in range(0,7):
   weights=[[2]*n for _ in plans];changed=[]
   for slot in R.sample(range(4*n),k):stage,i=divmod(slot,n);weights[stage][i]=3+(slot%5);changed.append((stage,i))
   gs=[green(pi,w) for pi,w in zip(plans,weights)];T=mm(add(gs[0],gs[1],3),add(gs[2],gs[3],5));rd=rank(add(T,T0,-1));rc=[rank(comm(T,pi)) for pi in pis];assert rd<=k and max(rc)<=2*k;perturb.append({'N':n,'edited_occurrences':k,'difference_rank':rd,'commutator_ranks':rc})
   for pi,w,G in zip(plans,weights,gs):
    Q=eye(n)
    for i in range(n):
     for j in range(n):Q[i][j]=w[i] if pi[i]==j else 0
    for shift in pis:assert comm(G,shift)==mm(mm(G,comm(Q,shift)),G);resolvent_identity+=1
 out['rank_perturbation_controls']=perturb;out['exact_resolvent_commutator_identities']=resolvent_identity
 # Reusing one changed parameter twice is TWO changed occurrences.
 n=16;pi=maps(4)[1];w0=[2]*n;w1=w0[:];w1[0]=3;G0=green(pi,w0);G1=green(pi,w1);single=rank(add(G1,G0,-1));squared=rank(add(mm(G1,G1),mm(G0,G0),-1));assert single==1 and squared==2
 out['shared_parameter_occurrence_control']={'single_resolvent_rank':single,'two_occurrences_difference_rank':squared,'distinct_changed_parameters':1,'charged_changed_occurrences':2}
 p=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
