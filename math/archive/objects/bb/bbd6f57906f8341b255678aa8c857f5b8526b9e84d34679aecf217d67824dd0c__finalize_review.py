"""Fresh bytes-only packaging and receipt reconciliation, not source execution."""
from pathlib import Path
import json,hashlib,csv,datetime,shutil
O=Path(__file__).parent;M=Path('fft_research_master_20261009');H=lambda b:hashlib.sha256(b).hexdigest();rows=json.loads((O/'ASSIGNED_SOURCES.json').read_text());ev=json.loads((O/'EVIDENCE_INDEX.json').read_text());eid={e['sha256']:e for e in ev};extras=[]
for i,r in enumerate(rows):
 root=(M/r['representative_path']).parent
 for p in root.rglob('*'):
  if not p.is_file() or p.suffix in ['.py','.pyc','.zip']:continue
  if p.suffix not in ['.gz','.sha256'] and not p.name.startswith('SHA256'):continue
  b=p.read_bytes();h=H(b)
  if h not in eid:
   local='evidence/'+h+'__'+p.name;(O/local).write_bytes(b);e={'sha256':h,'size_bytes':len(b),'local':local,'origins':[]};ev.append(e);eid[h]=e
  eid[h]['origins'].append({'kind':'supplemental_data_or_old_seal','path':str(p.relative_to(M)),'source_index':i})
# Verify the data-manifest formats not included in the seal dictionary pass.
for i,name in [(42,'SHA256SUMS.json'),(52,'source/SHA256SUMS.json')]:
 p=(M/rows[i]['representative_path']).parent/name;data=json.loads(p.read_text());items=[]
 for name,value in data.items():
  sha=value if isinstance(value,str) else value['sha256'];target=p.parent/name;b=target.read_bytes();items.append({'name':name,'expected':sha,'actual':H(b),'match':H(b)==sha,'bytes_match':len(b)==value['bytes'] if isinstance(value,dict) and 'bytes'in value else None})
 extras.append({'manifest':str(p.relative_to(M)),'sha256':H(p.read_bytes()),'entries':items,'interpretation':'Historical byte identity only; no source execution or proof acceptance.'})
(O/'SUPPLEMENTAL_MANIFEST_RECONCILIATION.json').write_text(json.dumps(extras,indent=2)+'\n');(O/'EVIDENCE_INDEX.json').write_text(json.dumps(ev,indent=2)+'\n')
# Correct lexical-reference candidates using actual source-local binding, not basename inference.
deps=json.loads((O/'DEPENDENCY_RECONCILIATION.json').read_text())
for d in deps:
 for ref in d['references']:
  if ref['kind']=='absolute_path':
   p=Path(ref['path']);ref['exists']=p.exists();ref['path_type']='file' if p.is_file() else 'directory' if p.is_dir() else 'missing';ref['role']='output' if d['source_index']==47 else 'input'
  if d['source_index']==52 and ref.get('name')=='test_phase16.py':
   p=(M/rows[52]['representative_path']).parent/'source/test_phase16.py';ref.update(context_candidate=str(p),exists=p.is_file(),sha256=H(p.read_bytes()),resolution='source variable bound to source subdirectory at L166; bytes hashed only, no AST parsed')
