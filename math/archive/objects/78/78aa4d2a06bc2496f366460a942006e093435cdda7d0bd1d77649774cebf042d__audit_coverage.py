#!/usr/bin/env python3
"""Fresh metadata-only integrity and exact-hash coverage reconciliation. Never imports supplied code."""
import hashlib,json,pathlib,collections,re
P=pathlib.Path('[local workspace]'); O=P/'final_review_closure_0535'; I=P/'code_coverage_audit_0228'; R=P/'post_v22_review_registry_0308'
def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
def dump(n,x): (O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def audit_package(d):
 entries=[]; top=[]; parse_errors=[]
 for name in ['SEAL.json','SEALED_MANIFEST.json','SHA256SUMS.txt','SHA256SUMS','SEALED_MANIFEST.sha256','MANIFEST.sha256','AUDIT_MANIFEST.sha256','AUDIT_SHA256SUMS.txt']:
  f=d/name
  if not f.exists():continue
  top.append({'file':name,'sha256':digest(f),'bytes':f.stat().st_size})
  if f.suffix=='.json':
   j=json.loads(f.read_text());fs=j.get('files',{})
   if isinstance(fs,dict):
    for k,v in fs.items():
     if isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v):entries.append((name,k,v,None))
     elif isinstance(v,dict) and 'sha256' in v:entries.append((name,k,v['sha256'],v.get('bytes',v.get('size_bytes'))))
   elif isinstance(fs,list):
    for e in fs:
     if isinstance(e,dict) and 'sha256' in e: entries.append((name,e.get('path',e.get('file')),e['sha256'],e.get('bytes',e.get('size_bytes'))))
   # Common seal links to its checksum list.
   for key in ['sha256sums_sha256','checksums_sha256','manifest_sha256','payload_manifest_sha256','checksum_list_sha256','SHA256SUMS.txt','SEALED_MANIFEST.json']:
    if key not in j:continue
    target=key if key in ['SHA256SUMS.txt','SEALED_MANIFEST.json'] else j.get('manifest',j.get('manifest_file',j.get('checksum_list','SHA256SUMS.txt')))
    if key=='manifest_sha256' and not any(t in j for t in ['manifest','manifest_file','checksum_list']) and (d/'SEALED_MANIFEST.json').exists():target='SEALED_MANIFEST.json'
    if key=='payload_manifest_sha256' and isinstance(fs,list):
     encoded=''.join(f"{r['sha256']}  {r['path']}\n" for r in fs).encode()
     reconstructed=hashlib.sha256(encoded).hexdigest()
     if reconstructed==j[key]:
      top.append({'reconstructed_from':name+'/files','sha256':reconstructed,'matches_declared_payload_manifest':True,'encoding':'sha256, two spaces, relative path, newline, in listed order'})
      continue
    if isinstance(target,str) and (d/target).exists():entries.append((name,target,j[key],None))
  else:
   for line in f.read_text().splitlines():
    if not line.strip():continue
    m=re.match(r'^([0-9a-fA-F]{64})\s+[ *]?(.+)$',line)
    if not m:parse_errors.append({'manifest':name,'line':line});continue
    entries.append((name,m[2],m[1].lower(),None))
 out=[]; byhash=collections.defaultdict(list)
 for manifest,name,sha,size in entries:
  f=d/name;exists=f.is_file();actual=digest(f) if exists else None
  rec={'manifest':manifest,'path':name,'expected_sha256':sha,'actual_sha256':actual,'exists':exists,'matches':actual==sha,'expected_bytes':size,'actual_bytes':f.stat().st_size if exists else None}
  rec['size_matches']=size is None or rec['actual_bytes']==size
  out.append(rec)
  if actual==sha and rec['size_matches']:byhash[sha].append(name)
 return {'directory':str(d),'seal_files':top,'entry_checks':out,'parse_errors':parse_errors,'entry_count':len(out),'unique_payload_paths':len({e['path'] for e in out}),'all_entry_hashes_match':all(x['matches'] and x['size_matches'] for x in out) and not parse_errors},byhash
