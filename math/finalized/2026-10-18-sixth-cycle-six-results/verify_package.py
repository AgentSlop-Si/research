"""Verify publication integrity and inert syntax. Never execute research programs."""
from pathlib import Path
import ast,hashlib,io,json,re,tarfile,zipfile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def load(path):return json.loads((ROOT/path).read_text())
def check_entry(root,e):
 path=e.get('path',e.get('file'));assert path and not Path(path).is_absolute() and '..' not in Path(path).parts,path
 p=root/path;b=p.read_bytes();assert sha(b)==e['sha256'],str(p)
 if 'bytes' in e:assert len(b)==e['bytes'],str(p)
 if 'git_blob_sha1' in e:assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha1']
def rows_of(d):
 if isinstance(d,list):return d
 for key in ('files','review_files','canonical_files'):
  if key in d:
   v=d[key];return [{'path':k,**x} for k,x in v.items()] if isinstance(v,dict) else v
 if d and all(isinstance(v,dict) and 'sha256' in v for v in d.values()):return [{'path':k,**x} for k,x in d.items()]
 return []
def inventory_rows(p):
 if p.suffix=='.sha256':return [{'path':ln.split(maxsplit=1)[1].removeprefix('./'),'sha256':ln.split(maxsplit=1)[0]} for ln in p.read_text().splitlines() if ln.strip()]
 return rows_of(json.loads(p.read_text()))
actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
expected=set(load('PRESERVATION_ALLOWLIST.json')['files']);assert actual==expected,{'missing':sorted(expected-actual),'extra':sorted(actual-expected)}
assert len(expected)==len(load('PRESERVATION_ALLOWLIST.json')['files'])
assert not any(p.is_symlink() for p in ROOT.rglob('*'))
manifest=load('MANIFEST.json');assert {e['path'] for e in manifest['files']}==actual-{'MANIFEST.json','SEAL.json'}
assert len(manifest['files'])==len(actual)-2
for e in manifest['files']:check_entry(ROOT,e)
seal=load('SEAL.json');assert seal['status']=='SEALED_LOCAL_PUBLICATION_PACKET' and seal['final_review_gate_passed']
for key,name in [('manifest_sha256','MANIFEST.json'),('allowlist_sha256','PRESERVATION_ALLOWLIST.json'),('final_acceptances_sha256','FINAL_ACCEPTANCES.json')]:assert seal[key]==sha((ROOT/name).read_bytes())
bind={e['path']:e for e in load('COPY_BINDINGS.json')['files']}
assert len(bind)==len(load('COPY_BINDINGS.json')['files'])
for path,e in bind.items():
 b=(ROOT/path).read_bytes();assert len(b)==e['public_bytes'] and sha(b)==e['public_sha256'],path
 assert e['byte_identical']==(e['original_sha256']==e['public_sha256'] and e['original_bytes']==e['public_bytes'])
 assert e['byte_identical'] or e['adaptations'],path
for inv in load('SOURCE_BINDINGS.json')['current_public_inventories']:
 p=ROOT/inv['path'];rr=inventory_rows(p);assert len(rr)==inv['rows']
 for e in rr:check_entry(p.parent,e)
