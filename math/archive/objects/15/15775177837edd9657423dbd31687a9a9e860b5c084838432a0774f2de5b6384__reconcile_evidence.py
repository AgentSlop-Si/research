"""Reviewer-authored data-only reconciliation. No source import, AST, compile or execution."""
from pathlib import Path,PurePosixPath
import json,re,hashlib,zipfile,io,posixpath,sys
O=Path(__file__).parent;ROOT=Path('fft_research_master_20261009')
E=json.loads((O/'EVIDENCE_INDEX.json').read_text());G={a['sha256']:a for a in json.loads((O/'ARCHIVE_GRAPH_SNAPSHOT.json').read_text())};P=json.loads((O/'PROVENANCE.json').read_text());R=json.loads((O/'REGISTRY_START_SNAPSHOT.json').read_text());ROWS=json.loads((O/'ASSIGNED_SOURCES.json').read_text());reviewed={r['sha256'] for r in R['rows']};assigned={r['sha256'] for r in ROWS};cache={}
def arch(h):
 if h in cache:return cache[h]
 bits=G[h]['first_observed_at'].split('!');b=(ROOT/bits[0]).read_bytes()
 for s in bits[1:]:
  with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(s)
 assert hashlib.sha256(b).hexdigest()==h;cache[h]=b;return b
manifest=[];manifest_ignored=[];refs=[];summaries=[]
for e in E:
 b=(O/e['local']).read_bytes();assert hashlib.sha256(b).hexdigest()==e['sha256']
 name=e['occurrences'][0]['member'];d=None
 if name.endswith('.json'):
  try:d=json.loads(b)
  except (ValueError,UnicodeError):continue
  summaries.append({'sha256':e['sha256'],'member':name,'type':type(d).__name__,'top_level_keys':list(d) if isinstance(d,dict) else None,'top_level_items':len(d) if hasattr(d,'__len__') else None,'status':d.get('status',d.get('verdict')) if isinstance(d,dict) else None,'scope':'data parsed; historical assertions not automatically verified'})
 entries=[]
 if any(s in PurePosixPath(name).name.lower() for s in ['manifest','sha256','bundle_sha']):
  if d is not None:
   obj=d.get('files',d) if isinstance(d,dict) else d
   if isinstance(obj,list):
    for v in obj:
     if isinstance(v,dict) and 'path' in v and 'sha256' in v:entries.append((v['path'],v['sha256'],v.get('bytes',v.get('size')),'sha256'))
     elif isinstance(v,dict) and 'path' in v and 'git_blob_sha' in v:entries.append((v['path'],v['git_blob_sha'],v.get('size'),'git_blob_sha1'))
   elif isinstance(obj,dict):
    for k,v in obj.items():
     if isinstance(v,str) and re.fullmatch('[a-f0-9]{64}',v):entries.append((k,v,None,'sha256'))
     elif isinstance(v,dict) and 'sha256' in v:entries.append((k,v['sha256'],v.get('bytes',v.get('size')),'sha256'))
  else:
   for line in b.decode(errors='replace').splitlines():
    m=re.fullmatch(r'([a-f0-9]{64})\s+[ *]?(.+)',line)
    if m:entries.append((m[2],m[1],None,'sha256'))
  if not entries:manifest_ignored.append({'member':name,'sha256':e['sha256'],'reason':'No supported hash/path entry schema; not counted as manifest validation'})
 for occ in e['occurrences']:
  h=occ['archive_sha256'];members={m['name']:m for m in G[h]['members']};base=str(PurePosixPath(occ['member']).parent)
  for rel,digest,size,algorithm in entries:
   target=posixpath.normpath(posixpath.join(base,rel));actual_member=members.get(target)
   if actual_member is None and algorithm=='git_blob_sha1':actual_member=members.get('upstream/'+rel);target='upstream/'+rel if actual_member else target
   rec={'manifest_sha256':e['sha256'],'archive_sha256':h,'manifest':occ['member'],'target':target,'expected_digest':digest,'algorithm':algorithm,'expected_size':size}
   if actual_member:
    with zipfile.ZipFile(io.BytesIO(arch(h))) as z:raw=z.read(z.infolist()[actual_member['member_index']])
    observed=hashlib.sha256(raw).hexdigest() if algorithm=='sha256' else hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
    rec.update(actual_digest=observed,actual_size=len(raw),matches_containing_archive=observed==digest and (size is None or len(raw)==size),archived_member_bytes_rehashed=True)
   else:rec.update(matches_containing_archive=False,archived_member_bytes_rehashed=False,reason='Target absent from containing archive')
   manifest.append(rec)
  if d is not None:
   def visit(v,path=''):
    if isinstance(v,dict):
     for k,val in v.items():
      if 'sha256' in k.lower():
       pairs=val.items() if isinstance(val,dict) else [(k,val)]
       for label,digest in pairs:
        if isinstance(digest,str) and re.fullmatch('[a-f0-9]{64}',digest):
         hits=[m['name'] for m in members.values() if m['sha256']==digest];refs.append({'evidence_sha256':e['sha256'],'archive_sha256':h,'member':occ['member'],'field':path+'/'+k,'label':label,'referenced_sha256':digest,'matching_archive_members':hits,'scope':'historical reference match only'})
      visit(val,path+'/'+k)
    elif isinstance(v,list):
     for k,val in enumerate(v):visit(val,path+'/'+str(k))
   if not entries:visit(d)
