"""Independently authored read-only artifact/register QA; never executes research programs."""
import json, pathlib, hashlib, collections, sys, datetime
BASE=pathlib.Path('research_cycle_0958'); SNAP=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else str(BASE/'integration/final_v1'))
def read(p):return json.loads(pathlib.Path(p).read_text())
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def check(p,h):
 p=pathlib.Path(p)
 return {'path':str(p),'expected_sha256':h,'actual_sha256':sha(p) if p.exists() else None,'match':p.exists() and sha(p)==h}
reg=read(SNAP/'STATUS_REGISTER.json'); payload=read(SNAP/'SHEET_PAYLOAD.json'); queue=read(BASE/'QUEUE.json'); review=read(BASE/'review/final_v2/review_ledger.json')
report={'as_of_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'snapshot':str(SNAP),'snapshot_sha256':sha(SNAP/'STATUS_REGISTER.json'),'payload_sha256':sha(SNAP/'SHEET_PAYLOAD.json'),'supplied_research_programs_executed':False}
report['sources']=[check(s['source'],s['sha256'])|{'id':s['id']} for s in reg['sources']]
report['acceptances']=[check(s['path'],s['sha256']) for s in read(BASE/'review/final_v2/ACCEPTANCE_MANIFEST.json')]
report['manifests']=[]
for rel in ['algebra/final_v1/MANIFEST.json','matrix/final_v1/MANIFEST.json','matrix/quadratic_supplement/MANIFEST.json','algorithms/FREEZE_MANIFEST.json','structured/MANIFEST.json','packing/artifact_hashes.json','intake_audit/MANIFEST.json','review/final_v2/MANIFEST.json']:
 p=BASE/rel; d=read(p); files=d if isinstance(d,list) else d.get('files',d)
 if isinstance(files,dict):files=[{'path':k,'sha256':v} for k,v in files.items()]
 checks=[]
 for f in files:
  fp=pathlib.Path(f['path']); fp=fp if fp.exists() else p.parent/fp
  checks.append(check(fp,f['sha256']))
 report['manifests'].append({'manifest':str(p),'sha256':sha(p),'file_count':len(checks),'failures':[c for c in checks if not c['match']]})
ids=[t['queue_id'] for t in reg['tasks']]; qids=[t['queue_id'] for t in queue['queue']]; vids=[v['id'] for v in reg['view_records']]; sids={s['id'] for s in reg['sources']}; rids={r['id'] for r in reg['independent_review']['rows']}
report['counts']={'tasks':len(ids),'view_rows':len(vids),'view_types':dict(collections.Counter(v['view'] for v in reg['view_records'])),'new_results':len(reg['new_results']),'fusion_rows':len(reg['fusion_list']),'fusion_states':dict(collections.Counter(f['state'] for f in reg['fusion_list'])),'review_decisions':dict(collections.Counter(r['verdict'] for r in reg['independent_review']['rows'])),'task_states':dict(collections.Counter(t['task_state'] for t in reg['tasks']))}
report['coverage']={'missing_original_tasks':sorted(set(qids)-set(ids)),'extra_tasks':sorted(set(ids)-set(qids)),'duplicate_tasks':[k for k,v in collections.Counter(ids).items() if v>1],'duplicate_views':[k for k,v in collections.Counter(vids).items() if v>1],'review_equal_to_v2':reg['independent_review']==review}
report['reference_errors']=[]
for family,idkey,taskkey,sourcekey,reviewkey in [('tasks','queue_id',None,'source_ids','review_ids'),('view_records','id','underlying_task_ids','source_ids','review_ids'),('new_results','id','tasks','sources',None),('fusion_list','id','tasks','sources',None)]:
 for row in reg[family]:
  for typ,key,valid in [('task',taskkey,set(ids)),('source',sourcekey,sids),('review',reviewkey,rids)]:
   if key:
    bad=set(row.get(key,[]))-valid
    if bad:report['reference_errors'].append({'row':row[idkey],'type':typ,'bad':sorted(bad)})
report['sheet_tabs']=[{'name':t['name'],'rows':len(t['rows']),'headers':len(t['headers']),'wrong_width_rows':[i+1 for i,r in enumerate(t['rows']) if len(r)!=len(t['headers'])]} for t in payload['tabs']]
report['snapshot_scope']=reg['scope']
report['summary_pass']=not(any(not x['match'] for x in report['sources']+report['acceptances']) or any(x['failures'] for x in report['manifests']) or report['reference_errors'] or report['coverage']['missing_original_tasks'] or report['coverage']['duplicate_tasks'] or report['coverage']['duplicate_views'] or not report['coverage']['review_equal_to_v2'] or any(x['wrong_width_rows'] for x in report['sheet_tabs']))
out=BASE/'qa'/('STRUCTURAL_QA_'+SNAP.name+'.json');out.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['sources','acceptances']},indent=2))
