#!/usr/bin/env python3
"""Separately authored check of saved exact certificates; standard library only."""
import argparse,itertools,json,time
from pathlib import Path
P,N,Q=53,13,16

def evaluate(coeff,x):return sum(c*pow(x,i,P) for i,c in enumerate(coeff))%P

def leibniz(a):
 n=len(a);s=0
 for perm in itertools.permutations(range(n)):
  term=1
  for i,j in enumerate(perm):term=term*a[i][j]%P
  if sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n))%2:term=-term
  s=(s+term)%P
 return s

def rank(a):
 a=[r[:] for r in a];i=0
 for j in range(len(a[0])):
  v=next((k for k in range(i,len(a)) if a[k][j]),None)
  if v is None:continue
  a[i],a[v]=a[v],a[i];iv=pow(a[i][j],-1,P)
  a[i]=[x*iv%P for x in a[i]]
  for k in range(i+1,len(a)):
   z=a[k][j];a[k]=[(x-z*y)%P for x,y in zip(a[k],a[i])]
  i+=1
  if i==len(a):break
 return i

def main():
 p=argparse.ArgumentParser();p.add_argument('directory');args=p.parse_args();d=Path(args.directory);start=time.monotonic();g=json.loads((d/'GATE.json').read_text());b=json.loads((d/'BASELINE.json').read_text())
 E=g['degree6_rows'];minors=g['degree6_augmented_maximal_minors'];bezout=g['minor_bezout'];s=[0]*100
 for m,c in zip(minors,bezout):
  for i,x in enumerate(m['coefficients_ascending']):
   for j,y in enumerate(c):s[i+j]=(s[i+j]+x*y)%P
 assert s[0]==1 and not any(s[1:])
 # Different determinant algorithm, at every base-field value.
 checks=0
 for m in minors:
  for y in range(P):
   a=[[evaluate(x,y) for x in E[i]] for i in m['row_indices']]
   assert leibniz(a)==evaluate(m['coefficients_ascending'],y);checks+=1
 enumerated=0;maxroots=0
 for c in g['census']:
  y=c['y'];M=[[evaluate(v,y) for v in r] for r in g['degree7_rows']];A=[r[:7] for r in M]
  assert rank(A)==6
  seen=set()
  for h in c['degree7_enumeration']:
   poly=h['polynomial_ascending'];assert len(poly)==8 and poly[-1]==1;seen.add(tuple(poly))
   assert all(sum(x*z for x,z in zip(row,poly))%P==0 for row in M)
   roots=[x for x in range(1,P) if evaluate(poly,x)==0]
   assert roots==h['distinct_nonzero_roots'] and len(roots)<7
   maxroots=max(maxroots,len(roots));enumerated+=1
  assert len(seen)==53
 assert enumerated==52*53
 # Verify supplied inverses against literal branches and reconstruct from raw weights.
 total=[[0]*N for _ in range(N)];branches=0;nonzero=0
 for raw,saved in zip(b['raw_certificate'],b['literal_banks']):
  e,ds,x,beta=raw['epsilon'],raw['delta_sign'],raw['alpha'],raw['beta'];assert beta==1 and raw['denominator']==(1-pow(x,N,P)-1)%P and raw['denominator']
  bank=[[0]*N for _ in range(N)]
  for j,R in enumerate(saved['inverses']):
   diag=[(1-pow(Q,e*ds*j+ds*t,P))%P for t in range(N)]
   # A R and R A using the exact two nonzero entries per original branch column/row.
   for r in range(N):
    for t in range(N):
     assert (diag[r]*R[r][t]-x*R[(r-e)%N][t])%P==int(r==t)
     assert (R[r][t]*diag[t]-x*R[r][(t+e)%N])%P==int(r==t)
     bank[r][t]=(bank[r][t]+raw['raw_weights'][j]*pow(N,-1,P)*R[r][t])%P
   branches+=1
  assert bank==saved['bank'];nonzero+=int(any(any(row) for row in bank))
  for r in range(N):
   for t in range(N):total[r][t]=(total[r][t]+bank[r][t])%P
 assert all(total[r][t]==pow(Q,-r*t,P) for r in range(N) for t in range(N));assert nonzero==24
 result={'bezout_identity_verified':True,'leibniz_determinants_checked':checks,'degree7_members_verified':enumerated,'maximum_distinct_nonzero_roots':maxroots,'literal_branches_verified':branches,'two_sided_inverse_identities':2*branches,'all_24_banks_nonzero':True,'target_entries_verified':N*N,'status':'PASS'}
 (d/'CERTIFICATE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');(d/'CHECK_TIMING.json').write_text(json.dumps({'elapsed_seconds':time.monotonic()-start},indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
