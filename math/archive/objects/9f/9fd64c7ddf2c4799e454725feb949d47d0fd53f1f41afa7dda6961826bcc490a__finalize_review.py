import json,hashlib,pathlib,shutil
D=pathlib.Path(__file__).resolve().parent
ROOT=pathlib.Path('master_v20_integration_20261010/fft_research_master_20261009/library')
QUEUE=pathlib.Path('coverage_audit_20261010/BASELINE_TEXT_REVIEW_QUEUE_1.json')
q=json.loads(QUEUE.read_text())['sources'];notes=[json.loads(l) for l in (D/'review_notes.jsonl').read_text().splitlines()]
assert sorted(x['row'] for x in notes)==list(range(40))
chunks={0:['07f1c1','e92257','076537','cace62','5c2a81'],1:['47578c'],2:['5426c8'],3:['47578c'],4:['1bd141'],5:['1bd141'],6:['a5455d'],7:['a5455d'],8:['83c4bd'],9:['83c4bd'],10:['f9bb9d'],11:['f9bb9d'],12:['2db0f0'],13:['2db0f0'],14:['c44d37'],15:['c44d37'],16:['0aeb9e'],17:['0aeb9e'],18:['686258'],19:['686258'],20:['1e9bd3'],21:['1e9bd3'],22:['4a98bf'],23:['4a98bf'],24:['02e7fe'],25:['02e7fe'],26:['dfce6e'],27:['dfce6e'],28:['4171e4'],29:['4171e4'],30:['bd7931'],31:['bd7931'],32:['76e368'],33:['76e368'],34:['53ddbd'],35:['53ddbd'],36:['ba25a2'],37:['ba25a2'],38:['78a386'],39:['78a386']}
proof=set(range(40))-{0,19,24,26,30,38,39}
secondary={1,10,16,21,36,37};conditional={2,8,18,20,32};support={0,19,24,26,38,39}
rows=[];evidence=[];manifest=[];detail=['# Per-source static review\n\nEvery claim below is tied to the exact source hash. Full-text inspection is distinct from theorem and executable acceptance. Source logs are not fresh executions.\n']
(D/'source_texts').mkdir(exist_ok=True)
for n in notes:
    idx=n['row'];s=q[idx];p=ROOT/s['canonical_path'];data=p.read_bytes();actual=hashlib.sha256(data).hexdigest()
    assert actual==s['sha256'] and len(data)==s['size_bytes']
    text=p.read_text(encoding='utf-8');dest=f'source_texts/{idx:03}_{actual[:16]}{p.suffix}'
    (D/dest).write_bytes(data)
    if idx==30:cat='source_test_log_only'
    elif idx==10:cat='duplicate_package_audit_report'
    elif idx in conditional:cat='conditional_proof_bearing_source'
    elif idx in secondary:cat='secondary_proof_and_implementation_audit'
    elif idx in support:cat='supporting_history_or_implementation_report'
    else:cat='proof_bearing_research_text'
    ranges=n.get('read_ranges_characters',[[0,len(text)]])
    assert ranges[0][0]==0 and ranges[-1][1]==len(text)
    assert all(a[1]==b[0] for a,b in zip(ranges,ranges[1:]))
    ev={'queue_index':idx,'sha256':actual,'byte_count':len(data),'character_count':len(text),'encoding':'utf-8 with universal newline normalization for display only','raw_decoded_character_count':len(data.decode('utf-8')),'crlf_count':data.count(b'\r\n'),'read_character_ranges':ranges,'tool_output_chunk_ids':chunks[idx],'status':'Complete source text read in returned untruncated output ranges. Rows1–3 dedicated rereads supersede initial combined-response truncation.','complete_character_coverage':True}
    row={'queue_index':idx,'sha256':actual,'filename':s['filename'],'display_title':s.get('display_title'),'size_bytes':len(data),'canonical_path':s['canonical_path'],'absolute_path':str(p),'source_provenance':s['provenance'],'inspection':'complete_text_read','full_text_inspection':'complete','classification':cat,'classification_detail':n['classification'],'substantive_content':n['claims'],'mathematical_defects_and_limits':n['defects'],'acceptance_and_dependencies':n['dependencies'],'constructive_implications':n['constructive'],'prior_art_and_novelty':n['novelty'],'proof_acceptance':'No blanket approval; see precise claims, limitations and fresh-control scope.','source_execution':'not executed; uploaded code never imported','historical_test_evidence':'Any tests/counts/benchmarks inside source are submitted claims, separate from INDEPENDENT_CONTROLS.json.','later_exact_review_link':None,'local_inert_snapshot':dest,'read_evidence':ev,'duplicate_status':{'unique_sha_within_assigned_chunk':True,'provenance_occurrences':len(s['provenance']),'multiple_occurrences_are_not_independent_corroboration':True,'reports_duplicate_package':idx==10}}
    if idx in [1,3,4,12,20,33]:row['fresh_bounded_control']='INDEPENDENT_CONTROLS.json; finite scope only, not full source-implementation or asymptotic acceptance'
    rows.append(row);evidence.append(ev);manifest.append({'queue_index':idx,'sha256':actual,'size_bytes':len(data),'absolute_path':str(p),'snapshot_path':dest})
    detail.append(f"\n## Row {idx}: {s['filename']}\n\nSHA-256: {actual}\n\nClassification: {n['classification']}\n\nSubstantive claims: {n['claims']}\n\nDefects and limits: {n['defects']}\n\nDependencies: {n['dependencies']}\n\nConstructive implications: {n['constructive']}\n\nPrior art: {n['novelty']}\n")
