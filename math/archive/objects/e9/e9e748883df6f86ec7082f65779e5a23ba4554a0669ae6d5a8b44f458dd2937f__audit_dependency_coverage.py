#!/usr/bin/env python3
"""Fresh crosswalk of available exact dependency candidates and full-source evidence."""
import json,pathlib,re,collections,hashlib
P=pathlib.Path('[local workspace]');O=P/'final_review_closure_0535';reg=json.loads((P/'post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json').read_text());inv=json.loads((P/'code_coverage_audit_0228/CODE_COVERAGE_INVENTORY.json').read_text());program={r['sha256'] for r in inv if r['coverage_status']!='non_program_build_metadata'};read={r['sha256'] for r in inv if r['static_inspection_complete']}|{r['sha256'] for r in reg['rows']};templates={r['sha256'] for r in reg['semantic_template_rows']}
rows=[]
def walk(v,path,incandidate=False):
 if isinstance(v,dict):
  if incandidate:
   h=next((v[k] for k in ['sha256','code_sha256','source_sha256','exact_sha256'] if isinstance(v.get(k),str) and re.fullmatch('[0-9a-f]{64}',v[k])),None)
   if h:rows.append({'metadata_file':current,'json_path':path,'candidate_sha256':h,'candidate_record':v,'in_frozen_program_universe':h in program,'literal_full_read_accepted':h in read,'template_complete_accepted':h in templates,'runtime_resolution_verified_by_this_audit':False})
  for k,x in v.items():walk(x,path+'/'+k,incandidate or 'candidate' in k.lower())
 elif isinstance(v,list):
  for i,x in enumerate(v):walk(x,path+'/'+str(i),incandidate)
for package in sorted({r['package'] for r in reg['rows']}):
 for f in sorted((P/package).glob('*DEPEND*.json')):
  current=str(f);walk(json.loads(f.read_text()),'')
hashes={r['candidate_sha256'] for r in rows if r['in_frozen_program_universe']};pending=hashes-read-templates
summary={'candidate_records':len(rows),'unique_candidate_hashes':len({r['candidate_sha256'] for r in rows}),'unique_in_frozen_program_universe':len(hashes),'in_corpus_candidate_hashes_with_accepted_static_coverage':len(hashes&(read|templates)),'in_corpus_candidate_hashes_pending':sorted(pending),'outside_frozen_universe_hashes':sorted({r['candidate_sha256'] for r in rows}-program),'boundary':'Only explicitly hash-bearing candidate objects in accepted package dependency metadata are crosswalked. This is not an exhaustive dynamic dependency graph, package version/build pinning or runtime import proof; plain names carry no identity credit.'}
(O/'DEPENDENCY_COVERAGE_CROSSWALK.json').write_text(json.dumps(rows,indent=2)+'\n');(O/'DEPENDENCY_COVERAGE_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
# Exact selected text reading queues; proof status remains each row's separately scoped finding.
textrows=[]
for package,key in [('coverage_audit_20261010/review_queue1_aggregate','q1'),('coverage_audit_20261010/review_queue2_complete207','q2')]:
 p=P/package;x=json.loads((p/'COVERAGE.json').read_text())
 for r in x['rows']:
  snap=r.get('source_snapshot',r.get('local_inert_snapshot'));q=pathlib.Path(snap);q=q if q.is_absolute() else p/q
  if not q.exists() and r.get('review_package'):q=p/r['review_package']/snap
  got=hashlib.sha256(q.read_bytes()).hexdigest() if q.exists() else None
  textrows.append({'queue':key,'queue_index':r['queue_index'],'sha256':r['sha256'],'snapshot':str(q),'snapshot_matches':got==r['sha256'],'declared_full_text_inspection':r.get('full_text_inspection'),'proof_acceptance':r.get('proof_acceptance')})
for r in json.loads((P/'external_inventory_text_review_0225/sealed_reconciliation_0233/ITEM_RECONCILIATION.json').read_text()):
 p=pathlib.Path(r['recovered_text']);textrows.append({'queue':'historical70','queue_index':r['index'],'sha256':r['sha256'],'snapshot':str(p),'snapshot_matches':hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256'],'declared_full_text_inspection':'full-text review and status reconciliation per sealed report','proof_acceptance':r['family_disposition']})
(O/'TEXT_READ_CROSSWALK.json').write_text(json.dumps(textrows,indent=2)+'\n');print('text',len(textrows),'unique',len({r['sha256'] for r in textrows}),'snapshot failures',[r for r in textrows if not r['snapshot_matches']])
