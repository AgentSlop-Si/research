"""Fresh reviewer metadata collector. Never executes/imports/parses archived source."""
from pathlib import Path, PurePosixPath
import json,hashlib,zipfile,collections,re
BASE=Path(__file__).resolve().parent
AUDIT=Path('code_coverage_audit_0228')
MASTER=Path('fft_research_master_20261009')
rows=json.loads((BASE/'ASSIGNED_SOURCES.json').read_text())['rows']
prov=json.loads((BASE/'PROVENANCE.json').read_text())
graph={x['sha256']:x for x in json.loads((AUDIT/'ARCHIVE_GRAPH.json').read_text())}
sha=lambda b:hashlib.sha256(b).hexdigest()
write=lambda n,v:(BASE/n).write_text(json.dumps(v,indent=2)+'\n')
# Full inventory copies are historical data, not newly generated syntax analysis.
for name in ['CODE_COVERAGE_INVENTORY.json','INPUT_SNAPSHOT.json']:(BASE/('INVENTORY_SNAPSHOT.json' if name.startswith('CODE') else 'INPUT_SNAPSHOT.json')).write_bytes((AUDIT/name).read_bytes())
evidences=json.loads((AUDIT/'COVERAGE_EVIDENCE.json').read_text());wanted={i for r in rows for i in r.get('evidence_ids',[])}
history=[x for x in evidences if x['id'] in wanted];write('HISTORICAL_COVERAGE_EVIDENCE.json',history)
# Preserve evidence exact bytes from all direct sibling data/report/receipt/seal files.
paths=set()
code_extensions={'.py','.cpp','.c','.h','.hpp','.pyc','.pyo','.sh','.smt2'}
for r in rows:
 parent=(MASTER/r['representative_path']).parent
 paths.update(p for p in parent.iterdir() if p.is_file() and p.suffix.lower() not in code_extensions|{'.zip','.png','.pdf','.pptx','.docx'} and p.name!='exhaustive_anchor')
for h in history:
 p=MASTER/h['document']
 if p.is_file():paths.add(p)
 for o in h.get('origin_evidence',[]):
  p=MASTER/o['path']
  if p.is_file():paths.add(p)
index=[];by_path={};by_hash={}
for p in sorted(paths):
 b=p.read_bytes();h=sha(b);rel=str(p.relative_to(MASTER));local=f'evidence/{h}__{p.name}'
 (BASE/local).write_bytes(b)
 row={'path':rel,'sha256':h,'bytes':len(b),'local':local,'kind':'stored historical evidence; not a fresh execution result'}
 index.append(row);by_path[rel]=row;by_hash.setdefault(h,[]).append(row)
write('EVIDENCE_INDEX.json',index)
# Verify exact standalone and archive occurrence identities. ZIP members stay inert bytes.
archive_handles={};archives=[]
for h in sorted({o['archive_sha256'] for r in rows for o in r['occurrences'] if o['kind']=='archive_member'}):
 a=graph[h];p=Path(a['first_observed_at']);p=p if p.is_absolute() else MASTER/p
 rec={'sha256':h,'path':str(p),'expected_bytes':a['size_bytes'],'available':p.is_file()}
 if p.is_file():
  b=p.read_bytes();rec.update(actual_sha256=sha(b),actual_bytes=len(b),byte_identity_verified=sha(b)==h and len(b)==a['size_bytes']);assert rec['byte_identity_verified'];archive_handles[h]=zipfile.ZipFile(p)
 archives.append(rec)
