"""Fresh 320-bit all-coefficient/all-row independent retained-target check."""
from fractions import Fraction
from pathlib import Path
import json,time
import reviewer_oracle as o
HERE=Path(__file__).resolve().parent
CANDIDATE=Path(__file__).resolve().parent.parent/'candidate'
def scale(x,a):
 z=[v*a for v in x];return min(z),max(z)
def add(x,y):return x[0]+y[0],x[1]+y[1]
def sub(x,y):return x[0]-y[1],x[1]-y[0]
def main():
 start=time.monotonic();d=json.loads((CANDIDATE/'OUTPUT.json').read_text());old=json.loads((CANDIDATE/'RETAINED_TARGET_CHECKS.json').read_text())
 source=d['source'];out=d['output'];m=source['m'];N=source['N'];M=4*N;P=d['estimates']['bits'];s=5*m;h=16*s+1;grid=o.Q+P
 rows=[];calls=0;contained=0;maximum=Fraction(0)
 for ell,pair in enumerate(out['pairs']):
  stencil={(4*ell+j)%M for j in range(-h,h+2)}
  re=im=(0,0);l1=0;count=0
  for k,(a,b) in d['estimates']['pairs']:
   if k not in stencil:continue
   c,e=o.coefficient(N,M,5,ell,k);calls+=1;count+=1
   re=add(re,sub(scale(c,a),scale(e,b)));im=add(im,add(scale(c,b),scale(e,a)));l1+=abs(a)+abs(b)
  lifted=[v << (grid-source['scale']) for v in pair]
  radii=[max(abs(v-lo),abs(v-hi)) for v,(lo,hi) in zip(lifted,(re,im))]
  squared=sum(r*r for r in radii);allowed=(l1 << (o.Q-8*m))+(1 << (grid-out['normalized_bits']))
  assert squared<=allowed*allowed
  for new,prev in zip((re,im),(old['rows'][ell]['real_interval'],old['rows'][ell]['imag_interval'])):
   assert prev[0]<<(o.Q-256)<=new[0]<=new[1]<=prev[1]<<(o.Q-256)
   contained+=1
  maximum=max(maximum,Fraction(squared,allowed*allowed))
  rows.append({'ell':ell,'terms':count,'real_interval':re,'imag_interval':im,'squared_endpoint_error':squared,'squared_allowed_error':allowed*allowed})
 assert calls==5733 and len(rows)==512 and contained==1024
 answer={'status':'PASS','oracle_grid_bits':o.Q,'target_grid_bits':grid,'fresh_coefficient_calls':calls,'all_output_rows_checked':len(rows),'independent_coordinate_intervals_contained_in_author_intervals':contained,'max_squared_error_to_allowed_squared_ratio':{'numerator':maximum.numerator,'denominator':maximum.denominator},'seconds':time.monotonic()-start,'candidate_modules_imported':False,'production_numeric_helpers_called':False,'rows':rows}
 (HERE/'INDEPENDENT_RETAINED_INTERVALS.json').write_text(json.dumps(answer,indent=2)+'\n')
 print(json.dumps({k:v for k,v in answer.items() if k!='rows'},indent=2))
if __name__=='__main__':main()
