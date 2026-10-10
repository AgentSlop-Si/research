"""New reviewer-authored bytes-only provenance/evidence checks. Never executes/parses supplied programs."""
from pathlib import Path, PurePosixPath
import json,hashlib,zipfile,io,re
OUT=Path(__file__).parent
MASTER=Path('fft_research_master_20261009')
AUDIT=Path('code_coverage_audit_0228')
rows=json.loads((OUT/'ASSIGNED_SOURCES.json').read_text())
G={a['sha256']:a for a in json.loads((AUDIT/'ARCHIVE_GRAPH.json').read_text())}
H=lambda b:hashlib.sha256(b).hexdigest()
cache={};archives=[];prov=[];evidence={};manifests=[];deps=[]
def archive(h):
 if h not in cache:
  a=G[h];parts=a['first_observed_at'].split('!');b=(MASTER/parts[0]).read_bytes()
  for part in parts[1:]:
   with zipfile.ZipFile(io.BytesIO(b)) as z:b=z.read(part)
  assert H(b)==h;cache[h]=b;archives.append({'sha256':h,'size_bytes':len(b),'first_observed_at':a['first_observed_at'],'verified':True})
 return cache[h]
def save_ev(b,path,origin):
 h=H(b);key=h+'__'+Path(path).name;local='evidence/'+key
 if not (OUT/local).exists():(OUT/local).write_bytes(b)
 if h not in evidence:evidence[h]={'sha256':h,'size_bytes':len(b),'local':local,'origins':[]}
 evidence[h]['origins'].append(origin)
 return h
for i,r in enumerate(rows):
 pp={'index':i,'sha256':r['sha256'],'representative_path':r['representative_path'],'occurrences':[],'historical_origin_class':r['origin_class'],'historical_evidence_ids':r.get('evidence_ids',[]),'source_bytes_verified':True}
 for o in r['occurrences']:
  rec=dict(o)
  if o['kind']=='master_standalone':
   f=MASTER/o['path'];b=f.read_bytes();assert H(b)==r['sha256'];rec.update(byte_identity_verified=True,local=str(f))
  elif o['kind']=='archive_member':
   h=o['archive_sha256'];raw=archive(h)
   with zipfile.ZipFile(io.BytesIO(raw)) as z:
    info=z.infolist()[o['member_index']];assert info.filename==o['name'];b=z.read(info);assert H(b)==r['sha256'];rec.update(byte_identity_verified=True,archive_first_observed_at=G[h]['first_observed_at'])
  else:rec['verification']='unsupported occurrence kind; recorded only'
  pp['occurrences'].append(rec)
 f=MASTER/r['representative_path'];context=f.parent
 ev=[]
 for e in sorted(context.rglob('*')):
  if not e.is_file() or e.suffix.lower() in ('.py','.pyc','.zip','.cpp','.cc','.c','.h','.hpp','.js','.ts','.sh'):continue
  if e.suffix.lower() not in ('.json','.jsonl','.txt','.md','.csv','.log') and not e.name.startswith('SHA256'):continue
  b=e.read_bytes();origin={'kind':'master_context','path':str(e.relative_to(MASTER)),'source_index':i}
  ev.append(save_ev(b,e.name,origin))
  if e.name=='SEALED_MANIFEST.json':
   try:
    obj=json.loads(b);checks=[]
    entries=obj.get('files',{}); entries=entries.items() if isinstance(entries,dict) else [(x.get('path',x.get('name')),x.get('sha256')) for x in entries]
    for name,h in entries:
     target=e.parent/name
     if not target.resolve().is_relative_to(MASTER.resolve()):checks.append({'name':name,'status':'outside_master_not_read'});continue
     actual=H(target.read_bytes()) if target.is_file() else None;checks.append({'name':name,'expected':h,'actual':actual,'match':actual==h})
    manifests.append({'manifest':str(e.relative_to(MASTER)),'sha256':H(b),'source_index':i,'entries':checks,'interpretation':'Historical file integrity only, no proof/execution acceptance.'})
   except (ValueError,KeyError,TypeError,AttributeError) as ex:manifests.append({'manifest':str(e),'error':str(ex)})
 pp['context_evidence_hashes']=sorted(set(ev));prov.append(pp)
 text=(OUT/'sources'/r['sha256']).read_text()
 references=[]
 for ln,line in enumerate(text.splitlines(),1):
  if re.match(r'\s*(from|import)\s',line):references.append({'line':ln,'text':line.strip(),'kind':'lexical_import'})
  for absref in re.findall(r"['\"](/workspace/[^'\"]+)['\"]",line):
   p=Path(absref);b=p.read_bytes() if p.is_file() else None;references.append({'line':ln,'path':absref,'kind':'absolute_path','exists':b is not None,'sha256':H(b) if b is not None else None,'assigned_source':H(b) in {x['sha256'] for x in rows} if b is not None else None})
  for name in re.findall(r"['\"]([^'\"]+\.py)['\"]",line):
   if name.startswith('/'):continue
   p=context/name;references.append({'line':ln,'kind':'relative_program_reference','name':name,'context_candidate':str(p),'exists':p.is_file(),'sha256':H(p.read_bytes()) if p.is_file() else None})
 for ref in references:
  if ref['kind']=='lexical_import':
   m=re.match(r'from\s+([A-Za-z_]\w*)\s+import|import\s+([A-Za-z_]\w*)',ref['text'])
   if m:
    mod=m.group(1) or m.group(2);p=context/(mod+'.py')
    if p.is_file():ref.update(sibling_candidate=str(p),sibling_sha256=H(p.read_bytes()),resolution='exact sibling bytes verified; runtime sys.path not executed')
 deps.append({'source_index':i,'sha256':r['sha256'],'references':references,'runtime_import_closure_complete':False})
 print('source',i,'occurrences',len(pp['occurrences']),'evidence',len(set(ev)),flush=True)
# Preserve historical declarations with their byte identity, without promoting their claims.
E=json.loads((AUDIT/'COVERAGE_EVIDENCE.json').read_text());wanted={eid for r in rows for eid in r.get('evidence_ids',[])};historical=[]
for e in E:
 if e['id'] not in wanted:continue
 doc=AUDIT/e['portable_document'];b=doc.read_bytes();assert H(b)==e['document_sha256'];localhash=save_ev(b,doc.name,{'kind':'historical_coverage_declaration','id':e['id'],'document':e['document']});historical.append({**e,'document_byte_identity_verified':True,'fresh_execution_or_proof_credit':False,'evidence_snapshot_sha256':localhash})
for name,obj in [('PROVENANCE.json',prov),('ARCHIVE_VERIFICATION.json',archives),('EVIDENCE_INDEX.json',list(evidence.values())),('STORED_MANIFEST_RECONCILIATION.json',manifests),('DEPENDENCY_RECONCILIATION.json',deps),('HISTORICAL_RECEIPT_RECONCILIATION.json',historical)]:
 (OUT/name).write_text(json.dumps(obj,indent=2)+'\n')
print('DONE',len(prov),len(archives),len(evidence),sum(x['size_bytes'] for x in evidence.values()),len(manifests),len(historical))
