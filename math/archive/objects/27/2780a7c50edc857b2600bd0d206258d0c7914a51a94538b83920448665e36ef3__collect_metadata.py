"""Fresh review metadata collector. Supplied source is only read as bytes/text."""
import hashlib,json,pathlib,re,shutil,zipfile
P=pathlib.Path('archived_proof_source_review_0527'); A=pathlib.Path('code_coverage_audit_0228'); M=pathlib.Path('fft_research_master_20261009')
def sha(b):return hashlib.sha256(b).hexdigest()
def put(n,x): (P/n).write_text(json.dumps(x,indent=2)+'\n')
rows=json.loads((P/'SOURCE_MANIFEST.json').read_text()); inv=json.loads((A/'WORKING_CODE_INVENTORY.json').read_text()); registry=json.loads((P/'REGISTRY_BEFORE.json').read_text())
put('INVENTORY_SNAPSHOT.json',[r for r in inv if r['sha256'] in {r['sha256'] for r in rows}])
(P/'provenance'/'records').mkdir(exist_ok=True)
seen={}; record_index=[]
def snapshot(path,kind,source_index=None):
 if not path.is_file():return {'path':str(path),'exists':False}
 b=path.read_bytes();h=sha(b); dst='provenance/records/'+h
 if h not in seen:(P/dst).write_bytes(b);seen[h]=dst
 item={'path':str(path),'sha256':h,'bytes':len(b),'snapshot':dst,'kind':kind}
 if source_index is not None:item['source_index']=source_index
 record_index.append(item);return item
for name in ['ARCHIVE_ROOTS.json','ARCHIVE_GRAPH.json','COVERAGE_EVIDENCE.json','MASTER_FILE_HASHES.json']:
 snapshot(A/name,'original_inventory')
checks=[]; root_info=[]; roots=json.loads((A/'ARCHIVE_ROOTS.json').read_text()); relevant={o['archive_sha256'] for r in rows for o in r['occurrences'] if o['kind']=='archive_member'}
for h in sorted(relevant):
 candidates=[r for r in roots if r['sha256']==h]; actual=None
 for r in candidates:
  path=pathlib.Path(r['path']);path=path if path.is_absolute() else M/path
  if path.is_file():
   b=path.read_bytes()
   if sha(b)==h:actual=path;break
 info={'sha256':h,'candidates':candidates,'verified_path':str(actual) if actual else None,'archive_hash_verified':actual is not None}
 if actual:
  info['size_bytes']=actual.stat().st_size
  with zipfile.ZipFile(actual) as z:
   zs=z.infolist();info['member_count']=len(zs)
   for r in rows:
    for o in r['occurrences']:
     if o.get('archive_sha256')!=h:continue
     q=zs[o['member_index']];b=z.read(q)
     checks.append({'source_index':r['index'],'sha256':r['sha256'],'occurrence':o,'archive_verified':True,'member_index_name_matches':q.filename==o['name'],'member_size_and_hash_match':len(b)==r['size_bytes'] and sha(b)==r['sha256']})
 root_info.append(info)
for r in rows:
 for o in r['occurrences']:
  if o['kind']=='master_standalone':
   p=M/o['path']; b=p.read_bytes() if p.is_file() else None
   checks.append({'source_index':r['index'],'sha256':r['sha256'],'occurrence':o,'exists':b is not None,'size_and_hash_match':b is not None and len(b)==r['size_bytes'] and sha(b)==r['sha256']})
put('ARCHIVE_PROVENANCE.json',root_info);put('SOURCE_OCCURRENCE_CHECKS.json',checks)
evidence=json.loads((A/'COVERAGE_EVIDENCE.json').read_text()); evid={e['id']:e for e in evidence};out=[]
for r in rows:
 for id in r['evidence_ids']:
  e=evid[id];candidate=A/e.get('portable_document','')
  if not candidate.is_file():candidate=M/e['document']
  rec=snapshot(candidate,'historical_evidence',r['index']);out.append({'source_index':r['index'],'evidence':e,'document_snapshot':rec,'expected_document_hash_matches':rec.get('sha256')==e.get('document_sha256')})
