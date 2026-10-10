"""Cross-check native certificate rows using own separate Python polynomial arithmetic."""
from pathlib import Path
from fractions import Fraction
import json,csv,hashlib
from fresh_reconstruct import macaulay,rankdet
R=Path(__file__).resolve().parent
records=[]
for file in sorted(R.glob('witness_N*_p*.csv')):
 inst=json.loads((R/file.name.replace('witness_','fresh_').replace('.csv','.json')).read_text());p=inst['p'];n=inst['n']
 selected=[];rows=list(csv.DictReader(file.open()))
 assert len({int(x['mapping']) for x in rows})==len(rows)
 if n==4:selected=rows
 else:selected=[rows[k*(len(rows)-1)//63] for k in range(64)]
 for x in selected:
  rs=[int(x['r0']),int(x['r1'])];cs=[int(x[f'c{k}']) for k in range(4)]
  for degree,label in [(3,'cubic'),(4,'quartic')]:
   M=macaulay(inst,rs,cs,degree);mask=int(x[label+'_row_mask']);K=[r for k,r in enumerate(M) if mask>>k&1]
   assert len(K)==len(K[0]);rank,ids,det=rankdet(K,p);sgn=(-1)**sum(ids[i]>ids[j] for i in range(len(ids)) for j in range(i+1,len(ids)));det=det*sgn%p
   assert rank==len(K) and det==int(x[label+'_det']) and det!=0
 records.append(dict(file=file.name,total_csv_rows=len(rows),python_checked_mappings=len(selected),python_checked_minors=2*len(selected),sha256=hashlib.sha256(file.read_bytes()).hexdigest(),all_checked_minors_match=True))
# Dense invertible local-window match can still fail global diagonal equivalence.
p=998244353;n=8;w=pow(3,(p-1)//n,p);F=[[pow(w,i*j,p) for j in range(n)] for i in range(n)];B=[row[:] for row in F];B[7][7]=2*B[7][7]%p
from fresh_reconstruct import inverse
_,df=inverse(F,p);_,db=inverse(B,p);assert db==df*(n+1)*pow(n,-1,p)%p
assert all(F[i][j]==B[i][j] for i in (0,1) for j in range(5))
minor=(pow(2,-1,p)-1)%p;assert minor
out=dict(records=records,counterexample=dict(N=n,prime=p,local_window_equal=True,modified_entry=[7,7],target_det=df,middle_det=db,global_quotient_minor=minor,diagonal_equivalence=False),caveat='Separate fresh implementations, same audit author; external independent review remains separate.')
(R/'fresh_crosscheck_results.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'native_csv_rows':sum(x['total_csv_rows'] for x in records),'python_rechecked_minors':sum(x['python_checked_minors'] for x in records),'all_match':True}))