# Only textual import syntax scans; no AST or module loading.
imports=[]
stdlib=set(sys.stdlib_module_names)|{'__future__'};third={'numpy','scipy','sympy','networkx','pytest'}
for row,pr in zip(ROWS,P):
 text=(O/'sources'/row['sha256']).read_text();members=G[pr['archive_sha256']]['members'];directory=PurePosixPath(pr['member']).parent
 refs0=[]
 for lineno,line in enumerate(text.splitlines(),1):
  m=re.match(r'\s*from\s+([.\w]+)\s+import\s+',line)
  if m:refs0.append((lineno,m[1]))
  else:
   m=re.match(r'\s*import\s+([^#;]+)',line)
   if m:
    for a in m[1].split(','):
     name=a.strip().split()[0]
     if re.fullmatch(r'[\w.]+',name):refs0.append((lineno,name))
  for m in re.finditer(r'__import__\([\'"]([\w.]+)[\'"]\)',line):refs0.append((lineno,m[1]))
 for ln,module in refs0:
  top=module.split('.')[0]
  if top in stdlib:kind='standard_library';candidates=[]
  elif top in third:kind='third_party_environment_dependency';candidates=[]
  else:
   paths=[str(directory/(module.replace('.','/')+'.py')),str(directory.parent/(module.replace('.','/')+'.py'))]
   hits=[m for m in members if m['name'] in paths]
   if not hits:hits=[m for m in members if PurePosixPath(m['name']).name==top+'.py']
   candidates=[{'member':m['name'],'sha256':m['sha256'],'coverage_status':'fully_read_this_package' if m['sha256'] in assigned else 'accepted_additional_registry' if m['sha256'] in reviewed else 'not_in_additional_registry_or_this_assignment'} for m in hits]
   kind='archive_exact_candidate' if len({m['sha256'] for m in hits})==1 else 'ambiguous_archive_candidates' if hits else 'unresolved_local_or_external'
  imports.append({'source_sha256':row['sha256'],'source_index':row['index'],'line':ln,'module':module,'kind':kind,'candidates':candidates,'runtime_resolution_verified':False})
(O/'STORED_MANIFEST_RECONCILIATION.json').write_text(json.dumps({'entries':manifest,'unparsed_manifests':manifest_ignored,'scope':'Every listed target rehashed from containing archive; mismatches retained'},indent=2));(O/'STORED_HASH_REFERENCE_RECONCILIATION.json').write_text(json.dumps(refs,indent=2));(O/'DEPENDENCY_RECONCILIATION.json').write_text(json.dumps({'method':'Textual import scan plus exact containing-archive candidate hashes; no supplied parse/import/run','runtime_closure_verified':False,'imports':imports},indent=2));(O/'STORED_RESULT_INDEX.json').write_text(json.dumps(summaries,indent=2))
print(json.dumps({'manifest_entries':len(manifest),'manifest_matches':sum(x['matches_containing_archive'] for x in manifest),'manifest_mismatches':[x for x in manifest if not x['matches_containing_archive']],'unsupported_manifests':manifest_ignored,'hash_references':len(refs),'hash_references_absent_from_containing_archive':sum(not x['matching_archive_members'] for x in refs),'imports':len(imports),'local_unresolved':[x for x in imports if x['kind']=='unresolved_local_or_external']},indent=2))
