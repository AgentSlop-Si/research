"""New review metadata-only archive pass. Never executes/imports/parses source code."""
from pathlib import Path, PurePosixPath
import json, hashlib, zipfile, io, re, collections
OUT=Path(__file__).parent
ROOT=Path('fft_research_master_20261009')
GRAPH=json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'));G={r['sha256']:r for r in GRAPH}
rows=json.load(open(OUT/'ASSIGNED_SOURCES.json'));registry=json.load(open(OUT/'REGISTRY_START_SNAPSHOT.json'));seen={r['sha256'] for r in registry['rows']};own={r['sha256'] for r in rows}
cache={};ev={};provenance=[];dependencies=[]
def read_archive(h):
 if h not in cache:
  parts=G[h]['first_observed_at'].split('!');b=(ROOT/parts[0]).read_bytes()
  for n in parts[1:]:
   with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(n)
  assert hashlib.sha256(b).hexdigest()==h;cache[h]=b
 return cache[h]
def rank(o):
 name=o['name'];return (name.startswith('originals/'),bool(re.search(r'baseline|original_copy|vendor|hardened',name)),len(name.split('/')),len(G[o['archive_sha256']]['first_observed_at']),name)
for r in rows:
 occ=[o for o in r['occurrences'] if o.get('archive_sha256') in G];primary=min(occ,key=rank);all_occ=[]
 for o in occ:
  h=o['archive_sha256']
  with zipfile.ZipFile(io.BytesIO(read_archive(h))) as z:
   info=z.infolist()[o['member_index']];assert info.filename==o['name'];b=z.read(info);assert hashlib.sha256(b).hexdigest()==r['sha256']
  all_occ.append({**o,'archive_first_observed_at':G[h]['first_observed_at'],'byte_identity_verified':True})
 h=primary['archive_sha256'];arc=G[h];directory=str(PurePosixPath(primary['name']).parent);deps=[];es=[]
 # Whole primary archive is a context, not a runtime resolution guarantee.
 with zipfile.ZipFile(io.BytesIO(read_archive(h))) as z:
  for m in arc['members']:
   if m['is_code']:
    deps.append({'name':m['name'],'sha256':m['sha256'],'coverage_at_start':'assigned_this_review' if m['sha256'] in own else 'accepted_registry_row' if m['sha256'] in seen else 'not_in_start_registry_rows'});continue
   if m['is_zip'] or m['size_bytes']>10000000 or not m['name'].lower().endswith(('.json','.jsonl','.txt','.md','.csv','.log','.gz')):continue
   b=z.read(z.infolist()[m['member_index']]);assert hashlib.sha256(b).hexdigest()==m['sha256'];eh=m['sha256'];es.append(eh)
   if eh not in ev:
    local='evidence/'+eh+'__'+Path(m['name']).name;(OUT/local).write_bytes(b);ev[eh]={'sha256':eh,'size_bytes':len(b),'local':local,'occurrences':[]}
   o2={'archive_sha256':h,'member':m['name']}
   if o2 not in ev[eh]['occurrences']:ev[eh]['occurrences'].append(o2)
 prov={'index':r['index'],'sha256':r['sha256'],'archive_sha256':h,'archive_first_observed_at':arc['first_observed_at'],'member_index':primary['member_index'],'member':primary['name'],'byte_identity_verified':True,'all_occurrences':all_occ,'related_archived_code_metadata_only':deps,'stored_evidence_hashes':es,'origin_class':r.get('origin_class','origin_unresolved'),'note':'Archive identities verified; historical independent/no-uploaded declarations do not independently establish authorship or execution.'};provenance.append(prov)
 for ref in r.get('import_references',[]):
  module=ref.get('module');names=[module] if module else ref.get('names',[])
  for module in names:
   if not module:continue
   stem=module.replace('.','/')+'.py';candidates=[d for d in deps if d['name']==(stem if directory=='.' else directory+'/'+stem)]
   status='same_directory_candidate' if candidates else 'no_same_directory_module'
   if not candidates:
    candidates=[d for d in deps if PurePosixPath(d['name']).name==module.split('.')[-1]+'.py'];status='archive_basename_candidates_not_runtime_resolution' if candidates else 'external_or_missing_archive_module'
   dependencies.append({'index':r['index'],'source_sha256':r['sha256'],'import':module,'status':status,'candidates':candidates,'runtime_resolution_verified':False})
(OUT/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2));(OUT/'EVIDENCE_INDEX.json').write_text(json.dumps(list(ev.values()),indent=2));(OUT/'DEPENDENCIES.json').write_text(json.dumps(dependencies,indent=2))
print('source hashes',len(rows),'verified occurrences',sum(len(r['all_occurrences']) for r in provenance),'primary archives',len(set(r['archive_sha256'] for r in provenance)),'all archive hashes verified',len(cache),'evidence files',len(ev),'evidence bytes',sum(e['size_bytes'] for e in ev.values()))
for e in ev.values():
 if any(re.search(r'result|certificate|receipt|guard|manifest|validation|checks|chart',o['member'],re.I) for o in e['occurrences']):print(e['sha256'][:12],e['size_bytes'],e['occurrences'][0]['member'])
