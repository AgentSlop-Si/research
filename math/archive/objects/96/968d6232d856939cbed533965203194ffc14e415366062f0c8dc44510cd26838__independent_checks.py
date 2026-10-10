#!/usr/bin/env python3
"""Independently authored standard-library audit. Never loads uploaded code.
Direct transforms/convolutions are correctness oracles, not fast-path claims.
"""
from itertools import product
from math import comb,isqrt
from pathlib import Path
import argparse, hashlib, json, random, time
RNG=random.Random(202610092025)
COUNTS={}
def add(k,v=1):COUNTS[k]=COUNTS.get(k,0)+v

def prime(p):
 return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
def field(n):
 p=n+1
 while not prime(p):p+=n
 for w in range(1,p):
  if pow(w,n,p)==1 and all(pow(w,n//d,p)!=1 for d in range(2,n+1) if n%d==0 and prime(d)):
   return p,w
 raise AssertionError(n)
def table(n,w,p):
 a=[1]
 for _ in range(1,n):a.append(a[-1]*w%p)
 assert len(set(a))==n and a[-1]*w%p==1
 return a
def dft(x,w,p):
 n=len(x); a=table(n,w,p)
 return [sum(x[j]*a[-j*k%n] for j in range(n))%p for k in range(n)]
def expand(c,w,p):
 a=table(len(c),w,p)
 return [sum(v*a[h*u%len(c)] for h,v in enumerate(c))%p for u in range(len(c))]
def modes_direct(x,roots,p):
 m=len(x); iv=pow(m,-1,p)
 return [(h,sum(x[u]*roots[-h*u%m] for u in range(m))*iv%p) for h in range(m) if sum(x[u]*roots[-h*u%m] for u in range(m))%p]
def bm(y,p,cap,meter):
 # Dynamic connection polynomial; inverse of reference discrepancy is cached.
 C=[1];B=[1];L=0;age=1;inv_b=1
 for pos,v in enumerate(y):
  err=(v+sum(C[j]*y[pos-j] for j in range(1,L+1)))%p
  if not err:age+=1;continue
  newL=pos+1-L if 2*L<=pos else L
  if newL>cap:return None
  old=C[:];scale=err*inv_b%p
  C += [0]*max(0,len(B)+age-len(C))
  for j,b in enumerate(B):C[j+age]=(C[j+age]-scale*b)%p
  if newL>L:
   B=old;L=newL;inv_b=pow(err,-1,p);meter['inversions']+=1;age=1
  else:age+=1
  C += [0]*max(0,L+1-len(C))
 return C[:L+1]
def weights(nodes,y,p,meter):
 poly=[1]
 for z in nodes:
  nxt=[0]*(len(poly)+1)
  for j,v in enumerate(poly):nxt[j]=(nxt[j]-z*v)%p;nxt[j+1]=(nxt[j+1]+v)%p
  poly=nxt
 out=[];r=len(nodes)
 for z in nodes:
  q=[0]*r;q[-1]=1
  for j in range(r-2,-1,-1):q[j]=(poly[j+1]+z*q[j+1])%p
  den=0
  for j in range(r,0,-1):den=(den*z+j*poly[j])%p
  out.append(sum(a*b for a,b in zip(q,y))*pow(den,-1,p)%p);meter['inversions']+=1
 return out

def cap_modes(y,roots,p,cap,meter):
 c=bm(y,p,cap,meter)
 if c is None:return None
 r=len(c)-1
 if not r:return [] if not any(y) else None
 nodes=[]
 for h,z in enumerate(roots):
  v=0
  for coefficient in c:v=(v*z+coefficient)%p
  if v==0:nodes.append((h,z))
 if len(nodes)!=r:return None
 amplitudes=weights([v for h,v in nodes],y,p,meter)
 if not all(amplitudes):return None
 state=[1]*r
 for value in y:
  if sum(v*a for v,a in zip(state,amplitudes))%p!=value:return None
  state=[v*z%p for v,(h,z) in zip(state,nodes)]
 return [(h,a) for (h,z),a in zip(nodes,amplitudes)]

def discover(y,roots,p,budget):
 # Same mathematical doubling route, independently written.
 meter={'inversions':0,'caps':[],'dense':False,'sample_count':len(y)}
 if not any(y):return [],meter
 if budget==0:return None,meter
 m=len(y)
 if m>=3:
  limit=min(m//3,budget);cap=1
  while True:
   cap=min(cap,limit);meter['caps'].append(cap)
   ans=cap_modes(y,roots,p,cap,meter)
   if ans is not None:return ans,meter
   if cap==limit:break
   cap*=2
  if budget<m//3:return None,meter
 meter['dense']=True;meter['inversions']+=1
 ans=modes_direct(y,roots,p)
 return (ans if len(ans)<=budget else None),meter

def interleave(rows):
 q=len(rows);m=len(rows[0]);return [rows[t][u] for u in range(m) for t in range(q)]
def unweave(x,q):return [x[t::q] for t in range(q)]
def differences(rows,d,p):
 return [[sum((-1)**j*comb(d,j)*rows[t-j][u] for j in range(d+1))%p for u in range(len(rows[0]))] for t in range(d,len(rows))]
def raw_newton(x,q,d,budget,w,p):
 rows=unweave(x,q);m=len(rows[0]);roots=table(m,pow(w,q,p),p);events=[];left=budget;inversions=0
 for t,diff in enumerate(differences(rows,d,p),d):
  found,meter=discover(diff,roots,p,left);inversions+=meter['inversions']
  if found is None:return None,{'inversions':inversions,'rows_scanned':t-d+1}
  left-=len(found);events += [(t,h,c) for h,c in found]
 return ([dft(r,pow(w,q,p),p) for r in rows[:d]],events),{'inversions':inversions,'rows_scanned':q-d}
def batch_inv(a,p):
 if not a:return []
 prefix=[1]
 for x in a:prefix.append(prefix[-1]*x%p)
 cur=pow(prefix[-1],-1,p);out=[0]*len(a)
 for i in range(len(a)-1,-1,-1):out[i]=cur*prefix[i]%p;cur=cur*a[i]%p
 return out

def kernel(z,L,d,p,zinv,zL):
 if L==0:return 0
 if z==1:return comb(L+d-1,d)%p
 u=(1-z)%p;s=0;term=1
 for j in range(d):s=(s+comb(L+j-1,j)*term)%p;term=term*u%p
 return (1-zL*s)*pow(zinv,d,p)%p

def eval_newton(base,events,q,m,w,p):
 n=q*m;d=len(base);pw=table(n,w,p);invs=[0]+batch_inv([(1-pw[-k])%p for k in range(1,n)],p)
 forward=[[sum((-1)**(j-i)*comb(j,i)*base[i][h] for i in range(j+1))%p for h in range(m)] for j in range(d)]
 out=[];by_h=[[] for _ in range(m)]
 for t,h,c in events:by_h[h].append((t,c))
 for k in range(n):
  z=pw[-k%n];h=k%m
  value=sum(forward[j][h]*pw[-k*j%n]*kernel(z,q-j,j+1,p,invs[k],pw[-k*(q-j)%n]) for j in range(d))
  for t,c in by_h[h]:value+=m*c*pw[-k*t%n]*kernel(z,q-t,d,p,invs[k],pw[-k*(q-t)%n])
  out.append(value%p)
 return out

def build_rows(q,m,d,initial,spectral_events,eta,p):
 rows=[r[:] for r in initial]
 for t in range(d,q):
  force=expand(spectral_events[t],eta,p)
  rows.append([(force[u]+sum((-1)**(j+1)*comb(d,j)*rows[t-j][u] for j in range(1,d+1)))%p for u in range(m)])
 return rows

def rank(A,p):
 a=[r[:] for r in A];r=0
 for h in range(len(a[0])):
  t=next((t for t in range(r,len(a)) if a[t][h]),None)
  if t is None:continue
  a[r],a[t]=a[t],a[r];iv=pow(a[r][h],-1,p);a[r]=[v*iv%p for v in a[r]]
  for t in range(r+1,len(a)):
   scale=a[t][h];a[t]=[(x-scale*y)%p for x,y in zip(a[t],a[r])]
  r+=1
  if r==len(a):break
 return r

def graph(A,B,q,m,eta,p):
 C=[[0]*m for _ in range(q)];edges=0
 for a in range(q):
  for b in range(q):
   for h in range(m):
    if A[a][h] and B[b][h]:
     edges+=1;C[(a+b)%q][h]=(C[(a+b)%q][h]+m*A[a][h]*B[b][h]*pow(eta,(-h*((a+b)//q))%m,p))%p
 return C,edges

def reconstruct_differences(C,d,eta,p):
 q=len(C);m=len(C[0]);roots=table(m,eta,p)
 def sparse_expand(row):
  support=[(h,c) for h,c in enumerate(row) if c]
  return [sum(c*roots[h*u%m] for h,c in support)%p for u in range(m)]
 out=[sparse_expand(r) for r in C[:d]]
 delta=differences(C,d,p)
 for t,row in enumerate(delta,d):
  force=sparse_expand(row)
  out.append([(force[u]+sum((-1)**(j+1)*comb(d,j)*out[t-j][u] for j in range(1,d+1)))%p for u in range(m)])
 return interleave(out)
def conv(x,y,p):
 n=len(x);return [sum(x[j]*y[(k-j)%n] for j in range(n))%p for k in range(n)]
def counts(C,p,d=1):
 return {'S':sum(v!=0 for r in C for v in r),'H':sum(any(row[h] for row in C) for h in range(len(C[0]))),'rank':rank(C,p),'V':sum(v!=0 for row in differences(C,d,p) for v in row),'root':sum(v!=0 for r in C[:d] for v in r)}

def greedy_resets(supports,R,B):
 spent=0;anchors=1;reset=[]
 for t,k in enumerate(supports,1):
  if k+spent<=R:spent+=k
  elif anchors<B:anchors+=1;reset.append(t)
  else:return False,reset,spent
 return True,reset,spent

def exact_resets(supports,R,B):
 removed=sorted(range(len(supports)),key=lambda i:(-supports[i],i))[:B-1]
 return sum(k for i,k in enumerate(supports) if i not in removed)<=R,[i+1 for i in removed]

def run():
 start=time.time();details={}
 # All short binomial kernels, including zero length and singular z=1.
 for p in [7,17,31]:
  for z in range(p):
   for d in range(1,7):
    for L in range(20):
     got=kernel(z,L,d,p,pow((1-z)%p,-1,p) if z!=1 else 0,pow(z,L,p))
     want=sum(comb(v+d-1,d-1)*pow(z,v,p) for v in range(L))%p
     assert got==want,(p,z,d,L);add('kernel_identities')
 # Exhaustive budget membership; no uploaded recognizer is called.
 for m,p,w in [(3,7,2),(4,5,2)]:
  roots=table(m,w,p)
  for y in product(range(p),repeat=m):
   truth=modes_direct(y,roots,p)
   for b in range(m+1):
    ans,meter=discover(y,roots,p,b)
    assert (ans is not None)==(len(truth)<=b)
    if ans is not None:assert ans==truth
    assert meter['inversions']<=8*b+1
    add('exhaustive_budget_tests')
 for m in [6,7,8,9,12,16,25]:
  p,w=field(m);roots=table(m,w,p)
  for trial in range(100):
   if trial<50:
    c=[0]*m
    for h in RNG.sample(range(m),RNG.randrange(m+1)):c[h]=RNG.randrange(1,p)
    y=expand(c,w,p)
   else:y=[RNG.randrange(p) for _ in range(m)]
   truth=modes_direct(y,roots,p)
   for b in sorted(set([0,1,m//3,max(0,len(truth)-1),len(truth),m])):
    ans,meter=discover(y,roots,p,b)
    assert (ans is not None)==(len(truth)<=b)
    if ans is not None:assert ans==truth
    assert meter['inversions']<=8*b+1
    add('random_budget_tests')
 # Exact full-vector Newton outputs including nonsquare/odd sizes and d=q.
 for q,m in [(2,3),(3,3),(3,4),(4,3),(4,4),(5,5),(5,7),(6,4),(6,6),(7,5),(8,8),(9,6)]:
  n=q*m;p,w=field(n);eta=pow(w,q,p)
  for d in range(1,min(4,q)+1):
   for trial in range(12):
    initial=[[RNG.randrange(p) for _ in range(m)] for _ in range(d)];ev=[[0]*m for _ in range(q)];left=q
    for t in range(d,q):
     for h in RNG.sample(range(m),RNG.randrange(min(m,left)+1)):
      ev[t][h]=RNG.randrange(1,p);left-=1
    rows=build_rows(q,m,d,initial,ev,eta,p);x=interleave(rows)
    cert,meter=raw_newton(x,q,d,q,w,p);assert cert is not None
    assert meter['rows_scanned']==q-d and meter['inversions']<=8*q+1
    got=eval_newton(*cert,q,m,w,p);assert got==dft(x,w,p)
    add('newton_full_vectors');add('newton_full_bins',n)
    if left<q:
     failed,_=raw_newton(x,q,d,q-left-1,w,p);assert failed is None;add('newton_tight_budget_rejections')
   for trial in range(8):
    x=[RNG.randrange(p) for _ in range(n)];rows=unweave(x,q)
    truth=sum(len(modes_direct(diff,table(m,eta,p),p)) for diff in differences(rows,d,p))
    cert,meter=raw_newton(x,q,d,q,w,p)
    assert (cert is not None)==(truth<=q);assert meter['inversions']<=8*q+1
    add('arbitrary_newton_membership_controls')
 # Old graph adversary: its rank grows, so new delta gate complements fixed rank.
 graph_results=[]
 for s,m in [(2,4),(3,9),(4,16),(5,25),(2,32),(3,81)]:
  q=s*s;n=q*m;p,w=field(n);eta=pow(w,q,p)
  A=[[int(h==t%s) for h in range(m)] for t in range(q)]
  B=[[int(h==t//s) for h in range(m)] for t in range(q)]
  C,edges=graph(A,B,q,m,eta,p);stats=counts(C,p)
  assert stats['S']==s*q and stats['V']==s-1 and stats['root']==s and stats['rank']==s
  # h-column carry flips exactly at t=h(s+1).
  for h in range(s):
   for t in range(q):assert C[t][h]==m*pow(eta,-h if t<h*(s+1) else 0,p)%p
  x=interleave([expand(r,eta,p) for r in A]);y=interleave([expand(r,eta,p) for r in B])
  out=reconstruct_differences(C,1,eta,p);assert out==conv(x,y,p)
  assert out==reconstruct_differences(C,2,eta,p)
  graph_results.append(dict(s=s,q=q,m=m,n=n,p=p,edges=edges,**stats));add('graph_full_vectors');add('graph_full_bins',n)
 details['graph_adversary']=graph_results
 # Rank-one graph inputs with high temporal variation: rank gate saves cases
 # that both literal state and first-difference gates reject.
 rank_examples=[]
 for s in [3,4,5]:
  q=m=s*s;n=q*m;p,w=field(n);eta=pow(w,q,p)
  A=[[0]*m for _ in range(q)];B=[[0]*m for _ in range(q)]
  # Label h at x-row h+s*v; y intervals overlap at most twice.
  # Carry cancellation leaves a common repeating nonconstant row factor.
  for h in range(s):
   for v in range(s):A[h+s*v][h]=pow(eta,h*((h+v)//s),p)
   for z in range(s):B[(s-1)*h+z][h]=1+z%2
  C,edges=graph(A,B,q,m,eta,p);stats=counts(C,p)
  assert stats['rank']==1 and stats['S']>2*q and stats['root']+stats['V']>2*q
  expected=[[m*(1+(t%s)%2)%p if h<s else 0 for h in range(m)] for t in range(q)]
  assert C==expected
  x=interleave([expand(r,eta,p) for r in A]);y=interleave([expand(r,eta,p) for r in B])
  out=reconstruct_differences(C,1,eta,p)
  assert out==conv(x,y,p)
  add('rank_high_variation_full_vectors');add('rank_high_variation_full_bins',n)
  rank_examples.append(dict(q=q,m=m,edges=edges,**stats))
 details['rank_high_variation_graph_controls']=rank_examples
 # General higher-difference output reconstruction on arbitrary coefficient
 # matrices, without presuming every matrix arises from sparse-input graph.
 for q,m in [(4,16),(7,5),(9,27)]:
  p,w=field(q*m);eta=pow(w,q,p)
  for d in range(1,min(4,q)+1):
   for _ in range(10):
    C=[[RNG.randrange(p) for _ in range(m)] for _ in range(q)]
    assert reconstruct_differences(C,d,eta,p)==interleave([expand(r,eta,p) for r in C]);add('higher_difference_matrix_checks')
 # Exact optional reset counterexample.
 p=17;w=3;q=m=4;rows=[[0]*4,[4,0,0,0],[5,1,1,1],[6,2,2,2]]
 x=interleave(rows);support=[len(modes_direct(v,table(m,pow(w,q,p),p),p)) for v in differences(rows,1,p)]
 assert support==[4,1,1] and greedy_resets(support,4,2)[0] is False and exact_resets(support,4,2)[0] is True
 details['reset_counterexample']={'q':q,'m':m,'p':p,'omega':w,'raw':x,'transition_supports':support,'greedy':greedy_resets(support,4,2),'optimal':exact_resets(support,4,2),'spectrum':dft(x,w,p)}
 # Exhaustive reset optimization against all subsets.
 from itertools import combinations
 for length in range(1,6):
  for support in product(range(5),repeat=length):
   for B in [1,2,3]:
    for R in [0,1,4,7]:
     oracle=any(sum(v for i,v in enumerate(support) if i not in rem)<=R for k in range(min(B-1,length)+1) for rem in combinations(range(length),k))
     assert exact_resets(support,R,B)[0]==oracle;add('reset_optimizer_checks')
 # A chosen-divisor witness for first differences with c=1.
 q0=2;q1=3;n=12;p=13;w=2;m=6;eta=pow(w,q0,p)
 for attempt in range(100):
  base=[RNG.randrange(p) for _ in range(m)];ev=[RNG.randrange(1,p) if h<2 else 0 for h in range(m)]
  rows=[base,[(a+b)%p for a,b in zip(base,expand(ev,eta,p))]];x=interleave(rows)
  c0,_=raw_newton(x,q0,1,q0,w,p);c1,_=raw_newton(x,q1,1,q1,w,p)
  if c0 is not None and c1 is None:
   details['default_divisor_counterexample']={'n':n,'p':p,'omega':w,'raw':x,'accepted_q':q0,'default_rejected_q':q1,'accepted_events':len(c0[1]),'default_difference_supports':[len(modes_direct(v,table(4,pow(w,3,p),p),p)) for v in differences(unweave(x,3),1,p)]};break
 else:raise AssertionError('no selector witness')
 # Full-rank dense-spectral rows: a dense baseline plus distinct new modes.
 p=257;q=m=8;n=64;w=next(w for w in range(2,p) if pow(w,n,p)==1 and pow(w,n//2,p)!=1);eta=pow(w,q,p)
 coeff=[[1]*m]
 for t in range(1,q):r=coeff[-1][:];r[t]+=1;coeff.append(r)
 rows=[expand(r,eta,p) for r in coeff];x=interleave(rows)
 assert rank(rows,p)==q and all(all(r) for r in coeff)
 cert,_=raw_newton(x,q,1,q,w,p);assert len(cert[1])==q-1 and eval_newton(*cert,q,m,w,p)==dft(x,w,p)
 details['dense_full_rank']={'q':q,'m':m,'rank':q,'spectral_nonzeros':q*m,'events':q-1};add('dense_full_rank_full_vectors')
 # Exhaustive family-count identity via invertible difference coordinates.
 q=m=2;p=5;w=2;seen={};roots=table(m,pow(w,q,p),p)
 for x in product(range(p),repeat=q*m):
  r=len(modes_direct(differences(unweave(x,q),1,p)[0],roots,p));seen[r]=seen.get(r,0)+1
 assert seen=={e:p**m*comb((q-1)*m,e)*(p-1)**e for e in range(m+1)}
 details['exact_family_count_control']=seen
 return {'status':'PASS','method':'Independent mathematical mechanisms and direct oracles; no uploaded code execution','counts':COUNTS,'details':details,'elapsed_seconds':round(time.time()-start,3)}

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output');args=parser.parse_args();result=run();txt=json.dumps(result,indent=2,sort_keys=True)+'\n'
 if args.output:Path(args.output).write_text(txt)
 print(txt)
