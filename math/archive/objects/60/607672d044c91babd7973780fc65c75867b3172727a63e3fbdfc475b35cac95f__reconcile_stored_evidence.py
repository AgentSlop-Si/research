"""Fresh inert metadata/manifest reconciliation. Never imports or executes supplied programs."""
from pathlib import Path,PurePosixPath
import json,re,hashlib,zipfile,io,collections,posixpath
O=Path(__file__).parent;R=Path('fft_research_master_20261009')
graph=json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'));G={a['sha256']:a for a in graph}
provs=json.loads((O/'PROVENANCE.json').read_text());rows=json.loads((O/'ASSIGNED_SOURCES.json').read_text());ev=json.loads((O/'EVIDENCE_INDEX.json').read_text())
def digest(b):return hashlib.sha256(b).hexdigest()
cache={}
def arc(h):
 if h not in cache:
  ps=G[h]['first_observed_at'].split('!');b=(R/ps[0]).read_bytes()
  for name in ps[1:]:
   with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(name)
  assert digest(b)==h;cache[h]=zipfile.ZipFile(io.BytesIO(b))
 return cache[h]
manifest=[];refs=[];eocc=[]
for p in provs:
 h=p['archive_sha256'];prefix=p['member'].rsplit('/',1)[0]+'/';a=G[h];z=arc(h)
 for m in a['members']:
  if m['name'].startswith(prefix) and m['sha256'] in p['stored_evidence_hashes']:
   eocc.append({'source_index':p['index'],'archive_sha256':h,'member':m['name'],'member_index':m['member_index'],'sha256':m['sha256']})
(O/'EVIDENCE_OCCURRENCES.json').write_text(json.dumps(eocc,indent=2))

def entries(obj):
 if isinstance(obj,list):
  for v in obj:yield from entries(v)
 elif isinstance(obj,dict):
  if isinstance(obj.get('path'),str) and re.fullmatch('[0-9a-f]{64}',str(obj.get('sha256',''))):yield obj['path'],obj['sha256'],obj.get('bytes')
  for k,v in obj.items():
   if isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) and ('.' in k or '/' in k):yield k,v,None
   if isinstance(v,dict) and 'sha256' in v and ('.' in k or '/' in k):yield k,v['sha256'],v.get('bytes')
   yield from entries(v)
seen=set()
for e in ev:
 h=e['archive_sha256'];z=arc(h);text=(O/e['local']).read_text();name=Path(e['member']).name
 if name in ['SEAL.json','SHA256SUMS.json','SEALED_MANIFEST.json','MANIFEST.json','ARCHIVE_MANIFEST.json']:
  es=list(entries(json.loads(text)))
 elif name=='SHA256SUMS.txt':
  es=[(m.group(2),m.group(1),None) for line in text.splitlines() if (m:=re.match(r'^([0-9a-f]{64})\s+\*?(.+)$',line))]
 else:es=[]
 for path,expected,length in es:
  key=(e['member'],path,expected)
  if key in seen:continue
  seen.add(key);target=posixpath.normpath(posixpath.join(posixpath.dirname(e['member']),path));infos=[i for i in z.infolist() if i.filename==target]
  matched=[]
  for info in infos:
   b=z.read(info);matched.append({'sha256':digest(b),'bytes':len(b),'matches_hash':digest(b)==expected,'matches_size':length is None or len(b)==length})
  manifest.append({'manifest':e['member'],'target':target,'claimed_sha256':expected,'claimed_bytes':length,'status':'match' if matched and all(m['matches_hash'] and m['matches_size'] for m in matched) else 'mismatch' if matched else 'absent_at_claimed_path','archive_occurrence_checks':matched})
 # Every stored hash remains a claim until mapped to exact archive data. Restrict to receipts/provenance/result inputs, not arbitrary theorem text.
 if name.lower().endswith('.json') and any(s in name.lower() for s in ['portable','portability','provenance','integrity','independent','results']):
  for hv in sorted(set(re.findall(r'(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])',text))):
   matches=[m for m in G[h]['members'] if m['sha256']==hv]
   verified=[]
   for m in matches:
    b=z.read(z.infolist()[m['member_index']]);assert digest(b)==hv;verified.append(m['name'])
   refs.append({'evidence_member':e['member'],'claimed_sha256':hv,'exact_archived_matches':verified,'status':'matched_bytes_in_containing_archive' if verified else 'not_in_selected_containing_archive','not_execution_proof':True})
