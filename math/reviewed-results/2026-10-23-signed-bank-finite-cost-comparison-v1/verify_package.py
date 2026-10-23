"""Check publication bytes and nested evidence integrity; never execute research code."""
from pathlib import Path, PurePosixPath
import hashlib, io, json, zipfile
ROOT=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
checks=0;archives=0;member_counts=[]
def ck(ok,label):
 global checks
 checks+=1
 if not ok:raise AssertionError(label)
def match(data,entry,label):
 ck(len(data)==entry['bytes'],label+' size');ck(sha(data)==entry['sha256'],label+' sha256')
def readzip(data,label,manifest=None):
 global archives
 archives+=1
 z=zipfile.ZipFile(io.BytesIO(data));names=z.namelist();ck(len(set(names))==len(names),label+' unique names')
 for n in names:ck(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts,label+' safe member '+n)
 ck(z.testzip() is None,label+' ZIP CRCs');member_counts.append({'archive':label,'members':len(names)})
 if manifest:
  a=manifest['archive'];match(data,a,label)
  entries=a['members'];ck(set(names)=={x['path'] for x in entries},label+' complete members')
  for x in entries:match(z.read(x['path']),x,label+'/'+x['path'])
  for x in manifest.get('projection',{}).get('source_correspondence',[]):
   name=x['archive_path']
   if x['public'] is None:ck(name not in names,label+' omitted binary '+name)
   else:
    match(z.read(name),x['public'],label+' projected '+name)
    if x['disposition']=='byte-exact':ck(x['original']==x['public'],label+' byte exact '+name)
  for x in manifest.get('direct_science_copies',[]):
   if label=='evidence.zip':ck((ROOT/x['path']).read_bytes()==z.read(x['archive_path']),'direct science '+x['path'])
 for name in names:
  if name.endswith('/evidence.zip'):
   parent=name.rsplit('/',1)[0];mp=parent+'/PUBLIC_MANIFEST.json';child_manifest=json.loads(z.read(mp)) if mp in names else None
   readzip(z.read(name),label+'!'+name,child_manifest)
 return z
m=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
for e in m['direct_files']:match((ROOT/e['path']).read_bytes(),e,e['path'])
chunks=[];off=0
for e in m['archive']['parts']:
 b=(ROOT/e['path']).read_bytes();match(b,e,e['path']);ck(len(b)<=409600,'raw part limit');ck(e['offset']==off,'part offset');off+=len(b);chunks.append(b)
z=readzip(b''.join(chunks),'evidence.zip',m)
# Specific scope controls, from stored records only.
final=json.loads(z.read('cost_author/RESULT.json'));first=json.loads(z.read('cost_author/RESULT_INITIAL_TIMING.json'))
for label,result in [('final',final),('first',first)]:
 ck(result['status']=='PASS',label+' recorded status')
 ck(all(len(v)==7 for v in result['timing_ns_per_complete_transform'].values()),label+' all raw batches retained')
ck(z.read('cost_author/benchmark.cpp').find(b'volatile uint64_t sink')>=0,'source output consumption retained')
tests=json.loads(z.read('cost_author/EXACT_TESTS.json'));ck(len(tests['inputs'])==len(tests['expected_outputs'])==8,'all recorded test vectors retained')
fixture=zipfile.ZipFile(io.BytesIO(z.read('dependencies/fixture/evidence.zip')));inverse=fixture.read('finite_author/RESOLVENT_INVERSES.u8');ck(len(inverse)==4828736,'full uint8 archive');ck(sha(inverse)=='6b3852380804f9a1a7d1f9f343af06b11f1dd2edc141f5e2f2e8c92213435bd6','uint8 archive hash')
for name in z.namelist():
 if name.startswith(('cost_author/','cost_review/')):
  ck(b'/workspace/' not in z.read(name),'no machine absolute locator '+name)
print(json.dumps({'status':'PASS_PACKAGE_INTEGRITY_ONLY','checks':checks,'archives':archives,'archive_member_counts':member_counts,'scientific_programs_executed':False,'timings_rerun':False,'timings_independently_reproduced':False,'full_uint8_archive_bytes':len(inverse)},indent=2))
