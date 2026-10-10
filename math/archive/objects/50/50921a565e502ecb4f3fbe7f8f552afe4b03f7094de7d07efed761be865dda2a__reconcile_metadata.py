"""Reviewer metadata reconciliation, reading source only as inert text."""
from pathlib import Path,PurePosixPath
import json,re,hashlib
O=Path(__file__).parent;R=Path('fft_research_master_20261009')
rows=json.load(open(O/'ASSIGNED_SOURCES.json'));provs=json.load(open(O/'PROVENANCE.json'));es=json.load(open(O/'EVIDENCE_INDEX.json'));E={e['sha256']:e for e in es}
G={a['sha256']:a for a in json.load(open('code_coverage_audit_0228/ARCHIVE_GRAPH.json'))}
imports=[];evidence_refs=[];manifests=[];mentions=[]
external={'__future__','collections','dataclasses','math','typing','numpy','scipy','fractions','pathlib','json','argparse','hashlib','random','time','itertools','decimal','numba','weakref','statistics','cmath','mpmath','sympy'}
for r,pv in zip(rows,provs):
 s=(O/'sources'/r['sha256']).read_text();mods=sorted(set(re.findall(r'^\s*from\s+([A-Za-z_]\w*)\b',s,re.M))-external)
 names=sorted(set(re.findall(r"['\"]([^'\"\n/]+\.(?:json|log|txt))['\"]",s)))
 context_records=[]
 if pv.get('archive_sha256'):
  a=G[pv['archive_sha256']];parent=PurePosixPath(pv['member']).parent; prefix='' if str(parent)=='.' else str(parent)+'/'
  candidates={m['name']:m for m in a['members']};ctx={'kind':'selected_archive','archive_sha256':a['sha256'],'source':pv['member'],'prefix':prefix,'members':[{k:m[k] for k in ('name','sha256','size_bytes')} for m in a['members'] if m['name'].startswith(prefix)]};context_records.append(ctx)
  imports.append({'index':r['index'],'sha256':r['sha256'],'context':'selected_archive','source':pv['member'],'imports':[{'module':m,'candidates':[{'name':n,'sha256':candidates[n]['sha256']} for n in [prefix+m+'.py',prefix+m+'/__init__.py'] if n in candidates],'runtime_import_resolution':'not executed'} for m in mods]})
 for c in pv['verified_standalone_contexts']:
  parent=Path(c['source_path']).parent;ms=[]
  for f in parent.rglob('*'):
   if f.is_file() and f.suffix in ('.py','.cpp','.cc','.h','.hpp','.sh','.json','.jsonl','.txt','.md','.csv','.log','.sha256'):
    ms.append({'name':str(f),'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'size_bytes':f.stat().st_size})
  context_records.append({'kind':'standalone','source':c['source_path'],'prefix':str(parent)+'/', 'members':ms})
 for ctx in context_records:
  hits=[m for m in ctx['members'] if m['name'] in [ctx['prefix']+n for n in names]]
  evidence_refs.append({'index':r['index'],'source_sha256':r['sha256'],'source':ctx['source'],'context_kind':ctx['kind'],'archive_sha256':ctx.get('archive_sha256'),'literal_result_or_data_names':names,'matching_exact_members':hits,'binding_caution':'File adjacency is historical context, not proof that this source produced that output.'})
 pv['evidence_contexts']=context_records
 # Dependency variants across all listed archive occurrences, metadata-only unless selected.
 variants=[]
 for o in r['occurrences']:
  if o.get('archive_sha256') not in G:continue
  pre=str(PurePosixPath(o['name']).parent);pre='' if pre=='.' else pre+'/'
  ms={m['name']:m for m in G[o['archive_sha256']]['members']}
  for m in mods:
   for nm in (pre+m+'.py',pre+m+'/__init__.py'):
    if nm in ms:variants.append({'module':m,'archive_sha256':o['archive_sha256'],'source_member':o['name'],'dependency_member':nm,'dependency_sha256':ms[nm]['sha256']})
 pv['dependency_archive_variants_metadata_only']=variants
# Manifest comparison uses source-adjacent contexts and records unmatched entries instead of guessing.
seen=set()
for pv in provs:
 for ctx in pv['evidence_contexts']:
  maps={m['name']:m for m in ctx['members']}
  for m in ctx['members']:
   name=m['name'];bn=PurePosixPath(name).name
   if m['sha256'] not in E or not ('manifest' in bn.lower() or 'sha256' in bn.lower() or 'checksums' in bn.lower()):continue
   key=(ctx.get('archive_sha256'),name,m['sha256'])
   if key in seen:continue
   seen.add(key);b=(O/E[m['sha256']]['local']).read_text();entries=[]
   if bn.endswith('.json'):
    try:j=json.loads(b)
    except Exception:continue
    v=j.get('files',j) if isinstance(j,dict) else j
    if isinstance(v,dict):
     for k,x in v.items():
      if isinstance(x,str) and re.fullmatch('[0-9a-f]{64}',x):entries.append((k,x))
      elif isinstance(x,dict) and isinstance(x.get('sha256'),str):entries.append((x.get('path',k),x['sha256']))
    elif isinstance(v,list):
     for x in v:
      if isinstance(x,dict) and isinstance(x.get('sha256'),str):entries.append((x.get('path',x.get('name','')),x['sha256']))
   else:
    for line in b.splitlines():
     z=re.match(r'^([0-9a-f]{64})\s+\*?(.+)$',line)
     if z:entries.append((z[2],z[1]))
   parent=str(PurePosixPath(name).parent);pre='' if parent=='.' else parent+'/'
   rec=[]
   for n,h in entries:
    actual=maps.get(pre+n)
    if actual:status='match' if actual['sha256']==h else 'mismatch'
    elif ctx['kind']=='standalone' and (Path(parent)/n).is_file():
     ah=hashlib.sha256((Path(parent)/n).read_bytes()).hexdigest();actual={'sha256':ah};status='match' if ah==h else 'mismatch'
    else:status='not_resolved_in_context'
    rec.append({'declared_name':n,'declared_sha256':h,'actual_sha256':actual['sha256'] if actual else None,'status':status})
   manifests.append({'manifest':name,'archive_sha256':ctx.get('archive_sha256'),'manifest_sha256':m['sha256'],'entries':rec})
for e in es:
 b=(O/e['local']).read_text(errors='replace');hit=[r['sha256'] for r in rows if r['sha256'] in b]
 if hit:mentions.append({'evidence_sha256':e['sha256'],'evidence_member':e['member'],'assigned_source_hashes_mentioned':hit})
(O/'PROVENANCE.json').write_text(json.dumps(provs,indent=2));(O/'DEPENDENCY_RECONCILIATION.json').write_text(json.dumps(imports,indent=2));(O/'STORED_RESULT_BINDINGS.json').write_text(json.dumps(evidence_refs,indent=2));(O/'STORED_MANIFEST_RECONCILIATION.json').write_text(json.dumps(manifests,indent=2));(O/'STORED_HASH_REFERENCE_RECONCILIATION.json').write_text(json.dumps(mentions,indent=2))
print('dependency source contexts',len(imports),'manifest contexts',len(manifests),'entries',sum(len(m['entries']) for m in manifests),'mismatches',sum(e['status']=='mismatch' for m in manifests for e in m['entries']),'unresolved',sum(e['status']=='not_resolved_in_context' for m in manifests for e in m['entries']))
print('DEPENDENCIES',json.dumps(imports,indent=2))
print('MISMATCHES',[(m['manifest'],e) for m in manifests for e in m['entries'] if e['status']=='mismatch'])
