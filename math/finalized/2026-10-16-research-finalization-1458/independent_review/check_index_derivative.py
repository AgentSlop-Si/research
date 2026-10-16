"""Self-authored data-only reconstruction of the existing open-index derivative.
Arguments: baseline-remote.json candidate.json before-native.json after-native.json candidate.csv result.json
"""
import sys,json,copy,re,csv,io,hashlib,collections
from pathlib import Path
def load(p):return json.loads(Path(p).read_text())
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def flat(obj):
    out={}
    for s in obj['structuredContent']['sheets']:
        if s['properties']['title']!='Research overview':continue
        for d in s.get('data',[]):
            for r,row in enumerate(d.get('rowData',[]),d.get('startRow',0)+1):
                for c,v in enumerate(row.get('values',[]),d.get('startColumn',0)+1):out[r,c]=v
    return out
def current(t):
    t=t.partition('Earlier dated history (preserved verbatim):')[0].strip()
    headings=list(re.finditer(r'^\[\d{4}-\d{2}-\d{2}',t,re.M))
    return t[:headings[1].start()].rstrip() if len(headings)>1 else t
bfile,nfile,bnative,anative,cfile,ofile=sys.argv[1:]
remote=load(bfile)['structuredContent'];base=json.loads(remote['content']);new=load(nfile)
before,after=flat(load(bnative)),flat(load(anative))
def text(r,c):return after[r,c].get('userEnteredValue',{}).get('stringValue','')
def urls(r):
    result=[]
    def add(u):
        if isinstance(u,str) and u.startswith(('http://','https://')) and u not in result:result.append(u)
    for c in (9,10):
        cell=after[r,c]
        for run in cell.get('textFormatRuns',[]):add(run.get('format',{}).get('link',{}).get('uri'))
        add(cell.get('userEnteredFormat',{}).get('textFormat',{}).get('link',{}).get('uri'))
        add(cell.get('hyperlink'))
    for c in (10,16,17):
        for u in re.findall(r'https?://[^\s<>"\[\]]+',current(text(r,c))):add(u.rstrip('.,;:!?)]}'))
    return result
removed={'ALG-050','STRUCTURED-RESIDUAL-EXECUTOR-20261012'}
updated={'ALG-034','ALG-079'};records=[];untouched=0
for old in base['records']:
    record=copy.deepcopy(old);r=record['overview_row'];owner=record['stable_id']
    assert text(r,2)==owner
    assert after[r,12]['userEnteredValue']['numberValue']==record['priority']
    if owner in removed:
        assert text(r,5)=='CLOSED';continue
    assert text(r,5)==record['status']=='TO RESEARCH'
    if owner in updated:
        record['recorded_current_gate']=current(text(r,16))
        record['recorded_pass_stop_condition']=current(text(r,17))
        record['recorded_source_urls']=urls(r)
    else:untouched+=1
    records.append(record)
assert records==new['records'] and untouched==238 and len(records)==240
assert {r['stable_id'] for r in base['records']}-{r['stable_id'] for r in records}==removed
for k in ('schema_version','artifact_kind','source','selection','extraction'):assert new[k]==base[k]
assert new['scope'].startswith(base['scope'])
counts=copy.deepcopy(base['counts'])
counts.update(open_records=240,closed_records=87,unique_open_stable_ids=240,nonempty_recorded_current_gates=240,nonempty_recorded_pass_stop_conditions=240,numeric_priorities=240,records_with_recorded_source_urls=240,source_url_count=sum(len(r['recorded_source_urls']) for r in records),min_priority=min(r['priority'] for r in records),max_priority=max(r['priority'] for r in records))
for col,name in [(16,'historical_action_suffixes_removed'),(17,'historical_condition_suffixes_removed')]:
    delta=0
    for r in (17,30,62,300):
        was='Earlier dated history (preserved verbatim):' in before[r,col].get('userEnteredValue',{}).get('stringValue','')
        if text(r,2) in removed:delta-=was
        else:delta+=not was
    counts[name]+=delta
assert new['counts']==counts
stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\r\n');keys=list(records[0]);writer.writerow(keys)
for row in records:writer.writerow([json.dumps(row[k],ensure_ascii=False,separators=(',',':')) if isinstance(row[k],list) else str(row[k]) for k in keys])
assert stream.getvalue().encode()==Path(cfile).read_bytes()
parsed=list(csv.DictReader(io.StringIO(Path(cfile).read_text(),newline='')))
for row in parsed:
    for k in ('priority','overview_row','recorded_source_urls'):row[k]=json.loads(row[k])
assert parsed==records
result={'decision':'PASS_INDEPENDENT_INDEX_RECONSTRUCTION','baseline_index_sha256':hashlib.sha256(remote['content'].encode()).hexdigest(),'candidate_json_sha256':sha(nfile),'candidate_csv_sha256':sha(cfile),'removed_only':sorted(removed),'updated_only':sorted(updated),'updated_fields_only':['recorded_current_gate','recorded_pass_stop_condition','recorded_source_urls'],'untouched_retained_records':untouched,'retained_records':len(records),'source_urls':counts['source_url_count'],'historical_suffix_counts':[counts['historical_action_suffixes_removed'],counts['historical_condition_suffixes_removed']],'csv_canonical_bytes_and_roundtrip':True,'schema_source_selection_extraction_unchanged':True,'new_ids':[],'source_program_execution':False}
Path(ofile).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
