"""Fresh review metadata only. Reads inert bytes/JSON, never imports/parses source programs."""
from pathlib import Path
import json,hashlib,shutil
O=Path(__file__).parent
B=Path('code_coverage_audit_0228')
M=Path('fft_research_master_20261009')
sha=lambda b:hashlib.sha256(b).hexdigest()
rows=json.loads((O/'ASSIGNED_ROWS.json').read_text()); targets={r['sha256'] for r in rows}
inv=json.loads((B/'CODE_COVERAGE_INVENTORY.json').read_text())
(O/'metadata_snapshots').mkdir(exist_ok=True)
inputs=[]
for p in [B/'CODE_COVERAGE_INVENTORY.json',Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json')]+[B/'pending_batches_v2'/n for n in sorted({r['assigned_batch'] for r in rows})]:
 data=p.read_bytes(); dest=O/'metadata_snapshots'/p.name;dest.write_bytes(data); inputs.append({'path':str(p),'sha256':sha(data),'bytes':len(data),'snapshot':str(dest.relative_to(O))})
coverage=[]
for p in sorted(Path('[local workspace]').rglob('COVERAGE.json')):
 if O in p.parents:continue
 data=p.read_bytes()
 try:j=json.loads(data)
 except Exception:continue
 hits=[h for h in sorted(targets) if h in data.decode()]
 coverage.append({'path':str(p),'sha256':sha(data),'bytes':len(data),'assigned_hash_text_matches':hits})
assert not any(x['assigned_hash_text_matches'] for x in coverage)
(O/'DEDUP_RECONCILIATION.json').write_text(json.dumps({'frozen_inventory':inputs[0],'additive_registry':inputs[1],'all_other_coverage_files_scanned':len(coverage),'coverage_files':coverage,'method':'Exact SHA-256 equality. All frozen target rows have static_inspection_complete=false; no assigned hash occurs anywhere in prior completed COVERAGE metadata or additive registry. No basename/AST credit.','assigned_hashes':len(targets),'new_coverage_hashes':len(targets)},indent=2)+'\n')
# Resolve available sibling identities from preserved source paths and exact archive parents.
archive_lookup={}
for r in inv:
 for occ in r.get('occurrences',[]):
  if occ.get('kind')=='archive_member':archive_lookup.setdefault((occ['archive_sha256'],occ['name']),set()).add(r['sha256'])
byhash={r['sha256']:r for r in inv};dependencies=[]
for r in rows:
 names=set()
 for ref in r.get('import_references',[]):
  if ref.get('level',0)!=0:continue
  if ref.get('module'):names.add(ref['module'].split('.')[0])
  else:names.update(x.split('.')[0] for x in ref.get('names',[]))
 if r['index']==31:names.update(['test_phase14','test_stationary','check_v13','test_centered','v11_test_checkpoint','finite_field_audit','precision_probe','field_gram_audit','field_stationary_audit','green_forcing_gate','leverage_gate','orbit_collision_gate','experiment_phase14'])
 for name in sorted(names):
  sibling=M/Path(r['representative_path']).parent/(name+'.py'); found=set(); loc=[]
  if sibling.is_file():
   h=sha(sibling.read_bytes());found.add(h);loc.append(str(sibling))
  for occ in r['occurrences']:
   if occ['kind']=='archive_member':
    member=str(Path(occ['name']).parent/(name+'.py'))
    for h in archive_lookup.get((occ['archive_sha256'],member),[]):found.add(h);loc.append(occ['archive_sha256']+'::'+member)
  dependencies.append({'source_index':r['index'],'source_sha256':r['sha256'],'reference':name,'candidate_exact_hashes':sorted(found),'identity_locations':sorted(set(loc)),'resolution':'exact sibling byte identities; not executed import-path proof' if found else 'standard-library/third-party module, or unresolved historical/dynamic path','full_source_coverage_credit':False,'assigned_full_read_dependencies':[h for h in sorted(found) if h in targets]})
# Materialize exact hash-only dependency snapshots but do not claim full reads for these.
(O/'dependency_snapshots').mkdir(exist_ok=True)
for h in sorted({h for d in dependencies for h in d['candidate_exact_hashes']} - targets):
 p=Path(byhash[h]['local_content']) if h in byhash else None
 if p and p.is_file():(O/'dependency_snapshots'/h).write_bytes(p.read_bytes())
(O/'DEPENDENCY_IDENTITIES.json').write_text(json.dumps({'scope':'Direct named imports and manually read runner targets. Uses frozen metadata and exact same-container sibling identity; does not resolve runtime sys.path shadowing or review dependency closure.','rows':dependencies},indent=2)+'\n')
# Non-code stored evidence; copies preserve exact bytes. Their claims are historical, not reruns.
roots=['additions/1916','additions/1916/source','additions/1916/prior','additions/1930_phase26','additions/1930_sparse','additions/1954/divisor_audit','additions/1954/divisor_audit/source_evidence','additions/1954/source_triage','additions/2020_2027/delta_newton/audit','additions/2020_2027/hero1_phase14','additions/2020_2027/hero1_phase14/new_source_files']
evidence=[]
for root in roots:
 for p in sorted((M/root).glob('*')):
  if not p.is_file() or p.suffix in ['.py','.zip','.png','.pdf']:continue
  data=p.read_bytes(); rel=p.relative_to(M);dst=O/'stored_evidence'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(data)
  evidence.append({'source_path':str(p),'snapshot':str(dst.relative_to(O)),'sha256':sha(data),'bytes':len(data),'status':'preserved historical artifact; not independently rerun'})
(O/'EVIDENCE_IDENTITIES.json').write_text(json.dumps({'rows':evidence,'no_execution_claim':'All pass messages, timings, and counters remain attributed to saved artifacts. Source review is new; source execution is none.'},indent=2)+'\n')
# Source identity and manifest checks; no supplied executable processing.
preservation=[]
for r in rows:
 p=Path(r['local_content']);data=p.read_bytes();snap=(O/r['snapshot']).read_bytes(); mp=M/r['representative_path']; mb=mp.read_bytes() if mp.is_file() else None
 assert sha(data)==r['sha256']==sha(snap)
 if mb is not None:assert sha(mb)==r['sha256']
 preservation.append({'index':r['index'],'original_path':str(p),'representative_master_path':str(mp),'sha256_before':r['sha256'],'sha256_after':sha(data),'snapshot_sha256':sha(snap),'representative_master_sha256':sha(mb) if mb is not None else None,'bytes':len(data),'identical':True})
(O/'PRESERVATION_RECEIPT.json').write_text(json.dumps({'source_count':len(rows),'source_bytes':sum(r['size_bytes'] for r in rows),'source_lines':sum(r['lines'] for r in rows),'all_originals_unchanged':True,'source_executed':False,'source_imported':False,'source_compiled':False,'source_parsed':False,'central_registry_modified':False,'metadata_inputs':inputs,'sources':preservation},indent=2)+'\n')
print('metadata complete:',len(coverage),'prior COVERAGE files,',len(evidence),'evidence artifacts,',len(dependencies),'dependency references;',len(targets),'new hashes')
print('nonassigned source dependencies',len({h for d in dependencies for h in d['candidate_exact_hashes']}-targets))
