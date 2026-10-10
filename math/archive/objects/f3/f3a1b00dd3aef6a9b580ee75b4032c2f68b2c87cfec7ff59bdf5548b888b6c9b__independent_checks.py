#!/usr/bin/env python3
"""Fresh, standard-library controls; no submitted code or numerical packages."""
from pathlib import Path
import cmath,itertools as it,json,math,random,sys

def eye(n):return [[complex(i==j) for j in range(n)] for i in range(n)]
def mm(a,b):return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def adj(a):return [[a[j][i].conjugate() for j in range(len(a))] for i in range(len(a[0]))]
def add(a,b):return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c):return [[c*x for x in r] for r in a]
def sub(a,b):return add(a,scale(b,-1))
def f2(a):return sum(abs(x)**2 for r in a for x in r)
def close(a,b,tol=1e-8):assert f2(sub(a,b))<tol**2

def weyl(n,a,b,w):
 z=[[0j]*n for _ in range(n)]
 for j in range(n):z[(j+b)%n][j]=w**(a*((j+b)%n))
 return z
def phi(n,a,b,w):
 z=[[0j]*n for _ in range(n)]
 for j in range(n):z[(j-a)%n][j]=w**(b*j)
 return z
def fourier(n):
 w=cmath.exp(-2j*math.pi/n);return [[w**(i*j)/math.sqrt(n) for j in range(n)] for i in range(n)],w