(O/'STORED_MANIFEST_RECONCILIATION.json').write_text(json.dumps(manifest,indent=2));(O/'STORED_HASH_REFERENCE_RECONCILIATION.json').write_text(json.dumps(refs,indent=2))
# Resolve only actual imports observed in full source reading, with same-directory exact hashes.
deps=[]
for i,module in [(10,'exact_utils'),(11,'exact_utils'),(12,'exact_utils'),(17,'independent_nonlinear_checks')]:
 p=provs[i];path=p['member'].rsplit('/',1)[0]+'/'+module+'.py';z=arc(p['archive_sha256']);b=z.read(path);dh=digest(b);(O/'evidence'/('dependency_'+dh)).write_bytes(b)
 deps.append({'source_index':i,'source_sha256':rows[i]['sha256'],'module':module,'archive_member':path,'sha256':dh,'bytes':len(b),'local':'evidence/dependency_'+dh,'byte_identity_verified':True,'execution_import_performed':False,'complete_source_read_credited_in_this_review':dh in [r['sha256'] for r in rows],'runtime_resolution_claim':'Exact sibling candidate verified; actual historical sys.path and imported module object not established.'})
(O/'DEPENDENCY_RECONCILIATION.json').write_text(json.dumps({'local_imports':deps,'third_party_dependencies':{'4':['numpy'],'17':['numpy'],'19':['numpy']},'data_dependency_note':'N16 tangent imports N8 checker, whose module initialization reads superconcentrator_N8_certificate.json. Other file inputs listed in SOURCE_REVIEWS.json.','closure_complete':False},indent=2))
print('manifest statuses',dict(collections.Counter(x['status'] for x in manifest)),'hash ref statuses',dict(collections.Counter(x['status'] for x in refs)),'evidence occurrences',len(eocc))
for m in manifest:
 if m['status']!='match':print(m)
# Distinguish serialization fingerprints from file provenance; resolve nested exact file references.
for e in refs:
 if e['status']!='not_in_selected_containing_archive':continue
 member=e['evidence_member'];hv=e['claimed_sha256']
 if member.endswith('review_nonlinear_cycle_bank/VERIFIED_RESULTS.json'):
  e['status']='serialized_permutation_fingerprint_not_a_file_claim';continue
 if member.endswith('fft_hero0_phase10_learned_rational/AUDIT_RESULTS.json'):
  e['status']='generated_input_or_output_fingerprint_not_a_file_claim';continue
 matches=[(a,m) for a in graph for m in a['members'] if m['sha256']==hv]
 if matches:
  a,m=matches[0];z=arc(a['sha256']);b=z.read(z.infolist()[m['member_index']]);assert digest(b)==hv
  local='evidence/external_'+hv+'__'+Path(m['name']).name;(O/local).write_bytes(b)
  e.update(status='matched_nested_archive_bytes',verified_nested_match={'archive_sha256':a['sha256'],'archive_first_observed_at':a['first_observed_at'],'member':m['name'],'member_index':m['member_index'],'sha256':hv,'local':local})
 else:e['status']='external_proposal_text_hash_unresolved_in_archive_graph'
(O/'STORED_HASH_REFERENCE_RECONCILIATION.json').write_text(json.dumps(refs,indent=2))
print('Final hash reference classes',dict(collections.Counter(e['status'] for e in refs)))
