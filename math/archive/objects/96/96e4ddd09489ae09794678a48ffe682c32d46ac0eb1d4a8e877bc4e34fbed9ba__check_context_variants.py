"""Fresh metadata-only exact-context comparison; does not interpret supplied source syntax."""
from pathlib import Path,PurePosixPath
import json,hashlib,zipfile,io,collections
O=Path(__file__).parent;M=Path('fft_research_master_20261009');rows=json.loads((O/'ASSIGNED_SOURCES.json').read_text());G={x['sha256']:x for x in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))};H=lambda b:hashlib.sha256(b).hexdigest();ev=json.loads((O/'EVIDENCE_INDEX.json').read_text());byh={e['sha256']:e for e in ev};contexts={};seals=[]
def save(b,name,origin):
 h=H(b)
 if h not in byh:
  local='evidence/'+h+'__'+Path(name).name;(O/local).write_bytes(b);rec={'sha256':h,'size_bytes':len(b),'local':local,'origins':[]};ev.append(rec);byh[h]=rec
 byh[h]['origins'].append(origin)
 return h
def entries(b):
 a=json.loads(b);x=a.get('files',{})
 if isinstance(x,dict):return [(k,v if isinstance(v,str) else v.get('sha256'))for k,v in x.items()]
 return [(r.get('path',r.get('name')),r.get('sha256'))for r in x]
# Every standalone occurrence context, even reused utility/replay sources.
for i,r in enumerate(rows):
 for occ in r['occurrences']:
  if occ['kind']!='master_standalone':continue
  context=(M/occ['path']).parent;key='master:'+str(context.relative_to(M))
  if key in contexts:contexts[key]['source_indices'].append(i);continue
  item={'kind':'master_context','directory':str(context.relative_to(M)),'source_indices':[i],'immediate_sibling_hashes':[]}
  for p in sorted(context.iterdir()):
   if p.is_file() and (p.suffix in ['.py','.json','.gz','.sha256'] or p.name.startswith('SHA256')):
    b=p.read_bytes();item['immediate_sibling_hashes'].append({'name':p.name,'sha256':H(b),'size_bytes':len(b),'bytes_verified':True,'source_read_credit':False})
    if p.name=='SEALED_MANIFEST.json':
     save(b,p.name,{'kind':'all_master_context_seal','path':str(p.relative_to(M))});ss=[]
     for name,h in entries(b):
      t=p.parent/name
      if t.is_file() and t.resolve().is_relative_to(M):actual=H(t.read_bytes());ss.append({'name':name,'expected':h,'actual':actual,'match':actual==h})
      else:ss.append({'name':name,'expected':h,'actual':None,'match':False})
     seals.append({'context':key,'manifest_sha256':H(b),'entries':ss})
  contexts[key]=item
# Archive membership is addressed by member index; duplicate filenames do not imply identity.
byarchive=collections.defaultdict(list)
for i,r in enumerate(rows):
 for o in r['occurrences']:
  if o['kind']=='archive_member':byarchive[o['archive_sha256']].append((i,o))
for h,occurrences in byarchive.items():
 parts=G[h]['first_observed_at'].split('!');assert len(parts)==1
 p=M/parts[0];assert H(p.read_bytes())==h
 with zipfile.ZipFile(p) as z:
  infos=z.infolist();byname=collections.defaultdict(list)
  for inf in infos:byname[inf.filename].append(inf)
  for i,o in occurrences:
   folder=str(PurePosixPath(o['name']).parent);key=h+':'+folder
   if key in contexts:contexts[key]['source_indices'].append(i);continue
   item={'kind':'archive_context','archive_sha256':h,'directory':folder,'source_indices':[i],'immediate_sibling_hashes':[]}
   for inf in infos:
    if inf.is_dir() or str(PurePosixPath(inf.filename).parent)!=folder:continue
    name=PurePosixPath(inf.filename).name
    if PurePosixPath(name).suffix not in ['.py','.json','.gz','.sha256'] and not name.startswith('SHA256'):continue
    b=z.read(inf);item['immediate_sibling_hashes'].append({'name':name,'member_index':infos.index(inf),'sha256':H(b),'size_bytes':len(b),'bytes_verified':True,'source_read_credit':False})
    if name=='SEALED_MANIFEST.json':
     save(b,name,{'kind':'archived_context_seal','archive_sha256':h,'member':inf.filename});ss=[]
     for name,expected in entries(b):
      target=str(PurePosixPath(folder)/name);matches=byname.get(target,[])
      actual=[H(z.read(inf)) for inf in matches];ss.append({'name':name,'expected':expected,'actual_sha256s':actual,'match':len(actual)==1 and actual[0]==expected,'duplicate_path_count':len(actual)})
     seals.append({'context':key,'manifest_sha256':H(b),'entries':ss})
   contexts[key]=item
for v in contexts.values():v['source_indices']=sorted(set(v['source_indices']))
(O/'ALL_CONTEXT_VARIANTS.json').write_text(json.dumps(list(contexts.values()),indent=2)+'\n');(O/'ALL_CONTEXT_SEAL_RECONCILIATION.json').write_text(json.dumps(seals,indent=2)+'\n');(O/'EVIDENCE_INDEX.json').write_text(json.dumps(ev,indent=2)+'\n')
print('contexts',len(contexts),'seals',len(seals),'entries',sum(len(s['entries']) for s in seals),'mismatches',sum(not e['match'] for s in seals for e in s['entries']))