for p,r in zip(prov,rows):
 occurrence_checks=[]
 for o in r['occurrences']:
  c=dict(o)
  if o['kind']=='master_standalone':
   f=MASTER/o['path'];b=f.read_bytes();c.update(bytes=len(b),actual_sha256=sha(b),byte_identity_verified=sha(b)==r['sha256'])
  elif o['kind']=='archive_member':
   a=graph[o['archive_sha256']];m=a['members'][o['member_index']];c['inventory_member_hash_match']=m['sha256']==r['sha256'] and m['name']==o['name']
   if o['archive_sha256'] in archive_handles:
    z=archive_handles[o['archive_sha256']];i=z.infolist()[o['member_index']];assert i.filename==o['name'];b=z.read(i);c.update(bytes=len(b),actual_sha256=sha(b),byte_identity_verified=sha(b)==r['sha256'])
   else:c['byte_identity_verified']=False
  occurrence_checks.append(c)
 p['occurrence_verification']=occurrence_checks;p['byte_identity_verified']=all(x['byte_identity_verified'] for x in occurrence_checks)
 p['stored_evidence']=[e for e in index if PurePosixPath(e['path']).parent==PurePosixPath(r['representative_path']).parent]
 p['historical_evidence_records']=[h['id'] for h in history if h['code_sha256']==r['sha256']]
write('PROVENANCE.json',prov);write('ARCHIVE_IDENTITIES.json',archives)
for z in archive_handles.values():z.close()
# Reconcile textual and JSON manifests/seals under their historical base directory.
checks=[];manifest_parse=[]
def ref(manifest,label,path,expected,size=None):
 path=str(path);target=manifest.parent/path
 c={'manifest':str(manifest.relative_to(MASTER)),'field':label,'target_recorded':path,'expected_sha256':expected,'target_exists':target.is_file()}
 if target.is_file():
  b=target.read_bytes();c.update(actual_sha256=sha(b),actual_bytes=len(b),digest_matches=sha(b)==expected)
  if size is not None:c.update(expected_bytes=size,size_matches=len(b)==size)
 checks.append(c)
def walk_json(obj,manifest,key='$'):
 if isinstance(obj,dict):
  h=obj.get('sha256');name=next((obj[x] for x in ['path','name','file','filename','relative_path','source_path'] if isinstance(obj.get(x),str)),None)
  if isinstance(h,str) and re.fullmatch('[0-9a-f]{64}',h) and name:ref(manifest,key,name,h,obj.get('bytes',obj.get('size_bytes',obj.get('size'))))
  for k,v in obj.items():
   if isinstance(v,dict) and isinstance(v.get('sha256'),str) and not any(isinstance(v.get(x),str) for x in ['path','name','file','filename','relative_path','source_path']):
    if re.fullmatch('[0-9a-f]{64}',v['sha256']):ref(manifest,key+'/'+k,k,v['sha256'],v.get('bytes',v.get('size_bytes',v.get('size'))))
   elif isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) and ('.' in k or '/' in k):ref(manifest,key+'/'+k,k,v)
   walk_json(v,manifest,key+'/'+k)
 elif isinstance(obj,list):
  for i,v in enumerate(obj):walk_json(v,manifest,key+'/'+str(i))
for p in sorted(paths):
 if not any(word in p.name.upper() for word in ['SHA256SUM','MANIFEST','SEAL']):continue
 if p.suffix.lower()=='.json':
  try:d=json.loads(p.read_text());walk_json(d,p);manifest_parse.append({'path':str(p.relative_to(MASTER)),'status':'parsed JSON metadata'})
  except (ValueError,UnicodeError) as e:manifest_parse.append({'path':str(p.relative_to(MASTER)),'status':'unparsed','error':str(e)})
 else:
  try:
   count=0
   for ln,line in enumerate(p.read_text().splitlines(),1):
    m=re.match(r'^([0-9a-f]{64})\s+\*?(.+)$',line)
    if m:ref(p,f'L{ln}',m[2],m[1]);count+=1
   manifest_parse.append({'path':str(p.relative_to(MASTER)),'status':'text metadata','digest_lines':count})
  except UnicodeError:pass
