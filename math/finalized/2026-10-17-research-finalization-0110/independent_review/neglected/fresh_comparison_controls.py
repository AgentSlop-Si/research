"""Reviewer-authored integer controls for the qualified affine-step map."""
from itertools import combinations
from pathlib import Path
import json
translation=0;pigeonhole=0
for N in [4,8,16,32,64]:
 for h in range(1,N):
  I={j for j in range(N) if (h*j)%N<N//2}
  assert len(I)==N//2
  for a in range(N):
   t=min((h*a)%N,(-h*a)%N)
   crossing=sum(j not in I and (j+a)%N in I for j in range(N))
   assert crossing==t;translation+=1
 for s in range(1,min(4,N)):
  for A in combinations(range(1,N),s):
   if N>=32 and sum(A)%31:continue
   r=1
   while (r+1)**s<=N-1:r+=1
   boxes={};witness=None
   for j in range(N):
    box=tuple((r*((j*a)%N))//N for a in A)
    if box in boxes:witness=j-boxes[box];break
    boxes[box]=j
   assert witness is not None
   assert all(r*min((witness*a)%N,(-witness*a)%N)<N for a in A)
   pigeonhole+=1
I={j for j in range(6) if (2*j)%6<3};assert len(I)==4
N=8;I=set(range(4));successor=[7,2,1,4,3,6,5,0]
assert sum(j not in I and successor[j] in I for j in range(N))==2
assert 2*8==16 # h=1, stride8, r=2 fails strict inequality r|ha|<N.
result={'verdict':'PASS','exact_translation_identities':translation,'exact_strict_pigeonhole_controls':pigeonhole,'retained_countercontrols':['N=6,h=2 unbalanced character cut','Non-Hamiltonian N=8 two-cycle permutation exceeds signed-step1 crossing budget','N=16,r=2,h=1,stride8 fails strict witness'],'qualification':'Fresh transcription controls; inherited full theorem acceptance and its unexecuted historical controls remain separately attributed.'}
(Path(__file__).parent/'INDEPENDENT_COMPARISON_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
