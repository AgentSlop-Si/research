"""Reviewer-authored inert packaging, hashing and manifest validation only."""
import json,pathlib,hashlib,re,datetime
P=pathlib.Path(__file__).parent
F=pathlib.Path('code_coverage_audit_0228')
R=pathlib.Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json')
def h(b):return hashlib.sha256(b).hexdigest()
def put(name,obj):(P/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
rows=json.loads((P/'SOURCE_INDEX.json').read_text());notes=[json.loads(x) for x in (P/'review_notes.jsonl').read_text().splitlines()]
assert [x['index'] for x in rows]==[x['index'] for x in notes]==list(range(81))
inventory=json.loads((F/'CODE_COVERAGE_INVENTORY.json').read_text());byhash={x['sha256']:x for x in inventory}
registry_raw=R.read_bytes();registry=json.loads(registry_raw)
(P/'input_manifests/ADDITIVE_CODE_COVERAGE_FINAL.json').write_bytes(registry_raw)
prior={x['sha256'] for x in inventory if x.get('static_inspection_complete')}
prior|={x['sha256'] for x in registry['rows'] if x.get('full_static_inspection')}
context=json.loads((P/'STORED_EVIDENCE_INDEX.json').read_text());families=json.loads((P/'EVIDENCE_RECONCILIATION.json').read_text())['families']
archive_graph={x['sha256']:x for x in json.loads((F/'ARCHIVE_GRAPH.json').read_text())}
findings=[];coverage=[];evidence=[];dependencies=[];preservation=[];invalid=[]
for r,n in zip(rows,notes):
 sha=r['sha256'];raw=(P/r['snapshot']).read_bytes();assert h(raw)==sha
 assert len(raw)==r['size_bytes'] and raw==pathlib.Path(r['local_content']).read_bytes()
 assert byhash[sha]['size_bytes']==len(raw)
 lines=raw.decode().splitlines();assert len(lines)==r['line_count']
 refs=[]
 for field in ('scope','cost','numerical','tests','dependencies'):
  assert n[field]
  for m in re.finditer(r'\bL(\d+)(?:[-–](\d+))?',n[field]):
   lo=int(m[1]);hi=int(m[2] or lo)
   if not 1<=lo<=hi<=len(lines):invalid.append([r['index'],field,lo,hi,len(lines)])
   else:refs.append({'field':field,'lines':[lo,hi]})
 assert refs
 family=next(f for f in families if r['index']in f['assigned_indices'])
 report=f'per_source/{r["index"]:03d}_{sha}.md'
 body=f'# Source {r["index"]:03d}: {r["representative_path"]}\n\nSHA-256: `{sha}`\n\nExact bytes: {len(raw)}. Lines: {len(lines)}. Fully read interval: 1–{len(lines)}.\n\nSnapshot: `{r["snapshot"]}`. Assigned batch: `{r["assigned_batch"]}`.\n\n'
 for key,title in [('scope','Theorem and algorithm scope'),('cost','Cost accounting'),('numerical','Numerical and input assumptions'),('tests','Test execution attribution'),('dependencies','Dependencies and closure')]:body+=f'## {title}\n\n{n[key]}\n\n'
 body+='## Stored-evidence reconciliation\n\n'+family['finding']+'\n\n'+family['attribution']+'\n\n'
 body+='## Review boundary\n\nComplete first-to-last inert text inspection. No supplied execution, import, compilation or AST parsing. This source receives static inspection credit only. Frozen metadata such as prior AST hashes is inherited provenance, not an action performed here. Dependency references do not extend full-read credit.\n'
 (P/report).write_text(body)
 report_hash=h((P/report).read_bytes())
 common={'index':r['index'],'sha256':sha,'representative_path':r['representative_path'],'source_snapshot':r['snapshot'],'full_static_inspection':True,'fully_read_line_intervals':[[1,len(lines)]],'source_executed_in_review':False,'source_imported_in_review':False,'source_compiled_in_review':False,'source_ast_parsed_in_review':False}
 findings.append({**common,**{k:n[k] for k in ('scope','cost','numerical','tests','dependencies')},'line_references':refs,'stored_evidence_group':family['group'],'report':report})
 coverage.append({**common,'bytes':len(raw),'lines':len(lines),'assigned_batch':r['assigned_batch'],'prior_full_static_inspection':sha in prior,'new_coverage_credit':sha not in prior,'inspection_method':'Complete first-to-last inert-text read and per-hash review of theorem scope, cost, numerical assumptions, tests, dependencies and stored evidence.','review_file':report,'review_sha256':report_hash})
 evidence.append({'evidence_id':f'FULL_STATIC_{r["index"]:03d}','sha256':sha,'scope':'whole exact source','line_intervals':[[1,len(lines)]],'source_snapshot':r['snapshot'],'review_file':report,'review_sha256':report_hash,'source_execution':'none'})
 preservation.append({'sha256':sha,'bytes':len(raw),'snapshot':r['snapshot'],'frozen_content_match':True,'frozen_inventory_match':True,'original_rechecked_unchanged':True,'occurrences':r['occurrences']})
 # Exact-hash possible local dependency candidates, using inherited reference metadata only.
 occ=next(o for o in r['occurrences'] if o.get('name')==r['representative_path']);arc=archive_graph[occ['archive_sha256']]
 candidates=[]
 for imp in r.get('import_references',[]):
  mods=[imp['module']] if imp.get('module') else imp.get('names',[])
  for mod in mods:
   suffix=mod.replace('.','/')
   matches=[m for m in arc['members'] if m.get('is_code') and (m['name'].endswith('/'+suffix+'.py') or m['name'].endswith('/'+suffix+'/__init__.py'))]
   candidates.append({'reference':mod,'inherited_syntactic_metadata':True,'same_archive_candidates':[{'name':m['name'],'sha256':m['sha256'],'covered_before_review':m['sha256']in prior,'assigned_here':m['sha256']in {x['sha256']for x in rows}} for m in matches],'resolution':'Possible path candidates only; actual sys.path, optional imports and transitive runtime closure not executed or certified.'})
 dependencies.append({'sha256':sha,'index':r['index'],'manual_dependency_findings':n['dependencies'],'possible_local_candidates':candidates,'full_runtime_closure_verified':False})
assert not invalid,invalid
assert sum(x['bytes']for x in coverage)==380628
assert len({x['sha256']for x in coverage})==81
put('FINDINGS.json',findings);put('EVIDENCE_INDEX.json',evidence);put('DEPENDENCIES.json',dependencies)
put('PRESERVATION_RECEIPT.json',{'rows':preservation,'all_exact_frozen_sources_rechecked':True})
new=sum(x['new_coverage_credit']for x in coverage)
put('COVERAGE.json',{'all_assigned_source_reads_complete':True,'fully_read_hashes_this_review':81,'new_full_read_hashes':new,'new_coverage_credit_count':new,'previously_covered_hashes':81-new,'assigned_batch_count':len({x['assigned_batch']for x in rows}),'assigned_batch_hashes':81,'total_source_bytes':380628,'total_source_lines':8709,'registry_at_final_dedup_sha256':h(registry_raw),'current_registry_read_count':registry['current_full_static_reads'],'central_registry_modified':False,'dependency_closure_complete':False,'all_research_material_checks_finished':False,'completion_scope':'Assigned 81 hashes only; no global or transitive completion.','rows':coverage})
put('DEDUP_FINAL.json',{'registry_sha256':h(registry_raw),'registry_current_full_static_reads':registry['current_full_static_reads'],'assigned_new':new,'assigned_previously_covered':81-new,'initial_dedup':json.loads((P/'DEDUP_SCAN.json').read_text()),'frozen_inventory_sha256':h((F/'CODE_COVERAGE_INVENTORY.json').read_bytes())})
put('VALIDATION.json',{'assigned_hashes':81,'unique_source_hashes':81,'per_hash_findings':len(findings),'source_bytes':380628,'source_lines':8709,'all_source_snapshots_hash_verified':True,'all_original_sources_rechecked':True,'all_report_line_references_in_range':True,'all_five_review_dimensions_present':True,'stored_context_members_preserved':sum('snapshot'in x for x in context),'stored_context_unique_preserved_hashes':len({x['sha256']for x in context if 'snapshot'in x}),'supplied_code_execution':False,'supplied_code_import':False,'supplied_code_compile':False,'supplied_code_ast_parse':False,'review_owned_independent_checks':'INDEPENDENT_CHECK_RESULTS.json','prior_package_0445_untouched':True})
print('Validated',len(rows),'sources;',new,'new against',registry['current_full_static_reads'])
