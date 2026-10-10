"""Fresh inert stored-data reconciliation, never imports supplied programs."""
from pathlib import Path,PurePosixPath
import json,hashlib,collections,zipfile,math
B=Path(__file__).resolve().parent;M=Path('fft_research_master_20261009');A=Path('code_coverage_audit_0228')
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda n:json.loads((B/n).read_text())
write=lambda n,v:(B/n).write_text(json.dumps(v,indent=2)+'\n')
index=load('EVIDENCE_INDEX.json');imap={e['path']:e for e in index};provenance=load('PROVENANCE.json')
known=collections.defaultdict(list)
for r in json.loads((A/'MASTER_FILE_HASHES.json').read_text()):known[r['sha256']].append(r['path'])
graph={a['sha256']:a for a in json.loads((A/'ARCHIVE_GRAPH.json').read_text())}
checks=load('STORED_MANIFEST_RECONCILIATION.json');opened={};archive_verified={}
for c in checks:
 if c['target_exists']:c['resolution']='direct historical filesystem path verified';continue
 # Missing paths in these manifests are ZIP member names, not filesystem paths.
 path=M/c['manifest'];d=json.loads(path.read_text());parts=c['field'].split('/')[1:];node=d;parents=[]
 for s in parts:
  parents.append(node);node=node[int(s)] if isinstance(node,list) else node[s]
 container=next((p for p in reversed(parents) if isinstance(p,dict) and 'members' in p and 'sha256' in p),None)
 if container is None:c['resolution']='unresolved provenance scope';continue
 h=container['sha256']
 if h not in opened:
  candidates=[M/p for p in known.get(h,[])]
  if h in graph:
   p=Path(graph[h]['first_observed_at']);candidates.append(p if p.is_absolute() else M/p)
  f=next((p for p in candidates if p.is_file() and sha(p.read_bytes())==h),None)
  if f is not None:opened[h]=zipfile.ZipFile(f);archive_verified[h]=str(f)
 if h in opened:
  z=opened[h];infos=[i for i in z.infolist() if i.filename==c['target_recorded']]
  if len(infos)==1:
   blob=z.read(infos[0]);c.update(resolution='exact member in rehashed source archive',archive_sha256=h,archive_path=archive_verified[h],actual_sha256=sha(blob),actual_bytes=len(blob),digest_matches=sha(blob)==c['expected_sha256'])
   if c.get('expected_bytes') is not None:c['size_matches']=len(blob)==c['expected_bytes']
  else:c['resolution']='archive member absent or duplicate'
 else:c['resolution']='exact source archive unavailable'
