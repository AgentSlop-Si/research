import pathlib,json,hashlib,datetime,shutil,collections
out=pathlib.Path('fusion_phase_source_review_0408'); base=pathlib.Path('code_coverage_audit_0228');root=pathlib.Path('[local workspace]')
def sha(b):return hashlib.sha256(b).hexdigest()
batches=['02_addition_2020_2027_02.json','02_addition_2020_2027_03.json','02_addition_2020_2027_04.json','02_addition_2044_01.json','02_addition_2115_01.json']
rows=[]; inputseals=[]
for n in batches:
 p=base/'pending_batches_v2'/n;b=p.read_bytes();(out/'inputs'/n).write_bytes(b);inputseals.append({'path':str(p),'sha256':sha(b),'snapshot':'inputs/'+n})
 for r in json.loads(b)['rows']:
  r['assigned_batch']=n;r['source_index']=len(rows)+1;b=pathlib.Path(r['local_content']).read_bytes();assert sha(b)==r['sha256']; name=f"{len(rows)+1:02d}_{pathlib.Path(r['representative_path']).name}"; (out/'sources'/name).write_bytes(b);r['snapshot']='sources/'+name;r['source_lines']=len(b.decode().splitlines());rows.append(r)
(out/'INPUT_ROWS.json').write_text(json.dumps(rows,indent=2))
paths=[base/'CODE_COVERAGE_INVENTORY.json',root/'post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json']+sorted(p for p in root.rglob('COVERAGE.json') if out not in p.parents)
seals=[]; unique={}
for i,p in enumerate(paths):
 b=p.read_bytes();h=sha(b);dest=f'baseline/{h}.json';(out/dest).write_bytes(b);seals.append({'path':str(p),'sha256':h,'size_bytes':len(b),'snapshot':dest});unique[h]=json.loads(b)
(out/'BASELINE_MANIFEST.json').write_text(json.dumps({'captured_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'inputs':inputseals,'coverage_sources':seals},indent=2))
print('Sources',len(rows),'bytes',sum(r['size_bytes'] for r in rows),'lines',sum(r['source_lines'] for r in rows),'baseline files',len(seals),'distinct',len(unique))
print('Inventory statuses',collections.Counter(r.get('coverage_status') for r in unique[seals[0]['sha256']]))
for h,d in unique.items():
 if isinstance(d,dict):print('BASEKEYS',h[:8],','.join(d.keys())[:450])
for r in rows:print(r['source_index'],r['snapshot'],r['source_lines'],r['sha256'][:12])
