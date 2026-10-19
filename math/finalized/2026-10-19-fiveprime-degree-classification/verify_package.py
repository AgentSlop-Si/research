"""Read-only portable verification of the public export, not private provenance."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent
EXPECTED_REPORT='ea1eafbcb45284d945feeb6a5b85f4958b4046c6b945526a26dbb483719ef172'
EXPECTED_CANDIDATE_MANIFEST='4c8007fa271fdbeecaa8d2f5e2516c003a7b05eefbe864264813b2885a3fa908'
EXPECTED_REVIEW_MANIFEST='8db99188bd6ae5f7d4cc416b532972ed2d5a25bce1ef87b7f7ffd803ca6ffccb'
EXPECTED_CHECKER='898ba533706aa6cc9cf63d3f68a8cd69c528f7ee6619f3cd47d281284a9aaab6'
EXPECTED_LABELS={'E','P','F','B','M','U','K'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p):return json.loads(p.read_text())
def verify(root=None):
 r=Path(root) if root is not None else ROOT
 assert not any(p.is_symlink() for p in r.rglob('*')), 'Symlinks are not allowed'
 m=js(r/'MANIFEST.json');seal=js(r/'SEAL.json')
 assert sha(r/'MANIFEST.json')==seal['manifest_sha256']
 items=m['files']; paths={e['path'] for e in items}
 assert len(paths)==len(items)
 actual={str(p.relative_to(r)) for p in r.rglob('*') if p.is_file()}
 assert actual==paths|{'MANIFEST.json','SEAL.json'},actual^(paths|{'MANIFEST.json','SEAL.json'})
 for e in items:
  p=r/e['path'];assert sha(p)==e['sha256'] and p.stat().st_size==e['bytes'],e['path']
 forbidden=[chr(47)+x+chr(47) for x in ('workspace','home','tmp')]+['docs.google.com'+'/spreadsheets','drive.'+'google.com']
 for p in r.rglob('*'):
  if p.is_file():
   s=p.read_text();assert not any(t in s for t in forbidden),str(p.relative_to(r))
 assert sha(r/'candidate/REPORT.md')==EXPECTED_REPORT
 assert sha(r/'candidate/MANIFEST.json')==EXPECTED_CANDIDATE_MANIFEST
 assert sha(r/'review/MANIFEST.json')==EXPECTED_REVIEW_MANIFEST
 assert sha(r/'review/independent_check.py')==EXPECTED_CHECKER
 L=js(r/'SOURCE_LEDGER.json'); entries=L['entries'];assert len(entries)==101
 keys={(e['namespace'],e['source_path']):e for e in entries};assert len(keys)==101
 counts={k:sum(e['mode']==k for e in entries) for k in ['exact','administrative_projection','omitted','deduplicated_alias']}
 assert counts==L['counts']=={'exact':35,'administrative_projection':9,'omitted':11,'deduplicated_alias':46}
 exported=set()
 for e in entries:
  mode=e['mode']
  if mode=='deduplicated_alias':
   ns,rel=e['alias_of'].split('/',1);target=keys[(ns,rel)];assert e['original']==target['original']
   assert e['export_path'] is None
  elif mode=='omitted':
   assert e['export_path'] is None and 'reason' in e
   assert not (r/e['namespace']/e['source_path']).exists()
  else:
   p=r/e['export_path'];assert e['export_path'] not in exported;exported.add(e['export_path'])
   assert sha(p)==e['exported']['sha256'] and p.stat().st_size==e['exported']['bytes']
   if mode=='exact':assert e['original']==e['exported']
   else:
    assert mode=='administrative_projection' and e['original']!=e['exported']
    assert e['projection']['scientific_text_values_checkers_and_controls_changed'] is False
    for op in e['projection']['operations']:
     assert op['operation'] in ('remove administrative local-location property','remove administrative absolute-directory prefix only')
 source_actual={str(p.relative_to(r)) for ns in ('candidate','review') for p in (r/ns).rglob('*') if p.is_file()}
 assert exported==source_actual
 # Every occurrence in both exact source manifests has a ledger disposition.
 for ns in ('candidate','review'):
  original=js(r/ns/'MANIFEST.json'); expected={e['path'] for e in original['files']}|{'MANIFEST.json','SEAL.sha256'}
  assert expected=={rel for (n,rel) in keys if n==ns}
 deps=js(r/'DEPENDENCIES.json');ds=deps['used_dependencies'];assert {d['label'] for d in ds}==EXPECTED_LABELS
 receipts=js(r/'IMMUTABLE_DEPENDENCY_LINKS.json')['sources'];assert {d['label'] for d in receipts}==EXPECTED_LABELS
 for d in ds:
  label=d['label'];assert sha(r/d['report'])==d['original_report_sha256']
  assert sha(r/'candidate/sources'/f'{label}_candidate_MANIFEST.json')==d['original_manifest_sha256']
  assert d['original_manifest_sha256'] in (r/d['review']).read_text()
  v=r/d['verdict'] if d['verdict'] else None
  if v:
   val=js(v);assert val.get('verdict',val.get('status'))=='PASS'
   assert val['candidate_report_sha256']==d['original_report_sha256'] and val['candidate_manifest_sha256']==d['original_manifest_sha256']
  else:assert label=='E' and 'ACCEPT all four' in (r/d['review']).read_text()
  receipt=next(x for x in receipts if x['label']==label)
  assert receipt['immutable_report_url']==d['immutable_report_url'] and receipt['report_sha256']==d['original_report_sha256']
  assert '/blob/'+receipt['commit']+'/' in receipt['immutable_report_url'] and len(receipt['commit'])==40
 verdict=js(r/'review/VERDICT.json');assert verdict['verdict']=='PASS' and verdict['proof_repairs_required']==[]
 assert verdict['candidate_report_sha256']==EXPECTED_REPORT and verdict['candidate_manifest_sha256']==EXPECTED_CANDIDATE_MANIFEST
 acceptance=js(r/'FINAL_ACCEPTANCE.json');assert acceptance['verdict']=='PASS' and acceptance['candidate_report_sha256']==EXPECTED_REPORT
 scope=js(r/'CLAIM_SCOPE.json');assert scope['complete_degree_classification_N5q'] is True
 for k in ['complete_support_classification','arbitrary_semiprime_classification','exact_nonsharp_optima','sharp_gap_rate','FFT_improvement_claim']:assert scope[k] is False
 assert scope['sharp_inverse_row_budgets']==['5q-1','5q-5','4q'] and scope['strict_infimum_separation_elsewhere'] is True
 owner=js(r/'OWNER_DISPOSITIONS.json');assert owner['owner']=='M-SPARSE-DEFECT' and owner['status']=='TO RESEARCH' and owner['priority']==42
 assert owner['native_state_changed'] is False and owner['score_change'] is False and owner['full_owner_closure'] is False
 assert '(d/N)I' in (r/'THEOREM.md').read_text() and 'd in {0, 1, 5, q, 5q}' in (r/'THEOREM.md').read_text()
 assert js(r/'OMISSIONS.json')['complete_logical_dependencies_available'] is True
 return {'verdict':'PASS','public_files':len(actual),'manifest_files':len(items),'manifest_sha256':sha(r/'MANIFEST.json'),'source_occurrences':len(entries),'source_counts':counts,'seven_logical_dependencies_verified':True,'scientific_originals_and_admin_mapping_verified':True,'privacy_scan':'PASS','original_private_provenance_replayed':False,'historical_checker_archives_bundled_or_rerun':False,'owner_full_closure':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2,sort_keys=True))
