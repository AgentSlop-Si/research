#!/usr/bin/env python3
"""Fresh inert digest reconciliation across verified corpus; no supplied program execution."""
import pathlib,json,hashlib,re,collections,zipfile,io,gzip
P=pathlib.Path('[local workspace]');O=P/'final_review_closure_0535';M=P/'fft_research_master_20261009';H=lambda b:hashlib.sha256(b).hexdigest()
def dump(n,x):(O/n).write_text(json.dumps(x,indent=2,ensure_ascii=False)+'\n')
known=collections.defaultdict(list)
for r in json.loads((O/'ARCHIVE_MEMBER_CHECKS.json').read_text()):
 if r['hash_matches'] and r['name_matches'] and r['size_matches']:known[r['expected_sha256']].append({'kind':'archive_member','archive_sha256':r['archive_sha256'],'member':r['member'],'member_index':r['member_index'],'freshly_rehashed':True})
for r in json.loads((O/'ARCHIVE_CONTAINER_CHECKS.json').read_text()):
 if r['archive_hash_matches']:known[r['archive_sha256']].append({'kind':'archive','origin':r['origin'],'freshly_rehashed':True})
for file in ['PACKAGE_INTEGRITY_CHECKS.json','SUPPLEMENTAL_PACKAGE_INTEGRITY.json']:
 for p in json.loads((O/file).read_text()):
  for r in p['entry_checks']:
   if r['matches'] and r['size_matches']:known[r['expected_sha256']].append({'kind':'verified_review_payload','path':str(pathlib.Path(p['directory'])/r['path']),'freshly_rehashed':True})
for r in json.loads((O/'MATERIAL_IDENTITY_CHECKS.json').read_text()):
 if r['byte_snapshot_matches']:known[r['expected_sha256']].append({'kind':'material_identity','library_file_id':r['library_file_id'],'path':r['local_source'],'preservation_status':r['preservation_status'],'freshly_rehashed':True})
# Rehash the exact decompressed serialized frame words, keeping compressed identity separate.
graph=json.loads((P/'code_coverage_audit_0228/ARCHIVE_GRAPH.json').read_text());frame=next(x for x in graph if x['sha256']=='2f1a39f6c6dc377711ba2e509e9afcd2da5ba9f92e15931667cc6ee1ffd3b775');parts=frame['first_observed_at'].split('!');b=(M/parts[0]).read_bytes()
for part in parts[1:]:
 with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(part)
words=[]
with zipfile.ZipFile(io.BytesIO(b)) as z:
 for n in ['results/baseline-23/word.json.gz','results/carrier-23/word.json.gz','results/baseline-25/word.json.gz','results/carrier-25/word.json.gz']:
  g=z.read(n);raw=gzip.decompress(g);r={'kind':'decompressed_serialized_json','archive_sha256':frame['sha256'],'member':n,'gzip_sha256':H(g),'raw_json_sha256':H(raw),'gzip_bytes':len(g),'raw_json_bytes':len(raw),'freshly_rehashed':True,'word_replayed':False};words.append(r);known[H(raw)].append(r)
dump('FRESH_FRAME_WORD_IDENTITIES.json',words)
# Logical matrix digests name compact JSON values, not standalone files.
logical=[]
checks=json.loads((P/'remaining_transform_source_review_0515/FRESH_REVIEWER_CHECKS.json').read_text())
for check in checks['checks']:
 if check['check']!='synthetic_full_state_matrix_hashes':continue
 for item in check['detail']:
  fs=list((P/'remaining_transform_source_review_0515/evidence').glob('*__'+pathlib.Path(item['case']).name));assert len(fs)==1
  f=fs[0];j=json.loads(f.read_text());raw=json.dumps(j['full_state_matrix'],separators=(',',':')).encode();assert H(raw)==item['sha256']
  rec={'kind':'serialized_JSON_value','path':str(f),'file_sha256':H(f.read_bytes()),'json_field':'full_state_matrix','serialization':'compact JSON array with comma/colon separators, no newline','logical_sha256':H(raw),'freshly_rehashed':True,'circuit_replayed':False};logical.append(rec);known[H(raw)].append(rec)
dump('FRESH_LOGICAL_MATRIX_IDENTITIES.json',logical)
# Map remaining frozen master files only on demand, rehashing exact candidates.
master=collections.defaultdict(list)
for r in json.loads((P/'code_coverage_audit_0228/MASTER_FILE_HASHES.json').read_text()):master[r['sha256']].append(r['path'])
def resolve(h):
 if not known.get(h):
  for rel in master.get(h,[]):
   p=M/rel
   if p.exists() and H(p.read_bytes())==h:known[h].append({'kind':'master_standalone','path':str(p),'freshly_rehashed':True})
 return known.get(h,[])
