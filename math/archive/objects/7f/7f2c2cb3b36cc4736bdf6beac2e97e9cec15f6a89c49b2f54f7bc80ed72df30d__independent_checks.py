#!/usr/bin/env python3
"""Fresh direct-matrix controls for paid sector shears, with own prior geometry."""
from pathlib import Path
import json,random
from itertools import product
from math import prod,gcd
from geometry import routes,cycles
from exact_utils import Field,prime_by_trial_division
BASE=Path(__file__).parent

def invperm(p):
 q=[None]*len(p)
 for i,j in enumerate(p):q[j]=i
 return q

def pmatrix(p):return [[int(p[j]==i) for j in range(len(p))] for i in range(len(p))]
def transpose(a):return list(map(list,zip(*a)))
def add(a,b,f,k=1):return [[(x+k*y)%f.p for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,t,f):return [[x*t%f.p for x in r] for r in a]
def left(a,d,f):return [[v*x%f.p for x in r] for r,v in zip(a,d)]
def right(a,d,f):return [[x*v%f.p for x,v in zip(r,d)] for r in a]
def green(p,t,f):
 a=add(f.eye(len(p)),pmatrix(p),f,-t);g=f.inverse(a)
 assert f.mul(a,g)==f.eye(len(p)) and f.mul(g,a)==f.eye(len(p))
 return g

def block(a,sig,tau,f):
 n=len(a)//2;h=f.inv(2)
 return [[h*(a[i][j]+tau*a[i][j+n]+sig*a[i+n][j]+sig*tau*a[i+n][j+n])%f.p for j in range(n)] for i in range(n)]

def reflect(p):
 order=[];v=0
 for k in range(len(p)):order.append(v);v=p[v]
 assert v==0 and len(set(order))==len(p)
 r=[None]*len(p)
 for k,v in enumerate(order):r[v]=order[-k%len(p)]
 return r

def paircheck(p0,p1,h,f,t,weighted=False):
 N=len(p0);n=N//2;I=f.eye(N);zero=[[0]*N for _ in range(N)]
 assert t and (1-pow(t,N,f.p))%f.p
 for p in (p0,p1):
  assert len(cycles(p))==1
  assert all(p[v+n]==(p[v]+n)%N for v in range(n))
  for v in range(N):
   w=v
   for _ in range(n):w=p[w]
   assert w==(v+n)%N
 assert [v%n for v in p0]==[v%n for v in p1]
 rel=[invperm(p0)[v] for v in p1];cc=cycles(rel);assert N-len(cc)==h
 g0,g1=green(p0,t,f),green(p1,t,f);k=add(g0,g1,f,-1)
 assert f.rank(k)==h and all(k[i+n][j]==-k[i][j]%f.p and k[j][i+n]==-k[j][i]%f.p for i in range(n) for j in range(N))
 C=block(k,-1,-1,f);assert f.rank(C)==h
 a=list(range(1,n+1)) if weighted else [1]*n
 b=list(range(n+1,2*n+1)) if weighted else [1]*n
 aa=a+[-x for x in a];bb=b+[-x for x in b]
 m=left(k,aa,f);assert f.mul(m,m)==zero
 results=[]
 for tr in (False,True):
  rev=right(transpose(k) if tr else k,bb,f);assert f.mul(rev,rev)==zero
  s=f.mul(add(I,m,f),add(I,rev,f));si=f.mul(add(I,rev,f,-1),add(I,m,f,-1))
  assert f.mul(s,si)==I and f.mul(si,s)==I and f.det(s)==1
  A=left(C,a,f);B=right(transpose(C) if tr else C,b,f)
  assert block(s,1,1,f)==add(f.eye(n),f.mul(A,B),f)
  assert block(s,1,-1,f)==A and block(s,-1,1,f)==B and block(s,-1,-1,f)==f.eye(n)
  ranks=[f.rank(A),f.rank(B)];rankdiff=f.rank(add(s,I,f,-1));assert ranks==[h,h] and rankdiff==2*h
  results.append({'transpose_reverse':tr,'cross_ranks':ranks,'rank_S_minus_I':rankdiff,'determinant':1,'both_inverse_products':True})
 # Reciprocal and reflection implementations, checked in full physical coordinates.
 for p,g in ((p0,g0),(p1,g1)):
  ip=invperm(p);gi=green(ip,t,f);gr=green(p,f.inv(t),f)
  assert gi==transpose(g)==add(I,gr,f,-1)
  r=reflect(p);assert all(r[r[v]]==v and r[p[r[v]]]==ip[v] for v in range(N))
  assert gi==[[g[r[i]][r[j]] for j in range(N)] for i in range(N)]
 if h==n:
  assert p1==[(v+n)%N for v in p0]
  T=block(pmatrix(p0),-1,-1,f)
  formula=scale(f.mul(T,f.inverse(add(f.eye(n),f.mul(T,T),f,-t*t))),2*t,f)
  assert C==formula and f.det(C)
 return {'N':N,'h':h,'relative_cycles':cc,'weighted':weighted,'shears':results}

def makepair(q,epsilon,flip):
 n=len(q)
 return [[q[k]+n*(s^epsilon[k]^(int(k in flip) if which else 0)) for s in range(2) for k in range(n)] for which in (0,1)]

def main():
 saved=json.loads((BASE/'sources/BIDIRECTIONAL_SHEAR_CONTROLS.json').read_text());p=saved['prime'];assert prime_by_trial_division(p);f=Field(p);t=f.inv(2);ps=routes();old=saved['original_nested_N64_pair']
 invs=[invperm(q) for q in ps];matches=[[j for j,q in enumerate(ps) if q==ip] for ip in invs]
 assert matches==old['all_eight_inverse_matches']==[[]]*8
 assert invs[0]==old['H0_minus_inverse_successor'] and invs[1]==old['H0_plus_inverse_successor']
 refs=[reflect(ps[j]) for j in (0,1)];assert refs==old['reflection_permutations']
 out=paircheck(ps[0],ps[1],16,f,t)
 assert out['relative_cycles']==old['relative_permutation_cycles']
 added=[v^32 for v in ps[0]];full=saved['one_added_order_full_coverage_N64']
 assert added==full['added_successor'] and added not in ps and not full['added_order_matches_existing']
 for v in range(64):
  w=v
  for _ in range(33):w=ps[0][w]
  assert w==added[v]
 o2=paircheck(ps[0],added,32,f,t);assert o2['relative_cycles']==full['relative_permutation_cycles']
 uniform=[]
 for rec in saved['uniform_instances']:
  N=rec['N'];n=N//2;q=[(k+1)%n for k in range(n)];epsilon=[int(k==n-1) for k in range(n)];flip=set(rec['flipped_base_edges']);assert len(flip)%2==0
  a,b=makepair(q,epsilon,flip);r=paircheck(a,b,len(flip),f,t)
  assert r['relative_cycles']==rec['relative_permutation_cycles'] and r['h']==rec['pair_difference_rank']
  for got,oldr in zip(r['shears'],rec['shears']):assert got['cross_ranks']==oldr['cross_ranks'] and got['rank_S_minus_I']==oldr['rank_S_minus_I']
  uniform.append(r)
 print('Original pair, added order, and all eight source uniform instances PASS',flush=True)
 # Nonconstant odd masks and independent pole/field controls.
 weighted=[]
 for prime,tn,td in [(p,2,1),(1000000007,3,5)]:
  assert prime_by_trial_division(prime);ff=Field(prime);tt=tn*ff.inv(td)%prime
  for a,b,h in [(ps[0],ps[1],16),(ps[0],added,32)]:
   r=paircheck(a,b,h,ff,tt,True);weighted.append({'prime':prime,'pole':[tn,td],'control':r})
 # Fresh arbitrary base cycles, odd voltage patterns, and all even-cardinality
 # toggle choices at small sizes. Includes h=0, odd n, and N=4 full coverage.
 rng=random.Random(341987);general=[];bad=[]
 for n in range(1,9):
  order=list(range(n));rng.shuffle(order);q=[None]*n
  for i,v in enumerate(order):q[v]=order[(i+1)%n]
  eps=[rng.randrange(2) for _ in range(n)];eps[-1]^=(1-sum(eps)%2)
  choices=[set(i for i in range(n) if (mask>>i)&1) for mask in range(1<<n) if mask.bit_count()%2==0]
  # All choices are checked combinatorially; every distinct rank choice
  # per size is also checked by full Green and shear matrices.
  for A in choices:
   a,b=makepair(q,eps,A);assert len(cycles(a))==len(cycles(b))==1
   rel=[invperm(a)[x] for x in b];assert 2*n-len(cycles(rel))==len(A)
  for h in sorted({len(A) for A in choices}):
   A=next(A for A in choices if len(A)==h);a,b=makepair(q,eps,A)
   r=paircheck(a,b,h,f,t,True);general.append({'n':n,'h':h,'rank_S_minus_I':r['shears'][0]['rank_S_minus_I']})
  a,b=makepair(q,eps,{0});assert len(cycles(a))==1 and len(cycles(b))==2
  fullflip=[(x+n)%(2*n) for x in a]
  assert len(cycles(fullflip))==(1 if n%2==0 else 2)
  bad.append({'n':n,'odd_toggle_cycles':2,'full_flip_cycles':len(cycles(fullflip))})
 # Generic rectangular-block algebra with noncommuting A,B and singular
 # diagonal I+AB cases. Enumeration over F3 of all 2x2 pairs is bounded.
 ff=Field(3);generic=0;singulardiag=0
 matrices=[[[v[0],v[1]],[v[2],v[3]]] for v in product(range(3),repeat=4)]
 for A in matrices:
  for B in matrices:
   ab=ff.mul(A,B);s=[[(int(i==j)+(ab[i][j] if i<2 and j<2 else A[i][j-2] if i<2 else B[i-2][j] if j<2 else 0))%3 for j in range(4)] for i in range(4)]
   diff=add(s,ff.eye(4),ff,-1)
   assert ff.rank(diff)==ff.rank(A)+ff.rank(B) and ff.det(s)==1
   if ff.det(add(ff.eye(2),ab,ff))==0:singulardiag+=1
   generic+=1
 out={'status':'ACCEPTED_PAID_BIDIRECTIONAL_SHEAR_PRIMITIVES','source_programs_executed':False,'original':out,'one_added_order':o2,'inverse_order_matches':matches,'source_uniform_instances':uniform,'weighted_multifield_controls':weighted,'arbitrary_voltage_rank_controls':general,'parity_negative_controls':bad,'generic_A_B_pairs_over_F3':generic,'singular_I_plus_AB_cases':singulardiag,'paid_costs':saved['per_shear_pair_application_cost'],'scope':'Explicit changed right-mask/residual/composition grammar, optional new routes or reciprocal poles; no Fourier or seed-preserving coefficient law.'}
 (BASE/'VERIFIED_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print('ALL INDEPENDENT CHECKS PASS',flush=True)
if __name__=='__main__':main()
