"""New reviewer inert archive/provenance collector. Never loads source as code."""
from pathlib import Path
import json,hashlib,zipfile,io
OUT=Path(__file__).parent;ROOT=Path('fft_research_master_20261009')
G={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))}
rows=json.load(open(OUT/'ASSIGNED_SOURCES.json'));cache={};evidence={};provenance=[]
def digest(b):return hashlib.sha256(b).hexdigest()
def arc(h):
 if h in cache:return cache[h]
 parts=G[h]['first_observed_at'].split('!');raw=(ROOT/parts[0]).read_bytes()
 for name in parts[1:]:
  with zipfile.ZipFile(io.BytesIO(raw)) as z:raw=z.read(name)
 assert digest(raw)==h
 cache[h]=raw;return raw
for r in rows:
 occ=sorted([o for o in r['occurrences'] if o.get('archive_sha256') in G],key=lambda o:len(G[o['archive_sha256']]['first_observed_at']))
 o=occ[0];h=o['archive_sha256'];a=G[h];siblings=[];es=[]
 with zipfile.ZipFile(io.BytesIO(arc(h))) as z:
  info=z.infolist()[o['member_index']];assert info.filename==o['name'];assert digest(z.read(info))==r['sha256']
  prefix=o['name'].rsplit('/',1)[0]+'/'
  for m in a['members']:
   if not m['name'].startswith(prefix):continue
   if m['is_code']:siblings.append({'name':m['name'],'sha256':m['sha256'],'size_bytes':m['size_bytes']});continue
   if m['is_zip'] or m['size_bytes']>2000000 or not m['name'].lower().endswith(('.json','.jsonl','.md','.log','.txt','.csv')):continue
   b=z.read(z.infolist()[m['member_index']]);assert digest(b)==m['sha256'];eh=m['sha256'];es.append(eh)
   if eh not in evidence:
    local='evidence/'+eh+'__'+Path(m['name']).name;(OUT/local).write_bytes(b);evidence[eh]={'sha256':eh,'size_bytes':len(b),'local':local,'archive_sha256':h,'member':m['name']}
 master=ROOT/r['representative_path'];master_ok=master.exists() and digest(master.read_bytes())==r['sha256']
 provenance.append({'index':r['index'],'sha256':r['sha256'],'archive_sha256':h,'archive_first_observed_at':a['first_observed_at'],'member_index':o['member_index'],'member':o['name'],'byte_identity_verified':True,'master_standalone_verified':master_ok,'all_declared_occurrences':r['occurrences'],'related_archived_code_metadata_only':siblings,'stored_evidence_hashes':es,'origin_class_from_prior_inventory':r['origin_class'],'historical_execution_flag_from_prior_inventory':r['recorded_execution'],'note':'Archived reviewer source is supplied material in this review. Prior origin/run classifications do not establish present execution or all-size proof.'})
(OUT/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2));(OUT/'EVIDENCE_INDEX.json').write_text(json.dumps(list(evidence.values()),indent=2))
print('Verified source archives',len(provenance),'archives',len(cache),'evidence',len(evidence),'bytes',sum(e['size_bytes'] for e in evidence.values()))
for i,r in enumerate(rows):
 es=[e for e in evidence.values() if e['sha256'] in provenance[i]['stored_evidence_hashes']];print(i,[(Path(e['member']).name,e['size_bytes']) for e in es])