write('STORED_MANIFEST_RECONCILIATION.json',checks);write('MANIFEST_FORMATS.json',manifest_parse)
# Record nested hash references without claiming that a reference proves execution.
master_hashes=json.loads((AUDIT/'MASTER_FILE_HASHES.json').read_text());known=collections.defaultdict(list)
for e in master_hashes:known[e['sha256']].append(e['path'])
refs=[]
def walk_refs(d,src,key='$'):
 if isinstance(d,dict):
  for k,v in d.items():walk_refs(v,src,key+'/'+k)
 elif isinstance(d,list):
  for i,v in enumerate(d):walk_refs(v,src,key+'/'+str(i))
 elif isinstance(d,str) and re.fullmatch('[0-9a-f]{64}',d):
  refs.append({'evidence':src,'field':key,'sha256':d,'matching_assigned_source':[r['representative_path'] for r in rows if r['sha256']==d],'matching_master_paths':known.get(d,[]),'reference_is_execution_proof':False})
for e in index:
 if e['path'].endswith('.json'):
  try:walk_refs(json.loads((BASE/e['local']).read_text()),e['path'])
  except (ValueError,UnicodeError):pass
write('STORED_HASH_REFERENCE_RECONCILIATION.json',refs)
# Dependencies resolved by exact sibling bytes rather than basename or old AST equivalence.
deps=[]
for source,target,line,kind in [(3,2,'L8-9','ordinary import'),(19,18,'L6-7','dynamic import/exec_module'),(27,25,'L4','ordinary import'),(28,25,'L3','ordinary import')]:
 a=rows[source-1];b=rows[target-1];f=(MASTER/a['representative_path']).parent/Path(b['representative_path']).name;blob=f.read_bytes()
 deps.append({'source_sha256':a['sha256'],'source_path':a['representative_path'],'line':line,'kind':kind,'target_path':str(f.relative_to(MASTER)),'target_sha256':sha(blob),'assigned_target_sha256':b['sha256'],'exact_sibling_match':sha(blob)==b['sha256'],'both_fully_read_now':True,'executed_now':False})
write('DEPENDENCY_RECONCILIATION.json',{'resolved_local_python_edges':deps,'external_packages':{'numpy':'versions/runtime unavailable from inert inspection','mpmath':'versions/runtime unavailable from inert inspection','sympy':'versions/runtime unavailable from inert inspection'},'S33_expression_parser':{'line':46,'action':'sympy.sympify on certificate coefficient strings','not_invoked_in_this_review':True},'runtime_dependency_closure_complete':False,'all_dependencies_executed':False})
# Preserve historical declarations and their original classifications.
execs=[]
for r in rows:
 hs=[h for h in history if h['code_sha256']==r['sha256']]
 execs.append({'sha256':r['sha256'],'path':r['representative_path'],'inventory_recorded_execution':r['recorded_execution'],'inventory_coverage_status':r['coverage_status'],'evidence':[{'id':h['id'],'kind':h['kind'],'scope':h.get('scope'),'run_role':h.get('run_role'),'program_reference':h.get('program_reference'),'document':h['document'],'document_sha256':h['document_sha256'],'document_exact_snapshot_match':by_path.get(h['document'],{}).get('sha256')==h['document_sha256'],'quote_or_record':h.get('quote_or_record')} for h in hs],'source_executed_in_this_review':False,'historical_result_does_not_prove_current_execution':True})
write('STORED_EXECUTION_RECONCILIATION.json',execs)
print(json.dumps({'sources':len(rows),'bytes':sum(r['size_bytes'] for r in rows),'archive_count':len(archives),'archives_available':sum(a['available'] for a in archives),'verified_source_occurrences':sum(sum(c['byte_identity_verified'] for c in p['occurrence_verification']) for p in prov),'evidence_files':len(index),'evidence_bytes':sum(e['bytes'] for e in index),'history_records':len(history),'historically_recorded_hashes':sum(r['recorded_execution'] for r in rows),'manifest_entries':len(checks),'manifest_present_matches':sum(c.get('digest_matches',False) for c in checks),'manifest_present_mismatches':sum(c.get('digest_matches') is False for c in checks),'manifest_missing_targets':sum(not c['target_exists'] for c in checks),'hash_references':len(refs),'dependencies':len(deps)},indent=2))