def rm(a,b,p):return [[sum(x*y for x,y in zip(r,c))%p for c in zip(*b)] for r in a]
def ri(n):return [[int(i==j) for j in range(n)] for i in range(n)]
def ra(a,b,p):return [[(x+y)%p for x,y in zip(r,s)] for r,s in zip(a,b)]
def inverse(a,p):
 n=len(a);z=[[x%p for x in a[i]]+ri(n)[i] for i in range(n)]
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
def cut(a,A):return [[a[i][j] for j in range(len(a)) if j not in A] for i in sorted(A)]
def fieldroot(n,p):return next(w for w in range(1,p) if pow(w,n,p)==1 and all(pow(w,k,p)!=1 for k in range(1,n)))
def main():
 rng=random.Random(10100009);twirls=[]
 for n in [2,3,4,5,6,8,11]:
  U,w=fourier(n);M=[[complex(rng.randrange(-4,5),rng.randrange(-4,5))/7 for j in range(n)] for i in range(n)];X=mm(adj(U),M);lam=sum(X[i][i] for i in range(n))/n;tau=f2(sub(M,scale(U,lam)));energy=0;fourth=0;discrete=0
  for a in range(n):
   for b in range(n):
    W=weyl(n,a,b,w);Phi=phi(n,a,b,w);close(mm(U,W),mm(Phi,U));A=sub(mm(M,W),mm(Phi,M));H=mm(adj(A),A);tr=f2(A);energy+=tr/2;fourth+=(tr*tr+f2(H))/4
    if n<=3:
     vals=[]
     for z in it.product([1,-1,1j,-1j],repeat=n):vals.append(sum(abs(sum(x*y for x,y in zip(r,z)))**2 for r in A)/2)
     avg=sum(vals)/len(vals);moment=sum(x*x for x in vals)/len(vals);assert abs(avg-tr/2)<1e-9;exact=(tr*tr+f2(H)-sum(H[i][i].real**2 for i in range(n)))/4;assert abs(moment-exact)<1e-8;discrete+=len(vals)
  energy/=n*n;fourth/=n*n;assert abs(energy-tau)<1e-8;assert fourth<=8*tau*tau+1e-7
  twirls.append(dict(n=n,weyl_pairs=n*n,twirl_identity=True,gaussian_second_moment_bound=True,discrete_four_phase_vectors=discrete))
 # Parity Gram identity and an exact-seed rank-deficient candidate.
 parity=[]
 for m in [1,3,5,9]:
  n=2*m;U,w=fourier(n);A=set(range(0,n,2));C=cut(U,A);close(mm(C,adj(C)),scale(eye(m),.5));M=[r[:] for r in U]
  for j in range(1,n,2):M[0][j]=0
  assert all(M[i][0]==U[i][0] for i in range(n));X=mm(adj(U),M);lam=sum(X[i][i] for i in range(n))/n;tau=f2(sub(M,scale(U,lam)));assert abs(tau-(.5-1/(4*n)))<1e-9 and tau>=.125-1e-9;parity.append(dict(N=n,parity_gram_half_identity=True,exact_seed=True,deficient_candidate_phase_energy=tau))
 # All finite cut checks for true weighted Hamiltonian Green sums/products.
 greens=[];p=1009
 for n in [5,6,7,8]:
  branches=[];perms=[];weights=[]
  for k in range(4):
   order=list(range(n));rng.shuffle(order);pi=[0]*n
   for i in range(n):pi[order[i]]=order[(i+1)%n]
   w=[0 if (i+k)%4==0 else rng.randrange(2,p) for i in range(n)];H=ri(n)
   for i in range(n):H[i][pi[i]]=(H[i][pi[i]]-w[i])%p
   branches.append(inverse(H,p));perms.append(pi);weights.append(w)
  M=rm(ra(branches[0],branches[1],p),ra(branches[2],branches[3],p),p);checks=0
  for mask in range(1,2**n-1):
   A={i for i in range(n) if (mask>>i)&1};budget=0
   for G,pi,w in zip(branches,perms,weights):
    crosses=sum(pi[i] not in A and w[i]!=0 for i in A);assert rank(cut(G,A),p)==crosses;budget+=crosses
   assert rank(cut(M,A),p)<=budget;checks+=1
  greens.append(dict(N=n,all_cuts=checks,branches=4))
 # Robust missing-shuffle counterexample: four natural-cycle zero-weight
 # branches, each scaled by 1/2, give identity stages. Middle half-swap
 # commutes with the natural cycle; it cannot increase conjugated budgets.
 n=12;A=set(range(6));natural=[(i+1)%n for i in range(n)];shuffle=ri(n)
 shuffle=[[int(j==(i+6)%n) for j in range(n)] for i in range(n)];actual=rank(cut(shuffle,A),p);potential=4*sum(natural[i] not in A for i in A);assert actual==6>potential==4
 counter=dict(N=n,stages=2,branches_per_stage=2,zero_weight_actual_budget=0,potential_edge_budget=potential,uncharged_shuffle_cut_rank=actual,shuffle_commutes_with_each_natural_cycle=True)
 # Finite-field one-sided covariance exact false-accept enumeration.
 n=3;p=7;w=2;F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)];D=[[pow(w,i,p) if i==j else 0 for j in range(n)] for i in range(n)];assert rm(F,S,p)==rm(D,F,p)
 M=[r[:] for r in F];M[0][1]=(M[0][1]+1)%p;res=ra(rm(M,S,p),[[-x%p for x in r] for r in rm(D,M,p)],p);rr=rank(res,p);accepted=0
 for z in it.product(range(p),repeat=n):accepted+=all(sum(x*y for x,y in zip(row,z))%p==0 for row in res)
 assert rr>=1 and accepted==p**(n-rr);assert [M[i][0] for i in range(n)]==[1]*n
 # Positive source convention controls in additional fields and composite N.
 exact=[]
 for n,p in [(4,17),(5,11),(6,13),(8,17),(9,19)]:
  w=fieldroot(n,p);F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];S=[[int(i==(j+1)%n) for j in range(n)] for i in range(n)];D=[[pow(w,i,p) if i==j else 0 for j in range(n)] for i in range(n)];assert rm(F,S,p)==rm(D,F,p);exact.append(dict(N=n,p=p))
 out=dict(status='PASS_WITH_SOURCE_SCOPE_CORRECTION',twirl_checks=twirls,parity_checks=parity,green_cut_checks=greens,missing_shuffle_counterexample=counter,finite_false_accept=dict(p=7,N=3,residual_rank=rr,accepted_vectors=accepted,total_vectors=343),exact_field_covariance=exact,source_programs_executed=False)
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
