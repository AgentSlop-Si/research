"""Independent targeted-index derivative checker against separately read native cells.
Usage: python check_index_derivative.py independent_directory publisher_directory
"""
import csv,hashlib,io,json,pathlib,re,sys
root=pathlib.Path(sys.argv[1]);pub=pathlib.Path(sys.argv[2]);stage=pub/'seal_stage/math/finalized/2026-10-15-rebuilt-open-record-index'
load=lambda p:json.loads(p.read_text())
base=load(root/'private/BASELINE_INDEX.json');out=load(stage/'open-record-index.json')
if 'structuredContent' in base:base=json.loads(base['structuredContent']['content'])
assert base==load(pub/'private/baseline_open-record-index.json')
cells={}
for s in load(root/'private/TERMINAL_NATIVE_READBACK.json')['structuredContent']['sheets']:
 if s['properties']['title']!='Research overview':continue
 for g in s['data']:
  for r,line in enumerate(g.get('rowData',[]),g.get('startRow',0)+1):
   for c,cell in enumerate(line.get('values',[]),g.get('startColumn',0)+1):cells[r,c]=cell
val=lambda r,c:cells[r,c].get('userEnteredValue',{}).get('stringValue','')
def prefix(t):
 t=t.partition('Earlier dated history (preserved verbatim):')[0].strip()
 starts=list(re.finditer(r'^\[\d{4}-\d{2}-\d{2}',t,re.M))
 return t[:starts[1].start()].rstrip() if len(starts)>1 else t
def urls(r):
 out=[]
 def add(u):
  if isinstance(u,str) and u.startswith(('http://','https://')) and u not in out:out.append(u)
 for c in (9,10):
  cell=cells[r,c]
  for run in cell.get('textFormatRuns',[]):add(run.get('format',{}).get('link',{}).get('uri'))
  add(cell.get('userEnteredFormat',{}).get('textFormat',{}).get('link',{}).get('uri'))
  add(cell.get('hyperlink'))
 for c in (10,16,17):
  for u in re.findall(r'https?://[^\s<>"\[\]]+',prefix(val(r,c))):add(u.rstrip('.,;:!?)]}'))
 return out
owners={'ALG-036','ALG-042','ALG-052','ALG-048','M-NILPOTENT-FOLD','M-SYMMETRY','F020'}
assert len(out['records'])==len(base['records'])==240
changed=[]
for old,new in zip(base['records'],out['records']):
 assert old.keys()==new.keys();r=new['overview_row'];owner=new['stable_id']
 assert owner==val(r,2) and new['status']==val(r,5)=='TO RESEARCH'
 assert new['priority']==cells[r,12]['userEnteredValue']['numberValue']
 diff={k for k in new if new[k]!=old[k]}
 if owner not in owners:assert not diff
 else:
  assert diff=={'recorded_current_gate','recorded_pass_stop_condition','recorded_source_urls'}
  assert new['recorded_current_gate']==prefix(val(r,16))
  assert new['recorded_pass_stop_condition']==prefix(val(r,17))
  assert new['recorded_source_urls']==urls(r)
  changed.append(owner)
assert set(changed)==owners
native_open=[val(r,2) for r in range(5,332) if val(r,5)=='TO RESEARCH']
assert native_open==[r['stable_id'] for r in out['records']]
assert len(set(native_open))==240
for k in base:
 if k not in {'records','counts','snapshot_read_completed_utc','scope'}:assert out[k]==base[k]
assert out['scope'].startswith(base['scope'])
expected=dict(base['counts']);expected['source_url_count']=sum(len(r['recorded_source_urls']) for r in out['records'])
for col,key in [(16,'historical_action_suffixes_removed'),(17,'historical_condition_suffixes_removed')]:
 n=0
 for p in load(pub/'private/NATIVE_PLAN.json')['plans']:
  if p['sheet']=='Research overview' and p['stable_id'] in owners and p['column_index']+1==col:
   n+='Earlier dated history (preserved verbatim):' not in p['before']
 expected[key]+=n
assert out['counts']==expected
keys=list(base['records'][0])
def encode(rows):
 stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\r\n');writer.writerow(keys)
 for row in rows:writer.writerow([json.dumps(row[k],ensure_ascii=False,separators=(',',':')) if k=='recorded_source_urls' else str(row[k]) for k in keys])
 return stream.getvalue().encode()
assert encode(base['records'])==(pub/'private/baseline_open-record-index.csv').read_bytes()
assert encode(out['records'])==(stage/'open-record-index.csv').read_bytes()
parsed=[]
for r in csv.DictReader(io.StringIO((stage/'open-record-index.csv').read_bytes().decode(),newline='')):
 for k in ['priority','overview_row','recorded_source_urls']:r[k]=json.loads(r[k])
 parsed.append(r)
assert parsed==out['records']
assert (stage/'README.md').read_bytes().endswith((pub/'private/baseline_index_README.md').read_bytes())
print(json.dumps({'verdict':'ACCEPT','changed_record_ids':changed,'changed_fields_only':['recorded_current_gate','recorded_pass_stop_condition','recorded_source_urls'],'unchanged_record_objects':233,'all_240_ids_order_positions_titles_statuses_priorities_preserved':True,'all_current_fields_match_independent_native_read':True,'csv_json_exact_roundtrip':True,'index_readme_old_body_preserved':True,'counts':out['counts'],'files':{f.name:{'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in [stage/'open-record-index.json',stage/'open-record-index.csv',stage/'README.md']}},indent=2))
