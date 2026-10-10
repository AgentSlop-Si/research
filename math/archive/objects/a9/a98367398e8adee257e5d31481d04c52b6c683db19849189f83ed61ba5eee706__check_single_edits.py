#!/usr/bin/env python3
"""Independent exhaustive 504 single-Toffoli layout search, all parity inputs."""
from independent_checks import affine,mcnot,compose,BASE
from itertools import combinations
import json

def boundary_table(order):
 n=len(order);a=[0]*n
 for i in range(n-1):a[order[i]^order[i+1]]+=1
 step=1
 while step<n:
  for i in range(0,n,2*step):
   for j in range(i,i+step):x,y=a[j],a[j+step];a[j],a[j+step]=x+y,x-y
  step*=2
 return [(n-1-v)//2 for v in a]
def best(perms):
 n=len(perms[0]);order=list(range(n));caps=boundary_table(order)
 for p in perms:
  order=compose(order,p);ds=boundary_table(order);caps=[a+b for a,b in zip(caps,ds)]
 bestgap=-n;bestmask=None
 for mask in range(1,n):
  h=1<<mask.bit_length();d=n//h
  if d==1:rank=n//2
  else:
   counts=[0]*d
   for i,v in enumerate(order):
    if (v&mask).bit_count()%2:counts[i%d]+=1
   rank=sum(min(c,h//2) for c in counts)
  gap=rank-caps[mask]
  if gap>bestgap:bestgap,bestmask=gap,mask
 return bestgap,bestmask

if __name__=='__main__':
 source=json.loads((BASE/'sources/EXACT_CERTIFICATES.json').read_text())['nonaffine_256'];ps=[affine(c) for c in source['affine_shuffle_columns']]
 base=best(ps);assert base[0]==-39
 records=[]
 for j in range(3):
  for t in range(8):
   for controls in combinations([v for v in range(8) if v!=t],2):
    new=[p[:] for p in ps];new[j]=compose(new[j],mcnot(8,controls,t));gap,mask=best(new)
    records.append({'shuffle':j,'controls':controls,'target':t,'best_gap':gap,'witness_mask':mask})
 assert len(records)==504 and max(r['best_gap'] for r in records)==-10 and all(r['best_gap']<0 for r in records)
 out={'status':'PASS','baseline_best_gap':base[0],'number_of_single_Toffoli_layouts':504,'input_masks_each':255,'best_gap':-10,'records':records}
 (BASE/'SINGLE_EDIT_SEARCH.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n');print('PASS all 504 layouts and 128520 parity probes; best gap -10')
