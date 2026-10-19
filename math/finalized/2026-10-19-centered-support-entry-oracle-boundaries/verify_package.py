"""Verify the publication projection without importing or running scientific programs."""
from pathlib import Path
import base64, gzip, hashlib, json, re, sys
FROZEN={'sets': [{'public_prefix': 'alg034/candidate', 'source_package': 'alg034_centered_support_obstruction_20261019_1527', 'manifest_path': 'alg034/candidate/MANIFEST.json', 'manifest_sha256': '30b228192c017fcf49c35df56dd19fe52dfe49dd6a27dec4731e21fce4f3e2a4', 'manifest_bytes': 1997, 'manifest_entries': 21, 'extra_bound_files': ['SEAL.json'], 'private_administrative_omissions': 2, 'scientific_files_complete': True, 'entire_original_packet_publicly_recoverable': False}, {'public_prefix': 'alg034/review', 'source_package': 'alg034_support_independent_review_20261019_1535', 'manifest_path': 'alg034/review/MANIFEST.json', 'manifest_sha256': '0b22a8eb283d3e82a13324fd212251275808fd86983c30512a5d699a09bb2333', 'manifest_bytes': 1362, 'manifest_entries': 14, 'extra_bound_files': ['SEAL.json'], 'private_administrative_omissions': 1, 'scientific_files_complete': True, 'entire_original_packet_publicly_recoverable': False}, {'public_prefix': 'c13/candidate', 'source_package': 'c13_entry_oracle_integration_20261019_1525', 'manifest_path': 'c13/candidate/MANIFEST.json', 'manifest_sha256': '4a482ce24330b5083b7aab921ab0ee1516aa940addffc3b80ee5f62e44ce750b', 'manifest_bytes': 2699, 'manifest_entries': 17, 'extra_bound_files': ['SEAL.sha256'], 'private_administrative_omissions': 6, 'scientific_files_complete': True, 'entire_original_packet_publicly_recoverable': False}, {'public_prefix': 'c13/review', 'source_package': 'c13_entry_oracle_independent_review_20261019_1539', 'manifest_path': 'c13/review/MANIFEST.json', 'manifest_sha256': '6f30c7f097d1979b6a9a07a2c6c912ba33e1a2348628e66a980e07fc5da1f636', 'manifest_bytes': 2229, 'manifest_entries': 14, 'extra_bound_files': ['SEAL.sha256'], 'private_administrative_omissions': 0, 'scientific_files_complete': True, 'entire_original_packet_publicly_recoverable': True}], 'allowed_omissions': ['alg034/candidate/SOURCE_BINDINGS.json', 'alg034/candidate/sources/OWNER_RECORD.json', 'alg034/review/order_probe/SOURCE_BINDINGS.json', 'c13/candidate/SOURCE_BINDINGS.json', 'c13/candidate/sources/c13_catalogue.json', 'c13/candidate/sources/c13_overview.json', 'c13/candidate/sources/index_selected_records.json', 'c13/candidate/sources/triage_disposition.md', 'c13/candidate/sources/triage_source_bindings.json'], 'c13': {'final_verdict_received': True, 'directory_name': 'c13_entry_oracle_independent_review_20261019_1539', 'manifest_sha256': '6f30c7f097d1979b6a9a07a2c6c912ba33e1a2348628e66a980e07fc5da1f636', 'verdict': 'ACCEPT_SCOPED_CLASSICAL_ENTRY_ORACLE_COSTING_AND_HAMILTONIAN_ADAPTER', 'verdict_file': 'DISPOSITION.json', 'verdict_key': 'verdict', 'candidate_manifest_key': 'candidate_manifest_sha256', 'private_administrative_omissions': {}}}
# Encoded vocabulary lets the verifier scan its own source without false self-matches.
PRIVACY_PATTERN=b'dGhyZWFkX2lkfG1lc3NhZ2VfaWR8ZmlsZV9pZHxkb2N1bWVudF9pZHxzcHJlYWRzaGVldF9pZHxkb2NzXC5nb29nbGVcLmNvbXxjaGF0Z3B0XC5jb218L3Jvb3QvfFswLTlhLWZdezh9LVswLTlhLWZdezR9LVswLTlhLWZdezR9LVswLTlhLWZdezR9LVswLTlhLWZdezEyfQ=='