for z in opened.values():z.close()
write('STORED_MANIFEST_RECONCILIATION.json',checks)
# Explicit source-to-result association from each complete source read.
result_names=['CHECK_RESULTS.json',None,'CHECK_RESULTS.json','VERIFICATION.txt','CHECK_RESULTS.json','CHECK_RESULTS.json','independent_graph_results.json','independent_results.json','independent_results.json','independent_check_results.json','independent_phase14_results.json','INDEPENDENT_RESULTS.json','FUSION_RESULTS.json','CHECK_RESULTS.json','CHECK_RESULTS.json','CHECK_RESULTS.json','CHECK_RESULTS.json','INDEPENDENT_RESULTS.json','EXTRA_RESULTS.json','INDEPENDENT_RESULTS.json','CHECK_RESULTS.json','CHECK_RESULTS.json','CHECK_RESULTS.json','anchor_ranks.bin','INDEPENDENT_RESULTS.json','PAIRED_DRESSING_RESULTS.json','SEPARATOR_RESULTS.json','V16_EXTRA_RESULTS.json','INDEPENDENT_RESULTS.json','LAYOUT_PROBE.json','EXACT_CHECK_RESULTS.json','INDEPENDENT_NETWORK_RESULTS.json','VERIFIED_RESULTS.json','PHASE5_REVIEW_RESULTS.json','PHASE8_REVIEW_RESULTS.json','CERTIFICATE_AUDIT_RESULTS.json','FRACTION_CONTROLS.json','LEDGER_CONTROLS.json','RESULTS.json','EXACT_RESULTS.json','RECTANGLE_GRAY_RESULTS.json','INDEPENDENT_RESULTS.json','JACOBIAN_RESULTS.json','EXACT_RESULTS.json','INDEPENDENT_RESULTS.json','INDEPENDENT_RESULTS.json','INDEPENDENT_RESULTS.json','INDEPENDENT_RESULTS.json','NORMALIZATION_RESULTS.json','INDEPENDENT_RESULTS.json','INDEPENDENT_RESULTS.json','INDEPENDENT_RESULTS.json']
assert len(result_names)==52
results=[]
for rec,name in zip(provenance,result_names):
 i=rec['index'];base=PurePosixPath(rec['representative_path']).parent
 out={'review_id':rec['review_id'],'source_sha256':rec['sha256'],'source_path':rec['representative_path'],'result_role':'stored result associated by literal output path and package context; no new execution','inventory_recorded_execution':rec['recorded_execution']}
 if name is None:
  out['result_role']='library helper, no standalone entrypoint/output; S03 imports this exact sibling';out['result_evidence']=None
 else:
  path=str(base/name);e=imap[path];out['result_evidence']=e
  blob=(B/e['local']).read_bytes();assert sha(blob)==e['sha256']
  if name.endswith('.json'):
   d=json.loads(blob);out['json_type']=type(d).__name__;out['top_level_keys']=list(d) if isinstance(d,dict) else None;out['top_level_list_count']=len(d) if isinstance(d,list) else None
   if isinstance(d,dict):
    out['stored_status_fields']={k:v for k,v in d.items() if k in ['status','all_passed','scope','method','source_policy','source_code_executed','uploaded_code_executed','no_uploaded_code_executed','source_execution','independence','interpretation','conclusion']}
    out['stored_count_fields']={k:v for k,v in d.items() if isinstance(v,int) and not isinstance(v,bool)}
    if 'checker_sha256' in d:out['checker_self_hash_matches']=d['checker_sha256']==rec['sha256']
  elif name.endswith('.bin'):out['stored_byte_histogram']={str(k):v for k,v in sorted(collections.Counter(blob).items())}
  else:out['stored_text']=blob.decode()
  logs=[e for e in index if PurePosixPath(e['path']).parent==base and e['path'].endswith('.log')];out['sibling_log_candidates']=[{'path':e['path'],'sha256':e['sha256'],'bytes':e['bytes']} for e in logs]
  out['same_directory_receipts']=[{'path':e['path'],'sha256':e['sha256']} for e in index if PurePosixPath(e['path']).parent==base and any(s in PurePosixPath(e['path']).name.upper() for s in ['PORTAB','REPLAY','REPRODUCIBILITY'])]
 results.append(out)
write('STORED_RESULT_RECONCILIATION.json',results)
# Reconcile JSON stdout fragments only with stored JSON payloads, ignoring no fields.
decoder=json.JSONDecoder();logchecks=[]
for r in results:
 e=r.get('result_evidence')
 if not e or not e['path'].endswith('.json'):continue
 data=json.loads((B/e['local']).read_text())
 for log in r.get('sibling_log_candidates',[]):
  s=(B/imap[log['path']]['local']).read_text();pos=0;values=[]
  while pos<len(s):
   if s[pos] not in '{[':pos+=1;continue
   try:v,end=decoder.raw_decode(s,pos);values.append(v);pos=end
   except ValueError:pos+=1
  comparable=[]
  for v in values:
   if isinstance(v,dict) and isinstance(data,dict):
    common=sorted(set(v)&set(data))
    if common:comparable.append({'shared_top_level_fields':common,'equal_fields':[k for k in common if v[k]==data[k]],'different_fields':[k for k in common if v[k]!=data[k]],'exact_full_json_match':v==data})
   elif type(v)==type(data) and v==data:comparable.append({'exact_full_json_match':True})
  logchecks.append({'source':r['review_id'],'result':e['path'],'log':log['path'],'json_fragments':len(values),'comparisons':comparable,'comparison_does_not_prove_new_execution':True})
write('STORED_LOG_RECONCILIATION.json',logchecks)
summary={'manifest_records':len(checks),'direct_matches':sum(c['resolution']=='direct historical filesystem path verified' and c.get('digest_matches',False) for c in checks),'archive_member_matches':sum(c['resolution']=='exact member in rehashed source archive' and c.get('digest_matches',False) for c in checks),'digest_mismatches':sum(c.get('digest_matches') is False for c in checks),'unresolved':sum('digest_matches' not in c for c in checks),'sources_with_result_artifacts':sum(r.get('result_evidence') is not None for r in results),'helper_without_standalone_result':1,'log_associations':len(logchecks),'current_execution':'none','history_status_preserved':True}
write('EVIDENCE_RECONCILIATION_SUMMARY.json',summary);print(json.dumps(summary,indent=2))
