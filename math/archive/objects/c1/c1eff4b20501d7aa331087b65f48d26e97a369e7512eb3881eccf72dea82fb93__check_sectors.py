#!/usr/bin/env python3
"""Independently regenerate fixed rational-sector certificates modulo good primes."""
from pathlib import Path
import json
from exact_utils import Field,prime_by_trial_division
from geometry import routes
BASE=Path(__file__).parent

def greens_mod(prime):
 f=Field(prime);ps=routes();out=[];guards=[]
 assert prime_by_trial_division(prime)
 for j,p in enumerate(ps):
  d=j+2;den=(pow(d,64,prime)-1)%prime;assert d%prime and den
  a=f.eye(64);tau=f.inv(d)
  for col,row in enumerate(p):a[row][col]=(a[row][col]-tau)%prime
  g=f.inverse(a);assert f.mul(a,g)==f.eye(64)
  assert all(p[i^32]==(p[i]^32) for i in range(64))
  for i in range(64):
   v=i
   for _ in range(32):v=p[v]
   assert v==i^32
  out.append(g);guards.append({'d':d,'d64_minus_1_mod_p':den})
 return out,guards

def frame(gs,i,sign,p):return [[(g[i][k]+sign*g[i][k+32])%p for k in range(32)] for g in gs]

def verify():
 src=json.loads((BASE/'sources/SECTOR_FRAME_CERTIFICATE.json').read_text());assert routes()==src['nested_cycle_successors']
 assert {(r['row'],r['sector_sign']) for r in src['projected_frame_minor_records']}=={(i,s) for i in range(32) for s in (1,-1)}
 records=[]
 for prime in (998244353,1000000007):
  f=Field(prime);gs,guards=greens_mod(prime);mins=[]
  if prime==src['prime']:assert guards==src['fixed_rational_inverse_guards']
  for saved in src['projected_frame_minor_records']:
   i,sign,cols=saved['row'],saved['sector_sign'],saved['columns'];v=frame(gs,i,sign,prime)
   m=[[r[c] for c in cols] for r in v];det=f.det(m);assert det and f.rank(v)==8
   if prime==src['prime']:assert det==saved['determinant_mod_p']
   partner=frame(gs,i+32,sign,prime);assert partner==[[sign*x%prime for x in r] for r in v]
   mins.append({'row':i,'sign':sign,'columns':cols,'determinant':det})
  directs=[]
  for saved in src['four_row_direct_sum_certificates']:
   sign=saved['sector_sign'];selected=saved['rows'];assert all((-1)**i==-sign for i in selected)
   stack=[r for i in selected for r in frame(gs,i,sign,prime)];det=f.det(stack);assert det
   if prime==src['prime']:assert det==saved['determinant_mod_p'] and stack==saved['stacked_minor_mod_p']
   directs.append({'sign':sign,'rows':selected,'determinant':det})
  if prime==src['prime']:
   for saved in src['minimal_row_zero_certificate']:
    v=frame(gs,0,saved['sector_sign'],prime);m=[[r[c] for c in saved['columns']] for r in v]
    assert m==saved['minor_mod_p'] and f.det(m)==saved['determinant_mod_p']
  records.append({'prime':prime,'all_inverse_entries':32768,'projected_minors':mins,'direct_sum_minors':directs})
  print('Sector minors PASS over',prime,flush=True)
 out={'status':'ACCEPTED_FIXED_POLE_SIGNED_PREFIX_OBSTRUCTION','field_controls':records,'rational_source_minors_match_exactly':True,'scope':'N64 fixed routes and poles 1/2 through 1/9; signed inner prefixes excluded; genuinely mixing families remain open'}
 (BASE/'SECTOR_RESULTS.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
if __name__=='__main__':verify()