def require(v,msg):
 if not v:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def info(b):return {'bytes':len(b),'sha256':sha(b)}
def safe(root,n):
 p=Path(n);require(p.parts and not p.is_absolute() and '..' not in p.parts,'Unsafe relative path')
 q=root/p;require(not any(x.is_symlink() for x in [q,*q.parents] if x!=root.parent),'Symlink in payload path')
 require(root.resolve() in q.resolve().parents,'Path escapes package')
 return q
def rows(obj):
 if 'files' in obj:return obj['files']
 require(all(isinstance(v,str) and len(v)==64 for v in obj.values()),'Unknown manifest format')
 return [{'path':k,'sha256':v} for k,v in obj.items()]
def decode(b,kind):
 if kind=='EXACT_COPY':return b
 require(kind=='GZIP_BASE64','Invalid representation')
 packed=base64.b64decode(b''.join(b.split()),validate=True)
 require(packed[:3]==b'\x1f\x8b\x08' and packed[4:8]==b'\0\0\0\0','Non-deterministic gzip header')
 raw=gzip.decompress(packed)
 require(base64.encodebytes(gzip.compress(raw,compresslevel=9,mtime=0))==b,'Non-canonical lossless encoding')
 return raw

def verify(root):
 root=Path(root).resolve()
 def read(n):return safe(root,n).read_bytes()
 def js(n):return json.loads(read(n))
 seal=js('SEAL.json');mb=read('MANIFEST.json');m=json.loads(mb)
 require(info(mb)==seal['manifest'],'Package manifest/seal mismatch')
 declared=m['files'];require(len(declared)==len({r['path'] for r in declared}),'Duplicate manifest entry')
 expected={r['path'] for r in declared}|{'MANIFEST.json','SEAL.json'}
 actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
 require(actual==expected,'Missing or unlisted public file')
 require(not any(p.is_symlink() for p in root.rglob('*')),'Symlink in public tree')
 allow=js('PRESERVATION_ALLOWLIST.json')['public_paths']
 require(len(allow)==len(set(allow)) and set(allow)==expected,'Publication allowlist mismatch')
 pattern=re.compile(base64.b64decode(PRIVACY_PATTERN),re.I)
 for r in declared:
  b=read(r['path']);require(info(b)=={k:r[k] for k in ('bytes','sha256')},'Stored-file mismatch: '+r['path'])
  require(not pattern.search(b),'Private identifier in public file: '+r['path'])
 ledger=js('SOURCE_LEDGER.json');files=ledger['exact_public_sources'];omitted=ledger['administrative_omissions'];sets=ledger['source_sets']
 require(sets==FROZEN['sets'],'Frozen source-set identity changed')
 require(len(files)==len({r['logical_path'] for r in files})==len({r['public_path'] for r in files}),'Duplicate exact source correspondence')
 require(len(omitted)==len({r['logical_path'] for r in omitted}),'Duplicate omission')
 require({r['logical_path'] for r in omitted}==set(FROZEN['allowed_omissions']),'Administrative omission set changed')
 require(ledger['scientific_files_complete'] is True and ledger['entire_original_packets_publicly_recoverable'] is False,'Scientific/public-coverage distinction changed')
 payload={};file_index={};omit_index={r['logical_path']:r for r in omitted}
 for r in files:
  raw=read(r['public_path']);require(info(raw)=={'bytes':r['public_bytes'],'sha256':r['public_sha256']},'Transport identity mismatch')
  b=decode(raw,r['representation'])
  require(info(b)=={'bytes':r['source_bytes'],'sha256':r['source_sha256']},'Original-source identity mismatch')
  require(not pattern.search(b),'Private identifier in decoded original')
  require((len(b)>2_000_000)==(r['representation']=='GZIP_BASE64'),'Large-source transport rule changed')
  require(r['logical_path'] not in omit_index,'Omitted original also published')
  payload[r['logical_path']]=b;file_index[r['logical_path']]=r
 for r in omitted:
  require(r['category']=='PRIVATE_ADMINISTRATIVE_EVIDENCE' and r['scientific_payload'] is False and r['original_preserved_locally'] is True,'Invalid omission classification')
  require(not (root/r['logical_path']).exists(),'Private original present in public tree')
 count=0
 for s in sets:
  raw=payload[s['manifest_path']];require(info(raw)=={'bytes':s['manifest_bytes'],'sha256':s['manifest_sha256']},'Original manifest mismatch')
  dr=rows(json.loads(raw));require(len(dr)==s['manifest_entries'] and len(dr)==len({r['path'] for r in dr}),'Source manifest cardinality mismatch')
  required={s['public_prefix']+'/'+r['path'] for r in dr}|{s['manifest_path']}|{s['public_prefix']+'/'+n for n in s['extra_bound_files']}
  actual_source={n for n,r in file_index.items() if r['source_package']==s['source_package']}|{n for n,r in omit_index.items() if r['source_package']==s['source_package']}
  require(required==actual_source,'Source-set coverage mismatch')
  for r in dr:
   logical=s['public_prefix']+'/'+r['path'];bound=file_index.get(logical,omit_index.get(logical))
   require(bound is not None,'Undeclared source omission')
   require(bound['source_sha256']==r['sha256'],'Original-manifest member hash mismatch')
   if 'bytes' in r:require(bound['source_bytes']==r['bytes'],'Original-manifest member length mismatch')
   require(bound['source_manifest_sha256']==s['manifest_sha256'] and bound['source_relative_path']==r['path'],'Source correspondence mismatch')
  for n in ('SEAL.json','SEAL.sha256'):
   logical=s['public_prefix']+'/'+n
   if logical in payload:
    if n=='SEAL.sha256':require(payload[logical].decode().split()[0]==s['manifest_sha256'],'Original SHA seal mismatch')
    else:
     sv=json.loads(payload[logical])
     if 'manifest_sha256' in sv:require(sv['manifest_sha256']==s['manifest_sha256'],'Original JSON seal mismatch')
  count+=len(dr)
 restoration=js('RESTORATION_LEDGER.json');rr=restoration['files']
 require(restoration['threshold_bytes']==2_000_000 and restoration['private_administrative_files_restorable_from_public'] is False and restoration['public_projections_are_originals'] is False,'Restoration boundary changed')
 require(len(rr)==len(files) and {r['logical_path'] for r in rr}==set(payload),'Incomplete restoration ledger')
 for r in rr:
  s=file_index[r['logical_path']]
  require(r=={'logical_path':s['logical_path'],'public_path':s['public_path'],'representation':s['representation'],'restored_bytes':s['source_bytes'],'restored_sha256':s['source_sha256'],'transport_bytes':s['public_bytes'],'transport_sha256':s['public_sha256']},'Restoration binding mismatch')
 privacy=js('PRIVACY_LEDGER.json');proj=js('PROJECTION_DISCLOSURE.json')
 require(privacy['administrative_omissions']==omitted,'Privacy/source omission discrepancy')
 require(privacy['private_administrative_content_published'] is False and privacy['private_identifiers_published'] is False,'Private content boundary changed')
 require(proj['scientific_files_projected']==0 and proj['original_manifests_rewritten'] is False and proj['scientific_proof_code_test_or_review_rewritten'] is False,'Scientific projection forbidden')
 require(proj['files']==privacy['administrative_projections'],'Projection ledgers differ')
 want={'alg034/candidate/SOURCE_BINDINGS.json','alg034/review/order_probe/SOURCE_BINDINGS.json','c13/candidate/SOURCE_BINDINGS.json'}
 require(len(proj['files'])==3 and {r['original_logical_path'] for r in proj['files']}==want,'Administrative projection set changed')
 for r in proj['files']:
  old=omit_index[r['original_logical_path']]
  require(r['original_source_sha256']==old['source_sha256'] and r['original_source_bytes']==old['source_bytes'],'Projection original binding mismatch')
  require(r['projection_kind']=='ADMINISTRATIVE_METADATA_ONLY' and r['scientific_text_edited'] is False,'Scientific file was projected')
  b=read(r['public_path']);require(info(b)=={'bytes':r['public_bytes'],'sha256':r['public_sha256']},'Projection byte identity mismatch')
  p=json.loads(b);require(p['original_source_sha256']==old['source_sha256'],'Projection falsely identifies original')
  retained=p['retained_metadata']
  if r['original_logical_path'].startswith('alg034/'):
   require(len(retained['bindings'])==11,'Scientific binding projection incomplete')
   for v in retained['bindings']:require(sha(payload['alg034/candidate/'+v['snapshot']])==v['sha256'],'Scientific projected binding mismatch')
  else:
   require(len(retained['scientific_sources'])==1,'C13 scientific citation missing')
   v=retained['scientific_sources'][0]
   require(sha(payload['c13/candidate/'+v['path']])==v['sha256'],'C13 scientific review identity mismatch')
   require(len(retained['administrative_sources'])==5,'C13 administrative projection incomplete')
   for v in retained['administrative_sources']:
    old=omit_index['c13/candidate/'+v['path']]
    require(v['sha256']==old['source_sha256'] and v['bytes']==old['source_bytes'] and v['public_content_omitted'] is True,'C13 omission projection mismatch')
 reference=js('SOURCE_REFERENCE_MAP.json')
 require(reference['files']==[{'source_package':r['source_package'],'source_relative_path':r['source_relative_path'],'logical_path':r['logical_path'],'public_path':r['public_path'],'sha256':r['source_sha256']} for r in files],'Source reference map changed')
 require(reference['original_source_paths_rewritten'] is False and reference['recursive_historical_dependencies_republished'] is False,'Reference scope changed')
 accept=js('FINAL_ACCEPTANCE.json');require(set(accept['results'])=={'alg034','c13'},'Acceptance set changed')
 for key,a in accept['results'].items():
  for field in ('candidate_manifest','review_manifest','proof','review','verdict'):
   r=a[field];require(r['logical_path'] in payload,'Acceptance evidence missing')
   require(info(payload[r['logical_path']])=={'bytes':r['source_bytes'],'sha256':r['source_sha256']},'Acceptance evidence identity mismatch')
   require(r['public_path']==file_index[r['logical_path']]['public_path'],'Acceptance storage mismatch')
 av=json.loads(payload['alg034/review/SEAL.json'])
 require(av['status']==accept['results']['alg034']['verdict_status']=='PASS_SCOPED_CENTERED_OUTPUT_SUPPORT_OBSTRUCTION','ALG034 verdict mismatch')
 require(av['author_manifest_sha256']==accept['results']['alg034']['candidate_manifest']['source_sha256'],'ALG034 verdict author mismatch')
 cv=json.loads(payload['c13/review/'+FROZEN['c13']['verdict_file']])
 require(cv[FROZEN['c13']['verdict_key']]==accept['results']['c13']['verdict_status']==FROZEN['c13']['verdict'],'C13 verdict mismatch')
 require(cv[FROZEN['c13']['candidate_manifest_key']]==accept['results']['c13']['candidate_manifest']['source_sha256'],'C13 verdict author mismatch')
 require(accept['packaging_independent_review']=='PENDING' and accept['external_publication']=='NOT_PERFORMED' and accept['publication_authorized_by_this_packet'] is False,'Publication gate changed')
 ch=json.loads(payload['c13/review/SOURCE_HASHES.json'])
 require(ch['candidate_manifest_sha256']==sha(payload['c13/candidate/MANIFEST.json']) and ch['candidate_files']==rows(json.loads(payload['c13/candidate/MANIFEST.json'])),'C13 complete original hash receipt changed')
 for name in ('RESULTS.json','adapter.py','check.py','example.py'):
  require(payload['c13/review/replay/'+name]==payload['c13/candidate/'+name],'C13 review replay source differs')
 scope=js('CLAIM_SCOPE.json');a=scope['alg034'];c=scope['c13']
 require(a['support_lower_bounds']=={'R*M^(-1/4)':'sqrt(M)/16','4*R*M^(-1/4)':'sqrt(M)/256'},'Centered support contract changed')
 for k in ('general_fourier_lower_bound','heavy_coordinate_recovery_algorithm','new_general_supplier','successful_comb_provider','full_comb_outer_execution','accepted_bv_supplier_changed','all_length_larger_support_allowance_contradicted'):require(a[k] is False,'ALG034 scope overclaim: '+k)
 require(c['invertible_target_promise']=='The same bound for invertible feasible targets over fields with more than two elements.','C13 field qualification changed')
 require(c['randomized_expected_query_lower_bound']=='(1-2*epsilon)*(N^2-|supp(U) union supp(V)|) for error epsilon<1/2 on every input.','C13 randomized query scope changed')
 require(c['adapter_upper_bound']=='At most 4N^2 target calls and 12N^2 sandwich field operations; O(N) supported graph field work; O(N^2) explicit root comparisons; O(N) auxiliary storage without tracing.','C13 cost contract changed')
 require(c['deterministic_distinct_query_lower_bound']=='N^2-|supp(U) union supp(V)| on each feasible target.','Frozen C13 query bound upgraded')
 require(c['nonzero_edge_family']=='Over Q, U=I-2P, V=I-3P, B=U^-1+V^-1, N>=3: N^2-2N queries.','C13 family scope changed')
 for k in ('implicit_fourier_formula_lower_bound','quantum_or_vector_oracle_lower_bound','general_direction_discovery_completed','singular_masks_completed','historical_priority_established','original_endpoint_value_contract_completed','new_iff_theorem_claim'):require(c[k] is False,'C13 scope overclaim: '+k)
 require(scope['broad_owner_closures']==0 and scope['scientific_programs_rerun_during_packaging'] is False and scope['general_fft_improvement_claim'] is False and scope['historical_novelty_claim'] is False,'Global overclaim')
 require(c['reviewer_only_refinement_independently_accepted'] is False and c['main_acceptance_includes_reviewer_only_refinement'] is False,'Unreviewed reviewer refinement promoted')
 owners=js('OWNER_DISPOSITIONS.json')
 require(owners['owner_closures']==0 and owners['canonical_records_modified'] is False and owners['status_changes']==0 and owners['priority_changes']==0 and owners['scores_changed'] is False and owners['discovery_count_change']==0,'Owner records changed')
 require(set(owners['owners'])=={'ALG-034','C13-FIXED-DIRECTIONS'} and all(v['whole_owner_closed'] is False for v in owners['owners'].values()),'Broad owner closed')
 preservation=js('ACCEPTED_RESULT_PRESERVATION.json')
 require(preservation['owners']==owners['owners'] and preservation['prior_acceptances_reopened'] is False and preservation['accepted_bv_source_modified'] is False and preservation['accepted_c13_theorem_reproved_or_relabelled_new'] is False and preservation['classical_attribution_retained'] is True,'Prior acceptance changed')
 return {'status':'PASS','public_files':len(actual),'source_sets':len(sets),'source_manifest_entries':count,'exact_public_source_files':len(files),'administrative_omissions':len(omitted),'administrative_projections':len(proj['files']),'lossless_encoded_files':sum(r['representation']=='GZIP_BASE64' for r in files),'scientific_programs_executed':False,'external_writes':False}

if __name__=='__main__':
 try:print(json.dumps(verify(Path(sys.argv[1]) if len(sys.argv)>1 else Path(__file__).resolve().parent),indent=2))
 except Exception as exc:
  print(json.dumps({'status':'FAIL','reason':str(exc)}),file=sys.stderr);raise SystemExit(1)
