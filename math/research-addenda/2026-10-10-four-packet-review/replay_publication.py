#!/usr/bin/env python3
"""Replay packaged reviewer-authored mathematics in a disposable local copy.
The source packet programs are never imported or executed. No network access.
Historical archive integrity and omitted baseline provenance are not replayed.
"""
from pathlib import Path
import argparse,concurrent.futures,hashlib,json,os,platform,shutil,subprocess,sys,time
P=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True,help='New local directory outside the sealed payload');args=ap.parse_args()
O=Path(args.output).resolve();assert P!=O and P not in O.parents,'Output must be outside sealed payload'
O.mkdir(parents=True,exist_ok=False);W=O/'work';W.mkdir()
for name in ['phase44','f11_v39','stable_arc','n256_full_model','comparisons']:
 shutil.copytree(P/name,W/name)
E=os.environ.copy();E['OPENBLAS_NUM_THREADS']='1';E['OMP_NUM_THREADS']='1'

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(group,args,log):
 start=time.monotonic();folder=W/group
 with (O/log).open('w') as f:
  result=subprocess.run(args,cwd=folder,env=E,stdout=f,stderr=subprocess.STDOUT)
 record={'group':group,'command':args,'exit_code':result.returncode,'elapsed_seconds':round(time.monotonic()-start,3),'log':log,'log_sha256':digest(O/log)}
 if result.returncode:raise RuntimeError(json.dumps(record))
 return record

def read(p):return json.loads(p.read_text())
def equal(group,name,drop=(),nested_scope=False):
 old=read(P/group/name);new=read(W/group/name)
 for k in drop:old.pop(k,None);new.pop(k,None)
 if nested_scope:
  old['scope_checks']={'difficult_block':old['scope_checks']['difficult_block']}
  new['scope_checks']={'difficult_block':new['scope_checks']['difficult_block']}
  for v in old.values():
   if isinstance(v,dict):v.pop('SECONDS',None)
  for v in new.values():
   if isinstance(v,dict):v.pop('SECONDS',None)
 assert old==new,(group,name,'scientific results differ')
 return {'group':group,'result':name,'recorded_scientific_result_match':True,'replay_sha256':digest(W/group/name),'excluded_nonscientific_fields':list(drop),'historical_scope_fields_excluded':nested_scope}

def phase44():
 g='phase44';runs=[];matches=[]
 for dps,radius,name in [(70,'1e-20','fresh_interval_results.json'),(55,'1e-20','fresh_interval_55dps_results.json'),(80,'1e-21','fresh_interval_80dps_results.json')]:
  runs.append(run(g,[sys.executable,'fresh_interval_check.py','--dps',str(dps),'--radius',radius,'--output',name],f'phase44_{dps}.log'))
  matches.append(equal(g,name,drop=('seconds',)))
 runs.append(run(g,[sys.executable,'fresh_controls.py'],'phase44_controls.log'))
 matches.append(equal(g,'fresh_controls_results.json',drop=('archive_manifest_all_match','archive_manifest_entries','standalone_report_equals_bundled_theorem','publication_archive_audit')))
 return runs,matches

def f11():
 g='f11_v39';runs=[run(g,[sys.executable,'run_fresh_review.py'],'f11_replay.log')]
 return runs,[equal(g,'independent_replay_results.json',nested_scope=True)]

def stable():
 g='stable_arc';runs=[run(g,[sys.executable,'fresh_controls.py'],'stable_arc.log')]
 return runs,[equal(g,'fresh_controls.json')]

def n256():
 g='n256_full_model';runs=[run(g,[sys.executable,'fresh_checker.py'],'n256.log')]
 return runs,[equal(g,'fresh_check_results.json',drop=('source_manifest_entries_verified','publication_inert_files_verified','elapsed_seconds'))]

def exponents():
 g='comparisons/phase44_priority';runs=[run(g,[sys.executable,'check_comparison_exponents.py'],'phase44_comparison.log')]
 return runs,[equal(g,'EXACT_COMPARISON_CHECKS.json')]

input_checks=[]
for group in ['phase44','f11_v39','n256_full_model']:
 for name,h in read(P/group/'PUBLICATION_INPUT_HASHES.json').items():
  assert digest(P/group/name)==h
  input_checks.append({'group':group,'path':name,'sha256':h})
commands=[];comparisons=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
 futures=[pool.submit(f) for f in [phase44,f11,stable,n256,exponents]]
 for future in concurrent.futures.as_completed(futures):
  runs,matches=future.result();commands.extend(runs);comparisons.extend(matches)
result={'status':'passed packaged mathematical replay','historical_archives_replayed':False,'complete_historical_corpus_replayed':False,'uploaded_packet_programs_executed':False,'source':'publication-adapted fresh reviewers plus unchanged fresh checkers','environment':{'python':platform.python_version(),'numpy':__import__('numpy').__version__,'mpmath':__import__('mpmath').__version__,'sympy':__import__('sympy').__version__,'compiler':subprocess.check_output(['g++','--version'],text=True).splitlines()[0]},'commands':sorted(commands,key=lambda x:(x['group'],x['log'])),'results':sorted(comparisons,key=lambda x:(x['group'],x['result'])),'input_hashes_verified':input_checks}
(O/'REPLAY_VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'command_count':len(commands),'compared_outputs':len(comparisons),'summary':'REPLAY_VERIFICATION.json'},indent=2))
