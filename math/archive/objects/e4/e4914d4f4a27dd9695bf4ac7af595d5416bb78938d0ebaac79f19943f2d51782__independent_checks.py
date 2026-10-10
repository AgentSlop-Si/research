#!/usr/bin/env python3
"""Independent audit: direct Leibniz integer polynomials, exact divisions,
modular coprimality certificates, and regenerated nested route matrices.
No source or constructor program is executed or imported.
"""
from pathlib import Path
from itertools import permutations,product
from fractions import Fraction
from collections import Counter
from math import prod
import json,hashlib
from geometry import routes,cycles,LABELS
from exact_utils import Field,prime_by_trial_division
BASE=Path(__file__).parent
P=998244353

def trim(a):
 a=list(a)
 while a and not a[-1]:a.pop()
 return a

def dense(p):
 a=[0]*(max((k for k,v in p),default=-1)+1)
 for k,v in p:a[k]=v
 return trim(a)

def sparse(a):return [[k,v] for k,v in enumerate(a) if v]

def mulpoly(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  if x:
   for j,y in enumerate(b):
    if y:c[i+j]+=x*y
 return trim(c)

def divexact(a,b):
 a=trim(a);b=trim(b);q=[0]*max(0,(len(a)-len(b)+1))
 while a and len(a)>=len(b):
  assert a[-1]%b[-1]==0
  z=a[-1]//b[-1];k=len(a)-len(b);q[k]=z
  for j,v in enumerate(b):a[k+j]-=z*v
  a=trim(a)
 assert not a
 return trim(q)

def modrem(a,b,p):
 a=trim([v%p for v in a]);b=trim([v%p for v in b]);ib=pow(b[-1],-1,p)
 while len(a)>=len(b):
  z=a[-1]*ib%p;k=len(a)-len(b)
  for j,v in enumerate(b):a[k+j]=(a[k+j]-z*v)%p
  a=trim(a)
 return a

def gcdmod(a,b,p):
 a=trim([v%p for v in a]);b=trim([v%p for v in b])
 while b:a,b=b,modrem(a,b,p)
 return [x*pow(a[-1],-1,p)%p for x in a]

def detinteger(a):
 b=[r[:] for r in a];sgn=1;prev=1
 for k in range(len(b)-1):
  t=next((i for i in range(k,len(b)) if b[i][k]),None)
  if t is None:return 0
  if t!=k:b[t],b[k]=b[k],b[t];sgn=-sgn
  z=b[k][k]
  for i in range(k+1,len(b)):
   for j in range(k+1,len(b)):
    w=b[i][j]*z-b[i][k]*b[k][j];assert w%prev==0;b[i][j]=w//prev
   b[i][k]=0
  prev=z
 return sgn*b[-1][-1]

PERMS={n:[(s,(-1)**sum(s[i]>s[j] for i in range(n) for j in range(i+1,n))) for s in permutations(range(n))] for n in (7,8)}
def monomialdet(a):
 # Entry is (integer sign, nonnegative exponent); enumerate every term.
 out={};n=len(a)
 for s,sg in PERMS[n]:
  deg=0;v=sg
  for i,j in enumerate(s):v*=a[i][j][0];deg+=a[i][j][1]
  out[deg]=out.get(deg,0)+v
 return dense([[k,v] for k,v in out.items() if v])

def positions(ps):
 out=[]
 for p in ps:
  pos=[None]*64;v=0
  for k in range(64):assert pos[v] is None;pos[v]=k;v=p[v]
  assert v==0;out.append(pos)
 return out

def monomialframe(pos,i,sig):
 return [[(sig**(((po[i]-po[k])%64)//32),(po[i]-po[k])%32) for k in range(32)] for po in pos]

def evalframe(pos,i,sig,taus,f):
 return [[sg*pow(t,q,f.p)*f.inv(1-sig*pow(t,32,f.p))%f.p for sg,q in row] for row,t in zip(monomialframe(pos,i,sig),taus)]

def makegreens(ps,t,f):
 out=[]
 for p in ps:
  a=f.eye(64)
  for j,i in enumerate(p):a[i][j]=(a[i][j]-t)%f.p
  g=f.inverse(a);assert f.mul(a,g)==f.eye(64);out.append(g)
 return out

def verify():
 f=Field(P);assert prime_by_trial_division(P)
 signed=json.loads((BASE/'sources/SIGNED_POLE_FAMILY_CERTIFICATE.json').read_text())
 common=json.loads((BASE/'sources/COMMON_POLE_SPAN_CERTIFICATE.json').read_text())
 ps=routes();pos=positions(ps)
 for label,p,saved in zip(LABELS,ps,common['routes']):
  assert list(label)==saved['label'] and p==saved['successor']
  assert all(p[v^32]==(p[v]^32) for v in range(64))
  for v in range(64):
   w=v
   for _ in range(32):w=p[w]
   assert w==(v^32)
  q=[p[v]%32 for v in range(32)];sg=[(-1)**(p[v]//32) for v in range(32)]
  assert q==saved['sector_successor'] and sg==saved['minus_sector_edge_signs']
  assert len(cycles(q))==1 and prod(sg)==saved['minus_holonomy']==-1
 assert [v%32 for v in ps[0]]==[v%32 for v in ps[1]]
 inv=[None]*64
 for v,w in enumerate(ps[0]):inv[w]=v
 rel=[inv[w] for w in ps[1]];cc=cycles(rel)
 assert cc==common['relative_H0_permutation_cycles']==signed['mixing_component']['relative_permutation_cycles']
 assert Counter(map(len,cc))=={1:32,2:16}
 # Regenerate tables and finite sign schedules, using the frame formula.
 for saved in signed['target_pole_equations']:
  i=saved['physical_row'];a=monomialframe(pos,i,-1);b=monomialframe(pos,i,1)
  assert [[q for s,q in r] for r in a]==saved['exponents']
  assert [[s for s,q in r] for r in a]==saved['minus_signs']
  assert saved['plus_signs']=='all +1' and all(s==1 for r in b for s,q in r)
 assert len(signed['schedules'])==256
 assert {tuple(x['pole_signs']) for x in signed['schedules']}==set(product((-1,1),repeat=8))
 counts=Counter();finite=[]
 for schedule in signed['schedules']:
  signs=schedule['pole_signs'];taus=[s*f.inv(2)%P for s in signs]
  assert all((1-pow(t,64,P))%P for t in taus)
  dets=[]
  for w in schedule['minus_sector_witnesses']:
   a=evalframe(pos,w['row'],-1,taus,f);m=[[r[c] for c in w['columns']] for r in a]
   d=f.det(m);assert d==w['determinant_mod_p'] and d and f.rank(a)==8;dets.append(d)
  a=evalframe(pos,0,1,taus,f);rank=f.rank(a);assert rank==schedule['plus_sector_rank']
  if signs[0]==signs[1]:
   assert a[0]==a[1] and rank==7
   w=schedule['plus_rank_seven_witness'];d=f.det([[a[r][c] for c in w['columns']] for r in w['rows']]);assert d==w['determinant_mod_p'] and d
  else:
   assert rank==8
   # Source stores the value but not columns for this nonzero minor.
   # An independently selected pivot minor certifies its rank instead.
   cols=[]
   for c in range(32):
    trial=cols+[c]
    if f.rank([[r[k] for k in trial] for r in a])>len(cols):cols=trial
    if len(cols)==8:break
   d=f.det([[r[c] for c in cols] for r in a]);assert d==schedule['plus_sector_nonzero_minor'] and d
  counts[rank]+=1;finite.append({'signs':signs,'minus_minor_residues':dets,'plus_rank':rank})
 assert counts=={7:128,8:128}
 print('All 256 signed half-pole schedules PASS',flush=True)
 # Full integer determinant polynomials, exact common factors, and rational
 # coprimality proved by a good-prime resultant certificate (gcd mod p=1).
 assert [r['physical_row'] for r in common['rows']]==list(range(32))
 guards=[];polycount=0
 for record in common['rows']:
  i=record['physical_row'];s=record['sectors']['-1'];polys=[]
  for sig in (-1,1):
   for saved in record['sectors'][str(sig)]['minors']:
    a=monomialframe(pos,i,sig);rows=saved['term_rows'];cols=saved['physical_columns']
    assert len(rows)==len(cols)==(8 if sig==-1 else 7) and len(set(cols))==len(cols)
    m=[[a[r][c] for c in cols] for r in rows];d=monomialdet(m)
    assert sparse(d)==saved['determinant_polynomial'];polycount+=1
    at2=detinteger([[sg*2**q for sg,q in r] for r in m]);assert at2==sum(v*2**k for k,v in enumerate(d))
    if sig==-1:polys.append(d)
    else:
     half=sum(Fraction(v,2**k) for k,v in enumerate(d));assert half
     vp=evalframe(pos,i,1,[f.inv(2)]*8,f);assert f.rank(vp)==7 and vp[0]==vp[1]
  d=dense(s['monic_gcd']);assert d[-1]==1
  quot=[divexact(a,d) for a in polys]
  # Each quotient retains its degree modulo this prime. The modular gcd 1
  # certifies their resultant is nonzero, hence coprime over Q.
  assert all(a[-1]%P for a in quot);assert gcdmod(*quot,P)==[1]
  g=s['guard_factorization'];v=g['zero_valuation'];fact=[0]*v+[1];layers=[]
  for layer in g['root_of_unity_layers']:
   a=dense(layer);divexact([-1]+[0]*63+[1],a);fact=mulpoly(fact,a);layers.append(len(a)-1)
  assert fact==d
  assert monomialframe(pos,i+32,-1)==[[(-sg,q) for sg,q in r] for r in monomialframe(pos,i,-1)]
  assert monomialframe(pos,i+32,1)==monomialframe(pos,i,1)
  guards.append({'row':i,'gcd':sparse(d),'zero_valuation':v,'root_of_unity_layer_degrees':layers,'quotient_degrees':[len(a)-1 for a in quot],'coprimality_prime':P})
  print('Integer determinants and exact gcd guard PASS row',i,flush=True)
 assert polycount==96
 # Independently inverted 64-point matrices verify every frame entry,
 # resolvent rank, and sector support at multiple legal poles and primes.
 controls=[]
 for prime,tn,td in [(P,1,2),(P,-1,2),(P,2,1),(1000000007,1,3)]:
  assert prime_by_trial_division(prime);ff=Field(prime);t=tn*ff.inv(td)%prime;assert t and (1-pow(t,64,prime))%prime
  gs=makegreens(ps,t,ff)
  for i in range(64):
   for sig in (-1,1):
    a=[[(g[i][k]+sig*g[i][k+32])%prime for k in range(32)] for g in gs]
    assert a==evalframe(pos,i,sig,[t]*8,ff)
    if sig==-1:assert ff.rank(a)==8
  k=[[(gs[0][i][j]-gs[1][i][j])%prime for j in range(64)] for i in range(64)]
  assert ff.rank(k)==16 and all(any(r) for r in k)
  assert all(k[i^32][j]==(-k[i][j])%prime and k[i][j^32]==(-k[i][j])%prime for i in range(64) for j in range(64))
  m=[[(1 if i<32 else -1)*x%prime for x in r] for i,r in enumerate(k)]
  assert ff.rank(m)==16 and all(m[i^32][j]==m[i][j] for i in range(64) for j in range(64))
  assert ff.mul(m,m)==[[0]*64 for _ in range(64)]
  pd=[[0]*64 for _ in range(64)]
  for j in range(64):pd[ps[0][j]][j]+=1;pd[ps[1][j]][j]-=1
  rhs=ff.mul(ff.mul(gs[0],pd),gs[1]);assert k==[[t*x%prime for x in r] for r in rhs]
  controls.append({'prime':prime,'pole':[tn,td],'full_inverse_entries':32768,'all_projected_entries':32768,'difference_rank':16,'mixer_rank':16,'mixer_square_zero':True})
 # t=0 is operator-zero, not coefficient-injective: every G=I.
 # Full support pure-row criterion controls: a proper kernel can still be
 # trapped in a coordinate hyperplane, and the zero-pole full/projected
 # ranks coincide rather than supplying a false pure-character row.
 zero_full=[[int(k==0) for k in range(64)] for _ in range(8)]
 zero_proj=[[int(k==0) for k in range(32)] for _ in range(8)]
 assert f.rank(zero_full)==f.rank(zero_proj)==1
 out={'status':'ACCEPTED_SCOPED_POLE_AND_SPAN_THEOREMS','source_programs_executed':False,'method':'Reviewer Leibniz determinants over Z; exact polynomial divisions; good-prime modular coprimality certificates; direct matrix inverses','signed_schedule_count':256,'signed_plus_rank_counts':dict(counts),'finite_schedule_records':finite,'exact_integer_determinants':polycount,'universal_minus_gcd_guards':guards,'relative_permutation_cycle_counts':{'1':32,'2':16},'independent_matrix_controls':controls,'zero_pole_full_projected_rank':1,'scope':'Universal common legal pole operator no-go; coefficient injectivity requires nonzero pole; plus-kernel classification certified at t=1/2; finite unequal-sign schedules are separate.'}
 (BASE/'VERIFIED_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
 print('ALL INDEPENDENT CHECKS PASS',flush=True)
if __name__=='__main__':verify()
