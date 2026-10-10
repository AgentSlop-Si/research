"""Byte-preserving integration. Read predecessor data, never execute predecessor programs."""
from pathlib import Path
from collections import Counter
import json,hashlib,shutil
H=lambda b:hashlib.sha256(b).hexdigest()
base=Path('coverage_audit_20261010');here=Path(__file__).resolve().parent
names=['review_constructor_baseline_rows0_39']+['review_bank_baseline_batch'+str(i) for i in range(1,6)]
expected=['c851acbe7f4af98fa36cd544bfe0ec7a296190d24148bb17ebfe2098377ce876','89ba24c6f85c558c7dfad78d2ed91c47b426348dee10fd1ed3163432032ae6d8','47fbed3b927a806f8ecfa516b9a9f176ad01021b1e50ac5b809be017354b3184','1986d23b0e3a5bae38ca939695049976edcfc4ca5716296e0b962123c6a35786','ea0a1e9ef84e89a654436d2bf3cc2960b44a41070e0d0d743dad7c5dfa1100e6','58294665d5c9c17a99a117b2c0b7af48c5301ba4b969bdd9366ddac4e7d099ad']
queue=json.loads((base/'BASELINE_TEXT_REVIEW_QUEUE_1.json').read_text())
shutil.copy2(base/'BASELINE_TEXT_REVIEW_QUEUE_1.json',here/'SOURCE_QUEUE.json')
rows=[];packs=[]
for name,sha in zip(names,expected):
 p=base/name;assert H((p/'SEALED_MANIFEST.json').read_bytes())==sha
 dst=here/'packages'/name
 if dst.exists():raise RuntimeError('Refuse to overwrite '+str(dst))
 shutil.copytree(p,dst,ignore=shutil.ignore_patterns('__pycache__'))
 m=json.loads((dst/'SEALED_MANIFEST.json').read_text())['files'];mf=m.items() if isinstance(m,dict) else ((r['path'],r['sha256']) for r in m)
 count=0
 for fn,hs in mf:assert H((dst/fn).read_bytes())==hs;count+=1
 cov=json.loads((dst/'COVERAGE.json').read_text())
 for r in cov['rows']:
  assert r['inspection']=='complete_text_read'
  q=queue['sources'][r['queue_index']]
  assert r['sha256']==q['sha256'] and r['canonical_path']==q['canonical_path']
  b=(dst/r['local_inert_snapshot']).read_bytes();assert len(b)==r['size_bytes'] and H(b)==r['sha256']
  rr=dict(r);rr['review_package']='packages/'+name;rr['review_manifest_sha256']=sha
  rr['scope_note']='Preserve the complete per-source acceptance and dependency wording. Full text inspection is not blanket theorem or code approval.'
  rows.append(rr)
 packs.append({'path':'packages/'+name,'original_path':str(p),'manifest_sha256':sha,'verified_manifest_members':count,'rows':sorted(r['queue_index'] for r in cov['rows']),'source_bytes':sum(r['size_bytes'] for r in cov['rows'])})
rows.sort(key=lambda r:r['queue_index'])
assert [r['queue_index'] for r in rows]==list(range(200));assert len(set(r['sha256'] for r in rows))==200;assert sum(r['size_bytes'] for r in rows)==1230558
out={'scope':'Frozen baseline queue1 only: full text inspection with per-claim scopes, independent controls and historical execution claims kept distinct.','source_queue_sha256':H((here/'SOURCE_QUEUE.json').read_bytes()),'completed_rows':200,'unique_source_hashes':200,'completed_source_bytes':1230558,'missing_rows':[],'overlap_rows':[],'source_programs_executed':0,'universal_FFT_improvement_accepted':False,'package_count':len(packs),'packages':packs,'classification_counts':dict(sorted(Counter(r['classification'] for r in rows).items())),'rows':rows}
(here/'COVERAGE.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
cp=Path('recovered_companion_review_0217');cs='dc1c7a8b1d2c9fcadb51c544c197e7b5a7eb3ba3ffa5c985d4ed6d2aeb68ba92'
assert H((cp/'SEALED_MANIFEST.json').read_bytes())==cs
cm=json.loads((cp/'SEALED_MANIFEST.json').read_text())['files']
for f,sha in cm.items():assert H((cp/f).read_bytes())==sha
cd=here/'companion_status';cd.mkdir()
for f in ['REVIEW.md','PROJECTIVE_REVIEW.md','OUTER_INVERSE_REVIEW.md','TENSOR_COMPANION_REVIEW.md','SOURCE_COVERAGE.json','PROVENANCE.json','SEALED_MANIFEST.json']:shutil.copy2(cp/f,cd/f)
status={'original_package':str(cp),'manifest_sha256':cs,'verified_members':len(cm),'copied_reports_only':True,'full_replay_remains_in_original_package':True,'queue1_row_count_contribution':0,'scope':'Projective fixed-stage and pinned-N256 outer proof accepted; missing tensor v24 full source remains pending.'}
(here/'COMPANION_STATUS.json').write_text(json.dumps(status,indent=2)+'\n')
print(json.dumps({'rows':200,'bytes':1230558,'packages':len(packs),'verified_members':sum(p['verified_manifest_members'] for p in packs),'companion_members_verified':len(cm)},indent=2))