(O/'DEPENDENCY_RECONCILIATION.json').write_text(json.dumps(deps,indent=2)+'\n')
# Explicit own-output association for each exact source, including stdout captures where archived.
output={0:['VERIFIED_RESULTS.json'],1:['INDEPENDENT_RESULTS.json'],2:['INDEPENDENT_RESULTS.json'],3:['INDEPENDENT_CERTIFICATE.json'],4:[],5:[],6:['VERIFIED_RESULTS.json'],7:['FLOW_RESULTS.json'],8:['MOVING_RESULTS.json'],9:['PHASE34_RESULTS.json'],10:['WEYL_V20_RESULTS.json'],11:['INDEPENDENT_RESULTS.json'],12:['INDEPENDENT_RESULTS.json'],13:['BANK_INTERFACE_CONTROLS.json'],14:['BATCHED_EQUIVALENCE_CONTROLS.json'],15:['CHANGED_INTERFACE_CONTROLS.json'],16:['EXTERIOR_UNIQUENESS_CONTROLS.json'],17:['NONZERO_BUTTERFLY_CONTROLS.json'],18:['ORIGINAL_ORIENTATION_CONTROLS.json'],19:['ODD_CHIRP_RESULTS.json'],20:['CHIRP_B_GATE_RESULTS.json'],21:['FOUR_BY_FOUR_GATE_RESULTS.json'],22:['CONJUGATED_RESULTS.json'],23:['TWO_CAYLEY_RESULTS.json'],24:['EXACT_RESULTS.json'],25:['SPECTRAL_RESULTS.json'],26:['INDEPENDENT_RESULTS.json'],27:['INDEPENDENT_RESULTS.json'],28:['INDEPENDENT_RESULTS.json'],29:['VERIFIED_RESULTS.json'],30:['PORTABLE_REPLAY.json'],31:['SINGLE_EDIT_SEARCH.json'],32:['VERIFIED_RESULTS.json'],33:[],34:['PORTABLE_REPLAY.json'],35:['VERIFIED_RESULTS.json'],36:['VERIFIED_RESULTS.json'],37:['COMPRESSED_BOUNDARY_CONTROLS.json'],38:['POLE_RATIONAL_DATA.json'],39:[],40:[],41:['EXACT_EXTENSION_RESULTS.json'],42:['EXACT_NTT_CHECKS.json'],43:['OCCUPANCY_CHECKS.json'],44:['WORD_ARRAY_CHECKS.json'],45:['BOUNDED_LEMMA_RESULTS.json'],46:['COVERAGE.json'],47:['GENERAL_PENCIL_CONTROLS.json'],48:['INDEPENDENT_RESULTS.json'],49:['VERIFIED_RESULTS.json'],50:['INDEPENDENT_RESULTS.json'],51:['INDEPENDENT_RESULTS.json'],52:['INDEPENDENT_RESULTS.json']}
receipts=[]
for i,r in enumerate(rows):
 rr=[]
 for name in output[i]:
  p=(M/r['representative_path']).parent/name;b=p.read_bytes();data=json.loads(b);h=H(b)
  if h not in eid:
   local='evidence/'+h+'__'+p.name;(O/local).write_bytes(b);e={'sha256':h,'size_bytes':len(b),'local':local,'origins':[{'kind':'mapped_historical_output','path':str(p.relative_to(M)),'source_index':i}]};ev.append(e);eid[h]=e
  rr.append({'name':name,'sha256':h,'snapshot':eid[h]['local'],'recorded_status':data.get('status',data.get('result')) if isinstance(data,dict) else None,'top_level_keys':list(data) if isinstance(data,dict) else None,'association':'Literal source output or documented stdout capture/replay metadata, not a new execution attestation','fresh_execution_credit':False,'independent_proof_acceptance':False})
 receipts.append({'source_index':i,'sha256':r['sha256'],'outputs':rr,'no_output_note':None if rr else 'Utility, exploratory stdout only, or generic manifest verifier; no unique receipt inferred.'})
