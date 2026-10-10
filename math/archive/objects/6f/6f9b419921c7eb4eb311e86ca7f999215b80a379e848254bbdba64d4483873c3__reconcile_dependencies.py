"""Review metadata and archive members only; no import execution or source parsing."""
from pathlib import Path
import json,hashlib,zipfile,posixpath
P=Path(__file__).parent;rows=json.loads((P/'SOURCE_MANIFEST.json').read_text());archive_records=json.loads((P/'ARCHIVE_RECONCILIATION.json').read_text());ars={a['archive_sha256']:a for a in archive_records};graph={a['sha256']:a for a in json.loads(Path('code_coverage_audit_0228/ARCHIVE_GRAPH.json').read_text())};registry=json.loads(Path('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json').read_text());reviewed={r['sha256'] for r in registry['rows']};assigned={r['sha256'] for r in rows};inv={r['sha256']:r for r in json.loads((P/'provenance/CODE_COVERAGE_INVENTORY.json').read_text())};standard={'pathlib','sys','os','dataclasses','collections','operator','json','random','hashlib','importlib','fractions','math','cmath','heapq','decimal','time','subprocess','unittest','itertools','csv','ctypes','gc','statistics','argparse','types'};third={'numpy','scipy','networkx','numba'};reports=[]
for r in rows:
 deps=[]
 for ref in r.get('import_references',[]):
  modules=[ref['module']] if ref['module'] else ref.get('names',[])
  for mod in modules:
   root=mod.split('.')[0]
   if root in standard:deps.append({'module':mod,'class':'standard_library','basis':'inherited import-reference metadata, not new AST parsing'});continue
   if root in third:deps.append({'module':mod,'class':'external_third_party','installation_and_version_verified':False});continue
   candidates={}
   tails=(mod.replace('.','/')+'.py',mod.replace('.','/')+'/__init__.py')
   for occ in r['occurrences']:
    if occ['kind']!='archive_member':continue
    ah=occ['archive_sha256'];parent=posixpath.dirname(occ['name']);exact={posixpath.join(parent,t) for t in tails}
    for member in graph[ah]['members']:
     name=member['name']
     if name in exact or any(name.endswith('/'+t) for t in tails):
      key=(ah,name);candidates[key]={'archive_sha256':ah,'member_name':name,'member_index':member['member_index'],'sha256':member['sha256'],'same_directory':name in exact}
   for c in candidates.values():
    with zipfile.ZipFile(ars[c['archive_sha256']]['archive_path']) as z:raw=z.read(z.infolist()[c['member_index']]);assert hashlib.sha256(raw).hexdigest()==c['sha256']
    c['bytes_rehashed']=True;c['assigned_full_review']=c['sha256'] in assigned;c['prior_full_review_registry']=c['sha256'] in reviewed;c['frozen_inventory_full_review']=inv.get(c['sha256'],{}).get('static_inspection_complete',False)
   same=[c for c in candidates.values() if c['same_directory']];chosen=same if same else list(candidates.values());deps.append({'module':mod,'class':'local_source_candidate','candidates':chosen,'resolution':'same_directory_candidates' if same else 'archive_suffix_candidates' if chosen else 'unresolved_or_dynamic_path','runtime_resolution_verified':False})
 reports.append({'source_sha256':r['sha256'],'source_path':r['representative_path'],'dependencies':deps,'dynamic_import_and_subprocess_closure':'Partially described in source review; not established by inherited syntactic import references.','closure_complete':False})
(P/'DEPENDENCY_RECONCILIATION.json').write_text(json.dumps({'basis':'Inherited syntactic import metadata reconciled to rehashed actual archive bytes; no source AST parsing and no runtime imports. Same-directory/suffix matches are candidates, not claims about dynamic sys.path execution.','registry_snapshot_digest':hashlib.sha256(json.dumps(registry).encode()).hexdigest(),'sources':reports},indent=2)+'\n')
print('Dependency sources',len(reports),'local candidate references',sum(d['class']=='local_source_candidate' for r in reports for d in r['dependencies']))
