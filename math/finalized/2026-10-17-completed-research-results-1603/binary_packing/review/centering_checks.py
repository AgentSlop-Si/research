#!/usr/bin/env python3
"""Fresh independent checks for the exact centering scope qualification."""
from math import comb,lcm,prod
from pathlib import Path
import json

def bp(x,j):return comb(x,j) if x>=j>=0 else (0 if x>=0 else (-1)**j*comb(j-x-1,j))
def pp(r):
 E=lcm(*range(1,r+1));d=E//r;qs=[]
 for p in range(2,r+1):
  if all(p%t for t in range(2,int(p**.5)+1)):
   u=p
   while u*p<=r:u*=p
   q=1
   while d%(q*p)==0:q*=p
   if q>1:qs.append((q,(-pow(E//u,-1,q))%q))
 k=sum(v*(d//q)*pow(d//q,-1,q) for q,v in qs)%d if d>1 else 1
 return 1+k*E

def pack(row,w):
 z=0
 for t in reversed(row):z=(z<<w)+t
 return z
count=0
for r in range(3,17):
 P=pp(r);C=P-1;L=128
 for x in range(-r+1,2*r-1):
  singles=[(-1)**j*((P-1)//(j+1)//2)*bp(x,j) for j in range(r-1)]
  row=singles+[C]*(L-len(singles)-2)+[0,C]
  A=max(map(abs,row))
  for center in [0,C,-C,A,-A,(min(row)+max(row))//2]:
   rr=[z-center for z in row];B=max(map(abs,rr));w=8*(((2*L*B*B).bit_length()+7)//8)
   z=pack(rr,w)
   assert abs(z).bit_length()>=(L-2)*w
   count+=1
# A permitted original placement does not support the unqualified stronger claim.
r=16;P=pp(r);C=P-1;E=lcm(*range(1,r+1));beta=prod(1+C//j for j in range(1,r+1))//(E//r);s=beta.bit_length()-1;L=3*(1<<(r-1))//s;x=-1
N=(L-1)*s+C.bit_length();assert N.bit_length()-1==r and L>=r+1
singles=[(-1)**j*((P-1)//(j+1)//2)*bp(x,j) for j in range(r-1)]
row=[0]+singles+[C]*(L-r)
rr=[z-C for z in row];B=max(map(abs,rr));w=8*(((2*L*B*B).bit_length()+7)//8)
actual=abs(pack(rr,w)).bit_length();assert actual<r*w
result={'penultimate_zero_center_tests_passed':count,'without_placement_counterexample':{'rank':r,'actual_input_bits':N,'actual_input_rank':N.bit_length()-1,'blocks':L,'center':C,'slot_bits':w,'allocated_bits':L*w,'actual_centered_bits':actual},'accepted_scope':'Centering preserves row-height and slot-width lower bounds. Actual-length resistance additionally uses zero immediately before the final constant.'}
(Path(__file__).parent/'CENTERING_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