accept=load('FINAL_ACCEPTANCES.json');assert accept['all_six_final_gates_passed'] and len(accept['acceptances'])==6
assert len({g['result'] for g in accept['acceptances']})==6
omitted={e['route']+'/'+e['path']:e for e in load('OMISSIONS.json')['omissions'] if 'route' in e}
for g in accept['acceptances']:
 assert g['verdict'].startswith(('ACCEPT','PASS','SCOPED'))
 for key,pathkey in [('original_candidate_manifest_sha256','original_candidate_integrity'),('original_review_manifest_sha256','original_review_integrity'),('public_candidate_report_sha256','public_candidate_report'),('public_review_report_sha256','public_review_report'),('public_verdict_sha256','public_verdict')]:assert sha((ROOT/g[pathkey]).read_bytes())==g[key],(g['result'],key)
 for role in ('candidate','review'):
  assert bind[g['public_'+role+'_report']]['original_sha256']==g['original_'+role+'_report_sha256']
 assert bind[g['public_verdict']]['original_sha256']==g['original_verdict_sha256']
 for key,route in [('original_candidate_integrity',g['result']+'/candidate'),('original_review_integrity',g['result']+'/review')]:
  for e in inventory_rows(ROOT/g[key]):
   rel=route+'/'+e.get('path',e.get('file'))
   if rel in bind:
    assert bind[rel]['original_sha256']==e['sha256'],rel
    if 'bytes' in e:assert bind[rel]['original_bytes']==e['bytes'],rel
   else:
    assert rel in omitted and omitted[rel]['sha256']==e['sha256'],rel
    if 'bytes' in e:assert omitted[rel]['bytes']==e['bytes'],rel
checks=load('PACKAGING_CHECKS.json');assert checks['status']=='PASS' and not checks['scientific_reruns'] and not checks['external_writes']
for path in checks['required_byte_identical_payloads']:assert bind[path]['byte_identical'],path
assert checks['proof_reports_and_reviews_byte_identical']
for e in load('SOURCE_PATH_ADAPTATION_VERIFICATION.json')['files']:
 b=(ROOT/e['path']).read_bytes();assert sha(b)==e['public_sha256'];s=b.decode()
 for x in reversed(e['substitutions']):assert s.count(x['new'])==x['occurrences'];s=s.replace(x['new'],x['old'])
 assert sha(s.encode())==e['original_sha256'] and e['reverse_substitution_byte_identical']
private_tokens=['docs.google.com/spreadsheets','library_file_id','sediment://','/agent_notes/','dream_notes']
secret_re=re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|\b(?:ghp_|github_pat_|sk-proj-)[A-Za-z0-9_]{12,}|\bAKIA[0-9A-Z]{16}\b')
def scan_text(label,b):
 try:s=b.decode('utf-8')
 except UnicodeDecodeError:return
 if label!='verify_package.py':assert not any(t in s for t in private_tokens) and not secret_re.search(s),label
 if label.endswith('.py'):ast.parse(s,filename=label)
for p in ROOT.rglob('*'):
 if p.is_file():scan_text(p.relative_to(ROOT).as_posix(),p.read_bytes())
for a in load('STATIC_CODE_AUDIT.json')['archives']:
 b=(ROOT/a['path']).read_bytes();assert sha(b)==a['sha256'];members=[]
 if a['path'].endswith(('.tar.gz','.tgz','.tar')):
  with tarfile.open(fileobj=io.BytesIO(b),mode='r:*') as z:
   for e in z.getmembers():
    assert not e.name.startswith('/') and '..' not in Path(e.name).parts and not e.issym() and not e.islnk()
    if e.isdir():continue
    assert e.isfile();raw=z.extractfile(e).read();members.append({'path':e.name,'bytes':len(raw),'sha256':sha(raw)});scan_text(a['path']+'!'+e.name,raw)
 else:
  with zipfile.ZipFile(io.BytesIO(b)) as z:
   for e in z.infolist():
    assert not e.filename.startswith('/') and '..' not in Path(e.filename).parts
    if e.is_dir():continue
    raw=z.read(e);members.append({'path':e.filename,'bytes':len(raw),'sha256':sha(raw)});scan_text(a['path']+'!'+e.filename,raw)
 assert members==a['members'] and not a['executed']
privacy=load('PRIVACY_REVIEW.json');assert privacy['status']=='PASS_PACKAGING_SCREEN' and not privacy['secrets_detected']
print(json.dumps({'status':'PASS','files':len(actual),'accepted_scoped_results':6,'scientific_reruns':False,'external_writes':False,'manifest_sha256':sha((ROOT/'MANIFEST.json').read_bytes())},indent=2))
