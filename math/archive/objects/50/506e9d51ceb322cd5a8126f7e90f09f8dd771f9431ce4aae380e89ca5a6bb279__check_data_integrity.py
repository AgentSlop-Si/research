"""Self-authored data-only QA. Reads JSON/text bytes; never imports research code."""
import json, hashlib, pathlib, re
ROOT=pathlib.Path('[local workspace]')
BASE=ROOT/'research_finalization_0923'
checks=[]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def walk(v,src,loc=''):
 if isinstance(v,dict):
  path=v.get('path') or v.get('workspace_path')
  sha=v.get('sha256')
  if isinstance(path,str) and isinstance(sha,str) and re.fullmatch('[a-f0-9]{64}',sha):
   p=pathlib.Path(path)
   if not p.is_absolute():
    choices=[src.parent/p,BASE/p,ROOT/p]
    p=next((x for x in choices if x.is_file()),choices[0])
   actual=digest(p) if p.is_file() else None
   checks.append(dict(source=str(src.relative_to(ROOT)),locator=loc,path=str(p),expected=sha,actual=actual,ok=actual==sha))
  for k,x in v.items():walk(x,src,loc+'/'+str(k))
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(x,src,loc+'/'+str(i))
inputs=[BASE/'algorithms/STATUS.json',BASE/'algebra/final_v1/MANIFEST.json',BASE/'algebra/final_v1/findings.json',BASE/'matrix/matrix_finalization.json',BASE/'intake/verified-intake-manifest.json']
for p in inputs:walk(json.loads(p.read_text()),p)
p=BASE/'review/review_manifest.json'
for name,sha in json.loads(p.read_text()).items():
 target=p.parent/name; actual=digest(target) if target.is_file() else None
 checks.append(dict(source=str(p.relative_to(ROOT)),locator=name,path=str(target),expected=sha,actual=actual,ok=actual==sha))
p=BASE/'algebra/FINAL_RECEIPT.json'; d=json.loads(p.read_text())
for field,target in [('archive_sha256',pathlib.Path(d['archive'])),('manifest_sha256',pathlib.Path(d['directory'])/'MANIFEST.json'),('manuscript_sha256',pathlib.Path(d['directory'])/'FINAL_THEOREMS.md'),('findings_sha256',pathlib.Path(d['directory'])/'findings.json')]:
 actual=digest(target) if target.is_file() else None
 checks.append(dict(source=str(p.relative_to(ROOT)),locator=field,path=str(target),expected=d[field],actual=actual,ok=actual==d[field]))
old=json.loads((ROOT/'novelty_catalogue_0825/merged_catalogue.json').read_text())
fusion=json.loads((BASE/'fusions/fusion_candidates.json').read_text())
ids={}
for row in old['all_rows']:
 for key in [row['canonical_id']]+row.get('aliases',[])+row.get('census_family_ids',[]):ids.setdefault(key,[]).append(row['canonical_id'])
lineage=[]
for row in fusion['fusions']:
 for cid in row['sourceCandidateIds']:lineage.append(dict(fusion=row['id'],source=cid,matches=sorted(set(ids.get(cid,[])))))
oldrank={r['rank']:r['canonical_id'] for r in old['ranked_candidates']}
p12=json.loads((BASE/'fusions/prior12_novelty_crosswalk.json').read_text())['candidates']
p12_checks=[dict(rank=r['oldRank'],candidate=r['candidateId'],expected=oldrank.get(r['oldRank']),ok=r['candidateId']==oldrank.get(r['oldRank'])) for r in p12]
summary=dict(hash_check_count=len(checks),hash_unique_files=len(set(x['path'] for x in checks)),hash_failures=[x for x in checks if not x['ok']],unmapped_sources=[x for x in lineage if not x['matches']],fusion_count=len(fusion['fusions']),theorem_count=len(fusion['theoremChecks']),evidence_count=len(fusion['evidence']),prior12_count=len(p12),prior12_errors=[x for x in p12_checks if not x['ok']],screening_count=len(fusion['screeningLedger']))
result=dict(summary=summary,hash_checks=checks,source_lineage=lineage,prior12=p12_checks)
(BASE/'qa/data_integrity_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(summary,indent=2))
