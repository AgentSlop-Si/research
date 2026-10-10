"""Fresh inert source/data-reference reconciliation; no supplied-code evaluation."""
from pathlib import Path
import json,hashlib,zipfile,posixpath,re,gzip,collections
P=Path(__file__).parent
rows=json.loads((P/'SOURCE_MANIFEST.json').read_text());registry=json.loads((P/'REGISTRY_BEFORE.json').read_text());prior={r['sha256']:r for r in registry['rows']};assigned={r['sha256']for r in rows};graph={r['sha256']:r for r in json.loads((P/'provenance/ARCHIVE_GRAPH_SUBSET.json').read_text())};ars=json.loads((P/'ARCHIVE_PROVENANCE.json').read_text());zs={r['sha256']:zipfile.ZipFile(P/r['snapshot'])for r in ars};outs=json.loads((P/'STORED_OUTPUTS_INDEX.json').read_text())
def H(b):return hashlib.sha256(b).hexdigest()
def save(name,x):(P/name).write_text(json.dumps(x,indent=2)+'\n')
refs=[];standalone=[];deps=[]
filepat=re.compile(r'''["']([^"'\n]+\.(?:py|hpp|cpp|c|so|dylib|dll|json|json\.gz|uses|bin))["']''')
for row in rows:
 text=(P/'sources'/row['sha256']).read_text();review=json.loads((P/'per_hash'/f"{row['sha256']}.json").read_text());imports=[]
 for ref in row.get('import_references',[]):
  for module in ([ref['module']]if ref.get('module')else ref.get('names',[])):
   suffix=module.replace('.','/')+'.py';package=module.replace('.','/')+'/__init__.py';candidates=[]
   for o in row['occurrences']:
    if o['kind']!='archive_member':continue
    for m in graph[o['archive_sha256']]['members']:
     if m.get('is_code') and any(m['name']==q or m['name'].endswith('/'+q)for q in (suffix,package)):
      candidates.append({'archive_sha256':o['archive_sha256'],'member_name':m['name'],'sha256':m['sha256'],'same_directory':posixpath.dirname(m['name'])==posixpath.dirname(o['name']),'assigned_full_read':m['sha256']in assigned,'prior_full_read_record':prior.get(m['sha256'])})
   imports.append({'module':module,'candidates':list({(c['archive_sha256'],c['member_name']):c for c in candidates}.values()),'runtime_resolution_verified':False,'candidate_resolution':'Static path suffix only; imports never performed'})
 for line_no,line in enumerate(text.splitlines(),1):
  for match in filepat.finditer(line):
   reference=match.group(1);cand=[]
   for o in row['occurrences']:
    if o['kind']!='archive_member':continue
    z=zs[o['archive_sha256']];base=posixpath.dirname(o['name']);exact=posixpath.normpath(posixpath.join(base,reference))
    names=[exact]if exact in z.namelist()else[n for n in z.namelist()if n==reference or n.endswith('/'+reference)]
    for name in names:
     b=z.read(name);cand.append({'archive_sha256':o['archive_sha256'],'member_name':name,'sha256':H(b),'bytes':len(b),'same_directory_literal':name==exact})
   refs.append({'source_index':row['index'],'source_sha256':row['sha256'],'line':line_no,'literal':reference,'candidates':list({(c['archive_sha256'],c['member_name']):c for c in cand}.values()),'scope':'Inert literal mapping only; formatted/dynamic paths, search paths, native ABI and external libraries unresolved'})
 for o in row['occurrences']:
  if o['kind']=='library_standalone':
   path=Path(o['path']);b=path.read_bytes()if path.is_file()else None;standalone.append({'source_index':row['index'],'source_sha256':row['sha256'],'path':str(path),'exists':b is not None,'exact_hash_matches':H(b)==row['sha256']if b is not None else False,'library_file_id':o.get('library_file_id'),'library_observed_version':o.get('observed_version'),'live_Library_version_refetched':False})
 review['dependency_reconciliation']=imports;review['literal_file_reference_reconciliation']=[r for r in refs if r['source_index']==row['index']];save('per_hash/'+row['sha256']+'.json',review);deps.append({'index':row['index'],'sha256':row['sha256'],'dependencies':imports})