put('HISTORICAL_EVIDENCE.json',out)
# Local data/log documents are indexed and hashed. This is not a full-read claim for each.
for r in rows:
 parent=(M/r['representative_path']).parent
 for f in sorted(parent.iterdir()):
  if f.is_file() and f.suffix.lower() in ('.json','.log','.md','.txt') and f.stat().st_size<16_000_000:snapshot(f,'neighbor_data_or_record',r['index'])
# Resolve explicit textual imports and wrapper targets, without compiling or AST.
deps=[]
for r in rows:
 text=(P/r['snapshot_path']).read_text(); parent=(M/r['representative_path']).parent;entries=[]
 for line_num,line in enumerate(text.splitlines(),1):
  found=[]
  m=re.match(r'^\s*from\s+([A-Za-z_][\w.]*)\s+import\s+',line)
  if m:found=[m.group(1)]
  else:
   m=re.match(r'^\s*import\s+(.+)',line)
   if m:found=[s.strip().split()[0] for s in m.group(1).split(',')]
  for mod in found:
   candidate=parent/(mod.replace('.','/')+'.py'); entry={'module':mod,'line':line_num,'text':line,'local_candidate':str(candidate),'local_candidate_exists':candidate.is_file()}
   if candidate.is_file():
    b=candidate.read_bytes();h=sha(b);entry.update(sha256=h,size_bytes=len(b),reviewed_in_this_assignment=h in {rr['sha256'] for rr in rows},inventory_candidates=[{'sha256':i['sha256'],'local_content':i['local_content']} for i in inv if i['sha256']==h])
   entry['resolution']='Static same-directory candidate only; runtime import path and installed dependency versions unverified.'
   entries.append(entry)
 if r['index'] in (34,38):
  targets=['audit_provenance.py','window_audit/independent_checks.py','phase23_audit/independent_checks.py'] if r['index']==34 else ['audit_provenance.py','rank_audit/independent_rank_checks.py','woodbury_audit/independent_checks.py','prior_window_audit/independent_checks.py']
  for target in targets:
   f=parent/target;b=f.read_bytes() if f.is_file() else None;entries.append({'subprocess_target':target,'exists':b is not None,'sha256':sha(b) if b else None,'execution_verified_by_current_review':False})
 deps.append({'source_index':r['index'],'sha256':r['sha256'],'dependencies':entries,'runtime_dependency_closure_complete':False})
put('DEPENDENCY_RECONCILIATION.json',deps);put('STORED_RECORDS_INDEX.json',record_index)
# Parse historical stored JSON summaries and command/receipt data, never execute or evaluate.
summary=[]
for rec in record_index:
 if rec['kind'] not in ('neighbor_data_or_record','historical_evidence'):continue
 if pathlib.Path(rec['path']).suffix.lower()!='.json':continue
 try:x=json.loads((P/rec['snapshot']).read_text())
 except Exception as e:summary.append({**rec,'json_parse_error':str(e)});continue
 if isinstance(x,dict):
  small={k:v for k,v in x.items() if isinstance(v,(str,int,float,bool,type(None))) or k.lower() in ('summary','checks','commands','runs','scripts','run','source_files') and len(json.dumps(v))<6000}
  structure={k:('list:'+str(len(v)) if isinstance(v,list) else 'dict:'+str(len(v)) if isinstance(v,dict) else type(v).__name__) for k,v in x.items()}
 else:small={};structure={'root_type':type(x).__name__,'length':len(x) if isinstance(x,list) else None}
 summary.append({**rec,'json_top_level':structure,'selected_saved_fields':small,'status':'stored historical data only; not regenerated'})
put('HISTORICAL_RESULTS_RECONCILIATION.json',summary)
print(json.dumps({'archive_roots_verified':sum(x['archive_hash_verified'] for x in root_info),'occurrences':len(checks),'failures':[x for x in checks if x.get('size_and_hash_match') is False or x.get('member_size_and_hash_match') is False or x.get('member_index_name_matches') is False],'historical_evidence_rows':len(out),'stored_record_occurrences':len(record_index),'unique_snapshots':len(seen),'dependency_local_files':sum(e.get('local_candidate_exists',False) for r in deps for e in r['dependencies'])},indent=2))
