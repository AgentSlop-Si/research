#!/usr/bin/env python3
"""Independent exact spectral projector controls. Never imports uploaded code."""
import itertools,json,math,random,sys
from pathlib import Path
rng=random.Random(17101093)
def root(n,p):return next(w for w in range(1,p)if pow(w,n,p)==1 and len({pow(w,k,p)for k in range(n)})==n)
def prime(p):return p>=2 and all(p%q for q in range(2,math.isqrt(p)+1))
def fixture(n):
 p=n+1
 while not prime(p):p+=n
 return p,root(n,p)
def fftdirect(x,w,p):
 n=len(x);return [sum(v*pow(w,-k*j,p)for j,v in enumerate(x))%p for k in range(n)]
def oracle(x,w,p,K):
 X=fftdirect(x,w,p);n=len(x);return [sum(X[k]*pow(w,k*j,p)for k in K)*pow(n,-1,p)%p for j in range(n)]
def matrix(n,w,p,K):return [[sum(pow(w,k*(j-i),p)for k in K)*pow(n,-1,p)%p for i in range(n)]for j in range(n)]
def mm(a,b,p):return [[sum(x*y for x,y in zip(row,col))%p for col in zip(*b)]for row in a]
def madd(a,b,p,s=1):return [[(x+s*y)%p for x,y in zip(r,t)]for r,t in zip(a,b)]
def rank(a,p):
 a=[r[:]for r in a];r=0
 for j in range(len(a[0])):
  k=next((k for k in range(r,len(a))if a[k][j]),None)
  if k is None:continue
  a[r],a[k]=a[k],a[r];v=pow(a[r][j],-1,p);a[r]=[x*v%p for x in a[r]]
  for k in range(r+1,len(a)):
   v=a[k][j];a[k]=[(x-v*y)%p for x,y in zip(a[k],a[r])]
  r+=1
  if r==len(a):break
 return r