save('DEPENDENCY_RECONCILIATION.json',deps);save('LITERAL_FILE_REFERENCES.json',refs);save('STANDALONE_OCCURRENCE_CHECKS.json',standalone)
# Explicitly reconcile zipped frame word declarations, which generic manifest scan does not infer.
word_checks=[]
rec=next(r for r in outs if r['member_name'].endswith('/frame/frame-compiler.json'));obj=json.loads((P/rec['snapshot']).read_text());z=zs[rec['archive_sha256']];base=posixpath.dirname(rec['member_name'])
word_alternatives=[]
for name in z.namelist():
 if name.endswith('/word.json.gz'):
  packed=z.read(name);raw=gzip.decompress(packed)
  word_alternatives.append({'member_name':name,'gzip_sha256':H(packed),'word_sha256':H(raw),'compressed_bytes':len(packed),'uncompressed_bytes':len(raw)})
for h,axis in obj['axes'].items():
 name=base+f'/frame-word-{h}.json.gz';matches=[x for x in word_alternatives if x['word_sha256']==axis['word_sha256']]
 assert matches
 word_checks.append({'h':int(h),'archive_sha256':rec['archive_sha256'],'expected_member_name':name,'original_path_present':name in z.namelist(),'declared_gzip_sha256':axis['gzip_sha256'],'declared_word_sha256':axis['word_sha256'],'status':'EXACT_DECOMPRESSED_CONTENT_RECOVERED_ALTERNATIVE_GZIP','exact_decompressed_matches':matches,'original_compressed_hash_found':any(x['gzip_sha256']==axis['gzip_sha256']for x in word_alternatives),'current_word_replay':False,'interpretation':'Original frame-word path and compressed representation absent; exact serialized raw JSON content rehashed under alternative archive paths. No supplied word executed or replayed.'})
save('FRAME_WORD_HASH_RECONCILIATION.json',word_checks)
# Focused historical evidence attribution. Never label stored PASS as current source run.
focus=[]
for ending in ['adaptive_results.json','api_guard_results.json','sanitizer_result.txt','adaptive_sanitizer_result.txt','sanitizer_initial_result.txt','N16_OUTER_GATE_RESULTS.json','SECTOR_FRAME_CERTIFICATE.json','SIGNED_POLE_FAMILY_CERTIFICATE.json','streaming/results.json','frame/frame-compiler.json','frame/frame-certificate.json','test_run.log','tests.log']:
 rec=next((r for r in outs if r['member_name'].endswith(ending)),None)
 if not rec:continue
 q={'member_name':rec['member_name'],'archive_sha256':rec['archive_sha256'],'sha256':rec['sha256'],'snapshot':rec['snapshot'],'current_run':False,'interpretation':'Stored evidence only; source/data chronology and historical execution not independently attested'}
 if ending=='adaptive_results.json':
  obj=json.loads((P/rec['snapshot']).read_text());q['heldout']=[{k:a[k]for k in ['n','method','correctness_max_abs_error','regret_vs_fastest_percent','break_even']}for a in obj['sizes']];q['attribution_note']='Contains explicit_fast_path and post_change_guard_results_file fields not emitted by reviewed test_adaptive.py; likely augmented artifact, no exact single-script-run attribution inferred.'
 if ending=='sanitizer_initial_result.txt':q['content']=(P/rec['snapshot']).read_text();q['interpretation']='Initial LeakSanitizer error under ptrace is preserved; later leak-disabled ASan/UBSan report cannot establish leak freedom.'
 elif ending.endswith('.txt'):q['content']=(P/rec['snapshot']).read_text()
 if ending=='streaming/results.json':q['current_fresh_check']='All184 count rows reconciled; historical transforms/timings not rerun.'
 if ending=='SECTOR_FRAME_CERTIFICATE.json':q['current_fresh_check']='Eight inverses independently rebuilt from archived routes;64 sector minors and2 direct-sum minors match.'
 if ending=='N16_OUTER_GATE_RESULTS.json':q['current_fresh_check']='16 stored9x9 matrices independently determinant-checked; full prefix not independently regenerated.'
 if ending=='frame/frame-compiler.json':q['current_fresh_check']='Original frame-word gzip paths absent; both exact raw word hashes independently recovered from alternative baseline word.json.gz members in same archive. Compressed hashes differ. No dirty-basis replay.'
 focus.append(q)
save('STORED_EVIDENCE_RECONCILIATION.json',{'evidence_records_preserved':len(outs),'unique_evidence_hashes':len({r['sha256']for r in outs}),'focused_attribution':focus,'all432_documents_fully_reviewed':False,'scope_note':'Evidence inventory, digest reconciliation and selected arithmetic checks supplement complete51-source readings; do not imply all ancillary proofs have been audited.'})
print(json.dumps({'literal_references':len(refs),'standalone_occurrences':len(standalone),'all_standalone_match':all(x['exact_hash_matches']for x in standalone),'frame_word_status':dict(collections.Counter(x.get('status','HASH_VERIFIED')for x in word_checks))}))
