"""Fresh secondary Python reconstruction of representative stored C++ minors."""
import sys,json,itertools,time
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));import pilot as p
records=[json.loads(x)for x in (ROOT/'COVERAGE_PRIMARY.jsonl').read_text().splitlines()]
chosen=[]
for family in sorted({r['family']for r in records}):
 rr=[r for r in records if r['family']==family]
 chosen.extend([rr[0],rr[-1]])
def det(A):
 A=[r[:]for r in A];result=1
 for k in range(len(A)):
  i=next((i for i in range(k,len(A))if A[i][k]),None)
  if i is None:return 0
  if i!=k:A[i],A[k]=A[k],A[i];result=-result
  v=A[k][k];result=result*v%p.p;inv=pow(v,-1,p.p)
  for i in range(k+1,len(A)):
   v=A[i][k]*inv%p.p
   for j in range(k,len(A)):A[i][j]=(A[i][j]-v*A[k][j])%p.p
 return result%p.p
out=[]
for record in chosen:
 label=[(x//24,x%24)for x in record['label']];Q,F,g=p.system(label,True)
 cols=[(c//16,(c//4)%4,c%4)for c in record['columns']]
 A=[[Q[w].get(c,0)for c in cols]for w in record['windows']]
 d=det(A);assert d==record['determinant'];bad=[row[:]for row in A];bad[-1]=bad[0][:];assert det(bad)==0
 # The same fixed minor is independently reconstructed in the opposite embedding.
 p.imag=p.p-p.imag
 Q2,F2,g2=p.system(label,True);A2=[[Q2[w].get(c,0)for c in cols]for w in record['windows']]
 d2=det(A2);assert d2
 p.imag=p.p-p.imag
 result={'label':record['label'],'family':record['family'],'determinant':d,'same_minor_conjugate_determinant':d2,'duplicate_row_determinant':0};out.append(result);print(json.dumps(result),flush=True)
(ROOT/'MINOR_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