(O/'EVIDENCE_INDEX.json').write_text(json.dumps(ev,indent=2)+'\n');(O/'SOURCE_RECEIPT_RECONCILIATION.json').write_text(json.dumps(receipts,indent=2)+'\n')
notes=list(csv.DictReader((O/'PER_SOURCE_NOTES.tsv').open(),delimiter='\t'));assert len(notes)==len(rows)==53;prov=json.loads((O/'PROVENANCE.json').read_text());reviews=[]
start=json.loads((O/'REGISTRY_START_SNAPSHOT.json').read_text());reg=Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json');shutil.copyfile(reg,O/'REGISTRY_END_SNAPSHOT.json');end=json.loads((O/'REGISTRY_END_SNAPSHOT.json').read_text());seen={r['sha256'] for r in end['rows']};old={r['sha256'] for r in start['rows']}
for i,(r,note) in enumerate(zip(rows,notes)):
 assert int(note['index'])==i;b=(O/'sources'/r['sha256']).read_bytes();assert H(b)==r['sha256'] and len(b)==r['size_bytes'];lines=len(b.decode().splitlines())
 reviews.append({'review_id':f'S{i:02d}','sha256':r['sha256'],'representative_path':r['representative_path'],'bytes':len(b),'lines':lines,'read_scope':{'first_line':1,'last_line':lines,'full_static_inspection':True,'source_executed':False,'source_imported':False,'source_compiled':False,'source_AST_parsed':False},'role':note['role'],'findings':note['findings'],'source_snapshot':'sources/'+r['sha256'],'numbered_snapshot':f'line_numbered/{i:02d}.txt','provenance':prov[i],'dependency_reconciliation':deps[i],'receipt_reconciliation':receipts[i],'previously_covered_at_start':r['sha256'] in old,'previously_covered_at_end':r['sha256'] in seen,'new_coverage_credit':r['sha256'] not in seen})
(O/'SOURCE_REVIEWS.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n');reviewhash=H((O/'SOURCE_REVIEWS.json').read_bytes());credit=sum(r['new_coverage_credit'] for r in reviews);lines=sum(r['lines'] for r in reviews)
md=['# Archived audit/constructor source review','All 53 exact source hashes were read first-to-last as inert text. No supplied execution, import, compilation, syntax parse or AST parse occurred.','']
for r in reviews:md.extend([f"## {r['review_id']} {r['role']}",f"SHA256: {r['sha256']}",f"Path: {r['representative_path']}",f"Read lines 1–{r['lines']} ({r['bytes']} bytes).",r['findings'],''])
(O/'SOURCE_REVIEWS.md').write_text('\n\n'.join(md)+'\n')
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
cov={'package':O.name,'completed_utc':now,'assigned_batches':['batch_08.json'],'assigned_batch_hashes':53,'fully_read_hashes_this_review':53,'new_full_read_hashes':credit,'new_coverage_credit':credit,'previously_covered_hashes':53-credit,'total_source_bytes_read':sum(r['bytes'] for r in reviews),'total_source_lines_read':lines,'all_assigned_new_source_reads_complete':True,'all_research_material_checks_finished':False,'dependency_closure_complete':False,'source_execution':'none','source_import_compilation_syntax_parse':'none','scope_note':'Full first-to-last inert inspection. Historical authorship, receipts and PASS text do not supply fresh execution or proof credit. Central registry not edited by this review.','rows':[{'review_id':r['review_id'],'sha256':r['sha256'],'representative_path':r['representative_path'],'batch':'batch_08.json','bytes':r['bytes'],'lines':r['lines'],'full_static_inspection':True,'static_inspection_complete':True,'full_source_read':True,'line_ranges':[[1,r['lines']]],'source_executed_in_review':False,'evidence_file':'SOURCE_REVIEWS.json','evidence_sha256':reviewhash,'snapshot':r['source_snapshot'],'new_coverage_credit':r['new_coverage_credit']} for r in reviews]}
(O/'COVERAGE.json').write_text(json.dumps(cov,indent=2)+'\n');(O/'DEDUPLICATION.json').write_text(json.dumps({'start_registry_count':start['current_full_static_reads'],'end_registry_count':end['current_full_static_reads'],'assignment_description_count':1277,'overlap_at_start':sum(r['previously_covered_at_start'] for r in reviews),'overlap_at_end':53-credit,'new_coverage_credit':credit,'central_registry_modified_by_this_review':False,'note':'Registry changed concurrently; only immutable local snapshots were used.'},indent=2)+'\n')
print('reviews',len(reviews),'lines',lines,'credit',credit,'evidence',len(ev),sum(e['size_bytes'] for e in ev),'extra_manifest_entries',sum(len(x['entries']) for x in extras))
