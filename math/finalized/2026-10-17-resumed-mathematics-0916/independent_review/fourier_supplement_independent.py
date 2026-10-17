"""Fresh rational inversion check for the separate low-rank restriction."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
n=8;A=[[F(3 if i==j else 1 if i>j else 2) for j in range(n)] for i in range(n)]
z=[r[:]+[F(i==j) for j in range(n)] for i,r in enumerate(A)]
for k in range(n):
 v=z[k][k];assert v;z[k]=[x/v for x in z[k]]
 for i in range(n):
  if i!=k:
   v=z[i][k];z[i]=[x-v*y for x,y in zip(z[i],z[k])]
C=[row[n:] for row in z]
H=[[F(255 if i==j else -2**(8-(j-i)) if i<j else -2**(i-j-1),511) for j in range(n)] for i in range(n)]
assert C==H
for X,Y in ((A,C),(C,A)):
 for i in range(n):
  for j in range(n):assert sum(X[i][k]*Y[k][j] for k in range(n))==int(i==j)
det=C[0][1]*C[2][3]-C[0][3]*C[2][1];assert C[0][2]==F(-64,511) and det==F(32,511)
import sys
B=Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).parent.parent/'reports'/'fourier_target'
m=json.loads((B/'SUPPLEMENT_V1_MANIFEST.json').read_text())
assert all(hashlib.sha256((B/f['path']).read_bytes()).hexdigest()==f['sha256'] for f in m['files'])
out={'status':'PASS','two_sided_inverse_entries':128,'far_entry':[-64,511],'disjoint_minor':[32,511],'supplement_sha256':hashlib.sha256((B/'SUPPLEMENT_V1.md').read_bytes()).hexdigest(),'supplement_manifest_sha256':hashlib.sha256((B/'SUPPLEMENT_V1_MANIFEST.json').read_bytes()).hexdigest(),'proof_review':'Invertibility injects ker(D) through R, so at most r zero diagonal entries; consecutive Fourier-row Vandermonde rank>=m-r minus rank<=r perturbation gives m-2r. For m=2r+2 and N>=4r+4 contradict rank-one lower block. Transpose and diagonal rescaling preserve hypotheses. General chart remains open.'}
Path(__file__).with_name('FOURIER_SUPPLEMENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
