import pathlib,json,hashlib,collections,re
out=pathlib.Path('fusion_phase_source_review_0408');rows=json.loads((out/'INPUT_ROWS.json').read_text());master=pathlib.Path('fft_research_master_20261009');manifest=json.loads((out/'BASELINE_MANIFEST.json').read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
wanted={r['sha256'] for r in rows};hits=[];seen=set();allfull={}
def walk(x,path):
 if isinstance(x,dict):
  h=x.get('sha256',x.get('source_sha256',x.get('content_sha256')))
  if h in wanted:hits.append({'hash':h,'file':path,'record':x})
  for v in x.values():walk(v,path)
 elif isinstance(x,list):
  for v in x:walk(v,path)
for e in manifest['coverage_sources']:
 if e['sha256'] in seen:continue
 seen.add(e['sha256']);walk(json.loads((out/e['snapshot']).read_text()),e['path'])
(out/'BASELINE_ASSIGNED_MATCHES.json').write_text(json.dumps(hits,indent=2))
print('Assigned baseline non-inventory matches',[(h['hash'][:10],h['file']) for h in hits if 'CODE_COVERAGE_INVENTORY.json' not in h['file']])
# Sibling saved result / log / scope documents; content is inert data.
paths=set()
for r in rows:
 p=(master/r['representative_path']).parent
 if p.name=='tests':p=p.parent
 for f in p.iterdir():
  if f.is_file() and f.suffix.lower() in ('.json','.csv','.log','.txt','.md','.sha256') and f.stat().st_size<120000 and f.name not in ['CONTENT_HASH_INVENTORY.json']:
   paths.add(f)
 if (p/'certificates').is_dir():paths.update((p/'certificates').glob('*.json'))
ev=[]
for i,p in enumerate(sorted(paths)):
 b=p.read_bytes();name=f'{i+1:03d}_{p.name}';dest='evidence/'+name;(out/dest).write_bytes(b);ev.append({'path':str(p),'sha256':sha(b),'bytes':len(b),'snapshot':dest})
(out/'EVIDENCE_MANIFEST.json').write_text(json.dumps(ev,indent=2));print('Evidence',len(ev),sum(e['bytes'] for e in ev))
# Resolve literal source import references by filesystem identity, without importing.
inv=json.loads((out/manifest['coverage_sources'][0]['snapshot']).read_text());byname=collections.defaultdict(list)
for ir in inv:
 for occ in ir['occurrences']:
  nm=pathlib.PurePosixPath(occ.get('path',occ.get('name',''))).name
  if nm.endswith('.py'):byname[nm].append((ir['sha256'],occ))
deps=[]
for r in rows:
 parent=(master/r['representative_path']).parent
 modules=set()
 for im in r.get('import_references',[]):
  if im.get('module'):modules.add(im['module'].split('.')[0])
  else:modules.update(n.split('.')[0] for n in im.get('names',[]))
 for m in sorted(modules):
  candidates=[]
  for p in [parent/(m+'.py'),parent.parent/(m+'.py')]:
   if p.is_file(): candidates.append({'path':str(p),'sha256':sha(p.read_bytes()),'resolution':'adjacent/package-parent literal file; runtime import not performed'})
  if not candidates and m+'.py' in byname:
   samearch={o.get('archive_sha256') for o in r['occurrences'] if o.get('archive_sha256')}
   cand={}
   for h,o in byname[m+'.py']:
    if o.get('archive_sha256') in samearch:cand.setdefault(h,[]).append(o)
   candidates=[{'sha256':h,'occurrences':os,'resolution':'same containing archive candidate only; runtime identity unresolved'} for h,os in cand.items()]
  deps.append({'source_index':r['source_index'],'source_sha256':r['sha256'],'module':m,'candidates':candidates,'kind':'project_dependency' if candidates else 'stdlib_or_external_or_unresolved','fully_read_here':any(c['sha256'] in wanted for c in candidates)})
(out/'DEPENDENCIES.json').write_text(json.dumps(deps,indent=2))
for d in deps:
 if d['candidates']:print('DEP',d['source_index'],d['module'],[(c['sha256'][:12],c['resolution'][:8]) for c in d['candidates']])
for e in ev:print('EV',e['snapshot'],e['bytes'])
