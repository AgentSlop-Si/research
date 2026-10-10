from pathlib import Path
import json,hashlib,shutil,datetime,re
B=Path('[local workspace]');W=B/'master_v26_integration_20261010';D=W/'fft_research_master_20261009';A=D/'additions/0536_final_static_review_closure';R=B/'post_v22_review_registry_0308'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def inv(p):return {str(x.relative_to(p)):{'bytes':x.stat().st_size,'sha256':sha(x)} for x in sorted(p.rglob('*')) if x.is_file()}
def verify(p,expected=None):
 out=[]
 for f in sorted(p.iterdir()):
  if not f.is_file() or f.name not in {'SHA256SUMS','SHA256SUMS.txt','MANIFEST.sha256','INPUTS.sha256'}:continue
  entries=[]
  for line in f.read_text().splitlines():
   m=re.match(r'^([0-9a-f]{64})\s+\*?(.+)$',line)
   if not m:raise ValueError((f,line))
   name=m[2];t=Path(name) if Path(name).is_absolute() else p/name
   assert t.is_file(),(f,name,'missing');assert sha(t)==m[1],(f,name,'mismatch')
   entries.append({'path':name,'sha256':m[1]})
  out.append({'file':f.name,'sha256':sha(f),'entries_verified':len(entries),'all_match':True})
 if expected:assert any(x['sha256']==expected for x in out),(p,'acceptance seal does not match')
 return out
receipts=[]; packs={}
for p in sorted(R.glob('POST25*.json')):
 d=json.loads(p.read_text());receipts.append({'name':p.name,'sha256':sha(p),'body':d});packs[d['package']]={'acceptance':p.name,'manifest_sha256':d.get('manifest_sha256')}
packs['final_publication_assessment_0538']={'status':'Root accepted publication assessment and ranking; not a new correctness or novelty certificate','manifest_sha256':'71db5c3a865ae80cc8d27a7803f904320c1167a462ecbdb41a0bd7ce09c03814'}
packs['pseudoforest_separator_research_0452']={'status':'historical author proposal; acceptance authority is independent audit'}
packs['private_research_inventory_0453']={'status':'previous verified private-inventory update receipt; historical 785-read sheet snapshot'}
report=[]
for name,meta in packs.items():
 s=B/name;dest=A/'packages'/name
 seals=verify(s,meta.get('manifest_sha256'));before=inv(s)
 if dest.exists():assert inv(dest)==before,(name,'existing staged bytes differ')
 else:shutil.copytree(s,dest)
 assert inv(dest)==before
 report.append({'name':name,'file_count':len(before),'bytes':sum(x['bytes'] for x in before.values()),'seals':seals,**meta})
stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S');dest=A/'registry_snapshots'/stamp;dest.mkdir()
for p in R.iterdir():
 if p.is_file() and p.suffix=='.json':shutil.copy2(p,dest/p.name)
coverage=json.loads((dest/'ADDITIVE_CODE_COVERAGE.json').read_text())
result={'status':'STAGED_ACCEPTED_PACKAGES_ONLY_NOT_FINAL','packages':report,'acceptance_receipts':receipts,'registry_snapshot':str(dest.relative_to(A)),'coverage_snapshot':{'full_static_reads':coverage['current_full_static_reads'],'complete_static_inspections':coverage['current_complete_static_inspections']},'awaiting':['root final count pin','root accepted closure audit','final packaging approval'],'canonical_modified':False,'uploads':False,'source_programs_executed':False}
(A/'STAGED_PACKAGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n');(W/'STAGED_PACKAGE_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'packages':len(report),'files':sum(p['file_count'] for p in report),'registry_snapshot':result['registry_snapshot'],'coverage_snapshot':result['coverage_snapshot']}))
