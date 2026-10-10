import pathlib,json,hashlib,shutil
p=pathlib.Path(__file__).parent;a=pathlib.Path('next_review_assignment_0456_b/ASSIGNMENT.json');assignment=json.loads(a.read_text()); rows=[]
shutil.copyfile(a,p/'ASSIGNMENT_SNAPSHOT.json')
for name in assignment['batch_names']:
 f=pathlib.Path(assignment['batch_directory'])/name;shutil.copyfile(f,p/'provenance/assigned_batches'/name)
 for item in json.loads(f.read_text())['rows']:
  r=dict(item);r['batch_name']=name;r['index']=len(rows)+1;raw=pathlib.Path(r['local_content']).read_bytes();assert hashlib.sha256(raw).hexdigest()==r['sha256'];assert len(raw)==r['size_bytes'];r['line_count']=len(raw.splitlines());(p/'sources'/r['sha256']).write_bytes(raw);rows.append(r)
(p/'SOURCE_MANIFEST.json').write_text(json.dumps(rows,indent=2)+'\n')
shutil.copyfile('post_v22_review_registry_0308/ADDITIVE_CODE_COVERAGE.json',p/'REGISTRY_BEFORE.json')
for name in ['CODE_COVERAGE_INVENTORY.json','SEAL.json','SHA256SUMS.txt','ARCHIVE_ROOTS.json']:
 shutil.copyfile('code_coverage_audit_0228/'+name,p/'provenance'/name)
print('Prepared',len(rows),'sources',sum(r['size_bytes'] for r in rows),'bytes',sum(r['line_count'] for r in rows),'lines')
