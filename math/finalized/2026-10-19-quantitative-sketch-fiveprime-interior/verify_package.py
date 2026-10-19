"""Read-only source integrity and scope verifier; never imports research code."""
from pathlib import Path
import hashlib,json,sys,base64,gzip
ROOT=Path(__file__).resolve().parent
ANCHORS={
'alg076/candidate/MANIFEST.json':'35106552ca46ffa2684814a47aa79ef76a03182d20fd3470bdd4a7df637717ca',
'alg076/review/REVIEW_MANIFEST.json':'4f6f4589b1e23ab6dc29e38492e6c81f6705d9579b06da093e062b56566dbb59',
'fiveprime/candidate/MANIFEST.json':'3764006c03cc895ea71d44764391867c17490957a2734007cb52a0b85b04650a',
'fiveprime/review/MANIFEST.json':'62940d93e3e48331b6255bbef1e2fef8f9a63b48b5b0b312bfdc1acf0d5111ed'}
LARGE='fiveprime/candidate/NEGATIVE_CONTROLS.json'
ENCODED=LARGE+'.gz.base64'
LARGE_HASH='f273537a04ec5b1a543133d25fe784871451da81830c7aae112a70a29d74bfdd'
ENCODED_HASH='e545bcc328a3dbd086b758ee17fa4281e0dace879c0ee50142c77ddb24d80897'
OMITTED='alg076/candidate/sources/OWNER_RECORD.json'
OMITTED_HASH='1e4a6106d425e2f7f4538752555827323c623e0e8ad3669d43c1dbec8698c5c3'
def require(ok,message):
 if not ok: raise ValueError(message)
def safe(name):
 require(isinstance(name,str) and name!='','Empty or nontext path')
 p=Path(name)
 require(not p.is_absolute() and '..' not in p.parts and str(p)==name,'Unsafe path: '+name)
 return ROOT/p
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(name): return json.loads(safe(name).read_text())
def matches(p,row): return p.is_file() and not p.is_symlink() and p.stat().st_size==row['bytes'] and h(p)==row['sha256']
def decoded_large():
 data=safe(ENCODED).read_bytes()
 require(len(data)==498413 and hashlib.sha256(data).hexdigest()==ENCODED_HASH,'Encoded controls changed')
 compressed=base64.b64decode(b''.join(data.split()),validate=True)
 require(len(compressed)==368954,'Compressed controls size changed')
 original=gzip.decompress(compressed)
 require(len(original)==27522877 and hashlib.sha256(original).hexdigest()==LARGE_HASH,'Decoded original controls changed')
 return original
def logical_matches(name,row):
 if name==LARGE:
  d=decoded_large(); return len(d)==row['bytes'] and hashlib.sha256(d).hexdigest()==row['sha256']
 return matches(safe(name),row)
