"""Reviewer archive and lexical-import reconciliation; does not parse source syntax or execute imports."""
from pathlib import Path,PurePosixPath
import json,re,hashlib,zipfile,io
O=Path(__file__).parent
rows=json.load(open(O/'ASSIGNED_SOURCES.json'));prov=json.load(open(O/'PROVENANCE.json'));ev=json.load(open(O/'EVIDENCE_INDEX.json'));graph={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))};cache={}
def arc(h):
 if h not in cache:
  parts=graph[h]['first_observed_at'].split('!');b=(Path('fft_research_master_20261009')/parts[0]).read_bytes()
  for name in parts[1:]:
   with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(name)
  assert hashlib.sha256(b).hexdigest()==h;cache[h]=b
 return cache[h]
inv=json.load(open(O/'INVENTORY_SNAPSHOT.json'));inv=inv.get('rows',inv) if isinstance(inv,dict) else inv
prior={r['sha256'] for r in inv if r.get('static_inspection_complete')}
reg=json.load(open(O/'REGISTRY_START_SNAPSHOT.json'));prior|={r['sha256'] for r in reg['rows'] if r.get('full_static_inspection')};assigned={r['sha256'] for r in rows}
verified={};imports=[]
for row,pr in zip(rows,prov):
 assert row['sha256']==pr['sha256']
 with zipfile.ZipFile(io.BytesIO(arc(pr['archive_sha256']))) as z:
  for m in pr['related_archived_code_metadata_only']:
   key=(pr['archive_sha256'],m['name'])
   if key not in verified:
    b=z.read(m['name']);h=hashlib.sha256(b).hexdigest();assert h==m['sha256'];verified[key]={'archive_sha256':key[0],'member':key[1],'sha256':h,'bytes':len(b),'bytes_rehashed':True,'coverage':'assigned_full_read' if h in assigned else 'previous_full_read' if h in prior else 'unread_dependency_candidate'}
 text=(O/row['snapshot']).read_text()
 lex=[]
 for i,line in enumerate(text.splitlines(),1):
  match=re.match(r'\s*(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))',line)
  if match:lex.append((i,match.group(1) or match.group(2),line.strip()))
 for lineno,module,statement in lex:
  basename=module.rsplit('.',1)[-1]+'.py'
  candidates=[v for k,v in verified.items() if k[0]==pr['archive_sha256'] and PurePosixPath(k[1]).name==basename and any(m['name']==k[1] for m in pr['related_archived_code_metadata_only'])]
  # Cross-project sys.path imports are matched elsewhere in the same archive, with ambiguity retained.
  if not candidates:
   for m in graph[pr['archive_sha256']]['members']:
    if m['is_code'] and PurePosixPath(m['name']).name==basename:
     key=(pr['archive_sha256'],m['name'])
     if key not in verified:
      with zipfile.ZipFile(io.BytesIO(arc(key[0]))) as z:b=z.read(key[1])
      assert hashlib.sha256(b).hexdigest()==m['sha256'];h=m['sha256'];verified[key]={'archive_sha256':key[0],'member':key[1],'sha256':h,'bytes':len(b),'bytes_rehashed':True,'coverage':'assigned_full_read' if h in assigned else 'previous_full_read' if h in prior else 'unread_dependency_candidate'}
     candidates.append(verified[key])
  imports.append({'source_index':row['index'],'source_sha256':row['sha256'],'line':lineno,'statement':statement,'module':module,'candidates':candidates,'resolution':'local_archived_candidates' if candidates else 'stdlib_or_external_package_or_unresolved','note':'Lexical discovery only. Multiple candidates are not asserted to be runtime resolution; installed package versions are not freshly verified.'})
# Two inherited manifest exceptions: preserve/re-hash the historical artifact, without rewriting the manifest.
exceptions=[]
for m in json.load(open(O/'STORED_MANIFEST_RECONCILIATION.json')):
 if m['matches_containing_archive']:continue
 matches=[]
 for h,a in graph.items():
  for entry in a['members']:
   if entry['sha256']==m['sha256']:matches.append((len(a['first_observed_at']),h,entry))
 _,h,entry=min(matches)
 with zipfile.ZipFile(io.BytesIO(arc(h))) as z:b=z.read(z.infolist()[entry['member_index']])
 assert hashlib.sha256(b).hexdigest()==m['sha256']
 local='evidence/'+m['sha256']+'__historical_'+PurePosixPath(entry['name']).name;(O/local).write_bytes(b)
 exceptions.append({**m,'historical_matching_archive_sha256':h,'historical_matching_member':entry['name'],'historical_snapshot':local,'historical_bytes_verified':True,'interpretation':'Inherited manifest is stale for the nested copied package: changed test log' if m['present_in_containing_archive'] else 'Inherited manifest references an omitted benchmark log; original log survives in recovered original archive'})
# Declared input hashes are provenance receipts; rehash known archives and corresponding members.
receipts=[]
for e in ev:
 if PurePosixPath(e['member']).name not in ['INPUT_PROVENANCE.json','PROVENANCE.json','archive_hashes.json']:continue
 try:d=json.loads((O/e['local']).read_text())
 except Exception:continue
 def walk(x,path=''):
  if isinstance(x,dict):
   for k,v in x.items():
    if isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v):
     known_archive=v in graph
     if known_archive:assert hashlib.sha256(arc(v)).hexdigest()==v
     matching=[m['name'] for m in graph[e['archive_sha256']]['members'] if m['sha256']==v]
     verified_member=None
     if not known_archive:
      options=[(0 if h==e['archive_sha256'] else 1,len(a['first_observed_at']),h,m) for h,a in graph.items() for m in a['members'] if m['sha256']==v]
      if options:
       _,_,ah,mm=min(options,key=lambda x:x[:3])
       with zipfile.ZipFile(io.BytesIO(arc(ah))) as z:raw=z.read(z.infolist()[mm['member_index']])
       assert hashlib.sha256(raw).hexdigest()==v
       local='evidence/'+v+'__receipt_'+PurePosixPath(mm['name']).name;(O/local).write_bytes(raw)
       verified_member={'archive_sha256':ah,'member':mm['name'],'snapshot':local,'bytes_rehashed':True}
     receipts.append({'evidence':e['member'],'field':path+'/'+k,'sha256':v,'known_archive_rehashed':known_archive,'matching_containing_archive_members':matching,'verified_member':verified_member})
    elif isinstance(v,(dict,list)):walk(v,path+'/'+k)
  elif isinstance(x,list):
   for i,v in enumerate(x):walk(v,path+'/'+str(i))
 walk(d)
(O/'DEPENDENCY_RECONCILIATION.json').write_text(json.dumps({'method':'Lexical import lines and archive-byte hashes; no AST or execution; candidate catalog is not dependency closure proof','imports':imports,'related_code_candidates':list(verified.values())},indent=2))
(O/'MANIFEST_EXCEPTIONS.json').write_text(json.dumps(exceptions,indent=2));(O/'INPUT_RECEIPT_RECONCILIATION.json').write_text(json.dumps(receipts,indent=2))
print(json.dumps({'import_lines':len(imports),'candidate_occurrences_rehashed':len(verified),'unique_candidate_hashes':len({r['sha256'] for r in verified.values()}),'unread_unique_candidate_hashes':len({r['sha256'] for r in verified.values() if r['coverage']=='unread_dependency_candidate'}),'manifest_exceptions':len(exceptions),'input_receipts':len(receipts)},indent=2))
