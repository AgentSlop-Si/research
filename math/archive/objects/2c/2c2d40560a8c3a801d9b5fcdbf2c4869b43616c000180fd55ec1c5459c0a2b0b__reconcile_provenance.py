"""Fresh audit-only inert ZIP/JSON reconciliation. Does not load supplied modules."""
import io,json,pathlib,hashlib,zipfile,shutil,posixpath,re,collections
P=pathlib.Path(__file__).parent
A=pathlib.Path('code_coverage_audit_0228')
M=pathlib.Path('fft_research_master_20261009')
rows=json.loads((P/'SOURCE_MANIFEST.json').read_text())
inv=json.loads((P/'INVENTORY_SNAPSHOT.json').read_text())
byhash={r['sha256']:r for r in inv}
roots=json.loads((A/'ARCHIVE_ROOTS.json').read_text())
graph={r['sha256']:r for r in json.loads((A/'ARCHIVE_GRAPH.json').read_text())}
registry=json.loads((P/'REGISTRY_BEFORE.json').read_text())
covered={r['sha256'] for r in inv if r.get('static_inspection_complete')}|{r['sha256'] for r in registry['rows']}
assigned={r['sha256'] for r in rows}
H=lambda b:hashlib.sha256(b).hexdigest()
def save(name,data):
 p=P/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,indent=2)+'\n')
def resolve(h):
 for rt in roots:
  if rt['sha256']!=h:continue
  path=pathlib.Path(rt['path']);path=path if path.is_absolute() else M/path
  if path.is_file():
   b=path.read_bytes()
   if H(b)==h:return b,{'kind':'root_path','path':str(path),'root_record':rt}
 parts=graph[h]['first_observed_at'].split('!')
 path=M/parts[0];b=path.read_bytes();chain=[{'path':str(path),'sha256':H(b)}]
 for name in parts[1:]:
  with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(name)
  chain.append({'member_name':name,'sha256':H(b)})
 assert H(b)==h
 return b,{'kind':'archive_chain','chain':chain}
ars=sorted({o['archive_sha256'] for r in rows for o in r['occurrences'] if o['kind']=='archive_member'})
archive_checks=[];archives={};source_occ=[];outrows=[];dep_rows=[]
for h in ars:
 b,origin=resolve(h)
 dest=P/'provenance'/'archives'/f'{h}.zip';dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
 z=zipfile.ZipFile(io.BytesIO(b)); archives[h]=z
 archive_checks.append({'sha256':h,'size_bytes':len(b),'snapshot':str(dest.relative_to(P)),'verified_against_inventory':True,'resolved_from':origin,'member_count':len(z.infolist())})
 names=[i.filename for i in z.infolist()]
 requested=[(r,o) for r in rows for o in r['occurrences'] if o.get('archive_sha256')==h]
 dirs=set()
 for r,o in requested:
  info=z.infolist()[o['member_index']]
  assert info.filename==o['name']
  data=z.read(info);assert H(data)==r['sha256'] and len(data)==r['size_bytes']
  source_occ.append({'source_index':r['index'],'sha256':r['sha256'],'archive_sha256':h,'member_index':o['member_index'],'member_name':o['name'],'hash_size_and_exact_member_index_verified':True})
  d=posixpath.dirname(o['name'])
  dirs.add(d)
  if posixpath.basename(d)=='tests':dirs.add(posixpath.dirname(d))
 # Select static data immediately beside assigned programs or in results/verification, not nested archives.
 for mi,info in enumerate(z.infolist()):
  name=info.filename;d=posixpath.dirname(name);ext=posixpath.splitext(name)[1].lower()
  if info.is_dir() or ext not in ('.json','.txt','.log','.md'):continue
  if d not in dirs and not any(d in (q+'/results',q+'/verification') for q in dirs):continue
  b=z.read(info);oh=H(b)
  dest=P/'provenance'/'stored_outputs'/oh;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(b)
  rr={'archive_sha256':h,'member_index':mi,'member_name':name,'sha256':oh,'size_bytes':len(b),'snapshot':str(dest.relative_to(P)),'evidence_status':'Archived data, not generated or executed in current review'}
  if ext=='.json':
   try:
    obj=json.loads(b);rr['json_kind']=type(obj).__name__
    if isinstance(obj,dict):
     rr['top_level_keys']=list(obj)
     rr['status_fields']={k:v for k,v in obj.items() if k in ('status','scope','statement','verdict','note','interpretation','proof_status','claim','not_a_sub_nlogn_fft','not_a_sub_nlogn_FFT')}
     rr['simple_top_level_counts']={k:v for k,v in obj.items() if isinstance(v,(int,float,bool))}
   except Exception as ex:rr['json_parse_error']=str(ex)
  if ext in ('.txt','.log'):
   txt=b.decode('utf8',errors='replace')
   rr['test_summary_lines']=[s for s in txt.splitlines() if re.search(r'Ran \d+ tests?|^OK\b|^FAILED\b|PASS|SKIPPED|FAIL',s)][:25]
  outrows.append(rr)
