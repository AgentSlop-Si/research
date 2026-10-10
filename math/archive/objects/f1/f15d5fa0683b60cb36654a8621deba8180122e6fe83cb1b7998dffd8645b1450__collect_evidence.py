"""Fresh reviewer inert byte/provenance collector; never imports/parses supplied source."""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,io
O=Path(__file__).parent; ROOT=Path('fft_research_master_20261009')
G={a['sha256']:a for a in json.loads((O/'ARCHIVE_GRAPH_SNAPSHOT.json').read_text())}
rows=json.loads((O/'ASSIGNED_SOURCES.json').read_text());cache={};ev={};prov=[]
def archive(h):
 if h in cache:return cache[h]
 pieces=G[h]['first_observed_at'].split('!'); b=(ROOT/pieces[0]).read_bytes()
 for name in pieces[1:]:
  with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(name)
 assert hashlib.sha256(b).hexdigest()==h
 cache[h]=b;return b
for r in rows:
 occurrences=[x for x in r['occurrences'] if x.get('archive_sha256') in G]
 # Prefer the smallest containing original archive over a historical originals wrapper.
 o=min(occurrences,key=lambda v:(v['name'].startswith('originals/'),len(G[v['archive_sha256']]['members']),v['name']!=r['representative_path']))
 h=o['archive_sha256'];a=G[h];deps=[];es=[]
 with zipfile.ZipFile(io.BytesIO(archive(h))) as z:
  inf=z.infolist()[o['member_index']]; assert inf.filename==o['name'];b=z.read(inf);assert hashlib.sha256(b).hexdigest()==r['sha256']
  parts=PurePosixPath(o['name']).parts
  prefix=parts[0]+'/' if len(parts)>1 else ''
  for m in a['members']:
   if not m['name'].startswith(prefix):continue
   if m['is_code']:deps.append({'name':m['name'],'sha256':m['sha256'],'size_bytes':m['size_bytes']});continue
   if m['is_zip'] or m['size_bytes']>2000000 or not m['name'].lower().endswith(('.json','.jsonl','.txt','.md','.csv','.log','.gz')):continue
   eb=z.read(z.infolist()[m['member_index']]);assert hashlib.sha256(eb).hexdigest()==m['sha256'];eh=m['sha256'];es.append(eh)
   occurrence={'archive_sha256':h,'member_index':m['member_index'],'member':m['name']}
   if eh not in ev:
    local='evidence/'+eh+'__'+PurePosixPath(m['name']).name;(O/local).write_bytes(eb);ev[eh]={'sha256':eh,'size_bytes':len(eb),'local':local,'occurrences':[]}
   if occurrence not in ev[eh]['occurrences']:ev[eh]['occurrences'].append(occurrence)
 prov.append({'index':r['index'],'sha256':r['sha256'],'archive_sha256':h,'archive_first_observed_at':a['first_observed_at'],'member_index':o['member_index'],'member':o['name'],'byte_identity_verified':True,'related_archived_code_metadata_only':deps,'stored_evidence_hashes':es,'origin_class':r['origin_class'],'note':'Byte identity, not authorship, is established. Stored PASS is historical, not rerun.'})
(O/'PROVENANCE.json').write_text(json.dumps(prov,indent=2));(O/'EVIDENCE_INDEX.json').write_text(json.dumps(list(ev.values()),indent=2));print(json.dumps({'source_occurrences_verified':len(prov),'archives_rehashed':len(cache),'evidence_files':len(ev),'evidence_bytes':sum(e['size_bytes'] for e in ev.values())}))