reg=json.loads((P/'post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json').read_text());pkgs=set(r['package'] for r in reg['rows']);refs=[]
def walk(x,context,path):
 if isinstance(x,dict):
  ctx={**context,**{k:v for k,v in x.items() if k in ['manifest','archive_sha256','declaration_member','member','result','record','evidence_sha256'] and isinstance(v,str)}}
  key=next((k for k in ['expected_sha256','declared_sha256','referenced_sha256','claimed_sha256','expected'] if isinstance(x.get(k),str) and re.fullmatch('[0-9a-f]{64}',x[k])),None)
  if key is None and any(k in x for k in ['target','label','declared_path','target_reference','target_name']) and isinstance(x.get('sha256'),str) and re.fullmatch('[0-9a-f]{64}',x['sha256']):key='sha256'
  if key:
   h=x[key];locs=resolve(h);status=x.get('status',x.get('resolution_status',x.get('resolution')))
   label=next((x[k] for k in ['target_reference','declared_path','declared_name','target_name','target','label'] if k in x),None)
   if isinstance(label,str) and label.startswith(('','/workspace/scratch/')):
    direct=pathlib.Path(label)
    if direct.is_file() and H(direct.read_bytes())==h:
     known[h].append({'kind':'explicit_reference_path','path':label,'freshly_rehashed':True});locs=known[h]
   refs.append({'source_record':ctx,'json_path':path,'reference_sha256':h,'target_label':label,'original_status':status,'original_record':x,'global_verified_occurrence_count':len(locs),'verified_example':locs[0] if locs else None,'is_nonfile_fingerprint':bool(status and 'not_a_file_claim' in status),'reconciled_status':'nonfile_fingerprint_not_replayed' if status and 'not_a_file_claim' in status else 'available_logical_JSON_digest' if locs and locs[0]['kind']=='serialized_JSON_value' else 'available_exact_decompressed_content' if locs and locs[0]['kind']=='decompressed_serialized_json' else 'available_exact_bytes' if locs else 'not_found_in_verified_frozen_hash_universe','boundary':'No runtime dependency or theorem acceptance implied.'})
  for k,v in x.items():
   if isinstance(v,(dict,list)):walk(v,ctx,path+'/'+str(k))
 elif isinstance(x,list):
  for i,v in enumerate(x):walk(v,context,path+'/'+str(i))
for name in sorted(pkgs):
 for f in sorted((P/name).glob('*.json')):
  if any(s in f.name for s in ['STORED_INTEGRITY','MANIFEST_RECON','HASH_REFERENCE','CHECKSUM_RECON','MANIFEST_EXCEPTIONS','INPUT_RECEIPT_RECON']):walk(json.loads(f.read_text()),{'package':name,'review_evidence_file':str(f)},'')
# Precisely named Tensor-Weil prerequisites from its frozen v19 manifest.
tensor=[]
f=P/'coverage_audit_20261010/changed_version_text_snapshots/[private-id].sha256'
for line in f.read_text().splitlines():
 h,name=line.split('  ',1);locs=resolve(h);tensor.append({'sha256':h,'name':name,'verified_occurrence_count':len(locs),'verified_example':locs[0] if locs else None,'status':'available_exact_bytes' if locs else 'not_found_in_verified_frozen_hash_universe','main_proof_text':name in ['RESEARCH.md','CHAIN_CHECKPOINT_2026-10-10_v24.md']})
dump('TENSOR_V24_REFERENCE_CLOSURE.json',tensor)
# Retain all context records; deduplicate only the digest availability index.
groups=[]
for h in sorted(set(r['reference_sha256'] for r in refs)):
 rr=[r for r in refs if r['reference_sha256']==h];locs=resolve(h)
 groups.append({'sha256':h,'record_occurrences':len(rr),'labels':sorted(set(str(x['target_label']) for x in rr if x['target_label'] is not None)),'source_packages':sorted(set(x['source_record']['package'] for x in rr)),'nonfile_fingerprint':any(x.get('is_nonfile_fingerprint') for x in rr),'available':bool(locs),'available_as_logical_JSON_digest':bool(locs and any(x['kind']=='serialized_JSON_value' for x in locs)),'available_as_decompressed_serialized_data':bool(locs and any(x['kind']=='decompressed_serialized_json' for x in locs)),'verified_example':locs[0] if locs else None})
dump('REFERENCE_RECORD_RECONCILIATION.json',refs);dump('REFERENCE_HASH_DISPOSITIONS.json',groups)
summary={'reference_record_count':len(refs),'unique_referenced_hashes':len(groups),'available_unique_hashes':sum(x['available'] for x in groups),'unmatched_unique_hashes':sum(not x['available'] for x in groups),'unmatched_nonfile_fingerprints':sum(not x['available'] and x['nonfile_fingerprint'] for x in groups),'unresolved_file_or_external_digest_references':sum(not x['available'] and not x['nonfile_fingerprint'] for x in groups),'logical_JSON_unique_hashes':sum(x['available_as_logical_JSON_digest'] for x in groups),'decompressed_unique_hashes':sum(x['available_as_decompressed_serialized_data'] for x in groups),'tensor_v24_references':len(tensor),'tensor_v24_exact_byte_available':sum(x['status']=='available_exact_bytes' for x in tensor),'tensor_v24_not_in_verified_hash_universe':[{'name':x['name'],'sha256':x['sha256']} for x in tensor if x['status']!='available_exact_bytes'],'unmatched_scope':'Unmatched digests include historical file versions, compressed representations, external retrieved text and logical-content hashes. This number is not a missing-file count and is not all-account absence. No basename substitution was used.'}
dump('REFERENCE_RECONCILIATION_SUMMARY.json',summary);print(json.dumps(summary,indent=2));print('UNMATCHED_SUMMARY',collections.Counter(tuple(x['source_packages']) for x in groups if not x['available']))
