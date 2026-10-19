#!/usr/bin/env python3
"""Read-only package verification; optional mathematical replay in a temporary copy."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parent
GIT_ROOT='math/finalized/2026-10-19-rectangle-3757-rank-three'
SCIENCE_PINS={
 'rectangle/candidate/REPORT.md':'034371f74e7e0797ada08ec208a7b31ff3a77bc128eaf31d0adefa98aaa5df2a',
 'rectangle/candidate/check_target.py':'095c9a5400bde83f31bfed923f787abda0031ee7855530d865160dcc65eac16b',
 'rectangle/candidate/MANIFEST.json':'25fd01c88af8eff922d5a4799337636bc4bebe8d5daf15cdc0a59d6d0b29a1d1',
 'rectangle/review/independent_controls.py':'0595bc9fb7d17d799644fb330de6d138a6b98c9862d9a256ca34f6deb01cde84',
 'provenance/review/REVIEW.md':'8ab17f529fad9034bfe9656beb27940cfe3cf32710d60474b771c515ef337094',
 'provenance/review/REVIEW_PINS.json':'974eb1e77c99b715254291ba37ed6ea293e2d7a342fb1cf34da590cfe635f553',
}

def require(ok,message):
 if not ok:raise ValueError(message)
def sha(data):return hashlib.sha256(data).hexdigest()
def read(name):return json.loads((ROOT/name).read_text())
def safe(name):
 p=Path(name)
 require(not p.is_absolute() and '..' not in p.parts and str(p)==name,'unsafe path: '+name)
 return p

def check_manifest(base,manifest):
 files=manifest['files']
 for name,expected in files.items():
  safe(name);p=base/name
  require(p.is_file() and not p.is_symlink(),'missing or linked file: '+name)
  data=p.read_bytes()
  require(len(data)==expected['bytes'] and sha(data)==expected['sha256'],'byte mismatch: '+name)
 return len(files)

def verify():
 all_paths=list(ROOT.rglob('*'))
 require(not any(p.is_symlink() for p in all_paths),'symlinks are forbidden')
 actual={str(p.relative_to(ROOT)) for p in all_paths if p.is_file()}
 manifest=read('MANIFEST.json')
 require(actual==set(manifest['files'])|{'MANIFEST.json'},'file inventory differs from manifest')
 count=check_manifest(ROOT,manifest)
 allow=read('GIT_PATH_ALLOWLIST.json')
 require(allow['git_root']==GIT_ROOT,'wrong Git root')
 require(allow['paths']==sorted(GIT_ROOT+'/'+p for p in actual),'Git path allowlist differs')
 require(allow['external_writes_performed'] is False,'unexpected write claim')
 for name,expected in SCIENCE_PINS.items():require(sha((ROOT/name).read_bytes())==expected,'accepted science changed: '+name)

 for folder in ['rectangle/candidate','rectangle/review']:
  check_manifest(ROOT/folder,read(folder+'/MANIFEST.json'))
 original_review=read('provenance/review/ORIGINAL_MANIFEST.json')
 projections=read('PROJECTION_DISCLOSURE.json')
 require(projections['mathematical_changes'] is False and projections['program_changes'] is False,'unexpected projection scope')
 require(len(projections['projections'])==2,'projection count')
 projected_names=set()
 for entry in projections['projections']:
  original=(ROOT/entry['original_path']).read_bytes()
  current=(ROOT/entry['path']).read_bytes()
  old=entry['old_literal'].encode();new=entry['new_literal'].encode()
  require(original.count(old)==entry['occurrences']==1,'projection literal count')
  require(original.replace(old,new)==current and current.replace(new,old)==original,'projection is not reversible')
  require(sha(original)==entry['original_sha256'] and sha(current)==entry['projected_sha256'],'projection hashes')
  projected_names.add(entry['path'].split('rectangle/review/',1)[1])
 for name,pin in original_review['files'].items():
  path=(ROOT/'provenance/review'/name) if name in projected_names else (ROOT/'rectangle/review'/name)
  data=path.read_bytes();require(len(data)==pin['bytes'] and sha(data)==pin['sha256'],'original review file binding')
 for binding in read('COPY_BINDINGS.json')['bindings']:
  data=(ROOT/binding['destination']).read_bytes()
  require(sha(data)==binding['destination_sha256'],'copy binding mismatch')
  if binding['projection']=='byte-identical':require(sha(data)==binding['source_sha256'] and len(data)==binding['source_bytes'],'source copy mismatch')

 cand=ROOT/'rectangle/candidate'
 sources=read('rectangle/candidate/SOURCE_PINS.json')
 for item in sources['sources']:
  data=(cand/item['snapshot']).read_bytes()
  require(sha(data)==item['sha256'] and len(data)==item['bytes'],'source snapshot hash')
  require(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['git_blob'],'source Git blob')
 receipt=read('rectangle/candidate/REMOTE_SOURCE_CHECK.json')['result']
 source=(cand/'sources/inherited_SOURCES.json').read_bytes()
 require(receipt['content'].encode()==source,'remote source receipt bytes')
 require(receipt['sha']==hashlib.sha1(b'blob '+str(len(source)).encode()+b'\0'+source).hexdigest(),'remote source receipt Git blob')
 pins=read('rectangle/review/REVIEW_PINS.json')
 require(pins['decision']=='ACCEPT' and pins['candidate_report']['path']=='../candidate/REPORT.md','acceptance reference')
 require(pins['candidate_report']['sha256']==SCIENCE_PINS['rectangle/candidate/REPORT.md'],'reviewed report hash')

 claims=read('rectangle/candidate/CLAIMS.json')
 require(claims['target']==3757 and claims['actual_rank_three_density']['lower_bound']=='16/221' and claims['original_disjoint_cost_optimum']==894166,'target claims')
 require(claims['optimizer_rank_one_only'] is True and claims['optimizer_tile_count']==3757 and claims['optimizer_unordered_sides']==[17,221],'target equality claims')
 require(claims['priority']==42 and claims['parent_status_unchanged'] is True,'owner state changed')

 proposal=read('OWNER_UPDATE_PROPOSAL.json')
 require(proposal['application_enabled'] is False and proposal['stable_id']=='M-RECTANGLE-TILING','proposal must remain inert')
 require(proposal['source_index']['sha256']=='ed49fa87918513fb598085c62d35c7e635ae9041aa7ecc5e4934e7a4284813ee' and proposal['source_index']['record_count']==225,'wrong index preimage')
 before=read(proposal['before_record']);after=read(proposal['proposed_record'])
 allowed={'recorded_current_gate','recorded_pass_stop_condition'}
 require(set(proposal['allowed_fields'])==allowed,'owner field scope')
 require(set(before)==set(after),'owner schema changed')
 for field in before:
  if field in allowed:
   require(sha(before[field].encode())==proposal['field_preimage_sha256'][field],'field preimage mismatch')
   require(after[field]==before[field]+'\n\n'+proposal['append_text'][field],'old gate not preserved exactly')
  else:require(after[field]==before[field],'unallowlisted owner change: '+field)
 require(after['status']=='TO RESEARCH' and after['priority']==42 and after['stable_id']=='M-RECTANGLE-TILING','owner status changed')
 require('N=2873' in before['recorded_current_gate'] and 'N=3757' in proposal['append_text']['recorded_current_gate'],'historical/target bounds')

 forbidden=[b'/workspace/',b'/home/agent/',b'/tmp/',b'codex://',b'dream_notes',b'/action_items.md']
 for name in actual:
  data=(ROOT/name).read_bytes()
  # The verifier lists these forbidden tokens so it can enforce the public boundary.
  if name=='verify_package.py':continue
  require(not any(token in data for token in forbidden),'local/internal locator in public file: '+name)
 return {'status':'PASS','manifest_entries':count,'source_snapshots':len(sources['sources']),'reversible_locator_projections':2,'owner_proposal':'inert, two append-only fields, old values preserved','mathematical_sources':'exact accepted bytes retained'}

def replay():
 with tempfile.TemporaryDirectory(prefix='rectangle3757_verify_') as tmp:
  work=Path(tmp)/'packet';shutil.copytree(ROOT,work)
  outputs=[]
  for folder,script,artifacts in [
   ('rectangle/candidate','check_target.py',['COVERAGE_CERTIFICATE.json','DANGEROUS_SHAPES.json']),
   ('rectangle/review','independent_controls.py',['MINOR_CONTROLS.json','DANGEROUS_SHAPES.json'])]:
   result=subprocess.run([sys.executable,str(work/folder/script)],capture_output=True,text=True,timeout=240)
   require(result.returncode==0,'mathematical replay failed: '+folder+'\n'+result.stdout+'\n'+result.stderr)
   expected=json.loads((ROOT/folder/'RESULTS.json').read_text());got=json.loads((work/folder/'RESULTS.json').read_text())
   expected.pop('elapsed_seconds',None);got.pop('elapsed_seconds',None)
   require(expected==got,'replayed mathematical result changed: '+folder)
   for artifact in artifacts:require((ROOT/folder/artifact).read_bytes()==(work/folder/artifact).read_bytes(),'replayed certificate changed: '+folder+'/'+artifact)
   outputs.append({'checker':folder+'/'+script,'results_equal_except_elapsed':True,'byte_identical_certificates':artifacts})
  return outputs

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--replay',action='store_true');args=parser.parse_args()
 try:
  result=verify()
  if args.replay:result['isolated_mathematical_replays']=replay()
  print(json.dumps(result,indent=2,sort_keys=True))
 except Exception as exc:
  print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