coverage={'scope':'Baseline queue1 rows0–39 inclusive, full static source-text inspection; not blanket proof/code approval.','source_queue':str(QUEUE),'source_queue_sha256':hashlib.sha256(QUEUE.read_bytes()).hexdigest(),'canonical_root':str(ROOT),'completed_rows':len(rows),'completed_bytes':sum(r['size_bytes'] for r in rows),'source_hashes_verified':len(rows),'unique_hashes':len(set(r['sha256'] for r in rows)),'assigned_rows':[0,39],'unfinished_assigned_rows':[],'integration_owner':'Main baseline auditor; this report does not update other ledgers.','uploaded_code_executed':False,'fresh_execution_evidence':'INDEPENDENT_CONTROLS.json and independent_controls.log only','rows':rows}
assert coverage['completed_bytes']==648428
for file,obj in [('COVERAGE.json',coverage),('FULL_READ_EVIDENCE.json',evidence),('SOURCE_MANIFEST.json',manifest)]:
    (D/file).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
(D/'SOURCE_HASHES.sha256').write_text(''.join(f"{x['sha256']}  {x['absolute_path']}\n" for x in manifest))
(D/'PER_SOURCE_REVIEW.md').write_text(''.join(detail))
refs={'scope':'Limited fresh primary-source checks, not exhaustive priority search or upstream framework verification.','date':'2026-10-10','checks':[{'url':'https://fftw.org/pruned.html','checked_fact':'Author documentation states O(N log K) pruning and arbitrary-output small-transform decomposition; arithmetic savings may not improve performance.'},{'url':'https://arxiv.org/abs/2211.04643','checked_fact':'Alman abstract states constant-size finite-field WHT O(N log N/loglog N) bit operations; lookup model distinct from arbitrary complex DFT.'},{'url':'https://arxiv.org/abs/math/0308286','checked_fact':'Tao abstract states prime cyclic support-sum uncertainty and sparse-polynomial zero consequence.'}],'not_verified':['Exhaustive novelty for this corpus','Current OpenAI/CrocSwap repository status','Inherited all-length/tape/frame compiler theorem bodies','All historical bibliographic attributions']}
(D/'PRIMARY_SOURCE_CHECKS.json').write_text(json.dumps(refs,indent=2)+'\n')
print(json.dumps({k:coverage[k] for k in ['completed_rows','completed_bytes','source_hashes_verified','unique_hashes']}))
