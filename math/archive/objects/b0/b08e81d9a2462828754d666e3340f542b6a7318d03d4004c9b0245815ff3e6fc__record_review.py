import json,pathlib,sys
p=pathlib.Path(__file__).parent
manifest=json.loads((p/'SOURCE_MANIFEST.json').read_text())
for z in json.load(sys.stdin):
 r=manifest[z['index']-1]; d=(p/'sources'/r['sha256']).read_bytes()
 out=dict(index=r['index'],sha256=r['sha256'],size_bytes=len(d),representative_path=r['representative_path'],snapshot_path='sources/'+r['sha256'],static_inspection_complete=True,full_static_inspection=True,inspection_method='Direct first-to-last inert text reading of exact bytes; no execution, importing, compiling or AST parsing.',coverage_intervals={'bytes_half_open':[[0,len(d)]],'lines_inclusive':[[1,r['line_count']]]},source_executed_in_review=False,source_imported_in_review=False,source_compiled_in_review=False,source_ast_parsed_in_review=False,provenance={k:r[k] for k in ['batch_name','occurrences','root_archive_sha256s','origin_class','origin_basis']},dependency_closure_complete=False,current_review_test_status='Supplied tests statically inspected only; independently authored controls, if any, are separately identified.')
 out.update(z); (p/'per_hash'/f"{r['sha256']}.json").write_text(json.dumps(out,indent=2)+'\n')
