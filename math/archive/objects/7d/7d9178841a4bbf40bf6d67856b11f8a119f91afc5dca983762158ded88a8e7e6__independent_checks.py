#!/usr/bin/env python3
"""Fresh exact chord identities, sharp examples and finite-field scope control."""
from pathlib import Path
import itertools as it,json,math,random,sys

def prime(p):return p>1 and all(p%d for d in range(2,math.isqrt(p)+1))
def root(n,p):return next(w for w in range(2,p) if pow(w,n,p)==1 and all(pow(w,d,p)!=1 for d in range(1,n) if n%d==0))
def h(t,a,b,p):return ((1-a*t)%p,t*(1-b*t)%p)
def determinant(v,w,p):return (v[0]*w[1]-v[1]*w[0])%p
def cycle(order):
 n=len(order);out=[0]*n
 for i,x in enumerate(order):out[x]=order[(i+1)%n]
 return out
def mul(A,B,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*B)] for row in A]
def denom(weights,pi,p):
 n=len(weights);A=[[int(i==j) for j in range(n)] for i in range(n)]
 for i in range(n):A[i][pi[i]]=(A[i][pi[i]]-weights[i])%p
 return A
def evaluate(n,p,w,a,b,pairs):
 ts=[pow(w,i,p) for i in range(n)];H=[h(t,a,b,p) for t in ts];assert all(v!=(0,0) for v in H)
 selected=[x for pair in pairs for x in pair];assert len(set(selected))==len(selected);order=selected+[i for i in range(n) if i not in selected];beta=cycle(order);weights=[0]*n
 for i,j in pairs:
  coordinate=next(k for k in range(2) if H[i][k]);weights[i]=H[j][coordinate]*pow(H[i][coordinate],-1,p)%p;assert all((weights[i]*H[i][k]-H[j][k])%p==0 for k in range(2))
 aa=[a,b]+[0]*(n-2);alpha=[(i+1)%n for i in range(n)];F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];T=mul(mul(denom(aa,alpha,p),F,p),denom(weights,beta,p),p);zeros=[j for j in range(n) if T[0][j]==T[1][j]==0];assert math.prod(aa)%p==math.prod(weights)%p==0
 return zeros,beta,weights

def main():
 sharp=[];identity_checks=0;rng=random.Random(35)
 for n in range(5,32,2):
  p=next(p for p in range(1000*n+1,1100*n,n) if prime(p));w=root(n,p);s1=(1+w*w)%p;s2=(w+pow(w,3,p))%p;d=(w*w-pow(w,4,p))%p;assert d;a=(s1-s2)*pow(d,-1,p)%p;z=(s1-a*w*w)%p;assert z;b=pow(z,-1,p);zeros,beta,weights=evaluate(n,p,w,a,b,[(0,2),(1,3)]);assert zeros==[2,3]
  vectors=[h(pow(w,i,p),a,b,p) for i in range(n)];pairs=[(i,j) for i,j in it.combinations(range(n),2) if determinant(vectors[i],vectors[j],p)==0];assert pairs==[(0,2),(1,3)];sharp.append(dict(N=n,p=p,root=w,a=a,b=b,joint_zero_columns=zeros,union_support=n-2))
  for trial in range(40):
   aa,bb,t,u=[rng.randrange(p) for _ in range(4)];assert determinant(h(t,aa,bb,p),h(u,aa,bb,p),p)==((u-t)*(1-bb*(t+u)+aa*bb*t*u))%p;identity_checks+=1
 # The complex geometric theorem cannot be transported to arbitrary fields.
 n=9;p=19;w=4;a=1;b=12;pairs=[(1,8),(2,5),(6,7)];zeros,beta,weights=evaluate(n,p,w,a,b,pairs);assert zeros==[5,7,8] and n-len(zeros)==6<n-2
 negative=dict(N=n,p=p,root=w,a=a,b=b,dependent_pairs=pairs,beta=beta,weights=weights,joint_zero_columns=zeros,union_support=6,claimed_complex_lower_bound=7,both_Green_denominators=1)
 # Exactly-zero column exceptional branch: all other columns independent.
 exceptional=[]
 for n,p,w in [(5,11,3),(9,19,4),(15,31,7)]:
  if not (pow(w,n,p)==1 and all(pow(w,k,p)!=1 for k in range(1,n))):w=root(n,p)
  ts=[pow(w,i,p) for i in range(n)];t0=ts[2];a=b=pow(t0,-1,p);vv=[h(t,a,b,p) for t in ts];assert vv[2]==(0,0);assert all(determinant(vv[i],vv[j],p) for i,j in it.combinations([i for i in range(n) if i!=2],2));exceptional.append(dict(N=n,p=p,zero_column=2))
 # Sparse bridge order and reachability bounds, exact polynomial supports.
 support=[]
 for n in [9,17,33,65,129]:
  for degree in range(5):
   budget=9*sum(4**r for r in range(degree+1));threshold=3*(4**(degree+1)-1);assert budget==threshold;support.append(dict(N=n,degree=degree,per_row_reachability_bound=budget,necessary_inequality=budget>=(n-2)/2))
 out=dict(status='PASS_WITH_COMPLEX_ONLY_SCOPE',determinant_identity_checks=identity_checks,sharp_cases=sharp,finite_field_counterexample=negative,zero_column_controls=exceptional,sparse_polynomial_budget_controls=support,source_code_executed=False)
 path=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).with_name('INDEPENDENT_RESULTS.json');path.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
if __name__=='__main__':main()
