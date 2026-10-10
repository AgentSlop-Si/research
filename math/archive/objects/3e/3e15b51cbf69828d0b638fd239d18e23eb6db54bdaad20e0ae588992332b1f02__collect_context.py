"""Review-authored inert archive/data collector. Does not execute supplied programs."""
import io,json,pathlib,hashlib,zipfile
P=pathlib.Path(__file__).parent
F=pathlib.Path('code_coverage_audit_0228')
M=pathlib.Path('fft_research_master_20261009')
rows=json.loads((P/'SOURCE_INDEX.json').read_text())
graph={g['sha256']:g for g in json.loads((F/'ARCHIVE_GRAPH.json').read_text())}
selected={}
for r in rows:
 o=next(o for o in r['occurrences'] if o.get('name')==r['representative_path'])
 selected.setdefault(o['archive_sha256'],[]).append(r['index'])
(P/'stored_evidence').mkdir(exist_ok=True)
context=[];archives=[]
for sha,ids in selected.items():
 g=graph[sha];parts=g['first_observed_at'].split('!')
 raw=(M/parts[0]).read_bytes()
 for name in parts[1:]:
  with zipfile.ZipFile(io.BytesIO(raw)) as z:raw=z.read(name)
 assert hashlib.sha256(raw).hexdigest()==sha
 archives.append({'sha256':sha,'locator':g['first_observed_at'],'assigned_indices':ids,'archive_hash_verified':True})
 with zipfile.ZipFile(io.BytesIO(raw)) as z:
  for m in g['members']:
   name=m['name'];base=pathlib.PurePosixPath(name).name.lower()
   if m['is_code'] or m['is_zip'] or any(x in name for x in ('/baseline','/inputs/','/original')):continue
   wanted=(('/results/' in name or '/audit/' in name or 'result' in base or 'test' in base or 'log' in base or base=='environment.json') and not base.endswith(('.md','.patch')))
   if not wanted:continue
   rec={**m,'archive_sha256':sha,'related_assigned_indices':ids}
   if m['size_bytes']>250000:
    rec['inspection']='not read; retained as locator only; no evidence claim';context.append(rec);continue
   b=z.read(z.infolist()[m['member_index']]);assert hashlib.sha256(b).hexdigest()==m['sha256']
   dest='stored_evidence/'+sha[:12]+'__'+str(m['member_index'])+'__'+pathlib.PurePosixPath(name).name
   (P/dest).write_bytes(b);rec['snapshot']=dest;rec['inspection']='preserved; contextual content inspection separately recorded'
   context.append(rec)
(P/'STORED_EVIDENCE_INDEX.json').write_text(json.dumps(context,indent=2)+'\n')
(P/'ARCHIVE_CONTEXT.json').write_text(json.dumps(archives,indent=2)+'\n')
print('archives',len(archives),'context items',len(context),'preserved',sum('snapshot'in x for x in context))
