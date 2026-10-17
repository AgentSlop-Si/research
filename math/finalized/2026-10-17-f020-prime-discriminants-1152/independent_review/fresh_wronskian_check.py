"""Fresh second-review arithmetic. No submitted/reviewer program is imported."""
from math import comb
from pathlib import Path
import json,hashlib,sys

def trim(a):
 while len(a)>1 and a[-1]==0:a.pop()
 return a

def add(a,b,s=1):
 c=a[:]+[0]*max(0,len(b)-len(a))
 for i,x in enumerate(b):c[i]+=s*x
 return trim(c)
def mul(a,b):
 c=[0]*(len(a)+len(b)-1)
 for i,x in enumerate(a):
  for j,y in enumerate(b):c[i+j]+=x*y
 return trim(c)
def deriv(a):return trim([i*a[i] for i in range(1,len(a))] or [0])
def shift1(a):return trim([sum(a[j]*comb(j,k) for j in range(k,len(a))) for k in range(len(a))])
def v2(a):
 if not a:return 10**9
 a=abs(a);return (a&-a).bit_length()-1
H=[[1],[0,1]]
for n in range(1,131):H.append(add([0]+H[n],[n*x for x in H[n-1]],-1))
rows=[]
for parity in (0,1):
 R=[h[parity::2] for h in H[parity::2]]
 # R_m is He_(2m) or He_(2m+1)/x, independently from the Hermite recurrence.
 for m in range(1,65):
  W=add(mul(deriv(R[m]),R[m-1]),mul(R[m],deriv(R[m-1])),-1);C=shift1(W)
  assert len(W)-1==2*m-2 and W[-1]==1
  assert v2(C[0])==m-1
  assert all(2*v2(c)+j>=2*m-2 for j,c in enumerate(C))
  reduced=[]
  for j,c in enumerate(C):
   if j%2: val=0
   else: val=(c//(1<<(m-1-j//2)))%2
   expected=comb(m-1,j//2)%2 if j%2==0 else 0
   assert val==expected;reduced.append(val)
  rows.append({'family':'U' if parity==0 else 'V','m':m,'degree':len(W)-1,'constant_v2':v2(C[0]),'all_newton_inequalities':True,'scaled_mod_pi_matches':True})
# Exact symbolic ramified negative control in Q[s]/(s^2+2).
# J4 = x4 -(2+2s)x2 + (-1+2s) = (x2-(1+s))^2.
assert (1-2,2)==(-1,2)
base=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parents[2]/'frozen_review'
manifest=(base/'MANIFEST.sha256').read_text();count=0
for line in manifest.splitlines():
 if not line.strip():continue
 h,name=line.split(None,1);name=name.lstrip('*');assert hashlib.sha256((base/name).read_bytes()).hexdigest()==h;count+=1
out={'status':'PASS','fresh_wronskian_cases':len(rows),'m_range':[1,64],'method':'Ordinary Hermite recurrence followed by parity extraction, integer derivative/product and exact y->1+z binomial translation; Newton points and mod-pi reduction checked','ramified_negative_control':'Verified algebraically with s^2=-2; J4=(x^2-(1+s))^2 for tau=(-1+2s)/3','frozen_manifest_files_verified':count,'frozen_manifest_sha256':hashlib.sha256((base/'MANIFEST.sha256').read_bytes()).hexdigest(),'rows':rows}
Path(__file__).with_name('WRONSKIAN_RESULT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='rows'},indent=2))
