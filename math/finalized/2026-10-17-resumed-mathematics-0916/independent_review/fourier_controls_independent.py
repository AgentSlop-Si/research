"""Fresh exact controls; imports own current-cycle quotient helpers only."""
from fractions import Fraction as R
from pathlib import Path
from itertools import combinations
import json,hashlib
import fourier_independent as I
D=(-12,12,28,28);invD=(R(-5,8),R(1,4),R(1,4),R(-5,8))
assert I.mul(D,invD)==I.O
norm=I.O
for k in (1,3,5,7):
 val=I.Z
 for j,c in enumerate(D):val=I.add(val,tuple(c*x for x in I.power(I.zeta,j*k%8)))
 norm=I.mul(norm,val)
assert norm==(2048,0,0,0)
controls=0
for centers in combinations(range(8),4):
 rows=[]
 for k in centers:
  coeff=[I.O]
  for s in ((k-1)%8,k,(k+1)%8):
   root=I.power(I.zeta,s);new=[I.Z]*(len(coeff)+1)
   for j,c in enumerate(coeff):new[j]=I.add(new[j],I.neg(I.mul(c,root)));new[j+1]=I.add(new[j+1],c)
   coeff=new
  rows.append(coeff)
 assert I.det(rows)!=I.Z;controls+=1
n=8;C=[[R(2 if i==j else -1 if abs(i-j)==1 else 0) for j in range(n)] for i in range(n)]
A=[[R((min(i,j)+1)*(n-max(i,j)),n+1) for j in range(n)] for i in range(n)]
J=[[R(2 if i==j else 1) for j in range(n)] for i in range(n)];JI=[[R(i==j)-R(1,9) for j in range(n)] for i in range(n)]
for X,Y in ((C,A),(A,C),(J,JI),(JI,J)):
 for i in range(n):
  for j in range(n):assert sum(X[i][k]*Y[k][j] for k in range(n))==int(i==j)
assert JI[0][2]==R(-1,9)
import sys
B=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent.parent/'reports'/'fourier_target'
m=json.loads((B/'MANIFEST.json').read_text())
assert all(hashlib.sha256((B/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in m['files'])
out={'status':'PASS','reciprocal_certificate':True,'field_norm':2048,'four_support_subsets_nonzero':controls,'two_sided_example_inverse_entries':256,'report_sha256':hashlib.sha256((B/'REPORT.md').read_bytes()).hexdigest(),'manifest_sha256':hashlib.sha256((B/'MANIFEST.json').read_bytes()).hexdigest(),'diagonal_scaling_scope':'Validated analytically: D_L F D_R=B P A implies F=(D_L^-1 B)P(A D_R^-1); right inverse D_R A^-1 and left inverse B^-1 D_L preserve cyclic-tridiagonal support.'}
Path(__file__).with_name('FOURIER_CONTROLS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