raw=(R/'ADDITIVE_CODE_COVERAGE.json').read_bytes();reg=json.loads(raw);dump('REGISTRY_SNAPSHOT.json',reg)
inv=json.loads((I/'CODE_COVERAGE_INVENTORY.json').read_text());invmap={x['sha256']:x for x in inv};program={x['sha256'] for x in inv if x['coverage_status']!='non_program_build_metadata'};baseline={x['sha256'] for x in inv if x['static_inspection_complete']};new=[x['sha256'] for x in reg['rows']];templates=[x['sha256'] for x in reg.get('semantic_template_rows',[])];complete=baseline|set(new)|set(templates)
pkgs=collections.defaultdict(list)
for row in reg['rows']+reg.get('semantic_template_rows',[]):pkgs[row['package']].append(row)
checks=[];rowchecks=[]
for name,rows in pkgs.items():
 check,bh=audit_package(P/name);checks.append(check)
 for row in rows:
  h=row['sha256'];e=row['evidence_sha256'];evidence=bh.get(e,[])
  evidence_contains=any(h in ((P/name/f).read_text(errors='replace')) for f in evidence)
  rowchecks.append({'sha256':h,'package':name,'evidence_sha256':e,'evidence_verified_paths':evidence,'source_verified_snapshot_paths':bh.get(h,[]),'evidence_contains_exact_hash':evidence_contains,'in_frozen_program_universe':h in program,'source_executed_in_review':row.get('source_executed_in_review'),'class':'template' if row in reg.get('semantic_template_rows',[]) else 'full_read'})
basecheck,_=audit_package(I);checks.append(basecheck)
bytescheck=[]
for row in inv:
 f=pathlib.Path(row['local_content']); exists=f.exists();h=digest(f) if exists else None
 bytescheck.append({'sha256':row['sha256'],'bytes':row['size_bytes'],'observed_bytes':f.stat().st_size if exists else None,'matches':h==row['sha256'] and f.stat().st_size==row['size_bytes'] if exists else False})
evs=json.loads((I/'COVERAGE_EVIDENCE.json').read_text());baseev=[]
for h in sorted(baseline):
 relevant=[e for e in evs if e['code_sha256']==h and e['kind'] in ['uploaded_static_full','generated_static_full']]
 # Retain all kinds so any variant is visible rather than silently asserted.
 if not relevant:relevant=[e for e in evs if e['code_sha256']==h]
 found=[]
 for e in relevant:
  f=I/e['portable_document'] if e.get('portable_document') else P/'fft_research_master_20261009'/e['document'];actual=digest(f) if f.exists() else None
  found.append({'id':e['id'],'kind':e['kind'],'path':str(f),'document_hash_matches':actual==e['document_sha256'],'scope':e.get('scope'),'record':e.get('quote_or_record')})
 baseev.append({'sha256':h,'evidence':found})
summary={'registry_sha256':hashlib.sha256(raw).hexdigest(),'inventory_sha256':digest(I/'CODE_COVERAGE_INVENTORY.json'),'frozen_candidate_hashes':len(inv),'frozen_program_hashes':len(program),'excluded_build_metadata_hashes':sorted(set(invmap)-program),'baseline_full_read_hashes':len(baseline),'additive_full_read_rows':len(new),'additive_full_read_unique_hashes':len(set(new)),'full_read_unique_hashes':len(baseline|set(new)),'complete_template_unique_hashes':len(set(templates)),'complete_static_inspection_unique_hashes':len(complete),'remaining_program_hashes':len(program-complete),'registry_full_read_count_agrees':reg['current_full_static_reads']==len(baseline|set(new)),'registry_complete_count_agrees':reg['current_complete_static_inspections']==len(complete),'duplicate_additive_hashes':sorted(h for h,n in collections.Counter(new).items() if n>1),'baseline_additive_overlap':sorted(baseline&set(new)),'template_literal_overlap':sorted((baseline|set(new))&set(templates)),'outside_program_universe':sorted(complete-program),'packages_checked':len(pkgs),'all_cached_inventory_bytes_match':all(x['matches'] for x in bytescheck),'all_package_entry_hashes_match':all(x['all_entry_hashes_match'] for x in checks),'all_additive_evidence_bound_to_source':all(x['evidence_contains_exact_hash'] and x['source_verified_snapshot_paths'] for x in rowchecks),'source_programs_executed_imported_compiled_or_ast_parsed_by_this_audit':False,'meaning':'Integrity and declared exact-hash full-static-read coverage, not independent repetition of all earlier source reviews or a correctness theorem.'}
dump('COVERAGE_AUDIT.json',summary);dump('PACKAGE_INTEGRITY_CHECKS.json',checks);dump('ADDITIVE_ROW_PROVENANCE.json',rowchecks);dump('BASELINE_READ_EVIDENCE.json',baseev);dump('FROZEN_SOURCE_BYTE_CHECKS.json',bytescheck);dump('REMAINING_SOURCE_HASHES.json',[{'sha256':h,'names':invmap[h]['names'],'representative_path':invmap[h]['representative_path']} for h in sorted(program-complete)])
print(json.dumps(summary,indent=2));print('PACKAGE_ERRORS',json.dumps([{'directory':x['directory'],'errors':[e for e in x['entry_checks'] if not e['matches'] or not e['size_matches']],'parse_errors':x['parse_errors']} for x in checks if not x['all_entry_hashes_match']],indent=2));print('ROW_ERRORS',json.dumps([x for x in rowchecks if not x['evidence_contains_exact_hash'] or not x['source_verified_snapshot_paths']],indent=2))
