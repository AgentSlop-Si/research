"""Reviewer-authored inert metadata/result reconciliation. Never executes source members."""
from pathlib import Path
import hashlib,io,json,zipfile
B=Path('material_extension_source_review_0500/worker_materials')
rows=json.loads((B/'ROWS.json').read_text()); hashes={r['sha256'] for r in rows}
inv=json.load(open('code_coverage_audit_0228/CODE_COVERAGE_INVENTORY.json'))
reg=json.load(open('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json'))
reviewed={r['sha256'] for r in reg['rows']}
archive='ab3415e2ff5e763f38a141c5ade7770e14ee4f11c64f1e8f608425607915836c'
outer=Path('fft_research_master_20261009/additions/0155_material_coverage_and_new_results/fft_historical_originals_recovered_20261010.zip')
member='originals/'+archive+'/fft_materials_extension_20261009.zip'
with zipfile.ZipFile(outer) as z:b=z.read(member)
assert hashlib.sha256(b).hexdigest()==archive
z=zipfile.ZipFile(io.BytesIO(b));info=z.infolist();catalog={x.filename:hashlib.sha256(z.read(x)).hexdigest() for x in info if not x.is_dir()}
std={'pathlib','sys','dataclasses','operator','collections','json','random','math','hashlib','itertools','concurrent.futures','subprocess','time','importlib.util'}
deps=[]
for r in rows:
 refs=[]
 for imp in r.get('import_references',[]):
  module=imp['module']; names=[module] if module else imp['names']
  for mod in names:
   if mod in std:continue
   candidates=[{'archive_path':p,'sha256':h,'prior_registry_full_read':h in reviewed,'in_this_full_read':h in hashes} for p,h in catalog.items() if p.endswith('/'+mod.replace('.','/')+'.py')]
   refs.append({'module':mod,'same_archive_candidates':candidates,'resolution':'same-archive path candidates; runtime import resolution and transitive closure not certified'})
 deps.append({'sha256':r['sha256'],'source_path':r['representative_path'],'import_candidates':refs})
folders={str(Path(r['representative_path']).parent) for r in rows if Path(r['representative_path']).name!='run_all.py'}
results=[]
for item in info:
 p=item.filename
 if not p.endswith('.json') or not (any(p.startswith(f+'/') for f in folders) or p.endswith('/verification_summary.json')):continue
 raw=z.read(item)
 try:d=json.loads(raw)
 except (ValueError,UnicodeDecodeError):continue
 if not isinstance(d,dict) or 'status' not in d:continue
 stored=B/'stored_results'/p.split('/',1)[1];stored.parent.mkdir(parents=True,exist_ok=True);stored.write_bytes(raw)
 scalar_summary={k:v for k,v in d.items() if isinstance(v,(str,int,float,bool)) or v is None}
 sourcebindings=[]
 sha=d.get('source_sha256')
 if isinstance(sha,str):sourcebindings.append({'recorded_sha256':sha,'in_this_full_read':sha in hashes,'present_in_same_archive':sha in catalog.values()})
 elif isinstance(sha,dict):
  for name,h in sha.items():sourcebindings.append({'name':name,'recorded_sha256':h,'same_directory_exact_match':catalog.get(str(Path(p).parent/name))==h,'in_this_full_read':h in hashes})
 if p.endswith('/verification_summary.json'):
  for check in d.get('checks',[]):
   source='fft_materials_extension_20261009/'+check['component']+'/'+check['script']
   sourcebindings.append({'source_path':source,'recorded_sha256':check['source_sha256'],'archive_exact_match':catalog.get(source)==check['source_sha256'],'in_this_full_read':check['source_sha256'] in hashes,'historical_exit_code':check['exit_code']})
 results.append({'archive_path':p,'sha256':hashlib.sha256(raw).hexdigest(),'size_bytes':len(raw),'local_copy':str(stored),'historical_summary':scalar_summary,'source_bindings':sourcebindings,'status_meaning':'Stored assertion only. Source was not executed in this review; matching digest does not validate result or dependency closure.'})
report={'archive_sha256':archive,'outer_archive':str(outer),'nested_member':member,'source_preservation_verified':all(catalog[r['representative_path']]==r['sha256'] for r in rows),'prior_registry_overlap':sorted(hashes & reviewed),'dependency_resolution':deps,'stored_results':results,'dependency_closure_complete':False,'source_executed_in_review':False}
(B/'RECONCILIATION.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({'exact_archive_source_matches':len(rows),'stored_result_count':len(results),'stored_summary':[{'path':r['archive_path'],'summary':r['historical_summary'],'bindings':r['source_bindings']} for r in results]},indent=2))
