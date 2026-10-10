import json,pathlib
P=pathlib.Path(__file__).parent
rows=json.loads((P/'SOURCE_MANIFEST.json').read_text())
def record(items):
 path=P/'REVIEWS.json'; previous=json.loads(path.read_text()) if path.exists() else []
 for i,scope,cost,limits,findings in items:
  r=rows[i-1]; previous=[x for x in previous if x['sha256']!=r['sha256']]
  previous.append({'index':i,'sha256':r['sha256'],'size_bytes':r['size_bytes'],'representative_path':r['representative_path'],'snapshot_path':'sources/'+r['sha256'],'static_inspection_complete':True,'full_static_inspection':True,'inspection_method':'Direct first-to-last inert text reading of this exact source; no execution, importing, compiling, or AST parsing.','coverage_intervals':{'bytes_half_open':[[0,r['size_bytes']]],'lines_inclusive':[[1,r['line_count']]]},'mathematical_scope':scope,'cost_scope':cost,'test_and_evidence_limitations':limits,'findings':findings,'source_executed_in_review':False,'source_imported_in_review':False,'source_compiled_in_review':False,'source_ast_parsed_in_review':False,'provenance':{'batch_name':r['batch_name'],'occurrences':r['occurrences'],'root_archive_sha256s':r['root_archive_sha256s'],'origin_class':r['origin_class'],'origin_basis':r['origin_basis']}})
 path.write_text(json.dumps(sorted(previous,key=lambda r:r['index']),indent=2)+'\n')
