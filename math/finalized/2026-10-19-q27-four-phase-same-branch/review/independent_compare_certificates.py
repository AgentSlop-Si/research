import json,itertools,hashlib
from pathlib import Path
D=Path(__file__).resolve().parent
labels=[(s,b,list(e)) for s in range(2) for b in [1,2] for e in itertools.combinations(range(8*b,8*b+8),4)]
vecs=[v for v in itertools.product(range(4),repeat=4) if max(v)-min(v)<=2 and sum(abs(v[j]-v[(j+1)%4]) for j in range(4))<=4]
cols=[sum(v[j]*4**(3-j) for j in range(4)) for v in vecs];assert len(cols)==126
names=['COVERAGE_PRIMARY.jsonl','COVERAGE_CONJUGATE.jsonl'];roots=[569522298,430477711]
rows=[[json.loads(x) for x in (D/'input'/n).read_text().splitlines()] for n in names]
ours=[list(map(int,x.split())) for x in (D/'INDEPENDENT_MINORS.txt').read_text().splitlines()]
assert all(len(r)==280 for r in rows) and len(ours)==560
out=[]
for i,(s,b,edges) in enumerate(labels):
 for j,root in enumerate(roots):
  a=rows[j][i];o=ours[2*i+j]
  assert a['label']==i and a['stage']==s and a['branch']==b and a['edges']==edges
  assert a['encoded']==[24*s+e for e in edges]
  assert a['prime']==1000000009 and a['i_image']==root and a['rank']==126
  assert len(a['windows'])==len(set(a['windows']))==126 and all(0<=v<784 for v in a['windows'])
  assert a['columns']==cols
  assert 0<a['determinant']<a['prime']
  assert o[:8]==[s,b,*edges,j,126] and a['windows']==o[8:-1] and a['determinant']==o[-1]
  out.append(' '.join(map(str,[s,b,*edges,j,126,*a['windows'],a['determinant']])))
(D/'AUTHOR_FIXED_MINORS.txt').write_text('\n'.join(out)+'\n')
result={'status':'PASS','labels':280,'independent_exact_matching_minors':560,'prime':1000000009,'embeddings':roots,'fixed_column_count':126,'source_hashes':{n:hashlib.sha256((D/'input'/n).read_bytes()).hexdigest() for n in names},'fixed_input_sha256':hashlib.sha256((D/'AUTHOR_FIXED_MINORS.txt').read_bytes()).hexdigest()}
(D/'CERTIFICATE_COMPARISON.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