def weights(n,w,p,d,S):return [sum(pow(w,-a*ell*(n//d),p)for a in S)*pow(d,-1,p)%p for ell in range(d)]
def filt(x,w,p,d,S,plus,minus):
 n=len(x);c=weights(n,w,p,d,S)
 y=[sum(v*x[(j+l*(n//d))%n]for l,v in enumerate(c))%p for j in range(n)]
 for k,sgn in [(k,1)for k in plus]+[(k,-1)for k in minus]:
  a=sum(v*pow(w,-k*j,p)for j,v in enumerate(x))*pow(n,-1,p)%p
  y=[(v+sgn*a*pow(w,k*j,p))%p for j,v in enumerate(y)]
 return y
def batch(x,w,p,d,masks):
 n=len(x);bases={};atoms={};corrections={};out=[]
 for S,plus,minus in masks:
  S=tuple(sorted(S));e=tuple(sorted([(k,1)for k in plus]+[(k,-1)for k in minus]))
  if S not in bases:bases[S]=filt(x,w,p,d,S,[],[])
  if e not in corrections:
   z=[0]*n
   for k,s in e:
    if k not in atoms:atoms[k]=oracle(x,w,p,{k})
    z=[(a+s*b)%p for a,b in zip(z,atoms[k])]
   corrections[e]=z
  out.append([(a+b)%p for a,b in zip(bases[S],corrections[e])])
 return out,{'bases':len(bases),'atoms':len(atoms),'patterns':len(corrections),'output_entries':n*len(out)}
def poly(nodes,p):
 f=[1]
 for x in nodes:
  g=[0]*(len(f)+1)
  for i,c in enumerate(f):g[i]=(g[i]-x*c)%p;g[i+1]=(g[i+1]+c)%p
  f=g
 return f
def transfer(n,w,p,K):
 m=n//2;P=poly([pow(w,-k,p)for k in K],p);cols=[]
 for j in range(m):
  f=[0]*(m+j)+[1]
  for k in range(len(f)-1,m-1,-1):
   c=f[k]
   for l,v in enumerate(P):f[k-m+l]=(f[k-m+l]-c*v)%p
  cols.append(f[:m])
 return [list(r)for r in zip(*cols)]
def powcost(e):return 0 if not e else e.bit_length()-1+e.bit_count()
def factors(n):return [q for q in range(2,n+1)if n%q==0 and prime(q)]
def validation_cost(n):return powcost(n)+sum(powcost(n//q)for q in factors(n))
def single_cost(n,p,w,d,S,plus,minus):
 r=sum(v!=0 for v in weights(n,w,p,d,S));q=len(plus)+len(minus)
 plan=validation_cost(n)+n-1+2*powcost(p-2)+d*len(S)+d
 online=2*r*n+q*(6*n+1)+len(minus)
 return {'plan':plan,'online':online,'total':plan+online,'nonzero_comb_weights':r}
def main():
 paircount=0;maskcount=0
 for n,p in [(2,7),(3,7),(4,13),(5,11),(6,13)]:
  w=root(n,p);sets=[{i for i in range(n)if bits>>i&1}for bits in range(2**n)];mats=[matrix(n,w,p,K)for K in sets]
  for i,A in enumerate(sets):
   assert mm(mats[i],mats[i],p)==mats[i] and rank(mats[i],p)==len(A);maskcount+=1
   for j,B in enumerate(sets):
    C=matrix(n,w,p,A&B);assert mm(mats[i],mats[j],p)==mm(mats[j],mats[i],p)==C
    assert madd(madd(mats[i],mats[j],p),C,p,-1)==matrix(n,w,p,A|B)
    assert rank(madd(mats[i],mats[j],p,-1),p)==len(A^B);paircount+=1
 complete=[];wrong_sign=0;batchcases=[]
 for n in [6,8,12,15,16,24,30,32,48,64,96,128]:
  p,w=fixture(n);divs=[d for d in range(1,n+1)if n%d==0]
  for trial in range(12):
   d=divs[trial%len(divs)];S={a for a in range(d)if rng.randrange(2)};B={k for k in range(n)if k%d in S}
   plus=rng.sample(sorted(set(range(n))-B),min(2,n-len(B)));minus=rng.sample(sorted(B),min(2,len(B)))
   K=(B-set(minus))|set(plus);x=[rng.randrange(p)for _ in range(n)]
   y=filt(x,w,p,d,S,plus,minus);assert y==oracle(x,w,p,K) and filt(y,w,p,d,S,plus,minus)==y
   X=fftdirect(x,w,p);Y=fftdirect(y,w,p);assert Y==[X[k]if k in K else 0 for k in range(n)]
   base=matrix(n,w,p,B);actual=matrix(n,w,p,K)
   if n<=32:assert rank(madd(actual,base,p,-1),p)==len(plus)+len(minus)
   if minus and filt(x,w,p,d,S,plus+minus,[])!=y:wrong_sign+=1
   complete.append({'N':n,'p':p,'d':d,'q':len(plus)+len(minus),'output_entries':n})
  d=3 if n%3==0 else 2
  masks=[]
  for trial in range(6):
   S={trial%d};B={k for k in range(n)if k%d in S};plus=sorted(set(range(n))-B)[:1];minus=sorted(B)[:1];masks.extend([(S,plus,minus)]*2)
  x=[rng.randrange(p)for _ in range(n)];out,meta=batch(x,w,p,d,masks)
  for y,(S,plus,minus)in zip(out,masks):assert y==filt(x,w,p,d,S,plus,minus)
  saved=out[1][:];out[0][0]=(out[0][0]+1)%p;assert out[1]==saved
  batchcases.append({'N':n,**meta})
 contrasts=[];density=[]
 for n in [8,16,32]:
  p,w=fixture(n);A=(set(range(0,n,2))-{0})|{1};B=set(range(n))-A
  ra=transfer(n,w,p,A);rb=transfer(n,w,p,B)
  assert rank(madd(mm(ra,rb,p),mm(rb,ra,p),p,-1),p)==2
  pa=matrix(n,w,p,A);pb=matrix(n,w,p,B);assert mm(pa,pb,p)==mm(pb,pa,p)==[[0]*n for _ in range(n)]
  dense=sum(x!=0 for r in pa for x in r);assert dense==n*n
  contrasts.append({'N':n,'p':p,'quotient_commutator_rank':2,'projector_commutator_rank':0});density.append({'N':n,'p':p,'nonzeros':dense})
 costs=[]
 for n,expected,generic_expected in [(256,4405,6974),(1024,17487,33877),(4096,69715,159841),(16384,278625,737394),(65536,1114213,3342462)]:
  p,w=fixture(n);c=single_cost(n,p,w,2,{0},[1],[0]);generic=2*validation_cost(n)+3*n-2+3*n*(n.bit_length()-1)+powcost(n-1)+powcost(p-2)
  assert c['total']==expected and generic==generic_expected
  costs.append({'N':n,'p':p,'projector':c,'generic_double_FFT':generic})
 n=4096;p,w=fixture(n);sep=4*single_cost(n,p,w,4,{0},[1],[0])['total']+4*single_cost(n,p,w,4,{0,2},[1],[0])['total']
 plan=validation_cost(n)+n-1+2*powcost(p-2)+4*(1+2)+2*4
 combined=plan+12*n+2*(5*n+1)+2*n+8*n
 assert sep==623304 and combined==135266
 signatures=[]
 for n in range(2,65):
  B=(n-1).bit_length();assert len({tuple(k>>j&1 for j in range(B))for k in range(n)})==n and 2**(B-1)<n
  signatures.append({'N':n,'masks_required':B,'explicit_entries':n*B})
 r={'status':'PASS','uploaded_code_executed':False,'exhaustive_small_masks':maskcount,'exhaustive_mask_pairs':paircount,'complete_filter_cases':complete,'complete_filter_count':len(complete),'complete_output_entries':sum(c['output_entries']for c in complete),'wrong_sign_controls_detected':wrong_sign,'batch_cases':batchcases,'quotient_projector_contrasts':contrasts,'dense_projectors':density,'static_ledger_reconstructions':costs,'batch_static_ledger':{'N':4096,'separate':sep,'shared':combined,'all_requested_entries':4096*8},'binary_signature_cases':signatures,'large_uploaded_NTT_executed':False}
 path=Path(sys.argv[1]if len(sys.argv)>1 else 'INDEPENDENT_RESULTS.json');path.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n');print('PASS',paircount,'exhaustive mask pairs;',len(complete),'full filters;',len(batchcases),'shared batches')
if __name__=='__main__':main()
