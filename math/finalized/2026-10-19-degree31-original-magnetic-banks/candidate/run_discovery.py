from pathlib import Path
import subprocess,json,hashlib,datetime,time,resource
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256((R/p).read_bytes()).hexdigest()
for p in ['FIELD_IRREDUCIBILITY.json','ARITHMETIC_CHECK.json','CONVOLUTION_BOUNDARY_CHECK.json']:assert json.loads((R/p).read_text())['verdict']=='PASS'
scope=json.loads((R/'SEARCH_SCOPE.json').read_text());assert scope['seed']==202610192024 and scope['cap_nonzero_cross_nodes']==100000
receipt={'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'seed':202610192024,'cap_nonzero_cross_nodes':100000,'preflight_hashes':{p:sha(p) for p in ['FIELD_IRREDUCIBILITY.json','ARITHMETIC_CHECK.json','CONVOLUTION_BOUNDARY_CHECK.json','SEARCH_SCOPE.json','SEARCH_SCOPE_AMENDMENT.json','search_degree31.cpp']}}
(R/'DISCOVERY_CHRONOLOGY.json').write_text(json.dumps(receipt,indent=2)+'\n')
start=time.time()
with (R/'NONSTABLE_CANDIDATE.json').open('w') as out,(R/'SEARCH_PROGRESS.log').open('w') as err:
 run=subprocess.run(['./search_degree31','100000'],cwd=R,stdout=out,stderr=err)
usage=resource.getrusage(resource.RUSAGE_CHILDREN)
(R/'SEARCH_RESOURCE.json').write_text(json.dumps({'user_cpu_seconds':usage.ru_utime,'system_cpu_seconds':usage.ru_stime,'peak_rss_KiB':usage.ru_maxrss,'wall_seconds':time.time()-start,'exit_code':run.returncode},indent=2)+'\n')
receipt.update(exit_code=run.returncode,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=time.time()-start,prefix_sha256=sha('PREFIX_LEDGER.jsonl'))
(R/'DISCOVERY_CHRONOLOGY.json').write_text(json.dumps(receipt,indent=2)+'\n')
if run.returncode==0:
 v=json.loads((R/'NONSTABLE_CANDIDATE.json').read_text());f=lambda x:'{'+','.join(map(str,x))+'}'
 (R/'candidate_data.h').write_text('static const int INPUT_Y[D]='+f(v['y'])+';\nstatic const int INPUT_H[8][D]={'+','.join(f(x) for x in v['H'])+'};\n')
 print('FIRST SPLIT',v['trial'],'nodes',v['nonzero_nodes'],'candidates',v['candidates'],flush=True)
else:print('SEARCH STOPPED',run.returncode,flush=True)