def verify():
 paths=list(ROOT.rglob('*'))
 require(not any(p.is_symlink() for p in paths),'Symlink in packet')
 allow=read('PRESERVATION_ALLOWLIST.json')['files']
 require(allow==sorted(set(allow)),'Duplicate or unsorted allowlist')
 for name in allow: safe(name)
 require(sorted(str(p.relative_to(ROOT)) for p in paths if p.is_file())==allow,'Exact allowlist mismatch')
 manifest=read('MANIFEST.json'); rows=manifest['files']; names=[r['path'] for r in rows]
 require(len(names)==len(set(names)),'Duplicate manifest entry')
 require(set(names)==set(allow)-{'MANIFEST.json','SEAL.json'},'Manifest coverage mismatch')
 for r in rows: require(matches(safe(r['path']),r),'Manifest bytes mismatch: '+r['path'])
 seal=read('SEAL.json')
 for filename,key in [('MANIFEST.json','manifest_sha256'),('PRESERVATION_ALLOWLIST.json','allowlist_sha256'),('FINAL_ACCEPTANCE.json','acceptance_sha256'),('OWNER_DISPOSITIONS.json','owner_dispositions_sha256'),('OMISSIONS.json','omissions_sha256')]:
  require(h(safe(filename))==seal[key],'Seal mismatch: '+filename)
 for name,digest in ANCHORS.items(): require(h(safe(name))==digest,'Original source anchor changed: '+name)
 omissions=read('OMISSIONS.json')['omitted_manifest_declared_files']
 require(len(omissions)==1 and omissions[0]['public_path']==OMITTED,'Unexpected omission set')
 omission=omissions[0]
 require(omission['sha256']==OMITTED_HASH and omission['bytes']==1566,'Wrong private omission receipt')
 require(not safe(OMITTED).exists(),'Private administrative file included')
 require(omission['public_replacement'] is None,'Silent replacement of omitted source')
 cb=read('COPY_BINDINGS.json'); copies={r['public_path']:r for r in cb['files']}
 require(len(copies)==len(cb['files'])==63,'Copy count or duplicate copy mismatch')
 expected_copies=set()
 for r in cb['files']:
  p=safe(r['public_path']); require(r['transformation']=='EXACT_COPY','Source transformation')
  require(p.stat().st_size==r['source_bytes']==r['public_bytes'],'Copy size mismatch')
  require(h(p)==r['source_sha256']==r['public_sha256'],'Copy hash mismatch')
 require(len(cb['source_sets'])==4,'Wrong source-set count')
 seen=[]
 for s in cb['source_sets']:
  prefix=s['public_prefix']; mp=s['manifest_path']; seen.append(mp)
  require(mp in ANCHORS and s['manifest_sha256']==ANCHORS[mp],'Unknown source anchor')
  expected_copies.add(mp)
  entries=read(mp)['files']; require(len(entries)==s['manifest_entries'],'Source manifest entry count')
  require(len(entries)==len({x['path'] for x in entries}),'Duplicate original source entry')
  for entry in entries:
   publicpath=prefix+'/'+entry['path']; safe(publicpath)
   if publicpath==OMITTED:
    require(entry['sha256']==omission['sha256'] and entry['bytes']==omission['bytes'],'Omission does not match original manifest')
   else:
    if publicpath!=LARGE: expected_copies.add(publicpath)
    require(logical_matches(publicpath,entry),'Incomplete manifested source: '+publicpath)
  require(s['public_manifest_omissions']==([OMITTED] if prefix=='alg076/candidate' else []),'Wrong source omission accounting')
  require(s['losslessly_represented_files']==([LARGE] if prefix=='fiveprime/candidate' else []),'Wrong lossless source accounting')
  require(s['locally_preserved_manifest_payload_complete'] is True,'Local preservation disclosure absent')
  for extra in s['extra_bound_files']:
   publicpath=prefix+'/'+extra; expected_copies.add(publicpath)
   require(extra=='SEAL.sha256','Unexpected source extras')
   require(safe(publicpath).read_text().split()[0]==s['manifest_sha256'],'Original seal mismatch')
 require(set(seen)==set(ANCHORS),'Missing or repeated primary source set')
 require(set(copies)==expected_copies,'Exact source copy coverage mismatch')
 # Validate unchanged manifest/report copies inside the final reviews.
 for a,b in [('alg076/candidate/MANIFEST.json','alg076/review/CANDIDATE_MANIFEST.json'),('alg076/candidate/REPORT.md','alg076/review/REVIEWED_REPORT.md'),('fiveprime/candidate/MANIFEST.json','fiveprime/review/CANDIDATE_MANIFEST.json'),('fiveprime/candidate/SOURCE_BINDINGS.json','fiveprime/review/CANDIDATE_SOURCE_BINDINGS.json')]:
  require(safe(a).read_bytes()==safe(b).read_bytes(),'Review/candidate binding copy differs')
 for entry in read('alg076/candidate/SOURCE_BINDINGS.json')['source_files']:
  name='alg076/candidate/'+entry['file']
  require((entry['sha256']==OMITTED_HASH and entry['bytes']==1566) if name==OMITTED else matches(safe(name),entry),'Sketch source binding mismatch')
 for entry in read('fiveprime/candidate/SOURCE_BINDINGS.json'):
  require(matches(safe('fiveprime/candidate/'+entry['copy']),entry),'Sparse source binding mismatch')
 ar=read('alg076/review/VERDICT.json'); fr=read('fiveprime/review/VERDICT.json')
 require(ar['verdict']=='SCOPED_PASS' and fr['verdict']=='PASS','Scientific review is not accepted')
 require(ar['required_repairs']==fr['required_repairs']==[],'Unresolved scientific repairs')
 for key,prefix,v in [('alg076','alg076',ar),('fiveprime','fiveprime',fr)]:
  require(v['candidate_manifest_sha256']==h(safe(prefix+'/candidate/MANIFEST.json')),'Review manifest binding changed')
  require(v['candidate_report_sha256']==h(safe(prefix+'/candidate/REPORT.md')),'Review proof binding changed')
  item=read('FINAL_ACCEPTANCE.json')['results'][key]
  require(item['verdict']==v['verdict'],'Acceptance verdict changed')
  for field in ('candidate_manifest','review_manifest','proof','review','verdict'):
   require(h(safe(item[field+'_path']))==item[field+'_sha256'],'Acceptance file binding failed')
 scope=read('CLAIM_SCOPE.json'); a=scope['alg076']; f=scope['fiveprime']
 require(a['measurement']=='input-independent complex linear L_omega with independent seed omega and complex rank r_omega<=k<N','Sketch model broadened')
 require(a['gaussian']=='CN(0,I_N), E|X_j|^2=1, real and imaginary variance 1/2','Gaussian normalization changed')
 require(a['absolute_bound']=='P(||g-U X||_2<=a)<=E G_(N-r_omega)(a^2)<=G_(N-k)(a^2)','Absolute bound changed')
 require(a['rank_necessity']=='liminf k_N/N>=1-epsilon^2 for fixed 0<epsilon<1 and uniform success bounded away from zero for Lebesgue-almost-every input','Rank scope broadened')
 require(a['relative_bound_sharpness_claim'] is False and a['rank_sufficiency_claim'] is False and a['exact_endpoint_is_inherited'] is True,'Invalid sketch extension')
 require(f['N']=='5q' and f['q_condition']=='q prime >=11' and f['degree_range']=='integer q<d<2q','Fiveprime quantifiers broadened')
 require(f['q7_control']=='7-by-35 rectangular row block, degree11, row Gram11 I7; not a square equality mask','q7 control misrepresented')
 for flag in ('q7_square_result_established','middle_interval_covered','full_fiveprime_classification','full_support_classification','new_optimal_gap_rate'): require(f[flag] is False,'Invalid fiveprime extension: '+flag)
 require(f['inherited_quantitative_gap']=='Delta_(5q,5q-d)^2>=d/(5q)+1/[50*q*d^(4*q-5)]','Inherited gap changed')
 for flag in ('historical_novelty_claim','world_first_claim','general_fft_gain_claim','scientific_reruns_during_packaging'): require(scope[flag] is False,'Improper publication claim: '+flag)
 owners=read('OWNER_DISPOSITIONS.json')
 require(set(owners['owners'])=={'ALG-076','M-SPARSE-DEFECT'},'Wrong owner set')
 for o in owners['owners'].values(): require(o['status']=='TO RESEARCH' and o['priority']==42 and o['owner_closure'] is False and o['priority_change'] is False,'Owner closure or priority change')
 for key in ('owner_closures','priority_changes','status_changes','discovery_count_change'): require(owners[key]==0,'Owner accounting change')
 require(owners['canonical_records_modified'] is False and owners['scores_changed'] is False,'External owner changes')
 # Privacy scan is supplementary to exact path/content inventory, not a claim of universal secret detection.
 forbidden=[b'docs.google.com/spreadsheets',b'X-Amz-Signature=',b'Authorization: Bearer ']
 for name in allow:
  if name=='verify_package.py': continue
  data=safe(name).read_bytes()
  require(not any(x in data for x in forbidden),'Known private identifier/category in payload: '+name)
 large=read('LARGE_FILE_NOTICE.json')['files']
 require(len(large)==1 and large[0]['path']==ENCODED,'Large scientific file omitted or representation changed')
 require(matches(safe(large[0]['path']),large[0]),'Encoded scientific file changed')
 require(not safe(LARGE).exists(),'Undeclared raw large-file duplicate')
 rep=read('LOSSLESS_REPRESENTATIONS.json')['files']
 require(len(rep)==1 and rep==cb['lossless_representations']==read('OMISSIONS.json')['losslessly_represented_manifest_files'],'Lossless representation ledgers disagree')
 r=rep[0]
 require(r['logical_original_path']==LARGE and r['representation_path']==ENCODED and r['transformation']=='LOSSLESS_GZIP_BASE64' and r['is_exact_public_byte_copy'] is False,'Representation misdeclared as exact copy')
 require(r['original_sha256']==LARGE_HASH and r['original_bytes']==27522877 and r['encoded_sha256']==ENCODED_HASH and r['encoded_bytes']==498413 and r['gzip_bytes']==368954,'Lossless representation receipt wrong')
 decoded_large()
 return {'status':'PASS','public_files':len(allow),'exact_source_copies':len(copies),'source_sets':4,'explicit_private_omissions':1,'lossless_scientific_representations':1,'scientific_code_executed':False}
if __name__=='__main__':
 try: print(json.dumps(verify(),indent=2))
 except Exception as e:
  print(json.dumps({'status':'FAIL','error':str(e)})); sys.exit(1)