for r in rows:
 review=json.loads((P/'per_hash'/f"{r['sha256']}.json").read_text())
 occurrences=[x for x in source_occ if x['sha256']==r['sha256']]
 dependencies=[]
 for ref in r.get('import_references',[]):
  mods=[ref['module']] if ref.get('module') else ref.get('names',[])
  for mod in mods:
   simple=mod.split('.')[0];candidate={}
   for o in r['occurrences']:
    if o['kind']!='archive_member':continue
    h=o['archive_sha256'];z=archives[h]
    current=posixpath.dirname(o['name']);rootdir=o['name'].split('/')[0]
    for gi in graph[h]['members']:
     if gi.get('is_code') and (posixpath.basename(gi['name'])==simple+'.py' or gi['name'].endswith('/'+simple+'/__init__.py')):
      ch=gi['sha256'];candidate[(h,gi['name'])]={'sha256':ch,'archive_sha256':h,'member_name':gi['name'],'same_directory':posixpath.dirname(gi['name'])==current,'reviewed_in_this_assignment':ch in assigned,'prior_full_static_review':ch in covered,'full_static_review_evidence':byhash.get(ch,{}).get('coverage_status') if ch in covered else None}
   dependencies.append({'module':mod,'candidates':list(candidate.values()),'resolution':'Static archive candidate mapping only; runtime sys.path/import closure not validated' if candidate else 'External standard/third-party module or unresolved import; not imported during review'})
 review['archive_occurrence_verification']=occurrences
 review['dependency_reconciliation']=dependencies
 related=[]
 for o in r['occurrences']:
  if o['kind']!='archive_member':continue
  parent=posixpath.dirname(o['name']); parent=posixpath.dirname(parent) if posixpath.basename(parent)=='tests' else parent
  related.extend({'sha256':x['sha256'],'archive_sha256':x['archive_sha256'],'member_name':x['member_name'],'snapshot':x['snapshot']} for x in outrows if x['archive_sha256']==o['archive_sha256'] and (posixpath.dirname(x['member_name'])==parent or posixpath.dirname(x['member_name']) in (parent+'/results',parent+'/verification')))
 review['stored_output_reconciliation']={'archived_related_records':related,'current_run_status':'Not regenerated; historical outputs/logs do not establish current execution or all-claim validity'}
 save('per_hash/'+r['sha256']+'.json',review)
 dep_rows.append({'index':r['index'],'sha256':r['sha256'],'dependencies':dependencies})
save('ARCHIVE_PROVENANCE.json',archive_checks)
save('SOURCE_OCCURRENCE_CHECKS.json',source_occ)
save('STORED_OUTPUTS_INDEX.json',outrows)
save('DEPENDENCY_RECONCILIATION.json',dep_rows)
save('provenance/ARCHIVE_GRAPH_SUBSET.json',[graph[h] for h in ars])
save('provenance/ARCHIVE_ROOTS_SUBSET.json',[x for x in roots if x['sha256'] in ars])
for name in ['SEAL.json','SHA256SUMS.txt','INPUT_SNAPSHOT.json']:
 shutil.copyfile(A/name,P/'provenance'/('ORIGINAL_INVENTORY_'+name))
print(json.dumps({'archives_verified':len(archive_checks),'source_occurrences_verified':len(source_occ),'stored_documents_snapshotted':len(outrows),'reports_augmented':len(rows),'stored_status_summary':collections.Counter(str(x.get('status_fields',{}).get('status')) for x in outrows if x.get('status_fields',{}).get('status') is not None)}))
